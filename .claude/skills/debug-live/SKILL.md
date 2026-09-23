---
name: debug-live
description: How the Platinum Oxide bug track debugs the running game. Ian runs melonDS on Windows and drives the game; the agent attaches to his emulator's GDB stub from WSL2 with tools/oxide/live_watch.py, plants breakpoints and reads memory. Use this for any in-game hang, crash, wrong behaviour or "what does the game do when", including every "Open bug" entry in the tracker, even if the user just says "look at the box hang" or "why does Sandgem crash".
---

# Debugging the live game

**The agent never launches an emulator.** Not melonDS under WSLg, and not an
AppImage or its AppRun; a hook refuses the command anyway. Part 5 of
`docs/oxide/setup-fork-and-wsl2.md` records that route and why it failed: one
session spent its whole budget rebuilding it. The method is a two-person loop:
Ian owns the emulator and the controller, and the agent owns the breakpoints
and the reading.

## Before asking Ian for anything

1. Read the bug's entry under Phase 5 in `docs/oxide/tracker.md`: what is
   known, what was ruled out, and which functions to break on. The bug track's
   status home is those entries and nothing else in the tracker. A fixed bug's
   entry moves to `docs/oxide/tracker-archive.md`, which also keeps the fuller
   wording of the two open entries as they stood on 2026-09-23.
2. Read the design doc's findings log for the area. The whiteout hang
   (2026-09-21) is the worked example of this whole method: a misaligned
   movement block in a generated script, found by breaking on the script
   commands.
3. **Make sure the ROM Ian runs is the one your symbols come from.**
   `live_watch.py` resolves names in `build/main.nef`, so a ROM from another
   build puts every breakpoint in the wrong place. Build, check the ROM's
   SHA-1 against GitHub's build of the same commit (CLAUDE.md, Build), and give
   Ian the path and the hash. He loads that file.
4. Pick the breakpoints and work out what each will cost Ian. Warn him before
   arming one that an ordinary action trips (talking to any NPC, opening a
   menu, every frame of a wait), and say how to get past it.

## The loop

Ian's side, in melonDS 1.1 on Windows: Devtools has the GDB stub on (ARM9 port
3333) and **Break on startup** on. He restarts melonDS for every session,
loads the ROM (or `~/roms/route202-hang.sav` when the bug needs a save), and
tells you it is sitting at the startup break.

Your side, from the repo root, started only after Ian says it is at the break:

```
PYTHONPATH=. python3 tools/oxide/live_watch.py SYMBOL [SYMBOL ...]
```

It connects, plants hardware breakpoints, continues the game, and logs every
stop to `~/roms/live-watch.log` with the time, pc, the symbol at pc, r0 to r3
and lr. Then Ian plays to the point of interest and describes what he sees,
and you read the log and decide the next step.

The options that matter:

| Option | What it is for |
|---|---|
| `--every N` | a breakpoint that fires every frame is logged on its first hits, then every N-th |
| `--arm-on SYM` with `--plant-on-arm A,B` | keep breakpoints inert until SYM fires, so reaching the scene does not trip them |
| `--hold-at SYM:N`, `--hold-burst SYM:K` | stop the game at a hit so `--auto` commands can read state |
| `--auto CMD` | `peek` (with nested dereferences), `readptr`, `steps`, `trace` while held |
| `touch ~/roms/live-watch.stop` | detach cleanly; Ian then restarts melonDS for the next session |

## Limits of the Windows stub

These were measured on 2026-09-21, and each one shapes the loop:

- It takes one client per emulator session and does not recover from a dropped
  one. So one `live_watch.py` per melonDS restart; plan the breakpoints before
  connecting.
- It only services the socket while the CPU is stopped, so a running game
  cannot be interrupted from the client. Attach at the startup break only, and
  get control back with a breakpoint, never by interrupting.
- Single-stepping runs at about ten instructions a second, so `trace` is for a
  few thousand instructions at most. Find the frame with heartbeat and stage
  breakpoints first.

Struct offsets are quickest offline, with no emulator at all:
`~/tools/gdb-nds/bin/arm-none-eabi-gdb -batch -ex "file build/main.nef" -ex "print/x &((BattleContext*)0)->battleMons[0].curHP"`.

## When the cause is found

- Fix it on `oxide` as its own commit. Say in the message what the cause was
  and how the stub showed it.
- Ask Ian to confirm the fix in melonDS, on a ROM whose hash you gave him.
  Until he confirms, the bug entry stays open with "fixed, awaiting Ian".
- Record the cause in the design doc's findings log when it teaches something
  beyond this one bug, the way the alignment rule did. Tick the Phase 5 entry.
