"""The learnset study's acceptance: its reading of Kaizo and its rules (learnstudy.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learnstudy

Reads Kaizo's lists and calculator file, vanilla from main and Oxide's
moves; runs no Node.
"""
import sys

from . import learnstudy as ls


def check_reading(results):
    """Every move in Ian's Kaizo lists is found in Kaizo's data, every species
    has Kaizo's types, and every species sits in exactly one line's family."""
    lists = ls.kaizo_lists()
    missing = sorted({e["move"] for sp in lists for e in ls.entries(sp) if e["kind"] == "unknown"})
    untyped = [r["name"] for r in lists.values() if not r["types"]]
    placed = {sp for line in ls.lines() for sp in line}
    ok = not missing and not untyped and placed == set(lists)
    results.append(("Kaizo's lists read in full", ok,
                    f"missing {missing[:5]}, untyped {untyped[:5]}, "
                    f"{len(set(lists) - placed)} species in no line" if not ok else
                    f"{len(lists)} species, {len(ls.lines())} lines"))


def check_named(results):
    """The dead-weight rule catches each move Ian named as never good, in
    every split and as a starting move (Octazooka at vanilla's values)."""
    kept = {name: where for name, where in ls.named_check().items() if where}
    results.append(("the rule catches every move Ian named, everywhere", not kept,
                    f"{kept}" if kept else f"{len(ls.NAMED)} moves"))


def check_kaizo_rate(results):
    """The rule is read off Kaizo's lists, so Kaizo's own lists rarely break it."""
    n, start, later = ls.kaizo_dead_weight()
    share = (sum(start.values()) + sum(later.values())) / n
    results.append(("Kaizo's own lists break the rule in under 5% of entries", share < 0.05,
                    f"{share:.3f} of {n}"))


def check_placement(results):
    """A move's usual split places Kaizo's moves on held-out families better
    than the strength curve or vanilla's timing, and a move Kaizo never used
    is placed better by moves of like strength than by the curve."""
    r = ls.placement_test()
    usual = r["a known move's usual split, damaging moves only"]["mean"]
    unseen = r["an unseen move, by moves of like strength"]["mean"]
    curve = r["an unseen move, by the curve"]["mean"]
    vanilla = r["vanilla's split, where vanilla has the move"]["mean"]
    ok = usual < unseen < curve and usual < vanilla
    results.append(("usual split beats the curve and vanilla on held-out families", ok,
                    f"usual {usual:.2f}, like strength {unseen:.2f}, curve {curve:.2f}, "
                    f"vanilla {vanilla:.2f}"))


def check_kaizo_docs(results):
    """Kaizo's documentation reads whole, and Ian's example holds: Kaizo's
    Route 207 Growlithe may Roar, a quarter of its turns."""
    from . import kaizo_docs, learnwild
    docs = kaizo_docs.load()
    rows, _later = learnwild.readings("kaizo")
    growlithe = [r for r in rows if r["species"] == "SPECIES_GROWLITHE" and r["area"] == "Route 207"]
    ok = (len(docs["field"]) == 202 and docs["hazards"] == ["MEMENTO", "ROAR", "WHIRLWIND",
                                                            "TELEPORT", "SELFDESTRUCT", "EXPLOSION"]
          and growlithe and all("Roar" in r["moves"] and r["ends"] == 0.25 for r in growlithe))
    results.append(("Kaizo's docs read, and its Route 207 Growlithe may Roar", bool(ok),
                    f"{len(docs['field'])} tables, hazards {docs['hazards']}, "
                    f"Growlithe {[r['moves'] for r in growlithe][:1]}"))


def check_generator(results):
    """Every proposed list keeps the rules: no level past 78; no dead weight,
    cut move or weather move for an obtainable species; a first stage starts
    with an attack (Abra with Confusion); no wild slot can end the encounter."""
    from . import learngen as g, learnwild
    g.propose_all()
    learnwild.clear()
    bad = []
    for sp, lst in g.PROPOSED.items():
        types = {t.title() for t in (g.pokedex.load(g.data.ROOT, sp) or {}).get("types", [])}
        for lv, c in lst:
            if lv > 78 or g._dropped(c, sp, lv, types):
                bad.append(f"{sp} {lv} {c}")
        chain = g._chain(sp)
        if len(chain) == 1 and not any(
                lv <= 1 and ls.strength(ls.oxide_move(g._oxide_moves()[c]))[0] in ("damage", "fixed")
                for lv, c in lst):
            bad.append(f"{sp}: no attack at level 1")
    abra = (1, "MOVE_CONFUSION") in g.PROPOSED.get("SPECIES_ABRA", [])
    rows, _later = learnwild.readings("proposal")
    ends = sum(1 for r in rows if r["ends"])
    learnwild.clear()
    ok = not bad and abra and ends == 0
    results.append(("the generator's lists keep the rules", ok,
                    f"{len(g.PROPOSED)} species" if ok else
                    f"{bad[:5]}, Abra's Confusion {abra}, ending slots {ends}"))


def main():
    results = []
    for check in (check_reading, check_named, check_kaizo_rate, check_placement,
                  check_kaizo_docs, check_generator):
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
