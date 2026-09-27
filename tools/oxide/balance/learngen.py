"""The learnset study, part 3: its analyses and the generator (balance plan,
"The learnset study"; Ian's answers of 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.balance.learngen delays     # (a), both games
    PYTHONPATH=. python3 -m tools.oxide.balance.learngen bare       # (c), Oxide's catches

(b), the wild movesets, is learnwild.py. Everything here reads; nothing is
written to the game data.

(a) Delays. Kaizo rewards waiting to evolve: a pre-evolution learns a strong
move (85 or more a turn, learnstudy's strength) at or after the level its
evolution comes, so a player who evolves on time goes without it, and the
evolved stage learns it a split or more later, or never. That is a delay.
A strong move the pre-evolution learns before it can evolve is a head start
instead: it is kept on evolving, so it asks no waiting. Levels come from each
game's own evolutions (Kaizo's documentation for Kaizo); an evolution by
item, place or friendship is taken at the encounter tool's stand-in level.
"""
import argparse
import collections
import functools
import statistics
import sys

from ..encounters import evolve, pokedex
from . import data, kaizo_docs, learnstudy as ls

STRONG = ls.STRONG


# ---- the two games, read alike -------------------------------------------------

def kaizo_constant(name):
    """A Kaizo species name (IVYSAUR, MR. MIME, NIDORAN♀) as a SPECIES_ constant."""
    n = name.upper().replace("♀", "_F").replace("♂", "_M")
    for a, b in ((". ", "_"), (".", ""), ("'", ""), ("’", ""), ("-", "_"), (" ", "_")):
        n = n.replace(a, b)
    return "SPECIES_" + n


@functools.lru_cache(maxsize=None)
def kaizo_reached():
    """{species: (parent, level it is reached at)} by Kaizo's own evolutions."""
    out = {}
    for parent, evos in kaizo_docs.load()["evolutions"].items():
        for method, need, result in evos:
            level = need if method.startswith("Level") and isinstance(need, int) and need > 0 \
                else evolve.DEFAULT_PSEUDO if not method.startswith("Use Item") \
                else evolve.PSEUDO["EVO_USE_ITEM"]
            out.setdefault(kaizo_constant(result), (kaizo_constant(parent), level))
    return out


@functools.lru_cache(maxsize=None)
def oxide_reached():
    """{species: (parent, level it is reached at)} by Oxide's evolutions."""
    out = {}
    for sp in pokedex.species_list(data.ROOT):
        party = [ls.evolution_result(sp, e, ref=None)
                 for e in (pokedex.load(data.ROOT, sp) or {}).get("evolutions", [])
                 if e["method"] == "LEVEL_SPECIES_IN_PARTY"]
        for level, target in evolve.evolutions(data.ROOT, sp):
            # evolve.py reads Mantyke's party species as its result (see
            # learnstudy.evolution_result); the entry's last species is it.
            # It also reads Feebas's beauty (170) as a level: past 100 it is
            # taken at the stand-in level, like the other non-level methods.
            if level > 100:
                level = evolve.DEFAULT_PSEUDO
            out.setdefault(party[0] if party else target, (sp, level))
        # evolve.py keeps only a stage's level evolutions when it has any;
        # the player can use the item too (Kirlia's Dawn Stone to Gallade).
        for e in (pokedex.load(data.ROOT, sp) or {}).get("evolutions", []):
            into = e.get("into")
            if e.get("item") and into and into not in out and not into.startswith(sp + "_"):
                out[into] = (sp, evolve.PSEUDO.get("EVO_" + e["method"], evolve.DEFAULT_PSEUDO))
    return out


def reached(game, species):
    table = kaizo_reached() if game == "kaizo" else oxide_reached()
    return table.get(species, (None, 0))[1]


# The generator's lists, {species: [(level, MOVE_X)]}, read as a third game,
# "proposal": Oxide's tables, evolutions and moves with these lists, so every
# analysis can be run on what the generator proposes.
PROPOSED = {}


def oxide_list(game, species):
    """[(level, MOVE_X)] for Oxide as it is, or as the generator proposes."""
    if game == "proposal":
        return PROPOSED.get(species, [])
    rec = pokedex.load(data.ROOT, species)
    return rec["learnset"] if rec else []


@functools.lru_cache(maxsize=None)
def _oxide_moves():
    return pokedex.moves(data.ROOT)


def game_entries(game, species):
    """A species' level-up list read the same way for either game: dicts of
    level, move (its name), kind, power, band, type, stab and split index."""
    if game == "kaizo":
        out = []
        for e in ls.entries(species):
            if e["kind"] == "unknown":
                continue
            out.append(dict(e, index=ls.SPLIT_NAMES.index(e["split"])))
        return out
    rec = pokedex.load(data.ROOT, species)
    if not rec:
        return []
    types = {t.title() for t in rec["types"]}
    out = []
    for level, mv in oxide_list(game, species):
        m = _oxide_moves().get(mv)
        if not m:
            continue
        kind, power = ls.strength(ls.oxide_move(m))
        split = ls.oxide_split(level)
        out.append({"species": species, "level": level, "move": m["name"], "kind": kind,
                    "power": round(power, 1), "band": ls.band(power) if kind == "damage" else None,
                    "type": m["type"].title(), "stab": m["type"].title() in types,
                    "split": split, "index": _oxide_index(split)})
    return out


OXIDE_ORDER = ["Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron", "Candice", "HQ",
               "Galactic", "Volkner", "Barry", "League", "Post"]


def _oxide_index(split):
    return OXIDE_ORDER.index(split) if split in OXIDE_ORDER else len(OXIDE_ORDER) - 1


@functools.lru_cache(maxsize=None)
def oxide_lines():
    """Oxide's evolution lines, each branch its own, over every species."""
    kids = collections.defaultdict(list)
    for into, (parent, _lv) in oxide_reached().items():
        kids[parent].append(into)
    out = []

    def walk(path):
        nxt = [k for k in kids.get(path[-1], []) if k not in path]
        if not nxt:
            out.append(path)
        for k in nxt:
            walk(path + [k])
    for sp in pokedex.species_list(data.ROOT):
        if sp not in oxide_reached():
            walk([sp])
    return out


def game_lines(game):
    return ls.lines() if game == "kaizo" else oxide_lines()


def is_oxide(game):
    return game in ("oxide", "proposal")


# ---- (a) delays ------------------------------------------------------------------

def delays(game):
    """Every strong move a pre-evolution has that its next stage learns later
    or never by level-up (only at level 1 counts as never: that is the
    relearner's, Ian, 2026-09-27): (line, pre, evolved, move, pre's level,
    evolution level, evolved stage's level or None, splits between them or
    None, kind) with kind "delay" (learnt at or after the evolution level)
    or "head start"."""
    out = []
    seen = set()
    for line in game_lines(game):
        for a, b in zip(line, line[1:]):
            if (a, b) in seen:
                continue
            seen.add((a, b))
            evo_level = reached(game, b)
            later = {}
            for e in game_entries(game, b):
                if e["level"] > 1:
                    later.setdefault(e["move"], e)
            for e in game_entries(game, a):
                if e["kind"] != "damage" or e["power"] < STRONG or e["level"] <= 1:
                    continue
                b_e = later.get(e["move"])
                gap = None if b_e is None else b_e["index"] - e["index"]
                if b_e is not None and b_e["level"] <= e["level"]:
                    continue
                kind = "delay" if e["level"] >= evo_level else "head start"
                out.append((line, a, b, e["move"], e["level"], evo_level,
                            b_e["level"] if b_e else None, gap, kind))
    return out


def never_learnt(game):
    """(moves, strong ones): what a pre-evolution learns by level-up at or
    after the level its next stage comes, which no later stage of the line
    then learns by level-up: a move only a Pokemon kept from evolving ever
    gets. Ian counts these as the strongest delay (2026-09-27). A move learnt
    before the evolution level is not one: a raised Pokemon keeps it."""
    n = strong = 0
    seen = set()
    for line in game_lines(game):
        for i, pre in enumerate(line[:-1]):
            evolves_at = reached(game, line[i + 1])
            later = {e["move"] for sp in line[i + 1:] for e in game_entries(game, sp)
                     if e["level"] > 1}
            for e in game_entries(game, pre):
                key = (pre, e["move"])
                if e["level"] < evolves_at or e["level"] <= 1 or e["move"] in later or key in seen:
                    continue
                seen.add(key)
                n += 1
                strong += e["kind"] == "damage" and e["power"] >= STRONG
    return n, strong


def split_index(game, level):
    if game == "kaizo":
        return ls.split_index("kaizo", level)
    return _oxide_index(ls.oxide_split(level))


def real_wait(game, row):
    """A delay a player can take: the pre-evolution learns the move in the
    split its evolution comes in, or the next. Past that it is the list's
    tail (Kaizo's lists run to 100), which no run waits for."""
    return split_index(game, row[4]) - split_index(game, row[5]) <= 1


def delay_report(out=sys.stdout):
    for game in ("kaizo", "oxide"):
        rows = delays(game)
        pairs = {p for line in game_lines(game) for p in zip(line, line[1:])}
        tails = [r for r in rows if r[8] == "delay" and not real_wait(game, r)]
        dl = [r for r in rows if r[8] == "delay" and real_wait(game, r)]
        hs = [r for r in rows if r[8] == "head start"]
        lines_with = {r[1] for r in dl}
        print(f"\n{game}: {len(pairs)} evolutions; {len(lines_with)} pre-evolutions hold a "
              f"strong move worth waiting a split or less for ({len(dl)} moves), "
              f"{len({r[1] for r in tails})} one only far past their evolution "
              f"({len(tails)} moves), and {len({r[1] for r in hs})} a head start "
              f"({len(hs)} moves)", file=out)
        waits = [r[4] - r[5] for r in dl]
        never = sum(r[6] is None for r in dl)
        gaps = collections.Counter("never" if r[7] is None else r[7] for r in dl)
        if waits:
            print(f"  levels waited past the evolution: median {statistics.median(waits)}, "
                  f"quartiles {ls._q(waits, .25)} to {ls._q(waits, .75)}, most {max(waits)}",
                  file=out)
        print(f"  the evolved stage learns it: never {never}; splits later "
              f"{dict(sorted((k, v) for k, v in gaps.items() if k != 'never'))}", file=out)
        stab = sum(1 for r in dl if _is_stab(game, r[1], r[3]))
        print(f"  same-type: {stab} of {len(dl)}", file=out)
        ex = sorted(dl, key=lambda r: -(r[4] - r[5]))[:12]
        for r in ex:
            print(f"  {r[1].replace('SPECIES_', '').title():12} {r[3]:16} at {r[4]:>3} "
                  f"(evolves at {r[5]:>2}); {r[2].replace('SPECIES_', '').title():12} "
                  f"{'never' if r[6] is None else 'at ' + str(r[6])}", file=out)


def _is_stab(game, species, move):
    return any(e["move"] == move and e["stab"] for e in game_entries(game, species))


# ---- (c) bare evolved catches ------------------------------------------------------

GOOD_STAB, GOOD_ANY = ls.FAIR, STRONG


def _good(e):
    return e["kind"] == "damage" and (e["power"] >= GOOD_ANY
                                      or (e["stab"] and e["power"] >= GOOD_STAB))


def learned_after(game, species, level, cap):
    """What a Pokemon caught as `species` at `level` learns by level-up up to
    a cap, on its form and on each later one from the level it is reached
    (a later form's level-1 moves are the relearner's, worth almost nothing:
    Ian, 2026-09-27)."""
    line = next((ln for ln in game_lines(game) if species in ln), [species])
    out = [e for e in game_entries(game, species) if level < e["level"] <= cap]
    for sp in line[line.index(species) + 1:]:
        at = reached(game, sp)
        if at > cap:
            break
        out += [e for e in game_entries(game, sp) if max(at, 2) <= e["level"] <= cap]
    return out


def worth(game, row, cap):
    """A catch's moves to the player: the four it knows at capture and what it
    learns by level-up afterwards, up to the cap (the entries, for _good)."""
    entries = {e["move"]: e for e in game_entries(game, row["species"])}
    return [entries[m] for m in row["moves"] if m in entries] + \
        learned_after(game, row["species"], row["level"], cap)


def bare_catches(game):
    """Evolved stages caught wild that have no good move (a same-type move of
    70 or more a turn, or any of 85 or more) at capture or by level-up before
    their split's cap, with what their pre-evolution learns by then that they
    lack: [(slot, moves at capture, the pre-evolution's good moves)]."""
    from . import learnwild
    rows, _later = learnwild.readings(game)
    lines = game_lines(game)
    parent = {b: a for ln in lines for a, b in zip(ln, ln[1:])}
    caps = learnwild._caps(game)
    out, seen = [], set()
    for r in rows:
        sp = r["species"]
        if sp not in parent:
            continue
        key = (sp, r["split"], r["level"])
        if key in seen:
            continue
        seen.add(key)
        cap = caps.get(r["split"], 100)
        entries = {e["move"]: e for e in game_entries(game, sp)}
        have = [entries[m] for m in r["moves"] if m in entries]
        if any(_good(e) for e in worth(game, r, cap)):
            continue
        pre = [e["move"] for e in game_entries(game, parent[sp]) if _good(e) and e["level"] <= cap]
        out.append((r, have, sorted(set(pre))))
    return out


def bare_report(out=sys.stdout):
    for game in ("kaizo", "oxide"):
        rows = bare_catches(game)
        species = sorted({r["species"] for r, _h, _p in rows})
        cause = sum(1 for _r, _h, pre in rows if pre)
        print(f"\n{game}: {len(rows)} evolved catches ({len(species)} species) with no good move "
              f"by their split's cap without the relearner; in {cause} of them the "
              f"pre-evolution learns one by then", file=out)
        for r, have, pre in sorted(rows, key=lambda x: (learnwild_order(game, x[0]["split"]),
                                                         x[0]["species"]))[:30]:
            print(f"  {r['split']:9} {r['area'][:26]:26} {r['species'].replace('SPECIES_', '').title():12}"
                  f" {r['level']:>3}: {', '.join(r['moves'])}"
                  f"{'; its pre-evolution learns ' + ', '.join(pre[:4]) if pre else ''}", file=out)


def learnwild_order(game, split):
    order = ls.SPLIT_NAMES if game == "kaizo" else OXIDE_ORDER
    return order.index(split) if split in order else 99


# ---- the generator ------------------------------------------------------------------
#
# For every species, a proposed level-up list, from the rules of parts 1 and 2
# and the analyses above:
#
# 1. The candidates are the moves the species and its earlier stages learn now,
#    and Kaizo's lists for the same species, by name, where Kaizo's move is
#    Oxide's move: the same type, and an attack in both or in neither (Kaizo
#    rebuilt some moves under their old names; its Swallow is a 90-power
#    Poison attack). A move only one line learns by level-up in Oxide, a
#    signature such as Spacial Rend, goes to no other line from Kaizo.
# 2. Dropped: dead weight by the confirmed rule (Ian added its nine further
#    catches, 2026-09-27), the move pool's first cut (b6.DEAD_MOVES), a
#    weather move for a species the player can own, and a damaging move under
#    nine tenths of a same-type move the species already knows by then
#    (Kaizo's lists are nine tenths upgrades), unless it has priority.
# 3. A damaging move goes where Kaizo usually has it, on Oxide's splits: its
#    own usual level when Kaizo's version is within ten of Oxide's strength,
#    else the usual level of Kaizo's moves of like strength (part 2's
#    placement for a move Kaizo never used). A status move keeps its level,
#    or Kaizo's usual one if it is new.
# 4. An evolved stage learns what comes at or after its evolution level. What
#    comes before sits at its level 1, for the Move Relearner (Ian's answer 7)
#    and so a wild or trainer one met before its own moves start still has
#    four: level 1 is ordered weakest first, so its four strongest are the
#    last four, which are the ones such a Pokemon knows.
# 5. Waiting is rewarded (analysis (a)): a strong move a pre-evolution gets
#    within a split of evolving comes to the evolved stage one split later.
# 6. A first stage starts with a damaging move at level 1, the weakest it has.
# 7. Every level is at or under the League's cap, 78, since Kaizo's 100 maps
#    to it.
# 8. A move that ends a wild encounter (learnwild.ENDS: Roar, Teleport,
#    Self-Destruct and the like) goes above the highest level the species is
#    met wild at, or out if that is past 78, so no wild one carries it.

# Kaizo's split closings against Oxide's, for carrying a level across.
LEVEL_MAP = [(0, 0), (16, 16), (28, 26), (38, 33), (47, 39), (54, 44), (65, 53), (74, 56),
             (84, 68), (100, 78)]
WEATHER_MOVES = {"MOVE_RAIN_DANCE", "MOVE_SUNNY_DAY", "MOVE_SANDSTORM", "MOVE_HAIL",
                 "MOVE_SNOWSCAPE", "MOVE_CHILLY_RECEPTION"}
SAME_POWER = 10


def oxide_level(kaizo_level):
    """A Kaizo level carried onto Oxide's splits, piecewise between closings."""
    for (k0, o0), (k1, o1) in zip(LEVEL_MAP, LEVEL_MAP[1:]):
        if kaizo_level <= k1:
            return max(1, round(o0 + (kaizo_level - k0) * (o1 - o0) / (k1 - k0)))
    return LEVEL_MAP[-1][1]


@functools.lru_cache(maxsize=None)
def kaizo_usual():
    """{compact move name: (median Kaizo level, Kaizo strength, kind)} over
    every line's path, past level 1."""
    levels, power, kind = collections.defaultdict(list), {}, {}
    for line in ls.lines():
        for e in ls.path(line):
            if e["kind"] == "unknown" or e["level"] <= 1:
                continue
            k = ls.metrics._compact(ls.SPELLING.get(e["move"], e["move"]))
            levels[k].append(e["level"])
            power[k], kind[k] = e["power"], e["kind"]
    return {k: (statistics.median(v), power[k], kind[k]) for k, v in levels.items()}


def target_level(rec, current=None):
    """Where the generator puts a move (Oxide's record), before stages. A
    recharging move is placed by its one-turn power: its strength a turn
    halves it, but a 150-power hit early is still a 150-power hit."""
    kind, power = ls.strength(ls.oxide_move(rec))
    if kind == "damage" and rec.get("effect") == "RECHARGE_AFTER":
        power = (rec["power"] or 0) * min(rec.get("accuracy") or 100, 100) / 100
    usual = kaizo_usual().get(ls.metrics._compact(rec["name"]))
    if kind != "damage":
        if current:
            return min(current, LEVEL_MAP[-1][1])
        return oxide_level(usual[0]) if usual else None
    if usual and usual[2] == "damage" and abs(usual[1] - power) <= SAME_POWER:
        return oxide_level(usual[0])
    near = [lv for lv, p, k in kaizo_usual().values()
            if k == "damage" and abs(p - power) <= SAME_POWER]
    return oxide_level(statistics.median(near)) if near else None


@functools.lru_cache(maxsize=None)
def _by_name():
    return {ls.metrics._compact(m["name"]): c for c, m in _oxide_moves().items()}


def _chain(species):
    """The species' earlier stages and itself, first stage first."""
    chain = [species]
    while chain[0] in oxide_reached() and oxide_reached()[chain[0]][0] not in chain:
        chain.insert(0, oxide_reached()[chain[0]][0])
    return chain


def _same_move(kaizo_name, const):
    """Whether Kaizo's move of that name is Oxide's: the same type, and an
    attack in both or in neither."""
    km = ls.kaizo_moves()
    k = km.get(ls.resolve(kaizo_name, km) or "")
    if not k:
        return False
    m = _oxide_moves()[const]
    attack = lambda cat, power: cat != "Status" and (power or 0) > 1
    return (k["type"] or "").title() == m["type"].title() and \
        attack(k["category"], k["power"]) == attack(m["class"].title(), m["power"])


@functools.lru_cache(maxsize=None)
def _level_up_lines():
    """{move: the first stages of the lines that learn it by level-up in Oxide}."""
    first = {sp: _chain(sp)[0] for sp in pokedex.species_list(data.ROOT)}
    out = collections.defaultdict(set)
    for sp in pokedex.species_list(data.ROOT):
        for _lv, mv in (pokedex.load(data.ROOT, sp) or {}).get("learnset", []):
            out[mv].add(first[sp])
    return out


def _signature_elsewhere(const, chain):
    lines = _level_up_lines().get(const, set())
    return len(lines) == 1 and chain[0] not in lines


@functools.lru_cache(maxsize=None)
def _obtainable():
    from . import b6
    return frozenset(b6.obtainable())


def _dropped(const, species, level, types):
    """Why a move stays out of a species' list at a level, or None."""
    from . import b6
    m = _oxide_moves()[const]
    if const in b6.DEAD_MOVES:
        return "the move pool's first cut"
    if const in WEATHER_MOVES and species in _obtainable():
        return "weather, for a species the player can own"
    split = ls.OXIDE_TO_KAIZO.get(ls.oxide_split(level), ls.oxide_split(level))
    split = "League" if split == "Post" else split
    return ls.dead_weight(ls.oxide_move(m), split, m["type"].title() in types, first=level <= 1)


# {species: {MOVE_X: why it left}} for the last proposal, filled by propose().
WHY = collections.defaultdict(dict)


def propose(species):
    """[(level, MOVE_X)] for one species, by the rules above."""
    why = WHY[species]
    why.clear()
    rec = pokedex.load(data.ROOT, species)
    if not rec:
        return []
    types = {t.title() for t in rec["types"]}
    chain = _chain(species)
    here = reached("oxide", species) if len(chain) > 1 else 0
    nxt = [b for b, (a, _lv) in oxide_reached().items() if a == species]
    next_at = min((reached("oxide", b) for b in nxt), default=None)
    current = {}
    for sp in chain:
        for lv, mv in (pokedex.load(data.ROOT, sp) or {}).get("learnset", []):
            if mv in _oxide_moves():
                current.setdefault(mv, lv)
    candidates = dict(current)
    for sp in chain:
        for _lv, name in (ls.kaizo_lists().get(sp) or {}).get("list", []):
            const = _by_name().get(ls.metrics._compact(ls.SPELLING.get(name, name)))
            if (const and const not in candidates and _same_move(name, const)
                    and not _signature_elsewhere(const, chain)):
                candidates[const] = None
    placed = []
    for const, lv in candidates.items():
        t = target_level(_oxide_moves()[const], lv)
        if t is None:
            why[const] = "no placement (a status move new from Kaizo that Kaizo never uses)"
            continue
        placed.append((t, const))
    out = []
    for t, const in sorted(placed):
        m = _oxide_moves()[const]
        kind, power = ls.strength(ls.oxide_move(m))
        level = t
        if len(chain) > 1:
            parent_next = here
            prev_split = split_index("oxide", parent_next)
            # A strong move the pre-evolution gets within a split of this
            # stage's evolution comes here one split later: waiting pays.
            if (kind == "damage" and power >= STRONG and t >= here
                    and split_index("oxide", t) - prev_split <= 1):
                level = _next_split_start(t)
            elif t < here:
                level = 1
        if ls.metrics._compact(m["name"]) in _ends() and level <= wild_top(species):
            level = wild_top(species) + 1
            if level > LEVEL_MAP[-1][1]:
                why[const] = "ends a wild encounter, and the species is wild past 77"
                continue
        if level > LEVEL_MAP[-1][1]:
            level = LEVEL_MAP[-1][1]
        reason = _dropped(const, species, level, types)
        if reason:
            why[const] = "dead weight" if reason not in (
                "the move pool's first cut", "weather, for a species the player can own") else reason
            continue
        out.append((level, const))
    kept = _prune(out, types)
    for _lv, c in set(out) - set(kept):
        why.setdefault(c, "a stronger same-type move comes first")
    final = _start(kept, species, types, chain)
    for _lv, c in set(kept) - set(final):
        why.setdefault(c, "past the six attacks and two status moves an evolved stage keeps at 1")
    return ordered(final, evolved=len(chain) > 1)


# How an evolved stage's level 1 is ordered. A wild or trainer Pokemon with
# fewer than four moves of its own at or under its level fills from level 1,
# taking the last entries in the list's order. Strongest first leaves it the
# weakest, so a wild evolved Pokemon met soon after its evolution level is
# not a better catch than one raised (Ian's rule of 2026-09-27); weakest
# first gives it the strongest. The relearner's menu is the same either way.
LEVEL1_STRONGEST_FIRST = True


def ordered(entries, evolved):
    """The list in the game's order: by level, level 1 by strength (strongest
    first on an evolved stage when LEVEL1_STRONGEST_FIRST), each later level
    weakest first."""
    power = lambda c: ls.strength(ls.oxide_move(_oxide_moves()[c]))[1]
    down = evolved and LEVEL1_STRONGEST_FIRST
    return sorted(entries, key=lambda e: (e[0], -power(e[1]) if e[0] <= 1 and down else power(e[1]),
                                          e[1]))


@functools.lru_cache(maxsize=None)
def _ends():
    from . import learnwild
    return frozenset(learnwild.ENDS_C)


@functools.lru_cache(maxsize=None)
def _wild_tops():
    from . import learnwild
    top = {}
    for e in learnwild.oxide_encounters():
        top[e["species"]] = max(top.get(e["species"], 0), e["hi"])
    return top


def wild_top(species):
    """The highest level Oxide's tables hold the species at, 0 if none."""
    return _wild_tops().get(species, 0)


def _next_split_start(level):
    """The first level of the split after the one `level` falls in."""
    from . import pool
    caps = sorted(pool.caps().values())
    for cap in caps:
        if level <= cap:
            return min(cap + 1, LEVEL_MAP[-1][1])
    return LEVEL_MAP[-1][1]


def _prune(entries, types):
    """Drops a damaging move under nine tenths of a same-type move already
    known by its level, unless it has priority."""
    best = {}
    out = []
    strength = lambda c: ls.strength(ls.oxide_move(_oxide_moves()[c]))[1]
    for level, const in sorted(entries, key=lambda e: (e[0], strength(e[1]), e[1])):
        m = _oxide_moves()[const]
        kind, power = ls.strength(ls.oxide_move(m))
        t = m["type"].title()
        if kind == "damage" and not (m.get("priority") or 0) > 0:
            if power < 0.9 * best.get(t, 0):
                continue
            best[t] = max(best.get(t, 0), power)
        out.append((level, const))
    return out


# The move-pool survey's level-1 picks for the species whose only start was
# Splash or Teleport (Ian, 2026-09-27). Hoppip's Absorb is dead weight since
# Ian confirmed the rule, so it takes Leafage, as Bounsweet does; that one
# change is for Ian to confirm.
RULED_FIRST = {"SPECIES_AZURILL": "MOVE_POUND", "SPECIES_BOUNSWEET": "MOVE_LEAFAGE",
               "SPECIES_FEEBAS": "MOVE_TACKLE", "SPECIES_HOPPIP": "MOVE_LEAFAGE",
               "SPECIES_WAILMER": "MOVE_WATER_GUN", "SPECIES_ABRA": "MOVE_CONFUSION",
               "SPECIES_MAGIKARP": "MOVE_TACKLE"}
# A weak attack of each type, for a first stage left with none.
STARTER_BY_TYPE = {"Normal": "MOVE_TACKLE", "Grass": "MOVE_LEAFAGE", "Water": "MOVE_WATER_GUN",
                   "Fire": "MOVE_EMBER", "Electric": "MOVE_THUNDER_SHOCK",
                   "Psychic": "MOVE_CONFUSION", "Bug": "MOVE_BUG_BITE", "Poison": "MOVE_ACID",
                   "Rock": "MOVE_ROCK_THROW", "Ground": "MOVE_MUD_SLAP",
                   "Ice": "MOVE_POWDER_SNOW", "Fighting": "MOVE_KARATE_CHOP", "Flying": "MOVE_GUST",
                   "Ghost": "MOVE_SHADOW_SNEAK", "Dark": "MOVE_BITE", "Dragon": "MOVE_TWISTER",
                   "Steel": "MOVE_METAL_CLAW", "Fairy": "MOVE_FAIRY_WIND"}
# An evolved stage's level 1 is the relearner's menu and the trainer palette;
# it costs the player nothing either way, so it is kept whole (Ian's question
# of 2026-09-27). None keeps every entry.
LEVEL1_ATTACKS, LEVEL1_STATUS = None, None


def _start(entries, species, types, chain):
    """A first stage's level 1 holds a damaging move: the ruled pick, else
    the weakest it has moved to level 1, else a weak attack of its type. An
    evolved stage's level 1 keeps its six strongest attacks and the two
    status moves it would have learnt last."""
    if len(chain) > 1:
        return _trim_level1(entries)
    pick = RULED_FIRST.get(species)
    if pick in _oxide_moves():
        return sorted([(1, pick)] + [e for e in entries if e[1] != pick])
    damaging = [(lv, c) for lv, c in entries
                if ls.strength(ls.oxide_move(_oxide_moves()[c]))[0] == "damage"]
    if any(lv <= 1 for lv, _c in damaging):
        return entries
    if not damaging:
        rec = pokedex.load(data.ROOT, species) or {}
        first_type = (rec.get("types") or ["NORMAL"])[0].title()
        const = STARTER_BY_TYPE.get(first_type, "MOVE_TACKLE")
        return sorted([(1, const)] + entries) if const in _oxide_moves() else entries
    damaging = [(lv, c) for lv, c in entries
                if ls.strength(ls.oxide_move(_oxide_moves()[c]))[0] == "damage"]
    if not damaging or any(lv <= 1 for lv, _c in damaging):
        return entries
    first = min(damaging, key=lambda e: (ls.strength(ls.oxide_move(_oxide_moves()[e[1]]))[1], e[0]))
    return sorted([(1, first[1]) if e == first else e for e in entries])


def _trim_level1(entries):
    """An evolved stage's level 1, cut to its strongest attacks and last
    status moves; the order within level 1 stays weakest first."""
    ones = [c for lv, c in entries if lv <= 1]
    rest = [e for e in entries if e[0] > 1]
    if LEVEL1_ATTACKS is None:
        return entries
    power = lambda c: ls.strength(ls.oxide_move(_oxide_moves()[c]))
    attacks = [c for c in ones if power(c)[0] == "damage"][-LEVEL1_ATTACKS:]
    status = [c for c in ones if power(c)[0] != "damage"][-LEVEL1_STATUS:]
    keep = set(attacks) | set(status)
    return [(1, c) for c in ones if c in keep] + rest


def propose_all():
    """Every species' proposed list, into PROPOSED, then the bare catches
    fixed (fix_bare)."""
    PROPOSED.clear()
    for sp in pokedex.species_list(data.ROOT):
        lst = propose(sp)
        if lst:
            PROPOSED[sp] = lst
    fix_bare()
    return PROPOSED


FIXED = {}


def fix_bare():
    """An evolved form caught wild with no good move by its split's cap gets
    its line's earliest good move by level-up on itself, between the level it
    is reached and the split's cap: known at capture when that is at or under
    the wild level, learnt soon after otherwise. Level-1 entries do not fix
    it: a wild Pokemon's four push them out first, and after capture they
    are the relearner's (Ian, 2026-09-27)."""
    from . import learnwild
    FIXED.clear()
    learnwild.clear()
    caps = learnwild._caps("proposal")
    # Each species once, placed for its earliest bare catch: at that catch's
    # level when the move comes by then (the newest of its four at capture),
    # else at its usual level if that is by the catch's split's cap.
    first = {}
    for r, _have, _pre in bare_catches("proposal"):
        sp = r["species"]
        cap = min(caps.get(r["split"], 100), LEVEL_MAP[-1][1])
        if sp not in first or (r["level"], cap) < first[sp]:
            first[sp] = (r["level"], cap)
    for sp, (wild, cap) in sorted(first.items()):
        rec = pokedex.load(data.ROOT, sp) or {}
        types = {t.title() for t in rec.get("types", [])}
        chain = _chain(sp)
        pool = {}
        for s in chain:
            for lv, c in PROPOSED.get(s, []):
                m = _oxide_moves()[c]
                kind, power = ls.strength(ls.oxide_move(m))
                if kind == "damage" and (power >= GOOD_ANY or
                                         (m["type"].title() in types and power >= GOOD_STAB)):
                    t = target_level(m) or lv
                    pool[c] = min(pool.get(c, 999), t)
        if not pool:
            continue
        const, t = min(pool.items(), key=lambda kv: (kv[1], kv[0]))
        at = reached("oxide", sp) if len(chain) > 1 else 1
        level = max(at, wild if t <= wild else min(t, cap))
        if level > LEVEL_MAP[-1][1]:
            continue
        lst = [e for e in PROPOSED.get(sp, []) if e[1] != const or e[0] <= 1]
        PROPOSED[sp] = ordered(lst + [(level, const)], evolved=len(chain) > 1)
        FIXED[sp] = (const, level)
    learnwild.clear()


def proposal_report(out=sys.stdout):
    """What the proposal changes, and the three analyses on it beside Oxide's
    lists now."""
    from . import learnwild
    propose_all()
    learnwild.clear()
    now = {sp: (pokedex.load(data.ROOT, sp) or {}).get("learnset", []) for sp in PROPOSED}
    added = removed = moved = 0
    for sp, lst in PROPOSED.items():
        a = {c: lv for lv, c in lst}
        b = {c: lv for lv, c in now[sp]}
        added += len(a.keys() - b.keys())
        removed += len(b.keys() - a.keys())
        moved += sum(1 for c in a.keys() & b.keys() if a[c] != b[c])
    over = sum(1 for lst in PROPOSED.values() for lv, _c in lst if lv > LEVEL_MAP[-1][1])
    print(f"proposal: {len(PROPOSED)} species; {added} moves added, {removed} dropped, {moved} "
          f"moved; {over} levels over 78", file=out)
    reasons = collections.Counter()
    for sp, lst in PROPOSED.items():
        kept = {c for _lv, c in lst}
        for _lv, c in now[sp]:
            if c not in kept:
                reasons[WHY[sp].get(c, "learnt before the evolution, and not good enough to keep")] += 1
    for r, n in reasons.most_common():
        print(f"  dropped, {r}: {n}", file=out)
    print(f"  species the bare-catch fix gave a move: {len(FIXED)}", file=out)
    for game in ("kaizo", "oxide", "proposal"):
        n, strong = never_learnt(game)
        print(f"  {game:8}: moves only a Pokemon kept from evolving learns (at or after its "
              f"evolution level, and no later stage by level-up): {n}, {strong} of them strong",
              file=out)
    print("  catches with a good move by their split's cap (known at capture or learnt by "
          "level-up after), by split, now against proposed:", file=out)
    for game in ("oxide", "proposal"):
        rows, _later = learnwild.readings(game)
        caps = learnwild._caps(game)
        by = collections.defaultdict(lambda: [0, 0])
        for r in rows:
            b = by[r["split"]]
            b[0] += 1
            b[1] += any(_good(e) for e in worth(game, r, caps.get(r["split"], 100)))
        print(f"    {game:8} " + ", ".join(f"{s} {b[1] / b[0]:.2f}" for s, b in
                                          sorted(by.items(), key=lambda kv: _oxide_index(kv[0]))),
              file=out)
    for game in ("oxide", "proposal"):
        rows, later = learnwild.readings(game)
        bare = bare_catches(game)
        dl = [r for r in delays(game) if r[8] == "delay" and real_wait(game, r)]
        print(f"  {game:8}: {len({r[1] for r in dl})} pre-evolutions reward waiting; "
              f"{sum(1 for r in rows if r['ends'])} wild slots can end the encounter, "
              f"{sum(1 for r in rows if r['self_ko'])} can knock themselves out, "
              f"{len(later)} have a better version later; {len(bare)} evolved catches "
              f"({len({r['species'] for r, _h, _p in bare})} species) have no good move", file=out)
    learnwild.clear()


def show(name, out=sys.stdout):
    """One line's lists now and as proposed, stage by stage."""
    want = "SPECIES_" + name.upper()
    line = next((ln for ln in oxide_lines() if want in ln), [want])
    for sp in line:
        now = (pokedex.load(data.ROOT, sp) or {}).get("learnset", [])
        new = propose(sp)
        print(f"\n{sp.replace('SPECIES_', '').title()} (reached at "
              f"{reached('oxide', sp) or 'the start'})", file=out)
        names = lambda lst: ", ".join(f"{lv} {_oxide_moves()[c]['name']}" for lv, c in lst)
        print(f"  now:      {names(now)}", file=out)
        print(f"  proposed: {names(new)}", file=out)


def main(argv=None):
    # Run as a script this file is __main__, a second copy of the module that
    # learnwild does not see; the work goes through the package's copy.
    from . import learngen as mod
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["delays", "bare", "propose", "line"])
    ap.add_argument("species", nargs="?", help="for line: a species of the line to show")
    args = ap.parse_args(argv)
    if args.what == "delays":
        mod.delay_report()
    elif args.what == "bare":
        mod.bare_report()
    elif args.what == "propose":
        mod.proposal_report()
    else:
        mod.show(args.species)
    return 0


if __name__ == "__main__":
    sys.exit(main())
