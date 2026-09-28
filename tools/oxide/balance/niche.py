"""Ian's niche check (2026-09-28): every Pokemon should have an important
niche at the point the player has it, while stronger and weaker lines stay
fine.

    PYTHONPATH=. python3 -m tools.oxide.balance.niche      # both readings and the report

It writes no game data. Each stage the player can own is read in the split
it is first owned in, at that split's cap, with the moves it can have by
then (the capture rule, TMs and tutors, as the power bar reads them),
against every trainer Pokemon of that split, by the calculator the scores
use (the middle roll), in four roles:

- offense: the mean share of a foe's HP its best move takes in one hit,
  capped at all of it;
- speed: the share of foes it outspeeds;
- physical wall and special wall: of the foes whose best attack on it is
  physical (or special), the share that need three or more hits to knock
  it out while it knocks them out in three or fewer, since a bulky stage
  with nothing to attack with is no wall in a nuzlocke (the Overseer,
  2026-09-28), and a wall walls one side (Ian's Aggron, Blissey);
- status: its best status move by Ian's tiers (status-move-tiers.md),
  counting only moves the player may use (no weather, no partner move,
  nothing the engine leaves undone, nothing the first cut removed).

Each role is ranked against every stage the player can own by the same
split, read the same way, as a mid-rank percentile (ties share the middle
of their block). Its standing is the mean of its five percentiles, 0.5
being the split's average; Ian's super-wanted lines should sit a little
above it. A stage has a niche when one role puts it at 0.75 or more, the
split's top quarter, or when its standing does (an all-rounder, such as
Milotic, good at much and best at nothing); a stage with none is a
finding, as an overbuff is (Ian, 2026-09-28).

Two readings: Oxide's lists today, and the proposal (the learnset proposal
with the later moves' adds, replaces and relearner entries). A stage's
bulk and speed do not depend on its moves, so the foes' attacks on it are
computed once for both, and its own attacks once per distinct move set.
"""
import argparse
import collections
import csv
import json
import os
import sys

from ..encounters import pokedex
from . import b6, data, learngen as g, laterlearn as ll, learnplan as lp, pool, pressure, teamscore

OUT_MD = os.path.join(data.ROOT, "docs", "oxide", "niche-check.md")
OUT_TSV = os.path.join(data.ROOT, "docs", "oxide", "niche-check.tsv")
VALUES = os.path.join(data.ROOT, "docs", "oxide", "encounters", "values.json")
ROLES = ("offense", "speed", "phys_wall", "spec_wall", "status")
ROLE_NAMES = {"offense": "offense", "speed": "speed", "phys_wall": "physical wall",
              "spec_wall": "special wall", "status": "status", "all_round": "all-rounder"}
NICHE = 0.75            # a role in the split's top quarter
CHUNK = 60              # stages per calculator run, to keep each output small
READINGS = ("today", "proposal")


def wanted():
    """Ian's super-wanted lines, by their first stages."""
    with open(VALUES, encoding="utf-8") as f:
        return set(json.load(f).get("wanted") or [])


def proposal_lists():
    """{species: [(level, MOVE_X)]}: the learnset proposal with the later
    moves placed on it (added, replacing a weaker move, or relearner only)."""
    lists = {s: list(v) for s, v in ll.proposal_lists().items()}
    by_name = {lp.name(c): c for c in lp.M()}
    with open(ll.OUT_TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["action"] not in ("added", "replaces", "relearner only") or not r["level"]:
                continue
            c = by_name.get(r["move"])
            if not c:
                continue
            s = r["species"]
            lst = lists.get(s) or list(lp._now(s))
            if r["replaces"]:
                gone = by_name.get(r["replaces"])
                lst = [e for e in lst if e[1] != gone]
            lists[s] = sorted(lst + [(int(r["level"]), c)])
    return lists


def _usable_status(c):
    return (c in lp.M() and lp.M()[c]["class"] == "STATUS" and c not in g.WEATHER_MOVES
            and c not in ll._doubles_only() and c not in b6.DEAD_MOVES and ll.placeable(c))


def status_value(species, split):
    """The best tier rank among the status moves the stage can have by the
    split (lp.PROPOSED decides the lists)."""
    return max((lp.rank(c) or 0 for c in lp._can_have(species, split) if _usable_status(c)), default=0)


def _use(lists):
    lp.PROPOSED.clear()
    lp.PROPOSED.update(lists)


def measure(split, blob, reading_lists, log=None):
    """{reading: {species: {role: value}}} for every stage the player can own
    by the split. A stage the calculator does not know is left out."""
    stages = sorted(s for s in pool.species_by_split()[split] if s in g._obtainable())
    foes = list({json.dumps(m, sort_keys=True): m for m in lp._split_trainer_mons(split)}.values())
    recs, status = {}, {}
    for reading, lists in reading_lists.items():
        _use(lists)
        for s in stages:
            recs[(reading, s)] = lp._bar_record(s, split, blob)
            status[(reading, s)] = status_value(s, split)
    measured = [s for s in stages if recs[(READINGS[0], s)]]
    dealt, taken, faster, side = {}, {}, {}, {}
    for start in range(0, len(measured), CHUNK):
        chunk = measured[start:start + CHUNK]
        jobs = {"pokemon": {f"f{j}": m for j, m in enumerate(foes)}, "pairs": []}
        keyed = {}          # (stage, move tuple) -> pokemon key
        for i, s in enumerate(chunk):
            jobs["pokemon"][f"s{i}"] = recs[(READINGS[0], s)]
            for j, m in enumerate(foes):
                jobs["pairs"].append([f"f{j}", f"s{i}", m["moves"], None])
            for reading in reading_lists:
                mv = tuple(recs[(reading, s)]["moves"])
                if (s, mv) in keyed or not mv:
                    continue
                key = f"s{i}m{len([k for k in keyed if k[0] == s])}"
                keyed[(s, mv)] = key
                jobs["pokemon"][key] = recs[(reading, s)]
                for j in range(len(foes)):
                    jobs["pairs"].append([key, f"f{j}", list(mv), None])
        out = pressure.run_node(teamscore._blob_path(), jobs)
        hp = {k: v["hp"] for k, v in out["pokemon"].items()}
        for r in out["results"]:
            best, cat = max(((v["rolls"][len(v["rolls"]) // 2], v.get("category") or "")
                             for v in r["moves"].values() if v.get("rolls")), default=(0, ""))
            share = min(1.0, best / hp[r["d"]]) if hp.get(r["d"]) else 0.0
            if r["a"].startswith("f"):
                taken[(r["d"], r["a"])] = share
                side[(r["d"], r["a"])] = cat          # the kind of the foe's best attack on it
                faster[(r["d"], r["a"])] = r["speeds"][1] > r["speeds"][0]
            else:
                dealt[(r["a"], r["d"])] = share
        index = {s: f"s{i}" for i, s in enumerate(chunk)}
        for s in chunk:
            base = index[s]
            for reading in reading_lists:
                key = keyed.get((s, tuple(recs[(reading, s)]["moves"])))
                vals = {"offense": 0.0, "speed": 0.0}
                walled = {"Physical": [0, 0], "Special": [0, 0]}      # [walled, met]
                for j in range(len(foes)):
                    f = f"f{j}"
                    d = dealt.get((key, f), 0.0) if key else 0.0
                    t = taken.get((base, f), 0.0)
                    vals["offense"] += d
                    vals["speed"] += faster.get((base, f), False)
                    if side.get((base, f)) in walled:
                        walled[side[(base, f)]][1] += 1
                        walled[side[(base, f)]][0] += t < 0.5 and d >= 1 / 3
                vals = {k: round(v / len(foes), 4) for k, v in vals.items()}
                vals["phys_wall"] = round(walled["Physical"][0] / walled["Physical"][1], 4) \
                    if walled["Physical"][1] else 0.0
                vals["spec_wall"] = round(walled["Special"][0] / walled["Special"][1], 4) \
                    if walled["Special"][1] else 0.0
                vals["status"] = status[(reading, s)]
                recs[("out", reading, s)] = vals
        if log:
            print(f"  {split}: {min(start + CHUNK, len(measured))} of {len(measured)} stages", file=log, flush=True)
    return {reading: {s: recs[("out", reading, s)] for s in measured} for reading in reading_lists}


def percentile(v, field):
    """The mid-rank percentile of v in the field: those below, and half of
    those equal."""
    below = sum(x < v for x in field)
    equal = sum(x == v for x in field)
    return round((below + equal / 2) / len(field), 3)


def passing(species, split):
    """Whether the player can evolve the stage within the split it is first
    owned in, so it is held only briefly."""
    return any(pool.reachable(need, item, split) for need, item, _t in pool.evolutions(species))


def first_stage(species):
    return lp.line_of(species)[0]


# Words in a scripted source's conditions that put it after the story.
POST_GAME = ("post-game", "national dex", "unreachable", "not released", "never distributed")


# Sources the conditions do not mark post-game but that come after the story.
AFTER_STORY = {
    "SPECIES_REGIGIGAS": "needs Regirock, Regice and Registeel, which are post-game",
    "SPECIES_DIALGA": "vanilla Platinum has it caught after the League; the sources file's "
                      "\"story battle\" at level 70 is not placed by the pool either",
    "SPECIES_PALKIA": "as Dialga",
}


def add_unmapped_sources():
    """{species: split} for the scripted sources the pool places nowhere. The
    pool places a source only in its location's split and only at or under
    that split's cap, so the Mining Museum's level 20 fossils, in Roark's
    split (cap 16), and Cresselia's Fullmoon Island release, whose location
    it does not know, sit in no split although the player can have them in
    the story. For this check only, each such source that nothing marks as
    after the story is placed in the later of its location's split and the
    first split whose cap admits its level, and the pool's caches are
    rebuilt with it."""
    locs = pool._location_splits()
    species = set(pokedex.species_list(data.ROOT))
    added = {}
    with open(pool.SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = row["species"]
            if s not in species or s not in g._obtainable() or lp._owned_from(s) or s in AFTER_STORY:
                continue
            if any(w in (row["conditions"] or "").lower() for w in POST_GAME):
                continue
            level = pool._source_level(row["level"])
            split = pool.later(*[x for x in (locs.get(row["location"]), lp._split_of(level)) if x])
            if split not in lp.SPLITS:
                continue
            pool.catches().setdefault(s, []).append((split, level, row["method"]))
            if s not in added or lp.SPLITS.index(split) < lp.SPLITS.index(added[s]):
                added[s] = split
    for s, split in added.items():
        pool.caught()[s] = (split, "source")
    pool.species_by_split.cache_clear()
    lp._owned_from.cache_clear()
    return added


def run(log=sys.stdout):
    """[row] for every stage the player can own, in both readings."""
    blob = teamscore._blob()
    reading_lists = {"today": {}, "proposal": proposal_lists()}
    added = add_unmapped_sources()
    species = set(pokedex.species_list(data.ROOT))
    firsts = {s: lp._owned_from(s) for s in g._obtainable() if s in species}
    splits = [sp for sp in lp.SPLITS if sp in set(firsts.values())]
    rows = []
    for split in splits:
        values = measure(split, blob, reading_lists, log)
        for reading, by_stage in values.items():
            field = {role: [v[role] for v in by_stage.values()] for role in ROLES}
            pct = {s: {role: percentile(v[role], field[role]) for role in ROLES} for s, v in by_stage.items()}
            standing = {s: round(sum(p.values()) / len(ROLES), 3) for s, p in pct.items()}
            for s, v in by_stage.items():
                if firsts.get(s) != split:
                    continue
                all_round = percentile(standing[s], list(standing.values()))
                niche = [role for role in ROLES if pct[s][role] >= NICHE]
                if all_round >= NICHE:
                    niche.append("all_round")
                rows.append({"species": s, "line": first_stage(s), "split": split, "reading": reading,
                             **v, **{f"{role}_pct": pct[s][role] for role in ROLES},
                             "standing": standing[s], "all_round_pct": all_round, "niche": niche,
                             "passing": passing(s, split), "field": len(by_stage)})
    unmeasured = sorted(s for s, sp in firsts.items() if sp in splits
                        and not any(r["species"] == s for r in rows))
    later = sorted(s for s, sp in firsts.items() if sp not in splits)
    return rows, unmeasured, later, added


def write(rows, unmeasured, later, added, log=sys.stdout):
    cols = ["species", "line", "split", "reading", *ROLES, *(f"{r}_pct" for r in ROLES),
            "standing", "all_round_pct", "niche", "passing", "field"]
    with open(OUT_TSV, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in sorted(rows, key=lambda r: (lp.SPLITS.index(r["split"]), r["species"], r["reading"])):
            cells = [",".join(r[c]) if c == "niche" else ("yes" if r[c] else "") if c == "passing"
                     else str(r[c]) for c in cols]
            f.write("\t".join(cells) + "\n")
    with open(OUT_MD, "w", encoding="utf-8") as out:
        _write_md(out, rows, unmeasured, later, added)
    print(f"wrote {os.path.relpath(OUT_MD, data.ROOT)} and the TSV beside it", file=log)


def _sp(s):
    return lp._sp(s)


def _write_md(out, rows, unmeasured, later, added):
    p = lambda *a: print(*a, file=out)
    by = {(r["species"], r["reading"]): r for r in rows}
    stages = sorted({r["species"] for r in rows}, key=lambda s: (lp.SPLITS.index(by[(s, "today")]["split"]), s))
    none = {reading: {s for s in stages if not by[(s, reading)]["niche"]} for reading in READINGS}
    p("# The niche check\n")
    p(f"Written by `niche.py` (2026-09-28) for Ian's ruling of the same day: every Pokemon should have "
      f"an important niche at the point the player has it, while stronger and weaker lines stay fine. "
      f"Nothing here is in the game data. Each of the {len(stages)} stages the player can own is read in "
      f"the split it is first owned in, at that split's cap, with the moves it can have by then, against "
      f"every trainer Pokemon of that split, by the calculator the scores use. Five roles: offense (the "
      f"mean share of a foe's HP its best move takes), speed (the share of foes it outspeeds), physical "
      f"wall and special wall (of the foes whose best attack on it is of that kind, the share that need "
      f"three or more hits on it while it needs three or fewer on them, since a bulky stage with nothing "
      f"to attack with is no wall) and status (its best status move by Ian's tiers). Each is ranked "
      f"against every stage the player can own by that split; its standing is the mean of its five "
      f"ranks, 0.5 being the split's average. A stage has a niche when one role, or its standing (an "
      f"all-rounder), puts it in the split's top quarter. Two readings: Oxide's lists today, and the "
      f"proposal (the learnset proposal with the later moves placed). `docs/oxide/niche-check.tsv` has "
      f"every stage's numbers.\n")
    held = lambda s: not by[(s, "today")]["passing"]
    p("| Stages without a niche | Held past their first split | Evolve within it |\n|---|---|---|")
    for label, group in (("On both readings", none["today"] & none["proposal"]),
                         ("Today only (the proposal gives one)", none["today"] - none["proposal"]),
                         ("On the proposal only (it takes one away)", none["proposal"] - none["today"])):
        p(f"| {label} | {sum(held(s) for s in group)} | {sum(not held(s) for s in group)} |")
    only = sorted((s for s in stages if by[(s, "proposal")]["niche"] == ["all_round"] and held(s)),
                  key=lambda s: (lp.SPLITS.index(by[(s, "proposal")]["split"]), s))
    if only:
        p(f"\n{len(only)} stages held past their first split have a niche on the proposal only as "
          f"all-rounders, good at much and best at nothing; without that niche they would be findings: "
          + ", ".join(_sp(s) for s in only) + ".")
    for label, group in (("No niche on either reading", none["today"] & none["proposal"]),
                         ("No niche today, one on the proposal", none["today"] - none["proposal"]),
                         ("A niche today, none on the proposal", none["proposal"] - none["today"])):
        if not group:
            continue
        p(f"\n## {label}\n")
        p("Stages the player can evolve within the split they are first owned in are held only briefly; "
          "they are marked. Each role's rank on the proposal, the best first:\n")
        p("| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | "
          "Status | Standing |\n|---|---|---|---|---|---|---|---|---|")
        for s in sorted(group, key=lambda s: (by[(s, "proposal")]["passing"], lp.SPLITS.index(by[(s, "proposal")]["split"]), s)):
            r = by[(s, "proposal")]
            p(f"| {_sp(s)} | {r['split']} | {'yes' if r['passing'] else ''} | {r['offense_pct']:.2f} | "
              f"{r['speed_pct']:.2f} | {r['phys_wall_pct']:.2f} | {r['spec_wall_pct']:.2f} | "
              f"{r['status_pct']:.2f} | {r['standing']:.2f} |")
    want = wanted()
    p("\n## Ian's super-wanted lines\n")
    p("Each stage of the lines, in the split it is first owned in: its standing today and on the proposal "
      "(0.5 is the split's average; Ian wants these a little above it) and its niche roles on the "
      "proposal. A stage the player evolves within its first split is marked.\n")
    p("| Line | Stage | First owned | Evolves within it | Standing today | On the proposal | Niche on the proposal |\n"
      "|---|---|---|---|---|---|---|")
    for s in sorted((s for s in stages if first_stage(s) in want),
                    key=lambda s: (first_stage(s), lp.SPLITS.index(by[(s, "today")]["split"]))):
        t, r = by[(s, "today")], by[(s, "proposal")]
        p(f"| {_sp(first_stage(s))} | {_sp(s)} | {r['split']} | {'yes' if r['passing'] else ''} | "
          f"{t['standing']:.2f} | {r['standing']:.2f} | {', '.join(ROLE_NAMES[n] for n in r['niche']) or 'none'} |")
    missing = sorted(w for w in want if not any(first_stage(s) == w for s in stages))
    if missing:
        p(f"\nSuper-wanted lines with no stage read here (after the story, not in the game yet, or with "
          f"no source): "
          + ", ".join(_sp(w) for w in missing) + ".")
    if unmeasured:
        p(f"\nNot read, since the calculator does not know them: " + ", ".join(_sp(s) for s in unmeasured) + ".")
    if added:
        p(f"\nThe pool places these in no split: a scripted source above its location split's cap (the "
          f"Mining Museum's level 20 fossils in Roark's split) or at a location it does not know "
          f"(Fullmoon Island). This check reads each in the later of its location's split and the first "
          f"split whose cap admits its level: "
          + ", ".join(f"{_sp(s)} ({sp})" for s, sp in sorted(added.items())) + ".")
    if later:
        p(f"\nFirst owned after the League or never on the story's path, so not read: "
          + ", ".join(_sp(s) for s in later) + ".")


def main(argv=None):
    argparse.ArgumentParser(description=__doc__.split("\n")[0]).parse_args(argv)
    write(*run())


if __name__ == "__main__":
    main()
