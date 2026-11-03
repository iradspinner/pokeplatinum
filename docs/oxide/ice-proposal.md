# Ice: three levers

## Summary

Ian answered on 2026-11-03: "Only the water resist, the others are approved." So Ice resists Water alone (option A, not B), snow replaces hail in place, and Delibird learns Aurora Veil at 36 while Alolan Ninetales learns it at 40 in place of level 1, with no TM. Snow Warning stays in its hidden slots. All three landed on `overseer-ice-levers`, one commit each; the text below is the proposal as it stood when he answered.

Ian asked on 2026-11-03 to change the chart for Ice, the one type whose lines average below zero on the [defensive index](defensive-index.md), and named two more levers to try: snow in place of hail, as in Generation 9, and wider access to Aurora Veil. This is the proposal. Nothing in the game, the engine or the simulator has changed.

What could not be checked comes first. No lever was played, in the game or on the simulator; every measure of a lever below is the defensive index, which reads typing only, and every engine rule is read from the source. The repo records no other hack that changed Ice's chart: the [staples survey](staples-survey.md) of seven hacks records only Steel's Generation 6 loss, the expansion engines' default, and it never read their charts directly. I did not browse. Candice's new team is being read on the scorer now under today's mechanics, so all three levers would stale that reading.

One finding outside the three levers needs fixing whatever Ian decides. The simulator, and so the scorer, plays the fights on Route 216 and Acuity Lakefront in clear weather, but the game plays them in hail on every day of the year. Those two maps, with Snowpoint City and Route 212 South, take their weather from a day-of-year table (`src/field_overworld_weather.c`), and `splits.battle_weather` reads only the plain weathers. Nine fights the player meets in hail are scored without it: four Ace Trainers on Route 216 (Blake, Garrett, Laura and Maria), Black Belt Philip, three skiers and Hiker Gunnar. Skier Edward is the tenth on those maps; his Abomasnow's Snow Warning hides the gap. Eleven trainers on Route 212 South fight in rain on 365 days of 366 and are scored dry too.

The outcome, lever by lever:

1. On the chart, one resistance lifts Ice's single-type index by 0.7 to 1.8 points. Water and Flying together bring Ice's lines from -2.48 to -0.45, level with Rock (-0.26) and Psychic (+0.14), the other types at the bottom. Adding Ground as well takes them to +0.70, past Normal, Psychic and Rock, and puts Froslass 25th of the 219 lines. No other single type moves at all, since each option changes only what hits Ice. Other types' line averages rise by 0.31 at most, through their Ice dual types, and no other type moves more than one place. Steel losing its Ghost and Dark resistances (on `overseer-steel-chart`) touches no Ice typing; Steel stays first by more than three points.
2. Snow in place of hail is a small change in Oxide's engine. Hail stops chipping anything, Ice types take physical hits on one and a half times their Defense, and every other reader keeps reading the same weather. The player sets no weather, so the player's Ice types get the boost only in a trainer's or a map's snow. That is 31 trainer fights before the League, 27 of them on the snowy maps of Candice's and HQ's splits. Candice's own fight is the largest change: four of her six are Ice types, and the player's answers to Ice are mostly physical.
3. Aurora Veil fails outside hail or snow, so for the player it works only in those 31 fights, or everywhere for one Pokemon that the game's one Ability Patch gives Snow Warning. Frosmoth already learns it at 36, after its catch at 33 or 34. Alolan Ninetales has it only at level 1, which means the relearner. Giving it to Delibird, one of the lines most at risk of having no niche, and moving Ninetales's copy to a real level is the cheap, distinct option.

Ian's decisions:

1. Ice's new resistances: Water and Flying (recommended); Water alone; Water, Flying and Ground; or none.
2. Snow in place of hail: convert the one weather in place (recommended); add snow beside hail as hg-engine does; or keep hail.
3. Aurora Veil: Delibird by level at 36 and Alolan Ninetales from level 1 to about 40 (recommended); that plus one single-copy TM in Candice's split; or no change.
4. The Ability Patch and Snow Warning: leave Snow Warning in the hidden slot of Snover's and Alolan Ninetales's lines, so one player Pokemon can set snow (recommended); or move it out, so the player never has snow of their own.
5. Order against Candice's reading: land whichever of 1 to 3 Ian takes, then judge Candice on the cheap checks, with a reading only if he names one (recommended); or tune Candice on today's reading first.
6. The yearly weather gap: fix `splits.battle_weather` so the four day-of-year maps are scored in their weather, as its own commit (recommended); or leave it.

Next steps, once Ian answers. Each lever is one helper session and one landing; the snow change also needs Ian's yes to its simulator change, since the simulator changes only with his approval.

| Step | Who | Time |
|---|---|---|
| The weather gap fix in `splits.py`, with a test | a worker helper | 30 minutes |
| The chart change | a worker helper | 1 hour |
| Snow for hail, the engine, the simulator and their tests | a worker helper | 3 to 5 hours |
| Aurora Veil, two learnset entries | a routine helper | 30 minutes |
| Each landing: build, gate, push | the Overseer | 30 to 40 minutes of machine time |
| In-game checks with the test kit | Ian | 15 minutes a lever |
| A Candice reading, only if Ian names one | the scorer | 2.5 to 4 hours |

## Lever 1: the chart

### The options

Ice today resists only Ice and is weak to Fire, Fighting, Rock and Steel. I tried every resistance Ice could gain, one at a time. Dark, Normal and Electric are worth the most, because trainers use them most (Dark is about a tenth of all their damaging moves), but none of them has a reason in the type's character. Water (ice is frozen water), Ground (frozen ground) and Flying (cold air) do. Flying also has a precedent in the chart: Electric and Rock both resist Flying and hit it super effectively, as Ice would. Grass, the other candidate with a reason, makes Ice a hard counter to Gardenia at the start of the game, where Alolan Ninetales is already one of the player's answers to her; I left it out.

| Option | Ice resists | Ice's single-type index, player's view (rank of 18) | Trainers' view (rank) | Mean of the 16 Ice lines, player's view | Trainers' view |
|---|---|---|---|---|---|
| Today | Ice | -3.72 (18) | -3.42 (18) | -2.48 | -2.20 |
| A | Ice, Water | -2.40 (16) | -2.22 (17) | -1.32 | -1.17 |
| B | Ice, Water, Flying | -1.49 (16) | -1.02 (16) | -0.45 | +0.02 |
| C | Ice, Water, Flying, Ground | -0.10 (15) | +0.31 (14) | +0.70 | +1.12 |
| D | Ice, Water, Ground | -1.02 (16) | -0.90 (16) | -0.17 | -0.07 |

Option A still leaves Ice last by more than a point. Option D lands near B, but Ground is among what trainers attack with most late in the game (11 to 12 percent of their attacks in the Galactic, Barry and League splits), so it moves the late bosses: Bertha, Lucas or Dawn 3 and Barry 6, where Ice is already the player's natural answer and would then resist their main attack as well. Option C is the strongest. It lifts Ice past three types and turns Froslass and Alolan Ninetales into top-50 defenders, which is power creep against Ian's warning.

Option B is the recommendation. It ends Ice's place as the outlier and leaves it at the bottom with Rock and Psychic, each of which also has a known weakness profile. It gives Ice a defensive role it lacks, as a check to Water and Flying attackers, and Flying is rare in trainers' hands (1 to 4 percent of their attacks in each split), so it moves few fights. I also tried taking away Ice's Steel weakness alongside B: Ice's lines reach +0.43, nearly C's figure. I do not recommend it, since a cut weakness moves every Steel attacker in the game.

### Where the Ice typings land

Player's view, with the rank among the 113 typings an obtainable stage has:

| Typing | Lines | Today | A | B | C |
|---|---|---|---|---|---|
| Ice/Ghost | Froslass | +2.88 (52) | +4.20 (30) | +5.11 (22) | +6.49 (14) |
| Ice/Fairy | Alolan Ninetales | +0.87 (78) | +2.19 (60) | +3.10 (49) | +4.49 (29) |
| Ice/Flying | Articuno, Delibird | -1.49 (97) | -0.17 (86) | +0.74 (79) | +0.74 (81) |
| Ice/Dark | Sneasel, Weavile | -2.56 (102) | -1.24 (97) | -0.33 (90) | +1.06 (78) |
| Water/Ice | Cloyster, Dewgong, Lapras, Walrein | -2.57 (103) | -1.91 (103) | -1.00 (96) | +0.38 (83) |
| Ice/Ground | Swinub, Piloswine, Mamoswine | -2.67 (104) | -1.03 (93) | -0.12 (87) | +1.27 (75) |
| Ice/Bug | Snom, Frosmoth | -2.94 (106) | -1.63 (101) | -0.80 (93) | -0.11 (91) |
| Grass/Ice | Snover, Abomasnow | -3.46 (109) | -2.80 (107) | -1.98 (105) | -1.29 (101) |
| Ice | Snorunt, Glaceon | -3.72 (110) | -2.40 (105) | -1.49 (102) | -0.10 (90) |
| Ice/Psychic | Smoochum, Jynx, Mr. Rime, Galarian Mr. Mime | -5.67 (112) | -4.35 (111) | -3.44 (111) | -2.05 (106) |
| Ice/Rock | Glalie | -6.53 (113) | -4.89 (112) | -4.44 (112) | -2.67 (109) |

Glalie and the Ice/Psychic lines stay near the bottom under every option. Their trouble is the second type's weaknesses (Rock's four, Psychic's Dark, Bug and Ghost), which no Ice resistance fixes, so their niche still has to come from offence, Speed or a learnset.

### The other types

No other type's single-type index changes under any option, because every option changes only what hits Ice. The line averages of other types move through their Ice dual types:

| Type | Lines | Today | A | B | C | B with Steel's later chart |
|---|---|---|---|---|---|---|
| Steel | 16 | +11.84 (1) | +11.84 (1) | +11.84 (1) | +11.84 (1) | +9.10 (1) |
| Ghost | 17 | +5.91 (2) | +5.99 (2) | +6.04 (2) | +6.12 (2) | +6.04 (2) |
| Fairy | 18 | +5.49 (3) | +5.56 (3) | +5.61 (3) | +5.69 (3) | +5.40 (3) |
| Electric | 16 | +5.01 (4) | +5.01 (4) | +5.01 (4) | +5.01 (4) | +4.66 (4) |
| Poison | 17 | +4.62 (5) | +4.62 (5) | +4.62 (5) | +4.62 (5) | +4.62 (5) |
| Dragon | 12 | +4.12 (6) | +4.12 (6) | +4.12 (6) | +4.12 (6) | +3.89 (6) |
| Fire | 19 | +3.34 (7) | +3.34 (7) | +3.34 (7) | +3.34 (7) | +3.34 (7) |
| Fighting | 19 | +3.32 (8) | +3.32 (8) | +3.32 (8) | +3.32 (8) | +3.22 (8) |
| Ground | 18 | +3.08 (9) | +3.17 (9) | +3.22 (9) | +3.30 (9) | +3.07 (9) |
| Flying | 25 | +2.80 (10) | +2.91 (10) | +2.98 (10) | +2.98 (10) | +2.75 (10) |
| Water | 49 | +2.68 (11) | +2.73 (11) | +2.80 (11) | +2.92 (11) | +2.75 (11) |
| Dark | 19 | +1.98 (12) | +2.05 (12) | +2.09 (12) | +2.17 (12) | +2.09 (12) |
| Grass | 25 | +1.16 (13) | +1.18 (13) | +1.22 (14) | +1.24 (14) | +1.10 (13) |
| Bug | 21 | +1.12 (14) | +1.18 (14) | +1.22 (13) | +1.25 (13) | +1.09 (14) |
| Normal | 19 | +0.37 (15) | +0.37 (15) | +0.37 (15) | +0.37 (16) | +0.37 (15) |
| Psychic | 23 | +0.14 (16) | +0.25 (16) | +0.33 (16) | +0.45 (17) | +0.02 (16) |
| Rock | 19 | -0.26 (17) | -0.17 (17) | -0.15 (17) | -0.05 (18) | -0.44 (17) |
| Ice | 16 | -2.48 (18) | -1.32 (18) | -0.45 (18) | +0.70 (15) | -0.45 (18) |

Steel's later chart lowers Steel by 2.7 points and every type that shares lines with it by up to 0.35, and changes nothing for Ice: no obtainable line is Steel and Ice. The two changes are independent.

### What it costs and which fights it moves

The work is small. The chart is `sTypeMatchupMultipliers` in `src/battle/battle_lib.c`, and each new resistance is one entry, placed before the table's 0xFE mark (Foresight ignores everything after it). The Poketch's move tester has its own copy (`sMoveTesterTypeChart`), and the encounter tool's test that pins the chart gains the new entries. The trainer AI, the simulator, the damage calculator and the OxiDex all read the chart from the battle code, so none of them changes, and no simulator approval is needed. The defensive index doc is regenerated from its script in 20 seconds. One helper hour, one landing, and one in-game check: a Water move into an Ice type reads "not very effective".

Ice's attackers do not move under any option, since no option changes what Ice hits. The fights that move are those where an Ice type takes a Water or Flying hit. On the trainers' side that is every team with an Ice member:

| Split | Roark | Gardenia | Fantina | Maylene | Wake | Byron | Candice | HQ | Galactic | Volkner | Barry | League |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Teams with an Ice member | 2 | 3 | 1 | 5 | 8 | 5 | 17 | 6 | 9 | 0 | 5 | 1 |
| Ice members, of all members | 2 of 129 | 4 of 147 | 2 of 182 | 5 of 168 | 8 of 246 | 5 of 275 | 50 of 115 | 8 of 115 | 10 of 247 | 0 of 50 | 6 of 142 | 1 of 60 |

By the boss-shape rule (a change to a boss's core, or to the player's core counterpiece to it), option B is material for three fights. Candice's core is Ice: on her new team Lapras and Cloyster go to a quarter of a Water hit, Ninetales to a half, and Mamoswine, her ace, from double to neutral. The Somnu and Moira double moves on Moira's side (Abomasnow, Mr. Rime and Glaceon). Wake moves through the player's side, since six of his 18 attacks are Water. The Ice lines first owned in his split (Abomasnow, Walrein, Mr. Rime and Glalie) all take his Water hits better, and Glalie goes from weak to neutral. The Flying resistance moves no boss by judgement: Lucas or Dawn 2 carries the most Flying attacks, 12 of 110 across her teams. The one-off Ice members on other bosses are not material: Dahlia's Cloyster, Cyrus 2's Weavile, and Deimos's Snorunt and two Froslass. Options C and D add Bertha, Lucas or Dawn 3 and Barry 6 through Ground.

## Lever 2: snow in place of hail

### What hail is in Oxide today

One weather, set four ways. Hail the move sets five turns (eight with an Icy Rock). Snow Warning sets it for the whole battle, because ability weather stays permanent in Oxide (Ian's answer of 2026-09-26). A map sets it for the whole battle when the battle starts in snowing, heavy snow or blizzard (`battle_lib.c`, the field weather check). The maps that do, from their headers and the day-of-year table:

| Map | Weather | Trainers fought there |
|---|---|---|
| Snowpoint Gym | blizzard | Candice, her six gym trainers and her rematch |
| Route 217 | blizzard | 9, Ace Trainers Dalton and Olivia among them |
| Route 216 | heavy snow on 356 days, blizzard on 9, snowing on 1 | 9, four of them Ace Trainers |
| Acuity Lakefront | heavy snow on 357 days, snowing on 9 | Hiker Gunnar |
| Snowpoint City | snowing on 356 days; on the other 10 the overworld "hailing" weather, which starts no battle weather | none |
| Mt. Coronet's two outside maps | heavy snow | none |
| Twinleaf Town | snowing (the base ROM's header) | none |

The player sets no weather (the standing ruling), so on the player's side only the one Ability Patch can bring snow: Snover's, Abomasnow's and Alolan Ninetales's hidden slot is Snow Warning, and the Patch is Ace Trainer Jose's reward on Route 228, in the Galactic split.

### The fights in hail

31 trainer teams the player fights in the twelve splits meet hail, 27 by their map and 4 by their own team. Tag partners are left out, as in the index.

| Split | By the map | By the team's Snow Warning or Hail |
|---|---|---|
| Gardenia | none | Camper Zackary (Snover) |
| Fantina | none | Officer Moira at the Eterna building (Snover) |
| Candice | Leader Candice; gym Ace Trainers Alicia, Anton, Brenna, Isaiah, Savannah and Sergio; Route 217's Ace Trainers Dalton and Olivia, Black Belt Luke, Ninja Boys Ethan and Matthew, Skiers Bjorn, Lexie, Madison and Shawn; Route 216's Ace Trainers Blake, Garrett, Laura and Maria, and Skier Edward; Candice's rematch, which the roster puts in her split | the Somnu and Moira double (Moira's Abomasnow) |
| HQ | Route 216's Black Belt Philip and Skiers Andrea, Bradley and Kaitlyn; Hiker Gunnar at Acuity Lakefront | none |
| Galactic | none | Officer Moira on Mt. Coronet 5F (Abomasnow) |

Brenna's Alolan Ninetales, Dalton's and Edward's Abomasnow, and the rematch's Abomasnow and Glaceon also set it on a snowy map. No gauntlet section is in snow.

### What each reader of hail does now, and should do in snow

| Reader | Where | Today | In snow |
|---|---|---|---|
| The end-of-turn chip | `battle_script.c`, BtlCmd_EndOfTurnWeatherEffect | a sixteenth to every Pokemon but Ice types, Snow Cloak, Overcoat, the Safety Goggles and the engine's other exemptions | none; the branch goes |
| Ice types' Defense | `battle_lib.c`, the damage formula, beside sand's Sp. Def rise for Rock types | nothing | one and a half times Defense against physical moves (hg-engine's CalcBaseDamage does the same) |
| Ice Body | the same end-of-turn command | heals a sixteenth | the same |
| Snow Cloak | `battle_controller_player.c`, the accuracy check | evasion, and no chip | evasion only; the chip immunity has nothing to do |
| Overcoat and the Safety Goggles | the end-of-turn command | no chip from sand or hail | no chip from sand; hail's part has nothing to do |
| Blizzard | `battle_controller_player.c`, the accuracy check | never misses | the same |
| Aurora Veil | `battle_script.c`, BtlCmd_TryAuroraVeil | fails outside hail | fails outside snow |
| Weather Ball | `battle_script.c` and `battle_lib.c` | Ice, double power | the same |
| Solar Beam, Synthesis, Moonlight, Morning Sun | the damage formula and BtlCmd_WeatherHPRecovery | halved power; a quarter healed | the same, as in Generation 9 |
| Castform's Forecast | `battle_lib.c` | the snowy form, Ice type | the same |
| Slush Rush | not read anywhere; no Oxide species has it | nothing | nothing, unless a species is given it |
| The Hail move | effect script 164 | five turns of hail | five turns of snow; renamed Snowscape, as in Generation 9, or kept as Hail with a new description |
| Battle text | the overworld, Snow Warning and end messages | "It started to hail!", "Hail continues to fall.", "The hail stopped.", "whipped up a hailstorm", the chip message | snow in each; the chip message goes unused |
| The trainer AI's damage estimate | `trainer_ai.c`, through BattleSystem_CalcMoveDamage | the engine's formula | follows the engine with no change |
| The trainer AI's scripts | `script.s`: Basic_CheckHail, Expert_Hail, the charge-turn routine's hail branch, the tag strategy | value hail by its chip and Ice Body | the charge-turn branch (a Dig or Fly user avoids the chip) should go; the Hail scores can stay, as only Candice's rematch uses the move |

Ability weather stays permanent. A Snow Warning holder's snow lasts the battle, as its hail does now.

### What the player gains and loses

In the 31 snow fights the player gains in two ways. The player's non-Ice Pokemon no longer lose a sixteenth a turn, which today breaks Focus Sashes and adds up over a long fight against Moira's or Candice's permanent hail. The player's Ice types also take physical hits on half again their Defense. The player loses the chip that hail did to the trainer's own non-Ice members (Candice's Chandelure and Gastrodon, and Somnu's half of the double, take it today), and the trainer's Ice types become a third harder to hurt physically. That second loss is the large one: the player's answers to an Ice core are mostly physical Fighting, Rock and Steel moves.

Outside those 31 fights nothing changes for the player, except one Pokemon given Snow Warning by the Ability Patch. For that one Pokemon snow becomes free: no chip on the player's own team, and a Defense rise for every Ice type on it. With Aurora Veil on the same team (lever 3) it would be the strongest use of the Patch. The ruling allows it, and there is only one Patch, so it is a build the player chooses, not a default; decision 4 asks whether to keep it.

The defensive index barely moves. Losing hail's chip immunity costs Ice 0.03 in the player's view, and the Defense rise is a stat, not a matchup, so the index does not count it.

### What it costs and which fights it moves

The engine work is small, about 40 lines of C and battle script plus text. It means deleting the chip branch, adding the Defense line beside sand's, removing the AI script's charge-turn hail branch, and rewriting about six battle strings, the Hail move's name and description, and the descriptions of Snow Cloak, Ice Body, Snow Warning and Slush Rush, which say "hailstorm", each measured to fit. A test kit set would show an Ice type taking less from a physical hit in snow and no chip at the turn's end. hg-engine runs snow and hail as two weathers, with snow behind a config switch; converting Oxide's one weather in place is less work and loses nothing, since no fight needs both.

The simulator needs the same three changes. Those are the end-of-turn chip in `fightsim.py`, the Defense line in the vendored calculator's Oxide mechanics (`calc/mechanics/gen4.js`, beside sand's line; the OxiDex's calculator page shares it), and the charge-turn branch in `fightai.py`. Each comes with a test that fails first. This is a new behaviour outside the approved gaps list, so it needs Ian's yes. With the weather gap fix it is one worker session of 3 to 5 hours, one landing, and Ian's test-kit check.

It moves the 31 fights in the table and no others. Material: Candice (her four Ice members and her map's blizzard); the Somnu and Moira double, whose theme is hail; Moira's fights at the Eterna building and on Mt. Coronet 5F; and the twelve Ace Trainers in snow, all mini-bosses. Not material by judgement: the ordinary trainers on Routes 216 and 217, Acuity Lakefront's hiker, Camper Zackary and the rematch.

## Lever 3: Aurora Veil

### Who has it now

Aurora Veil halves physical and special damage to the user's side for five turns (eight with Light Clay, a field item on Mt. Coronet B1F, a map of Candice's split), two thirds in a double, and does not stack with Reflect or Light Screen. It fails outside hail. Two lines can learn it. Frosmoth learns it at 36, after its catch at 33 or 34 on Routes 216 and 217, so under the capture rule it counts. Alolan Ninetales has it only at level 1, so only the relearner in Pastoria teaches it, for a Heart Scale, which makes it worth almost nothing. One trainer uses it: Ace Trainer Brenna's Ninetales in Snowpoint Gym.

### What it is worth to the player

Without snow it does nothing. In snow it is the strongest defensive move the player can have: one turn buys five turns of half damage, in the fights where it works. Those are the 31 snow fights, 23 of them in Candice's split, Candice's own fight among them. So for most players Aurora Veil is a tool for one split, and for the player who spends the Ability Patch on a Snow Warning holder it works in every fight from the Galactic split on.

### Which lines could have it

| Line | First owned | Today | Proposed | Why |
|---|---|---|---|---|
| Frosmoth | Candice | level 36 | keep | already counts |
| Alolan Ninetales | Gardenia (Route 211 West, levels 13 to 16) | level 1 only | about 40 | the line's own move in the later games; learned by Candice's split; its hidden Snow Warning makes it the one line that can bring its own snow, through the Patch |
| Delibird | Candice (Route 216 and Acuity Lakefront, level 33) | none | 36 | on the index's list of a poor typing on a low stat total, the lines most at risk of having no niche; 100 Speed makes it a fast Veil setter in Candice's split, a role no other line has there |
| Glaceon, Froslass, Lapras, Walrein, Articuno | Byron to Volkner | none | not recommended | each already has a role; Glaceon with Snow Cloak and Veil in snow would be power creep in exactly Candice's fight |
| Any line, by one single-copy TM in Candice's split | Candice | none | optional | lets the player choose, but costs a place in the TM list of about 100 and an optional trainer to give it |

The recommendation is the first three rows: two learnset entries, data only, with no engine or simulator change. A TM is possible but not recommended. It spreads the move to every compatible line, which is the flattening Ian warns against.

### What it costs and which fights it moves

Half an hour of a routine helper and one landing. It moves the fights where the player can set it: the 31 snow fights, and for a Patched Snow Warning holder every fight from the Galactic split on. Material: Candice, where a Veil set in her blizzard halves her team's damage for five turns, and the Somnu and Moira double. Nothing changes on the trainers' side unless a team is given the move, which would be team design and Ian's call.

## How the numbers were made

The chart options were run through `tools/oxide/balance/defensive_index.py` unchanged, with its chart swapped for each option in a driver script. Each option's run also had Steel's later chart applied. The trainers' and the player's attack weights do not depend on the chart, so only the index terms move. The snow run removes hail's chip immunity from every type and ability. The fights in hail come from the same trainer roster the index uses, with each team's maps read through `splits.trainer_maps` and the four day-of-year weathers resolved as `FieldSystem_GetWeather` does. The Ice members by split, the boss teams' Water, Flying and Ground attacks, and the catch levels come from the trainer files and the encounter tables at `origin/oxide` of 2026-11-03 (303b3665337).
