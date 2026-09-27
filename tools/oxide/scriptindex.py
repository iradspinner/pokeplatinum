#!/usr/bin/env python3
"""Index every field script and map event: what each map does.

Platinum Oxide project (Ian, 2026-09-27). Reads every field script, init
script and event file, and writes, per map, the Pokemon and eggs it gives,
its trades, its static and legendary battles, every trainer battle, the items
it gives, its item balls and hidden items, and every flag and variable it
sets, clears or checks. Each entry is compared with the same map on `main`
(vanilla Platinum) and marked vanilla or added; an added entry is put down to
the base ROM or to Oxide from git history. It changes no game data and needs
no ROM build.

Outputs, both generated, never edited by hand:
    docs/oxide/script-index.md    a summary page, then one section per map,
                                  grouped by split where the encounter tool
                                  can place the map
    docs/oxide/script-index.json  the same facts for the other tools

Usage:
    python3 tools/oxide/scriptindex.py            # write both files
    python3 tools/oxide/scriptindex.py --check    # exit 1 if either differs
                                                  # from what the tool renders

Run from the repository root. It needs `main` (vanilla) as a local branch and
the full history of this branch: `git fetch origin main:main` and, in a
shallow clone, `git fetch --unshallow`.

How the scripts are read. The 86 machine-generated scripts (bulk_scripts.py)
use primitive commands and raw numbers where the hand-written ones use
wrapper macros and names, so every line is expanded through the repo's own
`asm/macros/scrcmd.inc` down to primitive commands first, and every operand
is resolved to a number through the generated constant lists. Both kinds of
script then look the same. A number is named through the table its operand's
kind decides (a trainer slot through trainers.txt, and so on), which is
reading, not guessing; what the tool cannot read is counted, not guessed:
raw `.byte` data, commands with no name (`ScrCmd_20D`), numbers no table
holds, and a variable the script does not set on any path it can see.

A variable operand is traced back through the script's control flow, into and
out of `Call`s, to the commands that set it, with the branch conditions passed
on the way ("620 if VAR_0x800C == SPECIES_CHIMCHAR"). One the script never
sets is "set elsewhere"; for a saved variable the index adds the constants
any other script stores in it.

Where an added entry came from. The base ROM's content reached this branch
through a handful of import commits (the per-map carry-overs, the two bulk
generations of scripts and events, and the Test.nds update), recognised by
their subjects below. `git blame` names the commit that last wrote each line
an added entry rests on: one of those means base ROM, any later commit on
this branch means Oxide, and anything else (an upstream pret commit, or no
history) is "unclear". The Overseer checks the attribution locally against
the base ROM.
"""
import argparse
import collections
import concurrent.futures
import json
import os
import re
import subprocess
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

OUT_MD = os.path.join("docs", "oxide", "script-index.md")
OUT_JSON = os.path.join("docs", "oxide", "script-index.json")

SCRIPTS_DIR = "res/field/scripts"
EVENTS_DIR = "res/field/events"
HEADERS = "include/data/map_headers.h"
HIDDEN_ITEMS = "include/data/field/hidden_items.h"
SCRIPT_MANAGER_H = "include/script_manager.h"
SCRIPT_MANAGER_C = "src/script_manager.c"
NPC_TRADES_H = "include/constants/npc_trades.h"
NPC_TRADES_DIR = "res/npc_trades"
SCRCMD_INC = "asm/macros/scrcmd.inc"

# The commits that brought the base ROM's scripts and events in. Everything
# else on this branch after it left `main` is Oxide's own work.
BASE_ROM_SUBJECTS = re.compile(
    r"^(Carry over "
    r"|Generate the remaining 86 field scripts from the base ROM"
    r"|Rewrite the remaining 84 maps' events from the base ROM"
    r"|Base ROM to Test\.nds)")

# Script ids the engine reads as "an item ball", "a hidden item" and "a
# trainer who sees the player" (include/script_manager.h).
VISIBLE_ITEMS = (7000, 8000)
HIDDEN_ITEMS_RANGE = (8000, 8800)
SINGLE_BATTLES = (3000, 5000)
DOUBLE_BATTLES = (5000, 7000)

# Operands at or above this are variables: the engine reads the variable's
# value in their place (FieldSystem_TryGetVar).
VARS_START = 0x4000
TEMP_VARS_START = 0x8000

# The two common scripts that hand the player the item in VAR_0x8004, in the
# quantity in VAR_0x8005 (Common_GiveItemQuantity and its NoLineFeed twin).
GIVE_ITEM_COMMON = {0x7FC, 0x7E0}
VAR_ITEM, VAR_COUNT = 0x8004, 0x8005

# GoToIf's condition byte, as the wrapper macros write it.
CONDITIONS = {0: "<", 1: "==", 2: ">", 3: "<=", 4: ">=", 5: "!="}
NEGATED = {"<": ">=", "==": "!=", ">": "<=", "<=": ">", ">=": "<", "!=": "=="}

# Parameters a command writes to rather than reads. Every name with "dest"
# in it is a write; these are the others.
WRITE_PARAMS = {
    "countdownVarID", "cursorPosVar", "hasPrintVar", "printTypeVar",
    "resultVar", "selectedOptionVar", "successVar", "listOffsetVar",
    "speciesVar", "itemVar", "varPillarsSeen", "varRoomsVisited",
}

# What each command of interest is, and which operand holds what.
TRAINER_CMDS = {
    "StartTrainerBattle": ("enemyTrainer1", "enemyTrainer2"),
    "StartTagBattle": ("partnerTrainer", "enemyTrainer1", "enemyTrainer2"),
    "StartFirstBattle": ("trainerID",),
}
STATIC_CMDS = {
    "StartWildBattle": ("species", "level"),
    "StartLegendaryBattle": ("species", "level"),
    "StartGiratinaOriginBattle": ("species", "level"),
}
GIFT_CMDS = {
    "GivePokemon": ("species", "level", "heldItem"),
    "GiveDesignedPokemon": ("species", "level", "heldItem"),
}

# Shared files indexed by an id rather than by script: one entry per trainer
# (the trainers who see the player), per item (item balls) and per hidden
# item. An entry no event names is an unused id, not a lost script.
TABLE_FILES = {"scripts_battles", "scripts_visible_items", "scripts_hidden_items"}

# Script files whose scripts the engine starts by number from C, so an entry
# no event or script names is not lost. Matched as a prefix of the file name.
ENGINE_STARTED = {
    "scripts_villa": "src/overlay005/villa_furniture.c, sVillaFurnitureScriptIDs",
    "scripts_distortion_world": "src/overlay009/ov9_02249960.c",
}

KINDS = [
    ("pokemon", "Pokemon given"),
    ("eggs", "Eggs given"),
    ("trades", "Trades"),
    ("statics", "Static and legendary battles"),
    ("trainers", "Trainer battles"),
    ("items", "Items given"),
    ("item_balls", "Item balls"),
    ("hidden_items", "Hidden items"),
    ("flags", "Flags"),
    ("vars", "Variables"),
]


# ---------------------------------------------------------------- git
class Tree:
    """Files from the working tree (ref None) or from a git ref."""

    def __init__(self, ref=None):
        self.ref = ref
        self._cache = {}
        self._listing = None

    def read(self, path):
        if path in self._cache:
            return self._cache[path]
        if self.ref is None:
            try:
                with open(os.path.join(ROOT, path), encoding="utf-8") as f:
                    text = f.read()
            except OSError:
                text = None
        else:
            out = subprocess.run(["git", "show", f"{self.ref}:{path}"],
                                 capture_output=True, text=True)
            text = out.stdout if out.returncode == 0 else None
        self._cache[path] = text
        return text

    def prefetch(self, paths):
        """Read many files from the ref in one git process."""
        if self.ref is None:
            return
        want = [p for p in paths if p not in self._cache]
        if not want:
            return
        proc = subprocess.run(
            ["git", "cat-file", "--batch"], input="".join(f"{self.ref}:{p}\n" for p in want).encode(),
            capture_output=True, check=True)
        data = proc.stdout
        pos = 0
        for p in want:
            nl = data.index(b"\n", pos)
            header = data[pos:nl].decode()
            pos = nl + 1
            if header.endswith("missing"):
                self._cache[p] = None
                continue
            size = int(header.split()[2])
            self._cache[p] = data[pos:pos + size].decode("utf-8")
            pos += size + 1

    def listdir(self, path):
        if self.ref is None:
            try:
                return sorted(os.listdir(os.path.join(ROOT, path)))
            except OSError:
                return []
        if self._listing is None:
            out = subprocess.run(["git", "ls-tree", "-r", "--name-only", self.ref],
                                 capture_output=True, text=True, check=True)
            self._listing = out.stdout.splitlines()
        prefix = path.rstrip("/") + "/"
        return sorted({p[len(prefix):].split("/")[0] for p in self._listing if p.startswith(prefix)})


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


# ---------------------------------------------------------------- constants
def metang(text):
    """NAME -> value for a generated/*.txt list: a bare name is one more than
    the line before it, `NAME = X` takes X's value (a number or a name)."""
    out = {}
    prev = -1
    for raw in (text or "").splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if "=" in line:
            name, expr = (s.strip() for s in line.split("=", 1))
            value = int(expr, 0) if re.match(r"^-?(0x[0-9a-fA-F]+|\d+)$", expr) else out[expr]
        else:
            name, value = line, prev + 1
        out[name] = value
        prev = value
    return out


def c_enum(text):
    """NAME -> value for the enums and #defines of a C header."""
    out = {}
    for m in re.finditer(r"^\s*#define\s+(\w+)\s+(\(?-?(?:0x[0-9a-fA-F]+|\d+)\)?)\s*(?://.*|/\*.*)?$", text or "", re.M):
        out[m.group(1)] = int(m.group(2).strip("()"), 0)
    for body in re.findall(r"enum\s*\w*\s*\{(.*?)\}", text or "", re.S):
        prev = -1
        for entry in body.split(","):
            entry = re.sub(r"//.*|/\*.*?\*/", "", entry, flags=re.S).strip()
            if not entry:
                continue
            m = re.match(r"(\w+)\s*(?:=\s*(.+))?$", entry, re.S)
            if not m:
                continue
            if m.group(2):
                expr = m.group(2).strip()
                try:
                    value = int(expr, 0)
                except ValueError:
                    value = out.get(expr, prev + 1)
            else:
                value = prev + 1
            out[m.group(1)] = value
            prev = value
    return out


class Consts:
    """Every name a script operand can use, and the way back from a number."""

    def __init__(self, tree):
        self.tree = tree
        self.tables = {}
        for kind in ("vars_flags", "trainers", "species", "items", "moves", "map_headers"):
            self.tables[kind] = metang(tree.read(f"generated/{kind}.txt"))
        self.npc_trades = c_enum(tree.read(NPC_TRADES_H))
        self.values = {}
        for table in self.tables.values():
            self.values.update(table)
        self.values.update(self.npc_trades)
        self.values.update({"TRUE": 1, "FALSE": 0, "NULL": 0})
        vf = self.tables["vars_flags"]
        self.daily = (vf["DAILY_FLAGS_START"], vf["DAILY_FLAGS_END"])
        self.hidden_flags_start = vf["HIDDEN_ITEM_FLAGS_START"]
        self.trainer_flags_start = vf["TRAINER_DEFEATED_FLAGS_START"]
        self.vars_end = vf.get("VARS_END", TEMP_VARS_START - 1)
        self._names = {}

    def names(self, kind):
        """value -> preferred name, for a kind of operand."""
        if kind in self._names:
            return self._names[kind]
        out = {}
        if kind in ("flag", "var"):
            prefix = "FLAG_" if kind == "flag" else "VAR_"
            for name, value in self.tables["vars_flags"].items():
                if (value >= VARS_START) != (kind == "var"):
                    continue
                # an alias (VAR_RESULT = VAR_0x800C) is the better name, and
                # a range marker (MAP_LOCAL_FLAGS_START) never is
                if name.startswith(prefix) or value not in out:
                    if name.startswith(prefix) or not out.get(value, "").startswith(prefix):
                        out[value] = name
        elif kind == "trade":
            out = {v: k for k, v in self.npc_trades.items()}
        else:
            table = {"trainer": "trainers", "species": "species", "item": "items",
                     "move": "moves", "header": "map_headers"}[kind]
            for name, value in self.tables[table].items():
                out.setdefault(value, name)
        self._names[kind] = out
        return out

    def name(self, kind, value):
        return self.names(kind).get(value)

    def is_map_local_var(self, var):
        vf = self.tables["vars_flags"]
        return vf.get("MAP_LOCAL_VARS_START", 0) <= var <= vf.get("MAP_LOCAL_VARS_END", -1)

    def is_daily(self, flag):
        return self.daily[0] <= flag <= self.daily[1]


# ---------------------------------------------------------------- macros
class Macro:
    def __init__(self, name, params, defaults, body):
        self.name = name
        self.params = params
        self.defaults = defaults
        self.body = body
        head = body[0] if body else ""
        self.primitive = bool(re.match(r"\.short\s+SCRCMD_\w+$", head))


def strip_preprocessor(text, defined=()):
    """Drop C comments and the #ifdef blocks a normal build leaves out (the
    test kit's), keeping line numbers."""
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out = []
    stack = []
    for line in text.split("\n"):
        s = line.strip()
        m = re.match(r"#\s*(ifdef|ifndef|if|else|endif)\b\s*(\w*)", s)
        if m:
            kind, sym = m.groups()
            if kind in ("ifdef", "ifndef"):
                on = (sym in defined) == (kind == "ifdef")
                stack.append(on)
            elif kind == "if":
                stack.append(True)
            elif kind == "else" and stack:
                stack[-1] = not stack[-1]
            elif kind == "endif" and stack:
                stack.pop()
            out.append("")
            continue
        out.append(line if all(stack) else "")
    return out


def load_macros(tree):
    lines = strip_preprocessor(tree.read(SCRCMD_INC))
    macros = {}
    i = 0
    while i < len(lines):
        m = re.match(r"\s*\.macro\s+(\w+)\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        name, args = m.group(1), m.group(2)
        params, defaults = [], {}
        for a in args.split(","):
            a = a.strip()
            if not a:
                continue
            if "=" in a:
                p, d = (s.strip() for s in a.split("=", 1))
                defaults[p] = d
            else:
                p = a
            params.append(p)
        body = []
        i += 1
        while i < len(lines) and not re.match(r"\s*\.endm\b", lines[i]):
            s = re.sub(r"\s*@.*$", "", lines[i]).strip()
            if s:
                body.append(s)
            i += 1
        macros[name] = Macro(name, params, defaults, body)
        i += 1
    return macros


def split_args(text):
    out, depth, cur = [], 0, ""
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


class Resolver:
    """Turns operand text into a number: a literal, a name from the constant
    lists, a file's own #define, or simple arithmetic on those. None when it
    cannot."""

    NUMBER = re.compile(r"^-?(0x[0-9a-fA-F]+|\d+)$")
    EXPR = re.compile(r"^[\w\s()+\-*|&<>]+$")
    TOKEN = re.compile(r"\b(?:0x[0-9a-fA-F]+|\d+|[A-Za-z_]\w*)\b")

    def __init__(self, consts, local=None):
        self.consts = consts
        self.local = local or {}
        self.cache = {}

    def __call__(self, text):
        text = text.strip()
        if text not in self.cache:
            self.cache[text] = None     # a #define that names itself stops here
            self.cache[text] = self._resolve(text)
        return self.cache[text]

    def _name(self, name):
        if name in self.local:
            return self(self.local[name])
        return self.consts.values.get(name)

    def _resolve(self, text):
        if self.NUMBER.match(text):
            return int(text, 0)
        if re.match(r"^[A-Za-z_]\w*$", text):
            return self._name(text)
        if self.EXPR.match(text):
            def sub(m):
                tok = m.group(0)
                v = int(tok, 0) if tok[0].isdigit() else self._name(tok)
                if v is None:
                    raise KeyError(tok)
                return str(v)
            try:
                return int(eval(self.TOKEN.sub(sub, text), {"__builtins__": {}}))
            except Exception:
                return None
        return None


def eval_condition(cond, resolve):
    """A `.if` condition from scrcmd.inc. An operand that does not resolve
    counts as 0, which is the value side of every such test."""
    def sub(m):
        v = resolve(m.group(0))
        return str(v if v is not None else 0)
    expr = re.sub(r"\b(?:0x[0-9a-fA-F]+|[A-Za-z_]\w*)\b", sub, cond)
    expr = expr.replace("&&", " and ").replace("||", " or ").replace("!", " not ").replace(" not =", "!=")
    try:
        return bool(eval(expr, {"__builtins__": {}}))
    except Exception:
        return False


def expand(macros, name, args, resolve, depth=0):
    """A macro call down to primitive commands: [(name, {param: text})]."""
    macro = macros.get(name)
    if macro is None:
        return None
    values = {}
    for i, p in enumerate(macro.params):
        if i < len(args):
            values[p] = args[i]
        elif p in macro.defaults:
            values[p] = macro.defaults[p]
        else:
            values[p] = ""
    if macro.primitive:
        return [(name, values)]
    if depth > 8:
        return []
    out = []
    stack = []
    for line in macro.body:
        line = re.sub(r"\\(\w+)(\\\(\))?", lambda m: values.get(m.group(1), m.group(0)), line)
        m = re.match(r"\.(ifnb|ifb|if|else|endif)\b\s*(.*)$", line)
        if m:
            if m.group(1) == "if":
                stack.append(eval_condition(m.group(2), resolve))
            elif m.group(1) in ("ifnb", "ifb"):
                blank = not m.group(2).strip() or m.group(2).strip().startswith("\\")
                stack.append(blank == (m.group(1) == "ifb"))
            elif m.group(1) == "else":
                stack[-1] = not stack[-1]
            else:
                stack.pop()
            continue
        if not all(stack) or line.startswith("."):
            continue
        parts = line.split(None, 1)
        sub = expand(macros, parts[0], split_args(parts[1]) if len(parts) > 1 else [], resolve, depth + 1)
        if sub:
            out.extend(sub)
    return out


# ---------------------------------------------------------------- scripts
class Node:
    """One primitive command, or one line of data."""
    __slots__ = ("idx", "line", "kind", "cmd", "args", "source", "labels")

    def __init__(self, idx, line, kind, cmd=None, args=None, source=None):
        self.idx = idx
        self.line = line
        self.kind = kind            # "cmd", "data" or "move"
        self.cmd = cmd
        self.args = args or {}
        self.source = source        # the macro the line was written with
        self.labels = []


class Script:
    """One script file, flattened to primitive commands, with its control flow."""

    def __init__(self, stem, text, macros, consts):
        self.stem = stem
        self.entries = []           # label per script number - 1
        self.nodes = []
        self.labels = {}            # label -> node index
        self.label_line = {}
        self.defines = {}
        self.init = []              # (kind, script id or None, label or None, var, value)
        self.undecoded = collections.Counter()
        self.parse(text, macros, consts)
        self.flow()

    def parse(self, text, macros, consts):
        lines = strip_preprocessor(text or "")
        pending = []
        resolve = Resolver(consts, self.defines)
        for lineno, raw in enumerate(lines, 1):
            line = re.sub(r"(^|\s)@.*$", "", raw).strip()
            if not line:
                continue
            m = re.match(r"#\s*define\s+(\w+)\s+(.+)$", line)
            if m:
                self.defines[m.group(1)] = m.group(2).strip()
                continue
            if line.startswith("#"):
                continue
            m = re.match(r"^(\w+):\s*(.*)$", line)
            if m:
                pending.append(m.group(1))
                self.label_line[m.group(1)] = lineno
                line = m.group(2).strip()
                if not line:
                    continue
            parts = line.split(None, 1)
            head, rest = parts[0], (parts[1] if len(parts) > 1 else "")
            args = split_args(rest)
            if head == "ScriptEntry":
                self.entries.append(args[0])
                continue
            if head.startswith("InitScript"):
                self._init_line(head, args, lineno, resolve)
                pending = []
                continue
            if head in ("ScriptEntryEnd",) or head in (".balign", ".align", ".global", ".set", ".section"):
                continue
            new = []
            if head in (".byte", ".short", ".long", ".word", ".hword", ".4byte", ".2byte"):
                new.append(Node(0, lineno, "data", head, {"raw": rest}))
                self.undecoded["raw data lines"] += 1
            elif head in macros:
                prims = expand(macros, head, args, resolve)
                for cmd, values in prims or []:
                    new.append(Node(0, lineno, "cmd", cmd, values, head))
                    if cmd.startswith("ScrCmd_"):
                        self.undecoded["commands with no name"] += 1
            else:
                new.append(Node(0, lineno, "move", head))
            if not new:
                continue
            for n in new:
                n.idx = len(self.nodes)
                self.nodes.append(n)
            for lab in pending:
                self.labels[lab] = new[0].idx
            new[0].labels = pending
            pending = []
        for lab in pending:
            self.labels[lab] = len(self.nodes)

    def _init_line(self, head, args, lineno, resolve):
        """An init script line: (kind, script id, variable, value, line)."""
        if head in ("InitScriptEntry_OnTransition", "InitScriptEntry_OnResume", "InitScriptEntry_OnLoad"):
            self.init.append((head[len("InitScriptEntry_"):], resolve(args[0]), None, None, lineno))
        elif head == "InitScriptEntry_Fixed":
            self.init.append(("Fixed", resolve(args[1]), None, None, lineno))
        elif head == "InitScriptGoToIfEqual":
            self.init.append(("FrameTable", resolve(args[2]), resolve(args[0]), resolve(args[1]), lineno))

    # ---- control flow
    def target(self, node, param="offset"):
        return self.labels.get(node.args.get(param, "").strip())

    def flow(self):
        n = len(self.nodes)
        self.succ = [[] for _ in range(n)]
        self.calls = [None] * n         # call target of a Call/CallIf node
        self.cond = [None] * n          # (compare node, condition) of a GoToIf/CallIf
        for node in self.nodes:
            i = node.idx
            nxt = i + 1 if i + 1 < n and self.nodes[i + 1].kind == "cmd" else None
            if node.kind != "cmd":
                continue
            c = node.cmd
            if c == "GoTo":
                t = self.target(node)
                self.succ[i] = [t] if t is not None else []
            elif c in ("GoToIf", "ScrCmd_Unused_017", "ScrCmd_Unused_018", "ScrCmd_Unused_019"):
                t = self.target(node, "offset" if c == "GoToIf" else "arg1")
                self.succ[i] = [x for x in (t, nxt) if x is not None]
                self.cond[i] = self._condition(i)
            elif c == "GoToIfTargetTrainerDefeated":
                t = self.target(node)
                self.succ[i] = [x for x in (t, nxt) if x is not None]
            elif c in ("Call", "CallIf"):
                self.calls[i] = self.target(node)
                self.succ[i] = [nxt] if nxt is not None else []
                if c == "CallIf":
                    self.cond[i] = self._condition(i)
            elif c in ("End", "Return", "ReturnCommonScript"):
                self.succ[i] = []
            else:
                self.succ[i] = [nxt] if nxt is not None else []
        self.pred = [[] for _ in range(n)]
        for i, ss in enumerate(self.succ):
            for s in ss:
                self.pred[s].append(i)
        self.callers = collections.defaultdict(list)
        for i, t in enumerate(self.calls):
            if t is not None:
                self.callers[t].append(i)
        self._returns = {}

    def _condition(self, i):
        node = self.nodes[i]
        code = node.args.get("condition", "").strip()
        try:
            op = CONDITIONS.get(int(code, 0))
        except ValueError:
            op = None
        j = i - 1
        if j >= 0 and self.nodes[j].kind == "cmd":
            return (j, op)
        return (None, op)

    def returns_of(self, start):
        """The Return nodes a call to `start` can come back from."""
        if start in self._returns:
            return self._returns[start]
        seen, out, todo = set(), [], [start]
        while todo:
            i = todo.pop()
            if i in seen or i is None or i >= len(self.nodes):
                continue
            seen.add(i)
            if self.nodes[i].cmd == "Return":
                out.append(i)
            todo.extend(self.succ[i])
        self._returns[start] = out
        return out

    def reach(self, roots):
        """Every node reachable from the given node indices."""
        seen, todo = set(), [r for r in roots if r is not None]
        while todo:
            i = todo.pop()
            if i in seen or i >= len(self.nodes):
                continue
            seen.add(i)
            todo.extend(self.succ[i])
            if self.calls[i] is not None:
                todo.append(self.calls[i])
        return seen

    def entry_node(self, number):
        """The node a script number (1-based) starts at."""
        if 1 <= number <= len(self.entries):
            return self.labels.get(self.entries[number - 1])
        return None


# ---------------------------------------------------------------- tracing
def is_write(param):
    return "dest" in param.lower() or param in WRITE_PARAMS


def trace(script, start, var, resolve, depth=0, limit=64):
    """Where the variable `var` read at node `start` got its value.

    Walks the control flow backwards: from a command that follows a `Call`
    into the callee's `Return`s, and from the top of a callee back out to the
    call that entered it (or, when the walk began inside the callee, to every
    call of it). Returns [(what, conditions, node)]: what is ("value", n),
    ("from", command) or ("elsewhere", None); conditions are the branch tests
    passed between the setting and the reading; node is the index of the
    setting command, or None."""
    results = []
    seen = set()
    # breadth first, so each setting is reached by its shortest path and
    # carries only the branch tests that path passes
    todo = collections.deque([(start, (), (), True)])
    steps = 0
    while todo and len(results) < limit and steps < 20000:
        steps += 1
        i, stack, conds, skip = todo.popleft()
        key = (i, stack)
        if key in seen and not skip:
            continue
        seen.add(key)
        node = script.nodes[i]
        if not skip and node.kind == "cmd":
            hit = _defines(script, node, var, resolve, conds, depth)
            if hit is not None:
                results.extend(hit)
                continue
        moved = False
        for p in script.pred[i]:
            if script.calls[p] is not None and p + 1 == i:
                for r in script.returns_of(script.calls[p]):
                    todo.append((r, stack + (p,), conds + _cond(script, p, True), False))
                if script.nodes[p].cmd == "CallIf":
                    todo.append((p, stack, conds + _cond(script, p, False), False))
                moved = True
                continue
            c = ()
            if script.cond[p] is not None:
                taken = i != p + 1 or len(script.succ[p]) == 1
                c = _cond(script, p, taken)
            todo.append((p, stack, conds + c, False))
            moved = True
        if i in script.callers:
            if stack:
                if script.calls[stack[-1]] == i:
                    todo.append((stack[-1], stack[:-1], conds, False))
                    moved = True
            else:
                for c in script.callers[i]:
                    todo.append((c, stack, conds, False))
                    moved = True
        if not moved:
            results.append((("elsewhere", None), conds, None))
    out, keys = [], set()
    for what, conds, at in results:
        k = (what, tuple(c[:3] for c in conds))
        if k not in keys:
            keys.add(k)
            out.append((what, conds, at))
    return out


def entering_condition(script, d):
    """The branch test whose jump leads into the straight run of code
    holding node d, or () when it is reached unconditionally. Falling through
    a failed test is the "otherwise" case: the walk goes on past it."""
    i, steps = d, 0
    while steps < 64:
        steps += 1
        preds = script.pred[i]
        for p in preds:
            if script.cond[p] is not None and script.nodes[p].cmd == "GoToIf" and i != p + 1:
                return _cond(script, p, True)
        if len(preds) != 1 or i in script.callers:
            return ()
        i = preds[0]
    return ()


def _cond(script, p, taken):
    if script.cond[p] is None:
        return ()
    j, op = script.cond[p]
    if j is None or op is None:
        return ()
    cmp = script.nodes[j]
    if not taken:
        op = NEGATED[op]
    if cmp.cmd in ("CompareVarToValue", "CompareVarToVar"):
        a = cmp.args.get("varID") or cmp.args.get("varID1")
        b = cmp.args.get("value") or cmp.args.get("varID2")
        return ((a, op, b, j),)
    if cmp.cmd in ("CheckFlag", "CheckTrainerFlag"):
        what = cmp.args.get("flagID") or cmp.args.get("trainerID")
        kind = "flag" if cmp.cmd == "CheckFlag" else "trainer"
        return ((what, "is", ("set" if op == "==" else "unset", kind), j),)
    return ((cmp.cmd, "after", op, j),)


def _defines(script, node, var, resolve, conds, depth):
    """None if node does not write var; else what it writes."""
    c, a = node.cmd, node.args
    if c == "SetVarFromValue" and resolve(a.get("destVarID", "")) == var:
        v = resolve(a.get("value", ""))
        return [(("value", v) if v is not None else ("from", "an unreadable value"), conds, node.idx)]
    if c == "SetVarFromVar" and resolve(a.get("destVarID", "")) == var:
        src = resolve(a.get("srcVarID", ""))
        if src is None or depth > 4:
            return [(("from", "SetVarFromVar"), conds, node.idx)]
        return [(w, c2 + conds, at if at is not None else node.idx)
                for w, c2, at in trace(script, node.idx, src, resolve, depth + 1)]
    if c in ("AddVar", "SubVar") and resolve(a.get("destVarID", "")) == var:
        return [(("from", c), conds, node.idx)]
    for p, text in a.items():
        if is_write(p) and resolve(text) == var:
            return [(("from", c), conds, node.idx)]
    return None


# ---------------------------------------------------------------- the index of one tree
class Index:
    """Everything the tool reads from one tree: `oxide` or `main`."""

    def __init__(self, tree):
        self.tree = tree
        self.consts = Consts(tree)
        self.macros = load_macros(tree)
        names = [f for f in tree.listdir(SCRIPTS_DIR) if f.endswith(".s")]
        evnames = [f for f in tree.listdir(EVENTS_DIR) if f.endswith(".json")]
        tree.prefetch([f"{SCRIPTS_DIR}/{f}" for f in names] + [f"{EVENTS_DIR}/{f}" for f in evnames])
        self.scripts = {}
        for f in names:
            self.scripts[f[:-2]] = Script(f[:-2], tree.read(f"{SCRIPTS_DIR}/{f}"), self.macros, self.consts)
        self.events = {}
        self.event_text = {}
        for f in evnames:
            text = tree.read(f"{EVENTS_DIR}/{f}")
            try:
                self.events[f[:-5]] = json.loads(text)
            except (TypeError, ValueError):
                continue
            self.event_text[f[:-5]] = text
        self.headers = self._headers()
        self.chunks = self._chunks()
        self.stores = self._stores()
        self.hidden = self._hidden_items()
        self.daily_hidden = self._daily_hidden()
        self.visible = self._visible_items()
        self.trades = self._trades()

    def resolver(self, script):
        return Resolver(self.consts, script.defines)

    def _headers(self):
        text = self.tree.read(HEADERS) or ""
        out = collections.OrderedDict()
        for h, body in re.findall(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \},", text, re.S):
            def field(n):
                m = re.search(r"\.%s = (\w+)" % n, body)
                return m.group(1) if m else None
            out[h] = {"scripts": field("scriptsArchiveID"), "init": field("initScriptsArchiveID"),
                      "events": field("eventsArchiveID"), "encounters": field("wildEncountersArchiveID"),
                      "label": field("mapLabelTextID")}
        return out

    def _chunks(self):
        """[(first script id, file)] for the shared script files, highest first."""
        offsets = c_enum(self.tree.read(SCRIPT_MANAGER_H))
        text = self.tree.read(SCRIPT_MANAGER_C) or ""
        out = []
        for off, stem in re.findall(r"Entry\((SCRIPT_ID_OFFSET_\w+),\s*(scripts_\w+),", text):
            if off in offsets:
                out.append((offsets[off], stem))
        return sorted(out, reverse=True)

    def chunk_of(self, script_id):
        for start, stem in self.chunks:
            if script_id >= start:
                return start, stem
        return None

    def _stores(self):
        """saved variable -> {script file: constants it stores there}."""
        out = collections.defaultdict(lambda: collections.defaultdict(set))
        for stem, script in self.scripts.items():
            resolve = self.resolver(script)
            for n in script.nodes:
                if n.kind == "cmd" and n.cmd == "SetVarFromValue":
                    var = resolve(n.args.get("destVarID", ""))
                    val = resolve(n.args.get("value", ""))
                    if var is not None and VARS_START <= var < TEMP_VARS_START and val is not None:
                        out[var][stem].add(val)
        return out

    def _hidden_items(self):
        """hidden item flag -> (item, quantity, line)."""
        out = {}
        text = self.tree.read(HIDDEN_ITEMS) or ""
        resolve = Resolver(self.consts)
        for lineno, line in enumerate(text.splitlines(), 1):
            m = re.search(r"HIDDEN_ITEM_ENTRY\((\w+),\s*(\d+),\s*(\d+),\s*(\w+)\)", line)
            if m:
                out[resolve(m.group(4))] = (resolve(m.group(1)), int(m.group(2)), lineno)
        return out

    def _daily_hidden(self):
        """Hidden item flags the engine clears every day (Iron Island's star
        pieces and Floaroma Meadow's honey, src/script_manager.c)."""
        text = self.tree.read(SCRIPT_MANAGER_C) or ""
        out = set()
        for body in re.findall(r"static u16 s\w*HiddenItemFlags\[\][^=]*=\s*\{(.*?)\};", text, re.S):
            for name in re.findall(r"(FLAG_OBTAINED_HIDDEN_\w+)", body):
                if name in self.consts.values:
                    out.add(self.consts.values[name])
        return out

    def _visible_items(self):
        """item ball number -> (item, count)."""
        script = self.scripts.get("scripts_visible_items")
        out = {}
        if script is None:
            return out
        resolve = self.resolver(script)
        for n in range(1, len(script.entries) + 1):
            i = script.entry_node(n)
            item = count = None
            while i is not None and i < len(script.nodes) and script.nodes[i].kind == "cmd":
                node = script.nodes[i]
                if node.cmd == "SetVarFromValue":
                    dest = resolve(node.args.get("destVarID", ""))
                    if dest == 0x8008:
                        item = resolve(node.args.get("value", ""))
                    elif dest == 0x8009:
                        count = resolve(node.args.get("value", ""))
                if not script.succ[i] or node.cmd == "GoTo":
                    break
                i = script.succ[i][0]
            out[n - 1] = (item, count)
        return out

    def _trades(self):
        out = {}
        for name, value in self.consts.npc_trades.items():
            if not name.startswith("NPC_TRADE_") or name.endswith("COUNT") or name.endswith("MAX"):
                continue
            path = f"{NPC_TRADES_DIR}/{name[len('NPC_TRADE_'):].lower()}.json"
            text = self.tree.read(path)
            if text:
                d = json.loads(text)
                out[value] = {"id": name, "species": d.get("species"), "requested": d.get("requestedSpecies"),
                              "item": d.get("heldItem"), "nickname_giver": d.get("name")}
        return out

    # ---- which scripts start where
    def roots(self, header):
        """[(script number, how)] for everything the header starts in its own
        script file: its events and its init scripts."""
        h = self.headers[header]
        out = []
        ev = self.events.get(h["events"]) or {}
        for kind in ("object_events", "bg_events", "coord_events"):
            for k, e in enumerate(ev.get(kind, [])):
                s = e.get("script")
                if isinstance(s, int) and 0 < s < 2000:
                    out.append((s, kind))
        init = self.scripts.get(h["init"])
        if init is not None:
            for kind, sid, _, _, _ in init.init:
                if sid is not None and 0 < sid < 2000:
                    out.append((sid, "init"))
        return out


# ---------------------------------------------------------------- extraction
def fmt_value(consts, kind, value):
    if value is None:
        return "?"
    name = consts.name(kind, value) if kind else None
    return name or str(value)


LITERAL = re.compile(r"^-?(0x[0-9a-fA-F]+|\d+)$")

# The kind of value a compared variable holds, by the command that set it.
SOURCE_KINDS = {"GetPlayerStarterSpecies": "species", "GetPartyMonSpecies": "species",
                "GetSelectedItem": "item", "GetNPCTradeSpecies": "species"}


class Extractor:
    """Reads operands of one script file: names, numbers and traced variables."""

    def __init__(self, index, script):
        self.index = index
        self.consts = index.consts
        self.script = script
        self.resolve = index.resolver(script)

    def operand(self, node, param, kind, skip_zero=False):
        """(values, mode, lines, elsewhere, unreadable). values is a list of
        {"value", "name", "when"}; mode is how the script gives it: "name",
        "number" or "variable"; lines are the lines it rests on."""
        text = (node.args.get(param) or "0").strip()
        v = self.resolve(text)
        if v is None:
            return [], "unreadable", [], 0, 1
        if v < VARS_START:
            if skip_zero and v == 0:
                return [], "none", [], 0, 0
            mode = "number" if LITERAL.match(text) else "name"
            unread = 1 if kind and self.consts.name(kind, v) is None else 0
            return [{"value": v, "name": fmt_value(self.consts, kind, v), "when": ""}], mode, [], 0, unread
        values, lines, elsewhere = self.trace_var(node, v, kind)
        return values, "variable", lines, elsewhere, 0

    def trace_var(self, node, var, kind):
        found = trace(self.script, node.idx, var, self.resolve)
        # Only the tests that tell the values apart are worth saying: drop
        # those every path passes, and when a value has none left, name the
        # branch that leads into the code that sets it.
        sets = [{c[:3] for c in conds} for _, conds, _ in found]
        common = set.intersection(*sets) if len(sets) > 1 else set()
        distinct = len({w for w, _, _ in found}) > 1
        out, lines, elsewhere = [], set(), 0
        found_keep = []
        for what, conds, at in found:
            keep, seen = [], set()
            if distinct:
                for c in conds:
                    if c[:3] not in common and c[:3] not in seen:
                        seen.add(c[:3])
                        keep.append(c)
                if not keep and at is not None:
                    keep = list(entering_condition(self.script, at))
                # a test that names the value ("== 2") says more than the
                # ones it passed on the way ("!= 0", "!= 1")
                if any(c[1] == "==" for c in keep):
                    keep = [c for c in keep if c[1] != "!="]
            found_keep.append((what, keep, at))
        # two values the tests still cannot tell apart get the test that
        # enters each one's code (Lucas's or Dawn's team, by gender)
        whens = collections.Counter(tuple(c[:3] for c in keep) for _, keep, _ in found_keep)
        for what, keep, at in found_keep:
            if distinct and at is not None and whens[tuple(c[:3] for c in keep)] > 1:
                extra = entering_condition(self.script, at)
                if extra and extra[0][:3] not in {c[:3] for c in keep}:
                    keep.append(extra[0])
            when = self.describe(keep[:3])
            by = sorted({self.describe([c]).split(" ")[0] for c in keep if c[1] not in ("is", "after")})
            if what[0] == "value":
                out.append({"value": what[1], "name": fmt_value(self.consts, kind, what[1]), "when": when, "by": by})
            elif what[0] == "from":
                out.append({"value": None, "name": f"set by {what[1]}", "when": when, "by": by})
            else:
                # the note on who else stores the variable is for the reader;
                # matching with main goes by "set elsewhere" alone
                out.append({"value": None, "name": "set elsewhere" + self.set_elsewhere(var, kind),
                            "match": "set elsewhere", "when": when, "by": by})
                elsewhere += 1
            if at is not None:
                lines.add(self.script.nodes[at].line)
        merged = collections.OrderedDict()
        for v in out:
            k = (v["value"], v["name"])
            if k in merged:
                if merged[k]["when"] and v["when"] and v["when"] not in merged[k]["when"].split(" or "):
                    merged[k]["when"] += " or " + v["when"]
                elif not v["when"]:
                    merged[k]["when"] = ""
                merged[k]["by"] = sorted(set(merged[k]["by"]) | set(v["by"]))
            else:
                merged[k] = dict(v)
        out = list(merged.values())
        out.sort(key=lambda d: (d["when"] == "", d["value"] is None, str(d["value"])))
        return out, sorted(lines), elsewhere

    def set_elsewhere(self, var, kind):
        if var >= TEMP_VARS_START:
            return ""
        stores = self.index.stores.get(var, {})
        if self.consts.is_map_local_var(var):
            # every map has its own, so only this file's stores are the same variable
            stores = {k: v for k, v in stores.items() if k == self.script.stem}
        parts = []
        for stem in sorted(stores, key=lambda s: (s != self.script.stem, s)):
            vals = sorted(stores[stem])
            who = "this map's script" if stem == self.script.stem else stem
            parts.append(f"{who} stores " + ", ".join(fmt_value(self.consts, kind, x) for x in vals))
        return f" ({'; '.join(parts)})" if parts else ""

    def describe(self, conds):
        out = []
        for a, op, b, j in conds:
            if op == "is":
                v = self.resolve(a)
                state, kind = b
                if kind == "trainer":
                    name = "defeated " + fmt_value(self.consts, "trainer", v) if v is not None else a
                    out.append(f"{name} {'yes' if state == 'set' else 'no'}")
                else:
                    name = fmt_value(self.consts, "flag", v) if v is not None else a
                    out.append(f"{name} {state}")
                continue
            if op == "after":
                continue
            va, vb = self.resolve(a), self.resolve(b)
            left = fmt_value(self.consts, "var", va) if va is not None else a
            src = self.var_source(j, va)
            kind = SOURCE_KINDS.get(src)
            if vb is not None and vb >= VARS_START:
                right = fmt_value(self.consts, "var", vb)
            else:
                right = fmt_value(self.consts, kind, vb) if vb is not None else b
            label = f"{left} ({src})" if src else left
            out.append(f"{label} {op} {right}")
        return "; ".join(out)

    def var_source(self, j, var):
        """The command that set a compared temporary variable, if one did."""
        if var is None or var < TEMP_VARS_START:
            return None
        for what, _, _ in trace(self.script, j, var, self.resolve, depth=3, limit=4):
            if what[0] == "from":
                return what[1]
        return None


def keyof(values):
    return tuple(sorted(str(v["value"]) if v["value"] is not None else v.get("match", v["name"]) for v in values))


def extract_script(index, script):
    """Every entry in one script file: {kind: [entry]}, each tagged with the
    node it sits at so a map can take only the part it reaches."""
    ex = Extractor(index, script)
    consts = index.consts
    out = collections.defaultdict(list)
    und = collections.Counter(script.undecoded)

    def add(kind, node, lines, key, **fields):
        out[kind].append(dict(fields, file=script.stem, line=node.line, node=node.idx,
                              command=node.source, lines=sorted(set([node.line] + list(lines))), key=key))

    def read(node, param, kind, skip_zero=False):
        values, mode, lines, elsewhere, unread = ex.operand(node, param, kind, skip_zero)
        und["variables set elsewhere"] += elsewhere
        und["numbers no table holds"] += unread
        return values, mode, lines

    skip_items = script.stem in ("scripts_visible_items", "scripts_hidden_items")
    for node in script.nodes:
        if node.kind != "cmd":
            continue
        c, a = node.cmd, node.args
        if c in TRAINER_CMDS:
            slots, lines = [], []
            for p in TRAINER_CMDS[c]:
                vals, mode, ls = read(node, p, "trainer", skip_zero=True)
                if vals:
                    slots.append({"role": p, "mode": mode, "values": vals})
                    lines += ls
            add("trainers", node, lines, ("trainer", c) + tuple(keyof(s["values"]) for s in slots),
                how=c, slots=slots)
        elif c in STATIC_CMDS:
            sp, mode, l1 = read(node, "species", "species")
            lv, _, l2 = read(node, "level", None)
            add("statics", node, l1 + l2, ("static", c, keyof(sp), keyof(lv)), how=c, species=sp, level=lv, mode=mode)
        elif c == "StartHoneyTreeBattle":
            add("statics", node, [], ("static", c), how=c, mode="engine", level=[],
                species=[{"value": None, "name": "the honey tree's Pokemon", "when": ""}])
        elif c in GIFT_CMDS:
            sp, mode, l1 = read(node, "species", "species")
            lv, _, l2 = read(node, "level", None)
            it, _, l3 = read(node, "heldItem", "item", skip_zero=True)
            add("pokemon", node, l1 + l2 + l3, ("gift", keyof(sp), keyof(lv), keyof(it)),
                how=c, species=sp, level=lv, item=it, mode=mode)
        elif c == "GiveEgg":
            sp, mode, l1 = read(node, "species", "species")
            add("eggs", node, l1, ("egg", keyof(sp)), species=sp, mode=mode)
        elif c == "InitNPCTrade":
            v = ex.resolve(a.get("npcTradeID", ""))
            t = index.trades.get(v, {})
            add("trades", node, [], ("trade", v), trade=fmt_value(consts, "trade", v),
                offers=t.get("species"), wants=t.get("requested"), item=t.get("item"))
        elif not skip_items and (c == "AddItem" or (
                c == "CallCommonScript" and ex.resolve(a.get("scriptID", "")) in GIVE_ITEM_COMMON)):
            if c == "AddItem":
                it, mode, l1 = read(node, "item", "item")
                ct, _, l2 = read(node, "count", None)
            else:
                it, l1, e1 = ex.trace_var(node, VAR_ITEM, "item")
                ct, l2, e2 = ex.trace_var(node, VAR_COUNT, None)
                und["variables set elsewhere"] += e1 + e2
                mode = "variable"
            add("items", node, l1 + l2, ("item", keyof(it), keyof(ct)), item=it, count=ct, mode=mode,
                how="AddItem" if c == "AddItem" else "Common_GiveItemQuantity")
        # flags and saved variables
        for p, text in a.items():
            if c in ("SetFlag", "ClearFlag", "CheckFlag", "CheckFlagFromVar") and p == "flagID":
                v = ex.resolve(text)
                if v is None:
                    und["numbers no table holds"] += 1
                    continue
                op = {"SetFlag": "set", "ClearFlag": "clear"}.get(c, "check")
                add("flags", node, [], ("flag", op, v), flag=v, op=op)
            elif c in ("SetTrainerFlag", "ClearTrainerFlag", "CheckTrainerFlag") and p == "trainerID":
                v = ex.resolve(text)
                if v is None or v >= VARS_START:
                    continue
                op = {"SetTrainerFlag": "set", "ClearTrainerFlag": "clear"}.get(c, "check")
                f = consts.trainer_flags_start + v
                add("flags", node, [], ("flag", op, f), flag=f, op=op)
            else:
                v = ex.resolve(text)
                if v is None or not (VARS_START <= v < TEMP_VARS_START):
                    continue
                write = (c in ("SetVarFromValue", "SetVarFromVar", "AddVar", "SubVar") and p == "destVarID") \
                    or is_write(p)
                op = "set" if write else "check"
                add("vars", node, [], ("var", op, v), var=v, op=op)
    return out, und


def event_entries(index, header):
    """Entries a map's event file makes on its own: trainers who see the
    player, item balls, hidden items, and the flags that hide objects and
    the variables that arm coordinate triggers."""
    consts = index.consts
    h = index.headers[header]
    stem = h["events"]
    ev = index.events.get(stem)
    out = collections.defaultdict(list)
    if not ev:
        return out
    lines = script_lines(index.event_text.get(stem, ""))
    resolve = Resolver(consts)
    for kind in ("object_events", "bg_events", "coord_events"):
        for k, e in enumerate(ev.get(kind, [])):
            where = lines.get((kind, k), {})
            block = sorted(where.values())
            base = {"file": stem, "line": where.get("script"), "event": kind, "number": k}
            s = e.get("script")
            sid = resolve(s) if isinstance(s, str) else s
            if isinstance(s, str) and s.startswith("TRAINER_"):
                sid = resolve(s) - 1 + (DOUBLE_BATTLES[0] if e.get("double_battle_id") == 2 else SINGLE_BATTLES[0])
            flag = e.get("hidden_flag")
            fv = resolve(flag) if isinstance(flag, str) else flag
            if kind == "object_events" and sid is not None and SINGLE_BATTLES[0] <= sid < DOUBLE_BATTLES[1]:
                first = SINGLE_BATTLES[0] if sid < DOUBLE_BATTLES[0] else DOUBLE_BATTLES[0]
                tid = sid - first + 1
                how = "sees the player" if first == SINGLE_BATTLES[0] else "sees the player, double battle"
                out["trainers"].append(dict(base, how=how, lines=block, key=("trainer", "event", (str(tid),)),
                                            slots=[{"role": "event", "mode": "event",
                                                    "values": [{"value": tid, "name": fmt_value(consts, "trainer", tid), "when": ""}]}]))
            elif kind == "object_events" and sid is not None and VISIBLE_ITEMS[0] <= sid < VISIBLE_ITEMS[1]:
                item, count = index.visible.get(sid - VISIBLE_ITEMS[0], (None, None))
                out["item_balls"].append(dict(base, item=fmt_value(consts, "item", item), item_id=item, count=count,
                                              flag=fv, flag_name=fmt_value(consts, "flag", fv) if fv else None,
                                              daily=bool(fv) and consts.is_daily(fv), lines=block,
                                              key=("ball", item, count, fv)))
            elif kind == "bg_events" and sid is not None and HIDDEN_ITEMS_RANGE[0] <= sid < HIDDEN_ITEMS_RANGE[1]:
                f = sid - HIDDEN_ITEMS_RANGE[0] + consts.hidden_flags_start
                item, qty, hline = index.hidden.get(f, (None, None, None))
                out["hidden_items"].append(dict(base, item=fmt_value(consts, "item", item), item_id=item, count=qty,
                                                flag=f, flag_name=fmt_value(consts, "flag", f),
                                                daily=f in index.daily_hidden, lines=block,
                                                also=[(HIDDEN_ITEMS, hline)] if hline else [],
                                                key=("hidden", item, qty, f)))
            if kind == "object_events" and fv:
                out["flags"].append(dict(base, line=where.get("hidden_flag"), lines=[where.get("hidden_flag")],
                                         flag=fv, op="hides", key=("flag", "hides", fv)))
            if kind == "coord_events" and e.get("var"):
                v = resolve(e["var"]) if isinstance(e["var"], str) else e["var"]
                if v is not None and VARS_START <= v < TEMP_VARS_START:
                    out["vars"].append(dict(base, line=where.get("var"), lines=[where.get("var")],
                                            var=v, op="check", key=("var", "check", v)))
    return out


def script_lines(text):
    """{(event kind, number): {field: line}} for an event file, which keeps
    one field per line."""
    out = {}
    kind, count, cur = None, collections.Counter(), None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = re.match(r'\s*"(\w+_events)"\s*:', line)
        if m:
            kind = m.group(1)
            continue
        if kind and re.match(r"\s*\{\s*$", line):
            cur = (kind, count[kind])
            count[kind] += 1
            out[cur] = {}
            continue
        m = re.match(r'\s*"(\w+)"\s*:', line)
        if m and cur is not None:
            out[cur].setdefault(m.group(1), lineno)
        if re.match(r"\s*\}", line):
            cur = None
    return out


# ---------------------------------------------------------------- maps
class Maps:
    """Per map header: the entries its scripts and events make."""

    def __init__(self, index):
        self.index = index
        self._extracted = {}
        self.users = collections.defaultdict(list)
        for h, d in index.headers.items():
            self.users[d["scripts"]].append(h)
        self.chunk_stems = {stem for _, stem in index.chunks}

    def extracted(self, stem):
        if stem not in self._extracted:
            script = self.index.scripts.get(stem)
            self._extracted[stem] = extract_script(self.index, script) if script else ({}, collections.Counter())
        return self._extracted[stem]

    def roots(self, header):
        h = self.index.headers[header]
        script = self.index.scripts.get(h["scripts"])
        if script is None:
            return None, set()
        nodes = [script.entry_node(n) for n, _ in self.index.roots(header)]
        return script, script.reach(nodes)

    def view(self, header):
        """{kind: [entry]}, unreached scripts, undecoded counts, for one header."""
        index = self.index
        h = index.headers[header]
        stem = h["scripts"]
        shared = len(self.users[stem]) > 1
        script, reached = self.roots(header)
        out = collections.defaultdict(list)
        undecoded = collections.Counter()
        unreached = []
        if script is not None:
            entries, und = self.extracted(stem)
            for kind, items in entries.items():
                for e in items:
                    if shared and e["node"] not in reached:
                        continue
                    out[kind].append(dict(e, reached=e["node"] in reached))
            if not shared:
                undecoded.update(und)
                unreached = unreached_scripts(script, reached)
                engine = engine_starter(stem)
                if engine:
                    for u in unreached:
                        if u["number"]:
                            u["engine"] = engine
        for kind, items in event_entries(index, header).items():
            for e in items:
                out[kind].append(dict(e, reached=True))
        missing = []
        if script is not None and not shared:
            count = len(script.entries)
            ev = index.events.get(h["events"]) or {}
            lines = script_lines(index.event_text.get(h["events"], ""))
            for kind in ("object_events", "bg_events", "coord_events"):
                for k, e in enumerate(ev.get(kind, [])):
                    sid = e.get("script")
                    if isinstance(sid, int) and count < sid < 2000:
                        missing.append({"file": h["events"], "line": lines.get((kind, k), {}).get("script"),
                                        "event": kind, "id": e.get("id"), "script": sid, "has": count})
            init_file = index.scripts.get(h["init"])
            for kind, sid, _, _, line in (init_file.init if init_file else []):
                if sid is not None and count < sid < 2000:
                    missing.append({"file": h["init"], "line": line, "event": "init script", "id": kind,
                                    "script": sid, "has": count})
        init = index.scripts.get(h["init"])
        if init is not None:
            for kind, sid, var, value, line in init.init:
                if var is not None and VARS_START <= var < TEMP_VARS_START:
                    out["vars"].append({"file": h["init"], "line": line, "lines": [line], "var": var, "op": "check",
                                        "reached": True, "key": ("var", "check", var)})
        return out, unreached, undecoded, missing

    def file_view(self, stem, refs):
        """The same for a script file no single header owns: a shared file
        (reached from the script ids in refs, 0-based) or an unused one."""
        index = self.index
        script = index.scripts[stem]
        nodes = [script.labels.get(script.entries[n]) for n in refs if 0 <= n < len(script.entries)]
        if stem in self.users:
            for header in self.users[stem]:
                nodes += [script.entry_node(n) for n, _ in index.roots(header)]
        reached = script.reach(nodes)
        entries, und = self.extracted(stem)
        out = collections.defaultdict(list)
        table = stem in TABLE_FILES
        for kind, items in entries.items():
            for e in items:
                out[kind].append(dict(e, reached=table or e["node"] in reached))
        unreached = [] if table else unreached_scripts(script, reached)
        return out, unreached, collections.Counter(und)


def engine_starter(stem):
    for prefix, where in ENGINE_STARTED.items():
        if stem.startswith(prefix):
            return where
    return None


def unreached_scripts(script, reached):
    """[{"number", "label", "line"}] for script entries nothing reaches, then
    the heads of code nothing reaches at all."""
    out = []
    entry_nodes = []
    for n, label in enumerate(script.entries, 1):
        i = script.labels.get(label)
        if i is None or i in reached:
            continue
        entry_nodes.append(i)
        out.append({"number": n, "label": label, "line": script.label_line.get(label)})
    covered = set(reached) | script.reach(entry_nodes)
    for label, i in sorted(script.labels.items(), key=lambda kv: kv[1]):
        if i >= len(script.nodes) or i in covered or script.nodes[i].kind != "cmd":
            continue
        out.append({"number": None, "label": label, "line": script.label_line.get(label)})
        covered |= script.reach([i])
    return out


def chunk_refs(index):
    """{shared script file: {0-based entry}} for every script id any event,
    init script, CallCommonScript or SCRIPT_ID() in src/ names."""
    refs = collections.defaultdict(set)

    def add(sid):
        hit = index.chunk_of(sid) if sid is not None and sid >= 2000 else None
        if hit:
            refs[hit[1]].add(sid - hit[0])
    for ev in index.events.values():
        for kind in ("object_events", "bg_events", "coord_events"):
            for e in ev.get(kind, []):
                s = e.get("script")
                if isinstance(s, str) and s.startswith("TRAINER_") and s in index.consts.values:
                    first = DOUBLE_BATTLES[0] if e.get("double_battle_id") == 2 else SINGLE_BATTLES[0]
                    s = index.consts.values[s] - 1 + first
                if isinstance(s, int):
                    add(s)
    for script in index.scripts.values():
        resolve = index.resolver(script)
        for kind, sid, _, _, _ in script.init:
            add(sid)
        for n in script.nodes:
            if n.kind == "cmd" and n.cmd == "CallCommonScript":
                add(resolve(n.args.get("scriptID", "")))
    offsets = c_enum(index.tree.read(SCRIPT_MANAGER_H))
    for root, _, files in os.walk(os.path.join(ROOT, "src")) if index.tree.ref is None else []:
        for f in files:
            if not f.endswith(".c"):
                continue
            text = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for chunk, n in re.findall(r"SCRIPT_ID\((\w+),\s*(\d+)\)", text):
                off = offsets.get("SCRIPT_ID_OFFSET_" + chunk)
                if off is not None:
                    add(off + int(n))
    return refs


# ---------------------------------------------------------------- vanilla and history
IDENTITY = {
    "item_balls": lambda e: ("ball", e.get("flag")),
    "hidden_items": lambda e: ("hidden", e.get("flag")),
    "statics": lambda e: ("static", e.get("how"), keyof(e.get("species") or [])),
    "pokemon": lambda e: ("gift", keyof(e.get("species") or [])),
}


def compare(ours, theirs):
    """Mark each of our entries vanilla or added against theirs (the same
    map on main); return the entries of theirs we no longer have."""
    removed = {}
    for kind, _ in KINDS:
        if kind in ("flags", "vars"):
            # a flag or variable is one fact per map and use, however many
            # lines touch it, so these compare as sets
            have = {e["key"] for e in theirs.get(kind, [])}
            mine = {e["key"] for e in ours.get(kind, [])}
            for e in ours.get(kind, []):
                e["origin"] = "vanilla" if e["key"] in have else "added"
            gone, seen = [], set()
            for t in theirs.get(kind, []):
                if t["key"] not in mine and t["key"] not in seen:
                    seen.add(t["key"])
                    gone.append(t)
            if gone:
                removed[kind] = gone
            continue
        pool = collections.Counter(e["key"] for e in theirs.get(kind, []))
        left = list(theirs.get(kind, []))
        for e in ours.get(kind, []):
            if pool[e["key"]] > 0:
                pool[e["key"]] -= 1
                e["origin"] = "vanilla"
                for j, t in enumerate(left):
                    if t["key"] == e["key"]:
                        del left[j]
                        break
            else:
                e["origin"] = "added"
        ident = IDENTITY.get(kind)
        if ident:
            for e in ours.get(kind, []):
                if e["origin"] != "added":
                    continue
                for t in left:
                    if ident(t) == ident(e):
                        e["replaces"] = t
                        break
        if left:
            removed[kind] = left
    return removed


class History:
    """Who last wrote each line, and what kind of commit that was."""

    def __init__(self):
        self.shallow = git("rev-parse", "--is-shallow-repository").strip() == "true"
        base = git("merge-base", "main", "HEAD").strip()
        self.ours = {}
        if base:
            for line in git("log", "--format=%H %s", f"{base}..HEAD").splitlines():
                sha, _, subject = line.partition(" ")
                self.ours[sha] = "base ROM" if BASE_ROM_SUBJECTS.match(subject) else "Oxide"
        self._blame = {}

    def blame_many(self, paths):
        todo = [p for p in set(paths) if p not in self._blame]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for p, result in zip(todo, pool.map(self._run_blame, todo)):
                self._blame[p] = result

    def _run_blame(self, path):
        out = subprocess.run(["git", "blame", "--porcelain", "--", path],
                             capture_output=True, text=True).stdout
        lines = {}
        for line in out.splitlines():
            m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", line)
            if m:
                lines[int(m.group(2))] = m.group(1)
        return lines

    def source(self, places):
        """("base ROM" | "Oxide" | "unclear", commit) for the (path, line)
        places an entry rests on: Oxide if any was last written by Oxide,
        else base ROM if any came in with an import, else unclear."""
        if self.shallow:
            return "unclear", None
        found = []
        for path, ln in places:
            sha = (self._blame.get(path) or {}).get(ln)
            if sha is None:
                continue
            if set(sha) == {"0"}:
                found.append(("Oxide", "uncommitted"))
            else:
                found.append((self.ours.get(sha, "unclear"), sha[:9]))
        for want in ("Oxide", "base ROM"):
            for kind, sha in found:
                if kind == want:
                    return kind, sha
        return "unclear", None


def places(e):
    """Every (path, line) an entry rests on."""
    return [(path_of(e["file"]), ln) for ln in e.get("lines", []) if ln] + list(e.get("also", []))


def path_of(stem):
    if stem.startswith("scripts_"):
        return f"{SCRIPTS_DIR}/{stem}.s"
    return f"{EVENTS_DIR}/{stem}.json"


# ---------------------------------------------------------------- splits
def placements(index):
    """{header: (split, basis, order)} where the encounter tool can place it."""
    try:
        from tools.oxide.encounters import locations, model, progression
    except Exception:
        return {}, []
    sidecar = model.load_sidecar() or {}
    areas = sidecar.get("areas") or {}
    order = list(((sidecar.get("splits") or {}).get("order")) or progression.SPLITS)
    rank = {s: i for i, s in enumerate(order)}
    names = locations.label_names(ROOT)
    loc = locations.location_of(ROOT)
    by_loc = collections.defaultdict(list)
    for stem, name in loc.items():
        if name and areas.get(stem, {}).get("split"):
            by_loc[name].append((areas[stem]["split"], areas[stem].get("order")))
    by_file = collections.defaultdict(list)
    try:
        with open(os.path.join(ROOT, "docs/oxide/encounters/scripted.json"), encoding="utf-8") as f:
            for src in json.load(f).get("sources", []):
                if not src.get("split"):
                    continue
                if src.get("capture_area"):
                    by_loc[src["capture_area"]].append((src["split"], src.get("order")))
                if (src.get("from") or {}).get("file", "").startswith("scripts_"):
                    by_file[src["from"]["file"][:-2]].append((src["split"], src.get("order")))
    except (OSError, ValueError):
        pass
    out = {}
    for header, h in index.headers.items():
        area = areas.get(h["encounters"] or "")
        if area and area.get("split"):
            out[header] = (area["split"], "its encounter table", area.get("order"))
            continue
        name = names.get(h["label"])
        cands = list(by_loc.get(name, [])) + list(by_file.get(h["scripts"], []))
        cands = [c for c in cands if c[0] in rank]
        if cands:
            best = min(cands, key=lambda c: (rank[c[0]], c[1] if c[1] is not None else 1e9))
            out[header] = (best[0], "its location name", best[1])
    return out, order


# ---------------------------------------------------------------- the build
def title_of(header):
    words = header[len("MAP_HEADER_"):].split("_")
    out = []
    for w in words:
        if re.match(r"^(B?\d+F|DP|PC|HQ)$", w) or re.match(r"^\d", w):
            out.append(w)
        else:
            out.append(w.capitalize())
    return " ".join(out)


def anchor(title):
    """The anchor GitHub gives a heading: lower case, punctuation other than
    hyphens and underscores dropped, spaces to hyphens."""
    return re.sub(r"[^a-z0-9 _-]", "", title.lower()).replace(" ", "-")


def build():
    """Everything the two outputs say, as one JSON-ready dict."""
    ours = Index(Tree(None))
    theirs = Index(Tree("main"))
    ours_maps, their_maps = Maps(ours), Maps(theirs)
    history = History()
    place, split_order = placements(ours)
    label_names = {}
    try:
        from tools.oxide.encounters import locations
        label_names = locations.label_names(ROOT)
    except Exception:
        pass

    maps, blame_wanted = [], []
    for header, h in ours.headers.items():
        view, unreached, und, missing = ours_maps.view(header)
        tmissing = []
        if header in theirs.headers:
            tview, _, _, tmissing = their_maps.view(header)
        else:
            tview = {}
        for x in missing:
            x["origin"] = "vanilla" if any((y["event"], y["script"]) == (x["event"], x["script"])
                                           for y in tmissing) else "added"
        removed = compare(view, tview)
        split = place.get(header)
        maps.append({"header": header, "title": title_of(header),
                     "location": label_names.get(h["label"]), "scripts": h["scripts"], "events": h["events"],
                     "init": h["init"], "split": split[0] if split else None,
                     "split_basis": split[1] if split else None, "order": split[2] if split else None,
                     "entries": view, "removed": removed, "unreached": unreached, "undecoded": und,
                     "missing": missing})

    refs = chunk_refs(ours)
    their_refs = chunk_refs(theirs)
    files = []
    used = set(ours_maps.users) | {h["init"] for h in ours.headers.values()}
    for stem in sorted(ours.scripts):
        if stem.startswith("scripts_init_") and stem != "scripts_init_new_game":
            continue
        shared = stem in ours_maps.chunk_stems or len(ours_maps.users.get(stem, [])) > 1
        if not shared and stem in used:
            continue
        view, unreached, und = ours_maps.file_view(stem, refs.get(stem, set()))
        if stem in theirs.scripts:
            tview, _, _ = their_maps.file_view(stem, their_refs.get(stem, set()))
        else:
            tview = {}
        removed = compare(view, tview)
        files.append({"file": stem, "title": stem, "group": "shared" if shared else "no header",
                      "entries": view, "removed": removed, "unreached": unreached, "undecoded": und,
                      "missing": []})

    # Entries that repeat on a map (two Devons on Route 214) are matched with
    # main by count, so which copy is the added one is settled by history:
    # the copy whose lines are new.
    mixed = []
    for m in maps + files:
        for kind, items in m["entries"].items():
            groups = collections.defaultdict(list)
            for e in items:
                groups[e["key"]].append(e)
            for group in groups.values():
                origins = {e.get("origin") for e in group}
                if len(group) > 1 and origins == {"added", "vanilla"}:
                    mixed.append(group)
    for m in maps + files:
        for kind, items in m["entries"].items():
            for e in items:
                if e.get("origin") == "added" or any(e in g for g in mixed):
                    blame_wanted.extend(p for p, _ in places(e))
    history.blame_many(blame_wanted)
    for group in mixed:
        added = sum(1 for e in group if e["origin"] == "added")
        rank = {"Oxide": 0, "base ROM": 1, "unclear": 2}
        ordered = sorted(group, key=lambda e: rank[history.source(places(e))[0]])
        for n, e in enumerate(ordered):
            e["origin"] = "added" if n < added else "vanilla"
    for m in maps + files:
        for kind, items in m["entries"].items():
            for e in items:
                if e.get("origin") == "added":
                    e["source"], e["commit"] = history.source(places(e))
                else:
                    e.pop("source", None)
                    e.pop("commit", None)
    trainer_info = trainer_summaries()
    return {"maps": maps, "files": files, "split_order": split_order, "shallow": history.shallow,
            "consts": ours.consts, "trainers": trainer_info}


def trainer_summaries():
    """TRAINER_X -> "Name, level N" from res/trainers/data."""
    out = {}
    base = os.path.join(ROOT, "res", "trainers", "data")
    for f in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if not f.endswith(".json"):
            continue
        try:
            with open(os.path.join(base, f), encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        levels = [p.get("level", 0) for p in d.get("party", [])]
        top = max(levels) if levels else 0
        out["TRAINER_" + f[:-5].upper()] = f"{d.get('name', '?')}, level {top}" + \
            (f", {len(levels)} Pokemon" if len(levels) != 1 else ", 1 Pokemon")
    return out


# ---------------------------------------------------------------- rendering
MODES = {"name": "by name", "number": "by number", "variable": "through a variable",
         "event": "", "engine": "", "unreadable": "unreadable"}
ROLES = {"enemyTrainer1": "against", "enemyTrainer2": "and", "partnerTrainer": "partner",
         "trainerID": "against", "event": ""}
FLAG_OPS = [("set", "Set"), ("clear", "Cleared"), ("check", "Checked"), ("hides", "Hide an object")]
VAR_OPS = [("set", "Set"), ("check", "Checked")]


class Renderer:
    def __init__(self, result):
        self.r = result
        self.consts = result["consts"]
        self.trainers = result["trainers"]

    def values(self, values, kind=None):
        """One operand's possible values, with the condition for each."""
        if not values:
            return "unreadable"
        if len(values) > 6:
            by = sorted({b for v in values for b in v.get("by", [])})
            names = [v["name"] for v in values]
            return f"one of {len(names)}, " + ", ".join(names) + \
                (f", chosen by {' and '.join(by)}" if by else "")
        parts = []
        conditional = any(v["when"] for v in values)
        for v in values:
            name = v["name"]
            if kind == "trainer" and name in self.trainers:
                name = f"{name} ({self.trainers[name]})"
            if v["when"]:
                parts.append(f"{name} if {v['when']}")
            elif conditional and len(values) > 1:
                parts.append(f"{name} otherwise")
            else:
                parts.append(name)
        return ", ".join(parts)

    def origin(self, e):
        out = []
        if not e.get("reached", True):
            out.append("Unreached.")
        if e.get("origin") == "vanilla":
            out.append("Vanilla.")
        elif e.get("origin") == "added":
            src, commit = e.get("source"), e.get("commit")
            if src == "Oxide":
                out.append("Added by Oxide" + (" (not yet committed)." if commit == "uncommitted" else f" ({commit})."))
            elif src == "base ROM":
                out.append(f"Added from the base ROM ({commit}).")
            else:
                out.append("Added, origin unclear.")
            if e.get("replaces"):
                out.append("Replaces vanilla's " + self.entry(e["kind"], e["replaces"]) + ".")
        return " ".join(out)

    def where(self, e):
        f = e["file"]
        ext = ".s" if f.startswith("scripts_") else ".json"
        return f"`{f}{ext}:{e['line']}`" if e.get("line") else f"`{f}{ext}`"

    def entry(self, kind, e):
        if kind == "trainers":
            if e.get("how", "").startswith("sees"):
                return f"{self.values(e['slots'][0]['values'], 'trainer')}, {e['how']}"
            parts = []
            for s in e["slots"]:
                mode = MODES.get(s["mode"], s["mode"])
                parts.append(f"{ROLES.get(s['role'], s['role'])} {self.values(s['values'], 'trainer')}"
                             + (f", {mode}" if mode else ""))
            return f"{e['how']}: " + "; ".join(parts)
        if kind == "statics":
            level = self.values(e["level"]) if e.get("level") else None
            mode = MODES.get(e.get("mode"), "")
            return f"{e['how']}: {self.values(e['species'])}" + (f" at level {level}" if level else "") + \
                (f", {mode}" if mode else "")
        if kind == "pokemon":
            text = f"{e['how']}: {self.values(e['species'])} at level {self.values(e['level'])}"
            if e.get("item"):
                text += f", holding {self.values(e['item'])}"
            return text
        if kind == "eggs":
            return f"an egg of {self.values(e['species'])}"
        if kind == "trades":
            wants = "any Pokemon" if e.get("wants") in (None, "SPECIES_NONE") else e["wants"]
            held = f" holding {e['item']}" if e.get("item") and e["item"] != "ITEM_NONE" else ""
            return f"{e['trade']}: gives {e.get('offers')}{held} for {wants}"
        if kind == "items":
            return f"{self.values(e['item'])} x{self.values(e['count'])}"
        if kind in ("item_balls", "hidden_items"):
            if kind == "hidden_items" and e.get("daily"):
                when = "back each day (the engine clears its flag)"
            else:
                when = "daily" if e.get("daily") else "one time"
            return f"{e['item']} x{e['count']}, {when}, flag {e['flag_name']}"
        return str(e.get("key"))

    def flag_name(self, kind, v):
        c = self.consts
        if kind == "flags":
            name = fmt_value(c, "flag", v)
            return name + (" (daily)" if c.is_daily(v) else "")
        return fmt_value(c, "var", v)

    def aggregate(self, kind, items):
        """{op: [(value, first entry, vanilla?)]} with each value once."""
        field = "flag" if kind == "flags" else "var"
        out = collections.defaultdict(dict)
        for e in items:
            slot = out[e["op"]]
            v = e[field]
            if v not in slot:
                slot[v] = e
            elif e.get("origin") == "vanilla":
                slot[v] = e
        return out

    def flags_block(self, kind, items):
        ops = FLAG_OPS if kind == "flags" else VAR_OPS
        agg = self.aggregate(kind, items)
        lines = []
        for op, label in ops:
            if op not in agg:
                continue
            parts = []
            for v in sorted(agg[op]):
                e = agg[op][v]
                name = self.flag_name(kind, v)
                if e.get("origin") == "added":
                    src = e.get("source")
                    tag = "Oxide" if src == "Oxide" else ("base ROM" if src == "base ROM" else "unclear")
                    name += f" (added, {tag})"
                if not e.get("reached", True):
                    name += " (unreached)"
                parts.append(name)
            lines.append(f"- {label}: " + ", ".join(parts) + ".")
        return lines

    def section(self, m, level="###"):
        out = [f"{level} {m['title']}", ""]
        if "header" in m:
            desc = f"`{m['header']}`: scripts `{m['scripts']}`, events `{m['events']}`"
            if m.get("init") and m["init"] != "scripts_init_empty":
                desc += f", init scripts `{m['init']}`"
            desc += "."
            if m.get("location"):
                desc += f" Location name {m['location']}."
            if m.get("split"):
                desc += f" In {m['split']}'s split, placed by {m['split_basis']}."
            else:
                desc += " The encounter tool does not place it in a split."
        else:
            desc = ("A shared script file: other scripts, events and the engine start it by number." if m["group"] == "shared"
                    else "No map header uses this file, so nothing in it runs.")
        out += [desc, ""]
        for kind, label in KINDS:
            items = m["entries"].get(kind) or []
            if not items:
                continue
            out.append(f"{label}:")
            out.append("")
            if kind in ("flags", "vars"):
                out += self.flags_block(kind, items)
            else:
                for e in sorted(items, key=lambda e: (e["file"], e.get("line") or 0)):
                    out.append(f"- {self.entry(kind, e)}. {self.origin(e)} {self.where(e)}".replace("  ", " "))
            out.append("")
        gone = []
        for kind, label in KINDS:
            for e in m["removed"].get(kind, []):
                if kind in ("flags", "vars"):
                    gone.append(f"{label.lower()[:-1]} {self.flag_name(kind, e['flag' if kind == 'flags' else 'var'])} ({e['op']})")
                else:
                    gone.append(self.entry(kind, e))
        if gone:
            out += ["Gone from vanilla: " + "; ".join(dict.fromkeys(gone)) + ".", ""]
        for x in m.get("missing", []):
            ext = ".s" if x["file"].startswith("scripts_") else ".json"
            who = f"{x['event'][:-1] if x['event'].endswith('s') else x['event']} {x['id']}" if x.get("id") else x["event"]
            out += [f"Names a script the file does not have: {who} runs script {x['script']}, and "
                    f"`{m['scripts']}` has {x['has']}. {x['origin'].capitalize()}. `{x['file']}{ext}:{x['line']}`", ""]
        lost = [u for u in m["unreached"] if not u.get("engine")]
        engine = [u for u in m["unreached"] if u.get("engine")]
        if engine:
            out += [f"Started by the engine by number ({engine[0]['engine']}), not by an event: "
                    + ", ".join(f"script {u['number']} `{u['label']}`" for u in engine) + ".", ""]
        if lost:
            parts = []
            for u in lost:
                what = f"script {u['number']} `{u['label']}`" if u["number"] else f"code at `{u['label']}`"
                parts.append(what + (f" (line {u['line']})" if u.get("line") else ""))
            out += ["Scripts nothing reaches: " + ", ".join(parts) + ".", ""]
        und = {k: v for k, v in m["undecoded"].items() if v}
        if und:
            out += ["Could not read: " + ", ".join(f"{v} {k}" for k, v in sorted(und.items())) + ".", ""]
        return out

    def is_empty(self, m):
        return not any(m["entries"].get(k) for k, _ in KINDS) and not any(m["removed"].values()) \
            and not m["unreached"] and not any(m["undecoded"].values()) and not m.get("missing")

    def counts(self):
        rows = collections.OrderedDict((k, collections.Counter()) for k, _ in KINDS)
        for m in self.r["maps"] + self.r["files"]:
            for kind, _ in KINDS:
                items = m["entries"].get(kind) or []
                if kind in ("flags", "vars"):
                    units = [e for op in self.aggregate(kind, items).values() for e in op.values()]
                    gone = {(e["op"], e.get("flag", e.get("var"))) for e in m["removed"].get(kind, [])}
                    rows[kind]["gone"] += len(gone)
                else:
                    units = items
                    rows[kind]["gone"] += len(m["removed"].get(kind, []))
                for e in units:
                    rows[kind]["total"] += 1
                    if e.get("origin") == "vanilla":
                        rows[kind]["vanilla"] += 1
                    else:
                        rows[kind][e.get("source") or "unclear"] += 1
        return rows

    def markdown(self):
        r = self.r
        maps = r["maps"]
        placed = collections.defaultdict(list)
        for m in maps:
            placed[m["split"]].append(m)
        order = [s for s in r["split_order"] if placed.get(s)] + ([None] if placed.get(None) else [])
        used = [m for m in maps if not self.is_empty(m)]
        empty = [m for m in maps if self.is_empty(m)]
        out = ["# Script index", "",
               "Generated by `tools/oxide/scriptindex.py` from every field script, init script and event file, "
               "compared with `main`; do not edit it by hand, rerun the tool. `script-index.json` beside it holds "
               "the same facts for other tools, and the tool's docstring says how it reads the scripts.", "",
               "Each entry is vanilla when the same map on `main` has it, and added when it does not. An added entry "
               "names the commit that last wrote the lines it rests on: an import commit (the carry-overs, the bulk "
               "generation of scripts and events, the Test.nds update) means it came from the base ROM, any later "
               "commit on this branch means Oxide, and anything else is unclear. The Overseer checks this against "
               "the base ROM. A value set through a variable is traced back through the script with the conditions "
               "that choose it; one the script does not set is \"set elsewhere\". Flags and variables are listed once "
               "per map and use, and the temporaries (`VAR_0x8000` to `VAR_0x800F`) are left out. Test kit scripts "
               "are left out, since a normal build does not have them.", ""]
        if r.get("shallow"):
            out += ["This index was rendered in a shallow clone, so no added entry could be put down to a commit.", ""]
        out += ["## Summary", "",
                f"{len(maps)} map headers, {len(used)} with something to index; "
                f"{sum(1 for f in r['files'] if f['group'] == 'shared')} shared script files; "
                f"{sum(1 for f in r['files'] if f['group'] != 'shared')} script files no header uses.", "",
                "| Kind | Entries | Vanilla | Added from the base ROM | Added by Oxide | Added, unclear | Gone from vanilla |",
                "|---|---:|---:|---:|---:|---:|---:|"]
        for kind, label in KINDS:
            c = self.counts()[kind]
            out.append(f"| {label} | {c['total']} | {c['vanilla']} | {c['base ROM']} | {c['Oxide']} | "
                       f"{c['unclear']} | {c['gone']} |")
        out.append("")
        und = collections.Counter()
        und_maps = collections.Counter()
        unreached = collections.Counter()
        for m in maps + r["files"]:
            for k, v in m["undecoded"].items():
                if v:
                    und[k] += v
                    und_maps[k] += 1
            for u in m["unreached"]:
                if not u.get("engine"):
                    unreached["entries" if u["number"] else "code"] += 1
        missing = [(m, x) for m in maps for x in m.get("missing", [])]
        if missing:
            out += ["Events or init scripts that name a script number past the end of their map's script file; "
                    "if one runs, the engine reads its script's address from beyond the file's table:", ""]
            for m, x in missing:
                out.append(f"- [{m['title']}](#{anchor(m['title'])}): {x['event']} {x.get('id') or ''} runs "
                           f"script {x['script']}, the file has {x['has']}; {x['origin']}.".replace("  ", " "))
            out.append("")
        out += ["What the tool could not read, counted rather than guessed:", "",
                "| Could not read | Count | Maps or files |", "|---|---:|---:|"]
        for k in ("raw data lines", "commands with no name", "numbers no table holds", "variables set elsewhere"):
            out.append(f"| {k} | {und[k]} | {und_maps[k]} |")
        out += ["",
                f"Scripts nothing reaches (no event, header, other script or `SCRIPT_ID()` in `src/` starts them): "
                f"{unreached['entries']} numbered scripts and {unreached['code']} stretches of code, listed in each "
                f"section. The Villa's furniture and the Distortion World are started by the engine by number and "
                f"are marked so; a few other map scripts are too (the Union Room's script 5), which the tool does "
                f"not see. The shared files indexed by trainer, item or hidden item are not checked this way.", "",
                "### Maps by split", ""]
        for s in order:
            ms = sorted((m for m in placed[s] if not self.is_empty(m)),
                        key=lambda m: (m["order"] if m["order"] is not None else 1e9, m["title"]))
            if not ms:
                continue
            name = f"{s}'s split" if s else "Not placed"
            out.append(f"- {name}: " + ", ".join(f"[{m['title']}](#{anchor(m['title'])})" for m in ms) + ".")
        out.append("- Shared script files: " + ", ".join(
            f"[{f['title']}](#{anchor(f['title'])})" for f in r["files"] if f["group"] == "shared") + ".")
        out.append("- Script files no header uses: " + ", ".join(
            f"[{f['title']}](#{anchor(f['title'])})" for f in r["files"] if f["group"] != "shared") + ".")
        out.append("")
        if empty:
            out += ["Map headers with nothing to index: " + ", ".join(f"`{m['header']}`" for m in empty) + ".", ""]
        for s in order:
            ms = sorted((m for m in placed[s] if not self.is_empty(m)),
                        key=lambda m: (m["order"] if m["order"] is not None else 1e9, m["title"]))
            if not ms:
                continue
            out += [f"## {s}'s split" if s else "## Not placed in a split", ""]
            for m in ms:
                out += self.section(m)
        out += ["## Shared script files", ""]
        for f in r["files"]:
            if f["group"] == "shared":
                out += self.section(f)
        out += ["## Script files no header uses", ""]
        for f in r["files"]:
            if f["group"] != "shared":
                out += self.section(f)
        while out and out[-1] == "":
            out.pop()
        return "\n".join(out) + "\n"

    def json(self):
        def clean(e, kind):
            d = {k: v for k, v in e.items() if k not in ("key", "node", "lines", "replaces", "kind", "number", "also")
                 and v is not None}
            if e.get("replaces"):
                d["replaces"] = self.entry(kind, e["replaces"])
            if kind == "flags":
                d["flag_name"] = fmt_value(self.consts, "flag", e["flag"])
                d["daily"] = self.consts.is_daily(e["flag"])
            if kind == "vars":
                d["var_name"] = fmt_value(self.consts, "var", e["var"])
            return d

        def uses(kind, items):
            """Flags and variables as the Markdown lists them: one record per
            use and value, with every place that touches it."""
            field = "flag" if kind == "flags" else "var"
            out = collections.OrderedDict()
            for e in sorted(items, key=lambda e: (e["op"], e[field], e["file"], e.get("line") or 0)):
                k = (e["op"], e[field])
                if k not in out:
                    rec = {"op": e["op"], field: e[field], "name": fmt_value(self.consts, field, e[field]),
                           "origin": e.get("origin"), "reached": False, "at": []}
                    if kind == "flags":
                        rec["daily"] = self.consts.is_daily(e[field])
                    out[k] = rec
                rec = out[k]
                rec["reached"] = rec["reached"] or e.get("reached", True)
                if e.get("origin") == "vanilla":
                    rec["origin"] = "vanilla"
                    rec.pop("source", None)
                    rec.pop("commit", None)
                elif rec["origin"] == "added" and "source" not in rec:
                    rec["source"], rec["commit"] = e.get("source"), e.get("commit")
                where = f"{e['file']}:{e['line']}" if e.get("line") else e["file"]
                if where not in rec["at"]:
                    rec["at"].append(where)
            return list(out.values())

        def one(m):
            d = {k: v for k, v in m.items() if k not in ("entries", "removed", "undecoded", "order")}
            d["entries"] = {}
            for k, _ in KINDS:
                items = m["entries"].get(k)
                if not items:
                    continue
                if k in ("flags", "vars"):
                    d["entries"][k] = uses(k, items)
                else:
                    d["entries"][k] = [clean(e, k) for e in sorted(items, key=lambda e: (e["file"], e.get("line") or 0))]
            d["gone_from_vanilla"] = {}
            for k, v in m["removed"].items():
                if v:
                    d["gone_from_vanilla"][k] = uses(k, v) if k in ("flags", "vars") else [clean(e, k) for e in v]
            d["undecoded"] = {k: v for k, v in sorted(m["undecoded"].items()) if v}
            return d
        counts = {k: dict(sorted(v.items())) for k, v in self.counts().items()}
        doc = {"_comment": "Generated by tools/oxide/scriptindex.py; do not edit. script-index.md explains the fields.",
               "summary": counts, "split_order": self.r["split_order"],
               "maps": [one(m) for m in self.r["maps"] if not self.is_empty(m)],
               "files": [one(f) for f in self.r["files"]]}
        return dump_json(doc) + "\n"


def dump_json(obj, depth=0):
    """Indented down to each entry, and each entry on one line, so the file
    stays small and a diff shows the entries that changed."""
    pad = " " * depth
    if depth >= 5 or not isinstance(obj, (dict, list)) or not obj:
        return json.dumps(obj, sort_keys=True, ensure_ascii=False)
    if isinstance(obj, dict):
        items = [f'{pad} {json.dumps(k)}: {dump_json(obj[k], depth + 1)}' for k in sorted(obj)]
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    items = [f"{pad} {dump_json(x, depth + 1)}" for x in obj]
    return "[\n" + ",\n".join(items) + f"\n{pad}]"


def render():
    result = build()
    for m in result["maps"] + result["files"]:
        for kind, items in list(m["entries"].items()) + list(m["removed"].items()):
            for e in items:
                e["kind"] = kind
                if e.get("replaces"):
                    e["replaces"]["kind"] = kind
    r = Renderer(result)
    return r.markdown(), r.json(), result


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed index differs from what the tool renders")
    args = ap.parse_args()
    if not git("rev-parse", "--verify", "-q", "main").strip():
        print("scriptindex: no local `main` branch; run `git fetch origin main:main`", file=sys.stderr)
        return 2
    if args.check and git("rev-parse", "--is-shallow-repository").strip() == "true":
        print("scriptindex: shallow clone, so the history the index rests on is missing; not compared",
              file=sys.stderr)
        return 2
    md, js, _ = render()
    if args.check:
        stale = []
        for path, text in ((OUT_MD, md), (OUT_JSON, js)):
            try:
                with open(os.path.join(ROOT, path), encoding="utf-8") as f:
                    if f.read() != text:
                        stale.append(path)
            except OSError:
                stale.append(path)
        if stale:
            print("scriptindex: out of date, rerun tools/oxide/scriptindex.py: " + ", ".join(stale))
            return 1
        print("scriptindex: the committed index matches the scripts")
        return 0
    for path, text in ((OUT_MD, md), (OUT_JSON, js)):
        with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    print(f"scriptindex: wrote {OUT_MD} and {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
