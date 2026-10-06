"""The player never sets weather (Ian, 2026-09-26; the moves half,
2026-09-30): no species or form the player can own learns a weather move
by level-up, TM or tutor, and weather_moves.py's edits keep each file's
own layout.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_weather_moves

Writes nothing.
"""
import json
import os
import sys

from .. import verify_narcs
from . import weather_moves as W


def check_census(results):
    """Nothing the player can own carries a weather move; a species that
    becomes obtainable later (a new encounter, a gift) fails here until
    weather_moves.py --apply runs again."""
    rows = W.census()
    owned = [r[0] for r in rows if r[2]]
    results.append(("no species the player can own learns a weather move", not owned,
                    f"{len(owned)} do: {owned[:6]}" if owned else f"{len(rows)} trainer-only records keep theirs"))


def check_level_one(results):
    """A removed entry leaves nothing, except where it was the only move at
    level 1: then the next move comes down to level 1."""
    keep = W.strip_level_up([[1, "MOVE_TACKLE"], [1, "MOVE_RAIN_DANCE"], [13, "MOVE_BITE"]])
    bare = W.strip_level_up([[1, "MOVE_SANDSTORM"], [5, "MOVE_ROCK_THROW"], [9, "MOVE_BITE"]])
    later = W.strip_level_up([[1, "MOVE_TACKLE"], [20, "MOVE_HAIL"], [30, "MOVE_BLIZZARD"]])
    ok = keep == [[1, "MOVE_TACKLE"], [13, "MOVE_BITE"]] and \
        bare == [[1, "MOVE_ROCK_THROW"], [9, "MOVE_BITE"]] and \
        later == [[1, "MOVE_TACKLE"], [30, "MOVE_BLIZZARD"]]
    results.append(("a lone level-1 weather move is replaced by the next move", ok, ""))


def check_layout(results):
    """rewrite_list drops elements in place, in either layout the species
    files use, the last element included, and leaves the rest untouched."""
    compact = ('{\n    "a": [\n        [ 1, "MOVE_TACKLE" ],\n        [ 5, "MOVE_HAIL" ]\n    ],\n'
               '    "b": 1\n}\n')
    expanded = ('{\n    "a": [\n        [\n            1,\n            "MOVE_HAIL"\n        ],\n'
                '        [\n            4,\n            "MOVE_TACKLE"\n        ]\n    ]\n}\n')
    a = W.rewrite_list(compact, ["a"], [[1, "MOVE_TACKLE"]])
    b = W.rewrite_list(expanded, ["a"], [[1, "MOVE_TACKLE"]])
    ok = a == '{\n    "a": [\n        [ 1, "MOVE_TACKLE" ]\n    ],\n    "b": 1\n}\n' and \
        b == '{\n    "a": [\n        [\n            1,\n            "MOVE_TACKLE"\n        ]\n    ]\n}\n' and \
        json.loads(a)["b"] == 1
    results.append(("edits keep each file's layout", ok, "" if ok else repr((a, b))))


def check_tm_bits(results):
    """verify_narcs' rule clears exactly the four weather TMs' bits."""
    tail = bytes([0, 0]) + bytes([0xFF] * 16)
    cleared = verify_narcs.without_weather_tms(tail)
    gone = [v + 1 for v in range(128)
            if tail[2 + v // 8] >> (v % 8) & 1 and not cleared[2 + v // 8] >> (v % 8) & 1]
    results.append(("verify_narcs clears only the weather TMs", gone == [7, 11, 18, 37], str(gone)))


def main():
    results = []
    for check in (check_census, check_level_one, check_layout, check_tm_bits):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
