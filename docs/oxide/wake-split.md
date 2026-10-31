# Wake's split: mandatory fights, the level climb and Route 214

Wake's split (after Maylene, cap 39, to Wake, cap 44) went through the process Fantina's and Maylene's splits went through on 2026-10-29: the mandatory fights counted and raised, the trivial teams rebuilt, and the ordinary trainers' levels climbed in play order. It is a draft on the branch `overseer-wake-split`, not landed. Route 214 was read and left alone, as Ian asked.

## Summary

The split now holds 7 non-boss mandatory fights, up from 1, short of Ian's 10 to 15. Three more need placement changes on Route 214, which waits on Ian. Six trainers moved onto the story path: Route 213's three turners now look one fixed way at its chokepoints, Fisherman Travis left Route 212 South for Route 213, and Gentleman Jeremy and Socialite Reina left Route 212 North for Valor Lakefront.

51 ordinary teams were rebuilt. They climb from 39 on Route 214 to 42 in Pastoria's gym, with the gym's last guard, Sailor Samson, the one team at 43, and none at 44. Before, nearly all were vanilla one- and two-Pokemon teams, the Restaurant's at 25 to 31. 31 of the 164 rebuilt members are Oxide's later species, against none before. No member has an Adamant, Modest, Timid or Jolly nature. Every changed team passed the trainer lint and the real packer, every move is legal at its level, and no team repeats an item or a nature. No boss, no Route 214 team of Ian's and no hand-designed team was touched.

Two findings change what Wake's split holds. Barry 4 and the Valor Lakefront grunt are fought after Wake's badge, so they belong to Byron's split in play (question 1). The Surf trainers on these maps are met only in Byron's split too, now that Surf waits on Cyrus at Celestic Town as well, so they are left for Byron's climb.

What Ian decides:

1. Whether Barry 4 and the Valor Lakefront grunt move to Byron's split. Pastoria's gym script sets the city's story state to 3 when Wake falls; only then does Barry's scene run (state 4, at the Great Marsh gate), and his battle sets state 5, which brings the Galactic grunt out. The grunt runs to Route 213 (shown only with the Fen Badge) and then Valor Lakefront, where the battle is fought and Cynthia hands over the SecretPotion. So both fights sit after Wake. fights.json and the OxiDex still place Barry 4 in Wake's split, from the Level Caps sheet.
2. Whether to make the Route 214 changes below that take the count to 10. Abigail would look only west and Mitchell would stand looking south, both in place (the model reads each required that way). PI Carlos would move to the east edge of the narrows south of the berry field, at (733, 690), looking west with sight 2.
3. Whether to restore Krystal's team. Her file holds the Kaizo comb's draft of 2026-10-07, which replaced the team from your base ROM (that one had Dragonair at 44, the cap, with Life Orb Rotom and Icicle Plate Glalie).
4. Whether your Route 214 teams should climb or modernise (the read is below). Bryan, Devon and Douglas sit 1 to 3 under the climb's 39, Ronald on it, and Krystal at 43.
5. Whether Ronald's Drifblim keeps Selfdestruct and his Dugtrio keeps Arena Trap. One is a forced trade and the other trapping, neither allowed on an ordinary trainer.
6. Whether Collector Jamal stays as he is. He is a base-ROM Recycle team (Fling, Thick Club Delibird at 41) on Route 214, so I treated him as yours and left him.
7. Whether moving trainers across maps is acceptable: Travis, Jeremy and Reina leave Route 212 (off the path) for the story path.
8. Whether the Restaurant's nine daily doubles stand at three a side and 39 to 40. They repeat every day.
9. Whether the Pokemon Mansion's maid knockout (five Clefairy maids, then Liam or Celeste) stays the vanilla minigame. It is left alone.
10. Whether some teams should grow to 5 or 6. Most rebuilt teams carry 3 or 4, Collector Dean 5.

Next steps:

| Step | Who | Time |
|---|---|---|
| Ian answers the questions above | Ian | 15 minutes |
| The Route 214 changes, if he says yes | a helper | 30 minutes |
| The Overseer reviews and lands the branch with `merge-branch.sh` | the Overseer | 30 minutes |
| Ian plays the new checks in `docs/oxide/ingame-checklist.md` ("Mandatory fights, Wake's split") | Ian | 20 minutes with the test kit's warps |

What is unverified: everything in game; the moves come from the tile model. No fight was read by the scorer, the doubles were checked as singles, and the box sits at the cap, not the mid-split line. The trainer AI does not see some held items these teams carry, such as Weakness Policy and Rocky Helmet.

## The mandatory fights

Ian's rules of 2026-10-29 apply: gym trainers and bosses are not counted, a trainer who turns, spins or walks is optional, and a pair or a twins double is one fight. Two trainers fought alone together field six Pokemon at most.

The story path through the split is short: Veilstone, Route 214, Valor Lakefront, Route 213, Pastoria. Route 212 runs from Pastoria north to Hearthome and is off the path, so all its trainers are optional. The Great Marsh, the Maniac Tunnel and caves, the hotel and the Restaurant are optional too.

| # | Fight | Map | How it is known |
|---:|---|---|---|
| 1 | Beauty Devon and Collector Douglas, one eye-contact double (5 Pokemon) | Route 214 | required.py; `pairs.py` reads them always together |
| 2 | Gentleman Jeremy (new) | Valor Lakefront | required.py, after the move |
| 3 | Socialite Reina (new) | Valor Lakefront | required.py, after the move |
| 4 | Beauty Cyndy (new, now looks one way) | Route 213 | required.py, after the change |
| 5 | Tuber Chelsea (new, now looks one way) | Route 213 | required.py, after the change |
| 6 | Tuber Jared (new, now looks one way) | Route 213 | required.py, after the change |
| 7 | Fisherman Travis (new) | Route 213 | required.py, after the move |

Bosses: Officers Tyche and Hermes (the Veilstone tag beside Lucas or Dawn) and Wake. Barry 4 is fought after Wake's badge (question 1). The Pastoria gym's six trainers are gym trainers.

Optional on the path: Psychics Abigail and Mitchell and PI Carlos turn or walk on Route 214, and Ruin Maniacs Bryan and Ronald, Collector Jamal and Krystal stand off the path (below). Fisherman Kenneth stays where he was on Route 213, since he carries the Covert Cloak, and a reward belongs to an optional fight.

There is no gauntlet section in the split: `gauntlet.py` builds none here, and no stretch of the path is one-way.

### The trainers moved

Each keeps its team, class and script. The Route 213 turners now look one fixed way, as the Fantina and Maylene pass did for spinners.

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Gentleman Jeremy | Route 212 North (455, 796), turning north and east, sight 2 | Valor Lakefront (728, 740), looking east, sight 3 | The way in from Route 214 is a corridor four tiles wide (x 728 to 731) for ten rows. He stands at its west edge and sees the other three. |
| Socialite Reina | Route 212 North (458, 796), turning south and west, sight 3 | Valor Lakefront (720, 764), looking east, sight 5 | Below the grass the path narrows to six tiles (x 720 to 725) for six rows. She stands at its west edge and sees the other five. Cynthia's, Barry's and the grunt's later scenes walk at x 722 to 724, past her. |
| Beauty Cyndy | Route 213 (668, 827), turning west and east, sight 5 | (705, 822), looking east, sight 2 | Every way from the hotel down to the beach crosses rows 821 and 822 at x 705 to 707. She stands on the lower row and sees the other two tiles. |
| Tuber Chelsea | Route 213 (704, 827), turning three ways, sight 4 | (700, 831), looking south, sight 1 | West of the hotel's beach, a strip one tile wide (row 832, x 689 to 699) runs between the cliff and the sea. She stands above its entrance and sees it. |
| Tuber Jared | Route 213 (703, 832), walking, sight 3 | (670, 818), looking east, sight 7 | The beach joins the grass to Pastoria only through a neck eight tiles wide (x 670 to 677) and two rows deep. He stands at the west end of the south row and sees all of it. |
| Fisherman Travis | Route 212 South's bridge (499, 856), looking south, sight 0 | Route 213 (677, 817), looking west, sight 7 | At the east end of the neck's north row, seeing all of it. The player meets Jared, then Travis: two fights in a row, never one double (they see different rows). |

The checks, each run on the edited files: required.py reads all six required on the crossings Route 214, Valor Lakefront (a crossing added to its table) and Route 213; from every warp and map edge, in Wake's split and in Byron's and Candice's, the player still reaches every tile reachable before, the trainers' own tiles aside; no moved trainer stands on a warp, sign, hidden item, trigger or another object; and `pairs.py`'s eye-contact pairs lose Jeremy and Reina (they no longer share a tile) and gain none. The scripted walks on Route 213 (the grunt and Looker after Fen Badge) do not cross the new tiles. `test_b1e` passes 8 of 8, its totals pinned at 67 required and 107 avoidable. The four maps are declared in `bulk_events.py`'s DIVERGED.

## The level climb

Ordinary trainers climb in play order from 39 on Route 214 to 42 in the gym, never at 44, and the gym's last guard alone at 43. The Restaurant opens at Valor Lakefront, so its doubles sit at 39 and 40. Old and new are each team's highest level; size is old to new.

| # | Trainer | Area | Kind | Old | New | Size |
|---:|---|---|---|---:|---:|---|
| 1 | Psychic Mitchell | Route 214 | optional (turns) | 34 | 39 | 2 to 3 |
| 2 | Psychic Abigail | Route 214 | optional (turns) | 34 | 39 | 3 to 4 |
| 3 | PI Carlos | Route 214 | optional (turns; TM72 reward) | 36 | 39 | 1 to 3 |
| 4 | Gentleman Jeremy | Valor Lakefront (moved) | mandatory | 37 | 39 | 1 to 3 |
| 5 | Socialite Reina | Valor Lakefront (moved) | mandatory | 37 | 40 | 1 to 4 |
| 6 | Artist Ismael | Restaurant (daily double) | optional | 28 | 40 | 1 to 3 |
| 7 | Beauty Harley | Restaurant (daily double) | optional | 26 | 40 | 1 to 3 |
| 8 | Rich Boy Roman | Restaurant (daily double) | optional | 26 | 40 | 1 to 3 |
| 9 | Lady Kylie | Restaurant (daily double) | optional | 26 | 40 | 2 to 3 |
| 10 | Gentleman Leonardo | Restaurant (daily double) | optional | 27 | 40 | 1 to 3 |
| 11 | Socialite Rebecca | Restaurant (daily double) | optional | 27 | 40 | 1 to 3 |
| 12 | Collector Eugene | Restaurant (daily double) | optional | 28 | 40 | 1 to 3 |
| 13 | Aroma Lady Alison | Restaurant (daily double) | optional | 28 | 40 | 1 to 3 |
| 14 | School Kid Esteban | Restaurant (daily double) | optional | 26 | 40 | 1 to 3 |
| 15 | Pokefan Meredith | Restaurant (daily double) | optional | 26 | 40 | 2 to 3 |
| 16 | Veteran Emanuel | Restaurant (daily double) | optional | 28 | 40 | 2 to 3 |
| 17 | Lass Blythe | Restaurant (daily double) | optional | 25 | 40 | 2 to 3 |
| 18 | Cameraman Darryl | Restaurant (daily double) | optional | 26 | 40 | 2 to 3 |
| 19 | Reporter Valerie | Restaurant (daily double) | optional | 26 | 40 | 1 to 3 |
| 20 | PI Kendrick | Restaurant (daily double) | optional | 31 | 40 | 1 to 3 |
| 21 | Beauty Gabriella | Restaurant (daily double) | optional | 26 | 40 | 1 to 3 |
| 22 | Scientist Emilio | Restaurant (daily double) | optional | 27 | 40 | 1 to 3 |
| 23 | Breeder Kaylee | Restaurant (daily double) | optional | 26 | 40 | 3 to 3 |
| 24 | Beauty Cyndy | Route 213 | mandatory (now looks one way) | 37 | 40 | 1 to 3 |
| 25 | Tuber Chelsea | Route 213 | mandatory (now looks one way) | 37 | 40 | 1 to 3 |
| 26 | Tuber Jared | Route 213 | mandatory (now looks one way) | 36 | 40 | 3 to 4 |
| 27 | Fisherman Travis | Route 213 (moved) | mandatory | 38 | 41 | 2 to 3 |
| 28 | Fisherman Kenneth | Route 213 | optional (Covert Cloak reward) | 36 | 41 | 3 to 3 |
| 29 | Ranger Taylor | Route 212 South | optional | 30 | 40 | 2 to 3 |
| 30 | Scientist Shaun | Route 212 South | optional (Weakness Policy reward) | 37 | 40 | 2 to 4 |
| 31 | Parasol Lady Sabrina | Route 212 South | optional | 39 | 40 | 1 to 3 |
| 32 | Parasol Lady Alexa | Route 212 South | optional | 39 | 40 | 1 to 3 |
| 33 | Fisherman Juan | Route 212 South | optional | 36 | 40 | 1 to 3 |
| 34 | Fisherman Josh | Route 212 South | optional (Wide Lens reward) | 36 | 40 | 2 to 3 |
| 35 | Collector Dean | Route 212 South | optional | 37 | 41 | 2 to 5 |
| 36 | Policeman Danny | Route 212 South | optional (night) | 37 | 41 | 2 to 3 |
| 37 | Scientist Stefano | Route 212 South | optional | 38 | 41 | 1 to 3 |
| 38 | Ranger Allison | Route 212 South | optional, pair with Jeffrey | 39 | 41 | 2 to 3 |
| 39 | Ranger Jeffrey | Route 212 South | optional, pair with Allison | 39 | 41 | 1 to 3 |
| 40 | Policeman Caleb | Route 212 North | optional (night) | 35 | 41 | 2 to 3 |
| 41 | Policeman Dylan | Route 212 North | optional (night) | 36 | 41 | 2 to 4 |
| 42 | Policeman Alex | Route 212 North | optional (night) | 35 | 41 | 2 to 3 |
| 43 | Rich Boy Jason | Route 212 North | optional, pair with Melissa | 37 | 41 | 1 to 3 |
| 44 | Lady Melissa | Route 212 North | optional, pair with Jason | 37 | 41 | 1 to 3 |
| 45 | Policeman Bobby | Route 212 North | optional (night) | 34 | 41 | 2 to 4 |
| 46 | Tuber Jacky | Pastoria Gym | gym | 39 | 41 | 1 to 3 |
| 47 | Tuber Caitlyn | Pastoria Gym | gym | 39 | 41 | 3 to 4 |
| 48 | Sailor Damian | Pastoria Gym | gym | 39 | 42 | 2 to 3 |
| 49 | Fisherman Erick | Pastoria Gym | gym | 39 | 42 | 3 to 4 |
| 50 | Fisherman Walter | Pastoria Gym | gym | 39 | 42 | 1 to 3 |
| 51 | Sailor Samson | Pastoria Gym | gym, the last guard | 39 | 43 | 3 to 4 |

The pairs fought alone field six at most: Allison and Jeffrey 3 and 3, Jason and Melissa 3 and 3, each Restaurant pair 3 and 3. Devon and Douglas, Ian's, field 5.

Not climbed, and why:

- Bosses: Wake and his rematch, the three Pastoria Barrys, Officers Tyche and Hermes and their six partners.
- Ian's Route 214 teams (Bryan, Devon, Douglas, Ronald, Krystal) and Collector Jamal (question 6).
- Met only with Surf, so in Byron's split: Route 213's Swimmers Sheltin, Evan, Mary and Haley and Sailor Paul, Fisherman Cody on Route 208, and Tubers Trenton and Mariel on Route 219. The OxiDex tags the last three to Wake's split only because their aces (43 and 44) sit over the caps of the splits their maps belong to.
- The Valor Lakefront grunt, fought after Wake's badge (question 1).
- The Pokemon Mansion's maid knockout and its last fight (Rich Boy Liam or Lady Celeste), a timed minigame (question 9).

### The teams

Each line gives the team in send-out order and its one idea. Gym trainers carry water teams, the gym's theme.

| Trainer | Team | The idea |
|---|---|---|
| Psychic Mitchell | Orbeetle 38, Hypno 38, Chimecho 39 | Screens from a pivoting Orbeetle, Hypnosis, then a Calm Mind bell behind them. |
| Psychic Abigail | Wobbuffet 37, Metang 38, Exeggutor 38, Gothitelle 39 | A Counter and Mirror Coat wall (Telepathy, no trapping) in front of Psychic types that punish physical answers. |
| PI Carlos | Seaking 38, Absol 38, Togekiss 39 | The coin toss: a Razor Fang, a Scope Lens on Super Luck, Serene Grace Air Slash and a Quick Claw. |
| Gentleman Jeremy | Persian 38, Chatot 38, Mr Rime 39 | Technician Fake Out and Taunt, Nasty Plot Chatter, then Ice Body Mr. Rime. |
| Socialite Reina | Jumpluff 39, Lurantis 39, Salazzle 39, Milotic 40 | The garden party: Infiltrator sleep, Growth, Corrosion Toxic, Marvel Scale behind a Flame Orb. |
| Artist Ismael | Kecleon 39, Mr Mime 39, Toucannon 40 | With Harley: Protean Fake Out, screens, a Skill Link bird. |
| Beauty Harley | Golduck 39, Florges 39, Masquerain 40 | With Ismael: spread water, Calm Mind fairy, Intimidate. |
| Rich Boy Roman | Lickilicky 39, Ursaring 39, Snorlax 40 | With Kylie: big eaters behind her Follow Me. |
| Lady Kylie | Clefable 40, Wigglytuff 39, Chansey 39 | With Roman: Follow Me, Helping Hand and Heal Bell. |
| Gentleman Leonardo | Arcanine 39, Bronzong 39, Corviknight 40 | With Rebecca: Intimidate, Trick Room behind a Mental Herb, Mirror Armor. |
| Socialite Rebecca | Purugly 39, Liepard 39, Meowscarada 40 | With Leonardo: cats, Prankster Thunder Wave, Flower Trick. |
| Collector Eugene | Carbink 39, Sinistcha 39, Milotic 40 | With Alison: rare finds under Trick Room. |
| Aroma Lady Alison | Floette 39, Roserade 39, Meganium 40 | With Eugene: a flower bed with Helping Hand and Technician. |
| School Kid Esteban | Slowking 40, Golem 39, Quagsire 38 | With Meredith: a slow class under Trick Room. |
| Pokefan Meredith | Pachirisu 39, Emolga 39, Ampharos 40 | With Esteban: Ampharos's Discharge feeds Volt Absorb and Motor Drive beside it. |
| Veteran Emanuel | Hariyama 40, Steelix 39, Medicham 39 | With Blythe: Fake Out, Sheer Force steel, Pure Power. |
| Lass Blythe | Lopunny 39, Chimecho 39, Mawile 40 | With Emanuel: Scrappy kicks, Heal Bell, Intimidate. |
| Cameraman Darryl | Magneton 39, Mr Mime 39, Porygon2 40 | With Valerie: the crew's gadgets, Trick Room twice over. |
| Reporter Valerie | Exploud 39, Xatu 39, Gallade 40 | With Darryl: Tailwind from a Magic Bounce Xatu, then hitters. |
| PI Kendrick | Spiritomb 39, Dusknoir 39, Weavile 40 | With Gabriella: the detective's shadows, Trick Room or Fake Out. |
| Beauty Gabriella | Lumineon 39, Jynx 39, Froslass 40 | With Kendrick: ice and the sea, Tailwind and Lovely Kiss. |
| Scientist Emilio | Klefki 39, Vikavolt 39, Alakazam 40 | With Kaylee: Prankster screens behind Magic Guard Alakazam. |
| Breeder Kaylee | Ambipom 39, Azumarill 39, Altaria 40 | With Emilio: the babies she raised, grown: Technician Fake Out, Huge Power. |
| Beauty Cyndy | Lopunny 39, Mismagius 39, Sylveon 40 | Scrappy Jump Kick through ghosts, Will-O-Wisp into Hex, Calm Mind Sylveon. |
| Tuber Chelsea | Pelipper 39, Golduck 39, Azumarill 40 | Her own rain: Drizzle, a Swift Swim Golduck, Huge Power Azumarill. |
| Tuber Jared | Palossand 39, Gastrodon 39, Clodsire 39, Swampert 40 | Sandcastles: ground types that shrug off water, one Unaware Clodsire. |
| Fisherman Travis | Qwilfish 40, Wailord 40, Lapras 41 | Spikes on both layers, then Water Spout and a Serene Grace Lapras. |
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
| Policeman Dylan | Granbull 40, Marowak 40, Dodrio 40, Arcanine 41 | The dog unit, a Thick Club and a Quick Feet bird. |
| Policeman Alex | Electrode 40, Pidgeot 40, Ninetales 41 | The sirens: a fast screen setter, then Nasty Plot Ninetales. |
| Rich Boy Jason | Delphox 40, Serperior 40, Feraligatr 41 | With Melissa: a starter collection, his half. |
| Lady Melissa | Primarina 40, Gardevoir 40, Sceptile 41 | With Jason: her half, Trick Room beside Sceptile. |
| Policeman Bobby | Raichu 40, Mightyena 40, Swellow 40, Staraptor 41 | The patrol's fliers and a Moxie hound. |
| Tuber Jacky | Bibarel 40, Quagsire 40, Floatzel 41 | Simple Curse, an Unaware wall, a Bulk Up Floatzel. |
| Tuber Caitlyn | Lumineon 40, Seaking 40, Azumarill 40, Alomomola 41 | Belly Drum Azumarill behind a Regenerator nurse. |
| Sailor Damian | Pelipper 41, Kabutops 41, Crawdaunt 42 | Rain for the gym: Drizzle, Swift Swim, Adaptability Crabhammer. |
| Fisherman Erick | Lanturn 41, Mantine 41, Greninja 41, Gyarados 42 | Protean and Moxie behind a Volt Absorb lead. |
| Fisherman Walter | Politoed 41, Dewgong 41, Whiscash 42 | The old man's rain: Drizzle and a Swift Swim Whiscash. |
| Sailor Samson | Tentacruel 42, Golduck 42, Kingler 42, Starmie 43 | The last guard: Toxic Spikes, Life Orb Sheer Force, Analytic. |

No ordinary team carries a one-hit KO move, a forced trade (Explosion, Self-Destruct, Destiny Bond, Memento) or a trapping move or ability,. No team carries an evasion move or item. Setup moves used: Calm Mind, Nasty Plot, Swords Dance, Bulk Up, Curse, Belly Drum, Growth, Agility, Trick Room.

## Route 214, read only

Ian ruled on 2026-10-29 that Ruin Maniac Bryan, Beauty Devon, Collector Douglas, Ruin Maniac Ronald and Krystal are his, built before Oxide went past Generation 4, and he added blockages to the route. Nothing on the route or in those five files changed.

The blockages, from his base ROM (carried over in d3e44ec93):

- Two Strength boulders at (717, 667) and (718, 667) close the west branch south of the berry field until Strength (Candice's split). Behind them sit Krystal, the Maniac caves and the west half of the route.
- A vent at (733, 716) closes the east column past Devon and Douglas, so every way south crosses the row they watch.
- Krystal stands at (715, 669), looking south, beside the boulders; she is reached from below, through the west half.
- Devon is placed twice: the walking copy at (729, 685) on the old Collector Brady's spot, and a fixed copy at (728, 718) facing Douglas. Beating either beats both.

Which are mandatory: Devon and Douglas, as one eye-contact double of 5 Pokemon at the route's south end. Bryan, Ronald and Krystal stand on the west half, which the player can walk into from the south and leave the same way, so all three are optional. Abigail, Mitchell and Carlos turn, and Jamal can be walked round.

Ian's teams against the climb, whose line on Route 214 is 39:

| Trainer | Team (level, item) | Top | Against the climb |
|---|---|---:|---|
| Beauty Devon | Spinda 38 Quick Claw (Teeter Dance, Faint Attack, Fake Out, Last Resort); Clefable 37 Sitrus Berry (Follow Me, Belly Drum, Copycat, Last Resort) | 38 | 1 under |
| Collector Douglas | Banette 36 Sticky Barb (Curse, Icy Wind, Will-O-Wisp, Shadow Sneak); Typhlosion 35 Power Herb (Eruption, Thunder Punch, Solar Beam, Focus Blast); Octillery 37 Scope Lens (Water Spout, Aurora Beam, Focus Energy, Signal Beam) | 37 | 2 under |
| Ruin Maniac Bryan | Hippowdon 36 Leftovers (Stealth Rock, Yawn, Fire Fang, Sand Tomb); Corsola 37 Zoom Lens (Toxic, Light Screen, Defense Curl, Rollout); Steelix 34 Iron Plate (Iron Tail, Screech, Thunder Fang, Slam); Aerodactyl 36 Lum Berry (Aerial Ace, Stone Edge, Thunder Fang, Tailwind); Leafeon 36 Shell Bell (X-Scissor, Roar, Leaf Blade, Iron Tail) | 37 | 2 under |
| Ruin Maniac Ronald | Feraligatr 35 Muscle Band (Dragon Dance, Superpower, Outrage, Aqua Tail); Drifblim 35 Sitrus Berry (Selfdestruct, Payback, Tailwind, Shadow Ball); Dugtrio 36 Focus Sash, Arena Trap (Night Slash, Dig, Aerial Ace, Stone Edge); Chimecho 39 Colbur Berry (Psychic, Calm Mind, Attract, Charge Beam); Ursaring 36 Flame Orb (Facade, Superpower, Thunder Punch, Shadow Claw) | 39 | on the line |
| Krystal (`dummy_795`) | Metang 42, Glalie 42, Jumpluff 42, Rotom 42, Blaziken 42, Dragonair 43: the comb's draft (question 3) | 43 | 4 over, 1 under the cap |

None of the five names a nature, so each is rolled from the level. Bryan's Sand Tomb is trapping, Ronald's Selfdestruct a forced trade and his Dugtrio's Arena Trap trapping (question 5).

## How the numbers were made

The split's trainers came from `trainers.split_map` (the OxiDex's tagging, 86 files) and `balance.splits`, read against each map's events and scripts. Play order is the story path's order of maps, each trainer's tile, and, in the gym, distance from the door. The mandatory verdicts are `tools.oxide.balance.required` on the edited events; reachability was checked with its own field model, old events against new.

Teams were written as data and checked before saving by a script built on the Kaizo study's legality reader (`out/tools/oxide.py`), pointed at this branch's `res/` and at the pre-TM-pass export of 5c62989651. A move is legal when the species or an earlier stage learns it by level at or below its level, it is on the line's egg list, or it is a TM or tutor move of the line now or before the TM pass. Every team was then saved through `tools.oxide.encounters.trainers.save`, which runs the trainer lint and the real packer and records the file in `trainers_diverged.json`. A second pass reread every saved file for lint findings, legality, repeated items and natures, banned moves and items. The results:

| Check | Result |
|---|---|
| Trainer lint, every changed team | no errors, no warnings |
| The real packer, through `trainers.save` | all 51 packed |
| Moves legal at their level | all legal |
| Item or nature repeated in a team, nature unnamed | none |
| One-hit KO, forced trade, trapping, evasion, Choice item | none |
| `test_trainers` | 44 of 44 |
| `test_b1e` | 8 of 8 |
| `rewards.py check` | 0 failures |
| Build (`make rom` in the worktree) | built |

The Kaizo comb's drafts for these trainers were read for ideas, such as Dean's Eevee evolutions. No draft was copied: each team uses Oxide's later moves and abilities, at Oxide's levels.

### Speed against the box

Goal 3's Wake boxes (seeds 1 to 3) at 44 put these fast answers at the top: Crobat 126, Talonflame 122, Weavile 121, Greninja 118, Staraptor and Mienshao 104, Delphox 103. At 41, about the line a mid-split player rides, each is 7 to 9 lower. Each team's fastest member (box members at IV 15 and neutral natures; trainers at their own IVs and natures):

| Fastest member | Speed | Teams |
|---|---:|---|
| above every answer | 125 to 141 | Alex's Electrode (a screen setter), Erick's Greninja, Kendrick's Weavile, Melissa's Sceptile |
| among the fast answers | 100 to 122 | Jacky's Floatzel, Bobby's Swellow, Jeffrey's Tauros, Samson's Starmie, Dean's Espeon, Rebecca's Liepard, Kaylee's Ambipom, Jeremy's Persian, Dylan's Dodrio, Reina's Jumpluff, Emilio's Alakazam, Danny's Houndoom, Jason's Serperior, Blythe's Lopunny, Meredith's Emolga, Gabriella's Froslass, Shaun's Pawmot |
| under the fast answers | 61 to 97 | 28 teams |
| slow on purpose | under 60 | Roman's Ursaring and Esteban's Golem, both under Trick Room partners |

### Damage in the key exchanges

The trainer's member against a box member at its level; a rough estimate with no weather, and with abilities applied by hand where named.

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
| Rebecca's Meowscarada 40, Flower Trick, into Whiscash 42 | 167 to 197% |

The sharpest members are ones the box sees coming: Chelsea's Azumarill falls to the box's grass and electric hits, Damian's Crawdaunt sits behind rain the box can outspeed before it starts, and Samson's Kingler trades evenly with Luxray. No fight was read by the scorer, under the standing ruling.
