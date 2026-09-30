---
name: playtest-day
description: How to run a Platinum Oxide playtest session with Ian from docs/oxide/ingame-checklist.md, from fetching the right ROMs to recording each result as a tick or as an open bug. Use this whenever Ian says he is ready to play or test, the new CPU has arrived, a batch of in-game checks has piled up, or a session is asked to "go through the checks", even if he only names one check.
---

# A playtest day

Ian keeps in-game checks for one sitting, so they do not interrupt the build
work (his ruling of 2026-09-26). This skill runs that sitting. Ian drives
melonDS on Windows. The agent fetches ROMs, reads the checklist out in order,
attaches over the GDB stub for the live checks, and records what happened.
Never launch an emulator yourself.

## Before Ian starts

1. Read `docs/oxide/ingame-checklist.md` from the top.
2. Build both ROMs of the current, pushed `oxide` (`make rom` and `make
   testkit`), check the ordinary one's SHA-1 against GitHub's build of the
   commit, and copy them into `~/oxide-playtest` as
   `pokeplatinum-oxide-<commit>.nds` and `pokeplatinum-oxide-testkit-<commit>.nds`.
   `tools/oxide/fetch-rom <commit>` and `--testkit` do the same on GitHub.
   Give Ian the Windows paths (`\\wsl$\Ubuntu\home\ian\oxide-playtest\...`).
3. Pick the sections he can reach today. A new game covers sections 2 and 3;
   sections 4 and 5 need a mid-game or post-game save. Ask him which saves he
   has, and skip what none of them reach.

## During the session

Give Ian one check at a time, in the checklist's order, with what he should
see. Keep each to a sentence or two, and name the kit menu entry or map.

For a **(live)** check, attach with the `debug-live` skill before he reaches
the spot, set the breakpoint, and read the values yourself. He only has to
play to that point.

When a check passes, note it. When it fails, get the details while they are
fresh:
- what he did and what he saw;
- a screenshot or the message text;
- the save, and whether it happens again.

For a crash or hang, attach and read before he restarts.

## Recording results

At the end, or every few checks if the session is long:

- Tick each passed check and move it to the checklist's "Passed" section with
  the date.
- Turn each failure into an "Open bug" entry in the tracker's Phase 5, and
  point the checklist's line at it. Say whether the bug is also in vanilla
  Platinum, if that is known. A fix to a vanilla bug is a VANILLA FIX, called
  out apart.
- Answers Ian gives along the way are rulings: record them with the `ruling`
  skill.
- Commit the checklist and tracker by name, push `oxide`, and run
  `tools/oxide/sync-docs.sh`.

Report to Ian: what passed, what failed and where each failure is filed,
and what is left for next time.
