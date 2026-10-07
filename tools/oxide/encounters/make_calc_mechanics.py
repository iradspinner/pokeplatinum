"""The data the calculator's Platinum Oxide profile needs, read from the engine.

    PYTHONPATH=. python3 -m tools.oxide.encounters.make_calc_mechanics

Writes `calc/calc/mechanics/romhacks/profiles/platinum-oxide-data.js`, which
the page loads before the profile (`platinum-oxide.js`) and which the balance
track's headless runner loads with every other calculator script. Element 5's
abilities (Ian, 2026-09-26) act on lists the engine keeps in
`src/battle/battle_lib.c`: the slicing moves for Sharpness, the sound moves
for Liquid Voice, the ball and bomb moves for Bulletproof, the powder moves
for Overcoat, the Normal moves Pixilate leaves alone, and the effects Sheer
Force strips; and, from the effect scripts, the moves Reckless raises. They are Oxide's lists, not Showdown's (Sharpness counts five
claw moves the later games do not), so the calculator reads these rather
than its own move flags. The same file carries the type chart's row order,
since the game applies a dual type's two factors in chart order (Ian,
2026-09-22), and the moves that always land a critical hit.

Every list holds the calculator's names for the moves (calc_export's), so
the profile compares them with `move.name`. test_m8 fails if the file is
stale, as it does for the skin.
"""
import json
import os
import re
import sys

from . import calc_export
from . import model
from . import pokedex

OUT = os.path.join("tools", "oxide", "encounters", "calc", "calc", "mechanics", "romhacks",
                   "profiles", "platinum-oxide-data.js")
BATTLE_LIB = os.path.join("src", "battle", "battle_lib.c")
ALWAYS_CRIT = ("ALWAYS_CRITICAL", "HIT_THREE_TIMES_ALWAYS_CRITICAL")


def _array(src, name):
    """The constants of one static array in battle_lib.c, in order."""
    start = src.index(f"{name}[] = {{")
    body = src[start:src.index("};", start)]
    body = re.sub(r"//[^\n]*", "", body)
    return re.findall(r"\b((?:MOVE|BATTLE_EFFECT)_[A-Z0-9_]+)\b", body)


EFFECT_SCRIPTS = os.path.join("res", "battle", "scripts", "effects")
_RECKLESS = re.compile(r"CheckAbility\s+CHECK_NOT_HAVE,\s*BTLSCR_ATTACKER,\s*ABILITY_RECKLESS,\s*\w+\s*\n"
                       r"\s*UpdateVar\s+OPCODE_SET,\s*BTLVAR_POWER_MULTI,\s*12\b")


def reckless_effects(root):
    """The effect ids whose scripts give Reckless its 1.2: the script checks
    the attacker for Reckless and, if it has it, sets the power multiplier
    to 12 (tenths). Recoil moves, crash moves and Oxide's reworks alike."""
    out = set()
    base = os.path.join(root, EFFECT_SCRIPTS)
    for f in os.listdir(base):
        m = re.fullmatch(r"effect_script_(\d+)\.s", f)
        if m:
            with open(os.path.join(base, f), encoding="utf-8") as fh:
                if _RECKLESS.search(fh.read()):
                    out.add(int(m.group(1)))
    return out


def build(root=None):
    root = root or model.repo_root()
    with open(os.path.join(root, BATTLE_LIB), encoding="utf-8") as f:
        src = f.read()
    moves = pokedex.moves(root)
    name_of = calc_export.move_keys(root)

    def names(array):
        return sorted({name_of[m] for m in _array(src, array) if m in name_of})

    sheer_effects = {e.replace("BATTLE_EFFECT_", "") for e in _array(src, "sSheerForceEffects")}
    keep_effect = set(_array(src, "sSheerForceKeepEffectMoves"))
    sheer = sorted({name_of[m] for m, rec in moves.items() if m in name_of
                    and (rec["effect"] in sheer_effects or m in keep_effect)})
    crit = sorted({name_of[m] for m, rec in moves.items() if m in name_of
                   and rec["effect"] in ALWAYS_CRIT})
    contact = sorted({name_of[m] for m, rec in moves.items() if m in name_of
                      and "MAKES_CONTACT" in rec["flags"]})
    # Reckless raises a move by 1.2 when the move's effect script sets the
    # power multiplier to 12 for it (battle_lib.c applies powerMul to the
    # move's power), so the list is read from the scripts, not from the
    # calculator's own recoil and crash flags: the reworked one-turn moves
    # recoil in Oxide and in no later game.
    reckless = sorted({name_of[m] for m, rec in moves.items() if m in name_of
                       and rec.get("effect_id") in reckless_effects(root)})

    # The chart's rows in the engine's order: the game walks the table and
    # applies each matching row's factor in turn, so for a dual type the row
    # that comes first is applied first.
    chart_order = {}
    for i, (atk, dfn) in enumerate(pokedex.type_chart(root)):
        a, d = calc_export.type_name(atk), calc_export.type_name(dfn)
        chart_order.setdefault(a, {})[d] = i

    return {
        "slicing": names("sSlicingMoves"),
        "sound": names("sSoundMoves"),
        "bullet": names("sBallAndBombMoves"),
        "powder": names("sPowderMoves"),
        "pixilateKeepsType": names("sMovesKeepTheirType"),
        "sheerForce": sheer,
        "reckless": reckless,
        "alwaysCrit": crit,
        "contact": contact,
        "chartOrder": chart_order,
    }


def render(data):
    return ('"use strict";\n'
            "// Generated by tools/oxide/encounters/make_calc_mechanics.py from\n"
            "// src/battle/battle_lib.c, res/battle/scripts and res/moves; do not\n"
            "// edit. Oxide's own\n"
            "// move lists and type-chart order for the Platinum Oxide profile.\n"
            "exports.platinumOxideData = "
            + json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + ";\n")


def main(argv=None):
    root = model.repo_root()
    text = render(build(root))
    path = os.path.join(root, OUT)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
