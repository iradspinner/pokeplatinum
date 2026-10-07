#!/usr/bin/env python3
"""Write the TM list into the item records, and read it back from a ROM.

Platinum Oxide project, step 8 of docs/oxide/alpha-readiness.md. The TM pass
gives every TM and HM number a move (the Balance Agent's list, approved by
Ian); this makes the item records say so. It is rerun whenever the list
changes, which it will before step 10.

    python3 tools/oxide/tm_items.py apply --list LIST [--dry-run]
    python3 tools/oxide/tm_items.py check --list LIST [--rom ROM]

LIST is either a TSV with the columns tm and move (TM48 and MOVE_IRON_DEFENSE),
or the Markdown reward table (docs/oxide/reward-table.md), whose section
"## The TM list" has TM and Move columns with each move's in-game name.

What apply writes, in res/items/data/ and the two places that count TMs:

- Each listed TM or HM record's teachesMove. When the move changes, the
  record also takes the new move's description, rewrapped for the Bag's box
  (216 pixels by three lines, measured with textfit.py), and the TM disc's
  palette for the move's type. A description that will not fit is reported,
  and the record keeps its old one until someone writes one that does.
- A record for every TM past TM92 (ITEM_TM93 on), made from TM92's, and their
  ids in generated/items.txt, just before MAX_ITEMS, so no other item's id
  moves; and NUM_EXTRA_TMS and FIRST_EXTRA_TM_IDX in
  include/constants/items.h. Everything that counts TMs follows those two
  lines: the TM-to-move table (generated in item order by itemproc), the
  species learnset masks, the Bag's TM pocket. A list that shrinks takes the
  extra ids and records back out.
- A listed HM is a single-use TM, so its record no longer prevents tossing
  (the party menu uses it up like a TM).
- An unlisted number (Cut's HM01 and Rock Smash's HM06 in the list of
  2026-10-06) is left as it is: nothing places it.

Moving the TM count changes the Bag, which is save data, so a list with a
different number of TMs past TM92 costs a fresh game (save-change skill).
A TM keeps its number when its move changes, and a species' TM learnset
names TMs by number, so after a move change every species that lists the TM
learns the new move until the Balance Agent's compatibility lists catch up;
the two land together.

check reads the TM-to-move table out of a built ROM (its address from the
linker map beside the ROM) and requires it to be the list.
"""
import argparse
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DEFAULT = os.path.abspath(os.path.join(HERE, "..", ".."))

LAST_BASE_TM = 92
NUM_BASE_TMS = 92
NUM_HMS = 8
BAG_WIDTH, BAG_LINES = 216, 3
ITEMS_H = "include/constants/items.h"
ITEMS_TXT = "generated/items.txt"
DATA = "res/items/data"
# Fairy has no TM disc palette yet (res/items/icons has the seventeen
# Generation 4 types), so a Fairy TM takes Psychic's pink until one is drawn.
# Curse is the ??? type in Generation 4 and Ghost in the later games, so its
# disc is the Ghost one.
PALETTE_FALLBACK = {"fairy": "psychic", "mystery": "ghost"}


class ListError(Exception):
    pass


# ------------------------------------------------------------------ the list

def read_list(path):
    """[(label, move constant)] in the list's order, from a TSV or from the
    reward table's Markdown."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.endswith(".md"):
        if "## The TM list" not in text:
            raise ListError(f"{path} has no section '## The TM list'")
        sec = text[text.index("## The TM list"):]
        nxt = sec.find("\n## ", 5)
        sec = sec[:nxt] if nxt > 0 else sec
        rows = re.findall(r"^\| ((?:TM|HM)\d+) \| ([^|]+?) \|", sec, re.M)
        names = move_names()
        out = []
        for label, name in rows:
            if name not in names:
                raise ListError(f"{label}: no move is named {name!r}")
            out.append((label, names[name]))
        return out
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    head = [c.strip() for c in lines[0].split("\t")]
    if "tm" not in head or "move" not in head:
        raise ListError(f"{path}: the header needs tm and move columns")
    out = []
    for line in lines[1:]:
        rec = dict(zip(head, (c.strip() for c in line.split("\t"))))
        out.append((rec["tm"], rec["move"]))
    return out


def move_names(root=ROOT_DEFAULT):
    """{in-game name: MOVE_ constant}, from each move's own record; a name
    two moves share is left out, since it cannot say which is meant."""
    seen, out = {}, {}
    for d in sorted(os.listdir(os.path.join(root, "res", "moves"))):
        path = os.path.join(root, "res", "moves", d, "data.json")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            name = json.load(f).get("name")
        if name in seen:
            out.pop(name, None)
            continue
        seen[name] = d
        out[name] = "MOVE_" + d.upper()
    return out


def validate(entries, moves):
    """The list's labels and moves make sense: TMs numbered from TM01 with no
    gap past TM92, HMs within HM01 to HM08, every move real, none twice."""
    errors, seen_label, seen_move = [], set(), {}
    tms = []
    for label, move in entries:
        m = re.fullmatch(r"(TM|HM)(\d+)", label)
        if not m:
            errors.append(f"{label}: not a TM or HM number")
            continue
        n = int(m.group(2))
        if m.group(1) == "HM" and not 1 <= n <= NUM_HMS:
            errors.append(f"{label}: HMs run from HM01 to HM{NUM_HMS:02d}")
        if m.group(1) == "TM":
            tms.append(n)
        if label in seen_label:
            errors.append(f"{label} is listed twice")
        seen_label.add(label)
        if move not in moves:
            errors.append(f"{label}: {move} is not a move")
        if move in seen_move:
            errors.append(f"{label} and {seen_move[move]} both teach {move}")
        seen_move[move] = label
    extra = sorted(n for n in tms if n > LAST_BASE_TM)
    if extra and extra != list(range(LAST_BASE_TM + 1, extra[-1] + 1)):
        errors.append(f"the TMs past TM92 must run on with no gap: {['TM%02d' % n for n in extra]}")
    if errors:
        raise ListError("\n".join(errors))
    return len(extra)


# ------------------------------------------------------------------ the tree

class Tree:
    def __init__(self, root):
        self.root = root
        self.changed, self.removed = [], []
        self._text = {}

    def path(self, rel):
        return os.path.join(self.root, rel)

    def exists(self, rel):
        return (rel in self._text and self._text[rel] is not None) or \
            (rel not in self._text and os.path.exists(self.path(rel)))

    def read(self, rel):
        if rel not in self._text:
            with open(self.path(rel), encoding="utf-8", newline="") as f:
                self._text[rel] = f.read()
        return self._text[rel]

    def write(self, rel, text):
        old = self._text.get(rel) if rel in self._text else (self.read(rel) if os.path.exists(self.path(rel)) else None)
        if old != text:
            self._text[rel] = text
            if rel not in self.changed:
                self.changed.append(rel)

    def remove(self, rel):
        if self.exists(rel):
            self._text[rel] = None
            self.removed.append(rel)

    def flush(self):
        for rel in self.changed:
            if self._text.get(rel) is not None:
                with open(self.path(rel), "w", encoding="utf-8", newline="") as f:
                    f.write(self._text[rel])
        for rel in self.removed:
            os.remove(self.path(rel))


def dump_record(data, like):
    """An item record in the files' own style: two-space JSON, non-ASCII as
    it is, with a closing newline only where the old file had one."""
    text = json.dumps(data, indent=2, ensure_ascii=False)
    return text + ("\n" if like.endswith("\n") else "")


def move_record(tree, move):
    return json.loads(tree.read(f"res/moves/{move[len('MOVE_'):].lower()}/data.json"))


def bag_description(tree, move):
    """The move's own description, rewrapped for the Bag's box, or None when
    it does not fit there."""
    sys.path.insert(0, HERE)
    import textfit
    flat = " ".join("".join(move_record(tree, move)["description"]).replace("\n", " ").split())
    lines = textfit.wrap(flat, width=BAG_WIDTH)
    if len(lines) > BAG_LINES:
        return None
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def palette(tree, move):
    kind = move_record(tree, move)["type"][len("TYPE_"):].lower()
    kind = PALETTE_FALLBACK.get(kind, kind)
    icons = tree.path("res/items/icons")
    if not any(name.startswith(f"tm_{kind}.") or name.startswith(f"tm_{kind}_") for name in os.listdir(icons)):
        raise ListError(f"{move} is {kind}, and res/items/icons has no tm_{kind} disc palette")
    return f"tm_{kind}_NCLR"


# ------------------------------------------------------------------ apply

def apply(tree, entries):
    """Write the list. Returns the notes for the report."""
    moves = set(tree.read("generated/moves.txt").split())
    extra = validate(entries, moves)
    notes = []
    template_rel = f"{DATA}/tm{LAST_BASE_TM:02d}.json"
    template = json.loads(tree.read(template_rel))
    for label, move in entries:
        rel = f"{DATA}/{label.lower()}.json"
        if tree.exists(rel):
            text = tree.read(rel)
            data = json.loads(text)
        else:
            text = tree.read(template_rel)
            data = dict(template)
            data.update(name=label, plural=label + "s", article="a", gbaID="GBA_ITEM_NONE",
                        teachesMove="MOVE_NONE")
            notes.append(f"{label}: a new record, priced {data['price']} like TM{LAST_BASE_TM:02d}")
        if data.get("teachesMove") != move:
            desc = bag_description(tree, move)
            if desc is None:
                notes.append(f"{label}: {move}'s description does not fit the Bag's box in "
                             f"{BAG_LINES} lines of {BAG_WIDTH} pixels; the record keeps "
                             f"{data.get('teachesMove')}'s until one is written that does")
            else:
                data["description"] = desc
            data["teachesMove"] = move
            data["icon"] = dict(data["icon"], palette=palette(tree, move))
            if move_record(tree, move)["type"] == "TYPE_FAIRY":
                notes.append(f"{label}: a Fairy move, drawn with the Psychic disc until a Fairy one exists")
        # A listed HM is a single-use TM (standing rulings, 2026-09-28), so
        # it can be tossed like one.
        if label.startswith("HM"):
            data["preventToss"] = False
        tree.write(rel, dump_record(data, text))

    # The ids of the TMs past TM92, just before MAX_ITEMS so no other id moves.
    names = tree.read(ITEMS_TXT).split("\n")
    names = [n for n in names if not re.fullmatch(r"ITEM_TM(\d+)", n.strip())
             or int(n.strip()[len("ITEM_TM"):]) <= LAST_BASE_TM]
    at = names.index("MAX_ITEMS")
    names[at:at] = [f"ITEM_TM{n}" for n in range(LAST_BASE_TM + 1, LAST_BASE_TM + extra + 1)]
    tree.write(ITEMS_TXT, "\n".join(names))
    n = LAST_BASE_TM + extra + 1
    while tree.exists(f"{DATA}/tm{n}.json"):
        tree.remove(f"{DATA}/tm{n}.json")
        notes.append(f"TM{n}: its record removed, since the list stops at TM{n - 1}")
        n += 1

    text = tree.read(ITEMS_H)
    text = re.sub(r"(#define NUM_EXTRA_TMS\s+)\d+", lambda m: m.group(1) + str(extra), text)
    first = f"ITEM_TM{LAST_BASE_TM + 1}" if extra else "MAX_ITEMS"
    text = re.sub(r"(#define FIRST_EXTRA_TM_IDX )\w+", lambda m: m.group(1) + first, text)
    tree.write(ITEMS_H, text)
    return notes


# ------------------------------------------------------------------ check

def expected_table(entries, extra):
    """sTMHMMoves as itemproc lays it out: TM01 to TM92, HM01 to HM08, then
    the TMs past TM92. A number the list leaves out is None (not checked)."""
    by_label = dict(entries)
    table = [by_label.get(f"TM{n:02d}") for n in range(1, NUM_BASE_TMS + 1)]
    table += [by_label.get(f"HM{n:02d}") for n in range(1, NUM_HMS + 1)]
    table += [by_label.get(f"TM{n}") for n in range(LAST_BASE_TM + 1, LAST_BASE_TM + extra + 1)]
    return table


def check(tree, entries, rom_path):
    """Problems found reading the TM-to-move table out of the ROM."""
    moves_txt = tree.read("generated/moves.txt").split()
    extra = validate(entries, set(moves_txt))
    want = expected_table(entries, extra)
    xmap = os.path.join(os.path.dirname(os.path.abspath(rom_path)), "main.nef.xMAP")
    with open(xmap, encoding="utf-8", errors="replace") as f:
        m = re.search(r"^\s+([0-9A-F]{8}) ([0-9A-F]{8}) \.\w+\s+sTMHMMoves\s", f.read(), re.M)
    if not m:
        return [f"{xmap} does not place sTMHMMoves"]
    addr, size = int(m.group(1), 16), int(m.group(2), 16)
    if size != 2 * len(want):
        return [f"sTMHMMoves holds {size // 2} moves; the list needs {len(want)}"]
    import ndspy.rom
    arm9 = ndspy.rom.NintendoDSRom.fromFile(rom_path).loadArm9()
    sec = next(s for s in arm9.sections if s.ramAddress <= addr < s.ramAddress + len(s.data))
    got = struct.unpack_from(f"<{len(want)}H", sec.data, addr - sec.ramAddress)
    problems = []
    labels = [f"TM{n:02d}" for n in range(1, NUM_BASE_TMS + 1)] + \
             [f"HM{n:02d}" for n in range(1, NUM_HMS + 1)] + \
             [f"TM{n}" for n in range(LAST_BASE_TM + 1, LAST_BASE_TM + extra + 1)]
    for label, w, g in zip(labels, want, got):
        if w is not None and moves_txt[g] != w:
            problems.append(f"{label} teaches {moves_txt[g]} in the ROM, the list says {w}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=("apply", "check"))
    ap.add_argument("--list", required=True, help="the TM list: a tm/move TSV or the reward table's Markdown")
    ap.add_argument("--root", default=ROOT_DEFAULT)
    ap.add_argument("--rom", default="build/pokeplatinum.us.nds")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    tree = Tree(a.root)
    try:
        entries = read_list(a.list)
        if a.command == "apply":
            notes = apply(tree, entries)
            for n in notes:
                print(n)
            verb = "would change" if a.dry_run else "changed"
            print(f"{len(entries)} TMs and HMs; {verb} {len(tree.changed)} files, removed {len(tree.removed)}")
            if not a.dry_run:
                tree.flush()
            return 0
        problems = check(tree, entries, os.path.join(a.root, a.rom) if not os.path.isabs(a.rom) else a.rom)
    except ListError as e:
        print(e, file=sys.stderr)
        return 1
    for p in problems:
        print("FAIL:", p)
    print(f"{len(entries)} TMs and HMs, {len(problems)} problems"
          + (": the ROM's TM-to-move table is the list" if not problems else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
