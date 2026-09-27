"""The learnset study's analysis (b): the four moves every wild Pokemon
carries, in Kaizo's tables and Oxide's (Ian, 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.balance.learnwild            # the summary
    PYTHONPATH=. python3 -m tools.oxide.balance.learnwild --write    # and docs/oxide/wild-movesets.md

A wild Pokemon knows the last four moves of its level-up list at or below its
level (Generation 4's default moves, calc_trainers.default_moves), and picks
among them at random each turn, so a move that loses the encounter comes up
a quarter of the time when it is one of four. Ian's example is a Route 207
Growlithe that may Roar.

Two kinds of risk are flagged, per slot at the worst level of its range:

- the encounter ends: the Pokemon blows the player's out (Roar, Whirlwind),
  flees (Teleport) or faints itself (Self-Destruct, Explosion, Memento,
  Healing Wish, Lunar Dance, Final Gambit, Misty Explosion; Perish Song in
  three turns). Kaizo's own list of wild hazards is its first six;
- it may knock itself out while the player wears it down to catch it:
  recoil and crash moves, and a Ghost's Curse.

Each is given as the chance a turn, the share of its moves that are risky.
Also flagged: an encounter whose line comes later in a better version, a
later stage or a strong move of its own type that this one lacks, so a
nuzlocke may do better to wait. Kaizo's areas take the split of their
median level; Oxide's take the encounter design's, with water arriving when
its rod or Surf does.
"""
import argparse
import collections
import functools
import os
import statistics
import sys

from ..encounters import calc_trainers, model, pokedex, progression
from . import data, kaizo_docs, learngen, learnstudy as ls, metrics, pool

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(data.ROOT, "docs", "oxide", "wild-movesets.md")

ENDS = {"Roar", "Whirlwind", "Teleport", "Self-Destruct", "Selfdestruct", "Explosion", "Memento",
        "Healing Wish", "Lunar Dance", "Final Gambit", "Misty Explosion", "Perish Song"}
SELF_KO = {"Take Down", "Double-Edge", "Submission", "Volt Tackle", "Flare Blitz", "Brave Bird",
           "Wood Hammer", "Head Smash", "Wild Charge", "Head Charge", "Wave Crash",
           "Light of Ruin", "Jump Kick", "High Jump Kick", "Hi Jump Kick", "Mind Blown",
           "Steel Beam", "Chloroblast", "Supercell Slam", "Axe Kick"}
KINDS = ["land", "day", "night", "surf", "old_rod", "good_rod", "super_rod"]


def _c(name):
    return metrics._compact(name)


ENDS_C = {_c(m) for m in ENDS}
SELF_KO_C = {_c(m) for m in SELF_KO}


# ---- the encounters -------------------------------------------------------------

def kaizo_encounters():
    """[{"area", "split", "kind", "species", "lo", "hi"}] from Kaizo's tables."""
    docs = kaizo_docs.load()
    out = []
    for key, t in docs["field"].items():
        if not t["rate"]:
            continue
        levels = [lv for _r, sp, lv in t["slots"] if sp]
        if not levels:
            continue
        split = ls.split_of("kaizo", statistics.median(levels))
        for i, (_r, sp, lv) in enumerate(t["slots"]):
            if sp:
                out.append({"area": t["area"], "split": split, "kind": "land",
                            "species": learngen.kaizo_constant(sp), "lo": lv, "hi": lv})
        for kind in ("day", "night"):
            for j, sp in enumerate((docs["day_night"].get(key) or {}).get(kind) or []):
                if sp and j < 2 and len(t["slots"]) > 2 + j:
                    lv = t["slots"][2 + j][2]
                    out.append({"area": t["area"], "split": split, "kind": kind,
                                "species": learngen.kaizo_constant(sp), "lo": lv, "hi": lv})
    for t in docs["water"].values():
        for kind in ("surf", "old_rod", "good_rod", "super_rod"):
            slots = [s for s in t[kind] if s[1]]
            if not slots or not t["rates"].get(kind):
                continue
            split = ls.split_of("kaizo", statistics.median(s[2] for s in slots))
            for _r, sp, lo, hi in slots:
                out.append({"area": t["area"], "split": split, "kind": kind,
                            "species": learngen.kaizo_constant(sp), "lo": min(lo, hi),
                            "hi": max(lo, hi)})
    return out


def oxide_encounters():
    """The same from Oxide's tables, in the encounter design's splits."""
    sidecar = model.load_sidecar() or {}
    area_split = progression.split_of(sidecar)
    entries = sidecar.get("areas") or {}
    out = []
    for area in model.load_all():
        split = area_split.get(area.name)
        if not split:
            continue
        if area.land_active:
            slots = area.slots
            for sp, lv in slots:
                out.append({"area": area.name, "split": split, "kind": "land", "species": sp,
                            "lo": lv, "hi": lv})
            for kind in ("day", "night"):
                for j, sp in enumerate(area.data.get(kind) or []):
                    if sp and sp != "SPECIES_NONE" and j < 2:
                        lv = slots[2 + j][1]
                        out.append({"area": area.name, "split": split, "kind": kind,
                                    "species": sp, "lo": lv, "hi": lv})
        water = (entries.get(area.name) or {}).get("water_split") or split
        for kind in ("surf", "old_rod", "good_rod", "super_rod"):
            if not area.kind_rate(kind):
                continue
            arrives = pool.later(water, progression.rod_split(sidecar, kind))
            if not arrives:
                continue
            for sp, lo, hi in area.kind_slots(kind):
                if sp != "SPECIES_NONE":
                    out.append({"area": area.name, "split": arrives, "kind": kind,
                                "species": sp, "lo": lo, "hi": hi})
    return out


# ---- the movesets ---------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def learnset(game, species):
    """[(level, move name)] in the list's order."""
    if game == "kaizo":
        rec = ls.kaizo_lists().get(species)
        return tuple(rec["list"]) if rec else ()
    moves = pokedex.moves(data.ROOT)
    return tuple((lv, moves[mv]["name"]) for lv, mv in learngen.oxide_list(game, species)
                 if mv in moves)


@functools.lru_cache(maxsize=None)
def types_of(game, species):
    if game == "kaizo":
        rec = ls.kaizo_lists().get(species)
        return frozenset(t.title() for t in (rec or {}).get("types", []))
    rec = pokedex.load(data.ROOT, species) or {}
    return frozenset(t.title() for t in rec.get("types", []))


def moveset(game, species, level):
    return calc_trainers.default_moves(list(learnset(game, species)), level)


def risk(moves, ghost=False):
    """(share of moves that end the encounter, share that may knock it out)."""
    if not moves:
        return 0.0, 0.0
    ends = [m for m in moves if _c(m) in ENDS_C]
    self_ko = [m for m in moves if _c(m) in SELF_KO_C or (ghost and m == "Curse")]
    return len(ends) / len(moves), len(self_ko) / len(moves)


def read(game, enc):
    """One slot at the worst level of its range: its moves there and the two
    chances a turn."""
    ghost = "Ghost" in types_of(game, enc["species"])
    worst = None
    for lv in range(enc["lo"], enc["hi"] + 1):
        mv = moveset(game, enc["species"], lv)
        r = risk(mv, ghost)
        if worst is None or r > worst[1]:
            worst = (lv, r, mv)
    lv, (ends, self_ko), mv = worst
    return dict(enc, level=lv, moves=mv, ends=ends, self_ko=self_ko)


# ---- better later ------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def _family(game):
    """{species: (the line's first stage, its stage number)}."""
    out = {}
    for line in learngen.game_lines(game):
        for i, sp in enumerate(line):
            out.setdefault(sp, (line[0], i))
    return out


def best_stab(game, species, moves):
    """The strongest same-type move among `moves`, by learnstudy's strength."""
    best = 0.0
    types = types_of(game, species)
    for name in moves:
        rec = _move_record(game, name)
        if rec and rec["type"] in types:
            kind, power = ls.strength(rec)
            if kind == "damage":
                best = max(best, power)
    return best


@functools.lru_cache(maxsize=None)
def _move_record(game, name):
    if game == "kaizo":
        km = ls.kaizo_moves()
        k = ls.resolve(name, km)
        return dict(km[k], type=km[k]["type"]) if k else None
    for m in pokedex.moves(data.ROOT).values():
        if m["name"] == name:
            return dict(ls.oxide_move(m), type=m["type"].title())
    return None


def _order(game):
    return ls.SPLIT_NAMES if game == "kaizo" else learngen.OXIDE_ORDER


def clear():
    """Forget what was read, for a fresh proposal."""
    for f in (learnset, _can_reach, _path_stab):
        f.cache_clear()


@functools.lru_cache(maxsize=None)
def _caps(game):
    """{split: cap}, the post-game at 100."""
    if game == "kaizo":
        return dict(ls.splits("kaizo"))
    return dict(pool.caps(), Post=100)


@functools.lru_cache(maxsize=None)
def _can_reach(game, start, target, split):
    """Whether a Pokemon caught as `start` can be `target` by a split's end:
    each evolution on the way comes by the split's cap (Oxide's by its item's
    first split too, as the scores take stones)."""
    line = next((ln for ln in learngen.game_lines(game) if start in ln and target in ln), None)
    if not line or line.index(target) < line.index(start):
        return False
    cap = _caps(game).get(split, 100)
    for sp in line[line.index(start) + 1:line.index(target) + 1]:
        if learngen.is_oxide(game):
            gates = [(lv, item) for lv, item, t in pool.evolutions(learngen.oxide_reached()
                                                                     .get(sp, (None, 0))[0] or sp)
                     if t == sp]
            if gates and split in pool.SPLITS:
                if not any(pool.reachable(lv, item, split) for lv, item in gates):
                    return False
                continue
        if learngen.reached(game, sp) > cap:
            return False
    return True


@functools.lru_cache(maxsize=None)
def _path_stab(game, start, level, split):
    """The strongest same-type move a Pokemon caught as `start` at `level`
    can know by a split's end, by level-up along its line (each stage's moves
    from the level it is reached), its own moves at capture included."""
    cap = _caps(game).get(split, 100)
    line = next((ln for ln in learngen.game_lines(game) if start in ln), [start])
    best = best_stab(game, start, moveset(game, start, level))
    for i, sp in enumerate(line[line.index(start):], start=line.index(start)):
        if not _can_reach(game, start, sp, split):
            break
        lo = level if sp == start else learngen.reached(game, sp)
        moves = [m for lv, m in learnset(game, sp) if lo < lv <= cap or (sp != start and lv == lo)]
        best = max(best, best_stab(game, sp, moves))
    return best


def better_later(game, rows):
    """{index of a row: the later row that beats it}. A later split holds the
    same line as a stage the earlier catch cannot reach by then (a stone not
    yet in reach, a level past the cap), or with a same-type move a band or
    more stronger than any the earlier catch can learn by then. A later wild
    evolved stage often has one, from its level-1 moves, which an evolved
    catch of one's own never learns without the relearner."""
    order = _order(game)
    fam = _family(game)
    by_family = collections.defaultdict(list)
    for i, r in enumerate(rows):
        base, _stage = fam.get(r["species"], (r["species"], 0))
        by_family[base].append(i)
    out = {}
    for items in by_family.values():
        for i in items:
            a = rows[i]
            ai = order.index(a["split"]) if a["split"] in order else 99
            for j in items:
                b = rows[j]
                bi = order.index(b["split"]) if b["split"] in order else 99
                if bi <= ai:
                    continue
                if not _can_reach(game, a["species"], b["species"], b["split"]):
                    if fam.get(b["species"], (None, -1))[1] > fam.get(a["species"], (None, 0))[1]:
                        out[i] = j
                        break
                    continue
                theirs = best_stab(game, b["species"], b["moves"])
                mine = _path_stab(game, a["species"], a["level"], b["split"])
                if theirs >= mine + 15 and ls.band(theirs) != ls.band(mine):
                    out[i] = j
                    break
    return out


# ---- the report --------------------------------------------------------------------

def readings(game):
    encs = kaizo_encounters() if game == "kaizo" else oxide_encounters()
    rows = [read(game, e) for e in encs if learnset(game, e["species"])]
    return rows, better_later(game, rows)


def summary(out=sys.stdout):
    for game in ("kaizo", "oxide"):
        rows, later = readings(game)
        ends = [r for r in rows if r["ends"]]
        ko = [r for r in rows if r["self_ko"]]
        print(f"\n{game}: {len(rows)} wild slots in {len({r['area'] for r in rows})} areas; "
              f"{len(ends)} can end the encounter, {len(ko)} can knock themselves out; "
              f"{len(later)} have a better version of their line later", file=out)
        c = collections.Counter(m for r in ends for m in r["moves"] if _c(m) in ENDS_C)
        print(f"  ending moves: {dict(c.most_common())}", file=out)
        by_split = collections.Counter(r["split"] for r in ends)
        print(f"  slots that can end the encounter, by split: {dict(by_split)}", file=out)
        worst = sorted(ends, key=lambda r: -r["ends"])[:8]
        for r in worst:
            print(f"  {r['area']:28} {r['kind']:9} {r['species'].replace('SPECIES_', '').title():12}"
                  f" {r['level']:>3} {r['ends']:.2f} a turn: {', '.join(r['moves'])}", file=out)


def write_doc():
    """docs/oxide/wild-movesets.md: every flagged slot, Oxide's in full and
    Kaizo's by area."""
    lines = ["# Wild movesets, the risky and the ones to wait for", "",
             "Generated by `tools/oxide/balance/learnwild.py --write` (the learnset study's "
             "analysis (b), Ian's request of 2026-09-27). A wild Pokemon knows the last four "
             "level-up moves at or below its level and picks one at random each turn. A slot "
             "is listed when a move can end the encounter (it blows the player's Pokemon out, "
             "flees or faints itself) or can make the Pokemon knock itself out (recoil, crash, "
             "a Ghost's Curse), with the chance a turn, at the worst level of its range; or "
             "when a later split holds a better version of its line (a later stage, or a "
             "same-type move a band stronger). Nothing here is written to the game data.", ""]
    rows, later = readings("oxide")
    lines += ["## Oxide's tables, every flagged slot", "",
              "| Area | Split | Slot | Pokemon | Level | Ends it | Self knockout | "
              "Better later | Moves |", "|---|---|---|---|---|---|---|---|---|"]
    for i, r in sorted(enumerate(rows), key=lambda x: (x[1]["area"], x[1]["kind"])):
        if not (r["ends"] or r["self_ko"] or i in later):
            continue
        j = later.get(i)
        better = (f"{rows[j]['species'].replace('SPECIES_', '').title()}, {rows[j]['area']}"
                  if j is not None else "")
        lines.append(f"| {r['area'].replace('encounters_', '')} | {r['split']} | {r['kind']} | "
                     f"{r['species'].replace('SPECIES_', '').title()} | {r['level']} | "
                     f"{r['ends']:.2f} | {r['self_ko']:.2f} | {better} | "
                     f"{', '.join(r['moves'])} |")
    # Kaizo's tables run to thousands of flagged slots, so they are counted
    # by area: the pattern is the point there, not each slot.
    rows, later = readings("kaizo")
    per = collections.defaultdict(lambda: [0, 0, 0, 0, set()])
    for i, r in enumerate(rows):
        p = per[(r["area"], r["split"])]
        p[0] += 1
        p[1] += bool(r["ends"])
        p[2] += bool(r["self_ko"])
        p[3] += i in later
        p[4] |= {m for m in r["moves"] if _c(m) in ENDS_C}
    lines += ["", "## Platinum Kaizo's tables, by area", "",
              "| Area | Split | Slots | Can end it | Can knock itself out | Better later | "
              "Ending moves |", "|---|---|---|---|---|---|---|"]
    for (area, split), (n, e, k, b, moves) in sorted(per.items()):
        lines.append(f"| {area} | {split} | {n} | {e} | {k} | {b} | {', '.join(sorted(moves))} |")
    lines.append("")
    with open(DOC, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    summary()
    if args.write:
        write_doc()
    return 0


if __name__ == "__main__":
    sys.exit(main())
