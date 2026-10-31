# Wake's split: mandatory fights, the level climb and Route 214

Wake's split (after Maylene, cap 39, to Wake, cap 44) went through the process Fantina's and Maylene's splits went through on 2026-10-29: the mandatory fights counted and raised, the trivial teams rebuilt, and the ordinary trainers' levels climbed in play order. Ian answered the first draft's questions on 2026-10-31, and this page records the result, on the branch `overseer-wake-split`.

## Summary

The split holds 10 non-boss mandatory fights, up from 1, which meets Ian's 10 to 15. Nine trainers moved or now look one fixed way:

- Psychic Abigail and Psychic Mitchell on Route 214 now look one way.
- PI Carlos moved to the narrows south of Route 214's berry field.
- Route 213's three turners (Cyndy, Chelsea, Jared) now look one way at its chokepoints.
- Fisherman Travis left Route 212 South for Route 213.
- Gentleman Jeremy and Socialite Reina left Route 212 North for Valor Lakefront.

33 ordinary teams were rebuilt. They climb from 39 on Route 214 to 42 in Pastoria's gym. The gym's last guard, Sailor Samson, is the one team at 43, and none is at 44. Before, nearly all were vanilla one- and two-Pokemon teams. 27 of the 124 rebuilt members are Oxide's later species, against none before. 16 teams carry 3 Pokemon, 9 carry 4 and 8 carry 5, the larger ones on the mandatory fights and the walking policemen. No member has an Adamant, Modest, Timid or Jolly nature. Two forced trades come in, once each, under Ian's ruling below.

Ian's four Route 214 teams kept their sets and moved only in level, to the route's line of 39. Krystal has his base-ROM team back, topping at 42: in his words she is "meant to be a hard fight gating the encounter in ruin maniac cave/tunnel". PI Carlos's TM72, a reward on what is now a mandatory fight, moved to Policeman Caleb on Route 212 North.

Every changed team passed the trainer lint and the real packer. Every move on a rebuilt team is legal at its level, and no rebuilt team repeats an item or a nature. Ian's kept sets break some rules, listed below for him and not fixed.

Left out of this landing:

- The Restaurant's nine daily doubles, which wait for a later pass.
- The Pokemon Mansion, which will be done with Darach.
- The Surf trainers on these maps, met only in Byron's split, now that Surf also waits on Cyrus at Celestic Town.
- The Valor Lakefront grunt, which belongs to Byron's split.

Ian's answers (2026-10-31), as applied:

1. Barry 4 stays in Wake's split at cap 44, since he is fought before the gym. The Valor Lakefront grunt alone moves to Byron's split.
2. The three Route 214 changes are made.
3. Krystal has his base-ROM team back, topping at 42, two under each of his base ROM's levels.
4. Devon, Douglas, Bryan and Ronald climbed by level only.
5. Ronald keeps his team, Selfdestruct and Arena Trap included.
6. Collector Jamal stays as he is.
7. The moves of Travis, Jeremy and Reina across maps stand.
8. The Restaurant's doubles are back to oxide's teams.
9. The Mansion is left alone.
10. Some teams grew to 5. From Wake's split on, an ordinary trainer may occasionally carry a forced trade (Self-Destruct, Explosion or Destiny Bond) or trapping. They are used rarely, never as a pattern.

Ian's later answers (2026-10-31), as applied:

- Krystal tops at 42.
- TM72 moves from PI Carlos to an optional trainer of weak-to-medium strength nearby, placed by the reward tool's own rule (below).
- His kept sets' off-list moves are on their lines' egg lists, under his ruling of 2026-10-29, so every move on his five teams is legal.

Nothing waits on Ian from this page but the in-game checks.

Next steps:

| Step | Who | Time |
|---|---|---|
| Land the branch with `merge-branch.sh`, then run `sync-docs.sh` on oxide | the Overseer | 30 minutes |
| Play the checklist item "Mandatory fights, Wake's split" in `docs/oxide/ingame-checklist.md` | Ian | 25 minutes with the test kit's warps |

What is unverified:

- Nothing has been seen in game. The moves come from the tile model.
- No fight was read by the scorer.
- The doubles were checked as singles.
- The box sits at the cap, not the mid-split line.
- The trainer AI does not see some held items these teams carry, such as Weakness Policy and Rocky Helmet.

## Barry 4 and the Valor Lakefront grunt

The first draft read Barry 4 as fought after Wake. That was wrong; Ian's correction is right.

Barry 4 is a coord event in Pastoria at (589, 828), script 18 (`PastoriaCity_Entry17`). It fires when `VAR_PASTORIA_CITY_STATE` is 1, which the Veilstone warehouse sets after Tyche and Hermes. Winning sets the state to 2 (`PastoriaCity_0AA2`). Pastoria's gym sets it to 3 only when Wake falls. So Barry is fought before the gym, in Wake's split, at cap 44.

The Galactic grunt is another matter. The grunt's talk fires at state 5, which comes after the gym's state 3. Route 213 shows the grunt only with the Fen Badge. The battle at Valor Lakefront ends with Cynthia handing over the SecretPotion. So the grunt is fought after Wake's badge, in Byron's split.

## The mandatory fights

Ian's rules of 2026-10-29 apply. Gym trainers and bosses are not counted. A trainer who turns, spins or walks is optional. A pair, or a twins double, is one fight. Two trainers fought alone together field six Pokemon at most.

The story path through the split runs Veilstone, Route 214, Valor Lakefront, Route 213, Pastoria. Route 212 runs from Pastoria north to Hearthome and is off the path, so all its trainers are optional. The Great Marsh, the Maniac Tunnel and caves, the hotel and the Restaurant are optional too.

| # | Fight | Map | How it is known |
|---:|---|---|---|
| 1 | Psychic Abigail (now looks one way) | Route 214 | required.py, after the change |
| 2 | Psychic Mitchell (now stands still) | Route 214 | required.py, after the change |
| 3 | PI Carlos (moved) | Route 214 | required.py, after the move |
| 4 | Beauty Devon and Collector Douglas, one eye-contact double (5 Pokemon) | Route 214 | required.py; `pairs.py` reads them always together |
| 5 | Gentleman Jeremy (moved) | Valor Lakefront | required.py, after the move |
| 6 | Socialite Reina (moved) | Valor Lakefront | required.py, after the move |
| 7 | Beauty Cyndy (now looks one way) | Route 213 | required.py, after the change |
| 8 | Tuber Chelsea (now looks one way) | Route 213 | required.py, after the change |
| 9 | Tuber Jared (now looks one way) | Route 213 | required.py, after the change |
| 10 | Fisherman Travis (moved) | Route 213 | required.py, after the move |

The bosses are Officers Tyche and Hermes (the Veilstone tag battle beside Lucas or Dawn), Barry 4 and Wake. The Pastoria gym's six trainers are gym trainers.

Optional on the path:

- Ruin Maniacs Bryan and Ronald, Collector Jamal and Krystal stand on Route 214's west half, behind Ian's boulders, and are reached from the south.
- Fisherman Kenneth stays where he was on Route 213. He carries the Covert Cloak, and a reward belongs to an optional fight.

### TM72 changes holder

PI Carlos gave TM72 (Avalanche, a weak TM) as his reward. He is now a mandatory fight, and a reward belongs to an optional one, so Ian moved it (2026-10-31). The new holder is the one the reward tool's own rule picks: `rewards.pick_trainer` for a weak TM in Wake's split takes the strongest optional trainer of the split's easier half that holds no reward yet. That is Policeman Caleb on Route 212 North, three Pokemon topping at 41, met at night.

The steps:

- `rewards.py` gains `REHOMED`, which moves TM72's row of the approved table to Caleb.
- `rewards.py write` rewrote the tables, and only TM72's rows were kept.
- `place_rewards.py apply` moved the reward in `scripts_battles.s`. Caleb gives it under spare flag 0x03CD, and Carlos's 0x021F is free again.
- Checked: `rewards.py check` (0 failures), `test_place_rewards` (passed) and `place_rewards.py check` on the rebuilt ROM (168 rows, each found exactly once).

The split holds no gauntlet section: `gauntlet.py` builds none here, and no stretch of the path is one-way.

### The trainers moved

Each keeps its class and script, and now looks one fixed way.

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Psychic Abigail | Route 214 (721, 660), turning west and east, sight 5 | the same tile, looking west, sight 5 | Ian's yes. The model reads her required looking west. |
| Psychic Mitchell | Route 214 (731, 694), walking north and south, sight 1 | the same tile, looking south, sight 3 | Ian's yes. Standing still, he sees down the column every way south crosses. |
| PI Carlos | Route 214 (726, 676), turning north and south, sight 2 | (733, 690), looking west, sight 2 | Ian's yes. He stands at the east edge of the narrows south of the berry field. Devon's walking copy stays outside his sight. |
| Gentleman Jeremy | Route 212 North (455, 796), turning north and east, sight 2 | Valor Lakefront (728, 740), looking east, sight 3 | The way in from Route 214 is a corridor four tiles wide (x 728 to 731). He stands at its west edge and sees the other three. |
| Socialite Reina | Route 212 North (458, 796), turning south and west, sight 3 | Valor Lakefront (720, 764), looking east, sight 5 | Below the grass the path narrows to six tiles (x 720 to 725). She stands at its west edge and sees the other five. The later scenes there walk at x 722 to 724, past her. |
| Beauty Cyndy | Route 213 (668, 827), turning west and east, sight 5 | (705, 822), looking east, sight 2 | Every way from the hotel down to the beach crosses rows 821 and 822 at x 705 to 707. She stands on the lower row and sees the other two tiles. |
| Tuber Chelsea | Route 213 (704, 827), turning three ways, sight 4 | (700, 831), looking south, sight 1 | West of the hotel's beach, a strip one tile wide (row 832) runs between the cliff and the sea. She stands above its entrance and sees it. |
| Tuber Jared | Route 213 (703, 832), walking, sight 3 | (670, 818), looking east, sight 7 | The beach joins the grass to Pastoria only through a neck eight tiles wide (x 670 to 677) and two rows deep. He stands at the west end of the south row and sees all of it. |
| Fisherman Travis | Route 212 South's bridge (499, 856), looking south, sight 0 | Route 213 (677, 817), looking west, sight 7 | He stands at the east end of the neck's north row and sees all of it. The player meets Jared, then Travis: two fights in a row of four Pokemon each, never one double. |

The checks, each run on the edited files:

- required.py reads all nine trainers as required, on the crossings Route 214, Valor Lakefront (added to its table) and Route 213.
- From every warp and map edge, in Wake's, Byron's and Candice's splits, the player still reaches every tile reachable before, the trainers' own tiles aside.
- No moved trainer stands on a warp, sign, hidden item, trigger or another object.
- `pairs.py`'s eye-contact pairs lose Jeremy and Reina's (they no longer share a tile) and gain none.
- The scripted walks on Route 213 (the grunt and Looker after Fen Badge) do not cross the new tiles.
- `test_b1e` passes 8 of 8, its totals pinned at 68 required and 106 avoidable.
- The five maps are declared in `bulk_events.py`'s DIVERGED.

## The level climb

Ordinary trainers climb in play order from 39 on Route 214 to 42 in the gym, with only the gym's last guard at 43. In the table, "Old" and "New" are each team's highest level, and "Size" is the old size, then the new one.

| # | Trainer | Area | Kind | Old | New | Size |
|---:|---|---|---|---:|---:|---|
| 1 | Beauty Devon | Route 214 | mandatory, double with Douglas (Ian's) | 38 | 39 | 2 |
| 2 | Collector Douglas | Route 214 | mandatory, double with Devon (Ian's) | 37 | 39 | 3 |
| 3 | Psychic Abigail | Route 214 | mandatory (now looks one way) | 34 | 39 | 3 to 5 |
| 4 | Psychic Mitchell | Route 214 | mandatory (now stands still) | 34 | 39 | 2 to 4 |
| 5 | PI Carlos | Route 214 (moved) | mandatory | 36 | 39 | 1 to 4 |
| 6 | Ruin Maniac Bryan | Route 214, west half | optional (Ian's) | 37 | 39 | 5 |
| 7 | Ruin Maniac Ronald | Route 214, west half | optional (Ian's) | 39 | 39 | 5 |
| 8 | Krystal | Route 214, west half | optional, the gate to the Maniac caves (Ian's) | 43 | 42 | 6 |
| 9 | Gentleman Jeremy | Valor Lakefront (moved) | mandatory | 37 | 39 | 1 to 5 |
| 10 | Socialite Reina | Valor Lakefront (moved) | mandatory | 37 | 40 | 1 to 5 |
| 11 | Beauty Cyndy | Route 213 | mandatory (now looks one way) | 37 | 40 | 1 to 5 |
| 12 | Tuber Chelsea | Route 213 | mandatory (now looks one way) | 37 | 40 | 1 to 4 |
| 13 | Tuber Jared | Route 213 | mandatory (now looks one way) | 36 | 40 | 3 to 4 |
| 14 | Fisherman Travis | Route 213 (moved) | mandatory | 38 | 41 | 2 to 4 |
| 15 | Fisherman Kenneth | Route 213 | optional (Covert Cloak reward) | 36 | 41 | 3 |
| 16 | Ranger Taylor | Route 212 South | optional | 30 | 40 | 2 to 3 |
| 17 | Scientist Shaun | Route 212 South | optional (Weakness Policy reward) | 37 | 40 | 2 to 4 |
| 18 | Parasol Lady Sabrina | Route 212 South | optional | 39 | 40 | 1 to 3 |
| 19 | Parasol Lady Alexa | Route 212 South | optional | 39 | 40 | 1 to 3 |
| 20 | Fisherman Juan | Route 212 South | optional | 36 | 40 | 1 to 3 |
| 21 | Fisherman Josh | Route 212 South | optional (Wide Lens reward) | 36 | 40 | 2 to 3 |
| 22 | Collector Dean | Route 212 South | optional | 37 | 41 | 2 to 5 |
| 23 | Policeman Danny | Route 212 South | optional (night) | 37 | 41 | 2 to 3 |
| 24 | Scientist Stefano | Route 212 South | optional | 38 | 41 | 1 to 3 |
| 25 | Ranger Allison | Route 212 South | optional, pair with Jeffrey | 39 | 41 | 2 to 3 |
| 26 | Ranger Jeffrey | Route 212 South | optional, pair with Allison | 39 | 41 | 1 to 3 |
| 27 | Policeman Caleb | Route 212 North | optional (night, walks; TM72 reward) | 35 | 41 | 2 to 3 |
| 28 | Policeman Dylan | Route 212 North | optional (night, walks) | 36 | 41 | 2 to 5 |
| 29 | Policeman Alex | Route 212 North | optional (night, walks) | 35 | 41 | 2 to 5 |
| 30 | Rich Boy Jason | Route 212 North | optional, pair with Melissa | 37 | 41 | 1 to 3 |
| 31 | Lady Melissa | Route 212 North | optional, pair with Jason | 37 | 41 | 1 to 3 |
| 32 | Policeman Bobby | Route 212 North | optional (night) | 34 | 41 | 2 to 4 |
| 33 | Tuber Jacky | Pastoria Gym | gym | 39 | 41 | 1 to 3 |
| 34 | Tuber Caitlyn | Pastoria Gym | gym | 39 | 41 | 3 to 4 |
| 35 | Sailor Damian | Pastoria Gym | gym | 39 | 42 | 2 to 3 |
| 36 | Fisherman Erick | Pastoria Gym | gym | 39 | 42 | 3 to 4 |
| 37 | Fisherman Walter | Pastoria Gym | gym | 39 | 42 | 1 to 3 |
| 38 | Sailor Samson | Pastoria Gym | gym, the last guard | 39 | 43 | 3 to 5 |

The pairs fought alone field six at most: Allison and Jeffrey 3 and 3, Jason and Melissa 3 and 3, and Devon and Douglas 5 between them.

Not climbed, and why:

- **Bosses:** Wake and his rematch, the three Pastoria Barrys, and Officers Tyche and Hermes with their six partners.
- **Collector Jamal:** Ian keeps him as he is.
- **The Restaurant's nine daily doubles:** they wait for a later pass, and their files are oxide's.
- **The Pokemon Mansion's maid knockout and its last fight (Rich Boy Liam or Lady Celeste):** it will be done with Darach.
- **The Surf trainers, met in Byron's split:** Route 213's Swimmers Sheltin, Evan, Mary and Haley and Sailor Paul, Fisherman Cody on Route 208, and Tubers Trenton and Mariel on Route 219. The OxiDex tags the last three to Wake's split only because their aces (43 and 44) sit over the caps of the splits their maps belong to.
- **The Valor Lakefront grunt:** fought after Wake's badge, so in Byron's split.

### The teams

Each line gives the team in send-out order and its one idea. Gym trainers carry water teams, the gym's theme.

| Trainer | Team | The idea |
|---|---|---|
| Psychic Abigail | Wobbuffet 37, Metang 38, Exeggutor 38, Bronzong 38, Gothitelle 39 | A Telepathy Wobbuffet (no trapping) with Counter, Mirror Coat, Encore and his base ROM's Destiny Bond, in front of Psychic types that punish physical answers and a Trick Room Bronzong. |
| Psychic Mitchell | Orbeetle 38, Hypno 38, Grumpig 38, Chimecho 39 | Screens from a pivoting Orbeetle, Hypnosis, then a Calm Mind bell behind them. |
| PI Carlos | Seaking 38, Absol 38, Ambipom 38, Togekiss 39 | The coin toss: a Razor Fang, a Scope Lens on Super Luck, a King's Rock Technician Ambipom, Serene Grace Air Slash and a Quick Claw. |
| Gentleman Jeremy | Persian 38, Chatot 38, Cinccino 38, Corviknight 39, Mr Rime 39 | Technician Fake Out and Taunt, Nasty Plot Chatter, Skill Link Cinccino, a Mirror Armor Corviknight, then Ice Body Mr. Rime. |
| Socialite Reina | Jumpluff 39, Lurantis 39, Salazzle 39, Sinistcha 39, Milotic 40 | The garden party: Infiltrator sleep, Growth, Corrosion Toxic, a matcha Sinistcha, Marvel Scale behind a Flame Orb. |
| Beauty Cyndy | Lopunny 39, Mismagius 39, Liepard 39, Florges 39, Sylveon 40 | Scrappy Jump Kick through ghosts, Will-O-Wisp into Hex, Prankster Thunder Wave, then Calm Mind Sylveon. |
| Tuber Chelsea | Pelipper 39, Golduck 39, Floatzel 39, Azumarill 40 | Her own rain: Drizzle, two Swift Swim members, Huge Power Azumarill. |
| Tuber Jared | Palossand 39, Gastrodon 39, Clodsire 39, Swampert 40 | Sandcastles: ground types that shrug off water, one Unaware Clodsire. |
| Fisherman Travis | Qwilfish 40, Wailord 40, Whiscash 40, Lapras 41 | Spikes on both layers, then Water Spout, a Curse Whiscash and a Serene Grace Lapras. |
| Fisherman Kenneth | Octillery 40, Lanturn 40, Dhelmise 41 | The catch: Sniper crits, Volt Absorb, a Poltergeist anchor. |
| Ranger Taylor | Carnivine 39, Decidueye 39, Luxray 40 | A ranger's partners: a trap plant, a ghost archer, a Guts lion. |
| Scientist Shaun | Rotom 39, Electivire 39, Pawmot 40, Magnezone 40 | The lab's voltage: Adaptability, Iron Fist, Analytic, a Weakness Policy. |
| Parasol Lady Sabrina | Bellossom 39, Leavanny 39, Venusaur 40 | Her own sun: Sunny Day with a Heat Rock, then Chlorophyll. |
| Parasol Lady Alexa | Vileplume 39, Roserade 39, Toxapex 40 | Poison spores, Toxic Spikes, a Regenerator wall. |
| Fisherman Juan | Huntail 39, Gorebyss 39, Relicanth 40 | Deep-sea fish: Agility Gorebyss, a Sturdy Relicanth. |
| Fisherman Josh | Sharpedo 39, Kingler 40, Jellicent 40 | Speed Boost, Sheer Force, Cursed Body. |
| Collector Dean | Umbreon 40, Glaceon 40, Espeon 40, Flareon 40, Vaporeon 41 | Eevee's evolutions. |
| Policeman Danny | Noctowl 40, Houndoom 40, Machamp 41 | The night beat: Tinted Lens, Nasty Plot, No Guard Dynamic Punch. |
| Scientist Stefano | Glimmora 40, Swalot 40, Muk 41 | Toxic waste: Toxic Debris and Stealth Rock, then things that live in it. |
| Ranger Allison | Leafeon 40, Kangaskhan 40, Tangrowth 41 | With Jeffrey: Magic Guard grass, Scrappy, Regenerator. |
| Ranger Jeffrey | Ursaring 40, Donphan 40, Tauros 41 | With Allison: wild beasts, Guts and Sheer Force. |
| Policeman Caleb | Sandslash 40, Skuntank 40, Honchkrow 41 | Moxie at night behind Stealth Rock. |
| Policeman Dylan | Granbull 40, Marowak 40, Dodrio 40, Manectric 40, Arcanine 41 | The dog unit, a Thick Club, a Quick Feet bird and a Lightning Rod Manectric. |
| Policeman Alex | Electrode 40, Pidgeot 40, Crobat 40, Talonflame 40, Ninetales 41 | The sirens: a fast screen setter that may Explode, Gale Wings Aerial Ace, then Nasty Plot Ninetales. |
| Rich Boy Jason | Delphox 40, Serperior 40, Feraligatr 41 | With Melissa: a starter collection, his half. |
| Lady Melissa | Primarina 40, Gardevoir 40, Sceptile 41 | With Jason: her half, Trick Room beside Sceptile. |
| Policeman Bobby | Raichu 40, Mightyena 40, Swellow 40, Staraptor 41 | The patrol's fliers and a Moxie hound. |
| Tuber Jacky | Bibarel 40, Quagsire 40, Floatzel 41 | Simple Curse, an Unaware wall, a Bulk Up Floatzel. |
| Tuber Caitlyn | Lumineon 40, Seaking 40, Azumarill 40, Alomomola 41 | Belly Drum Azumarill behind a Regenerator nurse. |
| Sailor Damian | Pelipper 41, Kabutops 41, Crawdaunt 42 | Rain for the gym: Drizzle, Swift Swim, Adaptability Crabhammer. |
| Fisherman Erick | Lanturn 41, Mantine 41, Greninja 41, Gyarados 42 | Protean and Moxie behind a Volt Absorb lead. |
| Fisherman Walter | Politoed 41, Dewgong 41, Whiscash 42 | The old man's rain: Drizzle and a Swift Swim Whiscash. |
| Sailor Samson | Tentacruel 42, Golduck 42, Kingler 42, Jellicent 42, Starmie 43 | The last guard: Toxic Spikes, Life Orb Sheer Force, Cursed Body, Analytic. |

No rebuilt team carries a one-hit KO move, an evasion move or item, a Choice item, or trapping. Two forced trades come in, once each, under Ian's ruling of 2026-10-31: Abigail's Wobbuffet has Destiny Bond, and Alex's Electrode has Explosion. The setup moves used are Calm Mind, Nasty Plot, Swords Dance, Bulk Up, Curse, Belly Drum, Growth, Agility and Trick Room.

## Route 214

Ian ruled on 2026-10-29 that Ruin Maniac Bryan, Beauty Devon, Collector Douglas, Ruin Maniac Ronald and Krystal are his, built before Oxide went past Generation 4. He also added blockages to the route. On 2026-10-31 he approved the three trainer changes above, and asked for his teams to climb by level only. Krystal gets back the team from his base ROM.

His blockages are carried over from his base ROM (d3e44ec93) and untouched:

- **Two Strength boulders** at (717, 667) and (718, 667) close the west branch south of the berry field until Strength (Candice's split). Behind them sit Krystal, the Maniac caves and the west half of the route.
- **A vent** at (733, 716) closes the east column past Devon and Douglas, so every way south crosses the row they watch.
- **Krystal** stands at (715, 669), looking south, beside the boulders. She is reached from below, through the west half.
- **Devon is placed twice:** the walking copy at (729, 685), on the old Collector Brady's spot, and a fixed copy at (728, 718) facing Douglas. Beating either beats both.

### His teams, by level only

Each member moved by the same step, so each team keeps its shape. Devon, Douglas, Bryan and Ronald top out at the route's line of 39; Krystal tops at 42, as Ian chose, since she gates the Maniac caves. A member that named no nature would have its nature re-rolled by the level change, since the game rolls an unnamed one from the level. So Devon's, Douglas's, Bryan's and Krystal's members are each pinned by name to the nature they rolled before the climb. Ronald did not move and names none.

| Trainer | Team after the climb | Old top | New top |
|---|---|---:|---:|
| Beauty Devon | Spinda 39, Clefable 38 | 38 | 39 |
| Collector Douglas | Banette 38, Typhlosion 37, Octillery 39 | 37 | 39 |
| Ruin Maniac Bryan | Hippowdon 38, Corsola 39, Steelix 36, Aerodactyl 38, Leafeon 38 | 37 | 39 |
| Ruin Maniac Ronald | Feraligatr 35, Drifblim 35, Dugtrio 36, Chimecho 39, Ursaring 36 (unchanged) | 39 | 39 |
| Krystal (`dummy_795`) | Metang 39, Glalie 37, Jumpluff 40, Heat Rotom 38, Blaziken 36, Dragonair 42 | 43 (the comb's draft; 44 in his base ROM) | 42 |

Krystal's party and AI flags are the version at d3e44ec932f, before the comb's a725942be8b: Quick Claw Metang, Icicle Plate Glalie, Yache Berry Jumpluff, Life Orb Heat Rotom, Liechi Berry Blaziken and Draco Plate Dragonair, each with his moves. Her levels are two under his base ROM's each, Dragonair from 44 to 42, off the cap. Her natures are pinned to what she rolls today: Bashful, Lonely, Quirky, Gentle, Modest and Naive.

Ian's words, that she is "meant to be a hard fight gating the encounter in ruin maniac cave/tunnel", hold on the map. The Maniac caves' one warp, at (713, 670), opens only from (714, 670), which is reached only across (715, 670), the one tile Krystal sees. required.py's field model finds the warp reachable from Route 214's gate, and unreachable when her sight is avoided. This holds in Wake's, Byron's and Candice's splits, so also after Strength opens the boulders.

### The rules Ian's kept sets break

These are listed for Ian and not fixed. Every illegal move here was illegal at the old levels too.

- **Devon:** both members roll Gentle, a repeated nature.
- **Douglas:** Typhlosion's Eruption and Octillery's Water Spout are on no list of theirs.
- **Bryan:**
  - Hippowdon's Sand Tomb is trapping, now occasionally acceptable.
  - Corsola's Defense Curl, Aerodactyl's Tailwind and Leafeon's Leaf Blade are on no list of theirs.
  - His Hippowdon is Adamant, a textbook nature.
- **Ronald:** Drifblim's Selfdestruct (a forced trade, kept on Ian's word and on no list of Drifblim's) and Dugtrio's Arena Trap (trapping, kept).
- **Krystal:**
  - Ten moves are on no list of their species: Metang's Meteor Mash, Dynamic Punch and Gravity; Glalie's Sing and Weather Ball; Rotom's Overheat and Sunny Day (read against plain Rotom's lists, so a Heat Rotom may well have Overheat); Blaziken's Dynamic Punch, Flare Blitz and Brave Bird; and Dragonair's Extreme Speed.
  - Glalie at 37 sits five under the level it evolves at (42), which his base ROM had at three under. Blaziken is at its level, 36.
  - Her team carries two sleep moves (Glalie's Sing, Jumpluff's Sleep Powder).

Under Ian's ruling of 2026-10-29, a move on his team that its species cannot have goes on the egg list of the line's first stage, never by moving a level-up entry. All sixteen are now there:

| First stage | Moves | For |
|---|---|---|
| Cyndaquil | Eruption | Douglas's Typhlosion |
| Remoraid | Water Spout | Douglas's Octillery |
| Corsola | Defense Curl | Bryan's Corsola |
| Aerodactyl | Tailwind | Bryan's Aerodactyl |
| Eevee | Leaf Blade | Bryan's Leafeon |
| Drifloon | Selfdestruct | Ronald's Drifblim |
| Beldum | Meteor Mash, Dynamic Punch, Gravity (a new egg list) | Krystal's Metang |
| Snorunt | Sing, Weather Ball | Krystal's Glalie |
| Torchic | Dynamic Punch, Flare Blitz, Brave Bird | Krystal's Blaziken |
| Dratini | Extreme Speed | Krystal's Dragonair |
| Rotom | Overheat, Sunny Day | Krystal's Heat Rotom, which shares plain Rotom's lists |

Each is in `learnrewrite.IAN_EGG_MOVES` too, so a generator write keeps it, except Eevee's, which is in `learnsets_by_hand.txt` because Eevee's line is held out of the generator. The illegal-move entries in the list above are therefore settled, and the rest of each kept set's breaks stand.

## How the numbers were made

The split's trainers came from `trainers.split_map` (the OxiDex's tagging, 86 files) and `balance.splits`, read against each map's events and scripts. Play order follows the story path's order of maps, then each trainer's tile, and in the gym the distance from the door. The mandatory verdicts are `tools.oxide.balance.required` on the edited events. Reachability was checked with its own field model, old events against new.

The teams were written as data, then checked before saving by a script built on the Kaizo study's legality reader (`out/tools/oxide.py`). That reader was pointed at this branch's `res/`, and at the pre-TM-pass export of 5c62989651. A move is legal when the species or an earlier stage learns it by level at or below its level, when it is on the line's egg list, or when it is a TM or tutor move of the line, now or before the TM pass.

Every team was then saved through `tools.oxide.encounters.trainers.save`. That runs the trainer lint and the real packer, and records the file in `trainers_diverged.json`. A second pass reread every saved file, checking for lint findings, illegal moves, repeated items and natures, and banned moves and items.

The Kaizo comb's drafts for these trainers were read for ideas, such as Dean's Eevee evolutions. No draft was copied: each team uses Oxide's later moves and abilities, at Oxide's levels.

| Check | Result |
|---|---|
| Trainer lint, all 37 changed teams | no errors, no warnings |
| The real packer, through `trainers.save` | every team packed |
| Moves legal at their level, the rebuilt teams | all legal |
| Item or nature repeated in a rebuilt team, nature unnamed | none |
| One-hit KO, trapping, evasion, Choice item, rebuilt teams | none; two forced trades on purpose |
| `test_trainers` | 44 of 44 |
| `test_b1e` | 8 of 8 |
| `rewards.py check` | 0 failures |

### Speed against the box

Goal 3's Wake boxes (seeds 1 to 3) at 44 put these fast answers at the top: Crobat 126, Talonflame 122, Weavile 121, Greninja 118, Staraptor and Mienshao 104, Delphox 103. At 41, about the line a mid-split player rides, each is 7 to 9 lower. Box members are read at IV 15 with neutral natures, and trainers at their own IVs and natures. Each rebuilt team's fastest member:

| Fastest member | Speed | Teams |
|---|---:|---|
| above every answer | 125 to 141 | Alex's Electrode (a screen setter), Erick's Greninja, Melissa's Sceptile |
| among the fast answers | 100 to 122 | Jacky's Floatzel, Bobby's Swellow, Jeffrey's Tauros, Samson's Starmie, Cyndy's Liepard, Dean's Espeon, Jeremy's Persian, Dylan's Dodrio, Carlos's Ambipom, Reina's Jumpluff, Danny's Houndoom, Jason's Serperior, Chelsea's Floatzel, Shaun's Pawmot |
| under the fast answers | 61 to 97 | the other 16 teams |

### Damage in the key exchanges

Each row is the trainer's member against a box member at its level. It is a rough estimate with no weather, with any ability named applied by hand.

| Exchange | Damage |
|---|---:|
| Chelsea's Azumarill 40, Huge Power Waterfall, into Talonflame 42 | 124 to 146% |
| Torterra 42, Earthquake, into that Azumarill | 51 to 60% |
| Reina's Salazzle 39, Flamethrower, into Torterra 42 | 61 to 72% |
| Reina's Lurantis 39, Leaf Blade, into Whiscash 42 | 160 to 188% |
| Danny's Machamp 41, Muscle Band Dynamic Punch, into Corviknight 42 | 55 to 64% |
| Damian's Crawdaunt 42, Adaptability Crabhammer, into Torterra 44 (before rain) | 54 to 64% |
| Talonflame 44, Acrobatics, into that Crawdaunt | 28 to 32% |
| Samson's Kingler 42, Life Orb Crabhammer, into Luxray 44 | 78 to 92% |
| Luxray 44, Wild Charge, into that Kingler | 91 to 107% |
| Samson's Starmie 43, Expert Belt Thunderbolt, into Crobat 44 | 66 to 78% |
| Kenneth's Dhelmise 41, Spell Tag Poltergeist, into Delphox 42 | 177 to 208% |

The sharpest members are ones the box sees coming:

- Chelsea's Azumarill falls to the box's grass and electric hits.
- Damian's Crawdaunt sits behind rain the box can outspeed before it starts.
- Samson's Kingler trades evenly with Luxray.

No fight was read by the scorer, under the standing ruling.
