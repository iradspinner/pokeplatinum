"""The learnset pass: design pass 3 of docs/oxide/balance-plan.md.

    PYTHONPATH=. python3 tools/oxide/balance/learnset_pass.py --dry-run
    PYTHONPATH=. python3 tools/oxide/balance/learnset_pass.py --apply --report docs/oxide/learnset-pass.md

Rewrites the level-up learnset (learnset.by_level) of every species on the
pick-list (docs/oxide/species-pick-list.csv, status native or new), and of
the alternate forms with their own record whose species is on it. The
natives take Kaizo's list (docs/oxide/kaizo-learnsets.tsv) line by line; the
new species keep the donor list the tree already has. Both then take Ian's
adjustments of 2026-09-27 (the Kaizo comparison's answers and the move pool's
first cut), which the constants below spell out. Magikarp is off the pick-list
but is one of the seven level-1 picks, so it takes that pick and nothing else.

The source is read from git (the branch point, BASE_REV) rather than from the
working tree, so a second run gives the same result as the first and the
report always compares against the lists the pass started from.

TMs, tutors, egg moves, move data and trainers are not touched.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

from tools.oxide import jsonstyle
from tools.oxide.encounters import dex, pokedex

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
KAIZO = os.path.join(ROOT, "docs", "oxide", "kaizo-learnsets.tsv")
# The commit this pass was cut from; today's lists are read from it.
BASE_REV = "a5ca2f482"
MAX_LEARNSET_ENTRIES = 34   # include/struct_defs/species.h

# Ian, 2026-09-26 (staples survey): the player never sets weather, so no
# weather move is in any player learnset. Chilly Reception sets snow.
WEATHER = {"MOVE_RAIN_DANCE", "MOVE_SUNNY_DAY", "MOVE_SANDSTORM", "MOVE_HAIL",
           "MOVE_SNOWSCAPE", "MOVE_CHILLY_RECEPTION"}
# Ian, 2026-09-27 (move pool survey): twelve moves leave every learnset.
FIRST_CUT = {"MOVE_TELEKINESIS", "MOVE_ALLY_SWITCH", "MOVE_TOPSY_TURVY",
             "MOVE_FLOWER_SHIELD", "MOVE_FAIRY_LOCK", "MOVE_AROMATIC_MIST",
             "MOVE_MAGNETIC_FLUX", "MOVE_SPEED_SWAP", "MOVE_ELECTRIC_TERRAIN",
             "MOVE_GRASSY_TERRAIN", "MOVE_MISTY_TERRAIN", "MOVE_PSYCHIC_TERRAIN"}
# The same ruling: Splash and Teleport go, and seven species get a real
# level-1 move in their place, the balance track's picks.
SPLASH_TELEPORT = {"MOVE_SPLASH", "MOVE_TELEPORT"}
PICKS = {
    "SPECIES_AZURILL": "MOVE_POUND",
    "SPECIES_BOUNSWEET": "MOVE_LEAFAGE",
    "SPECIES_FEEBAS": "MOVE_TACKLE",
    "SPECIES_HOPPIP": "MOVE_ABSORB",
    "SPECIES_WAILMER": "MOVE_WATER_GUN",
    "SPECIES_ABRA": "MOVE_CONFUSION",
    "SPECIES_MAGIKARP": "MOVE_TACKLE",
}
# Ian, 2026-09-26 (native moves report): Beat Up leaves every learnset.
BEAT_UP = {"MOVE_BEAT_UP"}

# Kaizo's rebuilt moves, by the name its list uses, turned into the real move
# docs/oxide/kaizo-comparison.md names ("Kaizo-only moves in the learnsets"),
# or None where it names none. Vise Grip's row names three; Liquidation is the
# closest of them to Kaizo's physical Water 90.
REBUILT = {
    "ViceGrip": "MOVE_LIQUIDATION",
    "Swallow": "MOVE_POISON_JAB",
    "Lick": "MOVE_SHADOW_CLAW",
    "Stomp": "MOVE_HIGH_HORSEPOWER",
    "Memento": "MOVE_EXPLOSION",
    "Absorb": None,          # special Dark 60 that drains; Oxide has none
    "Rage": "MOVE_BRICK_BREAK",
    "Heart Swap": None,      # special Water 95 that drains; Oxide has none
    "Egg Bomb": "MOVE_SEED_BOMB",
    "Water Ball": "MOVE_SURF",
    "Bonemerang": None,      # Rock 60 twice; Oxide has none
    "HP Water": None,
}

# Kaizo's rows for the forms with their own record, by folder.
FORM_ROWS = {
    496: "deoxys/forms/attack", 497: "deoxys/forms/defense", 498: "deoxys/forms/speed",
    499: "wormadam/forms/sandy", 500: "wormadam/forms/trash",
    501: "giratina/forms/origin", 502: "shaymin/forms/sky",
    503: "rotom/forms/heat", 504: "rotom/forms/wash", 505: "rotom/forms/frost",
    506: "rotom/forms/fan", 507: "rotom/forms/mow",
}


def _norm(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def excluded_moves(moves):
    """{move: reason} for every move no learnset may carry: Z-moves and Max
    moves, effects that are still placeholders, and status moves whose record
    runs the plain-hit script (so their effect never happens)."""
    out = {}
    for mv, rec in moves.items():
        if "Z-Power" in rec["description"] or rec["id"] in range(625, 661) \
                or rec["id"] in range(698, 707) or rec["id"] in range(726, 732) \
                or mv == "MOVE_CATASTROPIKA" or mv.startswith("MOVE_MAX_"):
            out[mv] = "a Z-move or Max move"
        elif rec["stub"]:
            out[mv] = "its effect is a placeholder"
        elif rec["class"] == "STATUS" and rec["effect"] == "HIT":
            out[mv] = "a status move with no effect written"
    for mv in WEATHER:
        out[mv] = "a weather move"
    for mv in FIRST_CUT:
        out[mv] = "the move pool's first cut"
    for mv in SPLASH_TELEPORT:
        out[mv] = "Splash and Teleport go"
    for mv in BEAT_UP:
        out[mv] = "Beat Up leaves the game"
    return out


def kaizo_rows():
    """{id: [(Kaizo name, level)]} in Kaizo's order."""
    rows = {}
    with open(KAIZO, encoding="utf-8") as f:
        next(f)
        for line in f:
            fields = line.rstrip("\n").split("\t")
            rows[int(fields[0])] = [(n, int(l)) for n, l in
                                    (e.rsplit("@", 1) for e in fields[2:] if e)]
    return rows


def git_show(rev, path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def species_id_map():
    """{SPECIES_X: its id}: generated/species.txt lists every constant in id
    order, SPECIES_NONE first."""
    with open(os.path.join(ROOT, "generated", "species.txt"), encoding="utf-8") as f:
        return {line.strip(): i for i, line in enumerate(f) if line.strip()}


def targets():
    """[(species constant, form folder or None, data.json path relative to ROOT,
    Kaizo row id or None)] for everything the pass rewrites."""
    species_ids = species_id_map()
    out = []
    listed = {r["constant"] for r in dex.pick_list(ROOT)
              if r["status"] in ("native", "new") and r["constant"]}
    for sp in sorted(listed, key=lambda s: species_ids.get(s, 10**6)):
        folder = pokedex.folder_of(sp)
        idx = species_ids[sp]
        out.append((sp, None, f"res/pokemon/{folder}/data.json", idx if idx <= 493 else None))
        for row, form in FORM_ROWS.items():
            if form.split("/")[0] == folder:
                out.append((sp, form, f"res/pokemon/{form}/data.json", row))
    out.append(("SPECIES_MAGIKARP", None, "res/pokemon/magikarp/data.json", None))
    return out


def build(sp, kaizo, today, moves, excluded, name_to_move, pick_only=False):
    """(new list, notes) for one record. `kaizo` is Kaizo's row for a native
    (None for a new species or Magikarp), `today` the list at BASE_REV. Each
    note is (kind, text) where kind is what the report files it under."""
    notes = []
    names = {mv: rec["name"] for mv, rec in moves.items()}
    had_splash_teleport = False
    entries = []
    if kaizo is not None:
        for kname, lv in kaizo:
            if kname in REBUILT:
                real = REBUILT[kname]
                if real is None:
                    notes.append(("kaizo", f"Kaizo's {kname} {lv} left out: Oxide has no move like it"))
                    continue
                notes.append(("kaizo", f"Kaizo's {kname} {lv} became {names[real]}"))
                entries.append([lv, real])
                continue
            entries.append([lv, name_to_move[_norm(kname)]])
    else:
        entries = [list(e) for e in today]

    kept = []
    for lv, mv in entries:
        if mv in SPLASH_TELEPORT:
            had_splash_teleport = True
        if pick_only and mv not in SPLASH_TELEPORT:
            kept.append([lv, mv])
            continue
        if mv not in moves:
            notes.append(("kaizo", f"{mv} {lv} left out: not in Oxide's move table"))
            continue
        if mv in excluded:
            notes.append(("rule", f"{names[mv]} {lv} out: {excluded[mv]}"))
            continue
        if lv == 0:
            notes.append(("rule", f"{names[mv]} moved from level 0 (evolution) to 1"))
            lv = 1
        kept.append([lv, mv])

    seen, deduped = set(), []
    for lv, mv in kept:
        if (lv, mv) in seen:
            notes.append(("rule", f"{names[mv]} {lv} listed twice; one kept"))
            continue
        seen.add((lv, mv))
        deduped.append([lv, mv])
    kept = deduped

    pick = PICKS.get(sp)
    if pick and (had_splash_teleport or not any(lv == 1 for lv, _ in kept)):
        earlier = [lv for lv, mv in kept if mv == pick]
        kept = [[lv, mv] for lv, mv in kept if mv != pick]
        kept.insert(0, [1, pick])
        why = "in place of Splash or Teleport" if had_splash_teleport else "as its only level-1 move"
        notes.append(("rule", f"{names[pick]} at 1, the balance track's pick, {why}"
                      + (f" (was at {', '.join(map(str, earlier))})" if earlier else "")))
    elif pick:
        notes.append(("rule", f"{names[pick]} pick not applied: Kaizo's list has no Splash "
                      f"or Teleport and already starts with "
                      + ", ".join(names[mv] for lv, mv in kept if lv == 1)))

    kept.sort(key=lambda e: e[0])   # stable: Kaizo's order within a level stays
    # Where Teleport or Splash was the only level-1 move and no pick covers
    # the species, the list's first move comes down to level 1, so that a
    # low-level one is never generated with no move at all.
    if not pick and kept and not any(lv == 1 for lv, _ in kept) \
            and any(lv <= 1 and mv in SPLASH_TELEPORT for lv, mv in entries):
        notes.append(("rule", f"{names[kept[0][1]]} moved from {kept[0][0]} to 1: Teleport or "
                      f"Splash was the only level-1 move (a pick for the balance track to confirm)"))
        kept[0][0] = 1
    if len(kept) > MAX_LEARNSET_ENTRIES:
        raise SystemExit(f"{sp}: {len(kept)} entries, over {MAX_LEARNSET_ENTRIES}")
    if not any(lv == 1 for lv, _ in kept):
        notes.append(("warn", "no level-1 move"))
    return kept, notes


def _levels(lst):
    out = collections.defaultdict(list)
    for lv, mv in lst:
        out[mv].append(lv)
    return out


def diff(old, new, names):
    """(added, removed, moved) between two lists, as readable strings."""
    a, b = _levels(old), _levels(new)
    added = [f"{names.get(mv, mv)} {','.join(map(str, b[mv]))}" for mv in b if mv not in a]
    removed = [f"{names.get(mv, mv)} {','.join(map(str, a[mv]))}" for mv in a if mv not in b]
    moved = [f"{names.get(mv, mv)} {','.join(map(str, a[mv]))} to {','.join(map(str, b[mv]))}"
             for mv in b if mv in a and sorted(a[mv]) != sorted(b[mv])]
    return added, removed, moved


def kaizo_as_moves(kaizo, name_to_move):
    """Kaizo's row as [(level, move)] with its own names mapped as far as they
    go, for the comparison column (a rebuilt move keeps Kaizo's name)."""
    out = []
    for kname, lv in kaizo:
        mv = name_to_move.get(_norm(kname)) if kname not in REBUILT else None
        out.append((lv, mv or f"Kaizo's {kname}"))
    return out


def edit_text(text, new):
    """The file with learnset.by_level replaced, in the file's own style: the
    older one-line pairs, or one number and one move per line."""
    vs, ve, indent = jsonstyle._find_key(text, ["learnset", "by_level"])
    old_text = text[vs:ve]
    old = json.loads(old_text)
    style = None
    for max_inline in (2, 0):
        if jsonstyle.dumps(old, indent, max_inline=max_inline) == old_text:
            style = max_inline
            break
    if style is None:
        raise SystemExit("by_level is in neither style; refusing to reformat")
    return text[:vs] + jsonstyle.dumps(new, indent, max_inline=style) + text[ve:]


def run(apply, report_path):
    moves = pokedex.moves(ROOT)
    names = {mv: rec["name"] for mv, rec in moves.items()}
    name_to_move = {_norm(rec["name"]): mv for mv, rec in moves.items()}
    excluded = excluded_moves(moves)
    rows = kaizo_rows()
    species_ids = species_id_map()

    results = []
    for sp, form, path, row in targets():
        base_text = git_show(BASE_REV, path)
        today = json.loads(base_text)["learnset"]["by_level"]
        kaizo = rows[row] if row is not None else None
        new, notes = build(sp, kaizo, today, moves, excluded, name_to_move,
                           pick_only=(sp == "SPECIES_MAGIKARP"))
        results.append((sp, form, path, row, today, kaizo, new, notes))
        if apply:
            with open(os.path.join(ROOT, path), encoding="utf-8") as f:
                current = f.read()
            if json.loads(current)["learnset"]["by_level"] != today \
                    and json.loads(current)["learnset"]["by_level"] != new:
                raise SystemExit(f"{path} changed since {BASE_REV}; refusing to overwrite")
            out = edit_text(base_text, new) if current == base_text else edit_text(current, new)
            with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="\n") as f:
                f.write(out)

    changed = [r for r in results if [list(e) for e in r[4]] != r[6]]
    members = sorted(r[3] if r[3] is not None else species_ids[r[0]]
                     for r in changed if (r[3] is not None or species_ids[r[0]] <= 493))
    print(f"{len(results)} records, {len(changed)} changed; "
          f"{len(members)} are base-ROM wotbl members: {members}")
    warns = [(r[0], r[1]) for r in results if any(k == "warn" for k, _ in r[7])]
    if warns:
        print("no level-1 move:", warns)
    if report_path:
        write_report(results, names, name_to_move, report_path)
    return results


def write_report(results, names, name_to_move, path):
    def display(sp, form):
        base = sp.replace("SPECIES_", "").replace("_", " ").title()
        return f"{base} ({form.split('/')[-1]})" if form else base

    natives = [r for r in results if r[5] is not None]
    new = [r for r in results if r[5] is None and r[0] != "SPECIES_MAGIKARP"]
    counts = collections.Counter()
    for r in results:
        for kind, text in r[7]:
            counts[text.split(" out: ")[-1] if kind == "rule" and " out: " in text else kind] += 1

    lines = [
        "# The learnset pass",
        "",
        "Design pass 3 of `docs/oxide/balance-plan.md`, written on `cloud/balance-learnset-pass` "
        f"from `{BASE_REV}` by `tools/oxide/balance/learnset_pass.py`, which regenerates this file. "
        "Every species on the pick-list has a new level-up list: the natives take Kaizo's list "
        "line by line, the new species keep their donor lists, and both take Ian's adjustments of "
        "2026-09-27. The balance track reviews it line by line and rescores. Nothing here has been "
        "seen in game.",
        "",
        "Each line gives what the pass added, removed or moved against today's list (the tree at "
        f"`{BASE_REV}`), and for a native, where the result departs from Kaizo's own list and why. "
        "A move with two levels learns at both. Level 1 on an evolved stage is its evolution and "
        "relearner slot.",
        "",
        "## Choices the pass made that the balance track should confirm",
        "",
        "- Kaizo's lists sometimes repeat a move. The same move twice at the same level is kept "
        "once; a move repeated at another level stays, since each copy is a prompt at that level.",
        "- The seven level-1 picks go in where the list still carried Splash or Teleport, or had no "
        "level-1 move once Kaizo's rebuilt Absorb left: Abra, Hoppip, Bounsweet and Magikarp. "
        "Kaizo's Azurill, Feebas and Wailmer have no Splash and already open with Present, Water "
        "Pulse and Water Pulse, so their picks were not applied.",
        "- Kaizo's Shellder and Meditite had Teleport as their only level-1 move, which would leave "
        "a low-level one with no move at all. Their first move comes down to level 1: Take Down "
        "and Karate Chop.",
        "- Kaizo's Vise Grip becomes Liquidation, the closest to its physical Water 90 of the three "
        "moves the comparison names. Stomp becomes High Horsepower at Kaizo's level everywhere, so "
        "Ponyta has it at 6, in Roark's split; Rage becomes Brick Break, the comparison's move "
        "\"for the type\".",
        "- Weather Ball stays (Ledian, Piplup, Prinplup): it reads weather and sets none.",
        "- Cut (Zangoose), Rock Smash (Mudkip, Bagon) and Flash (nine species) stay where Kaizo "
        "teaches them by level. The ruling takes them out where they were only HMs, which is the "
        "TM pass's work.",
        "- Kaizo's levels stand as Kaizo has them, including those past the League cap of 78; none "
        "is re-timed to Oxide's evolution levels.",
        "- Kaizo's Wormadam (Plant) opens at 16, with no level-1 move; it is reached only by "
        "evolution at 20, so the list stands.",
        "- Only the pick-list and Magikarp are touched. Species off the pick-list that still learn "
        "Splash or Teleport (Spoink, Grumpig, Wynaut, Natu, Xatu, Claydol, Deoxys) or a weather "
        "move (Gyarados, which `b6.py` counts as obtainable, and twelve species neither list reaches) are "
        "left for the balance track, since each change moves a trainer's default moves.",
        "",
        "## How the rules came out",
        "",
        "| What | Entries |",
        "|---|---|",
    ]
    for what, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        if what in ("kaizo", "rule", "warn"):
            continue
        lines.append(f"| {what} | {n} |")
    lines.append(f"| Kaizo's rebuilt moves turned into a real move or left out | {counts['kaizo']} |")
    lines.append("")

    def section(title, recs, with_kaizo):
        lines.extend([f"## {title}", ""])
        for sp, form, path, row, today, kaizo, newl, notes in recs:
            added, removed, moved = diff([tuple(e) for e in today], [tuple(e) for e in newl], names)
            if not (added or removed or moved or notes):
                continue
            head = display(sp, form)
            if row is not None:
                head += f" ({row})"
            lines.append(f"**{head}**, {len(newl)} moves:")
            lines.append("")
            final = ", ".join(f"{names[mv]} {lv}" for lv, mv in newl)
            lines.append(f"- New list: {final}.")
            if added:
                lines.append(f"- Added against today's: {'; '.join(added)}.")
            if removed:
                lines.append(f"- Removed against today's: {'; '.join(removed)}.")
            if moved:
                lines.append(f"- Moved against today's: {'; '.join(moved)}.")
            if with_kaizo:
                ka = kaizo_as_moves(kaizo, name_to_move)
                kadd, krem, kmov = diff(ka, [tuple(e) for e in newl], names)
                if not (kadd or krem or kmov):
                    lines.append("- Against Kaizo's: the same.")
            for kind, text in notes:
                label = {"kaizo": "Against Kaizo's", "rule": "Rule", "warn": "Check"}[kind]
                lines.append(f"- {label}: {text}.")
            lines.append("")

    section("Natives, on Kaizo's lists", natives, True)
    section("New species, on their donor lists", new, False)
    section("Magikarp, off the pick-list", [r for r in results if r[0] == "SPECIES_MAGIKARP"], False)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the new lists into res/pokemon")
    ap.add_argument("--dry-run", action="store_true", help="count only (the default)")
    ap.add_argument("--report", help="write the per-line report here")
    args = ap.parse_args()
    run(args.apply, args.report)


if __name__ == "__main__":
    sys.exit(main())
