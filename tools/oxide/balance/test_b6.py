"""B6 acceptance: the audit's placements, scale and levers (b6.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b6

Runs no Node: it reads b6.json as rescore.py saved it. Whether each stored
score is current and verified is test_b3's fingerprint check.
"""
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


def main():
    results = []
    for check in (check_placements, check_scale, check_bases, check_levers, check_species):
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
