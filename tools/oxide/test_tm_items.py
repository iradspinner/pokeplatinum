"""Check tools/oxide/tm_items.py on a scratch copy of the files it reads and
writes. Nothing here writes to the checkout.

The fixture, tools/oxide/test_tm_items.tsv, is the TM list of the Balance
Agent's step 6 draft: test data, not the approved list.

    python3 tools/oxide/test_tm_items.py [--built-tree DIR]

What it checks:

1. Every listed TM and HM teaches its move; a record whose move changed
   takes that move's description, fitting the Bag's box, and a disc palette
   that exists; a listed HM can be tossed; HM01 and HM06, unlisted, are left
   as they were.
2. TM93 and TM94 get records, and ids just before MAX_ITEMS with no other id
   moved, and include/constants/items.h counts them.
3. A second apply changes nothing.
4. A list without TM94 takes its id and record back out, and the full list
   puts them back.
5. Bad lists are refused with their reason.

With --built-tree DIR, a checkout where the fixture was applied and the ROM
built, it also runs `check` there, which reads the TM-to-move table out of
the ROM.

Prints "passed" when every check passes.
"""
import argparse
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import textfit  # noqa: E402
import tm_items as tm  # noqa: E402

FIXTURE = os.path.join(HERE, "test_tm_items.tsv")
COPY = ["res/items/data", "res/items/icons", "res/moves", "generated", "include/constants"]

failures = []


def expect(ok, what):
    if not ok:
        failures.append(what)


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = tm.main(list(argv))
    return code, out.getvalue()


def record(root, label):
    with open(os.path.join(root, tm.DATA, f"{label.lower()}.json"), encoding="utf-8") as f:
        return json.load(f)


def write_list(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("tm\tmove\n")
        for label, move in rows:
            f.write(f"{label}\t{move}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--built-tree", help="a checkout with the fixture applied and its ROM built")
    a = ap.parse_args()
    entries = tm.read_list(FIXTURE)

    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, "tree")
        for rel in COPY:
            shutil.copytree(os.path.join(ROOT, rel), os.path.join(work, rel))
        before = {}
        for label in ("HM01", "HM06"):
            with open(os.path.join(work, tm.DATA, f"{label.lower()}.json"), encoding="utf-8") as f:
                before[label] = f.read()
        with open(os.path.join(work, tm.ITEMS_TXT), encoding="utf-8") as f:
            ids_before = [n for n in f.read().split() if not re.fullmatch(r"ITEM_TM(9[3-9]|1\d\d)", n)]

        # 1 to 3: apply, read back, apply again.
        code, out = run("apply", "--list", FIXTURE, "--root", work)
        expect(code == 0, f"apply failed: {out}")
        for label, move in entries:
            r = record(work, label)
            expect(r["teachesMove"] == move, f"{label} teaches {r['teachesMove']}, not {move}")
            lines = [l.rstrip("\n") for l in r["description"]]
            expect(textfit.fits(lines, width=tm.BAG_WIDTH, max_lines=tm.BAG_LINES),
                   f"{label}'s description does not fit the Bag's box: {lines}")
            pal = r["icon"]["palette"][:-len("_NCLR")]
            expect(any(n.startswith(pal + ".") for n in os.listdir(os.path.join(work, "res/items/icons"))),
                   f"{label}'s palette {pal} does not exist")
            if label.startswith("HM"):
                expect(r["preventToss"] is False, f"{label} still cannot be tossed")
        iron = record(work, "TM48")
        expect("".join(iron["description"]).startswith("The user hardens its body"),
               f"TM48's description is not Iron Defense's: {iron['description']}")
        for label, text in before.items():
            with open(os.path.join(work, tm.DATA, f"{label.lower()}.json"), encoding="utf-8") as f:
                expect(f.read() == text, f"{label}, unlisted, changed")
        with open(os.path.join(work, tm.ITEMS_TXT), encoding="utf-8") as f:
            ids = f.read().split()
        expect(ids[:ids.index("MAX_ITEMS")] == ids_before[:ids_before.index("MAX_ITEMS")] + ["ITEM_TM93", "ITEM_TM94"],
               "the new ids are not just before MAX_ITEMS, or another id moved")
        with open(os.path.join(work, tm.ITEMS_H), encoding="utf-8") as f:
            h = f.read()
        expect(re.search(r"#define NUM_EXTRA_TMS\s+2\b", h) and "#define FIRST_EXTRA_TM_IDX ITEM_TM93" in h,
               "items.h does not count TM93 and TM94")
        expect(record(work, "TM93")["name"] == "TM93" and record(work, "TM94")["plural"] == "TM94s",
               "TM93 and TM94 have no records of their own")
        code, out = run("apply", "--list", FIXTURE, "--root", work)
        expect(code == 0 and "changed 0 files, removed 0" in out, f"a second apply changed something: {out}")

        # 4: the list loses TM94 and gets it back.
        short = os.path.join(tmp, "short.tsv")
        write_list(short, [e for e in entries if e[0] != "TM94"])
        code, out = run("apply", "--list", short, "--root", work)
        with open(os.path.join(work, tm.ITEMS_TXT), encoding="utf-8") as f:
            ids = f.read().split()
        expect(code == 0 and "ITEM_TM94" not in ids and not os.path.exists(os.path.join(work, tm.DATA, "tm94.json")),
               f"a list without TM94 left it: {out}")
        code, out = run("apply", "--list", FIXTURE, "--root", work)
        expect(code == 0 and record(work, "TM94")["teachesMove"] == dict(entries)["TM94"],
               f"TM94 did not come back: {out}")

        # 5: refusals.
        bad = [
            ([("TM01", "MOVE_TACKLE"), ("TM02", "MOVE_TACKLE")], "both teach"),
            ([("TM95", "MOVE_TACKLE")], "no gap"),
            ([("HM09", "MOVE_TACKLE")], "HMs run from"),
            ([("TM01", "MOVE_NOT_A_MOVE")], "is not a move"),
        ]
        for rows, why in bad:
            path = os.path.join(tmp, "bad.tsv")
            write_list(path, rows)
            code, out = run("apply", "--list", path, "--root", work, "--dry-run")
            expect(code == 1 and why in out, f"{rows} was not refused for {why!r}: {out.strip()}")

    if a.built_tree:
        proc = subprocess.run([sys.executable, os.path.join(HERE, "tm_items.py"), "check", "--list", FIXTURE,
                               "--root", a.built_tree], capture_output=True, text=True)
        expect(proc.returncode == 0 and "is the list" in proc.stdout,
               f"check on {a.built_tree}: {proc.stdout.strip()}{proc.stderr.strip()}")

    for f in failures:
        print("FAILED:", f)
    print(f"{len(failures)} failed" if failures else "passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
