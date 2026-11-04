# Candice's rebuild: Froslass in the hail

Ian rejected the first build on 2026-11-03: "it doesn't scream of being either and ice gym or having Candice's iconic froslass. No hail-specific abilities, two of the ice types are ice/water, a full 3 water types, etc." This is the rebuild from scratch, erring on the side of too hard, aimed at about 80 to 90 percent won with three or more faints on the scorer. It is saved in her file on the branch `overseer-candice-build`. Nothing on this page has been played in game, and the scorer has not given it a full reading. Its cheap checks ran after the Ice levers landed on `oxide` (10d22b3da29), and their results are in the stage 2 section. Against the six the scorer chose to beat the first build on each box, the rebuild is won 55 percent of the time with 4.58 faints. The first build on the same levers is won 96 percent of the time with 2.31 faints. The check is one-sided, so only the Overseer's full reading can say where she lands. The first build and its reading stay below as the record.

## Summary

Every member is an Ice type in her room's permanent hail, and four of the six read the weather through their own ability. Froslass is back as her signature and her ace. Only Walrein is a Water type, and there is no off-type at all.

| Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---:|---|---|---|---:|---|
| Frosmoth (lead) | 53 | Ice Scales | Focus Sash | Bold | 90 | Aurora Veil, Quiver Dance, Blizzard, Giga Drain |
| Castform | 54 | Forecast | Expert Belt | Modest | 129 | Weather Ball, Fire Blast, Hydro Pump, Thunderbolt |
| Walrein | 54 | Ice Body | Chople Berry | Adamant | 91 | Curse, Waterfall, Ice Fang, Earthquake |
| Articuno | 54 | Snow Cloak (hidden) | Lax Incense | Calm | 113 | Hurricane, Freeze-Dry, Roost, Toxic |
| Mamoswine | 55 | Thick Fat | Life Orb | Jolly | 121 | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Froslass (ace) | 56 | Snow Cloak | BrightPowder | Timid | 159 | Blizzard, Shadow Ball, Double Team, Destiny Bond |

The AI flags are Basic, Evaluate Attack, Expert and Check HP. No item or nature repeats, and no move is a one-hit KO.

Each member's job, and what it is built to draw in. The trainer AI's replacement trace in stage 2 bore out the draws but two: the AI sends Froslass at Bronzong and Rotom, and Walrein at Corviknight, where the design meant Castform.

| Member | Job | The player's answers it draws in or beats |
|---|---|---|
| Frosmoth | Sets Aurora Veil on turn 1 behind its Sash, so the team takes half damage for five turns; Ice Scales halves special hits again, and Quiver Dance follows if it is given the turn | Its four-times weaknesses, the Rock and Fire attackers (Glimmora, Garganacl, Golem, Bastiodon; Cinderace, Houndoom, Rapidash, Talonflame), whose switch-ins then meet Mamoswine and Walrein under the Veil |
| Castform | Forecast makes it an Ice type on entry; Weather Ball is a 100-power Ice hit with the type bonus, and three covers on an Expert Belt | The Steel walls (Fire Blast into Bronzong, Metagross and Corviknight; Thunderbolt into Empoleon), the Waters (Thunderbolt), the Fire and Rock types (Hydro Pump) |
| Walrein | A Curse wall: Ice Body heals a sixteenth a turn in the hail, and snow gives it half again its Defense against physical hits | The Fire and Rock answers (Waterfall, Earthquake); the Chople Berry takes one Fighting hit |
| Articuno | An evasive staller: Snow Cloak and the Lax Incense, with Roost and Toxic | The Fighting, Grass and Bug answers (Hurricane), the Waters (Freeze-Dry) |
| Mamoswine | The physical breaker, Thick Fat against Fire | The Steel, Rock, Fire, Electric and Poison answers (Earthquake; Stone Edge for the Flying types Earthquake misses, Talonflame first); Ice Shard picks off the fast and the weakened |
| Froslass | The signature ace and the evasion stack: Snow Cloak, BrightPowder and Double Team, with Destiny Bond for the last blow | The Fighting and Normal answers, which cannot touch it; under Check HP its Destiny Bond waits until it is low |

The hail is the team's case, member by member. Blizzard never misses in it (Frosmoth's and Froslass's), Weather Ball turns Ice and doubles, Ice Body heals Walrein, Snow Cloak cuts every hit on Froslass and Articuno by a fifth before their items cut it again, Aurora Veil works only in it, and under the snow lever all six take physical hits on half again their Defense. Against an unboosted Froslass a 100-accuracy move lands 72 percent of the time; after one Double Team, 54 percent. Under the chart lever the player's Water moves are resisted by five of the six, Walrein twice over; Mamoswine takes them neutral.

Phobos and Deimos 3 (the HQ lobby, a helper's draft Ian will redraft) gave up its Froslass. Deimos's ace at 57 is now a Banette with Cursed Body, a Spell Tag and Adamant, on Icy Wind, Shadow Claw, Sucker Punch and Will-O-Wisp. It keeps the Ghost type, the Icy Wind and the Will-O-Wisp that Froslass gave the double, so Deimos still slows and the pair still burns; Banette, a cursed doll, keeps the dread. It runs at 119 where Froslass ran at 162, so Galvantula (157) is now Deimos's fastest.

Ian's decisions:

1. The evasion stack. Froslass with Snow Cloak, BrightPowder and Double Team, and Articuno with Snow Cloak and the Lax Incense (recommended, by his "no holds barred for evasion stacking"); or Froslass without Double Team (Will-O-Wisp instead); or Articuno on Leftovers.
2. Castform in the seat Kaizo's Regice held (recommended: Forecast is the hail ability the first build's list missed, and its covers answer the Steel walls), or Regice (Ice Body, Explosion), a second legendary beside Articuno.
3. Frosmoth leading with Aurora Veil, beside Ace Trainer Brenna's Veil Ninetales in the same gym (recommended: a different setter, with Ice Scales and Quiver Dance behind it), or Alolan Ninetales leading as Brenna's does, or Delibird, which the Ice proposal gives Veil at 36.
4. Deimos 3's ace: Banette (recommended), or Absol, Deimos's own disaster Pokemon from Pal Park, with Icy Wind by tutor.
5. Deimos 2 at Pal Park still carries a Froslass at 48, two splits before Candice. Keep it, since Froslass is the one exception to the nearby-boss rule (recommended), or replace it too.
6. A simulator gap, which needs Ian's approval to fix. The simulator's own accuracy check (`fightsim.Battle.accuracy_hits`) leaves out Snow Cloak, Sand Veil, the BrightPowder and the Lax Incense; the scorer's (`perfectline.accuracy_hits`) applies all four. None of this page's checks plays through the simulator's path. The full reading, the counterpiece check and the AI-picks probe all play through the scorer's, which applies the evasion. The matchup screen and the replacement trace roll no accuracy at all. Fix it with a test that fails first (recommended), or leave it, since no check of Candice's reaches it.

If the reading comes back harder than Ian wants, the dials, softest first: Double Team out for Will-O-Wisp; the Lax Incense for Leftovers; Walrein's Curse for Surf; Mamoswine's Life Orb for the Never-Melt Ice.

Next steps:

| Step | Who | Time |
|---|---|---|
| The Ice levers land on `oxide` | the Overseer | already under way |
| Stage 2: Speed tiers, the matchup screen, the probe, the counterpiece check on a tree rebuilt for the levers | this helper | done (2026-11-03) |
| The full reading on goal 3's three boxes | the Overseer, on the scorer | 2.5 to 4 hours of machine time |
| Ian's answers to the six decisions | Ian | 10 minutes |
| The playtest, with nerfs from the dials if it is too hard | Ian | the fight itself |

## Why each set is as it is

Kaizo's Candice, for reference, is Froslass (Spikes, Sheer Cold), a Dragon Dance Lapras, Articuno (Sheer Cold), Regice (Rock Polish, Explosion), Mamoswine (Head Smash) and Bronzor. The rebuild keeps her structure, an all-Ice six with Froslass, Articuno and Mamoswine kept, and translates it twice. Into Oxide's Generation 5 and later pool: Freeze-Dry and Hurricane on Articuno, Aurora Veil and Frosmoth, Weather Ball and Forecast, Curse on Walrein in the Dragon Dance Lapras's setup seat, Life Orb, Expert Belt and the Chople Berry. Down to Oxide's difficulty: no Sheer Cold, no Head Smash, Destiny Bond as the one trade. Regice's seat went to Castform, and Bronzor's to Frosmoth, the Veil setter. Kaizo's Froslass carried Snow Cloak, and Ian's ruling of 2026-11-03 frees evasion for Candice, so Froslass keeps it and Articuno takes its own hidden one, each with an evasion item.

Frosmoth leads because Aurora Veil is the hail's strongest tool and needs one turn. The AI scores Veil as it scores Reflect, a little higher at full HP and after the player's last move was an attack, and forbids it outside hail; in her room it is always hailing. The Sash makes the turn certain against the Rock and Fire leads that would otherwise one-shot it. Bold is for those physical Rock hits. Giga Drain is for the Rock and Ground answers that wall Blizzard.

Castform reaches Ice through Forecast, which the simulator runs (`fightsim.forecast`), and its Weather Ball reads Ice in hail. Ian named it as missing from the first build's list. Its 120 Special Attack and 100 Speed (Oxide's values) make it the fastest attacker after Froslass and the special breaker the Steel walls cannot sit in front of. Modest, since Timid is Froslass's.

Walrein is the team's one Water type. It answers the Fire attackers, Ice's commonest counter, which every other member but Mamoswine fears. Curse turns it into a physical wall that grows, which suits a snow fight where the player's answers to Ice are mostly physical; Check HP stops it setting up below 70 percent. The Chople Berry is for Machamp's or Heracross's first Close Combat.

Articuno's Snow Cloak is its hidden ability (slot 3 in the trainer file). Hurricane and Freeze-Dry are on no list of its, so both go on its own egg list by the egg-list rule, Articuno being a first stage of its own, and in `learnrewrite.IAN_EGG_MOVES`. Toxic is for the bulky walls it cannot hurt (Snorlax, Quagsire, Milotic); Calm is for the special Fire and Fighting hits.

Mamoswine keeps the first build's moves, which carried its knockouts there, with a Life Orb now that Alolan Ninetales has gone. Froslass is the ace at the cap and Candice's last Pokemon, as in Platinum. Double Team is legal by its old TM, and Destiny Bond by Snorunt's egg list.

Check HP is chosen for the setup and the trade: it discourages Quiver Dance, Curse and Double Team at 70 percent or less and Roost above it, and a faster Froslass bonds 0 percent of the time above 70 percent and 80 percent at 30 or less (`battle-ai/flags-guide.md`). Weather does nothing without a weather move. Harassment needs two moves from its table and the team has none. Risky would make a healthy Froslass bond half the time. Prioritize Extremes would lift every status move here to near-certain, which is a dial for later, not a default.

The first build's two egg entries, Shell Smash for Shellder and Freeze-Dry for Lapras, left with the Cloyster and Lapras they served; no other trainer uses either.

No member repeats a species from the bosses near her (the table in the first build's record below), checked on the saved trees: Frosmoth, Castform, Walrein, Articuno and Mamoswine stand on no boss's team, and Froslass is Ian's exception. Five of the six also stand on her own gym trainers (Anton's Articuno and Mamoswine, Sergio's Frosmoth, Brenna's Walrein, Savannah's Froslass, Isaiah's Mamoswine), as an Ice gym's trainers would.

## How the files were made

`/tmp/candice-rebuild/apply.py` writes both teams through `tools/oxide/encounters/trainers.save`, which ran the trainer lint (no findings for either file) and the packer. Move legality was read with the first build's checker (the Kaizo study's, with the TMs from before the TM pass). The Speed column is each member's stat at its level, nature and full IVs, before any check against the boxes.

| Check | Result |
|---|---|
| Trainer lint and packer, both files | no findings; packed |
| `make rom` | built |
| test_trainers, test_learncheck, test_learnrewrite, test_learnstudy, test_b1 | 44/44, 18/18, 6/6, 2/2, 50/50 |
| Speed tiers, matchup screen, probe, counterpiece check | the stage 2 section |

## Stage 2: the cheap checks on the Ice levers (2026-11-03)

Every check here ran on `overseer-candice-build` after it merged `oxide` at 10d22b3da29. That tree carries the three levers: Ice resists Water, snow replaces hail (no chip, and Ice types take physical hits on half again their Defense), and Delibird and Alolan Ninetales learn Aurora Veil. Each check used goal 3's three boxes as the first build's reading built them (run `candice-3ff0d0008`), so the rebuild and the first build were measured on the same boxes. The scripts are in `/tmp/candice-rebuild/` and their outputs in `/tmp/candice-rebuild/out/`. Each ran under `tools/oxide/capped`, and none wrote to `res/`.

### The counterpiece check

The check plays a team against the six the scorer chose to beat the first build on each box. It uses the scorer's own planner on each box: 75 fights at real odds and 25 very unlucky. The old reading's tree, `tree-candice-3ff0d0008`, could not be reused, since it predates the levers. Two trees were made instead. `~/oxide-trials/goal3/tree-candice-rebuild-5c0fa6b0e` is a `git archive` of this branch at 5c0fa6b0e6c, so it holds the levers and the rebuild. `~/oxide-trials/goal3/tree-candice-first-on-levers` is a `plcounter tree` copy of the first with the first build's file (3ff0d0008a3) put back. The driver refuses a box whose members, level, starter or history differ from the reading's, and every box rebuilt without a refusal.

| Box | The old reading (first build, before the levers): won, faints, clean | First build on the levers: won, faints, clean; very unlucky won, faints | Rebuild on the levers: won, faints, clean; very unlucky won, faints |
|---|---|---|---|
| 1 (Turtwig) | 96, 2.16, 20 | 97, 2.48, 19; 72, 4.08 | 88, 3.52, 4; 60, 4.44 |
| 2 (Scorbunny) | 92, 2.88, 0 | 92, 2.97, 0; 76, 3.64 | 16, 5.69, 0; 16, 5.76 |
| 3 (Piplup) | 93, 2.25, 15 | 100, 1.47, 25; 92, 2.04 | 61, 4.52, 0; 32, 5.60 |
| All three | 94, 2.43, 12 | 96, 2.31, 15 | 55, 4.58, 1 |

The levers alone barely moved the first build. Against these sixes it reads the same or easier, and the check marks all three of its boxes "too easy (old six wins as often)". The rebuild reads far harder against the same sixes, and the check gives "reading decides" on all three boxes. The check is one-sided, so these numbers are a floor for the player, not Candice's reading. A full team search can only find the player a stronger six than these, which were chosen against Cloyster, Chandelure and Gastrodon. Box 2's six leans on Manaphy, Heracross and Cinderace, which Walrein and Articuno meet, and those two made most of her knockouts there. The six the screen prefers for box 2 against the rebuild (below) is a different one. A full reading may still land under 80 percent won. If it does, the dials are on the summary page.

Her knockouts over each box's 75 fights at real odds, most first:

| Box | Her knockouts | The player's six, and what it lost |
|---|---|---|
| 1 | Mamoswine 101, Articuno 67, Froslass 54, Walrein 30, Castform 11, Frosmoth 1 | Manaphy 59, Abomasnow 51, Mamoswine 41, Bastiodon 38, Snorlax 38, Houndoom 37 |
| 2 | Walrein 108, Articuno 79, Frosmoth 78, Mamoswine 68, Froslass 59, Castform 35 | Glimmora 73, Arboliva 72, Bronzong 72, Cinderace 71, Heracross 70, Manaphy 69 |
| 3 | Froslass 75, Frosmoth 73, Articuno 62, Mamoswine 56, Walrein 47, Castform 26 | Leavanny 73, Machamp 57, Glimmora 56, Bronzong 56, Manaphy 50, Bastiodon 47 |

The six that played on each box, with the reading's moves and items:

| Box | Six (item; moves) |
|---|---|
| 1 | Abomasnow (Miracle Seed; Wood Hammer, Hammer Arm, Ice Punch, Rock Tomb), Bastiodon (Rock Incense; Rock Blast, Hard Press, Take Down, Taunt), Houndoom (Black Glasses; Fiery Wrath, Flamethrower, Mud Shot, Smog), Manaphy (Mystic Water; Aura Sphere, Bubble Beam, Signal Beam, Icy Wind), Snorlax (Silk Scarf; Giga Impact, Crunch, Belly Drum, Bulldoze), Mamoswine (Soft Sand; Earthquake, Brick Break, Take Down, Ancient Power) |
| 2 | Cinderace (Sitrus Berry; Flare Blitz, Bounce, Super Fang, Taunt), Arboliva (Miracle Seed; Energy Ball, Mud Shot, Strength Sap, Alluring Voice), Bronzong (Mind Plate; Mirror Shot, Future Sight, Bulldoze, Iron Defense), Glimmora (Poison Barb; Power Gem, Energy Ball, Flash Cannon, Sludge Wave), Heracross (Fist Plate; Close Combat, Bulldoze, Bulk Up, Megahorn), Manaphy (Mystic Water; Aura Sphere, Bubble Beam, Signal Beam, Icy Wind) |
| 3 | Machamp (Fist Plate; Close Combat, Throat Chop, Fire Punch, Bulk Up), Bastiodon (Rock Incense; Rock Blast, Hard Press, Take Down, Taunt), Leavanny (Miracle Seed; Leaf Blade, Throat Chop, Sticky Web, X-Scissor), Bronzong (Mind Plate; Mirror Shot, Future Sight, Bulldoze, Iron Defense), Glimmora (Poison Barb; Power Gem, Energy Ball, Flash Cannon, Sludge Wave), Manaphy (Mystic Water; Aura Sphere, Bubble Beam, Signal Beam, Icy Wind) |

### The matchup screen and the probe

Both teams were run on the same three boxes on the levers. The screen is the best six's score, and lower is harder. The probe is the rough wins of 150 greedy fights against the screen's best six and against the six its top 20 take most.

| Team | Screen, boxes 1 to 3 | Probe wins, boxes 1 to 3 (best six / common six) |
|---|---|---|
| First build | 16.55, 15.80, 15.80 | 31 / 26, 28 / 17, 23 (one six) |
| Rebuild | 16.65, 14.85, 14.85 | 36 / 33, 66 / 64, 40 / 21 |

These two disagree with the counterpiece check, and both have known blind spots here. The screen scores each move at its listed accuracy. It cannot see Snow Cloak, the evasion items, Double Team or Blizzard's sure hit in hail, and Aurora Veil, Curse and Roost are not in it either. The probe's greedy player never switches and attacks with its hardest hit 85 percent of the time. So it never plays round Destiny Bond or a Curse. Its numbers mean nothing alone, as on every page that uses it. The screen and the probe would read her easier than she is. The counterpiece check plays the scorer's planner and sees all of it.

The screen's best six against the rebuild: box 1, Probopass, Alolan Ninetales, Abomasnow, Bastiodon, Houndoom, Snorlax; box 2, Rapidash, Alolan Ninetales, Bronzong, Bastiodon, Glimmora, Glalie; box 3, Hariyama, Bastiodon, Bronzong, Gothitelle, Frosmoth, Glalie. The six its top 20 take most: box 1, Abomasnow, Houndoom, Probopass, Bastiodon, Garganacl, Metagross; box 2, Rapidash, Bronzong, Bastiodon, Glalie, Glimmora, Glaceon; box 3, Hariyama, Bronzong, Glalie, Bastiodon, Frosmoth, Rotom. Houndoom on box 1 and Rapidash on box 2 are in all 20 of the top sixes. Each beats Frosmoth, Castform, Articuno and Froslass one on one, and only Walrein and Mamoswine beat them back. Bronzong is in all 20 on boxes 2 and 3. It walls everything but Castform's Fire Blast (76 to 90 percent) and Froslass's Shadow Ball (64 to 75 percent).

In the probe, Frosmoth opened with Aurora Veil in 113 to 120 of each 150 fights. Its Sash was used in 8 to 45. Froslass used Double Team 86 to 192 times over 150 fights, and Destiny Bond 51 to 117 times. On box 3 Froslass lost its BrightPowder in about one fight in five (32 and 30 of 150).

### What each answer draws in

The trainer AI's own replacement rule (`fightai.replacement`), on every catch the top 20 sixes take, bore out the design. The Rock and Steel walls (Probopass, Bastiodon, Glimmora, Metagross, Empoleon, Glalie) draw Mamoswine. The Fire attackers (Houndoom, Rapidash, Cinderace, Talonflame), Corviknight, Garganacl, Golem, Carbink and Crustle draw Walrein. The Fighting types (Heracross, Hariyama, Machamp, Breloom, Mienshao) draw Articuno. The Waters (Manaphy, Octillery) draw Castform. Abomasnow, Snorlax and the Grass types draw Frosmoth while it stands. Two draws differ from the design. Bronzong and Rotom draw Froslass, not Castform, and Corviknight draws Walrein, not Castform.

### Speed tiers

Each member against every catch of the whole box, held-back versions included.

| Member | Speed | Outspeeds, boxes 1 to 3 (of 87, 93, 96) | At +1 |
|---|---:|---|---|
| Frosmoth | 90 | 42, 46, 42 | 135 after Quiver Dance: 80, 85, 88 |
| Castform | 129 | 76, 83, 87 | |
| Walrein | 91 | 42, 46, 42, ties 7, 6, 11 | falls a stage with each Curse |
| Articuno | 113 | 66, 60, 64 | |
| Mamoswine | 121 | 73, 79, 83 | Ice Shard for the rest |
| Froslass | 159 | 86, 92, 95, and ties Crobat at 159 | |

Faster than Mamoswine on every box are Crobat, Cinderace, Tentacruel and Manaphy. The others are Talonflame, Liepard, Gengar, Staraptor, Scyther, Mienshao, Houndoom and Alolan Ninetales on box 1; Liepard, Floatzel, Rapidash, Staraptor, Lopunny, Alolan Ninetales and Glalie on box 2; and Weavile (153), Salazzle, Floatzel, Lopunny, Castform and Glalie on box 3.

### Which checks meet the simulator's accuracy gap

None of these checks plays through the simulator's own accuracy check (`fightsim.Battle.accuracy_hits`), the one that leaves out Snow Cloak and the evasion items. The probe plays `perfectline.play_turn`. The counterpiece check and the full reading play `plteam.full_reading`. Both route every attack and status move through `perfectline`'s own `attack` and `status_move`, which call `perfectline.accuracy_hits`, and that check applies Snow Cloak, the BrightPowder and the Lax Incense. So the counterpiece numbers above and the Overseer's full reading both see her evasion. The matchup screen and the replacement trace roll no accuracy at all, so their blindness is their own and not this gap. The Speed tiers read no accuracy. The gap's fix is not approved, and nothing here changed it.

### The boxes

Box 1 (Turtwig), 63 catches: Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox, Nidorino, Pawmo, Corviknight, Mandibuzz, Crobat, Talonflame, Probopass, Seaking, Quagsire, Kingler, Tentacruel, Cherrim, Sharpedo, Plusle, Leavanny, Lombre, Alolan Ninetales, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis, Granbull, Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Scyther, Mienshao, Masquerain, Crustle, Onix, Houndoom, Liepard, Toxicroak, Jellicent, Manaphy, Snorlax, Milotic, Altaria, Gastrodon, Cinderace, Octillery, Metagross, Seadra, Corsola, Goodra, Frosmoth, Mamoswine, Jynx, Dewgong. Held-back versions of Torterra, Dustox, Corviknight (two), Talonflame (two), Seaking, Kingler, Sharpedo, Leavanny (two), Lurantis, Granbull, Crawdaunt, Masquerain (two), Snorlax (two), Altaria, Octillery, Metagross, Seadra, Goodra and Mamoswine.

Box 2 (Scorbunny), 64 catches: Cinderace, Whiscash, Staraptor, Masquerain, Lombre, Bibarel, Orbeetle, Liepard, Nidorino, Mandibuzz, Crobat, Rapidash, Donphan, Seaking, Garganacl, Lumineon, Tentacruel, Vespiquen, Arboliva, Tsareena, Leavanny, Primarina, Alolan Ninetales, Bronzong, Nuzleaf, Rotom, Togetic, Bastiodon, Onix, Glaceon, Glimmora, Heracross, Granbull, Glalie, Pachirisu, Gothitelle, Floette, Murkrow, Golem, Vikavolt, Drifblim, Magcargo, Hippowdon, Palossand, Tropius, Floatzel, Sharpedo, Drapion, Lopunny, Manaphy, Skitty, Jellicent, Toxicroak, Ceruledge, Empoleon, Gastrodon, Corsola, Octillery, Lurantis, Milotic, Frosmoth, Mr. Rime, Absol, Dewgong. Held-back versions of Cinderace, Masquerain (three), Orbeetle (three), Liepard (two), Donphan (two), Seaking, Lumineon, Tsareena, Leavanny (two), Bronzong (two), Nuzleaf, Granbull, Gothitelle, Vikavolt (two), Magcargo (two), Palossand, Sharpedo, Drapion and Lurantis.

Box 3 (Piplup), 64 catches: Empoleon, Seaking, Corviknight, Orbeetle, Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Mandibuzz, Crobat, Hariyama, Onix, Roselia, Golem, Kingler, Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom, Lombre, Mothim, Carbink, Vikavolt, Rotom, Togetic, Bastiodon, Salazzle, Glaceon, Crustle, Leavanny, Granbull, Bronzong, Gothitelle, Sinistea, Floette, Happiny, Glimmora, Yanmega, Castform, Quagsire, Garganacl, Palossand, Lopunny, Grapploct, Sharpedo, Gliscor, Qwilfish, Manaphy, Pikachu, Crawdaunt, Altaria, Gastrodon, Cinderace, Lumineon, Metagross, Octillery, Nuzleaf, Floatzel, Frosmoth, Glalie, Weavile, Dewgong. Held-back versions of Empoleon, Seaking, Corviknight (two), Orbeetle (three), Hariyama, Kingler, Breloom (three), Vikavolt (two), Leavanny (two), Granbull, Bronzong (two), Gothitelle, Yanmega, Palossand, Sharpedo, Gliscor (two), Crawdaunt, Altaria, Lumineon, Metagross and Weavile (three).

These are the boxes the first build's page lists below, rebuilt identically: 87, 93 and 96 entries counting the held-back versions.

## The first build, for the record

The first build's decisions below were superseded by Ian's rejection of 2026-11-03 and this rebuild.

Ian asked on 2026-11-03 for a helper to build Candice (Snowpoint Gym, cap 56) as the primary team, erring on the side of too hard, beside his own draft. The team is in her file on the branch `overseer-candice-build` (commit 3ff0d0008a3) and waits on the Overseer's full scorer reading before it lands. Nothing was read by the scorer here, so how hard it reads is a forecast from cheap checks, and the screen and the probe misread this range.

### Summary

The six, lead first. Every member holds its own item and has its own nature. Levels follow Mars 1's shape: the ace at the cap, one at 55, the rest at 53 and 54.

| Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---:|---|---|---|---:|---|
| Cloyster (lead) | 53 | Skill Link | Focus Sash | Adamant | 95 | Spikes, Shell Smash, Icicle Spear, Drill Run |
| Alolan Ninetales | 54 | Magic Guard | Life Orb | Timid | 141 | Nasty Plot, Blizzard, Psyshock, Flamethrower |
| Chandelure | 54 | Flash Fire | Passho Berry | Mild | 108 | Shadow Ball, Fire Blast, Energy Ball, Calm Mind |
| Gastrodon | 53 | Dry Skin | Rindo Berry | Bold | 62 | Earth Power, Surf, Recover, Stealth Rock |
| Lapras | 55 | Serene Grace | Leftovers | Modest | 88 | Blizzard, Freeze-Dry, Hydro Pump, Thunderbolt |
| Mamoswine (ace) | 56 | Thick Fat | Never-Melt Ice | Jolly | 122 | Earthquake, Ice Fang, Ice Shard, Stone Edge |

The AI flags are Basic, Evaluate Attack, Expert and Check HP.

Each member's job. Cloyster lays Spikes behind its Sash, so every switch the player makes costs an eighth of its HP on top of the gym's hail, then smashes if it is given the turn. Ninetales is the answer to the Fighting and Grass types, with Nasty Plot for the free turn their switch hands it. Chandelure is the off-type for the Steel walls, the Fire attackers and the Fighting types: Flash Fire takes the Fire moves, it is immune to Fighting, and its Passho Berry lets it beat Manaphy and the special Waters, which the AI sends it into. Gastrodon is the off-type for the Fire, Rock and Steel types and the Waters: Dry Skin heals from Water moves, Earth Power hits the walls, and it lays Stealth Rock as the hub most answers draw in. Lapras is the bulky Ice that hits the Fire and Rock types with Water and Manaphy with Freeze-Dry. Mamoswine is the ace, hitting 24 or 25 of each box's likely answers for half or more.

The bait order. Cloyster opens and lays hazards into whatever leads. The player's Steel, Rock and Fire answers then draw Gastrodon; Bronzong, Metagross and Corviknight draw Chandelure; the Fighting and Grass answers draw Ninetales; Manaphy draws Chandelure, then Lapras. Each switch pays Spikes and, once Gastrodon has been in, Stealth Rock.

What each answer draws in, by the trainer AI's own replacement rule (`fightai.replacement`, run on each box), and whether the member drawn beats it on the calculator:

| Answer in front | Drawn in | Its hit, the answer's hit back (lowest roll, percent of HP) |
|---|---|---|
| Bastiodon, Probopass, Glimmora, Garganacl, Empoleon, Tentacruel | Gastrodon (Mamoswine once Gastrodon is gone) | Bastiodon 71 to 22, Probopass 67 to 28, Glimmora 144 to 56, Garganacl 59 to 26, Tentacruel 52 to 16 |
| Cinderace, Houndoom, Rapidash | Gastrodon | Cinderace 80 to 50, Houndoom 77 to 39, Rapidash 76 to 36 |
| Bronzong, Metagross, Corviknight | Chandelure | Bronzong 166 to 40, Metagross 202 to 57, Corviknight 190 to 52 |
| Heracross, Machamp, Hariyama, Breloom | Ninetales (Chandelure once it is gone) | Heracross 72 to 64, Machamp 64 to 70, Breloom 206 to 67 |
| Grass answers to Gastrodon (Tsareena, Arboliva, Leavanny, Cherrim) | Ninetales or Chandelure | Tsareena 124 to 66, Leavanny 463 to 55 (Chandelure) |
| Manaphy | Chandelure, then Lapras | Chandelure 60 to 30 with the berry; Lapras 53 to 30 |
| Frosmoth, Abomasnow | Chandelure | Frosmoth 221 to 25, Abomasnow 400 to 39 |

Machamp is the one pairing the drawn member does not clearly win; Ninetales outspeeds it and it is close.

The checks, all on the saved file.

| Check | Result |
|---|---|
| Legality | every move legal; Shell Smash added to Shellder's egg list and Freeze-Dry to Lapras's, both in `learnrewrite.IAN_EGG_MOVES` |
| Trainer lint, packer | no findings; packed |
| test_b1, test_trainers, test_learncheck, test_learnrewrite, test_learnstudy | 50/50, 44/44, 18/18, 6/6, 2/2 |
| `make rom` | built |
| Gate (`integrate.sh --verify-only`) on 3ff0d0008a3 | 53 passed; 1 failed, sync-docs, which refuses off `oxide` by design |
| Matchup screen's best six, boxes 1 to 3 (background) | 15.55, 15.35, 14.50; today's team 17.40, 21.05, 20.05 |
| AI-picks probe, rough wins of 150 against the screen's six and the common six (background) | 15 / 12, 17 / 12, 18; today's team 51, 41 / 51 / 60, 63 |
| Speed tiers | below |

The screen falls by 2 to 6 points a box, about Byron's shape C3 and short of Cyrus 1's redesign (11.7, 11.6, 10.9), which read 82. The screen cannot see Spikes, Stealth Rock or the hail, which are much of this team's case. The probe's greedy player never switches, so it overrates every team against a switching player; only the drop from today's team means anything.

What Ian decides is listed at the end. The next step is the Overseer's full reading, two and a half to four hours of machine time. If it reads harder than Ian wants, the dials are listed there too, softest first.

### The reading (2026-11-03)

The scorer read this team on goal 3's three boxes (run `candice-3ff0d0008`, tree at 3ff0d0008a3, on today's hail and the old Steel chart). It reads easier than the aim of 80 to 90 percent won with three or more faints, though harder than anything Ian has drafted:

| Box | Six the scorer chose | Won | Faints | Clean | Very unlucky won, faints |
|---|---|---:|---:|---:|---|
| 1 (Turtwig) | Abomasnow, Bastiodon, Houndoom, Manaphy, Snorlax, Mamoswine | 96 | 2.16 | 20 | 96, 3.24 |
| 2 (Scorbunny) | Cinderace, Arboliva, Bronzong, Glimmora, Heracross, Manaphy | 92 | 2.88 | 0 | 84, 3.00 |
| 3 (Piplup) | Machamp, Bastiodon, Leavanny, Bronzong, Glimmora, Manaphy | 93 | 2.25 | 15 | 88, 2.64 |
| All three | | 94 | 2.43 | 12 | |

Her knockouts over each box's 75 fights at real odds, most first: box 1, Lapras 71, Mamoswine 61, Ninetales 20, Gastrodon 8, Chandelure 2; box 2, Mamoswine 83, Ninetales 66, Lapras 31, Chandelure 24, Gastrodon 11, Cloyster 1; box 3, Lapras 44, Mamoswine 41, Chandelure 40, Ninetales 21, Cloyster 18, Gastrodon 5. The lead and the hub do the least: Cloyster's Spikes and Gastrodon's Stealth Rock carry their case, and the knockouts come from Lapras, Mamoswine and Ninetales. Manaphy is in all three sixes, and Bronzong or Bastiodon in each.

Three pending changes would each make her harder without touching her file. Steel's later chart (landed at 04c99bc85) makes Chandelure's Shadow Ball neutral on the two Bronzong sixes. The Ice proposal's Water and Flying resistances would halve Manaphy's Water hits on Lapras, Cloyster and Mamoswine. Snow in place of hail would stop the chip on Chandelure and Gastrodon and give her four Ice types 1.5 times Defense against Machamp, Heracross and the rest.

### Why each set is as it is

Ian's theme is four or five Ice types and one or two off-types that answer Ice's counters, chosen with the gym's permanent hail in mind. Four of the six are Ice types and take no hail. Of the two off-types, neither has Overcoat, Magic Guard, Ice Body or Snow Cloak, so each takes a sixteenth a turn; Gastrodon has Recover and Chandelure is in for short stays. No Pokemon on the team has Snow Cloak, so the team carries no evasion at all.

Cloyster's lead job is Kaizo's (Froslass's Sash and Spikes), translated: Froslass is on Deimos's HQ team, and Cloyster gives the same Sash and Spikes with Shell Smash, a Generation 5 move, in Sheer Cold's place. Drill Run hits Bastiodon and Probopass four times over, and Metagross, Empoleon, Glimmora and the Fire types twice. The AI picks Spikes on most first turns and Shell Smash on about a fifth.

Ninetales keeps Magic Guard, so the Life Orb costs it nothing and nothing chips it. Psyshock is for Tentacruel and the Fighting types, Flamethrower for the Steel types. Brenna, the gym's first guard, already carries an Alolan Ninetales with Aurora Veil, so Candice's is the attacker instead.

Chandelure's Passho Berry replaced an Expert Belt after the first runs: with the belt it lost to Manaphy, the special Water every box carries and the answer the AI sends it into. With the berry it takes Manaphy's Water hit at half and wins with Energy Ball.

Gastrodon's Stealth Rock replaced Sludge Bomb, which the AI barely used. It is the member most answers draw in, so the Rocks go down where the player is switching most, and they hit the Fire types and Frosmoth hard.

Lapras took Regice's seat. Regice, with Rock Polish, Blizzard, Thunderbolt and Focus Blast (Kaizo's Regice with Focus Blast for Sheer Cold and no Explosion), was beaten by nine answers a box and rarely drawn in. Lapras hits 20 to 24 answers a box for half or more and is beaten by few. Freeze-Dry is its Manaphy and Tentacruel move; Serene Grace doubles every secondary effect.

Mamoswine took Ice Fang over Icicle Spear for a steady 90, and Stone Edge back over Knock Off, which the AI never picked in 300 fights.

No member carries a trade move, so Check HP is not there for one. The flags guide says Check HP makes setup and healing better timed: the AI stops setting up at 70 percent or less and stops Recovering above it, and this team has Shell Smash, Nasty Plot, Calm Mind and Recover. Weather does nothing (no weather move), Harassment needs two moves from its table (only Spikes is), Risky has no critical-hit idea to serve, and Prioritize Extremes is for teams that lean mostly on status, which this one does not.

Kaizo's Candice, for reference: Froslass (Spikes, Sheer Cold), a Dragon Dance Lapras, Articuno (Sheer Cold), Regice (Rock Polish, Explosion), Mamoswine (Head Smash) and Bronzor. Translated twice: into Oxide's pool (Shell Smash, Freeze-Dry, Chandelure and Gastrodon, Life Orb and the resist berries), and down to Oxide's difficulty (no Sheer Cold, no Explosion, no Snow Cloak).

### Speed tiers

Each member against the whole box, held-back versions included. Box 1 has 87, box 2 93 and box 3 96; each box's fastest is Crobat at 159.

| Member | Speed | Outspeeds, boxes 1 to 3 | Notes |
|---|---:|---|---|
| Cloyster | 95 | 50, 53, 54 | 190 at +2: every catch |
| Ninetales | 141 | 81, 86, 88 | |
| Chandelure | 108 | 60, 56, 60 | |
| Gastrodon | 62 | 11, 17, 15 | |
| Lapras | 88 | 39, 46, 39 | |
| Mamoswine | 122 | 73, 79, 83 | Ice Shard for the rest |

Oxide has no Slush Rush, so the hail gives no Speed. Faster than Mamoswine on most boxes are Cinderace (146), Houndoom (131), Rapidash (136), Tentacruel and Manaphy (125), and Weavile on box 3 (153). Only Cinderace, Talonflame, Floatzel, Liepard, Weavile and Crobat outspeed Ninetales.

### The boxes

Goal 3's boxes for Candice's place (`plgoal3 --box candice <seed>`, run name `candice-build-study`, seeds 1 to 3), on a tree of `origin/oxide` at 291689d989, each at 56 with no earlier reading behind it.

Box 1 (Turtwig), 63 catches: Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox, Nidorino, Pawmo, Corviknight, Mandibuzz, Crobat, Talonflame, Probopass, Seaking, Quagsire, Kingler, Tentacruel, Cherrim, Sharpedo, Plusle, Leavanny, Lombre, Alolan Ninetales, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis, Granbull, Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Scyther, Mienshao, Masquerain, Crustle, Onix, Houndoom, Liepard, Toxicroak, Jellicent, Manaphy, Snorlax, Milotic, Altaria, Gastrodon, Cinderace, Octillery, Metagross, Seadra, Corsola, Goodra, Frosmoth, Mamoswine, Jynx, Dewgong. Held-back versions of Torterra, Dustox, Corviknight (two), Talonflame (two), Seaking, Kingler, Sharpedo, Leavanny (two), Lurantis, Granbull, Crawdaunt, Masquerain (two), Snorlax (two), Altaria, Octillery, Metagross, Seadra, Goodra and Mamoswine.

Box 2 (Scorbunny), 64 catches: Cinderace, Whiscash, Staraptor, Masquerain, Lombre, Bibarel, Orbeetle, Liepard, Nidorino, Mandibuzz, Crobat, Rapidash, Donphan, Seaking, Garganacl, Lumineon, Tentacruel, Vespiquen, Arboliva, Tsareena, Leavanny, Primarina, Alolan Ninetales, Bronzong, Nuzleaf, Rotom, Togetic, Bastiodon, Onix, Glaceon, Glimmora, Heracross, Granbull, Glalie, Pachirisu, Gothitelle, Floette, Murkrow, Golem, Vikavolt, Drifblim, Magcargo, Hippowdon, Palossand, Tropius, Floatzel, Sharpedo, Drapion, Lopunny, Manaphy, Skitty, Jellicent, Toxicroak, Ceruledge, Empoleon, Gastrodon, Corsola, Octillery, Lurantis, Milotic, Frosmoth, Mr. Rime, Absol, Dewgong. Held-back versions of Cinderace, Masquerain (three), Orbeetle (three), Liepard (two), Donphan (two), Seaking, Lumineon, Tsareena, Leavanny (two), Bronzong (two), Nuzleaf, Granbull, Gothitelle, Vikavolt (two), Magcargo (two), Palossand, Sharpedo, Drapion and Lurantis.

Box 3 (Piplup), 64 catches: Empoleon, Seaking, Corviknight, Orbeetle, Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Mandibuzz, Crobat, Hariyama, Onix, Roselia, Golem, Kingler, Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom, Lombre, Mothim, Carbink, Vikavolt, Rotom, Togetic, Bastiodon, Salazzle, Glaceon, Crustle, Leavanny, Granbull, Bronzong, Gothitelle, Sinistea, Floette, Happiny, Glimmora, Yanmega, Castform, Quagsire, Garganacl, Palossand, Lopunny, Grapploct, Sharpedo, Gliscor, Qwilfish, Manaphy, Pikachu, Crawdaunt, Altaria, Gastrodon, Cinderace, Lumineon, Metagross, Octillery, Nuzleaf, Floatzel, Frosmoth, Glalie, Weavile, Dewgong. Held-back versions of Empoleon, Seaking, Corviknight (two), Orbeetle (three), Hariyama, Kingler, Breloom (three), Vikavolt (two), Leavanny (two), Granbull, Bronzong (two), Gothitelle, Yanmega, Palossand, Sharpedo, Gliscor (two), Crawdaunt, Altaria, Lumineon, Metagross and Weavile (three).

No six played a scored fight, since nothing was read by the scorer. The sixes the cheap checks played against the saved team were these.

| Box | The screen's best six (the probe's first six) | The six its top 20 take most (the probe's second) |
|---|---|---|
| 1 | Probopass, Abomasnow, Glimmora, Houndoom, Manaphy, Snorlax | the same six |
| 2 | Cinderace, Arboliva, Bronzong, Glimmora, Heracross, Manaphy | Heracross, Manaphy, Glimmora, Bronzong, Cinderace, Bastiodon |
| 3 | Breloom, Bastiodon, Bronzong, Glimmora, Manaphy, Frosmoth | Glimmora, Manaphy, Bastiodon, Cinderace, Bronzong, Leavanny |

The likely answers, by the kinds the brief names, as each box holds them:

| Kind | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Steel and Rock walls | Corviknight, Probopass, Bastiodon, Metagross, Garganacl, Glimmora, Golem, Carbink, Crustle, Onix | Bronzong, Bastiodon, Empoleon, Garganacl, Glimmora, Golem, Onix | Empoleon, Corviknight, Bronzong, Bastiodon, Metagross, Garganacl, Glimmora, Golem, Carbink, Crustle, Onix |
| Fire attackers | Cinderace, Houndoom, Talonflame | Cinderace, Rapidash, Ceruledge, Magcargo | Cinderace, Salazzle |
| Fighting attackers | Mienshao | Heracross, Lopunny | Machamp, Hariyama, Breloom, Grapploct, Lopunny |
| Special Waters | Manaphy, Tentacruel, Jellicent, Milotic, Octillery, Gastrodon | Manaphy, Primarina, Tentacruel, Jellicent, Milotic, Octillery, Gastrodon | Manaphy, Tentacruel, Octillery, Gastrodon |
| Others the screen takes against this team | Snorlax, Abomasnow, Frosmoth, Cherrim, Crawdaunt | Frosmoth, Tsareena, Arboliva, Leavanny, Glalie, Rotom | Frosmoth, Leavanny, Glalie, Floatzel, Rotom, Weavile |

Manaphy is in 16 to 20 of the screen's top 20 sixes on every box, Glimmora in 10 to 19, Bronzong in 9 to 13 on boxes 2 and 3.

### Species left out

No member repeats a species from the bosses near her, read from each file on `origin/oxide` and, for Byron, Ian's redraft on `origin/overseer-byron-ian`.

| Fight | Species left out |
|---|---|
| Mars 2 | Liepard, Crobat, Incineroar, Galarian Zapdos, Mesprit, Purugly |
| Saturn 1 | Glimmora, Mantine, Naganadel, Tropius, Azelf, Salazzle |
| Hesperid 1 | Weezing, Sceptile, Girafarig, Sudowoodo, Wigglytuff, Chatot |
| Somnu and Moira | Swalot, Stantler, Gardevoir, Abomasnow, Mr. Rime, Glaceon |
| Cyrus 1 | Swampert, Honchkrow, Porygon-Z, Electivire, Magmortar, Salamence |
| Byron (Ian's redraft) | Metagross, Galvantula, Hisuian Goodra, Kartana, Empoleon, Celesteela |
| Barry 5 | Staraptor, Primeape, Greninja, Snorlax, Turtonator, Torterra, Serperior, Infernape |
| Cyrus 2 | Skarmory, Magnezone, Dusknoir, Houndoom, Suicune, Weavile |
| Saturn 2 | Uxie, Lickilicky, Wobbuffet, Wailord, Rhyperior, Toxicroak |
| Phobos and Deimos 3 | Granbull, Mawile, Arcanine, Arbok, Froslass |
| Boreas and Laverna 2 | Talonflame, Pidgeot, Yanmega, Sableye, Kecleon |
| Argo and Hesperid at the HQ | Claydol, Cofagrigus, Bronzong, Relicanth, Polteageist, Spinda, Spiritomb, Pinsir |

That leaves Oxide's fully evolved Ice types as Alolan Ninetales, Articuno, Cloyster, Delibird, Dewgong, Frosmoth, Glalie, Jynx, Lapras, Mamoswine, Regice and Walrein. Of today's team, Froslass, Glaceon and Abomasnow were out by this rule; Walrein and Articuno were left for Lapras, and Articuno also for its Snow Cloak.

### Ian's decisions

1. Chandelure and Gastrodon as the two off-types (recommended), against a Steel type such as Lucario, which Rock and Fire answers would share less with the Ice core but which the hail chips the same.
2. Check HP for timing setup and Recover (recommended), or the three base flags alone.
3. Cloyster leading, with Brenna's Aurora Veil Ninetales already in the gym (recommended), or Ninetales leading with Veil as Brenna's does.
4. If the reading reads harder than he wants, the dials softest first: Stealth Rock back to Sludge Bomb; Ninetales's Life Orb for a Sitrus Berry; Cloyster's Shell Smash for Rock Blast.

### How the numbers were made

The scripts are in `/home/ian/.claude/jobs/382760ce/tmp/candice-build/`, adapted from the Candice pass's `bc.py` and `checks.py` and the Byron redesign's shapes, run under `tools/oxide/capped`; none writes to `res/`. `shapes.py` holds the five shapes tried (A to E; E is the build), and `bc.swap_party` puts one into Candice's file in memory. `checks.py` prints the six as the simulator builds it, the screen's top 20, the margins, the Speed tiers against each whole box, the replacement trace (`fightai.replacement` on a battle from `perfectline.make_battle`), the damage both ways and the AI-picks probe of 150 rough fights against two sixes. `matrix.py` prints each member's best hit on every likely answer and back, from the scorer's own calculator rows, with the screen's four moves for each answer. `apply.py` saved shape E through `trainers.save`. `legal.py` is the Kaizo study's legality checker with the TMs from before the TM pass. The saved file's checks are `out/saved-1.txt` to `out/saved-3.txt` and `out/saved-m-1.txt` to `out/saved-m-3.txt`. The hail is goal 3's own: `plscore.prepare` starts her fight in it (`candice-split.md`).

The shapes on the probe and the screen, box by box, for the record:

| Shape | What changed | Screen, boxes 1 to 3 | Probe rough wins |
|---|---|---|---|
| Today | the file before | 17.40, 21.05, 20.05 | 51, 41 / 51 / 60, 63 |
| A | Regice in Lapras's seat, Rock Blast for Drill Run, Expert Belt Chandelure | 16.30, 17.55, 16.90 | 33 / 60, 56 / 53, 42 |
| B | Lapras for Regice | 16.00, 17.40, 17.25 | 16 / 36, 10 / 37, 7 |
| C | Stealth Rock, Psyshock, Freeze-Dry | 15.55, 16.50, 15.65 | 21, 19 / 29, 25 / 12, 16 |
| D | Passho Berry, Knock Off | 15.55, 15.35, 14.50 | 28 / 17, 16 / 14, 9 |
| E, saved | Stone Edge back, Check HP | 15.55, 15.35, 14.50 | 15 / 12, 17 / 12, 18 |
