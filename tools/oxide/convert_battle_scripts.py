#!/usr/bin/env python3
"""Convert hg-engine's battle scripts into Platinum's dialect.

Phase 4 element 4. The 452 imported moves reference 116 battle effects Platinum
does not have, currently stubs. hg-engine has all 116, and the two projects'
battle scripts turn out to be the same language: the opcodes are the same, the
structure is the same, and what differs is a header and about sixty constant
names. `effect_script_0006` is identical in both once those are applied.

**The rename map is derived, not written down.** Both projects ship effect
scripts 0 to 276 and subscripts 0 to 296, numbered alike, so this tool lines
those 574 pairs up and reads the renames straight off them: where hg-engine
has one identifier in a position and Platinum has another, that is a rename,
witnessed by however many files agree. 387 of the pairs line up token for
token. The map cannot drift from the tree, because it is rebuilt from the
tree on every run. Messages are mapped before the pairs are compared, because
HeartGold's battle string bank is Platinum's with more appended: a number
below Platinum's 1,269 is Platinum's message at that index (`battle_strings`
has the evidence), and one past it is a string Platinum does not have.

Four rules keep the derivation honest, and each was learned by getting it
wrong. A `|`-joined flag list carries no order, so the two sides are compared
as sets and only the leftovers pair up. A name Platinum already defines is
shared, never renamed: when the two sides use different shared names in the
same place, the games are choosing different behaviour, and until 2026-09-23
the tool recorded three such choices as renames (`MOVE_SIDE_EFFECT_TO_ATTACKER`
to `ON_HIT`, `SPEED_UP_1_STAGE` to `RAPID_SPIN`, `SPEED_DOWN_2_STAGES` to
`SPEED_DOWN_1_STAGE`) and would have rewritten every converted script that
used them. A rename must agree on value wherever both sides have one, and a
command on its opcode, which rejected three false renames on 2026-09-22,
among them Growth's pointer, carried since the first version. And names no
shared script happens to use are not guessed: they are in `SUPPLEMENT`, each
matched by value.

**What the self-test says.** Of the 216 aligned effect pairs, 213 convert to
Platinum's own script exactly. The three that do not are Growth, String Shot
and Rapid Spin, which Hardlove really changed. Of the 171 aligned subscript
pairs, 167 do; the four that do not are Recover's rounding, Uproar's fixed
three turns, Minimize's two stages and the no-target message, each a later
generation's rule that hg-engine adopted. They are behaviour, and the
converter leaves Platinum's versions alone.

**What it checks before writing.** `--audit` triages hg-engine's effects for
Oxide and `--write` converts the ones it calls ready into
`res/battle/scripts/effects`, refusing the rest and anything already written.
A script is not ready if it uses a name Platinum lacks, prints an hg-engine
string, passes a bare number where a command takes a variable, or aims a side
effect at no battler (`unaimed`). Known defects in hg-engine's own scripts are
corrected on conversion from `FIXES`, and C that turned out to duplicate the
script is recorded in `C_REVIEWED`. `--write-sub` and `--add-ptr` bring
subscripts and side-effect pointers across under the same checks.

    python3 tools/oxide/convert_battle_scripts.py --selftest
    python3 tools/oxide/convert_battle_scripts.py --audit
"""

import argparse
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HG = os.environ.get("HG_ENGINE", os.path.expanduser("~/hg-engine"))
HG_EFFECTS = os.path.join(HG, "data", "battle_scripts", "effects")
HG_SUBSCRIPTS = os.path.join(HG, "data", "battle_scripts", "subscripts")
HG_POINTER_TABLE = os.path.join(HG, "src", "moves.c")
PLAT_EFFECTS = os.path.join(ROOT, "res", "battle", "scripts", "effects")
PLAT_SUBSCRIPTS = os.path.join(ROOT, "res", "battle", "scripts", "subscripts")
SUBSCRIPT_ORDER = os.path.join(PLAT_SUBSCRIPTS, "sub_seq.order")
SUBSCRIPT_MESON = os.path.join(PLAT_SUBSCRIPTS, "meson.build")
SUBSCRIPT_ENUM = os.path.join(ROOT, "generated", "battle_subscripts.txt")
POINTER_ENUM = os.path.join(ROOT, "generated", "battle_move_subscript_ptrs.txt")
POINTER_TABLE = os.path.join(ROOT, "include", "data", "move_side_effect_subscripts.h")
BATTLE_STRINGS = os.path.join(ROOT, "res", "text", "battle_strings.json")

PLATINUM_EFFECTS = 277      # the ids both projects have
PLATINUM_SUBSCRIPTS = 297   # likewise for subscripts; 292 share a name as well
# Platinum's battle strings, the part of the bank HeartGold shares index for
# index. Fixed rather than read from the bank's length: once Oxide appends
# strings of its own, hg-engine's number 1,275 must not map to whatever Oxide
# put at 1,275.
PLATINUM_BATTLE_STRINGS = 1269

# hg-engine's own battle strings that Oxide has added to Platinum's bank, by
# hg-engine's number. The text comes from the donor ROM's bank 197, the same
# bank hg-engine prints from, with Platinum's "The foe’s" for HeartGold's
# "The opposing" and lines rewrapped where Platinum's box needs it; each
# message about a Pokemon is three in a row, ally, wild and foe, because the
# engine picks the variant by adding to the first one's id (2026-09-22).
HG_STRINGS = {
    1436: "BattleStrings_Text_PokemonIsAbsorbingPower_Ally",
    1533: "BattleStrings_Text_PokemonBecameCloakedInAFreezingLight_Ally",
    1536: "BattleStrings_Text_PokemonBecameCloakedInFreezingAir_Ally",
    1542: "BattleStrings_Text_PokemonIsAboutToBeAttackedByItsItem_Ally",
    1545: "BattleStrings_Text_PokemonIsGoingAllOutForThisAttack_Ally",
    1548: "BattleStrings_Text_NeitherPokemonCanRunAway",
    1601: "BattleStrings_Text_PokemonBurnedItselfOut_Ally",
    1604: "BattleStrings_Text_PokemonUsedUpAllItsElectricity_Ally",
    1324: "BattleStrings_Text_PokemonSharedItsGuardWithTheTarget_Ally",
    1327: "BattleStrings_Text_PokemonSharedItsPowerWithTheTarget_Ally",
    1330: "BattleStrings_Text_PokemonTransformedIntoTheWaterType_Ally",
    1573: "BattleStrings_Text_PokemonsItemWasBurnedUp_Ally",
    1616: "BattleStrings_Text_PokemonConcentratedIntensely_Ally",
    1784: "BattleStrings_Text_PokemonFellStraightDown_Ally",
    1514: "BattleStrings_Text_AStickyWebHasBeenLaidOutOnYourSide",
    1516: "BattleStrings_Text_PokemonWasCaughtInAStickyWeb_Ally",
    1430: "BattleStrings_Text_PokemonTookTheKindOffer_Ally",
}

# The message commands and which argument is the message.
MESSAGE_ARG = {"PrintMessage": 0, "PrintGlobalMessage": 0, "BufferMessage": 0,
               "BufferLocalMessage": 1}
HEADER = '#include "macros/btlcmd.inc"\n\n\n'

TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def hg_index(folder, prefix):
    out = {}
    for p in glob.glob(os.path.join(folder, prefix + "_*.s")):
        m = re.match(prefix + r"_(\d{4})_(.+)\.s$", os.path.basename(p))
        if m:
            out[int(m.group(1))] = (m.group(2), p)
    return out


def body_lines(path):
    """A script's meaningful lines, with each project's own preamble dropped."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


def split_args(line):
    head, _, rest = line.partition(" ")
    return head, ([a.strip() for a in rest.split(",")] if rest.strip() else [])


def derive_renames(have=None):
    """The hg-engine to Platinum identifier map, read off the shared scripts.

    Returns (map, aligned, skipped). A pair that does not line up argument for
    argument is skipped rather than guessed at: those are the effects the two
    games implement differently, and forcing an alignment there would invent
    renames that are really behaviour differences.
    """
    strings = battle_strings()
    pairs = collections.Counter()
    aligned, skipped = 0, []
    for n, hg_path, plat in script_pairs():
        # hg-engine prints messages by number and Platinum by name; map the
        # numbers first, or every script that prints anything fails to align.
        a = [map_message(l, strings)[0] for l in body_lines(hg_path)]
        b = body_lines(plat)
        if len(a) != len(b):
            skipped.append(n)
            continue
        local, ok = [], True
        for la, lb in zip(a, b):
            ha, aa = split_args(la)
            hb, ab = split_args(lb)
            if ha != hb:
                local.append((ha, hb))
            if len(aa) != len(ab):
                ok = False
                break
            for x, y in zip(aa, ab):
                xs, ys = x.split("|"), y.split("|")
                if len(xs) != len(ys):
                    ok = False
                    break
                if len(xs) > 1:
                    # A flag list has no order. Pair only what the two sides do
                    # not already share, so flags both projects spell the same
                    # way are never mistaken for renames of each other.
                    rx, ry = sorted(set(xs) - set(ys)), sorted(set(ys) - set(xs))
                    if len(rx) == len(ry):
                        local += list(zip(rx, ry))
                    continue
                tx, ty = TOKEN.findall(x), TOKEN.findall(y)
                if len(tx) != len(ty):
                    ok = False
                    break
                local += [(p, q) for p, q in zip(tx, ty) if p != q]
            if not ok:
                break
        if not ok:
            skipped.append(n)
            continue
        aligned += 1
        for pr in local:
            pairs[pr] += 1

    # A rename also has to agree on value wherever both sides have one. With
    # subscripts in the derivation (2026-09-22), one subscript hg-engine had
    # rewritten produced two false renames: its new DivideVarByValueRoundUp
    # command became Platinum's truncating DivideVarByValue, and its target
    # variable (0x10) became Platinum's attacker (0x0F) instead of its
    # defender (0x10). Checking values rejects both without a list.
    hg_vals, plat_vals = hg_values(), platinum_values()
    hg_cmds, plat_cmds = hg_commands(), platinum_commands()
    votes = collections.defaultdict(collections.Counter)
    for (x, y), c in pairs.items():
        if x in hg_cmds:
            # A command renames only within the range both tables share, and
            # only to the command at the same opcode.
            if hg_cmds[x] >= SHARED_COMMANDS or plat_cmds.get(y) != hg_cmds[x]:
                continue
        elif x in hg_vals and y in plat_vals and hg_vals[x] != plat_vals[y]:
            continue
        votes[x][y] += c
    # A name Platinum already defines is shared, not renamed. When the two
    # sides of an aligned pair use different shared names in the same place,
    # that is the two games choosing different behaviour, and recording it as
    # a rename would silently rewrite hg-engine's choice into Platinum's
    # everywhere else. This was a real defect until 2026-09-23: it turned
    # MOVE_SIDE_EFFECT_TO_ATTACKER into ON_HIT and SPEED_UP_1_STAGE into
    # RAPID_SPIN in every converted script. Each false rename was witnessed by
    # a few pairs where Hardlove changed a move, then applied to every pair,
    # so it also caused most of the self-test's mismatches (161 exact of 198
    # with it, 196 without).
    have = have if have is not None else platinum_identifiers()
    shared = {x for x in votes if x in have}
    for x in shared:
        del votes[x]
    conflicts = {x: dict(ys) for x, ys in votes.items() if len(ys) > 1}
    return ({x: ys.most_common(1)[0][0] for x, ys in votes.items()},
            aligned, skipped, conflicts)


# Renames the shared scripts never witness, because no effect 0 to 276 happens
# to use them. Each one was matched by value and, for the flag words, by which
# status field Platinum's own scripts pair it with, so none is a guess from the
# name alone (2026-09-23). `supplemented()` refuses to run if a target stops
# existing in Platinum.
SUPPLEMENT = {
    "STATUS_NONE": "MON_CONDITION_NONE",                                   # 0
    "STATUS_POISON": "MON_CONDITION_POISON",                               # 1 << 3
    "STATUS_BAD_POISON": "MON_CONDITION_TOXIC",                            # 1 << 7
    "BMON_DATA_ABILITY": "BATTLEMON_ABILITY",                              # 0x1A
    "BMON_DATA_HELD_ITEM": "BATTLEMON_HELD_ITEM",                          # 0x37
    "BMON_DATA_STAT_CHANGE_SPEED": "BATTLEMON_SPEED_STAGE",                # 21
    "BMON_DATA_STAT_CHANGE_SPATK": "BATTLEMON_SP_ATTACK_STAGE",            # 22
    "BMON_DATA_STAT_CHANGE_SPDEF": "BATTLEMON_SP_DEFENSE_STAGE",           # 23
    "BSCRIPT_VAR_MOVE_TYPE": "BTLVAR_MOVE_TYPE",                           # 0x39
    "BSCRIPT_VAR_BATTLER_STAT_CHANGE": "BTLVAR_SIDE_EFFECT_MON",           # 0x11
    "BSCRIPT_VAR_BATTLE_STATUS_2": "BTLVAR_BATTLE_CTX_STATUS_2",           # 0x3C
    "BSCRIPT_VAR_SIDE_EFFECT_PARAM": "BTLVAR_SIDE_EFFECT_PARAM",           # 0x22
    "BATTLE_STATUS_MOVE_ANIMATIONS_OFF": "SYSCTL_PLAYED_MOVE_ANIMATION",   # status, 1 << 14
    "BATTLE_STATUS2_UPDATE_STAT_STAGES": "SYSCTL_UPDATE_STAT_STAGES",      # status 2, 1 << 1
    "BATTLE_STATUS2_STAT_STAGE_CHANGE_SHOWN": "SYSCTL_STAT_STAGE_CHANGE_SHOWN",  # status 2, 1 << 7
    "MULTIHIT_TRIPLE_KICK": "SYSCTL_TRIPLE_KICK",                          # 0xDD both sides
}


def platinum_identifiers():
    """Every name a Platinum battle script can use: generated enums, the
    script macros, and whatever the headers define or enumerate."""
    have = set()
    for f in glob.glob(os.path.join(ROOT, "generated", "*.txt")):
        have |= {l.strip() for l in open(f, encoding="utf-8") if l.strip()}
    for root in ("include", os.path.join("build", "res", "text", "bank"), "asm"):
        for dp, _, names in os.walk(os.path.join(ROOT, root)):
            for n in names:
                if not n.endswith((".h", ".inc")):
                    continue
                t = open(os.path.join(dp, n), encoding="utf-8", errors="ignore").read()
                have |= set(re.findall(r"#define\s+(\w+)", t))
                have |= set(re.findall(r"^\s*\.macro\s+(\w+)", t, re.M))
                have |= set(re.findall(r"^\s*\.equ\s+(\w+)\s*,", t, re.M))
                for blk in re.findall(r"enum\s*\w*\s*\{(.*?)\}", t, re.S):
                    have |= set(re.findall(r"^\s*([A-Za-z_]\w*)\s*(?:=|,|$)", blk, re.M))
    return have


def supplemented(renames, have=None):
    have = have if have is not None else platinum_identifiers()
    gone = sorted(v for v in SUPPLEMENT.values() if v not in have)
    if gone:
        sys.exit("SUPPLEMENT names identifiers Platinum no longer has: %s" % gone)
    merged = dict(SUPPLEMENT)
    merged.update(subscript_renames())
    merged.update(ability_renames())
    merged.update(battler_field_renames())
    merged.update(renames)
    return merged


def ability_renames():
    """hg-engine's ability names that differ from Oxide's at the same id. Element
    3 imported the donor's abilities contiguously, so the ids agree for good,
    and 309 of hg-engine's 320 names agree too (2026-09-22). The other ten are
    names the donor's display text squashed (MEGALAUNCHER for MEGA_LAUNCHER),
    the two As One forms and two placeholders, matched here by id."""
    oxide = lines_of(os.path.join(ROOT, "generated", "abilities.txt"))
    return {name: oxide[value] for name, value in hg_values().items()
            if name.startswith("ABILITY_") and value < len(oxide) and oxide[value] != name}


def battler_field_renames():
    """hg-engine's BMON_DATA_ names mapped to Platinum's battler fields by
    number. All 101 of hg-engine's fields name the same field as Platinum's at
    the same number (checked by eye, 2026-09-22), and the derivation had
    already found 49 of them independently; this supplies the rest, such as
    BMON_DATA_SPDEF, which no shared script happens to use."""
    fields = lines_of(os.path.join(ROOT, "generated", "battle_mon_params.txt"))
    return {name: fields[value] for name, value in hg_values().items()
            if name.startswith("BMON_DATA_") and value < len(fields) and fields[value] != name}


def lines_of(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip()]


# The command tables agree opcode for opcode below 222, apart from six names
# (HealthbarSlideIn against HealthBoxSlideIn and the like). HeartGold then adds
# two commands before End, and hg-engine's own start at 0xE1 after that, so
# nothing from 222 up is a rename of a Platinum command.
SHARED_COMMANDS = 222


def hg_commands():
    """hg-engine's command names by opcode, from its debug name table."""
    t = open(os.path.join(HG, "src", "battle", "battle_script_commands.c"),
             encoding="utf-8", errors="replace").read()
    start = t.index("BattleScrCmdNames[] = {")
    names = re.findall(r'"(\w+)"', t[start:t.index("\n};", start)])
    return {n: i for i, n in enumerate(names)}


def platinum_commands():
    names = re.findall(r"ScriptCommand\(\w+,\s*BtlCmd_(\w+)\)",
                       open(os.path.join(ROOT, "include", "data", "scripts", "btlcmd.h"),
                            encoding="utf-8").read())
    return {n: i for i, n in enumerate(names)}


def hg_values():
    """hg-engine's constants that are defined as a plain number."""
    out = {}
    for f in glob.glob(os.path.join(HG, "include", "constants", "*.h")):
        t = open(f, encoding="utf-8", errors="replace").read()
        for name, value in re.findall(r"^#define\s+(\w+)\s+\(?(0x[0-9A-Fa-f]+|\d+)\)?\s*(?://.*)?$",
                                      t, re.M):
            out.setdefault(name, int(value, 0))
    return out


def platinum_values():
    """Platinum's positional enums from generated/, where a name's value is
    its line number. The mask-type lists are left out, their values not being
    positions."""
    meson = open(os.path.join(ROOT, "generated", "meson.build"), encoding="utf-8").read()
    out = {}
    for name in re.findall(r"'(\w+)': \{ 'type': 'enum'", meson):
        path = os.path.join(ROOT, "generated", name + ".txt")
        if os.path.exists(path):
            for i, n in enumerate(lines_of(path)):
                out.setdefault(n, i)
    return out


def subscript_renames():
    """hg-engine's subscript names that differ from Platinum's at the same id.
    Both projects number subscripts 0 to 296 the same way and 292 of them share
    a name too; the other five are two projects' words for one subscript, so
    they are matched by id, the way SUPPLEMENT matches by value."""
    enum = lines_of(SUBSCRIPT_ENUM)[:PLATINUM_SUBSCRIPTS]
    out = {}
    for n, (name, _) in hg_index(HG_SUBSCRIPTS, "subscript").items():
        if n < len(enum) and "BATTLE_SUBSCRIPT_" + name != enum[n]:
            out["BATTLE_SUBSCRIPT_" + name] = enum[n]
    return out


def battle_strings():
    """Platinum's battle strings in bank order, as (id, text).

    HeartGold's bank is Platinum's with more appended, so hg-engine's message
    numbers below Platinum's count are Platinum's messages at the same index.
    Checked 2026-09-22 against the comments hg-engine writes above its message
    commands: 459 of the 511 below 1,269 carry Platinum's text at that index
    word for word, and the other 52 are the same message reworded ("is already
    burned!" against "already has a burn."). A number past the bank is a string
    Platinum does not have, and the audit calls that effect `text`."""
    import json
    out = []
    for m in json.load(open(BATTLE_STRINGS, encoding="utf-8"))["messages"]:
        text = "".join(m.get("en_US", []))
        text = re.sub(r"\{STRVAR_\d+ \d+, (\d+), \d+\}", r"{\1}", text)
        out.append((m["id"], " ".join(text.split())))
    return out


def map_message(line, strings):
    """A message command's bare number in hg-engine's line becomes Platinum's
    message id, returned with the message's text for a comment above it, which
    is how Platinum's own scripts are written. Anything else comes back as is."""
    head, args = split_args(line.strip())
    at = MESSAGE_ARG.get(head)
    if at is None or len(args) <= at or not re.fullmatch(r"\d+", args[at]):
        return line, None
    n = int(args[at])
    if n >= PLATINUM_BATTLE_STRINGS:
        if n not in HG_STRINGS:
            return line, None
        index = [i for i, (mid, _) in enumerate(strings) if mid == HG_STRINGS[n]]
        if not index:
            sys.exit("HG_STRINGS names %s, which the bank does not have" % HG_STRINGS[n])
        n = index[0]
    args[at] = strings[n][0]
    indent = line[:len(line) - len(line.lstrip())]
    return indent + head + " " + ", ".join(args), strings[n][1]


# Defects in hg-engine's own scripts, corrected on conversion so the fix is
# written down once and reapplied on every run. `check_script` flags the
# pattern, so a new one shows up in the audit rather than in a battle.
FIXES = {
    # Compares the target's HP with battle script variable 0, which in both
    # projects is the battle type, where it means the value 0: "is the target
    # already fainted". As written, Matcha Gotcha's burn would be skipped or
    # applied depending on the battle type rather than the target's HP.
    "subscript_0446_BURN_AND_DRAIN_HEALTH.s": [
        ("CompareMonDataToVar OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, NoBurn",
         "CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, NoBurn"),
    ],
    # Sets its side effect with no TO_ flag, so its subscript's Defense drop
    # lands on battler slot 0 rather than the user; `unaimed` flags it.
    # Geomancy's second turn buffers message 0 after raising its stats, which
    # nothing prints afterwards in Platinum; it is dropped (None deletes).
    "effect_script_0318_CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2.s": [
        ("BufferMessage 0, TAG_NONE", None),
        # Its second turn plays its own animation before the charge cleanup
        # sets the effect chance to 1, which is what its animation reads to
        # tell the turns apart; set it first so the second turn is not drawn
        # as another charge.
        ("PlayMoveAnimation BTLSCR_ATTACKER",
         "UpdateVar OPCODE_SET, BTLVAR_MOVE_EFFECT_CHANCE, 1\n    PlayMoveAnimation BTLSCR_ATTACKER"),
    ],
    # Guard Split and Power Split are status moves, and Platinum runs a status
    # move's side effect through the direct path, as its own Pain Split does;
    # hg-engine sets them as indirect, which Platinum only runs after a hit.
    "effect_script_0278_GUARD_SPLIT.s": [
        ("UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_GUARD_SPLIT",
         "UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_GUARD_SPLIT"),
    ],
    "effect_script_0279_POWER_SPLIT.s": [
        ("UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_POWER_SPLIT",
         "UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_POWER_SPLIT"),
    ],
    "effect_script_0343_USER_DEF_DOWN_HIT_REMOVE_PROTECT.s": [
        ("UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_HYPERSPACE_FURY",
         "UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_ATTACKER|MOVE_SUBSCRIPT_PTR_HYPERSPACE_FURY"),
    ],
}

# Effects the audit calls `c` whose hg-engine C has been read and found to do
# nothing Platinum's script does not, so `--write` may convert them. Each
# reason says what the C was. Behaviour Platinum lacks is not listed here: it
# is ported into Platinum's C and the script written by hand.
C_REVIEWED = {
    277: "BeforeMove fails the move early when both stats are maxed; the subscript checks the same",
    283: "BeforeMove fails the move early when all three stats are maxed; the subscript checks the same",
    286: "BeforeMove fails the move early when all three stats are maxed; the subscript checks the same",
    288: "BeforeMove fails the move early when both stats are maxed; the subscript checks the same",
    290: "BeforeMove fails the move when all three raised stats are maxed; the subscript lowers the "
         "defenses regardless, a small departure",
    295: "BeforeMove fails the move early when both stats are maxed; the subscript checks the same",
    328: "BeforeMove fails the move early when Defense is maxed, the same case as Iron Defense's, "
         "which Platinum's stat subscript handles",
    343: "BeforeMove fails the move for anyone but Hoopa; no Oxide species learns it and Hoopa is "
         "not in Oxide, so only Metronome reaches it",
    346: "BeforeMove fails the move below a third of max HP; the subscript checks the same",
    318: "BeforeMove runs the charge turn from C; Platinum runs it from the script, as Skull Bash "
         "does, and the effect is on Move_IsMultiTurn",
    345: "BeforeMove fails the move when the target holds nothing; the script checks the same",
    363: "BeforeMove runs the charge turn from C; Platinum runs it from the script, as Sky Attack "
         "does, with the message set in the move's own script.s, and the effect is on "
         "Move_IsMultiTurn; the rest is Kyurem's form change, and Kyurem is not in Oxide",
    364: "as Freeze Shock",
    399: "the C is hg-engine's move-condition flag; Oxide keeps it as a two-bit countdown in "
         "the unused effect-mask bits 19 and 20, run down at the end of turn with Lock-On's",
    406: "the C grounds the target after the hit, lets Smack Down hit a Pokemon mid-Fly and "
         "makes Thousand Arrows neutral on Flying; Oxide's subscript and battle_lib.c do the same "
         "with the unused effect-mask bit 31, and also end the target's Fly and block Fly, "
         "Bounce and Magnet Rise afterwards",
    278: "BeforeMove fails the move against a substitute; the Oxide subscript checks the same",
    279: "as Guard Split",
    284: "BeforeMove fails the move against pure Water, Multitype or a substitute; the Oxide "
         "subscript checks the same",
    292: "CalcBaseDamage works out the same weight ratio that CalcHeavySlamPower now does",
    378: "BeforeMove fails the move when the target's Attack is at its lowest; the Oxide "
         "subscript checks the same",
    348: "BeforeMove thaws a frozen user, ported beside Flame Wheel's in battle_controller_player.c",
    305: "BeforeMove fails the move when the target has already acted; ChangeExecutionOrderPriority "
         "checks the same, and moves the target's entry in battlerActionOrder where hg-engine flags "
         "it for its speed comparison",
}

# Commands whose arguments at these positions are battle script variables, so
# a bare number there is a variable id, almost certainly meant as a value.
VARIABLE_ARGS = {"CompareMonDataToVar": (3,), "CompareVarToVar": (1, 2),
                 "UpdateVarFromVar": (1, 2), "UpdateMonDataFromVar": (3,)}


def convert(path, renames, strings=None):
    """One hg-engine script in Platinum's dialect."""
    strings = strings if strings is not None else battle_strings()
    fixes = dict(FIXES.get(os.path.basename(path), []))
    out = [HEADER.rstrip("\n"), "", ""]
    for line in open(path, encoding="utf-8", errors="replace"):
        raw = line.rstrip("\n")
        stripped = raw.split("//")[0].rstrip()
        if stripped.startswith(("#include", ".include")) or stripped.strip() == ".data":
            continue
        if not stripped.strip():
            continue
        # Platinum indents with four spaces; a few hg-engine files use a tab.
        stripped = stripped.expandtabs(4)
        renamed = TOKEN.sub(lambda m: renames.get(m.group(0), m.group(0)), stripped)
        if renamed.strip() in fixes:
            indent = renamed[:len(renamed) - len(renamed.lstrip())]
            fixed = fixes.pop(renamed.strip())
            if fixed is None:
                continue
            renamed = indent + fixed
        renamed, text = map_message(renamed, strings)
        if text:
            out.append("%s// %s" % (renamed[:len(renamed) - len(renamed.lstrip())], text))
        out.append(renamed)
    if fixes:
        sys.exit("FIXES for %s no longer match its converted text: %s"
                 % (os.path.basename(path), sorted(fixes)))
    return "\n".join(out) + "\n"


def script_pairs():
    """Every hg-engine script with a Platinum counterpart at the same id: the
    277 shared effects and the 297 shared subscripts. The rename map is read
    off all of them, and the self-test scores all of them."""
    pairs = []
    effects = hg_index(HG_EFFECTS, "effect_script")
    for n in range(PLATINUM_EFFECTS):
        plat = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % n)
        if n in effects and os.path.exists(plat):
            pairs.append((("effect", n), effects[n][1], plat))
    subs = hg_index(HG_SUBSCRIPTS, "subscript")
    order = lines_of(SUBSCRIPT_ORDER)
    for n in range(PLATINUM_SUBSCRIPTS):
        plat = os.path.join(PLAT_SUBSCRIPTS, order[n] + ".s")
        if n in subs and os.path.exists(plat):
            pairs.append((("subscript", n), subs[n][1], plat))
    return pairs


def platinum_subscript_file(enum_name):
    """The file behind a Platinum BATTLE_SUBSCRIPT_ name, or None."""
    enum, order = lines_of(SUBSCRIPT_ENUM), lines_of(SUBSCRIPT_ORDER)
    if enum_name not in enum:
        return None
    return os.path.join(PLAT_SUBSCRIPTS, order[enum.index(enum_name)] + ".s")


def hg_pointer_targets():
    """hg-engine's side-effect pointer to subscript table, from its moves.c."""
    text = open(HG_POINTER_TABLE, encoding="utf-8", errors="replace").read()
    return dict(re.findall(r"^\s*\[(MOVE_SUBSCRIPT_PTR_\w+)\]\s*=\s*(BATTLE_SUBSCRIPT_\w+)",
                           text, re.M))


def register_subscript(name, text):
    """Write a new subscript and append it to the three lists that number it.
    The order file and the enum are positional and must grow together; the
    meson list only has to contain the file."""
    base = "subscript_" + name.lower()
    path = os.path.join(PLAT_SUBSCRIPTS, base + ".s")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    for list_file, entry in ((SUBSCRIPT_ORDER, base), (SUBSCRIPT_ENUM, "BATTLE_SUBSCRIPT_" + name)):
        with open(list_file, "a", encoding="utf-8", newline="\n") as f:
            f.write(entry + "\n")
    meson = open(SUBSCRIPT_MESON, encoding="utf-8").read().rstrip("\n")
    assert meson.endswith(")"), "subscripts meson.build no longer ends its list with )"
    meson = meson[:-1] + "    '%s.s',\n)\n" % base
    with open(SUBSCRIPT_MESON, "w", encoding="utf-8", newline="\n") as f:
        f.write(meson)
    return path


def register_pointer(pointer, subscript_enum):
    """Append a side-effect pointer and point it at a subscript. Nothing stores
    a pointer by number (scripts and this table both use the name), so a new
    one only has to be appended, and only pointers that have a subscript are
    added, which keeps the audit from counting an unimplemented one as there."""
    order, enum = lines_of(SUBSCRIPT_ORDER), lines_of(SUBSCRIPT_ENUM)
    target = order[enum.index(subscript_enum)]
    with open(POINTER_ENUM, "a", encoding="utf-8", newline="\n") as f:
        f.write(pointer + "\n")
    table = open(POINTER_TABLE, encoding="utf-8").read()
    width = re.search(r"^(    \[MOVE_SUBSCRIPT_PTR_NONE\]\s*)=", table, re.M).group(1)
    entry = ("    [%s]" % pointer).ljust(len(width)) + "= %s,\n" % target
    table = table.replace("};\n// clang-format on", entry + "};\n// clang-format on", 1)
    with open(POINTER_TABLE, "w", encoding="utf-8", newline="\n") as f:
        f.write(table)


def same_line(a, b):
    """Two script lines that mean the same thing. A `|`-joined flag list is a
    set, so `A|B` and `B|A` are the same line and a text comparison would call
    them different."""
    ha, aa = split_args(a)
    hb, ab = split_args(b)
    if ha != hb or len(aa) != len(ab):
        return False
    return all(set(x.split("|")) == set(y.split("|")) for x, y in zip(aa, ab))


def selftest(renames, skipped):
    """Convert the 277 effects both projects have and compare to Platinum's.

    Scored on the pairs that line up structurally, because those are the ones
    that say anything about the rename map. The rest are effects the two games
    implement differently, hg-engine having moved work out of the script that
    Platinum still does in it (effect 7, Selfdestruct, is the clearest: hg's is
    a bare hit, Platinum's carries the whole Damp check). A difference there is
    not a gap in the map and cannot be fixed by renaming anything.

    A map that rebuilds Platinum's own scripts from hg-engine's is good enough
    to bring the new ones across; that is the whole claim this test supports.
    """
    strings = battle_strings()
    exact, differ, structural = collections.Counter(), [], collections.Counter()
    for n, hg_path, plat in script_pairs():
        if n in skipped:
            structural[n[0]] += 1
            continue
        got = body_lines_from_text(convert(hg_path, renames, strings))
        want = body_lines(plat)
        if len(got) == len(want) and all(same_line(x, y) for x, y in zip(got, want)):
            exact[n[0]] += 1
        else:
            differ.append(n)
    return exact, differ, structural


def body_lines_from_text(text):
    out = []
    for line in text.splitlines():
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


PLAT_EFFECTS_OWNED = range(PLATINUM_EFFECTS, 407)   # the stubs element 4 created

# The two stubs element 4 wrote for every new effect: a plain hit, and a status
# move's "But nothing happened!". A script in the tree that is neither has been
# written, by `--write` or by hand, and the audit says so rather than offering
# to convert it again.
STUBS = (["_000:", "CalcCrit", "CalcDamage", "End"],
         ["_000:", "UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_SPLASH", "End"])

# Effects that are finished although the tree still holds a stub, because the
# work is in C or because the stub is already the right behaviour for Oxide.
SETTLED = {
    282: "always a critical hit, done in BattleSystem_CalcCriticalMulti",
    300: "a plain hit until Electric Terrain exists",
    307: "a plain hit of its own type; Drives are not in Oxide",
    308: "a plain hit of its own type; Memories are not in Oxide",
    405: "ignores Protect because its move record lacks MOVE_FLAG_CAN_PROTECT, as Feint's does",
}


def hg_move_names():
    """hg-engine's own MOVE_ constant for each move id, for finding where its C
    code names a move. Oxide's enum names differ in a few places (hg-engine's
    MOVE_GUARDIAN_OF_ALOLA is Oxide's MOVE_ALOLAN_GUARDIAN), so these have to
    come from hg-engine, not from generated/moves.txt."""
    out = {}
    for line in open(os.path.join(HG, "include", "constants", "moves.h"), encoding="utf-8"):
        m = re.match(r"#define\s+(MOVE_\w+)\s+(\d+)", line)
        if m:
            out.setdefault(int(m.group(2)), m.group(1))
    return out


def c_references(names):
    """Where hg-engine's C names each constant, split into behaviour and list
    membership. A line that is only `MOVE_X,` is an entry in an array (a
    Metronome ban list, the moves Iron Fist boosts), which belongs to whatever
    ability or item reads the list and says nothing about the move's own
    effect. Anything else (a `case`, a comparison) is behaviour."""
    import subprocess
    out = {}
    if not names:
        return out
    pattern = r"\b(" + "|".join(sorted(names)) + r")\b"
    found = subprocess.run(["grep", "-rnE", pattern, "src"], cwd=HG,
                           capture_output=True, text=True).stdout
    for line in found.splitlines():
        path, _, rest = line.split(":", 2)
        for name in re.findall(pattern, rest):
            kind = "list" if re.fullmatch(r"\s*\w+,?\s*(//.*)?", rest) else "code"
            out.setdefault(name, []).append((kind, os.path.basename(path)))
    return out


def oxide_effect_users():
    """Oxide's own moves by the effect id they use. The audit's list of effects
    comes from the donor's move records, which is 116, but Oxide's native moves
    keep Platinum's effects, so two of the 116, the donor's Howl and Tail Glow
    effects, have no user here (2026-09-22)."""
    import json
    effects = lines_of(os.path.join(ROOT, "generated", "move_battle_effects.txt"))
    out = collections.defaultdict(list)
    for p in glob.glob(os.path.join(ROOT, "res", "moves", "*", "data.json")):
        name = json.load(open(p, encoding="utf-8"))["effect"]["type"]
        if name in effects:
            out[effects.index(name)].append(os.path.basename(os.path.dirname(p)))
    return out


def unaimed(line):
    """Trap 2 of the element 4 brief, as a check. A side effect set with
    neither MOVE_SIDE_EFFECT_TO_ATTACKER nor TO_DEFENDER gets battler slot 0 as
    its side-effect battler in Platinum's engine. That is harmless when the
    subscript names its battler itself (Giga Drain's drain names the attacker)
    and wrong when it acts on the side-effect battler before setting one, which
    is what Hyperspace Fury's did (2026-09-22). Returns a reason, or None."""
    m = re.match(r"UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_(?:DIRECT|INDIRECT), (\S+)$", line)
    if not m or "TO_ATTACKER" in m.group(1) or "TO_DEFENDER" in m.group(1):
        return None
    ptr = [f for f in m.group(1).split("|") if f.startswith("MOVE_SUBSCRIPT_PTR_")]
    if not ptr:
        return None
    table = open(POINTER_TABLE, encoding="utf-8").read()
    target = re.search(r"\[%s\]\s*=\s*(\w+)," % re.escape(ptr[0]), table)
    path = target and os.path.join(PLAT_SUBSCRIPTS, target.group(1) + ".s")
    if not path or not os.path.exists(path):
        return None
    for l in body_lines(path):
        if "BTLVAR_SIDE_EFFECT_MON" in l and l.startswith("UpdateVarFromVar OPCODE_SET"):
            return None
        if "BTLSCR_SIDE_EFFECT_MON" in l or l == "Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE":
            return "%s aimed at no battler, so at slot 0" % ptr[0]
    return None


def oxide_effect_learners():
    """Effect id to the Oxide species that learn a move using it, from every
    list in every species' learnset. No trainer party, gift or field script
    uses a new move (checked 2026-09-22), so a learnset is the only way a
    player meets one; Metronome aside."""
    import json
    effects = lines_of(os.path.join(ROOT, "generated", "move_battle_effects.txt"))
    effect_of = {}
    for p in glob.glob(os.path.join(ROOT, "res", "moves", "*", "data.json")):
        name = json.load(open(p, encoding="utf-8"))["effect"]["type"]
        if name in effects:
            effect_of["MOVE_" + os.path.basename(os.path.dirname(p)).upper()] = effects.index(name)
    out = collections.defaultdict(set)
    for p in glob.glob(os.path.join(ROOT, "res", "pokemon", "*", "data.json")):
        learnset = json.dumps(json.load(open(p, encoding="utf-8")).get("learnset", {}))
        for move in set(re.findall(r"MOVE_\w+", learnset)):
            if move in effect_of:
                out[effect_of[move]].add(os.path.basename(os.path.dirname(p)))
    return out


def check_script(text, have):
    """The names a converted script uses that Platinum lacks, and the message
    numbers it still prints. After conversion a bare number in a message
    command can only be past the end of Platinum's bank, so it is a string
    Platinum does not have. Only PrintMessage was checked until 2026-09-22,
    which let Geomancy's BufferMessage 1436 through."""
    lines = body_lines_from_text(text)
    labels = {l[:-1] for l in lines if l.endswith(":")}
    unresolved, messages = set(), []
    for l in lines:
        if l.endswith(":"):
            continue
        head, args = split_args(l)
        why = unaimed(l)
        if why:
            unresolved.add(why)
        if head not in have:
            unresolved.add(head)
        for a in args:
            # A hex number is matched whole first, so its digits after the x
            # are not read as a name (they were, until 2026-09-22).
            for t in re.findall(r"\b0[xX][0-9A-Fa-f]+\b|[A-Za-z_]\w*", a):
                if t[:2] in ("0x", "0X") or t in labels or t in have:
                    continue
                unresolved.add(t)
        at = MESSAGE_ARG.get(head)
        if at is not None and len(args) > at and re.fullmatch(r"\d+", args[at]):
            messages.append(int(args[at]))
        for at in VARIABLE_ARGS.get(head, ()):
            if len(args) > at and re.fullmatch(r"-?\d+", args[at]):
                unresolved.add("%s with a bare number %s where a variable goes"
                               % (head, args[at]))
    return unresolved, messages


def hg_subscript(name):
    """hg-engine's subscript by name (with or without BATTLE_SUBSCRIPT_) or
    number, as (name, path)."""
    subs = hg_index(HG_SUBSCRIPTS, "subscript")
    if re.fullmatch(r"\d+", name):
        return subs[int(name)]
    name = name.replace("BATTLE_SUBSCRIPT_", "")
    for n, (hg_name, path) in subs.items():
        if hg_name == name:
            return hg_name, path
    sys.exit("hg-engine has no subscript %s" % name)


def audit(ids, renames, have):
    """What stands between each hg-engine effect and a working Platinum one.

    `ready` means the converted script uses only names Platinum has, prints no
    message by raw number, and hg-engine's C never implements part of the
    effect itself, keyed on either the effect's id or one of its moves. It
    does not mean the move has been tried in a battle.
    """
    import donor_moves
    effects = hg_index(HG_EFFECTS, "effect_script")
    dm = donor_moves.DonorMoves()
    recs = dm.moves()
    mnames = hg_move_names()
    users = collections.defaultdict(list)
    for i, r in enumerate(recs):
        if 0 < i <= 922:
            users[r["effect"]].append(i)
    effect_const = {e: "MOVE_EFFECT_" + effects[e][0] for e in ids}
    move_consts = {mnames[i] for e in ids for i in users[e] if i in mnames}
    refs = c_references(set(effect_const.values()) | move_consts)

    strings = battle_strings()
    oxide_users = oxide_effect_users()
    learners = oxide_effect_learners()
    rows = []
    for e in ids:
        unresolved, messages = check_script(convert(effects[e][1], renames, strings), have)
        items = {t for t in unresolved if t.startswith("HOLD_EFFECT_")}
        unresolved -= items
        code = sorted({f for n in [effect_const[e]] + [mnames.get(i) for i in users[e]]
                       for kind, f in refs.get(n, []) if kind == "code"})
        tree = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % e)
        if e in SETTLED:
            verdict = "settled"
        elif os.path.exists(tree) and body_lines(tree) not in STUBS:
            verdict = "done"
        elif e not in oxide_users:
            verdict = "unused"
        elif e not in learners:
            # Ian, 2026-09-22: an effect only Metronome can reach is not
            # ported. Computed, so one comes back if a later TM or tutor pass
            # makes one of its moves learnable.
            verdict = "unreachable"
        elif items:
            verdict = "items"
        elif unresolved:
            verdict = "names"
        elif messages:
            verdict = "text"
        elif code:
            verdict = "c"
        else:
            verdict = "ready"
        rows.append(dict(id=e, name=effects[e][0], verdict=verdict,
                         unresolved=sorted(unresolved), messages=messages,
                         items=sorted(items), code=code,
                         moves=[dm.names()[i] for i in users[e]][:3]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--audit", nargs="*", type=int, metavar="N",
                    help="triage hg-engine effects (default: every one Oxide's moves use)")
    ap.add_argument("--write", nargs="+", type=int, metavar="N",
                    help="convert these effects into res/battle/scripts/effects; "
                         "refuses any the audit does not call ready")
    ap.add_argument("--map", action="store_true", help="print the derived renames")
    ap.add_argument("--selftest", action="store_true",
                    help="convert the shared 277 effects and compare to Platinum's")
    ap.add_argument("--show", type=int, metavar="N",
                    help="print the conversion of hg-engine effect N")
    ap.add_argument("--show-sub", metavar="NAME",
                    help="print the conversion of hg-engine subscript NAME (or its number)")
    ap.add_argument("--write-sub", nargs="+", metavar="NAME",
                    help="convert these hg-engine subscripts into Platinum's and register "
                         "them; refuses any that use a name Platinum lacks")
    ap.add_argument("--add-ptr", nargs="+", metavar="POINTER",
                    help="append these side-effect pointers, each aimed at the subscript "
                         "hg-engine gives it; refuses one whose subscript Platinum lacks")
    a = ap.parse_args()

    if not os.path.isdir(HG_EFFECTS):
        sys.exit("no hg-engine checkout at %s; set HG_ENGINE or clone it "
                 "(see the tracker's element 4 entry)" % HG)

    renames, aligned, skipped, conflicts = derive_renames()
    # The summary goes to stderr: `--show N > effect_script_NNNN.s` must leave
    # nothing but the script on stdout (2026-09-22 review finding).
    print("rename map: %d entries, derived from %d aligned script pairs of %d; "
          "%d pairs differ in shape and were not used"
          % (len(renames), aligned, len(script_pairs()), len(skipped)), file=sys.stderr)
    if conflicts:
        print("AMBIGUOUS, the map is not trustworthy until these are resolved:", file=sys.stderr)
        for x, ys in conflicts.items():
            print("    %-44s %s" % (x, ys), file=sys.stderr)

    have = platinum_identifiers()
    renames = supplemented(renames, have)

    if a.audit is not None or a.write:
        import donor_moves
        recs = donor_moves.DonorMoves().moves()
        wanted = sorted({r["effect"] for r in recs[1:923] if r["effect"] >= PLATINUM_EFFECTS})
        rows = audit(a.audit or wanted, renames, have)
        if a.audit is not None:
            order = ["done", "settled", "unused", "unreachable", "ready", "c", "text", "names", "items"]
            for v in order:
                group = [r for r in rows if r["verdict"] == v]
                if not group:
                    continue
                print("%s: %d" % (v, len(group)))
                for r in group:
                    why = {"done": "", "settled": SETTLED.get(r["id"], ""), "ready": "",
                           "unused": "no Oxide move uses it",
                           "unreachable": "no Oxide species learns a move that uses it",
                           "c": ("C reviewed: " + C_REVIEWED[r["id"]]) if r["id"] in C_REVIEWED
                                else "C: " + ", ".join(r["code"]),
                           "text": "messages %s" % r["messages"],
                           "names": "unresolved: " + ", ".join(r["unresolved"]),
                           "items": "items: " + ", ".join(r["items"][:3])}[v]
                    print("    %d %-38s %-34s %s" % (r["id"], r["name"],
                                                    ", ".join(r["moves"])[:34], why))
        if a.write:
            verdicts = {r["id"]: r["verdict"] for r in audit(a.write, renames, have)}
            refused = [e for e in a.write
                       if verdicts[e] != "ready" and not (verdicts[e] == "c" and e in C_REVIEWED)]
            if refused:
                sys.exit("refusing %s: the audit does not call them ready" % refused)
            effects = hg_index(HG_EFFECTS, "effect_script")
            for e in a.write:
                if e not in PLAT_EFFECTS_OWNED:
                    sys.exit("%d is not one of the stubs element 4 created" % e)
                out = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % e)
                with open(out, "w", encoding="utf-8", newline="\n") as f:
                    f.write(convert(effects[e][1], renames))
            print("wrote %d effect scripts" % len(a.write), file=sys.stderr)

    if a.map:
        for x, y in sorted(renames.items()):
            print("    %-46s -> %s" % (x, y))
    if a.show is not None:
        effects = hg_index(HG_EFFECTS, "effect_script")
        sys.stdout.write(convert(effects[a.show][1], renames))
    if a.show_sub is not None:
        sys.stdout.write(convert(hg_subscript(a.show_sub)[1], renames))
    if a.write_sub:
        strings = battle_strings()
        enum = set(lines_of(SUBSCRIPT_ENUM))
        for name in a.write_sub:
            hg_name, path = hg_subscript(name)
            if "BATTLE_SUBSCRIPT_" + hg_name in enum:
                sys.exit("refusing %s: Platinum already has it" % hg_name)
            unresolved, messages = check_script(convert(path, renames, strings), have)
            if unresolved or messages:
                sys.exit("refusing %s: unresolved %s, hg-engine messages %s"
                         % (hg_name, sorted(unresolved), messages))
        for name in a.write_sub:
            hg_name, path = hg_subscript(name)
            out = register_subscript(hg_name, convert(path, renames, strings))
            print("wrote %s" % os.path.relpath(out, ROOT), file=sys.stderr)
    if a.add_ptr:
        targets = hg_pointer_targets()
        enum_ptrs = set(lines_of(POINTER_ENUM))
        enum_subs = set(lines_of(SUBSCRIPT_ENUM))
        plan = []
        for p in a.add_ptr:
            if p in enum_ptrs:
                sys.exit("refusing %s: Platinum already has it" % p)
            if p not in targets:
                sys.exit("refusing %s: hg-engine's table does not map it" % p)
            sub = renames.get(targets[p], targets[p])
            if sub == "BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE":
                # hg-engine decodes the stat and the amount from the pointer in
                # C, and Platinum's ChangeStatStage decodes only the ranges it
                # names; an unknown pointer there indexes past the stat array.
                # The three-stage ranges were taught on 2026-09-22, and they
                # must be appended whole and in hg-engine's order, which is
                # Platinum's stat order.
                known = open(os.path.join(ROOT, "src", "battle", "battle_script.c"),
                             encoding="utf-8").read()
                stages = re.search(r"_(UP|DOWN)_(\d)_STAGES?$", p)
                if not stages or ("MOVE_SUBSCRIPT_PTR_ATTACK_%s_%s_STAGES" % stages.groups()) not in known:
                    sys.exit("refusing %s: ChangeStatStage does not know its range" % p)
            if sub not in enum_subs:
                sys.exit("refusing %s: its subscript %s is not in Platinum yet" % (p, sub))
            plan.append((p, sub))
        for p, sub in plan:
            register_pointer(p, sub)
            print("added %s -> %s" % (p, sub), file=sys.stderr)
    if a.selftest:
        exact, differ, structural = selftest(renames, set(skipped))
        for kind in ("effect", "subscript"):
            d = [n for k, n in differ if k == kind]
            print("selftest, %ss: of the %d shared %ss that line up structurally, "
                  "%d convert to Platinum's own script exactly and %d differ%s"
                  % (kind, exact[kind] + len(d), kind, exact[kind], len(d),
                     (" (%s)" % d) if d else ""))
            print("  %d more were not scored: the two games implement those "
                  "differently, which no rename can fix" % structural[kind])
        return 0 if not differ else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
