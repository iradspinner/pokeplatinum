"""Run & Bun's trainers, read from Ian's sheet of its battles.

    PYTHONPATH=. python3 -m tools.oxide.balance.run_and_bun "Leader Roxanne"

The sheet (~/roms/balance-refs/run-and-bun-trainer-battles.xlsx, Ian's copy)
has one tab per split, in play order, and in each a block per trainer:

    B: location                      (a row with nothing in column A)
    A: Name        B: trainer
    A: Pokémon
                   B, C, D...: one species per column
    A: Level       one per column, as text with a trailing space
    A: Held Item
    A: Ability
    A: Nature
    A: Moves       first move per column, then three unlabelled rows

Species, moves and items are already spelled the way the calculator spells
them. The sheet has no IVs, EVs or trainer ids, so trainers are keyed by name
and IVs are left unset.
"""
import functools
import os
import sys

import openpyxl

from . import data

SHEET = os.path.join(data.REFS_DIR, "run-and-bun-trainer-battles.xlsx")
NOT_SPLITS = {"Dex", "Sprites"}
FIELDS = {"Level": "level", "Held Item": "item", "Ability": "ability", "Nature": "nature"}


def _cells(row):
    return [c.strip() if isinstance(c, str) else c for c in row]


@functools.lru_cache(maxsize=None)
def trainers():
    """Every trainer on the sheet, keyed by name, each with its split tab.
    A name that appears twice (a rematch, a doubles version) gets its
    tab-order number appended from the second on."""
    book = openpyxl.load_workbook(SHEET, read_only=True, data_only=True)
    out = {}
    for split_order, tab in enumerate(t for t in book.sheetnames if t not in NOT_SPLITS):
        location, current, expect_species, move_rows = None, None, False, 0
        for raw in book[tab].iter_rows(values_only=True):
            row = _cells(raw)
            label, rest = (row[0] if row else None), row[1:]
            values = [v for v in rest if v not in (None, "")]
            if not values and label in (None, ""):
                continue
            if label == "Name":
                name = values[0]
                key = name
                n = 2
                while key in out:
                    key, n = f"{name} ({n})", n + 1
                current = {"hack": "run_and_bun", "tr_id": None, "name": key,
                           "location": location, "split_tab": tab, "split_order": split_order,
                           "battle_type": "Doubles" if "[Double]" in name else "Singles",
                           "ai": None, "party": []}
                out[key] = current
                move_rows = 0
            elif label in ("Pokémon", "Pokemon"):
                expect_species = True
            elif label in (None, "") and expect_species and current is not None:
                # A double battle puts both trainers in one block with an
                # empty column between them, so each Pokemon is tied to its
                # column and every later row is read by the same columns.
                current["columns"] = [c for c, v in enumerate(rest) if v not in (None, "")]
                current["party"] = [
                    {"species": rest[c], "level": None, "item": None, "ability": None,
                     "nature": None, "ivs": None, "evs": None, "moves": [],
                     "sub_index": k, "mega": None}
                    for k, c in enumerate(current["columns"])]
                expect_species = False
            elif label in FIELDS and current is not None:
                for mon, v in _by_column(current, rest):
                    if v in (None, "", "-"):
                        continue
                    mon[FIELDS[label]] = int(v) if label == "Level" else v
            elif label == "Moves" and current is not None:
                move_rows = 4
                _add_moves(current, rest)
                move_rows -= 1
            elif label in (None, "") and move_rows and current is not None:
                _add_moves(current, rest)
                move_rows -= 1
            elif label in (None, "") and values:
                location, current = values[0], None
    return out


def _by_column(trainer, cells):
    return [(mon, cells[c] if c < len(cells) else None)
            for mon, c in zip(trainer["party"], trainer["columns"])]


def _add_moves(trainer, cells):
    for mon, v in _by_column(trainer, cells):
        if v not in (None, "", "-"):
            mon["moves"].append(v)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ts = trainers()
    for name in argv or [n for n in ts if n.startswith(("Leader", "Elite Four", "Champion"))]:
        t = ts[name]
        print(f"{t['split_tab']:20} {name} ({t['location']})")
        for m in t["party"]:
            print(f"    {m['species']:16} {str(m['level']):>3} {str(m['item']):16} "
                  f"{str(m['ability']):14} {str(m['nature']):8} {', '.join(m['moves'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
