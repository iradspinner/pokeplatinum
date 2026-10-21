"""The line tester: the OxiDex's Battle tab (docs/oxide/line-tester.md).

Ian sets up a party, from the calculator's party or from a reading's box,
and plays a hand-made line turn by turn against a trainer on the readings'
own simulator and trainer AI. Each position shows both sides, the speeds,
the AI's odds for every move and switch, and the damage both ways; each
turn lists every chance check it makes, any of which he can pin, and an
overview of every way it can go, from the planner's own enumeration. Every
position is a node of a tree he can return to, and a line saves to a file
under ~/oxide-lines/ that reloads to the same tree.

    PYTHONPATH=. python3 -m tools.oxide.encounters.linetester --serve

runs it as the OxiDex server's worker: one JSON request a line on stdin, one
answer a line on stdout. It runs in a process of its own because the
simulator keeps state in its modules, and the tester wraps a few of its
functions there.

Nothing here edits the simulator, the trainer AI or the scorer. The tester
reads them through the interfaces they already have: plplan.ai_distribution
and quick_outcomes for the AI's odds, turn_outcomes' enumeration for the
overview, and dice of its own for play, which answer the same calls as the
planner's EnumDice. Its only reach into their modules is in this process:
a pass-through around perfectline's move functions that records which
Pokemon and move a chance check belongs to, so each check can be labelled,
and around the two replacement functions, so that Ian picks his own
Pokemon after a faint and can pin the trainer's.
"""
import argparse
import collections
import datetime
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import traceback
import zlib

from ..balance import plthreads  # noqa: F401  (one numpy thread, before numpy loads)
from ..balance import data as bdata
from ..balance import fightai
from ..balance import fightsim as fs
from ..balance import perfectline as pl
from ..balance import plgoal3
from ..balance import plniche
from ..balance import plplan
from ..balance import plscore
from ..balance import plteam
from . import calc_trainers

# Where lines are kept, and the notes Ian leaves where the game did
# something else (OXIDE_LINES moves them, for the tests).
LINES = os.environ.get("OXIDE_LINES") or os.path.expanduser("~/oxide-lines")
READINGS = plgoal3.OUT
FORMAT = "oxide-line 1"
OVERVIEWS_KEPT = 24


class Refused(Exception):
    """A request the tester cannot serve, with the reason in words."""


# ---- which Pokemon and move a chance check belongs to ----------------------------------------
#
# Each wrapped function pushes a frame (phase, user, move, target) while it
# runs and changes nothing else, so a die cast inside it can say whose it
# is. The planner's dice never ask, so the wrappers cannot change what any
# enumeration or reading finds; a test checks that turn_outcomes gives the
# same positions with them as without.

_STACK = []
_INSTALLED = []            # (module, name, original), to take them out again


def _frame():
    return _STACK[-1] if _STACK else None


def _pusher(orig, phase, order):
    """A pass-through for orig that pushes (phase, user, move, target),
    reading them from its arguments in `order` ("amd": b, att, mv, dfn;
    "adm": b, att, dfn, mv)."""
    def wrapped(b, x, y, z, *rest, **kw):
        if order == "amd":
            _STACK.append((phase, x, y, z))
        else:
            _STACK.append((phase, x, z, y))
        try:
            return orig(b, x, y, z, *rest, **kw)
        finally:
            _STACK.pop()
    wrapped.__wrapped__ = orig
    return wrapped


def _status_pusher(orig):
    def wrapped(b, target, status):
        _STACK.append(("status", target, None, target))
        try:
            return orig(b, target, status)
        finally:
            _STACK.pop()
    wrapped.__wrapped__ = orig
    return wrapped


def _helps_pusher(orig):
    def wrapped(b, mon, kind, p):
        _STACK.append(("helps", mon, None, mon))
        try:
            return orig(b, mon, kind, p)
        finally:
            _STACK.pop()
    wrapped.__wrapped__ = orig
    return wrapped


def _phase_pusher(orig, phase):
    def wrapped(*a, **kw):
        _STACK.append((phase, None, None, None))
        try:
            return orig(*a, **kw)
        finally:
            _STACK.pop()
    wrapped.__wrapped__ = orig
    return wrapped


def _switch_pusher(orig):
    def wrapped(b, side, index, *a, **kw):
        mon = side.mons[index] if 0 <= index < len(side.mons) else None
        _STACK.append(("switch", mon, None, None))
        try:
            return orig(b, side, index, *a, **kw)
        finally:
            _STACK.pop()
    wrapped.__wrapped__ = orig
    return wrapped


# The play in progress (Play), whose replacements Ian chooses; None while
# the planner's own enumeration runs, which then picks as it always does.
_PLAY = None


class NeedReplacement(Exception):
    """The turn reached a point where Ian sends in a Pokemon he has not
    chosen yet."""

    def __init__(self, key, options, why):
        super().__init__(key)
        self.key, self.options, self.why = key, options, why


def _player_replacement(orig):
    def wrapped(b):
        p = _PLAY
        if p is None or b is not p.battle:
            return orig(b)
        side = b.p
        options = [i for i, m in enumerate(side.mons) if m.alive() and i != side.active]
        if not options:
            return None
        key = f"replace|p#{p.replacements}"
        p.replacements += 1
        out = side.cur()
        why = f"after {out.species} faints" if not out.alive() else f"as {out.species}'s move switches it out"
        pin = p.pins.get(key)
        if isinstance(pin, int) and pin in options:
            idx, how = pin, "your choice"
        elif len(options) == 1:
            idx, how = options[0], "the only one left"
        elif p.likeliest:
            idx, how = options[0], "you choose when it happens"
        else:
            raise NeedReplacement(key, options, why)
        p.record({"key": key, "kind": "replacement", "side": "p", "who": out.key,
                  "label": f"Your Pokemon to send in {why}",
                  "options": [side.mons[i].species for i in options], "values": options,
                  "probs": None, "outcome": options.index(idx), "value": idx, "how": how})
        return idx
    wrapped.__wrapped__ = orig
    return wrapped


def _ai_replacement(orig):
    def wrapped(b, side, target, owner=None):
        idx = orig(b, side, target, owner)
        p = _PLAY
        if p is None or b is not p.battle or idx is None or side is not b.b:
            return idx
        options = [i for i, m in enumerate(side.mons) if m.alive() and i not in (side.active, side.active2)]
        if idx not in options:
            options.append(idx)
        key = f"replace|b#{p.ai_replacements}"
        p.ai_replacements += 1
        pin = p.pins.get(key)
        chosen, how = (pin, "pinned") if isinstance(pin, int) and pin in options else (idx, "the AI's pick")
        gone = side.cur()
        why = f"after {gone.species} faints" if not gone.alive() else f"as {gone.species}'s move switches it out"
        p.record({"key": key, "kind": "replacement", "side": "b", "who": gone.key,
                  "label": f"The trainer's Pokemon to send in {why} (the AI's pick is certain; a pin overrides it)",
                  "options": [side.mons[i].species for i in options], "values": options,
                  "probs": [1.0 if i == idx else 0.0 for i in options],
                  "outcome": options.index(chosen), "value": chosen, "how": how})
        return chosen
    wrapped.__wrapped__ = orig
    return wrapped


def install():
    """Put the pass-throughs in place, once per process."""
    if _INSTALLED:
        return
    plan = [(pl, "use_move", lambda f: _pusher(f, "move", "amd")),
            (pl, "attack", lambda f: _pusher(f, "move", "amd")),
            (pl, "status_move", lambda f: _pusher(f, "move", "amd")),
            (pl, "accuracy_hits", lambda f: _pusher(f, "accuracy", "adm")),
            (pl, "crash", lambda f: _pusher(f, "crash", "adm")),
            (pl, "rolled_hits", lambda f: _pusher(f, "hits", "adm")),
            (pl, "crit_hits", lambda f: _pusher(f, "crit", "adm")),
            (pl, "multi_hit", lambda f: _pusher(f, "move", "amd")),
            (pl, "beat_up", lambda f: _pusher(f, "move", "amd")),
            (pl, "_after_attack", lambda f: _pusher(f, "effects", "amd")),
            (fs, "hit_aftermath", lambda f: _pusher(f, "aftermath", "adm")),
            (fs, "end_of_turn", lambda f: _phase_pusher(f, "end")),
            (fs, "switch_in", _switch_pusher),
            (fs, "helps", _helps_pusher),
            (fs, "player_replacement", _player_replacement),
            (fightai, "replacement", _ai_replacement)]
    for mod, name, make in plan:
        orig = getattr(mod, name)
        setattr(mod, name, make(orig))
        _INSTALLED.append((mod, name, orig))
    # perfectline put its own give_status into fightsim, and fightsim's
    # accuracy check for a landing Future Sight is perfectline's: both are
    # wrapped where they are called from.
    give = _status_pusher(pl.give_status)
    _INSTALLED.append((pl, "give_status", pl.give_status))
    _INSTALLED.append((fs, "give_status", fs.give_status))
    pl.give_status = fs.give_status = give
    _INSTALLED.append((fs, "DICE_ACCURACY", fs.DICE_ACCURACY))
    fs.DICE_ACCURACY = pl.accuracy_hits


def uninstall():
    """Take the pass-throughs out again (a test compares with and without)."""
    while _INSTALLED:
        mod, name, orig = _INSTALLED.pop()
        setattr(mod, name, orig)


# ---- the label of a check -----------------------------------------------------------------------

STATUS_WORDS = {"slp": "asleep", "par": "paralysed", "psn": "poisoned", "tox": "badly poisoned",
                "brn": "burned", "frz": "frozen"}
YES_NO = {
    "crit": ("critical hit", ("no critical hit", "critical hit")),
    "paralysis": ("fully paralysed", ("moves", "fully paralysed")),
    "confusion": ("hurts itself in confusion", ("acts", "hurts itself")),
    "love": ("immobilised by love", ("acts", "immobilised")),
    "flinch": ("the target flinches", ("no flinch", "flinches")),
    "kingsrock": ("King's Rock flinch", ("no flinch", "flinches")),
    "statdrop": ("its stat drop", ("no drop", "drops")),
    "statup": ("its stat rise", ("no rise", "rises")),
    "status": ("its added effect", ("no added effect", "the effect lands")),
    "confusehit": ("confuses the target", ("not confused", "confused")),
    "focusband": ("the Focus Band holds", ("does not hold", "holds")),
    "ohko": ("knocks out in one hit", ("fails", "knocks out")),
    "shedskin": ("Shed Skin cures it", ("not cured", "cured")),
    "cursedbody": ("Cursed Body disables the move", ("no", "disables")),
}


def _name(mon):
    return mon.species if mon is not None else "?"


def _owner(mon):
    return "Your" if mon is not None and mon.side == "p" else "The trainer's"


def _subject(frame, b=None):
    """(who key, what, phase, words) for the innermost frame: the key's
    parts from that frame, and the words from the move the check belongs to
    where one is running, naming the Pokemon it falls on when that is
    another (Sleep Powder's sleep on its target, Taunt's length on the
    taunted)."""
    if frame is None:
        return "field", "turn", "turn", "This turn"
    phase, user, mv, target = frame
    who = user.key if user is not None else "field"
    what = mv.name if mv is not None else phase
    if user is None:
        words = {"end": "End of turn", "turn": "This turn"}.get(phase, phase)
    elif phase == "switch":
        words = f"{_owner(user)} {user.species} coming in"
    elif mv is not None:
        words = f"{_owner(user)} {user.species}'s {mv.name}"
    else:
        outer = next((f for f in reversed(_STACK) if f[1] is not None and f[2] is not None), None)
        if outer is not None and outer[1] is not user:
            words = f"{_owner(outer[1])} {outer[1].species}'s {outer[2].name} on {_owner(user).lower()} {user.species}"
        elif outer is not None:
            words = f"{_owner(user)} {user.species}'s {outer[2].name}"
        else:
            words = f"{_owner(user)} {user.species}"
    return who, what, phase, words


def _victim(frame, side):
    """The Pokemon a duration or a roll of `side` falls on: the frame's
    target or user of that side, else that side's active Pokemon."""
    if frame is not None:
        _ph, user, _mv, target = frame
        for m in (target, user):
            if m is not None and m.side == side:
                return m
    return None


class Keys:
    """Each check's key: who, which move, which part of it, which call, and
    its count among checks alike this turn, so a pin finds its check again
    after the list is rebuilt, and is dropped once no check has its key."""

    def __init__(self):
        self.counts = {}

    def key(self, method, kind):
        who, what, phase, words = _subject(_frame())
        sig = f"{who}|{what}|{phase}|{method}:{kind or ''}"
        n = self.counts.get(sig, 0)
        self.counts[sig] = n + 1
        return f"{sig}#{n}", words


def binary_label(words, method, kind, frame):
    """(question, the two options' words) for a yes-or-no check."""
    phase = frame[0] if frame else "turn"
    if phase == "accuracy":
        return f"{words} hits", ("hits", "misses")
    if kind in YES_NO:
        q, opts = YES_NO[kind]
        if phase == "aftermath" and frame is not None and frame[3] is not None:
            return f"{_owner(frame[3])} {frame[3].species}'s {frame[3].ability or 'ability'} on {words}: {q}", opts
        return f"{words}: {q}", opts
    if method == "thaws":
        return f"{words} thaws out", ("stays frozen", "thaws")
    if method == "tie":
        return "Speed tie: who moves first", ("the trainer", "you")
    if kind is None and frame is not None and frame[2] is not None and frame[2].effect == "ONE_HIT_KO":
        return f"{words}: knocks out in one hit", ("fails", "knocks out")
    return f"{words}: {kind or 'a chance'}", ("no", "yes")


# ---- the tester's dice -----------------------------------------------------------------------------

def roll_groups(dmg, hp):
    """EnumDice.roll_grouped's grouping, as it groups: the rolls that knock
    out, then at most ROLL_BANDS bands of like damage among the rest."""
    groups = []
    kills = [r for r in range(16) if dmg[r] >= hp]
    if kills:
        groups.append(kills)
    rest = [r for r in range(16) if dmg[r] < hp]
    values = sorted({dmg[r] for r in rest})
    if len(values) <= plplan.ROLL_BANDS:
        groups += [[r for r in rest if dmg[r] == v] for v in values]
    else:
        n = len(rest)
        cuts = [round(n * k / plplan.ROLL_BANDS) for k in range(plplan.ROLL_BANDS + 1)]
        groups += [rest[cuts[k]:cuts[k + 1]] for k in range(plplan.ROLL_BANDS) if cuts[k + 1] > cuts[k]]
    return groups


def _roll_info(frame, side_hp, dmg, method):
    """What a damage roll's options show: each roll's damage and the HP it
    leaves, against whom."""
    phase = frame[0] if frame else "turn"
    if frame is None:
        victim = None
    elif phase == "crash":
        victim = frame[1]
    else:
        victim = frame[3]
    hp = side_hp if side_hp is not None else (victim.hp if victim is not None else None)
    maxhp = victim.maxhp if victim is not None else None
    return {"dmg": dmg, "hp": hp, "maxhp": maxhp, "victim": victim.side if victim is not None else None,
            "victim_name": _name(victim) if victim is not None else None}


class TesterDice:
    """Dice for play: the same calls as the planner's EnumDice, each made a
    check with its real odds; a pinned check takes its pin and the rest are
    drawn at their odds from `draw`, or, for the list shown before a turn is
    played, take their likeliest outcome. Every roll is exact: where
    perfectline hands over the damage of each roll (roll_grouped), the one
    drawn or pinned is played, never a band's stand-in."""
    mode = "run"
    luck = "real"
    one_crit = False

    def __init__(self, play, rng):
        self.play = play
        self.rng = rng
        self.crit_used = False

    def _choose(self, method, kind, probs, options, label, extra=None):
        p = self.play
        key, _words = p.keys.key(method, kind)
        pin = p.pins.get(key)
        how = None
        if isinstance(pin, int) and 0 <= pin < len(probs) and probs[pin] > 0:
            o, how = pin, "pinned"
        else:
            if pin is not None:
                p.dropped.append({"key": key, "label": label, "why": "the pinned outcome cannot happen here"})
            o, how = (_likeliest(probs), "likeliest") if p.likeliest else (_draw(p.draw, probs), "drawn")
        who, what, phase, _w = _subject(_frame())
        rec = {"key": key, "kind": kind or method, "method": method, "label": label, "who": who,
               "options": list(options), "probs": list(probs), "outcome": o, "how": how}
        if extra:
            rec.update(extra)
        p.record(rec)
        return o

    def _yes(self, p, method, kind):
        if p <= 0:
            return False
        if p >= 1:
            return True
        frame = _frame()
        _who, _what, _phase, words = _subject(frame)
        if method == "thaws":
            words = f"{_owner(frame[1] if frame else None)} {_name(frame[1] if frame else None)}" if frame else words
        q, opts = binary_label(words, method, kind, frame)
        return self._choose(method, kind, (1 - p, p), opts, q) == 1

    def bad(self, kind, p):
        return self._yes(p, "bad", kind)

    def good(self, p, kind=None):
        return self._yes(p, "good", kind)

    def lands_on_player(self, kind, p):
        return self._yes(p, "lands", kind)

    def roll(self, top):
        frame = _frame()
        _who, _what, _phase, words = _subject(frame)
        dmg = [None] * 16
        if frame is not None and frame[2] is not None and frame[1] is not None and frame[3] is not None:
            att, mv, dfn = frame[1], frame[2], frame[3]
            try:
                if mv.effect == "STRUGGLE":
                    dmg = [pl.struggle_damage(att, dfn, 85 + r, self.play.battle.wonder_room) for r in range(16)]
                else:
                    dmg = [self.play.battle.damage(att, dfn, mv, roll=r) for r in range(16)]
            except Exception:
                dmg = [None] * 16
        info = _roll_info(frame, None, dmg, "roll")
        return self._choose("roll", None, (1 / 16,) * 16, [f"roll {r + 1}" for r in range(16)],
                            f"{words}: damage roll", {"rolls": info})

    def roll_grouped(self, damage, hp):
        dmg = [damage(r) for r in range(16)]
        groups = roll_groups(dmg, hp)
        if len(groups) == 1:
            g = groups[0]
            return g[len(g) // 2]           # every roll alike: no check, as EnumDice makes none
        frame = _frame()
        _who, _what, phase, words = _subject(frame)
        info = _roll_info(frame, hp, dmg, "roll_grouped")
        info["groups"] = groups
        what = "crash damage roll" if phase == "crash" else "damage roll"
        return self._choose("roll", None, (1 / 16,) * 16, [f"roll {r + 1}" for r in range(16)],
                            f"{words}: {what}", {"rolls": info})

    def pick_weighted(self, items, weights):
        tot = sum(weights)
        frame = _frame()
        _who, _what, phase, words = _subject(frame)
        mv = frame[2] if frame else None
        if phase == "hits":
            q = f"{words}: number of hits"
            opts = [f"{h} hits" for h in items]
        elif mv is not None and mv.name == "Magnitude":
            q, opts = f"{words}: its power", [f"power {x}" for x in items]
        elif mv is not None and mv.name == "Present":
            q, opts = f"{words}: its power", ["heals" if not x else f"power {x}" for x in items]
        elif mv is not None and mv.effect == "FICKLE_BEAM":
            q, opts = f"{words}: goes all out", [str(x) for x in items]
        else:
            q, opts = f"{words}: a pick", [str(x) for x in items]
        o = self._choose("pick", None, tuple(w / tot for w in weights), opts, q)
        return items[o]

    def crit_count(self, n, p):
        if p >= 1:
            return n
        _who, _what, _phase, words = _subject(_frame())
        probs = tuple(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1))
        return self._choose("crits", None, probs, [f"{k} of {n}" for k in range(n + 1)],
                            f"{words}: critical hits")

    def _length(self, side, method, first, n, what):
        frame = _frame()
        mon = _victim(frame, side)
        if mon is None:
            b = self.play.battle
            mon = (b.p if side == "p" else b.b).cur()
        _who, _what, _phase, words = _subject(frame)
        # Named once: "it" where the words already name the Pokemon, as the
        # move's user or as the one it falls on.
        whose = f"{_owner(mon).lower()} {mon.species}"
        named = words.startswith(f"{_owner(mon)} {mon.species}") or words.endswith(f"on {whose}")
        label = f"{words}: {what.format('it' if named else whose)}"
        probs = (1 / n,) * n
        opts = [f"{first + i}" for i in range(n)]
        return first + self._choose(method, None, probs, opts, label, {"subject": mon.key})

    def sleep(self, side):
        return self._length(side, "sleep", 1, 4, "how long {} sleeps (the counter fightsim keeps)")

    def confusion(self, side):
        return self._length(side, "confusion", 2, 4, "how long {} stays confused (the counter fightsim keeps)")

    def taunt(self, side):
        return self._length(side, "taunt", 3, 3, "how long the Taunt on {} lasts")

    def bind(self, side):
        return self._length(side, "bind", 3, 4, "how long {} stays bound")

    def outrage(self, side):
        return self._length(side, "outrage", 2, 2, "how long {} stays locked into its move")

    def thaws(self, mon):
        _STACK.append(("thaw", mon, None, mon))
        try:
            return self._yes(0.2, "thaws", None)
        finally:
            _STACK.pop()

    def tie_player_first(self):
        return self._yes(0.5, "tie", None)

    def choice(self, kind, n):
        if n <= 1:
            return 0
        frame = _frame()
        _who, _what, _phase, words = _subject(frame)
        opts = [f"{i + 1}" for i in range(n)]
        what = f"{kind} ({n} ways)"
        if kind == "tri" and n == 3:
            opts, what = ["freeze", "paralysis", "burn"], "which status"
        elif kind == "tie" and n == 2:
            # fightsim.coin: the order of two Pokemon of equal Speed at the
            # turn's end (or another even coin the battle tosses).
            opts, what = ["one way", "the other way"], "a coin between two equally fast Pokemon"
        elif kind in ("moody", "harvest", "trace"):
            b = self.play.battle
            ability = {"moody": "Moody", "harvest": "Harvest", "trace": "Trace"}[kind]
            mon = next((m for m in (b.p.cur(), b.b.cur()) if m.ability == ability), None)
            if mon is not None:
                words = f"{_owner(mon)} {mon.species}'s {ability}"
        return self._choose("choice", kind, (1 / n,) * n, opts, f"{words}: {what}")

    def confusion_roll(self):
        frame = _frame()
        mon = frame[1] if frame else None
        dmg = [pl.confusion_damage(mon, 85 + r) for r in range(16)] if mon is not None else [None] * 16
        info = {"dmg": dmg, "hp": mon.hp if mon else None, "maxhp": mon.maxhp if mon else None,
                "victim": mon.side if mon else None, "victim_name": _name(mon)}
        return 85 + self._choose("confusion roll", None, (1 / 16,) * 16, [f"roll {r + 1}" for r in range(16)],
                                 f"{_owner(mon)} {_name(mon)}: its confusion self-hit's damage roll", {"rolls": info})


def _draw(rng, probs):
    x = rng.random()
    acc = 0.0
    last = 0
    for i, p in enumerate(probs):
        if p <= 0:
            continue
        last = i
        acc += p
        if x < acc:
            return i
    return last


def _likeliest(probs):
    best = max(probs)
    # The middle of equal odds, as a band's stand-in is its middle roll.
    ties = [i for i, p in enumerate(probs) if p >= best - 1e-12]
    return ties[len(ties) // 2] if len(ties) > 2 else ties[0]


class LabelledEnumDice(plplan.EnumDice):
    """The planner's enumerating dice, unchanged in what they decide, with
    each event keyed as the tester's dice key their checks, so an outcome of
    the overview can be followed by pinning the checks that define it."""

    def __init__(self, script, rng, battle):
        super().__init__(script, rng)
        self.keys = Keys()
        self.notes = []
        self.battle = battle

    def _note(self, method, kind, extra=None, event=True):
        key, words = self.keys.key(method, kind)
        rec = {"key": key, "method": method, "kind": kind or method, "event": len(self.events) if event else None}
        if extra:
            rec.update(extra)
        self.notes.append(rec)
        return rec

    def bad(self, kind, p):
        if 0 < p < 1:
            self._note("bad", kind)
        return super().bad(kind, p)

    def good(self, p, kind=None):
        if 0 < p < 1:
            self._note("good", kind)
        return super().good(p, kind)

    def lands_on_player(self, kind, p):
        if 0 < p < 1:
            self._note("lands", kind)
        return super().lands_on_player(kind, p)

    def roll(self, top):
        self._note("roll", None)
        return super().roll(top)

    def roll_grouped(self, damage, hp):
        dmg = [damage(r) for r in range(16)]
        groups = roll_groups(dmg, hp)
        if len(groups) == 1:
            g = groups[0]
        else:
            frame = _frame()
            rec = self._note("roll", None, {"rolls": dict(_roll_info(frame, hp, dmg, "roll_grouped"),
                                                         groups=groups)})
            g = groups[self._ev(tuple(len(x) / 16 for x in groups))]
            rec["group"] = groups.index(g)
        return g[len(g) // 2]

    def pick_weighted(self, items, weights):
        self._note("pick", None)
        return super().pick_weighted(items, weights)

    def crit_count(self, n, p):
        if p < 1:
            self._note("crits", None)
        return super().crit_count(n, p)

    def sleep(self, side):
        self._note("sleep", None)
        return super().sleep(side)

    def confusion(self, side):
        self._note("confusion", None)
        return super().confusion(side)

    def taunt(self, side):
        self._note("taunt", None)
        return super().taunt(side)

    def bind(self, side):
        self._note("bind", None)
        return super().bind(side)

    def outrage(self, side):
        self._note("outrage", None)
        return super().outrage(side)

    def thaws(self, mon):
        _STACK.append(("thaw", mon, None, mon))
        try:
            self._note("thaws", None)
            return super().thaws(mon)
        finally:
            _STACK.pop()

    def tie_player_first(self):
        self._note("tie", None)
        return super().tie_player_first()

    def choice(self, kind, n):
        if n > 1:
            self._note("choice", kind)
        return super().choice(kind, n)

    def confusion_roll(self):
        self._note("confusion roll", None)
        return super().confusion_roll()


# ---- one turn, played ---------------------------------------------------------------------------------

class Play:
    """One turn being played: its pins, its dice and the checks it made."""

    def __init__(self, battle, pins, draw, likeliest):
        self.battle = battle
        self.pins = dict(pins or {})
        self.draw = draw
        self.likeliest = likeliest
        self.keys = Keys()
        self.checks = []
        self.dropped = []
        self.replacements = 0
        self.ai_replacements = 0

    def record(self, rec):
        rec["n"] = len(self.checks)
        self.checks.append(rec)


def action_label(b, a, side="p"):
    if a[0] == "move":
        return a[1].name
    if a[0] == "switch":
        mons = (b.p if side == "p" else b.b).mons
        return "switch to " + mons[a[1]].species
    return str(a[1])


def ai_label(b, a):
    return action_label(b, a, "b")


def resolve_action(b, action):
    """The player's action as perfectline's turn takes it, from the page's
    ["move", name] or ["switch", party index]."""
    me = b.p.cur()
    kind, what = action[0], action[1]
    if kind == "move":
        if what == "Struggle":
            return "move", fs.move("Struggle")
        for m in me.moves:
            if m.name == what:
                return "move", m
        forced = fightai.forced_choice(me)
        if forced is not None and forced[1].name == what:
            return forced
        raise Refused(f"{me.species} has no move {what}")
    if kind == "switch":
        idx = int(what)
        if not 0 <= idx < len(b.p.mons) or idx == b.p.active or not b.p.mons[idx].alive():
            raise Refused("that Pokemon cannot come in")
        if fs.trapped(b, me):
            raise Refused(f"{me.species} is trapped and cannot switch")
        return "switch", idx
    raise Refused(f"unknown action {action}")


def run_turn(parent, action, pins, seed, likeliest=False):
    """Play one turn from `parent` (a battle, left as it is): the Quick Claw
    rolls and the trainer's choice first, settled as the turn begins and
    pinned or drawn like any other check, then perfectline's turn on the
    tester's dice. (battle after, the Play), or NeedReplacement raised with
    the Play so far kept on the exception (.play)."""
    global _PLAY
    draw = random.Random(seed)
    c = plplan.clone(parent)
    play = Play(c, pins, draw, likeliest)
    a = resolve_action(c, action)
    quick = {}
    for m in (c.p.cur(), c.b.cur()):
        if fs.custap_fires(m, c):
            quick[m.key] = True
        elif m.item == "Quick Claw":
            key = f"quick|{m.key}#0"
            probs = (0.8, 0.2)
            pin = play.pins.get(key)
            if isinstance(pin, int) and pin in (0, 1):
                o, how = pin, "pinned"
            else:
                o, how = (0, "likeliest") if likeliest else (_draw(draw, probs), "drawn")
            play.record({"key": key, "kind": "quickclaw", "method": "quick", "who": m.key,
                         "label": f"{_owner(m)} {m.species}'s Quick Claw fires",
                         "options": ["no", "fires"], "probs": list(probs), "outcome": o, "how": how})
            quick[m.key] = o == 1
        else:
            quick[m.key] = False
    c.quick = quick
    dist = plplan.ai_distribution(c)
    labels = [ai_label(c, x) for x, _p in dist]
    probs = [p for _x, p in dist]
    pin = play.pins.get("ai|choice#0")
    if isinstance(pin, str) and pin in labels:
        o, how = labels.index(pin), "pinned"
    else:
        if pin is not None:
            play.dropped.append({"key": "ai|choice#0", "label": "The trainer's choice",
                                 "why": f"{pin} is not among its choices here"})
        o, how = (0, "likeliest") if likeliest else (_draw(draw, probs), "drawn")
    if len(dist) > 1 or pin is not None:
        play.record({"key": "ai|choice#0", "kind": "ai", "method": "ai", "who": c.b.cur().key,
                     "label": f"The trainer's {c.b.cur().species} chooses", "options": labels,
                     "probs": probs, "outcome": o, "value": labels[o], "how": how})
    aa = dist[o][0]
    c.dice = TesterDice(play, random.Random(_mix(seed, "turn")))
    c.rng = c.dice.rng
    _PLAY = play
    try:
        pl._turn(c, a, aa)
    except NeedReplacement as exc:
        exc.play = play
        raise
    finally:
        _PLAY = None
        c.dice = c.rng = None
    for key, pin in play.pins.items():
        if key.startswith("replace|") or key == "ai|choice#0" or key.startswith("quick|"):
            continue
        if not any(ch["key"] == key for ch in play.checks) and not any(d["key"] == key for d in play.dropped):
            play.dropped.append({"key": key, "label": key, "why": "no such check this turn"})
    return c, play


def _mix(*parts):
    return zlib.crc32(":".join(str(x) for x in parts).encode())


# ---- the overview: the planner's own enumeration, every outcome kept with its checks ----------

def enumerate_turn(c0, a, aa, key):
    """turn_outcomes, as the planner runs it, keeping each merged outcome's
    members and what their dice decided: [{"c": position, "p": probability,
    "merge": merge key, "members": [(position, probability, dice)]}], in
    turn_outcomes' own order, its positions the ones it returns."""
    raw, stack = [], [()]
    while stack and len(raw) < plplan.BRANCH_CAP:
        script = stack.pop()
        c = plplan.clone(c0)
        d = LabelledEnumDice(script, random.Random(plplan._mix(key, len(raw))), c)
        c.dice, c.rng = d, d.rng
        pl._turn(c, a, aa)
        prob = 1.0
        for probs, o in zip(d.events, d.picked):
            prob *= probs[o]
        raw.append((c, prob, d))
        for i in range(len(script), len(d.events)):
            for o in range(1, len(d.events[i])):
                if d.events[i][o] > 0:
                    stack.append(script + (0,) * (i - len(script)) + (o,))
    total = sum(p for _c, p, _d in raw)
    merged = {}
    for c, p, d in raw:
        k = plplan.merge_key(c)
        if k in merged:
            rep, q, members = merged[k]
            merged[k] = ((rep if q >= p else (c, d)), q + p, members + [(c, p, d)])
        else:
            merged[k] = ((c, d), p, [(c, p, d)])
    return [{"c": rep[0], "dice": rep[1], "p": q / total, "merge": k, "members": members}
            for k, (rep, q, members) in merged.items()]


# ---- building a fight --------------------------------------------------------------------------------

class _BranchTrainers:
    """While a fight is prepared, the trainers' files from another branch:
    data.oxide_trainers answers with those trainers rebuilt from the branch's
    files, and plscore.with_genders reads the branch's file for them. Taken
    out again as soon as the fight is prepared."""

    def __init__(self, branch, stems):
        self.branch, self.stems = branch, stems

    def __enter__(self):
        root = bdata.ROOT
        if not re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./~^-]*", self.branch or ""):
            raise Refused(f"{self.branch!r} is not a branch or commit name")
        files = {}
        for stem in self.stems:
            try:
                text = subprocess.run(["git", "-C", root, "show", f"{self.branch}:res/trainers/data/{stem}.json"],
                                      check=True, capture_output=True, text=True).stdout
            except subprocess.CalledProcessError as exc:
                raise Refused(f"no res/trainers/data/{stem}.json on {self.branch}: {exc.stderr.strip()}")
            files[stem] = json.loads(text)
        base = bdata.oxide_trainers()
        out = dict(base)
        for tr_id, t in base.items():
            if t["stem"] in files:
                party = calc_trainers.build_trainer(root, t["stem"], files[t["stem"]])
                out[tr_id] = dict(t, ai=party[0][1].get("ai") if party else t["ai"],
                                  party=[bdata._mon(sp, s) for sp, s in party])
        self.saved = (bdata.oxide_trainers, plscore.with_genders)
        orig_genders = plscore.with_genders
        bdata.oxide_trainers = lambda root=bdata.ROOT: out
        plscore.with_genders = lambda t, tr=None: orig_genders(t, tr if tr is not None else files.get(t["stem"]))
        return files

    def __exit__(self, *exc):
        bdata.oxide_trainers, plscore.with_genders = self.saved
        return False


def fight_trainers(key):
    """The trainer records a fight key names, in variant order."""
    kind, k = plscore.parse_fight(key)
    if kind == "story":
        fight = next((x for x in bdata.fights()["fights"] if x["key"] == k), None)
        if fight is None:
            raise Refused(f"no story fight {k}")
        return fight, bdata.fight_trainers("oxide", fight)
    t = bdata.oxide_trainers().get(k)
    if t is None:
        raise Refused(f"no trainer {k}")
    return None, [t]


def prepare_fight(key, records, branch=None):
    """plscore.prepare for this party, the trainers' files read from
    `branch` when one is named."""
    if not branch:
        return plscore.prepare(plscore.parse_fight(key), given_side=records)
    fight, trainers = fight_trainers(key)
    with _BranchTrainers(branch, [t["stem"] for t in trainers]):
        return plscore.prepare(plscore.parse_fight(key), given_side=records)


def fight_of_trainer(tr_id):
    """(fight key, variant) for a trainer by id: its story fight, as the
    variant it is, else the trainer alone."""
    for fight in bdata.fights()["fights"]:
        if tr_id in fight["tr_ids"]:
            ts = bdata.fight_trainers("oxide", fight)
            for i, t in enumerate(ts):
                if t["tr_id"] == tr_id:
                    return fight["key"], i
    if tr_id not in bdata.oxide_trainers():
        raise Refused(f"no trainer with id {tr_id}")
    return f"tr:{tr_id}", 0


def fight_label(key):
    try:
        return plscore.fight_label(plscore.parse_fight(key))
    except Exception:
        return key


def build(setup):
    """The battle a setup describes: (st, team keys, boss keys, flags, root
    battle, the fight's split)."""
    records = setup["records"]
    if not 1 <= len(records) <= 6:
        raise Refused("a party is one to six Pokemon")
    prep = prepare_fight(setup["fight"], records, setup.get("branch"))
    if prep is None or prep.get("doubles"):
        raise Refused("this is a double or tag battle, which version 1 leaves out")
    st = prep["st"]
    st["item_stock"] = dict(fs.player_items(prep["split"]))
    v = setup.get("variant") or 0
    if not 0 <= v < len(prep["variants"]):
        raise Refused(f"the fight has no variant {v}")
    boss_keys, flags, _s = prep["variants"][v]
    team = [f"p{i}" for i in range(len(records))]
    for k, mv in zip(team, setup["moves"]):
        if mv:
            st["moves"][k] = list(mv)[:4]
    if setup.get("held") is not None:
        st["held"] = {k: it or None for k, it in zip(team, setup["held"])}
    lead = setup.get("lead") or 0
    b = plplan.make_battle(st, team, boss_keys, flags, lead)
    b.dice = b.rng = None
    return st, team, boss_keys, flags, b, prep["split"]


# ---- the party, from a reading's box or from the calculator ---------------------------------------

_BOXES = {}


def reading_fights():
    """Goal 3's single battles, the fights a reading reads."""
    return [{"slug": f["slug"], "name": f["name"], "split": f["split"], "kind": f["kind"]}
            for f in plgoal3.fights()]


def latest_reading(slug, seed, labels):
    """The newest reading of this fight on this box whose six are all in the
    box: {"run", "six", "moves", "items"}, or None."""
    best = None
    pattern = os.path.join(READINGS, "*", slug, f"box{seed}", "result.json")
    import glob
    for path in glob.glob(pattern):
        try:
            with open(path) as fh:
                r = json.load(fh)
        except (OSError, ValueError):
            continue
        six = r.get("winner") or []
        if not six or not all(x in labels for x in six):
            continue
        t = os.path.getmtime(path)
        if best is None or t > best[0]:
            best = (t, {"run": r.get("run"), "six": six, "moves": r.get("moves") or {},
                        "items": r.get("items") or {}, "when": datetime.datetime.fromtimestamp(t).isoformat(
                            timespec="minutes")})
    return best[1] if best else None


def reading_box(slug, seed):
    """A reading's box as plgoal3 reads it (roll, cut, met, level, records),
    with the reading's six and movesets where one has chosen them."""
    k = (slug, int(seed))
    if k in _BOXES:
        return _BOXES[k]
    f = next((x for x in plgoal3.fights() if x["slug"] == slug), None)
    if f is None:
        raise Refused(f"goal 3 has no single battle {slug}")
    whole = plgoal3.roll(f["split"], int(seed))
    caught = plgoal3.cut(whole, f)
    key, v, trainer = plgoal3.met(f, whole[0].species)
    lvl = plgoal3.level(f, trainer)
    recs = plgoal3.records(caught, f, lvl, int(seed))
    labels = [r["label"] for r in recs]
    stock = fs.player_items(f["split"])
    out = {"slug": slug, "seed": int(seed), "fight": key, "variant": v, "name": f["name"], "split": f["split"],
           "level": lvl, "trainer": trainer.get("name"), "starter": whole[0].species,
           "foes": [f"{m['species']} {m['level']}" for m in trainer["party"]],
           "members": [{"label": r["label"], "species": r["species"], "constant": r["constant"],
                        "level": r["level"], "ability": r["ability"], "pool": list(r["moves"]),
                        "area": r.get("area")} for r in recs],
           "records": recs, "stock": stock, "items": stock_items(stock),
           "reading": latest_reading(slug, seed, labels)}
    _BOXES[k] = out
    return out


def stock_items(stock):
    """{item: copies} the player holds by the split, from player_items: a
    booster each, and the Leftovers and Sitrus Berries counted."""
    out = {it: 1 for it in stock["boosters"].values()}
    for it in ("Leftovers", "Sitrus Berry"):
        if stock.get(it):
            out[it] = stock[it]
    return out


_NAMES = None


def species_constant(name):
    """A calculator species name's constant."""
    global _NAMES
    if _NAMES is None:
        from . import pokedex
        _NAMES = {}
        for sp in pokedex.species_list(bdata.ROOT):
            const = sp if isinstance(sp, str) else sp.get("species") or sp.get("constant")
            try:
                _NAMES.setdefault(plteam.species_name(const), const)
            except Exception:
                continue
    if name in _NAMES:
        return _NAMES[name]
    compact = {re.sub(r"[^a-z0-9]", "", k.lower()): v for k, v in _NAMES.items()}
    got = compact.get(re.sub(r"[^a-z0-9]", "", name.lower()))
    if got is None:
        raise Refused(f"no species named {name}")
    return got


IV_KEYS = ("hp", "at", "df", "sp", "sa", "sd")


def calc_records(party):
    """Simulator records for the calculator's party (its "My Box" sets),
    each through plteam.record, keeping its own IVs and EVs."""
    out = []
    for s in party:
        const = species_constant(s["species"])
        rec = plteam.record(const, int(s.get("level") or 50), s.get("nature") or "Hardy", s.get("ability"),
                            15, [m for m in (s.get("moves") or []) if m and m != "(No Move)"][:4],
                            label=s["species"])
        ivs = s.get("ivs") or {}
        evs = s.get("evs") or {}
        rec["ivs"] = {k: int(ivs.get(k, 31 if ivs else 15)) for k in IV_KEYS}
        rec["evs"] = {k: int(evs.get(k, 0)) for k in IV_KEYS}
        rec["item"] = s.get("item") or None
        out.append(rec)
    return out


# ---- the warnings ------------------------------------------------------------------------------------

def open_gaps(root=None):
    """{"effects": {effect: verdict}, "abilities": {ability: verdict}}: the
    rows of simulator-gaps.md's move and ability tables still open, that is
    neither fixed nor left as they are by Ian's choice."""
    root = root or bdata.ROOT
    path = os.path.join(root, "docs", "oxide", "simulator-gaps.md")
    out = {"effects": {}, "abilities": {}, "items": {}}
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return out
    section = None
    for line in lines:
        if line.startswith("## "):
            section = {"## Moves, by effect": "effects", "## Abilities": "abilities",
                       "## Held items": "items"}.get(line.strip())
            continue
        if section is None or not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or set(cells[0]) <= set("-:") or cells[0] in ("Mechanic", "Ability",
                                                                                         "Item"):
            continue
        verdict = cells[1]
        low = verdict.lower()
        if low.startswith("fixed") or "left as it is by ian's choice" in low:
            continue
        name = cells[0].split(":")[0].strip() if section == "effects" else cells[0].split(" (")[0].strip()
        out[section][name] = verdict
    return out


def gap_warnings(b):
    gaps = open_gaps()
    out = []
    for m in b.p.mons + b.b.mons:
        whose = "your" if m.side == "p" else "the trainer's"
        for mv in m.moves:
            v = gaps["effects"].get(mv.effect)
            if v:
                out.append(f"{mv.name} ({whose} {m.species}): simulator-gaps.md lists its effect {mv.effect} as "
                           f"open: {_short(v)}")
        v = gaps["abilities"].get(m.ability)
        if v:
            out.append(f"{m.ability} ({whose} {m.species}): simulator-gaps.md lists it as open: {_short(v)}")
        v = gaps["items"].get(m.item)
        if v:
            out.append(f"{m.item} ({whose} {m.species}): simulator-gaps.md lists it as open: {_short(v)}")
    return out


def _short(text, n=160):
    text = re.sub(r"\s+", " ", text)
    return text if len(text) <= n else text[:n - 1] + "…"


def rule_warnings(setup, b, split, fight_level):
    """The scorer's rules the party departs from, flagged and never
    blocking: a nature other than Hardy, IVs other than 15, an ability other
    than the reading's slot, a move outside the member's pool, an item the
    split's stock lacks or more copies than it holds, a level above the
    reading's. A calculator party is held to the level and item rules
    against the fight's split, and its moves to its line's pool from the
    line's earliest catch in that split."""
    out = []
    reading = setup.get("source") in ("reading", "records")
    stock = stock_items(fs.player_items(split))
    used = collections.Counter()
    for i, (rec, m) in enumerate(zip(setup["records"], b.p.mons)):
        name = rec.get("label") or m.species
        if reading:
            if rec.get("nature") != "Hardy":
                out.append(f"{name}: nature {rec.get('nature')}, where the reading's are Hardy")
            ivs = set((rec.get("ivs") or {}).values())
            if ivs != {15}:
                out.append(f"{name}: IVs other than 15")
            want = (setup.get("abilities") or {}).get(str(i))
            if want and m.ability != want:
                out.append(f"{name}: ability {m.ability}, where the reading's slot is {want}")
        pool = (setup.get("pools") or {}).get(str(i))
        if pool is None and not reading:
            pool = line_pool(rec, split, m.level)
        if pool is not None:
            extra = [mv.name for mv in m.moves if mv.name not in pool]
            if extra and reading:
                out.append(f"{name}: {', '.join(extra)} not in its pool at level {m.level}")
            elif extra:
                out.append(f"{name}: {', '.join(extra)} not in its line's pool at level {m.level} from any "
                           f"catch by {split}'s split")
        if m.item:
            used[m.item] += 1
        if fight_level and m.level > fight_level:
            out.append(f"{name}: level {m.level}, above the reading's {fight_level}")
    for item, n in used.items():
        have = stock.get(item, 0)
        if have == 0:
            out.append(f"{item}: not in the stock the player holds by {split}'s split")
        elif n > have:
            out.append(f"{item}: {n} held, where the stock by {split}'s split has {have}")
    return out


def line_pool(rec, split, level):
    """A calculator member's move pool by the scorer's rule, for the move
    warning: what its line could know at this level from any catch the run
    can have made by this split (each stage it is caught as, at each level
    the tables give it, its capture moves and every level-up move after),
    so a move is flagged only where no such catch could know it. None where
    the line has no catch by the split."""
    from ..balance import pool as bpool
    try:
        const = rec["constant"]
        here = bpool.split_index(split)
        line = plniche.line_of(const)
        out = set()
        for sp in _line_members(line):
            for s, lv, _how in bpool.catches().get(sp, []):
                if bpool.split_index(s) > here or lv > level:
                    continue
                path = plteam.chain(sp, lv, level)
                if not any(stage == const for stage, _at in path):
                    continue
                out.update(plteam.move_pool(sp, lv, level)[1])
        if not out and const == line:
            out.update(plteam.move_pool(const, min(5, level), level)[1])     # a gift or a starter, at 5
        return out or None
    except Exception:
        return None


def _line_members(line):
    out, todo = [], [line]
    while todo:
        sp = todo.pop()
        if sp in out:
            continue
        out.append(sp)
        for e in plteam.mon_data(sp).get("evolutions") or []:
            todo.append(e[-1])
    return out


# ---- what a position shows -------------------------------------------------------------------------

def _constant_of(b, m):
    """A Pokemon's species constant, for its sprite: the player's records
    carry it, a trainer's are named as the calculator names them."""
    c = (b.st["pokemon"].get(m.key) or {}).get("constant")
    if c:
        return c
    try:
        return species_constant(m.species)
    except Refused:
        return None


def mon_view(b, m, side, i):
    out = {"index": i, "key": m.key, "species": m.species, "constant": _constant_of(b, m), "level": m.level,
           "hp": m.hp, "maxhp": m.maxhp,
           "status": m.status, "status_words": STATUS_WORDS.get(m.status), "sleep": m.sleep, "toxic": m.toxic,
           "stages": {k: v for k, v in m.stages.items() if v}, "item": m.item, "ability": m.ability,
           "types": m.types, "alive": m.alive(), "active": i == side.active,
           "moves": [{"name": mv.name, "type": mv.type, "cat": mv.cat, "power": mv.power, "acc": mv.acc,
                      "pp": m.pp.get(mv.name, mv.pp), "maxpp": mv.pp} for mv in m.moves]}
    vol = []
    if m.confused:
        vol.append(f"confused ({m.confused})")
    if m.taunt:
        vol.append(f"taunted ({m.taunt})")
    if m.seeded:
        vol.append("seeded")
    if m.sub:
        vol.append(f"substitute {m.sub} HP")
    if m.charging is not None:
        vol.append(f"charging {m.charging.name}")
    if m.recharge:
        vol.append("must recharge")
    if m.lock:
        vol.append(f"locked into {m.lock[0].name} ({m.lock[1]})")
    if m.choice:
        vol.append(f"locked by its Choice item into {m.choice}")
    if m.encore is not None:
        vol.append(f"encored into {m.encore}")
    if m.disabled is not None:
        vol.append(f"{m.disabled} disabled")
    if m.bound:
        vol.append(f"bound ({m.bound})")
    if m.yawn:
        vol.append("drowsy")
    if m.perish:
        vol.append(f"perish count {m.perish}")
    if m.infatuated:
        vol.append("in love")
    if m.crit_stage:
        vol.append(f"critical stage +{m.crit_stage}")
    if m.protecting:
        vol.append("protected")
    out["volatile"] = vol
    if i == side.active:
        out["speed"] = b.speed(m)
    return out


def side_view(b, s):
    out = {"mons": [mon_view(b, m, s, i) for i, m in enumerate(s.mons)], "active": s.active,
           "screens": {k: v for k, v in s.screens.items() if v}, "tailwind": s.tailwind,
           "hazards": {k: v for k, v in s.hazards.items() if v}, "safeguard": s.safeguard,
           "mist": getattr(s, "mist", 0)}
    if s.aurora_veil:
        out["aurora_veil"] = s.aurora_veil
    if s.web:
        out["web"] = s.web
    if s.lucky_chant:
        out["lucky_chant"] = s.lucky_chant
    return out


def field_view(b):
    out = {"weather": b.weather, "weather_turns": b.weather_turns, "trick_room": b.trick_room,
           "turn": b.turn}
    if b.gravity:
        out["gravity"] = b.gravity
    if b.magic_room:
        out["magic_room"] = b.magic_room
    if b.wonder_room:
        out["wonder_room"] = b.wonder_room
    if b.fog:
        out["fog"] = True
    return out


def order_view(b):
    """Both Speeds after every modifier, who moves first at equal priority,
    and the Quick Claws' chances."""
    me, foe = b.p.cur(), b.b.cur()
    sm, sf = b.speed(me), b.speed(foe)
    tr = b.trick_room > 0
    if sm == sf:
        first = "a speed tie, either side first at even odds"
    elif (sm > sf) != tr:
        first = f"{me.species} first"
    else:
        first = f"{foe.species} first"
    quick = []
    for m in (me, foe):
        if fs.custap_fires(m, b):
            quick.append(f"{m.species}'s Custap Berry fires this turn: it moves first in its bracket")
        elif m.item == "Quick Claw":
            quick.append(f"{m.species}'s Quick Claw: one turn in five it moves first in its bracket")
    pri = {}
    for m in (me, foe):
        for mv in m.moves:
            p = fs.move_priority(m, mv)
            if p:
                pri[f"{m.species}'s {mv.name}"] = p
    return {"mine": sm, "theirs": sf, "trick_room": tr, "first": first, "quick": quick, "priority": pri}


def ai_odds(b):
    """The trainer's odds at this position: plplan.ai_distribution mixed
    over plplan.quick_outcomes, since the AI reads the turn's Quick Claw
    rolls. ({label: probability}, [(quick, probability, [(label, p)])])."""
    mixed = collections.defaultdict(float)
    parts = []
    for quick, pq in plplan.quick_outcomes(b):
        c = plplan.clone(b)
        c.quick = quick
        dist = plplan.ai_distribution(c)
        rows = [(ai_label(c, a), p) for a, p in dist]
        for lab, p in rows:
            mixed[lab] += pq * p
        parts.append((quick, pq, rows))
    return dict(mixed), parts


def ai_scores(b):
    """Each of the trainer's move slots' score odds, read as plplan._build
    reads them (fightai.score_slot through plplan.outcomes), with no Quick
    Claw fired, and the chance its switch rules fire."""
    c = plplan.clone(b)
    c.quick = {m.key: fs.custap_fires(m, c) for m in (c.p.cur(), c.b.cur())}
    u, t = c.b.cur(), c.p.cur()
    forced = fightai.forced_choice(u)
    if forced is not None:
        return {"forced": ai_label(c, forced), "slots": [], "switch": {}}
    fightai.record_last_move(t)
    saved = c.rng
    c.rng = None
    try:
        side = fightai._side(c, u)
        switch = collections.defaultdict(float)
        for r, p in plplan.outcomes(lambda: fightai.should_switch(c, side, u, t)):
            if r is not None:
                switch[c.b.mons[r].species] += p
        fixed = fightai.fixed_move(c, u)
        figs = [fightai.figure(c, u, t, m) for m in u.moves]
        best = max((f for f in figs if f is not None), default=None)
        slots = []
        for i, m in enumerate(u.moves):
            d = collections.defaultdict(float)
            for s, p in plplan.outcomes(lambda i=i: fightai.score_slot(c, u, t, i, figs, best, c.ai_flags)):
                d[s] += p
            slots.append({"move": m.name, "figure": figs[i], "scores": sorted(d.items(), key=lambda x: -x[0])})
    finally:
        c.rng = saved
    return {"forced": None, "fixed": ai_label(c, fixed) if fixed else None, "slots": slots,
            "switch": dict(switch)}


def damage_rows(b, att, dfn):
    """Every move's damage on dfn from the simulator's own numbers
    (Battle.rolls and Battle.damage): each roll as HP and a share of dfn's
    maximum, a critical hit's, and the chance to knock out from its HP now."""
    rows = []
    for mv in att.moves:
        r = b.rolls(att, dfn, mv)
        if not r or not mv.damaging():
            continue
        n = len(r)
        rh = fs.row_hits(att, mv)
        try:
            plain = [b.damage(att, dfn, mv, crit=False, roll=i) or 0 for i in range(n)]
            crit = [b.damage(att, dfn, mv, crit=True, roll=i) or 0 for i in range(n)]
        except Exception:
            continue
        rate = fs.crit_rate(b, att, dfn, mv)
        odds = fs.multi_hit_odds(att, mv)
        if odds:
            tot = sum(w for _h, w in odds)
            ko = sum(w / tot * sum(1 for d in plain if fs.use_damage(att, mv, d, h) >= dfn.hp) / n
                     for h, w in odds)
            ko_crit = sum(w / tot * sum(1 for d in crit if fs.use_damage(att, mv, d, h) >= dfn.hp) / n
                          for h, w in odds)
            hits = ", ".join(f"{h} hits {w / tot:.0%}" for h, w in odds)
            note = f"the row counts {rh} hits; {hits}"
        else:
            plain = [fs.use_damage(att, mv, d, rh) for d in plain]
            crit = [fs.use_damage(att, mv, d, rh) for d in crit]
            ko = sum(1 for d in plain if d >= dfn.hp) / n
            ko_crit = sum(1 for d in crit if d >= dfn.hp) / n
            note = f"{rh} hits" if rh > 1 else ""
        holds = dfn.hp == dfn.maxhp and (dfn.item == "Focus Sash" or (dfn.ability == "Sturdy"
                                                                       and att.ability != "Mold Breaker"))
        rows.append({"move": mv.name, "type": mv.type, "cat": mv.cat, "rolls": plain, "crit_rolls": crit,
                     "pct": [round(100 * d / dfn.maxhp, 1) for d in plain],
                     "crit_pct": [round(100 * d / dfn.maxhp, 1) for d in crit],
                     "crit_rate": rate, "ko": ko, "ko_crit": ko_crit,
                     "ko_chance": (1 - rate) * ko + rate * ko_crit if rate < 1 else ko_crit,
                     "note": note, "holds": holds, "priority": fs.move_priority(att, mv)})
    return rows


def menu(b):
    """Every action the game lets Ian choose: each move with PP that Taunt,
    Disable, Encore, Torment, Heal Block, Gravity or a Choice lock does not
    bar (plplan.options leaves out the moves that would do nothing, so it is
    not the menu), and each living bench member unless he is trapped."""
    me = b.p.cur()
    forced = fightai.forced_choice(me)
    if forced is not None:
        return {"forced": True, "moves": [{"name": forced[1].name, "ok": True, "why": "it must"}], "switches": []}
    moves = []
    for mv in me.moves:
        why = None
        if me.pp.get(mv.name, 1) <= 0:
            why = "no PP left"
        elif me.taunt and mv.cat == "Status":
            why = "Taunt"
        elif fs.tormented_out(me, mv):
            why = "Torment"
        elif fs.move_heal_blocked(me, mv):
            why = "Heal Block"
        elif fs.disabled_out(me, mv):
            why = "Disable"
        elif (me.rare or b.gravity) and fs.move_barred(b, me, mv):
            why = "barred"
        elif me.choice and mv.name != me.choice:
            why = f"Choice lock into {me.choice}"
        elif me.encore is not None and mv.name != me.encore:
            why = f"Encore into {me.encore}"
        moves.append({"name": mv.name, "ok": why is None, "why": why, "pp": me.pp.get(mv.name, mv.pp),
                      "maxpp": mv.pp, "type": mv.type, "cat": mv.cat})
    if not any(m["ok"] for m in moves):
        moves.append({"name": "Struggle", "ok": True, "why": "no other move can be chosen"})
    trapped = fs.trapped(b, me)
    switches = [{"index": i, "species": m.species, "hp": m.hp, "maxhp": m.maxhp}
                for i, m in enumerate(b.p.mons) if i != b.p.active and m.alive()] if not trapped else []
    return {"forced": False, "moves": moves, "switches": switches, "trapped": trapped}


# ---- the tree ----------------------------------------------------------------------------------------

def fingerprint(b):
    """A digest of the whole position (perfectline.state_key), the same in
    every process, to check that a reloaded line reproduces it."""
    def canon(x):
        if isinstance(x, (set, frozenset)):
            return ("set",) + tuple(sorted(repr(canon(y)) for y in x))
        if isinstance(x, (tuple, list)):
            return tuple(canon(y) for y in x)
        if isinstance(x, dict):
            return tuple(sorted((repr(k), canon(v)) for k, v in x.items()))
        return x
    return hashlib.sha1(repr(canon(pl.state_key(b))).encode()).hexdigest()[:16]


def finished(b):
    if not b.p.alive():
        return "lost"
    if not b.b.alive():
        return "won"
    return None


class Node:
    def __init__(self, nid, parent, kind, b, **kw):
        self.id, self.parent, self.kind, self.b = nid, parent, kind, b
        self.action = kw.get("action")
        self.pins = kw.get("pins") or {}
        self.seed = kw.get("seed")
        self.checks = kw.get("checks") or []
        self.dropped = kw.get("dropped") or []
        self.edits = kw.get("edits")
        self.outcome = kw.get("outcome")         # the overview outcome its turn fell into
        self.chance = kw.get("chance", 1.0)      # its turn's chance: that outcome's
        self.followed = kw.get("followed")
        self.note = kw.get("note")
        self.created = kw.get("created") or time.time()
        self.children = []


class Line:
    """One fight's tree of positions."""

    def __init__(self, setup, name=None):
        self.setup = setup
        st, team, boss_keys, flags, b, split = build(setup)
        self.st, self.team, self.boss_keys, self.flags, self.split = st, team, boss_keys, flags, split
        self.name = name or default_name(setup)
        self.nodes = {0: Node(0, None, "root", b)}
        self.next_id = 1
        self.overviews = {}
        self.fight_level = setup.get("level")
        self.warnings = {"gaps": gap_warnings(b), "rules": rule_warnings(setup, b, split, self.fight_level)}

    # -- growing the tree

    def add(self, parent, kind, b, **kw):
        n = Node(self.next_id, parent, kind, b, **kw)
        self.next_id += 1
        self.nodes[n.id] = n
        self.nodes[parent].children.append(n.id)
        return n

    def node(self, nid):
        n = self.nodes.get(int(nid))
        if n is None:
            raise Refused(f"no node {nid}")
        return n

    def preview(self, nid, action, pins):
        """The checks the turn makes with these pins, every other check at
        its likeliest outcome."""
        n = self.node(nid)
        try:
            _c, play = run_turn(n.b, action, pins, 0, likeliest=True)
        except NeedReplacement as exc:       # cannot happen with likeliest, but say so if it does
            play = exc.play
        return {"checks": play.checks, "dropped": play.dropped}

    def play(self, nid, action, pins, seed=None, followed=None):
        """Play the turn: a new node, or what Ian still has to choose."""
        n = self.node(nid)
        if finished(n.b):
            raise Refused("the battle is over at this position")
        seed = random.randrange(1 << 31) if seed is None else int(seed)
        try:
            c, play = run_turn(n.b, action, pins, seed)
        except NeedReplacement as exc:
            return {"needs": {"key": exc.key, "why": exc.why,
                              "options": [{"index": i, "species": n.b.p.mons[i].species} for i in exc.options]},
                    "checks": exc.play.checks, "seed": seed, "pins": dict(pins or {}), "followed": followed}
        outcome, chance = self.classify(n, action, play)
        child = self.add(n.id, "turn", c, action=list(action), pins=dict(pins or {}), seed=seed,
                         checks=play.checks, dropped=play.dropped, outcome=outcome, chance=chance,
                         followed=followed)
        self.save()
        return {"node": child.id}

    # -- the overview, and following one of its outcomes

    def overview(self, nid, action):
        """Every way the turn can go after Ian's action, most likely first:
        for each Quick Claw roll and each of the AI's choices weighted by
        its odds, turn_outcomes' merged positions with their chances."""
        n = self.node(nid)
        ck = (n.id, json.dumps(action))
        if ck in self.overviews:
            return self.overviews[ck]
        b = n.b
        a = resolve_action(b, action)
        key = _mix(self.name, n.id, "overview")
        lines = []
        for quick, pq in plplan.quick_outcomes(b):
            c0 = plplan.clone(b)
            c0.quick = quick
            for aa, pa in plplan.ai_distribution(c0):
                for out in enumerate_turn(c0, a, aa, key):
                    lines.append({"quick": quick, "pq": pq, "ai": ai_label(c0, aa), "pa": pa, "p": out["p"],
                                  "chance": pq * pa * out["p"], "out": out, "c0": c0})
        lines.sort(key=lambda x: -x["chance"])
        # The overviews of the last few turns looked at, kept for following
        # and for the chance of a played turn; an enumeration holds many
        # positions, so the oldest goes once there are OVERVIEWS_KEPT.
        while len(self.overviews) >= OVERVIEWS_KEPT:
            self.overviews.pop(next(iter(self.overviews)))
        self.overviews[ck] = lines
        return lines

    def overview_view(self, nid, action):
        n = self.node(nid)
        rows = []
        for i, ln in enumerate(self.overview(nid, action)):
            rows.append(dict(describe_outcome(n.b, ln), index=i))
        return rows

    def follow(self, nid, action, index, mode="worst", rolls=None, seed=None):
        """Play the overview's outcome `index`: its checks pinned as its
        representative branch decided them, each of its damage rolls an
        exact roll within its band: Ian's (`rolls`, by check key), the
        band's worst for him (mode "worst"), or one drawn within the band at
        its odds (mode "draw")."""
        lines = self.overview(nid, action)
        if not 0 <= int(index) < len(lines):
            raise Refused("no such outcome")
        ln = lines[int(index)]
        pins = follow_pins(ln, mode, rolls or {}, random.Random(seed))
        return self.play(nid, action, pins, seed=seed,
                         followed={"index": int(index), "mode": mode, "chance": ln["chance"]})

    def classify(self, n, action, play):
        """(the overview outcome a played turn fell into, its chance): its
        Quick Claw rolls and the AI's choice, then the planner's dice run
        once along the checks it made, each exact roll counted as its band,
        to the merged position that outcome is."""
        try:
            lines = self.overview(n.id, action)
        except Exception:
            return None, None
        quick_played = {}
        ai = None
        by_key = {}
        for ch in play.checks:
            if ch["kind"] == "quickclaw":
                quick_played[ch["who"]] = ch["outcome"] == 1
            elif ch["kind"] == "ai":
                ai = ch["value"]
            elif not ch["key"].startswith("replace|"):
                by_key[ch["key"]] = ch
        b = n.b
        for m in (b.p.cur(), b.b.cur()):
            quick_played.setdefault(m.key, fs.custap_fires(m, b))
        dist_labels = None
        for ln in lines:
            if ln["quick"] == quick_played:
                dist_labels = ln
                break
        if dist_labels is None:
            return None, None
        if ai is None:
            ai = next((x["ai"] for x in lines if x["quick"] == quick_played), None)
        c0 = next((x["c0"] for x in lines if x["quick"] == quick_played), None)
        a = resolve_action(c0, action)
        aa = None
        for x, _p in plplan.ai_distribution(c0):
            if ai_label(c0, x) == ai:
                aa = x
        if aa is None:
            return None, None
        c = plplan.clone(c0)
        d = GuidedEnumDice(by_key, random.Random(0), c)
        c.dice, c.rng = d, d.rng
        pl._turn(c, a, aa)
        k = plplan.merge_key(c)
        for i, ln in enumerate(lines):
            if ln["quick"] == quick_played and ln["ai"] == ai and ln["out"]["merge"] == k:
                return i, ln["chance"]
        return None, None

    # -- setting a position by hand

    def set_position(self, nid, edits):
        n = self.node(nid)
        c = plplan.clone(n.b)
        apply_edits(c, edits)
        child = self.add(n.id, "set", c, edits=edits, chance=1.0)
        self.save()
        return {"node": child.id}

    # -- what the page shows

    def view(self, nid):
        n = self.node(nid)
        b = n.b
        out = {"line": self.name, "node": n.id, "kind": n.kind, "fight": self.setup["fight"],
               "label": self.setup.get("label") or fight_label(self.setup["fight"]),
               "split": self.split, "branch": self.setup.get("branch"),
               "player": side_view(b, b.p), "trainer": side_view(b, b.b), "field": field_view(b),
               "finished": finished(b), "warnings": self.warnings, "path": self.path(n.id),
               "checks": n.checks, "dropped": n.dropped, "chance": n.chance, "path_chance": self.path_chance(n.id),
               "action": n.action,
               "pins": n.pins, "edits": n.edits, "followed": n.followed}
        if not finished(b):
            mixed, parts = ai_odds(b)
            out["ai"] = {"odds": sorted(mixed.items(), key=lambda x: -x[1]),
                         "by_quick": [{"quick": q, "p": pq, "odds": rows} for q, pq, rows in parts]}
            out["scores"] = ai_scores(b)
            out["order"] = order_view(b)
            out["damage"] = {"mine": damage_rows(b, b.p.cur(), b.b.cur()),
                             "theirs": damage_rows(b, b.b.cur(), b.p.cur())}
            out["menu"] = menu(b)
        out["tree"] = self.tree_view()
        return out

    def path(self, nid):
        out = []
        n = self.node(nid)
        while n is not None:
            out.append(n.id)
            n = self.nodes.get(n.parent) if n.parent is not None else None
        return out[::-1]

    def path_chance(self, nid):
        """A position's chance: the product, along its path, of the chances
        of the overview outcomes its turns fell into (so a band played at one
        roll counts as the whole band), from the root or from the last
        position set by hand; None where a turn's outcome is unknown."""
        p = 1.0
        n = self.nodes[nid]
        while n.parent is not None and n.kind == "turn":
            if n.chance is None:
                return None
            p *= n.chance
            n = self.nodes[n.parent]
        return p

    def tree_view(self):
        rows = []
        for nid in sorted(self.nodes):
            n = self.nodes[nid]
            rows.append({"id": n.id, "parent": n.parent, "kind": n.kind, "turn": n.b.turn,
                         "action": None if n.action is None else action_text(self.nodes[n.parent].b, n.action)
                         if n.parent is not None else None,
                         "ai": next((ch.get("value") for ch in n.checks if ch["kind"] == "ai"), None),
                         "summary": turn_summary(n), "chance": n.chance, "path": self.path_chance(nid),
                         "finished": finished(n.b),
                         "me": f"{n.b.p.cur().species} {n.b.p.cur().hp}/{n.b.p.cur().maxhp}",
                         "foe": f"{n.b.b.cur().species} {n.b.b.cur().hp}/{n.b.b.cur().maxhp}",
                         "faints": sum(1 for m in n.b.p.mons if not m.alive()), "note": n.note})
        return {"nodes": rows, "summary": self.coverage()}

    def coverage(self):
        """The share of the chance the played branches cover, and the share
        of that ending in a win, from the played leaves alone (no planner
        fills in the rest, by Ian's answer): from the root, or from the last
        position set by hand, along the action played last at each node,
        each overview outcome counted once."""
        def walk(nid):
            n = self.nodes[nid]
            if not n.children:
                end = finished(n.b)
                return 1.0, 1.0 if end == "won" else 0.0
            last = self.nodes[n.children[-1]]
            act = json.dumps(last.action)
            seen = {}
            for cid in n.children:
                ch = self.nodes[cid]
                if ch.kind != "turn" or json.dumps(ch.action) != act or ch.chance is None:
                    continue
                k = ch.outcome if ch.outcome is not None else f"n{cid}"
                if k not in seen:
                    seen[k] = (ch.chance, walk(cid))
            if not seen:
                sets = [cid for cid in n.children if self.nodes[cid].kind == "set"]
                return walk(sets[-1]) if sets else (0.0, 0.0)
            cov = sum(p * c for p, (c, _w) in seen.values())
            win = sum(p * w for p, (_c, w) in seen.values())
            return cov, win
        cov, win = walk(0)
        return {"covered": cov, "won": win, "won_of_covered": win / cov if cov else 0.0}

    # -- saving

    def to_json(self):
        nodes = []
        for nid in sorted(self.nodes):
            n = self.nodes[nid]
            rec = {"id": n.id, "parent": n.parent, "kind": n.kind, "state": fingerprint(n.b), "note": n.note,
                   "created": n.created}
            if n.kind == "turn":
                rec.update(action=n.action, pins=n.pins, seed=n.seed, followed=n.followed, chance=n.chance,
                           outcome=n.outcome,
                           outcomes={ch["key"]: ch.get("value", ch["outcome"]) for ch in n.checks})
            elif n.kind == "set":
                rec.update(edits=n.edits)
            nodes.append(rec)
        return {"format": FORMAT, "name": self.name, "saved": datetime.datetime.now().isoformat(timespec="seconds"),
                "commit": head_commit(), "setup": self.setup, "nodes": nodes}

    def save(self, path=None):
        path = path or line_path(self.name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(self.to_json(), fh, indent=1)
        os.replace(tmp, path)
        return path

    def transcript(self):
        out = [f"{self.setup.get('label') or fight_label(self.setup['fight'])}: line {self.name}",
               f"Party: " + ", ".join(f"{m.species} {m.level}" for m in self.nodes[0].b.p.mons),
               f"Against: " + ", ".join(f"{m.species} {m.level}" for m in self.nodes[0].b.b.mons), ""]

        def walk(nid, depth):
            n = self.nodes[nid]
            pad = "  " * depth
            if n.kind == "turn":
                parent = self.nodes[n.parent]
                out.append(f"{pad}[{n.id}] turn {parent.b.turn + 1}: {action_text(parent.b, n.action)}"
                           + (f" (chance {n.chance:.1%})" if n.chance is not None else ""))
                for ch in n.checks:
                    out.append(f"{pad}    {ch['label']}: {check_outcome_text(ch)}"
                               + (" (pinned)" if ch["how"] == "pinned" else ""))
                out.append(f"{pad}    after: you {n.b.p.cur().species} {n.b.p.cur().hp}/{n.b.p.cur().maxhp}, "
                           f"them {n.b.b.cur().species} {n.b.b.cur().hp}/{n.b.b.cur().maxhp}"
                           + (f"; the battle is {finished(n.b)}" if finished(n.b) else ""))
            elif n.kind == "set":
                out.append(f"{pad}[{n.id}] position set by hand: {json.dumps(n.edits)}")
            if n.note:
                out.append(f"{pad}    note: {n.note}")
            for cid in n.children:
                walk(cid, depth + 1)
        walk(0, 0)
        return "\n".join(out) + "\n"


class GuidedEnumDice(LabelledEnumDice):
    """The planner's dice run once along a played turn's checks: each event
    takes the outcome the turn's check of the same key took (a roll, the
    band its exact roll lies in), so the turn lands on the merged position
    of the overview outcome it fell into."""

    def __init__(self, by_key, rng, battle):
        super().__init__((), rng, battle)
        self.by_key = by_key

    def _ev(self, probs):
        rec = self.notes[-1] if self.notes and self.notes[-1]["event"] == len(self.events) else None
        o = 0
        if rec is not None:
            ch = self.by_key.get(rec["key"])
            if ch is not None:
                if rec["method"] == "roll" and "groups" in (rec.get("rolls") or {}):
                    o = next((g for g, rolls in enumerate(rec["rolls"]["groups"]) if ch["outcome"] in rolls), 0)
                else:
                    o = ch["outcome"]
        if not 0 <= o < len(probs) or probs[o] <= 0:
            o = 0
        self.events.append(probs)
        self.picked.append(o)
        return o


def follow_pins(ln, mode, rolls, rng):
    """The pins that play an overview outcome: its Quick Claw rolls, the
    AI's choice, and each check of its representative branch as its dice
    decided it; each damage roll an exact roll within the band it fell in."""
    pins = {}
    for k, fired in ln["quick"].items():
        pins[f"quick|{k}#0"] = 1 if fired else 0
    pins["ai|choice#0"] = ln["ai"]
    d = ln["out"]["dice"]
    for rec in d.notes:
        if rec["event"] is None or rec["event"] >= len(d.picked):
            continue
        o = d.picked[rec["event"]]
        if rec["method"] == "roll" and "groups" in (rec.get("rolls") or {}):
            band = rec["rolls"]["groups"][o]
            want = rolls.get(rec["key"])
            if isinstance(want, int) and want in band:
                pins[rec["key"]] = want
            elif mode == "draw":
                pins[rec["key"]] = band[rng.randrange(len(band))]
            else:
                # The band's worst for Ian: his own hits at their lowest,
                # the trainer's at their highest (the damage falls on the
                # victim, so the worst is the most on his side's Pokemon).
                victim = rec["rolls"].get("victim")
                dmg = rec["rolls"]["dmg"]
                pick = max if victim == "p" else min
                pins[rec["key"]] = pick(band, key=lambda r: (dmg[r], r))
        else:
            pins[rec["key"]] = o
    return pins


def describe_outcome(b, ln):
    """One line of the overview: what happened, both sides' HP after as a
    range over the outcome's members, any faint."""
    out = ln["out"]
    rep, d = out["c"], out["dice"]
    events = []
    for rec in d.notes:
        if rec["event"] is None or rec["event"] >= len(d.picked):
            continue
        o = d.picked[rec["event"]]
        events.append({"key": rec["key"], "method": rec["method"], "kind": rec["kind"], "outcome": o,
                       "band": rec["rolls"]["groups"][o] if rec["method"] == "roll" and rec.get("rolls")
                       and "groups" in rec["rolls"] else None,
                       "rolls": rec.get("rolls")})
    hp = []
    for side_name, side0 in (("p", b.p), ("b", b.b)):
        for i, m0 in enumerate(side0.mons):
            vals = [(c.p if side_name == "p" else c.b).mons[i].hp for c, _p, _d in out["members"]]
            lo, hi = min(vals), max(vals)
            if lo != m0.hp or hi != m0.hp:
                hp.append({"side": side_name, "index": i, "species": m0.species, "lo": lo, "hi": hi,
                           "maxhp": m0.maxhp, "before": m0.hp})
    faints = [m.species for m in rep.p.mons + rep.b.mons if not m.alive()
              and any(m0.key == m.key and m0.alive() for m0 in b.p.mons + b.b.mons)]
    quick = [k for k, v in ln["quick"].items() if v and not _custap(b, k)]
    return {"chance": ln["chance"], "ai": ln["ai"], "pa": ln["pa"], "quick": quick, "pq": ln["pq"],
            "p": ln["p"], "events": [describe_event(rep, e) for e in events], "hp": hp, "faints": faints,
            "members": len(out["members"]), "finished": finished(rep)}


def _custap(b, key):
    m = next((x for x in (b.p.cur(), b.b.cur()) if x.key == key), None)
    return m is not None and fs.custap_fires(m, b)


def describe_event(c, e):
    """An event of the overview in words, from its key and outcome."""
    who, what, phase, call = e["key"].split("|", 3)
    method, _sep, rest = call.partition(":")
    kind = rest.split("#")[0]
    mon = next((m for m in c.p.mons + c.b.mons if m.key == who), None)
    name = mon.species if mon else "field"
    o = e["outcome"]
    if e["band"] is not None:
        dmg = e["rolls"]["dmg"]
        band = e["band"]
        lo, hi = min(dmg[r] for r in band), max(dmg[r] for r in band)
        dmg_text = f"{lo} damage" if lo == hi else f"{lo} to {hi} damage"
        text = f"{name}'s {what}: rolls {min(band) + 1} to {max(band) + 1}, {dmg_text}"
        return {"text": text, "key": e["key"], "band": band, "dmg": [dmg[r] for r in band],
                "victim": e["rolls"].get("victim"), "maxhp": e["rolls"].get("maxhp"), "hp": e["rolls"].get("hp")}
    if phase == "accuracy":
        text = f"{name}'s {what} {'misses' if o else 'hits'}"
    elif kind in YES_NO:
        q, opts = YES_NO[kind]
        text = f"{name}'s {what}: {opts[o]}" if what not in ("helps", "end") else f"{name}: {q}: {opts[o]}"
    elif method in ("sleep", "confusion", "taunt", "bind", "outrage"):
        first = {"sleep": 1, "confusion": 2, "taunt": 3, "bind": 3, "outrage": 2}[method]
        text = f"{method} lasts {first + o}"
    elif method == "crits":
        text = f"{name}'s {what}: {o} critical hits"
    elif method == "pick":
        text = f"{name}'s {what}: pick {o + 1}"
    elif method == "tie":
        text = "speed tie: " + ("you first" if o else "the trainer first")
    elif method == "thaws":
        text = f"{name} " + ("thaws" if o else "stays frozen")
    else:
        text = f"{name}'s {what}: {kind or method} {o + 1}"
    return {"text": text, "key": e["key"]}


def action_text(b, action):
    try:
        return action_label(b, resolve_action(b, action))
    except Refused:
        return f"{action[0]} {action[1]}"


def check_outcome_text(ch):
    if ch.get("options"):
        o = ch["outcome"]
        text = ch["options"][o]
        r = ch.get("rolls")
        if r and r.get("dmg") and r["dmg"][o] is not None:
            text += f": {r['dmg'][o]} damage"
            if r.get("hp") is not None:
                text += f", leaves {max(0, r['hp'] - r['dmg'][o])} HP"
        return text
    return str(ch.get("value"))


def turn_summary(n):
    """A node's turn in a few words, for the tree."""
    if n.kind == "root":
        return "start"
    if n.kind == "set":
        return "set by hand"
    bits = []
    for ch in n.checks:
        if ch["kind"] == "ai":
            continue
        o = ch["outcome"]
        if ch.get("method") == "roll" or ch["kind"] == "replacement" or ch.get("probs") is None:
            continue
        probs = ch["probs"]
        if probs[o] < 0.5 and len(probs) == 2:
            bits.append(ch["label"].split(": ")[-1] + ": " + ch["options"][o])
    return "; ".join(bits[:3])


def apply_edits(c, edits):
    """A position set by hand: each Pokemon's HP, status, stages and item,
    who is in on each side, and the field."""
    for side_name, side in (("player", c.p), ("trainer", c.b)):
        e = edits.get(side_name) or {}
        if "active" in e:
            i = int(e["active"])
            if not 0 <= i < len(side.mons):
                raise Refused("no such Pokemon")
            side.active = i
        for k in ("tailwind", "safeguard"):
            if k in e:
                setattr(side, k, int(e[k]))
        if "screens" in e:
            for s, v in e["screens"].items():
                if s in side.screens:
                    side.screens[s] = int(v)
        if "hazards" in e:
            for h, v in e["hazards"].items():
                if h in side.hazards:
                    side.hazards[h] = int(v)
        for i, me in (e.get("mons") or {}).items():
            m = side.mons[int(i)]
            if "hp" in me:
                m.hp = max(0, min(m.maxhp, int(me["hp"])))
            if "status" in me:
                st = me["status"] or None
                if st not in (None, *STATUS_WORDS):
                    raise Refused(f"unknown status {st}")
                # A status the edit leaves as it was keeps its counters; a new
                # one starts them (sleep at two turns unless the edit says).
                if st != m.status or "sleep" in me or "toxic" in me:
                    m.status = st
                    m.sleep = int(me.get("sleep") or (2 if st == "slp" else 0))
                    m.toxic = 0 if st != "tox" else int(me.get("toxic") or 0)
            if "stages" in me:
                for k, v in me["stages"].items():
                    if k in m.stages:
                        m.stages[k] = max(-6, min(6, int(v)))
            if "item" in me:
                m.item = me["item"] or None
            if "confused" in me:
                m.confused = int(me["confused"] or 0)
    f = edits.get("field") or {}
    if "weather" in f:
        c.weather = f["weather"] or None
        c.weather_turns = int(f.get("weather_turns") or 0)
    if "trick_room" in f:
        c.trick_room = int(f["trick_room"] or 0)


# ---- lines on disk -----------------------------------------------------------------------------------

def default_name(setup):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", str(setup.get("fight")).lower()).strip("-")
    return f"{slug}-{stamp}"


def line_path(name):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name or ""):
        raise Refused("a line's name is letters, digits, dots, dashes and underscores")
    return os.path.join(LINES, name + ".json")


def head_commit():
    try:
        return subprocess.run(["git", "-C", bdata.ROOT, "rev-parse", "--short=9", "HEAD"], check=True,
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def list_lines():
    out = []
    if not os.path.isdir(LINES):
        return out
    for f in sorted(os.listdir(LINES)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(LINES, f)
        try:
            with open(path) as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if d.get("format") != FORMAT:
            continue
        out.append({"name": d.get("name") or f[:-5], "saved": d.get("saved"), "fight": d["setup"].get("fight"),
                    "label": d["setup"].get("label"), "nodes": len(d.get("nodes") or []),
                    "commit": d.get("commit")})
    out.sort(key=lambda x: x.get("saved") or "", reverse=True)
    return out


def load(path_or_name):
    """A saved line, its tree rebuilt by replaying each turn with every one
    of its checks as recorded: (Line, [differences]); a difference is a node
    whose position does not match the one saved (another tree's simulator,
    most likely)."""
    path = path_or_name if os.sep in path_or_name else line_path(path_or_name)
    with open(path) as fh:
        d = json.load(fh)
    if d.get("format") != FORMAT:
        raise Refused(f"{path} is not a saved line")
    line = Line(d["setup"], name=d.get("name"))
    diffs = []
    root = d["nodes"][0]
    if root.get("state") and root["state"] != fingerprint(line.nodes[0].b):
        diffs.append({"node": 0, "why": "the starting position differs"})
    line.nodes[0].note = root.get("note")
    ids = {0: 0}
    for rec in d["nodes"][1:]:
        parent = line.nodes[ids[rec["parent"]]]
        if rec["kind"] == "turn":
            pins = dict(rec.get("outcomes") or {})
            try:
                c, play = run_turn(parent.b, rec["action"], pins, rec.get("seed") or 0)
            except NeedReplacement:
                diffs.append({"node": rec["id"], "why": "the replay needed a replacement the line did not record"})
                continue
            n = line.add(parent.id, "turn", c, action=rec["action"], pins=rec.get("pins") or {},
                         seed=rec.get("seed"), checks=play.checks, dropped=play.dropped,
                         outcome=rec.get("outcome"), chance=rec.get("chance"), followed=rec.get("followed"),
                         note=rec.get("note"), created=rec.get("created"))
            for ch in n.checks:
                if ch["key"] in (rec.get("pins") or {}):
                    ch["how"] = "pinned"
                elif ch["how"] == "pinned":
                    ch["how"] = "drawn"
            if play.dropped:
                diffs.append({"node": rec["id"], "why": "checks no longer match: "
                              + "; ".join(x["label"] for x in play.dropped[:3])})
        else:
            c = plplan.clone(parent.b)
            apply_edits(c, rec.get("edits") or {})
            n = line.add(parent.id, "set", c, edits=rec.get("edits"), note=rec.get("note"),
                         created=rec.get("created"))
        ids[rec["id"]] = n.id
        if rec.get("state") and rec["state"] != fingerprint(n.b):
            diffs.append({"node": rec["id"], "why": "the replayed position differs from the saved one"})
    return line, diffs


def save_mismatch(line, nid, note):
    """"The game did something else here": the node, the path to it and
    Ian's note, under ~/oxide-lines/mismatches/, for the Overseer to turn
    into a gap row."""
    n = line.node(nid)
    path = []
    for pid in line.path(n.id):
        x = line.nodes[pid]
        path.append({"id": x.id, "kind": x.kind,
                     "action": None if x.parent is None or x.action is None
                     else action_text(line.nodes[x.parent].b, x.action),
                     "checks": [{"label": ch["label"], "outcome": check_outcome_text(ch), "how": ch["how"]}
                                for ch in x.checks], "edits": x.edits})
    v = line.view(n.id)
    for k in ("tree", "scores"):
        v.pop(k, None)
    rec = {"line": line.name, "node": n.id, "note": note, "commit": head_commit(),
           "saved": datetime.datetime.now().isoformat(timespec="seconds"), "setup": line.setup, "path": path,
           "position": v}
    folder = os.path.join(LINES, "mismatches")
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    out = os.path.join(folder, f"{line.name}-node{n.id}-{stamp}.json")
    with open(out, "w") as fh:
        json.dump(rec, fh, indent=1, default=str)
    n.note = note
    line.save()
    return out


# ---- setups ------------------------------------------------------------------------------------------

def setup_from_reading(req):
    """A setup from a reading's box: six of its members by label, in party
    order, each with four moves from its pool, and items (None: the
    scorer's own rule)."""
    box = reading_box(req["slug"], req["seed"])
    by_label = {r["label"]: r for r in box["records"]}
    six = req.get("six") or []
    if not six:
        raise Refused("choose the Pokemon to fight with")
    recs, moves, pools, abilities = [], [], {}, {}
    for i, label in enumerate(six):
        r = by_label.get(label)
        if r is None:
            raise Refused(f"{label} is not in box {box['seed']}")
        recs.append(dict(r))
        mv = (req.get("moves") or {}).get(label) or []
        # With no moves chosen, the last four of its pool: the moves it
        # learned last, as the game's own default moveset takes them.
        moves.append([m for m in mv if m][:4] or list(r["moves"])[-4:])
        pools[str(i)] = list(r["moves"])
        abilities[str(i)] = r["ability"]
    items = req.get("items")
    held = None if items is None else [items.get(label) or None for label in six]
    return {"source": "reading", "fight": box["fight"], "variant": box["variant"], "branch": req.get("branch") or None,
            "records": recs, "moves": moves, "held": held, "lead": int(req.get("lead") or 0),
            "level": box["level"], "pools": pools, "abilities": abilities,
            "reading": {"slug": box["slug"], "seed": box["seed"]},
            "label": f"{box['name']}, box {box['seed']}"}


def setup_from_calc(req):
    """A setup from the calculator: its party's "My Box" sets and the
    trainer on its right side, by the trainer's id."""
    party = req.get("party") or []
    if not party:
        raise Refused("the calculator's party is empty")
    tr = req.get("trainer") or {}
    if tr.get("tr_id") is None:
        raise Refused("pick a trainer's Pokemon on the calculator's right side")
    key, v = fight_of_trainer(int(tr["tr_id"]))
    recs = calc_records(party[:6])
    level = None
    slug = plscore.parse_fight(key)[1] if key[:3] != "tr:" else None
    f = next((x for x in plgoal3.fights() if x["slug"] == slug), None) if slug else None
    if f is not None:
        try:
            level = plgoal3.level(f, fight_trainers(key)[1][v])
        except Exception:
            level = None
    return {"source": "calc", "fight": key, "variant": v, "branch": req.get("branch") or None,
            "records": recs, "moves": [r["moves"] for r in recs], "held": [r.get("item") for r in recs],
            "lead": 0, "level": level, "label": f"{fight_label(key)} (from the calculator)",
            "trainer_set": tr.get("set")}


# ---- the worker ----------------------------------------------------------------------------------------

class Worker:
    def __init__(self):
        install()
        self.lines = {}

    def line(self, req):
        name = req.get("line")
        if name not in self.lines:
            try:
                line, _diffs = load(name)
            except FileNotFoundError:
                raise Refused(f"no line {name}")
            self.lines[name] = line
        return self.lines[name]

    def handle(self, req):
        op = req.get("op")
        if op == "fights":
            return {"fights": reading_fights()}
        if op == "box":
            box = reading_box(req["slug"], req["seed"])
            return {k: v for k, v in box.items() if k != "records"}
        if op == "new":
            setup = setup_from_reading(req) if req.get("source") == "reading" else setup_from_calc(req)
            line = Line(setup)
            line.save()
            self.lines[line.name] = line
            return {"line": line.name, "view": line.view(0)}
        if op == "lines":
            return {"lines": list_lines(), "dir": LINES}
        if op == "again":
            # The same party against the trainer read from another branch (or
            # this tree's again): a new line.
            old = self.line(req)
            line = Line(dict(old.setup, branch=(req.get("branch") or "").strip() or None))
            line.save()
            self.lines[line.name] = line
            return {"line": line.name, "view": line.view(0)}
        if op == "open":
            line, diffs = load(req["line"])
            self.lines[line.name] = line
            return {"line": line.name, "diffs": diffs, "view": line.view(int(req.get("node") or 0))}
        line = self.line(req)
        if op == "view":
            return {"view": line.view(req.get("node") or 0)}
        if op == "checks":
            return line.preview(req["node"], req["action"], req.get("pins") or {})
        if op == "play":
            out = line.play(req["node"], req["action"], req.get("pins") or {}, req.get("seed"),
                            followed=req.get("followed"))
            if "node" in out:
                out["view"] = line.view(out["node"])
            return out
        if op == "overview":
            return {"outcomes": line.overview_view(req["node"], req["action"])}
        if op == "follow":
            out = line.follow(req["node"], req["action"], req["index"], req.get("mode") or "worst",
                              req.get("rolls"), req.get("seed"))
            if "node" in out:
                out["view"] = line.view(out["node"])
            return out
        if op == "set":
            out = line.set_position(req["node"], req.get("edits") or {})
            out["view"] = line.view(out["node"])
            return out
        if op == "rename":
            new = req["name"]
            line_path(new)
            old = line_path(line.name)
            line.name = new
            line.save()
            if os.path.exists(old) and old != line_path(new):
                os.remove(old)
            self.lines.pop(req["line"], None)
            self.lines[new] = line
            return {"line": new}
        if op == "note":
            line.node(req["node"]).note = req.get("note") or None
            line.save()
            return {"ok": True}
        if op == "transcript":
            return {"text": line.transcript()}
        if op == "mismatch":
            return {"path": save_mismatch(line, req["node"], req.get("note") or "")}
        raise Refused(f"unknown request {op}")


def serve():
    """Answer the OxiDex server: one JSON request a line on stdin, one JSON
    answer a line on the stdout this process started with. Anything else
    the simulator prints goes to stderr, so it cannot break an answer."""
    out = os.fdopen(os.dup(1), "w")
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    worker = Worker()
    print("line tester ready", file=sys.stderr, flush=True)
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        t0 = time.perf_counter()
        try:
            req = json.loads(raw)
            ans = worker.handle(req)
        except Refused as exc:
            ans = {"error": str(exc)}
        except Exception as exc:
            traceback.print_exc()
            ans = {"error": f"{type(exc).__name__}: {exc}"}
        ans["seconds"] = round(time.perf_counter() - t0, 3)
        out.write(json.dumps(ans, default=_jsonable) + "\n")
        out.flush()


def _jsonable(x):
    if isinstance(x, (set, frozenset)):
        return sorted(x)
    if isinstance(x, fs.Move):
        return x.name
    return str(x)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--serve", action="store_true", help="answer the OxiDex server on stdin and stdout")
    ap.add_argument("--transcript", metavar="LINE", help="print a saved line as a transcript")
    a = ap.parse_args(argv)
    if a.serve:
        serve()
        return 0
    if a.transcript:
        install()
        line, diffs = load(a.transcript)
        print(line.transcript())
        for d in diffs:
            print(f"replay difference at node {d['node']}: {d['why']}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
