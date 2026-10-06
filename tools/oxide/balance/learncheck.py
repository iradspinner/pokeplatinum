"""The learnset baseline: checks 1, 4, 5 and 6 of docs/oxide/learnset-checks.md,
run on Oxide's level-up lists and on learnset v3's, side by side.

    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck summary   # headline numbers
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck report    # the baseline's tables, Markdown
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck sheets    # writes docs/oxide/learnset-sheets/
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck lines     # the 20 insight lines, five held out

It writes no game data. Only the level-up lists differ between the two
versions: Oxide's are the tree's (res/pokemon/<species>/data.json), and v3's
are the proposal's entries on origin/balance-learngen-v2
(docs/oxide/learnset-proposal.tsv), read with git and never checked out.
Everything else, the catches, evolutions, moves, TMs and tutors, is the
tree's, so a difference between the two columns is the lists' doing.

How the player has a Pokemon (the capture rule, Ian, 2026-09-27). A catch is
one row of pool.catches(): a species, the split it is first offered in, and
the level it comes at (a water slot's lowest). It knows the last four moves
its list gives by that level (the game's own rule, calc_trainers.default_moves:
in list order up to the level, level-0 entries skipped, a move already known
skipped, the oldest dropped once four are full). After capture it learns its
entries above the catch level. It evolves on time: a level evolution at its
level (or the next level-up when caught past it), in the first split whose cap
allows it; an item evolution as soon as the item is in reach (pool's item
census), at the catch level if that is the catch's split, else at the last
split's cap. An evolved stage keeps what it had, learns its own level-0
entries on evolving (v3 has them; Oxide has none yet), and then its entries
from the evolution level on. Anything else on its list, an evolved stage's
level 1 and every entry below the level it is had at, is the relearner's and
counts for nothing (standing rulings). Egg lists are the trainers' palette
only and are never read.
"""
import argparse
import collections
import csv
import functools
import io
import os
import random
import subprocess
import sys

from ..encounters import audit, calc_trainers, locations, model, pokedex, progression, scripted
from . import b6, data, learnstudy as ls, pool, weather_moves

SPLITS = pool.SPLITS            # Roark to League; the post-game has no cap
VERSIONS = ("oxide", "v3")
V3_REF = "origin/balance-learngen-v2"
V3_TSV = "docs/oxide/learnset-proposal.tsv"
V3_TM_SET = "docs/oxide/tm-pass-set.tsv"
SHEETS = os.path.join(data.ROOT, "docs", "oxide", "learnset-sheets")


def si(split):
    """A split's position, the post-game and anything unknown last."""
    return pool.split_index(split)


def caps():
    return pool.caps()


def split_of_level(level):
    """The first split whose cap reaches a level, None past the League's."""
    return next((s for s in SPLITS if level <= caps()[s]), None)


# ---- the moves ---------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def moves():
    return pokedex.moves(data.ROOT)


def move_name(const):
    return moves()[const]["name"]


def _compact(name):
    """Letters and digits only, lower case: the proposal writes some moves the
    Generation 4 way (ThunderShock, Faint Attack), as the tree's names do."""
    return "".join(c for c in name.lower() if c.isalnum())


# A move's downside, as learnset v3 weighs it (learnplan.DOWNSIDE on the v3
# branch): a lock-in and a self-drop count against the move's power.
DOWNSIDE = {"UPROAR": 0.5, "CONTINUE_AND_CONFUSE_SELF": 0.6, "USER_SP_ATK_DOWN_2": 0.8,
            "LOWER_OWN_ATK_AND_DEF": 0.85, "DEF_SPD_DOWN_HIT": 0.9, "SPEED_DOWN_HIT": 0.95}
# Moves that knock the user out: no usable attack in a nuzlocke, where the
# user is then dead.
SELF_KO = {"MOVE_EXPLOSION", "MOVE_SELF_DESTRUCT", "MOVE_MISTY_EXPLOSION", "MOVE_FINAL_GAMBIT",
           "MOVE_MEMENTO", "MOVE_HEALING_WISH", "MOVE_LUNAR_DANCE"}
USABLE_POWER = 50


def effective_power(const):
    """A move's power as v3's own-type rule reads it (learnplan.effective_power):
    the listed power after recoil, a recharge or charging turn and a downside,
    a multi-hit move at its average total, accuracy left out. Fixed-damage,
    variable-power and conditional moves read 0."""
    m = moves()[const]
    kind, per_turn = ls.strength(ls.oxide_move(m))
    if kind != "damage":
        return 0.0
    acc = m.get("accuracy")
    hit = min(acc, 100) / 100 if acc else 1.0
    return per_turn / hit * DOWNSIDE.get(m.get("effect"), 1.0)


def usable(const, types):
    """Check 1's attack: of one of the stage's types, 50 or more by effective
    power, and not one that knocks the user out."""
    return (const in moves() and const not in SELF_KO and moves()[const]["type"] in types
            and effective_power(const) >= USABLE_POWER)


@functools.lru_cache(maxsize=None)
def types_of(species):
    return frozenset((pokedex.load(data.ROOT, species) or {}).get("types") or [])


@functools.lru_cache(maxsize=None)
def species_set():
    return frozenset(pokedex.species_list(data.ROOT))


@functools.lru_cache(maxsize=None)
def species_name(species):
    """The OxiDex's name, except where the game's ten-letter slot shortened it
    (Corviknite, Poltegeist): those take their folder's spelling."""
    rec = pokedex.load(data.ROOT, species)
    folder = species.replace("SPECIES_", "").lower()
    if not rec:
        return folder.replace("_", " ").title()
    name = rec["name"]
    if len(name) >= 10 and len(folder.replace("_", "")) > len(name.replace(" ", "")):
        return folder.replace("_", " ").title()
    return name


# ---- the two versions' lists --------------------------------------------------

def _git_show(rel):
    out = subprocess.run(["git", "-C", data.ROOT, "show", f"{V3_REF}:{rel}"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"cannot read {rel} on {V3_REF}: {out.stderr.strip()}"
                         f" (run git fetch origin balance-learngen-v2)")
    return out.stdout


@functools.lru_cache(maxsize=None)
def _by_compact_name():
    """{compact move name: MOVE_X}, for names that name one move only (the
    Z-moves' physical and special halves share a name, and no list holds them)."""
    seen = collections.defaultdict(set)
    for const, m in moves().items():
        seen[_compact(m["name"])].add(const)
    return {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}


@functools.lru_cache(maxsize=None)
def v3_lists():
    """{species: ((level, MOVE_X), ...)} from the proposal: every entry it keeps
    at its proposed level, dropped ones left out, in the proposal's order
    sorted by level (a stable sort keeps the order within a level, which is
    the order the game reads them in). The scoring track's build_v3.py reads
    the same file the same way."""
    names = _by_compact_name()
    out = collections.defaultdict(list)
    unknown = collections.Counter()
    for row in csv.DictReader(io.StringIO(_git_show(V3_TSV)), delimiter="\t"):
        if row["change"] == "dropped" or not row["level_proposed"]:
            continue
        const = names.get(_compact(row["move"]))
        if const is None:
            unknown[row["move"]] += 1
            continue
        out[row["species"]].append((int(row["level_proposed"]), const))
    if unknown:
        raise SystemExit(f"v3 names moves the tree lacks: {dict(unknown)}")
    return {sp: tuple(sorted(lst, key=lambda e: e[0])) for sp, lst in out.items()}


@functools.lru_cache(maxsize=None)
def learnset(version, species):
    """((level, MOVE_X), ...) in the game's order."""
    if version == "v3":
        return v3_lists().get(species, ())
    return tuple(tuple(e) for e in (pokedex.load(data.ROOT, species) or {}).get("learnset", []))


def at_capture(version, species, level):
    """The four moves a Pokemon caught at `level` knows: the game's rule."""
    return calc_trainers.default_moves(list(learnset(version, species)), level)


# ---- where each Pokemon is caught ---------------------------------------------

@functools.lru_cache(maxsize=None)
def catch_rows():
    """((species, split, level, how, place), ...): pool.catches() row for row,
    with the capture area each comes from (the encounter tool's location name,
    "Honey trees", or a scripted source's location). test_learncheck checks
    that the rows are pool's."""
    sidecar = model.load_sidecar() or {}
    area_split = progression.split_of(sidecar)
    entries = sidecar.get("areas") or {}
    out = []

    def offer(species, split, level, how, place):
        if split in SPLITS:
            out.append((species, split, level, how, place))

    for area in model.load_all():
        split = area_split.get(area.name)
        if not split:
            continue
        place = locations.location(area.name) or area.name
        if area.land_active:
            slots = area.slots
            for sp, lv in slots:
                offer(sp, split, lv, "wild", place)
            for key in ("day", "night"):
                for j, sp in enumerate(area.data.get(key) or []):
                    if sp and sp != "SPECIES_NONE":
                        offer(sp, split, slots[2 + min(j, 1)][1], "wild", place)
        water = (entries.get(area.name) or {}).get("water_split") or split
        for kind in ("surf", "old_rod", "good_rod", "super_rod"):
            if not area.kind_rate(kind):
                continue
            arrives = pool.later(water, progression.rod_split(sidecar, kind))
            for sp, lo, _hi in area.kind_slots(kind):
                if sp != "SPECIES_NONE":
                    offer(sp, arrives, lo, kind, place)
    for table in model.honey_tree_tables():
        for key in (*model.HONEY_TREE_KEYS, "rare"):
            for sp in table.get(key) or []:
                offer(sp, table.get("split") or pool.HONEY_SPLIT, table.get("level_min") or 1,
                      "honey", "Honey trees")
    locs = pool._location_splits()
    from_file = set()
    with open(pool.SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["method"].startswith("great marsh daily"):
                continue
            split = locs.get(row["location"])
            level = pool._source_level(row["level"])
            if split and caps().get(split) and level <= caps()[split]:
                offer(row["species"], split, level, row["method"], row["location"])
                from_file.add(row["species"])
    # pool._tool_sources, with each source's capture area kept.
    live = {d["species"] for d in audit.pool_draws(data.ROOT)}
    for src in scripted.load(data.ROOT):
        if src["kind"] == "egg" or src.get("planned") or src.get("split") not in SPLITS \
                or not isinstance(src.get("level"), int):
            continue
        for species in src.get("pool") or []:
            if (src["pick"] != "legendary_pool" or species in live) and species not in from_file:
                offer(species, src["split"], src["level"], src["kind"],
                      src.get("capture_area") or src.get("label") or src["id"])
    return tuple(out)


# ---- what the player has, stage by stage ------------------------------------------

# One stage as the player first has it on one route. via: "caught", "level"
# for a level evolution, or the item an item evolution needs. brought: the
# moves it has then, each with where it came from ("capture", "carried" from
# the pre-evolution, "evolving" for a level-0 entry); own: the level-up entries
# it can still learn, (level, MOVE_X).
Stage = collections.namedtuple("Stage", "species split level via brought own")


def _evolution(version, parent, target):
    """The Stage `target` is first had as from `parent`, evolved on time, or
    None if no evolution to it opens by the League's cap."""
    pi = si(parent.split)
    best = None
    for need, item, into in pool.evolutions(parent.species):
        if into != target:
            continue
        if item:
            first = pool.evolution_items_first().get(item)
            if first not in SPLITS:
                continue
            ti = max(pi, si(first))
            level = parent.level if ti == pi else max(parent.level, caps()[SPLITS[ti - 1]])
        else:
            level = max(need, parent.level + 1)
            ti = next((i for i in range(pi, len(SPLITS)) if caps()[SPLITS[i]] >= level), None)
            if ti is None:
                continue
        if best is None or (ti, level) < best[:2]:
            best = (ti, level, item or "level")
    if best is None:
        return None
    ti, level, via = best
    carried = {m: "carried" for m, _o in parent.brought}
    carried.update({m: "carried" for lv, m in parent.own if lv <= level})
    lst = learnset(version, target)
    for lv, m in lst:
        if lv == 0:
            carried.setdefault(m, "evolving")
    own = tuple((lv, m) for lv, m in lst if lv >= max(level, 2))
    return Stage(target, SPLITS[ti], level, via, tuple(carried.items()), own)


def caught_stage(version, species, split, level):
    return Stage(species, split, level, "caught",
                 tuple((m, "capture") for m in at_capture(version, species, level)),
                 tuple((lv, m) for lv, m in learnset(version, species) if lv > level))


@functools.lru_cache(maxsize=None)
def branches(version, species, split, level):
    """((Stage, ...), ...): one path of stages for each branch of the line
    from a catch, each stage as first had, up to where no further evolution
    opens by the League's cap."""
    out = []

    def walk(path):
        kids, seen = [], set()
        for _need, _item, target in pool.evolutions(path[-1].species):
            if target in seen or any(s.species == target for s in path):
                continue
            seen.add(target)
            child = _evolution(version, path[-1], target)
            if child:
                kids.append(child)
        if not kids:
            out.append(tuple(path))
        for k in kids:
            walk(path + [k])
    walk([caught_stage(version, species, split, level)])
    return tuple(out)


@functools.lru_cache(maxsize=None)
def stage_routes(version):
    """{species: ((Stage, catch row), ...)}: every way each stage is first had,
    over every catch and branch, duplicates once."""
    out = collections.defaultdict(dict)
    for row in catch_rows():
        sp, split, level, _how, _place = row
        if sp not in species_set():
            continue        # the sources file's Day Care egg names no species
        for path in branches(version, sp, split, level):
            for st in path:
                out[st.species].setdefault(st, row)
    return {sp: tuple(d.items()) for sp, d in out.items()}


@functools.lru_cache(maxsize=None)
def family(species):
    """The line's first stage."""
    chain = pool.pre_evolutions().get(species) or []
    return chain[-1] if chain else species


# ---- check 1: a usable attack of its own type by the split's cap --------------------

def first_usable(stage):
    """(split index, level, MOVE_X, how) of the stage's first usable attack of
    its own type, or None by the League's cap."""
    types = types_of(stage.species)
    best = None
    here = si(stage.split)
    for m, origin in stage.brought:
        if usable(m, types):
            cand = (here, stage.level, m, origin)
            best = cand if best is None or cand < best else best
    for lv, m in stage.own:
        split = split_of_level(lv)
        if split and usable(m, types):
            cand = (max(here, si(split)), lv, m, "level-up")
            best = cand if best is None or cand < best else best
    return best


def evolves_early(species):
    """Whether the player can evolve the stage by the end of Gardenia's split
    (Ian, 2026-09-27): its gap bites only a player who keeps it back."""
    return any(pool.reachable(need, item, "Gardenia") for need, item, _t in pool.evolutions(species))


@functools.lru_cache(maxsize=None)
def _machine_splits():
    """{MOVE_X: (first split, label)} over the TMs and HMs in reach, by the
    tree's placements, which the TM pass has not yet redone."""
    machines = pokedex.machines(data.ROOT)
    out = {}
    for item, split in pool._items_first().items():
        label = item.replace("ITEM_", "")
        if label in machines and split in SPLITS:
            mv = machines[label]
            if mv not in out or si(split) < si(out[mv][0]):
                out[mv] = (split, label)
    return out


def tm_rescue(species):
    """(split, label, MOVE_X) of the earliest TM, HM or tutor that gives the
    stage a usable attack of its own type, or None."""
    rec = pokedex.load(data.ROOT, species) or {}
    machines = pokedex.machines(data.ROOT)
    types = types_of(species)
    cands = []
    for label in rec.get("by_tm") or []:
        mv = machines.get(label)
        if mv and usable(mv, types) and mv in _machine_splits():
            cands.append((si(_machine_splits()[mv][0]), _machine_splits()[mv][0], label, mv))
    tutors = pool._tutor_splits()
    for mv in rec.get("by_tutor") or []:
        if usable(mv, types) and mv in tutors:
            cands.append((si(tutors[mv]), tutors[mv], "tutor", mv))
    return min(cands)[1:] if cands else None


@functools.lru_cache(maxsize=None)
def check1(version):
    """{species: result} for every stage the player can have by the League's
    cap. A result says the split the stage is first had in, on which route, its
    first usable attack of its own type, the gap in splits between them (None
    for never by the League's cap), whether it is exempt, and the verdict:
    "pass" (the gap is a split or less), "fail" (two or more, or never), or
    "exempt" (it can evolve by the end of Gardenia's split). Where several
    routes first have the stage in the same split, the best of them counts."""
    owned = b6.obtainable()
    out = {}
    for sp, routes in stage_routes(version).items():
        if sp not in owned:
            continue
        first = min(si(st.split) for st, _row in routes)
        best = None
        for st, row in routes:
            if si(st.split) != first:
                continue
            fu = first_usable(st)
            gap = None if fu is None else fu[0] - first
            key = (99 if gap is None else gap, st.level)
            if best is None or key < best[0]:
                best = (key, st, row, fu, gap)
        _key, st, row, fu, gap = best
        exempt = evolves_early(sp)
        verdict = "exempt" if exempt else ("pass" if gap is not None and gap <= 1 else "fail")
        out[sp] = {"species": sp, "family": family(sp), "split": SPLITS[first], "stage": st,
                   "route": row, "first": fu, "gap": gap, "exempt": exempt, "verdict": verdict,
                   "tm": tm_rescue(sp) if verdict == "fail" else None}
    return out


def check1_counts(version):
    res = check1(version).values()
    c = collections.Counter(r["verdict"] for r in res)
    never = sum(1 for r in res if r["verdict"] == "fail" and r["gap"] is None)
    fam_fail = {r["family"] for r in res if r["verdict"] == "fail"}
    fams = {r["family"] for r in res}
    tm = sum(1 for r in res if r["verdict"] == "fail" and r["tm"]
             and si(r["tm"][0]) <= si(r["split"]) + 1)
    return {"stages": len(res), "pass": c["pass"], "fail": c["fail"], "never": never,
            "exempt": c["exempt"], "lines": len(fams), "lines_failing": len(fam_fail),
            "tm_closes": tm}


@functools.lru_cache(maxsize=None)
def bare_captures(version):
    """{species: (split, level, place, moves at capture)}: the species some catch
    of which knows no attack at all at capture (no move, or status moves only),
    each at its earliest such catch. A Pokemon caught with no move cannot act."""
    out = {}
    for sp, split, level, _how, place in catch_rows():
        if sp not in species_set():
            continue
        known = at_capture(version, sp, level)
        if any(moves()[m]["class"] != "STATUS" for m in known if m in moves()):
            continue
        cand = (si(split), level, place, tuple(known))
        if sp not in out or cand < (si(out[sp][0]),) + out[sp][1:]:
            out[sp] = (split, level, place, tuple(known))
    return out


# ---- check 4: early run-enders on the player's side ---------------------------------

# Fixed damage (Dragon Rage, Sonic Boom) and damage by level (Night Shade,
# Seismic Toss, Psywave), read by their effects so a renamed or new move with
# the same effect is caught too.
RUN_ENDER_EFFECTS = {"40_DAMAGE_FLAT", "20_DAMAGE_FLAT", "LEVEL_DAMAGE_FLAT",
                     "RANDOM_DAMAGE_1_TO_150_LEVEL"}
OHKO_EFFECTS = {"ONE_HIT_KO"}
EARLY_UNTIL = "Gardenia"
# Ian's rulings on one move: the split it must be learnt after.
RULED_OUT = {("SPECIES_CHARMANDER", "MOVE_DRAGON_RAGE"): "Roark"}


def run_ender(const):
    return const in moves() and moves()[const]["effect"] in RUN_ENDER_EFFECTS


def ohko(const):
    return const in moves() and moves()[const]["effect"] in OHKO_EFFECTS


@functools.lru_cache(maxsize=None)
def check4_early(version, until=EARLY_UNTIL):
    """{(species, MOVE_X): (split, level, how)}: every fixed or level damage
    move a stage the player can have by the end of a split (Gardenia's, the
    check's) knows or learns by level-up by then, at its earliest. A move an
    evolved stage carries from its pre-evolution is counted on the
    pre-evolution."""
    owned = b6.obtainable()
    limit = si(until)
    cap = caps()[until]
    found = {}

    def note(sp, mv, split, level, how):
        key = (sp, mv)
        cand = (si(split), level, how)
        if key not in found or cand < (si(found[key][0]), found[key][1], found[key][2]):
            found[key] = (split, level, how)

    for sp, routes in stage_routes(version).items():
        if sp not in owned:
            continue
        for st, _row in routes:
            if si(st.split) > limit:
                continue
            for mv, origin in st.brought:
                if run_ender(mv) and origin in ("capture", "evolving"):
                    note(sp, mv, st.split, st.level,
                         "known at capture" if origin == "capture" else "on evolving")
            for lv, mv in st.own:
                if lv <= cap and run_ender(mv):
                    note(sp, mv, SPLITS[max(si(st.split), si(split_of_level(lv)))], lv, "level-up")
    return found


def check4_machines():
    """[(species, label, MOVE_X, split)]: fixed or level damage by TM, HM or
    tutor that a stage had by the end of Gardenia's split can take by then.
    Lists are the tree's, the same in both versions."""
    owned = b6.obtainable()
    machines = pokedex.machines(data.ROOT)
    tutors = pool._tutor_splits()
    had = {sp for sp, r in check1("oxide").items() if si(r["split"]) <= si(EARLY_UNTIL)}
    out = []
    for sp in sorted(had & owned):
        rec = pokedex.load(data.ROOT, sp) or {}
        for label in rec.get("by_tm") or []:
            mv = machines.get(label)
            if mv and run_ender(mv) and mv in _machine_splits() \
                    and si(_machine_splits()[mv][0]) <= si(EARLY_UNTIL):
                out.append((sp, label, mv, _machine_splits()[mv][0]))
        for mv in rec.get("by_tutor") or []:
            if run_ender(mv) and mv in tutors and si(tutors[mv]) <= si(EARLY_UNTIL):
                out.append((sp, "tutor", mv, tutors[mv]))
    return out


def ruling_state(species, move, split):
    """For a move Ian ruled out of a split: "broken" while it is still learnt
    in or before that split, "met" once it is later; None for the rest."""
    ruled = RULED_OUT.get((species, move))
    if not ruled:
        return None
    return "broken" if si(split) <= si(ruled) else "met"


@functools.lru_cache(maxsize=None)
def check4_ohko(version):
    """[(species, MOVE_X, how)]: every one-hit KO move on a list of a species
    the player can own, with how the player gets it: by level-up at a level
    and split, as the relearner's only, or by TM, HM or tutor."""
    owned = b6.obtainable()
    machines = pokedex.machines(data.ROOT)
    routes = stage_routes(version)
    out = []
    for sp in sorted(owned):
        learnt = {}
        for st, _row in routes.get(sp, ()):
            for mv, origin in st.brought:
                if ohko(mv) and origin != "carried":
                    learnt.setdefault(mv, (si(st.split), st.level, st.split))
            for lv, mv in st.own:
                if ohko(mv):
                    split = split_of_level(lv) or "Post"
                    cand = (max(si(st.split), si(split)), lv, split)
                    if mv not in learnt or cand < learnt[mv]:
                        learnt[mv] = cand
        for lv, mv in learnset(version, sp):
            if ohko(mv) and mv not in learnt:
                learnt[mv] = None
        for mv, at in sorted(learnt.items()):
            how = f"level-up at {at[1]} ({at[2]})" if at else (
                "the relearner's only" if sp in routes else "level-up, post-game only")
            out.append((sp, mv, how))
        rec = pokedex.load(data.ROOT, sp) or {}
        for label in rec.get("by_tm") or []:
            if ohko(machines.get(label)):
                out.append((sp, machines[label], label))
        for mv in rec.get("by_tutor") or []:
            if ohko(mv):
                out.append((sp, mv, "tutor"))
    return out


# ---- check 5: Ian's standing move rules, as a lint ----------------------------------

# Stat-raising setup: a status move whose effect raises the user's own stats
# (or critical-hit stage), read by effect, plus the few whose effect the
# tree spells another way.
SETUP_EFFECTS = {
    "ATK_ACC_UP", "ATK_DEF_ACC_UP", "ATK_DEF_SPEED_UP", "ATK_DEF_UP", "ATK_SPD_UP",
    "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN", "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP",
    "ATK_SP_ATK_UP", "ATK_UP", "ATK_UP_2", "AUTOTOMIZE", "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2",
    "CRIT_UP_2", "CURSE", "DEF_SPD_UP", "DEF_UP", "DEF_UP_2", "DEF_UP_3",
    "DEF_UP_DOUBLE_ROLLOUT_POWER", "EVA_UP", "EVA_UP_2_MINIMIZE", "MAX_ATK_LOSE_HALF_MAX_HP",
    "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP", "RANDOM_STAT_UP_2", "SPEED_UP_2", "SPEED_UP_2_ATK_UP",
    "SP_ATK_SP_DEF_SPEED_UP", "SP_ATK_SP_DEF_UP", "SP_ATK_UP", "SP_ATK_UP_2", "SP_DEF_UP_2",
    "SP_DEF_UP_DOUBLE_ELECTRIC_POWER", "STOCKPILE", "STUFF_CHEEKS", "TIDY_UP"}
SETUP_BY_NAME = {"MOVE_NO_RETREAT", "MOVE_EXTREME_EVOBOOST", "MOVE_TAKE_HEART"}
# Moves that raise stats but not plainly the user's own in a single battle:
# reported, not judged.
SETUP_BORDERLINE = {"MOVE_COACHING", "MOVE_GEAR_UP", "MOVE_DRAGON_CHEER", "MOVE_PSYCH_UP",
                    "MOVE_LASER_FOCUS", "MOVE_DECORATE", "MOVE_MAGNETIC_FLUX", "MOVE_AROMATIC_MIST",
                    "MOVE_FLOWER_SHIELD", "MOVE_ROTOTILLER"}
SETUP_PP = (1, 3)

# Stat-lowering status moves (Ian, 2026-10-02): 3 to 6 PP, Sweet Scent 2,
# Defog 1, Memento as it is.
LOWERING_EFFECTS = {"ACC_DOWN", "ATK_DEF_DOWN", "ATK_DOWN", "ATK_DOWN_2", "DEF_DOWN", "DEF_DOWN_2",
                    "SPEED_DOWN", "SPEED_DOWN_2", "SP_ATK_DOWN", "SP_ATK_DOWN_2",
                    "SP_ATK_DOWN_2_OPPOSITE_GENDER", "SP_DEF_DOWN_2", "TEARFUL_LOOK",
                    "VENOM_DRENCH", "EVA_DOWN", "REMOVE_HAZARDS_SCREENS_EVA_DOWN"}
LOWERING_PP = (3, 6)
LOWERING_EXACT = {"MOVE_SWEET_SCENT": 2, "MOVE_DEFOG": 1}
LOWERING_AS_IS = {"MOVE_MEMENTO"}
# Status moves that lower a stat beside doing something else: reported, not judged.
LOWERING_BORDERLINE = {"MOVE_PARTING_SHOT", "MOVE_STRENGTH_SAP", "MOVE_TOXIC_THREAD",
                       "MOVE_OCTOLOCK", "MOVE_TAR_SHOT", "MOVE_SPICY_EXTRACT", "MOVE_SWAGGER",
                       "MOVE_FLATTER"}

# Generation 4's accuracy, which is vanilla Platinum's (the main branch).
GEN4_ACCURACY = ("MOVE_SPORE", "MOVE_SLEEP_POWDER", "MOVE_HYPNOSIS", "MOVE_SING",
                 "MOVE_GRASS_WHISTLE", "MOVE_LOVELY_KISS", "MOVE_DARK_VOID", "MOVE_YAWN",
                 "MOVE_STUN_SPORE", "MOVE_POISON_POWDER", "MOVE_THUNDER_WAVE", "MOVE_SWAGGER")
VANILLA_REF = "main"

# Ian's removed TMs (2026-09-28).
REMOVED_TMS = ("MOVE_PROTECT", "MOVE_DOUBLE_TEAM", "MOVE_RAIN_DANCE", "MOVE_SUNNY_DAY",
               "MOVE_SANDSTORM", "MOVE_HAIL", "MOVE_THIEF", "MOVE_SNATCH", "MOVE_SKILL_SWAP",
               "MOVE_FOCUS_PUNCH", "MOVE_SUBSTITUTE", "MOVE_DREAM_EATER", "MOVE_SWORDS_DANCE",
               "MOVE_EMBARGO")
# The rows of the TM pass draft that are in its set of TMs.
V3_TM_IN_SET = {"kept", "new", "reliable-status group"}


def setup_moves():
    return sorted(c for c, m in moves().items() if m["class"] == "STATUS"
                  and (m["effect"] in SETUP_EFFECTS or c in SETUP_BY_NAME)
                  and c not in SETUP_BORDERLINE)


def lowering_moves():
    return sorted(c for c, m in moves().items() if m["class"] == "STATUS"
                  and m["effect"] in LOWERING_EFFECTS)


def lint_pp():
    """{"setup": [(MOVE_X, pp, ok)], "lowering": [(MOVE_X, pp, ok, rule)],
    "borderline": [(MOVE_X, pp)]}. Move data, the same in both versions."""
    setup = [(c, moves()[c]["pp"], SETUP_PP[0] <= moves()[c]["pp"] <= SETUP_PP[1])
             for c in setup_moves()]
    lowering = []
    for c in lowering_moves():
        pp = moves()[c]["pp"]
        if c in LOWERING_EXACT:
            lowering.append((c, pp, pp == LOWERING_EXACT[c], f"exactly {LOWERING_EXACT[c]}"))
        else:
            lowering.append((c, pp, LOWERING_PP[0] <= pp <= LOWERING_PP[1], "3 to 6"))
    for c in LOWERING_AS_IS:
        lowering.append((c, moves()[c]["pp"], True, "as it is"))
    border = [(c, moves()[c]["pp"]) for c in sorted(SETUP_BORDERLINE | LOWERING_BORDERLINE)
              if c in moves()]
    return {"setup": setup, "lowering": lowering, "borderline": border}


def lint_accuracy():
    """[(MOVE_X, accuracy now, vanilla's, ok)]."""
    van = pokedex.vanilla_moves(data.ROOT, VANILLA_REF)
    out = []
    for c in GEN4_ACCURACY:
        now, was = moves()[c]["accuracy"], (van.get(c) or {}).get("accuracy")
        out.append((c, now, was, now == was))
    return out


@functools.lru_cache(maxsize=None)
def lint_weather(version):
    """{"moves": [(species, where, MOVE_X)], "abilities": [(species, ABILITY)]}
    for every species the player can own: a weather move on its level-up, TM
    or tutor list, and a weather ability in a regular slot."""
    owned = b6.obtainable()
    machines = pokedex.machines(data.ROOT)
    found, abilities = [], []
    for sp in sorted(owned):
        rec = pokedex.load(data.ROOT, sp) or {}
        for lv, mv in learnset(version, sp):
            if mv in weather_moves.WEATHER_MOVES:
                found.append((sp, f"level {lv}", mv))
        for label in rec.get("by_tm") or []:
            if machines.get(label) in weather_moves.WEATHER_MOVES:
                found.append((sp, label, machines[label]))
        for mv in rec.get("by_tutor") or []:
            if mv in weather_moves.WEATHER_MOVES:
                found.append((sp, "tutor", mv))
        abilities += [(sp, a) for a in pokedex.weather_abilities(data.ROOT, sp)]
    return {"moves": found, "abilities": abilities}


@functools.lru_cache(maxsize=None)
def lint_tms(version):
    """[(label, MOVE_X)] of Ian's removed TMs still on the TM list: the tree's
    machines for Oxide, the TM pass draft's set on the v3 branch for v3."""
    if version == "oxide":
        return sorted((label, mv) for label, mv in pokedex.machines(data.ROOT).items()
                      if mv in REMOVED_TMS)
    names = _by_compact_name()
    out = []
    for row in csv.DictReader(io.StringIO(_git_show(V3_TM_SET)), delimiter="\t"):
        mv = names.get(_compact(row["move"]))
        if row["status"] in V3_TM_IN_SET and mv in REMOVED_TMS:
            out.append((row["status"], mv))
    return sorted(out)


def v3_tm_set_size():
    return sum(1 for row in csv.DictReader(io.StringIO(_git_show(V3_TM_SET)), delimiter="\t")
               if row["status"] in V3_TM_IN_SET)


# ---- check 6: the sheets, one per split ----------------------------------------------

def _stage_at(path, split):
    """The stages of one branch the player has by a split's cap."""
    return [st for st in path if si(st.split) <= si(split)]


def sheet_entry(version, species, split, level):
    """[(stages had by the cap, known at capture, [(stage, level, MOVE_X)]
    learnt by level-up by the cap, [the next stages after the cap])]: one per
    distinct way the branches run up to the cap."""
    cap = caps()[split]
    seen, out = {}, []
    for path in branches(version, species, split, level):
        had = _stage_at(path, split)
        key = tuple(st.species for st in had)
        following = path[len(had)] if len(had) < len(path) else None
        if key in seen:
            if following and following not in out[seen[key]][3]:
                out[seen[key]][3].append(following)
            continue
        seen[key] = len(out)
        learnt = []
        for i, st in enumerate(had):
            if i:
                learnt += [(st.species, "evolving", mv) for mv, o in st.brought if o == "evolving"]
            nxt = had[i + 1].level if i + 1 < len(had) else None
            for lv, mv in st.own:
                # A stage stops learning its own list once it evolves on time.
                if lv <= cap and (nxt is None or lv <= nxt):
                    learnt.append((st.species, lv, mv))
        out.append((had, at_capture(version, species, level), learnt, [following] if following else []))
    return out


def _fmt_learnt(learnt, first):
    """'Ember 9, Dragon Rage 16; as Charmeleon: Scary Face 19'."""
    parts, cur, words = [], first, []
    for stage, lv, mv in learnt:
        if stage != cur:
            if words or parts:
                parts.append(", ".join(words) if words else "nothing")
            cur, words = stage, []
            parts.append(f"as {species_name(stage)}:")
        words.append(f"{move_name(mv)} {'on evolving' if lv == 'evolving' else lv}")
    if words:
        parts.append(", ".join(words))
    text = " ".join(p if p.endswith(":") else p + ";" for p in parts).rstrip(";")
    return text.replace(":;", ":") or "nothing"


def _fmt_stage(had, following):
    last = had[-1]
    text = species_name(last.species)
    if len(had) > 1:
        text += f" (from {last.level})"
    if following:
        text += "; " + ", ".join(f"{species_name(f.species)} in {f.split}"
                                 for f in sorted(following, key=lambda f: (si(f.split), f.species)))
    return text


def sheet_rows(split):
    """{place: [row]} for one split's sheet. A row: Pokemon, how, levels, and
    for each version its moves at capture, its moves learnt by the cap and its
    stage at the cap."""
    by_place = collections.defaultdict(lambda: collections.defaultdict(list))
    for sp, s, level, how, place in catch_rows():
        if s == split and sp in species_set():
            by_place[place][(sp, how)].append(level)
    out = {}
    for place, catches in by_place.items():
        rows = []
        for (sp, how), levels in sorted(catches.items(), key=lambda kv: (min(kv[1]), kv[0])):
            lo, hi = min(levels), max(levels)
            cells = {}
            for version in VERSIONS:
                cells[version] = [(", ".join(move_name(m) for m in cap) or "nothing",
                                   _fmt_learnt(learnt, sp), _fmt_stage(had, nxt))
                                  for had, cap, learnt, nxt in sheet_entry(version, sp, split, lo)]
            rows.append({"species": sp, "how": how, "levels": (lo, hi), "cells": cells})
        out[place] = rows
    return out


def _cell(text):
    return text.replace("|", "/")


def write_sheets():
    os.makedirs(SHEETS, exist_ok=True)
    written = []
    for split in SPLITS:
        cap = caps()[split]
        rows = sheet_rows(split)
        lines = [f"# {split}'s split: what each catch knows and learns", "",
                 f"Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset "
                 f"baseline (`docs/oxide/learnset-checks.md`). One table per capture area first "
                 f"offered in {split}'s split, whose cap is {cap}. Each Pokemon is read at the lowest "
                 f"level it is found at there. \"Knows at capture\" is the last four moves its list "
                 f"gives by that level; \"learns by level-up\" is every entry it reaches after capture "
                 f"up to {cap}, evolving on time, with each later stage's moves under its name; "
                 f"\"at the cap\" is the stage it can be by then and the next one after. A row "
                 f"marked v3 shows learnset v3 (unlanded, `{V3_REF}`) where it differs from "
                 f"Oxide's lists; a row marked both is the same in each. Relearner-only moves and "
                 f"egg moves are left out. Nothing here is in the game data.", ""]
        for place in sorted(rows, key=lambda p: (p == "Honey trees", p)):
            lines += [f"## {place}", "",
                      "| Pokemon | Found as | Level | Lists | Knows at capture | "
                      f"Learns by level-up by {cap} | At the cap |",
                      "|---|---|---|---|---|---|---|"]
            for r in rows[place]:
                lo, hi = r["levels"]
                lv = str(lo) if lo == hi else f"{lo} to {hi}"
                ox, v3 = r["cells"]["oxide"], r["cells"]["v3"]
                variants = [("both", c) for c in ox] if ox == v3 else \
                    [("Oxide", c) for c in ox] + [("v3", c) for c in v3]
                for label, (cap_moves, learnt, stage) in variants:
                    lines.append(f"| {species_name(r['species'])} | {_cell(r['how'].replace('_', ' '))} | {lv} | {label} | "
                                 f"{_cell(cap_moves)} | {_cell(learnt)} | {_cell(stage)} |")
            lines.append("")
        path = os.path.join(SHEETS, f"{split.lower()}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))
        written.append(path)
    return written


# ---- the 20 lines for Ian's insight sessions ------------------------------------------

# Chosen from the baseline's results (docs/oxide/learnset-baseline.md gives
# each one's reason), each by its first stage, in the split each line is first
# caught in. The draw below takes the five held out from this order, so the
# order is part of the seal; it was fixed before the draw was first run.
INSIGHT_LINES = (
    "SPECIES_CHARMANDER", "SPECIES_BUDEW", "SPECIES_SCORBUNNY", "SPECIES_ONIX", "SPECIES_SHINX",
    "SPECIES_TOGEPI", "SPECIES_TREECKO", "SPECIES_SNORUNT", "SPECIES_POPPLIO",
    "SPECIES_EEVEE", "SPECIES_GIBLE", "SPECIES_SWABLU", "SPECIES_TOTODILE", "SPECIES_MISDREAVUS",
    "SPECIES_TRAPINCH", "SPECIES_KOFFING", "SPECIES_TANGELA",
    "SPECIES_SKORUPI", "SPECIES_BELDUM", "SPECIES_DELIBIRD",
)
HELD_OUT_SEED = 20261006
HELD_OUT_COUNT = 5


def held_out():
    """The five lines kept from the generator, drawn with Ian's seed."""
    return tuple(random.Random(HELD_OUT_SEED).sample(list(INSIGHT_LINES), HELD_OUT_COUNT))


# ---- the report ------------------------------------------------------------------------

def _sp(species):
    return species_name(species)


def _route(r):
    sp, split, level, how, place = r["route"]
    st = r["stage"]
    if st.via == "caught":
        return f"{how}, {place}, {level}"
    by = "" if st.via == "level" else f" by {_item_name(st.via)}"
    return f"from {_sp(sp)} ({how}, {place}, {level}), at {st.level}{by}"


def _item_name(item):
    return item.replace("ITEM_", "").replace("_", " ").title()


def _first(r):
    fu = r["first"]
    if fu is None:
        return "none by 78"
    idx, lv, mv, how = fu
    where = "at capture" if how == "capture" else "carried" if how == "carried" else \
        "on evolving" if how == "evolving" else f"at {lv}"
    return f"{move_name(mv)} {where} ({SPLITS[idx]})"


def _gap(r):
    return "never" if r["gap"] is None else str(r["gap"])


def report(out=sys.stdout):
    """The baseline's tables, in Markdown."""
    p = lambda *a: print(*a, file=out)
    p("### Check 1 counts\n")
    p("| | Oxide | v3 |\n|---|---|---|")
    c = {v: check1_counts(v) for v in VERSIONS}
    for key, label in (("stages", "Stages the player can have by the League"),
                       ("pass", "Pass: an own-type attack within a split"),
                       ("fail", "Fail: two splits or more without one"),
                       ("never", "of which none by the League's cap"),
                       ("exempt", "Exempt: can evolve by the end of Gardenia's split"),
                       ("lines", "Lines"), ("lines_failing", "Lines with a failing stage"),
                       ("tm_closes", "Failing stages a TM or tutor would close in time")):
        p(f"| {label} | {c['oxide'][key]} | {c['v3'][key]} |")
    p("\n### Check 1 by the split the stage is first had in\n")
    p("| Split | Oxide pass | Oxide fail | v3 pass | v3 fail |\n|---|---|---|---|---|")
    for split in SPLITS:
        cells = []
        for v in VERSIONS:
            rows = [r for r in check1(v).values() if r["split"] == split]
            cells += [sum(r["verdict"] == "pass" for r in rows), sum(r["verdict"] == "fail" for r in rows)]
        p(f"| {split} | " + " | ".join(str(x) for x in cells) + " |")
    p("\n### Check 1: every stage that fails in either version, worst first\n")
    p("| Stage | First had | Route (Oxide's) | Oxide: first own-type attack | Gap | "
      "v3: first own-type attack | Gap | Earliest TM or tutor |")
    p("|---|---|---|---|---|---|---|---|")
    ox, v3 = check1("oxide"), check1("v3")
    failing = {s for s, r in ox.items() if r["verdict"] == "fail"} | \
        {s for s, r in v3.items() if r["verdict"] == "fail"}
    worst = lambda r: 99 if r["gap"] is None else r["gap"]
    for s in sorted(failing, key=lambda s: (-max(worst(ox[s]), worst(v3[s])), -worst(ox[s]),
                                            si(ox[s]["split"]), s)):
        r, w = ox[s], v3[s]
        tm = tm_rescue(s)
        tm_text = f"{tm[1]} {move_name(tm[2])} ({tm[0]})" if tm else "none"
        mark = lambda x: _gap(x) if x["verdict"] == "fail" else f"{_gap(x)}, passes"
        p(f"| {_sp(s)} | {r['split']} | {_route(r)} | {_first(r)} | {mark(r)} | "
          f"{_first(w)} | {mark(w)} | {tm_text} |")
    fixed = [s for s, r in check1("oxide").items() if r["verdict"] == "fail" and v3.get(s, {}).get("verdict") != "fail"]
    broke = [s for s, r in v3.items() if r["verdict"] == "fail" and check1("oxide").get(s, {}).get("verdict") != "fail"]
    p(f"\nv3 mends {len(fixed)}: {', '.join(_sp(s) for s in sorted(fixed)) or 'none'}.")
    p(f"\nv3 breaks {len(broke)}: {', '.join(_sp(s) for s in sorted(broke)) or 'none'}.")
    p("\n### Catches that know no attack at capture\n")
    bare = {v: bare_captures(v) for v in VERSIONS}
    empty = {v: sum(1 for b in bare[v].values() if not b[3]) for v in VERSIONS}
    p(f"Oxide: {len(bare['oxide'])} species, {empty['oxide']} of them with no move at all; "
      f"v3: {len(bare['v3'])}, {empty['v3']} with no move at all.\n")
    p("| Pokemon | Oxide | v3 |\n|---|---|---|")
    for sp in sorted(set(bare["oxide"]) | set(bare["v3"]),
                     key=lambda s: (min(si(bare[v][s][0]) for v in VERSIONS if s in bare[v]), s)):
        cells = []
        for v in VERSIONS:
            b = bare[v].get(sp)
            cells.append(f"{b[2]}, {b[1]} ({b[0]}): {', '.join(move_name(m) for m in b[3]) or 'no move'}"
                         if b else "has an attack")
        p(f"| {_sp(sp)} | {cells[0]} | {cells[1]} |")
    p("\n### Check 4: fixed and level damage by the end of Gardenia's split\n")
    early = {v: check4_early(v) for v in VERSIONS}
    keys = sorted(set(early["oxide"]) | set(early["v3"]),
                  key=lambda k: (min(si(early[v][k][0]) for v in VERSIONS if k in early[v]), k))
    p(f"Oxide: {len(early['oxide'])} entries on {len({k[0] for k in early['oxide']})} species; "
      f"v3: {len(early['v3'])} entries on {len({k[0] for k in early['v3']})} species.\n")
    p("| Pokemon | Move | Oxide | v3 | Ruling |\n|---|---|---|---|---|")
    for k in keys:
        cells = []
        for v in VERSIONS:
            e = early[v].get(k)
            cells.append(f"{e[2]} at {e[1]} ({e[0]})" if e else "not by then")
        rule = []
        for v in VERSIONS:
            st = ruling_state(k[0], k[1], early[v][k][0]) if k in early[v] else \
                ("met" if (k in RULED_OUT) else None)
            if st:
                rule.append(f"{'Oxide' if v == 'oxide' else 'v3'} {st}")
        p(f"| {_sp(k[0])} | {move_name(k[1])} | {cells[0]} | {cells[1]} | "
          f"{', '.join(rule) if rule else 'for Ian'} |")
    mach = check4_machines()
    p(f"\nBy TM, HM or tutor in reach by then (both versions): {len(mach)}"
      + (": " + ", ".join(f"{_sp(sp)} {label} {move_name(mv)} ({s})" for sp, label, mv, s in mach)
         if mach else "."))
    # The next split, for context only: the check stops at Gardenia's end.
    nxt = {v: {k: e for k, e in check4_early(v, "Fantina").items() if k not in early[v]}
           for v in VERSIONS}
    p(f"\nFor context, not part of the check: those first known or learnt in Fantina's split "
      f"(Oxide {len(nxt['oxide'])}, v3 {len(nxt['v3'])}): " + "; ".join(
          f"{_sp(k[0])} {move_name(k[1])} {e[2]} at {e[1]}"
          + ("" if nxt["v3"].get(k) == e else
             f" (v3: {nxt['v3'][k][2]} at {nxt['v3'][k][1]})" if k in nxt["v3"] else " (v3: not by then)")
          for k, e in sorted(nxt["oxide"].items(), key=lambda kv: (kv[1][1], kv[0]))) + ".")
    p("\n### Check 4: one-hit KO moves on a player list\n")
    p("| Pokemon | Move | Oxide | v3 |\n|---|---|---|---|")
    oh = {v: {(sp, mv): how for sp, mv, how in check4_ohko(v)} for v in VERSIONS}
    for k in sorted(set(oh["oxide"]) | set(oh["v3"])):
        p(f"| {_sp(k[0])} | {move_name(k[1])} | {oh['oxide'].get(k, 'not on its lists')} | "
          f"{oh['v3'].get(k, 'not on its lists')} |")
    p("\n### Check 5: PP\n")
    pp = lint_pp()
    bad_setup = [(c, n) for c, n, ok in pp["setup"] if not ok]
    bad_low = [(c, n, rule) for c, n, ok, rule in pp["lowering"] if not ok]
    p(f"Setup moves: {len(pp['setup'])} read, {len(pp['setup']) - len(bad_setup)} at 1 to 3 PP. "
      f"Stat-lowering status moves: {len(pp['lowering'])} read, {len(pp['lowering']) - len(bad_low)} "
      f"within their rule. The move data is the same in both versions.\n")
    if bad_setup or bad_low:
        p("| Move | Kind | PP | Rule |\n|---|---|---|---|")
        for c, n in bad_setup:
            p(f"| {move_name(c)} | setup | {n} | 1 to 3 |")
        for c, n, rule in bad_low:
            p(f"| {move_name(c)} | stat-lowering | {n} | {rule} |")
    p("\nRead but not judged (they raise or lower a stat beside something else): "
      + ", ".join(f"{move_name(c)} {n}" for c, n in pp["borderline"]) + ".")
    p("\n### Check 5: weather, accuracy and the TM list\n")
    p("| Rule | Oxide | v3 |\n|---|---|---|")
    wx = {v: lint_weather(v) for v in VERSIONS}
    for kind, label in (("moves", "Weather moves on an obtainable line's lists"),
                        ("abilities", "Weather abilities in an obtainable line's regular slots")):
        p(f"| {label} | {len(wx['oxide'][kind])} | {len(wx['v3'][kind])} |")
    acc = lint_accuracy()
    bad_acc = [c for c, _n, _w, ok in acc if not ok]
    p(f"| Sleep moves, powders, Thunder Wave, Dark Void, Swagger off Generation 4 accuracy | "
      f"{len(bad_acc)} of {len(acc)} | {len(bad_acc)} of {len(acc)} |")
    tms = {v: lint_tms(v) for v in VERSIONS}
    p(f"| Ian's removed TMs still on the TM list | {len(tms['oxide'])} of {len(REMOVED_TMS)} | "
      f"{len(tms['v3'])} of {len(REMOVED_TMS)} |")
    for v in VERSIONS:
        for kind in ("moves", "abilities"):
            if wx[v][kind]:
                p(f"\n{v} weather {kind}: " + ", ".join(
                    f"{_sp(sp)} {' '.join(str(x) for x in rest)}" for sp, *rest in wx[v][kind]))
    if bad_acc:
        p("\nOff Generation 4 accuracy: " + ", ".join(
            f"{move_name(c)} {n} (vanilla {w})" for c, n, w, ok in acc if not ok))
    p("\nOxide's TM list carries: " + ", ".join(f"{label} {move_name(mv)}" for label, mv in tms["oxide"]) + ".")
    p(f"\nv3's TM pass draft ({v3_tm_set_size()} in its set) carries: "
      + (", ".join(move_name(mv) for _s, mv in tms["v3"]) if tms["v3"] else "none of them") + ".")


def summary(out=sys.stdout):
    for v in VERSIONS:
        c = check1_counts(v)
        e = check4_early(v)
        o = check4_ohko(v)
        w = lint_weather(v)
        print(f"{v:5}: check 1 {c}; check 4 early {len(e)} entries on {len({k[0] for k in e})} species, "
              f"one-hit KO {len(o)}; check 5 weather moves {len(w['moves'])}, abilities "
              f"{len(w['abilities'])}, removed TMs {len(lint_tms(v))}; no attack at capture "
              f"{sorted(species_name(s) for s in bare_captures(v))}", file=out)
    pp = lint_pp()
    print(f"setup off 1 to 3 PP: {[(move_name(c), n) for c, n, ok in pp['setup'] if not ok]}", file=out)
    print(f"lowering off its rule: {[(move_name(c), n) for c, n, ok, _r in pp['lowering'] if not ok]}",
          file=out)
    print(f"accuracy off vanilla: {[(move_name(c), n, w) for c, n, w, ok in lint_accuracy() if not ok]}",
          file=out)


def lines_report(out=sys.stdout):
    held = set(held_out())
    for sp in INSIGHT_LINES:
        cells = []
        for v in VERSIONS:
            stages = [r for r in check1(v).values() if r["family"] == sp]
            fails = [_sp(r["species"]) for r in stages if r["verdict"] == "fail"]
            cells.append(f"{v} fails {fails}" if fails else f"{v} passes")
        print(f"{'HELD OUT ' if sp in held else '         '}{_sp(sp):12} {'; '.join(cells)}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["summary", "report", "sheets", "lines"])
    args = ap.parse_args(argv)
    if args.what == "summary":
        summary()
    elif args.what == "report":
        report()
    elif args.what == "sheets":
        for path in write_sheets():
            print(f"wrote {os.path.relpath(path, data.ROOT)}")
    else:
        lines_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
