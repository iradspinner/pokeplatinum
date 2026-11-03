"""The counterpiece check (plcounter): its one-sided verdict, its pooling,
and on a real Roark box at a small budget, that it rebuilds a reading's
box and six, plays it on the reading's dice, and refuses a box that is not
the reading's. About a minute.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plcounter
"""
import contextlib
import io
import json
import os
import sys
import tempfile

from . import fightsim as fs, plcounter as pc, plgoal3 as g, plteam as pt


def verdict_checks():
    out = []
    v = pc.verdict
    out.append(("a candidate the old six beats about as often as the old team is too easy",
                v(0.96, 1.0).startswith("too easy") and v(0.95, 1.0).startswith("too easy"),
                f"{v(0.96, 1.0)}; {v(0.95, 1.0)}"))
    out.append(("a lower rate under the target leaves it to the full reading",
                v(0.80, 1.0, 0.88) == "reading decides" and v(0.80, 1.0) == "reading decides", v(0.80, 1.0, 0.88)))
    out.append(("a lower rate over the target is too easy", v(0.90, 1.0, 0.88) == "too easy (over the target)",
                v(0.90, 1.0, 0.88)))
    p = pc.pooled([{"fights": 75, "won": 1.0, "faints": 0.4, "clean": 0.6},
                   {"fights": 25, "won": 0.6, "faints": 2.0, "clean": 0.2}])
    out.append(("numbers pool weighted by their fights",
                p["fights"] == 100 and abs(p["won"] - 0.9) < 1e-9 and abs(p["faints"] - 0.8) < 1e-9, str(p)))
    return out


def roark_checks():
    """A fake reading of Roark's box 1 whose six is two members (short
    fights), read with budget 2 on two fights and one."""
    out = []
    f = next(x for x in g.fights() if x["slug"] == "roark")
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = os.path.join(tmp, "counter-test-run")     # no such run under goal 3: no history
        s = g.setup(os.path.basename(run_dir), "roark", 1)
        recs = s["built"]["records"]
        st, keys, boss_keys, flags = g.fight_state(s["key"], recs, s["stock"], s["v"], "roark")
        win = keys[:2]
        cfg = {"budget": 2}
        with contextlib.redirect_stdout(io.StringIO()):
            real, unl, rows = pt.full_reading(st, boss_keys, flags, win, cfg, real=2, unlucky=1, procs=1)
        old = {"how": "search", "box": [f"{r['label']} ({r['area']})" for r in recs], "level": s["lvl"],
               "starter": s["whole"][0].species, "history_from": s["hist_from"], "trainer": s["trainer"]["constant"],
               "winner": [pt.member_name(st["pokemon"][k]) for k in win],
               "moves": {st["pokemon"][k]["species"]: st["moves"][k] for k in win},
               "items": {st["pokemon"][k]["species"]: it for k, it in fs.assign_items(st, win).items() if it},
               "chosen": g.uses(st, win, f, s["lvl"]), "real": real, "unlucky": unl,
               "foes": [f"{st['pokemon'][k]['species']} {st['pokemon'][k]['level']}" for k in boss_keys]}
        os.makedirs(os.path.join(run_dir, "roark", "box1"))
        with open(os.path.join(run_dir, "roark", "box1", "result.json"), "w") as fh:
            json.dump(old, fh)
        with contextlib.redirect_stdout(io.StringIO()):
            res = pc.check(run_dir, "roark", "test", seeds=(1,), procs=1, cfg=cfg, real=2, unlucky=1,
                           log=lambda *a: None)
        b = res["boxes"][0]
        out.append(("the reading's six is rebuilt and played on the reading's own dice",
                    b["six"] == old["winner"] and b["real"] == real and b["unlucky"] == unl
                    and res["same_team_as_reading"], f"{b['six']}: {b['real']} against {real}"))
        out.append(("the table and the pooled verdict come out", "| all |" in pc.table(res)
                    and res["pool"]["verdict"] in ("too easy (old six wins as often)", "reading decides"),
                    res["pool"]["verdict"]))
        # A box that is not the reading's is refused.
        old["box"] = old["box"][1:]
        with open(os.path.join(run_dir, "roark", "box1", "result.json"), "w") as fh:
            json.dump(old, fh)
        try:
            pc.check(run_dir, "roark", "test", seeds=(1,), procs=1, cfg=cfg, real=1, unlucky=0, log=lambda *a: None)
            refused = ""
        except pc.Mismatch as e:
            refused = str(e)
        out.append(("a box that differs from the reading's is refused", "box differs" in refused, refused[:80]))
    return out


def main():
    results = verdict_checks() + roark_checks()
    width = max(len(r[0]) for r in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
