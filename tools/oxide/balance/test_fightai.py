"""The fight simulator's trainer AI, routine by routine, against the game's
own AI at HEAD (src/battle/trainer_ai/script.s and trainer_ai.c): the
Scoring Agent's audit of 2026-09-30.

Each check builds a small battle with the Pokemon and moves the routine
needs, sets the state it reads, and calls the routine directly with the
dice fixed: PASS makes every chance(b, p) succeed, FAIL makes every one
fail, so both branches of a random check are pinned.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_fightai
"""
import functools
import sys

from . import fightai as ai, fightsim as fs, perfectline as pl

IV = {k: 31 for k in ("hp", "at", "df", "sp", "sa", "sd")}
EV = {k: 0 for k in IV}


class Dice:
    """A stand-in for the battle's random source that always returns one
    value: 0.0 passes every chance check, 0.9999 fails every one."""

    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value

    def choice(self, seq):
        return seq[0]


PASS, FAIL = 0.0, 0.9999


@functools.lru_cache(maxsize=None)
def _prepared(boss, player, split, weather):
    """The calculator's rows for one pair of parties, made once: each party
    is a tuple of (species, level, ability, moves, item)."""
    boss_recs = [{"species": sp, "level": lv, "ability": ab, "item": it, "nature": "Hardy",
                  "ivs": IV, "evs": EV, "moves": list(mv)} for sp, lv, ab, mv, it in boss]
    player_recs = [{"constant": "SPECIES_" + sp.upper().replace(" ", "_").replace("-", "_"),
                    "species": sp, "how": "test", "level": lv, "nature": "Hardy", "ivs": IV,
                    "evs": EV, "ability": ab, "moves": list(mv), "fill": False}
                   for sp, lv, ab, mv, _it in player]
    return fs.prepare(split, [boss_recs], weather, given_side=player_recs)


def battle(boss, player, split="Roark", weather=None, flags=7, dice=PASS):
    """A fresh battle with each side's first Pokemon in. boss and player are
    lists of (species, level, ability, [moves]) or with a fifth item."""
    def norm(party):
        return tuple((p[0], p[1], p[2], tuple(p[3]), p[4] if len(p) > 4 else None) for p in party)
    st = _prepared(norm(boss), norm(player), split, weather)
    b = pl.make_battle(st, [f"p{i}" for i in range(len(player))], st["bosses"][0], flags, 0)
    for m in b.p.mons:
        m.item = next((p[4] for p in player if p[0] == m.species and len(p) > 4), None)
    b.rng = Dice(dice)
    return b


def mv(mon, name):
    return next(m for m in mon.moves if m.name == name)


def roll(b, dice):
    """Fix the battle's dice to PASS or FAIL."""
    b.rng = Dice(dice)
    return b


def checks():
    """[(label, ok, note)] for every routine."""
    out = []
    for fn in CHECKS:
        try:
            out += fn()
        except Exception as exc:          # a check that cannot run is a failure, named
            out.append((fn.__name__, False, f"{type(exc).__name__}: {exc}"))
    return out


CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


@check
def fixture():
    b = battle([("Geodude", 16, "Sturdy", ["Rock Throw", "Defense Curl"])],
               [("Barboach", 16, "Oblivious", ["Mud Bomb", "Water Gun"])])
    u, t = b.b.cur(), b.p.cur()
    f = ai.figure(b, u, t, mv(u, "Rock Throw"))
    return [("the fixture builds a battle the AI can read", u.species == "Geodude" and f is not None and f > 0,
             f"{u} vs {t}, Rock Throw {f}")]


def main():
    results = checks()
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
