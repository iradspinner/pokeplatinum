"""Double battles against two trainers at once (Ian, 2026-09-28): each pair
is one fight against both teams, not two singles.

    PYTHONPATH=. python3 -m tools.oxide.balance.pairs      # the list

It writes no game data. `pairs()` is the one list, which the OxiDex's
Trainers tab reads: each pair's stable key, its two trainers, how it is
fought, whether the player has a partner, its maps and its split. Three
kinds, from the game's own rules:

- eye contact: two trainers on one map who can both see the player at
  once, which the game turns into one double battle when the player has
  two Pokemon able to fight (src/trainer_encounter.c,
  FieldSystem_CheckForTrainersWantingBattle). A trainer sees the player
  only in a straight line along its facing, within its sight range (its
  map object's first data value), and nothing blocks the view, so a pair
  is two trainers whose sight lines share a tile no object stands on. A
  tile may still be a wall the player cannot reach; the count of shared
  tiles, and whether each can also see a tile the other cannot, say how
  likely the double is;
- scripted: a script starts one battle against two trainers
  (StartTrainerBattle with two opponents), or a tag battle beside a
  partner (StartTagBattle);
- one trainer's double: a trainer whose own data is a double battle,
  whose second object follows it (MOVEMENT_TYPE_FOLLOW_PARTNER_TRAINER).
  It is one party already, listed so the Trainers tab can show it the
  same way.
"""
import argparse
import collections
import json
import os
import re
import sys

from . import data, splits

SIGHTED = {"TRAINER_TYPE_NORMAL", "TRAINER_TYPE_VIEW_ALL_DIRECTIONS", "TRAINER_TYPE_FACE_SIDES",
           "TRAINER_TYPE_FACE_COUNTERCLOCKWISE", "TRAINER_TYPE_FACE_CLOCKWISE",
           "TRAINER_TYPE_SPIN_COUNTERCLOCKWISE", "TRAINER_TYPE_SPIN_CLOCKWISE"}
STEP = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
INITIAL = {0: "NORTH", 1: "SOUTH", 2: "WEST", 3: "EAST"}
_SETVAR = re.compile(r"^\s*SetVar(?:FromValue)?\s+(?:VAR_0x8004|32772),\s*(\w+)", re.M)


def facings(obj):
    """(the directions the trainer can face, whether it moves). A fixed
    look names its directions; one that turns, wanders or walks may face
    any way, and a walker is placed at its starting tile here."""
    mt = obj.get("movement_type") or ""
    if obj.get("trainer_type") != "TRAINER_TYPE_NORMAL" or not mt.startswith("MOVEMENT_TYPE_LOOK_") \
            or mt == "MOVEMENT_TYPE_LOOK_AROUND":
        moves = "WALK" in mt or "WANDER" in mt
        if mt == "MOVEMENT_TYPE_WANDER_NORTH_AND_SOUTH":
            return ("NORTH", "SOUTH"), True
        if mt == "MOVEMENT_TYPE_WALK_BACK_AND_FORTH":
            first = INITIAL.get(obj.get("initial_dir"), "SOUTH")
            back = {"NORTH": "SOUTH", "SOUTH": "NORTH", "WEST": "EAST", "EAST": "WEST"}[first]
            return (first, back), True
        return tuple(STEP), moves
    return tuple(d for d in STEP if d in mt.replace("MOVEMENT_TYPE_LOOK_", "").split("_")), False


def sight(obj):
    """{tile the trainer sees the player on}."""
    rng = (obj.get("data") or [0])[0] or 0
    x, z = obj["x"], obj["z"]
    dirs, _moves = facings(obj)
    return {(x + dx * d, z + dz * d) for dx, dz in (STEP[n] for n in dirs) for d in range(1, rng + 1)}


def _stem(const):
    return const.replace("TRAINER_", "").lower()


def _events(header):
    events = splits.headers()[header].get("eventsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json") if events else None
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("object_events", [])


def _doubles_flagged():
    return {t["constant"] for t in data.oxide_trainers().values() if t.get("battle_type") == "Doubles"}


def eye_contact():
    """{(stem, stem): {"maps": set, "shared": tiles, "solo": bool, "moves": bool}}."""
    flagged = _doubles_flagged()
    out = {}
    seen_files = set()
    for header in sorted(splits.headers()):
        events = splits.headers()[header].get("eventsArchiveID")
        objs = _events(header)
        trainers = [o for o in objs if str(o.get("script", "")).startswith("TRAINER_")
                    and o.get("trainer_type") in SIGHTED
                    and o.get("movement_type") != "MOVEMENT_TYPE_FOLLOW_PARTNER_TRAINER"
                    and o["script"] not in flagged]
        taken = {(o["x"], o["z"]) for o in objs}
        views = [(o, sight(o) - taken) for o in trainers]
        for i, (a, va) in enumerate(views):
            for b, vb in views[i + 1:]:
                if a["script"] == b["script"]:
                    continue
                shared = va & vb
                if not shared:
                    continue
                key = tuple(sorted((_stem(a["script"]), _stem(b["script"]))))
                rec = out.setdefault(key, {"maps": set(), "shared": 0, "solo": True, "moves": False})
                rec["maps"].add(header)
                if events not in seen_files:
                    rec["shared"] += len(shared)
                rec["solo"] = rec["solo"] and bool(va - vb) and bool(vb - va)
                rec["moves"] = rec["moves"] or facings(a)[1] or facings(b)[1]
        seen_files.add(events)
    return out


def _token_ids(token, text):
    """Trainer ids a battle operand can be: a constant or number, or, for
    VAR_0x8004, every value a script in the file sets into it."""
    tid = splits._trainer_id(token)
    if tid is not None and tid < 0x4000:
        return [tid]
    if token in ("32772", "VAR_0x8004"):
        return [t for t in (splits._trainer_id(v) for v in _SETVAR.findall(text)) if t is not None and t < 0x4000]
    return []


_PARTNER_VAR = re.compile(r"^\s*SetVar(?:FromValue)?\s+VAR_PARTNER_TRAINER_ID,\s*(\w+)", re.M)
# Stems of the trainers that fight beside the player, as the scores name
# them (metrics.PARTNER_STEMS), and the rival's variants.
PARTNER_PREFIXES = ("cheryl", "mira", "riley", "marley", "buck", "lucas", "dawn", "rival")


def _script_text(header):
    scripts = splits.headers()[header].get("scriptsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "scripts", f"{scripts}.s") if scripts else None
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def partner_maps():
    """{map header: [partner stem]}: the maps whose scripts set a trainer to
    follow the player and fight beside it (VAR_PARTNER_TRAINER_ID, then
    SetHasPartner): Cheryl in Eterna Forest, Mira in Wayward Cave, Riley on
    Iron Island, Buck on Stark Mountain, Marley on Victory Road. Every
    trainer battle there, a pair's included, is fought beside the partner."""
    ox = data.oxide_trainers()
    out = {}
    for header in splits.headers():
        text = _script_text(header)
        if not text or "SetHasPartner" not in text:
            continue
        ids = [splits._trainer_id(v) for v in _PARTNER_VAR.findall(text)]
        stems = sorted({_stem(ox[i]["constant"]) for i in ids if i in ox})
        if stems:
            out[header] = stems
    return out


def _partner_stems(ids):
    ox = data.oxide_trainers()
    return sorted(st for st in {_stem(ox[i]["constant"]) for i in ids if i in ox}
                  if st.startswith(PARTNER_PREFIXES))


def scripted():
    """{(stem, stem): {"maps": set, "how": "scripted" or "tag", "partners": [stem]}}.
    A tag battle names the partner through VAR_0x8004, set a few lines
    before it; a two-trainer battle right after SetHasPartner is fought
    beside the map's partner (Riley on Iron Island)."""
    ox = data.oxide_trainers()
    out = {}
    for header in sorted(splits.headers()):
        text = _script_text(header)
        if not text:
            continue
        for m in splits._BATTLE.finditer(text):
            command, operands = m.group(1), m.group(2)
            tokens = [t.strip() for t in operands.split(",")]
            before = text[:m.start()].splitlines()
            near = "\n".join(before[-40:])
            if command == "StartTagBattle":
                foes = tokens[1:3]
                partners = _partner_stems(_token_ids(tokens[0], text))
                how = "tag"
            elif command == "StartTrainerBattle" and len(tokens) > 1 and tokens[1] not in ("0", ""):
                foes = tokens[:2]
                partnered = any("SetHasPartner" in line for line in before[-3:])
                partners = partner_maps().get(header, []) if partnered else []
                how = "tag" if partnered else "scripted"
            else:
                continue
            a_ids, b_ids = (_token_ids(t, text) for t in foes)
            for a in a_ids:
                for b in b_ids:
                    if a == b or a not in ox or b not in ox:
                        continue
                    key = tuple(sorted((_stem(ox[a]["constant"]), _stem(ox[b]["constant"]))))
                    rec = out.setdefault(key, {"maps": set(), "how": how, "partners": []})
                    rec["maps"].add(header)
                    rec["partners"] = sorted(set(rec["partners"]) | set(partners))
    return out


def pairs():
    """[{"key", "stems", "how", "partner", "partners", "maps", "split", ...}], every
    double the player fights against two trainers, and each trainer's own
    double, sorted by split. The key is the two stems joined by "+", in
    order, and stays the same while both trainers keep their names."""
    from . import b6
    ids = {_stem(t["constant"]): tr_id for tr_id, t in data.oxide_trainers().items()}
    placed = b6.placements()
    order = splits.SPLITS + ["Post"]

    def split_of(stems):
        """The later of the two trainers' splits: the balance track's
        placement (the split the story path first meets it in, which puts
        Lake Verity's officers in Candice's), else its map's."""
        found = [(placed.get(ids.get(st)) or {}).get("split") or splits.trainer_split(ids.get(st))
                 for st in stems]
        found = [s for s in found if s in order]
        return max(found, key=order.index) if found else None

    partnered = partner_maps()

    out = []
    for key, rec in eye_contact().items():
        partners = sorted({p for h in rec["maps"] for p in partnered.get(h, [])})
        out.append({"key": "+".join(key), "stems": list(key), "how": "eye contact", "partner": bool(partners),
                    "partners": partners, "maps": sorted(rec["maps"]), "split": split_of(key),
                    "shared_tiles": rec["shared"], "each_alone": rec["solo"], "moves": rec["moves"]})
    for key, rec in scripted().items():
        out.append({"key": "+".join(key), "stems": list(key), "how": rec["how"],
                    "partner": rec["how"] == "tag", "partners": rec["partners"],
                    "maps": sorted(rec["maps"]), "split": split_of(key)})
    for tr_id, t in sorted(data.oxide_trainers().items()):
        if t.get("battle_type") == "Doubles":
            stem = _stem(t["constant"])
            out.append({"key": stem, "stems": [stem], "how": "one trainer's double", "partner": False,
                        "partners": [], "maps": sorted(splits.trainer_maps().get(tr_id, ())),
                        "split": splits.trainer_split(tr_id)})
    # How each is scored today: inside a story fight (fights.json, whose
    # tag battles already count both opponents as one party), or as B6's
    # placed trainers, one at a time.
    fights = [(f["key"], {_stem(c) for c in f.get("trainers") or []}) for f in data.fights()["fights"]]
    for p in out:
        p["story"] = next((k for k, stems in fights if set(p["stems"]) <= stems), None)
        p["placed"] = [st for st in p["stems"] if ids.get(st) in placed]
    order = order + [None]
    return sorted(out, key=lambda p: (order.index(p["split"]) if p["split"] in order else len(order), p["key"]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="print the list as JSON")
    args = ap.parse_args(argv)
    ps = pairs()
    if args.json:
        json.dump(ps, sys.stdout, indent=1)
        return
    for p in ps:
        extra = ""
        if p["how"] == "eye contact":
            extra = (f" shared tiles {p['shared_tiles']}{', each can be met alone' if p['each_alone'] else ''}"
                     f"{', a walker' if p['moves'] else ''}")
        if p["partners"]:
            extra += f" beside {', '.join(p['partners'])}"
        print(f"{str(p['split']):9} {p['how']:20} {p['key']:55} {', '.join(p['maps'])[:60]}{extra}")


if __name__ == "__main__":
    main()
