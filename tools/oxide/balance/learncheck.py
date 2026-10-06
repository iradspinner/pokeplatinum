"""The learnset checks of docs/oxide/learnset-checks.md: checks 1, 4, 5 and 6
of the baseline (step 1), and checks 7 to 22 from the locked rules of
docs/oxide/learnset-insights.md (step 4), run on two versions of the
level-up lists side by side.

    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck summary   # headline numbers
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck report    # checks 1, 4 and 5, Markdown
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck rules     # checks 7 to 22, Markdown
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck sheets    # writes docs/oxide/learnset-sheets/
    PYTHONPATH=. python3 -m tools.oxide.balance.learncheck lines     # the 20 insight lines, five held out

It writes no game data. Only the level-up lists differ between the
versions. "oxide" is the lists as they were when the learnset rewrite began,
read with git from BASE_REF (the commit balance-learnset-rewrite was cut
from; OXIDE_LEARNSET_BASE overrides it), so the column stays put while the
rewrite changes the tree. "rewrite" is the tree's (res/pokemon/<species>/
data.json). "v3" is the old proposal's entries on origin/balance-learngen-v2
(docs/oxide/learnset-proposal.tsv), kept readable for the baseline's record.
Everything else, the catches, evolutions, moves, TMs and tutors, is the
tree's, so a difference between two columns is the lists' doing.

How the player has a Pokemon (the capture rule, Ian, 2026-09-27). A catch is
one row of pool.catches(): a species, the split it is first offered in, and
the level it comes at (a water slot's lowest). It knows the last four moves
its list gives by that level (the game's own rule, calc_trainers.default_moves:
in list order up to the level, level-0 entries skipped, a move already known
skipped, the oldest dropped once four are full). After capture it learns its
entries above the catch level. It evolves on time: a level evolution at its
level (or the next level-up when caught past it), in the first split whose cap
allows it; an item evolution as soon as the item is in reach (pool's item
census), from the stage's own level, the earliest the player can evolve it
at (a gift Eevee at 20 evolves from 20). An evolved stage keeps what it had, learns its own level-0
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
VERSIONS = ("oxide", "rewrite")
LABELS = {"oxide": "Oxide", "rewrite": "Rewrite", "v3": "v3"}
# The commit balance-learnset-rewrite was cut from (2026-10-06): Oxide's lists
# before step 4 touched them.
BASE_REF = os.environ.get("OXIDE_LEARNSET_BASE", "da6b92496c")
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
SELF_KO = {"MOVE_EXPLOSION", "MOVE_SELFDESTRUCT", "MOVE_MISTY_EXPLOSION", "MOVE_FINAL_GAMBIT",
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
    # Fights are read with no held items, so Acrobatics hits at double power
    # (the exam's regressions, 2026-10-06: Raboot's 110-power Acrobatics at 17).
    if m.get("effect") == "DOUBLE_DAMAGE_WITHOUT_ITEM":
        per_turn *= 2
    return per_turn / hit * DOWNSIDE.get(m.get("effect"), 1.0)


def usable(const, types):
    """Check 1's attack: of one of the stage's types, 50 or more by effective
    power, not one that knocks the user out, and one a list may rely on
    (reliable(): since 2026-10-06 the rampage moves and the moves waiting on
    Ian's rework do not count)."""
    return (const in moves() and const not in SELF_KO and moves()[const]["type"] in types
            and reliable(const) and effective_power(const) >= USABLE_POWER)


# ---- the moves the rulings of 2026-10-06 single out ----------------------------------

# The rampage moves lock the user in for two or three turns (R9): they count
# for nothing until the engine makes them one-turn moves (the tracker), and
# Uproar and Raging Fury wait on Ian's word on a one-turn version too.
RAMPAGE_EFFECTS = {"CONTINUE_AND_CONFUSE_SELF", "UPROAR"}
# Moves waiting on a rework Ian has not ruled on (the tracker's move reworks):
# Fury Cutter, Psywave, every two-turn attack that is neither setup nor made
# worthwhile by circumstance (Solar Beam and Solar Blade in sun; Skull Bash,
# Meteor Beam and Electro Shot raise a stat on the charging turn), and every
# multi-hit move, which the multi-hit review may merge or cut. A list may keep
# one where it stands, but none counts toward a check, so no list relies on one.
TWO_TURN_EFFECTS = {"RECHARGE_AFTER", "CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH",
                    "CHARGE_TURN_PARALYZE_HIT", "CHARGE_TURN_BURN_HIT", "FLY", "DIG", "DIVE",
                    "BOUNCE", "SHADOW_FORCE", "SKY_DROP"}
MULTI_HIT_EFFECTS = {"MULTI_HIT", "HIT_TWICE", "POISON_MULTI_HIT", "HIT_THREE_TIMES",
                     "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20", "HIT_THREE_TIMES_FIXED_POWER",
                     "HIT_THREE_TIMES_ALWAYS_CRITICAL", "UP_TO_10_HITS", "HIT_TWICE_AND_FLINCH",
                     "BEAT_UP"}
PENDING_BY_NAME = {"MOVE_FURY_CUTTER", "MOVE_PSYWAVE"}
# Moves leaving every player list or the game: Fury Attack and Feint (Ian,
# 2026-10-06, "useless"), the first cut of the move pool (2026-09-27: twelve
# moves, Splash and Teleport), and the terrain moves that stay dead with
# terrain (2026-09-27: Steel Roller and Ice Spinner).
REMOVED = {"MOVE_FURY_ATTACK", "MOVE_FEINT", "MOVE_TELEKINESIS", "MOVE_ALLY_SWITCH",
           "MOVE_TOPSY_TURVY", "MOVE_FLOWER_SHIELD", "MOVE_FAIRY_LOCK", "MOVE_AROMATIC_MIST",
           "MOVE_MAGNETIC_FLUX", "MOVE_SPEED_SWAP", "MOVE_ELECTRIC_TERRAIN", "MOVE_GRASSY_TERRAIN",
           "MOVE_MISTY_TERRAIN", "MOVE_PSYCHIC_TERRAIN", "MOVE_SPLASH", "MOVE_TELEPORT",
           "MOVE_STEEL_ROLLER", "MOVE_ICE_SPINNER"}
# Moves whose effect the engine does not run as designed, found after the
# move-pool survey of 2026-09-27 (the exam's regressions, 2026-10-06): Upper
# Hand is an unconditional +3 hit of 65, Shell Trap an unconditional -3 hit
# of 150, Burning Jealousy always burns. They stay off player lists until the
# move rework's cloud job fixes them (Ian approved that job taking them).
UNCHECKED = {"MOVE_UPPER_HAND", "MOVE_SHELL_TRAP", "MOVE_BURNING_JEALOUSY"}
# R26: moves for building a trainer's fight, bad for a player in a permadeath
# run: Destiny Bond and every move that knocks its own user out.
TRAINER_ONLY = SELF_KO | {"MOVE_DESTINY_BOND"}
# Moves that only help catch (they leave the target at 1 HP): early or not at
# all (Ian, 2026-10-06, on False Swipe).
CATCH_ONLY = {"MOVE_FALSE_SWIPE", "MOVE_HOLD_BACK"}
CATCH_ONLY_UNTIL = "Fantina"
# The recovery moves, by effect: a list carries few (Ian, 2026-10-06).
RECOVERY_EFFECTS = {"RESTORE_HALF_HP", "HEAL_HALF_MORE_IN_SUN", "HEAL_HALF_REMOVE_FLYING_TYPE",
                    "LIFE_DEW", "HEAL_IN_3_TURNS", "REST", "STRENGTH_SAP", "LUNAR_BLESSING",
                    "RESTORE_HP_EVERY_TURN", "SWALLOW"}
RECOVERY_MOST = 2
# R24: out of every player list (level-up, TM and tutor alike). Protect and
# every move sharing its effect (Detect, King's Shield and the rest), Double
# Team, Ingrain (too dangerous) and every one-hit KO move.
OUT_BY_NAME = {"MOVE_DOUBLE_TEAM", "MOVE_INGRAIN"}
OUT_EFFECTS = {"PROTECT", "ONE_HIT_KO"}


def rampage(const):
    return const in moves() and moves()[const]["effect"] in RAMPAGE_EFFECTS


def pending(const):
    """Waiting on Ian's rework ruling: counted by no check."""
    m = moves().get(const)
    return bool(m) and (const in PENDING_BY_NAME or m["effect"] in TWO_TURN_EFFECTS
                        or m["effect"] in MULTI_HIT_EFFECTS)


def out_of_lists(const):
    """R24: a move no player list may hold."""
    m = moves().get(const)
    return bool(m) and (const in OUT_BY_NAME or m["effect"] in OUT_EFFECTS)


def not_working(const):
    """A move whose effect the engine does not carry out: a status move left
    on the plain-hit script, or an effect still stubbed."""
    m = moves().get(const)
    return not m or m.get("stub") or (m["class"] == "STATUS" and m["effect"] == "HIT")


def reliable(const):
    """A move a list may rely on: none of the above, and not a fixed or level
    damage move (check 4's run-enders)."""
    return (const in moves() and not rampage(const) and not pending(const)
            and not out_of_lists(const) and const not in REMOVED and not not_working(const)
            and not run_ender(const) and const not in UNCHECKED)


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
    ref = BASE_REF if version == "oxide" else None
    return tuple(tuple(e) for e in (pokedex.load(data.ROOT, species, ref=ref) or {}).get("learnset", []))


def at_capture(version, species, level):
    """The four moves a Pokemon caught at `level` knows: the game's rule."""
    return calc_trainers.default_moves(list(learnset(version, species)), level)


# ---- where each Pokemon is caught ---------------------------------------------

# Two corrections to pool's catches that Ian made in the insight sessions
# (2026-10-06), kept here so the stored scores, which read pool, do not move.
# Amity Square's table is read as a catch, but no map header uses it, so no
# one can meet it (Swablu's session; the encounter track's open item). And
# Cynthia's Togepi egg is received in Fantina's split, after the Eterna
# building, not in Gardenia's, which Eterna City's location gives it
# (Togepi's session, R20).
UNMET_PLACES = {"Amity Square"}
SPLIT_FIXES = {("SPECIES_TOGEPI", "egg gift", "Eterna City"): "Fantina"}
# A third, from Ian's ruling of 2026-09-30 (the tracker's fossils entry): the
# Mining Museum revives a fossil only once the player is through Cycling
# Road, so every fossil comes in Fantina's split. The pool leaves fossils out
# (their revival level is above Roark's cap, their location's split), which
# the balance census still owes.
FOSSIL_SPLIT = "Fantina"


@functools.lru_cache(maxsize=None)
def fossil_rows():
    """((species, split, level, "fossil", place), ...) from the sources file."""
    out = []
    with open(pool.SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["method"] == "fossil" and row["species"].startswith("SPECIES_"):
                out.append((row["species"], FOSSIL_SPLIT, pool._source_level(row["level"]), "fossil",
                            row["location"]))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def catch_rows():
    """((species, split, level, how, place), ...): pool.catches() row for row,
    with the capture area each comes from (the encounter tool's location name,
    "Honey trees", or a scripted source's location), less UNMET_PLACES, with
    SPLIT_FIXES applied and the fossils added (fossil_rows). test_learncheck
    checks that the rows are pool's but for those."""
    rows = tuple((sp, SPLIT_FIXES.get((sp, how, place), split), level, how, place)
                 for sp, split, level, how, place in _pool_rows() if place not in UNMET_PLACES)
    have = {(r[0], r[3]) for r in rows}
    return rows + tuple(r for r in fossil_rows() if (r[0], r[3]) not in have)


@functools.lru_cache(maxsize=None)
def _pool_rows():
    """pool.catches() row for row, each with its capture area."""
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
            # The player levels the stage while the item is out of reach, to
            # the cap before the item's split, and evolves it there. A line
            # in STONE_EXCEPTIONS is kept at its level until it evolves (Ian's
            # exam verdict on Eevee, 2026-10-06), so it evolves from there.
            if ti == pi or family(parent.species) in STONE_EXCEPTIONS:
                level = parent.level
            else:
                level = max(parent.level, caps()[SPLITS[ti - 1]])
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
    machines for Oxide and the rewrite (which changes no TM), the TM pass
    draft's set on the v3 branch for v3."""
    if version != "v3":
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


# How each version is described in a sheet's header.
SHEET_SECOND = {"oxide": f"Oxide's lists before the learnset rewrite (`{BASE_REF}`)",
                "rewrite": "the learnset rewrite's lists (the tree's)",
                "v3": f"learnset v3 (unlanded, `{V3_REF}`)"}


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
                 f"marked {LABELS[VERSIONS[1]]} shows {SHEET_SECOND[VERSIONS[1]]} where it differs "
                 f"from the row marked {LABELS[VERSIONS[0]]}, {SHEET_SECOND[VERSIONS[0]]}; a row "
                 f"marked both is the same in each. Relearner-only moves and egg moves are left "
                 f"out.", ""]
        for place in sorted(rows, key=lambda p: (p == "Honey trees", p)):
            lines += [f"## {place}", "",
                      "| Pokemon | Found as | Level | Lists | Knows at capture | "
                      f"Learns by level-up by {cap} | At the cap |",
                      "|---|---|---|---|---|---|---|"]
            for r in rows[place]:
                lo, hi = r["levels"]
                lv = str(lo) if lo == hi else f"{lo} to {hi}"
                a, b = (r["cells"][v] for v in VERSIONS)
                variants = [("both", c) for c in a] if a == b else \
                    [(LABELS[VERSIONS[0]], c) for c in a] + [(LABELS[VERSIONS[1]], c) for c in b]
                for label, (cap_moves, learnt, stage) in variants:
                    lines.append(f"| {species_name(r['species'])} | {_cell(r['how'].replace('_', ' '))} | {lv} | {label} | "
                                 f"{_cell(cap_moves)} | {_cell(learnt)} | {_cell(stage)} |")
            lines.append("")
        path = os.path.join(SHEETS, f"{split.lower()}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))
        written.append(path)
    return written


# ---- checks 7 to 22: the locked rules (step 4) -----------------------------------------
#
# Each check reads one of the locked rules of docs/oxide/learnset-insights.md
# (or a few of the mechanical ones) as the player meets the lists, by the
# same capture rule and on-time evolution as checks 1 to 6. A line is walked
# from its earliest catch (the first split any stage of it is offered in, at
# the lowest level there), down every branch; a stage first had only from a
# later catch is walked from that catch. The thresholds are the defaults the
# rules state or imply, and Ian's to set.

# R1: five or six moves by the first split's cap, at most one of them filler.
R1_MOVES, R1_FILLER = 5, 1
# R2: two new moves in each band of R2_BAND levels a stage is held through.
R2_NEW, R2_BAND = 2, 8
# R4: the first coverage move by the second split; a weak one counts early.
COVER_EARLY = 40
# R5: several coverage types over the game, judged on attacks of 50 or more;
# a very strong line (R35) may have fewer, never almost none.
COVER_LATE, R5_TYPES, R5_STRONG_TYPES, R5_STRONG_BST = 50, 3, 2, 580
# R7: a good utility move by the second split; a less offensive line (its
# final form's better attacking stat under this) needs two over the game.
R7_LOW_OFFENSE, R7_LOW_GOOD = 85, 2
# R32: a setup move needs an attack of the class it boosts, this strong by
# effective power with same-type bonus, by the end of the next split.
R32_POWER = 80
# R37: an attack below this accuracy is very hard to justify on a list.
R37_ACCURACY = 90
# The late move (2026-09-28): each final stage learns a real move from here.
LATE_FROM = 61
# A move's stat fits the Pokemon when it is this share of its better attacking stat (R15).
FIT_SHARE = 0.8
# Effects of a damaging move with nothing beside the damage (R6's narrowing).
PLAIN_EFFECTS = {"HIT", "BYPASS_ACCURACY"}


def window(split):
    """(lowest, highest) level of a split: one above the cap before it, to its own cap."""
    i = si(split)
    return (caps()[SPLITS[i - 1]] + 1 if i else 1), caps()[split]


@functools.lru_cache(maxsize=None)
def stats(species):
    return (pokedex.load(data.ROOT, species) or {}).get("stats") or {}


def attack_stats(species):
    s = stats(species)
    return s.get("attack", 0), s.get("special_attack", 0)


def fits(const, species):
    """R15: the stat the move uses is at least FIT_SHARE of the Pokemon's
    better attacking stat, so a mixed attacker fits both kinds."""
    atk, spa = attack_stats(species)
    use = atk if moves()[const]["class"] == "PHYSICAL" else spa
    return use >= FIT_SHARE * max(atk, spa, 1)


def damaging(const):
    """A damaging move a list may rely on (any power, variable ones included)."""
    return const in moves() and moves()[const]["class"] != "STATUS" and reliable(const) \
        and const not in SELF_KO


def attack(const, floor):
    """A damaging move a list may rely on, of `floor` effective power or more."""
    return damaging(const) and effective_power(const) >= floor


def coverage(const, species, floor):
    """A coverage attack for a Pokemon: not of its types, not Normal (which
    hits nothing hard), on a stat that fits it (R15)."""
    return (attack(const, floor) and moves()[const]["type"] not in types_of(species)
            and moves()[const]["type"] != "NORMAL" and fits(const, species))


def _acc(const):
    acc = moves()[const]["accuracy"]
    return 101 if not acc else acc          # 0 means it never misses


# ---- R7's utility tiers -------------------------------------------------------------------

TIER_RANK = {"SSS": 9, "Fantastic": 8, "Incredible": 7, "Great": 6, "Good": 5, "Pretty solid": 4,
             "Okay": 3, "Niche": 2, "Bad": 1, "Useless": 0, "Terrible": 0}
GOOD = TIER_RANK["Good"]
BAD = TIER_RANK["Bad"]
# Ian's tiers (learnset-insights.md, "The utility tiers"), by move.
IAN_TIERS = {
    "SSS": ("ENCORE", "FOLLOW_ME", "TOXIC", "DRAGON_DANCE", "QUIVER_DANCE", "SHELL_SMASH",
            "MIRROR_MOVE"),
    "Fantastic": ("WISH", "CONFUSE_RAY", "MEAN_LOOK", "BLOCK", "SPIDER_WEB"),
    "Incredible": ("CHARM", "SWEET_KISS", "SWAGGER", "YAWN", "SYNTHESIS", "ICY_WIND"),
    "Great": ("AGILITY", "TICKLE", "IRON_DEFENSE"),
    "Good": ("SCARY_FACE", "SCREECH", "STUN_SPORE", "TOXIC_SPIKES", "CURSE", "ROCK_POLISH",
             "BABY_DOLL_EYES", "LIFE_DEW", "SPITE"),
    "Pretty solid": ("SAFEGUARD", "CAPTIVATE"),
    "Okay": ("CHARGE", "SING", "SAND_ATTACK", "LUCKY_CHANT", "FLAIL", "BATON_PASS"),
    "Niche": ("AROMATHERAPY", "FIRE_SPIN", "NATURAL_GIFT", "WORRY_SEED"),
    "Bad": ("GROWL", "LEER", "TACKLE", "BIND", "GROWTH", "WATER_SPORT", "SMOKE_SCREEN", "ROAR",
            "REFRESH", "MIST", "PAIN_SPLIT"),
    "Useless": ("METRONOME", "SWEET_SCENT", "MUD_SPORT", "RAGE", "GRUDGE", "WRING_OUT"),
    "Terrible": ("MEMENTO", "HAZE"),
}
# Ian's classes of move: every move raising Speed and an attacking stat is
# SSS like Dragon Dance; every blocking move is fantastic like Mean Look; an
# attack that always lowers Speed is incredible like Icy Wind (R27).
SSS_EFFECTS = {"ATK_SPD_UP", "SP_ATK_SP_DEF_SPEED_UP", "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN",
               "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP", "SPEED_UP_2_ATK_UP", "ATK_DEF_SPEED_UP",
               "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2", "TIDY_UP", "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP"}
BLOCK_EFFECTS = {"PREVENT_ESCAPE"}
SPEED_CONTROL_EFFECTS = {"LOWER_SPEED_HIT"}
# The Generation 9 list Ian agrees with almost entirely (status-move-tiers.md),
# for the moves he has not rated. It rates competitive play, so its tiers come
# down a step against his: its S is his good, its F his bad.
GEN9_RANK = {"SSS": 6, "S": 5, "A": 4, "B": 3, "C": 2, "D": 2, "F": 1, "Useless": 0}
TIERS_DOC = os.path.join(data.ROOT, "docs", "oxide", "status-move-tiers.md")


@functools.lru_cache(maxsize=None)
def _gen9_tiers():
    """{MOVE_X: tier} from status-move-tiers.md's table, by compact name.
    The moves Ian does not endorse there (the instant-death ones, the hazards
    but Toxic Spikes and Sticky Web) are left unrated, as the doc says."""
    unrated = {"revivalblessing", "destinybond", "healingwish", "lunardance", "memento",
               "stealthrock", "spikes"}
    names = _by_compact_name()
    out = {}
    with open(TIERS_DOC, encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 2 or cells[0] not in GEN9_RANK:
                continue
            for name in cells[1].split(","):
                key = _compact(name)
                if key in names and key not in unrated:
                    out[names[key]] = cells[0]
    return out


@functools.lru_cache(maxsize=None)
def tier(const):
    """(rank, source) of a utility move for R7: Ian's tier where he rated it
    or its class, else the Generation 9 list's a step down, else None (an
    unrated status move, or an attack that is no utility)."""
    if const not in moves():
        return None
    short = const[len("MOVE_"):]
    for name, members in IAN_TIERS.items():
        if short in members:
            return TIER_RANK[name], "Ian"
    m = moves()[const]
    if m["class"] == "STATUS" and m["effect"] in SSS_EFFECTS:
        return TIER_RANK["SSS"], "Ian"
    if m["class"] == "STATUS" and m["effect"] in BLOCK_EFFECTS:
        return TIER_RANK["Fantastic"], "Ian"
    if m["class"] != "STATUS" and m["effect"] in SPEED_CONTROL_EFFECTS and m["effect_chance"] == 100:
        return TIER_RANK["Incredible"], "Ian"
    if m["class"] == "STATUS" and const in _gen9_tiers():
        return GEN9_RANK[_gen9_tiers()[const]], "Generation 9 list"
    return None


def utility(const):
    """A utility move a list may rely on: a working status move, or an attack
    Ian rates as utility (sure speed control, Flail, Fire Spin)."""
    if not reliable(const):
        return False
    return moves()[const]["class"] == "STATUS" or tier(const) is not None


def counts(const):
    """A move that counts as one of a Pokemon's moves for R1 and R2: one a
    list may rely on, not rated useless or terrible, not one for trainers
    only (R26: Destiny Bond and the moves that knock their user out), and
    not an attack that works only on a condition the user rarely has (Last
    Resort, Dream Eater: the exam's reviewer read Last Resort as filler,
    2026-10-06)."""
    t = tier(const)
    return (reliable(const) and not (t and t[0] == 0) and const not in TRAINER_ONLY
            and ls.strength(ls.oxide_move(moves()[const]))[0] != "conditional")


def filler(const, species):
    """A move that fills a slot without adding a choice (R1's "uninspired"):
    a utility move Ian rates bad, or a weak plain Normal attack on a Pokemon
    that is not Normal (Scratch, Pound). A weak attack of another type is
    early coverage (Popplio's Disarming Voice), not filler."""
    t = tier(const)
    if t and t[0] <= BAD:
        return True
    m = moves()[const]
    return (m["class"] != "STATUS" and m["type"] == "NORMAL" and "NORMAL" not in types_of(species)
            and m["effect"] in PLAIN_EFFECTS and not m["priority"] and (m["power"] or 0) <= 40)


# ---- walking a line ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def line_catches():
    """{family: [(split, level, species)]}, every catch of every stage of an
    obtainable line, earliest first."""
    owned = b6.obtainable()
    out = collections.defaultdict(set)
    for sp, split, level, _how, _place in catch_rows():
        if sp in species_set() and sp in owned:
            out[family(sp)].add((split, level, sp))
    return {f: sorted(rows, key=lambda r: (si(r[0]), r[1], r[2])) for f, rows in out.items()}


@functools.lru_cache(maxsize=None)
def line_paths(version, fam):
    """The paths a line is walked on: every branch from its earliest catch,
    then from the earliest catch of any stage those do not reach."""
    paths, covered = [], set()
    for split, level, sp in line_catches()[fam]:
        if sp in covered:
            continue
        for path in branches(version, sp, split, level):
            paths.append(path)
            covered |= {st.species for st in path}
    return tuple(paths)


@functools.lru_cache(maxsize=None)
def path_events(path, upto=None):
    """((level, stage index, MOVE_X, how), ...): what the player gains along a
    path, in order. how: "capture" (known when caught), "evolving" (a level-0
    entry), or "level-up". A stage learns its own entries until it evolves
    on time, the evolution level included."""
    upto = caps()[SPLITS[-1]] if upto is None else upto
    ev = [(path[0].level, 0, m, "capture") for m, _o in path[0].brought]
    for i, st in enumerate(path):
        nxt = path[i + 1].level if i + 1 < len(path) else None
        if i:
            ev += [(st.level, i, m, "evolving") for m, o in st.brought if o == "evolving"]
        ev += [(lv, i, m, "level-up") for lv, m in st.own
               if lv <= upto and (nxt is None or lv <= nxt)]
    return tuple(sorted((e for e in ev if e[0] <= upto), key=lambda e: (e[0], e[1])))


def event_split(path, i, level):
    """The split index a stage gains a move in: never before the stage is had."""
    s = split_of_level(level)
    return max(si(path[i].split), si(s) if s else len(SPLITS))


def _final_paths(version):
    """{final species: (family, path)}: each branch's end once, from its first path."""
    out = {}
    for fam in sorted(line_catches()):
        for path in line_paths(version, fam):
            out.setdefault(path[-1].species, (fam, path))
    return out


def _stage_paths(version):
    """{species: (family, path, index)}: each stage once, from the first path it is on."""
    out = {}
    for fam in sorted(line_catches()):
        for path in line_paths(version, fam):
            for i, st in enumerate(path):
                out.setdefault(st.species, (fam, path, i))
    return out


# ---- check 7 (R1): a choice of moves from the first split ----------------------------------------

@functools.lru_cache(maxsize=None)
def check7(version):
    """{family: result}: the moves a line has by its first split's cap (known
    at capture or learnt by level-up, evolving on time), counting only the
    moves that count (counts()); the filler among them; and the verdict, pass
    with R1_MOVES or more of which no more than R1_FILLER are filler. The best
    catch and branch in that split is taken."""
    out = {}
    for fam, rows in line_catches().items():
        split = rows[0][0]
        cap = caps()[split]
        best = None
        for path in line_paths(version, fam):
            if path[0].split != split:
                continue
            got, fill = [], []
            for lv, i, mv, _how in path_events(path, cap):
                if mv not in got and counts(mv):
                    got.append(mv)
                    if filler(mv, path[i].species):
                        fill.append(mv)
            ok = len(got) >= R1_MOVES and len(got) - len(fill) >= R1_MOVES - R1_FILLER
            key = (ok, len(got) - len(fill), len(got))
            if best is None or key > best[0]:
                best = (key, path, got, fill)
        key, path, got, fill = best
        out[fam] = {"family": fam, "split": split, "species": path[0].species, "level": path[0].level,
                    "moves": tuple(got), "filler": tuple(fill), "verdict": "pass" if key[0] else "fail"}
    return out


# ---- check 8 (R2): steady learning, split by split ------------------------------------------------

def held_splits(path, i):
    """The split indices R2 holds stage i of a path to: those it is held at
    the cap of. A stage that evolves by level is held from the split after it
    is had until the split it evolves in, which is not counted. One that
    evolves by an item waits on the player, so it is held through the split
    after its item comes in reach (a split's grace; the player chooses when
    to use the item). A final stage is held to the League's cap, except one
    reached by an item, which keeps learning from about three splits on (R10)."""
    st = path[i]
    a = si(st.split)
    last = len(SPLITS) - 1
    exception = family(st.species) in STONE_EXCEPTIONS
    if i + 1 < len(path):
        if path[i + 1].via == "level":
            return list(range(a + 1, si(path[i + 1].split)))
        if exception:
            return []           # kept at its level until it evolves
        return list(range(a + 1, min(si(path[i + 1].split) + 1, last) + 1))
    if st.via not in ("caught", "level"):
        return list(range(a, last + 1)) if exception else list(range(a + 3, last + 1))
    return list(range(a + 1, last + 1))


# Ian's exception to R10 (the exam, 2026-10-06): "Eeveelutions should be the
# major exception to the evolution stone rule of limited/no moves learned
# after evolving via stone; eevee will almost certainly be kept at 20 until it
# is ready to be evolved, so it will need complete moveset reworks for the
# eeveelutions from 20-onwards." The line's first stage is held at its level,
# and each stone form is held from the level it arrives at.
STONE_EXCEPTIONS = {"SPECIES_EEVEE"}


def held_bands(path, i):
    """[(lowest, highest level)]: the levels stage i is held through (its
    held splits, contiguous), cut into bands of R2_BAND levels from the first.
    Ian, 2026-10-06, after reading the exam: count new moves by level band,
    not by split, since the late splits are three to five levels each and a
    count per split piled moves at the end of a list (Sceptile's twelve from
    53 up)."""
    xs = held_splits(path, i)
    if not xs:
        return []
    lo, hi = window(SPLITS[xs[0]])[0], window(SPLITS[xs[-1]])[1]
    if xs[0] == si(path[i].split):
        lo = max(path[i].level, 2)      # held from its arrival (STONE_EXCEPTIONS)
    out = []
    while lo <= hi:
        out.append((lo, min(lo + R2_BAND - 1, hi)))
        lo += R2_BAND
    return out


def band_need(lo, hi):
    """New moves a band asks for: R2_NEW in a full band, one in a band of at
    least half its width at the end of a stage's hold, none in a shorter one."""
    width = hi - lo + 1
    return R2_NEW if width >= R2_BAND else (1 if width * 2 >= R2_BAND else 0)


@functools.lru_cache(maxsize=None)
def check8(version):
    """{species: result}: for each stage, the new moves (counts()) it learns
    in each band of levels it is held through (held_bands); it fails when a
    band brings fewer than band_need asks."""
    out = {}
    for sp, (fam, path, i) in _stage_paths(version).items():
        st = path[i]
        # The stage's own list, read past an on-time item evolution: the
        # window a stage waiting on an item is held for runs that far.
        brought = {m for m, _o in st.brought}
        per = {}
        for lo, hi in held_bands(path, i):
            before = brought | {m for lv, m in st.own if lv < lo}
            new = []
            for lv, m in st.own:
                if lo <= lv <= hi and counts(m) and m not in before and m not in new:
                    new.append(m)
            per[f"{lo}-{hi}"] = (tuple(new), band_need(lo, hi))
        short = [b for b, (ms, need) in per.items() if len(ms) < need]
        out[sp] = {"species": sp, "family": fam, "bands": {b: ms for b, (ms, _n) in per.items()},
                   "short": tuple(short), "verdict": "fail" if short else "pass"}
    return out


# ---- checks 9 and 10 (R4, R5): coverage early, and over the game ---------------------------------

@functools.lru_cache(maxsize=None)
def check9(version):
    """{family: result}: the line's first coverage attack (COVER_EARLY or more,
    on a stat that fits its holder), known or learnt, on the best branch from
    its first split; it passes by the end of the second split (R4)."""
    out = {}
    for fam, rows in line_catches().items():
        first = si(rows[0][0])
        best = None
        for path in line_paths(version, fam):
            if si(path[0].split) != first:
                continue
            hit = None
            for lv, i, mv, _how in path_events(path):
                if coverage(mv, path[i].species, COVER_EARLY):
                    cand = (event_split(path, i, lv), lv, mv, path[i].species)
                    hit = cand if hit is None or cand < hit else hit
            key = hit[0] if hit else 99
            if best is None or key < best[0]:
                best = (key, hit)
        key, hit = best
        out[fam] = {"family": fam, "split": SPLITS[first], "first": hit,
                    "gap": None if hit is None else hit[0] - first,
                    "verdict": "pass" if hit is not None and hit[0] - first <= 1 else "fail"}
    return out


def _kaizo_cover(path, final):
    """The coverage types (against `final`'s Oxide types) of the attacks of 50
    or more on Kaizo's lists for the path's species, at any level but 1: R5's
    reference for which types a line should reach."""
    kz = learnstudy_kaizo()
    names = _by_compact_name()
    out = set()
    for st in path:
        for lv, name in (kz.get(st.species) or {}).get("list", []):
            mv = names.get(_compact(ls.SPELLING.get(name, name)))
            if lv > 1 and mv and moves()[mv]["class"] != "STATUS" and effective_power(mv) >= COVER_LATE \
                    and moves()[mv]["type"] not in types_of(final) and moves()[mv]["type"] != "NORMAL":
                out.add(moves()[mv]["type"])
    return out


@functools.lru_cache(maxsize=None)
def learnstudy_kaizo():
    return ls.kaizo_lists()


@functools.lru_cache(maxsize=None)
def check10(version):
    """{final species: result}: the coverage types a branch's final form has
    by the League's cap (attacks of COVER_LATE or more on a stat that fits it,
    known or learnt anywhere on the path), Kaizo's types for the line beside
    them; it passes with R5_TYPES, or R5_STRONG_TYPES for a very strong line."""
    out = {}
    for final, (fam, path) in _final_paths(version).items():
        types = {}
        for lv, i, mv, _how in path_events(path):
            if coverage(mv, final, COVER_LATE):
                types.setdefault(moves()[mv]["type"], mv)
        bst = sum(stats(final).values())
        need = R5_STRONG_TYPES if bst >= R5_STRONG_BST else R5_TYPES
        out[final] = {"species": final, "family": fam, "types": types, "need": need,
                      "kaizo": tuple(sorted(_kaizo_cover(path, final))),
                      "verdict": "pass" if len(types) >= need else "fail"}
    return out


# ---- check 11 (R6): dominated moves ---------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def check11(version):
    """[(species, level, MOVE_X, the stronger MOVE_Y)]: an entry learnt while
    the Pokemon already has a stronger move of the same type and class that is
    at least as accurate, where the entry has no secondary effect and no
    priority (R6 as narrowed, 2026-10-06)."""
    found = {}
    for fam in sorted(line_catches()):
        for path in line_paths(version, fam):
            held = []
            for lv, i, mv, how in path_events(path):
                m = moves()[mv]
                if how != "capture" and m["class"] != "STATUS" and m["effect"] in PLAIN_EFFECTS \
                        and not m["priority"]:
                    for n in held:
                        nm = moves()[n]
                        if n != mv and nm["type"] == m["type"] and nm["class"] == m["class"] \
                                and reliable(n) and effective_power(n) > effective_power(mv) \
                                and _acc(n) >= _acc(mv):
                            found.setdefault((path[i].species, lv, mv), n)
                            break
                if mv not in held:
                    held.append(mv)
    return sorted((sp, lv, mv, n) for (sp, lv, mv), n in found.items())


# ---- check 12 (R7): utility quality -----------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def check12(version):
    """{final species: result}: the good utility moves (Good or better) a
    branch has by the end of its line's second split and by the League's cap,
    and the bad ones (Bad or worse) it is given; it passes with one good move
    by the second split, and R7_LOW_GOOD over the game for a less offensive
    line."""
    out = {}
    for final, (fam, path) in _final_paths(version).items():
        first = si(line_catches()[fam][0][0])
        early_cap = caps()[SPLITS[min(first + 1, len(SPLITS) - 1)]]
        early, total, bad = [], [], []
        for lv, i, mv, _how in path_events(path):
            if not utility(mv):
                continue
            rank = tier(mv)
            if rank and rank[0] >= GOOD:
                if mv not in total:
                    total.append(mv)
                if lv <= early_cap and mv not in early:
                    early.append(mv)
            elif rank and rank[0] <= BAD and mv not in bad:
                bad.append(mv)
        offense = max(attack_stats(final))
        ok = bool(early) and (offense >= R7_LOW_OFFENSE or len(total) >= R7_LOW_GOOD)
        out[final] = {"species": final, "family": fam, "early": tuple(early), "total": tuple(total),
                      "bad": tuple(bad), "offense": offense, "verdict": "pass" if ok else "fail"}
    return out


# ---- check 13 (R8): choices that stay inside one split ----------------------------------------------

LEVEL_METHODS = {"LEVEL", "LEVEL_MALE", "LEVEL_FEMALE", "LEVEL_ATK_GT_DEF", "LEVEL_ATK_EQ_DEF",
                 "LEVEL_ATK_LT_DEF", "LEVEL_PID_LOW", "LEVEL_PID_HIGH", "LEVEL_NINJASK",
                 "LEVEL_SHEDINJA", "LEVEL_DAY", "LEVEL_NIGHT"}


@functools.lru_cache(maxsize=None)
def level_evolutions():
    """[(pre, level, target)]: every evolution by level alone, from the records."""
    out = []
    for sp in sorted(species_set()):
        for evo in (pokedex.load(data.ROOT, sp) or {}).get("evolutions", []):
            if evo["method"] in LEVEL_METHODS and evo["level"] and evo["into"]:
                out.append((sp, evo["level"], evo["into"]))
    return out


@functools.lru_cache(maxsize=None)
def check13(version):
    """[(kind, pre, target, MOVE_X, level a, level b)] for each level
    evolution the player can make. "free hold": the pre-evolution learns a
    move between its evolution level and the cap of that split which the
    evolved form does not have by the cap, so holding it costs nothing and
    is no choice. "one split": the same move at two levels on the two lists,
    both inside one split, where the later option always wins."""
    owned = b6.obtainable()
    out = []
    for pre, level, target in level_evolutions():
        if pre not in owned or target not in owned or not split_of_level(level):
            continue
        cap = caps()[split_of_level(level)]
        tgt = learnset(version, target)
        tgt_by_cap = {m for lv, m in tgt if lv == 0 or level <= lv <= cap}
        pre_list = learnset(version, pre)
        for lv, m in pre_list:
            if level < lv <= cap and m not in tgt_by_cap and counts(m):
                out.append(("free hold", pre, target, m, lv, None))
        pre_lv = {}
        for lv, m in pre_list:
            if lv >= 2:
                pre_lv.setdefault(m, lv)
        for lv, m in tgt:
            if lv >= level and m in pre_lv and pre_lv[m] != lv and counts(m) \
                    and split_of_level(pre_lv[m]) == split_of_level(lv):
                out.append(("one split", pre, target, m, pre_lv[m], lv))
    return out


# ---- check 14 (R11): an attack of each of the stage's types -----------------------------------------

@functools.lru_cache(maxsize=None)
def check14(version):
    """{species: result}: each stage's first attack of each of its types
    (any power), known or learnt, on its best route in the split it is first
    had in, as check 1 reads it; it passes when every type's comes in that
    split or the next, and is exempt where check 1 exempts it."""
    owned = b6.obtainable()
    out = {}
    for sp, routes in stage_routes(version).items():
        if sp not in owned:
            continue
        first = min(si(st.split) for st, _row in routes)
        best = None
        for st, _row in routes:
            if si(st.split) != first:
                continue
            per = {}
            for t in sorted(types_of(sp)):
                hit = None
                for m, _origin in st.brought:
                    if damaging(m) and moves()[m]["type"] == t:
                        cand = (si(st.split), st.level, m)
                        hit = cand if hit is None or cand < hit else hit
                for lv, m in st.own:
                    s = split_of_level(lv)
                    if s and damaging(m) and moves()[m]["type"] == t:
                        cand = (max(si(st.split), si(s)), lv, m)
                        hit = cand if hit is None or cand < hit else hit
                per[t] = hit
            key = max(99 if h is None else h[0] - first for h in per.values())
            if best is None or key < best[0]:
                best = (key, per)
        key, per = best
        missing = tuple(t for t, h in per.items() if h is None or h[0] - first > 1)
        verdict = "exempt" if missing and evolves_early(sp) else ("fail" if missing else "pass")
        out[sp] = {"species": sp, "split": SPLITS[first], "types": per, "missing": missing,
                   "verdict": verdict}
    return out


# ---- checks 15 to 22: the mechanical rules ----------------------------------------------------------

@functools.lru_cache(maxsize=None)
def families():
    """{family: {its species}} over every species."""
    out = collections.defaultdict(set)
    for sp in species_set():
        out[family(sp)].add(sp)
    return out


@functools.lru_cache(maxsize=None)
def check15(version):
    """[species]: R21, Baton Pass on a list (above level 1) of a species that
    learns no stat-raising move by level-up to pass on, on its own list or
    one it carries from what it evolves from (the exam's regressions,
    2026-10-06: Baton Pass on Eevee, which has no boost of its own)."""
    setup = set(setup_moves())
    out = []
    for sp in sorted(b6.obtainable()):
        if not any(m == "MOVE_BATON_PASS" and lv >= 2 for lv, m in learnset(version, sp)):
            continue
        own = [sp] + list(pool.pre_evolutions().get(sp) or [])
        if not any(m in setup and lv >= 2 for s in own for lv, m in learnset(version, s)):
            out.append(sp)
    return out


@functools.lru_cache(maxsize=None)
def check16(version):
    """[(species, where, MOVE_X, rule)]: R24's moves (Protect and its kin,
    Double Team, Ingrain, the one-hit KO moves) and the moves leaving the game
    on an obtainable species' level-up list at any level, and on its TM and
    tutor lists (the same in every version, for the TM pass)."""
    machines = pokedex.machines(data.ROOT)
    out = []
    for sp in sorted(b6.obtainable()):
        rec = pokedex.load(data.ROOT, sp) or {}
        where = [(f"level {lv}", m) for lv, m in learnset(version, sp)]
        where += [(label, machines.get(label)) for label in rec.get("by_tm") or []]
        where += [("tutor", m) for m in rec.get("by_tutor") or []]
        for w, m in where:
            if m and out_of_lists(m):
                out.append((sp, w, m, "R24"))
            elif m in REMOVED:
                out.append((sp, w, m, "removed"))
            elif m in UNCHECKED and w.startswith("level"):
                out.append((sp, w, m, "not run as designed"))
    return out


@functools.lru_cache(maxsize=None)
def check17(version):
    """[(species, level, MOVE_X, lowest level it is had at)]: R25, an entry
    above level 1 below the lowest level any player can have the stage at,
    which no earlier stage learns and the stage does not learn again later:
    a move only the relearner reaches."""
    routes = stage_routes(version)
    out = []
    for sp in sorted(b6.obtainable()):
        pres = pool.pre_evolutions().get(sp) or []
        if not pres or sp not in routes:
            continue
        lowest = min(st.level for st, _row in routes[sp])
        earlier = {m for p in pres for lv, m in learnset(version, p) if lv >= 2}
        later = {m for lv, m in learnset(version, sp) if lv >= lowest or lv == 0}
        for lv, m in learnset(version, sp):
            if 2 <= lv < lowest and m not in earlier and m not in later:
                out.append((sp, lv, m, lowest))
    return out


# What a setup move boosts, by effect (R32): a physical or special attack, an
# attack of either kind, any attack (Speed alone), or Electric ones (Charge).
# Defensive boosts need no attack and are not judged.
BOOSTS = {
    "ATK_UP": "PHYSICAL", "ATK_UP_2": "PHYSICAL", "ATK_DEF_UP": "PHYSICAL", "ATK_SPD_UP": "PHYSICAL",
    "ATK_ACC_UP": "PHYSICAL", "ATK_DEF_ACC_UP": "PHYSICAL", "MAX_ATK_LOSE_HALF_MAX_HP": "PHYSICAL",
    "SPEED_UP_2_ATK_UP": "PHYSICAL", "ATK_DEF_SPEED_UP": "PHYSICAL", "TIDY_UP": "PHYSICAL",
    "CURSE": "PHYSICAL",
    "SP_ATK_UP": "SPECIAL", "SP_ATK_UP_2": "SPECIAL", "SP_ATK_SP_DEF_UP": "SPECIAL",
    "SP_ATK_SP_DEF_SPEED_UP": "SPECIAL",
    "ATK_SP_ATK_UP": "EITHER", "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN": "EITHER",
    "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP": "EITHER", "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2": "EITHER",
    "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP": "EITHER", "RANDOM_STAT_UP_2": "EITHER", "CRIT_UP_2": "EITHER",
    "SPEED_UP_2": "ANY", "AUTOTOMIZE": "ANY",
    "SP_DEF_UP_DOUBLE_ELECTRIC_POWER": "ELECTRIC",
}
BOOSTS_BY_NAME = {"MOVE_NO_RETREAT": "EITHER", "MOVE_TAKE_HEART": "SPECIAL"}


def boosts(const):
    m = moves().get(const)
    if not m or m["class"] != "STATUS":
        return None
    return BOOSTS_BY_NAME.get(const) or BOOSTS.get(m["effect"])


def _boosted(kind, const, holder):
    """0 if an attack is not one the setup boosts strongly enough to be worth
    it (R32_POWER by effective power, same-type attacks at one and a half),
    2 if it is and is of the holder's type, else 1."""
    m = moves()[const]
    if not attack(const, 1):
        return 0
    if kind in ("PHYSICAL", "SPECIAL") and m["class"] != kind:
        return 0
    if kind == "ELECTRIC" and m["type"] != "ELECTRIC":
        return 0
    stab = m["type"] in types_of(holder)
    if effective_power(const) * (1.5 if stab else 1.0) < R32_POWER:
        return 0
    return 2 if stab else 1


@functools.lru_cache(maxsize=None)
def check18(version):
    """[(species, level, MOVE_X, kind)]: R32, a setup move gained on a branch
    without a strong same-type attack it boosts, or two strong attacks it
    boosts (_boosted: "decent physical attacks", Ian on Altaria's Dragon
    Dance), held or gained by the end of the next split. A Ghost's Curse
    costs HP instead and is not judged."""
    found = {}
    last = len(SPLITS) - 1
    for fam in sorted(line_catches()):
        for path in line_paths(version, fam):
            evs = path_events(path)
            for lv, i, mv, _how in evs:
                kind = boosts(mv)
                holder = path[i].species
                if not kind or (mv == "MOVE_CURSE" and "GHOST" in types_of(holder)):
                    continue
                horizon = caps()[SPLITS[min(event_split(path, i, lv) + 1, last)]]
                grades = {m2: _boosted(kind, m2, path[j].species) for lv2, j, m2, _h in evs if lv2 <= horizon}
                ok = 2 in grades.values() or sum(1 for g in grades.values() if g) >= 2
                if not ok:
                    found.setdefault((holder, lv, mv), kind)
    return sorted((sp, lv, mv, k) for (sp, lv, mv), k in found.items())


@functools.lru_cache(maxsize=None)
def check19(version):
    """[(species, level, MOVE_X, accuracy)]: R37, an attack under
    R37_ACCURACY accuracy on an obtainable species' list above level 1 (the
    one-hit KO moves are check 16's)."""
    out = []
    for sp in sorted(b6.obtainable()):
        for lv, m in learnset(version, sp):
            mm = moves().get(m)
            if lv >= 2 and mm and mm["class"] != "STATUS" and mm["accuracy"] \
                    and mm["accuracy"] < R37_ACCURACY and not ohko(m):
                out.append((sp, lv, m, mm["accuracy"]))
    return out


@functools.lru_cache(maxsize=None)
def know_move_evolutions():
    """[(pre, MOVE_X, target)]: every evolution that needs a known move, from
    the records (the dex's own reading drops the move)."""
    out = []
    for sp in sorted(species_set()):
        raw = pokedex._read(data.ROOT, f"res/pokemon/{pokedex.folder_of(sp)}/data.json") or {}
        for entry in raw.get("evolutions") or []:
            if entry and entry[0] == "EVO_LEVEL_KNOW_MOVE":
                mv = next((x for x in entry if isinstance(x, str) and x.startswith("MOVE_")), None)
                into = [x for x in entry if isinstance(x, str) and x.startswith("SPECIES_")]
                if mv and into:
                    out.append((sp, mv, into[-1]))
    return out


@functools.lru_cache(maxsize=None)
def check20(version):
    """[(pre, MOVE_X, target, how)]: every evolution that needs a known move,
    with how the player can first have the move: by level-up (the split), by
    TM or tutor only, or not at all; it fails unless level-up reaches it or
    the target has another way in from the same stage."""
    owned = b6.obtainable()
    machines = pokedex.machines(data.ROOT)
    tutors = pool._tutor_splits()
    out = []
    for pre, mv, target in know_move_evolutions():
        if pre not in owned:
            continue
        chain = [pre] + list(pool.pre_evolutions().get(pre) or [])
        levels = [lv for s in chain for lv, m in learnset(version, s) if m == mv and 2 <= lv <= caps()[SPLITS[-1]]]
        caught = [lv for s, _sp, lv, _h, _p in catch_rows() if s == pre and mv in at_capture(version, pre, lv)]
        if levels or caught:
            how = f"level-up, {split_of_level(min(levels + caught))}'s split"
        else:
            rec = pokedex.load(data.ROOT, pre) or {}
            tm = [_machine_splits()[machines[l]][0] for l in rec.get("by_tm") or []
                  if machines.get(l) == mv and mv in _machine_splits()]
            tu = [tutors[mv]] if mv in (rec.get("by_tutor") or []) and mv in tutors else []
            how = f"TM or tutor only, {min(tm + tu, key=si)}'s split" if tm or tu else "unreachable"
        other = any(t == target for _n, _i, t in pool.evolutions(pre)) and \
            any(e["into"] == target and e["method"] != "LEVEL_KNOW_MOVE"
                for e in (pokedex.load(data.ROOT, pre) or {}).get("evolutions", []))
        ok = how.startswith("level-up") or other
        out.append((pre, mv, target, how + ("; another evolution reaches it" if other else ""),
                    "pass" if ok else "fail"))
    return out


@functools.lru_cache(maxsize=None)
def check21(version):
    """{final species: [moves]}: the real moves (counts()) each branch's final
    form learns by level-up from LATE_FROM to the League's cap (2026-09-28)."""
    out = {}
    for final, (_fam, path) in _final_paths(version).items():
        out[final] = tuple(m for lv, i, m, how in path_events(path)
                           if how == "level-up" and i == len(path) - 1 and lv >= LATE_FROM and counts(m))
    return out


@functools.lru_cache(maxsize=None)
def check22(version):
    """{rule: [(species, detail)]}: list hygiene and fit. Two moves on one
    level (above 1), an entry past the League's cap, a move twice on one list
    above level 1; a trainer-only move (R26) a wild catch would know among its
    four; a catch-only move (False Swipe) after Fantina's split; more than
    RECOVERY_MOST recovery moves on a list (Ian, 2026-10-06, the exam's
    regressions); and, for information, the level-0 (on evolving) entries,
    which are used sparingly."""
    top = caps()[SPLITS[-1]]
    late = caps()[CATCH_ONLY_UNTIL]
    out = {"two on one level": [], "past the League": [], "twice on a list": [],
           "trainer-only move a wild catch knows": [], "catch-only move after Fantina's split": [],
           "more than two recovery moves": [], "on evolving": []}
    wild = {"wild", "surf", "old_rod", "good_rod", "super_rod", "honey"}
    for sp in sorted(b6.obtainable()):
        lst = learnset(version, sp)
        lv_count = collections.Counter(lv for lv, _m in lst if lv >= 2)
        mv_count = collections.Counter(m for lv, m in lst if lv >= 2)
        out["two on one level"] += [(sp, lv) for lv, n in sorted(lv_count.items()) if n > 1]
        out["past the League"] += [(sp, f"{move_name(m)} {lv}") for lv, m in lst if lv > top]
        out["twice on a list"] += [(sp, move_name(m)) for m, n in sorted(mv_count.items()) if n > 1]
        out["on evolving"] += [(sp, move_name(m)) for lv, m in lst if lv == 0]
        out["catch-only move after Fantina's split"] += [(sp, f"{move_name(m)} {lv}") for lv, m in lst
                                                         if m in CATCH_ONLY and lv > late]
        heal = sorted({m for lv, m in lst if lv >= 2 and m in moves() and moves()[m]["effect"] in RECOVERY_EFFECTS})
        if len(heal) > RECOVERY_MOST:
            out["more than two recovery moves"].append((sp, ", ".join(move_name(m) for m in heal)))
    for sp, _s, lv, how, _p in catch_rows():
        if how in wild and sp in species_set():
            for m in at_capture(version, sp, lv):
                if m in TRAINER_ONLY:
                    out["trainer-only move a wild catch knows"].append((sp, f"{move_name(m)} at {lv}"))
    out["trainer-only move a wild catch knows"] = sorted(set(out["trainer-only move a wild catch knows"]))
    return out


BRANCH_PARITY = 0.8     # the weakest branch's kit worth, as a share of the strongest's


def move_worth(const, holder):
    """A move's worth in one Pokemon's kit, for branch parity: an attack's
    effective power with the same-type bonus and the share of the holder's
    better attacking stat it uses; a utility move's tier rank times seven
    (a good move 35, an incredible one 49)."""
    if damaging(const) and effective_power(const) > 0:
        m = moves()[const]
        atk, spa = attack_stats(holder)
        use = atk if m["class"] == "PHYSICAL" else spa
        stab = 1.5 if m["type"] in types_of(holder) else 1.0
        return effective_power(const) * stab * use / max(atk, spa, 1)
    t = tier(const)
    return t[0] * 7 if t and utility(const) else 0.0


def kit_worth(held, holder):
    """The worth of the best four moves a Pokemon holds."""
    return sum(sorted((move_worth(m, holder) for m in set(held)), reverse=True)[:4])


@functools.lru_cache(maxsize=None)
def check24(version):
    """[(stage, choice split, {branch: worth}, verdict)]: branch parity (Ian's
    exam verdict on Koffing, 2026-10-06: branches of one line are close in
    worth by the split where the player chooses between them). For each
    stage the player can evolve two or more ways, at the cap of the split by
    which every branch is open, each branch's kit (kit_worth of what its path
    holds by then) is at least BRANCH_PARITY of the strongest branch's."""
    out = []
    for fam in sorted(line_catches()):
        groups = collections.defaultdict(dict)
        for path in line_paths(version, fam):
            for i in range(len(path) - 1):
                key = tuple(st.species for st in path[:i + 1])
                groups[key].setdefault(path[i + 1].species, path)
        for key, branches in sorted(groups.items()):
            if len(branches) < 2:
                continue
            choice = max(si(p[len(key)].split) for p in branches.values())
            cap = caps()[SPLITS[choice]]
            worth = {t: round(kit_worth([m for _lv, _j, m, _h in path_events(p, cap)], t), 1)
                     for t, p in branches.items()}
            best = max(worth.values()) or 1
            ok = min(worth.values()) >= BRANCH_PARITY * best
            out.append((key[-1], SPLITS[choice], worth, "pass" if ok else "fail"))
    return out


GEN4_LAST_ID = 467      # Shadow Force, the last move Platinum has


@functools.lru_cache(maxsize=None)
def check23(version):
    """{family: [moves]}: R16, the moves from after Generation 4 a line
    learns by level-up or knows at capture on any of its paths; a line with
    none fails (Ian on Onix: "all 3 pokemon so far have 0 newer gen moves")."""
    out = {}
    for fam in sorted(line_catches()):
        got = []
        for path in line_paths(version, fam):
            for _lv, _i, mv, _how in path_events(path):
                if (moves()[mv].get("id") or 0) > GEN4_LAST_ID and counts(mv) and mv not in got:
                    got.append(mv)
        out[fam] = tuple(got)
    return out


# ---- the rules' report ----------------------------------------------------------------------------

def _fails(version):
    """{check number: (failing, judged, unit)} for checks 7 to 22."""
    c7, c8, c9, c10, c12, c14 = (check7(version), check8(version), check9(version), check10(version),
                                 check12(version), check14(version))
    c20 = check20(version)
    c21 = check21(version)
    c16 = check16(version)
    c22 = check22(version)
    return {
        7: (sum(r["verdict"] == "fail" for r in c7.values()), len(c7), "lines"),
        8: (sum(r["verdict"] == "fail" for r in c8.values()), len(c8), "stages"),
        9: (sum(r["verdict"] == "fail" for r in c9.values()), len(c9), "lines"),
        10: (sum(r["verdict"] == "fail" for r in c10.values()), len(c10), "branches"),
        11: (len(check11(version)), None, "entries"),
        12: (sum(r["verdict"] == "fail" for r in c12.values()), len(c12), "branches"),
        13: (len(check13(version)), None, "pairs, for information"),
        14: (sum(r["verdict"] == "fail" for r in c14.values()), len(c14), "stages"),
        15: (len(check15(version)), None, "species"),
        16: (sum(1 for _sp, w, _m, _r in c16 if w.startswith("level")), None, "level-up entries"),
        17: (len(check17(version)), None, "entries"),
        18: (len(check18(version)), None, "entries"),
        19: (len(check19(version)), None, "entries"),
        20: (sum(r[4] == "fail" for r in c20), len(c20), "evolutions"),
        21: (sum(1 for ms in c21.values() if not ms), len(c21), "final forms"),
        22: (sum(len(v) for k, v in c22.items() if k != "on evolving"), None, "entries"),
        23: (sum(1 for ms in check23(version).values() if not ms), len(check23(version)), "lines"),
        24: (sum(1 for r in check24(version) if r[3] == "fail"), len(check24(version)), "choices of branch"),
    }


RULES = {7: "R1, five or six moves by the first split's cap, at most one filler",
         8: "R2, two new moves per band of eight levels a stage is held through",
         9: "R4, the first coverage move by the second split",
         10: "R5, three coverage types over the game (two for a very strong line)",
         11: "R6, no move dominated by a stronger one already had",
         12: "R7, a good utility move by the second split (two over the game if less offensive)",
         13: "R8, choices inside one split (for information: Ian, 2026-10-06, they cost the player nothing)",
         14: "R11, an attack of each of the stage's types within a split",
         15: "R21, Baton Pass only with a boost to pass",
         16: "R24, Protect and kin, Double Team, Ingrain, one-hit KO moves and removed moves off the lists",
         17: "R25, no move lost below the level a stage is first had at",
         18: "R32, a setup move only beside an attack it boosts",
         19: "R37, no attack under 90% accuracy",
         20: "Every evolution that needs a known move reachable by level-up",
         21: "A real level-up move from 61 on each final form",
         22: "List hygiene: one move a level, none past 78, no move twice",
         23: "R16, a move from after Generation 4 on every line",
         24: "Branches of one line close in worth where the player chooses (Ian, 2026-10-06)"}


def _names(items, n=12):
    items = list(items)
    more = f", and {len(items) - n} more" if len(items) > n else ""
    return ", ".join(items[:n]) + more


def rules_report(out=sys.stdout, worst=12):
    """Checks 7 to 22 in Markdown: the counts side by side, then each
    check's failures by name, the second version first."""
    p = lambda *a: print(*a, file=out)
    A, B = VERSIONS
    fa, fb = _fails(A), _fails(B)
    p(f"| Check | Rule | {LABELS[A]} | {LABELS[B]} |\n|---|---|---|---|")
    for k in sorted(RULES):
        cell = lambda f: f"{f[k][0]} of {f[k][1]} {f[k][2]} fail" if f[k][1] is not None \
            else f"{f[k][0]} {f[k][2]}"
        p(f"| {k} | {RULES[k]} | {cell(fa)} | {cell(fb)} |")
    for v in (B, A):
        L = LABELS[v]
        p(f"\n### {L}: the failures by name\n")
        c7 = check7(v)
        fails = sorted((r for r in c7.values() if r["verdict"] == "fail"),
                       key=lambda r: (si(r["split"]), len(r["moves"]) - len(r["filler"]), r["family"]))
        p(f"Check 7: " + _names(f"{_sp(r['family'])} ({r['split']}, {len(r['moves'])} moves, "
                                f"{len(r['filler'])} filler)" for r in fails[:worst * 3]) + ".")
        c8 = check8(v)
        fails = sorted((r for r in c8.values() if r["verdict"] == "fail"),
                       key=lambda r: (-len(r["short"]), r["species"]))
        p(f"\nCheck 8: " + _names(f"{_sp(r['species'])} ({', '.join(b + ': ' + str(len(r['bands'][b])) for b in r['short'])})"
                                 for r in fails[:worst * 3]) + ".")
        c9 = check9(v)
        fails = sorted((r for r in c9.values() if r["verdict"] == "fail"),
                       key=lambda r: (-(99 if r["gap"] is None else r["gap"]), r["family"]))
        p(f"\nCheck 9: " + _names(
            f"{_sp(r['family'])} ({'none by 78' if r['first'] is None else move_name(r['first'][2]) + ' at ' + str(r['first'][1])})"
            for r in fails[:worst * 3]) + ".")
        c10 = check10(v)
        fails = sorted((r for r in c10.values() if r["verdict"] == "fail"),
                       key=lambda r: (len(r["types"]), r["species"]))
        p(f"\nCheck 10: " + _names(
            f"{_sp(r['species'])} ({len(r['types'])}; Kaizo {len(r['kaizo'])})" for r in fails[:worst * 3]) + ".")
        p(f"\nCheck 11: " + _names(f"{_sp(sp)}'s {move_name(mv)} {lv} (after {move_name(n)})"
                                  for sp, lv, mv, n in check11(v)[:worst * 3]) + ".")
        c12 = check12(v)
        fails = sorted((r for r in c12.values() if r["verdict"] == "fail"), key=lambda r: r["species"])
        p(f"\nCheck 12: " + _names(f"{_sp(r['species'])} ({len(r['early'])} early, {len(r['total'])} in all)"
                                  for r in fails[:worst * 3]) + ".")
        p(f"\nCheck 13: " + _names(
            f"{_sp(pre)} to {_sp(t)}: {move_name(m)} {a}" + (f" and {b}" if b else "") + f" ({kind})"
            for kind, pre, t, m, a, b in check13(v)[:worst * 3]) + ".")
        c14 = check14(v)
        fails = sorted((r for r in c14.values() if r["verdict"] == "fail"), key=lambda r: (si(r["split"]), r["species"]))
        p(f"\nCheck 14: " + _names(f"{_sp(r['species'])} ({', '.join(t.title() for t in r['missing'])})"
                                  for r in fails[:worst * 3]) + ".")
        p(f"\nCheck 15: " + (_names(_sp(s) for s in check15(v)) or "none") + ".")
        lv16 = [(sp, w, m) for sp, w, m, _r in check16(v) if w.startswith("level")]
        p(f"\nCheck 16, level-up entries: " + (_names(f"{_sp(sp)} {move_name(m)} ({w})" for sp, w, m in lv16[:worst * 3]) or "none") + ".")
        p(f"\nCheck 17: " + (_names(f"{_sp(sp)}'s {move_name(m)} {lv} (had from {lo})"
                                    for sp, lv, m, lo in check17(v)[:worst * 3]) or "none") + ".")
        p(f"\nCheck 18: " + (_names(f"{_sp(sp)}'s {move_name(m)} {lv}" for sp, lv, m, _k in check18(v)[:worst * 3]) or "none") + ".")
        p(f"\nCheck 19: " + (_names(f"{_sp(sp)}'s {move_name(m)} {lv} ({a}%)"
                                    for sp, lv, m, a in check19(v)[:worst * 3]) or "none") + ".")
        p(f"\nCheck 20: " + "; ".join(f"{_sp(pre)} to {_sp(t)} by {move_name(m)}: {how} ({verdict})"
                                     for pre, m, t, how, verdict in check20(v)) + ".")
        c21 = check21(v)
        p(f"\nCheck 21: " + (_names(_sp(s) for s, ms in sorted(c21.items()) if not ms) or "none") + ".")
        c22 = check22(v)
        p(f"\nCheck 22: " + "; ".join(f"{k} {len(rows)}" for k, rows in c22.items()) + ".")
        p(f"\nCheck 23: " + (_names(_sp(f) for f, ms in check23(v).items() if not ms) or "none") + ".")
        p(f"\nCheck 24: " + (_names(
            f"{_sp(st)} in {split}'s split ({', '.join(_sp(t) + ' ' + str(w) for t, w in sorted(ws.items()))})"
            for st, split, ws, verdict in check24(v) if verdict == "fail") or "none") + ".")
    tm16 = [(sp, w, m) for sp, w, m, _r in check16(A) if not w.startswith("level")]
    p(f"\nCheck 16 on the TM and tutor lists, the same in both (for the TM pass): {len(tm16)} entries, "
      + _names(f"{_sp(sp)} {move_name(m)} ({w})" for sp, w, m in tm16) + ".")


def rules_summary(out=sys.stdout):
    for v in VERSIONS:
        f = _fails(v)
        print(f"{LABELS[v]:8} " + "  ".join(f"{k}:{f[k][0]}" + (f"/{f[k][1]}" if f[k][1] is not None else "")
                                           for k in sorted(f)), file=out)


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
    """Checks 1, 4 and 5's tables, in Markdown, the two versions side by side."""
    p = lambda *a: print(*a, file=out)
    A, B = VERSIONS
    LA, LB = LABELS[A], LABELS[B]
    p("### Check 1 counts\n")
    p(f"| | {LA} | {LB} |\n|---|---|---|")
    c = {v: check1_counts(v) for v in VERSIONS}
    for key, label in (("stages", "Stages the player can have by the League"),
                       ("pass", "Pass: an own-type attack within a split"),
                       ("fail", "Fail: two splits or more without one"),
                       ("never", "of which none by the League's cap"),
                       ("exempt", "Exempt: can evolve by the end of Gardenia's split"),
                       ("lines", "Lines"), ("lines_failing", "Lines with a failing stage"),
                       ("tm_closes", "Failing stages a TM or tutor would close in time")):
        p(f"| {label} | {c[A][key]} | {c[B][key]} |")
    p("\n### Check 1 by the split the stage is first had in\n")
    p(f"| Split | {LA} pass | {LA} fail | {LB} pass | {LB} fail |\n|---|---|---|---|---|")
    for split in SPLITS:
        cells = []
        for v in VERSIONS:
            rows = [r for r in check1(v).values() if r["split"] == split]
            cells += [sum(r["verdict"] == "pass" for r in rows), sum(r["verdict"] == "fail" for r in rows)]
        p(f"| {split} | " + " | ".join(str(x) for x in cells) + " |")
    p("\n### Check 1: every stage that fails in either version, worst first\n")
    p(f"| Stage | First had | Route ({LA}'s) | {LA}: first own-type attack | Gap | "
      f"{LB}: first own-type attack | Gap | Earliest TM or tutor |")
    p("|---|---|---|---|---|---|---|---|")
    ra, rb = check1(A), check1(B)
    failing = {s for s, r in ra.items() if r["verdict"] == "fail"} | \
        {s for s, r in rb.items() if r["verdict"] == "fail"}
    worst = lambda r: 99 if r is None or r["gap"] is None else r["gap"]
    for s in sorted(failing, key=lambda s: (-max(worst(ra.get(s)), worst(rb.get(s))), -worst(ra.get(s)),
                                            si((ra.get(s) or rb.get(s))["split"]), s)):
        r, w = ra.get(s), rb.get(s)
        tm = tm_rescue(s)
        tm_text = f"{tm[1]} {move_name(tm[2])} ({tm[0]})" if tm else "none"
        mark = lambda x: "not had" if x is None else (_gap(x) if x["verdict"] == "fail" else f"{_gap(x)}, passes")
        first = r or w
        p(f"| {_sp(s)} | {first['split']} | {_route(first)} | {_first(r) if r else 'not had'} | {mark(r)} | "
          f"{_first(w) if w else 'not had'} | {mark(w)} | {tm_text} |")
    fixed = [s for s, r in ra.items() if r["verdict"] == "fail" and (rb.get(s) or {}).get("verdict") != "fail"]
    broke = [s for s, r in rb.items() if r["verdict"] == "fail" and (ra.get(s) or {}).get("verdict") != "fail"]
    p(f"\n{LB} mends {len(fixed)}: {', '.join(_sp(s) for s in sorted(fixed)) or 'none'}.")
    p(f"\n{LB} breaks {len(broke)}: {', '.join(_sp(s) for s in sorted(broke)) or 'none'}.")
    p("\n### Catches that know no attack at capture\n")
    bare = {v: bare_captures(v) for v in VERSIONS}
    empty = {v: sum(1 for b in bare[v].values() if not b[3]) for v in VERSIONS}
    p(f"{LA}: {len(bare[A])} species, {empty[A]} of them with no move at all; "
      f"{LB}: {len(bare[B])}, {empty[B]} with no move at all.\n")
    p(f"| Pokemon | {LA} | {LB} |\n|---|---|---|")
    for sp in sorted(set(bare[A]) | set(bare[B]),
                     key=lambda s: (min(si(bare[v][s][0]) for v in VERSIONS if s in bare[v]), s)):
        cells = []
        for v in VERSIONS:
            b = bare[v].get(sp)
            cells.append(f"{b[2]}, {b[1]} ({b[0]}): {', '.join(move_name(m) for m in b[3]) or 'no move'}"
                         if b else "has an attack")
        p(f"| {_sp(sp)} | {cells[0]} | {cells[1]} |")
    p("\n### Check 4: fixed and level damage by the end of Gardenia's split\n")
    early = {v: check4_early(v) for v in VERSIONS}
    keys = sorted(set(early[A]) | set(early[B]),
                  key=lambda k: (min(si(early[v][k][0]) for v in VERSIONS if k in early[v]), k))
    p(f"{LA}: {len(early[A])} entries on {len({k[0] for k in early[A]})} species; "
      f"{LB}: {len(early[B])} entries on {len({k[0] for k in early[B]})} species.\n")
    p(f"| Pokemon | Move | {LA} | {LB} | Ruling |\n|---|---|---|---|---|")
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
                rule.append(f"{LABELS[v]} {st}")
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
      f"({LA} {len(nxt[A])}, {LB} {len(nxt[B])}): " + "; ".join(
          f"{_sp(k[0])} {move_name(k[1])} {e[2]} at {e[1]}"
          + ("" if nxt[B].get(k) == e else
             f" ({LB}: {nxt[B][k][2]} at {nxt[B][k][1]})" if k in nxt[B] else f" ({LB}: not by then)")
          for k, e in sorted(nxt[A].items(), key=lambda kv: (kv[1][1], kv[0]))) + ".")
    p("\n### Check 4: one-hit KO moves on a player list\n")
    p(f"| Pokemon | Move | {LA} | {LB} |\n|---|---|---|---|")
    oh = {v: {(sp, mv): how for sp, mv, how in check4_ohko(v)} for v in VERSIONS}
    for k in sorted(set(oh[A]) | set(oh[B])):
        p(f"| {_sp(k[0])} | {move_name(k[1])} | {oh[A].get(k, 'not on its lists')} | "
          f"{oh[B].get(k, 'not on its lists')} |")
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
    p(f"| Rule | {LA} | {LB} |\n|---|---|---|")
    wx = {v: lint_weather(v) for v in VERSIONS}
    for kind, label in (("moves", "Weather moves on an obtainable line's lists"),
                        ("abilities", "Weather abilities in an obtainable line's regular slots")):
        p(f"| {label} | {len(wx[A][kind])} | {len(wx[B][kind])} |")
    acc = lint_accuracy()
    bad_acc = [c for c, _n, _w, ok in acc if not ok]
    p(f"| Sleep moves, powders, Thunder Wave, Dark Void, Swagger off Generation 4 accuracy | "
      f"{len(bad_acc)} of {len(acc)} | {len(bad_acc)} of {len(acc)} |")
    tms = {v: lint_tms(v) for v in VERSIONS}
    p(f"| Ian's removed TMs still on the TM list | {len(tms[A])} of {len(REMOVED_TMS)} | "
      f"{len(tms[B])} of {len(REMOVED_TMS)} |")
    for v in VERSIONS:
        for kind in ("moves", "abilities"):
            if wx[v][kind]:
                p(f"\n{LABELS[v]} weather {kind}: " + ", ".join(
                    f"{_sp(sp)} {' '.join(str(x) for x in rest)}" for sp, *rest in wx[v][kind]))
    if bad_acc:
        p("\nOff Generation 4 accuracy: " + ", ".join(
            f"{move_name(c)} {n} (vanilla {w})" for c, n, w, ok in acc if not ok))
    for v in VERSIONS:
        if v == "v3":
            p(f"\nv3's TM pass draft ({v3_tm_set_size()} in its set) carries: "
              + (", ".join(move_name(mv) for _s, mv in tms[v]) if tms[v] else "none of them") + ".")
    p(f"\nThe tree's TM list carries: " + (", ".join(f"{label} {move_name(mv)}" for label, mv in tms[A])
                                           or "none of them") + ".")


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
    ap.add_argument("what", choices=["summary", "report", "rules", "rules-summary", "sheets", "lines"])
    args = ap.parse_args(argv)
    if args.what == "summary":
        summary()
    elif args.what == "report":
        report()
    elif args.what == "rules":
        rules_report()
    elif args.what == "rules-summary":
        rules_summary()
    elif args.what == "sheets":
        for path in write_sheets():
            print(f"wrote {os.path.relpath(path, data.ROOT)}")
    else:
        lines_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
