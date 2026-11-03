"""The defensive index pins a few known cases (docs/oxide/defensive-index.md):
the post's formula reproduces the post's own ranking on the later games'
chart, Oxide's chart is the later one since 2026-11-03 and so puts Steel at
the post's 8.5, the engine's immunities read as they should, and the usage weights keep the post's structure.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_defensive_index
"""
import sys

from . import defensive_index as di


def main():
    results = []
    later, ox, pw = di.later_chart(), di.oxide_chart(), di.post_weights()

    steel = di.index(["STEEL"], later, pw)
    results.append(("Steel is +8.5 on the post's formula and the later chart, as the post has it",
                    abs(steel - 8.5) < 1e-9, f"{steel}"))

    # Grass is the one type the post's numbers do not give back: -2.5 here
    # against the post's -2.0, half a point the post must count elsewhere.
    off = {t: (round(di.index([t], later, pw), 2), di.POST_RANKING[t]) for t in di.TYPES
           if abs(di.index([t], later, pw) - di.POST_RANKING[t]) > 1e-9}
    results.append(("every other single type matches the post's ranking exactly", set(off) == {"GRASS"},
                    f"off: {off}"))

    diffs = {(a, d) for a, d, _o, _l in di.chart_differences()}
    # Until 2026-11-03 Steel still resisted Ghost and Dark here, which put it
    # at +11.0; Ian moved Steel to the later chart that day.
    # Since 2026-11-03 Ice also resists Water (the Ice proposal's first
    # lever), the one place Oxide's chart leaves the later games'.
    results.append(("Oxide's chart is the later games' but for Ice resisting Water",
                    diffs == {("WATER", "ICE")}, f"{sorted(diffs)}"))
    ox_ice = di.index(["ICE"], ox, pw)
    results.append(("so Ice is -4.5 on the post's weights, the post's -5.5 and a resistance worth 1",
                    abs(ox_ice - (-4.5)) < 1e-9, f"{ox_ice}"))
    ox_steel = di.index(["STEEL"], ox, pw)
    results.append(("so Steel is the post's +8.5 on Oxide's chart too",
                    abs(ox_steel - 8.5) < 1e-9, f"{ox_steel}"))

    # Snow in place of hail (Ian, 2026-11-03, the Ice proposal's second
    # lever): hail bites no one, so no type or ability is immune to it, and
    # Ice's every-engine-term index is its post's-terms one.
    ice_all = di.index(["ICE"], ox, pw, count=di.OXIDE_GROUPS)
    hail_immune = [t for t in di.TYPES if "hail" in di.groups([t])] + [
        a for a in ("SNOW_CLOAK", "ICE_BODY", "OVERCOAT", "MAGIC_GUARD") if "hail" in di.groups(["NORMAL"], a)]
    results.append(("no type or ability is immune to hail, which no longer bites (snow)",
                    not hail_immune and abs(ice_all - ox_ice) < 1e-9, f"immune {hail_immune}; Ice, every term {ice_all}"))

    ghost = (di.multiplier(ox, "NORMAL", ["GHOST"]), di.multiplier(ox, "FIGHTING", ["GHOST"]))
    results.append(("Ghost is immune to Normal and Fighting on Oxide's chart", ghost == (0.0, 0.0), f"{ghost}"))

    lev = di.multiplier(ox, "GROUND", ["ELECTRIC"], "LEVITATE")
    results.append(("Levitate makes an Electric type immune to Ground, and lifts it off the hazards",
                    lev == 0.0 and not di.grounded(["ELECTRIC"], "LEVITATE"), f"{lev}"))
    fat = di.multiplier(ox, "FIRE", ["GRASS"], "THICK_FAT")
    results.append(("Thick Fat halves Fire, so a Grass type takes it neutrally", fat == 1.0, f"{fat}"))

    groups = (di.groups(["ELECTRIC"]), di.groups(["GRASS"]), di.groups(["DARK"]))
    results.append(("Oxide's engine gives Electric paralysis, Grass powders and Leech Seed, Dark Prankster",
                    "paralysis" in groups[0] and {"powder", "leech_seed"} <= groups[1]
                    and "prankster" in groups[2], f"{groups}"))

    # The weights keep the post's structure: shares of 2 for each common
    # coverage type and 1 for the rest give back the post's own weights.
    w = di.weights_from_shares({t: (2.0 if t in di.POST_CC else 1.0) for t in di.TYPES})
    same = all(abs(w[t] - pw[t]) < 1e-9 for t in di.TYPES)
    results.append(("usage weights reproduce the post's 1 and 2 from 1:2 shares, summing to 25",
                    same and abs(sum(w.values()) - 25) < 1e-9, f"sum {sum(w.values()):.2f}"))

    hp = di.hidden_power_type({k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")})
    results.append(("Hidden Power with every IV at 31 is Dark, as Move_CalcVariableType has it",
                    hp == "DARK", hp))

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
