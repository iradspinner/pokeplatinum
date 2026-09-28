"""Reads the battle log Oxide keeps in the save: its last 60 trainer battles,
who fought and who knocked out whom (Ian's request 4, 2026-09-27), for the
calculator's Battle Log and Fragsheet.

    PYTHONPATH=. python3 -m tools.oxide.encounters.cli battlelog PATH

Read-only, like savefile.py. The byte layout is docs/oxide/battle-log.md, the
engine side's own account of what it writes. In short: each flash half keeps
one copy of the log in its sector 44, a header, a ring of records and a
footer carrying the game's signature, a save counter and a CRC. The reader
takes the valid copy with the higher counter, as the game does with its own
blocks, and reads the records newest first from the ring's `next`.

The record size and capacity are read from the header rather than assumed,
so a later version that adds a field at the end still reads. A version this
reader has never seen is reported, not guessed at.

A save from before the log existed has both sectors erased, which reads as
an empty log, not as an error.
"""
import functools
import os
import struct

from . import dex
from . import model
from . import savefile

MAGIC = b"OBL1"
SECTORS = (0x2C000, 0x6C000)     # sector 44 of the primary and backup halves
HEADER_SIZE = 16
FOOTER_SIZE = 16                 # signature, save counter, size, id, CRC
LOG_ID = 0x4C42
KNOWN_VERSIONS = {1: 58}         # version: the record size it writes
EGG = 0x7FF                      # an egg in the party, a value no species reaches
# Knock-out credit values (battle-log.md, "Knock-out credit").
PARTNER, INDIRECT, NONE = 6, 7, 0xF
FLAG_WON, FLAG_LOST, FLAG_DOUBLE, FLAG_PARTNER, FLAG_TWO_TRAINERS = 1, 2, 4, 8, 16


# -- the copies -------------------------------------------------------------------

def _copy(data, at):
    """One copy of the log as its header and footer describe it, and whether
    it checks: {"at", "valid", "reason", ...}. Nothing is decoded yet."""
    out = {"at": at, "valid": False}
    if len(data) < at + HEADER_SIZE:
        return dict(out, reason="the file ends before this sector")
    if data[at:at + 4] != MAGIC:
        erased = all(b == 0xFF for b in data[at:at + HEADER_SIZE])
        return dict(out, reason="erased: a save from before the log" if erased else "no log magic")
    version, size, capacity, count, nxt = struct.unpack_from("<5H", data, at + 4)
    out.update(version=version, record_size=size, capacity=capacity, count=count, next=nxt)
    body = HEADER_SIZE + size * capacity
    if not size or not capacity or len(data) < at + body + FOOTER_SIZE:
        return dict(out, reason="its header gives no room for records")
    sig, counter, covered, log_id, crc = struct.unpack_from("<IIIHH", data, at + body)
    out.update(counter=counter, footer_at=at + body)
    if sig != savefile.SIGNATURE or log_id != LOG_ID:
        return dict(out, reason="its footer is not the log's")
    if covered != body:
        return dict(out, reason=f"its footer covers {covered:#x} bytes, not {body:#x}")
    if savefile.crc16(data[at:at + body]) != crc:
        return dict(out, reason="its checksum fails")
    if count > capacity or nxt >= capacity:
        return dict(out, reason=f"it holds {count} of {capacity} with next at {nxt}")
    out["valid"], out["reason"] = True, None
    return out


def copies(data):
    """Both copies, primary first, each as `_copy` describes it."""
    return [_copy(data, at) for at in SECTORS]


def footer_positions(data):
    """Where the log's footer signatures sit in the file, so the save reader's
    footer scan does not mistake them for the main save's blocks (the log's
    footer is laid out differently, and its size leaves out the footer)."""
    out = set()
    for at in SECTORS:
        if data[at:at + 4] != MAGIC or len(data) < at + HEADER_SIZE:
            continue
        size, capacity = struct.unpack_from("<HH", data, at + 6)
        out.add(at + HEADER_SIZE + size * capacity)
    return out


def current(data):
    """The copy the game would read back: the valid one with the higher save
    counter, or None when neither is valid."""
    valid = [c for c in copies(data) if c["valid"]]
    return max(valid, key=lambda c: c["counter"]) if valid else None


# -- one record -------------------------------------------------------------------

def _nibbles(raw):
    """Six 4-bit values, slot 0 in the low half of the first byte."""
    out = []
    for b in raw:
        out += [b & 0xF, b >> 4]
    return out[:6]


def decode_record(raw):
    """One version-1 record, ids and all, as battle-log.md lays it out."""
    ta, tb, turns, flags, split = struct.unpack_from("<HHHBB", raw, 0)
    counts = raw[0x39]
    return {
        "trainer_a": ta, "trainer_b": tb, "turns": turns, "flags": flags, "split": split,
        "player": list(struct.unpack_from("<6H", raw, 0x08)),
        "player_pid8": list(raw[0x14:0x1A]),
        "player_levels": list(raw[0x1A:0x20]),
        "opponents": list(struct.unpack_from("<6H", raw, 0x20)),
        "opponent_levels": list(raw[0x2C:0x32]),
        "ko_of_opponent": _nibbles(raw[0x32:0x35]),
        "ko_of_player": _nibbles(raw[0x35:0x38]),
        "player_count": raw[0x38], "count_a": counts & 0xF, "count_b": counts >> 4,
    }


def raw_records(data, copy=None):
    """The chosen copy's records, newest first, decoded but not named."""
    copy = copy or current(data)
    if not copy or copy["version"] not in KNOWN_VERSIONS:
        return []
    at, size, cap = copy["at"] + HEADER_SIZE, copy["record_size"], copy["capacity"]
    out = []
    for back in range(copy["count"]):
        i = (copy["next"] - 1 - back) % cap
        rec = decode_record(data[at + i * size:at + (i + 1) * size])
        rec["ring_slot"] = i
        out.append(rec)
    return out


# -- names ------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _names():
    """Today's species, trainer and split names by the ids a record stores."""
    root = model.repo_root()
    from . import calc_trainers, canon
    species = savefile._tables()["species"]
    with open(os.path.join(root, "generated", "trainers.txt"), encoding="utf-8") as f:
        trainers = [line.strip() for line in f if line.strip()]
    lay = savefile._vars_layout()
    return {"species": species, "calc_species": [canon.showdown_name(s) for s in species],
            "trainers": trainers, "trainer_name": calc_trainers.trainer_name,
            "splits": lay["splits"], "caps": lay["caps"]}


def species_name(value, calc=False):
    """A stored (form << 11) | species as a name: the calculator's spelling
    when `calc`, else the OxiDex's. A form shows as its species, as the
    calculator's Sync shows it."""
    if value == EGG:
        return "Egg"
    sid = value & 0x7FF
    n = _names()
    if sid == 0:
        return None
    if sid >= len(n["species"]):
        return f"#{sid}"
    return n["calc_species"][sid] if calc else dex.display_name(n["species"][sid])


@functools.lru_cache(maxsize=512)
def trainer_name(trainer_id):
    """A trainer id as the calculator names it ("Youngster Tristan"), or
    "Trainer #id" for one this build does not have."""
    import json
    n = _names()
    if not 0 < trainer_id < len(n["trainers"]):
        return f"Trainer #{trainer_id}"
    stem = n["trainers"][trainer_id][len("TRAINER_"):].lower()
    path = os.path.join(model.repo_root(), "res", "trainers", "data", stem + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            return n["trainer_name"](model.repo_root(), json.load(f), stem)
    except (OSError, KeyError, ValueError):
        return f"Trainer #{trainer_id}"


# -- the whole log ----------------------------------------------------------------

def _credit(value, count, side_word):
    """A knock-out credit value as {"by": slot or None, "how": word}."""
    if value < count and value <= 5:
        return {"by": value, "how": side_word}
    return {"by": None, "how": {PARTNER: "partner" if side_word == "player" else "own side",
                                INDIRECT: "indirect", NONE: None}.get(value, f"#{value}")}


def _match(save, species_id, pid8):
    """The Pokemon in the save that a logged one is: the same personality byte
    and the same evolution line (it may have evolved since), the party before
    the boxes, the same species before a relative. None when nothing fits."""
    if not save or species_id in (0, EGG):
        return None
    n = _names()
    if species_id >= len(n["species"]):
        return None
    root = model.repo_root()
    const = n["species"][species_id]
    line = dex.line_of(root, const)
    fits = [m for m in save["party"] + save["boxes"]
            if not m["is_egg"] and m["personality"] & 0xFF == pid8
            and dex.line_of(root, m["species"]) == line]
    fits.sort(key=lambda m: (m["species"] != const, "box" in m))
    return fits[0] if fits else None


def read(data, save=None):
    """The log in a save's bytes, named: {"state", "copy", "records"}, the
    records newest first. `save` is savefile.parse's reading of the same
    bytes, used to say which Pokemon now in the save each logged one is."""
    all_copies = copies(data)
    chosen = current(data)
    if not chosen:
        erased = all(c.get("reason", "").startswith("erased") for c in all_copies)
        return {"state": "empty" if erased else "invalid",
                "reason": "no log: a save from before the battle log" if erased
                else "; ".join(f"{c['at']:#x}: {c['reason']}" for c in all_copies),
                "copies": all_copies, "records": []}
    if chosen["version"] not in KNOWN_VERSIONS:
        return {"state": "unknown-version", "copies": all_copies, "records": [],
                "reason": f"log version {chosen['version']}, which this reader does not know"}
    n = _names()
    records = []
    for rec in raw_records(data, chosen):
        pc = min(rec["player_count"], 6)
        opp_count = min(rec["count_a"] + rec["count_b"], 6)
        player = []
        for i in range(pc):
            value = rec["player"][i]
            mon = _match(save, value & 0x7FF, rec["player_pid8"][i])
            player.append({
                "slot": i, "species": species_name(value), "calc_species": species_name(value, True),
                "species_id": value & 0x7FF, "form": value >> 11, "is_egg": value == EGG,
                "level": rec["player_levels"][i], "pid8": rec["player_pid8"][i],
                "ko_by": _credit(rec["ko_of_player"][i], opp_count, "opponent"),
                "now": {k: mon.get(k) for k in ("slot", "name", "level", "nature", "ability",
                                                  "personality", "species", "species_id")}
                if mon else None,
            })
        opponents = []
        for i in range(opp_count):
            value = rec["opponents"][i]
            opponents.append({
                "slot": i, "trainer": "A" if i < rec["count_a"] else "B",
                "species": species_name(value), "calc_species": species_name(value, True),
                "species_id": value & 0x7FF, "form": value >> 11,
                "level": rec["opponent_levels"][i],
                "ko_by": _credit(rec["ko_of_opponent"][i], pc, "player"),
            })
        split = n["splits"].get(rec["split"])
        flags = rec["flags"]
        records.append({
            "ring_slot": rec["ring_slot"],
            "trainer_a": rec["trainer_a"], "trainer_a_name": trainer_name(rec["trainer_a"]),
            "trainer_b": rec["trainer_b"] or None,
            "trainer_b_name": trainer_name(rec["trainer_b"]) if rec["trainer_b"] else None,
            "turns": rec["turns"],
            "result": ("draw" if flags & FLAG_WON and flags & FLAG_LOST else
                       "won" if flags & FLAG_WON else "lost" if flags & FLAG_LOST else None),
            "double": bool(flags & FLAG_DOUBLE), "partner": bool(flags & FLAG_PARTNER),
            "two_trainers": bool(flags & FLAG_TWO_TRAINERS),
            "split_index": rec["split"], "split": split,
            "player": player, "opponents": opponents,
        })
    return {"state": "ok", "copy": {k: chosen[k] for k in ("at", "counter", "version",
                                                           "record_size", "capacity", "count", "next")},
            "copies": all_copies, "records": records}


def describe(rec):
    """One battle in a few lines, as `cli battlelog` prints it."""
    who = rec["trainer_a_name"] + (f" and {rec['trainer_b_name']}" if rec["trainer_b_name"] else "")
    head = (f"{who}: {rec['result'] or 'no result'} in {rec['turns']} turn"
            f"{'s' if rec['turns'] != 1 else ''}" + (f", {rec['split']}'s split" if rec["split"] else ""))
    lines = [head]
    for o in rec["opponents"]:
        k = o["ko_by"]
        by = (rec["player"][k["by"]]["species"] if k["by"] is not None and k["by"] < len(rec["player"])
              else k["how"])
        lines.append(f"  Lv {o['level']} {o['species']}: " + (f"knocked out by {by}" if by else "stood"))
    for p in rec["player"]:
        k = p["ko_by"]
        if k["by"] is not None and k["by"] < len(rec["opponents"]):
            lines.append(f"  your {p['species']} fell to {rec['opponents'][k['by']]['species']}")
        elif k["how"]:
            lines.append(f"  your {p['species']} fell ({k['how']})")
    return lines


# -- the calculator's Battle Log ---------------------------------------------------

def calc_payload(log, save=None):
    """The log as the calculator's Battle Log stores a save file's log
    (`updateSaveFileBattleLog`'s payload: session_start, the knock-outs, then
    session_end, oldest battle first), with every name already the
    calculator's, under the version "oxide-save-v1" that the Oxide patch to
    battle_log.js passes through undecoded. `splits` gives the Battle Log its
    split tabs: Oxide's level-cap splits, by index, with their caps."""
    events, counters = [], {}
    for index, rec in enumerate(reversed(log.get("records") or [])):
        party = []
        for p in rec["player"]:
            now = p["now"] or {}
            name = p["calc_species"] or "Unknown"
            party.append({
                "species": name, "loggedSpecies": name, "level": p["level"],
                "nickname": "", "heldItem": "None", "moves": [],
                "ability": now.get("ability") or "Unknown", "nature": now.get("nature") or "Unknown",
                "currentSpecies": species_name(now["species_id"], True) if now.get("species_id") else name,
            })
            if p["now"]:
                key = p["now"]["personality"]
                c = counters.setdefault(key, {"species": party[-1]["currentSpecies"], "koCount": 0,
                                              "battlesBrought": 0, "battlesUsed": 0})
                c["battlesBrought"] += 1
        events.append({
            "type": "session_start", "enemyTrainerIdA": rec["trainer_a"],
            "enemyTrainerIdB": rec["trainer_b"] or 0, "pParty": party,
            "hideMoves": True, "hideHeldItems": True, "saveFileRecordIndex": index,
            "saveFileSplitIndex": rec["split_index"],
            "oxide": {"turns": rec["turns"], "result": rec["result"], "double": rec["double"],
                      "partner": rec["partner"], "split": rec["split"],
                      "opponents": [{"species": o["calc_species"], "level": o["level"],
                                     "trainer": o["trainer"]} for o in rec["opponents"]]},
        })
        for o in rec["opponents"]:
            k = o["ko_by"]
            base = {"turn": o["slot"], "aiSpecies": o["calc_species"] or "Unknown",
                    "aiLevel": o["level"], "aiPartySlot": o["slot"]}
            if k["by"] is not None and k["by"] < len(party):
                events.append(dict(base, type="pKo", pSlot=k["by"], pSpecies=party[k["by"]]["species"]))
                now = rec["player"][k["by"]]["now"]
                if now:
                    counters[now["personality"]]["koCount"] += 1
            elif k["how"] == "partner":
                events.append(dict(base, type="partnerKo"))
        for p in rec["player"]:
            k = p["ko_by"]
            if k["by"] is not None and k["by"] < len(rec["opponents"]):
                o = rec["opponents"][k["by"]]
                events.append({"type": "aiKo", "turn": p["slot"], "pSlot": p["slot"],
                               "pSpecies": party[p["slot"]]["species"],
                               "aiSpecies": o["calc_species"] or "Unknown", "aiLevel": o["level"],
                               "aiPartySlot": o["slot"]})
        events.append({"type": "session_end"})
    from . import calc_export
    return {
        "version": "oxide-save-v1", "sourceType": "save-file", "preserveDuplicateTrainers": True,
        "overflow": False, "omittedCorruptRecordCount": 0, "corruptRecordReason": "",
        "recordCount": len(log.get("records") or []),
        "splits": calc_export.splits(),
        "pokemonBattleCounters": list(counters.values()),
        "events": events,
    }


# -- for tests: a log image the way the engine writes one --------------------------

def pack_record(rec):
    """The inverse of decode_record, for building test saves."""
    def nib(vals):
        vals = list(vals) + [NONE] * (6 - len(vals))
        return bytes(vals[i] | vals[i + 1] << 4 for i in range(0, 6, 2))

    def six(vals, fill=0):
        return list(vals) + [fill] * (6 - len(vals))
    raw = struct.pack("<HHHBB", rec["trainer_a"], rec.get("trainer_b", 0), rec.get("turns", 1),
                      rec.get("flags", FLAG_WON), rec.get("split", 0))
    raw += struct.pack("<6H", *six(rec["player"]))
    raw += bytes(six(rec.get("player_pid8", []))) + bytes(six(rec.get("player_levels", [])))
    raw += struct.pack("<6H", *six(rec["opponents"]))
    raw += bytes(six(rec.get("opponent_levels", [])))
    raw += nib(rec.get("ko_of_opponent", [])) + nib(rec.get("ko_of_player", []))
    count_b = rec.get("count_b", 0)
    raw += bytes([len(rec["player"]), (len(rec["opponents"]) - count_b) | count_b << 4])
    assert len(raw) == KNOWN_VERSIONS[1]
    return raw


def pack_copy(records, counter=1, capacity=60, start=0):
    """One copy of the log holding `records` (oldest first), written into the
    ring from `start` as the engine would after wrapping."""
    size = KNOWN_VERSIONS[1]
    ring = bytearray(size * capacity)
    for n, rec in enumerate(records[-capacity:]):
        i = (start + n) % capacity
        ring[i * size:(i + 1) * size] = pack_record(rec)
    count = min(len(records), capacity)
    body = MAGIC + struct.pack("<6H", 1, size, capacity, count, (start + count) % capacity, 0) + ring
    return body + struct.pack("<IIIHH", savefile.SIGNATURE, counter, len(body), LOG_ID,
                              savefile.crc16(body))
