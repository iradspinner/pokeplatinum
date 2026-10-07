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
bytes (docs/oxide/save-layout.md), which moved the box block, and the 30 PC
boxes (2026-09-29) grew the box block from 18 boxes to 30; the footers carry
both, so the reader counts the boxes from the block's size. That is also why
a calculator reader with vanilla's fixed offsets finds no boxes in an Oxide
save.

A Pokemon is Platinum's 136-byte record (236 in the party): four 32-byte
blocks shuffled by personality and encrypted, laid out as
include/struct_defs/pokemon.h has them, with Oxide's changes: the ability is a
u16 at block B 0x1A, and block A 0x0D holds the hidden-ability bit (bit 0),
and since element 7 the Ability Capsule's swap (bit 1) and a Bottle Cap's
Hyper Training, one bit per stat (bits 2 to 7). Block B 0x19 holds a Mint's
nature, one more than its index, or 0.

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
# PCBoxes is a u32 (the current box), then every box's 30 records, then
# every box's 20-character name, then every box's wallpaper byte, then one
# byte of unlocked wallpapers; so each box adds this many bytes, and the
# block's size gives the count (18 in vanilla, 30 in Oxide since 2026-09-29).
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
    # Meloetta (2026-09-27) left it as it was: the arrays sized by the
    # species count are held at their size.
    (0xD01C, 0x121E4): "Oxide's from the Pokedex's growth (2026-09-21) until element 7",
    # Element 7 widened three Bag pockets (2026-09-28), 184 bytes, and the
    # Bag comes before the variables and flags, so they moved too.
    (0xD0D4, 0x121E4): "Oxide's from element 7's Bag (2026-09-28) until the 30 boxes",
    # The 30 PC boxes (2026-09-29), with the same fresh start as element 7:
    # the normal block is unchanged, and the box block keeps its shape.
    (0xD0D4, 0x1E310): "Oxide's since the 30 PC boxes (2026-09-29)",
}
# The layout this build writes. A save on an older one still gives its party
# (before the Bag) and its boxes (found by their footers), but its variables
# and flags sit where an older build put them, and a layout change costs a
# new game, not a converter (Ian, 2026-09-28). Only the normal block's size
# decides that: an 18-box save from element 7's builds reads in full.
CURRENT_LAYOUT = (0xD0D4, 0x1E310)
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
# enum PokemonStat's order, which the IVs are stored in and the Hyper
# Training bits follow.
STATS = ["HP", "Atk", "Def", "Spe", "SpA", "SpD"]
MAX_IV = 31


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
    """Every block footer in the file, valid or not, in file order. The battle
    log's footers carry the same signature but are laid out differently; they
    are the battle log reader's (battlelog.py), and are left out here."""
    from . import battlelog
    log_footers = battlelog.footer_positions(data)
    out = []
    for pos in range(12, len(data) - 8, 4):
        if struct.unpack_from("<I", data, pos)[0] != SIGNATURE or pos in log_footers:
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


def _entry_body(size):
    """SaveTableEntry_BodySize: an entry's size rounded past the next multiple
    of four, plus four, which is how far apart the save table lays entries."""
    size += 4 - size % 4
    return size + 4


def _c_value(name, defines, consts, depth=0):
    """A #define's value as the compiler would work it out: another define,
    an item constant, or arithmetic over them. Element 7 (2026-09-28) made
    TMHM_POCKET_SIZE the expression NUM_TMHMS, which a reader taking only
    numbers dropped, and that put the variables 400 bytes early."""
    import re
    if depth > 20:
        raise SaveError(f"{name}: the defines loop")
    if name in consts:
        return consts[name]
    expr = defines.get(name)
    if expr is None:
        if re.fullmatch(r"\d+|0x[0-9a-fA-F]+", name):
            return int(name, 0)
        raise SaveError(f"{name}: not a define this reader can resolve")
    expr = re.sub(r"[A-Za-z_]\w*", lambda m: str(_c_value(m.group(0), defines, consts, depth + 1)), expr)
    if not re.fullmatch(r"[\d\s()+\-*]+", expr):
        raise SaveError(f"{name}: '{defines[name]}' is not arithmetic this reader can work out")
    return eval(expr, {"__builtins__": {}})


@functools.lru_cache(maxsize=1)
def _vars_layout():
    """Where VarsFlags sits in the normal block, and what the level-cap split
    variable means, from this build's own source: the save table puts the
    party, then the bag, then the variables and flags (src/savedata/
    save_table.c); the bag's pockets are include/bag.h's; the ids are
    generated/vars_flags.txt's; the caps are the engine's sLevelCaps."""
    import re
    root = model.repo_root()
    read = lambda *p: open(os.path.join(root, *p), encoding="utf-8").read()
    # Every pocket's size, the TM pocket's included (NUM_TMHMS since element
    # 7): the defines of the bag and item headers, item constants by their ids.
    defines = {}
    for text in (read("include", "bag.h"), read("include", "constants", "items.h")):
        for n, v in re.findall(r"^#define[ \t]+(\w+)[ \t]+([^\n]+?)[ \t]*(?://[^\n]*)?$", text, re.M):
            defines[n] = v
    items = [line.strip() for line in read("generated", "items.txt").splitlines() if line.strip()]
    consts = {c: i for i, c in enumerate(c for c in items if not c.startswith("MAX_"))}
    consts["MAX_ITEMS"] = len(consts)
    # The pockets are the Bag struct's own arrays (BagItem items[ITEM_POCKET_SIZE];
    # and so on), not every *_POCKET_SIZE define: items.h has a
    # BATTLE_POCKET_SIZE of its own, for the battle bag's menu.
    sizes = re.findall(r"BagItem\s+\w+\[(\w+)\];", read("include", "bag.h"))
    if len(sizes) < 8:
        raise SaveError(f"include/bag.h lists {len(sizes)} pockets; this reader expects 8")
    pockets = sum(_c_value(n, defines, consts) for n in sizes)
    party = 4 + 4 + 6 * PARTY_RECORD
    bag = pockets * 4 + 4
    values, last = {}, -1
    for line in read("generated", "vars_flags.txt").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\w+)\s*=\s*(\w+)$", line)
        if m:
            name, v = m.groups()
            last = int(v, 0) if v[0].isdigit() else values[v]
        else:
            name, last = line, last + 1
        values[name] = last
    flags = int(re.search(r"#define NUM_FLAGS\s+(\d+)", read("include", "vars_flags.h")).group(1))
    # The splits by the names the rest of the tool uses (progression.SPLITS:
    # "HQ", not "Hq"); the one after the Champion, which has no cap, is Post.
    from . import progression
    canonical = {sp.upper(): sp for sp in progression.SPLITS}
    canonical["NONE"] = "Post"
    splits = dict((int(v), canonical.get(n, n.title())) for n, v in
                  re.findall(r"#define LEVEL_CAP_SPLIT_(\w+)\s+(\d+)", read("include", "constants", "level_caps.h"))
                  if n != "COUNT")
    caps = {}
    for n, v in re.findall(r"\[LEVEL_CAP_SPLIT_(\w+)\] = (\w+)", read("src", "system_vars.c")):
        caps[canonical.get(n, n.title())] = int(v) if v.isdigit() else 100
    return {"at": PARTY_AT + _entry_body(party) + _entry_body(bag),
            "vars_start": values["VARS_START"], "num_vars": values["VARS_END"] - values["VARS_START"],
            "num_flags": flags, "values": values, "splits": splits, "caps": caps}


OLDER_LAYOUT = ("made on an older layout than this build's, so its variables and flags "
                "are not where this build keeps them; a new game on this ROM reads in full "
                "(a layout change costs a new game, Ian, 2026-09-28)")


def _progress(data, n0, current=True):
    """The trainer's money and badges, and the level-cap split: what the
    save says about how far the player is. The split is left out of a save
    on an older layout (`current` False), whose variables have moved."""
    money, = struct.unpack_from("<I", data, n0 + 0x7C)
    mask = data[n0 + 0x82]
    out = {"money": money, "badge_mask": mask, "badges": bin(mask).count("1"), "split": None}
    if not current:
        return out
    lay = _vars_layout()
    var = lay["values"].get("VAR_LEVEL_CAP_SPLIT")
    if var is not None:
        i = struct.unpack_from("<H", data, n0 + lay["at"] + 2 * (var - lay["vars_start"]))[0]
        name = lay["splits"].get(i)
        out["split"] = {"index": i, "name": name, "cap": lay["caps"].get(name)} if name else {"index": i}
    return out


def flag(data, name):
    """Whether a named flag is set in a save's newest normal block. A save on
    an older layout is refused rather than read at the wrong place."""
    lay = _vars_layout()
    found = blocks(data)
    if found[BLOCK_NORMAL]["size"] != CURRENT_LAYOUT[0]:
        raise SaveError("this save was " + OLDER_LAYOUT)
    n0 = found[BLOCK_NORMAL]["start"]
    i = lay["values"][name]
    at = n0 + lay["at"] + 2 * lay["num_vars"] + i // 8
    return bool(data[at] >> (i % 8) & 1)


def flags_set(data, numbers):
    """The flags among `numbers` (flag ids, as vars_flags.txt numbers them)
    that a save has set, from its newest normal block: one read for the alpha
    checklist's ticks, a trainer's TRAINER_DEFEATED_FLAGS_START plus its id
    and every pickup's obtained flag. A save on an older layout is refused,
    as flag() refuses it."""
    lay = _vars_layout()
    found = blocks(data)
    if BLOCK_NORMAL not in found:
        raise SaveError("no valid copy of the normal block")
    if found[BLOCK_NORMAL]["size"] != CURRENT_LAYOUT[0]:
        raise SaveError("this save was " + OLDER_LAYOUT)
    base = found[BLOCK_NORMAL]["start"] + lay["at"] + 2 * lay["num_vars"]
    return {n for n in numbers
            if 0 <= n < lay["num_flags"] and data[base + n // 8] >> (n % 8) & 1}


PLAYER_GENDER_AT = 0x80     # TrainerInfo: name, id, money, then gender


def player(data):
    """{"gender": "male" or "female", "starter": species constant or None},
    which the alpha checklist uses to show the version of a fight the save
    meets: the scripts pick a rival's or Lucas's and Dawn's team by the
    player's starter (VAR_PLAYER_STARTER) and gender. None on a save of an
    older layout, whose variables are elsewhere."""
    found = blocks(data)
    if BLOCK_NORMAL not in found or found[BLOCK_NORMAL]["size"] != CURRENT_LAYOUT[0]:
        return None
    n0 = found[BLOCK_NORMAL]["start"]
    lay = _vars_layout()
    at = n0 + lay["at"] + 2 * (lay["values"]["VAR_PLAYER_STARTER"] - lay["vars_start"])
    sid = struct.unpack_from("<H", data, at)[0]
    species = _tables()["species"]
    return {"gender": "female" if data[n0 + PLAYER_GENDER_AT] else "male",
            "starter": species[sid] if 0 < sid < len(species) else None}


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
    egg, met = struct.unpack_from("<HH", b, 0x1C)
    stored_ivs = [ivs >> (5 * i) & 31 for i in range(6)]
    # Element 7: a Bottle Cap trains a stat, which then grows as if its IV
    # were 31, and a Mint sets the nature the stats grow by. The stored IVs
    # and the personality's nature stay as they were, as Pokemon_GetStatIV
    # and BoxPokemon_GetStatNature read them; a Mint byte past the 25 natures
    # counts as none there too.
    trained = [bool(a[0x0D] >> (2 + i) & 1) for i in range(6)]
    mint = b[0x19]
    if mint > len(NATURES):
        problems.append(f"its Mint byte reads {mint}, past the {len(NATURES)} natures")

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
        # The nature the game names; `stat_nature` is the one the stats
        # grow by, a Mint's when there is one.
        "nature": NATURES[pv % 25],
        "mint": NATURES[mint - 1] if 0 < mint <= len(NATURES) else None,
        "stat_nature": NATURES[mint - 1] if 0 < mint <= len(NATURES) else NATURES[pv % 25],
        "ability": t["tidy"](name("abilities", ability_id, "ABILITY_"), "ABILITY_"),
        "ability_id": ability_id, "hidden_ability": bool(a[0x0D] & 1),
        # The stored ability already reflects the swap; this says why it is
        # the other ordinary slot.
        "ability_swapped": bool(a[0x0D] >> 1 & 1),
        "move_ids": moves,
        "moves": [t["move_names"].get(name("moves", m, "MOVE_"), f"#{m}") for m in moves],
        # Stored IVs, and the ones the stats grow from, in STATS order.
        "ivs": stored_ivs,
        "hyper_trained": [s for s, on in zip(STATS, trained) if on],
        "stat_ivs": [MAX_IV if on else iv for iv, on in zip(stored_ivs, trained)],
        "evs": list(a[0x10:0x16]),
        "met_location": t["places"][met] if met < len(t["places"]) else f"#{met}",
        # Where an egg came from (a gift or the Day Care), kept once it hatches;
        # 0 for a Pokemon that was never an egg.
        "egg_location": (t["places"][egg] if egg < len(t["places"]) else f"#{egg}") if egg else None,
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
        "progress": _progress(data, n0, normal["size"] == CURRENT_LAYOUT[0]),
        "party": party, "boxes": boxes, "box_count": box_count, "current_box": current_box,
    }
    save["era"] = build_era(save)
    return save


def packed(data):
    """The save's party and boxes as the calculator's Sync decodes them
    (`decodeDsPackedBoxPayload`, format "DPB1"): an 18-byte header (the
    magic, the trainer's id and secret id, the party and box counts, the two
    record sizes, the box slots that follow and the current box), then the
    party's 236-byte records and every box slot's 136-byte record exactly as
    the save stores them. The calculator decrypts them itself, with the same
    parsePKM its Read Save uses, so this adds no second decoder to keep."""
    found = blocks(data)
    if BLOCK_NORMAL not in found:
        raise SaveError("no valid copy of the normal block")
    n0 = found[BLOCK_NORMAL]["start"]
    tid, sid = struct.unpack_from("<HH", data, n0 + TRAINER_ID_AT)
    capacity, count = struct.unpack_from("<ii", data, n0 + PARTY_AT)
    if capacity != 6 or not 0 <= count <= 6:
        raise SaveError(f"the party is not where Platinum keeps it (capacity {capacity})")
    first = n0 + PARTY_AT + 8
    party = data[first:first + count * PARTY_RECORD]
    boxes, box_count, current = b"", 0, 0
    if BLOCK_BOXES in found:
        bx = found[BLOCK_BOXES]
        box_count = (bx["size"] - FOOTER_SIZE - 5) // BOX_STRIDE
        current = struct.unpack_from("<I", data, bx["start"])[0]
        boxes = data[bx["start"] + 4:bx["start"] + 4 + box_count * MONS_PER_BOX * BOX_RECORD]
    header = b"DPB1" + struct.pack("<HHBBHHHB", tid, sid, count, box_count, PARTY_RECORD,
                                   BOX_RECORD, box_count * MONS_PER_BOX, min(current, 255)) + b"\0"
    return header + party + boxes


def summary(save):
    """What the OxiDex's save bar shows: the trainer, the party in words, how
    many are boxed, and the build signs."""
    return {"trainer_id": save["trainer_id"], "secret_id": save["secret_id"],
            "party": [describe(m) for m in save["party"]], "party_count": len(save["party"]),
            "boxed": len(save["boxes"]), "box_count": save["box_count"], "era": save["era"],
            "progress": save["progress"]}


def build_era(save):
    """What the save says about the build that wrote it, and any sign that it
    does not match this one: {"layout", "signs": [...], "mismatches": [...]}."""
    sizes = (save["blocks"].get(BLOCK_NORMAL, {}).get("size"),
             save["blocks"].get(BLOCK_BOXES, {}).get("size"))
    layout = KNOWN_LAYOUTS.get(sizes)
    signs, mismatches = [], []
    mons = save["party"] + save["boxes"]
    if layout and sizes[0] != CURRENT_LAYOUT[0]:
        mismatches.append(f"block sizes {sizes[0]:#x} and {sizes[1]:#x} are {layout}: "
                          f"{OLDER_LAYOUT}")
    elif layout:
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
    if any(mon["mint"] or mon["hyper_trained"] or mon["ability_swapped"] for mon in mons):
        signs.append("a Pokemon changed by a Mint, a Bottle Cap or an Ability Capsule "
                     "(element 7, 2026-09-28)")
    split = (save.get("progress") or {}).get("split")
    if split and "name" not in split:
        mismatches.append(f"the level-cap split reads {split['index']}, which this build has no "
                          f"split for; the variables may not be where this build keeps them")
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
            f"Lv {mon.get('level', '?')}",
            mon["nature"] + (f" (stats as {mon['mint']} by a Mint)" if mon.get("mint") else ""),
            mon["ability"] + (" (hidden)" if mon["hidden_ability"] else "")
            + (" (by an Ability Capsule)" if mon.get("ability_swapped") else "")]
    if mon.get("hyper_trained"):
        bits.append("Hyper Trained " + ", ".join(mon["hyper_trained"]))
    if mon["item"]:
        bits.append(f"holding {mon['item']}")
    bits.append(", ".join(mon["moves"]) or "no moves")
    bits.append(f"met at {mon['met_location']} at level {mon['met_level']}")
    return f"{mon['slot']}: " + "; ".join(bits)
