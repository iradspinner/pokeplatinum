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


def main():
    root = model.repo_root()
    data = alpha.build(root)
    results = []
    for check in (check_trainers, check_items, check_rewards, check_wild, check_zones,
                  check_checklist):
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
