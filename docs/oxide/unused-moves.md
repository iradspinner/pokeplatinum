# Moves Oxide holds that nobody uses

Ian asked on 2026-10-20 for every official move that Oxide lacks, leaving out the Z-moves, Max moves and other moves tied to mechanics Oxide does not have, and for the notable ones worth adding before trainer teambuilding resumes. It was read from origin/oxide at ab7c3c80c and changes no game data.

## Summary

No official move is missing. Oxide's move table, ported from hg-engine, holds every regular move through Generation 9's Indigo Disk. Two sources agree: the calculator's move tables for every generation, and hg-engine's own list of 923 moves. Once the old spellings Oxide keeps are matched (Hi Jump Kick, Faint Attack, SmellingSalt), the only moves Oxide lacks are Z-moves, which it does not want. Its extras are the 53 Z-moves and 19 Max moves, which nobody gets and which are due to be removed. One spelling slip turned up: Collision Course reads "ColisionCourse" in the game, and its constant is `MOVE_COLISION_COURSE`.

So the useful question is which of Oxide's own moves nobody can use. On the tree it was read from, before the signature-move homes of 2026-10-20 and 21 (`signature-moves.md`) gave many of them a home:

| Who can have the move | Moves |
|---|---|
| The player, by level-up, TM or tutor | 596 |
| Only a trainer's team | 34 |
| Only egg lists, the trainers' palette | 5 |
| Only species the player cannot obtain | 12 |
| Nobody: no species learns it and no trainer carries it | 200 |

Of the last two rows' 212 moves, the engine runs 136 as written, runs 29 as plain hits with an effect missing, and does nothing with 47 (the tables below). The stranded-moves pass of 2026-10-14 (`stranded-moves.md`) decided the ordinary moves among them, and Ian approved its homes. It left the later games' signature moves aside, and that is where most of the strong unused moves are: their home species are not in Oxide, so nothing learns them.

These are the picks worth a decision, all moves the engine runs as written:

| Pick | Moves | Why |
|---|---|---|
| Back to an owner the player can catch | Lumina Crash to Glimmora, Stone Axe to Kleavor, Shell Trap to Turtonator | each is its own signature, and its line is obtainable in Oxide but lacks it |
| The same, for trainers only | Baneful Bunker to Toxapex, on its egg list | a Protect variant, which Ian's ruling keeps off player lists |
| Signature moves that would suit obtainable lines | Spirit Break, Snipe Shot, Night Daze, Apple Acid, Grav Apple, Drum Beating, Jet Punch, Aqua Step, Torch Song, Esper Wing, Psyshield Bash, Bitter Malice, Infernal Parade, Kowtow Cleave, Thunderclap, Raging Bull | ordinary types and powers with a modern effect: a stat drop on hit (Spirit Break's Sp. Atk, Drum Beating's Speed, Apple Acid's Sp. Def, Grav Apple's Defense, Bitter Malice's Attack), a stat rise (Aqua Step's and Esper Wing's Speed, Torch Song's Sp. Atk, Psyshield Bash's Defense), priority (Jet Punch, Thunderclap), or a twist (Infernal Parade doubles into a status, Kowtow Cleave never misses, Raging Bull breaks screens) |
| Trainer palette | Ceaseless Edge, Dire Claw, Barb Barrage, Malignant Chain, Last Respects | strong enough to belong on egg lists, where trainers can use them and the player cannot: Ceaseless Edge sets Spikes on a hit, Dire Claw inflicts poison, paralysis or sleep half the time, Malignant Chain badly poisons half the time, and Last Respects grows with each fainted teammate |
| Legendary signatures, for the late bosses | V-create, Psystrike, Blue Flare, Bolt Strike, Freeze Shock, Ice Burn, Precipice Blades, Dragon Ascent, Steam Eruption, Prismatic Laser and the rest | for the bosses from Cyrus 3 on, which may carry two or three legendaries and moves that need not be legal |

Speed control and priority are the strongest of these, by Ian's own reading of the Gardenia dials, so Aqua Step, Esper Wing, Drum Beating, Jet Punch and Thunderclap want the most care if any goes to the player.

Ian answered on 2026-10-20 by asking for that pass over the last three picks. It is `signature-moves.md`, which records his answers (the returns among them: Stone Axe to Kleavor, Lumina Crash to the Slowbro line rather than Glimmora, Shell Trap held for its in-game check) and the homes that landed. The 29 partly working and 47 dead moves wait on engine work before any of them is worth a home.

The source of the engine verdicts is `move-access.md` of 2026-10-14; the engine changes since then (Eerie Spell, Burning Bulwark, the Dragon Tail drag and Pickpocket) touch none of these rows.

## The 212 moves nobody can use

"Home species" names the species that has the move in the later games, from `move-access.md`; an empty cell is a move with no single owner.

### The engine runs them as written (136)

| Move | Type | Category | Power | Home species in the later games | Engine |
|---|---|---|---|---|---|
| Steamroller | Bug | Physical | 65 | Scolipede | runs |
| Silk Trap | Bug | Status |  | Spidops | runs |
| Hyperspace Fury | Dark | Physical | 100 | Hoopa | runs |
| Night Daze | Dark | Special | 90 | Zoroark | runs |
| Kowtow Cleave | Dark | Physical | 85 | Kingambit | runs |
| Baddy Bad | Dark | Special | 80 |  | runs |
| False Surrender | Dark | Physical | 80 |  | runs |
| Wicked Blow | Dark | Physical | 80 | Single Strike Urshifu | runs |
| Wicked Torque | Dark | Physical | 80 | Starmobile | runs |
| Ceaseless Edge | Dark | Physical | 65 | Hisuian Samurott | runs |
| Beat Up | Dark | Physical | 10 |  | runs |
| Comeuppance | Dark | Physical | 1 |  | runs |
| Ruination | Dark | Special | 1 | the Treasures of Ruin | runs |
| Obstruct | Dark | Status |  | Obstagoon | runs |
| Eternabeam | Dragon | Special | 160 | Eternatus | runs |
| Dragon Energy | Dragon | Special | 150 | Regidrago | runs |
| Dragon Hammer | Dragon | Physical | 100 |  | runs |
| Dynamax Cannon | Dragon | Special | 100 | Eternatus | runs |
| Fickle Beam | Dragon | Special | 80 | Hydrapple | runs |
| Order Up | Dragon | Physical | 80 | Dondozo | runs |
| Bolt Strike | Electric | Special | 130 | Zekrom | runs |
| Electro Shot | Electric | Special | 130 | Archaludon | runs |
| Zap Cannon | Electric | Special | 120 | Deoxys (attack form) | runs |
| Supercell Slam | Electric | Physical | 100 |  | runs |
| WildboltStorm | Electric | Special | 100 | Thundurus | runs |
| Bolt Beak | Electric | Physical | 80 | Dracozolt and Arctozolt | runs |
| Overdrive | Electric | Special | 80 | Toxtricity | runs |
| Zippy Zap | Electric | Physical | 80 |  | runs |
| Thunderclap | Electric | Special | 70 | Raging Bolt | runs |
| Buzzy Buzz | Electric | Special | 60 |  | runs |
| Pika Papow | Electric | Special | 1 |  | runs |
| Misty Explosion | Fairy | Special | 200 |  | runs |
| Light of Ruin | Fairy | Special | 140 | Eternal Floette | runs |
| Fleur Cannon | Fairy | Special | 130 | Magearna | runs |
| Sparkly Swirl | Fairy | Special | 120 |  | runs |
| Magical Torque | Fairy | Physical | 100 | Starmobile | runs |
| SpringtideStorm | Fairy | Special | 100 | Enamorus | runs |
| Spirit Break | Fairy | Physical | 75 | the Impidimp line | runs |
| Geomancy | Fairy | Status |  | Xerneas; learned only by unobtainable Xerneas | runs |
| Meteor Assault | Fighting | Physical | 150 | Sirfetch'd | runs |
| Combat Torque | Fighting | Physical | 100 | Starmobile | runs |
| Secret Sword | Fighting | Special | 85 | Keldeo | runs |
| Submission | Fighting | Physical | 80 |  | runs |
| Upper Hand | Fighting | Physical | 65 |  | runs |
| V-create | Fire | Physical | 180 | Victini | runs |
| Mind Blown | Fire | Special | 150 | Blacephalon; learned only by unobtainable Blacephalon | runs |
| Shell Trap | Fire | Special | 150 | Turtonator | runs |
| Blue Flare | Fire | Special | 130 | Reshiram | runs |
| Raging Fury | Fire | Physical | 120 | Hisuian Arcanine | runs |
| Inferno | Fire | Special | 100 |  | runs |
| Searing Shot | Fire | Special | 100 | Victini | runs |
| Blazing Torque | Fire | Physical | 80 | Starmobile | runs |
| Torch Song | Fire | Special | 80 | Skeledirge | runs |
| BurningJealousy | Fire | Special | 70 |  | runs |
| Sizzly Slide | Fire | Physical | 60 |  | runs |
| Burning Bulwark | Fire | Status |  |  | runs |
| Dragon Ascent | Flying | Physical | 120 | Rayquaza | runs |
| BleakwindStorm | Flying | Special | 100 | Tornadus | runs |
| Floaty Fall | Flying | Physical | 90 |  | runs |
| Astral Barrage | Ghost | Special | 110 | Calyrex | runs |
| Shadow Bone | Ghost | Physical | 85 | Alolan Marowak | runs |
| Bitter Malice | Ghost | Special | 75 | Hisuian Zoroark | runs |
| Infernal Parade | Ghost | Special | 65 | Hisuian Typhlosion | runs |
| Last Respects | Ghost | Physical | 50 | Houndstone | runs |
| Chloroblast | Grass | Special | 150 | Hisuian Lilligant | runs |
| Sappy Seed | Grass | Physical | 100 |  | runs |
| Apple Acid | Grass | Special | 90 | Appletun | runs |
| Grav Apple | Grass | Physical | 90 | Flapple | runs |
| Drum Beating | Grass | Physical | 80 | Rillaboom | runs |
| Syrup Bomb | Grass | Special | 60 | Dipplin | runs |
| Branch Poke | Grass | Physical | 40 |  | runs |
| Jungle Healing | Grass | Status |  | Zarude | runs |
| Spicy Extract | Grass | Status |  | Scovillain | runs |
| Spiky Shield | Grass | Status |  | Chesnaught | runs |
| PrecipiceBlades | Ground | Physical | 120 | Groudon | runs |
| SandsearStorm | Ground | Special | 100 | Landorus | runs |
| Land’s Wrath | Ground | Physical | 90 | Zygarde 10, Zygarde 50; learned only by unobtainable Zygarde_10, Zygarde_50 | runs |
| Bone Club | Ground | Physical | 65 | Marowak; learned only by unobtainable Marowak | runs |
| Freeze Shock | Ice | Special | 140 | Black Kyurem | runs |
| Ice Burn | Ice | Special | 140 | White Kyurem | runs |
| Glacial Lance | Ice | Physical | 130 | Calyrex | runs |
| Mountain Gale | Ice | Physical | 120 | Hisuian Avalugg | runs |
| Freezy Frost | Ice | Special | 100 |  | runs |
| Ice Hammer | Ice | Physical | 100 |  | runs |
| Ice Spinner | Ice | Physical | 80 |  | runs |
| Head Charge | Normal | Physical | 120 | Bouffalant | runs |
| Tera Starstorm | Normal | Special | 120 | Terapagos | runs |
| Judgment | Normal | Special | 100 | Arceus | runs |
| Raging Bull | Normal | Physical | 90 | Paldean Tauros | runs |
| Tera Blast | Normal | Special | 80 |  | runs |
| Cut | Normal | Physical | 50 | Deoxys (attack form), Deoxys (defense form), Deoxys (speed form), Kartana; obtainable through HM01 only: Giratina (origin form); learned only by unobtainable Kartana | runs |
| Struggle | Normal | Physical | 50 |  | runs |
| Pay Day | Normal | Physical | 40 | Meowth; learned only by unobtainable Meowth | runs |
| Barrage | Normal | Physical | 25 |  | runs |
| Comet Punch | Normal | Physical | 25 |  | runs |
| Population Bomb | Normal | Physical | 20 | Maushold | runs |
| Wrap | Normal | Physical | 15 | Deoxys (attack form), Deoxys (defense form), Deoxys (speed form) | runs |
| Constrict | Normal | Physical | 10 |  | runs |
| Veevee Volley | Normal | Physical | 1 |  | runs |
| Autotomize | Normal | Status |  | Celesteela, Stakataka; learned only by unobtainable Celesteela, Stakataka | runs |
| Conversion 2 | Normal | Status |  | Porygon, Porygon Z, Porygon2; learned only by unobtainable Porygon, Porygon2, Porygon_Z | runs |
| Laser Focus | Normal | Status |  | Kartana; learned only by unobtainable Kartana | runs |
| Power Shift | Normal | Status |  |  | runs |
| Sharpen | Normal | Status |  | Diancie, Porygon; learned only by unobtainable Diancie, Porygon | runs |
| Spotlight | Normal | Status |  |  | runs |
| Work Up | Normal | Status |  |  | runs |
| Malignant Chain | Poison | Special | 100 | Pecharunt | runs |
| Noxious Torque | Poison | Physical | 100 | Starmobile | runs |
| Dire Claw | Poison | Physical | 80 | Sneasler | runs |
| Barb Barrage | Poison | Physical | 60 | Hisuian Qwilfish and Overqwil | runs |
| Baneful Bunker | Poison | Status |  | Toxapex | runs |
| Prismatic Laser | Psychic | Special | 160 | Necrozma | runs |
| Psystrike | Psychic | Special | 100 | Mewtwo | runs |
| Psyshield Bash | Psychic | Physical | 90 | Wyrdeer | runs |
| Eerie Spell | Psychic | Special | 80 |  | runs |
| Esper Wing | Psychic | Special | 80 | Hisuian Braviary | runs |
| Glitzy Glow | Psychic | Special | 80 |  | runs |
| Hyperspace Hole | Psychic | Special | 80 | Hoopa | runs |
| Lumina Crash | Psychic | Special | 80 | Glimmora | runs |
| Psywave | Psychic | Special | 1 |  | runs |
| Lunar Blessing | Psychic | Status |  | Cresselia | runs |
| Wonder Room | Psychic | Status |  | Nihilego; learned only by unobtainable Nihilego | runs |
| Stone Axe | Rock | Physical | 65 | Kleavor | runs |
| Behemoth Bash | Steel | Physical | 100 | Zamazenta | runs |
| Behemoth Blade | Steel | Physical | 100 | Zacian | runs |
| Spin Out | Steel | Physical | 100 | Revavroom | runs |
| Double IronBash | Steel | Physical | 60 | Melmetal | runs |
| Gear Grind | Steel | Physical | 60 | the Klink line | runs |
| King’s Shield | Steel | Status |  | Aegislash | runs |
| Steam Eruption | Water | Special | 110 | Volcanion | runs |
| Splishy Splash | Water | Special | 90 |  | runs |
| Snipe Shot | Water | Special | 85 | Inteleon | runs |
| Aqua Step | Water | Physical | 80 | Quaquaval | runs |
| Fishious Rend | Water | Physical | 80 | Dracovish and Arctovish | runs |
| Jet Punch | Water | Physical | 60 | Palafin | runs |
| Surging Strikes | Water | Physical | 25 | Rapid Strike Urshifu | runs |

### The engine runs them as plain hits, an effect missing (29)

| Move | Type | Category | Power | Home species in the later games | Engine |
|---|---|---|---|---|---|
| Glaive Rush | Dragon | Physical | 120 | Baxcalibur | partly: a plain hit: its effect script only works out damage (Oxide's Glaive Rush is a plain hit: its effect script is CalcCrit and CalcDamage only, and battle_lib.c lists it among the unreachable effects left as placeholders, so the later games' drawback is not in the game.) |
| Aura Wheel | Electric | Physical | 110 | Morpeko | partly: a plain hit; the Speed rise and the form's type are missing |
| Electro Drift | Electric | Special | 100 | Miraidon | partly: a plain hit; the boost on a super-effective hit is missing |
| Fusion Bolt | Electric | Special | 100 | Zekrom | partly: a plain hit; doubling after Fusion Flare is missing |
| Plasma Fists | Electric | Physical | 100 | Zeraora | partly: a plain hit; Ion Deluge's effect is a stub, so Normal moves are never turned Electric |
| Thunder Cage | Electric | Special | 80 | Regieleki | partly: a plain hit; the binding is missing |
| ColisionCourse | Fighting | Physical | 100 | Koraidon | partly: a plain hit; the boost on a super-effective hit is missing |
| Triple Arrows | Fighting | Physical | 90 | Hisuian Decidueye | partly: a plain hit; the Defense drop, the flinch and the high critical ratio are missing |
| Fusion Flare | Fire | Special | 100 | Reshiram | partly: a plain hit; doubling after Fusion Bolt is missing |
| Moongeist Beam | Ghost | Special | 100 | Lunala | partly: a plain hit; ignoring the target's ability is missing |
| Spectral Thief | Ghost | Physical | 90 | Marshadow | partly: a plain hit; stealing the target's stat rises is missing |
| Ivy Cudgel | Grass | Physical | 100 | Ogerpon | partly: a plain hit; the mask's type and the high critical ratio are missing |
| Blood Moon | Normal | Special | 130 | Bloodmoon Ursaluna | partly: a plain hit; the rule against using it twice in a row is missing |
| Hyper Drill | Normal | Physical | 120 | Dudunsparce | partly: a plain hit; passing Protect is missing |
| Multi-Attack | Normal | Physical | 120 | Silvally | partly: a plain hit: its effect script only works out damage (Multi-Attack is a plain 120-power hit in Oxide (effect_script_0308 is CalcCrit and CalcDamage; there are no Memories to change its type).) |
| Techno Blast | Normal | Special | 120 | Genesect | partly: a plain hit: its effect script only works out damage (Techno Blast is a plain Normal hit in Oxide (effect_script_0307 is CalcCrit and CalcDamage; there are no Drives).) |
| RevelationDance | Normal | Special | 100 | Oricorio | partly: a plain hit; it stays Normal instead of taking its user's type |
| Shell Side Arm | Poison | Special | 90 | Galarian Slowbro | partly: a plain hit; turning physical and the poison chance are missing |
| Synchronoise | Psychic | Special | 120 |  | partly: a plain hit; the rule that it hits only a foe sharing a type is missing |
| Photon Geyser | Psychic | Special | 100 | Necrozma | partly: a plain hit; turning physical and ignoring the target's ability are missing |
| Psyblade | Psychic | Physical | 80 | Iron Leaves | partly: a plain hit: its effect script only works out damage (Psyblade is a plain 80-power hit in Oxide: its Electric Terrain boost has no terrain to read (effect_script_0300 is CalcCrit and CalcDamage).) |
| Gigaton Hammer | Steel | Physical | 160 | Tinkaton | partly: a plain hit; the rule against using it twice in a row is missing |
| Steel Beam | Steel | Special | 140 |  | partly: a plain hit; the user's loss of half its HP is missing |
| Steel Roller | Steel | Physical | 130 | Copperajah | partly: a plain 130 hit; in the later games it fails with no terrain up, which in Oxide is always |
| Make It Rain | Steel | Special | 120 | Gholdengo | partly: a plain hit: its effect script only works out damage (Oxide's Make It Rain is a plain hit: its script is CalcCrit and CalcDamage only, and battle_lib.c lists it among the unreachable effects left as placeholders, so its Sp. Atk drop is not in the game.) |
| Sunsteel Strike | Steel | Physical | 100 | Solgaleo | partly: a plain hit; ignoring the target's ability is missing |
| Snap Trap | Steel | Physical | 35 |  | partly: a plain hit; the binding is missing |
| Hydro Steam | Water | Special | 80 | Walking Wake | partly: a plain hit; the boost in sun is missing |
| Bouncy Bubble | Water | Special | 60 |  | partly: a plain hit: its effect script only works out damage (Bouncy Bubble is a plain hit in Oxide: its effect script is CalcCrit and CalcDamage with no drain (effect_script_0315).) |

### The engine does nothing with them (47)

| Move | Type | Category | Power | Home species in the later games | Engine |
|---|---|---|---|---|---|
| Powder | Bug | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Quash | Dark | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Topsy-Turvy | Dark | Status |  |  | does nothing: a status move on a script that only works out damage |
| Dragon Cheer | Dragon | Status |  |  | does nothing: a status move on a script that only works out damage |
| ElectricTerrain | Electric | Status |  |  | does nothing: stub: "But nothing happened!" until terrain exists |
| Electrify | Electric | Status |  |  | does nothing: a status move on a script that only works out damage |
| Ion Deluge | Electric | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Magnetic Flux | Electric | Status |  |  | does nothing: a status move on a script that only works out damage |
| Aromatic Mist | Fairy | Status |  |  | does nothing: a status move on a script that only works out damage |
| Decorate | Fairy | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Fairy Lock | Fairy | Status |  |  | does nothing: a status move on a script that only works out damage |
| Floral Healing | Fairy | Status |  |  | does nothing: a status move on a script that only works out damage |
| Flower Shield | Fairy | Status |  |  | does nothing: a status move on a script that only works out damage |
| Misty Terrain | Fairy | Status |  |  | does nothing: stub: "But nothing happened!" until terrain exists |
| No Retreat | Fighting | Status |  |  | does nothing: a status move on a script that only works out damage |
| Trick-or-Treat | Ghost | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Forest’s Curse | Grass | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Grassy Terrain | Grass | Status |  |  | does nothing: stub: "But nothing happened!" until terrain exists |
| Rototiller | Ground | Status |  |  | does nothing: a status move on a script that only works out damage |
| ChillyReception | Ice | Status |  |  | does nothing: a status move on a script that only works out damage |
| Snowscape | Ice | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Bestow | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| Celebrate | Normal | Status |  |  | does nothing: does nothing |
| Confide | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| Court Change | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| Doodle | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| Happy Hour | Normal | Status |  |  | does nothing: doubles prize money; no battle effect |
| Hold Hands | Normal | Status |  |  | does nothing: does nothing |
| Reflect Type | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| RevivalBlessing | Normal | Status |  |  | does nothing: a status move on a script that only works out damage |
| Shed Tail | Normal | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Simple Beam | Normal | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Sketch | Normal | Status |  | 1: Ismael (no boss); learned only by unobtainable Smeargle | Smeargle (none obtainable) |
| Stuff Cheeks | Normal | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Tidy Up | Normal | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Corrosive Gas | Poison | Status |  |  | does nothing: a status move on a script that only works out damage |
| Purify | Poison | Status |  |  | does nothing: a status move on a script that only works out damage |
| Toxic Thread | Poison | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Ally Switch | Psychic | Status |  |  | does nothing: a status move on a script that only works out damage |
| Instruct | Psychic | Status |  |  | does nothing: a status move on a script that only works out damage |
| Magic Powder | Psychic | Status |  |  | does nothing: its effect script ends in Splash's message or "But nothing happened!" |
| Psychic Terrain | Psychic | Status |  |  | does nothing: stub: "But nothing happened!" until terrain exists |
| Speed Swap | Psychic | Status |  |  | does nothing: a status move on a script that only works out damage |
| Telekinesis | Psychic | Status |  |  | does nothing: a status move on a script that only works out damage |
| Teleport | Psychic | Status |  | Deoxys (attack form), Deoxys (defense form) | does nothing: flees a wild battle; fails against a trainer |
| Tar Shot | Rock | Status |  |  | does nothing: a status move on a script that only works out damage |
| Gear Up | Steel | Status |  |  | does nothing: a status move on a script that only works out damage |

