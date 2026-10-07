#!/usr/bin/env python3
"""Place the reward table's items in the game, and read them back from a ROM.

Platinum Oxide project, step 9 of docs/oxide/alpha-readiness.md. The Balance
Agent's docs/oxide/reward-placements.tsv lists one row per placement of every
TM copy and held item. `apply` writes each row into the files that hold it,
in each file's own style; `check` reads every placement back out of a built
ROM and requires each row to be found exactly once, with no other source of
any item the table places.

    python3 tools/oxide/place_rewards.py apply [--table TSV] [--dry-run]
    python3 tools/oxide/place_rewards.py check [--table TSV] [--roles TSV] [--rom ROM]

Run from the repository root (scriptdis reads its command table from there).
Apply is idempotent: run it again on an applied tree and nothing changes.

The table's columns are reward, copies, kind, split, map, place, replaces,
trainer_id, badges and note. reward and replaces are item constants, map a
map header constant, badges a count from 0 to 8 (shop rows only). What each
kind writes, and what its place column holds:

ball     An item ball. place is the ball's object id on the map
         (LOCALID_ITEM_...), or empty when replaces names the one ball on the
         map holding that item; its entry in scripts_visible_items.s is
         repointed. A new ball has its tile as place, "x,z" or "x,z,y": the
         object goes at the end of the map's object events, under a new
         visible-item entry and a spare story flag.
hidden   A hidden item. place is its obtained flag (FLAG_OBTAINED_HIDDEN_...),
         or empty with replaces; its row in include/data/field/hidden_items.h
         is repointed. A new one ("x,z" or "x,z,y") takes one of the spare
         FLAG_OBTAINED_HIDDEN_UNUSED_ slots and a bg event on the map.
gift     An item an NPC's script gives. replaces is required, and every give
         of it in the map's script file is repointed with its count. A new
         gift needs dialogue, so it is scripted by hand, not here.
trainer  An optional trainer's reward. trainer_id names the trainer
         (TRAINER_YOUNGSTER_MICHAEL, youngster_michael or its number), who
         must stand on the map as a sight or talk trainer; place is not read.
mart     A mart's stock. place is the mart (MART_SPECIALTIES_ID_...); the
         item is added, or put in the place of replaces. A TM with a badge
         count is sold once (below); copies is then what one purchase gives,
         and is not read otherwise.
prize    A Game Corner prize, in src/scrcmd_game_corner_prize.c's list. The
         reward takes the place of replaces and its coin price; a TM with a
         badge count is sold once, giving copies. A row whose reward is
         ITEM_NONE, with copies 0, takes replaces off the list.

A TM sold once (Ian, 2026-10-06) is listed only from its badge count and
only until it is bought: include/data/sold_tms.h, which this writes from the
mart and prize rows, gives each its badges, its copies and a bit in the
saved variables VAR_SOLD_TMS_0 and VAR_SOLD_TMS_1, kept for good once given,
as the trainer rewards keep their flags.

A trainer's reward is given automatically straight after the player wins
(Ian, 2026-10-06), whether the trainer saw the player or was talked to, in
singles, doubles and two-trainer battles alike. The shared trainer script,
scripts_battles.s, calls one routine after every won trainer battle; the
routine gives the items of the trainer it was called with, under that
trainer's own flag, and gives nothing to a trainer with no row. Talking to a
beaten trainer calls it too, so a reward a full Bag refused is given then.
Each reward trainer keeps the spare flag it was first given, so a rerun after
a table change never moves a flag a save has already set. A trainer that
leaves the table frees its flag for a later run, and a save that set it would
then count the next trainer given it as rewarded already; mid-run hotfixes
should keep reward trainers rather than drop them.

Files outside res/field/ that a row can write: hidden_items.h (hidden),
mart_items.h (mart), scrcmd_game_corner_prize.c (prize) and sold_tms.h
(mart and prize). Every changed script or events file must also be in the
DIVERGED register of bulk_scripts.py or bulk_events.py; `check` lists any
that are not.
"""
import argparse
import collections
import glob
import importlib
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

COLUMNS = ["reward", "copies", "kind", "split", "map", "place", "replaces", "trainer_id", "badges", "note"]
OPTIONAL_COLUMNS = ("badges",)
KINDS = ("ball", "hidden", "gift", "trainer", "mart", "prize")
PRIZES_C = "src/scrcmd_game_corner_prize.c"
SOLD_TMS_H = "include/data/sold_tms.h"
MAX_SOLD_TMS = 32  # two 16-bit saved variables
MAX_BADGES = 8
DEFAULT_TABLE = "docs/oxide/reward-placements.tsv"
DEFAULT_ROLES = "docs/oxide/trainer-roles.tsv"
DEFAULT_ROM = "build/pokeplatinum.us.nds"

# Script id ranges (include/script_manager.h).
SINGLE_BATTLES, DOUBLE_BATTLES = 3000, 5000
VISIBLE_ITEM_SCRIPT, HIDDEN_ITEM_SCRIPT = 7000, 8000
BG_HIDDEN_ITEM = 2
POKEBALL_GFX = "OBJ_EVENT_GFX_POKEBALL"
VISIBLE_ITEMS = "scripts_visible_items"
BATTLES = "scripts_battles"
HIDDEN_ITEMS_H = "include/data/field/hidden_items.h"
MARTS_H = "include/data/mart_items.h"
SHOP_ITEM_END = 0xFFFF

# The common scripts that give the item in VAR_0x8004, VAR_0x8005 times
# (Common_GiveItemQuantity and its no-line-feed twin).
GIVE_COMMON_SCRIPTS = (0x7FC, 0x7E0)
VAR_8004, VAR_8005, VAR_8008, VAR_8009 = 0x8004, 0x8005, 0x8008, 0x8009

BLOCK_BEGIN = "@ place_rewards.py: trainer rewards (begin)"
BLOCK_END = "@ place_rewards.py: trainer rewards (end)"
HOOK_BEGIN = "    @ place_rewards.py: hook begin"
HOOK_END = "    @ place_rewards.py: hook end"
CHAIN = "Battles_TrainerRewards"
DONE = "Battles_TrainerRewardsDone"
BAG_FULL = "Battles_TrainerRewardBagIsFull"


class TableError(Exception):
    pass


# ------------------------------------------------------------------ the tree

class Tree:
    """The files of one checkout, read once and written back on flush."""

    def __init__(self, root):
        self.root = root
        self._text = {}
        self.changed = []
        self.events = {}  # events file -> Events, one per file however many headers share it
        self.items = self.names("generated/items.txt")
        self.item_ids = {n: i for i, n in enumerate(self.items)}
        self.trainers = self.names("generated/trainers.txt")
        self.trainer_ids = {n: i for i, n in enumerate(self.trainers)}
        self.flags = flag_values(self.read("generated/vars_flags.txt"))
        self.headers = map_headers(self.read("include/data/map_headers.h"))

    def path(self, rel):
        return os.path.join(self.root, rel)

    def exists(self, rel):
        return rel in self._text or os.path.exists(self.path(rel))

    def read(self, rel):
        if rel not in self._text:
            with open(self.path(rel), encoding="utf-8", newline="") as f:
                self._text[rel] = f.read()
        return self._text[rel]

    def write(self, rel, text):
        if self.read(rel) != text:
            self._text[rel] = text
            if rel not in self.changed:
                self.changed.append(rel)

    def flush(self):
        for rel in self.changed:
            with open(self.path(rel), "w", encoding="utf-8", newline="") as f:
                f.write(self._text[rel])

    def names(self, rel):
        return [l.strip() for l in self.read(rel).splitlines() if l.strip()]

    def item(self, token):
        """An item constant from a constant or a number, or None."""
        if token.isdigit():
            n = int(token)
            return self.items[n] if n < len(self.items) else None
        if token.startswith("0x"):
            return self.items[int(token, 16)]
        return token if token in self.item_ids else None

    def header(self, name):
        name = name if name.startswith("MAP_HEADER_") else "MAP_HEADER_" + name
        if name not in self.headers:
            raise TableError(f"no map header {name}")
        return name, self.headers[name]

    def events_rel(self, header):
        return f"res/field/events/{self.headers[header]['eventsArchiveID']}.json"

    def script_rel(self, header):
        return f"res/field/scripts/{self.headers[header]['scriptsArchiveID']}.s"

    def text_rel(self, header):
        bank = self.headers[header].get("msgArchiveID", "")
        return f"res/text/{bank[len('TEXT_BANK_'):].lower()}.json" if bank.startswith("TEXT_BANK_") else None

    def trainer(self, token):
        """A trainer constant from TRAINER_X, x (any case) or its number."""
        token = token.strip()
        if token.isdigit():
            n = int(token)
            if n >= len(self.trainers):
                raise TableError(f"no trainer number {n}")
            return self.trainers[n]
        name = token if token.upper().startswith("TRAINER_") else "TRAINER_" + token
        name = name.upper()
        if name not in self.trainer_ids:
            raise TableError(f"no trainer {token}")
        return name


def flag_values(text):
    """{flag or var name: number}, numbered as metang numbers vars_flags.txt:
    each name one past the name before it, unless set to a number or to an
    earlier name, from which the count then continues."""
    out, nxt = {}, 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "=" in line:
            name, expr = (s.strip() for s in line.split("=", 1))
            value = int(expr, 0) if re.fullmatch(r"(0x[0-9a-fA-F]+|\d+)", expr) else out[expr]
        else:
            name, value = line, nxt
        out[name] = value
        nxt = value + 1
    return out


def map_headers(text):
    """{MAP_HEADER_X: {field: value}} from include/data/map_headers.h."""
    out = {}
    for m in re.finditer(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \}", text, re.S):
        out[m.group(1)] = dict(re.findall(r"\.(\w+) = ([^,\n]+),", m.group(2)))
    return out


# ------------------------------------------------------------------ the table

Row = collections.namedtuple("Row", COLUMNS + ["line"])


def read_table(path):
    """The table's rows. Blank lines and lines starting with # are skipped;
    an empty cell or "-" reads as empty."""
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    header = None
    for n, line in enumerate(lines, 1):
        if not line.strip() or line.startswith("#"):
            continue
        cells = [c.strip() for c in line.split("\t")]
        if header is None:
            header = cells
            missing = [c for c in COLUMNS if c not in header and c not in OPTIONAL_COLUMNS]
            if missing:
                raise TableError(f"{path}: the header lacks {', '.join(missing)}")
            continue
        cells += [""] * (len(header) - len(cells))
        rec = {c: ("" if v == "-" else v) for c, v in zip(header, cells)}
        rows.append(Row(**{c: rec.get(c, "") for c in COLUMNS}, line=n))
    return rows


def read_roles(path):
    """trainer-roles.tsv as a list of dicts, or None when it does not exist."""
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f.read().splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return []
    header = [c.strip() for c in lines[0].split("\t")]
    out = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split("\t")]
        cells += [""] * (len(header) - len(cells))
        out.append({c: ("" if v == "-" else v) for c, v in zip(header, cells)})
    return out


def tile(place):
    """(x, z, y) from "x,z" or "x,z,y", or None when place is not a tile."""
    if not re.fullmatch(r"\s*\d+\s*,\s*\d+\s*(,\s*\d+\s*)?", place or ""):
        return None
    parts = [int(p) for p in place.split(",")]
    return (parts[0], parts[1], parts[2] if len(parts) > 2 else 0)


class Placement:
    """One row, resolved against the tree."""

    def __init__(self, tree, row):
        self.row = row
        if row.kind not in KINDS:
            raise TableError(f"kind {row.kind!r} is not one of {', '.join(KINDS)}")
        self.kind = row.kind
        self.reward = tree.item(row.reward)
        # A prize row whose reward is ITEM_NONE takes a prize off the list.
        self.removes = self.kind == "prize" and self.reward == "ITEM_NONE"
        if not self.reward or (self.reward == "ITEM_NONE" and not self.removes):
            raise TableError(f"reward {row.reward!r} is not an item")
        self.replaces = None
        if row.replaces:
            self.replaces = tree.item(row.replaces)
            if not self.replaces:
                raise TableError(f"replaces {row.replaces!r} is not an item")
        self.badges = None
        if row.badges:
            if self.kind not in ("mart", "prize"):
                raise TableError("only a mart or prize row has a badge count")
            if not row.badges.isdigit() or int(row.badges) > MAX_BADGES:
                raise TableError(f"badges {row.badges!r} is not a count from 0 to {MAX_BADGES}")
            self.badges = int(row.badges)
        # Sold once, from a badge count (include/data/sold_tms.h).
        self.sold_once = self.badges is not None and not self.removes
        self.copies = None
        if self.removes:
            if row.copies not in ("", "0"):
                raise TableError("a row that takes a prize off the list has copies 0")
        elif self.kind not in ("mart", "prize") or self.sold_once:
            if not row.copies.isdigit() or not 1 <= int(row.copies) <= 99:
                raise TableError(f"copies {row.copies!r} is not a count from 1 to 99")
            self.copies = int(row.copies)
        self.header = None
        if self.kind not in ("mart", "prize"):
            self.header, _ = tree.header(row.map)
        if self.kind == "prize" and not self.replaces:
            raise TableError("a prize row names the prize it replaces, whose coin price it takes, "
                             "or which it takes off the list")
        self.place = row.place
        self.tile = tile(row.place)
        if self.kind == "trainer" and not row.trainer_id:
            raise TableError("a trainer row needs trainer_id")
        self.trainer = tree.trainer(row.trainer_id) if self.kind == "trainer" else None
        if self.kind == "gift" and not self.replaces:
            raise TableError("a gift row needs replaces: a new gift needs dialogue, so it is scripted by hand")
        if self.kind == "mart" and not row.place.startswith("MART_SPECIALTIES_ID_"):
            raise TableError("a mart row's place is its MART_SPECIALTIES_ID_ (the common stock is set by badge count by hand)")

    def where(self):
        if self.kind == "mart":
            return f"mart {self.place}" + (f" replacing {self.replaces}" if self.replaces else "")
        if self.kind == "prize":
            return f"prize {'removing' if self.removes else 'replacing'} {self.replaces}"
        bits = [self.kind, self.row.map]
        if self.kind == "trainer":
            bits.append(self.trainer)
        elif self.place:
            bits.append(self.place)
        elif self.replaces:
            bits.append("replacing " + self.replaces)
        return " ".join(bits)

    def key(self):
        """What makes two rows the same placement."""
        if self.kind == "trainer":
            return ("trainer", self.trainer, self.reward)
        if self.kind == "mart":
            return ("mart", self.place, self.reward)
        if self.kind == "prize":
            return ("prize", self.replaces)
        if self.kind == "gift":
            return ("gift", self.header, self.replaces)
        return (self.kind, self.header, self.place or self.replaces)

    def __str__(self):
        n = f" x{self.copies}" if self.copies else ""
        return f"line {self.row.line}: {self.reward}{n}, {self.where()}"


def resolve(tree, rows):
    """Placements for every row, or a TableError listing every bad row."""
    out, errors, seen = [], [], {}
    for row in rows:
        try:
            p = Placement(tree, row)
        except TableError as e:
            errors.append(f"line {row.line}: {e}")
            continue
        if p.key() in seen:
            errors.append(f"line {row.line}: the same placement as line {seen[p.key()]}")
            continue
        seen[p.key()] = row.line
        out.append(p)
    if errors:
        raise TableError("\n".join(errors))
    return out


# ------------------------------------------------------------------ item balls

ENTRY_LINE = re.compile(r"^    ScriptEntry (\w+)$")
SETVAR = re.compile(r"^(\s+)(SetVar|SetVarFromValue) (VAR_0x[0-9A-Fa-f]{4}|\d+), (\w+)$")
VAR_NAMES = {"VAR_0x8004": VAR_8004, "VAR_0x8005": VAR_8005, "VAR_0x8008": VAR_8008, "VAR_0x8009": VAR_8009}


def var_of(token):
    return VAR_NAMES.get(token, int(token) if token.isdigit() else None)


def set_value(tree, lines, i, value):
    """Point a SetVar line at a new value. A value that already means the
    same (the item's number where the constant is wanted) is left as written,
    so a row that keeps its item changes no line."""
    m = SETVAR.match(lines[i])
    old = m.group(4)
    if old == value or (value.startswith("ITEM_") and tree.item(old) == value):
        return
    lines[i] = f"{m.group(1)}{m.group(2)} {m.group(3)}, {value}"


class VisibleItems:
    """scripts_visible_items.s: entry n is script 7000 + n, and sets the item
    into VAR_0x8008 and the count into VAR_0x8009 before the shared give."""

    REL = f"res/field/scripts/{VISIBLE_ITEMS}.s"

    def __init__(self, tree):
        self.tree = tree
        self.lines = tree.read(self.REL).split("\n")
        self.labels = [m.group(1) for m in map(ENTRY_LINE.match, self.lines) if m]

    def _body(self, n):
        """Line numbers of entry n's item and count lines."""
        label = self.labels[n]
        start = self.lines.index(label + ":")
        item = count = None
        for i in range(start + 1, len(self.lines)):
            line = self.lines[i]
            if line and not line.startswith((" ", "\t")):
                break
            m = SETVAR.match(line)
            if m and var_of(m.group(3)) == VAR_8008:
                item = i
            elif m and var_of(m.group(3)) == VAR_8009:
                count = i
        if item is None or count is None:
            raise TableError(f"visible item entry {n} ({label}) does not set an item and a count")
        return item, count

    def get(self, n):
        item, count = self._body(n)
        return (self.tree.item(SETVAR.match(self.lines[item]).group(4)),
                int(SETVAR.match(self.lines[count]).group(4), 0))

    def set(self, n, reward, copies):
        item, count = self._body(n)
        set_value(self.tree, self.lines, item, reward)
        set_value(self.tree, self.lines, count, str(copies))

    def add(self, reward, copies):
        """A new entry, given through the same shared routine as the rest."""
        n = len(self.labels)
        if n >= HIDDEN_ITEM_SCRIPT - VISIBLE_ITEM_SCRIPT:
            raise TableError("no visible item script ids are left")
        shared = re.match(r"\s+GoTo (\w+)$", self.lines[self._body(0)[1] + 1])
        if not shared:
            raise TableError("visible item entry 0 does not end by going to the shared give")
        label = f"VisibleItems_Entry{n}"
        if label + ":" in self.lines:
            raise TableError(f"{label} is already a label in {self.REL}")
        last = max(i for i, l in enumerate(self.lines) if ENTRY_LINE.match(l))
        self.lines.insert(last + 1, f"    ScriptEntry {label}")
        at = self.lines.index(shared.group(1) + ":")
        self.lines[at:at] = [f"{label}:",
                             f"    SetVarFromValue VAR_0x8008, {reward}",
                             f"    SetVarFromValue VAR_0x8009, {copies}",
                             f"    GoTo {shared.group(1)}"]
        self.labels.append(label)
        return n

    def save(self):
        self.tree.write(self.REL, "\n".join(self.lines))


# ------------------------------------------------------------------ events

class Events:
    """One map's events file. Parsed for reading; new events are inserted as
    text at the end of their array, so the rest of the file is untouched."""

    def __init__(self, tree, header):
        self.tree = tree
        self.rel = tree.events_rel(header)
        self.data = json.loads(tree.read(self.rel))

    def _append(self, key, obj):
        text = self.tree.read(self.rel)
        m = re.search(r'\n(\s*)"%s": \[' % key, text)
        if not m:
            raise TableError(f"{self.rel} has no {key}")
        indent = m.group(1)
        start = m.end()
        depth, i = 1, start
        while depth:
            c = text[i]
            if c == '"':
                i = text.index('"', i + 1)
                while text[i - 1] == "\\":
                    i = text.index('"', i + 1)
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
            i += 1
        end = i - 1  # the array's closing bracket
        inner = indent + "    "
        rendered = json.dumps(obj, indent=4).replace("\n", "\n" + inner)
        if "[  ]" in text:
            rendered = rendered.replace("[]", "[  ]")
        body = text[start:end]
        if body.strip():
            new = text[:start] + body.rstrip() + ",\n" + inner + rendered + "\n" + indent + text[end:]
        else:
            new = text[:start] + "\n" + inner + rendered + "\n" + indent + text[end:]
        self.tree.write(self.rel, new)
        self.data[key].append(obj)

    def add_object(self, obj):
        self._append("object_events", obj)
        return len(self.data["object_events"]) - 1

    def add_bg(self, bg):
        self._append("bg_events", bg)


def script_number(value):
    if isinstance(value, int):
        return value
    return int(value) if str(value).isdigit() else None


def all_events(tree):
    for path in sorted(glob.glob(tree.path("res/field/events/events_*.json"))):
        rel = os.path.relpath(path, tree.root)
        yield rel, json.loads(tree.read(rel))


def jsonstyle_replace(text, path, value):
    """One value replaced in place, in the file's own style (jsonstyle)."""
    sys.path.insert(0, HERE)
    import jsonstyle
    return jsonstyle.replace_value(text, path, value)


# ------------------------------------------------------------------ spare flags

SPARE_STORY = re.compile(r"FLAG_UNUSED_0x[0-9A-Fa-f]{4}")
SPARE_HIDDEN = "FLAG_OBTAINED_HIDDEN_UNUSED_"


def referenced_flags(tree, pattern):
    """Every name the pattern matches anywhere a flag can be used by name."""
    used = set()
    globs = ["res/field/scripts/*.s", "res/field/events/*.json", "src/**/*.c",
             "include/**/*.h", "asm/**/*.inc", "asm/**/*.s"]
    for g in globs:
        for path in glob.glob(tree.path(g), recursive=True):
            rel = os.path.relpath(path, tree.root)
            try:
                used.update(pattern.findall(tree.read(rel)))
            except UnicodeDecodeError:
                continue
    return used


class SpareFlags:
    """Story flags vanilla never used, handed out lowest first. A flag the
    tree names anywhere is taken, including by this tool's own earlier
    placements, which keep theirs."""

    def __init__(self, tree):
        self.tree = tree
        self._free = None

    def take(self):
        if self._free is None:
            lo = self.tree.flags["MAP_LOCAL_FLAGS_END"]
            hi = self.tree.flags["HIDDEN_ITEM_FLAGS_START"]
            used = referenced_flags(self.tree, SPARE_STORY)
            self._free = sorted((v, n) for n, v in self.tree.flags.items()
                                if SPARE_STORY.fullmatch(n) and lo < v < hi and n not in used)
        if not self._free:
            raise TableError("no spare story flags are left")
        return self._free.pop(0)[1]


# ------------------------------------------------------------------ hidden items

HIDDEN_RE = re.compile(r"^(\s*HIDDEN_ITEM_ENTRY\()(ITEM_\w+,\s*)(\d+)(,\s*)(\d+)(,\s*)(FLAG_\w+)(\),?)$")


class HiddenItems:
    """include/data/field/hidden_items.h. A bg event's script is 8000 plus its
    flag's offset from HIDDEN_ITEM_FLAGS_START, and the row with that flag
    holds the item, count and dowsing range."""

    def __init__(self, tree):
        self.tree = tree
        self.lines = tree.read(HIDDEN_ITEMS_H).split("\n")
        self.start = tree.flags["HIDDEN_ITEM_FLAGS_START"]
        self.rows = {}
        for i, line in enumerate(self.lines):
            m = HIDDEN_RE.match(line)
            if m:
                self.rows[m.group(7)] = i

    def script(self, flag):
        return HIDDEN_ITEM_SCRIPT + self.tree.flags[flag] - self.start

    def flag(self, script):
        value = script - HIDDEN_ITEM_SCRIPT + self.start
        for name, i in self.rows.items():
            if self.tree.flags[name] == value:
                return name
        return None

    def get(self, flag):
        m = HIDDEN_RE.match(self.lines[self.rows[flag]])
        return m.group(2).split(",")[0], int(m.group(3))

    def set(self, flag, reward, copies):
        i = self.rows[flag]
        m = HIDDEN_RE.match(self.lines[i])
        field = m.group(2)
        if field.split(",")[0] == reward and int(m.group(3)) == copies:
            return
        item = (reward + ",").ljust(len(field)) if len(reward) + 1 < len(field) else reward + ", "
        self.lines[i] = m.group(1) + item + str(copies) + m.group(4) + m.group(5) + m.group(6) + m.group(7) + m.group(8)

    def spare(self, taken):
        """A spare slot no bg event uses yet."""
        for name in sorted(self.rows, key=lambda n: self.tree.flags[n]):
            if name.startswith(SPARE_HIDDEN) and self.script(name) not in taken:
                return name
        raise TableError("no spare hidden item slots are left")

    def save(self):
        self.tree.write(HIDDEN_ITEMS_H, "\n".join(self.lines))


# ------------------------------------------------------------------ marts

class Marts:
    """The marts' specialty stocks in include/data/mart_items.h."""

    def __init__(self, tree):
        self.tree = tree
        text = tree.read(MARTS_H)
        self.tables = dict(re.findall(r"\[(MART_SPECIALTIES_ID_\w+)\] = (\w+),?", text))

    def _span(self, text, mart):
        if mart not in self.tables:
            raise TableError(f"no mart {mart}")
        m = re.search(r"const u16 %s\[\] = \{\n(.*?)\n\};" % self.tables[mart], text, re.S)
        return m.start(1), m.end(1)

    def stock(self, mart):
        text = self.tree.read(MARTS_H)
        a, b = self._span(text, mart)
        return re.findall(r"ITEM_\w+", text[a:b])

    def place(self, mart, reward, replaces):
        text = self.tree.read(MARTS_H)
        a, b = self._span(text, mart)
        body = text[a:b].split("\n")
        items = [l.strip().rstrip(",") for l in body]
        if reward in items:
            return
        if replaces:
            if replaces not in items:
                raise TableError(f"{mart} does not sell {replaces}")
            i = items.index(replaces)
            body[i] = body[i].replace(replaces, reward)
        else:
            end = items.index("SHOP_ITEM_END")
            body.insert(end, f"    {reward},")
        self.tree.write(MARTS_H, text[:a] + "\n".join(body) + text[b:])


def block(lines, begin, rel):
    """The line numbers of a tool-owned block's begin and end markers."""
    end = begin.replace("(begin)", "(end)")
    if begin not in lines or end not in lines:
        raise TableError(f"{rel} has lost its '{begin}' block")
    return lines.index(begin), lines.index(end)


PRIZE_LINE = re.compile(r"^(\s*)\{ (ITEM_\w+), (\d+) \},$")


class Prizes:
    """The Game Corner's prize list in src/scrcmd_game_corner_prize.c."""

    BEGIN = "// place_rewards.py: Game Corner prizes (begin)"

    def __init__(self, tree):
        self.tree = tree

    def entries(self):
        """[(line, item, coins)] in the list's order."""
        lines = self.tree.read(PRIZES_C).split("\n")
        a, b = block(lines, self.BEGIN, PRIZES_C)
        return lines, [(i, m.group(2), int(m.group(3)))
                       for i in range(a, b) if (m := PRIZE_LINE.match(lines[i]))]

    def place_all(self, rows):
        """Every prize row at once. Rows chain (TM61 takes TM24's slot while
        TM24 takes TM90's), so one row at a time would swap a reward a
        second time on a rerun; the rows are one substitution over the list
        as it stands, and the list counts as applied when every reward is
        on it and no prize a row replaces or removes is."""
        if not rows:
            return
        lines, entries = self.entries()
        items = {item for _i, item, _coins in entries}
        swaps = {p.replaces: p.reward for p in rows if not p.removes}
        removes = {p.replaces for p in rows if p.removes}
        gone = (set(swaps) - set(swaps.values())) | removes
        if set(swaps.values()) <= items and not gone & items:
            return
        missing = sorted(r for r in set(swaps) | removes if r not in items)
        if missing:
            raise TableError(f"the Game Corner has no prize {', '.join(missing)} (or the list is "
                             "only partly applied)")
        out = []
        for i, line in enumerate(lines):
            m = PRIZE_LINE.match(line)
            if m and any(i == at for at, _item, _coins in entries):
                if m.group(2) in removes:
                    continue
                if m.group(2) in swaps:
                    line = f"{m.group(1)}{{ {swaps[m.group(2)]}, {m.group(3)} }},"
            out.append(line)
        self.tree.write(PRIZES_C, "\n".join(out))


SOLD_LINE = re.compile(r"^\s*\{ (ITEM_\w+), (\d+), (\d+), (\d+) \},$")


class SoldTMs:
    """include/data/sold_tms.h: every item a shop or prize row sells once,
    with its badges, its copies and its bit. A bit, once given, is kept by
    its item on every later run."""

    BEGIN = "// place_rewards.py: sold TMs (begin)"

    def __init__(self, tree):
        self.tree = tree

    def write(self, placements):
        lines = self.tree.read(SOLD_TMS_H).split("\n")
        a, b = block(lines, self.BEGIN, SOLD_TMS_H)
        kept = {m.group(1): int(m.group(4)) for line in lines[a:b]
                if (m := SOLD_LINE.match(line)) and m.group(1) != "ITEM_NONE"}
        rows = [p for p in placements if p.sold_once]
        seen = collections.Counter(p.reward for p in rows)
        twice = sorted(item for item, n in seen.items() if n > 1)
        if twice:
            raise TableError(f"sold once at two counters: {', '.join(twice)}")
        if len(rows) > MAX_SOLD_TMS:
            raise TableError(f"{len(rows)} items are sold once; the two saved variables hold {MAX_SOLD_TMS}")
        bits = {p.reward: kept[p.reward] for p in rows if p.reward in kept}
        free = (bit for bit in range(MAX_SOLD_TMS) if bit not in bits.values())
        for p in rows:
            if p.reward not in bits:
                bits[p.reward] = next(free)
        body = ["static const SoldTM sSoldTMs[] = {"]
        body += [f"    {{ {p.reward}, {p.badges}, {p.copies}, {bits[p.reward]} }},"
                 for p in sorted(rows, key=lambda p: (p.badges, bits[p.reward]))]
        body += ["    { ITEM_NONE, 0, 0, 0 },", "};"]
        self.tree.write(SOLD_TMS_H, "\n".join(lines[:a + 1] + body + lines[b:]))
        return bits


# ------------------------------------------------------------------ gifts

GIVE_LINE = re.compile(r"^\s+(Common_GiveItemQuantity|Common_GiveItemQuantityNoLineFeed"
                       r"|CallCommonScript (2044|2016|0x7FC|0x7E0)"
                       r"|(AddItem|CanFitItem|GoToIfCannotFitItem) (VAR_0x8004|32772),.*)$")
LITERAL_GIVE = re.compile(r"^(\s+)(AddItem|CanFitItem|GoToIfCannotFitItem) (\w+), (\w+)(,.*)$")
WINDOW = 6


def gift_sites(tree, lines, item):
    """Line pairs (item line, count line or None) where the script sets the
    item into VAR_0x8004 for a give, plus lines that give it literally."""
    sites = []
    for i, line in enumerate(lines):
        m = SETVAR.match(line)
        if m and var_of(m.group(3)) == VAR_8004 and tree.item(m.group(4)) == item:
            near = lines[max(0, i - WINDOW):i + WINDOW + 1]
            if not any(GIVE_LINE.match(l) for l in near):
                continue
            count = None
            for j in range(max(0, i - 3), min(len(lines), i + 4)):
                c = SETVAR.match(lines[j])
                if c and var_of(c.group(3)) == VAR_8005:
                    count = j
                    break
            sites.append((i, count))
        m = LITERAL_GIVE.match(line)
        if m and tree.item(m.group(3)) == item:
            sites.append((i, None))
    return sites


def place_gift(tree, p):
    rel = tree.script_rel(p.header)
    lines = tree.read(rel).split("\n")
    sites = gift_sites(tree, lines, p.replaces)
    if not sites and p.replaces != p.reward:
        if gift_sites(tree, lines, p.reward):
            return []  # already applied
    if not sites:
        raise TableError(f"{rel} gives no {p.replaces}")
    for i, count in sites:
        if SETVAR.match(lines[i]):
            set_value(tree, lines, i, p.reward)
            if count is not None:
                set_value(tree, lines, count, str(p.copies))
        else:
            m = LITERAL_GIVE.match(lines[i])
            item = m.group(3) if tree.item(m.group(3)) == p.reward else p.reward
            lines[i] = f"{m.group(1)}{m.group(2)} {item}, {p.copies}{m.group(5)}"
    tree.write(rel, "\n".join(lines))
    return text_mentions(tree, p)


def item_words(tree, item, vanilla=True):
    """The words a line of dialogue would use for an item: its name and, for
    a TM, the move it teaches. The dialogue was written for vanilla's TMs,
    and the TM pass gives TM numbers new moves, so with vanilla the record
    is read from `main` where git has it, and from the tree otherwise."""
    words = []
    rel = f"res/items/data/{item[len('ITEM_'):].lower()}.json"
    import subprocess
    proc = subprocess.run(["git", "-C", tree.root, "show", f"main:{rel}"], capture_output=True, text=True) \
        if vanilla else None
    if (proc and proc.returncode == 0) or tree.exists(rel):
        data = json.loads(proc.stdout if proc and proc.returncode == 0 else tree.read(rel))
        words.append(data.get("name", ""))
        move = data.get("teachesMove")
        if move and move != "MOVE_NONE":
            words.append(" ".join(w.capitalize() for w in move[len("MOVE_"):].split("_")))
    return [w for w in words if w]


def text_mentions(tree, p):
    """Lines in the map's text bank that name the item a gift used to give,
    which the gift's dialogue may still promise."""
    rel = tree.text_rel(p.header)
    if not rel or not tree.exists(rel):
        return []
    # The same item can still have changed, when its TM number teaches a new
    # move since the TM pass.
    words = item_words(tree, p.replaces)
    if set(words) == set(item_words(tree, p.reward, vanilla=False)):
        return []
    out = []
    for msg in json.loads(tree.read(rel)).get("messages", []):
        text = "".join(msg.get("en_US", [])) if isinstance(msg.get("en_US"), list) else str(msg.get("en_US", ""))
        flat = text.replace("\n", " ").replace("\r", " ").replace("\f", " ")
        for w in words:
            if w.lower() in flat.lower():
                out.append(f"dialogue to check: {msg.get('id')} ({rel}) still names {w!r}, "
                           f"which this gift no longer gives")
    return out


# ------------------------------------------------------------------ trainers

def camel(constant):
    return "".join(w.capitalize() for w in constant[len("TRAINER_"):].split("_"))


def strip_battles(text):
    """scripts_battles.s with this tool's block and hooks taken out."""
    lines = text.split("\n")
    out, skip = [], False
    for line in lines:
        if line in (BLOCK_BEGIN, HOOK_BEGIN):
            skip = True
            if line == BLOCK_BEGIN and out and out[-1] == "":
                out.pop()
            continue
        if line in (BLOCK_END, HOOK_END):
            skip = False
            continue
        if not skip:
            out.append(line)
    return "\n".join(out)


def existing_flags(text):
    """{trainer: flag} from the block an earlier run wrote."""
    out = {}
    for m in re.finditer(r"^@ (TRAINER_\w+): .* under (FLAG_\w+)$", text, re.M):
        out[m.group(1)] = m.group(2)
    return out


def norm(token):
    return {"VAR_0x8004": "32772", "VAR_0x8005": "32773", "VAR_0x8001": "32769"}.get(token, token)


def hook_battles(lines):
    """Insert the hooks: after each won battle's SetTrainerFlag, and after the
    beaten trainer's post-battle line. Returns the lines and the counts."""
    single = [HOOK_BEGIN, f"    Call {CHAIN}", HOOK_END]
    double = [HOOK_BEGIN, f"    Call {CHAIN}",
              "    GetApproachingTrainerID 1, VAR_0x800C",
              "    SetVarFromVar VAR_0x8004, VAR_0x800C",
              f"    Call {CHAIN}", HOOK_END]
    out, counts = [], collections.Counter()
    words = [[norm(w) for w in l.replace(",", " ").split()] for l in lines]
    for i, line in enumerate(lines):
        if words[i] == ["ReleaseAll"] and i > 0:
            prev = words[i - 1]
            if prev == ["SetTrainerFlag", "32772"]:
                out += single
                counts["single"] += 1
            elif prev == ["SetTrainerFlag", "32773"]:
                out += double
                counts["double"] += 1
            elif prev == ["CloseMessage"] and i > 2 and words[i - 2] == ["WaitButton"] \
                    and words[i - 3][:1] == ["PrintTrainerDialogue"] and words[i - 3][2:] == ["32769"]:
                out += single
                counts["retry"] += 1
        out.append(line)
    return out, counts


def align_movements(lines):
    """A movement block must start 4-aligned, and the hooks move it, so each
    one gets the .balign vanilla puts before it, between the hook markers so
    that taking the hooks out takes it out too."""
    out = []
    for line in lines:
        if re.match(r"^\w+_Movement_\w+:$", line):
            prev = next((l for l in reversed(out) if l.strip()), "")
            if prev.strip() != ".balign 4, 0":
                out += [HOOK_BEGIN, "    .balign 4, 0", HOOK_END]
        out.append(line)
    return out


def reward_block(rewards, flags):
    """The routine every won battle calls, one branch per reward trainer."""
    out = [BLOCK_BEGIN,
           "@ Written by tools/oxide/place_rewards.py from docs/oxide/reward-placements.tsv;",
           "@ change the table and rerun the tool rather than editing this block. Every won",
           "@ trainer battle calls Battles_TrainerRewards with the trainer in VAR_0x8004, and",
           "@ so does talking to a beaten trainer, which gives a reward a full Bag refused",
           "@ (Ian, 2026-10-06). A trainer without a branch here gets nothing.",
           f"{CHAIN}:"]
    trainers = sorted(rewards)
    for t in trainers:
        out.append(f"    GoToIfEq VAR_0x8004, {t}, Battles_TrainerReward_{camel(t)}")
    out.append("    Return")
    for t in trainers:
        items = rewards[t]
        given = ", ".join(f"{p.reward} x{p.copies}" for p in items)
        out += ["", f"@ {t}: {given}, under {flags[t]}",
                f"Battles_TrainerReward_{camel(t)}:",
                f"    GoToIfSet {flags[t]}, {DONE}"]
        for p in items:
            out += [f"    SetVar VAR_0x8004, {p.reward}",
                    f"    SetVar VAR_0x8005, {p.copies}",
                    f"    GoToIfCannotFitItem VAR_0x8004, VAR_0x8005, VAR_RESULT, {BAG_FULL}"]
        for p in items:
            if len(items) > 1:
                out += [f"    SetVar VAR_0x8004, {p.reward}", f"    SetVar VAR_0x8005, {p.copies}"]
            out.append("    Common_GiveItemQuantity")
        out += [f"    SetFlag {flags[t]}", "    CloseMessage", "    Return"]
    out += ["", f"{BAG_FULL}:", "    Common_MessageBagIsFull", "    CloseMessage",
            f"{DONE}:", "    Return", BLOCK_END]
    return out


def place_trainers(tree, placements, spare):
    rel = f"res/field/scripts/{BATTLES}.s"
    text = tree.read(rel)
    kept = existing_flags(text)
    base = strip_battles(text)
    rewards = collections.defaultdict(list)
    for p in placements:
        rewards[p.trainer].append(p)
    check_trainer_maps(tree, placements)
    if not rewards:
        tree.write(rel, base)
        return {}
    flags = {}
    for t in sorted(rewards):
        flags[t] = kept.get(t) or spare.take()
    lines, counts = hook_battles(base.split("\n"))
    if counts != {"single": 2, "double": 2, "retry": 1}:
        raise TableError(f"{rel} no longer has the five places this tool hooks (found {dict(counts)})")
    lines = align_movements(lines)
    # The block goes after the last line of code, before the file's trailing
    # blank lines, so taking it out leaves the file as it was.
    end = len(lines)
    while end and lines[end - 1] == "":
        end -= 1
    lines[end:end] = [""] + reward_block(rewards, flags)
    tree.write(rel, "\n".join(lines))
    return flags


def trainer_objects(tree):
    """{trainer constant: [events file]} for every sight or talk trainer."""
    out = collections.defaultdict(list)
    for rel, data in all_events(tree):
        for obj in data.get("object_events", []):
            s = obj.get("script")
            if isinstance(s, str) and s.startswith("TRAINER_"):
                out[s].append(rel)
    return out


def check_trainer_maps(tree, placements):
    if not placements:
        return
    objects = trainer_objects(tree)
    errors = []
    for p in placements:
        rel = tree.events_rel(p.header)
        if rel not in objects.get(p.trainer, []):
            found = ", ".join(objects.get(p.trainer, [])) or "no map: a map script battles them, so the reward is scripted by hand"
            errors.append(f"{p}: {p.trainer} is not a sight or talk trainer on {p.header} (found on {found})")
    if errors:
        raise TableError("\n".join(errors))


# ------------------------------------------------------------------ apply

def gauntlet_trainers(tree, roles):
    """The trainers trainer-roles.tsv puts in a gauntlet."""
    out = set()
    for rec in roles or []:
        if rec.get("role") == "gauntlet" and rec.get("trainer_id"):
            out.add(tree.trainer(rec["trainer_id"]))
    return out


def apply(tree, placements, roles=None):
    """Write every placement into the tree. Returns notes for the report."""
    notes, errors = [], []
    gauntlet = gauntlet_trainers(tree, roles)
    for p in placements:
        if p.kind == "trainer" and p.trainer in gauntlet:
            errors.append(f"{p}: {p.trainer} is a gauntlet trainer in trainer-roles.tsv, "
                          "and a gauntlet trainer gives no reward")
    if errors:
        raise TableError("\n".join(errors))
    spare = SpareFlags(tree)
    visible = VisibleItems(tree)
    hidden = HiddenItems(tree)
    marts = Marts(tree)

    def ev(header):
        rel = tree.events_rel(header)
        if rel not in tree.events:
            tree.events[rel] = Events(tree, header)
        return tree.events[rel]

    # The pickup flags of the objects using each visible-item entry. A map
    # with versions (a lake before and after it is drained, Ruin Maniac Cave
    # at its three lengths) repeats a ball in each under one flag, and those
    # copies are one ball.
    visible_refs = collections.defaultdict(set)
    hidden_refs = set()
    for rel, data in all_events(tree):
        for obj in data.get("object_events", []):
            s = script_number(obj.get("script"))
            if s is not None and VISIBLE_ITEM_SCRIPT <= s < HIDDEN_ITEM_SCRIPT:
                visible_refs[s - VISIBLE_ITEM_SCRIPT].add(obj.get("hidden_flag"))
        for bg in data.get("bg_events", []):
            if bg.get("type") == BG_HIDDEN_ITEM:
                hidden_refs.add(bg["script"])

    for p in placements:
        try:
            if p.kind == "ball":
                notes += place_ball(tree, p, ev(p.header), visible, visible_refs, spare)
            elif p.kind == "hidden":
                place_hidden(tree, p, ev(p.header), hidden, hidden_refs)
            elif p.kind == "gift":
                notes += place_gift(tree, p)
            elif p.kind == "mart":
                marts.place(p.place, p.reward, p.replaces)
        except TableError as e:
            errors.append(f"{p}: {e}")
    try:
        Prizes(tree).place_all([p for p in placements if p.kind == "prize"])
    except TableError as e:
        errors.append(str(e))
    try:
        flags = place_trainers(tree, [p for p in placements if p.kind == "trainer"], spare)
        notes += [f"{t} rewards under {f}" for t, f in sorted(flags.items())]
    except TableError as e:
        errors.append(str(e))
    try:
        if tree.exists(SOLD_TMS_H):
            SoldTMs(tree).write(placements)
    except TableError as e:
        errors.append(str(e))
    if errors:
        raise TableError("\n".join(errors))
    visible.save()
    hidden.save()
    return notes


def place_ball(tree, p, ev, visible, refs, spare):
    objs = ev.data["object_events"]
    balls = [(i, o) for i, o in enumerate(objs)
             if (s := script_number(o.get("script"))) is not None and VISIBLE_ITEM_SCRIPT <= s < HIDDEN_ITEM_SCRIPT]
    if p.tile:
        x, z, y = p.tile
        here = [(i, o) for i, o in balls if (o["x"], o["z"]) == (x, z)]
        if not here:
            n = visible.add(p.reward, p.copies)
            flag = spare.take()
            name = "LOCALID_ITEM_" + p.reward[len("ITEM_"):]
            ids = {o.get("id") for o in objs}
            k = 2
            while name in ids:
                name = f"LOCALID_ITEM_{p.reward[len('ITEM_'):]}_{k}"
                k += 1
            ev.add_object({"id": name, "graphics_id": POKEBALL_GFX, "movement_type": "MOVEMENT_TYPE_NONE",
                           "trainer_type": "TRAINER_TYPE_NONE", "hidden_flag": flag,
                           "script": VISIBLE_ITEM_SCRIPT + n, "initial_dir": 0, "data": [],
                           "movement_range_x": 0, "movement_range_z": 0, "x": x, "z": z, "y": y})
            refs[n].add(flag)
            return [f"{p}: new ball {name} under {flag}, visible item entry {n}"]
        (i, obj), = here
    elif p.place:
        here = [(i, o) for i, o in balls if o.get("id") == p.place]
        if not here:
            raise TableError(f"no item ball {p.place} on {p.header}")
        (i, obj), = here
    else:
        here = [(i, o) for i, o in balls
                if visible.get(script_number(o["script"]) - VISIBLE_ITEM_SCRIPT)[0] in (p.replaces, p.reward)]
        if len(here) != 1:
            raise TableError(f"{len(here)} balls on {p.header} hold {p.replaces}; name the one in place")
        (i, obj), = here
    n = script_number(obj["script"]) - VISIBLE_ITEM_SCRIPT
    held, _count = visible.get(n)
    if p.replaces and held not in (p.replaces, p.reward):
        raise TableError(f"the ball holds {held}, not {p.replaces}")
    if len(refs[n]) == 1:
        visible.set(n, p.reward, p.copies)
        return []
    # Vanilla shares one entry between some balls of the same item (two
    # Repels, one script), so repointing the entry would move them all. This
    # ball gets an entry of its own, and so do its copies in the map's other
    # versions, which carry its flag.
    flag = obj.get("hidden_flag")
    new = visible.add(p.reward, p.copies)
    moved = 0
    for rel, data in all_events(tree):
        for i, o in enumerate(data.get("object_events", [])):
            if script_number(o.get("script")) == VISIBLE_ITEM_SCRIPT + n and o.get("hidden_flag") == flag:
                tree.write(rel, jsonstyle_replace(tree.read(rel), ["object_events", i, "script"],
                                                  VISIBLE_ITEM_SCRIPT + new))
                if rel in tree.events:
                    tree.events[rel].data = json.loads(tree.read(rel))
                moved += 1
    refs[n].discard(flag)
    refs[new].add(flag)
    return [f"{p}: given its own visible item entry {new}, since entry {n} serves balls under other flags "
            f"({moved} objects moved)"]


def place_hidden(tree, p, ev, hidden, refs):
    bgs = [b for b in ev.data["bg_events"] if b.get("type") == BG_HIDDEN_ITEM]
    if p.tile:
        x, z, y = p.tile
        here = [b for b in bgs if (b["x"], b["z"]) == (x, z)]
        if not here:
            flag = hidden.spare(refs)
            script = hidden.script(flag)
            ev.add_bg({"script": script, "type": BG_HIDDEN_ITEM, "x": x, "z": z, "y": y,
                       "player_facing_dir": "BG_EVENT_DIR_ALL"})
            refs.add(script)
            hidden.set(flag, p.reward, p.copies)
            return
        flag = hidden.flag(here[0]["script"])
    elif p.place:
        flag = p.place
        if flag not in hidden.rows or hidden.script(flag) not in {b["script"] for b in bgs}:
            raise TableError(f"no hidden item {flag} on {p.header}")
    else:
        here = [b for b in bgs if hidden.get(hidden.flag(b["script"]))[0] in (p.replaces, p.reward)]
        if len(here) != 1:
            raise TableError(f"{len(here)} hidden items on {p.header} hold {p.replaces}; name the one in place")
        flag = hidden.flag(here[0]["script"])
    held, _ = hidden.get(flag)
    if p.replaces and held not in (p.replaces, p.reward):
        raise TableError(f"the hidden item holds {held}, not {p.replaces}")
    hidden.set(flag, p.reward, p.copies)


# ------------------------------------------------------------------ check

class RomReader:
    """Every placement of an item in a built ROM, read with scriptdis and
    the tree's own orders and constants."""

    def __init__(self, tree, rom_path):
        sys.path.insert(0, HERE)
        import import_base_rom as imp
        import scriptdis as sd
        self.sd = sd
        sd.use_base_rom_table(False)
        self.tree = tree
        self.rom_path = rom_path
        self.rom = imp.Rom(rom_path)
        self.scripts = self.rom.narc(sd.SCRIPTS_NARC)
        self.events = self.rom.narc(imp.EVENTS_NARC)
        self.script_order = tree.names("res/field/scripts/scripts.order")
        self.events_order = tree.names("res/field/events/zone_event.order")
        self.arm9 = self.rom.rom.loadArm9()

    def script_member(self, stem):
        return bytes(self.scripts[self.script_order.index(stem)])

    def events_member(self, stem):
        return bytes(self.events[self.events_order.index(stem)])

    def decoded(self, stem):
        decoded, _labels, _end, _moves = self.sd.walk(self.script_member(stem))
        return [decoded[o] for o in sorted(decoded)]

    @staticmethod
    def vals(dc):
        return [v for _k, _n, v in dc.values]

    def objects(self, stem):
        """[(local id, script, flag, x, z)] from a packed events file."""
        buf, o, out = self.events_member(stem), 0, []
        (n,) = struct.unpack_from("<I", buf, o)
        o += 4 + n * 20
        (n,) = struct.unpack_from("<I", buf, o)
        o += 4
        for _ in range(n):
            f = struct.unpack_from("<14HI", buf, o)
            out.append((f[0], f[5], f[4], f[12], f[13]))
            o += 32
        return out

    def bgs(self, stem):
        """[(script, type, x, z)] from a packed events file."""
        buf = self.events_member(stem)
        (n,) = struct.unpack_from("<I", buf, 0)
        out = []
        for i in range(n):
            script, type_, x, z = struct.unpack_from("<HHII", buf, 4 + 20 * i)
            out.append((script, type_, x, z))
        return out

    def visible_items(self):
        """{entry: (item, count)} from scripts_visible_items."""
        buf = self.script_member(VISIBLE_ITEMS)
        entries, _end, _t = self.sd.script_entries(buf)
        out = {}
        for n, off in enumerate(entries):
            got = {}
            for _ in range(3):
                dc = self.sd.decode_command(buf, off)
                if dc.cmd.macro == "SetVarFromValue":
                    var, value = self.vals(dc)
                    got[var] = value
                off += dc.size
            if VAR_8008 in got and VAR_8009 in got:
                out[n] = (self.tree.items[got[VAR_8008]], got[VAR_8009])
        return out

    def _arm9_find(self, check, step=4):
        hits = []
        for sec in self.arm9.sections:
            data = sec.data
            for off in range(0, len(data) - 8, step):
                if check(data, off):
                    hits.append((sec, off))
        return hits

    def hidden_items(self):
        """{script: (item, count)} from gHiddenItems in arm9, found by the
        tree's sequence of scripts."""
        hidden = HiddenItems(self.tree)
        want = [hidden.script(f) - HIDDEN_ITEM_SCRIPT
                for f in sorted(hidden.rows, key=lambda f: hidden.rows[f])]
        first = struct.pack("<HH", 0, want[0])

        def check(data, off):
            if data[off + 4:off + 8] != first or off + 8 * len(want) > len(data):
                return False
            return all(struct.unpack_from("<HH", data, off + 8 * i + 4) == (0, s) for i, s in enumerate(want))

        hits = self._arm9_find(check)
        if len(hits) != 1:
            raise TableError(f"found gHiddenItems {len(hits)} times in arm9")
        sec, off = hits[0]
        out = {}
        for i in range(len(want)):
            item, qty, _rng, _pad, script = struct.unpack_from("<HBBHH", sec.data, off + 8 * i)
            out[HIDDEN_ITEM_SCRIPT + script] = (self.tree.items[item], qty)
        return out

    def _symbol(self, name):
        """(the arm9 section, offset, size) of a symbol, by the linker map
        beside the ROM."""
        xmap = os.path.join(os.path.dirname(os.path.abspath(self.rom_path)), "main.nef.xMAP")
        if not os.path.exists(xmap):
            raise TableError(f"{name} is read at the address the linker map gives, and {xmap} is missing")
        with open(xmap, encoding="utf-8", errors="replace") as f:
            m = re.search(r"^\s+([0-9A-F]{8}) ([0-9A-F]{8}) \.\w+\s+%s\s" % name, f.read(), re.M)
        if not m:
            raise TableError(f"{xmap} does not place {name}")
        addr, size = int(m.group(1), 16), int(m.group(2), 16)
        sec = next((s for s in self.arm9.sections if s.ramAddress <= addr < s.ramAddress + len(s.data)), None)
        if sec is None:
            raise TableError(f"{name} at {addr:#x} is outside arm9")
        return sec, addr - sec.ramAddress, size

    def sold_tms(self):
        """{item: (badges, copies, bit)} from sSoldTMs, to its ITEM_NONE."""
        sec, off, size = self._symbol("sSoldTMs")
        out = {}
        for at in range(off, off + size, 6):
            item, badges, copies, bit = struct.unpack_from("<HBBB", sec.data, at)
            if item == 0:
                break
            out[self.tree.items[item]] = (badges, copies, bit)
        return out

    def prizes(self):
        """[(item, coins)] from the Game Corner's sGameCornerPrizes."""
        sec, off, size = self._symbol("sGameCornerPrizes")
        return [(self.tree.items[item], coins)
                for item, coins in struct.iter_unpack("<HH", sec.data[off:off + size])]

    def marts(self):
        """{MART_SPECIALTIES_ID_X: [item]} from PokeMartSpecialties in arm9.
        Its bytes are too common a shape to find by searching (a run of
        pointers to lists ending in SHOP_ITEM_END matches 18 places), so its
        address comes from the linker map beside the ROM, and the bytes there
        must still read as one list per mart."""
        ids = self.tree.names("generated/mart_specialties_id.txt")
        main = next(s for s in self.arm9.sections if s.ramAddress == 0x02000000)
        lo, hi = main.ramAddress, main.ramAddress + len(main.data)
        xmap = os.path.join(os.path.dirname(os.path.abspath(self.rom_path)), "main.nef.xMAP")
        if not os.path.exists(xmap):
            raise TableError(f"the marts are read at the address the linker map gives, and {xmap} is missing")
        with open(xmap, encoding="utf-8", errors="replace") as f:
            m = re.search(r"^\s+([0-9A-F]{8}) [0-9A-F]{8} \.data\s+PokeMartSpecialties\s", f.read(), re.M)
        if not m:
            raise TableError(f"{xmap} does not place PokeMartSpecialties")
        ptrs = struct.unpack_from(f"<{len(ids)}I", main.data, int(m.group(1), 16) - lo)
        out = {}
        for mart, ptr in zip(ids, ptrs):
            if not lo <= ptr < hi:
                raise TableError(f"the mart table at {m.group(1)} does not match this ROM (rebuilt since?)")
            off, items = ptr - lo, []
            while True:
                (v,) = struct.unpack_from("<H", main.data, off)
                if v == SHOP_ITEM_END:
                    break
                if v >= len(self.tree.items) or len(items) > 64:
                    raise TableError(f"the mart table at {m.group(1)} does not match this ROM (rebuilt since?)")
                items.append(self.tree.items[v])
                off += 2
            out[mart] = items
        return out

    def gifts(self, stem):
        """{item: [count]} for every give in one script file: the item set
        into VAR_0x8004 with a give close by, or given literally."""
        out = collections.defaultdict(list)
        cmds = self.decoded(stem)
        for i, dc in enumerate(cmds):
            name = dc.cmd.macro
            if name == "SetVarFromValue" and self.vals(dc)[0] == VAR_8004:
                near = cmds[max(0, i - WINDOW):i + WINDOW + 1]
                if not any(self._gives(c) for c in near):
                    continue
                count = next((self.vals(c)[1] for c in cmds[max(0, i - 3):i + 4]
                              if c.cmd.macro == "SetVarFromValue" and self.vals(c)[0] == VAR_8005), None)
                item = self.vals(dc)[1]
                if 0 < item < len(self.tree.items):
                    out[self.tree.items[item]].append(count)
            elif name in ("AddItem", "CanFitItem") and self.vals(dc)[0] < 0x4000:
                item, count = self.vals(dc)[:2]
                if 0 < item < len(self.tree.items):
                    out[self.tree.items[item]].append(count)
        return out

    def _gives(self, dc):
        name, vals = dc.cmd.macro, self.vals(dc)
        if name == "CallCommonScript":
            return vals[0] in GIVE_COMMON_SCRIPTS
        return name in ("AddItem", "CanFitItem") and vals[0] == VAR_8004

    def trainer_rewards(self):
        """{trainer id: ([(item, count)], flag)} from the reward routine, and
        a list of problems with the hooks."""
        cmds = self.decoded(BATTLES)
        at = {dc.offset: i for i, dc in enumerate(cmds)}
        problems, calls = [], collections.Counter()
        # The hooks lengthen the file ahead of its movement block, and the
        # ARM9 misreads a movement block at an odd offset (the whiteout hang,
        # findings log 2026-09-21).
        _d, _l, _e, moves = self.sd.walk(self.script_member(BATTLES))
        problems += [f"the movement block at {off:#x} is not 4-aligned" for off in moves if off % 4]
        chain = None
        for i, dc in enumerate(cmds):
            if dc.cmd.macro == "SetTrainerFlag":
                j = i + 1
                while j < len(cmds) and cmds[j].cmd.macro not in ("ReleaseAll", "End"):
                    if cmds[j].cmd.macro == "Call":
                        calls[cmds[j].targets[0]] += 1
                    j += 1
        if not calls:
            return {}, []  # no reward routine; any trainer row is then found 0 times
        chain = calls.most_common(1)[0][0]
        for i, dc in enumerate(cmds):
            if dc.cmd.macro == "SetTrainerFlag":
                j, found = i + 1, False
                while j < len(cmds) and cmds[j].cmd.macro not in ("ReleaseAll", "End"):
                    found |= cmds[j].cmd.macro == "Call" and cmds[j].targets[0] == chain
                    j += 1
                if not found:
                    problems.append(f"the win at {dc.offset:#x} does not call the reward routine")
        retry = any(dc.cmd.macro == "Call" and dc.targets[0] == chain and i >= 3
                    and cmds[i - 1].cmd.macro == "CloseMessage" and cmds[i - 2].cmd.macro == "WaitButton"
                    and cmds[i - 3].cmd.macro == "PrintTrainerDialogue"
                    for i, dc in enumerate(cmds))
        if not retry:
            problems.append("talking to a beaten trainer does not call the reward routine")
        out = {}
        i = at[chain]
        while cmds[i].cmd.macro != "Return":
            cmp, go = cmds[i], cmds[i + 1]
            if cmp.cmd.macro != "CompareVarToValue" or self.vals(cmp)[0] != VAR_8004 or go.cmd.macro != "GoToIf":
                problems.append(f"the reward routine has an unexpected {cmp.cmd.macro} at {cmp.offset:#x}")
                break
            out[self.vals(cmp)[1]] = self._branch(cmds, at[go.targets[0]], problems)
            i += 2
        return out, problems

    def _branch(self, cmds, i, problems):
        check = cmds[i]
        if check.cmd.macro != "CheckFlag":
            problems.append(f"a reward branch at {check.offset:#x} does not start by checking its flag")
            return [], None
        flag = self.vals(check)[0]
        items, pending, set_flag = [], {}, None
        while cmds[i].cmd.macro != "Return":
            dc = cmds[i]
            if dc.cmd.macro == "SetVarFromValue":
                var, value = self.vals(dc)
                pending[var] = value
            elif dc.cmd.macro == "CallCommonScript" and self.vals(dc)[0] in GIVE_COMMON_SCRIPTS:
                items.append((self.tree.items[pending[VAR_8004]], pending.get(VAR_8005)))
            elif dc.cmd.macro == "SetFlag":
                set_flag = self.vals(dc)[0]
            i += 1
        if set_flag != flag:
            problems.append(f"the reward branch for flag {flag} sets flag {set_flag}")
        return items, flag

    def flag_uses(self, flags):
        """{flag: [where]} for every script command and object event in the
        ROM that uses one of the flags."""
        uses = collections.defaultdict(list)
        for idx, buf in enumerate(self.scripts):
            stem = self.script_order[idx] if idx < len(self.script_order) else str(idx)
            if not buf or stem.startswith("scripts_init"):
                continue
            try:
                decoded, _l, _e, _m = self.sd.walk(bytes(buf))
            except Exception:
                continue
            for dc in decoded.values():
                if dc.cmd.macro in ("SetFlag", "ClearFlag", "CheckFlag") and self.vals(dc)[0] in flags:
                    uses[self.vals(dc)[0]].append(f"{stem} {dc.cmd.macro}")
        for stem in self.events_order:
            # An arrow signpost keeps the map header it points at in the same
            # field (Route 223's names Sunyshore City, 150), so the field is a
            # flag only where the events file names a flag or none.
            rel = f"res/field/events/{stem}.json"
            objs = json.loads(self.tree.read(rel)).get("object_events", []) if self.tree.exists(rel) else []
            for i, (_lid, _script, hidden_flag, _x, _z) in enumerate(self.objects(stem)):
                named = str(objs[i].get("hidden_flag", "")) if i < len(objs) else ""
                if hidden_flag in flags and not named.startswith("MAP_HEADER_"):
                    uses[hidden_flag].append(f"{stem} object {i}")
        return uses


# Map headers the player never reaches, by the start of their names. The
# Diamond and Pearl gym's rooms are entered only through three warps in
# Platinum's leader room that sit on tiles walled off from where the player
# arrives (tools/oxide/mapreach.py HEARTHOME_CITY_GYM_LEADER_ROOM puts them
# in a pocket of their own; findings log, 2026-10-06).
UNREACHED = ("MAP_HEADER_HEARTHOME_CITY_DP_GYM_",)


def reached(header):
    return "UNUSED" not in header and not header.startswith(UNREACHED)


def check(tree, placements, rom_path, roles, rows_only=False):
    """Read every placement back out of the ROM. Returns (errors, notes).
    With rows_only, other sources of the table's items and the DIVERGED
    registers are not looked at."""
    r = RomReader(tree, rom_path)
    errors, notes = [], []
    rewards = set() if rows_only else {p.reward for p in placements} - {"ITEM_NONE"}
    claimed = set()

    # Item balls and hidden items, events file by events file. One pickup is
    # one flag: a ball repeated in a map's versions (a lake before and after
    # it is drained) and a hidden item listed in a neighbouring map for the
    # dowsing app are each one source, wherever they appear.
    visible = r.visible_items()
    hidden = r.hidden_items()
    hidden_flags = HiddenItems(tree)
    spots = {}  # (kind, flag) -> {"files", "names", "tiles", "item", "count"}
    used_events = {fields.get("eventsArchiveID") for h, fields in tree.headers.items() if reached(h)}
    for stem in sorted(used_events & set(r.events_order)):
        rel = f"res/field/events/{stem}.json"
        objs = json.loads(tree.read(rel)).get("object_events", []) if tree.exists(rel) else []
        names = {i: o.get("id") for i, o in enumerate(objs)}
        for lid, script, flag, x, z in r.objects(stem):
            if VISIBLE_ITEM_SCRIPT <= script < HIDDEN_ITEM_SCRIPT and script - VISIBLE_ITEM_SCRIPT in visible:
                item, count = visible[script - VISIBLE_ITEM_SCRIPT]
                s = spots.setdefault(("ball", flag), {"files": set(), "names": set(), "tiles": set(),
                                                      "item": item, "count": count})
                s["files"].add(rel)
                s["names"].add(names.get(lid))
                s["tiles"].add((x, z))
        for script, type_, x, z in r.bgs(stem):
            if type_ == BG_HIDDEN_ITEM and script in hidden:
                item, count = hidden[script]
                flag = hidden_flags.flag(script)
                s = spots.setdefault(("hidden", flag), {"files": set(), "names": {flag}, "tiles": set(),
                                                        "item": item, "count": count})
                s["files"].add(rel)
                s["tiles"].add((x, z))

    def match_spot(p):
        hits = []
        for key, s in spots.items():
            if key[0] != p.kind or tree.events_rel(p.header) not in s["files"]:
                continue
            if p.tile and p.tile[:2] not in s["tiles"]:
                continue
            if p.place and not p.tile and p.place not in s["names"]:
                continue
            if not p.place and s["item"] != p.reward:
                continue
            hits.append(key)
        return hits

    for p in placements:
        if p.kind in ("ball", "hidden"):
            hits = match_spot(p)
            good = [k for k in hits if (spots[k]["item"], spots[k]["count"]) == (p.reward, p.copies)]
            if len(good) != 1:
                held = ", ".join(f"{spots[k]['item']} x{spots[k]['count']}" for k in hits) or "nothing"
                errors.append(f"{p}: found {len(good)} times (the place holds {held})")
            claimed.update(good)

    # Every other ball or hidden item of an item the table places.
    flag_names = {}
    for name, value in tree.flags.items():
        if name.startswith("FLAG_"):
            flag_names.setdefault(value, name)
    for key, s in sorted(spots.items(), key=lambda kv: str(kv[0])):
        if s["item"] in rewards and key not in claimed:
            where = ", ".join(sorted(os.path.basename(f)[len("events_"):-len(".json")] for f in s["files"]))
            flag = flag_names.get(key[1], key[1]) if isinstance(key[1], int) else key[1]
            errors.append(f"{s['item']} is also a {key[0]} on {where} ({flag}), which no row names")

    # Gifts.
    gift_rows = collections.defaultdict(list)
    for p in placements:
        if p.kind == "gift":
            gift_rows[tree.headers[p.header]["scriptsArchiveID"]].append(p)
    # Maps the player never reaches hold no source: those the decomp names
    # unused (vanilla left a TM04 in one), and Fantina's Diamond and Pearl
    # gym, which keeps its own TM65 gift.
    stems = sorted({fields["scriptsArchiveID"] for h, fields in tree.headers.items() if reached(h)}
                   & set(r.script_order))
    for stem in stems:
        if stem in (VISIBLE_ITEMS, BATTLES) or stem.startswith("scripts_init"):
            continue
        if not rewards and stem not in gift_rows:
            continue
        try:
            gives = r.gifts(stem)
        except Exception as e:
            notes.append(f"{stem}: could not be read ({e})")
            continue
        for p in gift_rows.pop(stem, []):
            counts = gives.pop(p.reward, [])
            if not counts:
                errors.append(f"{p}: found 0 times")
            elif any(c not in (p.copies, None) for c in counts):
                errors.append(f"{p}: given with counts {counts}")
        for item in gives:
            if item in rewards:
                errors.append(f"{item} is also a gift in {stem}, which no row names")
    for stem, ps in gift_rows.items():
        for p in ps:
            errors.append(f"{p}: found 0 times ({stem} is on no map the game uses)")

    # Trainer rewards.
    chain, problems = r.trainer_rewards()
    errors += [f"scripts_battles: {x}" for x in problems]
    rows = collections.defaultdict(list)
    for p in placements:
        if p.kind == "trainer":
            rows[tree.trainer_ids[p.trainer]].append(p)
    flags_seen = collections.Counter()
    uses = r.flag_uses({flag for _items, flag in chain.values()}) if chain else {}
    for tid, (items, flag) in chain.items():
        name = tree.trainers[tid]
        want = sorted((p.reward, p.copies) for p in rows.get(tid, []))
        if not want:
            errors.append(f"{name} gives {items}, which no row names")
        elif sorted(items) != want:
            errors.append(f"{name} gives {items}, the table says {want}")
        flags_seen[flag] += 1
        others = [u for u in uses.get(flag, []) if not u.startswith(BATTLES)]
        if others:
            errors.append(f"{name}'s reward flag {flag} is also used by {', '.join(others)}")
    for tid, ps in rows.items():
        if tid not in chain:
            for p in ps:
                errors.append(f"{p}: found 0 times")
    for flag, n in flags_seen.items():
        if n > 1:
            errors.append(f"reward flag {flag} is shared by {n} trainers")

    # Each reward trainer must stand on its row's map in the ROM.
    for tid, ps in rows.items():
        for p in ps:
            stem = tree.headers[p.header]["eventsArchiveID"]
            scripts = {s for _l, s, _f, _x, _z in r.objects(stem)}
            if not {SINGLE_BATTLES + tid - 1, DOUBLE_BATTLES + tid - 1} & scripts:
                errors.append(f"{p}: {p.trainer} is not a sight or talk trainer on {p.header} in the ROM")

    # Gauntlet trainers never get a reward (the Overseer, 2026-10-06).
    if roles is None:
        notes.append("trainer-roles.tsv not found: gauntlet trainers not checked")
    else:
        for rec in roles:
            if rec.get("role") == "gauntlet" and rec.get("trainer_id"):
                try:
                    tid = tree.trainer_ids[tree.trainer(rec["trainer_id"])]
                except TableError as e:
                    errors.append(f"trainer-roles.tsv: {e}")
                    continue
                if tid in chain:
                    errors.append(f"gauntlet trainer {tree.trainers[tid]} gives a reward")
            if rec.get("role") == "reward" and rec.get("trainer_id") and rec.get("reward"):
                try:
                    t = tree.trainer(rec["trainer_id"])
                except TableError as e:
                    errors.append(f"trainer-roles.tsv: {e}")
                    continue
                want = sorted((p.reward, str(p.copies)) for p in rows.get(tree.trainer_ids[t], []))
                # A trainer with two rewards lists both, comma-separated, with
                # their copies in the same order ("ITEM_TM03, ITEM_TM28" and
                # "1, 1"; Ian, 2026-10-07).
                items = [i.strip() for i in rec["reward"].split(",")]
                copies = [c.strip() for c in rec.get("copies", "").split(",")]
                try:
                    have = sorted(zip([tree.item(i) for i in items], copies, strict=True))
                except (TableError, ValueError):
                    have = None
                if have != want:
                    errors.append(f"trainer-roles.tsv gives {t} {rec['reward']} x{rec.get('copies')}, "
                                  "which the placements table does not")

    # Marts.
    mart_rows = [p for p in placements if p.kind == "mart"]
    stocks = r.marts()
    for p in mart_rows:
        n = stocks.get(p.place, []).count(p.reward)
        if n != 1:
            errors.append(f"{p}: found {n} times")
    for mart, items in stocks.items():
        for item in items:
            if item in rewards and not any(p.place == mart and p.reward == item for p in mart_rows):
                errors.append(f"{item} is also sold by {mart}, which no row names")

    # The Game Corner's prizes.
    prize_rows = [p for p in placements if p.kind == "prize"]
    prize_items = [item for item, _coins in r.prizes()]
    for p in prize_rows:
        if p.removes:
            if p.replaces in prize_items:
                errors.append(f"{p}: {p.replaces} is still a prize")
        elif prize_items.count(p.reward) != 1:
            errors.append(f"{p}: found {prize_items.count(p.reward)} times")
    for item in prize_items:
        if item in rewards and not any(p.reward == item for p in prize_rows):
            errors.append(f"{item} is also a Game Corner prize, which no row names")

    # What is sold once: each such row's badges and copies, and nothing else.
    sold = r.sold_tms()
    sold_rows = {p.reward: p for p in placements if p.sold_once}
    for item, p in sold_rows.items():
        got = sold.get(item)
        if got is None:
            errors.append(f"{p}: not sold once in the ROM")
        elif got[:2] != (p.badges, p.copies):
            errors.append(f"{p}: sold once from {got[0]} badges giving {got[1]}, the table says "
                          f"{p.badges} and {p.copies}")
    for item in sold:
        if item not in sold_rows:
            errors.append(f"{item} is sold once in the ROM, but no row says so")
    bits = collections.Counter(bit for _b, _c, bit in sold.values())
    for bit, n in bits.items():
        if n > 1 or bit >= MAX_SOLD_TMS:
            errors.append(f"purchase bit {bit} is used {n} times (or is past {MAX_SOLD_TMS - 1})")

    # The files the rows changed must be declared, or the restart checks
    # regenerate them from the base ROM.
    if not rows_only:
        errors += undeclared(tree, placements)
    return errors, notes


def touched_files(tree, placements):
    """The script and events stems the rows write. A ball the tool gave an
    entry of its own (a new ball, or one split from a shared entry) points
    past the shared give, which is the last entry vanilla has, so the events
    files holding such balls are touched too."""
    scripts, events = set(), set()
    visible = VisibleItems(tree)
    shared = re.match(r"\s+GoTo (\w+)$", visible.lines[visible._body(0)[1] + 1]).group(1)
    last_vanilla = visible.labels.index(shared)
    for rel, data in all_events(tree):
        for o in data.get("object_events", []):
            s = script_number(o.get("script"))
            if s is not None and VISIBLE_ITEM_SCRIPT + last_vanilla < s < HIDDEN_ITEM_SCRIPT:
                events.add(os.path.basename(rel)[:-len(".json")])
    for p in placements:
        if p.kind == "ball":
            scripts.add(VISIBLE_ITEMS)
        elif p.kind == "hidden" and p.tile:
            events.add(tree.headers[p.header]["eventsArchiveID"])
        elif p.kind == "gift":
            scripts.add(tree.headers[p.header]["scriptsArchiveID"])
        elif p.kind == "trainer":
            scripts.add(BATTLES)
    return scripts, events


def undeclared(tree, placements):
    sys.path.insert(0, HERE)
    out = []
    scripts, events = touched_files(tree, placements)
    for module, stems in (("bulk_scripts", scripts), ("bulk_events", events)):
        if not stems:
            continue
        diverged = importlib.import_module(module).DIVERGED
        for stem in sorted(stems - set(diverged)):
            out.append(f"{stem} is changed by the table but not in {module}.DIVERGED")
    return out


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=("apply", "check"))
    ap.add_argument("--table", default=DEFAULT_TABLE)
    ap.add_argument("--roles", default=DEFAULT_ROLES)
    ap.add_argument("--rom", default=DEFAULT_ROM)
    ap.add_argument("--root", default=os.getcwd(), help="the checkout to write (apply)")
    ap.add_argument("--dry-run", action="store_true", help="say what would change and write nothing")
    ap.add_argument("--rows-only", action="store_true",
                    help="check: only that each row is found exactly once and the trainer routine is sound, "
                         "skipping the search for other sources and the DIVERGED registers (for a partial "
                         "table or test data)")
    a = ap.parse_args(argv)

    tree = Tree(a.root)
    try:
        placements = resolve(tree, read_table(a.table))
        roles = read_roles(a.roles)
        if a.command == "apply":
            notes = apply(tree, placements, roles)
            for n in notes:
                print(n)
            verb = "would write" if a.dry_run else "wrote"
            print(f"{len(placements)} rows; {verb} {len(tree.changed)} files")
            for rel in tree.changed:
                print(" ", rel)
            if not a.dry_run:
                tree.flush()
            return 0
        errors, notes = check(tree, placements, a.rom, roles, rows_only=a.rows_only)
    except TableError as e:
        print(e, file=sys.stderr)
        return 1
    for n in notes:
        print("note:", n)
    for e in errors:
        print("FAIL:", e)
    print(f"{len(placements)} rows, {len(errors)} problems: "
          + ("every row found exactly once" if not errors else "see above"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
