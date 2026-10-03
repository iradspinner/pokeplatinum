"""The team search's first test (the Overseer's, Ian's go of 2026-10-02): the
search on the hand run's own boxes at Roark (cap 16), Mars 1 at its new soft
cap of 19, and Gardenia (cap 26). Does it find our hand-played sixes, or
sixes that read as well by Ian's order (wins first, then faints)? A miss at
Mars 1, which our six wins by a PP stall, would show the screen undervaluing
stall plans.

Each fight's box is the run's box at that fight (plstep3's ROARK, MARS and
GARDENIA records: natures, abilities, levels), each member with its whole
move pool by the capture rule from its catch level (box3.json) through the
run's holds and evolutions. Results and a log go to
~/oxide-trials/scorer-stage2/team/<fight>/.

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plteam_test roark mars gardenia
"""
import json
import os
import sys
import time

from . import plteam, plstep3

RUN = os.path.expanduser("~/oxide-trials/three-gym-run")
HOLDS = {"SPECIES_CHARMANDER": 25, "SPECIES_GRUBBIN": 21, "SPECIES_MAREEP": 28, "SPECIES_POPPLIO": 31}
# The two trades come in at the level of the Pokemon given (about the cap of
# the split they were made in), and the honey tree's Grubbin at 13.
EXTRA = {"SPECIES_VULLABY": 16, "SPECIES_POPPLIO": 20, "SPECIES_GRUBBIN": 13}
# fight: (story key, cap, box records, the bar's six with its moves, the bar's numbers)
TESTS = {
    "roark": ("roark", 16, plstep3.ROARK, plstep3.FIGHTS["roark"]["six"], "98.5% clean, 100% won, 0.015 faints"),
    "mars": ("mars_1", 19, plstep3.MARS, ["Geodude", "Vullaby", "Starly", "Onix", "Grubbin", "Nidorino"],
             "67.1% clean, 99.8% won, 0.423 faints (our line adjusted to 19)"),
    "gardenia": ("gardenia", 26, plstep3.GARDENIA, plstep3.FIGHTS["gardenia"]["six"],
                 "15.1% clean, 59.9% won, 3.212 faints"),
}


def caught_levels():
    """{caught species: level} from the rolled box, with the trades and the
    honey tree."""
    out = {}
    for _where, sp, lvl in json.load(open(os.path.join(RUN, "box3.json"))):
        out[sp] = int(str(lvl).split("-")[-1])
    out.update(EXTRA)
    return out


def family(sp):
    seen, todo = {sp}, [sp]
    while todo:
        cur = todo.pop()
        for e in plteam.mon_data(cur).get("evolutions") or []:
            if str(e[-1]).startswith("SPECIES_") and e[-1] not in seen:
                seen.add(e[-1])
                todo.append(e[-1])
    return seen


def box(records, cap):
    """The box's members as the team search reads them, at the cap: each
    from its catch through the run's holds and evolutions, with its whole
    move pool."""
    caught = caught_levels()
    out = []
    for name, rec in records.items():
        const, nature, ability = rec[0], rec[1], rec[2]
        ivs = rec[4] if len(rec) > 4 else 15
        level = rec[5] if len(rec) > 5 else cap
        if name == "Charjabug" and cap < 20:
            const = "SPECIES_GRUBBIN"
        base = next(sp for sp in caught if const in family(sp))
        final, pool_ = plteam.move_pool(base, caught[base], level, HOLDS, magnetic=cap >= 26)
        out.append(plteam.record(final, level, nature, ability, ivs, pool_))
    return out


def run(fight, procs=10, log_to=None):
    key, cap, records, bar_six, bar = TESTS[fight]
    out_dir = os.path.join(plteam.ROOT, "team", fight)
    os.makedirs(out_dir, exist_ok=True)
    logf = open(os.path.join(out_dir, "log.txt"), "a")

    def log(*a):
        line = " ".join(str(x) for x in a)
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    t0 = time.time()
    recs = box(records, cap)
    f = plstep3.FIGHTS[fight]
    stock = {"boosters": dict(f["boosters"]), "Leftovers": 0, "Sitrus Berry": 0}
    st, keys, boss_keys, flags = plteam.prepare(key, recs, stock)
    names = {k: st["pokemon"][k]["species"] for k in keys}
    log(f"== {fight} at {cap}: box of {len(keys)}: {', '.join(names[k] for k in keys)}; "
        f"prepared in {time.time() - t0:.0f} s")
    sixes, scores, M, moves = plteam.screen(st, keys, boss_keys)
    ours = [k for k in keys if names[k] in bar_six]
    log("screen, top sixes:")
    for s, sc in list(zip(sixes, scores))[:10]:
        log(f"  {sc:6.2f}  {', '.join(names[k] for k in s)}")
    all_scores = plteam.score_sixes(M)
    rank = next((i for i, (_s, idx) in enumerate(all_scores) if {keys[j] for j in idx} == set(ours)), None)
    log(f"our six ({', '.join(names[k] for k in ours)}): screen rank {rank} of {len(all_scores)}, "
        f"score {all_scores[rank][0]:.2f}" if rank is not None else "our six: not in the box")
    log("moves picked: " + "; ".join(f"{names[k]} {', '.join(moves[k])}" for k in keys))
    t1 = time.time()
    lab_dir = os.path.join(out_dir, "labels")
    metas = plteam.label(st, sixes[:10], boss_keys, flags, f"team:{fight}", lab_dir, procs=procs)
    log(f"labels: {sum(m['positions'] for m in metas)} positions from {sum(m['games'] for m in metas)} fights "
        f"in {time.time() - t1:.0f} s")
    t1 = time.time()
    base = plteam.without([fight], os.path.join(plteam.ROOT, "subsets", f"no-{fight}-team"))
    model = plteam.train(f"team-{fight}", [base, lab_dir])
    log(f"networks {model} trained in {time.time() - t1:.0f} s")
    cfg = {"value": model}
    t1 = time.time()
    finalists, tally, w = plteam.race(st, keys, boss_keys, flags, sixes, cfg, log=log)
    log(f"race in {time.time() - t1:.0f} s; finalists: " +
        "; ".join(f"{', '.join(names[k] for k in t)} ({tally.score(t):.2f} on {tally.numbers(t)['fights']})"
                  for t in finalists))
    log("member weights: " + ", ".join(f"{names[k]} {w[k]:.3f}" for k in sorted(keys, key=lambda k: -w[k])))
    results = []
    for t in finalists:
        real, unlucky, rows = plteam.full_reading(st, boss_keys, flags, list(t), cfg, procs=procs)
        results.append((t, real, unlucky, rows))
        log(f"finalist {', '.join(names[k] for k in t)}: real {real['won']:.1%} won, {real['faints']:.3f} faints, "
            f"{real['clean']:.1%} clean; very unlucky {unlucky['won']:.1%} won, {unlucky['faints']:.3f} faints")
    best = max(results, key=lambda r: plteam.ian_order(r[1]))
    ours_real, ours_unlucky, _rows = plteam.full_reading(st, boss_keys, flags, ours, cfg, procs=procs)
    log(f"our six read the same way (its members with the screen's moves): real {ours_real['won']:.1%} won, "
        f"{ours_real['faints']:.3f} faints, {ours_real['clean']:.1%} clean; the bar: {bar}")
    t1 = time.time()
    po = plteam.read(st, boss_keys, flags, [best[0]], 25, {}, procs=procs, seed0=77)
    n = po.numbers(best[0])
    log(f"diagnosis, the play-out planner on the winner (25 fights): {n['won']:.1%} won, {n['faints']:.3f} faints, "
        f"{n['clean']:.1%} clean, in {time.time() - t1:.0f} s; the network on it: {best[1]['won']:.1%} won, "
        f"{best[1]['faints']:.3f} faints")
    log("the winner's faints fell to: " + str(plteam.losing_enemies(best[3])[:4]))
    summary = {"fight": fight, "cap": cap, "box": [names[k] for k in keys],
               "screen": [[names[k] for k in s] for s in sixes], "our_rank": rank,
               "finalists": [{"six": [names[k] for k in t], "real": r, "unlucky": u} for t, r, u, _x in results],
               "ours": {"real": ours_real, "unlucky": ours_unlucky}, "bar": bar,
               "playouts_on_winner": n, "minutes": round((time.time() - t0) / 60, 1)}
    with open(os.path.join(out_dir, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    log(f"== {fight} done in {(time.time() - t0) / 60:.0f} minutes")
    return summary


if __name__ == "__main__":
    for fight in sys.argv[1:] or list(TESTS):
        run(fight)
