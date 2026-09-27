"""Reads a Platinum Oxide save file: the trainer, the party and the PC boxes,
for the Calc tab's save features (Ian's plan, steps 1 to 5, 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.encounters.cli save PATH

Read-only. The file is read whole in one call and never written, locked or
kept open, because the save it reads is Ian's own, beside the ROM he plays.

The layout is found, not assumed. A save holds two copies of the game's data,
the primary at 0 and the backup at 0x40000, each two blocks laid end to end:
the normal block (the trainer, the party, the Pokedex and everything else)
and the PC boxes. Each block ends in a footer (src/savedata.c): the save
counter, the block's own counter, its size, the signature 0x20060623, its id
and a CRC16 of the block. So the reader scans for the signature, keeps each
footer whose CRC is right, and takes per block the valid copy the game would
load, the one saved last. Oxide's larger Pokedex grew the normal block by 240
bytes (docs/oxide/save-layout.md), which moved the box block, and element 8's
30 boxes will grow the box block; the footers carry both, so neither needs a
change here. That is also why a calculator reader with vanilla's fixed offsets
finds no boxes in an Oxide save.

A Pokemon is Platinum's 136-byte record (236 in the party): four 32-byte
blocks shuffled by personality and encrypted, laid out as
include/struct_defs/pokemon.h has them, with Oxide's two changes: the ability
is a u16 at block B 0x1A, and block A 0x0D bit 0 marks the hidden ability.

Which build a save came from is not recorded in it, so `build_era` reads the
signs it leaves: the block sizes (vanilla's, or Oxide's since the Pokedex
grew on 2026-09-21), a move id past vanilla's 467 (element 4, 2026-09-22),
and an ability in the old place (a save from before element 2, 2026-09-20).
A record that fails its checksum, or an id past today's tables, is reported
as a mismatch with this build rather than shown as something it is not.
"""
import csv
import functools
import json
import os
import struct

from . import dex
from . import model
from . import pokedex

SIGNATURE = 0x20060623
FOOTER_SIZE = 20            # SaveBlockFooter: counters, size, signature, id, CRC
BACKUP_START = 0x40000      # BACKUP_SECTOR_START * SAVE_SECTOR_SIZE
BLOCK_NORMAL, BLOCK_BOXES = 0, 1
BOX_RECORD, PARTY_RECORD = 136, 236
MONS_PER_BOX = 30
# PCBoxes is a u32, then per box 30 records, a 20-character name and a
# wallpaper byte, then one byte of unlocked wallpapers.
BOX_STRIDE = MONS_PER_BOX * BOX_RECORD + 20 * 2 + 1
# In the normal block: the trainer's id and secret id, and the Party struct
# (capacity, count, six records), where vanilla Platinum has them. The reader
# checks both rather than trusting them: the capacity must be 6, and the
# party's own trainer ids must include the save's.
TRAINER_ID_AT = 0x78
PARTY_AT = 0x98
VANILLA_MOVES = 467
# The block sizes each era of the game saves with, largest change last.
KNOWN_LAYOUTS = {
    # Oxide's builds kept these until the Pokedex grew: a save from 2026-09-20
    # has them with its abilities already in Oxide's place.
    (0xCF2C, 0x121E4): "vanilla Platinum's, which Oxide kept until 2026-09-21",
    (0xD01C, 0x121E4): "Oxide's since the Pokedex grew to 655 species (2026-09-21)",
}
# BoxPokemon_GetDataBlock: for each shuffle case, the position of blocks
# A, B, C and D. Cases 24 to 31 repeat 0 to 7.
BLOCK_POSITIONS = [
    (0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3), (0, 3, 1, 2), (0, 2, 3, 1), (0, 3, 2, 1),
    (1, 0, 2, 3), (1, 0, 3, 2), (2, 0, 1, 3), (3, 0, 1, 2), (2, 0, 3, 1), (3, 0, 2, 1),
    (1, 2, 0, 3), (1, 3, 0, 2), (2, 1, 0, 3), (3, 1, 0, 2), (2, 3, 0, 1), (3, 2, 0, 1),
    (1, 2, 3, 0), (1, 3, 2, 0), (2, 1, 3, 0), (3, 1, 2, 0), (2, 3, 1, 0), (3, 2, 1, 0),
]
NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed",
           "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild",
           "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]


class SaveError(ValueError):
    """The file is not a save this reader can make sense of."""


# -- the file's layout ------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _crc_table():
    table = []
    for i in range(256):
        crc = i << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else (crc << 1)
        table.append(crc & 0xFFFF)
    return table


def crc16(data):
    """MATH_CalcCRC16CCITT as CalcCRC16Checksum uses it: CCITT from 0xFFFF."""
    table, crc = _crc_table(), 0xFFFF
    for b in data:
        crc = ((crc << 8) & 0xFFFF) ^ table[((crc >> 8) ^ b) & 0xFF]
    return crc


def footers(data):
    """Every block footer in the file, valid or not, in file order."""
    out = []
    for pos in range(12, len(data) - 8, 4):
        if struct.unpack_from("<I", data, pos)[0] != SIGNATURE:
            continue
        at = pos - 12
        save_counter, block_counter, size = struct.unpack_from("<III", data, at)
        end = at + FOOTER_SIZE
        start = end - size
        entry = {"at": at, "start": start, "size": size, "block": data[at + 16],
                 "save_counter": save_counter, "block_counter": block_counter,
                 "copy": "primary" if start < BACKUP_START else "backup"}
        entry["valid"] = (0 <= start < at
                          and crc16(data[start:at]) == struct.unpack_from("<H", data, at + 18)[0])
        out.append(entry)
    return out


def blocks(data):
    """{block id: the footer of the copy the game would load}: the valid copy
    saved last, by save counter and then the block's own counter."""
    best = {}
    for f in footers(data):
        if not f["valid"]:
            continue
        key = (f["save_counter"], f["block_counter"])
        if f["block"] not in best or key > (best[f["block"]]["save_counter"],
                                            best[f["block"]]["block_counter"]):
            best[f["block"]] = f
    return best


# -- one Pokemon ------------------------------------------------------------------

def _decode(data, seed):
    """EncodeData/DecodeData: each u16 xored with the LCRNG's high half."""
    words = list(struct.unpack(f"<{len(data) // 2}H", data))
    for i in range(len(words)):
        seed = (seed * 0x41C64E6D + 0x6073) & 0xFFFFFFFF
        words[i] ^= seed >> 16
    return struct.pack(f"<{len(words)}H", *words)


@functools.lru_cache(maxsize=1)
def _tables():
    """Today's id lists, and what the reader shows for each id."""
    root = model.repo_root()

    def ids(name):
        # The move and item lists end in a MAX_ count, which is not an id.
        with open(os.path.join(root, "generated", f"{name}.txt"), encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("MAX_")]

    moves = pokedex.moves(root)
    with open(os.path.join(root, "res", "text", "location_names.json"), encoding="utf-8") as f:
        places = [m.get("en_US") or "" for m in json.load(f)["messages"]]
    rates = {}
    with open(os.path.join(root, "res", "pokemon", ".shared", "exp_tables.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for k, v in row.items():
                if k != "level":
                    rates.setdefault(k, []).append(int(v))
    tidy = lambda c, p: c[len(p):].replace("_", " ").title() if c.startswith(p) else c
    return {
        "species": ids("species"), "moves": ids("moves"), "abilities": ids("abilities"),
        "items": ids("items"), "move_names": {c: r["name"] for c, r in moves.items()},
        "places": places, "exp": rates, "tidy": tidy,
    }


def _level(species, exp):
    """A boxed Pokemon's level, from its experience and its species' curve."""
    rec = pokedex.load(model.repo_root(), species) or {}
    # pokedex.load keeps the rate without its EXP_RATE_ prefix (MEDIUM_SLOW).
    rate = (rec.get("exp_rate") or "MEDIUM_FAST").replace("EXP_RATE_", "").lower()
    curve = _tables()["exp"].get(rate) or _tables()["exp"]["medium_fast"]
    level = 1
    for lv in range(1, 101):
        if curve[lv] <= exp:
            level = lv
    return level


def read_mon(raw, where):
    """One record decoded, or None for an empty slot. `where` says which slot,
    for the report. `problems` lists anything that says the record was written
    by another build or is corrupt, rather than guessing past it."""
    pv, _flags, checksum = struct.unpack_from("<IHH", raw, 0)
    if not any(raw[:BOX_RECORD]):
        return None
    plain = _decode(raw[8:BOX_RECORD], checksum)
    pos = BLOCK_POSITIONS[((pv & 0x3E000) >> 13) % 24]
    a, b, c, d = (plain[32 * p:32 * p + 32] for p in pos)
    species_id, item_id, ot_id, exp = struct.unpack_from("<HHII", a, 0)
    # An empty slot is not zero bytes: BoxPokemon_Init clears the record and
    # then encrypts it, so it decrypts to zeros with a checksum of 0.
    if species_id == 0 and checksum == 0 and pv == 0:
        return None
    t = _tables()
    problems = []
    if sum(struct.unpack("<64H", plain)) & 0xFFFF != checksum:
        problems.append("its checksum fails")
    moves = [m for m in struct.unpack_from("<4H", b, 0) if m]
    ivs = struct.unpack_from("<I", b, 0x10)[0]
    form = b[0x18] >> 3
    ability_id = struct.unpack_from("<H", b, 0x1A)[0]
    met = struct.unpack_from("<H", b, 0x1E)[0]

    def name(kind, i, prefix):
        seq = t[kind]
        if i >= len(seq):
            problems.append(f"{kind[:-1] if kind != 'species' else 'species'} id {i} is past this build's {len(seq) - 1}")
            return f"#{i}"
        return seq[i]

    species = name("species", species_id, "SPECIES_")
    mon = {
        "slot": where, "personality": pv, "species_id": species_id, "species": species,
        "name": dex.display_name(species) if species.startswith("SPECIES_") else species,
        "form": form, "is_egg": bool(ivs >> 30 & 1),
        "item": t["tidy"](name("items", item_id, "ITEM_"), "ITEM_") if item_id else None,
        "ot_id": ot_id & 0xFFFF, "ot_secret": ot_id >> 16, "exp": exp,
        "nature": NATURES[pv % 25],
        "ability": t["tidy"](name("abilities", ability_id, "ABILITY_"), "ABILITY_"),
        "ability_id": ability_id, "hidden_ability": bool(a[0x0D] & 1),
        "old_ability_byte": a[0x0D] >> 1,
        "move_ids": moves,
        "moves": [t["move_names"].get(name("moves", m, "MOVE_"), f"#{m}") for m in moves],
        "ivs": [ivs >> (5 * i) & 31 for i in range(6)],
        "evs": list(a[0x10:0x16]),
        "met_location": t["places"][met] if met < len(t["places"]) else f"#{met}",
        "met_level": d[0x1C] & 0x7F, "ball": d[0x1B],
    }
    if len(raw) >= PARTY_RECORD:
        stats = _decode(raw[BOX_RECORD:PARTY_RECORD], pv)
        mon["level"] = stats[4]
        mon["hp"] = struct.unpack_from("<HH", stats, 6)
    elif species.startswith("SPECIES_"):
        mon["level"] = _level(species, exp)
    mon["problems"] = problems
    return mon


# -- the whole save ---------------------------------------------------------------

def read(path):
    """The save at `path`, read once: its layout, trainer, party and boxes."""
    with open(path, "rb") as f:
        data = f.read()
    return parse(data, path)


def parse(data, path="(memory)"):
    found = blocks(data)
    if BLOCK_NORMAL not in found:
        raise SaveError(f"{path}: no valid copy of the normal block; not a Platinum save, "
                        f"or one never saved")
    normal = found[BLOCK_NORMAL]
    n0 = normal["start"]
    tid, sid = struct.unpack_from("<HH", data, n0 + TRAINER_ID_AT)
    capacity, count = struct.unpack_from("<ii", data, n0 + PARTY_AT)
    if capacity != 6 or not 0 <= count <= 6:
        raise SaveError(f"{path}: the party is not where Platinum keeps it "
                        f"(capacity {capacity}, count {count})")
    party = []
    for i in range(count):
        at = n0 + PARTY_AT + 8 + i * PARTY_RECORD
        mon = read_mon(data[at:at + PARTY_RECORD], f"party {i + 1}")
        if mon:
            party.append(mon)
    boxes, box_count, current_box = [], 0, None
    if BLOCK_BOXES in found:
        bx = found[BLOCK_BOXES]
        body = bx["size"] - FOOTER_SIZE
        box_count = (body - 5) // BOX_STRIDE
        current_box = struct.unpack_from("<I", data, bx["start"])[0]
        for i in range(box_count * MONS_PER_BOX):
            at = bx["start"] + 4 + i * BOX_RECORD
            mon = read_mon(data[at:at + BOX_RECORD],
                           f"box {i // MONS_PER_BOX + 1} slot {i % MONS_PER_BOX + 1}")
            if mon:
                mon["box"], mon["box_slot"] = i // MONS_PER_BOX + 1, i % MONS_PER_BOX + 1
                boxes.append(mon)
    save = {
        "path": path, "size": len(data),
        "blocks": {k: {x: v[x] for x in ("copy", "start", "size", "save_counter", "block_counter")}
                   for k, v in found.items()},
        "footers": footers(data),
        "trainer_id": tid, "secret_id": sid,
        "party": party, "boxes": boxes, "box_count": box_count, "current_box": current_box,
    }
    save["era"] = build_era(save)
    return save


def build_era(save):
    """What the save says about the build that wrote it, and any sign that it
    does not match this one: {"layout", "signs": [...], "mismatches": [...]}."""
    sizes = (save["blocks"].get(BLOCK_NORMAL, {}).get("size"),
             save["blocks"].get(BLOCK_BOXES, {}).get("size"))
    layout = KNOWN_LAYOUTS.get(sizes)
    signs, mismatches = [], []
    mons = save["party"] + save["boxes"]
    if layout:
        signs.append(f"block sizes {sizes[0]:#x} and {sizes[1]:#x} are {layout}")
    else:
        mismatches.append(f"block sizes {sizes[0]:#x} and {sizes[1] or 0:#x} match no known "
                          f"layout; read by their footers")
    if any(m for mon in mons for m in mon["move_ids"] if m > VANILLA_MOVES):
        signs.append("a move id past vanilla's 467: element 4's moves (2026-09-22 or later)")
    elif mons:
        signs.append("no move id past vanilla's 467 (any build; element 4 came on 2026-09-22)")
    if mons and all(mon["ability_id"] == 0 for mon in mons if not mon["is_egg"]):
        mismatches.append("every ability is 0 in Oxide's place: a save from before element 2 "
                          "(2026-09-20), whose abilities this build cannot read")
    if any(mon["hidden_ability"] for mon in mons):
        signs.append("a Pokemon with its hidden ability (element 8)")
    party_ids = {(mon["ot_id"], mon["ot_secret"]) for mon in save["party"]}
    if save["party"] and (save["trainer_id"], save["secret_id"]) not in party_ids:
        mismatches.append("no Pokemon in the party carries the save's trainer id; the trainer "
                          "or the party may not be where this reader looks")
    for mon in mons:
        for p in mon["problems"]:
            mismatches.append(f"{mon['slot']}: {p}")
    return {"layout": layout, "signs": signs, "mismatches": mismatches}


def describe(mon):
    """One line for a Pokemon, as `cli save` prints it."""
    if mon["is_egg"]:
        return f"{mon['slot']}: an egg"
    bits = [f"{mon['name']}" + (f" (form {mon['form']})" if mon["form"] else ""),
            f"Lv {mon.get('level', '?')}", mon["nature"],
            mon["ability"] + (" (hidden)" if mon["hidden_ability"] else "")]
    if mon["item"]:
        bits.append(f"holding {mon['item']}")
    bits.append(", ".join(mon["moves"]) or "no moves")
    bits.append(f"met at {mon['met_location']} at level {mon['met_level']}")
    return f"{mon['slot']}: " + "; ".join(bits)
