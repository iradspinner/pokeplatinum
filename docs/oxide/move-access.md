# Move access

This sorts every move in the game by who can have it, to answer Ian's question of 2026-10-14: how many moves sit in the data that no player and no trainer can use? It was read from origin/oxide at 0e3f757e81 and changes no game data.

Since 2026-10-14 (f5672c2460, Ian's picks from `stranded-moves.md`), 46 of these moves have a player learner by level-up, which leaves (a) at 198, (b) at 15 and (e) at 599; the tables below are as audited. The 26 from (a) are Chip Away, Circle Throw, Dragon Darts, Electro Ball, Fiery Dance, Fillet Away, Fire Lash, Frost Breath, Glaciate, Hard Press, Heart Stamp, Heat Crash, Jaw Lock, Leaf Tornado, Mighty Cleave, Mystical Power, Parabolic Charge, Power Trip, Psychic Fangs, Rising Voltage, Storm Throw, Tachyon Cutter, Take Heart, Triple Dive, Twin Beam and Victory Dance. The 20 from (b) are Aeroblast, Coil, Core Enforcer, Diamond Storm, Doom Desire, Fiery Wrath, Freezing Glare, Horn Leech, Hurricane, Luster Purge, Mist Ball, Nature's Madness, Oblivion Wing, Origin Pulse, Power-Up Punch, Sacred Sword, Shift Gear, Thousand Arrows, Thousand Waves and Thunderous Kick. Upper Hand and Burning Jealousy wait on in-game checks 81 and 83, and Psycho Boost stays trainer only.

## Summary

The audit covers 847 of the 923 move records. It leaves out the 53 Z-moves and 19 Max moves, which nobody gets (Ian, 2026-10-14), and the 4 placeholders (MOVE_NONE and the MOVE_UNUSED records). Learners come from every species and form record in res/pokemon, by level-up, TM, tutor and egg list, the 13 form records under forms/ included. A trainer carries a move when it is on one of the 768 trainer files the scorer reads, which are every named trainer and the dummy slots a map battles.

The player's Pokemon are the 468 species that obtainable() in tools/oxide/balance/pool.py names. It counts the player's side at the League from the encounter census, every scripted source whatever its level (starters, gifts, trades, eggs, static battles, fossils, honey trees), the drawn thirds of the legendary pool (docs/oxide/encounters/availability-plan.json, without the reserve and the caverns kept empty), and everything those evolve into. A form record counts when its species is obtainable, since the game reads a form's own level-up list (Pokemon_LoadLevelUpMovesOf goes through Pokemon_GetFormNarcIndex). A move is open to the player at any level of an obtainable species' level-up list (level 1 and the evolution moves at level 0 included), from a TM placed in the game, or from a reachable tutor.

| Group | Moves | What it holds |
|---|---|---|
| (a) | 224 | no species or form learns it by any route, and no trainer carries it |
| (b) | 35 | only species the player cannot obtain learn it, and no trainer carries it |
| (c) | 18 | the player cannot reach it, but a trainer carries it (7 have learners the player cannot obtain, 11 have none) |
| (d) | 17 | the player reaches it only through egg lists, the trainers' palette (12 of them carried by a trainer today) |
| (e) | 553 | the player can reach it |

These agree with the re-run of move_pool_survey.py: 612 of the 847 have a learner of some kind, and 235 have none (all of (a), and the 11 of (c) that no species learns). The survey judges the 612 against the pick-list's native and new species, which is wider than the encounter pool. Against obtainable() they split into 35 in (b), 7 in (c), 17 in (d) and 553 in (e).

Four kinds fill (a). 113 are signature moves of one species, line or form in the later games that has no learnset in Oxide, such as Victini's V-create, Keldeo's Secret Sword, the Calyrex, Urshifu, Zacian, Koraidon and Miraidon moves, the Hisuian forms' moves and the Starmobile's five torques. 13 are the Let's Go partner moves, Sizzly Slide among them. 45 do nothing in Oxide's engine at all: the four terrains, Ally Switch, Fairy Lock, Shed Tail, Tidy Up and other stub scripts. The last 53 are ordinary moves left with no learner. Among them are Barrage, Comet Punch and Psywave, which Ian took out on purpose, and Struggle, which needs no learner.

(b) is mostly legendary and mythical signatures of species that are not placed: Lugia's Aeroblast, Latias's Mist Ball and Latios's Luster Purge, Kyogre's Origin Pulse, Jirachi's Doom Desire and Deoxys's Psycho Boost, with the Zygarde, Xerneas, Yveltal, Diancie, Tapu, Ultra Beast and Galarian bird moves. It also holds a few ordinary moves whose only learners are out of reach. They are Hurricane (only Yveltal), Horn Leech (Tapu Bulu and Xerneas), Coil (Zygarde), Sacred Sword and Laser Focus (Kartana), Power-Up Punch (Buzzwole), Bone Club (Marowak), Pay Day (Meowth), Conversion 2 (the Porygon line), Sharpen, Wrap and Zap Cannon. Cut is here too: its only obtainable learner, Giratina's Origin form, has it on HM01, which is not placed.

Of the 259 moves in (a) and (b), Oxide's engine runs 184 as written, runs 29 as plain hits with an effect missing, and does nothing for 46. Many of the working ones could be given to a line or a trainer. Ordinary attacks with a clean effect include Hurricane, Horn Leech, Sacred Sword, Power-Up Punch, Fire Lash, Psychic Fangs, Snipe Shot, Spirit Break, Drum Beating, Apple Acid, Grav Apple, Night Daze, Lumina Crash, Torch Song, Fiery Dance, Burning Jealousy, Aqua Step, Jet Punch, Frost Breath, Storm Throw, Dragon Darts, Triple Dive, Bitter Malice, Infernal Parade, Shadow Bone and Esper Wing. Setup and utility moves include Coil, Work Up, Victory Dance, Take Heart, Shift Gear, Spicy Extract, Jungle Healing and Lunar Blessing, with the protecting moves King's Shield, Spiky Shield, Baneful Bunker, Obstruct and Silk Trap. Legendary-grade attacks fit the late teams that may carry anything: V-create, Blue Flare, Bolt Strike, Sacred Fire, Aeroblast, Psystrike, Origin Pulse, Precipice Blades, Dragon Ascent, Steam Eruption, Secret Sword and Glacial Lance.

The audit also turned up three things Ian may want to act on.

First, form records the learnset rewrite did not touch put three ruled-out moves in the player's reach. Rotom's five alternate forms learn Double Team, Wormadam's Sandy and Trash forms learn Protect, and the Sandy form learns Fissure. Shaymin's Sky form also learns Seed Flare, which base Shaymin no longer does.

Second, trainers still carry moves Ian ruled out: the one-hit KO moves (Guillotine on 5 teams and Sheer Cold on 6, with Horn Drill on 5 through egg lists), and Double Slap (2 teams) and Spike Cannon (1), which left the game with the multi-hit ruling. These go as each team is set by hand. The weather moves in (c) (Rain Dance on 19 teams, Sunny Day on 15, Sandstorm on 7, Hail on 1) are trainer-only by design.

Third, the simulator-gaps doc had not counted form records in its player columns. This branch corrects the cells that change (Protect, the one-hit KO moves and a few species counts); no gap changes group.

The next steps are Ian's. Cleaning the four form leftovers is a few minutes' data change once he rules on it. Giving a working (a) or (b) move to a line or a trainer is learnset or team work under the balance rules, a move at a time. Whether the 46 moves that do nothing and the 13 Let's Go moves should stay in the data is his call too. Leaving them costs nothing in play, and cutting move records would touch the move expansion, which is larger work.

## (a) No species or form learns it, and no trainer carries it (224)

Each table gives the move's type, category and power, and whether Oxide's engine runs it. "Partly" means the engine runs it as a plain hit and the effect it has in its home games is missing; "does nothing" means its effect script is a stub, a status move on the plain-hit script, or a terrain move.

### Signature moves of one species, line or form in the later games (113)

| Move | Type | Category | Power | Home species | Engine |
|---|---|---|---|---|---|
| Apple Acid | Grass | Special | 90 | Appletun | runs |
| Aqua Step | Water | Physical | 80 | Quaquaval | runs |
| Astral Barrage | Ghost | Special | 110 | Calyrex | runs |
| Aura Wheel | Electric | Physical | 110 | Morpeko | partly: a plain hit; the Speed rise and the form's type are missing |
| Baneful Bunker | Poison | Status | none | Toxapex | runs |
| Barb Barrage | Poison | Physical | 60 | Hisuian Qwilfish and Overqwil | runs |
| Behemoth Bash | Steel | Physical | 100 | Zamazenta | runs |
| Behemoth Blade | Steel | Physical | 100 | Zacian | runs |
| Bitter Malice | Ghost | Special | 75 | Hisuian Zoroark | runs |
| Blazing Torque | Fire | Physical | 80 | Starmobile | runs |
| BleakwindStorm | Flying | Special | 100 | Tornadus | runs |
| Blood Moon | Normal | Special | 130 | Bloodmoon Ursaluna | partly: a plain hit; the rule against using it twice in a row is missing |
| Blue Flare | Fire | Special | 130 | Reshiram | runs |
| Bolt Beak | Electric | Physical | 80 | Dracozolt and Arctozolt | runs |
| Bolt Strike | Electric | Special | 130 | Zekrom | runs |
| Ceaseless Edge | Dark | Physical | 65 | Hisuian Samurott | runs |
| Chloroblast | Grass | Special | 150 | Hisuian Lilligant | runs |
| ColisionCourse | Fighting | Physical | 100 | Koraidon | partly: a plain hit; the boost on a super-effective hit is missing |
| Combat Torque | Fighting | Physical | 100 | Starmobile | runs |
| Dire Claw | Poison | Physical | 80 | Sneasler | runs |
| Double IronBash | Steel | Physical | 60 | Melmetal | runs |
| Dragon Ascent | Flying | Physical | 120 | Rayquaza | runs |
| Dragon Energy | Dragon | Special | 150 | Regidrago | runs |
| Drum Beating | Grass | Physical | 80 | Rillaboom | runs |
| Dynamax Cannon | Dragon | Special | 100 | Eternatus | runs |
| Electro Drift | Electric | Special | 100 | Miraidon | partly: a plain hit; the boost on a super-effective hit is missing |
| Electro Shot | Electric | Special | 130 | Archaludon | runs |
| Esper Wing | Psychic | Special | 80 | Hisuian Braviary | runs |
| Eternabeam | Dragon | Special | 160 | Eternatus | runs |
| Fickle Beam | Dragon | Special | 80 | Hydrapple | runs |
| Fishious Rend | Water | Physical | 80 | Dracovish and Arctovish | runs |
| Fleur Cannon | Fairy | Special | 130 | Magearna | runs |
| Freeze Shock | Ice | Special | 140 | Black Kyurem | runs |
| Fusion Bolt | Electric | Special | 100 | Zekrom | partly: a plain hit; doubling after Fusion Flare is missing |
| Fusion Flare | Fire | Special | 100 | Reshiram | partly: a plain hit; doubling after Fusion Bolt is missing |
| Gear Grind | Steel | Physical | 60 | the Klink line | runs |
| Gigaton Hammer | Steel | Physical | 160 | Tinkaton | partly: a plain hit; the rule against using it twice in a row is missing |
| Glacial Lance | Ice | Physical | 130 | Calyrex | runs |
| Glaive Rush | Dragon | Physical | 120 | Baxcalibur | partly: a plain hit: its effect script only works out damage (Oxide's Glaive Rush is a plain hit: its effect script is CalcCrit and CalcDamage only, and battle_lib.c lists it among the unreachable effects left as placeholders, so the later games' drawback is not in the game.) |
| Grav Apple | Grass | Physical | 90 | Flapple | runs |
| Head Charge | Normal | Physical | 120 | Bouffalant | runs |
| Hydro Steam | Water | Special | 80 | Walking Wake | partly: a plain hit; the boost in sun is missing |
| Hyper Drill | Normal | Physical | 120 | Dudunsparce | partly: a plain hit; passing Protect is missing |
| Hyperspace Fury | Dark | Physical | 100 | Hoopa | runs |
| Hyperspace Hole | Psychic | Special | 80 | Hoopa | runs |
| Ice Burn | Ice | Special | 140 | White Kyurem | runs |
| Infernal Parade | Ghost | Special | 65 | Hisuian Typhlosion | runs |
| Ivy Cudgel | Grass | Physical | 100 | Ogerpon | partly: a plain hit; the mask's type and the high critical ratio are missing |
| Jet Punch | Water | Physical | 60 | Palafin | runs |
| Judgment | Normal | Special | 100 | Arceus | runs |
| Jungle Healing | Grass | Status | none | Zarude | runs |
| King’s Shield | Steel | Status | none | Aegislash | runs |
| Kowtow Cleave | Dark | Physical | 85 | Kingambit | runs |
| Last Respects | Ghost | Physical | 50 | Houndstone | runs |
| Light of Ruin | Fairy | Special | 140 | Eternal Floette | runs |
| Lumina Crash | Psychic | Special | 80 | Glimmora | runs |
| Lunar Blessing | Psychic | Status | none | Cresselia | runs |
| Magical Torque | Fairy | Physical | 100 | Starmobile | runs |
| Make It Rain | Steel | Special | 120 | Gholdengo | partly: a plain hit: its effect script only works out damage (Oxide's Make It Rain is a plain hit: its script is CalcCrit and CalcDamage only, and battle_lib.c lists it among the unreachable effects left as placeholders, so its Sp. Atk drop is not in the game.) |
| Malignant Chain | Poison | Special | 100 | Pecharunt | runs |
| Meteor Assault | Fighting | Physical | 150 | Sirfetch'd | runs |
| Moongeist Beam | Ghost | Special | 100 | Lunala | partly: a plain hit; ignoring the target's ability is missing |
| Mountain Gale | Ice | Physical | 120 | Hisuian Avalugg | runs |
| Multi-Attack | Normal | Physical | 120 | Silvally | partly: a plain hit: its effect script only works out damage (Multi-Attack is a plain 120-power hit in Oxide (effect_script_0308 is CalcCrit and CalcDamage; there are no Memories to change its type).) |
| Night Daze | Dark | Special | 90 | Zoroark | runs |
| Noxious Torque | Poison | Physical | 100 | Starmobile | runs |
| Obstruct | Dark | Status | none | Obstagoon | runs |
| Order Up | Dragon | Physical | 80 | Dondozo | runs |
| Overdrive | Electric | Special | 80 | Toxtricity | runs |
| Photon Geyser | Psychic | Special | 100 | Necrozma | partly: a plain hit; turning physical and ignoring the target's ability are missing |
| Plasma Fists | Electric | Physical | 100 | Zeraora | partly: a plain hit; Ion Deluge's effect is a stub, so Normal moves are never turned Electric |
| Population Bomb | Normal | Physical | 20 | Maushold | runs |
| PrecipiceBlades | Ground | Physical | 120 | Groudon | runs |
| Prismatic Laser | Psychic | Special | 160 | Necrozma | runs |
| Psyblade | Psychic | Physical | 80 | Iron Leaves | partly: a plain hit: its effect script only works out damage (Psyblade is a plain 80-power hit in Oxide: its Electric Terrain boost has no terrain to read (effect_script_0300 is CalcCrit and CalcDamage).) |
| Psyshield Bash | Psychic | Physical | 90 | Wyrdeer | runs |
| Psystrike | Psychic | Special | 100 | Mewtwo | runs |
| Raging Bull | Normal | Physical | 90 | Paldean Tauros | runs |
| Raging Fury | Fire | Physical | 120 | Hisuian Arcanine | runs |
| RevelationDance | Normal | Special | 100 | Oricorio | partly: a plain hit; it stays Normal instead of taking its user's type |
| Ruination | Dark | Special | varies | the Treasures of Ruin | runs |
| Sacred Fire | Fire | Physical | 100 | Ho-Oh | runs |
| SandsearStorm | Ground | Special | 100 | Landorus | runs |
| Searing Shot | Fire | Special | 100 | Victini | runs |
| Secret Sword | Fighting | Special | 85 | Keldeo | runs |
| Shadow Bone | Ghost | Physical | 85 | Alolan Marowak | runs |
| Shell Side Arm | Poison | Special | 90 | Galarian Slowbro | partly: a plain hit; turning physical and the poison chance are missing |
| Shell Trap | Fire | Special | 150 | Turtonator | runs |
| Silk Trap | Bug | Status | none | Spidops | runs |
| Snipe Shot | Water | Special | 85 | Inteleon | runs |
| Spectral Thief | Ghost | Physical | 90 | Marshadow | partly: a plain hit; stealing the target's stat rises is missing |
| Spicy Extract | Grass | Status | none | Scovillain | runs |
| Spiky Shield | Grass | Status | none | Chesnaught | runs |
| Spin Out | Steel | Physical | 100 | Revavroom | runs |
| Spirit Break | Fairy | Physical | 75 | the Impidimp line | runs |
| SpringtideStorm | Fairy | Special | 100 | Enamorus | runs |
| Steam Eruption | Water | Special | 110 | Volcanion | runs |
| Steamroller | Bug | Physical | 65 | Scolipede | runs |
| Steel Roller | Steel | Physical | 130 | Copperajah | partly: a plain 130 hit; in the later games it fails with no terrain up, which in Oxide is always |
| Stone Axe | Rock | Physical | 65 | Kleavor | runs |
| Sunsteel Strike | Steel | Physical | 100 | Solgaleo | partly: a plain hit; ignoring the target's ability is missing |
| Surging Strikes | Water | Physical | 25 | Rapid Strike Urshifu | runs |
| Syrup Bomb | Grass | Special | 60 | Dipplin | runs |
| Techno Blast | Normal | Special | 120 | Genesect | partly: a plain hit: its effect script only works out damage (Techno Blast is a plain Normal hit in Oxide (effect_script_0307 is CalcCrit and CalcDamage; there are no Drives).) |
| Tera Starstorm | Normal | Special | 120 | Terapagos | runs |
| Thunder Cage | Electric | Special | 80 | Regieleki | partly: a plain hit; the binding is missing |
| Thunderclap | Electric | Special | 70 | Raging Bolt | runs |
| Torch Song | Fire | Special | 80 | Skeledirge | runs |
| Triple Arrows | Fighting | Physical | 90 | Hisuian Decidueye | partly: a plain hit; the Defense drop, the flinch and the high critical ratio are missing |
| V-create | Fire | Physical | 180 | Victini | runs |
| Wicked Blow | Dark | Physical | 80 | Single Strike Urshifu | runs |
| Wicked Torque | Dark | Physical | 80 | Starmobile | runs |
| WildboltStorm | Electric | Special | 100 | Thundurus | runs |

### Let's Go partner moves (13)

| Move | Type | Category | Power | Engine |
|---|---|---|---|---|
| Baddy Bad | Dark | Special | 80 | runs |
| Bouncy Bubble | Water | Special | 60 | partly: a plain hit: its effect script only works out damage (Bouncy Bubble is a plain hit in Oxide: its effect script is CalcCrit and CalcDamage with no drain (effect_script_0315).) |
| Buzzy Buzz | Electric | Special | 60 | runs |
| Floaty Fall | Flying | Physical | 90 | runs |
| Freezy Frost | Ice | Special | 100 | runs |
| Glitzy Glow | Psychic | Special | 80 | runs |
| Pika Papow | Electric | Special | varies | runs |
| Sappy Seed | Grass | Physical | 100 | runs |
| Sizzly Slide | Fire | Physical | 60 | runs |
| Sparkly Swirl | Fairy | Special | 120 | runs |
| Splishy Splash | Water | Special | 90 | runs |
| Veevee Volley | Normal | Physical | varies | runs |
| Zippy Zap | Electric | Physical | 80 | runs |

### Other moves no species learns (53)

| Move | Type | Category | Power | Engine |
|---|---|---|---|---|
| Barrage | Normal | Physical | 25 | runs |
| Beat Up | Dark | Physical | 10 | runs |
| Branch Poke | Grass | Physical | 40 | runs |
| Burning Bulwark | Fire | Status | none | runs |
| BurningJealousy | Fire | Special | 70 | runs |
| Chip Away | Normal | Physical | 70 | runs |
| Circle Throw | Fighting | Physical | 60 | runs |
| Comet Punch | Normal | Physical | 25 | runs |
| Comeuppance | Dark | Physical | varies | runs |
| Constrict | Normal | Physical | 10 | runs |
| Dragon Darts | Dragon | Physical | 50 | runs |
| Dragon Hammer | Dragon | Physical | 100 | runs |
| Eerie Spell | Psychic | Special | 80 | runs |
| Electro Ball | Electric | Special | varies | runs |
| False Surrender | Dark | Physical | 80 | runs |
| Fiery Dance | Fire | Special | 80 | runs |
| Fillet Away | Normal | Status | none | runs |
| Fire Lash | Fire | Physical | 90 | runs |
| Frost Breath | Ice | Special | 60 | runs |
| Glaciate | Ice | Special | 65 | runs |
| Hard Press | Steel | Physical | varies | runs |
| Heart Stamp | Psychic | Physical | 60 | runs |
| Heat Crash | Fire | Physical | varies | runs |
| Ice Hammer | Ice | Physical | 100 | runs |
| Ice Spinner | Ice | Physical | 80 | runs |
| Inferno | Fire | Special | 100 | runs |
| Jaw Lock | Dark | Physical | 80 | runs |
| Leaf Tornado | Grass | Special | 65 | runs |
| Mighty Cleave | Rock | Physical | 95 | runs |
| Misty Explosion | Fairy | Special | 200 | runs |
| Mystical Power | Psychic | Special | 70 | runs |
| ParabolicCharge | Electric | Special | 65 | runs |
| Power Shift | Normal | Status | none | runs |
| Power Trip | Dark | Physical | 20 | runs |
| Psychic Fangs | Psychic | Physical | 85 | runs |
| Psywave | Psychic | Special | varies | runs |
| Rising Voltage | Electric | Special | 70 | runs |
| Snap Trap | Steel | Physical | 35 | partly: a plain hit; the binding is missing |
| Spotlight | Normal | Status | none | runs |
| Steel Beam | Steel | Special | 140 | partly: a plain hit; the user's loss of half its HP is missing |
| Storm Throw | Fighting | Physical | 60 | runs |
| Struggle | Normal | Physical | 50 | runs |
| Submission | Fighting | Physical | 80 | runs |
| Supercell Slam | Electric | Physical | 100 | runs |
| Synchronoise | Psychic | Special | 120 | partly: a plain hit; the rule that it hits only a foe sharing a type is missing |
| Tachyon Cutter | Steel | Special | 50 | runs |
| Take Heart | Psychic | Status | none | runs |
| Tera Blast | Normal | Special | 80 | runs |
| Triple Dive | Water | Physical | 35 | runs |
| Twin Beam | Psychic | Special | 40 | runs |
| Upper Hand | Fighting | Physical | 65 | runs |
| Victory Dance | Fighting | Status | none | runs |
| Work Up | Normal | Status | none | runs |

### Moves Oxide's engine does not run (45)

| Move | Type | Category | Power | Engine |
|---|---|---|---|---|
| Ally Switch | Psychic | Status | none | does nothing: a status move on a script that only works out damage |
| Aromatic Mist | Fairy | Status | none | does nothing: a status move on a script that only works out damage |
| Bestow | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| Celebrate | Normal | Status | none | does nothing: does nothing |
| ChillyReception | Ice | Status | none | does nothing: a status move on a script that only works out damage |
| Confide | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| Corrosive Gas | Poison | Status | none | does nothing: a status move on a script that only works out damage |
| Court Change | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| Decorate | Fairy | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Doodle | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| Dragon Cheer | Dragon | Status | none | does nothing: a status move on a script that only works out damage |
| ElectricTerrain | Electric | Status | none | does nothing: stub: "But nothing happened!" until terrain exists |
| Electrify | Electric | Status | none | does nothing: a status move on a script that only works out damage |
| Fairy Lock | Fairy | Status | none | does nothing: a status move on a script that only works out damage |
| Floral Healing | Fairy | Status | none | does nothing: a status move on a script that only works out damage |
| Flower Shield | Fairy | Status | none | does nothing: a status move on a script that only works out damage |
| Forest’s Curse | Grass | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Gear Up | Steel | Status | none | does nothing: a status move on a script that only works out damage |
| Grassy Terrain | Grass | Status | none | does nothing: stub: "But nothing happened!" until terrain exists |
| Happy Hour | Normal | Status | none | does nothing: doubles prize money; no battle effect |
| Hold Hands | Normal | Status | none | does nothing: does nothing |
| Instruct | Psychic | Status | none | does nothing: a status move on a script that only works out damage |
| Ion Deluge | Electric | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Magic Powder | Psychic | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Magnetic Flux | Electric | Status | none | does nothing: a status move on a script that only works out damage |
| Misty Terrain | Fairy | Status | none | does nothing: stub: "But nothing happened!" until terrain exists |
| No Retreat | Fighting | Status | none | does nothing: a status move on a script that only works out damage |
| Powder | Bug | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Psychic Terrain | Psychic | Status | none | does nothing: stub: "But nothing happened!" until terrain exists |
| Purify | Poison | Status | none | does nothing: a status move on a script that only works out damage |
| Quash | Dark | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Reflect Type | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| RevivalBlessing | Normal | Status | none | does nothing: a status move on a script that only works out damage |
| Rototiller | Ground | Status | none | does nothing: a status move on a script that only works out damage |
| Shed Tail | Normal | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Simple Beam | Normal | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Snowscape | Ice | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Speed Swap | Psychic | Status | none | does nothing: a status move on a script that only works out damage |
| Stuff Cheeks | Normal | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Tar Shot | Rock | Status | none | does nothing: a status move on a script that only works out damage |
| Telekinesis | Psychic | Status | none | does nothing: a status move on a script that only works out damage |
| Tidy Up | Normal | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Topsy-Turvy | Dark | Status | none | does nothing: a status move on a script that only works out damage |
| Toxic Thread | Poison | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Trick-or-Treat | Ghost | Status | none | does nothing: its effect script ends in Splash's message or "But nothing happened!" |

## (b) Only species the player cannot obtain learn it, and no trainer carries it (35)

Cut is here although obtainable forms have it, because their only route is HM01, which is not placed in the game.

| Move | Type | Category | Power | Learners (none obtainable) | Engine |
|---|---|---|---|---|---|
| Aeroblast | Flying | Special | 100 | Lugia | runs |
| Autotomize | Normal | Status | none | Celesteela, Stakataka | runs |
| Bone Club | Ground | Physical | 65 | Marowak | runs |
| Coil | Poison | Status | none | Zygarde 10, Zygarde 50 | runs |
| Conversion 2 | Normal | Status | none | Porygon, Porygon Z, Porygon2 | runs |
| Core Enforcer | Dragon | Special | 100 | Zygarde 10, Zygarde 50 | runs |
| Cut | Normal | Physical | 50 | Deoxys (attack form), Deoxys (defense form), Deoxys (speed form), Kartana; obtainable through HM01 only: Giratina (origin form) | runs |
| Diamond Storm | Rock | Physical | 100 | Diancie | runs |
| Doom Desire | Steel | Special | 140 | Jirachi | runs |
| Fiery Wrath | Dark | Special | 90 | Galarian Moltres | runs |
| Freezing Glare | Psychic | Special | 90 | Galarian Articuno | runs |
| Geomancy | Fairy | Status | none | Xerneas | runs |
| Horn Leech | Grass | Physical | 75 | Tapu Bulu, Xerneas | runs |
| Hurricane | Flying | Special | 110 | Yveltal | runs |
| Land’s Wrath | Ground | Physical | 90 | Zygarde 10, Zygarde 50 | runs |
| Laser Focus | Normal | Status | none | Kartana | runs |
| Luster Purge | Psychic | Special | 95 | Latios | runs |
| Mind Blown | Fire | Special | 150 | Blacephalon | runs |
| Mist Ball | Psychic | Special | 95 | Latias | runs |
| Nature’sMadness | Fairy | Special | varies | Tapu Bulu, Tapu Fini, Tapu Koko, Tapu Lele | runs |
| Oblivion Wing | Flying | Special | 80 | Yveltal | runs |
| Origin Pulse | Water | Special | 110 | Kyogre | runs |
| Pay Day | Normal | Physical | 40 | Meowth | runs |
| Power-Up Punch | Fighting | Physical | 40 | Buzzwole | runs |
| Psycho Boost | Psychic | Special | 140 | Deoxys (attack form), Deoxys (defense form), Deoxys (speed form) | runs |
| Sacred Sword | Fighting | Physical | 90 | Kartana | runs |
| Sharpen | Normal | Status | none | Diancie, Porygon | runs |
| Shift Gear | Steel | Status | none | Magearna | runs |
| Teleport | Psychic | Status | none | Deoxys (attack form), Deoxys (defense form) | does nothing: flees a wild battle; fails against a trainer |
| Thousand Arrows | Ground | Physical | 90 | Zygarde 10, Zygarde 50 | runs |
| Thousand Waves | Ground | Physical | 90 | Zygarde 10, Zygarde 50 | runs |
| Thunderous Kick | Fighting | Physical | 90 | Galarian Zapdos | runs |
| Wonder Room | Psychic | Status | none | Nihilego | runs |
| Wrap | Normal | Physical | 15 | Deoxys (attack form), Deoxys (defense form), Deoxys (speed form) | runs |
| Zap Cannon | Electric | Special | 120 | Deoxys (attack form) | runs |

## (c) The player cannot reach it, but a trainer carries it (18)

| Move | Type | Category | Power | Trainers that carry it | Learners |
|---|---|---|---|---|---|
| Absorb | Grass | Special | 20 | 4: Dawn, Lucas, Lucas and Dawn 1 (bosses: Lucas and Dawn 1) | none |
| Bonemerang | Ground | Physical | 50 | 2: Kevin, Nicholas (no boss) | Cubone, Marowak (none obtainable) |
| Conversion | Normal | Status | none | 1: Travon (no boss) | Porygon, Porygon Z, Porygon2 (none obtainable) |
| DoubleSlap | Normal | Physical | 25 | 2: Carrie, Danielle (no boss) | none |
| Eruption | Fire | Special | 150 | 5: Abel, Buck, Buck (Stark Mountain), Douglas, Hesperid (Mt. Coronet) (bosses: Hesperid (Mt. Coronet)) | Camerupt, Cyndaquil, Quilava, Torkoal, Typhlosion (none obtainable) |
| Focus Punch | Fighting | Physical | 150 | 4: Fantina, Grunt, Janet (bosses: Fantina) | Buzzwole, Vigoroth (none obtainable) |
| Guillotine | Normal | Physical | varies | 5: Francisco, Grunt, Kurt, Paul, Samson (no boss) | none |
| Hail | Ice | Status | none | 1: Candice rematch (bosses: Candice rematch) | none |
| Magma Storm | Fire | Special | 100 | 2: Cyrus 3, Palmer (bosses: Cyrus 3) | none |
| Mega Kick | Normal | Physical | 120 | 2: Carl, Miles (no boss) | none |
| Needle Arm | Grass | Physical | 80 | 1: Grunt (no boss) | Cacnea, Cacturne (none obtainable) |
| Rain Dance | Water | Status | none | 19: Caitlyn, Claire, Cody, Damian, Evan, Grunt, Janet, Jared and 11 more (bosses: Volkner rematch) | none |
| Sandstorm | Rock | Status | none | 7: Alexander, Buck, Byron rematch, Damon, Emma & Lil, Jo & Pat, Mariel (bosses: Byron rematch) | none |
| Sheer Cold | Ice | Special | varies | 6: Joanna, Lexie, Lydia, Paige, Sam, Trenton (no boss) | none |
| Sketch | Normal | Status | none | 1: Ismael (no boss) | Smeargle (none obtainable) |
| Spike Cannon | Normal | Physical | 25 | 1: Wesley (no boss) | none |
| Sunny Day | Fire | Status | none | 15: Alexa, Angela, Elizabeth, Flint rematch, Gardenia rematch, Grunt, Hannah, Jenna and 5 more (bosses: Flint rematch, Gardenia rematch) | none |
| Transform | Normal | Status | none | 1: Al & Kay (no boss) | Ditto, Mew (none obtainable) |

## (d) The player reaches it only through egg lists, the trainers' palette (17)

| Move | Type | Category | Power | Obtainable species with it on an egg list | Trainers that carry it |
|---|---|---|---|---|---|
| Bide | Normal | Physical | varies | Heracross, Snorunt | 1: Shelley (no boss) |
| Cross Chop | Fighting | Physical | 100 | Croagunk, Elekid, Magby, Makuhita, Psyduck, Riolu | 21: Dalton, Danny, Davon, Destiny, Ernest, Flint and Volkner, Grunt, Henry and 13 more (bosses: Flint and Volkner, Maylene, Maylene rematch, Saturn 1, Saturn 2, Volkner, Volkner rematch) |
| Detect | Fighting | Status | none | Makuhita, Riolu | 5: Aaron rematch, Brady, Griffin, Kyler, Willie (bosses: Aaron rematch) |
| DynamicPunch | Fighting | Physical | 100 | Croagunk, Elekid, Magby, Makuhita, Meditite | 4: Eddie, Grunt, Jarrett, Zachariah (no boss) |
| Feint | Normal | Physical | 30 | Croagunk, Gligar, Torchic, Yanma | 2: Jennifer, Leonard (no boss) |
| Final Gambit | Fighting | Special | varies | Mankey | none |
| Fury Attack | Normal | Physical | 25 | Starly | 6: Carrie, Crystal, Jessica, Karina, Leonardo, Norman (no boss) |
| Horn Drill | Normal | Physical | varies | Lapras, Ponyta, Seel | 5: Carlos, Crystal, Olivia rematch (no boss) |
| Ingrain | Grass | Status | none | Corsola | 6: Angela, Brady, Brian, Elizabeth, Hannah (no boss) |
| Mega Punch | Normal | Physical | 80 | Geodude, Magby | 3: Al & Kay, Brady, Carl (no boss) |
| Memento | Dark | Status | none | Drifloon, Duskull, Hoppip, Koffing, Litwick, Misdreavus, Ralts, Shellos, Sinistea, Slugma and 2 more | 1: Kassandra (no boss) |
| Rage | Normal | Physical | 20 | Houndour, Swablu | none |
| Razor Wind | Normal | Special | 80 | Gligar, Scyther, Seedot, Tropius | 1: Wesley (no boss) |
| Selfdestruct | Normal | Physical | 200 | Bonsly, Ferroseed, Geodude, Glimmet, Koffing, Sudowoodo | 3: Gerardo, Jo & Pat, Ronald (no boss) |
| Sleep Talk | Normal | Status | none | Goldeen, Lapras, Lickitung, Relicanth, Slowpoke, Wailmer | none |
| Splash | Normal | Status | none | Delibird, Finneon, Horsea, Luvdisc, Mantine, Mantyke, Poliwag | none |
| Switcheroo | Dark | Status | none | Buneary | none |

## (e) The player can reach it (553)

By any level of an obtainable species' level-up list (level 1 and the evolution moves at level 0 included), a TM placed in the game, or a reachable tutor. By type:

Bug (28): Attack Order, Bug Bite, Bug Buzz, Defend Order, Fell Stinger, FirstImpression, Fury Cutter, Heal Order, Infestation, Leech Life, Lunge, Megahorn, Pin Missile, Pollen Puff, Pounce, Quiver Dance, Rage Powder, Signal Beam, Silver Wind, Skitter Smack, Spider Web, Sticky Web, String Shot, Struggle Bug, Tail Glow, Twineedle, U-turn, X-Scissor.

Dark (29): Assurance, Bite, Brutal Swing, Crunch, Dark Pulse, Dark Void, Darkest Lariat, Embargo, Faint Attack, Fake Tears, Flatter, Fling, Foul Play, Hone Claws, Knock Off, Lash Out, Nasty Plot, Night Slash, Parting Shot, Payback, Punishment, Pursuit, Snarl, Snatch, Sucker Punch, Taunt, Thief, Throat Chop, Torment.

Dragon (17): Breaking Swipe, Clanging Scales, Clangorous Soul, Draco Meteor, Dragon Claw, Dragon Dance, Dragon Pulse, Dragon Rage, Dragon Rush, Dragon Tail, DragonBreath, Dual Chop, Outrage, Roar of Time, Scale Shot, Spacial Rend, Twister.

Electric (20): Charge, Charge Beam, Discharge, Double Shock, Eerie Impulse, Electroweb, Magnet Rise, Nuzzle, Shock Wave, Spark, Thunder, Thunder Fang, Thunder Wave, Thunderbolt, ThunderPunch, ThunderShock, Volt Switch, Volt Tackle, Wild Charge, Zing Zap.

Fairy (13): Alluring Voice, Baby-Doll Eyes, Charm, Crafty Shield, Dazzling Gleam, Disarming Voice, Draining Kiss, Fairy Wind, Moonblast, Moonlight, Play Rough, Strange Steam, Sweet Kiss.

Fighting (35): Arm Thrust, Aura Sphere, Axe Kick, Body Press, Brick Break, Bulk Up, Close Combat, Coaching, Counter, Double Kick, Drain Punch, Flying Press, Focus Blast, Force Palm, Hammer Arm, Hi Jump Kick, Jump Kick, Karate Chop, Low Kick, Low Sweep, Mach Punch, Mat Block, Octolock, Quick Guard, Revenge, Reversal, Rock Smash, Rolling Kick, Seismic Toss, Sky Uppercut, Superpower, Triple Kick, Vacuum Wave, Vital Throw, Wake-Up Slap.

Fire (24): Armor Cannon, Bitter Blade, Blast Burn, Blaze Kick, Burn Up, Ember, Fire Blast, Fire Fang, Fire Pledge, Fire Punch, Fire Spin, Flame Burst, Flame Charge, Flame Wheel, Flamethrower, Flare Blitz, Heat Wave, Incinerate, Lava Plume, Mystical Fire, Overheat, Pyro Ball, Temper Flare, Will-O-Wisp.

Flying (22): Acrobatics, Aerial Ace, Air Cutter, Air Slash, Beak Blast, Bounce, Brave Bird, Chatter, Defog, Drill Peck, Dual Wingbeat, FeatherDance, Fly, Gust, Mirror Move, Peck, Pluck, Roost, Sky Attack, Sky Drop, Tailwind, Wing Attack.

Ghost (19): Astonish, Confuse Ray, Destiny Bond, Grudge, Hex, Lick, Night Shade, Nightmare, Ominous Wind, Phantom Force, Poltergeist, Rage Fist, Shadow Ball, Shadow Claw, Shadow Force, Shadow Punch, Shadow Sneak, Spirit Shackle, Spite.

Grass (37): Aromatherapy, Bullet Seed, Cotton Guard, Cotton Spore, Energy Ball, Flower Trick, Frenzy Plant, Giga Drain, Grass Knot, Grass Pledge, GrassWhistle, Grassy Glide, Leaf Blade, Leaf Storm, Leafage, Leech Seed, Magical Leaf, Matcha Gotcha, Mega Drain, Petal Blizzard, Petal Dance, Power Whip, Razor Leaf, Seed Bomb, Seed Flare, Sleep Powder, Solar Blade, SolarBeam, Spore, Strength Sap, Stun Spore, Synthesis, Trailblaze, Trop Kick, Vine Whip, Wood Hammer, Worry Seed.

Ground (20): Bone Rush, Bulldoze, Dig, Drill Run, Earth Power, Earthquake, Fissure, Headlong Rush, High Horsepower, Magnitude, Mud Bomb, Mud Shot, Mud Sport, Mud-Slap, Sand Tomb, Sand-Attack, Scorching Sands, Shore Up, Spikes, StompingTantrum.

Ice (17): Aurora Beam, Aurora Veil, Avalanche, Blizzard, Freeze-Dry, Haze, Ice Ball, Ice Beam, Ice Fang, Ice Punch, Ice Shard, Icicle Crash, Icicle Spear, Icy Wind, Mist, Powder Snow, Triple Axel.

Mystery (1): Curse.

Normal (137): Acupressure, After You, Assist, Attract, Baton Pass, Belly Drum, Bind, Block, Body Slam, Boomburst, Camouflage, Captivate, Copycat, Covet, Crush Claw, Crush Grip, Defense Curl, Disable, Dizzy Punch, Double Hit, Double Team, Double-Edge, Echoed Voice, Egg Bomb, Encore, Endeavor, Endure, Entrainment, Explosion, ExtremeSpeed, Facade, Fake Out, False Swipe, Flail, Flash, Focus Energy, Follow Me, Foresight, Frustration, Fury Swipes, Giga Impact, Glare, Growl, Growth, Harden, Headbutt, Heal Bell, Helping Hand, Hidden Power, Hold Back, Horn Attack, Howl, Hyper Beam, Hyper Fang, Hyper Voice, Last Resort, Leer, Lock-On, Lovely Kiss, Lucky Chant, Me First, Mean Look, Metronome, Milk Drink, Mimic, Mind Reader, Minimize, Morning Sun, Natural Gift, Nature Power, Noble Roar, Odor Sleuth, Pain Split, Perish Song, Play Nice, Pound, Present, Protect, Psych Up, Quick Attack, Rapid Spin, Recover, Recycle, Refresh, Relic Song, Retaliate, Return, Roar, Rock Climb, Round, Safeguard, Scary Face, Scratch, Screech, Secret Power, Shell Smash, Sing, Skull Bash, Slack Off, Slam, Slash, SmellingSalt, SmokeScreen, Snore, Softboiled, SonicBoom, Spit Up, Stockpile, Stomp, Strength, Substitute, Super Fang, Supersonic, Swagger, Swallow, Sweet Scent, Swift, Swords Dance, Tackle, Tail Slap, Tail Whip, Take Down, Tearful Look, Teatime, Teeter Dance, Terrain Pulse, Thrash, Tickle, Tri Attack, Trump Card, Uproar, ViceGrip, Weather Ball, Whirlwind, Wish, Wring Out, Yawn.

Poison (23): Acid, Acid Armor, Acid Spray, Belch, Clear Smog, Cross Poison, Gastro Acid, Gunk Shot, Mortal Spin, Poison Fang, Poison Gas, Poison Jab, Poison Sting, Poison Tail, PoisonPowder, Sludge, Sludge Bomb, Sludge Wave, Smog, Toxic, Toxic Spikes, Venom Drench, Venoshock.

Psychic (44): Agility, Amnesia, Barrier, Calm Mind, Confusion, Cosmic Power, Dream Eater, Expanding Force, Extrasensory, Future Sight, Gravity, Guard Split, Guard Swap, Heal Block, Heal Pulse, Healing Wish, Heart Swap, Hypnosis, Imprison, Kinesis, Light Screen, Lunar Dance, Magic Coat, Magic Room, Meditate, Miracle Eye, Mirror Coat, Power Split, Power Swap, Power Trick, Psybeam, Psychic, Psychic Noise, Psycho Cut, Psycho Shift, Psyshock, Reflect, Rest, Role Play, Skill Swap, Stored Power, Trick, Trick Room, Zen Headbutt.

Rock (17): Accelerock, AncientPower, Head Smash, Meteor Beam, Power Gem, Rock Blast, Rock Polish, Rock Slide, Rock Throw, Rock Tomb, Rock Wrecker, Rollout, Salt Cure, Smack Down, Stealth Rock, Stone Edge, Wide Guard.

Steel (17): Anchor Shot, Bullet Punch, Flash Cannon, Gyro Ball, Heavy Slam, Iron Defense, Iron Head, Iron Tail, Magnet Bomb, Metal Burst, Metal Claw, Metal Sound, Meteor Mash, Mirror Shot, Shelter, Smart Strike, Steel Wing.

Water (33): Aqua Cutter, Aqua Jet, Aqua Ring, Aqua Tail, Brine, Bubble, BubbleBeam, Chilling Water, Clamp, Crabhammer, Dive, Flip Turn, Hydro Cannon, Hydro Pump, Life Dew, Liquidation, Muddy Water, Octazooka, Razor Shell, Scald, Soak, Sparkling Aria, Surf, Water Gun, Water Pledge, Water Pulse, Water Shuriken, Water Sport, Water Spout, Waterfall, Wave Crash, Whirlpool, Withdraw.
