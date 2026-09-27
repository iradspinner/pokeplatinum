# Platinum's moves with no Expert routine

A report for Ian (2026-09-27), read from the tree on `main-metronome`, which is `sinistea-split` plus a Metronome table change. It changes no AI code. Ian's ruling on routines is that every new move the trainer pass gives a trainer gets an Expert routine in that pass, and the rest wait; this list is the Platinum half, ids 1 to 467, for him to decide on.

## How a move reaches Expert

`Expert_Main` in `src/battle/trainer_ai/script.s` is a single jump table on the move's effect, one `IfCurrentMoveEffectEqualTo` line per effect, ending in `PopOrEnd`. A move whose effect is not in the table gets no Expert score at all, whatever its id; Expert never dispatches on a move id. The table now names 221 effects, Platinum's own and the ones element 6 added for the new moves on 2026-09-27.

A move outside the table is not left unscored. Basic scores every damaging move with a fixed power on its damage and on immunities, including the absorbing abilities and Wonder Guard, and Evaluate Attack takes a point off a move that is not the strongest the Pokemon has, adds four (six for a +1 priority effect) when it would knock out, and may add two when it is four times effective. So a damaging move with no Expert routine is still chosen on its damage; what goes unvalued is whatever it does besides, such as a flinch or a status chance, a stat change, or a condition that raises its power. A status move has no damage to fall back on, so it gets only the check Basic keeps for its effect, if there is one (mostly "this would fail, score -10"), and the effect lists some other flags keep.

The counts:

| | Moves |
|---|---|
| Platinum's moves, ids 1 to 467 | 467 |
| with an Expert routine | 267 |
| without one | 200 (91 effects) |
| of those, damaging | 170 |
| of those, status | 30 |
| without one and fielded by no Expert trainer | 36 |

Each move below carries, in brackets, how many trainers with the Expert flag field it, by hand or from their default learnset moves, counting only trainers some map in the game uses (the move pool survey's resolver). "Effect read by" names the other routines that test the move's effect; "move named by" those that test the move itself, usually for a list such as Soundproof's or for a partner in doubles. Effect names are the decomp's `BATTLE_EFFECT_` constants.

## Damaging moves

Chosen on damage by Basic and Evaluate Attack; the column says what else reads them.

| Effect | Moves (Expert trainers) | Beyond damage |
|---|---|---|
| LOWER_SP_DEF_HIT | Psychic (87), Shadow Ball (53), Energy Ball (41), Focus Blast (28), Flash Cannon (25), Earth Power (24), Bug Buzz (6), Acid (0), Luster Purge (0) | move named by Basic, Tag Strategy |
| FLINCH_HIT | Waterfall (45), Zen Headbutt (44), Headbutt (31), Dark Pulse (30), Iron Head (30), Extrasensory (18), Rock Slide (18), Air Slash (16), Bite (14), Astonish (7), Dragon Rush (4), Bone Club (1), Hyper Fang (1), Needle Arm (1), Rolling Kick (0) | nothing beyond the general checks |
| plain hit | Seed Bomb (44), Hydro Pump (32), Aqua Tail (25), Power Gem (13), Slam (12), Dragon Pulse (10), Tackle (10), Rock Throw (9), Scratch (9), Water Gun (9), Wing Attack (9), Hyper Voice (6), Peck (4), Mega Punch (3), Pound (3), Mega Kick (2), Egg Bomb (1), ViceGrip (1), Vine Whip (1), Cut (0), Horn Attack (0), Strength (0) | effect read by Basic; move named by Basic, Tag Strategy |
| PARALYZE_HIT | ThunderPunch (75), Thunderbolt (54), Body Slam (20), Discharge (9), Spark (5), Force Palm (3), ThunderShock (3), DragonBreath (2), Lick (1), Zap Cannon (0) | move named by Basic, Tag Strategy |
| PRIORITY_1 | Quick Attack (49), Bullet Punch (25), Aqua Jet (20), Mach Punch (16), Ice Shard (12), Shadow Sneak (12), ExtremeSpeed (8), Vacuum Wave (5) | effect read by Evaluate Attack, Tag Strategy |
| BURN_HIT | Fire Punch (52), Flamethrower (35), Fire Blast (16), Heat Wave (13), Ember (7), Lava Plume (3) | move named by Tag Strategy |
| FREEZE_HIT | Ice Punch (64), Ice Beam (55), Powder Snow (1) | nothing beyond the general checks |
| DOUBLE_DAMAGE_DIG | Earthquake (104) | move named by Tag Strategy |
| POISON_HIT | Poison Jab (37), Sludge Bomb (33), Gunk Shot (14), Poison Sting (6), Sludge (3), Attack Order (1), Smog (1) | move named by Basic, Tag Strategy |
| CONFUSE_HIT | Signal Beam (44), Psybeam (11), Confusion (10), Water Pulse (9), Dizzy Punch (6), DynamicPunch (4), Rock Climb (0) | move named by Tag Strategy |
| LOWER_DEFENSE_HIT | Crunch (60), Iron Tail (4), Crush Claw (2), Rock Smash (0) | nothing beyond the general checks |
| DOUBLE_DAMAGE_DIVE | Surf (63) | move named by Tag Strategy |
| RAISE_ALL_STATS_HIT | AncientPower (24), Ominous Wind (9), Silver Wind (8) | effect read by Risky |
| FLINCH_FREEZE_HIT | Ice Fang (37) | nothing beyond the general checks |
| FLINCH_PARALYZE_HIT | Thunder Fang (37) | nothing beyond the general checks |
| CONTINUE_AND_CONFUSE_SELF | Outrage (27), Thrash (5), Petal Dance (1) | nothing beyond the general checks |
| INCREASE_POWER_WITH_WEIGHT | Low Kick (23), Grass Knot (6) | effect read by Basic |
| MULTI_HIT | Fury Swipes (8), Bullet Seed (7), Fury Attack (4), Rock Blast (4), DoubleSlap (2), Icicle Spear (2), Pin Missile (1), Spike Cannon (1), Arm Thrust (0), Barrage (0), Bone Rush (0), Comet Punch (0) | move named by Basic |
| FLINCH_BURN_HIT | Fire Fang (26) | nothing beyond the general checks |
| RANDOM_POWER_BASED_ON_IVS | Hidden Power (23) | effect read by Basic |
| CRASH_ON_MISS | Hi Jump Kick (10), Jump Kick (5) | nothing beyond the general checks |
| LOWER_ACCURACY_HIT | Muddy Water (5), Mud-Slap (4), Mud Bomb (3), Mirror Shot (2), Octazooka (1) | move named by Basic |
| LEVEL_DAMAGE_FLAT | Seismic Toss (7), Night Shade (4) | effect read by Basic, Tag Strategy |
| TRI_ATTACK | Tri Attack (10) | nothing beyond the general checks |
| DOUBLE_POWER_EACH_TURN_LOCK_INTO | Rollout (9), Ice Ball (0) | move named by Basic |
| RAISE_ATTACK_HIT | Meteor Mash (6), Metal Claw (3) | nothing beyond the general checks |
| RAISE_DEF_HIT | Steel Wing (8) | nothing beyond the general checks |
| HIT_IN_3_TURNS | Future Sight (7), Doom Desire (0) | effect read by Basic, Evaluate Attack; move named by Tag Strategy |
| PSYWAVE (Magnitude's effect, despite the name; Psywave's is RANDOM_DAMAGE_1_TO_150_LEVEL) | Magnitude (7) | effect read by Basic; move named by Tag Strategy |
| BADLY_POISON_HIT | Poison Fang (6) | nothing beyond the general checks |
| HIT_TWICE | Double Kick (4), Bonemerang (1), Double Hit (1) | nothing beyond the general checks |
| HIT_FLY | Sky Uppercut (5) | nothing beyond the general checks |
| NATURAL_GIFT | Natural Gift (5) | effect read by Basic |
| RAISE_SP_ATK_HIT | Charge Beam (5) | nothing beyond the general checks |
| THAW_AND_BURN_HIT | Flame Wheel (5), Sacred Fire (0) | nothing beyond the general checks |
| UPROAR | Uproar (5) | move named by Basic |
| CHANGE_TYPE_WITH_WEATHER | Weather Ball (4) | move named by Basic |
| POWER_BASED_ON_FRIENDSHIP | Return (4) | effect read by Basic |
| RAISE_ATK_WHEN_HIT | Rage (4) | effect read by Check HP |
| DOUBLE_DAMAGE_FLY_OR_BOUNCE | Gust (3) | nothing beyond the general checks |
| FLINCH_MINIMIZE_DOUBLE_HIT | Stomp (3) | nothing beyond the general checks |
| RANDOM_POWER_MAYBE_HEAL | Present (3) | effect read by Basic, Risky |
| 20_DAMAGE_FLAT | SonicBoom (2) | effect read by Basic, Tag Strategy |
| CHATTER | Chatter (2) | move named by Basic |
| LOWER_ATTACK_HIT | Aurora Beam (2) | nothing beyond the general checks |
| FLINCH_DOUBLE_DAMAGE_FLY_OR_BOUNCE | Twister (1) | nothing beyond the general checks |
| RANDOM_DAMAGE_1_TO_150_LEVEL | Psywave (1) | effect read by Basic, Risky, Tag Strategy |
| WHIRLPOOL | Whirlpool (1) | effect read by Setup First Turn |
| 40_DAMAGE_FLAT | Dragon Rage (0) | effect read by Basic, Tag Strategy |
| BEAT_UP | Beat Up (0) | nothing beyond the general checks |
| DOUBLE_POWER_EACH_TURN | Fury Cutter (0) | effect read by Check HP |
| HIT_THREE_TIMES | Triple Kick (0) | nothing beyond the general checks |
| INCREASE_PRIZE_MONEY | Pay Day (0) | nothing beyond the general checks |
| JUDGEMENT | Judgment (0) | nothing beyond the general checks |
| LEAVE_WITH_1_HP | False Swipe (0) | nothing beyond the general checks |
| LOWER_SP_ATK_HIT | Mist Ball (0) | move named by Basic |
| LOWER_SP_DEF_2_HIT | Seed Flare (0) | move named by Tag Strategy |
| POISON_MULTI_HIT | Twineedle (0) | nothing beyond the general checks |
| POWER_BASED_ON_LOW_FRIENDSHIP | Frustration (0) | effect read by Basic |
| SECRET_POWER | Secret Power (0) | effect read by Harassment |
| STRUGGLE | Struggle (0) | nothing beyond the general checks |

## Status moves

No damage to fall back on; the column is everything that scores them.

| Effect | Moves (Expert trainers) | What scores it |
|---|---|---|
| STATUS_BURN | Will-O-Wisp (46) | effect read by Basic, Check HP, Harassment, Setup First Turn; move named by Tag Strategy |
| STATUS_SLEEP_NEXT_TURN | Yawn (24) | effect read by Basic, Harassment, Setup First Turn |
| PREVENT_STATUS | Safeguard (12) | effect read by Basic, Check HP |
| WEATHER_SANDSTORM | Sandstorm (12) | effect read by Basic, Weather; move named by Tag Strategy |
| ALL_FAINT_3_TURNS | Perish Song (11) | effect read by Basic, Check HP |
| TAUNT | Taunt (9) | effect read by Basic |
| DEF_UP_DOUBLE_ROLLOUT_POWER | Defense Curl (8) | effect read by Basic, Setup First Turn |
| CALL_RANDOM_MOVE | Metronome (5) | effect read by Risky |
| COPY_MOVE_FOR_BATTLE | Mimic (5) | nothing scores it |
| CRIT_UP_2 | Focus Energy (5) | effect read by Basic, Check HP, Setup First Turn |
| STOCKPILE | Stockpile (5) | effect read by Basic |
| INFATUATE | Attract (4) | effect read by Basic, Check HP, Harassment, Risky |
| DECREASE_LAST_MOVE_PP | Spite (3) | effect read by Check HP, Harassment |
| SP_DEF_UP_DOUBLE_ELECTRIC_POWER | Charge (3) | nothing scores it |
| CAMOUFLAGE | Camouflage (2) | effect read by Basic, Harassment, Setup First Turn |
| CONFUSE_ALL | Teeter Dance (2) | effect read by Harassment, Risky, Setup First Turn |
| NATURE_POWER | Nature Power (2) | effect read by Harassment |
| BOOST_ALLY_POWER_BY_50_PERCENT | Helping Hand (1) | effect read by Basic; move named by Tag Strategy |
| CONVERSION2 | Conversion 2 (1) | effect read by Check HP |
| MAKE_GLOBAL_TARGET | Follow Me (1) | move named by Tag Strategy |
| TORMENT | Torment (1) | effect read by Basic, Harassment, Setup First Turn |
| TRANSFORM | Transform (1) | nothing scores it |
| USE_RANDOM_ALLY_MOVE | Assist (1) | nothing scores it |
| DO_NOTHING | Splash (0) | nothing scores it |
| FLEE_FROM_WILD_BATTLE | Teleport (0) | effect read by Basic |
| HEAL_IN_3_TURNS | Wish (0) | nothing scores it |
| LEARN_MOVE_PERMANENT | Sketch (0) | nothing scores it |
| PREVENT_STAT_REDUCTION | Mist (0) | effect read by Basic, Check HP |
| REMOVE_ALL_PP_ON_DEFEAT | Grudge (0) | effect read by Check HP |
| STATUS_NIGHTMARE | Nightmare (0) | effect read by Basic |

## Reproducing it

The table was read by a short parser over `script.s` (the routine regions by their `_Main` labels, Expert's table by its run of effect tests) and the move records in `res/moves/`, and the trainer counts from `tools/oxide/move_pool_survey.py`'s `collect()`. A move changing effect, or a new line in Expert's table, changes the list; rerun rather than edit it by hand.
