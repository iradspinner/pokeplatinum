#!/usr/bin/env python3
"""Read pokeplatinum's field-script bytecode.

Platinum Oxide project. `scr_seq.narc` holds compiled field scripts; the decomp
keeps them as macro assembly in `res/field/scripts/scripts_<map>.s`. Carrying
over the base ROM's 91 edited scripts means reading the bytecode back, so this
builds the command table from the repo's own two sources of truth and walks a
script file with it.

The command table is generated, never hand-written. `include/data/scripts/scrcmd.h`
lists every command in opcode order; `asm/macros/scrcmd.inc` gives each one's
operand widths, which is what decides where the next command starts. Getting a
width wrong does not fail loudly, it silently desynchronises the rest of the
file, so the table has to come from the same files the assembler uses.

Usage:
    python3 tools/oxide/scriptdis.py --rom ROM.nds [--index N] [--verify]

Run from the repository root. Requires ndspy.
"""
import argparse
import os
import re
import struct
import sys

ROOT = os.getcwd()

SCRIPTS_NARC = "fielddata/script/scr_seq.narc"
SCRIPT_ENTRY_END = 0xFD13

# Operand kinds, and how many bytes each takes.
WIDTHS = {"byte": 1, "short": 2, "long": 4, "rel": 4}


# Six commands take a different number of operands depending on the value of an
# earlier one; asm/macros/scrcmd.inc spells them as .if blocks. The constants
# come from include/constants/scrcmd.h, include/constants/records_mixed_rng.h
# and generated/mystery_gift_delivery_stages.h.
FIELD_MOVE_FUNC_CHECK_ACTIVE = 2
GC_ACTION_TWO_EXTRA = (0, 1, 2, 3)  # check entry valid/override, buffer group/leader name
GC_ACTION_ONE_EXTRA = (4, 5)  # open group naming screen, join group
TV_ONE_EXTRA = (0, 6)
TV_THREE_EXTRA = (1, 3, 5)
TV_TWO_EXTRA = (4,)
MYSTERY_GIFT_ONE_EXTRA = (1, 2, 3)  # check available pgt, get pgt type, check can receive
MYSTERY_GIFT_TWO_EXTRA = (5, 6)  # received, cant receive


def _extra_field_move(values):
    return [("short", "checkDestVarID")] if values[0] == FIELD_MOVE_FUNC_CHECK_ACTIVE else []


def _extra_group_connection(values):
    if values[0] in GC_ACTION_TWO_EXTRA:
        return [("short", "arg1"), ("short", "arg2")]
    if values[0] in GC_ACTION_ONE_EXTRA:
        return [("short", "arg1")]
    return []


def _extra_tv_broadcast(values):
    if values[0] in TV_ONE_EXTRA:
        return [("short", "arg1")]
    if values[0] in TV_THREE_EXTRA:
        return [("short", "arg1"), ("short", "arg2"), ("short", "arg3")]
    if values[0] in TV_TWO_EXTRA:
        return [("short", "arg1"), ("short", "arg2")]
    return []


def _extra_mystery_gift(values):
    if values[0] in MYSTERY_GIFT_ONE_EXTRA:
        return [("short", "destVar1ID")]
    if values[0] in MYSTERY_GIFT_TWO_EXTRA:
        return [("short", "destVar1ID"), ("short", "destVar2ID")]
    return []


CONDITIONAL = {
    "SCRCMD_DOSTRENGTHFUNC": _extra_field_move,
    "SCRCMD_DOFLASHFUNC": _extra_field_move,
    "SCRCMD_DODEFOGFUNC": _extra_field_move,
    "SCRCMD_DOGROUPCONNECTIONACTION": _extra_group_connection,
    "SCRCMD_CALLTVBROADCAST": _extra_tv_broadcast,
    "SCRCMD_MYSTERYGIFTGIVE": _extra_mystery_gift,
}


# Commands whose operands the base ROM changed, keyed by the constant name.
# Applied with --base-rom, because the same opcode means different things in the
# two ROMs and decoding one with the other's table desynchronises the file.
#
# SCRCMD_DUMMY088: vanilla's ScrCmd_Dummy088 reads three halfwords and does
# nothing with them. The base ROM overwrites its body (arm9 0x0204EAE8) with a
# 60-byte routine that reads no operands at all: it writes one byte, taken from
# the synthetic overlay at 0x023D28FF, to *(u32 *)0x02101D40 + 0x8087. So in the
# base ROM the command is two bytes and nothing follows it.
#
# This is the answer to the long-open Battle Arcade question. It is called three
# times, all in scripts_common, and it is the only custom command any script in
# the base ROM calls. Two independent things agree on the operand count: the
# routine never touches the script context, and reading it as two bytes makes
# the surrounding code decode as RemoveItem / BufferPlayerName / BufferItemName
# / Message, where reading it as eight swallows the RemoveItem whole.
BASE_ROM_OVERRIDES = {
    "SCRCMD_DUMMY088": [],
}


class Command:
    def __init__(self, opcode, const, macro, operands, params=()):
        self.opcode = opcode
        self.const = const
        self.macro = macro
        self.operands = operands  # [(kind, arg name)]
        # the macro's declared parameters, in order. Emitting has to go by this
        # rather than by the order fields come out, because a macro can emit a
        # constant that is not a parameter at all (ChooseTwoCustomMessageWords
        # starts with an unused zero) or emit the same parameter twice
        # (ShowCurrentFloor writes destVarID and then writes it again).
        self.params = list(params)

    @property
    def conditional(self):
        return CONDITIONAL.get(self.const)

    def __repr__(self):
        return f"<{self.opcode:#05x} {self.macro}>"


def build_command_table(base_rom=False):
    """opcode -> Command, from the repo's own two sources."""
    header = open(os.path.join(ROOT, "include", "data", "scripts", "scrcmd.h")).read()
    order = [m.group(1) for m in re.finditer(r"^ScriptCommand\((\w+)\s*,", header, re.M)]

    inc = open(os.path.join(ROOT, "asm", "macros", "scrcmd.inc")).read()
    blocks = re.findall(r"^    \.macro\s+(\S+)([^\n]*)\n(.*?)^    \.endm", inc, re.S | re.M)

    by_const = {}
    for macro, _args, body in blocks:
        lines = [l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith("@")]
        if not lines:
            continue
        head = re.match(r"\.short\s+(\w+)$", lines[0])
        if head is None:
            continue  # a wrapper macro that expands to other macros
        const = head.group(1)
        operands = []
        for line in lines[1:]:
            if re.match(r"\.(if|else|endif)\b", line):
                continue  # handled by CONDITIONAL, keyed on const
            part = re.match(r"\.(byte|short|long)\s+(.*)$", line)
            if part is None:
                continue
            kind = part.group(1)
            # several macros annotate a field in place, and the comment would
            # otherwise end up glued to the parameter name and stop it matching
            # the macro's declared parameter list
            expr = re.sub(r"(/\*.*?\*/|//.*|@.*)", "", part.group(2)).strip()
            if expr.endswith("-.-4"):
                kind = "rel"
                expr = expr[: -len("-.-4")]
            operands.append((kind, expr.lstrip("\\")))
        params = []
        for arg in _args.split(","):
            arg = arg.strip().split("=")[0].strip()
            if arg:
                params.append(arg)
        by_const.setdefault(const, (macro, operands, params))

    table = {}
    for opcode, const in enumerate(order):
        if const not in by_const:
            continue
        macro, operands, params = by_const[const]
        if const in CONDITIONAL:
            # the .if body is reconstructed at decode time, so keep only what
            # comes before it
            operands = operands[:1]
        if base_rom and const in BASE_ROM_OVERRIDES:
            operands = list(BASE_ROM_OVERRIDES[const])
        table[opcode] = Command(opcode, const, macro, operands, params)
    return table


TABLE = None
TABLE_IS_BASE_ROM = False


def use_base_rom_table(enabled=True):
    """Switch to the base ROM's command meanings; see BASE_ROM_OVERRIDES."""
    global TABLE, TABLE_IS_BASE_ROM
    if enabled != TABLE_IS_BASE_ROM:
        TABLE = None
        TABLE_IS_BASE_ROM = enabled


def table():
    global TABLE
    if TABLE is None:
        TABLE = build_command_table(TABLE_IS_BASE_ROM)
    return TABLE


# Commands that end a straight-line run. Anything else falls through to the next
# command in memory.
TERMINATORS = {"SCRCMD_END", "SCRCMD_RETURN", "SCRCMD_GOTO", "SCRCMD_RETURNCOMMONSCRIPT"}

# Only these hand a relative offset to more script code. Other commands with a
# relative operand point at movement data or other tables, which is a different
# encoding and must not be walked as code.
def is_code_target(cmd, arg_name):
    if arg_name in ("movementOffset",):
        return False
    return cmd.macro.startswith(("GoTo", "Call", "JumpTo")) or cmd.const in ("SCRCMD_GOTO", "SCRCMD_CALL")


# ---------------------------------------------------------------- movement
#
# ApplyMovement points at a movement block, which is a different and far simpler
# encoding: pairs of (u16 action, u16 length) ending with MOVEMENT_ACTION_END
# and a zero length. asm/macros/movement.inc has one macro per action, and the
# ids come from generated/movement_actions.h.
MOVEMENT_TABLE = None


def build_movement_table():
    """action id -> macro name, from asm/macros/movement.inc."""
    inc = open(os.path.join(ROOT, "asm", "macros", "movement.inc")).read()
    blocks = re.findall(r"^    \.macro\s+(\S+)([^\n]*)\n(.*?)^    \.endm", inc, re.S | re.M)
    names = {}
    for macro, _args, body in blocks:
        head = re.search(r"\.short\s+(MOVEMENT_ACTION_\w+)", body)
        if head:
            names.setdefault(head.group(1), macro)

    header = open(os.path.join(ROOT, "build", "generated", "movement_actions.h")).read()
    found = re.search(r"enum \w+ \{(.*?)\};", header, re.S)
    table = {}
    values = {}
    for line in found.group(1).splitlines():
        entry = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*(.+?),?\s*$", line)
        if entry:
            value = eval(entry.group(2), {"__builtins__": {}}, dict(values))
            values[entry.group(1)] = value
            if entry.group(1) in names:
                table[value] = names[entry.group(1)]
    return table, values.get("MOVEMENT_ACTION_END")


MOVEMENT_END = None


def movement_table():
    global MOVEMENT_TABLE, MOVEMENT_END
    if MOVEMENT_TABLE is None:
        MOVEMENT_TABLE, MOVEMENT_END = build_movement_table()
    return MOVEMENT_TABLE


def decode_movement(buf, offset):
    """[(macro name, length)] and the block's size in bytes."""
    actions = []
    pos = offset
    while True:
        if pos + 4 > len(buf):
            raise ValueError(f"movement block at {offset:#06x} runs past the end of the file")
        action, length = struct.unpack_from("<2H", buf, pos)
        pos += 4
        name = movement_table().get(action)
        if name is None:
            raise KeyError(f"unknown movement action {action:#06x} at {pos - 4:#06x}")
        actions.append((name, length))
        if action == MOVEMENT_END:
            return actions, pos - offset


class DecodedCommand:
    def __init__(self, offset, size, cmd, values, targets):
        self.offset = offset
        self.size = size
        self.cmd = cmd
        self.values = values  # [(kind, arg name, value)]
        self.targets = targets  # absolute offsets this command points at

    def __repr__(self):
        return f"{self.offset:#06x} {self.cmd.macro} {[v for _, _, v in self.values]}"


def script_entries(buf):
    """The offsets of each ScriptEntry in a script file's header table, where
    the table ends, and whether it closed with an explicit ScriptEntryEnd.

    ScriptEntryEnd is optional: plenty of files just run the first script
    straight after the last entry, so the table also ends as soon as the
    position reaches the nearest target any entry points at."""
    entries = []
    pos = 0
    limit = len(buf)
    while pos + 2 <= len(buf):
        if struct.unpack_from("<H", buf, pos)[0] == SCRIPT_ENTRY_END:
            return entries, pos + 2, True
        if pos >= limit:
            return entries, pos, False
        if pos + 4 > len(buf):
            break
        (rel,) = struct.unpack_from("<i", buf, pos)
        target = pos + 4 + rel
        if not (0 < target <= len(buf)):
            raise ValueError(f"script entry {len(entries)} points outside the file ({target:#x})")
        entries.append(target)
        limit = min(limit, target)
        pos += 4
    raise ValueError("ran off the end while reading the script entry table")


def is_init_script(name):
    """The same archive holds two unrelated formats. A map header points at its
    script file and its init-script file separately, and the repo names the
    latter scripts_init_*."""
    return name.startswith("scripts_init")


def init_script_entries(buf):
    """Init scripts are a flat list of five-byte entries (a type byte then two
    shorts) closed by a zero byte, per InitScriptEntry_Fixed and
    InitScriptEntryEnd."""
    entries = []
    pos = 0
    while pos < len(buf):
        if buf[pos] == 0:
            return entries, pos + 1
        if pos + 5 > len(buf):
            raise ValueError("init script entry runs past the end of the file")
        kind, script_id, pad = struct.unpack_from("<BHH", buf, pos)
        entries.append((kind, script_id, pad))
        pos += 5
    raise ValueError("init script has no terminating zero byte")


def decode_command(buf, offset):
    """Decode one command. Returns a DecodedCommand, or raises on an opcode the
    table does not know."""
    (opcode,) = struct.unpack_from("<H", buf, offset)
    cmd = table().get(opcode)
    if cmd is None:
        raise KeyError(f"unknown opcode {opcode:#06x} at {offset:#06x}")
    pos = offset + 2
    values = []
    targets = []
    operands = list(cmd.operands)
    extra = cmd.conditional
    while operands:
        kind, name = operands.pop(0)
        width = WIDTHS[kind]
        if pos + width > len(buf):
            raise ValueError(f"{cmd.macro} at {offset:#06x} runs past the end of the file")
        fmt = {"byte": "<B", "short": "<H", "long": "<I", "rel": "<i"}[kind]
        (value,) = struct.unpack_from(fmt, buf, pos)
        # a relative offset is measured from just past the operand itself, which
        # is what `.long \target-.-4` assembles to
        if kind == "rel" and is_code_target(cmd, name):
            targets.append(pos + 4 + value)
        values.append((kind, name, value))
        pos += width
        if extra is not None and not operands:
            operands = extra([v for _, _, v in values])
            extra = None
    return DecodedCommand(offset, pos - offset, cmd, values, targets)


def walk(buf, with_movement=True):
    """Follow every script entry and every code target reachable from one.
    Returns {offset: DecodedCommand}, the set of offsets that need a label when
    this is written back out, the end of the header table, and the movement
    blocks ApplyMovement points at as {offset: (actions, size)}."""
    entries, header_end, _terminated = script_entries(buf)
    decoded = {}
    movements = {}
    labels = set(entries)
    work = list(entries)
    while work:
        offset = work.pop()
        while True:
            if offset in decoded or offset >= len(buf):
                break
            if offset < header_end:
                raise ValueError(f"control flow reaches the header table at {offset:#06x}")
            dc = decode_command(buf, offset)
            decoded[offset] = dc
            for target in dc.targets:
                labels.add(target)
                if target not in decoded:
                    work.append(target)
            if with_movement:
                pos = dc.offset + 2
                for kind, name, value in dc.values:
                    if kind == "rel" and not is_code_target(dc.cmd, name):
                        target = pos + 4 + value
                        labels.add(target)
                        if target not in movements:
                            movements[target] = decode_movement(buf, target)
                    pos += WIDTHS[kind]
            if dc.cmd.const in TERMINATORS:
                break
            offset += dc.size
    return decoded, labels, header_end, movements


def sweep_leftovers(buf, decoded, movements, header_end):
    """Account for what the reachable walk does not reach.

    Two things end up here, both real source that has to be emitted again if
    these files are ever to reassemble. Unreachable commands: an `End` written
    after an unconditional `GoTo` is never reached, but it is in the source.
    And movement blocks nothing reachable points at.

    This is a recovery pass, not a walk, so it is deliberately strict: a region
    is only claimed if it decodes *exactly*, filling the gap with nothing left
    over. Anything that does not is reported rather than guessed at.
    """
    covered = bytearray(len(buf))
    for i in range(header_end):
        covered[i] = 1
    for dc in decoded.values():
        for i in range(dc.offset, dc.offset + dc.size):
            covered[i] = 1
    for offset, (_actions, size) in movements.items():
        for i in range(offset, offset + size):
            covered[i] = 1

    extra_commands, extra_movements, unclaimed = {}, {}, []
    i = 0
    while i < len(buf):
        if covered[i]:
            i += 1
            continue
        j = i
        while j < len(buf) and not covered[j]:
            j += 1
        region = (i, j)
        # a region often opens with the `.balign 4, 0` that precedes whatever
        # follows, and closes with more of the same before the next block
        # a region often opens with the `.balign 4, 0` that precedes whatever
        # follows, and can close with more padding before the next block. Only
        # leading zeros are skipped outright; trailing ones are allowed for by
        # letting the decode stop early as long as nothing but zeros is left.
        # Stripping trailing zeros instead would eat the second byte of End.
        start = i
        while start < j and buf[start] == 0:
            start += 1
        if start == j:
            i = j  # all padding
            continue

        def fills(decoder, into):
            pos, found = start, {}
            while pos < j:
                try:
                    item = decoder(buf, pos)
                except Exception:
                    break
                size = item.size if hasattr(item, "size") else item[1]
                found[pos] = item
                pos += size
            if pos <= j and not any(buf[pos:j]):
                into.update(found)
                return True
            return False

        # several movement blocks can sit back to back with nothing referring to
        # the later ones
        if not fills(decode_movement, extra_movements):
            if not fills(decode_command, extra_commands):
                unclaimed.append((i, j))
        i = j
    return extra_commands, extra_movements, unclaimed


def coverage(buf):
    """How much of a script file the walk accounts for: the header table, every
    command reached from an entry, and every movement block pointed at. What is
    left should only be the `.balign 4, 0` padding between movement blocks and
    the odd run of unreferenced Noop."""
    decoded, labels, header_end, movements = walk(buf)
    extra_cmds, extra_moves, unclaimed = sweep_leftovers(buf, decoded, movements, header_end)
    decoded = {**decoded, **extra_cmds}
    movements = {**movements, **extra_moves}
    covered = bytearray(len(buf))
    for dc in decoded.values():
        for i in range(dc.offset, dc.offset + dc.size):
            covered[i] = 1
    for offset, (_actions, size) in movements.items():
        for i in range(offset, offset + size):
            covered[i] = 1
    for i in range(header_end):
        covered[i] = 1
    # zero bytes between blocks are the assembler's `.balign 4, 0`
    for i in range(len(buf)):
        if not covered[i] and buf[i] == 0:
            covered[i] = 1
    return decoded, labels, movements, sum(covered), len(buf), unclaimed


# ---------------------------------------------------------------- symbols
#
# Which operands are worth spelling out, keyed by the macro's own parameter
# name. Anything not listed, or whose value is not in the table it names, stays
# a plain number: a wrong symbol is worse than a number, and the round trip is
# what proves each of these resolves back to the same bytes.
VARS_START = 0x4000

SYMBOLIC = {
    "varID": "var", "destVarID": "var", "srcVarID": "var", "destVar": "var",
    "countdownVarID": "var", "checkDestVarID": "var", "destVar1ID": "var",
    "destVar2ID": "var", "resultVar": "var", "varID1": "var", "varID2": "var",
    "flagID": "flag",
    "item": "items", "itemID": "items",
    "species": "species", "speciesID": "species",
    "moveID": "moves", "move": "moves",
    "trainerID": "trainers", "trainerID1": "trainers", "trainerID2": "trainers",
    "seqID": "sound",
    "localID": "localid",
}

# LOCALID_* names are generated per map from that map's event file, so only the
# three the engine defines for everyone can be spelled here.
GLOBAL_LOCAL_IDS = {0xF1: "LOCALID_CAMERA", 0xF2: "LOCALID_FOLLOWER", 0xFF: "LOCALID_PLAYER"}

SYMBOL_TABLES = {}


def symbol_table(kind):
    """value -> name for one of the tables SYMBOLIC names."""
    if kind in SYMBOL_TABLES:
        return SYMBOL_TABLES[kind]
    table = {}
    if kind in ("var", "flag"):
        values = load_enum_values_local("vars_flags")
        for name, value in values.items():
            # vars and flags share one enum but not one number line, so each
            # side only offers the half that can legitimately appear
            if kind == "var" and value >= VARS_START:
                table.setdefault(value, name)
            elif kind == "flag" and value < VARS_START:
                table.setdefault(value, name)
    elif kind == "sound":
        # generated by nitrosfx from the sdat; names are a mix of SEQ_* and SE_*
        naix = os.path.join(ROOT, "build", "res", "sound", "pl_sound_data.naix")
        for line in open(naix):
            entry = re.match(r"#define\s+(\w+)\s+(\d+)\s*$", line)
            if entry:
                table.setdefault(int(entry.group(2)), entry.group(1))
    elif kind == "localid":
        table = dict(GLOBAL_LOCAL_IDS)
    else:
        for name, value in load_enum_values_local(kind).items():
            table.setdefault(value, name)
    SYMBOL_TABLES[kind] = table
    return table


def load_enum_values_local(name):
    """NAME -> value for a generated enum, aliases included."""
    header = os.path.join(ROOT, "build", "generated", name + ".h")
    body = open(header).read()
    found = re.search(r"enum \w+ \{(.*?)\};", body, re.S)
    table = {}
    for line in found.group(1).splitlines():
        entry = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*(.+?),?\s*$", line)
        if entry:
            table[entry.group(1)] = eval(entry.group(2), {"__builtins__": {}}, dict(table))
    return table


def symbolic(param_name, value, enabled):
    """The name for this operand's value, or None to leave it a number."""
    if not enabled:
        return None
    kind = SYMBOLIC.get(param_name)
    if kind is None and (param_name.endswith("Var") or param_name.endswith("VarID")):
        kind = "var"  # selectedOptionVar, checkDestVarID and friends
    if kind is None:
        return None
    try:
        return symbol_table(kind).get(value)
    except Exception:
        return None


# ---------------------------------------------------------------- emitting
def emit_source(buf, prefix, includes=("macros/scrcmd.inc",), symbols=True):
    """Write a script file back out as macro assembly.

    Operands are emitted as plain numbers and labels rather than symbolic
    constants. That is deliberate for now: it keeps the round trip a test of
    structure - label placement, ordering, padding, the entry table - and not of
    a naming table that could paper over a structural mistake. Symbolic operands
    go on top once this reassembles byte for byte.
    """
    decoded, labels, header_end, movements = walk(buf)
    extra_cmds, extra_moves, unclaimed = sweep_leftovers(buf, decoded, movements, header_end)
    # A region the recovery pass could not read is emitted as raw bytes rather
    # than refused or guessed at. That keeps the output exact and says plainly
    # which bytes are not understood yet, instead of inventing a reading that
    # happens to assemble.
    raw = {a: bytes(buf[a:b]) for a, b in unclaimed}
    emit_source.last_raw = raw
    decoded = {**decoded, **extra_cmds}
    movements = {**movements, **extra_moves}
    entries, _header_end, terminated = script_entries(buf)

    # Name only what is actually pointed at. Naming every command would mean
    # emitting a label for each one; naming too few leaves a jump referring to a
    # label that was never written, which the linker catches but only after a
    # confusing detour. Targets are recollected here over the merged set,
    # because the recovery pass finds commands the walk never saw and those can
    # jump too.
    referenced = set(entries)
    for dc in decoded.values():
        at = dc.offset + 2
        for kind, name, value in dc.values:
            if kind == "rel" and is_code_target(dc.cmd, name):
                referenced.add(at + 4 + value)
            at += WIDTHS[kind]
    names = {}
    for i, offset in enumerate(entries):
        names.setdefault(offset, f"{prefix}_Entry{i}")
    for offset in sorted(movements):
        names[offset] = f"{prefix}_Movement_{offset:04X}"
    for offset in sorted(referenced):
        names.setdefault(offset, f"{prefix}_{offset:04X}")

    out = [f'#include "{inc}"' for inc in includes] + ["", ""]
    for i, offset in enumerate(entries):
        out.append(f"    ScriptEntry {names[offset]}")
    if terminated:
        out.append("    ScriptEntryEnd")
    out.append("")

    pos = header_end
    while pos < len(buf):
        if pos in movements:
            actions, size = movements[pos]
            out.append(f"{names[pos]}:")
            for action, length in actions:
                # EndMovement takes no argument; its macro emits the zero itself
                out.append(f"    {action}" if action == "EndMovement" else f"    {action} {length}")
            out.append("")
            pos += size
        elif pos in decoded:
            dc = decoded[pos]
            if pos in names:
                out.append(f"{names[pos]}:")
            # render each decoded field, then hand the macro its declared
            # parameters in its own order
            rendered, at = {}, dc.offset + 2
            for kind, name, value in dc.values:
                if kind == "rel":
                    target = at + 4 + value
                    rendered.setdefault(name, names.get(target, f"{target:#x}"))
                else:
                    rendered.setdefault(name, symbolic(name, value, symbols) or str(value))
                at += WIDTHS[kind]
            params = dc.cmd.params
            if dc.cmd.conditional:
                params = [p for p in params if p in rendered]
            args = [rendered[p] for p in params if p in rendered]
            out.append(f"    {dc.cmd.macro}" + (" " + ", ".join(args) if args else ""))
            pos += dc.size
        elif pos in raw:
            out.append(f"    @ not decoded: {len(raw[pos])} bytes")
            out.append("    .byte " + ", ".join(str(b) for b in raw[pos]))
            out.append("")
            pos += len(raw[pos])
        else:
            run = pos
            while run < len(buf) and run not in decoded and run not in movements and run not in raw:
                run += 1
            pad = run - pos
            # `.balign 4, 0` is only written when it provably emits this exact
            # number of bytes from this exact offset; otherwise the bytes go out
            # literally. Vanilla's padding always happens to be what balign
            # would produce, so this never came up there, but the base ROM's
            # does not and a balign that pads two bytes too many silently shifts
            # every jump after it.
            aligned = (4 - pos % 4) % 4
            if buf[pos:run] == b"\x00" * pad and pad == aligned and pad:
                out.append("    .balign 4, 0")
            else:
                out.append("    .byte " + ", ".join(str(b) for b in buf[pos:run]))
            out.append("")
            pos = run
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", required=True)
    ap.add_argument("--index", type=int, help="disassemble one script file and print it")
    ap.add_argument("--verify", action="store_true", help="walk every script file and report coverage")
    ap.add_argument("--emit", type=int, help="write one script file back out as macro assembly")
    ap.add_argument("--roundtrip", action="store_true",
                    help="emit every script file, reassemble it, and require byte-identical output")
    ap.add_argument("--enumproc", default="build/tools/enumproc/enumproc")
    ap.add_argument("--no-symbols", action="store_true",
                    help="emit every operand as a plain number")
    ap.add_argument("--base-rom", action="store_true",
                    help="use the base ROM's command meanings (see BASE_ROM_OVERRIDES)")
    a = ap.parse_args()
    use_base_rom_table(a.base_rom)

    import ndspy.narc
    import ndspy.rom

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from import_base_rom import Rom

    rom = Rom(a.rom)
    files = rom.narc(SCRIPTS_NARC)

    if a.roundtrip:
        import subprocess, tempfile
        order = [l.strip() for l in open(os.path.join(ROOT, "res", "field", "scripts", "scripts.order")) if l.strip()]
        ok = emit_failed = asm_failed = differs = skipped = 0
        raw_files = raw_bytes = 0
        problems = []
        with tempfile.TemporaryDirectory() as tmp:
            for i, buf in enumerate(files):
                if not buf or (i < len(order) and is_init_script(order[i])):
                    skipped += 1
                    continue
                try:
                    text = emit_source(buf, f"S{i}", symbols=not a.no_symbols)
                except Exception as exc:
                    emit_failed += 1
                    if len(problems) < 8:
                        problems.append(f"  {order[i] if i < len(order) else i}: could not emit: {exc}")
                    continue
                if getattr(emit_source, "last_raw", None):
                    raw_files += 1
                    raw_bytes += sum(len(v) for v in emit_source.last_raw.values())
                src = os.path.join(tmp, f"s{i}.s")
                with open(src, "w") as f:
                    f.write(text)
                proc = subprocess.run(
                    ["bash", "tools/scripts/make_script_bin.sh",
                     "-i", "include", "-i", "asm", "-i", "build", "-i", ".",
                     "--enumproc", a.enumproc, "--assembler", "arm-none-eabi-gcc",
                     "--objcopy", "arm-none-eabi-objcopy", "--out-dir", tmp, src],
                    capture_output=True, text=True)
                out = os.path.join(tmp, f"s{i}")
                if proc.returncode != 0 or not os.path.exists(out):
                    asm_failed += 1
                    if len(problems) < 8:
                        problems.append(f"  {order[i] if i < len(order) else i}: assembler: "
                                        + (proc.stderr.strip().splitlines() or ["?"])[-1])
                    continue
                if open(out, "rb").read() == bytes(buf):
                    ok += 1
                else:
                    differs += 1
                    if len(problems) < 8:
                        problems.append(f"  {order[i] if i < len(order) else i}: reassembled bytes differ")
                os.remove(out)
        print(f"round trip: {ok} byte-identical, {differs} differ, {emit_failed} could not be emitted, "
              f"{asm_failed} failed to assemble ({skipped} init scripts and empty members skipped)")
        if raw_files:
            print(f"  {raw_files} of them carry a region emitted as raw bytes rather than decoded "
                  f"({raw_bytes} bytes total); they round-trip but are not understood yet")
        for p_ in problems:
            print(p_)
        return

    if a.emit is not None:
        print(emit_source(files[a.emit], f"S{a.emit}", symbols=not a.no_symbols))
        return

    if a.index is not None:
        buf = files[a.index]
        decoded, labels, header_end, movements = walk(buf)
        for offset in sorted(set(decoded) | set(movements)):
            mark = "  <-- label" if offset in labels else ""
            if offset in movements:
                actions, size = movements[offset]
                print(f"{offset:#06x} movement block, {len(actions)} actions, {size} bytes{mark}")
                for name, length in actions:
                    print(f"         {name} {length}")
            else:
                print(f"{decoded[offset]}{mark}")
        return

    if a.verify:
        order = [l.strip() for l in open(os.path.join(ROOT, "res", "field", "scripts", "scripts.order")) if l.strip()]
        total = full = failed = 0
        leftover = 0
        init_ok = init_bad = 0
        movement_targets = overlaps = unclaimed_regions = 0
        problems = []
        for i, buf in enumerate(files):
            if len(buf) == 0:
                continue
            if i < len(order) and is_init_script(order[i]):
                try:
                    init_script_entries(buf)
                    init_ok += 1
                except Exception as exc:
                    init_bad += 1
                    if len(problems) < 10:
                        problems.append(f"  init script {i} ({order[i]}): {exc}")
                continue
            total += 1
            try:
                decoded, labels, movements, covered, size, unclaimed = coverage(buf)
                unclaimed_regions += len(unclaimed)
            except Exception as exc:
                failed += 1
                if len(problems) < 10:
                    problems.append(f"  script {i}: {exc}")
                continue
            if covered == size:
                full += 1
            else:
                leftover += size - covered
            movement_targets += len(movements)
            overlaps += sum(1 for off in movements if off in decoded)
        print(f"{total} non-empty script files: {full} fully accounted for, "
              f"{total - full - failed} with bytes left over ({leftover} bytes), {failed} failed")
        print(f"{init_ok + init_bad} init scripts: {init_ok} read, {init_bad} failed")
        print(f"{movement_targets} movement blocks referenced; {overlaps} of them collide with "
              f"decoded code (any collision would mean the command table is wrong)")
        print(f"{leftover} bytes and {unclaimed_regions} regions still unaccounted for after "
              f"the recovery pass (unreachable commands and unreferenced movement blocks)")
        for p in problems:
            print(p)


if __name__ == "__main__":
    main()
