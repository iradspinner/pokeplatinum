# GDB init for debugging the built ROM in melonDS's GDB stub (ARM9 on port 3333).
#
# Use with the overlay-aware fork from INSTALL.md section 4:
#   ~/tools/gdb-nds/bin/arm-none-eabi-gdb -x tools/oxide/melonds.gdb
# from the repo root, after `make rom` (release, matches what Ian plays) or
# `make debug` (-O1, overlay table exported so `overlay auto` works).
# Full recipe: docs/oxide/setup-fork-and-wsl2.md part 5.
#
# The symbol file is build/main.nef, the ELF the ROM is made from. `debug.nef`
# is the same file with source paths rewritten by debugedit, which WSL2 lacks;
# the substitute-path below does the same job inside GDB, so main.nef is enough.

set architecture armv5te
set confirm off
set pagination off
file build/main.nef
# Metrowerks under Wine records paths as Z:\home\...; map them back.
set substitute-path Z:/ /
set substitute-path Z:\\ /
target remote 127.0.0.1:3333

# Only a debug build (make debug) exports _ovly_table, so only there can GDB
# follow overlay loads. On a release build these two lines just print errors;
# breakpoints on overlay functions still work while the overlay is loaded,
# because the fork sets them at the linked address.
overlay auto
overlay map build/overlay.map
