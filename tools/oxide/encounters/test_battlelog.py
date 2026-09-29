"""The battle log reader (battlelog.py), on saves built here byte by byte.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_battlelog

The log is written the way docs/oxide/battle-log.md says the engine writes
it, into a save made by test_savefile's builder: a copy in sector 44 of each
half, a header, a ring of 58-byte records and a footer with the game's
signature, a save counter and a CRC. No save with a real log exists yet (the
engine side is still to come), so these are the reader's only checks until
one does. Ian's own saves predate the log, and are read to show they still
read as they did, with an empty log.
"""
import io
import os
import contextlib
import struct
import sys
import tempfile

from . import battlelog as B
from . import calc_trainers
from . import cli
from . import model
from . import savefile as S
from . import savewatch
from . import test_savefile as T


def trainer_id(constant):
    return calc_trainers._tables(model.repo_root())["ids"][constant]


def with_log(data, primary=None, backup=None):
    """The save's bytes with log copies written into sector 44 of each half."""
    out = bytearray(data)
    for at, copy in zip(B.SECTORS, (primary, backup)):
        if copy is not None:
            out[at:at + len(copy)] = copy
    return bytes(out)


def main():
    results = []
    sid = T.species_id
    chimchar, monferno = sid("SPECIES_CHIMCHAR"), sid("SPECIES_MONFERNO")
    starly, geodude, onix = sid("SPECIES_STARLY"), sid("SPECIES_GEODUDE"), sid("SPECIES_ONIX")
    cranidos = sid("SPECIES_CRANIDOS")
    # The party now holds a Monferno that was a Chimchar in the older battles
    # (personality 0x...78, so its logged byte is 0x78) and a Starly. The
    # Monferno is Gentle by personality with an Adamant Mint (element 7).
    party = [T.record(0x12345678, monferno, [T.move_id("MOVE_SCRATCH")],
                      T.ability_id("ABILITY_BLAZE"), party_level=16,
                      mint=T.S.NATURES.index("Adamant") + 1),
             T.record(0x0000AB42, starly, [T.move_id("MOVE_TACKLE")],
                      T.ability_id("ABILITY_KEEN_EYE"), party_level=12)]
    base = T.make_save(party, {})
    tristan = trainer_id("TRAINER_YOUNGSTER_TRISTAN")
    roark = trainer_id("TRAINER_LEADER_ROARK")
    battles = [
        # Oldest: Chimchar beats Tristan's Starly; nothing of the player's falls.
        {"trainer_a": tristan, "turns": 3, "flags": B.FLAG_WON, "split": 0,
         "player": [chimchar], "player_pid8": [0x78], "player_levels": [9],
         "opponents": [starly], "opponent_levels": [7], "ko_of_opponent": [0],
         "ko_of_player": [B.NONE]},
        # Roark: Chimchar takes Geodude, Onix falls to poison, Cranidos
        # knocks out Starly and stands at the end; the player loses.
        {"trainer_a": roark, "turns": 11, "flags": B.FLAG_LOST, "split": 0,
         "player": [chimchar, starly, B.EGG], "player_pid8": [0x78, 0x42, 0x10],
         "player_levels": [14, 12, 1],
         "opponents": [geodude, onix, cranidos], "opponent_levels": [14, 15, 16],
         "ko_of_opponent": [0, B.INDIRECT, B.NONE], "ko_of_player": [B.NONE, 2, B.NONE]},
        # Newest: a double with a partner, the partner takes one.
        {"trainer_a": roark, "trainer_b": tristan, "turns": 5,
         "flags": B.FLAG_WON | B.FLAG_DOUBLE | B.FLAG_PARTNER | B.FLAG_TWO_TRAINERS, "split": 1,
         "player": [monferno, starly], "player_pid8": [0x78, 0x42], "player_levels": [16, 12],
         "opponents": [geodude, starly], "count_b": 1, "opponent_levels": [18, 17],
         "ko_of_opponent": [0, B.PARTNER], "ko_of_player": [B.NONE, B.NONE]},
    ]

    # -- a save from before the log --------------------------------------------------
    plain = S.parse(base, "no log")
    log = B.read(base, plain)
    results.append(("a save from before the log (both sectors erased) reads as an empty log, "
                    "not an error", log["state"] == "empty" and log["records"] == [], log.get("reason")))

    # -- the copies ------------------------------------------------------------------
    newer = B.pack_copy(battles, counter=7, start=58)      # the ring wraps past slot 59
    older = B.pack_copy(battles[:1], counter=6)
    data = with_log(base, newer, older)
    save = S.parse(data, "with log")
    log = B.read(data, save)
    results.append(("of two valid copies the one with the higher save counter is read, "
                    "newest battle first, across the ring's wrap",
                    log["state"] == "ok" and log["copy"]["counter"] == 7
                    and [r["ring_slot"] for r in log["records"]] == [0, 59, 58]
                    and [r["turns"] for r in log["records"]] == [5, 11, 3],
                    str([r["ring_slot"] for r in log["records"]])))
    swapped = with_log(base, older, B.pack_copy(battles, counter=9))
    results.append(("the backup copy is read when its counter is higher",
                    B.read(swapped)["copy"]["at"] == B.SECTORS[1], ""))
    broken = bytearray(newer)
    broken[40] ^= 0x01
    fallback = B.read(with_log(base, bytes(broken), older))
    results.append(("a copy whose checksum fails is passed over for the other",
                    fallback["state"] == "ok" and fallback["copy"]["counter"] == 6
                    and any(c.get("reason") == "its checksum fails" for c in fallback["copies"]), ""))
    both_bad = B.read(with_log(base, bytes(broken), None))
    results.append(("with no valid copy and one that is not erased, the log is reported invalid, "
                    "with each copy's reason", both_bad["state"] == "invalid"
                    and "checksum" in both_bad["reason"], both_bad.get("reason")))
    v2 = bytearray(newer)
    struct.pack_into("<H", v2, 4, 2)
    body = bytes(v2[:-B.FOOTER_SIZE])
    v2[-2:] = struct.pack("<H", S.crc16(body))
    unknown = B.read(with_log(base, bytes(v2), None))
    results.append(("a log version this reader does not know is reported, not guessed at",
                    unknown["state"] == "unknown-version", unknown.get("reason")))

    # -- the save reader is not disturbed ------------------------------------------------
    results.append(("the save reader leaves the log's footers out and picks the same blocks",
                    len(save["footers"]) == len(plain["footers"])
                    and save["blocks"] == plain["blocks"] and not save["era"]["mismatches"],
                    f"{len(save['footers'])} footers against {len(plain['footers'])}"))

    # -- one record, named -------------------------------------------------------------
    raw = B.pack_record(battles[1])
    back = B.decode_record(raw)
    six = lambda v: v + [0] * (6 - len(v)) if isinstance(v, list) else v
    results.append(("a record packs to 58 bytes and decodes back field for field, empty slots "
                    "as species 0 and knock-out 0xF",
                    len(raw) == 58 and all(back[k] == six(battles[1][k]) for k in
                                           ("trainer_a", "turns", "flags", "player", "player_pid8",
                                            "opponents", "opponent_levels"))
                    and back["ko_of_opponent"][3:] == [B.NONE] * 3
                    and (back["player_count"], back["count_a"], back["count_b"]) == (3, 3, 0),
                    str({k: back[k] for k in ("player", "ko_of_opponent")})))
    newest, roark_rec, first = log["records"]
    results.append(("trainers are named as the calculator names them",
                    first["trainer_a_name"] == "Youngster Tristan"
                    and roark_rec["trainer_a_name"] == "Leader Roark"
                    and newest["trainer_b_name"] == "Youngster Tristan",
                    f"{first['trainer_a_name']}, {roark_rec['trainer_a_name']}"))
    opp = roark_rec["opponents"]
    results.append(("opponents carry species and level; each knock-out names its cause: a party "
                    "slot, indirect damage, or none",
                    [(o["species"], o["level"]) for o in opp]
                    == [("Geodude", 14), ("Onix", 15), ("Cranidos", 16)]
                    and opp[0]["ko_by"] == {"by": 0, "how": "player"}
                    and opp[1]["ko_by"] == {"by": None, "how": "indirect"}
                    and opp[2]["ko_by"] == {"by": None, "how": None}, str([o["ko_by"] for o in opp])))
    pl = roark_rec["player"]
    results.append(("the player's side: the loss, Starly knocked out by Cranidos (slot 2), an egg "
                    "as Egg", roark_rec["result"] == "lost" and pl[1]["ko_by"]["by"] == 2
                    and pl[2]["species"] == "Egg" and pl[2]["is_egg"], ""))
    results.append(("the partner's knock-out, the double and the two trainers are read from the "
                    "flags, and the split by its name", newest["opponents"][1]["ko_by"]["how"] == "partner"
                    and newest["double"] and newest["partner"] and newest["two_trainers"]
                    and newest["split"] == "Gardenia" and first["split"] == "Roark"
                    and [o["trainer"] for o in newest["opponents"]] == ["A", "B"], newest["split"]))
    results.append(("a logged Chimchar is matched to the Monferno it became (same line, same "
                    "personality byte); the egg matches nothing",
                    first["player"][0]["now"] and first["player"][0]["now"]["species"] == "SPECIES_MONFERNO"
                    and roark_rec["player"][1]["now"]["species"] == "SPECIES_STARLY"
                    and roark_rec["player"][2]["now"] is None, ""))
    stranger = dict(battles[0], player_pid8=[0x99])
    other = B.read(with_log(base, B.pack_copy([stranger], counter=1), None), save)
    results.append(("a logged Pokemon whose personality byte matches nothing in the save stays "
                    "unmatched", other["records"][0]["player"][0]["now"] is None, ""))

    # -- the calculator's payload --------------------------------------------------------
    calc = B.calc_payload(log, save)
    ev = calc["events"]
    starts = [e for e in ev if e["type"] == "session_start"]
    results.append(("the calculator's payload has one session per battle, oldest first, with "
                    "the version its patch passes through",
                    calc["version"] == "oxide-save-v1" and len(starts) == 3
                    and [s["enemyTrainerIdA"] for s in starts] == [tristan, roark, roark]
                    and sum(e["type"] == "session_end" for e in ev) == 3, ""))
    kinds = [(e["type"], e.get("pSpecies"), e.get("aiSpecies"), e.get("aiLevel"))
             for e in ev if e["type"] not in ("session_start", "session_end")]
    results.append(("knock-outs become pKo, aiKo and partnerKo events in the calculator's names, "
                    "with the opponent's level; indirect ones are left out",
                    kinds == [("pKo", "Chimchar", "Starly", 7),
                              ("pKo", "Chimchar", "Geodude", 14),
                              ("aiKo", "Starly", "Cranidos", 16),
                              ("pKo", "Monferno", "Geodude", 18),
                              ("partnerKo", None, "Starly", 17)], str(kinds)))
    results.append(("each session carries its split index, and the payload lists Oxide's "
                    "thirteen splits with their caps",
                    [s["saveFileSplitIndex"] for s in starts] == [0, 0, 1]
                    and len(calc["splits"]) == 13 and calc["splits"][0] == {"index": 0, "name": "Roark", "cap": 16}
                    and calc["splits"][-1]["name"] == "Post", str(calc["splits"][:2])))
    # The Battle Log rebuilds a set from each party entry, so it takes the
    # nature the stats grow by, as Read Save and Sync do; the log's own
    # record keeps the nature the game names.
    first = starts[0]["pParty"][0]
    results.append(("a party entry carries the Mint's nature for its set, and the log keeps "
                    "the personality's",
                    first["nature"] == "Adamant"
                    and log["records"][-1]["player"][0]["now"]["nature"] == T.S.NATURES[0x12345678 % 25],
                    f"{first['nature']}, now {log['records'][-1]['player'][0]['now']['nature']}"))
    counters = {c["species"]: c for c in calc["pokemonBattleCounters"]}
    results.append(("battle counters follow each Pokemon into its evolution: Monferno was brought "
                    "to 3 battles with 3 knock-outs, Starly to 2 with none",
                    counters.get("Monferno", {}).get("battlesBrought") == 3
                    and counters["Monferno"]["koCount"] == 3
                    and counters.get("Starly", {}).get("battlesBrought") == 2
                    and counters["Starly"]["koCount"] == 0, str(counters)))

    # -- the watcher and the command line ---------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "oxide.sav")
        with open(path, "wb") as f:
            f.write(data)
        w = savewatch.Watcher()
        w.state["path"] = path
        w.check()
        out = w.battle_log()
        snap = w.snapshot()
        results.append(("the watcher serves the log with the save it read, and the save bar's "
                        "summary says how many battles it holds",
                        out and out["seq"] == 1 and len(out["log"]["records"]) == 3
                        and out["calc"]["recordCount"] == 3
                        and snap["save"]["battle_log"] == {"count": 3, "counter": 7},
                        str(snap["save"].get("battle_log"))))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cli.main(["battlelog", path])
        text = buf.getvalue()
        results.append(("`cli battlelog` prints the battles newest first",
                        rc == 0 and "3 of 60 battles" in text
                        and text.index("Leader Roark and Youngster Tristan") < text.index("Youngster Tristan: won"),
                        text.splitlines()[0] if text else f"exit {rc}"))

    # -- the Fragsheet's thirteen splits (Ian, 2026-09-28) ----------------------------------
    from . import calc_export
    sp = calc_export.splits()
    results.append(("the calculator's blob lists Oxide's thirteen splits in the game's order, each "
                    "with its cap, the last at 100",
                    [s["name"] for s in sp] == ["Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron",
                                                "Candice", "HQ", "Galactic", "Volkner", "Barry", "League",
                                                "Post"]
                    and sp[0]["cap"] == 16 and sp[-1]["cap"] == 100
                    and all(a["cap"] < b["cap"] for a, b in zip(sp, sp[1:])), str([s["cap"] for s in sp])))
    calc = os.path.join(model.repo_root(), "tools", "oxide", "encounters", "calc")
    read = lambda *p: open(os.path.join(calc, *p), encoding="utf-8").read()
    grid, page, init = read("js", "fragsheet", "aggrid_options.js"), read("index.html"), read("js", "initialize.js")
    results.append(("the Fragsheet has thirteen split slots, the stats view moved to 13 and no "
                    "comparison left against the old 9 (VENDORED.md patch 19)",
                    "const FRAGSHEET_SPLIT_SLOTS = 13;" in grid and "activeSplit == 9" not in grid
                    and "activeSplit != 9" not in grid and "i < 9;" not in grid
                    and all(f"field: 'split{i}'" in grid for i in range(13))
                    and all(f'id="split-{i}-tab"' in page for i in range(13))
                    and 'id="stats-tab" data-split="13"' in page, ""))
    results.append(("under the Oxide title the Fragsheet takes its split names and caps from the "
                    "blob, rather than vanilla Platinum's by a match on the title",
                    'splitData[TITLE] = {' in init and 'data["splits"].map(function (s) { return s.cap })' in init,
                    ""))

    # -- Ian's saves, from before the log ------------------------------------------------
    for label, copy in (("2026-09-21", T.IAN_COPY), ("2026-09-27", T.IAN_CURRENT)):
        if not os.path.exists(copy):
            results.append((f"Ian's {label} save (working copy not on this machine; skipped)", True, ""))
            continue
        with open(copy, "rb") as f:
            ian = f.read()
        s = S.parse(ian, copy)
        # The later save was made in his room after the intro, before the
        # starter, so its party is empty; the blocks are what must not move.
        results.append((f"Ian's {label} save predates the log: it reads as empty, and the save "
                        f"reader finds both blocks, unchanged by the log's footers",
                        B.read(ian, s)["state"] == "empty" and set(s["blocks"]) == {0, 1}
                        and not B.footer_positions(ian), f"{len(s['party'])} in the party"))

    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
