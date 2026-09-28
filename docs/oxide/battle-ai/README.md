# How Platinum's trainer AI chooses a move

Phase 4 element 6, first step: understand the AI well enough to predict a change before it is made (tracker, element 6). This file is the engine and the map; the flag routines and the switching logic each have their own file, listed at the end. Everything here was read from the code before element 6's fixes, when `script.s` and the AI's C were still vanilla, so **every line number in these files is vanilla's, on `main`**. The fixes and changes since have shifted lines in the branch by hundreds in `script.s` and dozens in `trainer_ai.c`; find a routine by its label, not its number, and read the README's later sections for what each routine now does. The code is the ground truth; where Ian's two references (pokemow.com's Gen 4 Trainer AI pages and lhearachel's gist) disagree with it, the part files say so.

The AI lives in two files. `src/battle/trainer_ai/trainer_ai.c` is the interpreter: it sets up the scores, runs the script, picks the move, and holds the switching and item logic, which are plain C. `src/battle/trainer_ai/script.s` is the script itself, about 8,100 lines of commands such as "if the target is asleep, add minus 10", one routine per AI flag. The commands are the `AICmd_*` functions in the C file. The game asks for a move from `src/battle/battle_display.c` line 3590, through `TrainerAI_Main`, but only for a trainer's Pokemon, a roaming legendary, the tutorial battle, or a partner on the player's side (lines 3586 to 3589). **Every other wild Pokemon picks a usable move at random** (lines 3600 to 3612) and never reaches anything described here. That includes both Pokemon in a wild double battle, so Oxide's wild doubles do not run the AI unless element 8 changes that line; whether they should is a decision for then.

A trainer's turn is decided in the order switch, then item, then move (`TrainerAI_PickCommand`, `trainer_ai.c` lines 3989 to 4040, in `switching-and-items.md`), and the move scoring below never runs on a turn the AI switches. Oxide's trainers never use items: 40 trainer files still list some, but Phase 3 made `BattleControllerPlayer_InitAI` stop loading them (`battle_controller_player.c`), so in practice it is switch or move.

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

About 70 distinct bugs, all but one present in vanilla Platinum. Each part lists its own with the vanilla line on `main`; `script.s` was byte-identical to `main` when they were written, so every script bug is vanilla at the line given. The headline items, the ones that change what Oxide's trainers actually do:

| Finding | Origin | Where | What it does in play |
|---|---|---|---|
| Revealed abilities above 255 are remembered as another ability | Oxide | `ai_context.h` line 28 | Quark Drive reads as Levitate and Protosynthesis as Wonder Guard, Hospitality as Soundproof. Element 2 widened abilities to u16 and missed this one byte |
| The Weather flag does nothing | vanilla | `other-flags.md` O1 | Every move falls into the Sunny Day branch, so on the first turn every move gets the same +5 (or, with the sun already up, nothing). 17 Oxide trainers carry the flag, gym leaders and Elite Four among them |
| A faster Pokemon almost never heals | vanilla | `expert-1.md` bug 4 | Under Expert (559 trainers), Recover, Roost, Synthesis and the rest get -8 whenever the user is not slower |
| Some moves skip every immunity check | vanilla | `basic.md` B6 | Moves whose power is worked out elsewhere (Solar Beam, Eruption, Sucker Punch and others) keep a full score into an immune target; Oxide's Dragon Energy into a Fairy is one |
| Punishment adds every rung of its ladder | vanilla | `expert-2.md` bug 2 | Up to +10 where one rung was meant |
| The AI will Trick or Gastro Acid its own partner | vanilla | `other-flags.md` O11 | Several partner cases leave the move at 100, which passes the doubles filter |
| The bench damage check uses the active Pokemon's stats and types | vanilla | `expert-2.md` bug 10, `switching-and-items.md` | Skews U-turn, Healing Wish and switching |
| Status moves count as super-effective in the bench checks | vanilla | `switching-and-items.md` | Skews when and to what the AI switches |

The eleven battle_edits fixes Ian approved on 2026-09-15 are all vanilla bugs. Nine are in the script (Basic, both Expert halves and Tag Strategy); Fire Fang against Wonder Guard lives in `battle_lib.c` and Rage in `battle_controller_player.c` line 846. All eleven are now applied (below). Each was checked against the guide's own byte edits for Platinum: every offset holds the vanilla byte the guide expects, and the source edits, assembled, give exactly the guide's bytes. The guide's "Sunny Day check" is `basic.md` B2 (Hydration becomes Leaf Guard, and the status test is inverted) and its "charge-turn scoring fix" is `expert-2.md` bug 3.

What Oxide's new content meets, beyond the bug above: none of the new effects 277 to 406 has an Expert routine, so the 452 new moves are scored only by Basic's generic checks and the damage comparison; the 51 new status moves on new effects get no Basic check at all; the seven new Protect-type moves never take the repeat penalty and the seven new Speed-lowering attacks get nothing, because those checks key on move ids; and Fairy makes the switching checks see Poison as super-effective on a Poison-immune Steel/Fairy. Teaching the AI these is element 6's later step; the Phase 4 catch-up below took the part of it that is a fix, and the changes of play of 2026-09-27 most of the rest.

## Fixes applied, 2026-09-22

One Oxide fix, twenty-four vanilla fixes and one change Ian asked for, each its own commit so any can be reverted alone. **Every vanilla fix changes how the game plays and was approved by Ian**; each is marked in `script.s` with an "Oxide, vanilla fix" comment.

| Fix | Kind | What changes in play |
|---|---|---|
| The AI's remembered ability is u16 (`ai_context.h`) | Oxide | Quark Drive, Protosynthesis, Hospitality and the rest are remembered as themselves |
| Weather flag (O1) | vanilla | Only a weather move that would set new weather gets the +5 on the first turn |
| Immunity checks for damaging moves outside the damage comparison (B6) | vanilla | 52 moves now go through the checks (every damaging move the comparison leaves out: the recharge moves, Explosion, Dream Eater, Focus Punch, Solar Beam, and the power-1 moves such as Counter, Flail and Fling among them), so Water Spout into Water Absorb, Dragon Energy into a Fairy, Explosion or Counter into a Ghost are now refused |
| Punishment's ladder (expert-2 bug 2) | vanilla | 50% +4, 25% +3, 12.5% +2, 6.25% +1 against +7 boosts or more, as its comment says, instead of summing up to +10 |
| Trick, Switcheroo and Gastro Acid on the partner (O11) | vanilla | Refused (-30), except Gastro Acid on a partner with Truant or Slow Start (+5, as before) |
| Weather Ball's type in clear weather (switching bug 1) | vanilla | All three type helpers start from Normal. Read from the compiled code, they had returned a pointer: the engine's redirection check was right by luck, but the AI's effectiveness check took the low byte of the battle system's address as the type. `Heap_Alloc` aligns to 4, so that read as Normal, Ground, Steel, Grass or Dragon for a byte of 00 to 10, and as neutral against everything above. The fix also changes AI switching, through `Move_CalcVariableType`'s callers in the switching checks and the post-knockout pick |
| Weather Ball in the AI's damage estimate (found after the write-up, from Ian's pokemow reference) | vanilla | In weather the AI now estimates the doubled power and the weather's type, as the battle sets them, instead of always a 50-power Normal move |
| Weather Ball's weather type where the AI read the listed type (QA pass before the integration) | vanilla | Basic's absorb and Levitate checks, Tag Strategy's type dispatch and the absorb-ability switch now see a rain Weather Ball as Water and a sun one as Fire. Hidden Power, Natural Gift and Judgment still read their listed type |
| Weather Ball in the post-knockout pick (same QA pass) | vanilla | A bench Weather Ball in weather is costed at double power and the weather's type, not as a 50-power Normal move |
| Trainer form Pokemon use their form's stats (pret's `docs/bugs_and_glitches.md`; a party-building fix in `trainer_data.c`, not an AI one) | vanilla | The party builder set the form after the stats were worked out, so a trainer's form Pokemon had its base form's stats. Six in Oxide change: Volkner's Rotom-Mow in both battles, Fantina's rematch Rotom-Wash, Beauty Devon's two Wormadam and Worker Jackson's |
| A lone Pokemon's spread moves read its fainted partner (`doubles.md` 1) | vanilla | Earthquake, Magnitude, Surf, Discharge and Lava Plume make no partner check once the partner's slot is empty for the rest of the battle, instead of -3, or -10 after a partner weak to them |
| Steel missing from Earthquake's partner check, Rock from Surf's (`doubles.md` 2, O7) | vanilla | -10 beside a partner weak to the move, except where a second type cancels the weakness (Bug or Grass for Earthquake, Water, Grass or Dragon for Surf) |
| Mold Breaker ignored beside an ability that protects the partner (`doubles.md` 3) | vanilla | With Mold Breaker, a partner's Levitate, Volt Absorb, Motor Drive, Water Absorb, Dry Skin or Flash Fire no longer earns the spread move a bonus |
| Follow Me with no partner (`doubles.md` 6, O9) | vanilla | -10 once the partner's slot is empty, instead of up to +3 |
| Explosion and Self-Destruct beside a partner (`doubles.md` 4) | change | -10 beside a partner, -3 beside a Rock or Steel one, nothing beside a Ghost or an empty slot |

Put to Ian and kept as vanilla has them: the faster Pokemon that almost never heals (expert-1 bug 4), the bench damage check that uses the active Pokemon's stats (expert-2 bug 10), and status moves counting as super-effective in the switching checks. The eleven battle_edits fixes (approved by Ian on 2026-09-15) are applied as eleven more commits, each titled "VANILLA FIX (battle_edits)":

| battle_edits fix | Where | In Ian's base ROM | What changes in play |
|---|---|---|---|
| Water immunity vs Dry Skin | `basic.md` B1 | yes | A Water move into a known Dry Skin Pokemon takes -12 |
| Sunny Day check | `basic.md` B2 | yes | Sunny Day takes -10 against a target with Leaf Guard and no status, not one with Hydration and a status |
| Foresight and Odor Sleuth Ghost check | `expert-1.md` bug 2 | yes | They are rewarded against a Ghost target, not for a Ghost user |
| Leaf Guard Sunny Day logic | `expert-1.md` bug 3 | yes | Sunny Day is rewarded for a Leaf Guard user without a status, not with one |
| Charge-turn scoring | `expert-2.md` bug 3 | yes | Fly, Dig, Dive, Bounce and Shadow Force take -1, not +1, into a target that resists or is immune |
| Facade status check | `expert-2.md` bug 7 | yes | Facade's +1 follows the user's status |
| Water Spout and Eruption HP check | `expert-2.md` bug 8 | yes | Both follow the user's HP, not the target's |
| Thunder scoring | `expert-1.md` bug 1 | no | Thunder reaches its weather routine |
| Discharge in doubles | `other-flags.md` O6 | no | A Ground partner is checked first, so a Swampert or Gliscor partner no longer stops Discharge |
| Fire Fang vs Wonder Guard | battle engine | no | Fire Fang no longer hits a Wonder Guard Pokemon regardless of type |
| Rage glitch | battle engine | no | Choosing another move after Rage clears only Rage, not every other volatile status |

The first seven are the ones Ian played with: the base ROM's overlay 14 carries exactly their thirteen bytes, and the source edits assembled reproduce that overlay with no byte different. Phase 3 rebuilt the game from source, so they had been missing from Oxide until now. The last four are new behaviour.

## The Phase 4 catch-up, 2026-09-26

Phase 4 changed rules the AI had its own copies of, so the AI went stale: it estimated computed powers at table power, ignored Neutralizing Gas, and still believed Platinum's Simple, trapping, Magic Guard and Lightning Rod. The catch-up (`cloud/element6-catch-up`) taught it what elements 4 and 5 and the staples rulings changed, one commit per rule. Every one of these is an Oxide fix: each makes an existing check agree with the engine as Oxide now has it, and none is a vanilla fix. No trainer yet carries a move from past Platinum's 467, so the move fixes change nothing in play until the trainer pass hands those moves out; the ability fixes act now, mostly against the player's Pokemon.

| Commit | What the AI now knows | Where |
|---|---|---|
| 1766ae164, f215db7b2 | Computed powers: Electro Ball, Stored Power, Power Trip, Retaliate, Echoed Voice, Stomping Tantrum, Temper Flare, Last Respects, Hard Press, Grav Apple, Rage Fist, Pika Papow and Veevee Volley. Electro Ball and Hard Press (power 1) now reach the damage comparison, the kill checks and the partner check. Lash Out stays at table power, since its trigger falls in the same turn | `TrainerAI_ComputedMovePower` |
| 218376d2d | Neutralizing Gas suppresses the abilities it reads, as Gastro Acid does | both ability readers, the Wonder Guard switch test |
| 993ff0a23 | Nothing traps a Ghost: it may switch, Mean Look and its kin fail on it, a Ghost roamer always escapes | `TrainerAI_ShouldSwitch`, `Basic_CheckMeanLook`, `RoamingPokemon_Main` |
| 9eb05c721 | Simple's stages are real, so only +6 stops a boost | Basic's raising checks, Tag Strategy's Acupressure |
| 57d4737ef | Keen Eye and Illuminate ignore evasion; Illuminate stops accuracy drops | Basic's accuracy and evasion checks |
| 1fafc84fa | Electric types cannot be paralysed | `Basic_CheckCannotParalyze` |
| 9dfac258a | Magic Guard no longer makes paralysis pointless | `Basic_CheckCannotParalyze` |
| dca45c8f6, 3d7cb5923 | Grass types and Overcoat are immune to powder moves (Rage Powder aside, which targets its user) | `Basic_CheckPowderImmunity` |
| 90b18098b | Lightning Rod and Storm Drain absorb; a partner with either takes a spread move whole | Basic's immunity check, Thunder Wave, Tag Strategy's Discharge and Surf |
| 500c188ca | Sap Sipper absorbs Grass attacks and Grass status moves | Basic's immunity check, `Basic_CheckSapSipper` |
| a27c8dea6, 4d050750c | Purifying Salt stops every status; Sweet Veil sleep and Pastel Veil poison, on the target or its partner; Water Bubble burns | Basic's four status checks |
| 1a6e129b1, aa0b13b1f, 7f10550c0 | Big Pecks, Flower Veil (on a Grass target or beside one) and Mirror Armor stop stat drops | Basic's stat drop checks |
| af7beb0e8 | Sturdy survives any hit from full HP | `AI_SturdySurvives`, in both kill checks |
| e022dfd46, 9264b9cc1 | Bulletproof stops the ball and bomb moves; the new sound moves meet Soundproof | `Basic_CheckBulletproof`, Basic's Soundproof list |
| c0cc01208 | Queenly Majesty stops a raised-priority move at its holder or partner, through a new command, `IfMoveHasRaisedPriority` | `Basic_CheckQueenlyMajesty` |
| 888c89759 | The new stat raisers (Shell Smash, Quiver Dance, Coil and eight more) are refused at +6, as Dragon Dance is | Basic's effect dispatch |
| 96130d20a | Status moves whose effect is not written yet do nothing, so they score -10 | Basic's effect dispatch |

Each ability check honours Mold Breaker exactly where the engine does. Most use the script's ability guess, as vanilla's do; the Sturdy cap is in C and reads the target's real ability, as the AI's other C checks do.

Checked and found already right, with nothing to change:

- **Saturn 2's permanent Trick Room.** Every "who moves first" test in the script goes through `BattleSystem_CompareBattlerSpeed`, which reads Trick Room, and Basic already scores Speed raises, Speed drops, Tailwind and Dragon Dance -10 while the room is up, so all of them hold for the whole fight. The Trick Room move itself already scores -10 under the permanent room (7657103c9). The only raw Speed reader, `TrainerAI_GetStats` behind `IfBattlerHasHigherStat` and its two siblings, is used nowhere in the script.
- **Critical hits at 1.5x.** No score reads the multiplier. The damage estimates leave critical hits out, and Expert's high-critical and Focus Energy bonuses are flat.
- **The stat and type choosers** (`cloud/element4-stat-choice`). Foul Play, Body Press, Psyshock and the rest live in `BattleSystem_CalcMoveDamage`, which the estimate calls, and Freeze-Dry and Flying Press go through the two type chart walks the AI's effectiveness checks call.
- **The held items** on the list (Eviolite, Assault Vest, Air Balloon, Rocky Helmet, Weakness Policy, the seeds) do not exist until element 7, so there is nothing to teach yet.
- **The new Protect moves** kept the AI's repeat penalty at 0, which was what the engine did then, but only by accident: `BtlCmd_TryProtection` reset the run for any move but Protect, Detect, Endure, Wide Guard and Quick Guard, so King's Shield and the rest never lost reliability. The engine and the AI were fixed together on 2026-09-27 (next section).

### Changes of play, for Ian

The catch-up listed eight ways the AI could play the new rules better. Ian wanted all eight (2026-09-27), and they are made; the next section has them.

## Changes of play and fixes, 2026-09-27

`cloud/element6-changes` made Ian's eight changes of play, one commit per rule, and two fixes. `cloud/element6-followups` made three more that Ian approved the same day: Rapid Spin's clearing, the partner check for the new spread moves, and a vanilla fix to the own-partner Lightning Rod and Storm Drain check. Every change is marked in the code with "Oxide, change (Ian, 2026-09-27)", each vanilla fix with "Oxide, vanilla fix (Ian, 2026-09-27)" and a "VANILLA FIX" commit subject. As with the catch-up, most of the move changes act only once the trainer pass gives trainers the new moves; the ability changes act now wherever a Pokemon on either side has the ability.

Four vanilla fixes are among them. They change how Platinum's own AI plays, so they are listed for Ian apart from the rest: the absorber switch now knows Motor Drive and Dry Skin (8b06bb2b5), Basic checks that the AI's own Rest can work (260718b36), Hyper Voice joins Basic's Soundproof list (d5bc49486), and Tag Strategy no longer refuses a spread move beside its own Lightning Rod or Storm Drain partner (81f6d887).

| Commit | Change | Kind |
|---|---|---|
| b42430802 | Tag Strategy: -10 for a move the foe's Lightning Rod or Storm Drain partner would draw in | change 1 |
| 2c500dd1a | Tag Strategy: aim Electric and Water moves at its own Lightning Rod or Storm Drain partner, Grass moves at a Sap Sipper one | change 2 |
| a55af5a76 | The absorber switch knows Lightning Rod, Storm Drain and Sap Sipper | change 3 |
| 8b06bb2b5 | The absorber switch knows Motor Drive and Dry Skin | change 3, VANILLA FIX |
| 4c7e307fd | The new Speed raisers take -10 under Trick Room | change 4 |
| 7516f40e6 | Expert: the new setup moves | change 5 |
| 938a08d44 | Expert: Parting Shot; Basic: when it fails | change 5 |
| b76f89126 | Expert: Strength Sap and Life Dew; Basic: when they fail | change 5 |
| e038640a4 | Expert: the new Speed-lowering attacks | change 5 |
| 8683308bf | Expert: Hex, Venoshock, Acrobatics and Bolt Beak and their kin when their power doubles | change 5 |
| 3c2f329e6 | Sticky Web and Aurora Veil, Basic and Expert | change 5 |
| 1ea62f51f | Expert: Hurricane, the Hisuian storms, the new draining, self-lowering and always-critical attacks | change 5 |
| cf2a08ed3 | First Impression and Poltergeist, Basic and Expert | change 5 |
| d2ec8fb9c | Expert: Flame Charge and the other attacks that raise Speed | change 5 |
| 8ac764a21 | Expert: Freeze Shock and Ice Burn | change 5 |
| 1c86dd3cd | Defog clearing the hazards on the AI's own side | change 6 |
| 75fbc76b6 | Rapid Spin's Speed raise | change 6 |
| 260718b36 | Basic checks the AI's own Rest (vanilla failures) | change 7, VANILLA FIX |
| 7a6143667 | Basic checks the AI's own Rest (Oxide's failures) | change 7 |
| be01afea7 | Basic refuses Taunt into Oblivious | change 7 |
| 69798bb36 | Basic refuses a Prankster status move into a Dark type | change 8 |
| fb3b0f1e3 | Tag Strategy: a Telepathy partner is safe from spread moves | change 8 |
| d5bc49486 | Hyper Voice in Basic's Soundproof list | fix, VANILLA FIX |
| a11da24d1 | The engine: the new Protect moves lose reliability in a row | fix, Oxide (element 4) |
| 1be560b12 | The AI reads the Protect run with the engine's test | fix, follows the engine |
| 895ff303 | Expert: what Rapid Spin clears on its own side | follow-up to change 6 |
| 81cf6509 | Tag Strategy: the partner check for the new spread moves | follow-up to change 8 |
| 81f6d887 | Tag Strategy: the own-partner Lightning Rod and Storm Drain check skips spread moves | VANILLA FIX |

Three new AI commands came with them, each making the engine's own test so the AI and the battle cannot disagree. `IfMoveCanBeDrawnIn` jumps when Lightning Rod or Storm Drain could draw the move being scored away from its target: aimed at one target or a random foe, used without Normalize or Mold Breaker (`BattleSystem_CheckRedirectionAbilities`). `IfPranksterBlockedByDark` jumps when the user has Prankster, the move is a status move aimed at the target (not at the user's side, the whole field or the foe's side), and the target is a Dark type (`BattleControllerPlayer_PriorityBlock`). `IfPartnerEffectivenessEquals` is `IfMoveEffectivenessEquals` with the AI's own partner in the target's place: the engine's type chart, which counts Levitate, Magnet Rise and Wonder Guard and lets Mold Breaker past them.

### How each changed check now decides

**Tag Strategy, a single-target Electric or Water move at a foe** (`TagStrategy_CheckElectricMove`, `TagStrategy_CheckWaterMove`). Discharge and Parabolic Charge, and Surf and Sparkling Aria, go to their spread checks. For any other Electric move, the AI first asks whether the move can be drawn in; if it cannot, neither check applies and the move is left alone. If it can, the foe's partner is standing, and the AI knows or guesses that partner has Lightning Rod, the move takes -10 and scoring stops; otherwise, if the AI's own partner has Lightning Rod, -10. Water moves do the same with Storm Drain. Vanilla gave the first case -1, and -8 more beside a Ground holder, and gave both cases to spread moves such as Muddy Water too, which are never drawn in; those now take nothing. The first was a change of play; the second, beside the AI's own partner, is the VANILLA FIX (81f6d887).

**Tag Strategy, a move aimed at the AI's own partner** (`TagStrategy_Partner`). A damaging Electric move at a partner with Lightning Rod, a damaging Water move at a partner with Storm Drain, a damaging Grass move at a partner with Sap Sipper, Thunder Wave at a Lightning Rod partner and a Grass status move at a Sap Sipper partner are all scored as vanilla scores Motor Drive: 62.5% of the time no change, otherwise -30 if the stat the ability raises (Sp. Atk, or Attack for Sap Sipper) is already at +6 and +3 if not. A partner without the ability still takes -30. The doubles driver keeps a move aimed at the partner only if it scores 100 or more, as before.

**The switch to an absorber** (`AI_HasAbsorbAbilityInParty`, before any move is scored). When the last attack that hit the AI's Pokemon was of a type some ability takes, and the Pokemon does not have such an ability itself, the AI looks through its bench and switches to the first Pokemon with one, half the time. The abilities are now, by type: Fire, Flash Fire; Water, Water Absorb, Storm Drain and Dry Skin; Electric, Volt Absorb, Lightning Rod and Motor Drive; Grass, Sap Sipper (`AI_AbilityAbsorbsType`). Vanilla had one per type, and never switched for a Grass hit. The other conditions are vanilla's: the hit had to be an attack, and a Pokemon with a super-effective move stays in two times in three.

**Speed raisers under Trick Room** (Basic). Quiver Dance, Shift Gear, Shell Smash, Fillet Away, Geomancy, Victory Dance and Autotomize now take -10 while Trick Room is up, the five-turn room or Saturn 2's permanent one, as Dragon Dance and Agility already did. Clangorous Soul, which raises all five stats, does not.

**Expert, the new setup moves.** Each goes to the routine vanilla uses for its nearest Platinum move. Quiver Dance, Shift Gear, Shell Smash, Fillet Away, Geomancy, Victory Dance and Clangorous Soul go to Dragon Dance's: 50% chance of +1 when slower than the target, otherwise a 72.7% chance of -1 at half HP or less. Coil and Cotton Guard go to the Defense raise, as Bulk Up does; Hone Claws and Work Up to the Attack raise; Take Heart to the Sp. Def raise, as Calm Mind does; Autotomize to the Speed raise, as Agility does. Those routines are in `expert-1.md`. Basic checks Autotomize as a Speed raise and Take Heart as Calm Mind, unless Take Heart has a status to cure.

**Expert, the switching moves.** Volt Switch and Flip Turn share U-turn's effect and have always gone to its routine. Parting Shot now does too, leaving out U-turn's check that the target resists, since it is a status move; with no Pokemon left to switch to it is scored as Growl. Basic gives Parting Shot -10 when the target's Attack and Sp. Atk are both at -6, where it fails and its user stays in.

**Expert, the new recovery.** Strength Sap and Life Dew go to the recovery routine, as Recover does (-3 at full HP, -8 when faster, otherwise a likely +2 below 70% HP). Basic gives Life Dew -8 at full HP, as Recover, and Strength Sap -10 when the target's Attack is at -6, where it fails.

**Expert, the Speed-lowering attacks.** The routine for attacks that may lower Speed names the ones that always do, by move id. Low Sweep, Bulldoze, Electroweb, Glaciate, Drum Beating and Pounce join Icy Wind, Rock Tomb and Mud Shot: into a target that does not resist, a 72.7% chance of +2 when slower, -3 when already faster.

**Expert, attacks whose power doubles in their effect script**, which the damage estimate does not see. Each now has a routine in Wake-Up Slap's shape, -1 into a target that resists or is immune and +1 when the power doubles: Hex and Infernal Parade against a target with a status or Comatose, Venoshock and Barb Barrage against a poisoned target, Acrobatics when the user holds no item, Bolt Beak and Fishious Rend when the user is faster.

**Sticky Web and Aurora Veil.** Basic gives Sticky Web -10 when the target's side already has one or the target is its side's last Pokemon, as Spikes; Expert scores it as Spikes. Basic gives Aurora Veil -8 while it is up, as Reflect, and -10 outside hail, where it fails. Expert scores it in Reflect's shape: -2 below half HP, a 50% chance of +1 at 90% or more, and a 75% chance of +1 when the target's last move was an attack of either class.

**Expert, attacks that work as a Platinum move does.** Hurricane goes to Thunder's routine (80.5% chance of -3 into a resisting target or in sun, +1 in rain). The three Hisuian storms go to a copy without the sun part, since the engine keeps their accuracy in sun. Draining Kiss, Oblivion Wing, Bouncy Bubble and Matcha Gotcha go to Giga Drain's; V-create, Clanging Scales and Hyperspace Fury to Close Combat's; Spin Out to Hammer Arm's; Storm Throw, Frost Breath, Wicked Blow, Flower Trick and Surging Strikes to the high critical routine; Freeze Shock and Ice Burn to Skull Bash's. Flame Charge, Aqua Step, Trailblaze and Esper Wing share Rapid Spin's new routine (below).

**First Impression and Poltergeist.** Basic gives First Impression -10 after its user's first turn out, through Fake Out's check, and Expert gives it Fake Out's +2. Basic gives Poltergeist -10 into a target holding no item.

**Defog** (Basic and Expert). Defog now clears the hazards on both sides and the target's Aurora Veil. Basic's "useless" test (-10) no longer fires when the AI's own side has Spikes, Toxic Spikes, Stealth Rock or Sticky Web, or the target's side has Aurora Veil or Sticky Web. Expert adds +2 when the AI's side has a hazard and the AI has a benched Pokemon, and then scores the target's side as vanilla does: its screens and Aurora Veil favour Defog, its hazards, which the AI would rather keep, count against it.

**Rapid Spin and the attacks that raise Speed** (Expert, `Expert_RapidSpin`, then `Expert_SpeedUpOnHit`). Rapid Spin first: into an immune target it clears nothing and takes -1, and scoring stops. Otherwise it takes +2, once, when its user is bound or seeded, or when its side has Spikes, Toxic Spikes, Stealth Rock or Sticky Web and a party member is left to switch in, as Defog's own-side bonus. Then Rapid Spin, Flame Charge and its kin are scored alike: -1 into a target that resists; otherwise a 50% chance of +1 when the user is not already faster, unless Trick Room is up or its Speed is at +6. Vanilla valued none of Rapid Spin's clearing; the first job valued only its Speed raise, and Ian approved the clearing as a follow-up.

**Rest** (Basic, new). -8 at full HP; -10 with Insomnia or Vital Spirit; -10 during an Uproar unless the user has Soundproof. Those three are vanilla's failures, the VANILLA FIX. Oxide's add -10 with Purifying Salt, with Leaf Guard in sun, and with Sweet Veil on the user or its standing partner in a double battle. Expert's Rest routine is unchanged and still applies after.

**Taunt** (Basic, new). -10 into a target the AI knows or guesses has Oblivious, unless the user has Mold Breaker.

**Prankster** (Basic). A status move the user's Prankster raises takes -10 into a Dark-type target, through `IfPranksterBlockedByDark`.

**The new spread moves beside the AI's partner** (Tag Strategy). Each of element 4's spread moves that hits the partner too now has a partner check. Bulldoze is scored as Earthquake; Parabolic Charge as Discharge; Searing Shot and Mind Blown as Lava Plume; Sparkling Aria as Surf, after +2 beside a Soundproof partner. Brutal Swing, Boomburst, Sludge Wave, Petal Blizzard, Synchronoise and Misty Explosion go to `TagStrategy_SpreadMove`, which reads the type chart against the partner: +2 when the partner takes no damage (immune by type, Levitate or Wonder Guard, Telepathy, or Soundproof against Boomburst), +3 for a Sap Sipper partner against Petal Blizzard, -10 when the partner is weak to the move, and -3 otherwise. Misty Explosion follows Explosion: no change beside an unharmed partner, -3 beside one that resists, -10 beside any other. An empty partner slot changes nothing, and the user's Mold Breaker gets past every ability named here.

**Telepathy** (Tag Strategy's spread moves). A partner with Telepathy takes no damage from its partner's moves, unless the user has Mold Breaker. Beside one, Earthquake and Magnitude take +2 (as beside Levitate), Discharge +3 (as beside a Ground type), Surf and Lava Plume +2, and Explosion and Self-Destruct no change (as beside a Ghost), in place of the penalties for a partner the move would hurt.

**Soundproof** (Basic). Hyper Voice takes -10 into a Soundproof target, as the other sound moves do. Vanilla's list lacked it though the engine's has it.

**The Protect run** (the engine and the AI). The engine now keeps the run of Protect successes going after any move on Protect's effect, Endure, Wide Guard or Quick Guard (`Move_KeepsProtectRun`), where it named Protect, Detect and Endure (and Oxide's two guards). So King's Shield, Spiky Shield, Baneful Bunker, Obstruct, Silk Trap, Burning Bulwark and Max Guard fall to one in two, one in four and one in eight when used in a row, as Protect does. `AICmd_LoadProtectChain` calls the same test, so Expert's Protect routine sees the run too.

### Still open after the changes

This list is superseded by the routing of 2026-09-27 below: every learnable new move now takes the routine of its nearest Platinum effect, or none, and [expert-new-moves.md](expert-new-moves.md) has each one. Of the effects this paragraph named, the trapping attacks, Dragon Tail, Incinerate, Entrainment, Noble Roar and Tearful Look, Venom Drench, Burn Up and Double Shock, Clear Smog, Mortal Spin, and Smack Down and Thousand Arrows now have one, and so does Circle Throw, which no species learns but which shares Dragon Tail's effect. Jaw Lock, Throat Chop and the other moves no species learns are not routed, since the ruling covers learnable moves. The status moves whose effects are unwritten keep Basic's -10 from the catch-up.

Two gaps found on the way were put to Ian, and both are closed by the follow-ups above: the partner check for the new spread moves, and the own-partner draw-in check firing for spread moves (the VANILLA FIX). No trainer in a double battle today carries a new spread move, or a spread Water or Electric move beside a Storm Drain or Lightning Rod partner, so neither acts until the trainer pass gives them out.

## The new moves' routines, 2026-09-27

Ian's ruling: the moves added since Platinum follow Platinum's own Expert pattern. Each learnable new move takes the Expert routine of its nearest Platinum effect, judged by what its effect script does, where that effect has one, and none where Platinum gives its equivalents none; Platinum's own moves without a routine stay as they are ([expert-gaps.md](expert-gaps.md)). It is a change of play, marked in the code "Oxide, change (Ian, 2026-09-27)". Of 156 learnable new moves, 65 are now scored by a routine and 91 are not; [expert-new-moves.md](expert-new-moves.md) has every move, the reasons, and eleven judgment calls for Ian where a near routine would misjudge the move. Two routines are trimmed copies, `Expert_ClearSmog` (Haze's, the target's half) and `Expert_MortalSpin` (Rapid Spin's clearing, without the Speed raise), and Shore Up is scored as Recover, since the engine heals it by its own rule rather than Synthesis's.

## The parts

| File | Covers |
|---|---|
| `basic.md` | the Basic flag: refusing moves that cannot work |
| `expert-1.md` | the Expert flag, its dispatch and its first half |
| `expert-2.md` | the Expert flag, second half |
| `other-flags.md` | every other flag, and the double-battle driver |
| `switching-and-items.md` | the damage the AI calculates, switching, replacements and item use |
| `doubles.md` | the doubles review: which of the double-battle faults Oxide's own double battles reach, and the fixes proposed for them |
| `expert-gaps.md` | Platinum's own moves with no Expert routine, grouped by effect, with what else scores them |
| `expert-new-moves.md` | every learnable new move and the Expert routine it takes, or why none |

Each part ends with its apparent bugs, every one labelled as present in vanilla Platinum or introduced by Oxide, then the battle_edits fixes that fall in it, then what Oxide's new moves, abilities and types do there. Fixing a bug that is present in vanilla is Ian's call and is always called out as such.
