"""Check the script index against facts known from the scripts.

tools/oxide/scriptindex.py reads every field script and event file and says,
per map, what the map does. These are things the project already knows from
reading the scripts by hand (docs/oxide/trainer-survey.md, the fossil ruling
of 2026-09-26), so if the tool stops seeing one of them, its reading has
broken somewhere:

- the five level 100 superbosses, which the machine-generated scripts start
  by trainer number: May at the Resort Area, Steven at Stark Mountain, Cyrus
  at Turnback Cave, and Red and Gold outside Mt. Coronet;
- Barry's partner team at Spear Pillar, which the script picks through a
  variable by the player's starter;
- the Maids' training battles (the base ROM's "Experiencia" teams), started by
  number in eight towns, the League and the Day Care;
- the Root, Armor and Skull Fossil balls in Oreburgh Mine B2F, one-time finds
  that Oxide added;
- the base ROM's Black Belt on Route 210 South, whose event runs script 13 of
  a script file that has 8 (checked by hand, 2026-09-27);

and a few checks of the reading itself: the constant lists, the macro
expansion that makes a hand-written and a generated script look alike, a
variable traced through a Call, and the rendered Markdown passing Ian's
writing rules. It needs `main` and the branch's history, as the tool does.

    python3 tools/oxide/test_scriptindex.py
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools", "oxide"))
sys.path.insert(0, os.path.join(ROOT, ".claude", "hooks"))

import scriptindex as si  # noqa: E402

SUPERBOSSES = {
    "TRAINER_DUMMY_060": ("MAP_HEADER_RESORT_AREA", "May"),
    "TRAINER_DUMMY_061": ("MAP_HEADER_STARK_MOUNTAIN_ROOM_1", "Steven"),
    "TRAINER_DUMMY_005": ("MAP_HEADER_TURNBACK_CAVE_GIRATINA_ROOM", "Cyrus"),
    "TRAINER_DUMMY_058": ("MAP_HEADER_MT_CORONET_OUTSIDE_SOUTH", "Red"),
    "TRAINER_DUMMY_059": ("MAP_HEADER_MT_CORONET_OUTSIDE_NORTH", "Gold"),
}

MAIDS = {
    "TRAINER_DUMMY_208": "MAP_HEADER_OREBURGH_CITY",
    "TRAINER_DUMMY_209": "MAP_HEADER_ETERNA_CITY",
    "TRAINER_DUMMY_210": "MAP_HEADER_HEARTHOME_CITY",
    "TRAINER_DUMMY_211": "MAP_HEADER_VEILSTONE_CITY",
    "TRAINER_DUMMY_212": "MAP_HEADER_PASTORIA_CITY",
    "TRAINER_DUMMY_213": "MAP_HEADER_CANALAVE_CITY",
    "TRAINER_DUMMY_214": "MAP_HEADER_SNOWPOINT_CITY",
    "TRAINER_DUMMY_215": "MAP_HEADER_SUNYSHORE_CITY",
    "TRAINER_DUMMY_216": "MAP_HEADER_POKEMON_LEAGUE",
}
MAIDS.update({f"TRAINER_DUMMY_{n}": "MAP_HEADER_POKEMON_DAY_CARE" for n in range(217, 223)})

FOSSILS = ["ITEM_ARMOR_FOSSIL", "ITEM_SKULL_FOSSIL", "ITEM_ROOT_FOSSIL"]


def trainer_battles(m):
    """[(trainer name, mode, entry)] for every trainer slot a map fights."""
    out = []
    for e in m["entries"].get("trainers", []):
        for slot in e["slots"]:
            for v in slot["values"]:
                out.append((v["name"], slot["mode"], e))
    return out


def main():
    results = []

    def check(name, ok, detail=""):
        results.append(bool(ok))
        print(("PASS " if ok else "FAIL ") + name + (": " + str(detail) if detail and not ok else ""))

    # ---- the reading itself
    vf = si.metang(open("generated/vars_flags.txt").read())
    check("the constant lists count as metang does",
          vf["FLAG_UNK_0x0FFF"] == 0xFFF and vf["FLAG_DAILY_0x0B5F"] == 0xB5F
          and vf["VAR_0x800C"] == 0x800C and vf["VAR_RESULT"] == 0x800C)

    tree = si.Tree(None)
    consts = si.Consts(tree)
    macros = si.load_macros(tree)
    resolve = si.Resolver(consts)
    hand = si.expand(macros, "GoToIfEq", ["VAR_RESULT", "TRUE", "Label"], resolve)
    made = si.expand(macros, "CompareVarToValue", ["VAR_0x800C", "1"], resolve) + \
        si.expand(macros, "GoToIf", ["1", "Label"], resolve)
    check("a hand-written GoToIfEq expands to what a generated script writes",
          [c for c, _ in hand] == [c for c, _ in made] == ["CompareVarToValue", "GoToIf"]
          and [resolve(a["varID"]) for c, a in hand if c == "CompareVarToValue"] == [0x800C], hand)
    check("SetVar with a variable becomes SetVarFromVar, with a value SetVarFromValue",
          si.expand(macros, "SetVar", ["VAR_0x8004", "VAR_0x8005"], resolve)[0][0] == "SetVarFromVar"
          and si.expand(macros, "SetVar", ["VAR_0x8004", "ITEM_POTION"], resolve)[0][0] == "SetVarFromValue")

    text = """#include "macros/scrcmd.inc"

    ScriptEntry Test_Start
    ScriptEntryEnd

Test_Start:
    Call Test_Pick
    AddItem VAR_0x8004, 1, VAR_RESULT
    End

Test_Pick:
    SetVar VAR_0x8004, ITEM_POTION
    GoToIfSet FLAG_UNK_0x0FFF, Test_Done
    SetVar VAR_0x8004, ITEM_ELIXIR
Test_Done:
    Return
"""
    script = si.Script("scripts_test", text, macros, consts)
    add = [n for n in script.nodes if n.cmd == "AddItem"][0]
    found = si.trace(script, add.idx, 0x8004, si.Resolver(consts))
    values = {w[1] for w, _, _ in found if w[0] == "value"}
    check("a variable is traced into the Call that sets it, both branches",
          values == {consts.values["ITEM_POTION"], consts.values["ITEM_ELIXIR"]}, found)

    # ---- the index, as the tool renders it now
    md, _, result = si.render()
    maps = {m["header"]: m for m in result["maps"]}
    # Where an added entry came from rests on the branch's history, which a
    # shallow clone does not have; those checks say so there instead.
    history = not result["shallow"]
    if not history:
        print("NOTE shallow clone: the base ROM and Oxide attributions are not checked")

    for trainer, (header, name) in SUPERBOSSES.items():
        hits = [(mode, e) for n, mode, e in trainer_battles(maps.get(header, {"entries": {}})) if n == trainer]
        check(f"{name}, the level 100 superboss {trainer}, is fought at {header} by number",
              hits and all(mode == "number" for mode, _ in hits) and result["trainers"].get(trainer, "").startswith(f"{name}, level 100"),
              hits or result["trainers"].get(trainer))
        check(f"{trainer} is added, from the base ROM",
              hits and all(e.get("origin") == "added" and (e.get("source") == "base ROM" or not history)
                           for _, e in hits),
              [(e.get("origin"), e.get("source")) for _, e in hits])

    pillar = [e for e in maps["MAP_HEADER_SPEAR_PILLAR"]["entries"].get("trainers", []) if e["how"] == "StartTagBattle"]
    partner = pillar[0]["slots"][0] if pillar else {}
    picks = {v["name"]: v["when"] for v in partner.get("values", [])}
    check("Spear Pillar's tag battle picks Barry's team through a variable",
          partner.get("role") == "partnerTrainer" and partner.get("mode") == "variable", partner)
    # The fire slot's team files keep Chimchar's name, but Scorbunny is the
    # starter that picks them since 2026-09-21 (Ian).
    check("Barry's fire-slot team when the starter is Scorbunny, Turtwig's for Turtwig, Piplup's otherwise",
          "SPECIES_SCORBUNNY" in picks.get("TRAINER_RIVAL_SPEAR_PILLAR_CHIMCHAR", "")
          and "SPECIES_TURTWIG" in picks.get("TRAINER_RIVAL_SPEAR_PILLAR_TURTWIG", "")
          and picks.get("TRAINER_RIVAL_SPEAR_PILLAR_PIPLUP") == ""
          and "GetPlayerStarterSpecies" in picks.get("TRAINER_RIVAL_SPEAR_PILLAR_CHIMCHAR", ""), picks)
    check("the Spear Pillar tag battle is vanilla (main picks the same three teams)",
          pillar and pillar[0].get("origin") == "vanilla", pillar and pillar[0].get("origin"))

    for trainer, header in MAIDS.items():
        hits = [(mode, e) for n, mode, e in trainer_battles(maps[header]) if n == trainer]
        check(f"the Maid's training battle {trainer} is at {header}, by number",
              hits and all(mode == "number" for mode, _ in hits)
              and result["trainers"].get(trainer, "").startswith("Experiencia"), hits)

    mine = maps["MAP_HEADER_OREBURGH_MINE_B2F"]["entries"].get("item_balls", [])
    for item in FOSSILS:
        balls = [e for e in mine if e["item"] == item]
        check(f"Oreburgh Mine B2F has one {item} ball, a one-time find Oxide added",
              len(balls) == 1 and not balls[0]["daily"] and balls[0]["origin"] == "added"
              and (balls[0].get("source") == "Oxide" or not history)
              and balls[0]["flag_name"] == "FLAG_OBTAINED_OREBURGH_MINE_B2F_" + item[len("ITEM_"):],
              balls)
    check("no Helix, Dome or Claw Fossil ball is left anywhere",
          not any(e["item"] in ("ITEM_HELIX_FOSSIL", "ITEM_DOME_FOSSIL", "ITEM_CLAW_FOSSIL")
                  for m in result["maps"] for e in m["entries"].get("item_balls", [])))

    acuity = maps["MAP_HEADER_ACUITY_CAVERN"]["entries"].get("statics", [])
    check("Acuity Cavern's drawn legendary is set elsewhere, and the index names who stores it",
          acuity and "set elsewhere" in acuity[0]["species"][0]["name"]
          and "scripts_init_new_game" in acuity[0]["species"][0]["name"], acuity)

    black_belt = [x for x in maps["MAP_HEADER_ROUTE_210_SOUTH"].get("missing", []) if x.get("id") == "LOCALID_BLACK_BELT"]
    check("Route 210 South's Black Belt, from the base ROM, runs script 13 of a file with 8, and is flagged",
          black_belt and black_belt[0]["script"] == 13 and black_belt[0]["has"] == 8
          and black_belt[0]["origin"] == "added", black_belt)

    import style_check
    check("the rendered Markdown passes Ian's writing rules", not style_check.findings(md),
          style_check.findings(md))

    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
