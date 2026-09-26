"""B5: Ian's bellwether fights, and each reading against the reference hacks.

    PYTHONPATH=. python3 -m tools.oxide.balance.calibrate --run      # score the extra fights
    PYTHONPATH=. python3 -m tools.oxide.balance.calibrate --report

Ian named three bellwethers on 2026-09-25, fights he built or played and
whose feel he knows:

- Maylene, whom he expected B3's threat to overrate: a fast team of
  attackers;
- Officer Hesperid at Lake Valor, just before Saturn 1 ("[TESTING, DEMON
  FIGHT]" in his sheet): very hard to plan for, and likely underrated;
- Volkner, so easy as to be boring: little coverage, Choice items, mostly
  hyper offense, and a crippling weakness to Ground.

He added that a fight whose every turn can be foreseen is easy to plan
against, which pressure.py's "predictable" reading estimates.

Maylene and Volkner are story fights, scored in pressure.json. Hesperid is
an ordinary trainer, so this tool scores her, and her second fight on Mt.
Coronet 6F, the same way into calibrate.json, at the split each is fought
in. The report ranks the bellwethers on every reading among Oxide's fights,
and sets each reading's mean over the gyms and the League beside Ian's
rating of every reference hack.
"""
import argparse
import json
import os
import sys
import tempfile

from ..encounters import calc_export
from . import data, pressure, refpressure

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "calibrate.json")

EXTRA = [("TRAINER_GALACTIC_GRUNT_LAKE_VALOR_2", "Candice", "hesperid_valor",
          "Hesperid, Valor"),
         ("TRAINER_GALACTIC_GRUNT_MT_CORONET_6F", "Galactic", "hesperid_coronet",
          "Hesperid, Coronet")]
BELLWETHERS = ["maylene", "hesperid_valor", "volkner"]
# Each reading, and whether a higher value reads harder.
READINGS = [("threat", True), ("threat_chance", True), ("answers", False),
            ("answers_duel", False), ("broad", False), ("unseen_count", True),
            ("predictable", False)]
# The seats every reference fills: the gyms, the Elite Four and the Champion.
SEATS = ["roark", "gardenia", "fantina", "maylene", "wake", "byron", "candice", "volkner",
         "aaron", "bertha", "flint", "lucian", "cynthia"]


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "fights": {}}


def save(results):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")


def run(results):
    by_constant = {t["constant"]: t for t in data.oxide_trainers().values()}
    blob = calc_export.build()
    with tempfile.TemporaryDirectory(prefix="oxide-b5-blob-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        for constant, split, key, label in EXTRA:
            t = by_constant[constant]
            fight = {"key": key, "label": label, "split": split, "tr_ids": [t["tr_id"]]}
            r = pressure.score_fight(fight, blob, blob_path, parties=[t["party"]])
            results["fights"][key] = r
            save(results)
            print(f"{label}: threat {r['threat']:.2f}, answers {r['answers']:.2f}", flush=True)


def _fights():
    """Oxide's story fights and the extra ones, keyed as scored."""
    return {**pressure.load()["fights"], **load()["fights"]}


def rank_table(out=sys.stdout):
    """Each bellwether's value and rank on every reading, 1 the hardest,
    among Oxide's story fights and the extras."""
    fights = _fights()
    print(f"Ranks among {len(fights)} fights, 1 the hardest:", file=out)
    print(f"{'reading':16}" + "".join(f"{fights[k]['label'][:18]:>22}" for k in BELLWETHERS),
          file=out)
    for reading, harder_high in READINGS:
        vals = {k: r.get(reading) for k, r in fights.items() if r.get(reading) is not None}
        order = sorted(vals, key=lambda k: -vals[k] if harder_high else vals[k])
        cells = []
        for k in BELLWETHERS:
            v = vals.get(k)
            cells.append(f"{v:.2f} (#{order.index(k) + 1})" if v is not None else "none")
        print(f"{reading:16}" + "".join(f"{c:>22}" for c in cells), file=out)


def _mean(rows, reading):
    vals = [r[reading] for r in rows if r.get(reading) is not None]
    return sum(vals) / len(vals) if vals else None


def _spearman(xs, ys):
    """Rank correlation, with ties given their mean rank."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                out[order[k]] = (i + j) / 2
            i = j + 1
        return out
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sx = sum((a - mx) ** 2 for a in rx) ** 0.5
    sy = sum((b - my) ** 2 for b in ry) ** 0.5
    return cov / (sx * sy) if sx and sy else None


def ref_table(out=sys.stdout):
    """Each reading's mean over the seats a hack fills, beside Ian's rating,
    and each reading's rank correlation with the ratings (a reading that
    tracks Ian's ratings comes out near 1 when higher reads harder, near
    -1 when lower does)."""
    oxide = pressure.load()["fights"]
    rows = [("oxide", "Oxide as it stands", None, [oxide[k] for k in SEATS if k in oxide])]
    for hack in refpressure.HACKS:
        if not os.path.exists(refpressure.out_path(hack)):
            continue
        saved = refpressure.load(hack)
        rows.append((hack, saved["title"], saved["rating"],
                     [saved["fights"][k] for k in SEATS if k in saved["fights"]]))
    print("\nThe gyms and the League, mean over the seats each hack fills:", file=out)
    print(f"{'hack':12}{'rating':>7}{'seats':>6}" + "".join(f"{r[:9]:>10}" for r, _ in READINGS),
          file=out)
    for hack, _title, rating, fights in rows:
        cells = "".join(f"{_mean(fights, r):>10.2f}" if _mean(fights, r) is not None
                        else f"{'':>10}" for r, _ in READINGS)
        print(f"{hack:12}{str(rating or ''):>7}{len(fights):>6}{cells}", file=out)
    rated = [(rating, fights) for _h, _t, rating, fights in rows if isinstance(rating, (int, float))]
    print(f"{'rank corr.':25}" + "".join(
        f"{_spearman([_mean(f, r) for _, f in rated], [x for x, _ in rated]) or 0:>10.2f}"
        for r, _ in READINGS), file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    results = load()
    if args.run:
        run(results)
    if args.report or not args.run:
        rank_table()
        ref_table()
    return 0


if __name__ == "__main__":
    sys.exit(main())
