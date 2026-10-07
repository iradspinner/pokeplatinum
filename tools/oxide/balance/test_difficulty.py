"""The fight difficulty store (difficulty.json) parses, every key is a real
trainer or a story fight with several, and every reading is well formed;
put() replaces a reading in place; the formula is Ian's.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_difficulty
"""
import json
import os
import shutil
import sys
import tempfile

from . import pldifficulty as pd


def main():
    results = []
    store = pd.load()
    found = pd.problems(store)
    n = sum(len(v) for v in store["fights"].values()) + sum(len(s["readings"]) for s in store["sections"].values())
    results.append(("the store parses, and every key, trainer and reading is well formed", not found,
                    f"{len(store['fights'])} keys, {n} readings; problems {found[:5]}"))

    sample = {"won": 0.9, "faints": 0.5}
    results.append(("difficulty is faints plus 40 times the losing rate", abs(pd.difficulty(sample) - 4.5) < 1e-9,
                    f"{pd.difficulty(sample)} for 90% won and 0.5 faints"))

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "difficulty.json")
        shutil.copy(pd.PATH, path)
        before = pd.load(path)["fights"]["TRAINER_LEADER_ROARK"]
        new = dict(before[0], won=0.5, clean=0.4, date="2026-10-08", stale=None)
        pd.put("TRAINER_LEADER_ROARK", new, path)
        after = pd.load(path)["fights"]["TRAINER_LEADER_ROARK"]
        ok = (len(after) == len(before) and after[0]["won"] == 0.5 and [r["team"] for r in after]
              == [r["team"] for r in before] and not pd.problems(pd.load(path)))
        results.append(("put() replaces the reading of the same team and trainer, in order", ok,
                        f"{[(r['team'], r['won']) for r in after]}"))

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
