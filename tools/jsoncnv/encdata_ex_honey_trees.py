#!/usr/bin/env python3
import json
import pathlib
import sys

from convert import u32
from generated import species

ANSI_BOLD_WHITE = "\033[1;37m"
ANSI_BOLD_RED = "\033[1;31m"
ANSI_RED = "\033[31m"
ANSI_CLEAR = "\033[0m"

def as_species(s: str) -> bytes:
    return u32(species.Species[s].value)

# Platinum Oxide: the honey trees have one table per badge count (1 to 8),
# each with its own level range, packed into one member that honey_tree.c
# reads as HoneyTreeTable[8]: six common species, six uncommon, then the
# minimum and maximum level, all u32. The two other outputs keep vanilla's
# member count so the Trophy Garden and Great Marsh members do not move.
input_path = pathlib.Path(sys.argv[1])
output_path_tables = pathlib.Path(sys.argv[2])
output_path_unused = [pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4])]

NUM_TABLES = 8
TIER_SIZE = 6

try:
    data = {}
    with open(input_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
except json.decoder.JSONDecodeError as e:
    doc_lines = e.doc.splitlines()
    start_line = max(e.lineno - 2, 0)
    end_line = min(e.lineno + 1, len(doc_lines))

    error_lines = [f"{line_num:>4} | {line}" for line_num, line in zip(list(range(start_line + 1, end_line + 1)), doc_lines[start_line : end_line])][ : end_line - start_line]
    error_line_index = e.lineno - start_line - 1
    error_lines[error_line_index] = error_lines[error_line_index][ : 5] + f"{ANSI_RED}{error_lines[error_line_index][5 : ]}{ANSI_CLEAR}"
    error_out = "\n".join(error_lines)

    print(f"{ANSI_BOLD_WHITE}{input_path}:{e.lineno}:{e.colno}: {ANSI_BOLD_RED}error: {ANSI_BOLD_WHITE}{e.msg}{ANSI_CLEAR}\n{error_out}", file=sys.stderr)
    sys.exit(1)

tables = data['tables']
if len(tables) != NUM_TABLES:
    print(f"{input_path}: expected {NUM_TABLES} honey tables, found {len(tables)}", file=sys.stderr)
    sys.exit(1)

packables = bytearray([])
for i, table in enumerate(tables):
    # The engine picks a table by position, so the file must list them in
    # badge order; `badges` is there to say so to a human reader.
    if table['badges'] != i + 1:
        print(f"{input_path}: table {i} is for {table['badges']} badges, expected {i + 1}", file=sys.stderr)
        sys.exit(1)
    if not 1 <= table['level_min'] <= table['level_max'] <= 100:
        print(f"{input_path}: table {i} has a bad level range", file=sys.stderr)
        sys.exit(1)
    for tier in ('common', 'uncommon'):
        if len(table[tier]) != TIER_SIZE:
            print(f"{input_path}: table {i} {tier} needs {TIER_SIZE} species", file=sys.stderr)
            sys.exit(1)
        for s in table[tier]:
            packables.extend(as_species(s))
    packables.extend(u32(table['level_min']))
    packables.extend(u32(table['level_max']))

with open(output_path_tables, 'wb') as output_file:
    output_file.write(packables)

for path in output_path_unused:
    with open(path, 'wb') as output_file:
        output_file.write(bytes(4 * TIER_SIZE))
