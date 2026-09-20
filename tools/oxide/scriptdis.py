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
    def __init__(self, opcode, const, macro, operands):
        self.opcode = opcode
        self.const = const
        self.macro = macro
        self.operands = operands  # [(kind, arg name)]

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
            expr = part.group(2).strip()
            if expr.endswith("-.-4"):
                kind = "rel"
                expr = expr[: -len("-.-4")]
            operands.append((kind, expr.lstrip("\\")))
        by_const.setdefault(const, (macro, operands))

    table = {}
    for opcode, const in enumerate(order):
        if const not in by_const:
            continue
        macro, operands = by_const[const]
        if const in CONDITIONAL:
            # the .if body is reconstructed at decode time, so keep only what
            # comes before it
            operands = operands[:1]
        if base_rom and const in BASE_ROM_OVERRIDES:
            operands = list(BASE_ROM_OVERRIDES[const])
        table[opcode] = Command(opcode, const, macro, operands)
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
    """The offsets of each ScriptEntry in a script file's header table, and
    where the table ends.

    ScriptEntryEnd is optional: plenty of files just run the first script
    straight after the last entry, so the table also ends as soon as the
    position reaches the nearest target any entry points at."""
    entries = []
    pos = 0
    limit = len(buf)
    while pos + 2 <= len(buf):
        if struct.unpack_from("<H", buf, pos)[0] == SCRIPT_ENTRY_END:
            return entries, pos + 2
        if pos >= limit:
            return entries, pos
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
    entries, header_end = script_entries(buf)
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
        if not any(buf[i:j]):
            i = j  # alignment padding
            continue
        claimed = False
        try:
            actions, size = decode_movement(buf, i)
            if size == j - i:
                extra_movements[i] = (actions, size)
                claimed = True
        except Exception:
            pass
        if not claimed:
            try:
                pos, found = i, {}
                while pos < j:
                    dc = decode_command(buf, pos)
                    found[pos] = dc
                    pos += dc.size
                if pos == j:
                    extra_commands.update(found)
                    claimed = True
            except Exception:
                pass
        if not claimed:
            unclaimed.append(region)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", required=True)
    ap.add_argument("--index", type=int, help="disassemble one script file and print it")
    ap.add_argument("--verify", action="store_true", help="walk every script file and report coverage")
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
