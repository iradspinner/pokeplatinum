"""The save reader (savefile.py), on a save built here byte by byte.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_savefile

The save is made in memory the way the game writes one: two copies, each a
normal block and a box block with footers and CRCs, Pokemon records
shuffled and encrypted as include/struct_defs/pokemon.h lays them out, and
empty slots as the encrypted zeros BoxPokemon_Init leaves. No real save is
in the repository, which is public. Ian's own save is read too when its
working copy is on this machine (~/roms/oxide-save-2026-09-21.sav, never the
original), and that check is skipped where it is not, as on a cloud session.
"""
import hashlib
import os
import struct
import subprocess
import sys
import tempfile

from . import savefile as S

NORMAL_SIZE, BOX_SIZE = 0xD01C, 0x121E4
IAN_COPY = os.path.expanduser("~/roms/oxide-save-2026-09-21.sav")
# His first save on a current ROM (53b863005), in his room after the intro.
IAN_CURRENT = os.path.expanduser("~/roms/oxide-save-2026-09-27-53b863005.sav")


def species_id(constant):
    return S._tables()["species"].index(constant)


def move_id(constant):
    return S._tables()["moves"].index(constant)


def ability_id(constant):
    return S._tables()["abilities"].index(constant)


def record(pv, species, moves, ability, exp=0, hidden=False, met=0, party_level=None,
           corrupt=False):
    """One Pokemon record as the game stores it."""
    a = (struct.pack("<HHII", species, 0, 25097 | 32454 << 16, exp)
         + bytes([70, 1 if hidden else 0, 0, 2]) + bytes(12) + bytes(4))
    b = (struct.pack("<4H", *(moves + [0] * (4 - len(moves)))) + bytes(8)
         + struct.pack("<I", 31 | 31 << 5) + bytes(4) + bytes(2)
         + struct.pack("<H", ability) + struct.pack("<HH", 0, met))
    c, d = bytes(32), bytes(28) + bytes([5, 0, 0, 0])
    arranged = [None] * 4
    for blk, p in zip((a, b, c, d), S.BLOCK_POSITIONS[((pv & 0x3E000) >> 13) % 24]):
        arranged[p] = blk
    plain = b"".join(arranged)
    checksum = sum(struct.unpack("<64H", plain)) & 0xFFFF
    body = S._decode(plain, checksum)
    if corrupt:
        body = bytes([body[0] ^ 0xFF]) + body[1:]
    rec = struct.pack("<IHH", pv, 0, checksum) + body
    if party_level is not None:
        stats = bytes(4) + bytes([party_level, 0]) + struct.pack("<HH", 17, 20) + bytes(90)
        rec += S._decode(stats, pv)
    return rec


EMPTY = struct.pack("<IHH", 0, 0, 0) + S._decode(bytes(128), 0)


def footer(body, block, save_counter, block_counter, size):
    return (struct.pack("<IIII", save_counter, block_counter, size, S.SIGNATURE)
            + bytes([block, 0]) + struct.pack("<H", S.crc16(body)))


def make_save(party, boxed, normal_counters=(2, 3), box_counters=(1, 0), split=4, badges=0x1F,
              money=12345):
    """A 512 KB save. `boxed` is {(box, slot): record}; the counters say which
    copy of each block is newer (0 leaves that copy's block unwritten)."""
    data = bytearray(b"\xff" * 0x80000)
    normal = bytearray(NORMAL_SIZE - S.FOOTER_SIZE)
    struct.pack_into("<HH", normal, S.TRAINER_ID_AT, 25097, 32454)
    struct.pack_into("<ii", normal, S.PARTY_AT, 6, len(party))
    struct.pack_into("<I", normal, 0x7C, money)
    normal[0x82] = badges
    lay = S._vars_layout()
    var = lay["values"]["VAR_LEVEL_CAP_SPLIT"] - lay["vars_start"]
    struct.pack_into("<H", normal, lay["at"] + 2 * var, split)
    for i, rec in enumerate(party):
        normal[S.PARTY_AT + 8 + i * S.PARTY_RECORD:S.PARTY_AT + 8 + (i + 1) * S.PARTY_RECORD] = rec
    boxes = bytearray(BOX_SIZE - S.FOOTER_SIZE)
    for i in range(18 * 30):
        rec = boxed.get((i // 30 + 1, i % 30 + 1), EMPTY)
        boxes[4 + i * S.BOX_RECORD:4 + (i + 1) * S.BOX_RECORD] = rec
    for base, n_ctr, b_ctr in ((0, normal_counters[0], box_counters[0]),
                               (S.BACKUP_START, normal_counters[1], box_counters[1])):
        if n_ctr:
            data[base:base + NORMAL_SIZE] = normal + footer(normal, 0, 1, n_ctr, NORMAL_SIZE)
        if b_ctr:
            at = base + NORMAL_SIZE
            data[at:at + BOX_SIZE] = boxes + footer(boxes, 1, 1, b_ctr, BOX_SIZE)
    return bytes(data)


def main():
    results = []
    chimchar, glimmet = species_id("SPECIES_CHIMCHAR"), species_id("SPECIES_GLIMMET")
    party = [record(0x12345678, chimchar, [move_id("MOVE_SCRATCH"), move_id("MOVE_LEER")],
                    ability_id("ABILITY_BLAZE"), exp=S._tables()["exp"]["medium_slow"][6] + 10,
                    met=3, party_level=6)]
    names = S._tables()["move_names"]
    new_move = next(i for i, m in enumerate(S._tables()["moves"]) if i > S.VANILLA_MOVES
                    and names.get(m) not in (None, "", "-"))
    boxed = {(2, 5): record(0x0BADF00D, glimmet, [new_move], ability_id("ABILITY_TOXIC_DEBRIS")
                            if "ABILITY_TOXIC_DEBRIS" in S._tables()["abilities"] else 1,
                            exp=1000, hidden=True),
             (3, 1): record(0x0000BEEF, chimchar, [move_id("MOVE_SCRATCH")],
                            ability_id("ABILITY_BLAZE"), corrupt=True)}
    data = make_save(party, boxed)
    s = S.parse(data, "synthetic")

    results.append(("each block comes from its newest valid copy: the backup's normal block "
                    "(counter 3), the primary's boxes (the backup's never written)",
                    s["blocks"][0]["copy"] == "backup" and s["blocks"][1]["copy"] == "primary"
                    and s["box_count"] == 18, str({k: v["copy"] for k, v in s["blocks"].items()})))
    p = s["party"][0] if s["party"] else {}
    results.append(("a party Pokemon decodes: species, level from its stats, moves, "
                    "ability from Oxide's u16 in block B, nature, trainer id",
                    p.get("species") == "SPECIES_CHIMCHAR" and p.get("level") == 6
                    and p.get("moves") == ["Scratch", "Leer"] and p.get("ability") == "Blaze"
                    and p.get("nature") == S.NATURES[0x12345678 % 25] and p.get("hp") == (17, 20)
                    and (s["trainer_id"], s["secret_id"]) == (25097, 32454), S.describe(p) if p else ""))
    # The game stores a party Pokemon's level; a boxed one's comes from its
    # experience on its species' curve, so the two must agree on a party
    # Pokemon (Chimchar is medium slow; reading every curve as medium fast
    # once gave level 5 here).
    results.append(("the level from experience follows the species' own curve and agrees "
                    "with the level the party stores",
                    p.get("level") == 6 and S._level("SPECIES_CHIMCHAR", p.get("exp", 0)) == 6,
                    f"stored {p.get('level')}, from experience "
                    f"{S._level('SPECIES_CHIMCHAR', p.get('exp', 0))}"))
    by_slot = {(m["box"], m["box_slot"]): m for m in s["boxes"]}
    g = by_slot.get((2, 5), {})
    results.append(("a boxed Pokemon decodes in its box and slot, with its level from "
                    "experience and its hidden ability bit",
                    g.get("species") == "SPECIES_GLIMMET" and g.get("hidden_ability") is True
                    and g.get("level") == S._level("SPECIES_GLIMMET", 1000) and g.get("level", 0) > 1,
                    S.describe(g) if g else "missing"))
    results.append(("empty slots, the encrypted zeros the game leaves, are not Pokemon",
                    len(s["boxes"]) == 2, f"{len(s['boxes'])} boxed"))
    era = s["era"]
    results.append(("the build signs: Oxide's layout since 2026-09-21, a move past vanilla's "
                    "467, a hidden ability; a record failing its checksum is a mismatch",
                    era["layout"] and any("467" in x and "element 4" in x for x in era["signs"])
                    and any("hidden" in x for x in era["signs"])
                    and any("box 3 slot 1" in x and "checksum" in x for x in era["mismatches"]),
                    "; ".join(era["mismatches"])))
    pr = s["progress"]
    results.append(("the save's progress: money and badges from the trainer, the level-cap "
                    "split from its variable (after the party and the bag), with the engine's cap",
                    pr["money"] == 12345 and pr["badges"] == 5 and pr["split"]
                    == {"index": 4, "name": "Wake", "cap": 44} and S._vars_layout()["at"] == 0xDAC
                    # the split names are the simulator's, so it can resume there
                    and S._vars_layout()["splits"][7] == "HQ"
                    and S._vars_layout()["splits"][12] == "Post",
                    f"{pr['badges']} badges, {pr['split']}"))
    vanilla_sized = S.KNOWN_LAYOUTS.get((0xCF2C, 0x121E4), "")
    results.append(("a save with no valid normal block is refused, not guessed at",
                    _refuses(bytes(0x80000)) and "2026-09-21" in vanilla_sized, ""))

    # Read-only: reading the file leaves it byte for byte as it was.
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "synthetic.sav")
        with open(path, "wb") as f:
            f.write(data)
        before = (hashlib.sha1(open(path, "rb").read()).hexdigest(), os.stat(path).st_mtime_ns)
        S.read(path)
        rc = subprocess.run([sys.executable, "-m", "tools.oxide.encounters.cli", "save", path],
                            capture_output=True, text=True, env=dict(os.environ, PYTHONPATH="."),
                            cwd=S.model.repo_root())
        after = (hashlib.sha1(open(path, "rb").read()).hexdigest(), os.stat(path).st_mtime_ns)
    results.append(("reading a save never changes it; `cli save` exits 2 on a mismatch",
                    before == after and rc.returncode == 2 and "does not match" in rc.stdout,
                    f"exit {rc.returncode}"))

    # The calculator reads the same saves through its own reader, with
    # Oxide's tables from the blob and two patches (VENDORED.md, 14 and 15).
    from . import calc_export
    inc = calc_export.save_includes()
    t = S._tables()
    results.append(("the calculator's save tables line up with the game's ids: species with "
                    "their growth curves, moves, items, abilities, and the two eggs",
                    len(inc["poks"]) == len(t["species"]) == len(inc["growths"])
                    and len(inc["moves"]) == len(t["moves"]) and len(inc["items"]) == len(t["items"])
                    and len(inc["abilities"]) == len(t["abilities"])
                    and inc["poks"][chimchar] == "Chimchar" and inc["growths"][chimchar] == 3
                    and inc["poks"][species_id("SPECIES_EGG")] == "Egg"
                    and inc["moves"][move_id("MOVE_SCRATCH")] == "Scratch"
                    and inc["abilities"][ability_id("ABILITY_BLAZE")] == "Blaze",
                    {k: len(v) for k, v in inc.items()}))
    calc = os.path.join(S.model.repo_root(), "tools", "oxide", "encounters", "calc", "js")
    reader = open(os.path.join(calc, "savereaders", "savereader.js"), encoding="utf-8").read()
    init = open(os.path.join(calc, "initialize.js"), encoding="utf-8").read()
    oxide_branch = init[init.index('title == "Platinum Oxide"'):init.index('title == "Platinum Kaizo"')]
    results.append(("the calculator's reader carries Oxide's patches: the layout by footer, the "
                    "u16 ability and hidden bit, the blob's tables kept from the Gen 6-7 extender",
                    "applyOxideSaveLayout(view)" in reader and "0x20060623" in reader
                    and "decryptedData[move_data_offset + 13]" in reader
                    and "settings.readIncludes = true" in oxide_branch
                    and 'TITLE != "Platinum Oxide"' in init, ""))

    if os.path.exists(IAN_COPY):
        ian = S.read(IAN_COPY)
        first = ian["party"][0] if ian["party"] else {}
        results.append(("Ian's save of 2026-09-21 (its working copy): Chimchar at level 6 with "
                        "Blaze, on Oxide's layout, nothing contradicting this build",
                        first.get("species") == "SPECIES_CHIMCHAR" and first.get("level") == 6
                        and S._level("SPECIES_CHIMCHAR", first.get("exp", 0)) == 6
                        and first.get("ability") == "Blaze" and not ian["era"]["mismatches"]
                        and ian["blocks"][1]["copy"] == "backup",
                        S.describe(first) if first else "no party"))
    else:
        print(f"  skip  Ian's save: no working copy at {IAN_COPY}")
    if os.path.exists(IAN_CURRENT) and os.path.exists(IAN_COPY):
        now = S.read(IAN_CURRENT)
        old = open(IAN_COPY, "rb").read()
        results.append(("Ian's first save on a current ROM: the same layout, an empty party, "
                        "3000 money, Roark's split at cap 16; his older save has the Pokedex "
                        "flag set, read from the same place",
                        now["blocks"][0]["size"] == 0xD01C and not now["party"]
                        and now["progress"]["money"] == 3000
                        and now["progress"]["split"] == {"index": 0, "name": "Roark", "cap": 16}
                        and not now["era"]["mismatches"] and S.flag(old, "FLAG_HAS_POKEDEX")
                        and not S.flag(open(IAN_CURRENT, "rb").read(), "FLAG_HAS_POKEDEX"),
                        str(now["progress"])))
    else:
        print(f"  skip  Ian's current save: no working copy at {IAN_CURRENT}")

    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


def _refuses(data):
    try:
        S.parse(data)
    except S.SaveError:
        return True
    return False


if __name__ == "__main__":
    sys.exit(main())
