#!/usr/bin/env python3
"""Read Hardlove Gold's move tables.

The move data survived hg-engine's expansion better than the species data did.
It is still a 16-byte record in `a/0/1/1`, still Platinum's field order, and the
ids still line up with Platinum's for 0..467, so a move can be read with
Platinum's own enums and almost every field carried straight across. Two fields
are not Platinum's, and this module is where that knowledge lives:

  * `range` is a bitmask in the donor where Platinum has an enum index, so it
    goes through `range_to_platinum` on the way in.
  * `effect` agrees with Platinum for 0..276 and then continues up to 406 with
    effects hg-engine added, which Platinum has no battle script for.

`docs/oxide/donor-move-tables.md` has the evidence for every claim above; read
it before trusting a number out of here.

Nothing here writes. It sits on `donor.py` and deliberately does not touch it,
so the two can be worked on separately.

    python3 tools/oxide/donor_moves.py            # summary
    python3 tools/oxide/donor_moves.py --move 85  # one record
"""

import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import donor  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MSGENC = os.path.join(ROOT, "build", "tools", "msgenc", "msgenc")
CHARMAP = os.path.join(ROOT, "tools", "msgenc", "charmap.txt")

NARC_MOVE_DATA = "a/0/1/1"       # 924 members, 16 bytes each

# Text banks in a/0/2/7. 923 entries each, one per move id 0..922; the data
# archive has one more record than that and nothing names it.
TEXT_MOVE_DESCRIPTIONS = 749
TEXT_MOVE_NAMES = 750
TEXT_MOVE_NAMES_UPPER = 751
TEXT_MOVES_USED_IN_BATTLE = 3    # 2769 entries, three per move

MOVE_RECORD_SIZE = 16
NUM_MOVE_RECORDS = 924           # members of a/0/1/1
NUM_MOVES = 923                  # named ids, 0..922

# Platinum's own numbers, for the "does the donor need this or does Oxide
# already have it" question that the whole import turns on.
PLATINUM_MOVES = 468             # MOVE_NONE plus 467
PLATINUM_BATTLE_EFFECTS = 277

# 468, 469 and 470 are the three inaccessible tail records the retail game
# ships and pokeplatinum reproduces in moveproc.c's pack_extra_moves(). The
# donor kept them and started its own moves at 471.
FIRST_NEW_MOVE = 471
PLACEHOLDER_MOVES = (468, 469, 470)

# As in the species record, hg-engine put Fairy in the dead TYPE_MYSTERY slot.
# Platinum's own Curse legitimately has type 9 meaning Mystery, so the
# substitution is only ever valid on a donor record.
DONOR_TYPE_FAIRY = 9
OXIDE_TYPE_FAIRY = 18

CLASS_NAMES = ("physical", "special", "status")


class DonorMoves:
    def __init__(self, path=donor.DEFAULT_ROM, rom=None):
        self.donor = rom if rom is not None else donor.Donor(path)
        self._text = {}

    # ------------------------------------------------------------- records
    def count(self):
        """Records in a/0/1/1. Note this is one more than the number of named
        moves; see NUM_MOVES."""
        return len(self.donor.narc(NARC_MOVE_DATA))

    def move(self, index):
        """One move record. Field order and widths are Platinum's MoveTable
        exactly, including the two padding bytes at 0x0E, which are zero in all
        924 records: hg-engine did not widen this table, it only lengthened it.

        `range` is returned raw, as the donor's bitmask. `range_platinum` is the
        same value as a Platinum RANGE_* index, or None when the donor packed
        more than one bit and Platinum has no single value for it."""
        b = self.donor.narc(NARC_MOVE_DATA)[index]
        (effect, cls, power, mtype, accuracy, pp, chance,
         rng, priority, flags, contest_effect, contest_type) = struct.unpack("<HBBBBBBHbBBB", b[0:14])
        return {
            "effect": effect,
            "class": cls,
            "power": power,
            "type": mtype,
            "accuracy": accuracy,
            "pp": pp,
            "effect_chance": chance,
            "range": rng,
            "range_platinum": range_to_platinum(rng),
            "priority": priority,
            "flags": flags,
            "contest_effect": contest_effect,
            "contest_type": contest_type,
            "padding": b[14:16],
        }

    def moves(self):
        return [self.move(i) for i in range(self.count())]

    def is_placeholder(self, index):
        """True for the three retail tail records the donor inherited, which
        have no name and a "--" description."""
        return index in PLACEHOLDER_MOVES

    def new_move_ids(self):
        """The ids Hardlove added on top of Platinum's range, named ones only."""
        return [i for i in range(FIRST_NEW_MOVE, NUM_MOVES)]

    # ---------------------------------------------------------------- text
    def _bank(self, index, msgenc, charmap):
        if index not in self._text:
            self._text[index] = self.donor.text_bank(index, msgenc, charmap)
        return self._text[index]

    def names(self, msgenc=MSGENC, charmap=CHARMAP):
        return [_flatten(m) for m in self._bank(TEXT_MOVE_NAMES, msgenc, charmap)]

    def names_upper(self, msgenc=MSGENC, charmap=CHARMAP):
        return [_flatten(m) for m in self._bank(TEXT_MOVE_NAMES_UPPER, msgenc, charmap)]

    def descriptions(self, msgenc=MSGENC, charmap=CHARMAP):
        """One description per move id. Each is the list of lines msgenc gives
        back, because the line breaks are the game's own wrapping and res/moves
        stores them that way too."""
        out = []
        for m in self._bank(TEXT_MOVE_DESCRIPTIONS, msgenc, charmap):
            out.append(m if isinstance(m, list) else [m])
        return out


def range_to_platinum(value):
    """The donor's range field as a Platinum RANGE_* index, or None.

    Platinum numbers its ranges 0..16 in a plain enum. The donor's values are
    0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 and one combination, 24,
    which is the giveaway: this is a bitmask where bit n-1 stands for Platinum's
    range n, and 0 still means a single target. 24 is 8|16, all-adjacent plus
    the user, and Platinum has no single range for that."""
    if value == 0:
        return 0
    if value & (value - 1):
        return None              # more than one bit, no Platinum equivalent
    return value.bit_length()


def platinum_to_range(index):
    """The inverse, for writing a donor-shaped value back out."""
    return 0 if index == 0 else 1 << (index - 1)


def type_to_oxide(value):
    """A donor type id as an Oxide one. Only ever call this on a donor record:
    Platinum's own Curse really is type 9, TYPE_MYSTERY."""
    return OXIDE_TYPE_FAIRY if value == DONOR_TYPE_FAIRY else value


def _flatten(message):
    if isinstance(message, list):
        return "".join(message)
    return message or ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rom", default=donor.DEFAULT_ROM)
    ap.add_argument("--msgenc", default=MSGENC)
    ap.add_argument("--charmap", default=CHARMAP)
    ap.add_argument("--move", type=int, action="append",
                    help="print one move id in full; may be repeated")
    ap.add_argument("--no-text", action="store_true",
                    help="skip the name and description banks (they need a built msgenc)")
    a = ap.parse_args()

    dm = DonorMoves(a.rom)
    recs = dm.moves()
    names = None if a.no_text else dm.names(a.msgenc, a.charmap)
    descs = None if a.no_text else dm.descriptions(a.msgenc, a.charmap)

    def name_of(i):
        if names is None or i >= len(names):
            return f"<{i}>"
        return names[i]

    if a.move:
        for i in a.move:
            r = dm.move(i)
            print(f"{i} {name_of(i)}")
            for k, v in r.items():
                print(f"    {k:<16} {v}")
            if descs is not None and i < len(descs):
                print("    description")
                for line in descs[i]:
                    print("        " + line.rstrip("\n"))
        return

    print(f"move records in {NARC_MOVE_DATA}: {len(recs)} of {MOVE_RECORD_SIZE} bytes")
    if names is not None:
        print(f"named move ids: {len(names)} (0..{len(names) - 1})")
        print(f"description entries: {len(descs)}")
    widened = [i for i, r in enumerate(recs) if r["padding"] != b"\x00\x00"]
    print(f"records using the two padding bytes at 0x0E: {len(widened)}")

    new = dm.new_move_ids()
    print(f"new move ids above Platinum's range: {len(new)} ({new[0]}..{new[-1]}), "
          f"plus the {len(PLACEHOLDER_MOVES)} retail tail records {PLACEHOLDER_MOVES}")

    known = [i for i in new if recs[i]["effect"] < PLATINUM_BATTLE_EFFECTS]
    unknown = [i for i in new if recs[i]["effect"] >= PLATINUM_BATTLE_EFFECTS]
    print(f"new moves whose effect Platinum already has: {len(known)} "
          f"({len(set(recs[i]['effect'] for i in known))} distinct)")
    print(f"new moves whose effect Platinum lacks:       {len(unknown)} "
          f"({len(set(recs[i]['effect'] for i in unknown))} distinct)")
    print(f"highest effect id in the donor: {max(r['effect'] for r in recs)}")

    fairy = [i for i in new if recs[i]["type"] == DONOR_TYPE_FAIRY]
    print(f"new moves typed Fairy (donor type {DONOR_TYPE_FAIRY}): {len(fairy)}")

    odd = sorted(set(r["range"] for r in recs if range_to_platinum(r["range"]) is None))
    print(f"range values with no single Platinum equivalent: {odd}")

    print()
    print("spot checks")
    for i in (1, 33, 85, 63, 144, 467, 471, NUM_MOVES - 1):
        r = recs[i]
        cls = CLASS_NAMES[r["class"]] if r["class"] < len(CLASS_NAMES) else r["class"]
        print(f"  {i:>4} {name_of(i):<20} type {r['type']:>2} {cls:<8} "
              f"pow {r['power']:>3} acc {r['accuracy']:>3} pp {r['pp']:>2} "
              f"effect {r['effect']:>3} range {r['range']:>4} prio {r['priority']:>2} "
              f"flags 0x{r['flags']:02x}")


if __name__ == "__main__":
    main()
