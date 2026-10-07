"""B1 acceptance: the reference data, the story fights and the milestone maps.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b1

Reads the pinned reference files in ~/roms/balance-refs and res/trainers/.
Writes nothing.
"""
import glob
import hashlib
import json
import os
import re
import sys

from . import data

# Sets per file, counted by hand from the raw JSON on 2026-09-22. A loader
# that drops or duplicates members fails here before anything is scored.
SET_COUNTS = {"vanilla": 1873, "renegade": 2823, "redux": 2829, "redux_hc": 2829,
              "kaizo": 3077, "hardlove": 1871, "null": 2282, "unbound": 357}
# Words a trainer's name must contain for a fight to count as found. The
# calculator's data calls the rival "Pkmn Trainer Cedric".
NAME_WORD = {"barry": "Cedric", "mars": "Mars", "jupiter": "Jupiter",
             "saturn": "Saturn", "cyrus": "Cyrus"}
PLATINUM_HACKS = [h for h in data.REFS if data.REFS[h]["game"] == "platinum"]


def check_pinned_files(results):
    """Every reference file is the copy MANIFEST.txt pinned. A changed file
    would silently change every score calibrated on it."""
    with open(os.path.join(data.REFS_DIR, "MANIFEST.txt"), encoding="utf-8") as f:
        pinned = dict(reversed(line.split(None, 1)) for line in f
                      if line.strip() and not line.startswith("#"))
    bad = []
    for name, digest in pinned.items():
        with open(os.path.join(data.REFS_DIR, name.strip()), "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != digest:
                bad.append(name.strip())
    results.append(("every pinned reference file matches its SHA-256", not bad,
                    f"{len(pinned)} files" + (f", changed: {bad}" if bad else "")))


def check_set_counts(results):
    """The loader keeps every set each file holds, no more and no fewer."""
    for hack, want in SET_COUNTS.items():
        raw = sum(len(v) for v in data.raw(hack)["formatted_sets"].values())
        loaded = sum(len(t["party"]) for t in data.calc_sets(hack).values())
        results.append((f"{hack}: every set is read once", raw == want == loaded,
                        f"{raw} in the file, {loaded} loaded, {want} expected"))


def check_oxide_members(results):
    """Oxide is read per trainer, so every party member of every real
    trainer arrives, duplicates of a species included. A dummy_ slot is real
    when a map battles it and it is not a Maid's training battle (Ian's
    Lucas and Dawn fights, Krystal, Officer Argo)."""
    want = 0
    for path in glob.glob(os.path.join(data.ROOT, "res", "trainers", "data", "*.json")):
        stem = os.path.basename(path)[:-len(".json")]
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        if stem.startswith("dummy_") and (
                not {"TRAINER_" + stem.upper(), stem[len("dummy_"):]} & data.battled()
                or raw.get("class") == "TRAINER_CLASS_MAID"):
            continue
        want += len(raw["party"])
    got = sum(len(t["party"]) for t in data.oxide_trainers().values())
    results.append(("oxide: every party member of every real trainer is read",
                    got == want, f"{got} of {want}"))


def _word(fight):
    return NAME_WORD.get(fight["key"].split("_")[0], fight["label"].split()[0])


def check_fights_resolve(results):
    """Each story fight finds its trainers in Oxide and in every hack that
    keeps Platinum's ids, under a name that says who they are."""
    for hack in ["oxide"] + PLATINUM_HACKS:
        word_ok = lambda f, n: (_word(f) in n or (hack == "oxide" and _word(f) == "Cedric"
                                                  and "Barry" in n)
                                or (f["key"] == "mars_jupiter" and ("Mars" in n or "Jupiter" in n))
                                or (f["key"] == "flint_volkner" and ("Flint" in n or "Volkner" in n))
                                or (f["key"] == "somnu_moira" and ("Somnu" in n or "Moira" in n))
                                or (f["key"].startswith("lucas_dawn")
                                    and ("Lucas" in n or "Dawn" in n)))
        # A hack whose override lists no trainers has no seat for that fight
        # by design (Oxide's Lucas and Dawn fights, in slots the hacks leave
        # unused or give to their League).
        seated = [f for f in data.fights()["fights"]
                  if data.fights()["overrides"].get(hack, {}).get(f["key"]) != []]
        missing = []
        for fight in seated:
            ts = data.fight_trainers(hack, fight)
            if not ts or not all(word_ok(fight, t["name"]) for t in ts):
                missing.append(fight["key"])
        results.append((f"{hack}: all {len(seated)} story fights it seats resolve",
                        not missing, f"unresolved: {missing}" if missing else ""))


def check_sheet_levels(results):
    """Oxide's aces match Ian's Level Caps sheet, apart from the fights
    whose note says why not."""
    off = []
    for fight in data.fights()["fights"]:
        if fight["sheet_ace"] is None or "note" in fight:
            continue
        ace = max(m["level"] for t in data.fight_trainers("oxide", fight) for m in t["party"])
        if ace != fight["sheet_ace"]:
            off.append(f"{fight['key']} {ace} vs {fight['sheet_ace']}")
    results.append(("oxide's boss aces match the Level Caps sheet", not off, "; ".join(off)))


def check_league_after_volkner(results):
    """No hack's League is weaker than its last gym. This is the check that
    caught Kaizo and Redux keeping vanilla's League in Platinum's slots."""
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    for hack in ["oxide"] + PLATINUM_HACKS:
        ace = lambda k: max(m["level"] for t in data.fight_trainers(hack, by_key[k])
                            for m in t["party"])
        low = [k for k in ("aaron", "bertha", "flint", "lucian", "cynthia")
               if ace(k) < ace("volkner")]
        results.append((f"{hack}: the League is at or above Volkner", not low,
                        f"Volkner {ace('volkner')}" + (f", below it: {low}" if low else "")))


def check_roark(results):
    """Roark's party sizes, as read by hand from each file."""
    roark = next(f for f in data.fights()["fights"] if f["key"] == "roark")
    got = {h: len(data.fight_trainers(h, roark)[0]["party"])
           for h in ("oxide", "vanilla", "renegade", "kaizo")}
    want = {"oxide": 5, "vanilla": 3, "renegade": 6, "kaizo": 6}    # Oxide 5 since the comb (step 12)
    results.append(("Roark's party sizes", got == want, str(got)))


def check_megas_folded(results):
    """A Mega listed as its own set is folded into the Pokemon that becomes
    it, so no compared fight runs past six Pokemon a trainer. Null's gym
    leaders had seven before folding. Only the fights that get compared are
    checked: some filler keys (Null's Root Academy slots, Unbound's rivals
    keyed by name) hold several alternative teams under one key."""
    compared = data.fights()["fights"]
    for hack in ("null", "kaizo", "renegade", "unbound"):
        over = [t["name"] for f in compared for t in data.fight_trainers(hack, f)
                if len(t["party"]) > 6]
        megas = sum(1 for t in data.ref_trainers(hack).values() for m in t["party"] if m.get("mega"))
        results.append((f"{hack}: no compared fight over six a trainer, Megas folded", not over,
                        f"{megas} Megas folded" + (f"; over six: {over[:3]}" if over else "")))


def check_hardlove_rom(results):
    """Hardlove comes from the donor ROM. Its first seven gyms agree with the
    calculator's file wherever that file is current; the League is the
    ROM's own, at 82, with Lance an Elite Four member and Blue the Champion."""
    from . import hardlove_rom
    rom, calc = hardlove_rom.trainers(), data.calc_sets("hardlove")
    members = sum(len(t["party"]) for t in rom.values())
    results.append(("hardlove: every trainer in the ROM is read", (len(rom), members) == (737, 1909),
                    f"{len(rom)} trainers, {members} Pokemon"))
    # Falkner and Whitney are left out: the calculator's file has one old
    # level and no Galarian forms there, and the ROM is the newer of the two.
    diff = []
    for tr_id in (21, 31, 34, 33, 32):
        a = sorted((m["mega"] or m["species"], m["level"]) for m in rom[tr_id]["party"])
        b = sorted((m["species"], m["level"]) for m in calc[tr_id]["party"])
        if a != b:
            diff.append(tr_id)
    results.append(("hardlove: Bugsy to Pryce match the calculator's file", not diff,
                    f"differ: {diff}" if diff else "5 gyms, species and levels"))
    anchors = {m["species"]: m["types"] for t in rom.values() for m in t["party"]}
    ok = (rom[244]["name"].startswith("Elite Four") and rom[727]["name"].startswith("Champion")
          and anchors.get("Farfetch’d-Galar") == ["Fighting"]
          and anchors.get("Ninetales-Alola") == ["Ice", "Fairy"])
    results.append(("hardlove: League roles and form types read from the ROM", ok,
                    f"244 {rom[244]['name']}, 727 {rom[727]['name']}"))


def check_run_and_bun(results):
    """Ian's Run & Bun sheet: every Pokemon has a level, every boss a full
    set of moves. 76 filler trainers in the later splits have no moves on
    the sheet itself, which is the sheet's gap, not the reader's."""
    from . import run_and_bun
    ts = run_and_bun.trainers()
    members = sum(len(t["party"]) for t in ts.values())
    no_level = sum(1 for t in ts.values() for m in t["party"] if m["level"] is None)
    boss_gaps = [k for k, t in ts.items() if "[Boss]" in k and any(not m["moves"] for m in t["party"])]
    results.append(("run_and_bun: the sheet reads whole",
                    (len(ts), members, no_level, boss_gaps) == (436, 1832, 0, []),
                    f"{len(ts)} trainers, {members} Pokemon, {no_level} without a level, "
                    f"bosses without moves: {boss_gaps}"))


def check_milestones_resolve(results):
    """Each hack built on another game has a counterpart for every gym, Elite
    Four seat and Champion, found under the name its milestone map gives."""
    seats = ("roark", "gardenia", "fantina", "maylene", "wake", "byron", "candice", "volkner",
             "aaron", "bertha", "flint", "lucian", "cynthia")
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    for hack in ("hardlove", "null", "unbound", "run_and_bun"):
        want = data.fights()["milestones"][hack]
        missing = [k for k in seats if len(data.fight_trainers(hack, by_key[k])) != len(want[k])]
        results.append((f"{hack}: all 13 gym and League seats resolve", not missing,
                        f"unresolved: {missing}" if missing else ""))


# Trainers no map fields are expected to be one of these: a numbered or
# rematch copy, a tag partner or unused rival variant, or an unused slot.
UNPLACED_OK = re.compile(r"rematch|_\d+$|^rival_|^lucas_|^dawn_|^cheryl_|^mira_|^riley_"
                         r"|^marley_|^buck_|_unused$")
# First-run trainers the base ROM itself took off the map: Test.nds (the base
# ROM since 2026-09-25) puts Beauty Devon where Collector Brady stood.
REMOVED_BY_BASE = {"collector_brady"}


def check_split_map(results):
    """B1d: every map outside the internal Mystery Zone has a split; every
    story fight lands in the split Ian's sheet gives it, apart from the
    fights STORY_REVISITS lists, which do not; and no trainer stays
    unplaced unless it is a rematch copy, a partner or rival variant, or an
    unused slot."""
    from . import splits
    unplaced = sorted({splits.location_name(h) for h in splits.headers()
                       if splits.map_split(h)[0] is None} - {"Mystery Zone"})
    results.append(("every map but the internal ones has a split", not unplaced,
                    f"{len(splits.headers())} maps" + (f", unplaced: {unplaced}" if unplaced else "")))
    wrong, revisits = [], []
    for fight in data.fights()["fights"]:
        got = {splits.trainer_split(t) for t in fight["tr_ids"]}
        (revisits if fight["key"] in splits.STORY_REVISITS else wrong).append(
            (fight["key"], got == {fight["split"]}))
    bad = [k for k, ok in wrong if not ok] + [k for k, ok in revisits if ok]
    results.append(("every story fight's map lands in its sheet split", not bad,
                    f"{len(wrong)} fights, {len(revisits)} listed revisits"
                    + (f"; wrong: {bad}" if bad else "")))
    ox = data.oxide_trainers()
    stray = [ox[t]["stem"] for t in ox if splits.trainer_split(t) is None
             and not UNPLACED_OK.search(ox[t]["stem"]) and ox[t]["stem"] not in REMOVED_BY_BASE]
    placed = sum(1 for t in ox if splits.trainer_split(t))
    results.append(("no first-run trainer is left without a split", not stray,
                    f"{placed} placed" + (f"; stray: {stray[:5]}" if stray else "")))


def check_items_and_marts(results):
    """Every item ball and hidden item names an item and has a split, and
    every mart table has its city's split. Two anchors: Poke Balls are on
    sale from the start, and the Eterna herb shop opens in Gardenia's split."""
    from . import splits
    items = splits.item_reach()
    loose = [(h, i) for sp, h, i, _how, needs in items
             if (not sp and needs != "unreached") or not i or not i.startswith("ITEM_")]
    results.append(("every item ball and hidden item resolves", not loose,
                    f"{len(items)} items" + (f"; loose: {loose[:3]}" if loose else "")))
    marts = splits.marts()
    poke = [sp for sp, t, i in marts if t == "common" and i == "ITEM_POKE_BALL"]
    herb = {sp for sp, t, _i in marts if t == "EternaHerbShopStock"}
    ok = not [m for m in marts if m[0] is None] and poke == ["Roark"] and herb == {"Gardenia"}
    results.append(("every mart item has a split", ok, f"{len(marts)} mart items"))


def _table():
    """The reward table's rows (docs/oxide/reward-placements.tsv)."""
    import csv
    with open(os.path.join(data.ROOT, "docs", "oxide", "reward-placements.tsv"), encoding="utf-8") as f:
        return list(csv.DictReader((line for line in f if not line.startswith("#")), delimiter="\t"))


def check_tm_sources(results):
    """Every TM and HM on the TM pass's list (docs/oxide/tm-list.tsv) is
    found in a ball, a hidden item, a gift, a shop or a trainer's reward,
    and Roark's gym gives what the reward table says in Roark's split. The
    Frontier's three (TM08, TM61, TM73), which no source read offered
    before, are placed by the table. Until step 10 applies the table to the
    tree (place_rewards.py), TM93 and TM94 have no source and this fails."""
    import csv
    from . import splits
    found = {}
    for sp, _h, item, _how in splits.items():
        found.setdefault(item, sp)
    for sp, _t, item in splits.marts():
        found.setdefault(item, sp)
    for sp, _h, item in splits.gifts():
        found.setdefault(item, sp)
    for sp, _t, item in splits.trainer_rewards():
        found.setdefault(item, sp)
    with open(os.path.join(data.ROOT, "docs", "oxide", "tm-list.tsv"), encoding="utf-8") as f:
        tms = [f"ITEM_{r['tm']}" for r in csv.DictReader(f, delimiter="\t")]
    missing = [t for t in tms if t not in found]
    gym = next((r["reward"] for r in _table() if r["map"] == "MAP_HEADER_OREBURGH_CITY_GYM" and r["kind"] == "gift"),
               None)
    roark = [(sp, h) for sp, h, item in splits.gifts() if item == gym]
    ok = not missing and ("Roark", "OREBURGH_CITY_GYM") in roark
    results.append(("every TM and HM on the list has a source", ok,
                    f"{len(tms) - len(missing)} of {len(tms)}; not found: {missing}; "
                    f"Roark's gym gives {gym}: {bool(roark)}"))
    # The table's trainer rewards and once-sold TMs, as the census reads them
    # once step 10 has written them: each at its row's split.
    rewards = set(splits.trainer_rewards())
    marts = {(sp, item) for sp, _t, item in splits.marts()}
    off = [(r["trainer_id"], r["reward"]) for r in _table()
           if r["kind"] == "trainer" and (r["split"], r["trainer_id"], r["reward"]) not in rewards]
    off += [(r["place"], r["reward"]) for r in _table()
            if r["kind"] in ("mart", "prize") and r["reward"] != "ITEM_NONE"
            and (splits.BADGE_SPLIT[int(r["badges"])], r["reward"]) not in marts]
    results.append(("the census reads the table's trainer rewards and once-sold TMs at their splits", not off,
                    f"{len(off)} not read: {off[:4]}" if off else "all read"))


def check_weather(results):
    """The weather the base ROM set on three gyms and two Elite Four rooms,
    as a battle sees it: sand at Roark's, rain at Wake's, hail at Candice's
    and Bertha's sand. Flint's ashfall starts no battle weather."""
    from . import splits
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    got = {k: splits.trainer_weather(by_key[k]["tr_ids"][0])
           for k in ("roark", "wake", "candice", "bertha", "flint")}
    want = {"roark": ["Sand"], "wake": ["Rain"], "candice": ["Hail"], "bertha": ["Sand"], "flint": []}
    results.append(("boss fights start in the weather their maps set", got == want, str(got)))


# When each way opens (Ian's split definition for the bike; the badge alone
# for the rest, since main-field-moves), and one item behind each, as the
# census had them wrong: Lake
# Verity's TM38 in Roark's split, Oreburgh Gate B1F's TM01 in Byron's,
# Valor Lakefront's Sun Stone in Wake's, and so on. Five of those balls now
# hold the reward table's items (step 10, 2026-10-07), named here.
FIELD_MOVE_SPLITS = {"Bicycle": "Fantina", "Rock Smash": "Gardenia", "Cut": "Fantina", "Surf": "Byron",
                     "Strength": "Candice", "Rock Climb": "HQ", "Waterfall": "Barry"}
REACH_ANCHORS = [("LAKE_VERITY", "ITEM_LUM_BERRY", "Byron", "Surf"),
                 ("RAVAGED_PATH", "ITEM_LUM_BERRY", "Gardenia", "Rock Smash"),
                 ("ETERNA_CITY", "ITEM_TM83", "Fantina", "Cut"),
                 ("OREBURGH_GATE_B1F", "ITEM_TM20", "Candice", "Strength"),
                 ("VALOR_LAKEFRONT", "ITEM_SUN_STONE", "HQ", "Rock Climb"),
                 ("ROUTE_208", "ITEM_CARBOS", "Barry", "Waterfall"),
                 ("SOLACEON_TOWN", "ITEM_PP_UP", "Maylene", "foot"),
                 ("WAYWARD_CAVE_B1F", "ITEM_RARE_CANDY", "Fantina", "Bicycle"),
                 ("VICTORY_ROAD_B1F", "ITEM_SITRUS_BERRY", "Barry", "Waterfall"),
                 ("AMITY_SQUARE", "ITEM_SPOOKY_PLATE", "Fantina", "foot"),
                 ("VICTORY_ROAD_2F", "ITEM_MAX_ELIXIR", "Barry", "Strength")]
# The items the flood cannot reach with every way open, named so a new one
# is noticed and goes on Ian's in-game checklist; the census gives them no
# split. None since Ian's answers of 2026-09-29: Wayward Cave's basement by
# ramp jumps, Amity Square's plate through the ruins' teleporters, Victory
# Road 2F's Max Elixir by a slow-gear ramp jump, and B1F's TM59 once
# waterfalls were read before the collision bit.
UNREACHED = set()


def check_item_reach(results):
    """An item behind water, a waterfall, a Rock Climb wall, a bike path or
    a Rock Smash rock, Cut tree or Strength boulder counts from the split
    the way to it first opens; one on foot keeps its map's; an item on
    several maps under one pickup flag counts once; and the items nothing
    reaches are the named ones. Each way opens when the game's own check
    allows it, the badge it names won (no HM since main-field-moves), with
    Surf where the encounter tool has it."""
    from . import splits
    moves = splits.field_move_splits()
    ok = moves == FIELD_MOVE_SPLITS and moves["Surf"] == splits.surf_split()
    results.append(("each field move opens in the split after its badge is won", ok, str(moves)))
    rows = splits.item_reach()
    got = {(r[1], r[2]): (r[0], r[4]) for r in rows}
    wrong = [(m, i, got.get((m, i))) for m, i, s, n in REACH_ANCHORS if got.get((m, i)) != (s, n)]
    results.append(("an item counts from the split the way to it opens", not wrong,
                    str(wrong) if wrong else f"{len(REACH_ANCHORS)} anchors"))
    unreached = {(r[1], r[2]) for r in rows if r[4] == "unreached"}
    ok = unreached == UNREACHED and all(r[0] is None for r in rows if r[4] == "unreached")
    results.append(("the items nothing reaches are the named ones, with no split", ok,
                    f"new {sorted(unreached - UNREACHED)}, gone {sorted(UNREACHED - unreached)}"
                    if not ok else f"{len(unreached)} named"))
    keys = splits.pickups()
    water = splits._surfable()
    ok = len(rows) == len(keys) and {"TILE_BEHAVIOR_WATER_SEA", "TILE_BEHAVIOR_WATER_RIVER"} <= water \
        and not [n for n in water if "BRIDGE" in n]
    results.append(("each pickup counts once, and only water is surfable", ok,
                    f"{len(rows)} items from {sum(len(m) for _r, m in keys.values())} map copies"))


def check_testkit(results):
    """The test kit adds nothing to the census, since only `make testkit`
    builds it. The filter keeps what a normal build keeps, #else branches
    and other conditionals included; no field script holds a conditional
    other than the kit's, so a new one gets a decision about which branch
    the census reads; and no item or trainer that only a kit block names
    reaches the gifts, the trainer maps or the battled set. The kit block
    does name items (its Rare Candies), so the last part has teeth."""
    from . import splits
    sample = ["a", "#ifdef OXIDE_TESTKIT", "kit", "#ifdef OTHER", "kit2", "#endif", "#else",
              "plain", "#endif", "#ifndef OXIDE_TESTKIT", "b", "#else", "kit3", "#endif",
              "#ifdef OTHER", "c", "#else", "d", "#endif", "e"]
    want = ["a", "plain", "b", "#ifdef OTHER", "c", "#else", "d", "#endif", "e"]
    got = data.without_testkit("\n".join(sample)).split("\n")
    results.append(("the test-kit filter keeps what a normal build keeps", got == want,
                    "sample of nested and #else blocks" if got == want else f"got {got}"))
    kit_files, other = {}, []
    for path in sorted(glob.glob(os.path.join(data.ROOT, "res", "field", "scripts", "*.s"))):
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        heads = [line.split()[:2] for line in raw.split("\n") if line.split()[:1] in (["#if"], ["#ifdef"], ["#ifndef"])]
        if any(h[1:] == [data.TESTKIT] for h in heads):
            kit_files[os.path.basename(path)[:-2]] = (raw, data.without_testkit(raw))
        other += [(os.path.basename(path), " ".join(h)) for h in heads if h[1:] != [data.TESTKIT] or h[0] == "#if"]
    results.append(("no field script has a conditional but the test kit's", not other,
                    f"{len(kit_files)} script(s) with kit blocks" + (f"; others: {other[:3]}" if other else "")))
    maps = {h for h, f in splits.headers().items() if f.get("scriptsArchiveID") in kit_files}
    items, trainers = set(), set()
    for raw, built in kit_files.values():
        items |= set(re.findall(r"\bITEM_\w+", raw)) - set(re.findall(r"\bITEM_\w+", built))
        trainers |= set(re.findall(r"\bTRAINER_\w+", raw)) - set(re.findall(r"\bTRAINER_\w+", built))
    leaked = sorted({i for _s, h, i in splits.gifts() if h in maps and i in items})
    ids = {data.oxide_trainers()[t]["constant"] for t in data.oxide_trainers()} & trainers
    tr_ids = {t for t in data.oxide_trainers() if data.oxide_trainers()[t]["constant"] in ids}
    leaked += sorted(str(t) for t in tr_ids if maps & (splits.trainer_maps().get(t, set())
                                                       | splits.trainer_mentions().get(t, set())))
    leaked += sorted(trainers & data.battled())
    results.append(("nothing only the test kit names reaches the census",
                    "ITEM_RARE_CANDY" in items and not leaked,
                    f"{len(items)} kit-only items, {len(trainers)} kit-only trainers"
                    + (f"; leaked: {leaked[:5]}" if leaked else "")))


def main():
    results = []
    for check in (check_pinned_files, check_set_counts, check_oxide_members,
                  check_fights_resolve, check_sheet_levels,
                  check_league_after_volkner, check_roark, check_megas_folded,
                  check_hardlove_rom, check_run_and_bun, check_milestones_resolve,
                  check_split_map, check_items_and_marts, check_tm_sources,
                  check_weather, check_item_reach, check_testkit):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
