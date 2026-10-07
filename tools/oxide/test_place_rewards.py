"""Check tools/oxide/place_rewards.py on a scratch copy of the tree.

The fixture, tools/oxide/test_place_rewards.tsv, is test data: the TM pass
draft's placements (docs/oxide/tm-pass-set.tsv on balance-learngen-v2) and a
few synthetic rows for the kinds the draft has none of. It is never a reward
table, and nothing here writes to the checkout.

    python3 tools/oxide/test_place_rewards.py [--built-tree DIR]

What it checks, without building a ROM:

1. Every row lands where it says, read back from the file that holds it.
2. A second apply changes nothing.
3. The trainer routine has one branch per trainer in the table and no other
   (a trainer with no row gets nothing and no flag), gives each trainer
   exactly its rows, and uses distinct spare flags that nothing else in the
   tree names; the five hooks are in and the movement block is aligned.
4. Each reward trainer keeps its flag when the table loses and regains
   other trainers, and a table with no trainer rows puts scripts_battles.s
   back byte for byte.
5. Bad rows are refused with their reason, a gauntlet trainer's reward among
   them.
6. The shop rows (tools/oxide/test_place_rewards_shops.tsv, test data too):
   a sold-once row lands in include/data/sold_tms.h with its badges, copies
   and a purchase bit of its own that survives the table losing and
   regaining rows; a prize takes the place and coin price of the one it
   replaces, or leaves the list; a second apply changes nothing.

With --built-tree DIR, a checkout where both fixtures were applied and the ROM
built (`place_rewards.py apply --table <fixture> --root DIR`, then `make -C
DIR rom`), it also reads every row back out of that ROM with `check
--rows-only` and requires each to be found exactly once.

Prints "passed" when every check passes.
"""
import argparse
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import place_rewards as pr  # noqa: E402

FIXTURE = os.path.join(HERE, "test_place_rewards.tsv")
SHOPS = os.path.join(HERE, "test_place_rewards_shops.tsv")
COPY = ["res/field/scripts", "res/field/events", "res/text", "res/items/data", "include",
        "generated", "src", "asm"]
BATTLES = "res/field/scripts/scripts_battles.s"

failures = []


def expect(ok, what):
    if not ok:
        failures.append(what)


def run(*argv):
    """place_rewards.main with its output captured: (exit code, output)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = pr.main(list(argv))
    return code, out.getvalue()


def table(path, rows, header=True):
    """A table of rows in the fixture's columns, which leave out the
    optional ones (badges)."""
    with open(path, "w", encoding="utf-8") as f:
        if header:
            f.write("\t".join(c for c in pr.COLUMNS if c not in pr.OPTIONAL_COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(r) + "\n")


def fixture_lines():
    with open(FIXTURE, encoding="utf-8") as f:
        return [l for l in f.read().splitlines() if l.strip() and not l.startswith("#")][1:]


def sold_tms(root):
    """{item: (badges, copies, bit)} as sold_tms.h lists them."""
    with open(os.path.join(root, pr.SOLD_TMS_H), encoding="utf-8") as f:
        return {m.group(1): (int(m.group(2)), int(m.group(3)), int(m.group(4)))
                for line in f.read().split("\n")
                if (m := pr.SOLD_LINE.match(line)) and m.group(1) != "ITEM_NONE"}


def block_branches(text):
    """{trainer: ([(item, count)], flag)} read from the routine's text."""
    out = {}
    begin, end = text.index(pr.BLOCK_BEGIN), text.index(pr.BLOCK_END)
    block = text[begin:end]
    dispatch = re.findall(r"GoToIfEq VAR_0x8004, (TRAINER_\w+), (\w+)", block)
    for trainer, label in dispatch:
        body = block[block.index(label + ":"):]
        body = body[:body.index("    Return")]
        flag = re.search(r"GoToIfSet (FLAG_\w+)", body).group(1)
        sets = re.findall(r"SetVar VAR_0x8004, (ITEM_\w+)\n    SetVar VAR_0x8005, (\d+)", body)
        gives = body.count("Common_GiveItemQuantity")
        items = sorted(dict.fromkeys((i, int(c)) for i, c in sets))
        expect(gives == len(items), f"{trainer}'s branch gives {gives} times for {len(items)} items")
        expect(f"SetFlag {flag}" in body, f"{trainer}'s branch does not set its own flag {flag}")
        out[trainer] = (items, flag)
    return out


def check_landed(tree_root, placements):
    """Read every row back with the tool's readers from the written files."""
    tree = pr.Tree(tree_root)
    visible, hidden, marts = pr.VisibleItems(tree), pr.HiddenItems(tree), pr.Marts(tree)
    for p in placements:
        if p.kind == "ball":
            objs = pr.Events(tree, p.header).data["object_events"]
            if p.tile:
                hits = [o for o in objs if (o["x"], o["z"]) == p.tile[:2]]
            elif p.place:
                hits = [o for o in objs if o.get("id") == p.place]
            else:
                hits = [o for o in objs if isinstance(o.get("script"), int)
                        and 7000 <= o["script"] < 8000 and visible.get(o["script"] - 7000)[0] == p.reward]
            got = [visible.get(o["script"] - 7000) for o in hits]
            expect(got == [(p.reward, p.copies)], f"{p}: the ball holds {got}")
        elif p.kind == "hidden":
            bgs = [b for b in pr.Events(tree, p.header).data["bg_events"] if b["type"] == pr.BG_HIDDEN_ITEM]
            if p.tile:
                flags = [hidden.flag(b["script"]) for b in bgs if (b["x"], b["z"]) == p.tile[:2]]
            elif p.place:
                flags = [p.place]
            else:
                flags = [hidden.flag(b["script"]) for b in bgs if hidden.get(hidden.flag(b["script"]))[0] == p.reward]
            got = [hidden.get(f) for f in flags]
            expect(got == [(p.reward, p.copies)], f"{p}: the hidden item holds {got}")
        elif p.kind == "gift":
            lines = tree.read(tree.script_rel(p.header)).split("\n")
            expect(pr.gift_sites(tree, lines, p.reward), f"{p}: the script gives no {p.reward}")
            if p.replaces != p.reward:
                expect(not pr.gift_sites(tree, lines, p.replaces), f"{p}: the script still gives {p.replaces}")
        elif p.kind == "mart":
            stock = marts.stock(p.place)
            expect(stock.count(p.reward) == 1, f"{p}: the mart sells {stock}")
            if p.replaces:
                expect(p.replaces not in stock, f"{p}: the mart still sells {p.replaces}")


def check_routine(tree_root, placements, original):
    """The trainer routine against the table, and the rest of the file."""
    tree = pr.Tree(tree_root)
    text = tree.read(BATTLES)
    branches = block_branches(text)
    want = {}
    for p in placements:
        if p.kind == "trainer":
            want.setdefault(p.trainer, []).append((p.reward, p.copies))
    expect(set(branches) == set(want), f"the routine's trainers {sorted(branches)} differ from the table's")
    for t, items in want.items():
        if t in branches:
            expect(branches[t][0] == sorted(items), f"{t} gives {branches[t][0]}, the table says {items}")
    flags = [f for _i, f in branches.values()]
    expect(len(set(flags)) == len(flags), f"reward flags repeat: {flags}")
    expect(all(pr.SPARE_STORY.fullmatch(f) for f in flags), f"a reward flag is not a spare story flag: {flags}")
    # No other file in the tree names a reward flag.
    for path in ["res/field/scripts", "res/field/events", "src", "include"]:
        for dirpath, _d, files in os.walk(os.path.join(tree_root, path)):
            for name in files:
                full = os.path.join(dirpath, name)
                if os.path.relpath(full, tree_root) == BATTLES or not name.endswith((".s", ".json", ".c", ".h")):
                    continue
                with open(full, encoding="utf-8", errors="replace") as f:
                    body = f.read()
                for flag in flags:
                    expect(not re.search(r"\b%s\b" % flag, body), f"{flag} is also named in {full}")
    hooks = text.count(f"{pr.HOOK_BEGIN}\n    Call {pr.CHAIN}")
    expect(hooks == 5, f"{hooks} hooks, not 5")
    expect(f"    .balign 4, 0\n{pr.HOOK_END}\nBattles_Movement_1252:" in text, "the movement block lost its .balign")
    expect(pr.strip_battles(text).rstrip("\n") == original.rstrip("\n"), "the rest of scripts_battles.s changed")
    return {t: f for t, (_i, f) in branches.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--built-tree", help="a checkout with the fixture applied and its ROM built")
    a = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, "tree")
        for rel in COPY:
            shutil.copytree(os.path.join(ROOT, rel), os.path.join(work, rel), symlinks=True)
        with open(os.path.join(work, BATTLES), encoding="utf-8") as f:
            original = f.read()

        tree = pr.Tree(work)
        placements = pr.resolve(tree, pr.read_table(FIXTURE))
        none = os.path.join(tmp, "no-roles.tsv")

        # 1 and 2: apply, read back, apply again.
        code, out = run("apply", "--table", FIXTURE, "--root", work, "--roles", none)
        expect(code == 0, f"apply failed: {out}")
        check_landed(work, placements)
        code, out = run("apply", "--table", FIXTURE, "--root", work, "--roles", none)
        expect(code == 0 and "wrote 0 files" in out, f"a second apply changed something: {out}")

        # 3: the routine.
        flags = check_routine(work, placements, original)

        # 4: flags survive the table losing and regaining trainers, and no
        # trainer rows at all restore the file.
        lines = fixture_lines()
        trainer_rows = [l for l in lines if l.split("\t")[2] == "trainer"]
        kept = trainer_rows[::2]
        part = os.path.join(tmp, "part.tsv")
        table(part, [l.split("\t") for l in kept])
        code, out = run("apply", "--table", part, "--root", work, "--roles", none)
        expect(code == 0, f"apply of half the trainers failed: {out}")
        half = check_routine(work, pr.resolve(pr.Tree(work), pr.read_table(part)), original)
        expect(all(half[t] == flags[t] for t in half), "a trainer's flag moved when others left the table")
        code, out = run("apply", "--table", FIXTURE, "--root", work, "--roles", none)
        again = check_routine(work, placements, original)
        expect(all(again[t] == flags[t] for t in half), "a trainer's flag moved when others came back")
        empty = os.path.join(tmp, "empty.tsv")
        table(empty, [])
        code, out = run("apply", "--table", empty, "--root", work, "--roles", none)
        with open(os.path.join(work, BATTLES), encoding="utf-8") as f:
            expect(f.read() == original, "a table with no trainer rows left scripts_battles.s changed")

        # 5: refusals, each on its own.
        bad = [
            (["ITEM_NOT_REAL", "1", "ball", "Roark", "MAP_HEADER_ROUTE_202", "", "ITEM_POTION", "", ""], "is not an item"),
            (["ITEM_TM10", "0", "ball", "Roark", "MAP_HEADER_ROUTE_202", "", "ITEM_POTION", "", ""], "copies"),
            (["ITEM_TM10", "1", "gift", "Roark", "MAP_HEADER_SANDGEM_TOWN", "", "", "", ""], "needs replaces"),
            (["ITEM_TM10", "1", "trainer", "Roark", "MAP_HEADER_ROUTE_202", "", "", "TRAINER_YOUNGSTER_MICHAEL", ""],
             "is not a sight or talk trainer on MAP_HEADER_ROUTE_202"),
            (["ITEM_TM10", "1", "trainer", "Roark", "MAP_HEADER_OREBURGH_CITY_GYM", "", "", "TRAINER_LEADER_ROARK", ""],
             "a map script battles them"),
            (["ITEM_TM10", "1", "ball", "Gardenia", "MAP_HEADER_ROUTE_204_NORTH", "LOCALID_ITEM_TM09", "ITEM_POTION", "", ""],
             "the ball holds"),
            (["ITEM_TM10", "1", "mart", "Roark", "", "common", "", "", ""], "MART_SPECIALTIES_ID_"),
            (["ITEM_TM10", "1", "gift", "Roark", "MAP_HEADER_ROUTE_202", "", "ITEM_TM48", "", ""], "gives no ITEM_TM48"),
        ]
        for row, why in bad:
            path = os.path.join(tmp, "bad.tsv")
            table(path, [row])
            code, out = run("apply", "--table", path, "--root", work, "--roles", none, "--dry-run")
            expect(code == 1 and why in out, f"row {row[:3]} was not refused for {why!r}: {out.strip()}")
        dup = fixture_lines()[0].split("\t")
        path = os.path.join(tmp, "dup.tsv")
        table(path, [dup, dup])
        code, out = run("apply", "--table", path, "--root", work, "--roles", none, "--dry-run")
        expect(code == 1 and "the same placement as line" in out, f"a repeated row was not refused: {out.strip()}")
        roles = os.path.join(tmp, "roles.tsv")
        with open(roles, "w", encoding="utf-8") as f:
            f.write("split\ttrainer_id\ttrainer\tmap\tobject\trequired\trole\tsection\treward\tcopies\n")
            f.write("Roark\tTRAINER_YOUNGSTER_MICHAEL\tMichael\tROUTE_203\t\tyes\tgauntlet\t1\t\t\n")
        code, out = run("apply", "--table", FIXTURE, "--root", work, "--roles", roles, "--dry-run")
        expect(code == 1 and "gauntlet trainer" in out, f"a gauntlet trainer's reward was not refused: {out.strip()}")

        # 6: the shops. A sold-once row goes into sold_tms.h with its badges,
        # copies and a bit of its own, kept across reruns; a prize takes the
        # place and coin price of the one it replaces, or leaves the list.
        code, out = run("apply", "--table", SHOPS, "--root", work, "--roles", none)
        expect(code == 0, f"apply of the shop rows failed: {out}")
        sold = sold_tms(work)
        expect(sorted(sold) == ["ITEM_TM02", "ITEM_TM05", "ITEM_TM23"]
               and sold["ITEM_TM05"][:2] == (3, 2) and sold["ITEM_TM02"][:2] == (4, 2)
               and sold["ITEM_TM23"][:2] == (5, 1), f"sold_tms.h holds {sold}")
        expect(len({bit for _b, _c, bit in sold.values()}) == 3, f"purchase bits repeat: {sold}")
        tree = pr.Tree(work)
        _lines, prizes = pr.Prizes(tree).entries()
        coins = {item: c for _l, item, c in prizes}
        expect("ITEM_SILK_SCARF" not in coins and "ITEM_TM74" not in coins and "ITEM_TM10" not in coins
               and coins.get("ITEM_TM02") == 15000 and coins.get("ITEM_TM45") == 6000,
               f"the prize list is {coins}")
        stock = pr.Marts(tree).stock("MART_SPECIALTIES_ID_VEILSTONE_3F_UP")
        expect("ITEM_TM23" in stock and "ITEM_TM54" not in stock, f"the 3F counter sells {stock}")
        code, out = run("apply", "--table", SHOPS, "--root", work, "--roles", none)
        expect(code == 0 and "wrote 0 files" in out, f"a second shop apply changed something: {out}")
        only = os.path.join(tmp, "only.tsv")
        with open(SHOPS, encoding="utf-8") as f:
            shop_lines = [l for l in f.read().splitlines() if l.strip() and not l.startswith("#")]
        with open(only, "w", encoding="utf-8") as f:
            f.write("\n".join([shop_lines[0]] + [l for l in shop_lines[1:] if l.startswith("ITEM_TM02\t")]) + "\n")
        run("apply", "--table", only, "--root", work, "--roles", none)
        run("apply", "--table", SHOPS, "--root", work, "--roles", none)
        expect(sold_tms(work)["ITEM_TM02"][2] == sold["ITEM_TM02"][2],
               "a sold TM's purchase bit moved when the others left the table and came back")

    # With a built tree: every row read back out of its ROM.
    if a.built_tree:
        for table_path in (FIXTURE, SHOPS):
            proc = subprocess.run([sys.executable, os.path.join(HERE, "place_rewards.py"), "check", "--rows-only",
                                   "--table", table_path], cwd=a.built_tree, capture_output=True, text=True)
            expect(proc.returncode == 0 and "every row found exactly once" in proc.stdout,
                   f"check of {os.path.basename(table_path)} on {a.built_tree}: "
                   f"{proc.stdout.strip()}{proc.stderr.strip()}")

    for f in failures:
        print("FAILED:", f)
    print(f"{len(failures)} failed" if failures else "passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
