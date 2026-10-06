"""The player never sets, changes or ends weather (Ian, 2026-09-26), so no
species or form the player can own learns a weather move: not by level-up
(level 1 included), not by TM, not from a tutor. The abilities half of the
ruling landed on 2026-09-29; this is the moves half (Ian, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.weather_moves            # the census
    PYTHONPATH=. python3 -m tools.oxide.balance.weather_moves --apply    # remove them

A species the player cannot own (b6.obtainable: the League's side, every
scripted source, the drawn legendary thirds, and what each evolves into)
keeps its weather moves, since only trainers use it. A form counts as
owned when its species is. Egg lists are left alone: a nuzlocke has no
breeding, so they are only the trainers' palette (Ian, 2026-09-28).

A removed level-up entry leaves nothing in its place, except where it was
the species' only move at level 1: then the next move on its list comes
down to level 1, so a Pokemon met at its lowest level still knows one
(learngen's rule for a first stage's level 1).
"""
import argparse
import functools
import glob
import json
import os
import sys

from .. import jsonstyle
from ..encounters import pokedex
from . import b6, data

WEATHER_MOVES = {"MOVE_RAIN_DANCE", "MOVE_SUNNY_DAY", "MOVE_SANDSTORM", "MOVE_HAIL",
                 "MOVE_SNOWSCAPE", "MOVE_CHILLY_RECEPTION"}
POKEMON = os.path.join(data.ROOT, "res", "pokemon")


@functools.lru_cache(maxsize=None)
def weather_tms():
    """The TM and HM labels ("TM18") whose move sets weather."""
    return frozenset(m for m, mv in pokedex.machines(data.ROOT).items() if mv in WEATHER_MOVES)


@functools.lru_cache(maxsize=None)
def species_of_folder():
    out = {}
    with open(os.path.join(data.ROOT, "generated", "species.txt"), encoding="utf-8") as f:
        for line in f:
            sp = line.strip()
            if sp.startswith("SPECIES_"):
                out.setdefault(pokedex.folder_of(sp), sp)
    return out


def records():
    """[(data.json path, its folder under res/pokemon, species constant)]
    for every species and form record."""
    out = []
    for path in sorted(glob.glob(os.path.join(POKEMON, "**", "data.json"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(path), POKEMON)
        out.append((path, rel, species_of_folder().get(rel.split(os.sep)[0])))
    return out


def carried(rec):
    """(level-up entries, TM labels, tutor moves) that set weather."""
    ls = rec.get("learnset") or {}
    return ([e for e in ls.get("by_level") or [] if e[1] in WEATHER_MOVES],
            [m for m in ls.get("by_tm") or [] if m in weather_tms()],
            [m for m in ls.get("by_tutor") or [] if m in WEATHER_MOVES])


def census():
    """[(folder, species, owned, level entries, TMs, tutor moves)] for every
    record that carries a weather move."""
    owned = b6.obtainable()
    rows = []
    for path, rel, sp in records():
        with open(path, encoding="utf-8") as f:
            lv, tm, tu = carried(json.load(f))
        if lv or tm or tu:
            rows.append((rel, sp, sp in owned, lv, tm, tu))
    return rows


def strip_level_up(entries):
    """The level-up list without weather moves; where one was the only move
    at level 1, the next move on the list comes down to level 1."""
    kept = [e for e in entries if e[1] not in WEATHER_MOVES]
    had_one = any(lv <= 1 for lv, _m in entries)
    if had_one and kept and not any(lv <= 1 for lv, _m in kept):
        first = min(range(len(kept)), key=lambda i: kept[i][0])
        kept[first] = [1, kept[first][1]]
        kept.sort(key=lambda e: e[0])
    return kept


def _elements(body):
    """The top-level elements of a JSON array's inner text, each with the
    whitespace before it, as (start, end) spans."""
    spans, depth, start, in_str, esc = [], 0, 0, False, False
    for i, ch in enumerate(body):
        if in_str:
            esc = ch == "\\" and not esc
            if ch == '"' and not esc:
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            spans.append((start, i))
            start = i + 1
    # The last element stops at its own text: the whitespace before the
    # closing bracket belongs to the array, whichever element is last.
    if body[start:].strip():
        spans.append((start, len(body.rstrip())))
    return spans


def rewrite_list(text, path, new):
    """The text with the array at `path` holding `new`, a subsequence of
    what it holds now with at most some elements changed in value, each kept
    element keeping its own text and the file's own layout. A changed
    element (a move brought down to level 1) is rendered in its neighbours'
    style."""
    vs, ve, _indent = jsonstyle._find_key(text, path)
    inner = text[vs + 1:ve - 1]
    spans = _elements(inner)
    old = json.loads(text[vs:ve])
    assert len(old) == len(spans)
    tail = inner[spans[-1][1]:] if spans else inner
    kept, j = [], 0
    for (s, e), value in zip(spans, old):
        piece = inner[s:e]
        if j < len(new) and new[j] == value:
            kept.append(piece)
            j += 1
        elif j < len(new) and isinstance(value, list) and new[j][1:] == value[1:]:
            # The same move at a new level: only the level's digits change.
            kept.append(piece.replace(str(value[0]), str(new[j][0]), 1))
            j += 1
    assert j == len(new), (path, new)
    return text[:vs + 1] + ",".join(kept) + tail + text[ve - 1:]


def apply(dry_run=False):
    """Removes every weather move from the owned records' lists; returns
    [(folder, what changed)]."""
    owned = b6.obtainable()
    changes = []
    for path, rel, sp in records():
        if sp not in owned:
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        rec = json.loads(text)
        lv, tm, tu = carried(rec)
        if not (lv or tm or tu):
            continue
        ls = rec["learnset"]
        what = []
        if lv:
            new = strip_level_up(ls["by_level"])
            moved = [e for e in new if e not in ls["by_level"]]
            text = rewrite_list(text, ["learnset", "by_level"], new)
            what.append(f"level-up {[tuple(e) for e in lv]}"
                        + (f", {moved[0][1]} to level 1" if moved else ""))
        if tm:
            text = rewrite_list(text, ["learnset", "by_tm"],
                                           [m for m in ls["by_tm"] if m not in weather_tms()])
            what.append(f"TMs {tm}")
        if tu:
            text = rewrite_list(text, ["learnset", "by_tutor"],
                                           [m for m in ls["by_tutor"] if m not in WEATHER_MOVES])
            what.append(f"tutor {tu}")
        if not dry_run:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        changes.append((rel, "; ".join(what)))
    return changes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    if a.apply:
        changes = apply()
        for rel, what in changes:
            print(f"{rel}: {what}")
        print(f"{len(changes)} records changed")
    rows = census()
    owned = [r for r in rows if r[2]]
    print(f"weather TMs: {sorted(weather_tms())}")
    print(f"{len(rows)} records carry a weather move: {len(owned)} the player can own, "
          f"{len(rows) - len(owned)} trainer-only")
    for rel, sp, own, lv, tm, tu in owned:
        print(f"  owned: {rel} level-up {lv} TMs {tm} tutor {tu}")
    return 1 if owned else 0


if __name__ == "__main__":
    sys.exit(main())
