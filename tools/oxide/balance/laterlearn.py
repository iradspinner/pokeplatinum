"""Generation 5 to 9 level-up moves for Platinum's species (Ian, 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.balance.laterlearn           # the report
    PYTHONPATH=. python3 -m tools.oxide.balance.laterlearn line eevee  # one species

It writes no game data. For each of vanilla Platinum's 493 species that
Oxide keeps obtainable, it lists the moves from Generation 5 on that a later
game (Black and White to Legends Z-A, hg-engine's per-game lists in
~/hg-engine) teaches by level-up and that Oxide's engine runs in full (the
move-pool survey's engine column, or its engine_status for a move no
learnset has yet; a move missing only a doubles effect counts as run, and
Lunar Blessing and Throat Chop, which element 4 will fix, are shown where
they would go but not placed), and proposes each: added, or replacing
a weaker Generation 4 move in the same role at a similar level. Moves a
later game gives only by TM, tutor or egg go on a separate list for the TM
pass.

A proposal starts from the learnset proposal's lists (learnset-proposal.tsv)
and the later game's level (the latest game that teaches it; level 0, on
evolving, is the level the stage is had at), and goes through the
generator's rules (learnplan.py): a strong move no earlier than Kaizo's
level for like moves within its split; on a stage the power flags or the
bar hold, an attack only as an alternative no earlier than its first good
one of that type, and an S or SSS status move never, since Kaizo can give a
later move to no species; the capture rule (a level below where the stage
is had is the relearner's); no weather move; no dead weight; the one-level
rule; setup moves at 1 to 3 PP; and today's own-type rule, which a stronger
same-type move cannot break.
"""
import collections
import csv
import functools
import json
import os
import subprocess
import sys

from . import data, learngen as g, learnplan as lp

HG = os.path.expanduser("~/hg-engine")
GAMES = [("11_bw", "Black and White"), ("12_b2w2", "Black 2 and White 2"), ("13_xy", "X and Y"),
         ("14_oras", "Omega Ruby and Alpha Sapphire"), ("15_sm", "Sun and Moon"),
         ("16_usum", "Ultra Sun and Ultra Moon"), ("17_lgpe", "Let's Go"),
         ("18_swsh", "Sword and Shield"), ("19_bdsp", "Brilliant Diamond and Shining Pearl"),
         ("20_la", "Legends Arceus"), ("21_sv", "Scarlet and Violet"), ("22_za", "Legends Z-A")]
REPLACE_WITHIN = 5          # levels either side for "a similar level"
OUT_MD = os.path.join(data.ROOT, "docs", "oxide", "later-moves-proposal.md")
OUT_TSV = os.path.join(data.ROOT, "docs", "oxide", "later-moves-proposal.tsv")
OUT_TM = os.path.join(data.ROOT, "docs", "oxide", "later-moves-tm.tsv")


@functools.lru_cache(maxsize=None)
def game(key):
    text = subprocess.run(["git", "-C", HG, "show", f"HEAD:data/learnsets/base/{key}.json"],
                          capture_output=True, text=True, check=True).stdout
    return json.loads(text)


def _lines(name):
    with open(os.path.join(data.ROOT, "generated", f"{name}.txt"), encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


@functools.lru_cache(maxsize=None)
def gen4_moves():
    """Platinum's own 467 moves (Pound to Shadow Force)."""
    return frozenset(_lines("moves")[1:468])


@functools.lru_cache(maxsize=None)
def vanilla_species():
    """Platinum's 493 species, in national order."""
    return _lines("species")[1:494]


# Attacks whose record is a plain hit although the real move has a rule the
# engine lacks, found by reading the later moves the survey never covered.
LATER_NOTES = {
    "MOVE_SYNCHRONOISE": "partial: plain 120 hit on any foe; the rule that it hits only "
                         "a foe sharing a type is missing",
}


@functools.lru_cache(maxsize=None)
def engine():
    """{MOVE_X: whether Oxide's engine runs it in full} for every move.

    The move-pool survey's engine column covers only the moves some Oxide
    learnset teaches today, so a later move no learnset has yet is judged
    here by the survey's own engine_status, which reads the effect scripts.
    Its notes list the status moves left on the plain-hit script only among
    the surveyed moves, so the same test is applied to the rest: a status
    move whose effect is a plain hit, and which Oxide's C never names, does
    nothing."""
    from tools.oxide import move_pool_survey as mps
    from tools.oxide.encounters import pokedex
    with open(os.path.join(data.ROOT, "docs", "oxide", "move-pool-survey.csv"), encoding="utf-8") as f:
        out = {r["move"]: r["engine"] for r in csv.DictReader(f)}
    moves = pokedex.moves(data.ROOT)
    in_c = mps.c_special()
    for c, rec in moves.items():
        if c in out:
            continue
        if c in LATER_NOTES:
            out[c] = LATER_NOTES[c]
        elif rec["class"] == "STATUS" and rec["effect"] == "HIT" and c not in in_c:
            out[c] = "partial: status move running the plain-hit script: its effect never happens"
        else:
            out[c] = mps.engine_status({"moves": moves}, c)
    return out


# Moves the engine does not run yet that element 4's follow-up will make work
# (Ian, 2026-09-27). Until it lands they stay out of every list, but the
# report shows where each would go.
ONCE_FIXED = {"MOVE_LUNAR_BLESSING", "MOVE_THROAT_CHOP"}


def placeable(c):
    """True when the move may be placed now: the engine runs it in full, or
    what is missing matters only with a partner on the field (Ian,
    2026-09-27, "Yes, placeable"; Flame Burst's splash is the case)."""
    eng = engine().get(c, "")
    return eng == "runs" or eng.endswith("(doubles only)")


# hg-engine writes the modern names; Oxide keeps Generation 4's. Most differ
# only by an underscore (Thunder Punch), these four by a letter or more.
RENAMED = {"FEINTATTACK": "FAINTATTACK", "HIGHJUMPKICK": "HIJUMPKICK", "VISEGRIP": "VICEGRIP",
           "SMELLINGSALTS": "SMELLINGSALT"}


@functools.lru_cache(maxsize=None)
def _oxide_by_compact():
    return {c[len("MOVE_"):].replace("_", ""): c for c in _lines("moves")}


def oxide_move(hg):
    """Oxide's constant for an hg-engine move constant, or the constant itself."""
    key = hg[len("MOVE_"):].replace("_", "")
    return _oxide_by_compact().get(RENAMED.get(key, key), hg)


def later(species):
    """({MOVE_X: [(game, level)]} by level-up, {MOVE_X: [(game, how)]} by TM,
    tutor or egg only), for moves from Generation 5 on, by Oxide's constants."""
    level, other = collections.defaultdict(list), collections.defaultdict(list)
    for key, name in GAMES:
        rec = game(key).get(species)
        if not rec:
            continue
        for e in rec.get("LevelMoves") or []:
            mv = oxide_move(e["Move"])
            if mv not in gen4_moves() and mv.startswith("MOVE_"):
                level[mv].append((name, e["Level"]))
        for kind, how in (("MachineMoves", "TM"), ("TutorMoves", "tutor"), ("EggMoves", "egg")):
            for mv in rec.get(kind) or []:
                mv = oxide_move(mv["Move"] if isinstance(mv, dict) else mv)
                if mv not in gen4_moves() and str(mv).startswith("MOVE_"):
                    other[mv].append((name, how))
    return dict(level), {m: v for m, v in other.items() if m not in level}


def latest_level(sources):
    """(game, level) from the latest game that teaches the move, passing
    over a level 1 (the relearner's list in the newer games) for the latest
    game that gives it a real level, when one does."""
    real = [(g_, lv) for g_, lv in sources if lv != 1]
    return real[-1] if real else sources[-1]


@functools.lru_cache(maxsize=None)
def proposal_lists():
    """{species: [(level, MOVE_X)]} from the learnset proposal."""
    by_name = {lp.name(c): c for c in lp.M()}
    out = collections.defaultdict(list)
    with open(os.path.join(data.ROOT, "docs", "oxide", "learnset-proposal.tsv"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["level_proposed"] and r["move"] in by_name:
                out[r["species"]].append((int(r["level_proposed"]), by_name[r["move"]]))
    return {s: sorted(v) for s, v in out.items()}


# The stat-raising setup effects (fightsim's SELF_STAGES, by Oxide's effect
# names), which Ian keeps at 1 to 3 PP.
SETUP_EFFECTS = {
    "ATK_UP", "ATK_UP_2", "DEF_UP", "DEF_UP_2", "SPEED_UP_2", "SP_ATK_UP", "SP_ATK_UP_2",
    "SP_DEF_UP_2", "SP_ATK_SP_DEF_UP", "ATK_SPD_UP", "ATK_DEF_UP", "DEF_SPD_UP", "EVA_UP",
    "EVA_UP_2_MINIMIZE", "DEF_UP_DOUBLE_ROLLOUT_POWER", "SP_DEF_UP_DOUBLE_ELECTRIC_POWER",
    "STOCKPILE", "SP_ATK_SP_DEF_SPEED_UP", "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN",
    "ATK_DEF_ACC_UP", "SPEED_UP_2_ATK_UP", "ATK_SP_ATK_UP", "ATK_ACC_UP", "DEF_UP_3",
    "ATK_DEF_SPEED_UP", "TAKE_HEART", "SHELL_SMASH", "QUIVER_DANCE", "COIL", "SHIFT_GEAR",
    "HONE_CLAWS", "WORK_UP", "GROWTH", "MAX_ATK_LOSE_HALF_MAX_HP", "CRIT_UP_2"}


def _setup(const):
    return lp.M()[const].get("effect") in SETUP_EFFECTS


def propose(species):
    """[proposal dict] for the species' later level-up moves."""
    base = proposal_lists().get(species) or lp._now(species)
    have = {c for _lv, c in base}
    types = lp._types(species)
    here = lp.reach(species)
    strong = lp.strong_stage(species)
    taken = collections.Counter(lv for lv, _c in base if lv > 1)
    level_moves, _other = later(species)
    out = []
    for c, sources in sorted(level_moves.items()):
        game_name, raw = latest_level(sources)
        row = {"species": species, "move": c, "games": sources, "game": game_name, "later": raw,
               "action": None, "level": None, "replaces": None, "notable": False, "why": []}
        out.append(row)
        if c not in lp.M():
            row["action"], row["why"] = "left out", ["Oxide has no such move"]
            continue
        if c in have:
            row["action"], row["why"] = "already there", ["the proposal has it"]
            continue
        eng = engine().get(c, "")
        pending = c in ONCE_FIXED
        if pending:
            row["why"].append(f"the engine does not run it yet ({eng}); element 4 will make it work")
        elif not placeable(c):
            row["action"], row["why"] = "left out", [f"the engine does not run it in full ({eng or 'not surveyed'})"]
            continue
        elif eng != "runs":
            row["why"].append(f"placeable, since only its doubles effect is missing ({eng})")
        if c in g.WEATHER_MOVES:
            row["action"], row["why"] = "left out", ["a weather move, which the player never has"]
            continue
        lv = here if raw == 0 else max(1, raw)
        kind, _p = lp.strength(c)
        r = lp.rank(c)
        good = lp.good_attack(c, types)
        strong_move = good or (r or 0) >= lp.STRONG_RANK
        row["notable"] = good or (r or 0) >= 4
        drop = g._dropped(c, species, lv, types)
        if drop:
            row["action"], row["why"] = "left out", [f"dead weight: {drop}"]
            continue
        if kind != "damage" and (r or 0) >= lp.STRONG_RANK:
            row["action"] = "for Ian"
            row["why"].append("an S or SSS status move, which the rules add only where Kaizo gives the "
                              "species the move, and Kaizo gives no species a later move")
            continue
        if strong_move:
            kl = lp.analogue_kaizo_level(species, c)
            if kl and kl <= 78:
                fl = lp.floor_level(kl)
                if fl > lv:
                    row["why"].append(f"{lv} to {fl}: no earlier than Kaizo's level for like moves "
                                      f"({kl}) within its split")
                    lv = fl
        if strong and good:
            first = lp.first_good_of_type(species, lp.M()[c]["type"], base)
            if first is None or lv < first:
                row["action"] = "for Ian"
                row["why"].append("a stage the power flags or the bar hold takes a new attack only "
                                  "no earlier than its first good one of that type")
                continue
        if lv < here:
            # Below where the stage is had: the relearner's, unless a first
            # stage caught at `here` knows it as one of its last four moves.
            known = species not in g.oxide_reached() and c in lp.calc_trainers.default_moves(
                [list(e) for e in sorted(base + [(lv, c)])], here)
            if not known:
                row["action"], row["level"] = "relearner only", lv
                row["why"].append(f"below {here}, where the stage is had: the relearner's")
                if pending:
                    row["why"].append("would be relearner only")
                    row["action"] = "once fixed"
                continue
            row["why"].append(f"known at capture at {here}")
        if lv > 78:
            row["action"], row["why"] = "left out", [f"at {lv}, past 78"]
            continue
        if _setup(c) and (lp.M()[c].get("pp") or 0) > 3:
            row["why"].append(f"a setup move at {lp.M()[c].get('pp')} PP in Oxide's data; Ian's rule is 1 to 3")
        # The same role: a weaker Generation 4 move of the same type and
        # category (or the same effect) at a similar level.
        cands = []
        for blv, bc in base:
            if bc not in gen4_moves() or blv <= 1 or abs(blv - lv) > REPLACE_WITHIN:
                continue
            bk, bp = lp.strength(bc)
            m, bm = lp.M()[c], lp.M()[bc]
            if kind == "damage" and bk == "damage" and m["type"] == bm["type"] and m["class"] == bm["class"] \
                    and bp < lp.strength(c)[1]:
                cands.append((abs(blv - lv), blv, bc))
            elif kind != "damage" and bk != "damage" and m.get("effect") == bm.get("effect"):
                cands.append((abs(blv - lv), blv, bc))
        if cands:
            _d, blv, bc = min(cands)
            row["action"], row["replaces"] = "replaces", bc
            if not pending:
                taken[blv] -= 1          # the weaker move's level is free again
            if not strong_move or blv >= lv:
                lv = blv                 # it takes the weaker move's place
            row["why"].append(f"replaces {lp.name(bc)} at {blv}")
        else:
            row["action"] = "added"
        # The one-level rule, within the split.
        if taken[lv]:
            split = lp._split_of(lv)
            step = [d for k in range(1, 12) for d in ((k, -k) if strong_move else (-k, k))]
            new = next((lv + d for d in step if 2 <= lv + d <= 78 and taken[lv + d] == 0
                        and lp._split_of(lv + d) == split and (not strong_move or lv + d >= lv)), None)
            if new is not None:
                row["why"].append(f"{lv} to {new}: the one-level rule")
                lv = new
        row["level"] = lv
        if pending:
            # Where it would go, holding no level, so nothing else moves for it.
            row["why"].append(f"would be {row['action']}" + (f" {lp.name(row['replaces'])}" if row["replaces"] else ""))
            row["action"] = "once fixed"
            continue
        taken[lv] += 1
    return out


def _own_type_offers(species):
    """[(effective power, level, MOVE_X, game)] the later games offer the
    stage as an attack of its own type of 50 or more, that Oxide runs in
    full and no rule leaves out, weakest first."""
    types = lp._types(species)
    here = lp.reach(species)
    level_moves, _other = later(species)
    out = []
    for c, sources in level_moves.items():
        if c not in lp.M() or not placeable(c) or c in g.WEATHER_MOVES:
            continue
        if not lp._own_type_attack(c, types):
            continue
        game_name, raw = latest_level(sources)
        lv = here if raw == 0 else max(1, raw)
        if g._dropped(c, species, lv, types):
            continue
        out.append((lp.effective_power(c), lv, c, f"{game_name} {raw}"))
    return sorted(out, key=lambda o: (o[0], o[1]))


def gap_fill(species):
    """Ian (2026-09-27): a stage that goes more than one split without an
    attack of its own type, and that the player cannot evolve by the end of
    Gardenia's split, takes one from a later game where one is offered: the
    weakest such attack, at the later game's level if that closes the gap,
    else at the last level that does. On a stage the flags or the bar hold,
    a good attack goes to Ian. None: the stage has no gap to fill."""
    lists = dict(proposal_lists())
    lists[species] = lists.get(species) or lp._now(species)
    if not lp.gap_applies(species) or not lp.breaks_gap(species, lists):
        return None
    here = lp.reach(species)
    i = lp.SPLITS.index(lp._split_of(here))
    window_end = lp.pool.caps()[lp.SPLITS[min(i + 1, len(lp.SPLITS) - 1)]]
    types = lp._types(species)
    offers = _own_type_offers(species)
    row = {"species": species, "here": here, "window_end": window_end, "offers": offers,
           "result": "unfilled", "move": None, "level": None, "game": None}
    if not offers:
        return row
    taken = collections.Counter(lv for lv, _c in lists[species] if lv > 1)
    blocked = []
    for power, lv, c, game_name in offers:
        at = min(max(lv, here), window_end)
        # A good attack keeps the generator's floor: no earlier than Kaizo's
        # level for like moves within its split. Past the window, it cannot
        # fill the gap by the rules.
        if lp.good_attack(c, types):
            kl = lp.analogue_kaizo_level(species, c)
            fl = lp.floor_level(kl) if kl and kl <= 78 else None
            if fl and fl > at:
                if fl > window_end:
                    blocked.append((c, game_name, f"its floor, {fl}, is past {window_end}, the gap's end"))
                    continue
                at = fl
        at = next((x for x in [at] + [at - k for k in range(1, at - here + 1)] if taken[x] == 0), at)
        trial = dict(lists, **{species: sorted(lists[species] + [(at, c)])})
        if lp.breaks_gap(species, trial):
            continue
        # The flags and the bar, on the lists with the move in.
        held = lp.strong_stage(species)
        if not held:
            was = lp.PROPOSED.get(species)
            lp.PROPOSED[species] = trial[species]
            try:
                held = lp.stage_flag(species) is not None or (lp.USE_BAR and lp.passes_bar_proposed(species) is not None)
            finally:
                if was is None:
                    lp.PROPOSED.pop(species, None)
                else:
                    lp.PROPOSED[species] = was
        row.update(move=c, level=at, game=game_name)
        if held and lp.good_attack(c, types):
            row["result"], row["why"] = "for Ian", "a good attack on a stage the flags or the bar hold (with it in)"
        else:
            row["result"] = "filled"
        return row
    if blocked:
        c, game_name, why = blocked[0]
        row.update(move=c, game=game_name, result="for Ian", why=why)
    return row


def pokedex_has(species):
    from ..encounters import pokedex
    return bool(pokedex.load(data.ROOT, species))


def species_list():
    """Platinum's species that Oxide keeps obtainable."""
    ob = g._obtainable()
    return [s for s in vanilla_species() if s in ob]


def _good_by(species, lists, cap):
    """The good attacks and S or SSS status moves the stage has by a level."""
    types = lp._types(species)
    return sorted((lv, lp.name(c)) for c, lv in lp.had_from(species, lists).items()
                  if lv <= cap and (lp.good_attack(c, types) or (lp.rank(c) or 0) >= lp.STRONG_RANK))


def report(log=sys.stdout):
    rows, tm = [], []
    sp = species_list()
    for n, s in enumerate(sp, 1):
        lp.PROPOSED.clear()
        lp.PROPOSED.update(proposal_lists())
        rows += propose(s)
        _lv, other = later(s)
        tm += [(s, c, v) for c, v in sorted(other.items()) if c in lp.M()]
        if n % 50 == 0:
            print(f"  {n} of {len(sp)}", file=log, flush=True)
    with open(OUT_TSV, "w", encoding="utf-8") as f:
        f.write("species\tmove\taction\tlevel\treplaces\tnotable\tlatest_game\tlater_level\tgames\twhy\n")
        for r in rows:
            mv = lp.name(r["move"]) if r["move"] in lp.M() else r["move"]
            f.write(f"{r['species']}\t{mv}\t{r['action']}\t{r['level'] or ''}\t"
                    f"{lp.name(r['replaces']) if r['replaces'] else ''}\t{'yes' if r['notable'] else ''}\t"
                    f"{r['game']}\t{r['later']}\t{'; '.join(f'{a} {b}' for a, b in r['games'])}\t"
                    f"{'; '.join(r['why'])}\n")
    with open(OUT_TM, "w", encoding="utf-8") as f:
        f.write("species\tmove\tengine\tgames\n")
        for s, c, v in tm:
            f.write(f"{s}\t{lp.name(c)}\t{engine().get(c, '')}\t{'; '.join(f'{a} {b}' for a, b in v)}\n")
    # The own-type gaps, over every stage the player can have.
    lp.PROPOSED.clear()
    lp.PROPOSED.update(proposal_lists())
    gap_rows = [r for r in (gap_fill(s) for s in sorted(g._obtainable()) if pokedex_has(s)) if r]
    with open(OUT_MD, "w", encoding="utf-8") as out:
        _write_md(out, sp, rows, tm, gap_rows)
    print(f"wrote {os.path.relpath(OUT_MD, data.ROOT)}, the TSV beside it and later-moves-tm.tsv", file=log)


# The eleven own-type moves the learnset proposal held for Ian (2026-09-27):
# (the stage whose list holds it, the move, its level now, the stages it is for).
HELD = [("SPECIES_ARMAROUGE", "MOVE_LAVA_PLUME", 32, ["SPECIES_ARMAROUGE"]),
        ("SPECIES_BEAUTIFLY", "MOVE_AIR_SLASH", 26, ["SPECIES_BEAUTIFLY"]),
        ("SPECIES_BRIONNE", "MOVE_SCALD", 34, ["SPECIES_BRIONNE"]),
        ("SPECIES_GROVYLE", "MOVE_LEAF_BLADE", 29, ["SPECIES_GROVYLE", "SPECIES_SCEPTILE"]),
        ("SPECIES_HIPPOWDON", "MOVE_EARTHQUAKE", 40, ["SPECIES_HIPPOWDON"]),
        ("SPECIES_LITTEN", "MOVE_FIRE_FANG", 14, ["SPECIES_LITTEN", "SPECIES_TORRACAT"]),
        ("SPECIES_NIDOQUEEN", "MOVE_EARTH_POWER", 43, ["SPECIES_NIDOQUEEN"]),
        ("SPECIES_PIKACHU", "MOVE_THUNDERBOLT", 26, ["SPECIES_PIKACHU"]),
        ("SPECIES_SCIZOR", "MOVE_X_SCISSOR", 41, ["SPECIES_SCIZOR"]),
        ("SPECIES_SCORBUNNY", "MOVE_BLAZE_KICK", 26, ["SPECIES_SCORBUNNY"]),
        ("SPECIES_SKIPLOOM", "MOVE_BULLET_SEED", 20, ["SPECIES_SKIPLOOM", "SPECIES_JUMPLUFF"])]


def _write_md(out, sp, rows, tm, gap_rows=()):
    p = lambda *a: print(*a, file=out)
    lists = proposal_lists()
    p("# Later moves for Platinum's species\n")
    p(f"Written by `laterlearn.py` (2026-09-27) for the Overseer to read before Ian. For each of "
      f"the {len(sp)} of vanilla Platinum's species that Oxide keeps obtainable, the moves from "
      f"Generation 5 on that a later game teaches by level-up (Black and White to Legends Z-A, "
      f"hg-engine's per-game lists), each proposed through the learnset generator's rules on top "
      f"of the learnset proposal. Nothing here is in the game data. "
      f"`docs/oxide/later-moves-proposal.tsv` has every row with the games and the reasons; "
      f"`docs/oxide/later-moves-tm.tsv` has the later moves those games give only by TM, tutor "
      f"or egg, for the TM pass.\n")
    counts = collections.Counter(r["action"] for r in rows)
    left = collections.Counter(r["why"][0].split(" (")[0].split(":")[0] for r in rows if r["action"] == "left out")
    p("| Later level-up moves | Count |\n|---|---|")
    for k in ("added", "replaces", "for Ian", "relearner only", "once fixed", "already there", "left out"):
        p(f"| {lp.cap(k)} | {counts[k]} |")
    p("\nWhy moves are left out:\n\n| Reason | Count |\n|---|---|")
    for why, n in left.most_common():
        p(f"| {lp.cap(why)} | {n} |")
    notable = [r for r in rows if r["notable"] and r["action"] in ("added", "replaces")]
    p(f"\n## The notable adds and replaces, by split\n")
    p(f"{len(notable)} of the adds and replaces are notable: a good attack for the species, or a "
      f"status move Ian's tier list rates A or better. By the split in which the player first has "
      f"the move: its level, or where the stage is first had when it knows the move at capture:\n")
    by_split = collections.defaultdict(list)
    for r in notable:
        by_split[lp._split_of(max(r["level"], lp.reach(r["species"])))].append(r)
    for split in lp.SPLITS + ["Post"]:
        rs = by_split.get(split)
        if not rs:
            continue
        p(f"\n**{split}**\n")
        p("| Stage | Move | Level | Action | From |\n|---|---|---|---|---|")
        for r in sorted(rs, key=lambda r: (r["level"], r["species"])):
            act = "added" if r["action"] == "added" else f"replaces {lp.name(r['replaces'])}"
            if any(w.startswith("known at capture") for w in r["why"]):
                act += f", known at capture at {lp.reach(r['species'])}"
            p(f"| {lp._sp(r['species'])} | {lp.name(r['move'])} | {r['level']} | {act} | "
              f"{r['game']} {r['later']} |")
    p("\n## The lines they touch\n")
    p("Each stage with a notable add or replace: where it is first had, the good attacks and S "
      "or SSS status moves it has by the cap of the split the new move lands in, on the proposal "
      "now and with the later moves.\n")
    by_species = collections.defaultdict(list)
    for r in notable:
        by_species[r["species"]].append(r)
    for s, rs in sorted(by_species.items(), key=lambda kv: min(r["level"] for r in kv[1])):
        cap = max(lp.pool.caps().get(lp._split_of(max(r["level"], lp.reach(s))), 78) for r in rs)
        base = dict(lists)
        base[s] = lists.get(s) or lp._now(s)
        new = list(base[s])
        for r in rs:
            if r["action"] == "replaces":
                new = [e for e in new if e[1] != r["replaces"]]
            new.append((r["level"], r["move"]))
        withl = dict(base, **{s: sorted(new)})
        before, after = _good_by(s, base, cap), _good_by(s, withl, cap)
        gained = [m for m in after if m not in before]
        p(f"- {lp._sp(s)}, had from {lp.reach(s)} ({lp._split_of(lp.reach(s))}), by {cap}: "
          f"{', '.join(f'{n} {lv}' for lv, n in before) or 'nothing strong'}; gains "
          f"{', '.join(f'{n} {lv}' for lv, n in gained) or 'nothing strong by then'}.")
    p("\n## The own-type gaps\n")
    p("Ian's ruling (2026-09-27): a stage the player can evolve by the end of Gardenia's split "
      "is exempt from the own-type rule, since only a player who keeps it back meets its gap. "
      "Every other stage that goes more than one split without an attack of its own type of 50 "
      "or more takes one from a later game where one is offered: the weakest such attack, at the "
      "later game's level if that closes the gap, else at the last level that does. A good attack "
      "on a stage the flags or the bar hold goes to Ian. Over every stage the player can have, not "
      "only Platinum's:\n")
    filled = [r for r in gap_rows if r["result"] == "filled"]
    asked = [r for r in gap_rows if r["result"] == "for Ian"]
    open_ = [r for r in gap_rows if r["result"] == "unfilled"]
    p(f"| Gaps | Stages |\n|---|---|\n| Filled from a later game | {len(filled)} |\n"
      f"| For Ian (the rules would not place the move to fill it) | {len(asked)} |\n"
      f"| Unfilled: no later game offers one | {len(open_)} |\n")
    if filled or asked:
        p("| Stage | Had from | Move | Level | Later game | Result |\n|---|---|---|---|---|---|")
        for r in sorted(filled + asked, key=lambda r: (r["here"], r["species"])):
            res = "filled" if r["result"] == "filled" else f"for Ian: {r.get('why', '')}"
            p(f"| {lp._sp(r['species'])} | {r['here']} | {lp.name(r['move'])} | {r['level'] or ''} | "
              f"{r['game']} | {res} |")
    if open_:
        p(f"\nUnfilled, for Ian: " + ", ".join(f"{lp._sp(r['species'])} (had from {r['here']})"
                                              for r in sorted(open_, key=lambda r: r["species"])) + ".")
    p("\n## The eleven held moves\n")
    p("The learnset proposal held eleven Generation 4 moves for Ian, each the move that would close "
      "a stage's own-type gap but would reach a stage the flags or the bar hold. Beside each, what "
      "the later games offer the same stages as an attack of their own type of 50 or more (Oxide "
      "runs each in full; by effective power, weakest first):\n")
    p("| Held move | For | Exempt now | Later games offer |\n|---|---|---|---|")
    for holder, mv, lv, stages in HELD:
        offers = []
        for s in stages:
            for power, olv, c, game_name in _own_type_offers(s):
                offers.append(f"{lp._sp(s)}: {lp.name(c)} {olv} ({game_name}, {power:.0f})")
        exempt = ", ".join(lp._sp(s) for s in stages if lp.evolves_early(s)) or "none"
        p(f"| {lp.name(mv)} at {lv} ({lp._sp(holder)}) | {', '.join(lp._sp(s) for s in stages)} | {exempt} | "
          f"{'; '.join(offers) or 'nothing'} |")
    fixed = [r for r in rows if r["action"] == "once fixed"
             or (r["move"] in ONCE_FIXED and r["action"] == "for Ian")]
    if fixed:
        p("\n## Placeable once element 4 fixes them\n")
        p("Lunar Blessing and Throat Chop stay out until element 4's follow-up makes them work "
          "(Ian, 2026-09-27). Where the rules would put each, holding no level meanwhile:\n")
        p("| Stage | Move | Level | Would be | Later game |\n|---|---|---|---|---|")
        for r in sorted(fixed, key=lambda r: (r["move"], r["species"])):
            p(f"| {lp._sp(r['species'])} | {lp.name(r['move'])} | {r['level'] or ''} | "
              f"{r['why'][-1].removeprefix('would be ') if r['action'] == 'once fixed' else 'for Ian: ' + r['why'][-1]} | "
              f"{r['game']} {r['later']} |")
    doubles = [r for r in rows if any(w.startswith("placeable, since only its doubles") for w in r["why"])]
    if doubles:
        outcome = collections.Counter(r["action"] for r in doubles)
        p(f"\n{len(doubles)} rows carry a move whose only missing effect is a doubles one, which "
          f"Ian ruled placeable (2026-09-27): "
          + ", ".join(sorted({lp.name(r['move']) for r in doubles})) + ". By outcome: "
          + ", ".join(f"{k} {n}" for k, n in outcome.most_common()) + ".")
    ian = [r for r in rows if r["action"] == "for Ian"]
    p(f"\n## For Ian\n")
    p(f"{len(ian)} later moves the rules do not place on their own:\n")
    p("| Stage | Move | Later game | Why |\n|---|---|---|---|")
    for r in sorted(ian, key=lambda r: (r["species"], r["move"])):
        p(f"| {lp._sp(r['species'])} | {lp.name(r['move'])} | {r['game']} {r['later']} | {r['why'][-1]} |")
    setup = [r for r in rows if any("setup move at" in w for w in r["why"])]
    if setup:
        p(f"\n{len(setup)} proposed setup moves have more than 3 PP in Oxide's data, against Ian's rule "
          f"of 1 to 3: " + ", ".join(sorted({lp.name(r['move']) for r in setup})) + ".")
    p(f"\n## For the TM pass\n")
    moves = collections.Counter(lp.name(c) for _s, c, _v in tm)
    p(f"{len(tm)} rows, {len(moves)} moves: the later moves a later game gives these species only by "
      f"TM, tutor or egg (`docs/oxide/later-moves-tm.tsv`). The most common: "
      + ", ".join(f"{m} ({n})" for m, n in moves.most_common(20)) + ".")


def line(species, out=sys.stdout):
    for row in propose(species):
        src = ", ".join(f"{g_} {l}" for g_, l in row["games"])
        print(f"{lp._sp(species):12} {lp.name(row['move']) if row['move'] in lp.M() else row['move']:18} "
              f"{row['action']:14} {row['level'] or '':>3} {'notable' if row['notable'] else '':8} "
              f"({src}) {'; '.join(row['why'])}", file=out)


def main(argv=None):
    import argparse
    from . import laterlearn as mod
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="report", choices=["report", "line"])
    ap.add_argument("species", nargs="*")
    args = ap.parse_args(argv)
    if args.what == "line":
        for n in args.species:
            mod.line("SPECIES_" + n.upper())
    else:
        mod.report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
