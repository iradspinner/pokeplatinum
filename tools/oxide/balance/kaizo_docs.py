"""Platinum Kaizo's own documentation, read once into kaizo_docs.json.

    PYTHONPATH=. python3 -m tools.oxide.balance.kaizo_docs [path to the .xlsx]

The learnset study's analyses need what Kaizo's calculator file does not
hold: its wild encounter tables, its evolution levels and its list of wild
hazard moves. They are in Kaizo's documentation workbook, which Ian keeps on
the G: drive ("Platinum Kaizo Docs.xlsx"). This reads the sheets that carry
them and writes kaizo_docs.json beside this file, so the analyses run on any
machine, cloud sessions included, without the workbook. The workbook's
SHA-256 goes in the file, and a rerun on a changed workbook shows as a diff.

Sheets read:

- RAW Field Enc: each area's land table, twelve slots of rate, species and
  level, after a header row carrying the area's number, name and rate.
- RAW Water Enc: each area's Surf, Old, Good and Super Rod tables, five slots
  each with a level range.
- Swarm_ Day_ Night Encounters: the day and night species, which replace the
  land table's two 10% slots (the third and fourth) at their levels, as in
  vanilla Platinum. Swarms are read but, as in Oxide, not used.
- Evolutions: each species' methods, requirements and results.
- Wild Hazard Moves: the moves Kaizo's authors flagged as hazards in a wild
  battle, from the sheet's header row. Their note says the list leaves out
  recoil and trapping moves.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "kaizo_docs.json")
DEFAULT = "/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/Platinum Kaizo Docs.xlsx"


def _num(v):
    return int(v) if isinstance(v, (int, float)) else None


def _species(v):
    """A species cell, or None for an empty slot."""
    if not isinstance(v, str) or not v.strip() or set(v.strip()) <= {"-"}:
        return None
    return v.strip()


def field(ws):
    out = {}
    cur = None
    for row in ws.iter_rows(values_only=True):
        row = list(row) + [None] * 6
        if _num(row[0]) is not None and isinstance(row[1], str):
            cur = {"area": row[1].strip(), "rate": _num(row[4]) or 0, "slots": []}
            out[str(_num(row[0]))] = cur
        elif cur is not None and isinstance(row[2], (int, float)):
            cur["slots"].append([row[2], _species(row[3]), _num(row[4]) or 0])
    return out


def water(ws):
    # Slot rows hold each kind's species and level range from these columns;
    # the header row holds the four rates in pairs from column 3 (a label,
    # then the rate).
    kinds = [("surf", 3), ("old_rod", 6), ("good_rod", 9), ("super_rod", 12)]
    rate_col = {"surf": 4, "old_rod": 6, "good_rod": 8, "super_rod": 10}
    out = {}
    cur = None
    for row in ws.iter_rows(values_only=True):
        row = list(row) + [None] * 16
        if _num(row[0]) is not None and isinstance(row[1], str):
            cur = {"area": row[1].strip(),
                   "rates": {k: _num(row[rate_col[k]]) or 0 for k, _c in kinds},
                   **{k: [] for k, _c in kinds}}
            out[str(_num(row[0]))] = cur
        elif cur is not None and isinstance(row[2], (int, float)):
            for k, c in kinds:
                cur[k].append([row[2], _species(row[c]), _num(row[c + 1]) or 0,
                               _num(row[c + 2]) or 0])
    return out


def day_night(ws):
    out = {}
    cur = None
    for row in ws.iter_rows(values_only=True):
        row = list(row) + [None] * 6
        if _num(row[0]) is not None and isinstance(row[1], str):
            cur = {"area": row[1].strip(), "swarm": [], "day": [], "night": []}
            out[str(_num(row[0]))] = cur
        elif cur is not None and any(isinstance(row[c], str) for c in (2, 3, 4)):
            cur["swarm"].append(_species(row[2]))
            cur["day"].append(_species(row[3]))
            cur["night"].append(_species(row[4]))
    return out


def evolutions(ws):
    out = {}
    rows = ws.iter_rows(values_only=True)
    next(rows)
    for row in rows:
        if _num(row[0]) is None or not isinstance(row[1], str):
            continue
        evos = []
        for c in range(2, len(row) - 2, 3):
            method, need, result = row[c], row[c + 1], row[c + 2]
            if isinstance(method, str) and _species(result):
                evos.append([method.strip(), need if not isinstance(need, float) else int(need),
                             result.strip()])
        out[row[1].strip()] = evos
    return out


def hazards(ws):
    head = next(ws.iter_rows(values_only=True))
    return [v.strip() for v in head
            if isinstance(v, str) and v.strip().isupper() and v.strip().isalpha()]


def read(path=DEFAULT):
    import openpyxl
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return {
        "_comment": "Read from Platinum Kaizo's documentation workbook by kaizo_docs.py; "
                    "see its docstring for what each part holds.",
        "source": os.path.basename(path), "sha256": digest,
        "field": field(wb["RAW Field Enc"]), "water": water(wb["RAW Water Enc"]),
        "day_night": day_night(wb["Swarm_ Day_ Night Encounters"]),
        "evolutions": evolutions(wb["Evolutions"]), "hazards": hazards(wb["Wild Hazard Moves"]),
    }


def load():
    with open(OUT, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    docs = read(argv[0] if argv else DEFAULT)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"{len(docs['field'])} land tables, {len(docs['water'])} water tables, "
          f"{len(docs['day_night'])} day and night tables, {len(docs['evolutions'])} species' "
          f"evolutions, hazards {docs['hazards']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
