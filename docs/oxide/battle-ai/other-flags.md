# The other flags, and double battles

This part covers every AI flag except Basic and Expert: the flag table at the top of `src/battle/trainer_ai/script.s` (lines 1 to 51), the eleven routines from `EvalAttack_Main` to `CatchTutorial_Main` (lines 6353 to 8108), and the double-battle driver `TrainerAI_MainDoubles` in `src/battle/trainer_ai/trainer_ai.c` (lines 352 to 472), without which Tag Strategy cannot be understood.

Everything is read from the code in this tree. `script.s` is byte for byte the same as vanilla on `main`, and `trainer_ai.c` differs from `main` only in two type declarations at lines 3645 and 3646 (which do not move any line), so every line number here is also the vanilla line number.

## How to read the chances and the commands

`IfRandomLessThan N, label` draws a number from 0 to 255 and jumps to `label` when it is below N (`AICmd_IfRandomLessThan`, `trainer_ai.c` line 535). The jump almost always skips the score change, so the change happens with chance (256 - N) / 256. Where the jump goes to the score change instead, the section says so. The values used in this part:

| N | Jump taken | Jump not taken |
|---|---|---|
| 20 | 7.8% | 92.2% |
| 50 | 19.5% | 80.5% |
| 51 | 19.9% | 80.1% |
| 64 | 25% | 75% |
| 80 | 31.25% | 68.75% |
| 100 | 39.1% | 60.9% |
| 128 | 50% | 50% |
| 160 | 62.5% | 37.5% |
| 170 | 66.4% | 33.6% |
| 192 | 75% | 25% |

The shared labels `ScoreMinus1` to `ScorePlus10` (lines 1567 to 1621) add their value and run `PopOrEnd`, which ends this flag's work on this move. None of the routines in this part pushes onto the script stack, so an inline `AddToMoveScore` carries on to the next line and a jump to a `ScoreX` label is the last thing that happens.

These commands decide most of the results below. Each was read in `trainer_ai.c`.

| Command | What it really does | Lines |
|---|---|---|
| `IfTargetIsPartner` | Jumps when attacker and target are on the same side (same low bit of the battler id). Never true in a single battle. | 2630 to 2639 |
| `FlagMoveDamageScore USE_MAX_DAMAGE` | Loads one of three answers for the current move against the current target, at the top damage roll. "No comparison made" if the move's effect is not in `sAltPowerMoveEffects` and either its power is 0 or 1 or its effect is in `sNoDamageCalcMoveEffects`. Otherwise "highest damage" if no move in the attacker's four slots does strictly more damage (a tie counts as highest), else "not highest". The four slots include moves with no PP, disabled moves and a Choice-locked set. | 1012 to 1066, tables 31 to 61 |
| `IfCurrentMoveKills USE_MAX_DAMAGE` | True when the current move's damage at the top roll is at least the target's current HP. Moves that get "no comparison made" above never count as killing. | 1525 to 1574 |
| `CheckIfHighestDamageWithPartner` | As `FlagMoveDamageScore`, but the move must also match or beat every move of the attacker's partner against the same target. The partner's moves are counted even if it has fainted. | 2369 to 2436 |
| `IfMoveEffectivenessEquals` | Runs the real type chart from a base of 40 and compares the result with the multiplier constants. It works on status moves too, since the base is fixed at 40. STAB results are mapped back (60 times 2 reads as double), but Adaptability, Filter, Solid Rock and Expert Belt produce numbers that match the wrong constant or none. | 1311 to 1346 |
| `IfHPPercentLessThan` / `GreaterThan` / `EqualTo` | Compare `curHP * 100 / maxHP`, rounded down. "Equal to 0" is used as "absent", and it is also true for a Pokemon on 1 HP whose maximum is above 100. | 588 to 631 |
| `LoadBattlerAbility` | The attacker's own ability exactly. For any other battler (including the attacker's partner when that partner is the target), the remembered ability if one has been revealed, else Shadow Tag, Magnet Pull or Arena Trap if it is one of those, else a coin flip between the species' two ability slots, fresh on every call. | 1170 to 1210 |
| `CheckBattlerAbility` | For the attacker and the attacker's partner, the real ability. For the target and the target's partner, the remembered ability, else the real one if it is a trapping ability, else: one listed ability, that one; two listed abilities, "not have" if neither is the one asked about, and "unknown" (which never matches `AI_HAVE`) if either is. So an unrevealed Lightning Rod on a Pokemon that could also have Rock Head counts as absent. | 1212 to 1266 |
| `LoadAbility` | The real ability of any battler, through `Battler_Ability`. Used only by the roaming routine. | 2654 to 2662 |
| `FlagBattlerIsType` | True if either of the battler's types matches. | 991 to 1004 |
| `LoadTypeFrom LOAD_MOVE_TYPE` | The type in the move data, not the type the move will have in battle, so Hidden Power, Weather Ball, Judgment and Natural Gift read as Normal (or their listed type). | 961 to 963 |
| `IfMoveKnown` | For the attacker, its real moves. For the attacker's partner, its real moves, and false if the partner has 0 HP. For the target, only the moves the AI has seen it use. | 1627 to 1681 |
| `IfMoveEffectKnown` | As above, by battle effect, attacker or target only. | 1739 to 1779 |
| `IfHeldItemEqualTo` | Real item for battlers on the AI's side, remembered item for the other side. | 1915 to 1934 |
| `LoadBattlerSpeedRank` | Sorts all battlers on the field by `BattleSystem_CompareBattlerSpeed` and returns the battler's place, 0 for fastest. The comparison includes Trick Room, Tailwind, Stall, Lagging Tail and this turn's Quick Claw roll, ignores move priority, and breaks exact ties at random. Two battlers never share a rank. | 2056 to 2094 |
| `IfBattlerFainted` | Despite the name, true only if the slot is permanently empty (`battlersSwitchingMask`, set when a battler faints with nothing left to send in, and for the unused slots of a single battle). | 2438 to 2452 |
| `LoadTurnCount` | The battle's turn counter, 0 on the first turn. | 931 to 935 |
| `LoadIsFirstTurnInBattle` | True on the first turn after the battler came in. | 2480 to 2492 |
| `IfStatStage...` | Stat stages run 0 to 12 with 6 as neutral, so "greater than 8" means +3 or more and "equal to 12" means +6. | 1465 to 1523 |
| `CountAlivePartyBattlers` | Party members with HP, not counting the battler on the field (and in a double battle, not its partner either). | 1126 to 1156 |
| `Escape` | Sets the escape, done and break flags; the AI flees instead of choosing a move. | 1875 to 1879 |
| `Dummy3E`, `Dummy3F` | Do nothing at all, not even advance the script cursor. | 1881 to 1889 |

"No comparison made" matters in half the routines here, so it is worth being exact about what it covers. It is every status move, every move with power 1 whose effect is not in the alternative-power table (Flail, Reversal, Magnitude, Present, Super Fang, Endeavor, Counter, Mirror Coat, Metal Burst, Bide, Fling, Trump Card, Punishment, Wring Out, Crush Grip and the OHKO moves), and every move whose effect is in `sNoDamageCalcMoveEffects`: Explosion and Self-Destruct, Dream Eater, Razor Wind and Sky Attack, Hyper Beam and its kin, Skull Bash, Solar Beam, Spit Up, Focus Punch, Superpower, Eruption and Water Spout, Sucker Punch and Head Smash. The alternative-power moves that do get a comparison are Hidden Power, Gyro Ball, Natural Gift, Judgment, Dragon Rage, Seismic Toss and Night Shade, Psywave, Return, Frustration, Sonic Boom, Low Kick and Grass Knot.

## The flag table (lines 1 to 51)

`gTrainerAITable` is 32 entries, one per bit of the trainer's `ai_flags` mask, each the distance from the table to that flag's routine. `TrainerAI_EvalMoves` starts each flag's run at `aiScriptTemp[thinkingBitShift]` (`trainer_ai.c` line 488), so the table order is the bit order and the run order. Bits 11 to 28 point at `Terminate` (line 8105), which ends at once. The README has the full table. Two things in it are easy to miss: Risky is bit 4 and Prioritize Extremes bit 5, so Risky runs first although it comes second in the file, and Tag Strategy, bit 7, runs before Check HP, Weather and Harassment.

Bits 29 to 31 are never set by a trainer file in this tree. The roaming bit is set by `TrainerAI_Init` alone, which replaces the whole mask with it in a roamer battle (`trainer_ai.c` lines 246 to 250). Nothing in the source or the trainer data sets the Safari or Catch Tutorial bits, so those two routines are unreachable (see their sections).

## When the AI runs at all, and the double-battle driver

The AI is asked for a move only in `Task_TrainerShowMoveSelectMenu` (`src/battle/battle_display.c` lines 3586 to 3590): in a trainer battle, in a roamer battle, in the first battle of the game, or for a battler on the player's side that the player does not control (the partners Cheryl, Mira, Riley, Buck and Marley). A wild Pokemon in any other battle picks a random usable move (lines 3600 to 3613) and never sees the script. So in vanilla, Tag Strategy already runs in the wild double battles fought alongside a partner, but only for the partner. A wild double battle added by Oxide will run Tag Strategy for the wild side only if its implementation routes the wild Pokemon through `TrainerAI_Main`; as the code stands it would not, and a wild Pokemon there would presumably have a mask of 0 (its trainer slot is empty; I did not trace how it is filled), so Tag Strategy, forced on by line 254, would be its only flag.

`TrainerAI_MainDoubles` runs the whole flag pass once for each other battler on the field, the partner included, with that battler as the target.

1. Skip the attacker's own slot and any battler with 0 HP (lines 362 to 367).
2. Call `TrainerAI_Init` again (line 369), which resets every score to 100 or 0, draws fresh damage rolls, and reloads the flag mask with Tag Strategy added. If the target is on the other side, record its last move into the AI's knowledge (lines 372 to 375).
3. Run every set flag over every move slot (lines 377 to 394), exactly as in a single battle.
4. Keep the best-scoring move for this target, ties broken at random (lines 401 to 429).
5. If this target is the partner and that best score is below 100, discard the target by setting its score to -1 (lines 431 to 436).
6. Choose the target whose best score is highest, ties at random (lines 440 to 457), and use its best move.
7. Two overrides (lines 461 to 469): a move with range "user or ally" (only Acupressure) is aimed at the user when the chosen target is on side 0; a Curse from a non-Ghost is aimed at the user.

Every routine except Tag Strategy and Check HP ends at once when the target is the partner (their first lines, 54, 1625, 6355, 6418, 6501, 6523, 6565, 7980 and 8022). So on the partner pass each move starts at 100 and only `TagStrategy_Partner` moves it, and the rule in step 5 turns that routine's result into a yes or no: any move it leaves at 100 or raises is allowed on the partner, and any penalty at all forbids it. "No score change" in the partner routine therefore means "allowed", which is behind two of the bugs below. Check HP also jumps to `TagStrategy_Partner` for the partner (line 7697), so a trainer with both flags runs the partner routine twice and every partner change is applied twice with independent rolls. No trainer in the current data has Check HP in a double battle.

A spread move such as Earthquake is scored separately against each opponent, and Tag Strategy's penalty for hitting the partner is applied in each of those passes. On the partner pass the same move is usually forbidden, which does not matter, since a spread move is not aimed at the partner.

## Evaluate Attack (bit 1), lines 6353 to 6415

Evaluate Attack makes the AI prefer the strongest move and a move that knocks the target out. It is pokemow's "Strong AI". It never scores moves against the partner (line 6355).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Kills at the top roll, effect is +1 priority (`BATTLE_EFFECT_PRIORITY_1`) | +6 | certain | 6358, 6400, 6408 to 6412 |
| Kills, effect is Future Sight or Doom Desire | +4 | 33.6% | 6358, 6396, 6403 to 6406 |
| Kills, any other effect | +4 | certain | 6358, 6401, 6411, 6412 |
| Does not kill, is not the strongest move | -1, then stop | certain | 6361, 6362 |
| Does not kill, effect is Explosion, Focus Punch or Sucker Punch | -2 | 80.1% | 6365 to 6367, 6372 to 6375 |
| Does not kill, the move is four times effective (then the routine ends) | +2 | 68.75% | 6379, 6382 to 6384 |

The kill check comes first, so a killing move skips the -1 and the effectiveness bonus. Explosion, Focus Punch and Sucker Punch are all in the no-damage-calc table, so they never "kill" and never get the -1: they get the 80.1% -2 instead, and then the four-times check. The kill-branch tests for them at lines 6389, 6394 and 6395 can never be reached, which the code's own comment at 6392 says for two of the three. The priority check reads the move's effect, not its priority, so Fake Out, Feint, Sucker Punch and Oxide's Thunderclap are not "+1 priority" here while Accelerock and Jet Punch are. A status move gets "no comparison made", skips the -1 and falls through to the four-times check; see bug O12.

## Setup First Turn (bit 3), lines 6417 to 6497

Setup First Turn makes the AI open the battle with a stat change, screen or status move. It never scores against the partner (line 6418).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Battle turn 0 and the move's effect is in `SetupFirstTurn_SetupEffects` | +2 | 68.75% | 6421, 6422, 6425 to 6430 |

The turn is the battle's, not the Pokemon's, so a Pokemon sent in later never gets the bonus. The table (lines 6435 to 6497) holds: every one-stage and two-stage raise and drop of Attack, Defense, Speed, Sp. Atk, Sp. Def, accuracy and evasion; Conversion; Light Screen and Reflect; Focus Energy; confusion, poison, paralysis and burn infliction; Substitute; Leech Seed; Minimize; Curse; Swagger; Flatter; Camouflage; Yawn; Defense Curl; Torment; Ingrain; Imprison; Teeter Dance; Tickle; Cosmic Power and Defend Order; Bulk Up; Calm Mind; Tailwind; Acupressure; Lucky Chant; Magnet Rise; Defog; and Whirlpool. Amnesia's effect (line 6452 and 6459) and Camouflage (6477 and 6490) are listed twice, which does no harm. Whirlpool is a damaging trapping move and gets the setup bonus. Dragon Dance, Sleep moves, Toxic, Spikes and Stealth Rock are absent.

## Risky (bit 4), lines 6521 to 6562

Risky makes the AI favour gambles. It never scores against the partner (line 6523).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| The move's effect is in `Risky_RiskyEffects` | +2 | 50% | 6526 to 6531 |

The table (lines 6536 to 6562): sleep, Explosion and Self-Destruct, Mirror Move, the OHKO moves, the high-critical-hit moves, confusion, Metronome, Psywave, Counter, Destiny Bond, Swagger, Attract, Present, Ancient Power and its kin, Belly Drum, Mirror Coat, Focus Punch, Revenge and Avalanche, Teeter Dance, Gyro Ball, Acupressure, Metal Burst, Payback, Me First and Sucker Punch. There is no turn or damage condition.

## Prioritize Extremes (bit 5), lines 6499 to 6519

Prioritize Extremes favours status moves and moves the damage calculator does not handle. It never scores against the partner (line 6501).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| `FlagMoveDamageScore` gives "no comparison made" | +2 | 60.9% | 6511 to 6516 |

The comment at lines 6503 to 6510 says variable-power moves qualify and points to both effect tables. That is half right: the no-damage-calc effects qualify, but the alternative-power table is exactly the list of variable-power moves that do get a comparison, so Hidden Power, Gyro Ball, Return, Low Kick, Seismic Toss and the rest do not qualify. What qualifies is the list under "No comparison made" above: every status move plus Flail, Reversal, the OHKO moves, Explosion, Hyper Beam, Solar Beam, Focus Punch, Eruption, Sucker Punch, Head Smash and so on.

## Baton Pass (bit 6), lines 6564 to 6635

Baton Pass sets up for a Baton Pass chain: boost, protect, then pass. It never scores against the partner (line 6565).

| Step | Condition | Change | Chance | Lines |
|---|---|---|---|---|
| Gate | No other living party member | stop | certain | 6568, 6569 |
| Gate | The move gets a damage comparison | stop | certain | 6572, 6573 |
| Gate | The attacker has no move with Baton Pass's effect | stop | 31.25% | 6576, 6577 |
| Boost | Swords Dance, Dragon Dance, Calm Mind, Nasty Plot on turn 0 | +5 | certain | 6581 to 6584, 6596, 6597 |
| Boost | Same moves, later turn, attacker below 60% HP | -10 | certain | 6600 |
| Boost | Same moves, later turn, 60% HP or more | +1 | certain | 6603 |
| Protect | Protect's effect, attacker's last move was Protect or Detect | -2 | certain | 6586, 6608, 6609 |
| Protect | Protect's effect, otherwise | +2 | certain | 6612 |
| Pass | Baton Pass itself on turn 0 | -2 | certain | 6588, 6622, 6623 |
| Pass | Baton Pass, Attack at +3 or more | +3 | certain | 6626 |
| Pass | Baton Pass, Attack at +2 | +2 | certain | 6627 |
| Pass | Baton Pass, Attack at +1 | +1 | certain | 6628 |
| Pass | Baton Pass, Attack not raised, Sp. Atk at +3, +2 or +1 | +3, +2, +1 | certain | 6629 to 6631 |
| Other | Any other move past the gates | +3, then the Boost rows | 92.2% | 6591 to 6603 |

Two things here are not what the comments say. The third gate lets the routine run 68.75% of the time even when the attacker does not know Baton Pass. And "any other move" does not stop after its +3: it falls through into the Boost handling, so on turn 0 it collects +8 in total, more than the four named boosting moves get, and below 60% HP it nets -7 (bug O2). The 7.8% of the time the +3 roll fails, the move is left alone. The Baton Pass rows stop at the first stage that matches, so Sp. Atk counts only if Attack is not raised, and Speed and the defences are never looked at. The labels `Risky_Terminate` used at 6577 and 6591 belong to Risky, but they only end the move, so this is harmless.

## Tag Strategy (bit 7), lines 6637 to 7694

Tag Strategy is the double-battle routine: it adjusts moves for what they do to the AI's own partner and what the partner can do with them. `TrainerAI_Init` forces it on in every double battle (`trainer_ai.c` lines 253 to 255), and it is the only routine in the file that scores moves aimed at the partner. It has two halves: `TagStrategy_Main` for moves aimed at an opponent, and `TagStrategy_Partner` (line 7339) for moves aimed at the partner. In a single battle, if a trainer carried the flag, "the partner" would be the empty slot opposite, whose leftover data would be read.

### Aimed at an opponent: damage adjustments (lines 6640 to 6730)

Only moves that get a damage comparison take this step; the rest jump straight to the special cases at line 6642.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Resisted (half damage), does not kill, the target's partner is present | -1 | 75% | 6652, 6658 to 6668 |
| Doubly resisted (quarter damage), same conditions | -2 | 75% | 6653, 6670 to 6680 |
| The strongest move of either AI Pokemon against this target, effect +1 priority | +1, and skip the effectiveness bonus | 80.5% | 6684, 6691, 6700 to 6704 |
| The strongest move, any other effect | +1, and skip the effectiveness bonus | 50% | 6684, 6694, 6695 |
| Super effective, not a fixed-damage move, reached because the move was not the strongest or its +1 roll failed | +1 | 60.9% | 6715, 6720 to 6724 |
| Four times effective, same | +1 | 75% | 6716, 6726 to 6730 |

"Present" means the target's partner is not at 0% HP (lines 6663 and 6675); the comments call this "not on their last Pokemon", but it tests the other opponent on the field. The fixed-damage moves (Dragon Rage, Seismic Toss and Night Shade, Psywave, Sonic Boom) skip the resist penalty and the effectiveness bonus but can still get the strongest-move bonus. So this step gives at most +1: a strongest, super-effective, non-priority move gets it with 80.5% (50% plus half of 60.9%). The OHKO tests at 6645 and 6708 and the Explosion test at 6688 cannot be reached, because those moves never get a comparison.

### Aimed at an opponent: special cases (lines 6732 to 7337)

Every move aimed at an opponent, status or not, then goes through this dispatch (lines 6734 to 6752), checked in order: by move id Skill Swap, Earthquake, Magnitude, Future Sight, Doom Desire, Rain Dance, Sunny Day, Hail, Sandstorm, Gravity, Trick Room and Follow Me; then by the move's listed type Electric, Fire and Water; then, if the partner is alive and knows Helping Hand, the Helping Hand bonus. Each branch ends the move, so a move gets only the first that applies. The second `LoadTypeFrom` at 6747 repeats the one at 6735.

In the ability checks below, "attacker" and "partner" mean the AI's two Pokemon, whose abilities are read exactly. Each "and partner" check reads the partner slot without testing that the partner is alive, so a fainted partner's leftover ability and types still count. The code's own comment at 7133 says this for Earthquake.

Weather and field moves:

| Move | Condition | Change | Chance | Lines |
|---|---|---|---|---|
| Rain Dance | Attacker has Hydration and a status, or Dry Skin | +2 | certain | 6759 to 6769 |
| Rain Dance | Partner has Hydration and a status, or Dry Skin | +2 | certain | 6771 to 6783 |
| Sunny Day | Attacker has Leaf Guard, no status and 30% HP or more | +2 | certain | 6797, 6803 to 6808 |
| Sunny Day | Attacker has Flower Gift | +2 | certain | 6798, 6807 |
| Sunny Day | Attacker has Dry Skin | -2 | certain | 6799, 6811, 6812 |
| Sunny Day | Attacker has Solar Power, 50% HP or more | +1, then -2 with 50% | see text | 6800, 6815 to 6821 |
| Sunny Day | Attacker has Solar Power, below 50% HP | -2 | 50% | 6816, 6819 to 6821 |
| Sunny Day | The same four checks for the partner | same | same | 6823 to 6852 |
| Hail | Attacker has Ice Body or Snow Cloak, or knows Blizzard | +2 | certain | 6863 to 6870 |
| Hail | Partner has Ice Body or Snow Cloak, or knows Blizzard | +2 | certain | 6872 to 6881 |
| Sandstorm | Attacker has Sand Veil or is Rock type | +2 | certain | 6891 to 6900 |
| Sandstorm | Partner has Sand Veil or is Rock type | +2 | certain | 6903 to 6913 |
| Gravity | Gravity already in effect | -30 | certain | 6920 |
| Gravity | Attacker has Levitate, is Flying, or has Magnet Rise | -5 | certain | 6927 to 6935 |
| Gravity | Partner has Levitate, is Flying, or has Magnet Rise | -5 | certain | 6938 to 6947 |
| Gravity | Target has Levitate (guess rules), is Flying, or has Magnet Rise | +3 | 75% | 6950 to 6960 |
| Gravity | Target's partner, same | +3 | 75% | 6963 to 6973 |

Solar Power at 50% HP or more is meant to give +1 but falls through into the next label (bug O5), so it nets +1 or -1 at even odds. Rain Dance ignores Swift Swim and Rain Dish, and Sandstorm ignores Ground and Steel types, which the sand does not hurt either; these are omissions of design rather than code faults.

Trick Room (lines 6979 to 7030) looks at the speed ranks of the two AI Pokemon among all four battlers:

| Condition | Change | Chance | Lines |
|---|---|---|---|
| The partner, the target or the target's partner is at 0% HP | -30 | certain | 6981 to 6983 |
| Attacker fastest, partner second | -30 | certain | 6993 to 6996 |
| Attacker second, partner fastest | -30 | certain | 7000 to 7003 |
| Attacker first or second, otherwise | -5 | certain | 6998, 7004, 7026 |
| Attacker third, partner not last; or attacker last, partner not third | -5 | certain | 7009, 7019, 7026 |
| The two AI Pokemon are the two slowest | +5, else -5 | 75% / 25% | 7012, 7013, 7022, 7023 |

The rank comes from the live speed comparison, which already reverses order under Trick Room. So with Trick Room up and two AI Pokemon that are fast in normal terms, they rank slowest and the AI favours Trick Room again, which ends it. That happens to be the right move. The test for rank 0 at line 6997 cannot succeed, since the attacker holds rank 0 on that branch.

Follow Me (lines 7032 to 7100), by the attacker's and the partner's HP. Every change happens with 75% (`IfRandomLessThan 64` skips it):

| Attacker HP | Partner above 90% | Partner 51 to 90% | Partner 31 to 50% | Partner 30% or less | Lines |
|---|---|---|---|---|---|
| Above 90% | -1 | +1 | +2 | +3 | 7050, 7056 to 7060 |
| 51 to 90% | -2 | -1 | +1 | +2 | 7051, 7062 to 7066 |
| 31 to 50% | -2 | -2 | +1 | +2 | 7052, 7068 to 7072 |
| 30% or less | -5 | -5 | -5 | -5 | 7053, 7054 |

"Partner 30% or less" includes a fainted partner, so Follow Me with no partner left gets its largest bonus (bug O9).

Moves that hit the partner too, and partner combinations:

| Move | Condition | Change | Chance | Lines |
|---|---|---|---|---|
| Earthquake, Magnitude | Partner has Magnet Rise, Levitate, or is Flying | +2 | certain | 7135 to 7139 |
| Earthquake, Magnitude | Otherwise partner is Fire, Electric, Poison or Rock | -10 | certain | 7140 to 7147 |
| Earthquake, Magnitude | Otherwise | -3 | certain | 7148 |
| Future Sight, Doom Desire | Partner at 0% HP, or knows neither move | none | | 7156 to 7159 |
| Future Sight, Doom Desire | Partner knows one and is faster than the attacker | -3 | certain | 7161 to 7190 |
| Skill Swap | Attacker has Truant, Slow Start, Stall or Klutz | +5 | certain | 7200 to 7204 |
| Skill Swap | Otherwise the target has (guess rules) Shadow Tag, Pure Power, Huge Power, Mold Breaker, Solid Rock, Filter or Flower Gift | +2 | certain | 7205 to 7212 |
| Discharge | Partner has Motor Drive or Volt Absorb | +3 | certain | 7221, 7246 to 7249 |
| Discharge | Otherwise partner is Water or Flying | -10 | certain | 7250 to 7253 |
| Discharge | Otherwise partner is Ground | +3 | certain | 7258, 7259 |
| Discharge | Otherwise | -3 | certain | 7260 |
| Other Electric move | The target's partner has Lightning Rod (check rules) | -1 | certain | 7222, 7223, 7226, 7227 |
| Other Electric move | ... and that Pokemon is Ground | a further -8 | certain | 7228 to 7230 |
| Other Electric move | The attacker's partner has Lightning Rod | -10, then stop | certain | 7232 to 7234 |
| Surf | Partner has Dry Skin or Water Absorb | +3 | certain | 7270, 7289 to 7292 |
| Surf | Otherwise partner is Ground or Fire | -10 | certain | 7295 to 7298 |
| Surf | Otherwise | -3 | certain | 7299 |
| Other Water move | The target's partner has Storm Drain (check rules) | -1 | certain | 7271 to 7273 |
| Other Water move | The attacker's partner has Storm Drain | -10 | certain | 7275 to 7277 |
| Any Fire move | The attacker's Flash Fire is active | +1 | certain | 7311 to 7315 |
| Lava Plume | Partner has Dry Skin | -3 | certain | 7318, 7322, 7323 |
| Lava Plume | Otherwise partner has Flash Fire | +3 | certain | 7324, 7325 |
| Lava Plume | Otherwise partner is Grass, Steel, Ice or Bug | -10 | certain | 7326 to 7333 |
| Lava Plume | Otherwise | -3 | certain | 7334 |
| Any other damaging move | Partner alive and knows Helping Hand | +1 | certain | 6751, 7102 to 7111 |

A Future Sight partner that is faster means ranks: attacker last, or attacker third with partner first or second, or attacker second with partner first. The three "speed tie" branches (lines 7173 to 7175, 7181 to 7183, 7187 to 7189) roll 50% and then test whether the partner has the same rank as the attacker, which cannot happen, so there is no random part in practice (bug O8). The Discharge order is the battle_edits bug (O6). Surf has no Rock check, as the code's comment at 7294 notes, and treats a Water and Ground partner, which Surf does not hurt much, like a Ground one (O7). Earthquake leaves out Steel (O7). The second Discharge test at 7235 and the second Surf test at 7280 cannot be reached, because both moves were sent to their spread handler already. The Lightning Rod and Storm Drain tests on the other side use the check rules, and every Pokemon that can have those abilities in vanilla has a second possible ability, so both tests are off until the ability has been revealed. The Helping Hand bonus is reached only by moves that fall through the whole dispatch, so Electric, Fire and Water moves never get it (O10). Its flat-damage exclusions at 7105 to 7109 are needed, since those moves do get a comparison; the OHKO one is not.

Lines 7116 to 7125 (`TagStrategy_Unused_1` and `_2`) are never jumped to.

### Aimed at the partner (lines 7339 to 7694)

Everything here decides whether a move may be used on the AI's own partner. By the driver's rule, a result of 100 or more allows it and anything lower forbids it, so the sizes of the penalties do not matter, only whether there is one.

| Move | Condition | Change | Chance | Lines |
|---|---|---|---|---|
| Any | The partner's slot is permanently empty | -30 | certain | 7340 |
| Damaging Fire move | Partner has Flash Fire, not yet active | +3 | certain | 7344, 7352 to 7362 |
| Damaging Fire move | Otherwise | -30 | certain | 7358, 7361 |
| Damaging Electric move | Partner has Motor Drive: no change | 100 kept | 62.5% | 7376, 7377, 7383 |
| Damaging Electric move | Motor Drive, rest of the time, partner's Speed at +6 | -30 | 37.5% | 7384 |
| Damaging Electric move | Motor Drive, rest of the time, otherwise | +3 | 37.5% | 7385 |
| Damaging Electric move | Partner has Volt Absorb, full HP | -10 | certain | 7388 |
| Damaging Electric move | Volt Absorb, 91 to 99% HP | 100 kept | certain | 7389 |
| Damaging Electric move | Volt Absorb, 76 to 90% | +3 | 25% | 7390, 7394, 7395 |
| Damaging Electric move | Volt Absorb, 51 to 75% | +3 | 50% | 7391, 7398, 7399 |
| Damaging Electric move | Volt Absorb, 50% or less | +3 | 75% | 7392, 7402, 7403 |
| Damaging Electric move | Neither ability | -30 | certain | 7380 |
| Damaging Water move | Partner has Water Absorb or Dry Skin: the Volt Absorb ladder above | same | same | 7416 to 7439 |
| Damaging Water move | Neither ability | -30 | certain | 7420 |
| Any other damaging move | | -30 | certain | 7347 to 7350 |
| Skill Swap | Partner has (guess rules) Truant or Slow Start | +10 | certain | 7467 to 7469 |
| Skill Swap | Attacker has Levitate, partner (guess rules) has Levitate | -30 | certain | 7471 to 7475 |
| Skill Swap | Attacker has Levitate, partner is mono Electric | +2 | certain | 7477 to 7485 |
| Skill Swap | Attacker has Levitate, partner Electric only in its first type slot | +1 then -30 | certain | 7479 to 7482, 7487 to 7491 |
| Skill Swap | Attacker has Compound Eyes or No Guard, partner knows one of 14 inaccurate moves | +3 | certain | 7487 to 7511 |
| Skill Swap | Otherwise | -30 | certain | 7478, 7491, 7508 |
| Will-O-Wisp | Partner has Flash Fire | as the Fire rows | | 7524, 7525 |
| Will-O-Wisp | Partner has Guts, no status, not Fire, no Flame Orb or Toxic Orb, 81% HP or more | +5 | certain | 7527 to 7542 |
| Will-O-Wisp | Otherwise | -30 | certain | 7528 to 7540 |
| Thunder Wave | Partner is Ground | -30 | certain | 7548 to 7551 |
| Thunder Wave | Partner has Motor Drive or Volt Absorb | as the Electric rows | | 7553 to 7557 |
| Thunder Wave | Otherwise | -30 | certain | 7559 |
| Poison Powder, Poison Gas, Toxic | Partner has Poison Heal, no status, no Toxic Orb, 91% HP or less | +5 | certain | 7448, 7449, 7571 to 7580 |
| Poison Powder, Poison Gas, Toxic | Otherwise | -30 | certain | 7572 to 7578 |
| Helping Hand | Partner at 0% HP | -30 | certain | 7589 |
| Helping Hand | Partner above 50% HP, or partner fastest of all four | +2, else -1 | 75% / 25% | 7590 to 7597 |
| Helping Hand | Otherwise | 100 kept | certain | 7593 |
| Swagger | Partner holds a Persim or Lum Berry and its Attack is below +2 | +3 | certain | 7610, 7611, 7614 to 7616 |
| Swagger | Berry, Attack +2 or more | 100 kept | certain | 7615 |
| Swagger | No such berry | -30 | certain | 7612 |
| Trick, Switcheroo | Always | 100 kept | certain | 7452, 7453, 7621, 7622 |
| Gastro Acid | Partner's ability already suppressed | -30 | certain | 7630 |
| Gastro Acid | Partner has Truant or Slow Start | +5 | certain | 7632 to 7641 |
| Gastro Acid | Otherwise | 100 kept | certain | 7638 |
| Acupressure | Partner has Simple and any stat at +3 or more | -10 | certain | 7656, 7657, 7667 to 7674 |
| Acupressure | Partner without Simple has any stat at +6 | -30 | certain | 7658 to 7664 |
| Acupressure | Then partner below 51% HP | -1 | certain | 7677, 7686, 7687 |
| Acupressure | Then partner above 90% HP | +2 | 68.75% | 7678, 7681 to 7683 |
| Acupressure | Then 51 to 90% HP | +2 | 34.4% | 7679 to 7683 |
| Any other status move | | -30 | certain | 7456 |

"Status move" here means "no comparison made", so Explosion, Hyper Beam, Solar Beam, Flail, Fling and the OHKO moves aimed at the partner land on the last row and are forbidden. Fling's own test at line 7347 is never reached for that reason. Helping Hand's -1 forbids it for the turn, so with a healthy partner the AI refuses Helping Hand one time in four. The "100 kept" rows all allow the move: attacking a Volt Absorb partner at 91 to 99% HP, a Motor Drive partner most of the time, Swagger on a partner already at +2 Attack, and Trick, Switcheroo or Gastro Acid on any partner (O11). The inaccurate moves for Skill Swap are Fire Blast, Thunder, Cross Chop, Hydro Pump, Dynamic Punch, Blizzard, Zap Cannon, Megahorn, Focus Blast, Gunk Shot, Magma Storm, Power Whip, Seed Flare and Head Smash. The Skill Swap Levitate branch gives +1 and then -30 to a partner that is Electric in its first type slot only, because the "second type is not Electric" test jumps into the accuracy routine, which ends in -30 (O4); a partner that is Electric only in its second slot goes the same way without the +1. The Acupressure +6 test at 7658 and 7664 looks at Attack, Defense, Speed, Sp. Atk, Sp. Def, evasion and accuracy.

## Check HP (bit 8), lines 7696 to 7977

Check HP stops the AI using moves that suit a different HP level, both its own and the target's. On the partner it runs the partner half of Tag Strategy (line 7697), as described under the driver.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Attacker above 70% HP and the effect is in `CheckHP_DiscourageAtHighHP` | -2 | 80.5% | 7700, 7706 to 7708, 7716 to 7719 |
| Attacker 31 to 70% and the effect is in `CheckHP_DiscourageAtMediumHP` | -2 | 80.5% | 7701, 7711 to 7713, 7716 to 7719 |
| Attacker 30% or less and the effect is in `CheckHP_DiscourageAtLowHP` | -2 | 80.5% | 7702, 7703, 7716 to 7719 |
| Then, target above 70% HP: the target high table is empty | none | | 7724, 7730 to 7732, 7866, 7867 |
| Target 31 to 70% and the effect is in `CheckHP_Target_DiscourageAtMediumHP` | -2 | 80.5% | 7725, 7735 to 7737, 7740 to 7743 |
| Target 30% or less and the effect is in `CheckHP_Target_DiscourageAtLowHP` | -2 | 80.5% | 7726, 7727, 7740 to 7743 |

A move can take both penalties, -4 in all. The tables:

| Table | Lines | Effects |
|---|---|---|
| Attacker high | 7748 to 7761 | Explosion and Self-Destruct, Recover and its kin, Rest, Destiny Bond, Flail and Reversal, Endure, Morning Sun and its kin, Memento, Grudge, Roost, Healing Wish, Lunar Dance |
| Attacker medium | 7763 to 7810 | Explosion; every one-stage and two-stage raise and drop; Bide; Conversion; Light Screen; Mist; Focus Energy; Conversion 2; Safeguard; Belly Drum; Tickle; Cosmic Power; Bulk Up; Calm Mind; Dragon Dance; Lucky Chant; Power Swap; Guard Swap; Captivate |
| Attacker low | 7812 to 7864 | every one-stage and two-stage raise and drop; Bide; Conversion; Light Screen; Mist; Focus Energy; Rage; Conversion 2; Lock-On and Mind Reader; Safeguard; Belly Drum; Psych Up; Mirror Coat; Eruption and Water Spout; Tickle; Cosmic Power; Bulk Up; Calm Mind; Dragon Dance; Mud Sport; Water Sport; Acupressure; Metal Burst; Captivate |
| Target high | 7866, 7867 | empty |
| Target medium | 7869 to 7912 | every one-stage and two-stage raise and drop; Mist; Focus Energy; poison infliction; Pain Split; Perish Song; Safeguard; Tickle; Cosmic Power; Bulk Up; Calm Mind; Dragon Dance; Acupressure; Wring Out and Crush Grip; Captivate |
| Target low | 7914 to 7977 | sleep; Explosion; every one-stage and two-stage raise and drop; Bide; Conversion; Toxic; Light Screen; the OHKO moves; Super Fang (listed twice, 7936 and 7937); Mist; Focus Energy; confusion; poison; paralysis; Pain Split; Conversion 2; Lock-On; Spite; Perish Song; Swagger; Fury Cutter; Attract; Safeguard; Psych Up; Mirror Coat; Will-O-Wisp; Tickle; Cosmic Power; Bulk Up; Calm Mind; Dragon Dance; Acupressure; Wring Out; Captivate |

Reflect is in no table although Light Screen is in three.

## Weather (bit 9), lines 7979 to 8019

Weather is meant to make the AI set its weather on the first turn. It never scores against the partner (line 7980).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Not battle turn 0 | stop | certain | 7983, 7984 |
| Sunny Day, Rain Dance, Sandstorm or Hail, and that weather is not already up | +5 | certain | 7987 to 8016 |
| Any other move, and it is not sunny | +5 | certain | 7991 to 7995, 8012 to 8016 |

The last row is bug O1: after the four effect tests there is no jump, so every other move falls into the Sunny Day handler and gets the same +5 unless the sun is out. On turn 0 under clear skies every move gets +5, so the flag changes nothing. It changes the order only when weather is already up from the map: a weather move that repeats the current weather loses its +5 while everything else keeps it, and under sun the other three weather moves are the only moves to gain. The `LoadIsFirstTurnInBattle` test at 8014 is always true on turn 0, so it adds nothing. Seventeen trainers carry this flag in Oxide, among them Gardenia, Wake, Candice, Volkner, Bertha and Flint, so this bug is live.

## Harassment (bit 10), lines 8021 to 8071

Harassment favours moves that annoy the target. It never scores against the partner (line 8022). The label is spelled `Harrassment` in the code.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| The move's effect is in `Harrassment_Effects` | +2 | 50% | 8026 to 8031 |

The table (lines 8036 to 8071): sleep; one-stage Attack, Defense, accuracy and evasion drops; confusion; two-stage Attack, Defense, Speed and Sp. Def drops; poison; paralysis; Leech Seed; Encore; Spite; Spikes; Swagger; Attract; Torment; Flatter; Will-O-Wisp; Nature Power; Yawn; Knock Off; Imprison; Secret Power; Teeter Dance; Tickle; Camouflage; Embargo; Psycho Shift; Toxic Spikes; Defog; Captivate. Toxic is absent while Poison Powder is present; Nature Power, Secret Power and Camouflage are odd members.

## Roaming Pokemon (bit 29), lines 8073 to 8089

A roamer flees unless it believes it is trapped. `TrainerAI_Init` gives a roamer this flag and nothing else (`trainer_ai.c` lines 246 to 247).

| Condition | Result | Lines |
|---|---|---|
| The roamer is bound (Wrap and its kin) or held by Mean Look, Block or Spider Web | no change: all usable moves stay at 100 and one is picked at random | 8076, 8077 |
| The target has Shadow Tag (real ability) | same | 8078, 8079 |
| The target has Arena Trap and the roamer does not have Levitate | same | 8080 to 8083 |
| Otherwise | `Escape` | 8085, 8086 |

Escape sets the break flag, so the first move slot ends the evaluation. The check misses what the engine's own Arena Trap test (`BattlerIsGrounded`, `battle_lib.c` line 5554) knows: a Flying roamer is not held by Arena Trap, but the AI thinks it is, so Articuno, Zapdos and Moltres stay and fight a Dugtrio (O13). Ingrain and Magnet Pull are not checked either.

## Safari (bit 30), lines 8091 to 8094, and Catch Tutorial (bit 31), lines 8096 to 8103

Safari would run `Dummy3E 1`, `Dummy3F` and `Escape`. Neither dummy command advances the script cursor, so the interpreter would call `Dummy3E` for ever and the game would hang (O14). Catch Tutorial flees when the target is at 20% HP or less (lines 8098, 8099) and otherwise changes nothing. Nothing in this tree sets either bit, and wild Pokemon do not reach the AI at all, so both routines are dead code. `Terminate` (lines 8105, 8106) is the shared "end this move" label.

## How far these flags can push a score

No routine in this part can push a score past 127 by itself. The largest totals one move can collect here, for the flag sets Oxide's trainers actually carry:

| Case | Flags | Total |
|---|---|---|
| Turn 0, a +1 priority move that kills | Evaluate Attack, Weather | +11 |
| Turn 0, a setup move also in the Risky list (Swagger) | Setup First Turn, Risky, Prioritize Extremes | +6 |
| Turn 0, a status move under Baton Pass | Baton Pass | +8 |
| Double battle, Gravity with both opponents floating | Tag Strategy | +6 |
| Double battle, Lava Plume with Flash Fire active and a Flash Fire partner | Tag Strategy | +4 |
| Partner pass, Skill Swap onto Truant | Tag Strategy, twice with Check HP | +10 or +20 |

With every flag in this part at once, Swagger on turn 0 could collect +21 (Setup First Turn, Risky, Prioritize Extremes, Baton Pass's fall-through, Weather's fall-through, Harassment); no trainer carries that set. So an overflow needs Expert to add around +17 on top of the realistic worst case here, and the Expert parts decide whether that can happen.

## Apparent bugs

Fixed on 2026-09-22: O1, the Weather flag, and O11, Trick, Switcheroo and Gastro Acid on the partner (both vanilla fixes, approved by Ian), O6, Discharge (battle_edits, vanilla fix approved by Ian on 2026-09-15), and O19, the ability byte (Oxide). The rest stand as vanilla has them.

Every script bug below is present in vanilla Platinum at the same line on `main`, because `script.s` is unchanged. The C bugs are present in vanilla at the same lines of `trainer_ai.c`. One entry is introduced by Oxide. None has been fixed.

1. O1, Weather falls through for every move. Lines 7987 to 7992. Present in vanilla Platinum, `main` `script.s` lines 7987 to 7992. The four `IfCurrentMoveEffectEqualTo` tests have no jump after them, so a move that is not a weather move runs `Weather_Sun` and gets +5 unless it is sunny. Evidence: line 7991 is followed directly by the label `Weather_Sun:` at 7992. Effect: the flag gives every move +5 on turn 0 and so does nothing, except to favour the non-sun weather moves in sun and to punish repeating the current weather.
2. O2, Baton Pass's "other moves" fall into the boosting handler. Lines 6590 to 6603. Present in vanilla Platinum, `main` `script.s` lines 6590 to 6603. After `AddToMoveScore 3` at 6592 there is no end, so the move also gets the Swords Dance treatment: +5 on turn 0, -10 below 60% HP, else +1. Effect: a generic status move scores +8 on turn 0, above the four named boosting moves (+5) that the routine singles out. pokeemerald's `AI_BatonPass` has the same shape, so the fault is old.
3. O3, Baton Pass lets some attacks through its "status moves only" gate. Lines 6572, 6573. Present in vanilla Platinum, `main` `script.s` lines 6572, 6573. The comment says damaging moves are ignored, but the test is "no comparison made", which includes Explosion, Hyper Beam, Solar Beam, Focus Punch, Eruption, Sucker Punch, Head Smash, Flail and the OHKO moves. They then get the +3 and the fall-through of O2.
4. O4, Skill Swap to give Levitate forbids most Electric partners. Lines 7477 to 7491. Present in vanilla Platinum, `main` `script.s` lines 7477 to 7491. The comment promises +1 for an Electric partner and +1 more if mono Electric. The code sends a partner whose second type is not Electric (or whose first type is not) to the accuracy routine, which ends in -30 unless the attacker has Compound Eyes or No Guard. Only a mono-Electric partner gets its +2.
5. O5, Solar Power at high HP falls through into the penalty. Lines 6815 to 6821 and 6846 to 6852. Present in vanilla Platinum, `main` `script.s` same lines. After the +1 at 6817 (and 6848) the code runs straight on into the 50% -2 meant for low HP. Effect: +1 or -1 at even odds instead of +1.
6. O6, Discharge treats an immune partner as weak. Lines 7250 to 7259. Present in vanilla Platinum, `main` `script.s` lines 7250 to 7259. The Water and Flying tests come before the Ground test, so a Ground partner that is also Water or Flying gets -10 though Discharge cannot touch it. The code's comment at 7255 says so. This is the battle_edits fix; see below.
7. O7, Earthquake and Surf miss weak partners. Earthquake, lines 7140 to 7148, has no Steel test, so a Steel partner gets -3 instead of -10. Surf, lines 7294 to 7299, has no Rock test (the code's comment at 7294), and a Water and Ground partner, which takes neutral damage from Surf, gets -10. Present in vanilla Platinum, `main` `script.s` same lines.
8. O8, Future Sight's speed-tie branches can never fire. Lines 7173 to 7175, 7181 to 7183, 7187 to 7189. Present in vanilla Platinum, `main` `script.s` same lines. Each rolls 50% and then asks whether the partner has the attacker's own speed rank; `LoadBattlerSpeedRank` gives every battler a distinct rank (`trainer_ai.c` lines 2072 to 2093), so the answer is always no. Effect: none beyond the wasted roll; the comment's "50% on a tie" never happens.
9. O9, Follow Me rewards a missing partner. Lines 7057 to 7072. Present in vanilla Platinum, `main` `script.s` same lines. The partner bands test "HP above 30%" and fall through to the largest bonus, so a fainted partner (0%) reads as "badly hurt": +3 (75%) with the attacker above 90% HP.
10. O10, Helping Hand's bonus skips Electric, Fire and Water moves. Lines 6747 to 6751. Present in vanilla Platinum, `main` `script.s` same lines. The type branches at 6748 to 6750 end the move before the Helping Hand test at 6751, although the comment at 7103 says every damaging move but the fixed-damage ones gets +1.
11. O11, the AI will Trick, Switcheroo or Gastro Acid its own partner. Lines 7452, 7453, 7621, 7622 and 7638, with `trainer_ai.c` lines 431 to 436. Present in vanilla Platinum, `main` same lines. `TagStrategy_PartnerTrick` is an empty stub and Gastro Acid's "otherwise" changes nothing, so these moves stay at 100 on the partner and pass the driver's filter. When the attacker's best move against both opponents scores 100, the partner is one of the tied targets and is picked at random; when it scores less, the partner wins outright.
12. O12, Evaluate Attack gives status moves the four-times bonus. Lines 6361 to 6384. Present in vanilla Platinum, `main` `script.s` same lines. A status move gets "no comparison made", which is not "not highest", so it runs on to the effectiveness test, and the type chart works for status moves because it starts from a fixed 40 (`trainer_ai.c` lines 1317 to 1343). Thunder Wave into Gyarados gets +2 (68.75%).
13. O13, a Flying roamer believes Arena Trap holds it. Lines 8080 to 8083. Present in vanilla Platinum, `main` `script.s` same lines. Only Levitate is exempted; the engine also exempts Flying types and Magnet Rise.
14. O14, the Safari routine would hang the game. Lines 8092, 8093, with `trainer_ai.c` lines 1881 to 1889. Present in vanilla Platinum, `main` same lines. `AICmd_Dummy3E` and `AICmd_Dummy3F` return without moving the cursor, so `TrainerAI_EvalMoves` (line 501) would call the same command for ever. Unreachable today, since nothing sets the Safari bit.
15. O15, the double-battle driver shifts a signed mask. `trainer_ai.c` lines 354, 379, 391. Present in vanilla Platinum, `main` same lines. `thinkingMask` is an `int`; with bit 31 (Catch Tutorial) set, `>>=` keeps the sign bit and the loop never ends. Unreachable today.
16. O16, the driver leaves a target's score unset after an escape. `trainer_ai.c` lines 396 to 399. Present in vanilla Platinum, `main` same lines. The escape and Safari branches set the action but not `maxScoreForBattler`, which is then compared uninitialised at 441 to 454. Unreachable today, since no escaping flag runs in a double battle; it would matter if Oxide's wild doubles sent wild Pokemon through the AI with an escaping flag.
17. O17, Acupressure's retarget assumes the AI is on side 1. `trainer_ai.c` lines 462 to 465. Present in vanilla Platinum, `main` same lines. "Chosen target on side 0" means "an opponent" only for the enemy side. For a partner AI on the player's side (Cheryl and the others), side 0 is its own side, so an Acupressure it chose for the player's Pokemon is redirected to itself.
18. O18, "0% HP" doubles as "absent". Lines 6663, 6675, 6981 to 6983, 7156, 7589, with `trainer_ai.c` lines 618 to 631. Present in vanilla Platinum, `main` same lines. The percentage is rounded down, so a Pokemon on 1 HP with more than 100 maximum HP counts as gone: Trick Room gets -30 and Future Sight skips its partner check.
19. O19, the remembered-ability store truncates Oxide's abilities. `include/battle/ai_context.h` line 28 with `battle_script.c` line 12178. Introduced by Oxide. This is basic.md's B11, and it reaches this part through every target-side ability read: Gravity's Levitate test (6951, 6964), the Skill Swap lists (7205 to 7212, 7467 to 7475), Lightning Rod (7222) and Storm Drain (7271). Oxide widened `BattleAI_SetAbility`'s parameter to u16 but the array it writes is still `u8`, so a revealed ability of id 256 or more is remembered as id minus 256. The aliases that would matter here: Quark Drive reads as Levitate, Commander as Shadow Tag, Supreme Overlord as Huge Power, Beads of Ruin as Lightning Rod, Poison Puppeteer as Truant. No Oxide species has any of those five today, so this part is not affected yet.

Dead code, harmless, all present in vanilla at the same lines: the kill-branch tests at 6389, 6394 and 6395; the OHKO tests at 6645 and 6708; the Explosion test at 6688; the second Discharge and Surf tests at 7235 and 7280; Fling at 7347; the rank-0 test at 6997; `TagStrategy_Unused_1` and `_2` at 7116 to 7125; the partner-fainted test at 7340, which the driver makes unreachable by never passing a 0-HP target. One C bug sits outside this part's reach: `LOAD_DEFENDER_PARTNER_TYPE_2` loads type 1 (`trainer_ai.c` line 982, vanilla), but no script line uses it.

## The battle_edits fixes

Only one of the eleven falls in this part: the Discharge double-battle scoring fix. I could not read the guide (it is not one of the two references I was cleared to fetch), so the fix below is worked out from the code.

What goes wrong: `TagStrategy_SpreadElectricMove` (lines 7238 to 7260) tests the partner in the order Motor Drive or Volt Absorb (+3), Water (-10), Flying (-10), Ground (+3), else -3. The first test that matches ends the move. A Ground type takes nothing from Discharge whatever its other type, but a Water and Ground partner (Wooper, Quagsire, Marshtomp, Swampert, Barboach, Whiscash, Gastrodon) or a Flying and Ground partner (Gligar, Gliscor) matches the Water or Flying test first and gets -10. The fix moves the Ground test (7258, 7259) above the Water test (7250). The score change: those partners go from -10 to +3, thirteen points, in each opponent pass; every other partner is unchanged. Discharge with such a partner goes from nearly never chosen to mildly favoured. The bug is present in vanilla Platinum (`main` `script.s` lines 7250 to 7259), so this fix changes vanilla behaviour and must be named as such when applied.

The other ten are not in this part. The Water immunity versus Dry Skin check (line 78) and the Sunny Day check (line 215 and its handler) are in Basic. The Foresight and Odor Sleuth Ghost check, the Facade status check, the Leaf Guard Sunny Day logic, the Water Spout and Eruption HP check, the charge-turn scoring fix and the Thunder scoring fix are in Expert (around lines 1657 to 1742 and their handlers). Fire Fang against Wonder Guard and the Rage glitch are named for battle-engine behaviour, not AI scoring; I did not locate them. This part's Tag Strategy Sunny Day and Leaf Guard rows (6788 to 6855) are a separate routine from the Expert Leaf Guard fix.

## Oxide consequences

These routines recognise moves in four ways, and whatever Oxide adds outside those lists falls through to the default, which here is "no change".

By battle effect: Evaluate Attack's special cases (6365 to 6400), the tables of Setup First Turn, Risky, Check HP and Harassment, Baton Pass's Protect test (6586), Tag Strategy's fixed-damage lists (6645 to 6649, 6708 to 6712, 7105 to 7109) and poison test (7448, 7449), and Weather's four effects (7987 to 7990). None of the new effects 277 to 406 is on any of these lists. So Hone Claws, Quiver Dance, Coil, Shift Gear, Shell Smash, Work Up, Cotton Guard and the other three-stage effects, Sticky Web, Aurora Veil and the rest get no Setup First Turn bonus and no Check HP penalty; Toxic Thread, Venom Drench, Tearful Look, Parting Shot and the three-stage drops get nothing from Harassment; and Snowscape (`WEATHER_SNOW`) is not a weather move to the Weather flag, so it falls through with everything else (O1). New moves on old effects inherit that effect's treatment: King's Shield, Spiky Shield, Baneful Bunker, Max Guard, Obstruct, Silk Trap and Burning Bulwark use Protect's effect, so Baton Pass gives them +2, and its "used last turn" list (7615 to 7618) names only Protect and Detect, so it will reward a second consecutive King's Shield. Accelerock and Jet Punch get the +1 priority kill bonus; Aqua Cutter, Drill Run and Snipe Shot are Risky; Misty Explosion is Explosion throughout; Thunderclap is Sucker Punch throughout; Play Nice, Baby-Doll Eyes, Confide, Eerie Impulse and Shelter count as setup and harassment moves as their effects dictate; Nature's Madness and Ruination count as Super Fang for Check HP.

By move id: all of Tag Strategy's special cases and Baton Pass's four boosting moves. Oxide's new spread moves (Bulldoze, Sludge Wave, Boomburst, Parabolic Charge, Petal Blizzard, Searing Shot, Mind Blown, Misty Explosion) get no penalty for hitting the partner, so the AI will Bulldoze next to its own Heatran. Rage Powder is not Follow Me, Snowscape is not Hail, and the terrains, Wonder Room, Magic Room, Ally Switch, After You, Quash, Wide Guard and Quick Guard have no double-battle handling. The moves that help an ally (Heal Pulse, Floral Healing, Pollen Puff, Decorate, Instruct, Coaching) are status or damaging moves without a partner case, so the partner pass gives them -30 and the AI can never use them on its partner. Shell Smash, Quiver Dance and the others are not in Baton Pass's boosting list, so they get the generic +3 and fall-through.

By ability id: every ability test in Tag Strategy and the roaming routine. The newer absorbing and immunity abilities (Sap Sipper, Earth Eater, Well-Baked Body, Wind Rider, Storm Drain and Lightning Rod in their later absorbing form, Telepathy against an ally's spread move) and the newer weather abilities (Swift Swim and Rain Dish were already missing; Chlorophyll, Sand Rush, Sand Force, Slush Rush, Overcoat) are unknown here. If element 5 gives Lightning Rod or Storm Drain their later form, the -10 for a partner with either ability (7233, 7276) becomes wrong, since the partner would absorb the move instead of taking it. Ability values themselves compare correctly as 32-bit words; the one failure is the u8 store, O19.

By type: Rock, Flying, Electric, Fire, Water, Ground, Poison, Grass, Steel, Ice and Bug are named. Fairy, type 18, is named nowhere in this part and needs to be nowhere: none of the spread-move tables involves a type that Fairy resists or is weak to among Ground, Electric, Water and Fire moves, except that a Fire move is neutral on Fairy, which the tables already treat as the default. The effectiveness tests go through the real type chart, which basic.md reports already has Fairy. `LOAD_MOVE_TYPE` reads the listed type, so Oxide's type-changing moves (Multi-Attack, Techno Blast) are placed by their listed type in the Electric, Fire and Water branches.

The wild double battles planned for element 8 do not by themselves exercise this part more: as shown under the driver, wild Pokemon never reach the AI. If the implementation does send them through it, they will presumably run Tag Strategy alone, and O16 becomes reachable if any escaping flag is ever added.

## Where the references disagree with the code

lhearachel's gist agrees with the code on most values and differs in these places. It gives Evaluate Attack's four-times bonus a 31.25% chance; the code's chance is 68.75% (`IfRandomLessThan 80` skips it, line 6383). For Baton Pass it lists "all other moves, +3" as a separate step, missing the fall-through (O2). It says Thunder Wave on the partner is always -30, missing the Motor Drive and Volt Absorb route (7553 to 7557). It says a Poison Heal partner must be at 81% HP or more; the code requires 91% or less (7578), and the code's own comment also says 81%. It gives Solar Power a clean +1 (O5), the Future Sight tie a live 50% (O8), and Skill Swap's Levitate case a clean +1 (O4). It gives Acupressure at 51 to 90% HP a 31.25% chance of +2, as does the code's comment at 7655; the code's chance is 34.4%. It describes Weather as scoring only weather moves, missing O1. It says nothing on Roaming, Safari or Catch Tutorial.

The code's own comments disagree with it in a few more places: Lava Plume's comment (7308) gives a Dry Skin partner +3, the code gives -3 (7323), which suits Dry Skin's fire weakness but, being tested first, lets a Dry Skin Parasect (Bug and Grass) escape its -10; Baton Pass's comment at 6625 says "+1 for each positive stat stage", the code stops at the first match; the Tag Strategy damage comments call a missing partner "on their last Pokemon".

The pokemow page could not be read in full: its per-move detail is behind an interactive selector that the fetch did not return. Its summary names the modules "Strong AI" (Evaluate Attack) and "Doubles AI" (Tag Strategy), which match the code's structure, and says nothing checkable about the other flags.
