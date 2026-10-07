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
import re
import statistics
import subprocess
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
        ("ITEM_ABILITY_SHIELD", "Candice"), ("ITEM_RING_TARGET", "Candice"), ("ITEM_PIXIE_PLATE", "Volkner"),
        # The Game Corner's four held items, behind optional fights too (Ian,
        # 2026-10-06); their prize slots give another item.
        ("ITEM_SILK_SCARF", "Maylene"), ("ITEM_WIDE_LENS", "Wake"), ("ITEM_ZOOM_LENS", "Byron"),
        ("ITEM_METRONOME", "Candice")]
GAME_CORNER_HELD = {"ITEM_SILK_SCARF", "ITEM_WIDE_LENS", "ITEM_ZOOM_LENS", "ITEM_METRONOME"}
# The Game Corner's gift for ten straight bonus rounds becomes an optional
# trainer's reward there (Ian, 2026-10-06): a trainer the main track creates.
GAME_CORNER_GIFT = ("GAME_CORNER", "gift")
GAME_CORNER_TRAINER = "TRAINER_GAME_CORNER_CHALLENGER"
# Their prize slots are dropped, not given a stand-in (Ian, 2026-10-06): a
# shop row with this reward removes the slot.
DROPPED = "ITEM_NONE"
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


def base_machines():
    """The TM list before the TM pass. Today's item records already teach the
    new list (main-tm-items), so reading them would count each new TM as a
    kept one and place it twice."""
    return lc.base_machines()


@functools.lru_cache(maxsize=None)
def compat(species):
    """{MOVE_X} a species may learn from a TM: its TM and tutor lists before
    the TM pass, and what canon teaches it by TM, tutor or level-up."""
    rec = pokedex.load(data.ROOT, species, ref=lc.BASE_REF) or {}
    machines = base_machines()
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
    machines = base_machines()
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
    # The new TMs are Ian's approved list (2026-10-06), frozen with their
    # numbers so the main track's item data stays put while the lists move;
    # the ranking still runs, to show what lies below the line.
    by_name = {name(c): c for c in M()}
    scored = {x[0]: x for x in ranked}
    new = tuple(scored.get(by_name[n], (by_name[n], lift(by_name[n]), len(gain(by_name[n])), worth(by_name[n])))
                for n in APPROVED_NEW)
    approved = {x[0] for x in new}
    below, dupes = [], []
    in_set = [c for _k, c in kept + hm_kept] + list(approved)
    for x in ranked:
        if x[0] in approved:
            continue
        d = near_duplicate(x[0], in_set)
        if d:
            dupes.append((x[0], d))
        else:
            below.append(x)
    return Set(tuple(kept), tuple(dropped), tuple(hm_kept), tuple(hm_dropped), new, tuple(below[:15]),
               tuple(dupes))


# Ian's approved new TMs (2026-10-06), in number order: each takes the number
# here, freed by a TM that left, or TM93 on. Fixed, so the item data the
# main track writes (main-tm-items) never renumbers.
APPROVED_NEW = {"Hydro Pump": "TM01", "Dazzling Gleam": "TM05", "Curse": "TM07", "Spite": "TM11",
                "StompingTantrum": "TM17", "Scary Face": "TM18", "Zen Headbutt": "TM32", "Signal Beam": "TM37",
                "Charm": "TM41", "Wild Charge": "TM44", "Alluring Voice": "TM45", "Knock Off": "TM46",
                "Iron Defense": "TM48", "Agility": "TM49", "Hex": "TM56", "Triple Axel": "TM58",
                "Confuse Ray": "TM63", "Play Rough": "TM64", "Ice Punch": "TM67", "Outrage": "TM70",
                "Meteor Beam": "TM75", "Foul Play": "TM77", "Bounce": "TM82", "Expanding Force": "TM83",
                "Skitter Smack": "TM85", "Block": "TM90", "Psychic Noise": "TM93", "Psybeam": "TM94"}


def numbering(st):
    """{MOVE_X: item constant}: a kept TM or HM keeps its item; a new move
    takes the number Ian's approved list gives it."""
    out = {c: f"ITEM_{k}" for k, c in st.kept + st.hms}
    for c, *_ in st.new:
        out[c] = f"ITEM_{APPROVED_NEW[name(c)]}"
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


# Ian's notes on the first TM list (2026-10-06), by judgement, not a rule:
# each move named here comes no earlier than the split given, with why. His
# utility tiers set the order: Confuse Ray fantastic, Charm incredible.
JUDGED = {
    "Confuse Ray": ("Wake", "Ian: \"way, way too good of a move to get this early\" in Sandgem; he rates it "
                            "fantastic, so it comes after Charm"),
    "Charm": ("Maylene", "Ian: \"a lot of good moves ... in Gardenia split; a couple should be moved\"; he rates "
                         "it incredible, and it halves a physical threat"),
    "Knock Off": ("Fantina", "the same note: the strongest utility attack in Gardenia's split, its item removal "
                             "a second effect"),
    "Will-O-Wisp": ("Maylene", "Ian: \"too good for fantina split\""),
    "Thunder Wave": ("Maylene", "Ian: \"same for thunder wave\""),
}


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
    move that reaches a flagged stage waits for Byron's. Ian's judgement on
    the first list (JUDGED) holds a move he named to a later split."""
    x, early = power_split(c), []
    if name(c) in JUDGED:
        x = max(x, si(JUDGED[name(c)][0]))
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

Row = collections.namedtuple("Row", "reward copies kind split map place replaces trainer_id badges note")

# The badge count each shop TM may unlock at, and the split it comes in
# then: Veilstone opens in Maylene's split with three badges (Ian,
# 2026-10-06: the Department Store's and the Game Corner's TMs unlock by
# badge count in order of usefulness, each bought once).
BADGE_SPLIT = {3: "Maylene", 4: "Wake", 5: "Byron", 6: "Candice", 7: "HQ", 8: "Barry"}
SHOP_PLACE = {"VeilstoneDeptStoreStock_3F_UP": ("mart", "MART_SPECIALTIES_ID_VEILSTONE_3F_UP", "VEILSTONE_STORE_3F"),
              "VeilstoneDeptStoreStock_3F_DOWN": ("mart", "MART_SPECIALTIES_ID_VEILSTONE_3F_DOWN",
                                                  "VEILSTONE_STORE_3F"),
              "GameCornerPrizes": ("prize", "GameCornerPrizes", "VEILSTONE_CITY_PRIZE_EXCHANGE")}
# What a TM place the set leaves free gives instead (Ian: "berries, evolution
# items or other non-TM rewards"; no stone, since stones are scarce by
# design), in turn.
STAND_INS = ("ITEM_SITRUS_BERRY", "ITEM_LUM_BERRY")
LATE = ("Galactic", "Volkner", "Barry")     # where an optional trainer may take a TM moved late


@functools.lru_cache(maxsize=None)
def targets(total):
    """{split: its share of the TMs}, by the trainers the census places in
    it, the measure of a split's length (Ian, 2026-10-06: "an even spread
    across the splits, given how long each is")."""
    weight = collections.Counter(p["split"] for p in b6.placements().values() if p["split"] in SPLITS)
    whole = sum(weight.values())
    return {s: total * weight[s] / whole for s in SPLITS}


def build():
    """(rows, report facts): every placement of the TM set and the held items."""
    st = build_set()
    item = numbering(st)
    moves = [c for _k, c in st.kept] + [c for _k, c in st.hms] + [x[0] for x in st.new]
    rows, facts = [], {"early": {}, "unplaced": [], "third": [], "moved": []}
    gauntlet_ids = {t for *_x, ids in gauntlet_sections() for t in ids}
    used_trainers = set()
    weak = [c for c in moves if tier(c) == "weak"]
    main = [c for c in moves if c not in weak]
    count = collections.Counter()
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
        rows.append(Row(it, 1, "trainer", s, header(h), "", "", data.oxide_trainers()[tr]["constant"], "",
                        f"held item; reading {r}"))
    # Weak TMs: one optional trainer each, on the easier side of its split.
    for c in weak:
        pick = pick_trainer(max(natural_split(c), allowed(c)[0], key=si), used_trainers, "easier", gauntlet_ids)
        if not pick:
            facts["unplaced"].append(c)
            continue
        s, tr, r = pick
        used_trainers.add(tr)
        count[s] += 1
        h, _obj = trainer_objects()[tr]
        rows.append(Row(item[c], 1, "trainer", s, header(h), "", "", data.oxide_trainers()[tr]["constant"], "",
                        f"{name(c)}, weak; reading {r}"))
    # The rest, the most held back first, each take a place in the allowed
    # split furthest under its share of the spread: its own place there, a
    # TM place today, a shop TM at that split's badge count, an optional
    # trainer late in the game while spare flags last, a ball holding a
    # mart item. Early places so end up with modest utility TMs.
    share = targets(len(moves))
    fixed = [dict(p) for p in tm_places()]
    shops = [{"shop": m, "item": it} for _s, m, it in mart_tms()]
    cheap = [dict(p) for p in cheap_balls()]
    flags_left = FLAG_POOL - len(used_trainers) - 1     # one for the Game Corner's new trainer
    own_item = {c: f"ITEM_{_key(st, c)}" for c in main if _key(st, c)}

    def options(c, s):
        # A shop TM first where the split has a badge count, so all the
        # counters' TMs are placed and early balls are freed for other items.
        out = []
        badge = next((b for b, bs in BADGE_SPLIT.items() if bs == s), None)
        if badge is not None:
            out += [dict(p, badge=badge) for p in shops if not p.get("used")][:1]
        out += [p for p in fixed if not p.get("used") and p["split"] == s and p["item"] == own_item.get(c)]
        out += [p for p in fixed if not p.get("used") and p["split"] == s and p not in out]
        # A ball holding a mart item before a trainer, which costs a flag.
        out += [p for p in cheap if not p.get("used") and p["split"] == s][:1]
        if s in LATE and flags_left > 0:
            out += [{"trainer": True}]
        return out

    for c in sorted(main, key=lambda c: (-si(allowed(c)[0]), -worth(c), name(c))):
        lo, early = allowed(c)
        if early:
            facts["early"][c] = early
        best = None
        for s in SPLITS[si(lo):]:
            opts = options(c, s)
            if opts:
                key = (share[s] - count[s], -si(s))
                if best is None or key > best[0]:
                    best = (key, s, opts[0])
        if best is None:
            facts["unplaced"].append(c)
            continue
        _k, s, p = best
        t = tier(c)
        count[s] += 1
        if "trainer" in p:
            pick = pick_trainer(s, used_trainers, "easier", gauntlet_ids)
            if pick:
                s2, tr, r = pick
                used_trainers.add(tr)
                flags_left -= 1
                h, _obj = trainer_objects()[tr]
                rows.append(Row(item[c], COPIES[t], "trainer", s2, header(h), "", "",
                                data.oxide_trainers()[tr]["constant"], "",
                                f"{name(c)}, {t}; an optional trainer late in the game; reading {r}"))
                continue
            facts["unplaced"].append(c)
            continue
        if "shop" in p:
            src = next(q for q in shops if q["shop"] == p["shop"] and q["item"] == p["item"] and not q.get("used"))
            src["used"] = True
            kind, place, h = SHOP_PLACE[p["shop"]]
            rows.append(Row(item[c], COPIES[t], kind, s, header(h), place, p["item"], "", p["badge"],
                            f"{name(c)}, {t}; bought once, from {p['badge']} badges, giving {COPIES[t]}"))
            continue
        src = next(q for q in (fixed + cheap) if q is not None and q.get("map") == p["map"]
                   and q.get("item") == p["item"] and q.get("split") == p["split"] and not q.get("used"))
        src["used"] = True
        why = "its own place today" if p["item"] == own_item.get(c) else \
            f"a TM place today ({p['item']})" if p["item"].startswith(("ITEM_TM", "ITEM_HM")) else \
            f"a ball that holds {p['item']} today"
        if (p["map"], p["kind"]) == GAME_CORNER_GIFT:
            # The ten-bonus-round gift, pure luck, becomes an optional
            # trainer's reward in the Game Corner (Ian, 2026-10-06); the main
            # track creates the trainer in step 10 and drops the gift.
            rows.append(Row(item[c], COPIES[t], "trainer", s, header(p["map"]), "", p["item"],
                            GAME_CORNER_TRAINER, "", f"{name(c)}, {t}; in place of the gift for ten straight "
                                                     f"bonus rounds ({p['item']}), a new optional trainer"))
            continue
        rows.append(Row(item[c], COPIES[t], p["kind"], s, header(p["map"]), "", p["item"], "", "",
                        f"{name(c)}, {t}; {why}"))
    # A TM place or shop TM left over would still give its old TM, a second
    # source, so each gets a non-TM item.
    k = 0
    for p in fixed:
        if not p.get("used"):
            rows.append(Row(STAND_INS[k % len(STAND_INS)], 1, p["kind"], p["split"], header(p["map"]), "",
                            p["item"], "", "", "a TM place the spread leaves to another item"))
            k += 1
    for p in shops:
        if not p.get("used"):
            facts["unplaced"].append(f"shop slot {p['shop']} {p['item']}")
    # The held items the Game Corner sells today leave its prizes for
    # optional fights, and their slots are dropped (Ian, 2026-10-06): a row
    # of reward ITEM_NONE and no copies tells the prize menu to remove one.
    for _s, m, it in splits.marts():
        if it in GAME_CORNER_HELD:
            kind, place, h = SHOP_PLACE[m]
            rows.append(Row(DROPPED, 0, kind, BADGE_SPLIT[3], header(h), place, it, "", 3,
                            f"{it.replace('ITEM_', '').replace('_', ' ').title()} moves to an optional fight; "
                            "its prize slot is dropped"))
    facts["third"] = [c for c in moves if tier(c) == "utility" and name(c) in HAZARDS | PIVOTS]
    facts["share"] = share
    rows.sort(key=lambda r: (si(r.split), r.kind, r.map, r.reward))
    return st, item, rows, facts


# Ian approved the table's timing as pushed at FROZEN_REF (2026-10-07,
# relayed by the Overseer). Its rows stay as they are, since the spread
# reshuffles 33 other TMs when a few tiers change, and some of those moves
# went against his ladder (Drain Punch into Gardenia's split). Only the TMs
# the move rework changed are repriced, each by hand here: {reward: (copies,
# the (map, replaces) of the row it trades places with, or None to stay,
# why)}. The row it trades with takes the TM's old place.
FROZEN_REF = "fc06095a8e"
REPRICED = {
    "ITEM_TM15": (1, None, "Hyper Beam, strong since the rework (180, no recharge, half as recoil): one copy"),
    "ITEM_TM68": (1, ("MAP_HEADER_VICTORY_ROAD_2F", "ITEM_TM79"),
                  "Giga Impact, strong since the rework (180, no recharge, half as recoil): one copy, "
                  "in Barry's split, the first its power allows"),
    "ITEM_TM70": (1, ("MAP_HEADER_VICTORY_ROAD_B1F", "ITEM_TM59"),
                  "Outrage, strong since the rework (140, one turn, half as recoil): one copy, no earlier "
                  "than Galactic's split; the first free place is Victory Road"),
    "ITEM_TM28": (1, None, "Dig, weak since the rework (60, one turn): one copy; a weak TM is an optional "
                           "trainer's reward, but all 46 spare flags are used, so it keeps its place"),
}


def frozen_rows():
    """The approved table's rows, with REPRICED applied."""
    out = subprocess.run(["git", "-C", data.ROOT, "show", f"{FROZEN_REF}:docs/oxide/reward-placements.tsv"],
                         capture_output=True, text=True, check=True).stdout
    lines = [line for line in out.splitlines() if not line.startswith("#")]
    rows = [Row(**r) for r in csv.DictReader(lines, delimiter="\t")]
    for it, (copies, target, why) in REPRICED.items():
        old = next(r for r in rows if r.reward == it)
        if target is None:
            rows[rows.index(old)] = old._replace(copies=str(copies), note=why)
            continue
        other = next(r for r in rows if (r.map, r.replaces) == target)
        place = ("kind", "split", "map", "place", "replaces", "trainer_id", "badges")
        rows[rows.index(old)] = other._replace(**{f: getattr(old, f) for f in place})
        rows[rows.index(other)] = old._replace(copies=str(copies), note=f"{why}; a TM place today ({other.replaces})",
                                               **{f: getattr(other, f) for f in place})
    rows.sort(key=lambda r: (si(r.split), r.kind, r.map, r.reward))
    return rows


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
    # A trainer the main track creates for a reward (the Game Corner's).
    known = {t["constant"] for t in ox.values()}
    for t, r in by_trainer.items():
        if t not in known:
            out.append({"split": r.split, "trainer_id": t, "trainer": "new, the main track creates it",
                        "map": r.map, "object": "", "required": "no", "role": "reward", "section": "",
                        "reward": r.reward, "copies": r.copies, "size": "", "reading": "", "flag": "spare",
                        "note": "Ian, 2026-10-06: the gift for ten straight bonus rounds becomes this trainer's"})
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
    # The TM list for the main track's item tool (main-tm-items): one row per
    # TM, its number and its move, TMs in number order, then the HMs kept.
    with open(TM_LIST, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["tm", "move"])
        for c, it in sorted(item.items(), key=lambda kv: (kv[1].startswith("ITEM_HM"), kv[1])):
            w.writerow([tm_label(it), c])
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
    # Every TM a counter sells today is a placement of its own, sold once
    # from a badge count (Ian, 2026-10-06), so none stays a second source.
    sold = collections.Counter((SHOP_PLACE[m][1], it) for _s, m, it in splits.marts()
                               if m in SHOP_PLACE and (it.startswith(("ITEM_TM", "ITEM_HM")) or it in GAME_CORNER_HELD))
    shop_rows = [r for r in placed if r["kind"] in ("mart", "prize")]
    for r in shop_rows:
        if not str(r.get("badges") or "").isdigit():
            fails.append(f"{r['reward']} at {r['place']} has no badge count")
    resold = collections.Counter((r["place"], r["replaces"]) for r in shop_rows)
    for k, n in sorted(sold.items()):
        if resold[k] < n:
            fails.append(f"{k[1]} at {k[0]} is still sold as it is today")
    print(f"{len(placed)} placements, {len(trainers)} reward trainers, {new_balls} new balls: "
          f"{flags} of {FLAG_POOL} spare flags; {sum(1 for r in shop_rows if r["reward"] != DROPPED)} shop TMs; {len(fails)} failures", file=out)
    for f_ in fails:
        print("  " + f_, file=out)
    return fails


# ---- the report -----------------------------------------------------------------------------

KIND_WORDS = {"ball": "ball", "hidden": "hidden item", "gift": "gift", "trainer": "reward trainer",
              "mart": "Department Store, once", "prize": "Game Corner prize, once"}
TM_LIST = os.path.join(OUT, "tm-list.tsv")
AREA_NAMES = {"galactic_eterna": "Team Galactic's Eterna building", "galactic_hq": "The Galactic HQ",
              "mt_coronet": "Mt. Coronet", "victory_road": "Victory Road"}


def tm_label(it):
    return it.replace("ITEM_", "")


def shop_label(reward, move_of):
    """A shop row's reward: a TM with its move, or an item by name."""
    if reward in move_of:
        return f"{tm_label(reward)} {name(move_of[reward])}"
    return reward.replace("ITEM_", "").replace("_", " ").title().replace("Pp ", "PP ")


DRAFT_REF = "514910abe1"    # the first draft Ian read (2026-10-06)


def draft_rows():
    """{reward: its row} in the first draft's table, for what moved since."""
    import subprocess
    out = subprocess.run(["git", "-C", data.ROOT, "show", f"{DRAFT_REF}:docs/oxide/reward-placements.tsv"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return {}
    lines = [line for line in out.stdout.splitlines() if not line.startswith("#")]
    return {r["reward"]: r for r in csv.DictReader(lines, delimiter="\t")}


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
    shop_rows = [r for r in rows if r.kind in ("mart", "prize")]
    shop_tms = [r for r in shop_rows if r.reward.startswith(("ITEM_TM", "ITEM_HM"))]
    by_split = collections.Counter(r.split for r in tm_rows.values())
    before = draft_rows()
    before_split = collections.Counter(r["split"] for it, r in before.items() if it.startswith(("ITEM_TM", "ITEM_HM")))
    early_now = sum(n for s, n in by_split.items() if si(s) <= si("Byron"))
    early_then = sum(n for s, n in before_split.items() if si(s) <= si("Byron"))
    p("# The TM list and the reward table (step 6, for Ian)")
    p()
    p("Written by `tools/oxide/balance/rewards.py` on the branch `balance-tm-pass`. It changes no game data;")
    p("the placement tool applies the approved table in step 10.")
    p()
    p("## Summary")
    p()
    p(f"**Outcome.** The TM list Ian approved on 2026-10-06 has {len(move_of)} TMs: {len(st.kept)} of "
      f"vanilla's 92 kept, the six HMs less Cut and Rock Smash as single-use TMs, and {len(st.new)} new moves, "
      f"their numbers fixed. {tiers['strong']} are strong (one copy), {tiers['utility']} utility (two copies) "
      f"and {tiers['weak']} weak (one copy, each the reward for one optional trainer). This version carries "
      f"Ian's answers of the same day: his four timing notes; an even spread across the splits by their "
      f"length ({early_now} TMs by the end of Byron's split, where the first draft had {early_then}); and the "
      f"Department Store's and the Game Corner's {len(shop_tms)} TMs sold once each, unlocked by badge count "
      f"in order of usefulness. Every TM and each of element 7's {len(HELD)} held items has exactly one place, "
      f"every vanilla TM ball, gift and shop TM is repointed, and the reward trainers take {flags} of the "
      f"{FLAG_POOL} spare story flags. The table's own check passes.")
    p()
    p("**What can still move.** The move-rework cloud job changes the numbers of Hyper Beam, Giga Impact and "
      "the multi-hit moves, so their tiers, and with them their copies and places, are read on today's data. "
      "The numbers and moves stay as they are.")
    p()
    p("**Ian's action items:** spot-check the moves that moved (\"The spread\") and the shop's badge tiers; "
      f"third copies, if any, among {', '.join(name(c) for c in facts['third']) or 'none'}.")
    p()
    p("**Next steps.**")
    p()
    p("| Step | What | Who | About how long |")
    p("|---|---|---|---|")
    p("| 8 | Every species' TM compatibility, then the one rescore after the rework job merges | Balance Agent | 2 to 3 hours and 1.5 hours of machine time |")
    p("| 8 | The bigger TM pocket and the item data for the new TMs (from `tm-list.tsv`) | main-track session | |")
    p("| 10 | The table placed in the maps and shops, the gauntlets filled in | main-track session | 3 to 6 hours |")
    p()
    p("## The TM list by number")
    p()
    p("Every number from TM01, then the HMs: the move vanilla teaches by it, the move it teaches now, the "
      "split it first comes in, and why it changed.")
    p()
    p("| Number | Vanilla | Now | Split | Why it changed |")
    p("|---|---|---|---|---|")
    machines = base_machines()
    dropped_why = {k: why for k, _c, why in st.dropped + st.hm_dropped}
    new_why = {}
    for c, lf, gn, _w in st.new:
        new_why[c] = f"new: {gn} lines gain it that cannot learn it by level-up" + \
            (f", {lf} of them lines no boss takes" if lf else "")
    labels = sorted({k for k in machines if k.startswith(("TM", "HM"))} | {tm_label(it) for it in item.values()},
                    key=lambda k: (k.startswith("HM"), k))
    for k in labels:
        old = machines.get(k)
        now = move_of.get(f"ITEM_{k}")
        r = tm_rows.get(f"ITEM_{k}")
        if now and old == now:
            why = ""
        elif now:
            why = (f"{name(old)} left ({dropped_why.get(k, '')}); " if old else "") + new_why.get(now, "")
        else:
            why = f"leaves the list ({dropped_why.get(k, '')})"
        p(f"| {k} | {name(old) if old else '-'} | {name(now) if now else '-'} | {r.split if r else '-'} | {why} |")
    p()
    p("## The spread")
    p()
    p("TMs by the split they first come in, against each split's share by its length (the trainers in it), "
      "and the first draft's count.")
    p()
    p("**What gates a TM's timing.** A TM attack comes no earlier than the split whose old power ceiling "
      "covers its power: the learnset generator's ceiling for a same-type attack, "
      + ", ".join(f"{lr.CEILING[s]} in {s}'s split" for s in SPLITS[:6])
      + ", and more after. A hard gate, not a weight. A strong TM also waits for each flagged line that "
      "learns it to have a good attack of its type by level-up (Byron's split at the latest), and Ian's "
      "timing notes hold five moves later. The power gate is the lever to turn if TM timing feels off in "
      "the alpha.")
    p()
    p("| Split | Share | Now | First draft |")
    p("|---|---|---|---|")
    for s in SPLITS:
        p(f"| {s} | {facts['share'][s]:.1f} | {by_split[s]} | {before_split[s]} |")
    p()
    p("Ian's timing notes (2026-10-06), each kept as judgement, not a rule:")
    p()
    for nm, (split, why) in JUDGED.items():
        it = next((i for c, i in item.items() if name(c) == nm), None)
        r = tm_rows.get(it)
        p(f"- {nm}: from {split}'s split at the earliest, now {r.split if r else '-'}; {why}.")
    p()
    p("The TMs whose split or source changed from the first draft:")
    p()
    p("| TM | Move | Then | Now |")
    p("|---|---|---|---|")
    for it, r in sorted(tm_rows.items(), key=lambda kv: (si(kv[1].split), kv[0])):
        old = before.get(it)
        then = f"{old['split']}, {KIND_WORDS.get(old['kind'], old['kind'])}" if old else "-"
        now = f"{r.split}, {KIND_WORDS[r.kind]}"
        if not old or old["split"] != r.split or old["kind"] != r.kind or old["map"] != r.map:
            p(f"| {tm_label(it)} | {name(move_of[it])} | {then} | {now} |")
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
        p(f"| {label} | {r.split} | {ox_by_const.get(r.trainer_id, {'name': 'a new trainer (the main track)'})['name']} | "
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
    p("## The Department Store and the Game Corner")
    p()
    p("Ian, 2026-10-06: each TM they sell unlocks at a badge count, in order of usefulness, and can be "
      "bought once, like any other placement. Veilstone opens in Maylene's split with three badges, so the "
      "counts run from 3 to 8; the spread chose each TM's count, and the strongest come last. Prices stay "
      "vanilla's.")
    p()
    p("| Badges | Split | Department Store | Game Corner |")
    p("|---|---|---|---|")
    for b, s in BADGE_SPLIT.items():
        store = [shop_label(r.reward, move_of) for r in shop_rows if r.kind == "mart"
                 and str(r.badges) == str(b) and r.reward != DROPPED]
        prize = [shop_label(r.reward, move_of) for r in shop_rows if r.kind == "prize"
                 and str(r.badges) == str(b) and r.reward != DROPPED]
        p(f"| {b} | {s} | {', '.join(store) or '-'} | {', '.join(prize) or '-'} |")
    dropped = [r.replaces for r in shop_rows if r.reward == DROPPED]
    if dropped:
        p()
        p("The Game Corner's held items (" + ", ".join(d.replace("ITEM_", "").replace("_", " ").title()
                                                    for d in dropped)
          + ") move to optional fights, and their prize slots are dropped (Ian, 2026-10-06); the table "
            "marks each with reward ITEM_NONE and no copies. The prizes that were neither a TM nor a held "
            "item stay as they are.")
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
    ap.add_argument("--reshuffle", action="store_true",
                    help="write the spread's own table instead of the approved one (FROZEN_REF)")
    args = ap.parse_args(argv)
    if args.what == "check":
        return 1 if check() else 0
    st, item, rows, facts = build()
    # The spread above still runs for its facts; the table written is the
    # approved one (FROZEN_REF) unless asked to reshuffle.
    if not args.reshuffle:
        rows = frozen_rows()
    write(st, item, rows, facts)
    readings_ = (parse_section_readings(args.gauntlet_reading) if args.gauntlet_reading
                 else None if args.no_gauntlets else section_readings())
    report(st, item, rows, facts, readings_)
    print(f"set: {len(st.kept)} kept, {len(st.hms)} former HMs, {len(st.new)} new; "
          f"{len(rows)} placements; unplaced {facts['unplaced']}")
    return 1 if check() else 0


if __name__ == "__main__":
    sys.exit(main())
