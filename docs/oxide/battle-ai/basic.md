# The Basic flag

The Basic flag (bit 0, `Basic_Main`, `src/battle/trainer_ai/script.s` lines 52 to 1622) stops the AI from choosing a move that cannot work or that does nothing useful right now: an attack the target is immune to, a status move on a target that already has a status, a stat boost at +6, a heal at full HP, a screen that is already up. It never makes a move more attractive, apart from one small bonus for throwing away a harmful held item with Fling. Every trainer in Oxide carries it (the README has the count), so its penalties apply in every trainer battle, and because it is bit 0 it always runs first, on scores that are still at 100.

Everything below is read from the code in this tree. `script.s` is byte for byte the same as vanilla on `main`, so every script line number here is also the vanilla line number. The C commands it calls are unchanged from vanilla too, except where the Oxide section says otherwise.

## How to read the scores

Five facts about the commands decide almost every result, and each was checked in `src/battle/trainer_ai/trainer_ai.c`.

A penalty ends the evaluation of that move for this flag. Every `ScoreMinusN` label (lines 1567 to 1621) adds its value and then runs `PopOrEnd`. Basic never pushes onto the script stack, so `PopOrEnd` always finishes the move (`AICmd_PopOrEnd`, line 2568, sets `AI_STATUS_FLAG_DONE` when the stack is empty). So in any chain of checks only the first one that fires counts, and a move gets at most one penalty from Basic. The exceptions are the few places that call `AddToMoveScore` inline and then carry on (Hail, Healing Wish, Lunar Dance, Recover, Last Resort, Worry Seed, Fling); those are stated where they occur.

The AI knows its own Pokemon exactly but guesses the target's ability. `AICmd_LoadBattlerAbility` (line 1170) returns the attacker's real ability. For the target it returns, in this order: no ability if the target's ability is suppressed by Gastro Acid; the ability the AI has recorded for that battler, if any (recorded whenever the ability's name appears in a battle message or a script changes it, `BattleAI_SetAbility` in `battle_script.c`); the real ability if it is Shadow Tag, Magnet Pull or Arena Trap; otherwise a guess from the species data. If the species lists two abilities, the guess is a fresh coin flip between them on every call (line 1195); if it lists one, that one. In this file, "guess rule" next to a check means: the check is certain if the ability has been revealed or the species has only that ability, it fires half the time if the ability is one of two different ones the species can have, and it never fires otherwise. Each `LoadBattlerAbility` is a separate flip, so two checks on the same move can disagree about the same target, and each move slot is judged with its own flips.

`CheckBattlerAbility`, used once (line 441), guesses differently. When the ability is unrevealed and the species has two abilities, it answers "unknown" if either of them is the one asked about, and "does not have" otherwise. Only "has" triggers the penalty, so this check fires only for a revealed ability or a species with a single ability.

The type check sees the truth. `IfMoveEffectivenessEquals` (line 1311) runs the real type chart, `BattleSystem_ApplyTypeChart`, with the real target, and counts the move as immune if the chart says so, or if the target really has Levitate against a Ground move, is under Magnet Rise, or really has Wonder Guard against a move that is not super effective. Mold Breaker is honoured, and so are Foresight, Scrappy, Gravity, Iron Ball, Roost and Miracle Eye. The Wonder Guard part applies only when the move is "on its damaging turn", which during move choice is false for Bide, Razor Wind, Sky Attack, Skull Bash, Solar Beam, Fly, Dig, Dive, Bounce and Fire Fang (`MoveIsOnDamagingTurn`, `battle_lib.c` line 7659). The result is then put in a bucket by its multiplier on a base of 40, and the buckets Basic asks about are exactly 0 (immune), exactly 80 (called "2x") and exactly 160 (called "4x"), with 120 and 240 folded into 2x and 4x to allow for STAB.

Numbers in the checks mean what the engine stores. Stat stages run from 0 (minus 6) through 6 (neutral) to 12 (plus 6). HP percent is `curHP * 100 / maxHP` rounded down. "No Pokemon left" means `CountAlivePartyBattlers` returned 0: it counts party members that are alive, not eggs, and not on the field (in doubles, neither active slot counts).

## Entry: the checks every move goes through

| Lines | What it tests | Score change |
|---|---|---|
| 54 | The target is on the AI's own side (the partner, in doubles) | Basic does nothing for this move and this target |
| 57, 58 | The move is Fissure or Horn Drill | none; jumps straight to the immunity check at 65 |
| 62, 63 | Damage comparison, see below. Status moves and the moves below that the comparison skips jump to 115 | none |
| 68 | The move cannot affect the target by the real type chart (see above) | -10, end |
| 69, 70 | The attacker has Mold Breaker | none; skips the ability checks at 71 to 79 |
| 71 to 73, 81 to 84 | Target has Volt Absorb or Motor Drive (guess rule) and the move is Electric | -12, end |
| 74, 86 to 89 | Target has Water Absorb (guess rule) and the move is Water | -12, end |
| 75, 91 to 94 | Target has Flash Fire (guess rule) and the move is Fire | -12, end |
| 76, 96 to 99 | Target has Wonder Guard (guess rule) and the move is not in the 2x or 4x bucket | -12, end |
| 77, 101 to 104 | Target has Levitate (guess rule) and the move is Ground | -12, end |
| 78, 106 to 109 | Meant to be Dry Skin against Water; can never fire (bug B1) | none |
| 112, 113 | The damage comparison again; both outcomes continue at 115 | none |
| 115 to 131 | Target has Soundproof (guess rule), the attacker lacks Mold Breaker, and the move is Growl, Roar, Sing, Supersonic, Screech, Snore, Uproar, Metal Sound, GrassWhistle, Bug Buzz or Chatter | -10, end |

The damage comparison at lines 62 and 112 (`AICmd_FlagMoveDamageScore`, line 1012) works out the maximum-roll damage of all four of the attacker's moves and records whether this move is the strongest. Basic ignores that answer. The only thing it uses is whether a comparison was made at all: none is made for a move with power 0 or 1, unless its effect is in the "alternative power" list (Hidden Power, Gyro Ball, Natural Gift, Judgment, Dragon Rage, Seismic Toss and Night Shade, Psywave, Return, Frustration, SonicBoom, Low Kick and Grass Knot), and none is made for a move whose effect is in the "no damage calculation" list at line 31 (Selfdestruct and Explosion, Dream Eater, Razor Wind, Sky Attack, Hyper Beam and the other recharge moves, Skull Bash, Solar Beam, Spit Up, Focus Punch, Superpower, Eruption and Water Spout, Sucker Punch, Head Smash). Every such move skips lines 65 to 109, the immunity checks. Most of them get an equivalent check later from their own effect handler; the ones that do not are bug B6. The comparison uses no random number, so it does not disturb the rolls.

The target's types are read straight from the battle state, so type immunities are always known. Absorbing abilities, Wonder Guard, Levitate and Soundproof go through the guess rule. The ability checks at 72 to 77 and the absorb checks use the move's listed type from its data (`LoadTypeFrom LOAD_MOVE_TYPE`), which is Normal for Hidden Power, Weather Ball, Judgment and Natural Gift, whatever type they really are.

Because line 68 already gives -10 for a target that really has Levitate or Wonder Guard, the -12 at lines 76 and 77 in practice fires when the AI's guess says the target has the ability and the truth says it does not (for example Bronzong, which can have Levitate or Heatproof). For Fire Fang, Fly, Dig, Dive and Bounce, whose Wonder Guard immunity line 68 does not see, the -12 is the only Wonder Guard penalty. Razor Wind and Skull Bash skip the entry checks and get -10 from their handler instead, and Solar Beam and Sky Attack get nothing (bug B6).

The entry labels are `Basic_Main` (52), `Basic_CheckForImmunity` (65), the five absorb and immunity branches `Basic_CheckElectricAbsorption`, `Basic_CheckWaterAbsorption`, `Basic_CheckFireAbsorption`, `Basic_CheckWonderGuard`, `Basic_CheckGroundAbsorption` and the dead `Basic_CheckWaterAbsorption2` (81 to 109), `Basic_NoImmunityAbility` (111), `Basic_CheckSoundproof` (115) and `Basic_ScoreMoveEffect` (133).

## The effect dispatch

Lines 133 to 285 compare the move's battle effect against a list and jump to a handler; line 286 ends the flag with no change for any effect not listed. So a move whose effect is missing from this list gets only the entry checks above. The handlers follow, grouped by purpose, each with the dispatch lines that reach it. A move named in a handler is an example of that effect, not the whole list.

Each handler below is named with its full line range. The labels inside those ranges are its internal branches and are covered by its rows: every name ending in `_Terminate`, `_NoSimple`, `_Simple`, `_CheckStatStages`, `_Levels`, `_CheckGender`, `_CheckMale`, `_CheckFemale`, `_CheckStatStage`, `_BothMale`, `_BothFemale`, `_GhostType`, `_ThunderWave`, `_ImmuneToStatus`, `_Hydration` and `_StatusOrSafeguard`; `Basic_CheckLastMon` and `Basic_Explode_Terminate` inside the Explosion handler; `Basic_CheckCurrentWeatherIsRain` and `Basic_CheckCurrentWeatherIsSun` inside the two weather handlers; `Basic_CheckGuardSwap_SpAttack` and `Basic_CheckGuardSwap_SpDefense` inside the two swap handlers; `Basic_FlingPoison`, `Basic_FlingPoison_AttackerChecks`, `Basic_FlingBurn`, `Basic_FlingBurn_AttackerChecks`, `Basic_FlingParalyze` and the three item tables `Basic_FlingItems_Poison`, `_Burn` and `_Paralyze` inside Fling; the four `Basic_PsychoShift_*` labels inside Psycho Shift; and the data table `Basic_NaturalGiftBerries` inside Natural Gift.

### Putting a status on the target

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckCannotSleep`, 288 to 295 | 134 (Sing, Spore, Hypnosis and the rest), 239 (Yawn) | Target already has any major status | -10 |
| | | Target's side has Safeguard | -10 |
| | | Target has Insomnia or Vital Spirit (guess rule) | -10 |
| `Basic_CheckCannotPoison`, 519 to 547 | 155 (Toxic), 179 (PoisonPowder, Poison Gas) | Target is Steel or Poison type | -10 |
| | | Target has Immunity, Magic Guard or Poison Heal (guess rule) | -10 |
| | | Target has Leaf Guard (same guess as above) and it is sunny | -10 |
| | | Target has Hydration (a second, separate guess) and it is raining | -10 |
| | | Target already has a status, or has Safeguard | -10 |
| `Basic_CheckCannotParalyze`, 612 to 631 | 180 (Stun Spore, Thunder Wave, Glare) | The move cannot affect the target by type (Thunder Wave on Ground, Glare on Ghost) | -10 |
| | | Target has Limber or Magic Guard (guess rule) | -10 |
| | | The move is Thunder Wave, the attacker lacks Mold Breaker, and the target has Motor Drive or Volt Absorb (a second guess) | -10 |
| | | Target already has a status, or has Safeguard | -10 |
| `Basic_CheckCannotBurn`, 879 to 890 | 231 (Will-O-Wisp) | Target has Water Veil or Magic Guard (guess rule) | -10 |
| | | Target already has a status | -10 |
| | | Target is Fire type | -10 |
| | | Target has Safeguard | -10 |
| `Basic_CheckCannotConfuse`, 597 to 605 | 163 (Supersonic, Confuse Ray, Sweet Kiss), 201 (Swagger), 230 (Flatter) | Target is already confused | -5 |
| | | Target has Own Tempo (guess rule) | -10 |
| | | Target has Safeguard | -10 |
| `Basic_CheckCannotAttract`, 731 to 752 | 202 (Attract) | Target is already infatuated | -10 |
| | | Target has Oblivious (guess rule) | -10 |
| | | Attacker is genderless, or target is the same gender or genderless | -10 |
| `Basic_CheckNightmare`, 321 to 327 | 194 (Nightmare) | Target already has Nightmare | -10 |
| | | Target is not asleep | -8 |
| | | Target has Magic Guard (guess rule) | -10 |
| `Basic_CheckCannotLeechSeed`, 639 to 648 | 183 (Leech Seed) | Target already seeded | -10 |
| | | Target is Grass type | -10 |
| | | Target has Magic Guard (guess rule) | -10 |
| `Basic_CheckCanPsychoShift`, 1301 to 1351 | 264 (Psycho Shift) | Attacker has no status, or target already has one, or target has Safeguard | -10 |
| | | Attacker is poisoned and has Poison Heal | -10 |
| | | Attacker is poisoned and target is Poison or Steel, or has Immunity, Poison Heal or Magic Guard (guess rule) | -10 |
| | | Attacker is burned and target is Fire, or has Magic Guard or Water Veil (guess rule) | -10 |
| | | Attacker is paralysed and target has Limber (guess rule) | -10 |
| | | Attacker is asleep or frozen | no further check |

The checks run top to bottom and the first that fires ends the move. So for Toxic on a statused Poison type the answer is -10 either way, but for Confuse Ray the order matters: a target that is already confused gets -5 and the Own Tempo check is never reached.

### Raising the attacker's own stats

Each of these handlers checks the attacker's real stat stages and real ability, so none is random. With Simple a stage of +3 counts as maxed, because Simple doubles stages in the damage formula; the code tests "greater than 8", that is +3 or higher, although the comment at line 340 says +2.

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckHighStatStage_Attack`, 343 to 351 | 137 (Meditate, Sharpen, Howl), 164 (Swords Dance), and by falling through from Belly Drum | Attack at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_Defense`, 353 to 361 | 138 (Harden, Withdraw), 165 (Barrier, Acid Armor, Iron Defense), 222 (Defense Curl) | Defense at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_Speed`, 363 to 372 | 139 (none in vanilla), 166 (Agility, Rock Polish) | Trick Room is up | -10 |
| | | Speed at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_SpAttack`, 374 to 382 | 140 (Growth), 167 (Tail Glow, Nasty Plot) | Sp. Atk at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_SpDefense`, 384 to 392 | 141 (none), 168 (Amnesia) | Sp. Def at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_Accuracy`, 394 to 405 | 142, 169 (no move in vanilla or Oxide) | Target has No Guard (guess rule), or attacker has No Guard | -10 |
| | | Accuracy at +6, or +3 with Simple | -10 |
| `Basic_CheckHighStatStage_Evasion`, 407 to 418 | 143 (Double Team), 170 (none), 195 (Minimize) | Target has No Guard (guess rule), or attacker has No Guard | -10 |
| | | Evasion at +6, or +3 with Simple | -10 |
| `Basic_CheckBellyDrum`, 335 to 337 | 216 (Belly Drum) | Attacker at 50% HP or less | -10, else falls into the Attack check above |
| `Basic_CheckCosmicPower`, 949 to 963 | 247 (Cosmic Power, Defend Order) | With Simple: Defense or Sp. Def at +3 | -10 |
| | | Without: Defense at +6 | -10 |
| | | Without: Sp. Def at +6 | -8 |
| `Basic_CheckBulkUp`, 965 to 979 | 248 (Bulk Up) | With Simple: Attack or Defense at +3 | -10 |
| | | Without: Attack at +6 / Defense at +6 | -10 / -8 |
| `Basic_CheckCalmMind`, 986 to 1000 | 250 (Calm Mind) | With Simple: Sp. Atk or Sp. Def at +3 | -10 |
| | | Without: Sp. Atk at +6 / Sp. Def at +6 | -10 / -8 |
| `Basic_CheckDragonDance`, 1002 to 1019 | 251 (Dragon Dance) | Trick Room is up | -10 |
| | | With Simple: Attack or Speed at +3 | -10 |
| | | Without: Attack at +6 / Speed at +6 | -10 / -8 |
| `Basic_CheckCurse`, 679 to 705 | 196 (Curse) | Attacker is Ghost type: target already cursed, or target has Magic Guard (guess rule) | -10 |
| | | Not Ghost, with Simple: Attack or Defense at +3 | -10 |
| | | Not Ghost, without: Attack at +6 / Defense at +6 | -10 / -8 |
| `Basic_CheckAcupressure`, 1135 to 1158 | 260 (Acupressure) | Any one of the seven stats at +6, or at +3 with Simple | -10 |
| `Basic_CheckAlreadyPumpedUp`, 592 to 595 | 162 (Focus Energy) | Attacker already has Focus Energy | -10 |
| `Basic_CheckMaxStockpile`, 835 to 839 | 225 (Stockpile) | Stockpile count already 3 | -10 |

The two-stat moves only penalise the second stat by -8, so Calm Mind at +6 Sp. Def but not Sp. Atk still loses 8 points: the AI treats a half-wasted boost as nearly as bad as a wasted one.

### Lowering the target's stats

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckLowStatStage_Attack`, 428 to 432 | 144 (Growl), 171 (Charm, FeatherDance) | Target's Attack at -6 | -10 |
| | | Target has Hyper Cutter (guess rule) | -10 |
| `Basic_CheckLowStatStage_Defense`, 434 to 436 | 145 (Tail Whip, Leer), 172 (Screech) | Target's Defense at -6 | -10 |
| `Basic_CheckLowStatStage_Speed`, 438 to 443 | 146 (String Shot), 173 (Cotton Spore, Scary Face) | Trick Room is up | -10 |
| | | Target's Speed at -6 | -10 |
| | | Target has Speed Boost, by `CheckBattlerAbility` (revealed, or the species' only ability) | -10 |
| `Basic_CheckLowStatStage_SpAttack`, 445 to 447 | 147, 174 (no vanilla move; Oxide's Confide and Eerie Impulse) | Target's Sp. Atk at -6 | -10 |
| `Basic_CheckLowStatStage_SpDefense`, 449 to 451 | 148 (none), 175 (Fake Tears, Metal Sound) | Target's Sp. Def at -6 | -10 |
| `Basic_CheckLowStatStage_Accuracy`, 453 to 460 | 149 (Sand-Attack, SmokeScreen, Kinesis, Flash), and 176 by mistake (bug B3) | Target's Accuracy at -6 | -10 |
| | | Attacker has No Guard, or target has Keen Eye or No Guard (guess rule) | -10 |
| `Basic_CheckLowStatStage_Evasion`, 462 to 467 | 150 (Sweet Scent), and 177 by mistake (bug B3) | Target's Evasion at -6 | -10 |
| | | Attacker has No Guard, or target has No Guard (guess rule) | -10 |
| `Basic_CheckClearBodyEffect`, 469 to 473 | the end of every handler above | Target has Clear Body or White Smoke (a separate guess) | -10 |
| `Basic_CheckTickle`, 933 to 947 | 246 (Tickle) | Attacker lacks Mold Breaker and target has Clear Body or White Smoke (guess rule) | -10 |
| | | Target's Attack at -6 / Defense at -6 | -10 / -8 |
| `Basic_CheckCaptivate`, 1508 to 1538 | 283 (Captivate) | Attacker lacks Mold Breaker and target has Oblivious, Clear Body or White Smoke (guess rule) | -10 |
| | | Attacker genderless, or the two are the same gender, or target genderless | -10 |
| | | Target's Sp. Atk at -6 | -10 |
| `Basic_CheckMemento`, 759 to 778 | 232 (Memento) | Attacker lacks Mold Breaker and target has Clear Body or White Smoke (guess rule) | -10 |
| | | Target's Attack at -6 / Sp. Atk at -6 | -10 / -8 |
| | | Attacker has no Pokemon left | -10 |

The single-stat handlers do not check Mold Breaker, so a Mold Breaker attacker is still told Growl will fail on a Clear Body target, although Tickle, Captivate and Memento get this right (bug B8).

### Stat stage swaps and resets

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckStatStageImbalance`, 475 to 497 | 151 (Haze), 217 (Psych Up), 278 (Heart Swap) | None of the attacker's seven stages is below neutral and none of the target's is above neutral | -10 |
| `Basic_CheckPowerSwap`, 1392 to 1404 | 272 (Power Swap) | Target's Attack stage is not higher than the attacker's, and neither is its Sp. Atk stage | -10 |
| `Basic_CheckGuardSwap`, 1406 to 1418 | 273 (Guard Swap) | The same for Defense and Sp. Def | -10 |
| `Basic_CheckPowerTrick`, 1358 to 1361 | 268 (Power Trick; Oxide's Power Shift) | Attacker already under Power Trick | -10 |

`DiffStatStages` returns the target's stage minus the attacker's, so "less than 1" at lines 1396, 1401, 1410 and 1415 means the swap would gain nothing. The label at line 1399 is called `Basic_CheckGuardSwap_SpAttack` but belongs to Power Swap; the name is wrong and the logic is right.

### Screens, field effects and one-time conditions

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckAlreadyUnderLightScreen`, 549 to 552 | 156 (Light Screen) | Attacker's side already has Light Screen | -8 |
| `Basic_CheckAlreadyUnderReflect`, 607 to 610 | 178 (Reflect) | Attacker's side already has Reflect | -8 |
| `Basic_CheckAlreadyUnderMist`, 587 to 590 | 161 (Mist) | Attacker's side already has Mist | -8 |
| `Basic_CheckAlreadyUnderSafeguard`, 754 to 757 | 206 (Safeguard) | Attacker's side already has Safeguard | -8 |
| `Basic_CheckLuckyChant`, 1378 to 1381 | 270 (Lucky Chant) | Attacker's side already has Lucky Chant | -10 |
| `Basic_CheckTailwind`, 1128 to 1133 | 259 (Tailwind) | Trick Room is up, or Tailwind already on the attacker's side | -10 |
| `Basic_CheckGravityActive`, 1026 to 1029 | 254 (Gravity) | Gravity already up | -10 |
| `Basic_CheckTrickRoom`, 1501 to 1506 | 282 (Trick Room) | The attacker would move first, or it is a speed tie | -10 |
| `Basic_CheckCanMudSport`, 928 to 931 | 245 (Mud Sport) | Attacker already under Mud Sport | -10 |
| `Basic_CheckWaterSport`, 981 to 984 | 249 (Water Sport) | Attacker already under Water Sport | -10 |
| `Basic_CheckAlreadyIngrained`, 906 to 909 | 236 (Ingrain) | Attacker already rooted | -10 |
| `Basic_CheckAquaRing`, 1456 to 1459 | 279 (Aqua Ring) | Attacker already has Aqua Ring | -10 |
| `Basic_CheckMagnetRise`, 1461 to 1474 | 280 (Magnet Rise) | Attacker already under Magnet Rise, has Levitate, or is Flying type | -10 |
| `Basic_CheckCamouflage`, 1021 to 1024 | 252 (Camouflage) | Attacker has used Camouflage already | -10 |
| `Basic_CheckCannotSubstitute`, 633 to 637 | 181 (Substitute) | Attacker already behind a Substitute | -8 |
| | | Attacker at 25% HP or less | -10 |
| `Basic_CheckCanImprison`, 917 to 921 | 242 (Imprison) | Attacker has already used Imprison, or target is already imprisoned | -10 |
| `Basic_CheckFutureSight`, 823 to 827 | 220 (Future Sight, Doom Desire) | A Future Sight is already pending on either side | -12 |
| `Basic_CheckHelpingHand`, 892 to 896 | 234 (Helping Hand) | Not a double battle | -10 |
| `Basic_CheckFirstTurnInBattle`, 829 to 833 | 224 (Fake Out) | Not the attacker's first turn out | -10 |
| `Basic_CheckCopycat`, 1383 to 1390 | 271 (Copycat) | First turn of the battle and the attacker moves first | -10 |
| `Basic_CheckLastResort`, 1420 to 1426 | 275 (Last Resort) | The attacker has not yet used every other move it knows (or knows only Last Resort) | -10 |
| none | 221 (Teleport) | always, since Teleport cannot flee a trainer battle | -10 |

The Trick Room check uses `BattleSystem_CompareBattlerSpeed`, which already turns the order round under Trick Room, so a Trick Room that is up and helping the AI also scores -10 (using it again would end it). Future Sight checks the attacker's own side as well, so the AI will not start one while the player has one pending against it.

### Volatile conditions on the target

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckCannotDisable`, 650 to 653 | 184 (Disable) | Target already disabled | -8 |
| `Basic_CheckCannotEncore`, 655 to 658 | 188 (Encore) | Target already encored | -8 |
| `Basic_CheckTorment`, 874 to 877 | 229 (Torment) | Target already tormented | -10 |
| `Basic_CheckMeanLook`, 674 to 677 | 193 (Mean Look, Block, Spider Web) | Target already trapped | -10 |
| `Basic_CheckForesight`, 715 to 718 | 198 (Foresight, Odor Sleuth) | Target already identified | -10 |
| `Basic_CheckMiracleEye`, 1031 to 1034 | 255 (Miracle Eye) | Target already under Miracle Eye | -10 |
| `Basic_CheckLockOn`, 665 to 672 | 190 (Lock-On, Mind Reader) | Target already locked on, or either side has No Guard (target by guess rule) | -10 |
| `Basic_CheckPerishSong`, 720 to 723 | 199 (Perish Song) | Target already has a Perish count | -10 |
| `Basic_CheckHealBlock`, 1353 to 1356 | 266 (Heal Block) | Target already under Heal Block | -10 |
| `Basic_CheckEmbargo`, 1184 to 1197 | 262 (Embargo) | Target already under Embargo | -10 |
| | | Target has an item Recycle could restore, and the battle is in the Frontier | -10 |
| `Basic_CheckGastroAcid`, 1363 to 1376 | 269 (Gastro Acid) | Target's ability already suppressed | -10 |
| | | Target has Multitype, Truant, Slow Start, Stench, Run Away, Pickup or Honey Gather (guess rule) | -10 |
| `Basic_CheckWorrySeed`, 1428 to 1443 | 276 (Worry Seed) | Target has Truant, Insomnia, Vital Spirit or Multitype (guess rule) | -10 |
| | | Target is asleep and the AI has not seen it use Sleep Talk or Snore | -10 |

The Worry Seed rule is deliberate: in Generation 4 it wakes a sleeping target, so the AI refuses to wake a target that could not act while asleep. The Embargo rule is hard to read as intended; see the note after the bug list.

### Weather

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckSandstorm`, 725 to 729 | 200 (Sandstorm) | It is already sandstorming | -8 |
| `Basic_CheckRainDance`, 786 to 801 | 214 (Rain Dance) | Attacker lacks Swift Swim and Hydration, target has Hydration (guess rule), and target has a status | -8 |
| | | It is already raining | -8 |
| `Basic_CheckSunnyDay`, 803 to 821 | 215 (Sunny Day) | Attacker lacks Flower Gift, Leaf Guard and Solar Power, target has Hydration (guess rule), and target has a status | -10 (bug B2) |
| | | It is already sunny | -8 |
| `Basic_CheckHail`, 853 to 872 | 228 (Hail) | It is already hailing | -8, end |
| | | Otherwise, target has Ice Body (guess rule) | -8, and carry on |
| | | ... and then the attacker also has Ice Body | +8 (bug B4) |

Weather is read from the field flags without regard to Cloud Nine. The Rain Dance rule makes sense: rain would cure a Hydration target's status, unless the AI's own Pokemon gains from rain as well.

### Hazards

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckSpikes`, 707 to 713 | 197 (Spikes) | Three layers already down, or target has no Pokemon left | -10 |
| `Basic_CheckToxicSpikes`, 1445 to 1454 | 277 (Toxic Spikes) | Two layers already down, or target has no Pokemon left | -10 |
| `Basic_CheckStealthRock`, 1540 to 1547 | 284 (Stealth Rock) | Stealth Rock already down, or target has no Pokemon left | -10 |
| `Basic_CheckDefog`, 1476 to 1499 | 281 (Defog) | If the target's Evasion is above -6, or its side has Light Screen or Reflect, or the weather is fog: no change | none |
| | | Otherwise, target has no Pokemon left | -10 |
| | | Otherwise, the target's side has no Spikes, Stealth Rock or Toxic Spikes | -10 |

Line 1454 is a second `PopOrEnd` that can never run. Defog's hazard logic looks copied from the hazard-setting moves; see bug B10.

### Healing and HP

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckCanRecoverHP`, 511 to 517 | 154 (Recover, Softboiled, Milk Drink, Slack Off, Heal Order), 210 (Morning Sun, Synthesis, Moonlight; Oxide's Shore Up), 211, 212, 223 (unused effects), 253 (Roost), and from Swallow | Attacker at exactly 100% HP | -8 |
| `Basic_CheckCanSpitUpOrSwallow`, 841 to 851 | 226 (Spit Up), 227 (Swallow) | The move cannot affect the target by type (a Normal move into a Ghost) | -10 |
| | | Stockpile count is 0 | -10 |
| | | Swallow only: then the Recover check above | -8 at full HP |
| `Basic_CheckCanRefreshStatus`, 923 to 926 | 243 (Refresh) | Attacker is not burned, poisoned or paralysed | -10 |
| `Basic_CheckAttackerAsleep`, 660 to 663 | 189 (Snore), 191 (Sleep Talk) | Attacker is not asleep | -8 |
| `Basic_CheckDreamEater`, 329 to 333 | 136 (Dream Eater) | Target is not asleep | -8 |
| | | The move cannot affect the target by type | -10 |

"At exactly 100%" means a Pokemon at 99.6% (which rounds down to 99) is not penalised. Swallow is checked against the target's type although it heals the user, so it is never used against a Ghost (the comment at line 843 says so).

### Moves that faint the user or hand over to the party

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckCannotExplode`, 297 to 319 | 135 (Selfdestruct, Explosion; Oxide's Misty Explosion) | The move cannot affect the target by type | -10 |
| | | Attacker lacks Mold Breaker and target has Damp (guess rule) | -10 |
| | | Attacker has no Pokemon left and the target has some | -10 |
| | | Both sides have no Pokemon left | -1 |
| `Basic_CheckBatonPass`, 780 to 784 | 208 (Baton Pass) | Attacker has no Pokemon left | -10 |
| `Basic_CheckHealingWish`, 1036 to 1051 | 257 (Healing Wish) | Always | -20, and carry on |
| | | Attacker has no Pokemon left | a further -10 (total -30) |
| | | No benched Pokemon has a status and none is below full HP | a further -10 (total -30) |
| `Basic_CheckLunarDance`, 1549 to 1565 | 285 (Lunar Dance) | Always | -20, and carry on |
| | | Attacker has no Pokemon left | a further -10 (total -30) |
| | | No benched Pokemon is below full HP, has a status, or has used any PP | a further -10 (total -30) |

So Healing Wish and Lunar Dance leave Basic at 80 at best, and are chosen only if every other move scores lower. The "below full HP" test counts fainted and on-field party members (bug B7).

### Forcing a switch and taking items

| Handler, lines | Reached from | Check | Change |
|---|---|---|---|
| `Basic_CheckCanForceSwitch`, 499 to 509 | 153 (Roar, Whirlwind) | Target has no Pokemon left | -10 |
| | | Attacker lacks Mold Breaker and target has Suction Cups (guess rule) | -10 |
| `Basic_CheckCanRemoveItem`, 898 to 904 | 235 (Trick, Switcheroo), 240 (Knock Off) | Target has Sticky Hold (guess rule) | -10 |
| | | Target holds no item (its real item, whether or not the AI has seen it) | -10 |
| `Basic_CheckCanRecycle`, 911 to 915 | 238 (Recycle) | Attacker has no item to recycle | -10 |
| `Basic_CheckNaturalGift`, 1053 to 1059 | 258 (Natural Gift) | Attacker's item is not one of the 64 berries listed at lines 1061 to 1126 | -10 |
| | | The move, at the berry's type, cannot affect the target | -10 |

The item-removal check reads the target's real held item (`LoadHeldItem`, line 1891), while the Metal Burst and Fling checks below read only what the AI has seen. Roar does not check Ingrain, which also blocks it.

### Fling

`Basic_CheckFling`, lines 1199 to 1300, reached from 263.

| Lines | Check | Change |
|---|---|---|
| 1201 | The move cannot affect the target by type | -10 |
| 1204, 1205 | Fling power under 10 (no item, or an item that cannot be thrown) | -10 |
| 1208, 1209 | Attacker has Multitype | -10 |
| 1212 to 1216 | Branch on the attacker's held item: Toxic Orb or Poison Barb, Flame Orb, or Light Ball. Any other item | no change |
| 1218 to 1233 | Poison item: target can be poisoned (no Safeguard, no status, not Poison or Steel, no Immunity, Poison Heal or Magic Guard by guess rule) and the attacker lacks Poison Heal | no change |
| 1235 to 1251 | Otherwise: the attacker would not be hurt by keeping the item (Safeguard, already statused, Poison or Steel type, or has Klutz, Immunity, Poison Heal, Magic Guard or Guts) | -5 |
| 1250 | Otherwise: throwing the item gets rid of it | +3 |
| 1253 to 1278 | Flame Orb: the same pattern with burn (Fire type, Magic Guard, Water Veil, Klutz, Guts) | -5 or +3 |
| 1280 to 1286 | Light Ball: target has Safeguard, a status, or Limber (guess rule) | -5 |

The +3 is the only score Basic ever adds for its own sake, so Basic cannot push a score over 103 and cannot reach the overflow the README describes.

### Moves with odd damage

`Basic_CheckNonStandardDamageOrChargeTurn`, lines 572 to 585, covers the moves whose damage is fixed, variable or delayed: Bide (152), Razor Wind (158), Super Fang (159), Dragon Rage (160), Hyper Beam and the other recharge moves (182), Seismic Toss and Night Shade (185), Psywave (186), Counter (187), Flail and Reversal (192), Return (203), Present (204), Frustration (205), SonicBoom (209), Hidden Power (213), Mirror Coat (218), Skull Bash (219), Focus Punch (233), Superpower (237), Endeavor (241), Low Kick and Grass Knot (244), Gyro Ball (256), Trump Card (265), Wring Out and Crush Grip (267), and Punishment (274).

| Lines | Check | Change |
|---|---|---|
| 575 | The move cannot affect the target by the real type chart | -10 |
| 576 to 582 | Target has Wonder Guard (guess rule), attacker lacks Mold Breaker, and the move is not in the 2x or 4x bucket | -10 |

This is where the moves that skipped the entry checks get their immunity test back. Note the Wonder Guard penalty here is -10, where the entry check gives -12, so a move that goes through both (Hidden Power, Return and the other alternative-power moves) can get either, depending on which coin flip says Wonder Guard first.

`Basic_CheckMagnitude`, lines 566 to 570, reached from 207 (the effect pret calls `PSYWAVE`, which is Magnitude's). It is meant to give -10 when the target has Levitate and the attacker lacks Mold Breaker, then falls into the handler above. It reads the wrong battler (bug B5).

`Basic_CheckOHKOWouldFail`, lines 554 to 564, reached from 157 (Guillotine, Horn Drill, Fissure, Sheer Cold): -10 if the move cannot affect the target by type, if the attacker lacks Mold Breaker and the target has Sturdy (guess rule), or if the attacker's level is below the target's.

`Basic_CheckMetalBurst`, lines 1160 to 1182, reached from 261 (Metal Burst; Oxide's Comeuppance): -10 if the move cannot affect the target by type, or if the target has Stall (guess rule) or is known to hold a Shiny Stone. Then, unless the attacker itself has Stall or holds a Shiny Stone, -10 if the attacker would move first. Shiny Stone is a mistake for Lagging Tail (bug B9).

### The score labels

Lines 1567 to 1621 are the shared exits `ScoreMinus1`, `ScoreMinus2`, `ScoreMinus3`, `ScoreMinus5`, `ScoreMinus6`, `ScoreMinus8`, `ScoreMinus10`, `ScoreMinus12`, `ScoreMinus30`, `ScorePlus1`, `ScorePlus2`, `ScorePlus3`, `ScorePlus5` and `ScorePlus10`, each adding the value in its name and ending the move. Basic uses -1, -5, -8, -10 and -12; the rest serve the other flags. `ScoreMinus6` (line 1583) is used by nothing in the whole script.

## Apparent bugs

Fixed on 2026-09-22: B11 (Oxide, the ability byte), B6 (vanilla fix, approved by Ian), and B1 and B2 (battle_edits, vanilla fixes approved by Ian on 2026-09-15). The rest stand as vanilla has them.

Every script bug below is present in vanilla Platinum, at the same line on `main`, because `script.s` is unchanged. Two of them come from C code, and one of those (B11) is introduced by Oxide. None has been fixed.

| # | Lines | Origin | What goes wrong |
|---|---|---|---|
| B1 | 78 | Vanilla, `main` line 78 | Dry Skin is never checked. |
| B2 | 811 to 815 | Vanilla, `main` lines 811 to 815 | Sunny Day checks the target's Hydration. |
| B3 | 176, 177 | Vanilla, `main` lines 176, 177 | The two harsh accuracy and evasion drops are sent to each other's handler. |
| B4 | 858 to 869 | Vanilla, `main` lines 858 to 869 | Ice Body on the AI's side cancels a penalty and never adds a bonus. |
| B5 | 568 | Vanilla, `main` line 568 | Magnitude's Mold Breaker test reads the target's guessed ability. |
| B6 | 62, 63 with `trainer_ai.c` line 31 | Vanilla, `main` `trainer_ai.c` line 31 | Some moves skip every immunity check. |
| B7 | 1047, 1559 with `trainer_ai.c` line 1968 | Vanilla, `main` `trainer_ai.c` line 1968 | Healing Wish and Lunar Dance count fainted and on-field Pokemon as wounded. |
| B8 | 428 to 473, 612 to 619 | Vanilla, `main` same lines | Mold Breaker is ignored for most ability checks. |
| B9 | 1169, 1176 | Vanilla, `main` lines 1169, 1176 | Metal Burst tests Shiny Stone instead of Lagging Tail. |
| B10 | 1487 to 1496 | Vanilla, `main` same lines | Defog treats clearing the foe's hazards as useful. |
| B11 | `ai_context.h` line 28 | Introduced by Oxide | Revealed abilities above 255 are remembered as a different ability. |
| B12 | `trainer_ai.c` lines 1311 to 1344 | Vanilla, `main` `trainer_ai.c` lines 1311 to 1344 | Expert Belt, Filter and Adaptability break the 2x bucket used by the Wonder Guard checks. |
| B13 | 121 to 131 | Vanilla, `main` same lines | Hyper Voice is missing from the Soundproof list. |

**B1, Dry Skin.** Line 77 already branches when the ability is Levitate, so line 78, which tests Levitate again, is unreachable, and its target `Basic_CheckWaterAbsorption2` (lines 106 to 109) is dead. The target code is a copy of the Water Absorb check, and the pret comment says the line should test Dry Skin. As it stands, a Water move into a Dry Skin target that the AI knows or guesses gets no penalty, and the engine heals the target by a quarter (`BattleSystem_TriggerImmunityAbility`, `battle_lib.c` line 3560). This is the battle_edits "Water Immunity vs Dry Skin" item below.

**B2, Sunny Day and Hydration.** Hydration works in rain. The block at lines 811 to 815 is a copy of Rain Dance's (lines 792 to 795) with the ability left unchanged and the penalty raised from -8 to -10, and pret's own comment at line 812 calls it a bug. Its effect: a Sunny Day against a statused Hydration target (guess rule) scores -10 for no reason. This is the battle_edits "Sunny Day check" item below.

**B3, the swapped harsh drops.** Line 176 sends `EVA_DOWN_2` to the Accuracy handler and line 177 sends `ACC_DOWN_2` to the Evasion handler; every other pair in the list goes to its own stat. No move in vanilla or in Oxide uses either effect today, so nothing is affected yet. It becomes live the moment a move is given one of these effects.

**B4, Hail and Ice Body.** When the target has Ice Body the move takes -8 and carries on (line 861); if the attacker also has Ice Body it gets +8 back (line 869). The net is 0, so an Ice Body attacker never gets an incentive to set Hail, only the removal of a disincentive, which pret's comment at lines 863 to 866 also points out. Separately, the -8 for the target's Ice Body applies even when the AI's side would gain more from Hail. This is a structure that does not match its evident purpose; whether to change it is a behaviour decision, not a plain fix.

**B5, Magnitude and Mold Breaker.** Line 568 compares the loaded value with Mold Breaker, but nothing in the handler loads the attacker's ability first. Magnitude has power 1, so it reaches the dispatch through the Soundproof check, whose last load (line 117) was the target's guessed ability. So the test asks whether the target has Mold Breaker. The effect: a Mold Breaker attacker's Magnitude still takes -10 when a (second) guess says the target has Levitate, although Mold Breaker would let it hit; and a target that has Mold Breaker skips the Levitate test, which cannot matter since it then has no Levitate. The fix would be a `LoadBattlerAbility AI_BATTLER_ATTACKER` before line 568.

**B6, moves that skip every immunity check.** The entry immunity checks (lines 65 to 109) run only when the damage comparison is made. Moves on the "no damage calculation" list skip them, and Basic relies on their own handlers to check again. Five of those effects have no handler in the dispatch: Sky Attack, Solar Beam, Eruption and Water Spout, Sucker Punch, and Head Smash. For these, Basic applies no type check and no ability check at all. In vanilla the type part never matters (none of those five types has an immunity against it), but the ability part does: Water Spout into Water Absorb or Dry Skin, Eruption into Flash Fire, and Solar Beam or Water Spout into Shedinja all keep a full 100. Oxide makes this worse (see below).

**B7, Healing Wish and Lunar Dance.** `AICmd_IfAnyPartyMemberIsWounded` (line 1968) counts every party slot except the attacker's own whose HP is not at maximum. A fainted Pokemon has 0 HP, so it counts as wounded, although Healing Wish cannot revive it; the command also skips no egg and, in doubles, does not skip the partner who is on the field. So once any party member has fainted, Healing Wish and Lunar Dance always pass the "is it useful" test and score -20 instead of -30. The status test next to it (`IfPartyMemberStatus`) does skip fainted Pokemon, eggs and the partner, which shows what was intended. `IfAnyPartyMemberUsedPP` (line 1987), used only by Lunar Dance, has the same gap.

**B8, Mold Breaker ignored.** Mold Breaker bypasses Clear Body, White Smoke, Hyper Cutter, Keen Eye, Limber, Insomnia, Vital Spirit, Immunity, Water Veil, Own Tempo and Oblivious in the engine. Basic checks for Mold Breaker before the immunity abilities, Soundproof, Damp, Sturdy, Suction Cups, Tickle, Captivate and Memento, but not in the single-stat drop handlers (428 to 473), not in the sleep, poison, burn, confusion and attraction handlers, and only after Limber in the paralysis handler (line 619 comes after line 616). So a Mold Breaker Pokemon is still told its Growl, Thunder Wave or Hypnosis will fail against those abilities. The inconsistency, next to the handlers that do check, suggests an oversight; changing it is a small, predictable fix, since each affected check would simply stop firing when the attacker has Mold Breaker.

**B9, Shiny Stone.** Lines 1169 and 1176 test for the item Shiny Stone where the logic (a slow holder makes Metal Burst work) wants Lagging Tail. pret's comments at lines 1165 and 1172 say so. The effect: a target known to hold Lagging Tail is not penalised, and an attacker holding Lagging Tail is still told it moves first.

**B10, Defog.** In Generation 4 Defog clears hazards on the target's side, which helps the foe. Yet lines 1493 to 1496 penalise Defog only when the target's side has no hazards, and line 1488 penalises it when the target has no Pokemon left to be hurt by them. That is the reasoning for setting a hazard, copied onto a move that removes them, so when the target's evasion is already at -6, the AI regards "clearing the player's Spikes" as a good reason to Defog. Low impact in practice: the check is reached only at -6 evasion.

**B11, remembered abilities above 255.** In Oxide, abilities are u16 and `BattleAI_SetAbility` (`battle_script.c` line 12176) takes a u16, but the store it writes to is still `u8 battlerAbilities[MAX_BATTLERS]` (`include/battle/ai_context.h` line 28, unchanged from vanilla). A revealed ability with id 256 or more is therefore remembered as id minus 256, and every later `LoadBattlerAbility` on that target returns the wrong ability. Vanilla cannot hit this because no ability passed 255. The collisions that Basic can act on today, for species that carry these abilities now:

| Revealed ability (id) | Remembered as | Species now | What Basic then does |
|---|---|---|---|
| Hospitality (299) | Soundproof | Sinistcha | -10 on Growl, Roar, Sing and the other listed sound moves |
| Pastel Veil (257) | Stench | Galarian Rapidash | -10 on Gastro Acid |
| Neutralizing Gas (256) | nothing (0) | Galarian Weezing | treated as unrevealed, so guessed again |
| Seed Sower (269) | Cloud Nine | Arboliva | nothing in Basic |
| Purifying Salt (272) | Color Change | Nacli line | nothing in Basic |
| Toxic Debris (295) | Inner Focus | Glimmet, Glimmora | nothing in Basic |
| Sharpness (292) | Trace | Kleavor | nothing in Basic |

Worse collisions are waiting in the id table for species that do not carry them yet: Protosynthesis (281) becomes Wonder Guard, Quark Drive (282) Levitate, As One (266, 267) Volt Absorb and Water Absorb, Wind Rider (274) Flash Fire, Sword of Ruin (285) Clear Body, Earth Eater (297) Water Veil, Transistor (262) Damp, Curious Medicine (261) Sturdy, Quick Draw (259) Speed Boost. A Protosynthesis target, once revealed, would draw -12 on every attack that is not super effective. The fix is to widen `battlerAbilities` to u16, which moves every later field of `AIContext`; that struct lives in the battle context, not the save, so the cost is a rebuild, but it wants the same care as the element 4 widening.

**B12, the 2x bucket.** `AICmd_IfMoveEffectivenessEquals` (`trainer_ai.c` line 1311, the same on `main`) buckets the result of `BattleSystem_ApplyTypeChart`, which also applies Adaptability, Filter, Solid Rock and Expert Belt to its number. A super effective move from an Expert Belt holder comes out at 96 or 144, which matches neither 2x (80, or 120 with STAB) nor 4x, so the Wonder Guard checks at lines 97, 98, 580 and 581 treat it as not super effective: -12 at the entry, -10 in the odd-damage handler. With Adaptability a neutral STAB move comes out at 80 and counts as 2x, and a 4x STAB move comes out at 320 and counts as neither. Only the Wonder Guard checks use these buckets in Basic, so the effect is limited to Wonder Guard targets, but the same command serves the other flags.

**B13, Hyper Voice.** The engine's sound list (`sSoundMoves`, `battle_lib.c` line 3495, vanilla line 3473) has twelve moves; Basic's list at lines 121 to 131 has eleven and leaves out Hyper Voice. So Hyper Voice into a Soundproof target keeps its score.

Three further behaviours look questionable without being plainly wrong, so they are recorded here and not as bugs. Acupressure (lines 1139 to 1158) takes -10 if any one stat is maxed, although the move only fails when all seven are. Embargo (lines 1188 to 1194) is penalised only when the target has a recyclable item and the battle is in the Frontier, and the intent of that pairing cannot be read from the code. Knock Off is penalised -10 against a target with no item although it still does damage, which mattered little at 20 power and matters more in Oxide (below).

## The battle_edits fixes

Two of the eleven fall in this section. I could not read the ds-pokemon-hacking guide itself (fetching it was outside this task's permission), so each is explained from the code, and the lead should confirm the guide's wording before applying either.

**Water Immunity vs Dry Skin** is bug B1. The fix changes line 78 from `ABILITY_LEVITATE` to `ABILITY_DRY_SKIN`, which makes lines 106 to 109 reachable. Score change after the fix: a damaging Water move into a target the AI believes has Dry Skin goes from no penalty to -12. In Oxide's species data that is certain for Croagunk, Toxicroak, Parasect, Shellos and Gastrodon (Dry Skin in both slots, the last two from the base ROM) and a coin flip for an unrevealed Paras (Effect Spore or Dry Skin). Dry Skin's other effect (Fire does more) is not a Basic matter. The fix does not help the Water moves in bug B6, which never reach line 78.

**Sunny Day check** is bug B2. The code gives -10 when the target has Hydration and a status; since sun does nothing for Hydration, the fix removes a penalty that should not be there. What the check should test instead is the part to confirm against the guide. The Rain Dance block it was copied from punishes weather that helps the target, and the sun equivalents in Generation 4 are a target with Leaf Guard (sun blocks new status), Chlorophyll, Solar Power or Flower Gift. If the fix is to replace Hydration with Leaf Guard and keep the "target has a status" test, it will almost never fire, because Leaf Guard does not cure an existing status; the natural reading is "target has Leaf Guard and has no status". Either way, after the fix a Sunny Day against a statused Hydration target stops losing 10 points, and the new condition's penalty is whatever the guide sets (-10 as written now).

**Fire Fang vs Wonder Guard** is an engine fix in `battle_lib.c`, outside this section, but it moves two Basic scores. The fix in pret's `docs/bugs_and_glitches.md` replaces `BATTLE_EFFECT_FLINCH_BURN_HIT` with `BATTLE_EFFECT_SHADOW_FORCE` in `MoveIsOnDamagingTurn` (line 7671 here, 7600 on `main`). Fire Fang is super effective on Shedinja, so both changes only matter against another Wonder Guard holder (one that gained it by Skill Swap or Role Play). Against such a target, Fire Fang now passes line 68 and takes -12 at line 99 if the AI knows the ability; after the fix line 68 sees the immunity and it takes -10. Shadow Force moves the other way: today line 68 gives it -10 against a Wonder Guard target it does not hit super effectively, and after the fix line 68 no longer sees it, so it takes -12 if the AI knows the ability and 0 if it does not.

**Rage Glitch** is in `battle_controller_player.c` and does not touch the AI. Basic never checks Rage.

The other seven (Foresight and Odor Sleuth Ghost check, Facade status check, Leaf Guard Sunny Day logic, Water Spout and Eruption HP check, charge-turn scoring, Thunder scoring, Discharge in doubles) are in the Expert and Tag Strategy flags and are not in this section. The Foresight one sits next to Basic's own Foresight handler (lines 715 to 718), which only checks "already identified" and is not the check the edit is about.

## Oxide consequences

Basic recognises moves by battle effect (lines 134 to 285), by move id (the OHKO shortcut at 57 and 58, the sound list at 121 to 131, Thunder Wave at 620), by ability id (throughout), by type (Poison, Steel, Fire, Grass, Ghost, Flying, Electric, Water, Ground), and by item (the berry table, Shiny Stone, three hold effects for Fling). Anything Oxide adds that is not on those lists falls through to the defaults: a damaging move gets only the entry immunity checks, and a status move gets nothing.

**New effects.** None of the new effects 277 to 406 is in the dispatch, so all 136 moves using them take only the entry checks. The 51 status moves among them get no Basic check at all and keep a full 100 from Basic, however useless they are at the moment: Hone Claws, Wide Guard, Guard Split, Power Split, Autotomize, Quiver Dance, Soak, Coil, Simple Beam, Entrainment, After You, Quick Guard, Shell Smash, Heal Pulse, Shift Gear, Quash, Work Up, Cotton Guard, Mat Block, Sticky Web, Trick-or-Treat, Noble Roar, Ion Deluge, Forest's Curse, Parting Shot, Crafty Shield, the four terrains, Venom Drench, Powder, Geomancy, Strength Sap, Toxic Thread, Laser Focus, Aurora Veil, Tearful Look, Stuff Cheeks, Magic Powder, Clangorous Soul, Decorate, Life Dew, Coaching, Victory Dance, Take Heart, Spicy Extract, Fillet Away, Shed Tail, Tidy Up and Snowscape. So the AI will Quiver Dance at +6, lay a second Sticky Web, and Shell Smash when it has no Pokemon to benefit, as far as Basic is concerned. Teaching Basic these is the "teach it the new moves" item of element 6, and the handlers above are the templates (the stat-raise handlers for the dances, `Basic_CheckSpikes` for Sticky Web, the screen handlers for Aurora Veil).

**New moves on old effects.** Sixteen new moves reuse an effect Basic handles, and inherit its check whether or not it fits: Play Nice and Baby-Doll Eyes (Attack drop), Confide (Sp. Atk drop), Eerie Impulse (harsh Sp. Atk drop), Shore Up (heal), Prismatic Laser, Meteor Assault and Eternabeam (recharge), Nature's Madness and Ruination (halve HP), Pika Papow and Veevee Volley (Return's effect), Misty Explosion (Explosion), Power Shift (Power Trick's flag, so the AI thinks Power Shift and Power Trick exclude each other), Shelter (Defense +2), and Comeuppance (Metal Burst, which fits). Confide is a sound move but is on neither sound list, engine or AI, so the two agree for now.

**Oxide moves that hit bug B6.** Oxide put three new moves on effects that skip every immunity check: Dragon Energy (Eruption's effect, Dragon type), Thunderclap (Sucker Punch's, Electric) and Light of Ruin (Head Smash's, Fairy), plus Solar Blade on Solar Beam's. Two of these now have a type immunity Basic cannot see: Dragon Energy into a Fairy type and Thunderclap into a Ground type both keep a full 100, and Thunderclap into Volt Absorb or Motor Drive gets no penalty either. Heavy Slam, Heat Crash and Final Gambit have power 1 and new effects, so they also skip the entry checks and have no handler: Final Gambit into a Ghost and Heat Crash into Flash Fire go unpenalised.

**Changed moves.** Knock Off is 70 power in Oxide (20 in vanilla) but still takes -10 whenever the target holds nothing, which now throws away a strong attack. Snore is 80 power and still takes -8 unless the user is asleep, which is correct since it fails otherwise. Sweet Kiss, Charm and Moonlight became Fairy; none of their handlers looks at the move's type, so nothing changes.

**Fairy, type 18.** Types are compared as whole numbers and 18 fits, so nothing breaks. Fairy's one immunity (to Dragon) is seen by the real type chart at lines 68, 575 and the other effectiveness checks, because Oxide added it to the chart before the Foresight marker. Nothing in Basic checks for Fairy by name, and nothing needs to yet. Two gaps sit next to this: `TrainerAI_MoveType` (`trainer_ai.c` line 3127) has no Fairy case for Judgment, so a future Pixie Plate would read as Normal, and new type-changing moves (Multi-Attack, Techno Blast, Revelation Dance, Terrain Pulse, Weather Ball's newer relatives) are judged by their listed type everywhere.

**Abilities above 255.** Every comparison in the script is a 32-bit word against the 32-bit `calcTemp`, and `LoadBattlerAbility` reads the u16 species and battle fields in full, so a guessed or real ability above 255 compares correctly. The one failure is the remembered-ability store, bug B11. Separately, the new abilities that grant an immunity or block a move (Sap Sipper, Storm Drain and Lightning Rod in their later form, Earth Eater, Well-Baked Body, Bulletproof, Overcoat against powders, Wind Rider, Good as Gold, Purifying Salt, the Veil abilities, Dazzling, Queenly Majesty, Armor Tail) are unknown to Basic; until element 5 gives them effects the engine does not honour them either, so the AI and the engine agree for now, and they will disagree as soon as element 5 lands.

**The ability guess.** The guess reads only the first two ability slots (`SPECIES_DATA_ABILITY_1` and `_2`). Element 8's hidden abilities go in a third slot, so an unrevealed hidden ability will never be guessed; a trainer's Pokemon with a hidden ability will be judged as if it had one of its normal two. Oxide also has 234 species whose second slot repeats the first; `LoadBattlerAbility` handles that correctly (both flips give the same answer), but `CheckBattlerAbility` (line 441, Speed Boost) would answer "unknown" for such a species, which would switch the check off. No Speed Boost species has a duplicated slot today (Ninjask's second slot is empty; Yanma and Yanmega have two different abilities). Whether regional forms are guessed from their own abilities or the base form's depends on how `SpeciesData_GetSpeciesValue` is called with the battle species, which I did not trace.

**New berries and items.** The Natural Gift table at lines 1061 to 1126 is a fixed list of 64 berries; any berry added in element 7 (Roseli, Kee, Maranga) is refused with -10 until it is added. The Fling tables use hold effects, so a new item with an old hold effect is covered automatically.

## Where the references disagree with the code

lhearachel's gist gives -10 for every immunity found by ability. The code gives -12 for Volt Absorb, Motor Drive, Water Absorb, Flash Fire, Wonder Guard and Levitate at the entry (lines 83 to 108) and -10 only for the true type chart, Soundproof and the handlers. The gist leaves out the -8 for a Substitute that is already up and the -8 (not -10) for a second screen, Mist or Safeguard; its -5 for an already confused target matches, and it describes the Sunny Day and Dry Skin bugs as the code shows them. The pokemow page describes Basic only in general terms, so there is nothing in it to contradict.
