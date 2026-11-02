"""The Trainers tab's coverage tables (coverage.py, Ian, 2026-11-02).

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_coverage

Each expected number below is worked out by hand from Oxide's type chart
and the abilities' rules in src/battle/battle_lib.c, so a change to either
that moves one fails here. Nothing is written.
"""
import copy
import http.client
import json
import sys
import threading

from . import coverage
from . import model
from . import pokedex
from . import server
from . import trainers


def member(species, ability, moves, types=None, item=None, iv=31):
    """A team member as trainers.detail hands it to coverage.team."""
    root = model.repo_root()
    return {"species": species, "types": types or pokedex.load(root, species)["types"],
            "ability": ability, "moves": moves, "item": item, "iv": iv}


def counts(row):
    return {b: len(v) for b, v in row["cells"].items() if v}


def check_rules(results):
    """The engine's rules, one hit at a time."""
    root = model.repo_root()
    chart, fs = pokedex.type_chart(root), pokedex.foresight_entries(root)
    m = lambda *a, **k: coverage.multiplier(chart, fs, *a, **k)[0]
    cases = [
        ("Levitate takes nothing from Ground", m("GROUND", ["GHOST", "POISON"], dfn="LEVITATE"), 0),
        ("but Thousand Arrows hits it", m("GROUND", ["GHOST", "POISON"], move="MOVE_THOUSAND_ARROWS",
                                          dfn="LEVITATE"), 2),
        ("and Mold Breaker ignores it", m("GROUND", ["GHOST", "POISON"], atk="MOLD_BREAKER",
                                          dfn="LEVITATE"), 2),
        ("Thick Fat halves Fire on Grass", m("FIRE", ["GRASS"], dfn="THICK_FAT"), 1),
        ("Dry Skin takes Water and a quarter more Fire", (m("WATER", ["GRASS"], dfn="DRY_SKIN"),
                                                         m("FIRE", ["GRASS"], dfn="DRY_SKIN")), (0, 2.5)),
        ("Scrappy hits Ghost with Normal and Fighting", (m("NORMAL", ["GHOST"], atk="SCRAPPY"),
                                                        m("FIGHTING", ["GHOST", "DARK"], atk="SCRAPPY")), (1, 2)),
        ("Tinted Lens doubles a resisted hit", m("BUG", ["FIRE", "STEEL"], atk="TINTED_LENS"), 0.5),
        ("Wonder Guard stops all but super effective", (m("FIGHTING", ["BUG", "STEEL"], dfn="WONDER_GUARD"),
                                                        m("FIRE", ["BUG", "STEEL"], dfn="WONDER_GUARD")), (0, 4)),
        ("Filter keeps x2 a super effective column", coverage.bucket(m("FIRE", ["GRASS"], dfn="FILTER")), 2),
        ("Freeze-Dry and Flying Press read the chart their own way",
         (m("ICE", ["WATER"], move="MOVE_FREEZE_DRY"), m("FIGHTING", ["GRASS"], move="MOVE_FLYING_PRESS")), (2, 2)),
        ("a fixed-damage move is x1 or x0", (m("FIGHTING", ["ROCK", "STEEL"], fixed=True),
                                             m("FIGHTING", ["GHOST"], fixed=True)), (1, 0)),
        ("Steel still resists Ghost in Oxide's chart", m("GHOST", ["STEEL"]), 0.5),
        ("Hidden Power is Dark at odd IVs, Fighting at even",
         (coverage.hidden_power_type([31] * 6), coverage.hidden_power_type([30] * 6)), ("DARK", "FIGHTING")),
    ]
    for label, got, want in cases:
        results.append((label, got == want, str(got)))


def check_defence(results):
    """A built team (trainers.detail on an edit of Roark's file): Gengar has
    only Levitate and Meganium only Thick Fat, Kangaskhan its slot-2 Scrappy."""
    root = model.repo_root()
    data = copy.deepcopy(trainers.load(root, "leader_roark"))
    # Roark's lead asks to be male, which Kangaskhan cannot be, and the
    # personality then keeps the gender over the ability slot.
    template = {k: v for k, v in data["party"][0].items() if k != "gender"}

    def mon(species, moves, slot=1):
        return dict(template, species=species, form=0, level=15, item="ITEM_NONE", moves=moves,
                    ability=slot, nature="NATURE_HARDY")
    data["party"] = [mon("SPECIES_GENGAR", ["MOVE_SHADOW_BALL", "MOVE_SLUDGE_BOMB"]),
                     mon("SPECIES_MEGANIUM", ["MOVE_GIGA_DRAIN"]),
                     mon("SPECIES_KANGASKHAN", ["MOVE_BODY_SLAM", "MOVE_CLOSE_COMBAT"], slot=2)]
    d = trainers.detail(root, "leader_roark", data)
    cov = d["coverage"]
    rows = {r["type"]: r for r in cov["defence"]}
    ground, fire = rows["GROUND"], rows["FIRE"]
    gengar_zero = ground["cells"]["0"]
    results.append(("Ground: Gengar x0 by Levitate (x2 without), Meganium x1/2, Kangaskhan x1",
                    counts(ground) == {"0": 1, "0.5": 1, "1": 1}
                    and gengar_zero[0]["i"] == 0 and gengar_zero[0].get("ability") == "LEVITATE"
                    and gengar_zero[0].get("plain") == 2, str(counts(ground))))
    meganium = [e for e in fire["cells"]["1"] if e["i"] == 1]
    results.append(("Fire: all three x1, Meganium there by Thick Fat (x2 without)",
                    counts(fire) == {"1": 3} and meganium and meganium[0].get("ability") == "THICK_FAT"
                    and meganium[0].get("plain") == 2, str(counts(fire))))
    results.append(("the table has the eighteen types in the games' order",
                    [r["type"] for r in cov["defence"]] == coverage.TYPES, ""))
    kang = d["coverage"]["scopes"]["dex"]["members"][2]
    results.append(("the built Kangaskhan has Scrappy and both its moves count",
                    [a["move"] for a in kang["attacks"]] == ["MOVE_BODY_SLAM", "MOVE_CLOSE_COMBAT"]
                    and data["party"][2]["ability"] == 2
                    and any(e.get("ability") == ["SCRAPPY"] for e in kang["moved"]["neutral"]),
                    str(kang["counts"])))


SCOPE = ("SPECIES_GASTLY", "SPECIES_GEODUDE", "SPECIES_SNORLAX", "SPECIES_BRONZOR",
         "SPECIES_SHEDINJA", "SPECIES_SABLEYE", "SPECIES_STEELIX")


def check_offence(results):
    """Kangaskhan with Scrappy, Body Slam and Close Combat against a fixed
    scope of seven:
      Gastly x1 (Normal, by Scrappy; x0 without), Geodude x2 (Fighting),
      Snorlax x2, Bronzor x1 (its two abilities, so neither counts),
      Shedinja x0 (Wonder Guard), Sableye x2 (Fighting, by Scrappy),
      Steelix x2 (Fighting; Solid Rock is one of two slots)."""
    root = model.repo_root()
    kang = member("SPECIES_KANGASKHAN", "SCRAPPY", ["MOVE_BODY_SLAM", "MOVE_CLOSE_COMBAT", "MOVE_PROTECT"])
    out = coverage.offence(root, [kang], SCOPE)
    row = out["members"][0]
    results.append(("one member's counts: 4 super, 2 neutral, 0 resisted, 1 immune",
                    row["counts"] == {"super": 4, "neutral": 2, "resisted": 0, "immune": 1},
                    str(row["counts"])))
    results.append(("status moves do not count", [a["move"] for a in row["attacks"]]
                    == ["MOVE_BODY_SLAM", "MOVE_CLOSE_COMBAT"], ""))
    moved = {e["sp"]: e.get("ability") for g in row["moved"].values() for e in g}
    results.append(("Scrappy is named where it moved a count (Gastly, Sableye)",
                    moved == {"SPECIES_GASTLY": ["SCRAPPY"], "SPECIES_SABLEYE": ["SCRAPPY"]}, str(moved)))
    results.append(("the x0 list is Shedinja", [e["sp"] for e in row["immune"]] == ["SPECIES_SHEDINJA"], ""))


def check_walls(results):
    """Three members against the same scope. Shedinja walls Kangaskhan
    (Wonder Guard) and Snorlax (Body Slam x0), and Steelix walls Gengar
    (Shadow Ball x1/2 on Steel, Sludge Bomb x0) and Snorlax (Body Slam
    x1/2): the two rows of two, in dex order. Geodude walls Snorlax alone."""
    root = model.repo_root()
    team = [member("SPECIES_KANGASKHAN", "SCRAPPY", ["MOVE_BODY_SLAM", "MOVE_CLOSE_COMBAT"]),
            member("SPECIES_GENGAR", "LEVITATE", ["MOVE_SHADOW_BALL", "MOVE_SLUDGE_BOMB"]),
            member("SPECIES_SNORLAX", "THICK_FAT", ["MOVE_BODY_SLAM", "MOVE_REST"])]
    out = coverage.offence(root, team, SCOPE)
    walls = {w["sp"]: [m["i"] for m in w["members"]] for w in out["walls"]}
    top = [w["sp"] for w in out["walls"][:2]]
    results.append(("the walls row for Steelix: Gengar and Snorlax, among the worst two",
                    top == ["SPECIES_SHEDINJA", "SPECIES_STEELIX"] and walls["SPECIES_STEELIX"] == [1, 2]
                    and walls["SPECIES_SHEDINJA"] == [0, 2], str(walls)))
    results.append(("Geodude walls Snorlax alone; Gastly walls Snorlax but not Scrappy's Kangaskhan",
                    walls.get("SPECIES_GEODUDE") == [2] and "SPECIES_GASTLY" in walls
                    and 0 not in walls["SPECIES_GASTLY"], str(walls.get("SPECIES_GASTLY"))))
    results.append(("sorted by how many it walls", [len(w["members"]) for w in out["walls"]]
                    == sorted((len(w["members"]) for w in out["walls"]), reverse=True), ""))


def check_scope(results):
    """The split's scope comes from the Box sim's availability; the switch
    shows the whole dex."""
    root = model.repo_root()
    roark = coverage.split_scope(root, "Roark")
    gardenia = coverage.split_scope(root, "Gardenia")
    dex_all = coverage.dex_scope(root)
    results.append(("Roark's scope holds the starters and Geodude but not Graveler (25, over the cap 16)",
                    {"SPECIES_TURTWIG", "SPECIES_PIPLUP", "SPECIES_GEODUDE"} <= set(roark)
                    and "SPECIES_GRAVELER" not in roark, f"{len(roark)} species"))
    results.append(("Gardenia's cap 26 lets Graveler in; each split's scope holds the one before",
                    "SPECIES_GRAVELER" in gardenia and set(roark) <= set(gardenia), f"{len(gardenia)} species"))
    results.append(("the whole dex is every species the Dex lists, Garchomp among them",
                    dex_all == tuple(pokedex.species_list(root)) and "SPECIES_GARCHOMP" in dex_all
                    and "SPECIES_GARCHOMP" not in roark, f"{len(dex_all)} species"))
    team = [member("SPECIES_GEODUDE", "STURDY", ["MOVE_ROCK_THROW"])]
    both = coverage.team(root, team, "Roark")
    none = coverage.team(root, team, None)
    results.append(("a team with a split gets both scopes, one without gets only the dex",
                    set(both["scopes"]) == {"split", "dex"} and set(none["scopes"]) == {"dex"}
                    and both["scopes"]["split"]["size"] == len(roark)
                    and both["scopes"]["dex"]["size"] == len(dex_all), ""))
    shown = {sp for r in both["scopes"]["split"]["walls"] for sp in [r["sp"]]}
    results.append(("every Pokemon a list can show has its name and types sent",
                    shown <= set(both["species"]) and all(both["species"][sp]["types"] for sp in shown), ""))


def check_route(results):
    httpd = server.Server(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=120)
        conn.request("GET", "/api/trainer/leader_roark")
        r = conn.getresponse()
        body = json.loads(r.read())
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    cov = body.get("coverage") or {}
    results.append(("/api/trainer sends the coverage with the team, Roark's split scope included",
                    r.status == 200 and len(cov.get("defence") or []) == 18
                    and set(cov.get("scopes") or {}) == {"split", "dex"},
                    f"{len(json.dumps(cov))} bytes"))


def main():
    results = []
    for check in (check_rules, check_defence, check_offence, check_walls, check_scope, check_route):
        check(results)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
