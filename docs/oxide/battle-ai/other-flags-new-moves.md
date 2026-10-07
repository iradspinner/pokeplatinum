# The new moves in the other flags

Ian's ruling of 2026-10-07 (alpha readiness, step 18) carries the Expert pass of 2026-09-27 ([expert-new-moves.md](expert-new-moves.md)) over to the nine flags beyond Basic and Expert, which [other-flags.md](other-flags.md) describes. Each learnable move past Platinum's 467 is routed in each flag the way its nearest Platinum effect is routed there, judged by what its effect script does. Where that effect is on a flag's list, the new move or its effect now sits beside it; where Platinum gives its equivalents nothing, the new move gets nothing. This is routing only: no flag gained a test, a score or a routine. It is a change of play, marked in `src/battle/trainer_ai/script.s` as "Oxide, change (Ian, 2026-10-07, the other flags' routing)".

It acts only once trainers carry these moves. No trainer in the tree has any of the 21 routed moves today, by hand or through default moves (checked on 2026-10-07 against `res/trainers/data/` with the move pool survey's reading), so the ROM plays the same until the trainer pass gives them out.

A move counts as learnable when any species' or form's level, TM, tutor or egg list has it, read by `tools/oxide/move_pool_survey.py` on `balance-tm-pass` after the learnset rewrite: 165 moves, against the Expert pass's 156, since the rewrite made 27 learnable that were not and took 18 out. The nearest Platinum effect is the one the Expert pass and element 6 chose wherever they chose one, read from Expert's dispatch, so that the scoring track's simulator can use one mapping for every flag. The appendix gives it for all 165. A flag that lists effects routes every move on an added effect, learnable or not; none of the 20 added effects carries a move that is not learnable.

| Flag | Newly routed | Already reached, by a Platinum effect or an earlier pass | Commit |
|---|---|---|---|
| Evaluate Attack | Final Gambit | Accelerock | 05f668d029 |
| Setup First Turn | Hone Claws, Coil, Cotton Guard, Autotomize, Noble Roar, Tearful Look, Aurora Veil | Play Nice, Baby-Doll Eyes, Eerie Impulse, Shelter | d7f78a8014 |
| Risky | Final Gambit | Drill Run, Aqua Cutter | 7d4744b142 |
| Prioritize Extremes | none: it has no list of its own | every status move, Heavy Slam, Final Gambit, Nature's Madness | none |
| Baton Pass | Quiver Dance, Shift Gear, Shell Smash, Geomancy, Clangorous Soul | none | c89b37dce0 |
| Tag Strategy | none | the seven spread moves of 2026-09-27; Accelerock | none |
| Check HP | 18 moves, listed below | Play Nice, Baby-Doll Eyes, Eerie Impulse, Shelter, Shore Up, Nature's Madness | a556685571 |
| Weather | none | none | none |
| Harassment | Noble Roar, Tearful Look, Venom Drench, Sticky Web, Magic Room | Play Nice, Baby-Doll Eyes | 5a5e3a5646 |

Every learnable new move not named in a flag's section below gets nothing from that flag, because its nearest Platinum effect gets nothing there.

## Judgment calls

Each of these departs from a plain reading of the rule, and each is Ian's to reverse.

Three of Ian's eleven Expert judgment calls of 2026-09-27 are routed here, because the flags in question do not read what made Expert's routines misjudge them. Final Gambit follows Explosion in Evaluate Attack, Risky and Check HP's target-low table: those treat it as a sacrifice that is wasted when it does not knock out, which fits. It stays out of Check HP's attacker-high and attacker-medium tables, which hold Explosion back until its user is hurt, the opposite of what Final Gambit wants, since its damage is its user's HP. Guard Split and Power Split follow Guard Swap and Power Swap into Check HP's attacker-medium table, which only holds a stat move back at middling HP. Their Expert routines stay as Ian left them, and the other eight judgment calls get nothing here either: Laser Focus, because its two candidates (Focus Energy and Lock-On) sit in different tables; Wonder Room, Salt Cure and Core Enforcer, whose Platinum candidates (Trick Room, Bind, Gastro Acid) are on no list these flags read for a move aimed at a foe; and Wide Guard, Quick Guard, Mat Block and Crafty Shield, below.

Eight moves get nothing although their nearest effect is listed, because the list's reason does not hold for them. Venom Drench stays out of Setup First Turn, which acts only on the battle's first turn, when its target is almost never poisoned and the move fails. Flower Trick follows Karate Chop but stays out of Risky, which rewards a gamble, and an always-critical hit is none. Heal Pulse and Pollen Puff follow Present but stay out of Risky, whose Present entry is the gamble that it may heal the foe: Heal Pulse aimed at a foe always heals it, and Pollen Puff aimed at a foe always hits. Wide Guard, Quick Guard, Mat Block and Crafty Shield share Protect's subscript but stay out of Baton Pass's Protect test, since none of them shields its user from a single-target attack the way Protect does before a pass.

Four choices follow the Expert mapping where another reading was possible. Quiver Dance, Shift Gear, Shell Smash, Geomancy and Clangorous Soul follow Dragon Dance, as Expert's dispatch sends them, so they get nothing from Setup First Turn, where Dragon Dance is absent and Calm Mind is not. Clangorous Soul could instead follow Belly Drum (stats for HP), which would put it in Risky and out of Baton Pass. Aurora Veil follows Reflect, so it gets Setup First Turn's bonus but nothing from Check HP, where Light Screen is in three tables and Reflect in none. Sticky Web follows Spikes, so it is in Harassment and not in Setup First Turn. Magic Room follows Embargo into Harassment, though it stops the AI's own held items as well as the target's.

## For Ian: what would need new behaviour

These were left unbuilt, as the job required, since each needs a test or a score no flag has.

- Tag Strategy aiming Heal Pulse, Pollen Puff, Coaching and After You at the partner. The partner pass forbids any move it has no case for, so the AI never uses these on its partner. Entrainment onto a Truant or Slow Start partner is the same: it follows Worry Seed, which the partner pass forbids, though Skill Swap's case would fit it.
- Rage Powder as Follow Me. It is on Follow Me's effect, but Tag Strategy names Follow Me by move id, and Rage Powder misses Grass types and Overcoat, which Follow Me's case does not test.
- Wide Guard, Quick Guard, Mat Block and Crafty Shield. No flag measures which moves each stops.
- Smack Down and Thousand Arrows in double battles. Expert scores them as Gravity, but Tag Strategy's Gravity case penalises the AI's own floating side, which Smack Down does not ground.
- The terrains and Snowscape. Neither is learnable today; Snowscape would need its own weather test in the Weather flag and Hail's rows in Tag Strategy, and the terrains are not in Oxide.
- Prioritize Extremes, two mismatches that sit in `trainer_ai.c`'s damage tables, which Basic, Expert and every flag share and which this pass left alone. Heavy Slam has power 1 and an effect on no table, so it gets the flag's +2, which Low Kick, its Platinum match, does not; and Meteor Beam is costed as an attack, so it misses the +2 that Skull Bash, its match, gets as a charge move.

## Evaluate Attack

Explosion's effect is tested twice: for the kill bonus, which it is denied, and for the 80% -2 when it does not kill. A move on the no-damage-calculation list or with power 1 never counts as a kill here, so only the second test can reach Final Gambit, and only that one names it.

| Move | Follows | What the flag does |
|---|---|---|
| Final Gambit | Explosion | -2 (80.1%), then the four-times check; routed |
| Accelerock | Quick Attack, its own effect | +6 for a kill; inherited |

## Setup First Turn

The table of effects that get +2 (68.75%) on the battle's first turn.

| Move | Follows | What the flag does |
|---|---|---|
| Hone Claws | Meditate | +2; routed |
| Coil | Harden | +2; routed |
| Cotton Guard | Harden | +2; routed |
| Autotomize | Agility | +2; routed |
| Noble Roar, Tearful Look | Growl | +2; routed |
| Aurora Veil | Reflect | +2; routed |
| Play Nice, Baby-Doll Eyes | Growl, their own effect | +2; inherited |
| Eerie Impulse | its own effect, Sp. Atk down two stages | +2; inherited |
| Shelter | Barrier, its own effect | +2; inherited |
| Venom Drench | Growl | none: it fails on the first turn (judgment calls) |
| Quiver Dance, Shift Gear, Shell Smash, Geomancy, Clangorous Soul | Dragon Dance | none, as Dragon Dance |
| Sticky Web | Spikes | none, as Spikes |
| Laser Focus | Focus Energy or Lock-On | none (judgment calls) |

## Risky

The table of effects that get +2 (50%) on any turn.

| Move | Follows | What the flag does |
|---|---|---|
| Final Gambit | Explosion | +2; routed |
| Drill Run, Aqua Cutter | Karate Chop, their own effect | +2; inherited |
| Flower Trick | Karate Chop | none: no chance involved (judgment calls) |
| Heal Pulse, Pollen Puff | Present | none (judgment calls) |
| Clangorous Soul | Dragon Dance | none, as Dragon Dance |

## Prioritize Extremes

The flag gives +2 (60.9%) to any move the damage comparison skips, and it reads no list in `script.s`: the comparison's own tables are in `trainer_ai.c` and shared with every flag. So no commit. A learnable new move gets the +2 when it is a status move, has power 1 and an effect outside the alternative-power table (Heavy Slam, Final Gambit, Nature's Madness), or has an effect on the no-damage-calculation table (Solar Blade, on SolarBeam's). Every other new attack is compared and gets nothing. Two of these disagree with their Platinum match, Heavy Slam and Meteor Beam, as the section for Ian says.

## Baton Pass

Baton Pass names its four boosting moves by move id; a move named there gets +5 on the battle's first turn, -10 later below 60% HP, else +1, where any other status move gets the flag's generic +3 and the same treatment after it (bug O2). Protect's effect is tested by effect, and no learnable new move is on it.

| Move | Follows | What the flag does |
|---|---|---|
| Quiver Dance, Shift Gear, Shell Smash, Geomancy, Clangorous Soul | Dragon Dance | Dragon Dance's case; routed |
| Wide Guard, Quick Guard, Mat Block, Crafty Shield | Protect | none: the generic status move case (judgment calls) |
| Coil, Cotton Guard, Hone Claws, Autotomize, Shelter | Harden, Meditate, Agility, Barrier | none, as their matches |

Protect's "used last turn" list names Protect and Detect by move id. King's Shield, Spiky Shield, Baneful Bunker, Obstruct, Silk Trap and Burning Bulwark, which share Protect's effect, are not learnable today; if one becomes learnable it belongs in that list.

## Tag Strategy

Every new spread move that hits the partner has had its partner case since 2026-09-27: Bulldoze as Earthquake, Mind Blown as Lava Plume, Sparkling Aria as Surf, and Brutal Swing, Boomburst, Sludge Wave and Petal Blizzard by the type chart, with Misty Explosion and Synchronoise, which are not learnable. The flag's special cases are named by move id, and no other learnable new move is a match for one of them, apart from those the section for Ian lists. Moves are placed in its Electric, Fire and Water rows, and the partner pass's Grass row, by their listed type, so the new moves of those types are already there. No commit.

| Move | Follows | What the flag does |
|---|---|---|
| Bulldoze, Mind Blown, Sparkling Aria, Brutal Swing, Boomburst, Sludge Wave, Petal Blizzard | Earthquake, Lava Plume, Surf, the type chart | partner checks (2026-09-27) |
| Accelerock | Quick Attack, its own effect | its +1 priority bonus (80.5%) as the strongest move; inherited |
| Rage Powder | Follow Me | none (for Ian) |
| Heal Pulse, Pollen Puff, Coaching, After You, Entrainment | Present, Helping Hand, Worry Seed | none on the partner pass (for Ian) |
| Smack Down, Thousand Arrows | Gravity | none (for Ian) |

## Check HP

Each table takes 80.5% -2 from a move whose effect it lists: three by the attacker's HP (above 70%, 31 to 70%, 30% or less) and two by the target's (31 to 70%, 30% or less; the target-high table is empty).

| Move | Follows | Attacker high | Attacker medium | Attacker low | Target medium | Target low |
|---|---|---|---|---|---|---|
| Hone Claws | Meditate | | routed | routed | routed | routed |
| Coil | Harden | | routed | routed | routed | routed |
| Cotton Guard | Harden | | routed | routed | routed | routed |
| Autotomize | Agility | | routed | routed | routed | routed |
| Noble Roar, Tearful Look | Growl | | routed | routed | routed | routed |
| Venom Drench | Growl | | routed | routed | routed | routed |
| Quiver Dance, Shift Gear, Shell Smash, Geomancy, Clangorous Soul | Dragon Dance | | routed | routed | routed | routed |
| Soak | Conversion 2 | | routed | routed | | routed |
| Guard Split | Guard Swap | | routed | | | |
| Power Split | Power Swap | | routed | | | |
| Strength Sap | Recover | routed | | | | |
| Life Dew | Recover | routed | | | | |
| Final Gambit | Explosion | none (judgment calls) | none (judgment calls) | | | routed |
| Play Nice, Baby-Doll Eyes, Eerie Impulse, Shelter | their own effects | | inherited | inherited | inherited | inherited |
| Shore Up | Morning Sun, its own effect | inherited | | | | |
| Nature's Madness | Super Fang, its own effect | | | | | inherited |

Aurora Veil gets nothing here, as Reflect, which is in no table, and Laser Focus nothing (judgment calls).

## Weather

The flag tests the four Platinum weather effects. No learnable new move sets weather, so nothing is routed; Snowscape is in the section for Ian.

## Harassment

The table of effects that get +2 (50%) on any turn.

| Move | Follows | What the flag does |
|---|---|---|
| Noble Roar, Tearful Look | Growl | +2; routed |
| Venom Drench | Growl | +2; routed. Nothing refuses it into an unpoisoned target, where it fails, as Expert's note says |
| Sticky Web | Spikes | +2; routed |
| Magic Room | Embargo | +2; routed (judgment calls) |
| Play Nice, Baby-Doll Eyes | Growl, their own effect | +2; inherited |
| Parting Shot | U-turn | none, as U-turn |
| Octolock, Spirit Shackle, Anchor Shot, Thousand Waves | Mean Look | none, as Mean Look |
| Entrainment | Worry Seed | none, as Worry Seed |
| Soak | Conversion 2 | none, as Conversion 2 |

## Appendix: every learnable new move

The effect is the move's battle effect in `res/moves/`; effects up to 276 are Platinum's own. "Follows" is the Platinum move whose effect the move is routed as, in every flag above and in Expert.

| Move | Effect | Follows |
|---|---|---|
| Hone Claws | 277, `ATK_ACC_UP` | Meditate |
| Wide Guard | 371, `PROTECT_USER_SIDE` | Protect (judgment call) |
| Guard Split | 278, `GUARD_SPLIT` | Guard Swap (judgment call) |
| Power Split | 279, `POWER_SPLIT` | Power Swap (judgment call) |
| Wonder Room | 407, `WONDER_ROOM` | Trick Room (judgment call) |
| Psyshock | 0, `HIT` | Tackle (its own effect) |
| Venoshock | 280, `DOUBLE_POWER_ON_POISONED` | Wake-Up Slap |
| Autotomize | 281, `AUTOTOMIZE` | Agility |
| Rage Powder | 172, `MAKE_GLOBAL_TARGET` | Follow Me (its own effect) |
| Magic Room | 411, `MAGIC_ROOM` | Embargo |
| Smack Down | 406, `SMACK_DOWN` | Gravity |
| Flame Burst | 0, `HIT` | Tackle (its own effect) |
| Sludge Wave | 2, `POISON_HIT` | Poison Sting (its own effect) |
| Quiver Dance | 283, `SP_ATK_SP_DEF_SPEED_UP` | Dragon Dance |
| Heavy Slam | 292, `HEAVY_SLAM` | Low Kick |
| Soak | 284, `CHANGE_TO_WATER_TYPE` | Conversion 2 |
| Flame Charge | 285, `RAISE_SPEED_HIT` | Rapid Spin (its Speed part) |
| Coil | 286, `ATK_DEF_ACC_UP` | Harden |
| Low Sweep | 70, `LOWER_SPEED_HIT` | BubbleBeam (its own effect) |
| Acid Spray | 271, `LOWER_SP_DEF_2_HIT` | Seed Flare (its own effect) |
| Foul Play | 0, `HIT` | Tackle (its own effect) |
| Entrainment | 384, `ENTRAINMENT` | Worry Seed |
| After You | 305, `AFTER_YOU` | Helping Hand |
| Round | 0, `HIT` | Tackle (its own effect) |
| Echoed Voice | 0, `HIT` | Tackle (its own effect) |
| Clear Smog | 390, `CLEAR_SMOG` | Haze |
| Stored Power | 0, `HIT` | Tackle (its own effect) |
| Quick Guard | 371, `PROTECT_USER_SIDE` | Protect (judgment call) |
| Scald | 125, `THAW_AND_BURN_HIT` | Flame Wheel (its own effect) |
| Shell Smash | 290, `ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN` | Dragon Dance |
| Heal Pulse | 379, `HEAL_TARGET` | Present |
| Hex | 287, `DOUBLE_DAMAGE_ON_STATUS` | Wake-Up Slap |
| Sky Drop | 414, `SKY_DROP` | Fly |
| Shift Gear | 288, `SPEED_UP_2_ATK_UP` | Dragon Dance |
| Incinerate | 372, `INCINERATE` | Pluck |
| Acrobatics | 289, `DOUBLE_DAMAGE_WITHOUT_ITEM` | Wake-Up Slap |
| Retaliate | 0, `HIT` | Tackle (its own effect) |
| Final Gambit | 402, `FINAL_GAMBIT` | Explosion (judgment call) |
| Water Pledge | 0, `HIT` | Tackle (its own effect) |
| Fire Pledge | 0, `HIT` | Tackle (its own effect) |
| Grass Pledge | 0, `HIT` | Tackle (its own effect) |
| Volt Switch | 228, `SWITCH_HIT` | U-turn (its own effect) |
| Struggle Bug | 71, `LOWER_SP_ATK_HIT` | Mist Ball (its own effect) |
| Bulldoze | 70, `LOWER_SPEED_HIT` | BubbleBeam (its own effect) |
| Dragon Tail | 395, `FORCE_SWITCH_HIT` | Roar |
| Electroweb | 70, `LOWER_SPEED_HIT` | BubbleBeam (its own effect) |
| Wild Charge | 198, `RECOIL_THIRD` | Double-Edge (its own effect) |
| Drill Run | 43, `HIGH_CRITICAL` | Karate Chop (its own effect) |
| Dual Chop | 44, `HIT_TWICE` | Double Kick (its own effect) |
| Horn Leech | 3, `RECOVER_HALF_DAMAGE_DEALT` | Absorb (its own effect) |
| Sacred Sword | 0, `HIT` | Tackle (its own effect) |
| Razor Shell | 69, `LOWER_DEFENSE_HIT` | Iron Tail (its own effect) |
| Cotton Guard | 328, `DEF_UP_3` | Harden |
| Tail Slap | 29, `MULTI_HIT` | DoubleSlap (its own effect) |
| Hurricane | 341, `HURRICANE` | Thunder |
| Relic Song | 301, `SLEEP_HIT` | ThunderPunch (a hit with a status chance) |
| Snarl | 71, `LOWER_SP_ATK_HIT` | Mist Ball (its own effect) |
| Icicle Crash | 31, `FLINCH_HIT` | Rolling Kick (its own effect) |
| Flying Press | 0, `HIT` | Tackle (its own effect) |
| Mat Block | 371, `PROTECT_USER_SIDE` | Protect (judgment call) |
| Belch | 396, `BELCH` | Tackle |
| Sticky Web | 326, `STICKY_WEB` | Spikes |
| Fell Stinger | 388, `FELL_STINGER` | Metal Claw |
| Phantom Force | 272, `SHADOW_FORCE` | Shadow Force (its own effect) |
| Noble Roar | 362, `TEARFUL_LOOK` | Growl |
| Petal Blizzard | 0, `HIT` | Tackle (its own effect) |
| Freeze-Dry | 5, `FREEZE_HIT` | Ice Punch (its own effect) |
| Disarming Voice | 17, `BYPASS_ACCURACY` | Swift (its own effect) |
| Parting Shot | 389, `PARTING_SHOT` | U-turn |
| Draining Kiss | 347, `RECOVER_THREE_QUARTERS_DAMAGE_DEALT` | Absorb |
| Crafty Shield | 371, `PROTECT_USER_SIDE` | Protect (judgment call) |
| Play Rough | 68, `LOWER_ATTACK_HIT` | Aurora Beam (its own effect) |
| Fairy Wind | 0, `HIT` | Tackle (its own effect) |
| Moonblast | 71, `LOWER_SP_ATK_HIT` | Mist Ball (its own effect) |
| Boomburst | 0, `HIT` | Tackle (its own effect) |
| Play Nice | 18, `ATK_DOWN` | Growl (its own effect) |
| Diamond Storm | 317, `RAISE_DEF_2_HIT` | Steel Wing |
| Water Shuriken | 29, `MULTI_HIT` | DoubleSlap (its own effect) |
| Mystical Fire | 71, `LOWER_SP_ATK_HIT` | Mist Ball (its own effect) |
| Eerie Impulse | 61, `SP_ATK_DOWN_2` | no Platinum move; Sp. Atk down two stages (its own effect) |
| Venom Drench | 361, `VENOM_DRENCH` | Growl |
| Geomancy | 318, `CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2` | Dragon Dance |
| Dazzling Gleam | 0, `HIT` | Tackle (its own effect) |
| Baby-Doll Eyes | 18, `ATK_DOWN` | Growl (its own effect) |
| Nuzzle | 6, `PARALYZE_HIT` | ThunderPunch (its own effect) |
| Hold Back | 101, `LEAVE_WITH_1_HP` | False Swipe (its own effect) |
| Infestation | 42, `BIND_HIT` | Bind (its own effect) |
| Power-Up Punch | 139, `RAISE_ATTACK_HIT` | Metal Claw (its own effect) |
| Oblivion Wing | 347, `RECOVER_THREE_QUARTERS_DAMAGE_DEALT` | Absorb |
| Thousand Arrows | 406, `SMACK_DOWN` | Gravity |
| Thousand Waves | 351, `PREVENT_ESCAPE_HIT` | Mean Look |
| Land’s Wrath | 0, `HIT` | Tackle (its own effect) |
| Origin Pulse | 0, `HIT` | Tackle (its own effect) |
| Shore Up | 132, `HEAL_HALF_MORE_IN_SUN` | Morning Sun (its own effect) |
| FirstImpression | 373, `FIRST_TURN_ONLY` | Fake Out |
| Spirit Shackle | 351, `PREVENT_ESCAPE_HIT` | Mean Look |
| Darkest Lariat | 0, `HIT` | Tackle (its own effect) |
| Sparkling Aria | 0, `HIT` | Tackle (its own effect) |
| High Horsepower | 0, `HIT` | Tackle (its own effect) |
| Strength Sap | 378, `STRENGTH_SAP` | Recover |
| Solar Blade | 151, `SKIP_CHARGE_TURN_IN_SUN` | SolarBeam (its own effect) |
| Leafage | 0, `HIT` | Tackle (its own effect) |
| Laser Focus | 399, `LASER_FOCUS` | Focus Energy or Lock-On (judgment call) |
| Throat Chop | 401, `THROAT_CHOP` | Tackle (its sound lock has no Platinum match) |
| Pollen Puff | 380, `POLLEN_PUFF` | Present |
| Anchor Shot | 351, `PREVENT_ESCAPE_HIT` | Mean Look |
| Lunge | 68, `LOWER_ATTACK_HIT` | Aurora Beam (its own effect) |
| Burn Up | 393, `REMOVE_USER_FIRE_TYPE_HIT` | Overheat |
| Smart Strike | 17, `BYPASS_ACCURACY` | Swift (its own effect) |
| Core Enforcer | 413, `CORE_ENFORCER` | Gastro Acid (judgment call) |
| Trop Kick | 68, `LOWER_ATTACK_HIT` | Aurora Beam (its own effect) |
| Beak Blast | 0, `HIT` | Tackle (its own effect) |
| Clanging Scales | 342, `USER_DEF_DOWN_HIT` | Close Combat |
| Brutal Swing | 0, `HIT` | Tackle (its own effect) |
| Aurora Veil | 377, `SET_AURORA_VEIL` | Reflect |
| StompingTantrum | 0, `HIT` | Tackle (its own effect) |
| Accelerock | 103, `PRIORITY_1` | Quick Attack (its own effect) |
| Liquidation | 69, `LOWER_DEFENSE_HIT` | Iron Tail (its own effect) |
| Tearful Look | 362, `TEARFUL_LOOK` | Growl |
| Zing Zap | 31, `FLINCH_HIT` | Rolling Kick (its own effect) |
| Nature’sMadness | 40, `HALVE_HP` | Super Fang (its own effect) |
| Mind Blown | 408, `MIND_BLOWN` | Head Smash |
| Teatime | 412, `TEATIME` | none |
| Octolock | 410, `OCTOLOCK` | Mean Look |
| Clangorous Soul | 346, `RAISE_ALL_STATS_LOSE_THIRD_MAX_HP` | Dragon Dance |
| Body Press | 0, `HIT` | Tackle (its own effect) |
| Pyro Ball | 4, `BURN_HIT` | Fire Punch (its own effect) |
| Breaking Swipe | 68, `LOWER_ATTACK_HIT` | Aurora Beam (its own effect) |
| Strange Steam | 76, `CONFUSE_HIT` | Psybeam (its own effect) |
| Life Dew | 383, `LIFE_DEW` | Recover |
| Expanding Force | 0, `HIT` | Tackle (its own effect) |
| Scale Shot | 29, `MULTI_HIT` | DoubleSlap (its own effect) |
| Meteor Beam | 324, `CHARGE_TURN_SP_ATK_UP` | Skull Bash |
| Grassy Glide | 0, `HIT` | Tackle (its own effect) |
| Terrain Pulse | 0, `HIT` | Tackle (its own effect) |
| Skitter Smack | 71, `LOWER_SP_ATK_HIT` | Mist Ball (its own effect) |
| Lash Out | 0, `HIT` | Tackle (its own effect) |
| Poltergeist | 345, `POLTERGEIST` | Tackle |
| Coaching | 381, `COACHING` | Helping Hand |
| Flip Turn | 228, `SWITCH_HIT` | U-turn (its own effect) |
| Triple Axel | 298, `HIT_THREE_TIMES_INCREMENT_BASE_POWER_20` | Triple Kick |
| Dual Wingbeat | 44, `HIT_TWICE` | Double Kick (its own effect) |
| Scorching Sands | 4, `BURN_HIT` | Fire Punch (its own effect) |
| Freezing Glare | 5, `FREEZE_HIT` | Ice Punch (its own effect) |
| Fiery Wrath | 31, `FLINCH_HIT` | Rolling Kick (its own effect) |
| Thunderous Kick | 69, `LOWER_DEFENSE_HIT` | Iron Tail (its own effect) |
| Wave Crash | 198, `RECOIL_THIRD` | Double-Edge (its own effect) |
| Headlong Rush | 229, `DEF_SPD_DOWN_HIT` | Close Combat (its own effect) |
| Shelter | 51, `DEF_UP_2` | Barrier (its own effect) |
| Axe Kick | 293, `CONFUSE_HIT_CRASH_ON_MISS` | Jump Kick |
| Salt Cure | 409, `SALT_CURE` | Bind (judgment call) |
| Mortal Spin | 369, `MORTAL_SPIN` | Rapid Spin |
| Flower Trick | 282, `ALWAYS_CRITICAL` | Karate Chop |
| Pounce | 70, `LOWER_SPEED_HIT` | BubbleBeam (its own effect) |
| Trailblaze | 285, `RAISE_SPEED_HIT` | Rapid Spin (its Speed part) |
| Chilling Water | 68, `LOWER_ATTACK_HIT` | Aurora Beam (its own effect) |
| Rage Fist | 0, `HIT` | Tackle (its own effect) |
| Armor Cannon | 229, `DEF_SPD_DOWN_HIT` | Close Combat (its own effect) |
| Bitter Blade | 3, `RECOVER_HALF_DAMAGE_DEALT` | Absorb (its own effect) |
| Double Shock | 394, `REMOVE_USER_ELECTRIC_TYPE_HIT` | Overheat |
| Aqua Cutter | 43, `HIGH_CRITICAL` | Karate Chop (its own effect) |
| Matcha Gotcha | 348, `RECOVER_HALF_DAMAGE_DEALT_BURN_HIT` | Absorb |
| Alluring Voice | 0, `HIT` | Tackle (its own effect) |
| Temper Flare | 0, `HIT` | Tackle (its own effect) |
| Psychic Noise | 320, `HIT_AND_PREVENT_HEALING` | Heal Block |
