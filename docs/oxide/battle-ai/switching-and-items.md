# Switching, replacements, items and the AI's damage estimate

This part covers the plain C that sits beside the script interpreter: the damage figure the AI uses to compare moves, the decision to switch out, the choice of which Pokemon comes in, and the decision to use an item. It covers `src/battle/trainer_ai/trainer_ai.c` from line 2750 to the end (line 4199), the replacement routine in `src/battle/battle_lib.c`, and the callers in `src/battle/battle_display.c` and `src/battle/battle_controller_player.c`.

Everything was read from this tree and compared with vanilla on `main`. In `trainer_ai.c` the only difference from vanilla is two variable types at lines 3645 and 3646, which do not move any line, so every `trainer_ai.c` line number below is also the vanilla line number. In `battle_lib.c` the replacement routine and the type helpers it uses sit 71 lines lower than on `main` (the Fairy rows added to the type chart and a few other edits push them down); the vanilla line is given wherever a bug is cited. The lines cited in `battle_display.c` are unchanged from vanilla.

The short version, for a reader who wants the answer first. A trainer's turn is decided in the order switch, then item, then move. Oxide's trainers never use items, because nothing ever gives them any, so in practice the order is switch or move. The switch rules are seven checks with fixed chances, listed in the table under "Switching". The AI's damage figure is the game's own damage formula at the top of the damage range: the 85 to 100 roll drawn for each move in `TrainerAI_Init` is never used, because every script call asks for maximum damage.

## Where these routines run, and in what order

A trainer battler's turn starts in `Task_TrainerSetCommandSelection` (`battle_display.c` lines 3408 to 3417), which calls `TrainerAI_PickCommand` (`trainer_ai.c` lines 3989 to 4040). That function decides the command.

1. It only thinks at all when the battle is a trainer battle or the battler is on the player's side, which means an AI partner (line 4000). A wild Pokemon, in singles or in Oxide's wild doubles, skips straight to Fight.
2. It asks `TrainerAI_ShouldSwitch` first (line 4001). If that says yes, the command is Party (line 4030), and the slot to send in is settled before returning (lines 4004 to 4028; see "Choosing the Pokemon that comes in").
3. Only if there is no switch does it ask `TrainerAI_ShouldUseItem` (lines 4034 to 4036). If that says yes, the command is Item.
4. Otherwise the command is Fight (line 4039). The game then asks for a move through `Task_TrainerShowMoveSelectMenu`, which calls `TrainerAI_Main` (`battle_display.c` line 3590), the scoring engine described in `README.md`.

So the decision order is switch, item, move, and the move scoring never runs on a turn the AI switches or uses an item. The brief this file was written from had the order as item, switch, move; the code puts the switch first.

The execution order is separate from the decision order. Once every battler has chosen, the controller puts every Item and Party action ahead of every Fight action (`battle_controller_player.c` lines 753 to 770), sorting battlers who chose the same kind of action by speed. So an AI switch always happens before any move that turn, whatever the speeds.

Two consequences follow for wild Pokemon, which matter because Oxide adds wild double battles. A wild Pokemon never switches and never uses an item (line 4000). And it never runs the scoring script either: `Task_TrainerShowMoveSelectMenu` only calls `TrainerAI_Main` for a trainer battle, a roamer, the game's scripted first battle, or a player-side battler (`battle_display.c` lines 3587 to 3590); any other wild Pokemon picks a random usable move (lines 3600 to 3612). The README's remark that Tag Strategy will run in Oxide's wild doubles is therefore wrong for the wild side; it runs only for an AI partner fighting alongside the player there.

When a Pokemon faints, or uses U-turn, the replacement is asked for separately, through `Task_TrainerShowPartyMenu` (`battle_display.c` lines 4528 to 4562), described under "Choosing the Pokemon that comes in".

## Every function from line 2750 to the end

| Lines | Function | What it is | Where described |
|---|---|---|---|
| 2752 to 2755 | `AIScript_Iter` | moves the script cursor | script engine, not decision logic |
| 2765 to 2782 | `AIScript_Battler` | turns the script's battler code (attacker, defender, their partners) into a battler id | script engine, not decision logic |
| 2799 to 2849 | `TrainerAI_CalcAllDamage` | damage of all four moves, and the highest | the damage estimate |
| 2851 | include of `weight_to_power.h` | the Low Kick and Grass Knot table | the damage estimate |
| 2868 to 3113 | `TrainerAI_CalcDamage` | damage of one move | the damage estimate |
| 3127 to 3248 | `TrainerAI_MoveType` | type of a variable-type move on the field | the damage estimate |
| 3263 to 3272 | `AI_PerishSongKO` | switch rule 1 | switching |
| 3286 to 3350 | `AI_CannotDamageWonderGuard` | switch rule 2 | switching |
| 3361 to 3546 | `AI_OnlyIneffectiveMoves` | switch rule 3 | switching |
| 3560 to 3624 | `AI_HasSuperEffectiveMove` | the gate before rules 6 and 7, also used by rule 4 | switching |
| 3640 to 3714 | `AI_HasAbsorbAbilityInParty` | switch rule 4 | switching |
| 3727 to 3807 | `AI_HasPartyMemberWithSuperEffectiveMove` | rules 6 and 7, and part of rule 5 | switching |
| 3817 to 3859 | `AI_IsAsleepWithNaturalCure` | switch rule 5 | switching |
| 3872 to 3884 | `AI_IsHeavilyStatBoosted` | the stat-boost gate | switching |
| 3894 to 3987 | `TrainerAI_ShouldSwitch` | runs the rules in order | switching |
| 3989 to 4040 | `TrainerAI_PickCommand` | switch, item or fight | decision order, and replacements |
| 4056 to 4199 | `TrainerAI_ShouldUseItem` | item use | items |

The replacement routine `BattleAI_PostKOSwitchIn` is in `battle_lib.c` lines 7994 to 8160 (vanilla 7923 to 8089), with `Move_CalcVariableType` below it at line 8168.

## The damage estimate

The script asks for damage through five commands: "is this the highest-damage move" (`FlagMoveDamageScore`), "does this move kill" and its opposite, "does a party member out-damage me", "does the defender out-damage me", and the doubles "highest damage with partner". All of them end in `TrainerAI_CalcAllDamage` or `TrainerAI_CalcDamage`. The scoring that uses the figures belongs to the other part files; this section says how the figure itself is made.

### Which moves get a figure at all

Before calculating, each caller checks a move's battle effect against two tables at the top of the file (lines 31 to 61). The same test appears in `TrainerAI_CalcAllDamage` (lines 2809 to 2838) and in the script commands that call `TrainerAI_CalcDamage` directly. A move gets a damage figure when its effect is in the second table ("alternative power"), or when it is a real move, its effect is not in the first table ("no damage calculation"), and its listed power is more than 1. Any other move is given 0 damage.

The first table, moves the AI never calculates:

| Effect id | Effect | Vanilla moves | Oxide moves that share it |
|---|---|---|---|
| 7 | faint the user | Selfdestruct, Explosion | Misty Explosion |
| 8 | Dream Eater | Dream Eater | |
| 39 | charge turn, high critical | Razor Wind | |
| 75 | charge turn, critical and flinch | Sky Attack | |
| 80 | recharge next turn | Hyper Beam, Giga Impact, Blast Burn, Frenzy Plant, Hydro Cannon, Rock Wrecker, Roar of Time | Eternabeam, Meteor Assault, Prismatic Laser |
| 145 | charge turn, Defense up | Skull Bash | |
| 151 | charge turn skipped in sun | SolarBeam | Solar Blade |
| 161 | Spit Up | Spit Up | |
| 170 | Focus Punch | Focus Punch | |
| 182 | lowers own Attack and Defense | Superpower | |
| 190 | weaker at lower HP | Eruption, Water Spout | Dragon Energy |
| 248 | fails unless the target attacks | Sucker Punch | Thunderclap |
| 269 | half recoil | Head Smash | Light of Ruin |

The second table, moves whose power is worked out specially:

| Effect id | Effect | Moves | How `TrainerAI_CalcDamage` handles it (lines) |
|---|---|---|---|
| 135 | Hidden Power | Hidden Power | power 30 to 70 and type from the IVs, the Generation 4 formula (2973 to 2993) |
| 219 | Gyro Ball | Gyro Ball | power 1 + 25 x target speed / user speed, at most 150 (2995 to 3003) |
| 222 | Natural Gift | Natural Gift | power and type from the held berry, none under Klutz or Embargo (2885 to 2895) |
| 268 | Judgment | Judgment | type from the held plate (2897 to 2971) |
| 41 | 40 damage | Dragon Rage | 40 (3005 to 3007) |
| 87 | damage equal to level | Seismic Toss, Night Shade | the user's level (3009 to 3012) |
| 88 | Psywave | Psywave | level x (5 to 15) / 10, drawn at random each time, each of the eleven values 1 in 11 (3014 to 3016) |
| 121 | stronger with friendship | Return, and Oxide's Pika Papow and Veevee Volley | friendship x 10 / 25 for Return only (3018 to 3021) |
| 123 | stronger with low friendship | Frustration | (255 minus friendship) x 10 / 25 (3023 to 3026) |
| 130 | 20 damage | Sonic Boom | 20 (3051 to 3053) |
| 196 | stronger against heavier targets | Low Kick, Grass Knot | the weight table below (3055 to 3072) |

The special cases in `TrainerAI_CalcDamage` are chosen by move id, not by effect, so a move that shares an effect but has its own id takes the default path. That default (lines 3074 to 3078) passes power 0 and type 0 to the engine, which means "use the move's own listed power and type".

The weight table (`weight_to_power.h`), in the game's unit of 0.1 kg, matches the engine's own Low Kick code in `battle_script.c`:

| Target weight up to | Power |
|---|---|
| 10.0 kg | 20 |
| 25.0 kg | 40 |
| 50.0 kg | 60 |
| 100.0 kg | 80 |
| 200.0 kg | 100 |
| heavier | 120 |

The two tables and the special cases are consistent with each other except for Magnitude, whose branch at lines 3028 to 3049 can never run: Magnitude's effect (126, which the decomp names `PSYWAVE`) is in neither table and its listed power is 1, so the gate gives it 0 before the special case is reached. The AI therefore treats Magnitude as a move that does no damage. Every other power-1 move not in the second table also scores 0: the one-hit KO moves, Counter, Mirror Coat, Metal Burst, Bide, Super Fang, Endeavor, Flail, Reversal, Present, Fling, Trump Card, Wring Out, Crush Grip and Punishment.

### How the figure is made

For a move that passes the gate, `TrainerAI_CalcDamage` (lines 2868 to 3113) works in three steps.

1. For a fixed-damage move (Dragon Rage, Sonic Boom, Seismic Toss, Night Shade, Psywave) the damage is set directly. For everything else it calls the engine's `BattleSystem_CalcMoveDamage` with the attacker, the AI's current target, the target side's screens, the field conditions and a critical multiplier of 1 (lines 3081 to 3091). That is the same function the real attack uses, so the attacker's and defender's stats and stages, abilities such as Huge Power and Technician, items such as Choice Band and type-boosting items, screens and weather all count exactly as they do in battle.
2. It then calls `BattleSystem_ApplyTypeChart` (lines 3096 to 3103). That applies same-type bonus (doubled by Adaptability), the type chart, Levitate and Magnet Rise against Ground moves, the Wonder Guard test, and Filter, Solid Rock, Expert Belt and Tinted Lens. For fixed-damage moves a flag is set first (line 3093) so the chart can still make the move fail against an immune type but cannot scale the number.
3. If the result carries any immunity flag (type immunity, Wonder Guard, Levitate, Magnet Rise) the damage is 0 (lines 3106 to 3107). Otherwise it is multiplied by the roll and divided by 100 (line 3109).

What is left out: critical hits, and anything the real attack applies after this point in its battle script, such as Life Orb and the damage-halving berries. The engine's variable-power moves that set their power in a battle script (Brine, Payback and the like) are seen at their listed base power, because the AI only reproduces the handful of cases in the table above. Weather Ball was one of them until element 6 gave the estimate its case (2026-09-22).

`TrainerAI_CalcAllDamage` (lines 2799 to 2849) runs this for all four moves and returns the highest figure. The comparison that uses it (`AICmd_FlagMoveDamageScore`, lines 1052 to 1062) counts a move as the highest when no other move is strictly higher, so two equal moves are both "highest".

### The damage roll is never used

`TrainerAI_Init` draws a roll from 85 to 100 for each move slot (line 240), and `TrainerAI_CalcAllDamage` would use it when asked (lines 2829 to 2833). But the script decides whether to ask, and all 18 calls in `script.s` pass `USE_MAX_DAMAGE` (0), never `ROLL_FOR_DAMAGE` (1). Vanilla's script has the same 18 calls. So in practice every AI damage figure uses a roll of 100: the AI always assumes its move does the top of its damage range, and a "does this move kill" test succeeds whenever the maximum non-critical roll kills. The only randomness left in the figure is Psywave, which is re-drawn every time it is calculated, and the four rolls in `TrainerAI_Init` still consume four random numbers per decision.

This contradicts step 2 of `README.md`, which says the script's damage comparisons use the per-move rolls; they could, but the script never asks for them. pokemow's page agrees with the code here: it lists random variance among the factors the AI leaves out.

### The type of a variable-type move

`TrainerAI_MoveType` (lines 3127 to 3248) gives the type of a move known by a battler on the field, for the switching checks. For Natural Gift it asks the engine, for Judgment it reads the plate, for Hidden Power it uses the IV formula, and for Weather Ball it reads the weather. For every other move it returns 0, which the type-chart functions read as "the move's own type". Its bench counterpart for Pokemon in the party is the engine's `Move_CalcVariableType` (`battle_lib.c` line 8168). Both leave Weather Ball's type unset when there is no weather or when Cloud Nine or Air Lock is out (see bug 1).

## Switching

`TrainerAI_ShouldSwitch` (lines 3894 to 3987) is asked once per turn for each AI battler, before its item and move.

### When it will not even look

It returns "no switch" at once if the battler cannot legally switch as the AI understands it (lines 3906 to 3913): it is bound or under Mean Look (the trapped volatile status), it has used Ingrain, any opposing Pokemon has Shadow Tag or Arena Trap, or it is Steel-type and any other battler has Magnet Pull. This is stricter than the engine's own test (`Battler_IsTrapped`, `battle_lib.c` line 5538). The AI still thinks it is trapped when holding Shed Shell, when it has Shadow Tag itself, when it is Flying-type, Levitating or under Magnet Rise against Arena Trap, and when the Magnet Pull is its own ally's. Each of these makes the AI switch less often, never attempt an illegal switch.

It also returns "no switch" if there is no Pokemon to switch to (lines 3915 to 3940). A candidate is a party Pokemon with HP above 0 that is not an egg, not either active Pokemon on the AI's side, and not a Pokemon the AI's other battler has already chosen to switch in this turn. In a tag or multi battle, where each trainer has a separate party, only the battler's own active Pokemon is excluded.

### The rules, in order

Then the rules run in this order, and the first to give an answer decides. "Per move" below means each of a bench Pokemon's moves is tried in turn with its own random roll, going through the party in order, and the first roll that succeeds picks that Pokemon; so a bench Pokemon with two qualifying moves has two chances.

| Order | Rule | Lines | Condition | Chance | Result |
|---|---|---|---|---|---|
| 1 | Perish Song | 3263 to 3272 | the Perish Song count is 0, so the Pokemon faints at the end of this turn | certain | switch, replacement chosen as after a faint |
| 2 | Wonder Guard | 3286 to 3350 | singles only; the foe has Wonder Guard and none of our moves is super-effective on it | 2 in 3 per super-effective move on a bench Pokemon | switch to that Pokemon |
| 3 | Nothing can hit | 3361 to 3546 | every damaging move we know has no effect on every living foe, and we know at least two damaging moves | super-effective: 2 in 3 per move per foe; then neutral: 1 in 2 per move per foe | switch to that Pokemon |
| 4 | Absorbing ability | 3640 to 3714 | last hit by a damaging Fire, Water or Electric move; our ability does not absorb it; a bench Pokemon has Flash Fire, Water Absorb or Volt Absorb to match | skipped 2 in 3 of the time if we have a super-effective move; then 1 in 2 per matching bench Pokemon | switch to that Pokemon |
| 5 | Natural Cure | 3817 to 3859 | asleep, has Natural Cure, at least half HP | see the Natural Cure table | switch |
| gate | we can hit hard | 3560 to 3624 | we have a super-effective move on a foe | 9 in 10 per such move and foe | stop: no switch |
| gate | we are boosted | 3872 to 3884 | our positive stat stages add up to 4 or more | certain | stop: no switch |
| 6 | Immune switch-in | 3727 to 3807 | last hit by a damaging move; a bench Pokemon is immune to it and has a super-effective move on the attacker | 1 in 2 per super-effective move | switch to that Pokemon |
| 7 | Resisting switch-in | 3727 to 3807 | as rule 6, but the bench Pokemon resists the move | 1 in 3 per super-effective move | switch to that Pokemon |
| end | | 3986 | none of the above | | no switch |

What "last hit by" means. Rules 4 to 7 read `moveHit`, which the controller sets to the move used against a battler when that move's attack message is shown (`battle_controller_player.c` line 4527), and clears when the battler finishes its own action (line 4416) and when it switches in. So at the start of a turn it holds a move only if the Pokemon was attacked after it last acted: it moved first last turn and was then hit, or it was hit by a second foe in doubles after acting. A slower AI Pokemon has usually had it cleared, and rules 4, 6 and 7 then cannot fire.

What "super-effective" and "no effect" mean. The active Pokemon's own moves are checked with `BattleSystem_ApplyTypeChart`, the same function the damage figure uses, so status moves never count as super-effective there. Bench Pokemon are checked with `BattleSystem_CalcEffectiveness` (`battle_lib.c` line 2699), which looks only at types, Levitate, Iron Ball, Gravity, Scrappy, Mold Breaker and Wonder Guard, and does not check power; rules 2, 6 and 7 therefore count a bench Pokemon's status move of the right type as a super-effective move (bug 9). Both functions have the "dual non-immunity" quirk, bug 10.

### Rule by rule

Rule 1, Perish Song (lines 3263 to 3272). When the battler is under Perish Song and its count is 0, it switches, and the replacement is chosen the same way as after a faint. The count is set to 3 when Perish Song is used and falls by one at each end of turn, and the Pokemon faints at the end of the turn that starts with the count at 0 (`battle_controller_player.c` lines 1800 to 1809). So the test catches exactly the last turn. The comment above the function (lines 3255 to 3257) says the routine is bugged and never fires; that comment is wrong, and pokemow's description of this rule is right.

Rule 2, Wonder Guard (lines 3286 to 3350). Skipped in any double battle. If the foe directly opposite has Wonder Guard, and none of the active Pokemon's moves is super-effective on it, the AI looks through the party in order for a Pokemon with a super-effective move and switches to it with a 2 in 3 chance for each such move. Two effects hide inside "super-effective" here. Moves on their charging turn (SolarBeam, Fly, Dig and the others in `MoveIsOnDamagingTurn`, plus Fire Fang in vanilla) are never treated as blocked by Wonder Guard, because the flag that marks a second turn is always clear when the AI thinks. And a bench status move counts (bug 9).

Rule 3, nothing can hit (lines 3361 to 3546). First the active Pokemon's damaging moves are tested against each foe (both foes in doubles, the one foe twice in singles). If any damaging move is not marked "no effect" against any foe, there is no switch. Only type immunity sets "no effect" here: `ApplyTypeChart` marks Levitate, Magnet Rise and Wonder Guard with other flags, so a Pokemon whose only moves are Ground moves against a Levitating foe is not stuck by this rule's reckoning. If the active Pokemon knows fewer than two damaging moves, there is no switch either (line 3413; the comment there says the opposite of what the code does). Then the bench is searched twice. The first pass looks for a damaging move that is super-effective on a foe and takes it with a 2 in 3 chance per move per foe; the second pass, if the first found nothing, looks for a damaging move that is exactly neutral (no effectiveness flag at all, so a resisted move does not qualify) and takes it with a 1 in 2 chance per move per foe. In singles the one foe is tested twice (lines 3378 to 3379), so each qualifying move gets two rolls:

| Battle | Super-effective move on one foe | Super-effective on both foes | Neutral on one foe | Neutral on both |
|---|---|---|---|---|
| singles | 8 in 9 per move | n/a | 3 in 4 per move | n/a |
| doubles | 2 in 3 per move | 8 in 9 per move | 1 in 2 per move | 3 in 4 per move |

Rule 4, absorbing ability (lines 3640 to 3714). First, if the active Pokemon has any super-effective move on a foe (the gate function with its randomness turned off, line 3651), the rule is skipped with a 2 in 3 chance. Then it needs the last move that hit to be damaging and, by its listed type, Fire, Water or Electric, which picks Flash Fire, Water Absorb or Volt Absorb. If the active Pokemon has that ability already there is no switch. Otherwise each bench Pokemon with that ability is taken with a 1 in 2 chance. Motor Drive and Dry Skin, both in Platinum, are not considered, and the move's listed type is used rather than the type it actually had (Weather Ball, Hidden Power and Judgment are read as Normal).

Rule 5, Natural Cure (lines 3817 to 3859). It needs the battler asleep, with Natural Cure, and at or above half its maximum HP. Then:

| What last hit it | Lines | Chance to switch | Replacement |
|---|---|---|---|
| nothing since it last acted | 3828 to 3856 | 7 in 8 (three separate 1 in 2 rolls) | as after a faint |
| a status move | 3835 to 3856 | 3 in 4 (two 1 in 2 rolls) | as after a faint |
| a damaging move, and a bench Pokemon is immune to it and has a super-effective move on the attacker | 3842 | certain | that Pokemon |
| a damaging move, and a bench Pokemon resists it and has a super-effective move on the attacker | 3848 | certain | that Pokemon |
| a damaging move, neither of the above | 3853 to 3856 | 1 in 2 | as after a faint |

The first row is 7 in 8 rather than the 1 in 2 the code's structure suggests, because when the first roll fails the "status move" test runs next on the empty move, whose listed power is 0, and passes (bug 12). The two "certain" rows pass a chance of 1 to the helper, and `% 1 == 0` is always true; the comments at lines 3840 and 3846 say 50%.

The first gate, we can hit hard (lines 3560 to 3624, called at 3964). It looks at the foe directly across first, then in doubles at that foe's partner, skipping a foe that is already switching out this turn. For each of the active Pokemon's moves that is super-effective on that foe, it stops the switch with a 9 in 10 chance. So one super-effective move blocks rules 6 and 7 nine times in ten, two block them 99 times in a hundred.

The second gate, we are boosted (lines 3872 to 3884, called at 3969). It adds up every stage above neutral across all stats, accuracy and evasion included, and stops the switch at 4 or more. Lowered stats do not subtract.

Rules 6 and 7, immune or resisting switch-in (lines 3727 to 3807, called at 3975 and 3981). Both need the last move that hit to be a damaging move from a known battler. For each bench Pokemon in order, the AI checks that move against the bench Pokemon's types, ability and held item. Rule 6 wants "no effect", rule 7 wants "not very effective". If it matches, each of that Pokemon's moves that is super-effective on the battler that used the move gets a roll: 1 in 2 for rule 6, 1 in 3 for rule 7. The comments at lines 3973 and 3979 say 33% and 25% and describe both as immunity; the code gives 50% and 33% and the second is resistance. The attacker whose weakness is checked is whoever used the move, which in doubles can be the AI's own partner (bug 11).

## Choosing the Pokemon that comes in

There are two routes. When a switch rule names a Pokemon (rules 2, 3, 4, 6, 7 and two rows of rule 5), that slot is stored in `aiSwitchedPartySlot` and used as it is. When the rule stores 6 instead (rule 1, and the "as after a faint" rows of rule 5), `TrainerAI_PickCommand` runs the post-faint routine at once (line 4005) and stores its answer. After a faint or a U-turn, `Task_TrainerShowPartyMenu` (`battle_display.c` lines 4528 to 4562) reads the stored slot, which the controller resets to 6 after every action (`battle_lib.c` line 2015), and so runs the post-faint routine too.

### The post-faint routine

`BattleAI_PostKOSwitchIn` (`battle_lib.c` lines 7994 to 8160, vanilla 7923 to 8089) first picks one foe at random as the target (line 8020). Candidates are the same as for switching: alive, not an egg, not already active, not already chosen this turn.

Stage 1, best type match with a super-effective move (lines 8030 to 8099). Each candidate gets a score from its own types against the target's types, using the type chart: for each of the candidate's two types, start at 40 and multiply by the chart's factor for each of the target's types. A single-typed Pokemon has its type counted twice.

| Candidate type against the target | Score for that type |
|---|---|
| 4 times | 160 |
| 2 times | 80 |
| neutral | 40 |
| half | 20 |
| quarter | 10 |
| no effect | 0 |

The two scores are added and stored in a single byte (line 8003), so a total of 320 (both types, or one type counted twice, 4 times effective) wraps to 64 and ranks below a neutral dual type. No other total can wrap: the next highest is 240. The candidate with the highest total is chosen, the earlier party slot winning ties. If it has any move marked super-effective on the target (by `BattleSystem_CalcEffectiveness`, which counts status moves too), it comes in. If not, it is set aside and the next highest is tried, until none are left.

Stage 2, most damage (lines 8104 to 8159). Each candidate's moves are scored by damage against the target, using `BattleSystem_CalcMoveDamage` and then `ApplyTypeChart`, and the highest wins, the earlier slot winning ties. Four details change the answer. The attacker in that calculation is the AI's battler slot, which still holds the Pokemon that just fainted (or, for a Perish Song or Natural Cure switch, the Pokemon about to leave), so the stats, ability, item and same-type bonus are that Pokemon's, not the candidate's: only the candidate's move list matters. The damage is stored in a single byte after each of the two calls, so it wraps at 256 twice. A move of power 1 or an empty slot does not reset the score, so it inherits the previous move's figure. And status moves (power 0) are not skipped; the formula's constant +2 gives them a small score.

If neither stage finds anyone the routine returns 6, and a plain fallback takes the first party slot with HP above 0 that is not active. There are two copies of that fallback: `TrainerAI_PickCommand` lines 4006 to 4024 for a voluntary switch, and `battle_display.c` lines 4549 to 4557 after a faint. Stage 2 almost never leaves it that far, since any candidate with any move scores above 0 unless every move is blocked by immunity.

## Items

### What this means in Oxide today

Oxide took items out of trainer battles on purpose. Vanilla's `BattleControllerPlayer_InitAI` copied each opposing trainer's items into `trainerItems` and counted them in `trainerItemCounts` (vanilla `battle_controller_player.c` lines 4801 to 4813). Oxide's version (lines 4823 to 4835) only clears the AI context and points it at the script, so both arrays stay at zero for the whole battle, and nothing else in the tree writes to them.

`TrainerAI_ShouldUseItem` still runs every turn the AI does not switch, and always returns "no item". Slot 0 is always examined and is empty, so it is skipped (line 4095). Slots 1 to 3 are only examined when the number of living party Pokemon is at most `trainerItemCounts` minus the slot number plus 1 (line 4092), which with a count of 0 is 0 or less, and in any case they are empty too. The one thing the call still does is reset `usedItemCondition` (line 4066), which only the unreachable item command reads. The AI branch of `BattleControllerPlayer_ItemCommand` (lines 1905 to 1945) is therefore unreachable in trainer battles. So in Oxide a trainer's turn is a switch or a move, and the item rules below, including bugs 19 and 20, have no effect unless trainer items are turned back on.

### What the routine would do if items came back

For the record, since a later element might restore items. Items are held per side of the field for the opponent (`battler >> 1`), up to 4 (`MAX_TRAINER_ITEMS`). The routine never uses an item for an AI partner in a battle with one (lines 4070 to 4073), nor under Embargo (4076 to 4078). It counts living party Pokemon, then walks the four item slots. Slot 0 is always open; slot `i` is open only when the living count is at most the number of items minus `i` plus 1, which rations later items for later in the fight:

| Items held | Slot 1 open when alive at most | Slot 2 | Slot 3 |
|---|---|---|---|
| 2 | 2 | | |
| 3 | 3 | 2 | |
| 4 | 4 | 3 | 2 |

For each open, non-empty slot it tests the item in this order, and the first matching kind decides:

| Item | Lines | Used when |
|---|---|---|
| Full Restore (by item id) | 4099 to 4104 | HP below a quarter and above 0 |
| any HP-restoring item | 4105 to 4117 | HP above 0, and HP below a quarter or HP missing more than the item restores |
| heals sleep | 4118 to 4123 | asleep |
| heals poison | 4124 to 4130 | poisoned or badly poisoned |
| heals burn | 4131 to 4136 | burned |
| heals freeze | 4137 to 4142 | frozen |
| heals paralysis | 4143 to 4148 | paralysed |
| heals confusion | 4149 to 4154 | confused |
| X items and Guard Spec. | 4156 to 4185 | only on the Pokemon's first turn in play (the comment at 4155 says the opposite); Guard Spec. only without Mist on the opposing side |

## Cross-check with the references

pokemow's switching page (https://pokemow.com/Gen4/TrainerAI/switching.html) against the code, rule by rule. The code is the ground truth.

| Rule | pokemow says | The code | Agree |
|---|---|---|---|
| trapping | opposing Shadow Tag, Arena Trap, Magnet Pull on Steel; ignores Shed Shell and the Flying and Levitate exemptions | the same, except Magnet Pull on any other battler including the AI's own ally, and an own Shadow Tag is not an exemption | mostly |
| 1 Perish Song | guaranteed switch when the count will reach 0 at the end of the turn | the same | yes |
| 2 Wonder Guard | skipped in doubles; 66.6% for each matching Pokemon | 2 in 3 for each super-effective move, so a Pokemon with two such moves is taken 8 in 9 | chance per move, not per Pokemon |
| 3 nothing can hit | at least two damaging moves; singles 88.8% and 75%, doubles 66.6% or 88.8% and 50% or 75% | the same figures, per move rather than per Pokemon; the second pass needs an exactly neutral move, not any damaging one | mostly |
| 4 absorbing ability | 66.6% skip if a super-effective move, then 50% per Pokemon | the same | yes |
| 5 Natural Cure, not hit | 50% | 7 in 8 | no |
| 5 Natural Cure, hit by a status move | not separated | 3 in 4 | not covered |
| 5 Natural Cure, immune or resisting Pokemon | guaranteed | guaranteed | yes |
| gate | skipped if the Pokemon can hit a foe super-effectively | skipped 9 in 10 per super-effective move and foe | close |
| gate | 4 or more positive boosts | the same | yes |
| 6 immune | 50% per Pokemon | 1 in 2 per super-effective move | chance per move |
| 7 resisting | 33.3% per Pokemon | 1 in 3 per super-effective move | chance per move |
| after a faint, phase 1 | type scores 160 to 0, single types counted twice, 320 wraps to 64, ties to the front | the same | yes |
| after a faint, phase 2 | most damage, variable-type moves at base type with corrected effectiveness, wraps at 255 to 0 | the same, and also: the attacker is the fainted Pokemon, not the candidate; a power-1 move inherits the previous score; status moves score 2 or so | partly |
| after a faint, fallback | first Pokemon able to switch in | the same | yes |
| effectiveness quirk | the dual non-immunity glitch (Gligar weak to Electric, Skarmory and Aerodactyl to Ground, Girafarig to Ghost) | present in both effectiveness functions, bug 10 | yes |
| allied battles | rule 3 treats the player's side as the foe | the same, bug 8 | yes |

pokemow's main page lists the moves the AI treats as doing 0 damage. The code agrees: its list is the first table above plus every power-1 move not in the second table. It also says random variance is left out of the AI's damage, which matches the code as the script uses it. It lists Filter, Solid Rock, Expert Belt and Tinted Lens among the factors removed; in this code they are applied, by `ApplyTypeChart` in step 2 of the damage figure, so on that point the page and the code disagree.

lhearachel's gist covers move scoring only; it says nothing about switching, replacements or items. Its list of effects "never regarded for damage-calculation" merges the two tables above. In the C, the second table's moves are calculated, with their special power; whether the script ever asks for them is the script's business and is covered in the flag part files.

The pret file `docs/bugs_and_glitches.md` gives the stage 1 wrap as 65. The arithmetic (320 minus 256) gives 64, as pokemow says.

## Apparent bugs

Fixed on 2026-09-22: bug 1, Weather Ball's unset type (vanilla fix, approved by Ian), in all three helpers; the compiled code showed each returned its caller's register, a pointer. Also fixed, and missed by this write-up: `TrainerAI_CalcDamage` has no Weather Ball case, so the AI always estimated it as a 50-power Normal move (vanilla; Ian's pokemow reference names it). The ability byte (Oxide) is fixed in another part. Otherwise nothing in this file's code has been changed; status moves counting as super-effective and the bench damage check were put to Ian and kept as vanilla has them.

Each entry is labelled as present in vanilla Platinum or introduced by Oxide. A fix to a vanilla bug changes the game's original behaviour and is Ian's call; none has been made.

1. **Weather Ball's type is unset with no weather.** Present in vanilla (`trainer_ai.c` 3222 to 3240; `battle_lib.c` vanilla 8176, Oxide 8247). Both type helpers assign Weather Ball's type only inside the weather tests, and neither sets it first, so with clear skies or Cloud Nine or Air Lock out the function returns whatever the register held. Every other case in both functions sets a type, including a default of Normal. What the compiled code returns cannot be read from the source. It affects the switching checks and the replacement routine when a Pokemon knows Weather Ball.
2. **Magnitude is always scored as 0 damage.** Present in vanilla (lines 3028 to 3049, the same in vanilla). The special case can never be reached, because Magnitude's effect is in neither table and its power is 1. Evidence that it was meant to run: the branch simulates the Magnitude roll in full.
3. **The per-move damage rolls are drawn but never used.** Present in vanilla (line 240 draws them; `script.s` has 18 damage calls, all `USE_MAX_DAMAGE`, in vanilla and Oxide alike). The C supports rolled damage everywhere, and the script never asks for it. Whether this was a design choice or an oversight cannot be told from the code, but any change to the script's argument would change every damage comparison at once.
4. **Rule 3 rolls twice in singles.** Present in vanilla (lines 3378 to 3379 with 3459 to 3479 and 3518 to 3538). In singles the second foe is set to the first, so each move's roll happens twice and the chances are 8 in 9 and 3 in 4, not the 66% and 50% the comments at 3429 and 3489 state.
5. **Rule 3 never fires in doubles when one foe slot is empty.** Present in vanilla (lines 3393 to 3408). A fainted foe is skipped, which leaves its effectiveness at 0, which the test reads as "this move can hit". So a Pokemon with only immune moves against the one remaining foe never switches by this rule.
6. **The gate does not check whether a foe has fainted.** Present in vanilla (lines 3574 to 3621). In doubles with one foe slot left empty, the fainted Pokemon's data is still there and a move super-effective on it still blocks rules 6 and 7.
7. **The AI's trap test is stricter than the engine's.** Present in vanilla (lines 3906 to 3913; engine `battle_lib.c` 5538, vanilla 5514). Shed Shell, an own Shadow Tag, Flying, Levitate or Magnet Rise against Arena Trap, and an ally's Magnet Pull all leave the AI thinking it is trapped. The comment at 3902 to 3905 acknowledges this.
8. **Rule 3 checks the wrong side for an AI partner.** Present in vanilla (lines 3374 to 3380). The foes are hard-coded as the player's two battlers, so an AI partner on the player's side tests its moves against itself and its ally.
9. **Bench checks count status moves as super-effective.** Present in vanilla (rule 2 lines 3322 to 3343; rules 5, 6, 7 lines 3780 to 3800; replacement stage 1 `battle_lib.c` 8066 to 8087, vanilla 7995 to 8016). `BattleSystem_CalcEffectiveness` does not look at power. Rule 3 checks power explicitly (lines 3445 and 3504), which shows the intent. So a bench Pokemon whose only Fire move is Will-O-Wisp is treated as a counter to Shedinja, and a Thunder Wave user as a counter to a Water type.
10. **Immune then super-effective reads as super-effective.** Present in vanilla (`battle_lib.c` 2799 to 2824 and 7613 to 7646, vanilla 2781 and 7542). When a move's type chart entry for one of the target's types is an immunity and a later entry is super-effective, the later one sets the super-effective flag without clearing "no effect". The switching checks look for the super-effective flag and so see Electric as super-effective on Gligar, Ground on Skarmory and Aerodactyl, and Ghost on Girafarig. Oxide's Fairy rows come after the whole vanilla chart, which gives one new case: Poison is immune on Steel in the vanilla rows and super-effective on Fairy in the Fairy rows, so the switching checks read Poison as super-effective on Oxide's Steel and Fairy Pokemon (Mawile, Klefki, Magearna). The Dragon immunity to Fairy comes last and is read correctly.
11. **Rules 6 and 7 can pick a counter to the AI's own partner.** Present in vanilla (lines 3737 and 3786 to 3794). The battler whose weakness is checked is whoever used the last move on the AI's Pokemon, and in doubles that can be its ally (Earthquake, Surf).
12. **Natural Cure switches 7 in 8 when not hit, not 1 in 2.** Present in vanilla (lines 3828 to 3856). The "status move" test at 3835 reads the power of the empty move, 0, and passes, and the final fallback rolls again.
13. **The replacement type score wraps at 320.** Present in vanilla (`battle_lib.c` 8003, vanilla 7933, already marked `BUG` in the source). A 4 times matchup on both types scores 64.
14. **The replacement damage score wraps at 256, twice.** Present in vanilla (`battle_lib.c` 8125 to 8144, vanilla 8054 to 8073). The engine's damage is cut to one byte before the type chart is applied and again after.
15. **The replacement damage uses the fainted Pokemon as the attacker.** Present in vanilla (`battle_lib.c` 8125 to 8134, vanilla 8054 to 8063). The routine works out each candidate's move type from the candidate, which shows it meant to judge the candidate's damage, but passes the AI's battler slot as the attacker.
16. **A skipped move keeps the last score.** Present in vanilla (`battle_lib.c` 8121 to 8154, vanilla 8050 to 8083). When a slot is empty or the move's power is 1, `score` is not reset, so the previous move's figure (or, for the very first move, a leftover stage 1 type score or an uninitialised value) is compared again for this candidate.
17. **The absorbing-ability rule reads the listed type.** Present in vanilla (line 3665). The controller records the type the move actually had (`moveHitType`), but the rule reads the move's data, so a Fire-type Weather Ball, Hidden Power or Judgment does not count.
18. **Several comments misstate the code.** Present in vanilla. Lines 3255 to 3257 (Perish Song "does nothing"; it works), 3412 ("more than 1 attacking move, do not switch"; it is fewer than 2), 3840 and 3846 (50%; certain), 3973 and 3979 (33% and 25%, both "immunity"; 50% and 33%, immunity and resistance), 4155 ("until after the first turn"; only on the first turn). These do not change behaviour, but they will mislead anyone editing the code.
19. **Using one item empties every later open item slot.** Present in vanilla (lines 4091 to 4196). There is no `break` after an item is chosen, and `result` stays true, so every later open, non-empty slot is also cleared, and `usedItem` ends as the last of them. With two Full Restores and one Pokemon left, both go at once and the message names the second. No effect in Oxide, since trainers have no items.
20. **A multi-status heal is only used for sleep.** Present in vanilla (lines 4118 to 4154). The tests are one `else if` chain, so an item that heals every status (Full Heal) matches the sleep test first and is used only when asleep. No effect in Oxide.
21. **The AI's record of a revealed ability is one byte.** Introduced by Oxide. This one is outside this file's lines, in the script-command side, but it is the one place an ability is still held in a `u8`: `AIContext.battlerAbilities` (`include/battle/ai_context.h` line 28) is filled by `BattleAI_SetAbility`, which now takes a `u16` (`battle_script.c` lines 12176 to 12179), and read by `AICmd_LoadBattlerAbility` and `AICmd_CheckBattlerAbility` (`trainer_ai.c` lines 1181 and 1225). An announced ability numbered 256 or above is stored as its number minus 256, and an ability numbered exactly 256 is stored as 0, which those commands read as "not yet known". In vanilla no ability was above 123.

## The battle_edits fixes

None of the eleven lives in `trainer_ai.c` from line 2750 to the end.

Fire Fang vs Wonder Guard is in `battle_lib.c`, in `MoveIsOnDamagingTurn` (line 7671, vanilla 7600), where the effect for Fire Fang (273) sits in the list of two-turn moves instead of Shadow Force's (272), one number away. The switching logic here meets it through `ApplyTypeChart` and `CalcEffectiveness`, which both skip the Wonder Guard test for moves in that list when the "last turn of a two-turn move" flag is clear, and that flag is always clear when the AI decides (it is reset after every action). So today the AI's switching and damage checks never see Wonder Guard block Fire Fang, SolarBeam, Fly and the rest of that list, and do see it block Shadow Force and Oxide's Phantom Force. After the fix Fire Fang is judged like an ordinary move and Shadow Force and Phantom Force join the unblocked list. In practice the AI change is almost nil: Shedinja is the only Wonder Guard Pokemon and Fire is super-effective on it anyway, so Fire Fang only differs against a Pokemon that gained Wonder Guard through Skill Swap or Role Play.

Rage Glitch is in `battle_controller_player.c` line 846 (the same in vanilla), where `&= VOLATILE_CONDITION_RAGE` should be `&= ~VOLATILE_CONDITION_RAGE`. Nothing in this file's lines reads the Rage bit.

The other nine are script fixes, named for the flag routine they sit in (Basic: Water immunity vs Dry Skin, Sunny Day; Expert: Foresight and Odor Sleuth, Facade, Leaf Guard, Water Spout and Eruption, charge turns, Thunder; Tag Strategy: Discharge). They belong to the flag part files. Two touch this file's tables indirectly: Water Spout and Eruption, and the charge-turn moves, are in the "no damage calculation" table, which is why the script has to score them by hand. The Dry Skin fix is in the script's Basic flag; the C absorbing-ability rule (rule 4) also ignores Dry Skin and Motor Drive, but that is a separate gap and not part of the list.

## What Oxide's new content does here

### Keyed on move effect ids

Both effect tables are `u16` lists ended by `0xFFFF`, so ids up to 406 fit. New moves that share a vanilla effect behave like their vanilla sibling: Misty Explosion, Eternabeam, Meteor Assault, Prismatic Laser, Solar Blade, Dragon Energy, Thunderclap and Light of Ruin are all left out of the damage calculation, as the table shows. None of Oxide's new effects (277 to 406) is in either table, which means:

| Effect | Moves | What the AI does |
|---|---|---|
| 324, 325, 363, 364 (charge turn) | Meteor Beam, Electro Shot, Freeze Shock, Ice Burn | calculates full damage as if it hit this turn, where SolarBeam and Skull Bash are left out |
| 272 (Shadow Force, vanilla too) | Phantom Force | calculates full damage |
| 403 (recoil half max HP) | Chloroblast | calculates full damage, where Head Smash is left out |
| 402 (Final Gambit), 292 (Heavy Slam) | Final Gambit, Heavy Slam, Heat Crash | 0 damage, power 1 |
| 0 (plain hit) with power 1 or 0 | Electro Ball, Hard Press | 0 damage |
| 121 (friendship) | Pika Papow, Veevee Volley | passes the gate but falls to the default path, where the listed power of 0 gives the formula's constant, about 2 damage |
| 280, 287, 289, 321, 322, 382, 388 and plain hits whose power varies | Venoshock, Hex, Acrobatics, Infernal Parade, Barb Barrage, Bolt Beak, Fishious Rend, Fell Stinger, Stored Power, Power Trip, Last Respects, Rage Fist and the like | listed base power only, since the doubling or scaling is done in the battle script |
| multi-hit effects 297 to 299, 366 | Population Bomb, Triple Axel, Triple Dive, Surging Strikes | one hit's damage |

Mind Blown and Steel Beam carry the plain-hit effect in the move data, so the AI and the engine both treat them as ordinary 150 and 140 power moves; that is a move-data question for element 4.

### Keyed on move ids

`TrainerAI_CalcDamage` and both type helpers switch on move ids. Techno Blast, Multi-Attack, Revelation Dance and any other move whose type depends on an item or the user are read at their listed type. Judgment has no Pixie Plate case, so if Oxide adds one, a Fairy Judgment is read as Normal in three places (lines 2901 to 2969, 3137 to 3205, and `Move_CalcVariableType`). Weather Ball only knows rain, sand, sun and hail. Hidden Power's formula (lines 2980 to 2992) gives types 1 to 17 skipping the unused type 9, so it can never be Fairy, which matches later generations.

### Keyed on types

Fairy (18) works wherever the type chart is used, because every effectiveness check and the replacement type score walk the same chart, where the Fairy rows now sit. Types are held in `u8`s throughout, which is enough.

### Keyed on ability ids

The switching logic names abilities directly: Klutz (2886, 2898), Wonder Guard (3298), Flash Fire, Water Absorb and Volt Absorb (3666 to 3671), Natural Cure (3821), Shadow Tag, Arena Trap and Magnet Pull (3908 to 3911). The engine helpers it calls add Normalize, Levitate, Scrappy, Mold Breaker, Filter, Solid Rock, Tinted Lens and Adaptability. The one `u8` that held an ability in these lines, in rule 4, was widened by Oxide (lines 3645 to 3646) and is correct. New abilities the logic does not know, and what that means:

| Ability | Effect on these routines |
|---|---|
| Storm Drain, Lightning Rod, Sap Sipper, Earth Eater, Well-Baked Body (and vanilla's Motor Drive, Dry Skin) | not seen as immunities by any switching check, and not considered by rule 4 |
| Teravolt, Turboblaze | `CalcEffectiveness` tests for Mold Breaker by id, so these do not ignore Levitate or Wonder Guard in the bench checks |
| Pixilate, Aerilate, Refrigerate, Galvanize, Liquid Voice | the type helpers know only Normalize, so the AI reads the move's listed type |
| Regenerator | no switch rule for it |

### Fixed sizes

`MAX_TRAINER_ITEMS` is 4. The replacement routine marks party slots in a 6-bit mask (`0x3F`) and uses 6 as "none", which still fits Oxide's party size. `AIContext.moveTable` is sized by `MAX_MOVES`, so it grows with the move count. The new trapping moves (Anchor Shot, Spirit Shackle, Thousand Waves, Jaw Lock, Octolock, Fairy Lock) are only seen by the AI's trap test if their engine code sets the bound or Mean Look status; that depends on how element 4 implemented them.

### Where the held items would plug in

None of these items exists in the tree yet. Where each would reach the decisions described here:

| Item | Where it reaches this logic |
|---|---|
| Air Balloon | Ground immunity. For the damage figure and the active Pokemon's checks, beside Levitate in `ApplyTypeChart` (`battle_lib.c` 2617 to 2620); for bench checks and replacements, beside Levitate in `CalcEffectiveness` (2717 to 2722), which already receives the defender's item effect. Note that `ApplyTypeChart` marks Levitate with its own flag, not "no effect", so rule 3 would not count a balloon immunity unless it is marked the same way. |
| Eviolite, Assault Vest | defensive stat changes. If added to `BattleSystem_CalcMoveDamage`, the AI's damage figure and the replacement stage 2 pick them up with no AI change. Assault Vest's ban on status moves belongs to the invalid-move check in `TrainerAI_Init`, not here. |
| Rocky Helmet | no effect on damage or switching; a contact-move penalty would be a script scoring rule. |
| Weakness Policy | no effect on the figure; avoiding a super-effective hit on the holder would be a script rule. The switching gates count super-effective moves and would not know to avoid them. |
| the seeds | they raise stats when a terrain starts; the stat-boost gate (3872 to 3884) counts the stages once they are raised, and anything more is script. |
| Shed Shell (vanilla item) | the AI's trap test at 3906 to 3913 is where an exemption would go, matching the engine's `Battler_IsTrapped`. |
