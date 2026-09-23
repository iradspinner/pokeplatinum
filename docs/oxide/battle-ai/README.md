# How Platinum's trainer AI chooses a move

Phase 4 element 6, first step: understand the AI well enough to predict a change before it is made (tracker, element 6). This file is the engine and the map; the flag routines and the switching logic each have their own file, listed at the end. Everything here is read from the code in this tree, with line numbers, and was checked against vanilla on `main` where the two could differ. The code is the ground truth; where Ian's two references (pokemow.com's Gen 4 Trainer AI pages and lhearachel's gist) disagree with it, the part files say so.

The AI lives in two files. `src/battle/trainer_ai/trainer_ai.c` is the interpreter: it sets up the scores, runs the script, picks the move, and holds the switching and item logic, which are plain C. `src/battle/trainer_ai/script.s` is the script itself, about 8,100 lines of commands such as "if the target is asleep, add minus 10", one routine per AI flag. The commands are the `AICmd_*` functions in the C file. The game asks for a move from `src/battle/battle_display.c` line 3590, through `TrainerAI_Main`, but only for a trainer's Pokemon, a roaming legendary, the tutorial battle, or a partner on the player's side (lines 3586 to 3589). **Every other wild Pokemon picks a usable move at random** (lines 3600 to 3612) and never reaches anything described here. That includes both Pokemon in a wild double battle, so Oxide's wild doubles do not run the AI unless element 8 changes that line; whether they should is a decision for then.

A trainer's turn is decided in the order switch, then item, then move (`TrainerAI_PickCommand`, `trainer_ai.c` lines 3989 to 4040, in `switching-and-items.md`), and the move scoring below never runs on a turn the AI switches. Oxide's trainers never use items, since Phase 3 stopped giving them any, so in practice it is switch or move.

## The scoring engine

Every decision is a score per move slot, and the move with the highest score is used.

1. **The scores start at 100.** `TrainerAI_Init` (lines 211 to 256) gives every move slot 100, then sets any move that `BattleSystem_CheckInvalidMoves` rules out for this turn to 0 (called with `CHECK_INVALID_ALL`, line 234; the part files say what that covers where it matters).
2. **Each move draws a damage roll, which is never used.** `TrainerAI_Init` gives each slot a random roll from 85 to 100 (`moveDamageRolls`, line 240), and the C honours it wherever a command asks for it. No command in the script ever does: all eighteen damage checks pass `USE_MAX_DAMAGE` (which is 0, meaning "use 100%"), in vanilla as in Oxide. So every damage figure the AI works with is the top of the damage range, and its view of which move hits hardest does not vary from turn to turn.
3. **The trainer's flags decide which routines run.** The flags are a bitmask in the trainer file (`ai_flags`). A roaming Pokemon gets the roaming flag instead, and in any double battle the Tag Strategy flag is added on top (lines 245 to 255), whatever the trainer file says.
4. **Each flag's routine runs over every move, lowest flag first.** `TrainerAI_MainSingles` (lines 286 to 309) walks the mask one bit at a time. For each set bit, `TrainerAI_EvalMoves` (lines 483 to 526) runs that flag's routine once for each of the four move slots, and the routine adds to or takes from that slot's score. A move with no PP, or an empty slot, is scored 0 and skipped. So Basic has scored every move before Evaluate Attack sees any, and so on in the order below.
5. **The highest score wins, and ties are broken at random.** Lines 316 to 338. Only occupied slots take part. A routine can also end the turn early with an escape (wild Pokemon, roamers) or a Safari action.

The order the routines run in, which is the order of the flag table at the top of `script.s` (lines 18 to 51):

| Bit | Flag | Routine |
|---|---|---|
| 0 | Basic | `Basic_Main` |
| 1 | Evaluate Attack | `EvalAttack_Main` |
| 2 | Expert | `Expert_Main` |
| 3 | Setup First Turn | `SetupFirstTurn_Main` |
| 4 | Risky | `Risky_Main` |
| 5 | Prioritize Extremes | `PrioritizeExtremes_Main` |
| 6 | Baton Pass | `BatonPass_Main` |
| 7 | Tag Strategy | `TagStrategy_Main` (forced on in doubles) |
| 8 | Check HP | `CheckHP_Main` |
| 9 | Weather | `Weather_Main` |
| 10 | Harassment | `Harrassment_Main` |
| 11 to 28 | unused | `Terminate` |
| 29 | Roaming Pokemon | `RoamingPokemon_Main` |
| 30 | Safari | `Safari_Main` |
| 31 | Catch Tutorial | `CatchTutorial_Main` |

**One quirk of the engine that every part file has to keep in mind.** A move's score is stored in a signed byte (`s8 moveScore[4]`, `include/battle/ai_context.h` line 14). `AICmd_AddToMoveScore` (lines 576 to 586) adds the script's value and then raises anything below 0 to 0. Nothing caps it at the top, so a score pushed past 127 wraps round to a large negative number, which that same check then turns into 0: the move the AI likes best would become the one it never picks. This is present in vanilla Platinum (`main` has the same type and the same line). Whether any real combination of routines can push a score that far is for the part files to say, since it depends on how many bonuses can stack on one move.

### Double battles

`TrainerAI_MainDoubles` (lines 352 to 472) runs the whole pass above once for every other battler on the field, the partner included, each time with that battler as the target. For each target it keeps the best-scoring move (ties random). A move aimed at the partner is thrown out unless its score is at least 100 (lines 431 to 436), which is how helping moves and spread moves that hit the partner are allowed or refused. Then the target whose best move scored highest is chosen, ties random again, and two moves have their target overridden: a move that can target the user or its ally goes to the user when the chosen target is on the other side, and a non-Ghost Curse always targets the user.

## What Oxide's trainers actually use

The flags matter only as far as trainers carry them. Counted over the 747 trainers with a party, leaving out the dummies:

| Flag | Oxide | Vanilla |
|---|---|---|
| Basic | 747 | 747 |
| Expert | 559 | 289 |
| Evaluate Attack | 517 | 239 |
| Prioritize Extremes | 75 | 53 |
| Setup First Turn | 35 | 6 |
| Weather | 17 | 0 |
| Check HP | 10 | 0 |
| Risky | 8 | 4 |
| Baton Pass | 2 | 0 |
| Harassment | 1 | 0 |

The base ROM changed the flags of 362 trainers, nearly all towards more: the commonest set is now Basic, Evaluate Attack and Expert together (430 trainers, against 226 in vanilla), and only 171 trainers are left on Basic alone (400 in vanilla). Two consequences follow. The Expert routine, the largest part of the script, now drives most battles, so its behaviour is the game's behaviour. And four routines that no vanilla trainer uses (Weather, Check HP, Baton Pass, Harassment) now run for 30 trainers, so any fault in them, which vanilla never exercised, will be seen. Tag Strategy runs in the 18 double battles against trainers, and for a partner on the player's side; not for wild Pokemon, as the first section says.

## What the write-up found

About 70 distinct bugs, all but one present in vanilla Platinum. Each part lists its own with the vanilla line on `main`; `script.s` is byte-identical to `main`, so every script bug is vanilla at the same line. The headline items, the ones that change what Oxide's trainers actually do:

| Finding | Origin | Where | What it does in play |
|---|---|---|---|
| Revealed abilities above 255 are remembered as another ability | Oxide | `ai_context.h` line 28 | Quark Drive reads as Levitate and Protosynthesis as Wonder Guard, Hospitality as Soundproof. Element 2 widened abilities to u16 and missed this one byte |
| The Weather flag does nothing | vanilla | `other-flags.md` O1 | Every move falls into the Sunny Day branch and gets the same +5 on the first turn. 17 Oxide trainers carry the flag, gym leaders and Elite Four among them |
| A faster Pokemon almost never heals | vanilla | `expert-1.md` bug 4 | Under Expert (559 trainers), Recover, Roost, Synthesis and the rest get -8 whenever the user is not slower |
| Some moves skip every immunity check | vanilla | `basic.md` B6 | Moves whose power is worked out elsewhere (Solar Beam, Eruption, Sucker Punch and others) keep a full score into an immune target; Oxide's Dragon Energy into a Fairy is one |
| Punishment adds every rung of its ladder | vanilla | `expert-2.md` bug 2 | Up to +10 where one rung was meant |
| The AI will Trick or Gastro Acid its own partner | vanilla | `other-flags.md` O11 | Several partner cases leave the move at 100, which passes the doubles filter |
| The bench damage check uses the active Pokemon's stats and types | vanilla | `expert-2.md` bug 10, `switching-and-items.md` | Skews U-turn, Healing Wish and switching |
| Status moves count as super-effective in the bench checks | vanilla | `switching-and-items.md` | Skews when and to what the AI switches |

The eleven battle_edits fixes Ian approved on 2026-09-15 are all vanilla bugs. Nine are in the script (Basic, both Expert halves and Tag Strategy); Fire Fang against Wonder Guard lives in `battle_lib.c` and Rage in `battle_controller_player.c` line 846. The guide they come from was not read for this write-up, so each is located from the code; two (the "Sunny Day check", most likely `basic.md` B2, and the "charge-turn scoring fix", most likely `expert-2.md` bug 3) need the guide's wording confirmed before they are applied.

What Oxide's new content meets, beyond the bug above: none of the new effects 277 to 406 has an Expert routine, so the 452 new moves are scored only by Basic's generic checks and the damage comparison; the 51 new status moves on new effects get no Basic check at all; the seven new Protect-type moves never take the repeat penalty and the seven new Speed-lowering attacks get nothing, because those checks key on move ids; and Fairy makes the switching checks see Poison as super-effective on a Poison-immune Steel/Fairy. Teaching the AI these is element 6's later step.

## Fixes applied, 2026-09-22

One Oxide fix and six vanilla fixes, each its own commit so any can be reverted alone. **Every vanilla fix changes how the game plays and was approved by Ian**; each is marked in `script.s` with an "Oxide, vanilla fix" comment.

| Fix | Kind | What changes in play |
|---|---|---|
| The AI's remembered ability is u16 (`ai_context.h`) | Oxide | Quark Drive, Protosynthesis, Hospitality and the rest are remembered as themselves |
| Weather flag (O1) | vanilla | Only a weather move that would set new weather gets the +5 on the first turn |
| Immunity checks for damaging moves outside the damage comparison (B6) | vanilla | Water Spout into Water Absorb, Dragon Energy into a Fairy and the like are now refused |
| Punishment's ladder (expert-2 bug 2) | vanilla | 50% +4, 25% +3, 12.5% +2, 6.25% +1 against +7 boosts or more, as its comment says, instead of summing up to +10 |
| Trick, Switcheroo and Gastro Acid on the partner (O11) | vanilla | Refused (-30), except Gastro Acid on a partner with Truant or Slow Start (+5, as before) |
| Weather Ball's type in clear weather (switching bug 1) | vanilla | All three type helpers start from Normal. Read from the compiled code, they had returned a pointer: the engine's redirection check was right by luck, but the AI's effectiveness check saw Weather Ball as Normal only if the heap put the battle system at an address ending in 00, and otherwise as neutral against everything, Ghost types included |
| Weather Ball in the AI's damage estimate (found after the write-up, from Ian's pokemow reference) | vanilla | In weather the AI now estimates the doubled power and the weather's type, as the battle sets them, instead of always a 50-power Normal move |

Put to Ian and kept as vanilla has them: the faster Pokemon that almost never heals (expert-1 bug 4), the bench damage check that uses the active Pokemon's stats (expert-2 bug 10), and status moves counting as super-effective in the switching checks. The eleven battle_edits fixes are approved but not yet applied: two of their locations need the guide's wording confirmed first.

## The parts

| File | Covers |
|---|---|
| `basic.md` | the Basic flag: refusing moves that cannot work |
| `expert-1.md` | the Expert flag, its dispatch and its first half |
| `expert-2.md` | the Expert flag, second half |
| `other-flags.md` | every other flag, and the double-battle driver |
| `switching-and-items.md` | the damage the AI calculates, switching, replacements and item use |

Each part ends with its apparent bugs, every one labelled as present in vanilla Platinum or introduced by Oxide, then the battle_edits fixes that fall in it, then what Oxide's new moves, abilities and types do there. Fixing a bug that is present in vanilla is Ian's call and is always called out as such.
