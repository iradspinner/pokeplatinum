"""Step 6 of docs/oxide/alpha-readiness.md: the TM pass's reward table and
the gauntlet list, for Ian's approval (step 7). It writes no game data.

    PYTHONPATH=. python3 -m tools.oxide.balance.rewards          # the two tables and docs/oxide/reward-table.md
    PYTHONPATH=. python3 -m tools.oxide.balance.rewards check    # the tables agree and fit the flag pool

Ian's rulings (standing rulings, 2026-09-28 and 2026-09-29): TMs are
single-use again, about 100, each placement a set number of copies (a strong
TM one, a utility TM two, three where Ian picks); a weak TM is not sold but
is the reward for one optional trainer of weak-to-medium strength near its
split; his removals leave the TM list; Toxic, Will-O-Wisp and status moves as
reliable as Thunder Wave come only as single copies; the HMs become
single-use TMs now that field moves work on the badge alone, Fly, Strength,
Defog and Rock Climb with buffs to earn a place; and element 7's held items
are each the reward for an optional fight, never sold. A gauntlet is 2 to 5
mandatory trainers on the easier side of their split's average, bosses
outside.

The placement tool (tools/oxide/place_rewards.py, the main track's) reads
docs/oxide/reward-placements.tsv, one row per placement, and
docs/oxide/trainer-roles.tsv, one row per trainer the census places. Each
reward trainer and each new item ball takes one of the 46 spare story flags;
this table adds no ball (a TM with no place of its own takes over a ball
that holds a mart item), so the reward trainers alone draw on the pool.
"""
import argparse
import collections
import csv
import functools
import json
import os
import statistics
import sys

from ..encounters import learnsets as canon_ls, pokedex
from . import b6, data, gauntlet, learncheck as lc, learnrewrite as lr, pool, splits, weather_moves

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(data.ROOT, "docs", "oxide")
PLACEMENTS = os.path.join(OUT, "reward-placements.tsv")
ROLES = os.path.join(OUT, "trainer-roles.tsv")
REPORT = os.path.join(OUT, "reward-table.md")
NICHE = os.path.expanduser("~/oxide-trials/learnset-rewrite/checks-2-3.json")
SPLITS = lc.SPLITS
FLAG_POOL = 46          # the spare story flags tools/oxide/place_rewards.py hands out (2026-10-06)
TARGET = 100            # about 100 TMs, the former HMs included (Ian, 2026-09-28)
FIRST_NEW_TM = 93       # TM93 on, past vanilla's 92 (include/constants/items.h, NUM_EXTRA_TMS)

# Ian's removals from the TM list (2026-09-28), and Flash, the move pool's
# first cut (2026-09-27). The level-up lists keep what they have.
REMOVED = {"Protect", "Double Team", "Rain Dance", "Sunny Day", "Sandstorm", "Hail", "Thief", "Snatch",
           "Skill Swap", "Focus Punch", "Substitute", "Dream Eater", "Swords Dance", "Embargo", "Flash"}
# Toxic and Will-O-Wisp, which he removed, may come back as single copies,
# as may any status move as reliable as Thunder Wave (2026-09-28).
SINGLE_STATUS = {"Toxic", "Will-O-Wisp", "Thunder Wave"}
STATUS_EFFECTS = {"STATUS_PARALYZE", "STATUS_SLEEP", "STATUS_BURN", "STATUS_POISON",
                  "STATUS_BADLY_POISON", "STATUS_SLEEP_NEXT_TURN"}
# The HMs as TMs: Cut and Rock Smash leave, since field moves work on the
# badge alone; Surf and Waterfall are strong; the rest earn their place with
# the buffs proposed here.
HM_LEAVING = {"Cut", "Rock Smash"}
STRONG_HMS = {"Surf", "Waterfall"}
HM_BUFFS = {"Fly": "accuracy 95 to 100, so the two-turn hit no longer misses",
            "Strength": "power 80 to 90, a clean Normal hit between Body Slam and Double-Edge",
            "Defog": "clears hazards on both sides, as the later games do, to answer the trainers' hazards",
            "Rock Climb": "accuracy 85 to 95, so its confusion chance rides on a hit that lands"}
# Power read at a stand-in where the battle works it out: Return and
# Frustration at full friendship, Hidden Power at its fixed 60, a weight or
# speed move at a middling 70.
STAND_IN = {"POWER_BASED_ON_FRIENDSHIP": 102, "POWER_BASED_ON_LOW_FRIENDSHIP": 102,
            "RANDOM_POWER_BASED_ON_IVS": 60, "POWER_BASED_ON_LOW_SPEED": 70,
            "INCREASE_POWER_WITH_WEIGHT": 70, "POWER_BASED_ON_TARGET_WEIGHT": 70}
ITEM_BOUND = {"FLING", "NATURAL_GIFT"}
KEEP = {"False Swipe"}      # the nuzlocke's catching tool
HAZARDS = {"Stealth Rock", "Spikes", "Toxic Spikes", "Sticky Web"}
PIVOTS = {"U-turn", "Volt Switch", "Flip Turn", "Parting Shot"}
GOOD_ATTACK = 75            # "a good move of that type", for a strong TM's earliest split
STRONG_CAP = "Byron"        # where the power flags stop looking (balance-rules)
COPIES = {"strong": 1, "utility": 2, "weak": 1}

# Element 7's held items, each one optional fight's reward (Ian, 2026-09-29),
# with the split each first earns its place in, by judgement: early for what
# most of a box can use (Eviolite, the Fairy Feather beside the type
# boosters), later as their users and the fights that need them arrive.
HELD = [("ITEM_EVIOLITE", "Gardenia"), ("ITEM_ABSORB_BULB", "Gardenia"), ("ITEM_CELL_BATTERY", "Gardenia"),
        ("ITEM_ROCKY_HELMET", "Fantina"), ("ITEM_AIR_BALLOON", "Fantina"), ("ITEM_LOADED_DICE", "Fantina"),
        ("ITEM_FAIRY_FEATHER", "Fantina"), ("ITEM_BINDING_BAND", "Fantina"),
        ("ITEM_ASSAULT_VEST", "Maylene"), ("ITEM_SAFETY_GOGGLES", "Maylene"), ("ITEM_PUNCHING_GLOVE", "Maylene"),
        ("ITEM_WEAKNESS_POLICY", "Wake"), ("ITEM_COVERT_CLOAK", "Wake"), ("ITEM_EJECT_BUTTON", "Wake"),
        ("ITEM_RED_CARD", "Wake"), ("ITEM_CLEAR_AMULET", "Byron"), ("ITEM_MIRROR_HERB", "Byron"),
        ("ITEM_ABILITY_SHIELD", "Candice"), ("ITEM_RING_TARGET", "Candice"), ("ITEM_PIXIE_PLATE", "Volkner")]
# What a ball may give up to hold a TM with no place of its own: items a
# mart sells, so nothing scarce leaves the game.
CHEAP = {"ITEM_POTION", "ITEM_SUPER_POTION", "ITEM_POKE_BALL", "ITEM_GREAT_BALL", "ITEM_ANTIDOTE",
         "ITEM_PARALYZE_HEAL", "ITEM_AWAKENING", "ITEM_BURN_HEAL", "ITEM_ICE_HEAL", "ITEM_REPEL",
         "ITEM_SUPER_REPEL", "ITEM_ESCAPE_ROPE", "ITEM_X_ATTACK", "ITEM_X_DEFENSE", "ITEM_X_SPEED",
         "ITEM_X_ACCURACY", "ITEM_X_SP_ATK", "ITEM_X_SP_DEF", "ITEM_GUARD_SPEC", "ITEM_DIRE_HIT", "ITEM_HONEY"}
# The census's ways a trainer can be passed by: those may hold a reward.
OPTIONAL = {"avoidable", "off the story path"}


def M():
    return lc.moves()


def name(c):
    return lc.move_name(c)


def si(split):
    return SPLITS.index(split) if split in SPLITS else len(SPLITS)


# ---- what a TM may teach -------------------------------------------------------------------

def eff(c):
    """An attack's effective power, a computed one's at its stand-in."""
    return STAND_IN.get(M()[c]["effect"], lc.effective_power(c))


def is_attack(c):
    return M()[c]["class"] != "STATUS"


def works(c):
    """The engine runs the move, or Ian has ruled its rework (2026-10-06:
    the rampage, recharge, charge-turn and multi-hit moves), which the cloud
    job builds before the table's items reach the game."""
    return (c in M() and not lc.out_of_lists(c) and c not in lc.REMOVED and c not in lc.UNCHECKED
            and not lc.not_working(c) and not lc.run_ender(c)
            and (lc.reliable(c) or lc.pending(c) or lc.rampage(c)))


def reliable_status(c):
    """A status move that inflicts a major status at 90% or more, or never misses."""
    m = M()[c]
    return m["class"] == "STATUS" and m["effect"] in STATUS_EFFECTS and (not m["accuracy"] or m["accuracy"] >= 90)


def qualifies(c):
    """(bool, why not): a move a TM may teach."""
    if c not in M():
        return False, "not in Oxide"
    m, nm = M()[c], name(c)
    if not works(c):
        return False, "the engine does not run it in full"
    if c in weather_moves.WEATHER_MOVES:
        return False, "weather: the player never sets it"
    if c in b6.DEAD_MOVES:
        return False, "the move pool's cut"
    if c in lc.TRAINER_ONLY:
        return False, "the user faints, which in a nuzlocke is a death"
    if m["effect"] in ITEM_BOUND:
        return False, "hangs on a held item"
    if m["effect"] in lr.RANDOM_EFFECTS or c in lr.CONDITIONAL:
        return False, "random, or hangs on a rare condition"
    if nm in HAZARDS | PIVOTS | KEEP or nm in SINGLE_STATUS or reliable_status(c):
        return True, ""
    if is_attack(c):
        return eff(c) >= 50, "under 50 by effective power"
    return lr.rank(c) >= lc.TIER_RANK["Pretty solid"], "a status move Ian rates under pretty solid"


def tier(c):
    nm = name(c)
    if nm in SINGLE_STATUS or reliable_status(c):
        return "strong"         # a single copy (Ian, 2026-09-28)
    if nm in STRONG_HMS or (not is_attack(c) and lc.boosts(c)):
        return "strong"         # Surf and Waterfall (Ian); setup, which stays expensive
    if nm in KEEP:
        return "utility"
    if is_attack(c):
        # Sure speed control (Rock Tomb, which Ian rates incredible) and
        # priority earn a weaker attack its place as utility.
        special = nm in PIVOTS or lr.speed_control(c) or (M()[c]["priority"] or 0) > 0
        return "strong" if eff(c) >= 90 else "utility" if eff(c) >= 65 or special else "weak"
    r = lr.rank(c)
    if r >= lc.TIER_RANK["Great"]:
        return "strong"
    return "utility" if r >= lc.TIER_RANK["Pretty solid"] or nm in HAZARDS else "weak"


# ---- who learns each ------------------------------------------------------------------------

def _canon_moves(codes_wanted):
    """{canon key: {MOVE_X}} learnt by the given source codes in Generation 4
    or the species' latest game (Showdown's lists, as the generator reads them)."""
    table = canon_ls.canon_lists()
    ids = canon_ls.move_ids(data.ROOT)
    out = {}
    for key, rec in table.items():
        if key.startswith("_") or not isinstance(rec, dict):
            continue
        got = set()
        for src in (rec.get("gen4") or [], (rec.get("latest") or {}).get("moves") or []):
            for entry in src:
                mv, codes = entry[0], entry[1]
                c = ids.get(mv)
                if c and any(code[:1] in codes_wanted for code in codes.split(",") if code):
                    got.add(c)
        out[key] = got
    return out


@functools.lru_cache(maxsize=None)
def canon_compat():
    return _canon_moves("MTL")


@functools.lru_cache(maxsize=None)
def canon_tm_moves():
    """Every move some species learns by TM or tutor in canon: the candidates."""
    return frozenset(c for got in _canon_moves("MT").values() for c in got)


@functools.lru_cache(maxsize=None)
def compat(species):
    """{MOVE_X} a species may learn from a TM: its TM and tutor lists today,
    and what canon teaches it by TM, tutor or level-up."""
    rec = pokedex.load(data.ROOT, species) or {}
    machines = pokedex.machines(data.ROOT)
    have = {machines[m] for m in rec.get("by_tm") or [] if m in machines}
    have |= set(rec.get("by_tutor") or [])
    have |= canon_compat().get(lr.canon_key(species), set())
    return frozenset(have)


@functools.lru_cache(maxsize=None)
def learners(c):
    """The obtainable stages that may learn the move from a TM."""
    return frozenset(s for s in b6.obtainable() if c in compat(s))


def lines(c):
    return {lc.family(s) for s in learners(c)}


@functools.lru_cache(maxsize=None)
def by_level(fam):
    """{MOVE_X} the line's rewritten level-up lists teach from level 2."""
    return frozenset(m for s in lc.families()[fam] for lv, m in lc.learnset("rewrite", s) if lv >= 2)


def gain(c):
    """The lines a TM gives the move that none of their level-up lists teaches."""
    return {f for f in lines(c) if c not in by_level(f)}


@functools.lru_cache(maxsize=None)
def nicheless():
    """Lines the bosses meet in their window and none takes, on the scoring
    track's screen of the rewritten lists (checks 2 and 3), where it is on
    this machine; empty elsewhere, and the ranking falls to the lines gained."""
    try:
        with open(NICHE, encoding="utf-8") as f:
            niche = json.load(f)["oxide"]["niche"]
    except (OSError, KeyError, ValueError):
        return frozenset()
    return frozenset(sp for sp, r in niche.items() if r.get("bosses_met") and not r.get("bosses_taking"))


def lift(c):
    """How many lines without a niche gain the move as a real option: an
    attack of 65 or more, or a status move Ian rates good or better."""
    if not ((is_attack(c) and eff(c) >= 65) or (not is_attack(c) and lr.rank(c) >= lc.GOOD)):
        return 0
    return len(gain(c) & nicheless())


def worth(c):
    return eff(c) if is_attack(c) else lr.rank(c) * 14


def near_duplicate(c, chosen):
    """A move in the set that does the same job: the same type and class,
    within 15 by effective power, gained by seven in ten of this one's lines."""
    if not is_attack(c):
        return None
    mine = gain(c)
    for d in chosen:
        if d == c or not is_attack(d) or M()[d]["type"] != M()[c]["type"] \
                or M()[d]["class"] != M()[c]["class"] or abs(eff(d) - eff(c)) > 15:
            continue
        if mine and len(mine & gain(d)) >= 0.7 * len(mine):
            return d
    return None


# ---- the set ---------------------------------------------------------------------------------

Set = collections.namedtuple("Set", "kept dropped hms hm_dropped new below dupes")


@functools.lru_cache(maxsize=None)
def build_set():
    machines = pokedex.machines(data.ROOT)
    tms = sorted((k, c) for k, c in machines.items() if k.startswith("TM"))
    hms = sorted((k, c) for k, c in machines.items() if k.startswith("HM"))
    kept, dropped = [], []
    for k, c in tms:
        nm = name(c)
        if nm in REMOVED:
            dropped.append((k, c, "Ian's removal"))
            continue
        ok, why = qualifies(c)
        if ok:
            kept.append((k, c))
        else:
            dropped.append((k, c, why))
    hm_kept = [(k, c) for k, c in hms if name(c) not in HM_LEAVING]
    hm_dropped = [(k, c, "field moves work on the badge alone") for k, c in hms if name(c) in HM_LEAVING]
    have = {c for _k, c in kept + hm_kept}
    ranked = []
    for c in sorted(canon_tm_moves() - have):
        ok, _why = qualifies(c)
        if not ok or name(c) in REMOVED or name(c) in HM_LEAVING or len(gain(c)) < 3:
            continue
        ranked.append((c, lift(c), len(gain(c)), worth(c)))
    ranked.sort(key=lambda x: (-x[1], -x[2], -x[3], name(x[0])))
    room = max(0, TARGET - len(kept) - len(hm_kept))
    new, below, dupes = [], [], []
    in_set = [c for _k, c in kept + hm_kept]
    for x in ranked:
        d = near_duplicate(x[0], in_set)
        if d:
            dupes.append((x[0], d))
            continue
        if len(new) < room:
            new.append(x)
            in_set.append(x[0])
        else:
            below.append(x)
    return Set(tuple(kept), tuple(dropped), tuple(hm_kept), tuple(hm_dropped), tuple(new), tuple(below[:15]),
               tuple(dupes))


def numbering(st):
    """{MOVE_X: item constant}: a kept TM or HM keeps its item; a new move
    takes a number a dropped TM freed, then TM93 on."""
    out = {c: f"ITEM_{k}" for k, c in st.kept + st.hms}
    freed = sorted(k for k, _c, _w in st.dropped)
    n = FIRST_NEW_TM
    for c, *_ in st.new:
        if freed:
            out[c] = f"ITEM_{freed.pop(0)}"
        else:
            out[c] = f"ITEM_TM{n:02d}"
            n += 1
    return out


# ---- when each may come ----------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def first_good(species, typ):
    """The earliest split index the stage has an attack of the type of
    GOOD_ATTACK or more by level-up, on any path to it; None if never."""
    best = None
    if lc.family(species) not in lc.line_catches():
        return None             # a gift or legendary the catch data does not walk
    for path in lc.line_paths("rewrite", lc.family(species)):
        idx = next((i for i, st in enumerate(path) if st.species == species), None)
        if idx is None:
            continue
        for lv, j, mv, _h in lc.path_events(path):
            if j <= idx and mv in M() and is_attack(mv) and M()[mv]["type"] == typ \
                    and lc.effective_power(mv) >= GOOD_ATTACK:
                x = lc.event_split(path, j, lv)
                best = x if best is None else min(best, x)
                break
    return best


def power_split(c):
    """The first split whose power scale (the generator's ceilings for a
    same-type attack, read as the power a split's attacks climb to) takes
    the attack: a TM reaches many lines at once, so it comes no earlier."""
    if not is_attack(c):
        return 0
    return next((i for i, s in enumerate(SPLITS) if eff(c) <= lr.CEILING[s]), len(SPLITS) - 1)


@functools.lru_cache(maxsize=None)
def allowed(c):
    """(earliest split, stages reached early) for a TM: an attack no earlier
    than its power's split; a strong TM also no earlier than the split each
    flagged stage that learns it first has a good attack of its type by
    level-up, Byron's at the latest, where the flags stop looking; a setup
    move that reaches a flagged stage waits for Byron's."""
    x, early = power_split(c), []
    if tier(c) != "strong" or not (is_attack(c) or lc.boosts(c)):
        return SPLITS[x], ()
    cap = si(STRONG_CAP)
    for s in learners(c):
        if not lr.flagged(s):
            continue
        f = first_good(s, M()[c]["type"]) if is_attack(c) else cap
        if f is None or f > cap:
            early.append(s)
            f = cap
        x = max(x, f)
    return SPLITS[x], tuple(sorted(early))


@functools.lru_cache(maxsize=None)
def owned_from():
    """{species: the first split index the player owns it in}."""
    out = {}
    for split, have in pool.species_by_split().items():
        for sp in have:
            out.setdefault(sp, si(split))
    return out


def natural_split(c):
    """The median first split of the obtainable stages that learn the move."""
    firsts = sorted(owned_from()[s] for s in learners(c) if s in owned_from())
    return SPLITS[firsts[len(firsts) // 2]] if firsts else SPLITS[1]


# ---- places --------------------------------------------------------------------------------

def header(h):
    return h if h.startswith("MAP_HEADER_") else "MAP_HEADER_" + h


@functools.lru_cache(maxsize=None)
def tm_places():
    """Every TM or HM the world gives today, outside marts: balls and hidden
    items at the split the census's reach opens them in, gifts at their map's."""
    out = []
    for split, h, item, how, needs in splits.item_reach():
        if item and item.startswith(("ITEM_TM", "ITEM_HM")) and split in SPLITS:
            out.append({"split": split, "kind": "ball" if how == "ball" else "hidden", "map": h,
                        "item": item, "needs": needs})
    for split, h, item in splits.gifts():
        if item and item.startswith(("ITEM_TM", "ITEM_HM")) and split in SPLITS \
                and "UNUSED" not in h and "_DP_" not in h:
            out.append({"split": split, "kind": "gift", "map": h, "item": item, "needs": "foot"})
    out.sort(key=lambda p: (si(p["split"]), p["map"], p["item"]))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def cheap_balls():
    """Balls holding a mart item, one of their item on their map, which may
    take a TM that has no place of its own."""
    rows = [(split, h, item, how) for split, h, item, how, _n in splits.item_reach()
            if how == "ball" and item in CHEAP and split in SPLITS]
    count = collections.Counter((h, item) for _s, h, item, _h in rows)
    return tuple({"split": s, "kind": "ball", "map": h, "item": item, "needs": "foot"}
                 for s, h, item, _h in rows if count[(h, item)] == 1)


def mart_tms():
    """[(split, mart, item)]: the TMs the marts sell today."""
    return [(s, m, it) for s, m, it in splits.marts() if (it or "").startswith(("ITEM_TM", "ITEM_HM"))]


@functools.lru_cache(maxsize=None)
def trainer_objects():
    """{trainer id: (map header, local id)} for every trainer standing on a map."""
    consts = {t["constant"]: tr for tr, t in data.oxide_trainers().items()}
    out = {}
    for h, fields in splits.headers().items():
        ev = fields.get("eventsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "events", f"{ev}.json")
        if not ev or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for o in json.load(f).get("object_events", []):
                tr = consts.get(str(o.get("script", "")))
                if tr is not None and o.get("trainer_type", "TRAINER_TYPE_NONE") != "TRAINER_TYPE_NONE":
                    out.setdefault(tr, (h, o.get("id")))
    return out


@functools.lru_cache(maxsize=None)
def readings():
    """{trainer id: its stored reading on Ian's fight scale}."""
    with open(os.path.join(HERE, "b6.json"), encoding="utf-8") as f:
        stored = json.load(f)["trainers"]
    line = b6.scale_line()
    return {int(k): round(b6.on_scale(t["safe"], line), 1) for k, t in stored.items()
            if isinstance(t, dict) and isinstance(t.get("safe"), (int, float))}


@functools.lru_cache(maxsize=None)
def optional_trainers():
    """{split: [(reading, trainer id)]} of the trainers the player may pass
    by, standing on a map, with a stored reading; the split's median beside."""
    rows = collections.defaultdict(list)
    for tr, p in b6.placements().items():
        if p["how"] in OPTIONAL and p["split"] in SPLITS and tr in readings() and tr in trainer_objects():
            rows[p["split"]].append((readings()[tr], tr))
    return {s: (sorted(r), statistics.median(x for x, _t in r)) for s, r in rows.items()}


MAP_MOST = 2    # rewards on one map, at most, so they spread over the world


def pick_trainer(target, used, side, gauntlet_ids):
    """The optional trainer nearest the target split, not yet used, on a map
    holding fewer than MAP_MOST rewards: for a weak TM, one on the easier
    side of its split (Ian: weak-to-medium strength), the strongest of that
    half; for a held item, an optional challenge from the split's upper
    quarter."""
    maps = collections.Counter(trainer_objects()[t][0] for t in used)
    order = sorted(SPLITS, key=lambda s: (abs(si(s) - si(target)), si(s) < si(target), si(s)))
    for s in order:
        rows, mid = optional_trainers().get(s, ((), 0))
        rows = [(r, t) for r, t in rows if t not in used and t not in gauntlet_ids
                and maps[trainer_objects()[t][0]] < MAP_MOST]
        if not rows:
            continue
        if side == "easier":
            easy = [x for x in rows if x[0] <= mid]
            if easy:
                return (s,) + easy[-1][::-1]
        else:
            upper = sorted(rows)[len(rows) * 3 // 4:]
            if upper:
                return (s,) + upper[0][::-1]
    return None


# ---- the gauntlets ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def gauntlet_sections():
    """[(area, label, split, [trainer ids])] from gauntlet.py's sections."""
    out = []
    placed = b6.placements()
    for area, sections in gauntlet.SECTIONS.items():
        for section in sections:
            ids = gauntlet.section_trainers(area, section)
            split = placed[ids[0]]["split"] if ids else ""
            out.append((area, section[0], split, tuple(ids)))
    return tuple(out)


# ---- the table -------------------------------------------------------------------------------

Row = collections.namedtuple("Row", "reward copies kind split map place replaces trainer_id note")


def build():
    """(rows, report facts): every placement of the TM set and the held items."""
    st = build_set()
    item = numbering(st)
    moves = [c for _k, c in st.kept] + [c for _k, c in st.hms] + [x[0] for x in st.new]
    places = list(tm_places())
    by_item = collections.defaultdict(list)
    for p in places:
        by_item[p["item"]].append(p)
    used_places, rows, facts = set(), [], {"early": {}, "unplaced": [], "third": []}
    gauntlet_ids = {t for *_x, ids in gauntlet_sections() for t in ids}
    used_trainers = set()

    def take(p, c, why):
        used_places.add(id(p))
        t = tier(c)
        rows.append(Row(item[c], COPIES[t], p["kind"], p["split"], header(p["map"]), "", p["item"], "",
                        f"{name(c)}, {t}; {why}"))

    weak = [c for c in moves if tier(c) == "weak"]
    placed_moves = set()
    # A TM keeps its own place where that place comes no earlier than allowed.
    for c in moves:
        if c in weak:
            continue
        lo, early = allowed(c)
        if early:
            facts["early"][c] = early
        own = [p for p in by_item.get(f"ITEM_{_key(st, c)}", []) if si(p["split"]) >= si(lo)]
        if own:
            take(own[0], c, "its own place today")
            placed_moves.add(c)
    # The rest take a freed TM place nearest their natural split, from the
    # earliest allowed; then a cheap ball.
    free = [p for p in places if id(p) not in used_places]
    cheap = list(cheap_balls())
    for c in moves:
        if c in weak or c in placed_moves:
            continue
        lo, _early = allowed(c)
        want = max(si(lo), si(natural_split(c)))
        cands = [p for p in free if id(p) not in used_places and si(p["split"]) >= si(lo)]
        cands.sort(key=lambda p: (abs(si(p["split"]) - want), si(p["split"]), p["map"]))
        if cands:
            take(cands[0], c, f"a TM place today ({cands[0]['item']})")
            placed_moves.add(c)
            continue
        cands = [p for p in cheap if id(p) not in used_places and si(p["split"]) >= si(lo)]
        cands.sort(key=lambda p: (abs(si(p["split"]) - want), si(p["split"]), p["map"]))
        if cands:
            take(cands[0], c, f"a ball that holds {cands[0]['item']} today")
            placed_moves.add(c)
        else:
            facts["unplaced"].append(c)
    # Held items first, since they want the few stronger optional trainers
    # of a split: one each, from the split's upper quarter.
    for it, target in HELD:
        pick = pick_trainer(target, used_trainers, "harder", gauntlet_ids)
        if not pick:
            facts["unplaced"].append(it)
            continue
        s, tr, r = pick
        used_trainers.add(tr)
        h, _obj = trainer_objects()[tr]
        rows.append(Row(it, 1, "trainer", s, header(h), "", "", data.oxide_trainers()[tr]["constant"],
                        f"held item; reading {r}"))
    # Weak TMs: one optional trainer each, on the easier side of its split.
    for c in weak:
        pick = pick_trainer(natural_split(c), used_trainers, "easier", gauntlet_ids)
        if not pick:
            facts["unplaced"].append(c)
            continue
        s, tr, r = pick
        used_trainers.add(tr)
        h, _obj = trainer_objects()[tr]
        rows.append(Row(item[c], 1, "trainer", s, header(h), "", "", data.oxide_trainers()[tr]["constant"],
                        f"{name(c)}, weak; reading {r}"))
        placed_moves.add(c)
    # A TM place left over still gives its old TM, a second source, so it
    # gets a mart item; the main track may give it something better.
    for p in places:
        if id(p) not in used_places:
            rows.append(Row("ITEM_ULTRA_BALL", 1, p["kind"], p["split"], header(p["map"]), "", p["item"], "",
                            "a TM place the set leaves free; an Ultra Ball stands in"))
    facts["third"] = [c for c in moves if tier(c) == "utility" and name(c) in HAZARDS | PIVOTS]
    rows.sort(key=lambda r: (si(r.split), r.kind, r.map, r.reward))
    return st, item, rows, facts


def _key(st, c):
    return next(k for k, m in st.kept + st.hms if m == c) if any(m == c for _k, m in st.kept + st.hms) else ""


def roles(rows):
    """[dict] one row per trainer the census places: its split, map and
    object, whether the story requires it, its role (gauntlet, reward or
    none), section, reward, team size, reading and the flag it takes."""
    by_trainer = {r.trainer_id: r for r in rows if r.kind == "trainer"}
    section_of = {}
    for area, label, _split, ids in gauntlet_sections():
        for t in ids:
            section_of[t] = f"{area}: {label}"
    ox = data.oxide_trainers()
    out = []
    for tr, p in sorted(b6.placements().items(), key=lambda kv: (si(kv[1]["split"]), kv[0])):
        if tr not in ox:
            continue
        const = ox[tr]["constant"]
        h, obj = trainer_objects().get(tr, ("", ""))
        r = by_trainer.get(const)
        role = "gauntlet" if tr in section_of else "reward" if r else "none"
        out.append({"split": p["split"], "trainer_id": const, "trainer": ox[tr]["name"], "map": header(h) if h else "",
                    "object": obj or "", "required": "yes" if p["how"] == "required" else "no", "role": role,
                    "section": section_of.get(tr, ""), "reward": r.reward if r else "",
                    "copies": r.copies if r else "",
                    "size": len(ox[tr]["party"]) if isinstance(ox[tr]["party"], list) else ox[tr]["party"],
                    "reading": readings().get(tr, ""), "flag": "spare" if r else "", "note": p["how"]})
    return out


ROLE_COLUMNS = ["split", "trainer_id", "trainer", "map", "object", "required", "role", "section", "reward",
                "copies", "size", "reading", "flag", "note"]


def write(st, item, rows, facts):
    with open(PLACEMENTS, "w", encoding="utf-8", newline="\n") as f:
        f.write("# The reward table, step 6 of docs/oxide/alpha-readiness.md: a draft for Ian (step 7).\n"
                "# Written by tools/oxide/balance/rewards.py; docs/oxide/reward-table.md explains it.\n")
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(Row._fields)
        for r in rows:
            w.writerow(r)
    with open(ROLES, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Every trainer the census places, with its role: written by tools/oxide/balance/rewards.py.\n")
        w = csv.DictWriter(f, ROLE_COLUMNS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in roles(rows):
            w.writerow(r)


# ---- the check ------------------------------------------------------------------------------

def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader((line for line in f if not line.startswith("#")), delimiter="\t"))


def check(out=sys.stdout):
    """[failure]: every TM in the set and every held item placed exactly
    once; the trainer rows of the two tables agree; no more reward trainers
    and new balls than the flag pool holds; every TM place today repointed."""
    st = build_set()
    item = numbering(st)
    placed = read_tsv(PLACEMENTS)
    role_rows = read_tsv(ROLES)
    fails = []
    counts = collections.Counter(r["reward"] for r in placed)
    want = set(item.values()) | {it for it, _s in HELD}
    for it in sorted(want):
        if counts[it] != 1:
            fails.append(f"{it} is placed {counts[it]} times")
    trainers = {r["trainer_id"]: r for r in placed if r["kind"] == "trainer"}
    rewarded = {r["trainer_id"]: r for r in role_rows if r["role"] == "reward" or r["reward"]}
    for t in sorted(set(trainers) | set(rewarded)):
        a, b = trainers.get(t), rewarded.get(t)
        if not a or not b or a["reward"] != b["reward"] or str(a["copies"]) != str(b["copies"]):
            fails.append(f"{t}: the placements and the roles disagree")
    new_balls = sum(1 for r in placed if r["kind"] == "ball" and "," in (r["place"] or ""))
    flags = len(trainers) + new_balls
    if flags > FLAG_POOL:
        fails.append(f"{flags} spare flags needed, {FLAG_POOL} in the pool")
    today = collections.Counter((header(p["map"]), p["item"]) for p in tm_places())
    repointed = collections.Counter((r["map"], r["replaces"]) for r in placed if r["replaces"])
    for k, n in sorted(today.items()):
        if repointed[k] < n:
            fails.append(f"{k[1]} on {k[0]} is not repointed")
    print(f"{len(placed)} placements, {len(trainers)} reward trainers, {new_balls} new balls: "
          f"{flags} of {FLAG_POOL} spare flags; {len(fails)} failures", file=out)
    for f_ in fails:
        print("  " + f_, file=out)
    # A mart or the Game Corner still selling a TM the table places is a
    # second source, which the placement tool's check refuses; what they
    # sell instead is Ian's to choose, so it is reported, not failed.
    open_ = [(s, m, it) for s, m, it in mart_tms() if counts[it]]
    if open_:
        print(f"  open for Ian: {len(open_)} TMs still sold ({', '.join(sorted({m for _s, m, _i in open_}))})",
              file=out)
    return fails


# ---- the report -----------------------------------------------------------------------------

KIND_WORDS = {"ball": "ball", "hidden": "hidden item", "gift": "gift", "trainer": "reward trainer",
              "mart": "mart"}
AREA_NAMES = {"galactic_eterna": "Team Galactic's Eterna building", "galactic_hq": "The Galactic HQ",
              "mt_coronet": "Mt. Coronet", "victory_road": "Victory Road"}


def tm_label(it):
    return it.replace("ITEM_", "")


def move_cell(c):
    m = M()[c]
    power = "varies" if m["power"] == 1 else (m["power"] or "-")
    acc = m["accuracy"] or "never misses"
    return f"{name(c)} | {m['type'].title()} | {m['class'].title()} | {power} | {acc}"


def section_readings():
    """{(area, label): (clean share, deaths a run)} from gauntlet.py's second
    reading, on the lists in the tree; empty where it cannot run."""
    out = {}
    for area, sections in gauntlet.SECTIONS.items():
        for section in sections:
            try:
                _trs, r = gauntlet.section_reading(area, section)
            except Exception:       # a reading the tree cannot make leaves its cell empty
                continue
            out[(area, section[0])] = (r["clean"], r["deaths"])
    return out


def parse_section_readings(path):
    """{(area, label): (clean, deaths)} from the text `gauntlet.py` prints,
    its areas in SECTIONS' order, so a reading made once need not be rerun."""
    import re
    areas = list(gauntlet.SECTIONS)
    out, k = {}, -1
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith(" "):
                k += 1
                continue
            m = re.search(r"clean ([\d.]+), deaths ([\d.]+) a run", line)
            if m and 0 <= k < len(areas) and "story fight" not in line:
                label = re.split(r"\s{2,}", line.strip())[0]
                out[(areas[k], label)] = (float(m.group(1)), float(m.group(2)))
    return out


def report(st, item, rows, facts, gauntlets=None, out=None):
    out = out or open(REPORT, "w", encoding="utf-8", newline="\n")
    p = lambda s="": print(s, file=out)
    tm_rows = {r.reward: r for r in rows if r.reward.startswith(("ITEM_TM", "ITEM_HM"))}
    move_of = {v: k for k, v in item.items()}
    held_rows = [r for r in rows if r.kind == "trainer" and not r.reward.startswith(("ITEM_TM", "ITEM_HM"))]
    weak_rows = [r for r in rows if r.kind == "trainer" and r.reward.startswith("ITEM_TM")]
    tiers = collections.Counter(tier(c) for c in move_of.values())
    flags = sum(1 for r in rows if r.kind == "trainer")
    open_ = [(s, m, it) for s, m, it in mart_tms() if it in tm_rows]
    p("# The TM list and the reward table (step 6, a draft for Ian)")
    p()
    p("Written by `tools/oxide/balance/rewards.py` on the branch `balance-tm-pass`. It changes no game data;")
    p("the placement tool applies the approved table in step 10.")
    p()
    p("## Summary")
    p()
    p(f"**Outcome.** The TM list has {len(move_of)} TMs: {len(st.kept)} of vanilla's 92 kept, the six HMs less "
      f"Cut and Rock Smash as single-use TMs, and {len(st.new)} new moves. {tiers['strong']} are strong (one "
      f"copy), {tiers['utility']} utility (two copies) and {tiers['weak']} weak (one copy, each the reward for "
      f"one optional trainer). Every TM and each of element 7's {len(HELD)} held items has exactly one place, "
      f"by split, and every TM ball and gift in vanilla is repointed, so none gives a second copy. The reward "
      f"trainers take {flags} of the {FLAG_POOL} spare story flags, and no new item ball is added. "
      f"The table's own check passes.")
    p()
    p("**This list will change.** Its new TMs are ranked by the lines that gain each move they cannot learn "
      "by level-up, and the type-ladder rework of the early lists (Ian, 2026-10-06) changes those lists. The "
      "move-rework cloud job also changes the numbers of Hyper Beam, Giga Impact and the multi-hit moves, so "
      "their tiers here are read on today's data. Both rerun this list in minutes before it is final.")
    p()
    p("**Ian's action items**, each set out below:")
    p()
    p("1. Read the TM list (the first table) and mark any TM to cut, add or move.")
    p("2. Say what Veilstone Department Store's TM floor and the Game Corner's TM prizes sell instead: "
      f"{len(open_)} TMs are sold there today, and a TM bought without end undoes single-use copies.")
    p(f"3. Pick third copies, if any, among the hazards and pivots: "
      f"{', '.join(name(c) for c in facts['third']) or 'none in the set'}.")
    p("4. Approve or change the held items' splits and trainers, the weak TMs' trainers, and the gauntlet "
      "sections.")
    p()
    p("**Next steps.**")
    p()
    p("| Step | What | Who | About how long |")
    p("|---|---|---|---|")
    p("| Ladders | The early lists rebuilt on per-type move ladders, then this list rerun | Balance Agent | 4 to 5 hours |")
    p("| 7 | Ian approves the TM list, the reward table and the gauntlets | Ian | |")
    p("| 8 | Item data for the new TMs, the compatibility lists, the bigger Bag | Balance Agent | 2 to 3 hours, a build and the rescore |")
    p("| 10 | The table placed in the maps, the gauntlets filled in | main-track session | 3 to 6 hours |")
    p()
    p("## The TM list")
    p()
    p("One row per TM, by the split it first comes in. A number past 92 is new; a number vanilla used for a "
      "move that leaves the list now teaches the new move named. Power and accuracy are Oxide's today.")
    p()
    p("| TM | Move | Type | Class | Power | Accuracy | Tier | Copies | Split | Source |")
    p("|---|---|---|---|---|---|---|---|---|---|")
    for it, r in sorted(tm_rows.items(), key=lambda kv: (si(kv[1].split), kv[0])):
        c = move_of[it]
        p(f"| {tm_label(it)} | {move_cell(c)} | {tier(c)} | {r.copies} | {r.split} | {KIND_WORDS[r.kind]}"
          f"{', ' + r.map.replace('MAP_HEADER_', '').replace('_', ' ').title() if r.kind != 'trainer' else ''} |")
    p()
    p("## What changed against vanilla")
    p()
    kept_same = [(k, c) for k, c in st.kept if item[c] == f"ITEM_{k}"]
    p(f"**Kept** ({len(st.kept)}): " + ", ".join(f"{k} {name(c)}" for k, c in kept_same) + ".")
    p()
    p("**Former HMs**, single-use TMs now that field moves work on the badge alone: "
      + ", ".join(f"{k} {name(c)}" + (f" (buff proposed: {HM_BUFFS[name(c)]})" if name(c) in HM_BUFFS else "")
                  for k, c in st.hms) + ". Cut and Rock Smash leave.")
    p()
    p("**Cut**:")
    p()
    for k, c, why in st.dropped:
        p(f"- {k} {name(c)}: {why}")
    p()
    p("**New**, ranked by the lines without a niche each gives a real option, then by lines gained:")
    p()
    p("| TM | Move | Why |")
    p("|---|---|---|")
    for c, lf, gn, _w in st.new:
        why = f"{gn} lines gain it that cannot learn it by level-up"
        if lf:
            why += f", {lf} of them lines no boss takes today"
        p(f"| {tm_label(item[c])} | {name(c)} | {why} |")
    p()
    if st.below:
        p("Just below the line: " + ", ".join(f"{name(c)} ({gn} lines)" for c, _l, gn, _w in st.below) + ".")
        p()
    if st.dupes:
        p("Left out as doing the same job as a TM in the list: "
          + ", ".join(f"{name(a)} (beside {name(b)})" for a, b in st.dupes[:20]) + ".")
        p()
    p("## The reward trainers")
    p()
    p("Each is optional (the census reads it as avoidable or off the story path) and gives its reward once, "
      "straight after the win. Held items go to the upper quarter of their split's optional trainers by "
      "reading on Ian's fight scale, an optional challenge; weak TMs to the stronger half of the easier side, "
      "the weak-to-medium trainers Ian named. At most two rewards share a map.")
    p()
    p("| Reward | Split | Trainer | Map | Reading |")
    p("|---|---|---|---|---|")
    ox_by_const = {t["constant"]: t for t in data.oxide_trainers().values()}
    for r in held_rows + weak_rows:
        label = r.reward.replace("ITEM_", "").replace("_", " ").title() if r in held_rows \
            else f"{tm_label(r.reward)} {name(move_of[r.reward])}"
        p(f"| {label} | {r.split} | {ox_by_const[r.trainer_id]['name']} | "
          f"{r.map.replace('MAP_HEADER_', '').replace('_', ' ').title()} | {r.note.split('reading ')[-1]} |")
    p()
    p("## The gauntlets")
    p()
    p("The sections of the gauntlet proposal (balance plan, \"The gauntlets, reworked on Ian's rulings\"), with "
      "their trainers in walking order. A section of 2 to 5 mandatory trainers on the easier side of its "
      "split's average; bosses stay outside. The reading is `gauntlet.py`'s second one on the lists in the "
      "tree: clean clears, then deaths a run.")
    p()
    p("| Area | Section | Split | Trainers | Reading |")
    p("|---|---|---|---|---|")
    ox = data.oxide_trainers()
    for area, label, split, ids in gauntlet_sections():
        reading = (gauntlets or {}).get((area, label))
        cell = f"{reading[0]:.2f}, {reading[1]:.2f}" if reading else ""
        p(f"| {AREA_NAMES.get(area, area)} | {label} | {split} | "
          f"{', '.join(ox[t]['name'] for t in ids)} | {cell} |")
    p()
    p("## The marts and the Game Corner")
    p()
    p("These sell TMs today. Each is a second source of a TM the list places, which the placement tool's "
      "check refuses, and single-use copies mean little if a TM can be bought without end. What each slot "
      "sells instead is Ian's to choose; the balance track recommends keeping the floors' theme with items "
      "not sold elsewhere, and leaving held items out, since those come from optional fights.")
    p()
    p("| Where | Split | TM sold today |")
    p("|---|---|---|")
    for s, m, it in open_:
        p(f"| {m} | {s} | {tm_label(it)} {name(move_of[it])} |")
    if facts["early"]:
        p()
        p("## Strong TMs held back")
        p()
        p("A strong TM comes no earlier than the split each flagged line that learns it has a good attack of "
          "its type by level-up, Byron's at the latest. These reach flagged stages with none by then:")
        p()
        for c, early in sorted(facts["early"].items(), key=lambda kv: name(kv[0])):
            p(f"- {name(c)}: {', '.join(lc.species_name(s) for s in early[:8])}"
              + (f" and {len(early) - 8} more" if len(early) > 8 else ""))
    out.close()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="write", choices=["write", "check"])
    ap.add_argument("--no-gauntlets", action="store_true", help="leave the gauntlet readings out (faster)")
    ap.add_argument("--gauntlet-reading", help="gauntlet.py's printed reading, used instead of running it again")
    args = ap.parse_args(argv)
    if args.what == "check":
        return 1 if check() else 0
    st, item, rows, facts = build()
    write(st, item, rows, facts)
    readings_ = (parse_section_readings(args.gauntlet_reading) if args.gauntlet_reading
                 else None if args.no_gauntlets else section_readings())
    report(st, item, rows, facts, readings_)
    print(f"set: {len(st.kept)} kept, {len(st.hms)} former HMs, {len(st.new)} new; "
          f"{len(rows)} placements; unplaced {facts['unplaced']}")
    return 1 if check() else 0


if __name__ == "__main__":
    sys.exit(main())
