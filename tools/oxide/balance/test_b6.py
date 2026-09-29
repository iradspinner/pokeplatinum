"""B6 acceptance: the audit's placements, scale and levers (b6.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b6

Runs no Node: it reads b6.json as rescore.py saved it, and checks that
each B6 score's fingerprint matches its inputs and is verified, as test_b3
does for the scores before B6.
"""
import os
import sys

from . import b6, data, pool


def check_placements(results):
    """Every placed trainer lands in a split with a cap, at or under that
    cap, and no story fight or Hesperid is placed as an ordinary trainer."""
    caps = pool.caps()
    ox = data.oxide_trainers()
    story = {i for f in data.fights()["fights"] for i in f["tr_ids"]}
    bad = []
    for tr, p in b6.placements().items():
        ace = max(m["level"] for m in ox[tr]["party"])
        if p["split"] not in caps or ace > caps[p["split"]] or tr in story:
            bad.append(tr)
    placed = b6.placements()
    results.append(("every ordinary trainer placed in a split, under its cap", not bad,
                    f"{bad[:5]}" if bad else f"{len(placed)} trainers, "
                    f"{sum(p['how'] == 'required' for p in placed.values())} required"))


def check_scale(results):
    """The fight scale's line reads safer switch-ins as easier, and a fight
    every switch-in survives sits at the bottom band."""
    a, b = b6.scale_line()
    ok = b < 0 and b6.band(b6.on_scale(1.0, (a, b))) == b6.BANDS[0][0]
    results.append(("the fight scale falls with safe switch-ins", ok, f"{a:.1f} {b:+.1f} x safe"))


def check_bases(results):
    """Each fight's lever record starts from the fight's own stored score."""
    story = b6.story_scores()
    bad = []
    for key, rec in b6.load().get("fights", {}).items():
        old = story.get(key, {})
        if any(rec["base"][k] != old.get(k) for k in b6.LEVER_READ):
            bad.append(key)
    n = len(b6.load().get("fights", {}))
    results.append(("every lever record starts from its fight's stored score", not bad and n,
                    f"{bad[:5]}" if bad else f"{n} fights"))


def check_levers(results):
    """A lever on the player's attacking side (a TM, a damage item, the
    Choice items) changes only what the player's hits decide: never the
    boss's threat or the safe switch-ins, which its hits decide."""
    bad = []
    for key, rec in b6.load().get("fights", {}).items():
        for label, lv in rec["levers"].items():
            if lv["kind"] in ("cap", "weather") or not lv["delta"]:
                continue
            if lv["delta"]["threat_chance"] or lv["delta"]["safe"]:
                bad.append(f"{key} {label}")
    results.append(("attacking levers leave threat and safe switch-ins alone", not bad,
                    f"{bad[:5]}" if bad else ""))


def check_species(results):
    """Per species, a count of what it answers never passes what it faces."""
    bad = [sp for sp, t in b6.species_table(b6.load()).items()
           if not (t["alone"] <= t["answered"] <= t["faced"] and t["safe_in"] <= t["variants"])]
    results.append(("species tallies are consistent", not bad, f"{bad[:5]}" if bad else ""))


def check_teamscore(results):
    """The team builder's instant estimate: its fit covers every stored fight,
    it places Roark within the fit's story error of his full score, and an
    unsaved edit that raises every level reads no safer than the saved team."""
    import copy
    import json
    import os

    from . import pressure, teamscore
    fit = teamscore._fit()
    stored = len(pressure.load()["fights"]) + len(b6.load().get("trainers", {}))
    if not fit or fit.get("n") != stored or "story_max_error" not in fit:
        results.append(("team builder estimate is fitted to every stored fight", False,
                        f"fit {fit and fit.get('n')} of {stored} fights; run teamscore --fit"))
        return
    line = b6.scale_line()
    full = b6.on_scale(pressure.load()["fights"]["roark"]["safe"], line)
    est = teamscore.estimate("leader_roark")
    with open(os.path.join(data.ROOT, "res", "trainers", "data", "leader_roark.json"),
              encoding="utf-8") as f:
        edited = copy.deepcopy(json.load(f))
    for mon in edited["party"]:
        mon["level"] += 10
    harder = teamscore.estimate("leader_roark", edited)
    ok = abs(est["scale"] - full) <= fit["story_max_error"] and harder["safe"] <= est["safe"]
    results.append(("team builder estimate is fitted and tracks the full score", ok,
                    f"Roark {est['scale']} against {full:.1f}, {harder['scale']} ten levels up; "
                    f"story error {fit['story_mean_error']} over {fit['story_n']}"))


def check_gauntlet(results):
    """The gauntlet reading's duel, by hand: a member taking half the boss a
    turn and losing 0.3 a turn beats it in two turns, moving first, for one
    hit; moving second, for two; and a member that falls leaves the boss
    what its hits did not take."""
    from . import gauntlet
    cases = [
        gauntlet.duel((0.5, 0.3, True), 1.0, 1.0) == (True, 0.7, 0.0),
        abs(gauntlet.duel((0.5, 0.3, False), 1.0, 1.0)[1] - 0.4) < 1e-9,
        gauntlet.duel((0.2, 0.6, False), 1.0, 1.0) == (False, 0.0, 0.8),
        gauntlet.duel((0.2, 0.6, True), 1.0, 1.0)[2] == 0.6,
        gauntlet.duel((0.0, 0.1, True), 1.0, 1.0) == (False, 0.0, 1.0),
    ]
    results.append(("the gauntlet reading's duel carries damage both ways", all(cases),
                    str(cases)))
    # The sections keep Ian's rulings: 2 to 5 trainers each, Victory Road 1F
    # halved from its entrance, and Mt. Coronet's bosses and hard officers out.
    sizes = {(area, s[0]): len(gauntlet.section_trainers(area, s))
             for area, sections in gauntlet.SECTIONS.items() for s in sections}
    coronet = {tr for s in gauntlet.SECTIONS["mt_coronet"]
               for tr in gauntlet.section_trainers("mt_coronet", s)}
    vr = [gauntlet.section_trainers("victory_road", s) for s in gauntlet.SECTIONS["victory_road"][:2]]
    ok = (all(2 <= n <= 5 for n in sizes.values()) and not coronet & {520, 526, 834}
          and vr[0] == [234, 233, 226] and len(vr[1]) == 3)
    results.append(("gauntlet sections hold 2 to 5 trainers, bosses left out", ok,
                    f"{len(sizes)} sections" if ok else f"{sizes}, Coronet {coronet}, 1F {vr}"))


def check_pairs(results):
    """Every trainer the pair finder names, opponent or partner, has a file
    in res/trainers/data, and each key is its stems joined by "+", so the
    team builder's pair view can open both teams by the key."""
    from . import pairs
    ps = pairs.pairs()
    folder = os.path.join(data.ROOT, "res", "trainers", "data")
    missing = sorted({st for p in ps for st in p["stems"] + p["partners"]
                      if not os.path.exists(os.path.join(folder, f"{st}.json"))})
    bad_keys = [p["key"] for p in ps if p["key"] != "+".join(p["stems"])]
    results.append(("every pair names trainers with files, keyed by their stems",
                    not missing and not bad_keys,
                    f"no file: {missing[:5]}; bad keys: {bad_keys[:3]}" if missing or bad_keys
                    else f"{len(ps)} entries"))


def check_fingerprints(results):
    """Every B6 score (the ordinary trainers, each double against two
    trainers and each fight's levers) matches its inputs as they are now,
    and a second run has verified it."""
    from . import rescore
    problems = rescore.check(kinds=("b6", "b6lever", "b6pair"))
    kinds = {p: sum(q == p for _n, q in problems) for _n, p in problems}
    results.append(("every B6 score matches its inputs and is verified", not problems,
                    f"{kinds}; first {problems[:4]}" if problems else ""))


def main():
    results = []
    for check in (check_placements, check_scale, check_bases, check_levers, check_species,
                  check_teamscore, check_gauntlet, check_pairs, check_fingerprints):
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
