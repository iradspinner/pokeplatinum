# QA review: element 6, battle AI (2026-09-22)

## What was reviewed

The range is `c3312759e..a7e6763dd` on `worktree-element6` (the merge base with `oxide` to the branch tip), ten commits, 12 files, 2,808 lines added and 5 removed. Almost all of the added lines are the six `docs/oxide/battle-ai/` files; the code change is 67 lines across four files.

| Commit | What it does |
|---|---|
| 77de75473 | Writes down how the trainer AI picks a move (`docs/oxide/battle-ai/`, six files) and maps them in `sync-docs.sh` |
| 5e276cbfd | Oxide fix: `AIContext.battlerAbilities` from u8 to u16 |
| 77da99169 | Vanilla fix: the Weather flag no longer gives every move +5 |
| ea9920f85 | Vanilla fix: damaging moves outside the damage comparison get Basic's immunity checks |
| 666d01819 | Vanilla fix: Punishment's ladder stops at the first rung won |
| 91c14e2d2 | Vanilla fix: Trick, Switcheroo and Gastro Acid are refused on the partner |
| e90b85c59 | Tracker and README record the five fixes above and the in-game check |
| 483f91fdd | Vanilla fix: Weather Ball's type starts from Normal in all three type helpers |
| 3191fa2a4 | Vanilla fix: the AI's damage estimate has a Weather Ball case |
| a7e6763dd | Tracker and README record the two Weather Ball fixes |

Left out, as the brief asked: the gate (step 4), which the integration runs on the merged tree. Nothing was fixed. The build was not rerun (see the last section).

No finding blocks the merge. Every code change does what its message says on the paths it names. The findings are about paths the messages do not name and about docs that the fixes made stale.

## Findings, most serious first

### 1. The battle-ai docs went stale when the fixes landed (low, open)

The docs were written against the tree before the fixes and say so: the README states that "Everything here is read from the code in this tree, with line numbers" and that "`script.s` is byte-identical to `main`". Both stopped being true in the same branch. Every `script.s` line cited past line 62 is now 8 to 22 lines off, `trainer_ai.c` lines past 3054 are 29 to 31 off, and `battle_lib.c` lines past 7963 are 2 to 4 off. Evidence: `expert-1.md` line 632 cites Swift Swim at script lines 3747 to 3749, which is the Swift Swim check on `main` but a comment block in the branch; the README cites `TrainerAI_PickCommand` at lines 3989 to 4040, and it now starts at `trainer_ai.c:4020`.

Four smaller statements are wrong or out of date in the same files:

- `switching-and-items.md:115` still says Weather Ball is "seen at [its] listed base power", which 3191fa2a4 changed.
- `README.md:94` says the unfixed AI saw a clear-weather Weather Ball as Normal when the battle system's address ended in 00 "and otherwise as neutral against everything". `Heap_Alloc` aligns to 4 (`src/heap.c:216`) and the type chart takes the pointer's low byte, so a low byte of 0x04, 0x08, 0x0C or 0x10 read it as Ground, Steel, Grass or Dragon. This only matters as a record, since the bug is fixed.
- `README.md` (the Weather row of the headline table, and commit 77da99169) says every move got the same +5. That is true only when the sun is not already up; under sun the vanilla routine gave the other moves nothing (`script.s:8014` to `8017`: `Weather_Sun` ends without a bonus when the weather is already sunny).
- `README.md` line 7 says Oxide's trainers never use items "since Phase 3 stopped giving them any". 40 trainer files still list items (21 Full Restores among them); the reason the AI never uses them is that Oxide's `BattleControllerPlayer_InitAI` no longer loads them (`battle_controller_player.c:4823` to `4835`). `switching-and-items.md:222` describes this correctly.

Suggested fix for the track: renumber against the branch tip, or state once that line numbers refer to the pre-fix tree and `main`, and correct the four statements.

### 2. Weather Ball is still misjudged on two AI paths (low, Ian's call)

3191fa2a4 covers `TrainerAI_CalcDamage`, which every script damage check and the switching checks in `trainer_ai.c` use. The replacement pick after a knockout does not go through it. `BattleAI_PostKOSwitchIn` stage 2 (`battle_lib.c:8124` to `8150`) calls `BattleSystem_CalcMoveDamage` with power 0 and type 0, so a bench Weather Ball in rain is still costed as a 50-power Normal move, same-type bonus and rain boost included. After 483f91fdd only its type-chart step sees Water. That path also ignores every other variable-power move, which the switching doc already records as vanilla.

Four more places read a move's listed type rather than its battle type, so Weather Ball in weather still reads as Normal there: `LoadTypeFrom LOAD_MOVE_TYPE` (`trainer_ai.c:962`, used by Basic's absorb and Levitate checks, so rain Weather Ball into Water Absorb is not refused), `AICmd_LoadTypeOfLoadedMove` (`trainer_ai.c:2523`), `AI_HasAbsorbAbilityInParty` (`trainer_ai.c:3696`), and Tag Strategy's Electric, Fire and Water dispatch. The docs list these as vanilla gaps for every variable-type move (`basic.md:41`, `other-flags.md:40`, `switching-and-items.md` bug 17). No commit claims to fix them; they are named here because the brief asked about every path.

### 3. Two commit messages understate what changes in play (low, open)

ea9920f85 names twelve moves. Its rule (`LoadMovePower`, then any power above 0) routes 52 moves into the immunity checks, counted from `res/moves/*/data.json` against the two tables at `trainer_ai.c:31` and `48`. The 40 it does not name are the ten recharge moves (Hyper Beam and nine others), Selfdestruct, Explosion and Misty Explosion, Dream Eater, Focus Punch, Superpower, Razor Wind, Skull Bash, Solar Blade, and 21 moves listed at power 1: Counter, Mirror Coat, Metal Burst, Comeuppance, Bide, Super Fang, Ruination, Endeavor, Flail, Reversal, Crush Grip, Wring Out, Magnitude, Present, Punishment, Fling, Trump Card, Spit Up, Electro Ball, Guillotine and Sheer Cold. So Explosion or Hyper Beam into a Ghost, or Counter into a Ghost, is now refused where it was not. I found no case where the engine's own immunity result is wrong for these moves (the check calls the real `BattleSystem_ApplyTypeChart`), so this is correct behaviour that the message does not describe. Status moves stay out: no status move has power above 0.

483f91fdd describes the effect of fixing `TrainerAI_MoveType` and `CalcMoveType`, but not `Move_CalcVariableType`, whose other callers are all AI switching: `battle_lib.c:8071` and `8124` (post-knockout replacement, both stages) and `trainer_ai.c:3355`, `3474`, `3533` and `3813`. A bench Pokemon's clear-weather Weather Ball is now Normal there, where it used to be whatever the caller left in the register, so switching can change. `switching-and-items.md` bug 1 says this; the commit message does not.

The tracker trace for this merge should carry the full scope, so a later session does not read the fixes as narrower than they are.

### 4. The Camper Zackary check states its expected score loosely (low, Ian's call)

The new "Waiting on Ian" line (from e90b85c59) says Rain Dance "should be 5 above his other moves". Zackary carries Basic, Evaluate Attack and Expert too (`res/trainers/data/camper_zackary.json`). Evaluate Attack takes 1 from the weaker of Water Pulse and Powder Snow, and adds more to an attack that would knock out or hit four times over (`script.s:6364` onward), so Rain Dance can read 6 above one move, or sit close to or below an attack that would knock out. A tighter statement is that Rain Dance reads 105 on turn one and neither attack carries the Weather flag's +5. The tracker is the main session's to edit.

## Claims re-checked

| Claim | Result |
|---|---|
| 17 Oxide trainers carry the Weather flag (77da99169) | Confirmed, `grep -l '"AI_FLAG_WEATHER"' res/trainers/data/*.json` gives 17, including Gardenia, Wake, Candice, Volkner, Bertha and Flint |
| Four Oxide trainers carry Weather Ball (3191fa2a4) | Confirmed: Shannon, Dennis, Gardenia, a Galactic HQ grunt. No trainer with a default moveset knows it (Roserade's level-1 Weather Ball is pushed out by four later level-1 moves) |
| Quark Drive read as Levitate, Protosynthesis as Wonder Guard, Hospitality as Soundproof, Pastel Veil as Stench (5e276cbfd) | Confirmed from `generated/abilities.txt`: 282, 281, 299 and 257 are 26, 25, 43 and 1 plus 256 |
| Every reader of `battlerAbilities` copies it into an int (5e276cbfd) | Confirmed. Writers are `battle_script.c:12178` (a u16 parameter) and `battle_lib.c:7797`; readers are `trainer_ai.c:1181` to `1227`, into `calcTemp` and `tmpAbility`, both int. Script operands are 32-bit (`asm/macros/aicmd.inc:484`). No other u8 ability variable in `src/battle` or `include/battle`. The struct is only in battle memory and cleared by `sizeof` |
| The three type helpers returned the caller's register, a pointer (483f91fdd) | Confirmed on the pre-fix objects in the main checkout's `build/`: all three return r5 unset on the Weather Ball path; the effectiveness command holds `battleSys` in r5 and the redirection check holds `battleCtx`. Read from an Oxide build, not the vanilla ROM; these functions have no Oxide edits before this branch |
| Vanilla line references in all six fix messages | Confirmed against `main` |
| Punishment gives 50%, 25%, 12.5%, 6.25% after the fix | Confirmed by reading: each rung jumps to the end on a win, and `IfRandomLessThan 128` is one in two |
| Partner moves below 100 are thrown out | Confirmed, `trainer_ai.c:431` to `436` |
| README flag counts (747 trainers, 430 on Basic, Evaluate Attack and Expert, 171 on Basic alone, 18 doubles, the vanilla column) | Reproduced exactly when the 180 `dummy_NNN` files are left out |
| All eighteen damage checks pass `USE_MAX_DAMAGE` | Confirmed, 18 on both `main` and the branch |
| Expert's faster-heal branch is unreachable (`expert-1.md` bug 4) | Confirmed at `main` `script.s:2650` to `2657` |
| `BattleSystem_CalcMoveDamage` and the type chart honour the power and type passed in (3191fa2a4) | Confirmed, `battle_lib.c:6695` to `6706` and `2600` to `2606` |

Not rerun, and why:

- "The build succeeds" (5e276cbfd, 3191fa2a4). Not rebuilt, to keep load off the CPU; the integration gate builds the merged tree. The worktree's objects postdate the last source edit, and their sizes show the fixes compiled in (`TrainerAI_CalcDamage` 0x3F8 to 0x46C bytes, `TrainerAI_MoveType` 0x178 to 0x180).
- Ian's approval of each vanilla fix on 2026-09-22 cannot be checked from the tree.
- The in-game effect of any fix needs Ian's emulator.
