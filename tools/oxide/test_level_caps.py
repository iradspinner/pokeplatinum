"""Check the engine's level caps against the balance track's.

Phase 4 element 8 keeps the cap of each split in one C table, sLevelCaps in
src/system_vars.c, indexed by the LEVEL_CAP_SPLIT_ constants in
include/constants/level_caps.h. The balance track keeps the same caps in
tools/oxide/balance/fights.json, which its tools score fights against. If
the level-cap design moves a cap in one place and not the other, the game
and the balance scores disagree without anyone noticing; this catches it.

It also checks that each split's closing fight raises the cap to the next
split, by finding RaiseLevelCap in the script that fights the last trainer
of every split fights.json lists.

    python3 tools/oxide/test_level_caps.py
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# The script that fights each split's closing trainer, and the split that
# script moves the player into. Gym leaders are fought by trainer number in
# the generated scripts, so the file is named here rather than searched for.
CLOSING_SCRIPTS = {
    "Roark": ("scripts_oreburgh_city_gym", "GARDENIA"),
    "Gardenia": ("scripts_eterna_city_gym", "FANTINA"),
    "Fantina": ("scripts_hearthome_city_gym_leader_room", "MAYLENE"),
    "Maylene": ("scripts_veilstone_city_gym", "WAKE"),
    "Wake": ("scripts_pastoria_city_gym", "BYRON"),
    "Byron": ("scripts_canalave_city_gym", "CANDICE"),
    "Candice": ("scripts_snowpoint_city_gym", "HQ"),
    "HQ": ("scripts_galactic_hq_control_room", "GALACTIC"),
    "Galactic": ("scripts_distortion_world_b7f", "VOLKNER"),
    "Volkner": ("scripts_sunyshore_city_gym_room_3", "BARRY"),
    # The Barry split has no closing fight: it ends when the player enters
    # the Elite Four, as Aaron's room shuts its door behind them (Ian,
    # 2026-09-27), so its raise lives in that room's entry scene.
    "Barry": ("scripts_pokemon_league_aaron_room", "LEAGUE"),
    "League": ("scripts_pokemon_league_champion_room", "NONE"),
}


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def split_constants():
    """LEVEL_CAP_SPLIT_ name to value, from the constants header."""
    text = read("include/constants/level_caps.h")
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"#define LEVEL_CAP_SPLIT_(\w+)\s+(\d+)", text)}


def engine_caps():
    """Split name to cap, from sLevelCaps in src/system_vars.c."""
    text = read("src/system_vars.c")
    table = re.search(r"sLevelCaps\[[^\]]*\] = \{(.*?)\};", text, re.S).group(1)
    return {m.group(1): m.group(2)
            for m in re.finditer(r"\[LEVEL_CAP_SPLIT_(\w+)\] = (\w+),", table)}


def main():
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail and not ok else ""))

    fights = json.loads(read("tools/oxide/balance/fights.json"))
    splits = fights["splits"]
    caps = {k: v for k, v in fights["caps"].items() if not k.startswith("_")}
    consts = split_constants()
    engine = engine_caps()

    names = [s.upper() for s in splits] + ["NONE"]
    check("the constants are the balance track's splits in play order, then NONE",
          [consts.get(n) for n in names] == list(range(len(names)))
          and consts.get("COUNT") == len(names),
          f"constants {consts}")
    for s in splits:
        check(f"{s}'s cap is {caps[s]} in the engine too",
              engine.get(s.upper()) == str(caps[s]),
              f"engine has {engine.get(s.upper())}")
    check("after the League there is no cap", engine.get("NONE") == "MAX_POKEMON_LEVEL",
          f"engine has {engine.get('NONE')}")

    # The closing fight of each split is the last fight fights.json lists in it.
    last = {}
    for f in fights["fights"]:
        last[f["split"]] = f
    for s in splits:
        stem, nxt = CLOSING_SCRIPTS[s]
        text = read(f"res/field/scripts/{stem}.s")
        check(f"{last[s]['label']} closes {s}'s split, and {stem} raises the cap to {nxt}",
              f"RaiseLevelCap LEVEL_CAP_SPLIT_{nxt}\n" in text)
    check("every split has a closing script", set(CLOSING_SCRIPTS) == set(splits))

    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
