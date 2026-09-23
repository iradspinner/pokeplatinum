"""B1's data layer: every hack's trainers in one shape.

    PYTHONPATH=. python3 -m tools.oxide.balance.data roark

A trainer is a dict: hack, tr_id (None where the source has no ids), name,
location, battle_type, ai, and party, a list of Pokemon. A Pokemon is a
dict: species, level, item, ability, nature, ivs, evs, moves, all spelled
the way the damage calculator spells them, so the same records can be fed
to its engine later.

The references are the calculator's own data files for each hack, pinned in
~/roms/balance-refs with their SHA-256 sums in MANIFEST.txt. They are read
as JSON text and never executed. Oxide's own trainers are rebuilt from
res/trainers/ by the encounter tool's calc_trainers, which reconstructs the
nature, ability, IVs and default moves the game gives a party member.

The calculator's format keys each set by species and then by set name, so a
trainer who brings the same species twice under one name keeps only one of
them. That is a limit of every reference file, not of this reader; Oxide is
read per trainer and loses nothing.
"""
import functools
import glob
import json
import os
import re
import sys

from ..encounters import calc_trainers

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
REFS_DIR = os.path.expanduser("~/roms/balance-refs")
FIGHTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fights.json")

# Ian's ratings on his 1 to 10 scale (docs/oxide/balance-plan.md). "game"
# says whether the hack keeps Platinum's trainer ids, which is what lets a
# fight be looked up by id rather than matched by milestone.
REFS = {
    "vanilla": {"file": "pt.js", "title": "Vanilla Platinum", "rating": 3, "game": "platinum"},
    "renegade": {"file": "rp.js", "title": "Renegade Platinum", "rating": 7, "game": "platinum"},
    "redux": {"file": "platredux.js", "title": "Platinum Redux", "rating": 8, "game": "platinum"},
    "redux_hc": {"file": "platreduxhc.js", "title": "Platinum Redux hardcore", "rating": 8.5, "game": "platinum"},
    "kaizo": {"file": "pkv5h.js", "title": "Platinum Kaizo", "rating": 10, "game": "platinum"},
    # Hardlove is read from the donor ROM (hardlove_rom.py): the calculator's
    # file predates 0.6.9's Clair and League. The file stays as a cross-check.
    "hardlove": {"file": "hardlove.js", "title": "Hardlove Gold 0.6.9", "rating": 9.5,
                 "game": "hgss", "source": "rom"},
    "null": {"file": "null12.js", "title": "Pokemon Null 1.2", "rating": 10, "game": "emerald"},
    "unbound": {"file": "unbound.js", "title": "Pokemon Unbound, difficult", "rating": 5.25,
                "game": "firered", "mode": "difficult"},
    # Run & Bun is read from Ian's sheet of its battles (run_and_bun.py).
    "run_and_bun": {"file": "run-and-bun-trainer-battles.xlsx", "title": "Run & Bun",
                    "rating": 10, "game": "emerald", "source": "sheet"},
}

NO_MOVE = {"", "-", "(No Move)", "None"}
NO_ITEM = {"", "-", "None", "(No Item)"}
_LEVEL_PREFIX = re.compile(r"^Lvl \d+ ")
_LOCATION = re.compile(r"\|([^|]*)\|")


def _json_after_brace(text):
    """The object literal that starts at the first brace. The files are
    written as `backup_data = {...}` and are otherwise plain JSON."""
    body = text[text.index("{"):].rstrip()
    return json.loads(body[:-1] if body.endswith(";") else body)


@functools.lru_cache(maxsize=None)
def raw(hack):
    """The whole data file for a reference hack, as parsed JSON.

    Unbound's file is a script of one assignment per mode,
    `formatted_sets["difficult"] = {...}`, so only its sets are read, for the
    mode Ian rated."""
    spec = REFS[hack]
    with open(os.path.join(REFS_DIR, spec["file"]), encoding="utf-8") as f:
        text = f.read()
    if "mode" not in spec:
        return _json_after_brace(text)
    want = f'formatted_sets["{spec["mode"]}"] = '
    for line in text.split("\n"):
        if line.startswith(want):
            return {"formatted_sets": _json_after_brace(line[len(want):])}
    raise KeyError(f"{spec['file']} has no {spec['mode']} mode")


def split_set_name(name):
    """'Lvl 7 Youngster Tristan |Route 202| ' -> ('Youngster Tristan', 'Route 202')."""
    location = _LOCATION.search(name)
    base = _LOCATION.sub("", _LEVEL_PREFIX.sub("", name)).strip()
    return base, (location.group(1).strip() if location else None)


def _mon(species, s):
    item = s.get("item")
    return {
        "species": species,
        "level": s["level"],
        "item": None if item in NO_ITEM or item is None else item,
        "ability": s.get("ability"),
        "nature": s.get("nature"),
        "ivs": s.get("ivs"),
        "evs": s.get("evs"),
        "moves": [m for m in s.get("moves", []) if m not in NO_MOVE],
        "sub_index": s.get("sub_index"),
        "mega": None,
    }


def _ordered(trainers):
    for t in trainers.values():
        if all(m["sub_index"] is not None for m in t["party"]):
            t["party"].sort(key=lambda m: m["sub_index"])
    return trainers


def _fold_megas(trainers):
    """The calculator lists a Mega as its own set beside the Pokemon that
    becomes it ("Aerodactyl" and "Aerodactyl-Mega"). That is one Pokemon, so
    the Mega set is folded into its base as the form it turns into."""
    for t in trainers.values():
        by_species = {m["species"]: m for m in t["party"]}
        kept = []
        for m in t["party"]:
            base = m["species"].split("-Mega")[0] if "-Mega" in m["species"] else None
            if base and base in by_species and by_species[base] is not m:
                by_species[base]["mega"] = m["species"]
            else:
                kept.append(m)
        t["party"] = kept
    return trainers


def calc_sets(hack):
    """Every set the hack's calculator file holds, keyed as ref_trainers
    keys trainers, before Megas are folded. Tests count against this."""
    return _read_calc(hack)


@functools.lru_cache(maxsize=None)
def ref_trainers(hack):
    """Every trainer in a reference hack, keyed by tr_id where the source has
    ids, else by trainer name. Megas are folded into their base Pokemon."""
    if REFS[hack].get("source") == "rom":
        from . import hardlove_rom
        return hardlove_rom.trainers()
    if REFS[hack].get("source") == "sheet":
        from . import run_and_bun
        return run_and_bun.trainers()
    return _fold_megas(_read_calc(hack))


def _read_calc(hack):
    out = {}
    for species, sets in raw(hack)["formatted_sets"].items():
        for set_name, s in sets.items():
            name, location = split_set_name(set_name)
            key = s.get("tr_id", name)
            t = out.setdefault(key, {
                "hack": hack, "tr_id": s.get("tr_id"), "name": name,
                "location": location, "battle_type": s.get("battle_type"),
                "ai": s.get("ai"), "party": []})
            t["party"].append(_mon(species, s))
    return _ordered(out)


@functools.lru_cache(maxsize=None)
def oxide_trainers(root=ROOT):
    """Every Oxide trainer, rebuilt from res/trainers/data/, keyed by tr_id.
    The unused dummy_ slots are left out. Each trainer also carries its
    constant, which is TRAINER_ plus its file name in capitals."""
    out = {}
    for path in sorted(glob.glob(os.path.join(root, "res", "trainers", "data", "*.json"))):
        stem = os.path.basename(path)[:-len(".json")]
        if stem.startswith("dummy_"):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        party = calc_trainers.build_trainer(root, stem, data)
        if not party:
            continue
        tr_id = party[0][1]["tr_id"]
        out[tr_id] = {
            "hack": "oxide", "tr_id": tr_id, "name": calc_trainers.trainer_name(root, data, stem),
            "constant": "TRAINER_" + stem.upper(), "stem": stem, "location": None,
            "battle_type": "Doubles" if data.get("double_battle") else "Singles",
            "ai": party[0][1].get("ai"), "party": [_mon(sp, s) for sp, s in party]}
    return out


@functools.lru_cache(maxsize=None)
def fights():
    """The story bosses from fights.json, each with its trainers' ids
    resolved through Oxide's trainer constants."""
    with open(FIGHTS, encoding="utf-8") as f:
        spec = json.load(f)
    by_constant = {t["constant"]: t["tr_id"] for t in oxide_trainers().values()}
    for fight in spec["fights"]:
        fight["tr_ids"] = [by_constant[c] for c in fight["trainers"]]
    return spec


def fight_trainers(hack, fight):
    """The trainers a hack fields for one story fight. Hacks that keep
    Platinum's trainer ids are looked up by id; others need a milestone map,
    which B1 builds next, so they return nothing yet."""
    if hack == "oxide":
        pool, ids = oxide_trainers(), fight["tr_ids"]
    elif REFS[hack]["game"] == "platinum":
        pool = ref_trainers(hack)
        ids = fights()["overrides"].get(hack, {}).get(fight["key"], fight["tr_ids"])
    else:
        pool = ref_trainers(hack)
        ids = fights()["milestones"].get(hack, {}).get(fight["key"], [])
    return [pool[i] for i in ids if i in pool]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    key = argv[0] if argv else "roark"
    fight = next(f for f in fights()["fights"] if f["key"] == key)
    for hack in ["oxide"] + list(REFS):
        for t in fight_trainers(hack, fight):
            print(f"{hack:10} {str(t['tr_id'] or ''):>4} {t['name']}")
            for m in t["party"]:
                print(f"{'':16}{m['species']:12} {m['level']:>3} {str(m['item']):16} "
                      f"{str(m['nature']):8} {', '.join(m['moves'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
