"""The gates the game puts on a gift or an item ball, read from its scripts.

    PYTHONPATH=. python3 -m tools.oxide.balance.gates

The census (splits.gifts and splits.items, read by pool.items_by_split)
used to place every gift by its map's split and nothing else. The Flame
Plate's Hiker in Oreburgh Mine B1F is hidden until the Arceus event, which
is post-game, so the scorer's boxes handed Roark's split a Flame Plate the
player cannot have (found at least three times before 2026-10-22, fixed
then). This module reads when the player can first reach the line of
script that gives an item, so a gift counts only from that split.

A gift's split is the latest of three things:

1. Its map's split (splits.map_split), or none at all for a map no usable
   warp leads into (reachable_map): the decomp's UNUSED_ houses, whose only
   warps in sit on solid tiles with no stairs or door.
2. When the object that runs the giving script can first be seen. An
   object whose hidden flag is set at a new game or by its map's own
   transition script is shown only where some script clears that flag, so
   it is seen from the earliest split one of those clears is reached in.
3. The checks the script makes on the way to the give, each taken branch
   or fall-through read as a requirement:
   a. post-game: the Arceus event's variable, the game-completed flag, and
      the commands that read the National Dex or the League's victories,
      all zero before the Hall of Fame. A branch zero cannot take needs
      the post-game (POST_GAME_VARS, POST_GAME_FLAGS, POST_GAME_COMMANDS).
   b. a flag set (or, for one set at a new game, cleared): the earliest
      split a script on a map sets (clears) it in.
   c. a story variable at some value: the earliest split a script on a
      map sets it to a value the branch takes.
   d. an item in the Bag (CheckItem): the item's first split in the
      ungated census; a badge (CheckBadgeAcquired): its gym's split, since
      the census counts what is held by a split's end.
   A script's split for a line is the best over every path from its
   entries, each path as late as its latest requirement.

Wherever the reading is unsure (a flag or variable the game's C code
names, one a script outside any map writes, one written other than by
SetFlag, ClearFlag or SetVar, a compare against a non-number) it adds no
requirement, so the census keeps the map's split there, as before. The
known gaps: a transition script that hides an object again on every visit
after another map cleared its flag is read as shown, and a clear's own
script is read with its map's entries ungated by their objects.
"""
import collections
import functools
import glob
import json
import os
import re
import sys

from . import data, splits

SPLITS = splits.SPLITS
POST = SPLITS.index("Post")

# Post-game gates. Each is zero (unset) for the whole game before the Hall
# of Fame, so a branch that zero cannot take is post-game.
POST_GAME_VARS = {
    # Set to 1 in the Hall of Origin (scripts_hall_of_origin.s), reached
    # with the Azure Flute after the League, or by receiving an event
    # Arceus (mystery gift, GTS, trade), which a single run never does. It
    # shows the Flame Plate's Hiker in Oreburgh Mine B1F.
    "VAR_ARCEUS_EVENT_STATE",
}
POST_GAME_FLAGS = {"FLAG_GAME_COMPLETED"}   # set as the Hall of Fame closes
# Commands that write a post-game fact into their variable operand: which
# operand is the destination.
POST_GAME_COMMANDS = {"GetNationalDexEnabled": 0, "CheckGameCompleted": 0,
                      "CheckNationalDex": 0, "CheckNationalDexCompleted": 0,
                      "GetLeagueVictories": 0, "GetSetNationalDexEnabled": 1}

# Each badge id's gym (CheckBadgeAcquired's operand is the id, 0 for Coal).
BADGE_GYMS = ["Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron", "Candice", "Volkner"]

# The comparison codes GoToIf and CallIf take (scrcmd.inc): less, equal,
# greater, less or equal, greater or equal, not equal; and each one's
# opposite, which the fall-through of a GoToIf takes.
_TEST = {0: lambda a, b: a < b, 1: lambda a, b: a == b, 2: lambda a, b: a > b,
         3: lambda a, b: a <= b, 4: lambda a, b: a >= b, 5: lambda a, b: a != b}
_OPPOSITE = {0: 4, 1: 5, 2: 3, 3: 2, 4: 0, 5: 1}
_MACRO_TEST = {"Lt": 0, "Eq": 1, "Gt": 2, "Le": 3, "Ge": 4, "Ne": 5}
_LABEL = re.compile(r"^\s*(\w+):\s*$")
_LINE = re.compile(r"^\s*(\w+)\s*(.*?)\s*$")
_NAME = re.compile(r"\b((?:FLAG|VAR)_\w+)\b")


def _number(token):
    """A literal's value, or None for anything that is not a number."""
    token = token.strip()
    if token in ("TRUE", "FALSE"):
        return int(token == "TRUE")
    try:
        return int(token, 0)
    except ValueError:
        return None


def _key(token):
    """A flag or variable as its number, so VAR_RESULT, VAR_0x800C and 32780
    are one variable; anything else as its text."""
    token = token.strip()
    value = splits.flag_values().get(token)
    if value is not None:
        return value
    n = _number(token)
    return n if n is not None else token


@functools.lru_cache(maxsize=None)
def _names():
    """{number: name} for the persistent flags and variables, for reports."""
    out = {}
    for name, value in splits.flag_values().items():
        if name.startswith(("FLAG_", "VAR_")):
            out.setdefault(value, name)
    return out


def _is_var(key):
    return isinstance(key, int) and key >= splits.flag_values()["VARS_START"]


def _is_temp(key):
    """A variable that holds nothing between scripts: the script-local ones
    (VAR_0x8000 up, VAR_RESULT among them), the map-local ones and the
    object graphics ones."""
    fv = splits.flag_values()
    return isinstance(key, int) and (key >= fv["SCRIPT_LOCAL_VARS_START"]
                                     or fv["MAP_LOCAL_VARS_START"] <= key <= fv["VAR_OBJ_GFX_ID_F"])


POST_KEYS = frozenset(_key(n) for n in POST_GAME_VARS | POST_GAME_FLAGS)


def _sat(value, code, x):
    return _TEST[code](value, x)


class Script:
    """One script file read line by line, its lines kept in step with the
    text splits._script gives (so a gift's line number is the same here).
    `ops[i]` is what line i does to the flow: ("next",), ("stop",),
    ("goto", label), ("call", label), or ("branch", label, is_call, taken,
    fall) with each requirement as a tuple (see _requirement) or None."""

    def __init__(self, stem):
        self.stem = stem
        self.lines = splits._script(stem).split("\n")
        self.labels, self.entries, self.ops = {}, [], []
        self.sets, self.clears, self.setvars, self.other_writes = [], [], [], set()
        self._read()

    def _read(self):
        compare, made, comment = None, {}, False
        for i, raw in enumerate(self.lines):
            line = raw
            if comment:
                if "*/" not in line:
                    self.ops.append(("next",))
                    continue
                line, comment = line.split("*/", 1)[1], False
            if "/*" in line:
                head, tail = line.split("/*", 1)
                comment = "*/" not in tail
                line = head + (tail.split("*/", 1)[1] if not comment else "")
            line = line.split("@", 1)[0] if line.lstrip().startswith("@") else line
            m = _LABEL.match(line)
            if m:
                self.labels[m.group(1)] = i
                compare, made = None, {}
                self.ops.append(("next",))
                continue
            m = _LINE.match(line)
            if not m:
                self.ops.append(("next",))
                continue
            cmd, args = m.group(1), [a.strip() for a in m.group(2).split(",")] if m.group(2) else []
            op = ("next",)
            if cmd == "ScriptEntry" and args:
                self.entries.append(args[0])
            elif cmd in ("End", "EndMovement", "ScriptEntryEnd", "Return", "ReturnCommonScript"):
                op = ("stop",)
            elif cmd == "GoTo" and args:
                op = ("goto", args[0])
            elif cmd == "Call" and args:
                op = ("call", args[0])
            elif cmd == "CheckFlag" and args:
                compare = ("flag", _key(args[0]))
            elif cmd in ("CompareVarToValue", "CompareVar") and len(args) >= 2:
                compare = ("var", _key(args[0]), _number(args[1]))
            elif cmd == "CompareVarToVar":
                compare = None
            elif cmd in ("GoToIf", "CallIf") and len(args) >= 2:
                code = _number(args[0])
                op = self._branch(args[1], cmd == "CallIf", compare, code, made)
            elif re.fullmatch(r"(GoTo|Call)If(Set|Unset)", cmd) and len(args) >= 2:
                code = 1 if cmd.endswith("IfSet") else 0
                op = self._branch(args[1], cmd.startswith("Call"), ("flag", _key(args[0])), code, made)
            elif re.fullmatch(r"(GoTo|Call)If(Lt|Eq|Gt|Le|Ge|Ne)", cmd) and len(args) >= 3:
                code = _MACRO_TEST[cmd[-2:]]
                op = self._branch(args[2], cmd.startswith("Call"),
                                  ("var", _key(args[0]), _number(args[1])), code, made)
            elif cmd == "GoToIfBadgeAcquired" and len(args) >= 2:
                made = {**made, _key("VAR_RESULT"): ("badge", _number(args[0]))}
                op = self._branch(args[1], False, ("var", _key("VAR_RESULT"), 1), 1, made)
            elif re.match(r"(GoTo|Call)If", cmd) and args:
                # Any other conditional jump (the Bag is full, not enough
                # money): either way, with nothing required.
                op = ("branch", args[-1], cmd.startswith("Call"), None, None)
            elif cmd == "CheckItem" and len(args) >= 3:
                made = {**made, _key(args[2]): ("item", args[0])}
            elif cmd == "CheckBadgeAcquired" and len(args) >= 2:
                made = {**made, _key(args[1]): ("badge", _number(args[0]))}
            elif cmd in POST_GAME_COMMANDS and len(args) > POST_GAME_COMMANDS[cmd]:
                made = {**made, _key(args[POST_GAME_COMMANDS[cmd]]): ("post",)}
            elif cmd == "SetFlag" and args:
                self.sets.append((_key(args[0]), i))
            elif cmd == "ClearFlag" and args:
                self.clears.append((_key(args[0]), i))
            elif cmd in ("SetVar", "SetVarFromValue") and len(args) >= 2:
                var, value = _key(args[0]), _number(args[1])
                made = {**made, var: ("const", value)}
                if _is_var(var) and not _is_temp(var):
                    if value is None:
                        self.other_writes.add(var)
                    else:
                        self.setvars.append((var, value, i))
            else:
                # Anything else that names a persistent variable may write
                # it; and a variable a command writes no longer holds what
                # an earlier command left in it.
                for a in args:
                    k = _key(a)
                    if _is_var(k):
                        made.pop(k, None)
                        if not _is_temp(k):
                            self.other_writes.add(k)
            self.ops.append(op)

    def _branch(self, label, is_call, compare, code, made):
        taken = _requirement(compare, code, made)
        fall = None if is_call or code not in _OPPOSITE else _requirement(compare, _OPPOSITE[code], made)
        return ("branch", label, is_call, taken, fall)

    def successors(self, i):
        """[(line, requirement)] the flow can go to from line i."""
        op, nxt = self.ops[i], i + 1
        out = []
        if op[0] == "stop":
            return out
        if op[0] == "goto":
            return [(self.labels[op[1]], None)] if op[1] in self.labels else []
        if op[0] == "call":
            if op[1] in self.labels:
                out.append((self.labels[op[1]], None))
        elif op[0] == "branch":
            _b, label, _is_call, taken, fall = op
            if label in self.labels:
                out.append((self.labels[label], taken))
            if nxt < len(self.ops):
                out.append((nxt, fall))
            return out
        if nxt < len(self.ops):
            out.append((nxt, None))
        return out


def _requirement(compare, code, made):
    """What taking a branch needs: None for nothing, ("never",) for a branch
    the script cannot take, ("post",), ("flag", key, wanted set or clear),
    ("var", key, code, value), ("item", constant) or ("badge", id)."""
    if compare is None or code not in _TEST:
        return None
    if compare[0] == "flag":
        key = compare[1]
        if code not in (0, 1):
            return None
        if key in POST_KEYS:
            return ("post",) if code == 1 else None
        return ("flag", key, code == 1)
    _v, key, x = compare
    if x is None:
        return None
    source = made.get(key)
    if key in POST_KEYS or (source and source[0] == "post"):
        return None if _sat(0, code, x) else ("post",)
    if source and source[0] == "const":
        return None if source[1] is None or _sat(source[1], code, x) else ("never",)
    if source and source[0] == "item":
        return None if _sat(0, code, x) else ("item", source[1])
    if source and source[0] == "badge":
        return None if _sat(0, code, x) or source[1] is None else ("badge", source[1])
    if _is_temp(key) or not _is_var(key):
        return None
    return ("var", key, code, x)


@functools.lru_cache(maxsize=None)
def script(stem):
    return Script(stem)


@functools.lru_cache(maxsize=None)
def _map_stems():
    """{script file stem: [map headers that run it]}."""
    out = collections.defaultdict(list)
    for header, fields in splits.headers().items():
        stem = fields.get("scriptsArchiveID")
        if stem and os.path.exists(os.path.join(data.ROOT, "res", "field", "scripts", f"{stem}.s")):
            out[stem].append(header)
    return dict(out)


@functools.lru_cache(maxsize=None)
def _events(header):
    stem = splits.headers()[header].get("eventsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "events", f"{stem}.json") if stem else None
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def _init_entries(header):
    """The entry numbers a map runs as it loads (its init script's
    InitScriptEntry lines): they run before the player can act."""
    stem = splits.headers()[header].get("initScriptsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "scripts", f"{stem}.s") if stem else None
    if not path or not os.path.exists(path):
        return frozenset()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return frozenset(int(n) for n in re.findall(r"^\s*InitScriptEntry_\w+\s+(\d+)", text, re.M))


@functools.lru_cache(maxsize=None)
def _c_names():
    """Every flag and variable name the game's C code mentions: those may be
    written where no script shows it, so the reading adds no requirement."""
    out = set()
    for pattern in ("src/**/*.c", "include/**/*.h"):
        for path in glob.glob(os.path.join(data.ROOT, pattern), recursive=True):
            with open(path, encoding="utf-8", errors="replace") as f:
                out.update(_NAME.findall(f.read()))
    return frozenset(_key(n) for n in out)


@functools.lru_cache(maxsize=None)
def _sites():
    """Where every flag is set and cleared and every story variable set,
    over all script files: {"set"|"clear": {key: [(stem, line)]},
    "setvar": {key: [(stem, value, line)]}, "unsure": {keys}}. A write in a
    file no map runs (scripts_common and the like) makes its key unsure,
    except a new game's own sets, kept apart as "new_game"."""
    out = {"set": collections.defaultdict(list), "clear": collections.defaultdict(list),
           "setvar": collections.defaultdict(list), "unsure": set(), "new_game": set(),
           "new_game_vars": {}}
    maps = _map_stems()
    for path in sorted(glob.glob(os.path.join(data.ROOT, "res", "field", "scripts", "*.s"))):
        stem = os.path.basename(path)[:-2]
        sc = script(stem)
        if stem == "scripts_init_new_game":
            out["new_game"].update(k for k, _i in sc.sets)
            out["new_game_vars"].update({k: v for k, v, _i in sc.setvars})
            continue
        if stem not in maps:
            out["unsure"].update(k for k, _i in sc.sets + sc.clears)
            out["unsure"].update(k for k, _v, _i in sc.setvars)
            out["unsure"].update(sc.other_writes)
            continue
        for k, i in sc.sets:
            out["set"][k].append((stem, i))
        for k, i in sc.clears:
            out["clear"][k].append((stem, i))
        for k, v, i in sc.setvars:
            out["setvar"][k].append((stem, v, i))
        out["unsure"].update(sc.other_writes)
    return out


# A guard against loops: a flag's split asks for its clears' splits, which
# ask for their scripts' entries, which may ask for that flag again. A
# question asked again while it is being answered adds no requirement.
_ASKING = set()


def _guarded(key, compute):
    if key in _ASKING:
        return 0
    _ASKING.add(key)
    try:
        return compute()
    finally:
        _ASKING.discard(key)


def _earliest(sites):
    """The earliest split index among script lines, or None for none."""
    found = [line_split(stem, i) for stem, i in sites]
    found = [s for s in found if s is not None]
    return min(found) if found else None


@functools.lru_cache(maxsize=None)
def requirement_split(req):
    """The earliest split index a requirement can hold in; None if never."""
    if req is None:
        return 0
    kind = req[0]
    if kind == "never":
        return None
    if kind == "post":
        return POST
    if kind == "badge":
        # The badge is won as its gym's split closes, and the census counts
        # what is held by a split's end (a gym's TM is its own split's), so
        # a badge check holds from the gym's own split.
        gym = BADGE_GYMS[req[1]] if 0 <= req[1] < len(BADGE_GYMS) else None
        return SPLITS.index(gym) if gym else 0
    if kind == "item":
        first = _raw_item_first().get(req[1])
        return first if first is not None else 0
    sites = _sites()
    key = req[1]
    if key in sites["unsure"] or key in _c_names():
        return 0
    if kind == "flag":
        wanted = req[2]
        starts = key in sites["new_game"]
        if wanted == starts:
            return 0
        found = _guarded(req, lambda: _earliest(sites["set" if wanted else "clear"].get(key, ())))
        return 0 if found is None else found
    if kind == "var":
        _k, _key_, code, x = req
        start = sites["new_game_vars"].get(key, 0)
        if _sat(start, code, x):
            return 0
        found = _guarded(req, lambda: _earliest(
            [(stem, i) for stem, v, i in sites["setvar"].get(key, ()) if _sat(v, code, x)]))
        return 0 if found is None else found
    return 0


@functools.lru_cache(maxsize=None)
def _raw_item_first():
    """{item: the first split index it is in hand in}, from the census's
    sources without any gate: marts, trainer rewards, and every gift, ball
    and hidden item at its map's split. A CheckItem requirement reads it."""
    first = {}

    def seen(split, item):
        if split in SPLITS and (item not in first or SPLITS.index(split) < first[item]):
            first[item] = SPLITS.index(split)
    for split, _t, item in splits.marts():
        seen(split, item)
    for split, _t, item in splits.trainer_rewards():
        seen(split, item)
    for header, _stem, _i, item in raw_gifts():
        seen(splits.map_split(header)[0], item)
    return first


def _object_gate(header, flag):
    """The earliest split index an object with this hidden flag is shown
    in: at once unless the flag starts set, at a new game or by the map's
    own loading scripts; then the earliest split a script clears it in."""
    if flag in (None, "0", 0, ""):
        return 0
    key = _key(flag)
    if key in _sites()["unsure"] or key in _c_names():
        return 0
    starts = key in _sites()["new_game"] or _set_on_load(header, key)
    if not starts:
        return 0
    found = _guarded(("show", key), lambda: _earliest(_sites()["clear"].get(key, ())))
    return 0 if found is None else found


def _set_on_load(header, key):
    """Whether the map's loading scripts can set the flag."""
    stem = splits.headers()[header].get("scriptsArchiveID")
    if stem not in _map_stems():
        return False
    sc = script(stem)
    starts = [sc.labels[sc.entries[n - 1]] for n in _init_entries(header)
              if 0 < n <= len(sc.entries) and sc.entries[n - 1] in sc.labels]
    seen, todo = set(starts), list(starts)
    while todo:
        i = todo.pop()
        for j, _req in sc.successors(i):
            if j not in seen:
                seen.add(j)
                todo.append(j)
    return any(k == key and i in seen for k, i in sc.sets)


@functools.lru_cache(maxsize=None)
def _entry_gates(header):
    """{entry number: the earliest split index something can run it in}.
    An entry the map loads with, or a sign or trigger runs, is open at
    once; one only objects run opens with the first of them to be shown;
    one nothing on the map runs (another script calls it) is open at once."""
    ev = _events(header)
    runners = collections.defaultdict(list)
    for obj in ev.get("object_events", []):
        if isinstance(obj.get("script"), int):
            runners[obj["script"]].append(obj.get("hidden_flag"))
    for kind in ("bg_events", "coord_events"):
        for e in ev.get(kind, []):
            if isinstance(e.get("script"), int):
                runners[e["script"]].append(None)
    for n in _init_entries(header):
        runners[n].append(None)
    return {n: min(_object_gate(header, flag) for flag in flags) for n, flags in runners.items()}


@functools.lru_cache(maxsize=None)
def _line_splits(stem, header):
    """{line: the earliest split index the script reaches it in}, over every
    path from the map's entries, each path as late as its latest gate and
    never earlier than the map's own split."""
    sc = script(stem)
    base = splits.map_split(header)[0]
    if base not in SPLITS or not reachable_map(header):
        return {}
    base = SPLITS.index(base)
    gates = _entry_gates(header)
    best = {}
    todo = []
    for n, label in enumerate(sc.entries, 1):
        if label in sc.labels:
            g = gates.get(n, 0)
            if g is not None:
                todo.append((max(base, g), sc.labels[label]))
    # A bottleneck search: a line's split is the least, over the paths to
    # it, of the latest requirement on the path. Splits are few, so a plain
    # work list that revisits a line whenever its split improves is enough.
    while todo:
        todo.sort(reverse=True)
        at, i = todo.pop()
        if i in best and best[i] <= at:
            continue
        best[i] = at
        for j, req in sc.successors(i):
            need = requirement_split(req)
            if need is None:
                continue
            nxt = max(at, need)
            if j not in best or nxt < best[j]:
                todo.append((nxt, j))
    return best


def line_split(stem, i):
    """The earliest split index any map running this script file reaches
    line i in, or None if none does."""
    found = [_line_splits(stem, h).get(i) for h in _map_stems().get(stem, ())]
    found = [s for s in found if s is not None]
    return min(found) if found else None


@functools.lru_cache(maxsize=None)
def reachable_map(header):
    """Whether the player can enter a map. False for a map every warp into
    which is unusable (a solid tile with no behaviour, the stairs of the
    decomp's UNUSED_ upper floors) or comes from a map that cannot be
    entered, and for an UNUSED_ map nothing leads into, unless a script
    puts the player there."""
    if header in splits.script_arrivals():
        return True
    usable, dead = False, False
    for src in splits._warps_into().get(header, ()):
        for warp in _events(src).get("warp_events", []):
            if warp.get("dest_header_id") != "MAP_HEADER_" + header:
                continue
            if _dead_tile(src, warp["x"], warp["z"]):
                dead = True
            elif src != header and _guarded(("map", src), lambda: reachable_map(src)):
                usable = True
    if usable:
        return True
    return not (dead or header.startswith("UNUSED_"))


@functools.lru_cache(maxsize=None)
def _grid(header):
    try:
        return splits._grid(header)[0]
    except (SystemExit, OSError, KeyError, ValueError):
        return None


def _dead_tile(header, x, z):
    grid = _grid(header)
    if grid is None or (x, z) not in grid:
        return False
    collision, behaviour = grid[(x, z)]
    return bool(collision) and behaviour in ("", "TILE_BEHAVIOR_NONE")


# An NPC gift, as splits.gifts reads it: the item set into VAR_0x8004 and a
# give script called, or AddItem.
@functools.lru_cache(maxsize=None)
def raw_gifts():
    """[(map, script stem, line, item)] for every gift line on every map."""
    out = []
    for header, fields in splits.headers().items():
        stem = fields.get("scriptsArchiveID")
        if stem not in _map_stems():
            continue
        last = None
        for i, line in enumerate(script(stem).lines):
            m = splits._SET_ITEM.match(line)
            if m:
                last = m.group(1)
                continue
            m = splits._ADD_ITEM.match(line)
            token = (last if m.group(1) in splits._ITEM_VAR else m.group(1)) if m else \
                (last if splits._GIVE.match(line) else None)
            if token and (token.startswith("ITEM_") or token.isdigit()):
                item = splits._item(token)
                if item.startswith("ITEM_") and item != "ITEM_NONE":
                    out.append((header, stem, i, item))
    return out


# Gates the reading cannot see, by hand: {(map, item): (split or None,
# the script and the gate that hold it)}. A row overrides the reading for
# every give of that item on that map. Empty since the reader covers every
# gate found on 2026-10-22; add a row rather than special-casing a box.
OVERRIDES = {}


def gift_split(header, stem, i):
    """The split a gift line can first be had in, or None (an unreachable
    map, an unplaced one, or a line no path reaches)."""
    item = next((it for h, st, j, it in raw_gifts() if (h, st, j) == (header, stem, i)), None)
    if (header, item) in OVERRIDES:
        return OVERRIDES[(header, item)][0]
    at = _line_splits(stem, header).get(i)
    return SPLITS[at] if at is not None else None


def ball_split(header, flag):
    """The split an item ball can first be picked up in, before the flood
    of splits.item_reach: its map's split, or later if its object is hidden
    until a script shows it; None on a map that cannot be entered."""
    base = splits.map_split(header)[0]
    if base not in SPLITS:
        return base
    if not reachable_map(header):
        return None
    gate = _object_gate(header, flag)
    return SPLITS[max(SPLITS.index(base), gate)]


def describe(req):
    """A requirement in words, for the audit."""
    if req is None:
        return "nothing"
    kind = req[0]
    if kind in ("flag", "var"):
        name = _names().get(req[1], req[1])
        if kind == "flag":
            return f"{name} {'set' if req[2] else 'clear'}"
        return f"{name} {['<', '==', '>', '<=', '>=', '!='][req[2]]} {req[3]}"
    return " ".join(str(r) for r in req)


def why(header, stem, i):
    """The requirements on the paths to a gift line that set its split, for
    the audit: the entry gate and every requirement met on the way whose
    split is the line's own."""
    at = _line_splits(stem, header).get(i)
    if at is None:
        return "unreachable map" if not reachable_map(header) else "no path"
    sc = script(stem)
    reasons = set()
    for n, g in _entry_gates(header).items():
        if g == at and g > 0:
            for obj in _events(header).get("object_events", []):
                if obj.get("script") == n and obj.get("hidden_flag") not in (None, "0"):
                    reasons.add(f"object hidden by {obj['hidden_flag']}")
    for j, op in enumerate(sc.ops):
        if op[0] == "branch":
            for req in op[3:5]:
                if req and requirement_split(req) == at and at > 0:
                    reasons.add(describe(req))
    return "; ".join(sorted(reasons)) or "map split"


def main(argv=None):
    rows = []
    for header, stem, i, item in raw_gifts():
        before = splits.map_split(header)[0]
        after = gift_split(header, stem, i)
        if before != after:
            rows.append((item, header, before, after, why(header, stem, i)))
    for row in sorted(set(rows), key=lambda r: (SPLITS.index(r[2]) if r[2] in SPLITS else 99, r[1], r[0])):
        print(" | ".join(str(c) for c in row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
