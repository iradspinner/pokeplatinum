"""The alpha checklist (alpha readiness step 17): every count on the page
against the data it is read from.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_alpha

Read-only. Each source is counted on its own and then found on the page:
every story fight and every trainer the census places once, every ball and
hidden item once, every NPC gift once, every row of the reward table once
(a trainer's reward on that trainer, a ball or gift on the place it
replaces, a shop TM in the shop list), every wild table a map uses once,
every scripted capture once, and every in-game checklist item once.
"""
import collections
import json
import os
import sys

from . import alpha, locations, model, scripted
from ..balance import splits as bsplits


def _all(data, kind):
    """[(split, zone, row)] for one kind across the page; gauntlet trainers
    count as trainers."""
    out = []
    for s in data["splits"]:
        for z in s["zones"]:
            rows = list(z[kind])
            if kind == "trainers":
                rows += [t for g in z["gauntlets"] for t in g["trainers"]]
            out += [(s["split"], z["zone"], r) for r in rows]
    return out


def check_trainers(results, data, root):
    roles, _where = alpha.tables(root)["roles"]
    with open(os.path.join(root, alpha.FIGHTS), encoding="utf-8") as f:
        fights = json.load(f)["fights"]
    ids = alpha._trainer_ids(root)
    want_bosses = [f["key"] for f in fights if any(c in ids for c in f["trainers"])]
    bosses = {c for f in fights for c in f["trainers"]}
    want_ordinary = [r["trainer_id"] for r in roles if r["trainer_id"] not in bosses]
    got = collections.Counter(t["key"] for _s, _z, t in _all(data, "trainers"))
    once = all(got[k] == 1 for k in want_bosses + want_ordinary)
    extra = set(got) - set(want_bosses) - set(want_ordinary)
    results.append(("every story fight and every trainer the census places shows once",
                    once and not extra and len(want_ordinary) > 0,
                    f"{len(want_bosses)} fights, {len(want_ordinary)} trainers, extra {sorted(extra)[:3]}"))
    teams = [t for _s, _z, t in _all(data, "trainers")]
    empty = [t["key"] for t in teams if not any(x["team"] for x in t["teams"]) and not t.get("planned")]
    planned = [t["key"] for t in teams if t.get("planned")]
    results.append(("every trainer row carries its team from res/trainers/data, but a planned one",
                    not empty, f"{len(teams)} rows, empty {empty[:4]}, planned {planned}"))
    gauntlet = sum(1 for r in roles if r.get("role") == "gauntlet")
    shown = sum(len(g["trainers"]) for s in data["splits"] for z in s["zones"] for g in z["gauntlets"])
    sections = {(r["split"], r["section"]) for r in roles if r.get("role") == "gauntlet"}
    shown_sections = {(s["split"], g["section"]) for s in data["splits"] for z in s["zones"]
                      for g in z["gauntlets"]}
    results.append(("every gauntlet trainer sits in its section",
                    shown == gauntlet and sections == shown_sections,
                    f"{gauntlet} trainers, {len(sections)} sections"))
    required = sum(1 for r in roles if r["required"] == "yes" and r.get("role") != "gauntlet"
                   and r["trainer_id"] not in bosses)
    counted = sum(z["counts"]["mandatory"] for s in data["splits"] for z in s["zones"])
    results.append(("the mandatory counts add up to the census's required trainers and the fights",
                    counted == required + len(want_bosses), f"{counted} = {required} + {len(want_bosses)}"))


def check_items(results, data, root):
    pickups = bsplits.pickups()
    got = _all(data, "pickups")
    tree = [r for _s, _z, r in got if r["item"]]
    results.append(("every ball and hidden item shows once, with a flag for the save",
                    len(tree) == len(pickups) and all(r["flag"] is not None for r in tree),
                    f"{len(tree)} of {len(pickups)}"))
    by_kind = collections.Counter(row[3] for row, _maps in pickups.values())
    counted = collections.Counter()
    for s in data["splits"]:
        for z in s["zones"]:
            counted["ball"] += z["counts"]["balls"]
            counted["hidden"] += z["counts"]["hidden"]
    results.append(("the ball and hidden counts add up to the census's",
                    counted["ball"] >= by_kind["ball"] and counted["hidden"] == by_kind["hidden"],
                    f"{dict(counted)} against {dict(by_kind)}"))
    gifts = [r for _s, _z, r in _all(data, "gifts") if r["item"]]
    results.append(("every item an NPC script gives shows once",
                    len(gifts) == len(bsplits.gifts()), f"{len(gifts)} of {len(bsplits.gifts())}"))


def check_rewards(results, data, root):
    rewards, where = alpha.tables(root)["rewards"]
    kinds = collections.Counter(r["kind"] for r in rewards)
    trainer = sum(len(t["rewards"]) for _s, _z, t in _all(data, "trainers"))
    placed = [r for k in ("pickups", "gifts") for _s, _z, r in _all(data, k) if r["placed"]]
    unmatched = [r for r in placed if not r["item"]]
    shop = _all(data, "shop")
    dropped = sum(1 for r in rewards if r["kind"] in ("mart", "prize") and r["reward"] == "ITEM_NONE")
    results.append(("every reward-table row shows once: trainers, balls and gifts, shops "
                    "(a dropped shop slot sells nothing and is left out)",
                    trainer == kinds["trainer"]
                    and len(placed) == kinds["ball"] + kinds["gift"]
                    and len(shop) == kinds["mart"] + kinds["prize"] - dropped and len(rewards) > 0,
                    f"from {where}: {dict(kinds)}, {dropped} shop slots dropped"))
    results.append(("every ball or gift reward found the place it replaces",
                    not unmatched, f"{len(unmatched)} unmatched"))
    badges = [r for _s, _z, r in shop if r["badges"] is None]
    results.append(("every shop and Game Corner TM carries its badge count",
                    not badges and len(shop) > 0, f"{len(shop)} rows"))


def check_wild(results, data, root):
    sc = (model.load_sidecar() or {}).get("areas") or {}
    used = locations.header_uses(root)
    want = []
    for a in model.load_all():
        e = sc.get(a.name) or {}
        split = e.get("split") if a.land_active else (e.get("water_split") or e.get("split"))
        if a.name in used and split in alpha.SPLITS:
            want.append(a.name)
    got = collections.Counter(r["area"] for _s, _z, r in _all(data, "wild"))
    results.append(("every encounter table a map uses shows once, under its split",
                    sorted(got) == sorted(want) and all(v == 1 for v in got.values()),
                    f"{len(got)} of {len(want)}"))
    srcs = scripted.load(root)
    got = _all(data, "scripted")
    results.append(("every scripted capture shows once",
                    len(got) == len(srcs), f"{len(got)} of {len(srcs)}"))


def check_zones(results, data, root):
    results.append(("nothing is left unplaced", not data["unplaced"],
                    f"{[(u['kind'], u['split'], u['zone']) for u in data['unplaced'][:4]]}"))
    missing = [z["zone"] for s in data["splits"] for z in s["zones"] if z["order"] is None]
    results.append(("every zone has a walking position", not missing, f"{missing[:5]}"))
    roark = [z["zone"] for z in data["splits"][0]["zones"]]
    barry = [z["zone"] for s in data["splits"] if s["split"] == "Barry" for z in s["zones"]]
    results.append(("walking order: Roark's split opens in Twinleaf Town and reaches Oreburgh "
                    "City after Jubilife; the Barry split ends at the League",
                    roark[:2] == ["Twinleaf Town", "Route 201"]
                    and roark.index("Jubilife City") < roark.index("Oreburgh City")
                    and barry[-1] == "Pokémon League", f"{roark[:3]}, {barry[-1:]}"))
    jub = next(z for z in data["splits"][0]["zones"] if z["zone"] == "Jubilife City")
    potion = [p for p in jub["pickups"] if p["placed"] and p["item"] == "ITEM_POTION"]
    rewards, _w = alpha.tables(root)["rewards"]
    row = next((r for r in rewards if r["map"] == "MAP_HEADER_JUBILIFE_CITY" and r["kind"] == "ball"), None)
    results.append(("Jubilife's Potion ball shows the reward that replaces it",
                    row is None or (potion and potion[0]["placed"]["item"] == row["reward"]),
                    f"{row['reward'] if row else 'no row'}"))


def check_checklist(results, data, root):
    items = alpha.checklist_items(root)
    keys = [i["key"] for i in items]
    placed = [c["key"] for s in data["splits"] for z in s["zones"] for c in z["checks"]]
    placed += [c["key"] for c in data["anywhere"]]
    results.append(("every in-game checklist item maps to a zone or to anywhere, once",
                    sorted(placed) == sorted(keys) and len(set(keys)) == len(keys),
                    f"{len(keys)} items, {len(data['anywhere'])} anywhere"))
    over = alpha._check_overrides(root)
    zones = {z["zone"] for s in data["splits"] for z in s["zones"]}
    stale = [k for k in over if k not in keys]
    bad = [v for v in over.values() if v.partition("|")[0] not in zones | {"anywhere"}]
    results.append(("every override names a live item and a real zone",
                    not stale and not bad, f"stale {stale[:2]}, bad {bad[:2]}"))
    lost = [c["key"] for c in data["anywhere"] if c.get("zone") not in ("anywhere", None)]
    results.append(("no item falls to anywhere because its zone is missing", not lost, f"{lost[:3]}"))


def check_ticks(results, data, root):
    """Check 4: a save with two trainers beaten (a rival fight's variant and
    an ordinary trainer) and two items taken (a ball and a hidden item) ticks
    those four rows and no other."""
    from . import savefile
    from . import test_savefile as T
    targets = alpha.tick_targets(root)
    start = savefile._vars_layout()["values"]["TRAINER_DEFEATED_FLAGS_START"]
    ids = alpha._trainer_ids(root)
    flags = bsplits.flag_values()
    ball = flags["FLAG_OBTAINED_ROUTE_202_POTION"]
    hidden = next(p["flag"] for _s, _z, p in _all(data, "pickups") if p["how"] == "hidden")
    set_ = [start + ids["TRAINER_RIVAL_ROUTE_201_TURTWIG"], start + ids["TRAINER_YOUNGSTER_TRISTAN"],
            ball, hidden]
    save = T.make_save([], {}, box_size=T.BOX_SIZE_30, flags=set_)
    got = alpha.ticks(root, save)
    beaten = sorted(k for k, v in got["trainers"].items() if v)
    taken = sorted(int(k) for k, v in got["pickups"].items() if v)
    results.append(("a test save ticks the rows its flags name and no other",
                    beaten == sorted(["barry_1", "TRAINER_YOUNGSTER_TRISTAN"])
                    and taken == sorted([ball, hidden])
                    and len(got["trainers"]) == len(targets["trainers"]),
                    f"beaten {beaten}, taken {taken}"))
    empty = alpha.ticks(root, T.make_save([], {}, box_size=T.BOX_SIZE_30))
    # A planned trainer (the Game Corner challenger before step 10) has no id
    # yet, so nothing in the save can tick it.
    page_keys = {t["key"] for _s, _z, t in _all(data, "trainers") if not t.get("planned")}
    results.append(("an unplayed save ticks nothing, and every trainer row but a planned one has a tick",
                    not any(empty["trainers"].values()) and not any(empty["pickups"].values())
                    and page_keys == set(empty["trainers"]),
                    f"{len(empty['trainers'])} trainer rows, {len(empty['pickups'])} pickups"))
    old = T.make_save([], {}, box_size=T.BOX_SIZE_30, normal_size=T.NORMAL_SIZE - 4)
    try:
        alpha.ticks(root, old)
        refused = False
    except savefile.SaveError:
        refused = True
    results.append(("a save on an older layout is refused rather than ticked at the wrong place",
                    refused, ""))


def check_versions(results, data, root):
    """Ian's layout note 2: a fight kept once per starter knows whom each
    version is for, every player meets exactly one, and the save says which
    player it is (a girl who chose Scorbunny meets Lucas and his Turtwig)."""
    from . import savefile
    from . import test_savefile as T
    starters = {"SPECIES_TURTWIG", "SPECIES_SCORBUNNY", "SPECIES_PIPLUP"}
    bad = []
    for _s, _z, t in _all(data, "trainers"):
        if len(t["teams"]) < 2 or t.get("tag"):
            continue
        fors = [(x["for"] or {}).get("starter") for x in t["teams"]]
        pairs = [((x["for"] or {}).get("starter"), (x["for"] or {}).get("gender")) for x in t["teams"]]
        if set(fors) != starters or len(set(pairs)) != len(pairs):
            bad.append(t["key"])
    save = T.make_save([], {}, box_size=T.BOX_SIZE_30, gender=1,
                       variables={"VAR_PLAYER_STARTER": T.species_id("SPECIES_SCORBUNNY")})
    who = savefile.player(save)
    lucas = next(t for _s, _z, t in _all(data, "trainers") if t["key"] == "lucas_dawn_1")
    mine = [x for x in lucas["teams"] if x["for"]["starter"] == who["starter"] and x["for"]["gender"] == who["gender"]]
    turtwig = mine and any(m["species"] == "SPECIES_TURTWIG" for m in mine[0]["team"])
    results.append(("every version of a fight is for one player, and the save says which",
                    not bad and who == {"gender": "female", "starter": "SPECIES_SCORBUNNY"}
                    and len(mine) == 1 and turtwig and mine[0]["label"].startswith("Lucas"),
                    f"bad {bad}, save {who}, {mine[0]['label'] if mine else 'none'}"))
    items = alpha.checklist_items(root)
    seeker = next((i for i in items if "Vs. Seeker never reached" in i["text"]), None)
    results.append(("each check shows its whole first sentence; an abbreviation does not end one",
                    all(i["first"] for i in items) and seeker is not None
                    and "Vs. Seeker" in seeker["first"] and alpha.first_sentence("Lv. 16 holds. Next")[0]
                    == "Lv. 16 holds.", f"{len(items)} items"))


def check_notes(results, data, root):
    """Checks 3 and 6: a note is stamped from the save, a bad rating is
    refused, the export writes JSON and Markdown in the repo's folder, and
    with the local file gone the export is read back; a new run sets the
    run aside. All under OXIDE_ALPHA_DIR, so Ian's notes are never touched."""
    import tempfile
    from . import alphanotes
    from . import savefile
    from . import test_savefile as T
    old_env = os.environ.get("OXIDE_ALPHA_DIR")
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["OXIDE_ALPHA_DIR"] = tmp
        try:
            monferno = T.species_id("SPECIES_MONFERNO")
            party = [T.record(0x12345678, monferno, [T.move_id("MOVE_SCRATCH")],
                              T.ability_id("ABILITY_BLAZE"), party_level=16)]
            raw_bytes = T.make_save(party, {}, box_size=T.BOX_SIZE_30, badges=0x03)
            raw = (raw_bytes, savefile.parse(raw_bytes), 7,
                   "/mnt/c/Users/Ian/oxide-playtest/pokeplatinum-oxide-085f72211.sav")
            e = alphanotes.record(root, "roark", {"fought": True, "rating": 7, "note": "Onix hit hard",
                                                  "death": {"mon": "Starly", "killer": "Rock Tomb", "saw": "no"}},
                                  label="Roark", zone="Oreburgh City", split="Roark", raw=raw, bridge=False)
            s = e["stamp"]
            stamped = (s["rom"] == "085f72211" and s["badges"] == 2 and s["zone"] == "Oreburgh City"
                       and s["save_split"] and len(s["party"]) == 1 and "Monferno" in s["party"][0])
            try:
                alphanotes.record(root, "roark", {"rating": 11}, raw=raw, bridge=False)
                bad = False
            except ValueError:
                bad = True
            alphanotes.record(root, "zone:Roark:Route 202", {"note": "the Potion ball moved"},
                              label="Route 202", zone="Route 202", split="Roark", raw=None, bridge=False)
            results.append(("a note is stamped with the ROM, badges, split, party and zone; a rating "
                            "of 11 is refused", stamped and bad, f"{s['rom']}, {s['badges']} badges, {s['party']}"))
            before = alphanotes.load(root)["notes"]
            paths = alphanotes.export(root, [("Roark", "Route 202"), ("Roark", "Oreburgh City")])
            md = open(paths[1], encoding="utf-8").read()
            os.remove(os.path.join(tmp, alphanotes.LOCAL))
            back = alphanotes.load(root)
            results.append(("the export writes JSON and Markdown, and is read back in the local "
                            "file's place",
                            back["notes"] == before and back["from"] == "export"
                            and md.index("Route 202") < md.index("Oreburgh City")
                            and "rated 7 of 10" in md and "killed by Rock Tomb" in md
                            and all(os.path.dirname(p) == tmp for p in paths),
                            f"{len(back['notes'])} notes back"))
            alphanotes.record(root, "barry_1", {"fought": True}, raw=None, bridge=False)
            fresh = alphanotes.new_run(root, "run two")
            aside = [f for f in os.listdir(tmp) if f.startswith("alpha-feedback-")]
            results.append(("a new run starts empty and keeps the old one aside",
                            fresh["notes"] == {} and fresh["run"] == "run two" and len(aside) == 1,
                            f"{aside}"))
        finally:
            if old_env is None:
                os.environ.pop("OXIDE_ALPHA_DIR", None)
            else:
                os.environ["OXIDE_ALPHA_DIR"] = old_env


def main():
    root = model.repo_root()
    data = alpha.build(root)
    results = []
    for check in (check_trainers, check_items, check_rewards, check_wild, check_zones,
                  check_checklist, check_ticks, check_versions, check_notes):
        check(results, data, root)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
