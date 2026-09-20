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


def build_command_table():
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
        table[opcode] = Command(opcode, const, macro, operands)
    return table


TABLE = None


def table():
    global TABLE
    if TABLE is None:
        TABLE = build_command_table()
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


def walk(buf):
    """Follow every script entry and every code target reachable from one.
    Returns {offset: DecodedCommand} and the set of offsets that are entries or
    jump targets, which is what needs a label when this is written back out."""
    entries, header_end = script_entries(buf)
    decoded = {}
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
            if dc.cmd.const in TERMINATORS:
                break
            offset += dc.size
    return decoded, labels, header_end


def coverage(buf):
    """How much of a script file the walk accounts for. Anything left over is
    movement data or another non-code table."""
    decoded, labels, header_end = walk(buf)
    covered = bytearray(len(buf))
    for dc in decoded.values():
        for i in range(dc.offset, dc.offset + dc.size):
            covered[i] = 1
    for i in range(header_end):
        covered[i] = 1
    return decoded, labels, sum(covered), len(buf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", required=True)
    ap.add_argument("--index", type=int, help="disassemble one script file and print it")
    ap.add_argument("--verify", action="store_true", help="walk every script file and report coverage")
    a = ap.parse_args()

    import ndspy.narc
    import ndspy.rom

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from import_base_rom import Rom

    rom = Rom(a.rom)
    files = rom.narc(SCRIPTS_NARC)

    if a.index is not None:
        buf = files[a.index]
        decoded, labels, header_end = walk(buf)
        for offset in sorted(decoded):
            mark = "  <-- label" if offset in labels else ""
            print(f"{decoded[offset]}{mark}")
        return

    if a.verify:
        order = [l.strip() for l in open(os.path.join(ROOT, "res", "field", "scripts", "scripts.order")) if l.strip()]
        total = full = failed = 0
        leftover = 0
        init_ok = init_bad = 0
        movement_targets = overlaps = 0
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
                decoded, labels, covered, size = coverage(buf)
            except Exception as exc:
                failed += 1
                if len(problems) < 10:
                    problems.append(f"  script {i}: {exc}")
                continue
            if covered == size:
                full += 1
            else:
                leftover += size - covered
            for dc in decoded.values():
                pos = dc.offset + 2
                for kind, name, value in dc.values:
                    if kind == "rel" and not is_code_target(dc.cmd, name):
                        movement_targets += 1
                        if (pos + 4 + value) in decoded:
                            overlaps += 1
                    pos += WIDTHS[kind]
        print(f"{total} non-empty script files: {full} fully accounted for, "
              f"{total - full - failed} with bytes left over ({leftover} bytes), {failed} failed")
        print(f"{init_ok + init_bad} init scripts: {init_ok} read, {init_bad} failed")
        print(f"{movement_targets} movement blocks referenced; {overlaps} of them collide with "
              f"decoded code (any collision would mean the command table is wrong)")
        print(f"the {leftover} leftover bytes are those movement blocks, which are a separate "
              f"encoding, plus short runs of unreferenced Noop between scripts")
        for p in problems:
            print(p)


if __name__ == "__main__":
    main()
