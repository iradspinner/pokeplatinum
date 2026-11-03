"""Goal 3's fight list, for Ian to prune before any labelling starts.

Goal 3 of the trainer scorer (docs/oxide/trainer-scoring-handoff.md, "The
order of work") reads every major boss, rival, named Galactic fight and Ace
Trainer. Each fight needs labelled positions of its own, so every row costs
machine time. This lists one row per fight with the flags that could drop
it, and proposes a drop only where a flag says so.

    cd <worktree> && PYTHONPATH=. python3 /home/ian/.claude/jobs/d83f782f/tmp/goal3_fights.py

It reads the tree and writes nothing but the Markdown file named in OUT.
"""
import collections
import glob
import json
import os
import re
import sys

from tools.oxide.balance import data, plscore, required, splits

OUT = "/home/ian/.claude/jobs/d83f782f/tmp/goal3-fights.md"
ROOT = data.ROOT
LEAGUE_CAP = data.fights()["caps"]["League"]
SPLIT_ORDER = splits.SPLITS + [None]

# Classes that make a trainer a boss, a rival or a named Galactic fight.
BOSS_CLASS = ("TRAINER_CLASS_LEADER_", "TRAINER_CLASS_ELITE_FOUR_", "TRAINER_CLASS_CHAMPION_")
GALACTIC_CLASS = ("TRAINER_CLASS_COMMANDER_", "TRAINER_CLASS_GALACTIC_BOSS")
RIVAL_CLASS = "TRAINER_CLASS_RIVAL"
PLAYER_CLASS = ("TRAINER_CLASS_PLAYER_MALE", "TRAINER_CLASS_PLAYER_FEMALE")   # Lucas and Dawn
STARTERS = ("_piplup", "_turtwig", "_chimchar")

# Areas the docs call optional, by the location name the map carries. The
# Battle Zone is optional before the League (balance plan, "the zone is
# optional"; battle-zone-plan.md), its Fight Area tag fight excepted, which
# fights.json makes a story fight. Iron Island is an optional gauntlet with
# the Riolu egg at its end (balance plan, the gauntlet table).
OPTIONAL_LOCATIONS = {
    "Route 225": "the Battle Zone, optional", "Route 226": "the Battle Zone, optional",
    "Route 227": "the Battle Zone, optional", "Route 228": "the Battle Zone, optional",
    "Route 229": "the Battle Zone, optional", "Route 230": "the Battle Zone, optional",
    "Stark Mountain": "the Battle Zone, optional", "Survival Area": "the Battle Zone, optional",
    "Resort Area": "the Battle Zone, optional",
    "Iron Island": "Iron Island, an optional gauntlet",
}

# What required.placements' "how" (the reach model) says about a
# trainer being on the main path.
HOW_WORDS = {
    "required": "on the path (reach model: required)",
    "avoidable": "optional (reach model: avoidable)",
    "off the story path": "optional (off the story path)",
    "behind a field move": "optional (behind a field move)",
    "gym with moving parts": "path unknown (gym not modelled)",
    "multi-floor dungeon": "path unknown (dungeon not modelled)",
    "not on a crossing": "path unknown (scripted, not on a crossing)",
}


def trainer_class(t):
    """The trainer's class constant, from its data file."""
    with open(os.path.join(ROOT, "res", "trainers", "data", t["stem"] + ".json"), encoding="utf-8") as f:
        return json.load(f).get("class", "")


def ace(t):
    return max(m["level"] for m in t["party"])


def trainer_split(tr):
    """The scorer's own split for a trainer, as plgen.trainer_split and
    plscore.prepare give it (copied so this needs no network modules)."""
    if tr in plscore.SPLIT_OVERRIDE:
        return plscore.SPLIT_OVERRIDE[tr]
    placed = required.placements()
    if tr in placed:
        return placed[tr]["split"]
    return splits.trainer_split(tr)


def maps_of(tr):
    """The maps that battle a trainer, else those whose scripts name it."""
    return sorted(splits.trainer_maps().get(tr, ()) or splits.trainer_mentions().get(tr, ()))


def partner_maps():
    """{map header: partner trainer id} for maps whose scripts give the
    player a battle partner. With the partner flag set, every trainer
    battle the field starts is a tag battle with the partner beside the
    player (ScrCmd_StartTrainerBattle passes the partner on)."""
    by_script = {}
    for path in glob.glob(os.path.join(ROOT, "res", "field", "scripts", "*.s")):
        text = data.read_script(path)
        m = re.search(r"VAR_PARTNER_TRAINER_ID,\s*(\w+)", text)
        if m and "SetHasPartner" in text:
            tok = m.group(1)
            tr = int(tok) if tok.isdigit() else required.trainer_ids().get("TRAINER_" + tok.replace("TRAINER_", ""))
            by_script[os.path.basename(path)[:-2]] = tr
    out = {}
    for header, fields in splits.headers().items():
        if fields.get("scriptsArchiveID") in by_script:
            out[header] = by_script[fields["scriptsArchiveID"]]
    return out


def sight_pairs():
    """{tr_id: {other tr_id: (shared tiles, own tiles)}} for trainers on one
    map whose sight lines share a tile. Two undefeated trainers that both
    see the player start one double battle against both
    (FieldSystem_CheckForTrainersWantingBattle), if the player has two
    Pokemon able to fight. Sight is read as required.Field reads it."""
    out = collections.defaultdict(dict)
    ids = required.trainer_ids()
    for header in splits.headers():
        try:
            objs = [o for o in world_events(header) if str(o.get("script", "")).startswith("TRAINER_")]
        except FileNotFoundError:
            continue
        if len(objs) < 2:
            continue
        split = splits.map_split(header)[0]
        field_split = split if split in required.SPLITS else "League"
        try:
            field = required.Field(header, field_split)
        except Exception:
            continue
        seen = {}
        for t in field.trainers:
            tr = ids.get(t["script"])
            if tr is not None:
                seen[tr] = field.sight(t)
        for a in seen:
            for b in seen:
                if a != b and seen[a] & seen[b]:
                    out[a][b] = (len(seen[a] & seen[b]), len(seen[a]))
    return out


def world_events(header):
    from tools.oxide.balance import world
    return world.events(header)["object_events"]


def location_flags(maps):
    """Post-game and optional readings from the maps alone. A fight is
    post-game only when every map that battles it is: Lucas and Dawn 3's
    slots are also re-fought at the Battleground, which does not move the
    Victory Road fight."""
    post_maps = [h for h in maps if splits.map_split(h)[0] == "Post"]
    post = [f"{h.lower()} is post-game" for h in post_maps] if maps and len(post_maps) == len(maps) else []
    optional = [OPTIONAL_LOCATIONS[splits.location_name(h)] for h in maps
                if splits.location_name(h) in OPTIONAL_LOCATIONS]
    return post, optional


# The order a row's drop reasons are listed and counted in: the first one
# is the most telling, and the counts use it.
REASON_ORDER = ["rematch", "post-game", "double", "unreachable", "not placed", "does not count"]


# The kinds of row, in the order the summary lists them.
KINDS = ["gym leaders, Elite Four and Champion", "Barry", "Lucas and Dawn",
         "named Galactic fights", "Ace Trainers", "rematches and re-fights"]


def story_kind(f, cls):
    """Which kind a fights.json fight is, from its first trainer's class.
    Somnu and Moira are officers in grunt slots, so a grunt class counts as
    Galactic; Flint and Volkner's tag fight counts with the leaders."""
    c = cls[f["tr_ids"][0]]
    if c.startswith(GALACTIC_CLASS) or "GRUNT" in c:
        return "named Galactic fights"
    if c == RIVAL_CLASS:
        return "Barry"
    if c in PLAYER_CLASS:
        return "Lucas and Dawn"
    return "gym leaders, Elite Four and Champion"


class Row:
    def __init__(self, order, name, ids, split, maps, kind):
        self.order, self.name, self.ids, self.split, self.maps = order, name, ids, split, maps
        self.kind = kind
        self.flags = []         # what the data says, in words
        self.drop = []          # the flags that propose a drop

    def flag(self, text, drop=None):
        if text not in self.flags:
            self.flags.append(text)
        if drop and drop not in self.drop:
            self.drop.append(drop)
            self.drop.sort(key=REASON_ORDER.index)


def main():
    ox = data.oxide_trainers()
    spec = data.fights()
    story = spec["fights"]
    story_ids = {i for f in story for i in f["tr_ids"]}
    partner_ids = {i for f in story for i in f["partner_ids"]}
    placed = required.placements()
    partners = partner_maps()
    pairs = sight_pairs()
    cls = {tr: trainer_class(t) for tr, t in ox.items()}
    rows, left_out = [], []

    def common_flags(row, trs):
        """Flags read from the trainers themselves and their maps."""
        post, optional = location_flags(row.maps)
        for p in sorted(set(post)):
            row.flag(p, "post-game")
        top = max(ace(ox[t]) for t in trs)
        if top > LEAGUE_CAP:
            row.flag(f"ace {top}, above the League cap of {LEAGUE_CAP}", "post-game")
        if any(ox[t]["battle_type"] == "Doubles" for t in trs):
            row.flag("double battle (its data's flag)", "double")
        for h in row.maps:
            if h in partners:
                p = ox.get(partners[h], {}).get("name", partners[h])
                row.flag(f"tag battle beside {p} ({h}'s partner)", "double")
        for o in sorted(set(optional)):
            row.flag(o)
        if not row.maps:
            row.flag("no map battles it", "unreachable")
        if row.split is None:
            row.flag("no split", "not placed")

    # 1. The story fights, as fights.json lists them, in play order.
    for i, f in enumerate(story):
        maps = sorted({h for t in f["tr_ids"] for h in maps_of(t)})
        row = Row((0, i), f["label"], f["tr_ids"], f["split"], maps, story_kind(f, cls))
        common_flags(row, f["tr_ids"])
        if f.get("tag"):
            row.flag("double against two trainers (fights.json: tag)", "double")
        if f.get("partner_ids"):
            row.flag("Barry beside the player")
        if f.get("trick_room"):
            row.flag("whole fight under Trick Room")
        if f["key"] in splits.STORY_REVISITS:
            row.flag("map first reached earlier; fought on a return visit")
        if f["key"] == "barry_1":
            row.flag("Ian ruled it does not count for deaths or a wipe (2026-10-02)", "does not count")
        if f["key"] == "lucas_dawn_1":
            row.flag("dropped from goal 2 as trivial (Ian, 2026-10-02)")
        if f["key"] == "lucas_dawn_3":
            row.flag("the same six slots are fought again at the Battleground after the League")
        rows.append(row)

    # Stark Mountain room 1's script starts Mars's battle and then
    # Jupiter's with only messages and movement between, so the second is
    # fought on what the first left (read from the script by hand).
    back_to_back = {926: "Jupiter (927) follows straight after, no heal between",
                    927: "fought straight after Mars (926), no heal between"}

    # 2. Other boss, rival, Lucas and Dawn, and named Galactic trainers.
    groups = collections.OrderedDict()
    for tr, t in sorted(ox.items()):
        if tr in story_ids:
            continue
        c = cls[tr]
        named_officer = t["name"].startswith("Galactic Officer")
        if not (c.startswith(BOSS_CLASS + GALACTIC_CLASS) or c in (RIVAL_CLASS,) + PLAYER_CLASS or named_officer):
            continue
        if tr in partner_ids:
            left_out.append((t["name"], [tr], "a tag fight's partner beside the player (fights.json partners)"))
            continue
        if c in PLAYER_CLASS and t["stem"].startswith(("lucas_", "dawn_")):
            left_out.append((t["name"], [tr], "a tag partner beside the player against two grunts"))
            continue
        # A rival's three starter variants are one fight.
        stem = t["stem"]
        for s in STARTERS:
            if stem.endswith(s):
                stem = stem[:-len(s)]
        groups.setdefault(stem, []).append(tr)
    for stem, trs in groups.items():
        t = ox[trs[0]]
        c = cls[trs[0]]
        order = 1 if (c.startswith(GALACTIC_CLASS) or t["name"].startswith("Galactic Officer")) else 3
        maps = sorted({h for tr in trs for h in maps_of(tr)})
        split = trainer_split(trs[0])
        name = f"{t['name']} ({stem})"
        if order == 1:
            kind = "named Galactic fights"
        elif "rematch" in stem or ("survival_area" in stem and "unused" not in stem):
            kind = "rematches and re-fights"
        else:
            kind = "Barry" if c == RIVAL_CLASS else "gym leaders, Elite Four and Champion"
        row = Row((order, SPLIT_ORDER.index(split), trs[0]), name, trs, split, maps, kind)
        common_flags(row, trs)
        if "rematch" in stem:
            row.flag("rematch team", "rematch")
        if c == RIVAL_CLASS and maps and all(splits.map_split(h)[0] == "Post" for h in maps):
            row.flag("a Battleground re-fight of Barry", "rematch")
        if "unused" in stem:
            row.flag("an unused slot, by its name")
        if trs[0] in back_to_back:
            row.flag(back_to_back[trs[0]])
        p = placed.get(trs[0])
        if p:
            row.flag(HOW_WORDS.get(p["how"], p["how"]))
        rows.append(row)

    # 3. Ace Trainers: every trainer named or classed Ace Trainer. Two Ace
    # Trainers met only as a tag battle are one row (a double against two
    # trainers is one fight, Ian, 2026-09-28).
    aces = [tr for tr, t in sorted(ox.items())
            if "ACE_TRAINER" in cls[tr] or t["name"].startswith("Ace Trainer")]
    done = set()
    for tr in aces:
        if tr in done:
            continue
        t = ox[tr]
        maps = maps_of(tr)
        mates = [o for o in pairs.get(tr, {}) if o in aces and any(h in partners for h in maps)]
        trs = [tr] + mates
        done.update(trs)
        split = trainer_split(tr)
        name = " and ".join(ox[x]["name"] if i == 0 else ox[x]["name"].replace("Ace Trainer ", "")
                            for i, x in enumerate(trs))
        row = Row((2, SPLIT_ORDER.index(split), tr), f"{name} (ace {max(ace(ox[x]) for x in trs)})",
                  trs, split, sorted({h for x in trs for h in maps_of(x)}), "Ace Trainers")
        common_flags(row, trs)
        if "rematch" in t["stem"]:
            row.flag("Vs. Seeker rematch team", "rematch")
        for x in trs:
            for o, (shared, own) in sorted(pairs.get(x, {}).items()):
                if o in trs:
                    continue
                whole = "every tile it sees" if shared == own else f"{shared} of its {own} sight tiles"
                row.flag(f"sight crosses {ox[o]['name']} ({o}) on {whole}: a double against both "
                         "when both see the player, a single when talked to from outside both lines")
        if len(trs) > 1:
            row.flag("sight lines cross: met together as one tag battle")
        p = placed.get(tr)
        if p:
            row.flag(HOW_WORDS.get(p["how"], p["how"]))
            if p["late"]:
                row.flag("placed late: its ace is over its map's split cap")
        rows.append(row)

    # Ace Trainer slots data.oxide_trainers() leaves out (unused dummy_ files).
    for path in sorted(glob.glob(os.path.join(ROOT, "res", "trainers", "data", "dummy_*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        stem = os.path.basename(path)[:-5]
        if "ACE_TRAINER" in d.get("class", "") and not any(t["stem"] == stem for t in ox.values()):
            left_out.append((f"Ace Trainer {d.get('name', '?')} ({stem})", [],
                             "an unused dummy_ slot no map battles, which data.oxide_trainers() skips"))

    rows.sort(key=lambda r: r.order)

    # The brief's check: every fights.json fight and every Ace Trainer
    # data.oxide_trainers() knows has a row.
    listed = {i for r in rows for i in r.ids}
    missing = [f["key"] for f in story if not set(f["tr_ids"]) <= listed]
    missing += [tr for tr in aces if tr not in listed]
    if missing:
        raise SystemExit(f"left out without a row: {missing}")
    write(rows, left_out)


def cell(items):
    return "; ".join(items) if items else ""


def short_map(h):
    return h.lower().replace("_", " ")


def write(rows, left_out):
    kept = [r for r in rows if not r.drop]
    dropped = [r for r in rows if r.drop]
    by_reason = collections.Counter(r.drop[0] for r in dropped)
    lines = []
    lines.append("# Goal 3's fights, for pruning")
    lines.append("")
    lines.append(INTRO.strip())
    lines.append("")
    lines.append(f"Rows: {len(rows)}. Kept: {len(kept)}. Proposed drops: {len(dropped)} "
                 f"({', '.join(f'{n} {r}' for r, n in by_reason.most_common())}; a row with "
                 "several reasons is counted under its first).")
    lines.append("")
    lines.append("Rows by kind:")
    lines.append("")
    lines.append("| kind | kept | dropped |")
    lines.append("|---|---|---|")
    for kind in KINDS:
        k = sum(1 for r in kept if r.kind == kind)
        d = sum(1 for r in dropped if r.kind == kind)
        lines.append(f"| {kind} | {k} | {d} |")
    lines.append("")
    lines.append("| fight | ids | split | maps | flags | proposed | reason |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append("| " + " | ".join([
            r.name, ", ".join(str(i) for i in r.ids), r.split or "none",
            ", ".join(short_map(h) for h in r.maps) or "none",
            cell(r.flags), "drop" if r.drop else "keep", cell(r.drop)]) + " |")
    lines.append("")
    lines.append("Left out of the table, each with why:")
    lines.append("")
    for name, ids, why in left_out:
        lines.append(f"- {name}{' (' + ', '.join(map(str, ids)) + ')' if ids else ''}: {why}.")
    lines.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{OUT}: {len(rows)} rows, {len(kept)} kept, {len(dropped)} proposed drops {dict(by_reason)}")


INTRO = """
One row per fight goal 3 could label: the 33 story fights of `fights.json`,
every other trainer of a leader, Elite Four, Champion, rival, commander or
Galactic boss class, every Galactic Officer, and every trainer named or
classed Ace Trainer. A rival's three starter teams and Lucas and Dawn's six
slots are one row; two Ace Trainers met only together are one row, since a
double against two trainers is one fight (Ian, 2026-09-28). The split is
`fights.json`'s for a story fight and the scorer's own rule for the rest
(`plscore.SPLIT_OVERRIDE`, then `required.placements`, then
`splits.trainer_split`). Post-game means every map that battles it is in
the Post split (Route 224, Victory Road's back room, the Battleground) or
its ace is above the League cap of 78. Rematch means a team whose file is
named a rematch, or Barry's Battleground teams. Double means the trainer's
own double flag, a tag fight in `fights.json`, or a map whose script gives
the player a partner (Riley on Iron Island B2F, Buck in Stark Mountain's
second room, Marley in Victory Road's back room), where the engine makes
every trainer battle a tag battle; the planner plays one Pokemon a side and
`pdoubles` is a separate first-version search, so none of these can be
labelled yet. Unreachable means no map battles it; not placed means it has
no split. Optional comes from the reach model behind `required.placements` and
from the docs, which call the Battle Zone and Iron Island optional; gyms
and dungeons are not modelled, so their trainers read "path unknown".

Uncertain. The three tag story fights (Somnu and Moira, Mars and Jupiter at
Spear Pillar, Flint and Volkner) are major bosses proposed for a drop only
because the planner cannot read doubles; covering them means doubles
support first. Two Ace pairs face each other with no partner: Dennis and
Maya on Route 215 (both on the path) and Felix and Dana on Route 229. Seen
together they are one double, but each can be fought alone by talking to it
from outside both sight lines, so they are kept as singles. Barry 1 is
proposed for a drop on Ian's ruling that it does not count; Lucas and Dawn
1 is kept, though goal 2 dropped it as trivial. The eight officer rows
(Somnu, Moira, Hesperid and Argo, twice each) and Mars and Jupiter at
Stark Mountain are probably not in the Overseer's count of about 12
Galactic fights; they are kept as named Galactic fights. The rematches'
post-game reading comes from their levels (82 to 90), not from their
scripts' gates. Goal 3's wording does not name the Frontier Brains (optional
bosses since 2026-09-27, still drafts) or the partners' own fights (Cheryl,
Riley, Marley, Buck, Mira), so they have no rows.
"""

if __name__ == "__main__":
    sys.exit(main())
