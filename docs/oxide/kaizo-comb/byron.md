# The comb: Byron's split

**Every trainer of Byron's split is now combed.** The bosses were combed
earlier. On 2026-10-07 I added all 52 ordinary trainers, in walking order.
Every file passes the checker and the rule audit.

Kaizo has few of this split's trainers by name. Most ideas come from Kaizo's
teams at the same places: the Canalave gym's Hiker David, Idol Skylar and
Scientist Bill, its Iron Island Galactic pairs, and its Fuego Ironworks
workers, scaled down from level 90. The rest of the ideas are mine. Each team
then moves into Oxide's Generation 5+ pool where the species' lists allow,
and is scaled to the dial, as Ian ruled on 2026-10-07.

| Check | Result |
|---|---|
| Single battles read blind (43) | 93 to 100 won, mean 96.5 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 65 to 88, mean 76 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.26 to 1.06, mean 0.69 |
| The double (Zac and Jen) and Iron Island's eight tag files | not readable yet |
| Move slots that are Generation 5+ | 105 of 788, 13 percent |
| Hidden abilities | 38, on 30 of 52 teams |
| Element 7 items held | 11: three Rocky Helmets, two Air Balloons, two Covert Cloaks, an Assault Vest, an Eviolite, a Mirror Herb and a Clear Amulet |

The ordinary trainers read a step harder than Maylene's (mean 98.7 won).
The first build read 62 to 99 won. Six rounds then took boosting items off
the strongest members, kept setup only where it carries a team's idea, gave
the top level to a bulky or support member, and cut four optional five-member
teams to four. The dial's floor limits how far levels can soften. Each
member must sit within three levels of the highest, and the highest one or
two under the cap, so every member stands at 48 or above against a box at 53
that knows no TMs. The scorer's step 15 reading decides any further change.

Three trainers award an item and hold it: Swimmer Adrian (Zoom Lens),
Swimmer Jessica (Mirror Herb) and Fisherman Cory (Clear Amulet). Veteran
Brian, the split's one ordinary single on the path, previews Byron's screens
alone. Canalave's gym trainers each pair two of Byron's tools: Stealth Rock,
Spikes, screens, phazing and a setup move.

Two teams carry no modern move although their species have one:

| Team | Why no modern move |
|---|---|
| Bird Keeper Brianna | Pidgeot, Swellow and Skarmory have none. Tropius's options (Dual Wingbeat, Bulldoze, Stomping Tantrum) are physical, on a set built on special attacks. |
| Fisherman Cory | Seadra, Dragonair and Gyarados have none. Sharpedo's only one, Bulldoze, is weaker than the moves it carries. |

My simulator does not model a few things these teams use. These are Sticky
Web (Galvantula), White Herb, Mirror Herb, Zoom Lens and Wide Lens, Harvest,
Memento, and Rage Fist's growing power. Each of those teams reads a little
softer than it plays.

## The bosses, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of Byron's split are combed: Ace Trainers Ernest and Alyssa on
Route 210 north, Officer Argo and Cyrus at Celestic Town, Barry 5 (three
files) on Canalave's bridge, gym trainers Cesar and Breanna, Byron, the
Iron Island tag pair Jonah and Brenda, and the optional Ace Trainers Jake and
Shannon on Route 221.

The cap is 53 throughout. My simulator reads the bosses against the
scorer's box at Byron, which knows no TMs, so they read harsher than they
will once the TM pass lands. It now models Explosion, screens, phazing,
Perish Song and Protect, and each map's own weather, so today's files were
read again beside mine. Each boss is a step harder than today's: Cyrus about
90 won to today's 100, Byron about 89 to today's 99.6, and Argo and Barry 5
level on wins with far more faints. No map in this split has its own
weather. Barry's Ambipom keeps Last Resort, the split's one conditional
attack. The new rules show in two places: Cyrus's Exploud carries Fire Blast
and Focus Blast, which miss more than one time in ten, and Jake's Super Luck
Absol holds a Scope Lens.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Byron's six | Byron's dial is two hazards, screens and a legendary, every member Steel. Bastiodon leads with Stealth Rock and Roar behind a Focus Sash, Skarmory adds Spikes and Whirlwind, Magnezone sets both screens on a Light Clay, Bronzong carries the trade (Explosion), Heatran is the legendary, and Metagross is the ace with Agility and Bullet Punch. Today's Steelix, Forretress and Empoleon are out. My first build kept Steelix and Forretress and read 99 won, barely harder than today's, because the box's Water and Ground types walled it; Skarmory and Bronzong are immune to Ground. | `leader_byron.json`; the scorer's reading later. | Accept (recommended), or keep Steelix in Skarmory's place for a softer fight. |
| 2 | Cyrus 1 | Gliscor leads with Stealth Rock and U-turn on Poison Heal. Honchkrow is the trapping member the dial asks of Cyrus: Mean Look, Perish Song and Protect, which is also his one trade. Exploud, Hariyama, Gyarados and a Dragon Dance Salamence ace follow, all from today's six with Vibrava and Shelgon evolved. A second Dragon Dance on Gyarados read about 72 won, so it carries Stone Edge instead. | `galactic_boss_cyrus_celestic_town_ruins.json`; the scorer's reading later. | Accept (recommended). |
| 3 | Ace Trainers read harsh blind | Built to the dial's numbers for this split: six members, top IVs, an item on every member, one level under the cap. With a planned six they read 93 to 100 won, like Wake's and Maylene's. Met blind they win 22 to 51 percent of fights in my simulator, where Krystal reads 64. Alyssa is the one required single. | My readings now; the scorer's planned reading after the TM pass; Ian's alpha run. | Keep (recommended, since Ian asked that fights not be tuned to a box without TMs), or trim Alyssa and the gym pair to five. |
| 4 | Iron Island tag | Jonah (Ground) and Brenda (Fighting and Psychic) bring four each at 50 to 51, beside Riley. | The scorer cannot read tag battles yet. | Nothing now. |
| 5 | Ordinary trainers past the band | They win 93 to 100 percent blind, a step harder than Maylene's, and cost about 0.69 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25. | The scorer's step 15 reading. | Accept for now (recommended: Ian asked for dangerous ordinary trainers, and the scorer's numbers decide), or soften now by dropping items below "most members" or cutting members. |
| 6 | Shedinja on Ninja Boy Brennan | Brennan's Wonder Guard Shedinja is touched only by super-effective hits (Fire, Flying, Rock, Ghost, Dark), beside its Speed Boost Ninjask. He is optional; he reads 97 won blind with no stalled fights. | `ninja_boy_brennan.json`. | Accept (recommended), or replace Shedinja. |
| 7 | Rain on Route 220 | Swimmer Vincent is the route's one weather team. His Pelipper's Drizzle lasts the whole fight, so Lanturn's Thunder never misses and Kabutops swims at double speed. He reads 93 won, the split's lowest, and is optional. | `swimmer_vincent.json`. | Accept (recommended), or take Swift Swim off Kabutops. |

## What comes next

The ordinary trainers of the later splits, as task 4 goes on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Veteran Grant | Oreburgh Gate B1F | optional | single | 4 | 48 to 51 | Old warhorses | 98 / 1.76 / 13 blind in my simulator, about 65 clean in the scorer's terms |
| Fisherman Miguel | Route 218 | optional | single | 4 | 48 to 51 | Water that hits back | 93 / 1.24 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Fisherman Luc | Route 218 | optional | single | 4 | 48 to 51 | Sniper | 96 / 1.34 / 34 blind in my simulator, about 73 clean in the scorer's terms |
| Guitarist Tony | Route 218 | optional | single | 4 | 49 to 51 | Sound | 99 / 1.00 / 37 blind in my simulator, about 75 clean in the scorer's terms |
| Sailor Skyler | Route 218 | optional | single | 4 | 49 to 51 | Belly Drum | 99 / 1.10 / 28 blind in my simulator, about 71 clean in the scorer's terms |
| Black Belt Sean | Route 211 east | optional | single | 4 | 48 to 51 | Kicks and punches | 96 / 0.98 / 48 blind in my simulator, about 79 clean in the scorer's terms |
| Ninja Boy Nick | Route 211 east | optional | single | 4 | 49 to 51 | Poison that waits | 96 / 1.48 / 26 blind in my simulator, about 70 clean in the scorer's terms |
| Bird Keeper Katherine | Route 211 east | optional | single | 4 | 48 to 51 | Birds | 95 / 0.97 / 55 blind in my simulator, about 82 clean in the scorer's terms |
| Ruin Maniac Harry | Route 211 east | optional | single | 4 | 48 to 51 | Fossils | 96 / 1.60 / 19 blind in my simulator, about 68 clean in the scorer's terms |
| Hiker Alexander | Route 208 | optional | single | 4 | 48 to 51 | Rock and Ground | 96 / 1.13 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| Ace Trainer Ernest | Route 210 north | optional | single, Ace Trainer | 6 | 50 to 52 | Steel and Electric | about 100 / 1.1 / 34 with a planned six |
| Ace Trainer Alyssa | Route 210 north | on the path | single, Ace Trainer | 6 | 50 to 52 | Normal types with tricks | about 100 / 2.2 / 1 with a planned six |
| Veteran Brian | Route 210 north (fog) | on the path | single | 5 | 48 to 51 | Screens alone | 95 / 1.30 / 33 blind in my simulator, about 73 clean in the scorer's terms |
| Black Belt Adam | Route 210 north (fog) | optional | single | 4 | 48 to 51 | Fighters with tricks | 95 / 1.51 / 26 blind in my simulator, about 70 clean in the scorer's terms |
| Ninja Boy Joel | Route 210 north (fog) | optional | single | 4 | 49 to 51 | Bugs with blades | 98 / 1.10 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Ninja Boy Nathan | Route 210 north (fog) | optional | single | 4 | 49 to 51 | Sticky Web and Quiver Dance | 96 / 0.81 / 60 blind in my simulator, about 84 clean in the scorer's terms |
| Ninja Boy Davido | Route 210 north (fog) | optional | single | 4 | 48 to 51 | Fliers | 97 / 1.05 / 42 blind in my simulator, about 77 clean in the scorer's terms |
| Dragon Tamer Patrick | Route 210 north (fog) | optional | single | 4 | 49 to 51 | Dragons | 94 / 1.50 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Bird Keeper Brianna | Route 210 north (fog) | optional | single | 4 | 49 to 51 | Spikes and Whirlwind from Skarmory on a Rocky Helmet | 99 / 0.43 / 70 blind in my simulator, about 88 clean in the scorer's terms |
| Double Team Zac and Jen | Route 210 north (fog) | optional | double | 4 | 50 to 51 | Rain | not readable yet (a double) |
| Ninja Boy Fabian | Route 210 south | optional | single | 4 | 49 to 51 | Dark ambush | 96 / 1.31 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Ninja Boy Brennan | Route 210 south | optional | single | 4 | 49 to 51 | The Nincada pair | 97 / 0.61 / 65 blind in my simulator, about 86 clean in the scorer's terms |
| Ninja Boy Bruce | Route 210 south | optional | single | 4 | 49 to 51 | Poison and steel | 96 / 1.04 / 48 blind in my simulator, about 79 clean in the scorer's terms |
| Galactic Officer Argo | Celestic Town | on the path | single, named officer | 6 | 51 to 53 | Today's five on sharper sets plus a Drapion | about 98 / 2.3 / 1 in my simulator, where today's file reads 100 / 0.3 / 66 |
| Cyrus 1 | Celestic Town ruins | on the path | single, boss | 6 | 51 to 53 | A hazard lead and a trap | about 90 / 2.7 / 0 in my simulator, where today's file reads 100 / 0.3 / 68 |
| Barry 5 | Canalave City bridge | on the path | single, boss | 6 | 51 to 53 | Barry 4's six grown to the cap | about 98 / 2.5 / 1 in my simulator, where today's file reads 100 / 0.0 / 98 |
| Black Belt David | Canalave Gym | gym trainer | single | 4 | 50 to 52 | Byron's Stealth Rock and screens together | 98 / 0.91 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Worker Jackson | Canalave Gym | gym trainer | single | 4 | 49 to 52 | Byron's Stealth Rock and phazing together | 95 / 1.31 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Ace Trainer Cesar | Canalave Gym | gym trainer | single, Ace Trainer | 6 | 50 to 52 | Byron's tools one at a time | about 100 / 0.2 / 87 with a planned six |
| Ace Trainer Breanna | Canalave Gym | gym trainer | single, Ace Trainer | 6 | 50 to 52 | Byron's lead and screens rehearsed | about 100 / 1.3 / 6 with a planned six |
| Worker Gary | Canalave Gym | gym trainer | single | 4 | 48 to 52 | Byron's screens | 94 / 1.25 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Black Belt Ricky | Canalave Gym | gym trainer | single | 4 | 49 to 52 | Byron's setup and phazing together | 94 / 1.26 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Worker Gerardo | Canalave Gym | gym trainer | single | 4 | 50 to 52 | Byron's Spikes and a setup ace together | 95 / 0.95 / 56 blind in my simulator, about 83 clean in the scorer's terms |
| Byron | Canalave Gym | on the path | single, boss | 6 | 51 to 53 | Two hazards | about 89 / 1.9 / 16 in my simulator, where today's file reads 100 / 1.4 / 20 |
| Battle Girl Tyler | Iron Island B2F | optional | tag beside Riley | 3 | 49 to 51 | Paired with Kendal | not readable yet (a tag battle) |
| Camper Lawrence | Iron Island B1F | optional | single | 4 | 49 to 51 | Campfire speed | 98 / 1.41 / 21 blind in my simulator, about 68 clean in the scorer's terms |
| Ace Trainer Jonah | Iron Island B2F | on the path | tag, beside Riley | 4 | 50 to 51 | Ground types | not readable yet |
| Ace Trainer Brenda | Iron Island B2F | on the path | tag, beside Riley | 4 | 50 to 51 | Fighting and Psychic types | not readable yet |
| Black Belt Kendal | Iron Island B2F | optional | tag beside Riley | 2 | 50 to 51 | Paired with Tyler | not readable yet (a tag battle) |
| Hiker Damon | Iron Island B2F | optional | tag beside Riley | 3 | 50 to 51 | Paired with Maurice | not readable yet (a tag battle) |
| Hiker Maurice | Iron Island B2F | optional | tag beside Riley | 2 | 50 to 51 | Paired with Damon | not readable yet (a tag battle) |
| Picnicker Summer | Iron Island B1F | optional | single | 4 | 49 to 51 | Cute and sturdy | 98 / 0.68 / 59 blind in my simulator, about 83 clean in the scorer's terms |
| Worker Noel | Iron Island B2F | optional | single | 4 | 48 to 51 | Steel at work | 95 / 1.16 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Worker Braden | Iron Island B2F | optional | single | 4 | 48 to 51 | Salt Cure | 95 / 1.07 / 47 blind in my simulator, about 79 clean in the scorer's terms |
| Worker Brendon | Iron Island B2F | optional | tag beside Riley | 2 | 50 to 51 | Paired with Quentin | not readable yet (a tag battle) |
| Worker Quentin | Iron Island B2F | optional | tag beside Riley | 2 | 50 to 51 | Paired with Brendon | not readable yet (a tag battle) |
| Galactic Grunt (Iron Island, 1) | Iron Island B2F | optional | tag beside Riley | 3 | 50 to 51 | Paired with the other grunt | not readable yet (a tag battle) |
| Galactic Grunt (Iron Island, 2) | Iron Island B2F | optional | tag beside Riley | 3 | 50 to 51 | Paired with the first grunt | not readable yet (a tag battle) |
| Swimmer Adrian | Route 220 | optional | single | 4 | 49 to 51 | Scald everywhere | 95 / 1.40 / 28 blind in my simulator, about 71 clean in the scorer's terms |
| Swimmer Erik | Route 220 | optional | single | 4 | 49 to 51 | Bulk | 97 / 1.33 / 25 blind in my simulator, about 70 clean in the scorer's terms |
| Swimmer Vincent | Route 220 | optional | single | 4 | 48 to 51 | The route's one rain team | 93 / 1.48 / 28 blind in my simulator, about 71 clean in the scorer's terms |
| Swimmer Jessica | Route 220 | optional | single | 4 | 49 to 51 | Water Spout from a Mirror Herb Wailord (Jessica's reward) | 99 / 1.10 / 32 blind in my simulator, about 73 clean in the scorer's terms |
| Swimmer Erica | Route 220 | optional | single | 4 | 49 to 51 | Simple | 98 / 0.92 / 51 blind in my simulator, about 80 clean in the scorer's terms |
| Swimmer Katelyn | Route 220 | optional | single | 4 | 48 to 51 | Politoed's Hypnosis and Scald | 97 / 1.16 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Swimmer Claire | Route 220 | optional | single | 4 | 49 to 51 | Spikes from Omastar | 98 / 0.85 / 54 blind in my simulator, about 82 clean in the scorer's terms |
| Swimmer Dillon | Route 221 | optional | single | 4 | 49 to 51 | Vaporeon's Scald | 97 / 1.10 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Swimmer Vanessa | Route 221 | optional | single | 4 | 49 to 51 | Healers | 100 / 0.50 / 58 blind in my simulator, about 83 clean in the scorer's terms |
| Fisherman Cory | Route 221 | optional | single | 4 | 49 to 51 | Dragons from the deep | 97 / 1.16 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Ace Trainer Jake | Route 221 | optional | single, Ace Trainer | 6 | 50 to 52 | Ghosts and blades | about 94 / 1.8 / 5 with a planned six |
| Ace Trainer Shannon | Route 221 | optional | single, Ace Trainer | 6 | 50 to 52 | Sun | about 93 / 1.7 / 10 with a planned six |
| Collector Ivan | Route 221 | optional | single | 4 | 48 to 51 | Rare finds | 96 / 1.12 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Worker Dillan | Fuego Ironworks | optional | single | 4 | 48 to 51 | Kaizo's ironworks team scaled from level 90 | 96 / 1.42 / 26 blind in my simulator, about 70 clean in the scorer's terms |
| Worker Holden | Fuego Ironworks | optional | single | 4 | 48 to 51 | Kaizo's fire squad scaled | 97 / 1.63 / 21 blind in my simulator, about 68 clean in the scorer's terms |
| Worker Conrad | Fuego Ironworks | optional | single | 4 | 48 to 51 | Kaizo's double scaled to a single | 98 / 0.82 / 48 blind in my simulator, about 79 clean in the scorer's terms |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Veteran Grant: Oreburgh Gate B1F, optional, single, cap 53

Old warhorses: Spiritomb burns, then Hex hits the burn, with Memento to hand the field to the next member; Mightyena's Throat Chop, Dusknoir and Lucario follow. Kaizo's Veteran is a level-99 joke; this keeps its sacrifice idea.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mightyena | 49 | Sitrus Berry | Intimidate | default | Throat Chop, Sucker Punch, Play Rough, Taunt |
| Dusknoir | 48 | Leftovers | Levitate | default | Shadow Punch, Ice Punch, Earthquake, Pain Split |
| Lucario | 49 | Sitrus Berry | Iron Fist | default | Close Combat, Meteor Mash, Crunch, Stone Edge |
| Spiritomb | 51 | Leftovers | Pressure | default | Will-O-Wisp, Hex, Foul Play, Memento |

Today's team: Lucario 45 (Force Palm, Quick Attack, Counter, Screech), Exploud 45 (Bite, Fire Fang, Thunder Fang, Ice Fang), Golem 45 (Earthquake, Rock Slide, Rock Polish, Defense Curl). Expected: 98 / 1.76 / 13 blind in my simulator, about 65 clean in the scorer's terms.

### Fisherman Miguel: Route 218, optional, single, cap 53

Water that hits back: Lanturn's Volt Absorb and Discharge, an Analytic Starmie with Dazzling Gleam, Quagsire's Yawn and Whiscash.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lanturn | 51 | Leftovers | Volt Absorb | default | Discharge, Surf, Ice Beam, Thunder Wave |
| Starmie | 50 | Leftovers | Analytic | default | Surf, Thunderbolt, Dazzling Gleam, Recover |
| Quagsire | 48 | Leftovers | Unaware | default | Earthquake, Waterfall, Yawn, Toxic |
| Whiscash | 48 | Sitrus Berry | Hydration | default | Earthquake, Aqua Tail, Zen Headbutt, Stone Edge |

Today's team: Starmie 44 (Surf, Recover, Psychic, Confuse Ray), Lanturn 44 (Thunderbolt, Surf, Signal Beam, Discharge). Expected: 93 / 1.24 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Fisherman Luc: Route 218, optional, single, cap 53

Sniper: Kingdra's critical hits score triple, beside Seaking's Throat Chop and Kingler's Sheer Force Crabhammer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Whiscash | 49 | Leftovers | Hydration | default | Earthquake, Aqua Tail, Zen Headbutt, Stone Edge |
| Seaking | 51 | Mystic Water | Lightning Rod | default | Waterfall, Megahorn, Throat Chop, Aqua Jet |
| Kingler | 48 | Sitrus Berry | Sheer Force | default | Crabhammer, Knock Off, StompingTantrum, X-Scissor |
| Kingdra | 49 | none | Sniper | default | Octazooka, Dragon Pulse, Ice Beam, Flash Cannon |

Today's team: Octillery 45 (Waterfall, Seed Bomb, Gunk Shot, Thunder Wave). Expected: 96 / 1.34 / 34 blind in my simulator, about 73 clean in the scorer's terms.

### Guitarist Tony: Route 218, optional, single, cap 53

Sound: a Silk Scarf Exploud's Scrappy Hyper Voice, Primarina's Liquid Voice and Sparkling Aria, Kricketune's Throat Chop and Sing, Chatot's Chatter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chatot | 49 | Sharp Beak | Scrappy | default | Chatter, Hyper Voice, Heat Wave, U-turn |
| Kricketune | 50 | SilverPowder | Technician | default | X-Scissor, Throat Chop, Bug Bite, Sing |
| Primarina | 50 | none | Liquid Voice | default | Sparkling Aria, Hyper Voice, Dazzling Gleam, Icy Wind |
| Exploud | 51 | Silk Scarf | Scrappy | default | Hyper Voice, Flamethrower, Ice Beam, Crunch |

Today's team: Kricketune 44 (X-Scissor, Screech, Taunt, Night Slash), Exploud 44 (Fire Fang, Thunder Fang, Ice Fang, Crunch). Expected: 99 / 1.00 / 37 blind in my simulator, about 75 clean in the scorer's terms.

### Sailor Skyler: Route 218, optional, single, cap 53

Belly Drum: Hariyama drums behind a Sitrus Berry and Bullet Punch, after Tentacruel's Toxic Spikes and Mantine's Scald.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mantine | 49 | Leftovers | Water Absorb | default | Scald, Ice Beam, Roost, Confuse Ray |
| Tentacruel | 50 | Black Sludge | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Knock Off |
| Machamp | 49 | Sitrus Berry | Steadfast | default | Close Combat, Throat Chop, Rock Slide, Ice Punch |
| Hariyama | 51 | Sitrus Berry | Thick Fat | default | Belly Drum, Bullet Punch, Close Combat, Knock Off |

Today's team: Mantine 44 (Surf, Psybeam, Confuse Ray, Signal Beam), Hariyama 44 (Sitrus Berry; Belly Drum, Superpower, Fire Punch, Ice Punch). Expected: 99 / 1.10 / 28 blind in my simulator, about 71 clean in the scorer's terms.

### Black Belt Sean: Route 211 east, optional, single, cap 53

Kicks and punches: Hitmontop's Fake Out and Technician Triple Axel, Poliwrath's Hypnosis, Breloom's Mach Punch and Stun Spore, Toxicroak.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 51 | Leftovers | Technician | default | Fake Out, Triple Axel, Rapid Spin, Sucker Punch |
| Poliwrath | 49 | Sitrus Berry | Water Absorb | default | Waterfall, Drain Punch, Ice Punch, Hypnosis |
| Breloom | 49 | Coba Berry | Technician | default | Mach Punch, Bullet Seed, Stun Spore, Rock Slide |
| Toxicroak | 48 | none | Dry Skin | default | Poison Jab, Drain Punch, Sucker Punch, Ice Punch |

Today's team: Croagunk 31 (default moves), Meditite 31 (default moves), Machoke 31 (default moves). Expected: 96 / 0.98 / 48 blind in my simulator, about 79 clean in the scorer's terms.

### Ninja Boy Nick: Route 211 east, optional, single, cap 53

Poison that waits: Drapion's Toxic Spikes and Poison Fang, then Ariados's Foul Play, Skuntank's Throat Chop and Crobat's Confuse Ray.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 51 | Black Sludge | Hyper Cutter | default | Toxic Spikes, Poison Fang, Crunch, Earthquake |
| Ariados | 49 | Sitrus Berry | Intimidate | default | Poison Jab, Leech Life, Sucker Punch, Foul Play |
| Skuntank | 49 | none | Aftermath | default | Throat Chop, Poison Jab, Sucker Punch, Flamethrower |
| Crobat | 49 | Leftovers | Inner Focus | default | Cross Poison, Brave Bird, U-turn, Confuse Ray |

Today's team: Skorupi 32 (default moves), Croagunk 30 (default moves). Expected: 96 / 1.48 / 26 blind in my simulator, about 70 clean in the scorer's terms.

### Bird Keeper Katherine: Route 211 east, optional, single, cap 53

Birds: a Tinted Lens Noctowl with Moonblast and Hypnosis, Togekiss's Super Luck Air Slash, Staraptor's Brave Bird and Chatot.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Noctowl | 51 | Leftovers | Tinted Lens | default | Air Slash, Moonblast, Hypnosis, Roost |
| Togekiss | 49 | Sitrus Berry | Super Luck | default | Air Slash, Dazzling Gleam, Aura Sphere, Thunder Wave |
| Staraptor | 48 | Sitrus Berry | Reckless | default | Brave Bird, Close Combat, U-turn, Quick Attack |
| Chatot | 48 | Sitrus Berry | Scrappy | default | Chatter, Hyper Voice, Heat Wave, U-turn |

Today's team: Noctowl 34 (default moves). Expected: 95 / 0.97 / 55 blind in my simulator, about 82 clean in the scorer's terms.

### Ruin Maniac Harry: Route 211 east, optional, single, cap 53

Fossils: Bastiodon lays Stealth Rock and phazes with Roar behind a Rocky Helmet, then Aerodactyl's Dual Wingbeat, Armaldo and Bronzong's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bastiodon | 51 | Rocky Helmet | Solid Rock | default | Stealth Rock, Iron Head, Metal Burst, Roar |
| Bronzong | 48 | Sitrus Berry | Levitate | default | Gyro Ball, Psychic Noise, Earthquake, Hypnosis |
| Aerodactyl | 48 | none | Rock Head | default | Stone Edge, Crunch, Ice Fang, Dual Wingbeat |
| Armaldo | 48 | Sitrus Berry | Battle Armor | default | X-Scissor, Rock Slide, Aqua Tail, Knock Off |

Today's team: Bronzor 28 (default moves), Shieldon 30 (default moves), Cranidos 32 (default moves). Expected: 96 / 1.60 / 19 blind in my simulator, about 68 clean in the scorer's terms.

### Hiker Alexander: Route 208, optional, single, cap 53

Rock and Ground: a Poison Heal Gliscor on a Toxic Orb with Lunge, Rhyperior's Breaking Swipe, Probopass's paralysis and Sudowoodo. Kaizo's Spore Smeargle is barred; the idea is mine.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Probopass | 51 | Leftovers | Solid Rock | default | Power Gem, Earth Power, Thunder Wave, Flash Cannon |
| Sudowoodo | 48 | Sitrus Berry | Rock Head | default | Wood Hammer, Rock Slide, Sucker Punch, StompingTantrum |
| Gliscor | 49 | Toxic Orb | Poison Heal | default | Earthquake, U-turn, Knock Off, Lunge |
| Rhyperior | 48 | none | Solid Rock | default | Earthquake, Stone Edge, Hammer Arm, Breaking Swipe |

Today's team: Golem 45 (Rock Blast, Earthquake, Explosion, Double-Edge), Probopass 45 (Thunder Wave, Rock Slide, Sandstorm, Rest). Expected: 96 / 1.13 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### Ace Trainer Ernest: Route 210 north, optional, single, Ace Trainer, cap 53

Steel and Electric: Probopass leads with Stealth Rock and Thunder Wave, then Scizor's Bullet Punch and Swords Dance, Ampharos, an Expert Belt Electivire with Thunder Punch, Ice Punch, Cross Chop and Earthquake, a Life Orb Lucario, and a Magnezone ace with a Shuca Berry.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Probopass | 50 | Leftovers | Solid Rock | Modest | Stealth Rock, Earth Power, Power Gem, Thunder Wave |
| Scizor | 51 | Metal Coat | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Swords Dance |
| Ampharos | 51 | Magnet | Static | Modest | Thunderbolt, Power Gem, Focus Blast, Signal Beam |
| Electivire | 51 | Expert Belt | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |
| Lucario | 51 | Life Orb | Adaptability | Timid | Aura Sphere, Flash Cannon, Dragon Pulse, Vacuum Wave |
| Magnezone | 52 | Shuca Berry | Levitate | Modest | Thunderbolt, Flash Cannon, Tri Attack, Mirror Coat |

Today's team: Scizor 41 (Bullet Punch, Night Slash, Iron Head, X-Scissor), Probopass 41 (Earth Power, Thunder Wave, Flash Cannon, Thunderbolt), Ampharos 41 (ThunderPunch, Fire Punch, Outrage, Thunder Wave). Expected: about 100 / 1.1 / 34 with a planned six; read blind, 23 / 5.2 / 0.

### Ace Trainer Alyssa: Route 210 north, on the path, single, Ace Trainer, cap 53

Normal types with tricks: Ambipom's Fake Out and U-turn, Girafarig's two screens, Kangaskhan's Scrappy Double-Edge, a Flame Orb Guts Ursaring with Facade, Staraptor, and a Torterra ace with Wood Hammer and Stone Edge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 50 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Knock Off |
| Girafarig | 51 | Sitrus Berry | Sap Sipper | Modest | Reflect, Light Screen, Psychic, Thunderbolt |
| Kangaskhan | 51 | Leftovers | Scrappy | Adamant | Double-Edge, Earthquake, Sucker Punch, Crunch |
| Ursaring | 51 | Flame Orb | Guts | Adamant | Facade, Close Combat, Crunch, Earthquake |
| Staraptor | 51 | Sharp Beak | Intimidate | Jolly | Brave Bird, Close Combat, U-turn, Roost |
| Torterra | 52 | Miracle Seed | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Crunch |

Today's team: Ambipom 42 (Fake Out, Fire Punch, Low Kick, Aerial Ace), Girafarig 42 (Headbutt, Zen Headbutt, Sucker Punch, Light Screen), Torterra 42 (Energy Ball, Earth Power, Giga Drain, Leech Seed). Expected: about 100 / 2.2 / 1 with a planned six; read blind, 45 / 5.2 / 0.

### Veteran Brian: Route 210 north (fog), on the path, single, cap 53

Screens alone, as Byron's preview on the path: Claydol sets Reflect and Light Screen, then Slowking's Regenerator, Tangrowth's Sleep Powder, Magcargo's Scorching Sands and Milotic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 49 | Leftovers | Levitate | default | Reflect, Light Screen, Earth Power, Ice Beam |
| Tangrowth | 48 | Sitrus Berry | Regenerator | default | Giga Drain, Knock Off, Sleep Powder, Earthquake |
| Magcargo | 49 | Leftovers | Solid Rock | default | Lava Plume, Scorching Sands, Earth Power, Recover |
| Slowking | 51 | Sitrus Berry | Regenerator | default | Psychic, Surf, Slack Off, Thunder Wave |
| Milotic | 48 | none | Filter | default | Surf, Ice Beam, Recover, Dragon Pulse |

Today's team: Tangrowth 43 (AncientPower, Energy Ball, Focus Blast, Sleep Powder), Magcargo 43 (Lava Plume, AncientPower, Earth Power, Will-O-Wisp), Milotic 43 (Dragon Pulse, Rest, Hydro Pump, Confuse Ray). Expected: 95 / 1.30 / 33 blind in my simulator, about 73 clean in the scorer's terms.

### Black Belt Adam: Route 210 north (fog), optional, single, cap 53

Fighters with tricks: Annihilape's Rage Fist, Mienshao's Regenerator and Triple Axel, Hitmonlee's Fake Out and High Jump Kick, and Gallade.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gallade | 51 | Lum Berry | Justified | default | Psycho Cut, Leaf Blade, Drain Punch, Night Slash |
| Hitmonlee | 48 | Sitrus Berry | Limber | default | Fake Out, Hi Jump Kick, Blaze Kick, Knock Off |
| Annihilape | 48 | Sitrus Berry | Defiant | default | Rage Fist, Close Combat, StompingTantrum, U-turn |
| Mienshao | 49 | none | Regenerator | default | Drain Punch, U-turn, Knock Off, Triple Axel |

Today's team: Primeape 42 (Outrage, Poison Jab, Ice Punch, Close Combat). Expected: 95 / 1.51 / 26 blind in my simulator, about 70 clean in the scorer's terms.

### Ninja Boy Joel: Route 210 north (fog), optional, single, cap 53

Bugs with blades: Butterfree's Compound Eyes Sleep Powder, Leavanny's Throat Chop and Triple Axel, Heracross, and Scizor's Technician Bullet Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Butterfree | 49 | Leftovers | Compound Eyes | default | Sleep Powder, Bug Buzz, Psychic, U-turn |
| Leavanny | 50 | Miracle Seed | Swarm | default | Leaf Blade, X-Scissor, Throat Chop, Triple Axel |
| Heracross | 50 | Sitrus Berry | Guts | default | Close Combat, Pin Missile, Knock Off, Stone Edge |
| Scizor | 51 | Metal Coat | Technician | default | Bullet Punch, X-Scissor, Knock Off, U-turn |

Today's team: Butterfree 39 (Silver Wind, Tailwind, Sleep Powder, Psychic), Drapion 39 (Night Slash, Ice Fang, Fire Fang, Poison Fang). Expected: 98 / 1.10 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Ninja Boy Nathan: Route 210 north (fog), optional, single, cap 53

Sticky Web and Quiver Dance: Galvantula lays the web, then Venomoth's Sleep Powder, Mothim and a Quiver Dance Dustox behind Shield Dust.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Galvantula | 49 | Leftovers | Compound Eyes | default | Sticky Web, Thunder, Bug Buzz, Energy Ball |
| Venomoth | 50 | Black Sludge | Tinted Lens | default | Sludge Bomb, Psychic, Signal Beam, Sleep Powder |
| Mothim | 49 | SilverPowder | Tinted Lens | default | Signal Beam, Air Slash, Psychic, Energy Ball |
| Dustox | 51 | Leftovers | Shield Dust | default | Quiver Dance, Bug Buzz, Sludge Bomb, Roost |

Today's team: Dustox 42 (Light Screen, Sludge Bomb, Giga Drain, Bug Buzz). Expected: 96 / 0.81 / 60 blind in my simulator, about 84 clean in the scorer's terms.

### Ninja Boy Davido: Route 210 north (fog), optional, single, cap 53

Fliers: Yanmega's Psychic Noise behind a Wide Lens, Honchkrow's Sucker Punch, Vespiquen's Dual Wingbeat and Kricketune's Taunt.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Yanmega | 50 | Wide Lens | Speed Boost | default | Signal Beam, Air Cutter, Psychic Noise, U-turn |
| Honchkrow | 48 | Sitrus Berry | Super Luck | default | Sucker Punch, Night Slash, Drill Peck, U-turn |
| Vespiquen | 49 | none | Tinted Lens | default | X-Scissor, Power Gem, Dual Wingbeat, Roost |
| Kricketune | 51 | Leftovers | Technician | default | X-Scissor, Throat Chop, Night Slash, Taunt |

Today's team: Mothim 41 (Signal Beam, Psychic, Energy Ball, Air Slash). Expected: 97 / 1.05 / 42 blind in my simulator, about 77 clean in the scorer's terms.

### Dragon Tamer Patrick: Route 210 north (fog), optional, single, cap 53

Dragons: Gabite's Rough Skin and Scale Shot, Altaria's Dazzling Gleam and Will-O-Wisp, Flygon's Levitate and Dragonair's Thunder Wave.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Altaria | 50 | Leftovers | Cloud Nine | default | Dragon Pulse, Dazzling Gleam, Roost, Will-O-Wisp |
| Flygon | 49 | none | Levitate | default | Dragon Claw, Earthquake, U-turn, Fire Punch |
| Gabite | 49 | none | Rough Skin | default | Scale Shot, Earthquake, Stone Edge, Iron Head |
| Dragonair | 51 | Sitrus Berry | Marvel Scale | default | Dragon Rush, Aqua Tail, Iron Tail, Thunder Wave |

Today's team: Altaria 43 (Outrage, Sky Attack, Earthquake, Dragon Dance). Expected: 94 / 1.50 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Bird Keeper Brianna: Route 210 north (fog), optional, single, cap 53

Spikes and Whirlwind from Skarmory on a Rocky Helmet, then a Guts Swellow on a Toxic Orb, Pidgeot and Tropius.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tropius | 49 | Sitrus Berry | Overgrow | default | Air Slash, Energy Ball, Dragon Pulse, Synthesis |
| Swellow | 49 | Toxic Orb | Guts | default | Facade, Aerial Ace, U-turn, Quick Attack |
| Pidgeot | 50 | Leftovers | Intimidate | default | Air Slash, Heat Wave, U-turn, Roost |
| Skarmory | 51 | Rocky Helmet | Weak Armor | default | Spikes, Brave Bird, Roost, Whirlwind |

Today's team: Pidgeot 42 (Brave Bird, Steel Wing, Roost, Tailwind), Skarmory 42 (Drill Peck, Steel Wing, Rock Tomb, Whirlwind). Expected: 99 / 0.43 / 70 blind in my simulator, about 88 clean in the scorer's terms.

### Double Team Zac and Jen: Route 210 north (fog), optional, double, cap 53

Rain: Raichu's Fake Out and Rain Dance on a Damp Rock, then a Thunder that cannot miss, Lanturn's Discharge beside Raichu's Lightning Rod, Ludicolo's Swift Swim and Gyarados. A double because they stand together; a notch softer until the scorer reads doubles.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Raichu | 50 | Damp Rock | Lightning Rod | default | Fake Out, Rain Dance, Thunder, Encore |
| Gyarados | 51 | Sitrus Berry | Intimidate | default | Waterfall, Ice Fang, Stone Edge, Taunt |
| Ludicolo | 50 | Leftovers | Swift Swim | default | Muddy Water, Scald, Energy Ball, Ice Beam |
| Lanturn | 50 | Sitrus Berry | Volt Absorb | default | Discharge, Surf, Ice Beam, Thunder Wave |

Today's team: Gyarados 42 (Ice Fang, Waterfall, Stone Edge, Outrage), Raichu 42 (Volt Tackle, Rain Dance, Fake Out, Thunder Wave). Expected: not readable yet (a double).

### Ninja Boy Fabian: Route 210 south, optional, single, cap 53

Dark ambush: Shiftry's Fake Out and Foul Play, Weavile's Ice Shard and Triple Axel, a Speed Boost Sharpedo, Absol's Super Luck.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shiftry | 50 | Leftovers | Chlorophyll | default | Fake Out, Leaf Storm, Sucker Punch, Foul Play |
| Weavile | 50 | NeverMeltIce | Inner Focus | default | Night Slash, Ice Shard, Triple Axel, Knock Off |
| Sharpedo | 49 | Mystic Water | Speed Boost | default | Crunch, Waterfall, Ice Fang, Aqua Jet |
| Absol | 51 | Sitrus Berry | Super Luck | default | Sucker Punch, X-Scissor, Play Rough, Superpower |

Today's team: Shiftry 41 (Dark Pulse, Whirlwind, Shadow Ball, Energy Ball). Expected: 96 / 1.31 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Ninja Boy Brennan: Route 210 south, optional, single, cap 53

The Nincada pair: a Speed Boost Ninjask with Swords Dance and a Wonder Guard Shedinja that only super-effective hits touch, with Kricketune and a Guts Heracross.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shedinja | 49 | none | Wonder Guard | default | Shadow Claw, X-Scissor, Shadow Sneak, Will-O-Wisp |
| Kricketune | 50 | SilverPowder | Technician | default | X-Scissor, Throat Chop, Night Slash, Taunt |
| Heracross | 50 | Flame Orb | Guts | default | Close Combat, Facade, Pin Missile, Knock Off |
| Ninjask | 51 | Leftovers | Speed Boost | default | X-Scissor, Aerial Ace, Night Slash, Swords Dance |

Today's team: Ninjask 41 (Night Slash, Swords Dance, Slash, X-Scissor). Expected: 97 / 0.61 / 65 blind in my simulator, about 86 clean in the scorer's terms.

### Ninja Boy Bruce: Route 210 south, optional, single, cap 53

Poison and steel: a Focus Sash Beedrill, Scizor's Dual Wingbeat, Galvantula's Thunder and Ariados.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ariados | 49 | Sitrus Berry | Sniper | default | Poison Jab, Leech Life, Sucker Punch, Shadow Sneak |
| Galvantula | 50 | Magnet | Compound Eyes | default | Thunder, Bug Buzz, Energy Ball, Sucker Punch |
| Scizor | 49 | Leftovers | Technician | default | Bullet Punch, X-Scissor, Knock Off, Dual Wingbeat |
| Beedrill | 51 | Focus Sash | Swarm | default | Poison Jab, X-Scissor, U-turn, Knock Off |

Today's team: Beedrill 41 (Brick Break, Knock Off, Poison Jab, X-Scissor). Expected: 96 / 1.04 / 48 blind in my simulator, about 79 clean in the scorer's terms.

### Galactic Officer Argo: Celestic Town, on the path, single, named officer, cap 53

Today's five on sharper sets plus a Drapion: Protean Kecleon with Thunder Wave, Houndoom's Nasty Plot and Sucker Punch, Rotom's Will-O-Wisp, a Focus Sash Dugtrio whose Arena Trap is the fight's one trade, and an Armaldo ace with Rock Polish and a Salac Berry.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kecleon | 51 | Lum Berry | Protean | Adamant | Shadow Claw, Drain Punch, Knock Off, Thunder Wave |
| Drapion | 51 | Black Sludge | Hyper Cutter | Jolly | Crunch, Poison Jab, Earthquake, Ice Fang |
| Houndoom | 51 | Dread Plate | Flash Fire | Timid | Flamethrower, Dark Pulse, Sucker Punch, Nasty Plot |
| Rotom | 52 | Sitrus Berry | Levitate | Modest | Thunderbolt, Shadow Ball, Will-O-Wisp, Dark Pulse |
| Dugtrio | 51 | Focus Sash | Arena Trap | Jolly | Earthquake, Stone Edge, Sucker Punch, Aerial Ace |
| Armaldo | 53 | Salac Berry | Swift Swim | Adamant | X-Scissor, Stone Edge, Earthquake, Rock Polish |

Today's team: Kecleon 42 (Lum Berry; Focus Punch, Recover, Thunder Wave, Shadow Claw), Houndoom 43 (Focus Band; Thunder Fang, Sucker Punch, Fire Fang, Iron Tail), Armaldo 43 (Salac Berry; Rock Polish, X-Scissor, Cross Poison, Stone Edge), Dugtrio 42 (Focus Sash; Earthquake, Rock Slide, Pursuit, Magnitude), Rotom 43 (Wise Glasses; Will-O-Wisp, Leaf Storm, Discharge, Ominous Wind). Expected: about 98 / 2.3 / 1 in my simulator, where today's file reads 100 / 0.3 / 66.

### Cyrus 1: Celestic Town ruins, on the path, single, boss, cap 53

A hazard lead and a trap, as the dial asks of Cyrus: Gliscor sets Stealth Rock and pivots out, Honchkrow traps with Mean Look and sings Perish Song behind Protect, then Exploud, a Flame Orb Hariyama, Gyarados and a Dragon Dance Salamence at the cap.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gliscor | 51 | Toxic Orb | Poison Heal | Jolly | Stealth Rock, Earthquake, U-turn, Ice Fang |
| Honchkrow | 51 | Leftovers | Moxie | Adamant | Mean Look, Perish Song, Protect, Sucker Punch |
| Exploud | 51 | Silk Scarf | Scrappy | Modest | Hyper Voice, Fire Blast, Ice Beam, Focus Blast |
| Hariyama | 51 | Flame Orb | Guts | Adamant | Close Combat, Knock Off, Ice Punch, Bullet Punch |
| Gyarados | 52 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Salamence | 53 | Yache Berry | Intimidate | Adamant | Dragon Dance, Dragon Claw, Earthquake, Fire Fang |

Today's team: Vibrava 45 (Shell Bell; DragonBreath, Earth Power, Tailwind, U-turn), Exploud 45 (Expert Belt; Brick Break, Ice Beam, Earthquake, Uproar), Hariyama 45 (Leftovers; Counter, Revenge, Whirlwind, Fire Punch), Shelgon 45 (King’s Rock; Dragon Claw, Rock Slide, Zen Headbutt, Body Slam), Honchkrow 45 (Sitrus Berry; Drill Peck, Sucker Punch, Confuse Ray, Whirlwind), Gyarados 45 (Life Orb; Aqua Tail, Ice Fang, Earthquake, Bite). Expected: about 90 / 2.7 / 0 in my simulator, where today's file reads 100 / 0.3 / 68.

### Barry 5: Canalave City bridge, on the path, single, boss, cap 53

Barry 4's six grown to the cap: the Ambipom Fake Out lead, Staraptor, Heracross, Floatzel, Snorlax with Curse, and his starter at 53 with a Life Orb (Torterra, Infernape or Empoleon by the player's choice).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 51 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 52 | Sharp Beak | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Heracross | 52 | Lum Berry | Guts | Jolly | Close Combat, Night Slash, Stone Edge, Earthquake |
| Floatzel | 52 | Mystic Water | Swift Swim | Adamant | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 52 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Curse, Ice Punch |
| Torterra | 53 | Life Orb | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Crunch |

Today's team: Staraptor 48 (White Herb; Aerial Ace, Double-Edge, Close Combat, Roost), Starmie 48 (Sea Incense; Surf, Psychic, Brine, Recover), Snorlax 48 (Leftovers; Body Slam, Brick Break, Rest, Sleep Talk), Ninetales 48 (Choice Specs; Heat Wave, Energy Ball, Extrasensory, Dark Pulse), Torterra 49 (Sitrus Berry; Earthquake, Crunch, Wood Hammer, Leech Seed). Expected: about 98 / 2.5 / 1 in my simulator, where today's file reads 100 / 0.0 / 98.

### Black Belt David: Canalave Gym, gym trainer, single, cap 53

Byron's Stealth Rock and screens together: Dunsparce lays the rocks and Glares, Ampharos sets Light Screen, then a Guts Hariyama with Fake Out and a Prankster Sableye. Kaizo's Hiker David, who stands in this gym.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hariyama | 50 | Flame Orb | Guts | default | Fake Out, Bullet Punch, Force Palm, Knock Off |
| Sableye | 51 | Leftovers | Prankster | default | Will-O-Wisp, Recover, Foul Play, Knock Off |
| Ampharos | 50 | none | Static | default | Thunderbolt, Dazzling Gleam, Light Screen, Thunder Wave |
| Dunsparce | 52 | Leftovers | Serene Grace | default | Stealth Rock, Glare, Roost, Earthquake |

Today's team: Lucario 51 (Flash Cannon, Aura Sphere, Dark Pulse, Psychic). Expected: 98 / 0.91 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Worker Jackson: Canalave Gym, gym trainer, single, cap 53

Byron's Stealth Rock and phazing together: Flygon's rocks, Skarmory's Whirlwind, then Aggron and a Poison Heal Gliscor. Kaizo's Idol Skylar from this gym.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Flygon | 50 | Leftovers | Levitate | default | Stealth Rock, Earthquake, Dragon Claw, U-turn |
| Gliscor | 49 | Toxic Orb | Poison Heal | default | Earthquake, Knock Off, U-turn, Lunge |
| Aggron | 50 | Sitrus Berry | Rock Head | default | Double-Edge, Iron Head, Earthquake, Stone Edge |
| Skarmory | 52 | none | Filter | default | Brave Bird, Roost, Whirlwind, Iron Defense |

Today's team: Wormadam 49 (Gyro Ball, Bug Bite, Sucker Punch, Stealth Rock), Magneton 49 (Flash Cannon, Thunderbolt, Thunder Wave, Tri Attack). Expected: 95 / 1.31 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Ace Trainer Cesar: Canalave Gym, gym trainer, single, Ace Trainer, cap 53

Byron's tools one at a time: Skarmory's Spikes and Whirlwind, Ferrothorn, a Rock Head Aggron, Mawile, a Lucario with ExtremeSpeed, and a Scizor ace with Bullet Punch, Swords Dance and an Occa Berry.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 50 | Leftovers | Filter | Impish | Spikes, Brave Bird, Roost, Whirlwind |
| Ferrothorn | 51 | Leftovers | Iron Barbs | Relaxed | Iron Head, Seed Bomb, Knock Off, Thunder Wave |
| Aggron | 51 | Hard Stone | Rock Head | Adamant | Double-Edge, Iron Head, Earthquake, Stone Edge |
| Mawile | 51 | Sitrus Berry | Intimidate | Adamant | Iron Head, Crunch, Fire Fang, Ice Fang |
| Lucario | 51 | Black Belt | Iron Fist | Adamant | Close Combat, ExtremeSpeed, Crunch, Stone Edge |
| Scizor | 52 | Occa Berry | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Swords Dance |

Today's team: Scizor 51 (Metal Claw, X-Scissor, Slash, Pursuit). Expected: about 100 / 0.2 / 87 with a planned six; read blind, 23 / 5.1 / 5.

### Ace Trainer Breanna: Canalave Gym, gym trainer, single, Ace Trainer, cap 53

Byron's lead and screens rehearsed: Probopass sets Stealth Rock behind a Focus Sash, Bronzong sets both screens (without Light Clay), then Skarmory, Empoleon, Steelix and a Corviknight ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Probopass | 50 | Focus Sash | Solid Rock | Modest | Stealth Rock, Power Gem, Earth Power, Thunder Wave |
| Bronzong | 51 | Leftovers | Levitate | Relaxed | Reflect, Light Screen, Gyro Ball, Earthquake |
| Skarmory | 51 | Sharp Beak | Filter | Adamant | Brave Bird, Steel Wing, Roost, Swords Dance |
| Empoleon | 51 | Mystic Water | Torrent | Modest | Surf, Ice Beam, Flash Cannon, Grass Knot |
| Steelix | 51 | Passho Berry | Solid Rock | Adamant | Iron Head, Earthquake, Stone Edge, Crunch |
| Corviknight | 52 | Leftovers | Mirror Armor | Impish | Brave Bird, Iron Head, Revenge, Roost |

Today's team: Skarmory 50 (Steel Wing, Drill Peck, Stealth Rock, Roost), Probopass 50 (Thunderbolt, Hidden Power, Power Gem, Thunder Wave), Bronzong 50 (Gyro Ball, Zen Headbutt, Confuse Ray, Iron Defense). Expected: about 100 / 1.3 / 6 with a planned six; read blind, 51 / 4.6 / 0.

### Worker Gary: Canalave Gym, gym trainer, single, cap 53

Byron's screens: Electrode's Light Screen and Bronzong's Reflect around Rampardos's Head Smash and an Eviolite Porygon2. Kaizo's Scientist Bill from this gym.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electrode | 52 | Leftovers | Static | default | Light Screen, Thunderbolt, Foul Play, Thunder Wave |
| Rampardos | 48 | none | Rock Head | default | Head Smash, Zen Headbutt, Earthquake, Crunch |
| Porygon2 | 50 | Eviolite | Download | default | Ice Beam, Thunderbolt, Psychic, Recover |
| Bronzong | 50 | none | Levitate | default | Reflect, Flash Cannon, Earthquake, Psychic Noise |

Today's team: Magneton 51 (Thunderbolt, Tri Attack, Flash Cannon). Expected: 94 / 1.25 / 36 blind in my simulator, about 74 clean in the scorer's terms.

### Black Belt Ricky: Canalave Gym, gym trainer, single, cap 53

Byron's setup and phazing together: Steelix's Curse and Roar, then Hitmonchan's Bullet Punch, Lucario's Meteor Mash and Toxicroak's Foul Play.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Toxicroak | 50 | Black Sludge | Dry Skin | default | Poison Jab, Drain Punch, Sucker Punch, Foul Play |
| Lucario | 49 | Sitrus Berry | Iron Fist | default | Close Combat, Meteor Mash, Crunch, Stone Edge |
| Steelix | 49 | none | Rock Head | default | Curse, Iron Head, Earthquake, Roar |
| Hitmonchan | 52 | none | Keen Eye | default | Drain Punch, Ice Punch, ThunderPunch, Bullet Punch |

Today's team: Steelix 51 (Iron Head, Stone Edge, Fire Fang, Thunder Fang). Expected: 94 / 1.26 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Worker Gerardo: Canalave Gym, gym trainer, single, cap 53

Byron's Spikes and a setup ace together: Forretress lays Spikes on a Rocky Helmet, Mawile has Swords Dance, with Magneton and Probopass's Dazzling Gleam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Forretress | 50 | Rocky Helmet | Heatproof | default | Spikes, Gyro Ball, Rapid Spin, Rock Slide |
| Magneton | 50 | Magnet | Analytic | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Mawile | 50 | none | Intimidate | default | Play Rough, Iron Head, Sucker Punch, Swords Dance |
| Probopass | 52 | Sitrus Berry | Solid Rock | default | Power Gem, Earth Power, Flash Cannon, Dazzling Gleam |

Today's team: Forretress 49 (Selfdestruct, Stealth Rock, Gyro Ball, Toxic Spikes), Mawile 49 (Thunder Fang, Brick Break, Fire Fang, Iron Head). Expected: 95 / 0.95 / 56 blind in my simulator, about 83 clean in the scorer's terms.

### Byron: Canalave Gym, on the path, single, boss, cap 53

Two hazards, screens and a legendary: Bastiodon's Stealth Rock and Roar behind a Focus Sash, Skarmory's Spikes and Whirlwind, Magnezone's screens on a Light Clay, Bronzong's Explosion, Heatran, and a Metagross ace with Agility and Bullet Punch. Every member is a Steel type.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bastiodon | 51 | Focus Sash | Solid Rock | Impish | Stealth Rock, Roar, Stone Edge, Iron Head |
| Skarmory | 51 | Leftovers | Filter | Impish | Spikes, Brave Bird, Roost, Whirlwind |
| Magnezone | 51 | Light Clay | Levitate | Modest | Reflect, Light Screen, Thunderbolt, Flash Cannon |
| Bronzong | 51 | Sitrus Berry | Levitate | Relaxed | Gyro Ball, Earthquake, Explosion, Psychic |
| Heatran | 52 | Shuca Berry | Flash Fire | Modest | Flamethrower, Earth Power, Flash Cannon, Will-O-Wisp |
| Metagross | 53 | Occa Berry | Clear Body | Adamant | Meteor Mash, Earthquake, Bullet Punch, Agility |

Today's team: Forretress 52 (Sitrus Berry; Bug Bite, Toxic Spikes, Explosion, Earthquake), Steelix 52 (Passho Berry; Iron Head, Ice Fang, Earthquake, Sandstorm), Magnezone 52 (Focus Sash; Mirror Coat, Thunderbolt, Flash Cannon, Reflect), Metagross 52 (Shuca Berry; Zen Headbutt, Agility, Meteor Mash, Hammer Arm), Empoleon 52 (Chople Berry; Aqua Tail, Iron Head, Drill Peck, Earthquake), Bastiodon 53 (Leftovers; Metal Burst, Stone Edge, Iron Head, Avalanche). Expected: about 89 / 1.9 / 16 in my simulator, where today's file reads 100 / 1.4 / 20.

### Battle Girl Tyler: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Kendal: Lopunny's Fake Out and Triple Axel, Medicham, Breloom's Mach Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lopunny | 50 | Sitrus Berry | Scrappy | default | Fake Out, Jump Kick, Triple Axel, Ice Punch |
| Medicham | 49 | Leftovers | Pure Power | default | Hi Jump Kick, Zen Headbutt, Bullet Punch, Ice Punch |
| Breloom | 51 | Coba Berry | Technician | default | Mach Punch, Bullet Seed, Rock Slide, Stun Spore |

Today's team: Breloom 48 (Sky Uppercut, ThunderPunch, Seed Bomb, Spore). Expected: not readable yet (a tag battle).

### Camper Lawrence: Iron Island B1F, optional, single, cap 53

Campfire speed: Arcanine's Extreme Speed and Wild Charge, Ambipom's Fake Out, Floatzel's Low Sweep, Ninetales' Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ninetales | 49 | Leftovers | Magic Guard | default | Flamethrower, Extrasensory, Alluring Voice, Will-O-Wisp |
| Ambipom | 49 | Sitrus Berry | Technician | default | Fake Out, Double Hit, Knock Off, U-turn |
| Floatzel | 50 | Mystic Water | Swift Swim | default | Waterfall, Ice Fang, Crunch, Low Sweep |
| Arcanine | 51 | none | Intimidate | default | Flare Blitz, ExtremeSpeed, Wild Charge, Crunch |

Today's team: Ambipom 46 (Fake Out, Headbutt, Low Kick, Fire Punch), Floatzel 46 (Aqua Jet, Crunch, Ice Punch, Low Kick). Expected: 98 / 1.41 / 21 blind in my simulator, about 68 clean in the scorer's terms.

### Ace Trainer Jonah: Iron Island B2F, on the path, tag, beside Riley, cap 53

Ground types: Hippowdon's sand, Quagsire's Yawn, Mamoswine's Ice Shard and Torterra.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hippowdon | 50 | Smooth Rock | Sand Stream | Impish | Earthquake, Crunch, Ice Fang, Slack Off |
| Quagsire | 50 | Leftovers | Unaware | Relaxed | Waterfall, Earthquake, Ice Punch, Yawn |
| Mamoswine | 50 | NeverMeltIce | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Torterra | 51 | Miracle Seed | Thick Fat | Adamant | Wood Hammer, Earthquake, Crunch, Stone Edge |

Today's team: Hippowdon 47 (Earthquake, Thunder Fang, Crunch, Fire Fang), Quagsire 47 (Waterfall, Yawn, Earthquake, Ice Punch), Torterra 47 (Earthquake, Leech Seed, Seed Bomb, Crunch). Expected: not readable yet.

### Ace Trainer Brenda: Iron Island B2F, on the path, tag, beside Riley, cap 53

Fighting and Psychic types: Lopunny's Fake Out, Medicham's Hi Jump Kick, Hitmontop's Helping Hand and a Calm Mind Gardevoir.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lopunny | 50 | Silk Scarf | Scrappy | Jolly | Fake Out, Jump Kick, Dizzy Punch, Ice Punch |
| Medicham | 50 | Black Belt | Pure Power | Adamant | Hi Jump Kick, Zen Headbutt, Bullet Punch, Ice Punch |
| Hitmontop | 50 | Leftovers | Steadfast | Adamant | Hi Jump Kick, Sucker Punch, Stone Edge, Helping Hand |
| Gardevoir | 51 | TwistedSpoon | Trace | Modest | Psychic, Focus Blast, Thunderbolt, Calm Mind |

Today's team: Lopunny 47 (Low Kick, Dizzy Punch, Fake Out, Bounce), Gardevoir 47 (Calm Mind, Psychic, Focus Blast, Signal Beam), Medicham 47 (Zen Headbutt, Hi Jump Kick, Fire Punch, Bullet Punch). Expected: not readable yet.

### Black Belt Kendal: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Tyler: an Assault Vest Toxicroak with Fake Out and Foul Play, and Hitmonchan.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmonchan | 50 | Leftovers | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Toxicroak | 51 | Assault Vest | Dry Skin | default | Fake Out, Poison Jab, Drain Punch, Foul Play |

Today's team: Toxicroak 48 (Sludge Bomb, Dark Pulse, Mud Bomb, Vacuum Wave). Expected: not readable yet (a tag battle).

### Hiker Damon: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Maurice: Probopass's Stealth Rock on an Air Balloon, Sudowoodo, Aggron.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Probopass | 50 | Air Balloon | Solid Rock | default | Stealth Rock, Power Gem, Earth Power, Thunder Wave |
| Sudowoodo | 50 | Sitrus Berry | Rock Head | default | Wood Hammer, Rock Slide, Sucker Punch, StompingTantrum |
| Aggron | 51 | Hard Stone | Rock Head | default | Double-Edge, Iron Head, Earthquake, Stone Edge |

Today's team: Probopass 46 (Thunder Wave, Flash Cannon, Sandstorm, AncientPower), Aggron 46 (Earthquake, Iron Head, Fire Punch, Ice Punch), Sudowoodo 46 (Wood Hammer, Low Kick, Rock Slide, ThunderPunch). Expected: not readable yet (a tag battle).

### Hiker Maurice: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Damon: Golem and Rhyperior's Earthquakes.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golem | 50 | Soft Sand | Shell Armor | default | Earthquake, Stone Edge, Sucker Punch, Rock Slide |
| Rhyperior | 51 | Sitrus Berry | Solid Rock | default | Earthquake, Stone Edge, Hammer Arm, Breaking Swipe |

Today's team: Graveler 35 (default moves), Rhyhorn 35 (default moves). Expected: not readable yet (a tag battle).

### Picnicker Summer: Iron Island B1F, optional, single, cap 53

Cute and sturdy: Raichu's Surf and Focus Blast, an Unaware Clefable with Moonblast, Lopunny's Fake Out, Sudowoodo.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sudowoodo | 49 | Leftovers | Rock Head | default | Wood Hammer, Rock Slide, Sucker Punch, Hammer Arm |
| Lopunny | 50 | Sitrus Berry | Scrappy | default | Fake Out, Return, Jump Kick, Ice Punch |
| Clefable | 50 | Leftovers | Unaware | default | Moonblast, Flamethrower, Moonlight, Thunder Wave |
| Raichu | 51 | Sitrus Berry | Lightning Rod | default | Thunderbolt, Surf, Focus Blast, Encore |

Today's team: Raichu 46 (Thunder Wave, Grass Knot, Signal Beam, Thunderbolt). Expected: 98 / 0.68 / 59 blind in my simulator, about 83 clean in the scorer's terms.

### Worker Noel: Iron Island B2F, optional, single, cap 53

Steel at work: an Analytic Magneton on an Air Balloon, a Sheer Force Mawile, Aggron and Bronzong's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 49 | Leftovers | Levitate | default | Gyro Ball, Earthquake, Hypnosis, Psychic Noise |
| Magneton | 51 | Air Balloon | Analytic | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Mawile | 49 | Sitrus Berry | Sheer Force | default | Play Rough, Iron Head, Crunch, Fire Fang |
| Aggron | 48 | Leftovers | Rock Head | default | Double-Edge, Iron Head, Earthquake, Stone Edge |

Today's team: Magneton 46 (Magnet Bomb, Screech, Discharge, Mirror Shot), Mawile 46 (Iron Head, Crunch, ThunderPunch, Sucker Punch). Expected: 95 / 1.16 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Worker Braden: Iron Island B2F, optional, single, cap 53

Salt Cure: Garganacl's lingering chip behind a Covert Cloak, then Golem, Rhyperior and Steelix.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Garganacl | 51 | Covert Cloak | Purifying Salt | default | Salt Cure, Stone Edge, Earthquake, Recover |
| Golem | 50 | Soft Sand | Shell Armor | default | Earthquake, Stone Edge, Sucker Punch, Fire Punch |
| Rhyperior | 48 | Sitrus Berry | Solid Rock | default | Earthquake, Stone Edge, Hammer Arm, Breaking Swipe |
| Steelix | 48 | none | Rock Head | default | Iron Head, Crunch, Fire Fang, Earthquake |

Today's team: Steelix 48 (Earthquake, Curse, Iron Tail, Crunch). Expected: 95 / 1.07 / 47 blind in my simulator, about 79 clean in the scorer's terms.

### Worker Brendon: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Quentin: Granbull's Play Rough and Steelix's Curse.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Granbull | 50 | Sitrus Berry | Intimidate | default | Play Rough, Crunch, Earthquake, Close Combat |
| Steelix | 51 | Leftovers | Rock Head | default | Iron Head, Earthquake, Curse, Crunch |

Today's team: Granbull 48 (Headbutt, Ice Fang, Fire Fang, Thunder Fang), Golem 48 (Rock Blast, Earthquake, Explosion, Double-Edge). Expected: not readable yet (a tag battle).

### Worker Quentin: Iron Island B2F, optional, tag beside Riley, cap 53

Paired with Brendon: a Guts Ursaring on a Flame Orb and Rhydon's Breaking Swipe.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Rhydon | 50 | Sitrus Berry | Rock Head | default | Earthquake, Rock Slide, Hammer Arm, Breaking Swipe |
| Ursaring | 51 | Flame Orb | Guts | default | Facade, Close Combat, Crunch, Earthquake |

Today's team: Ursaring 48 (Close Combat, Slash, Shadow Claw, Ice Punch), Rhyperior 48 (Poison Jab, ThunderPunch, Hammer Arm, Stone Edge). Expected: not readable yet (a tag battle).

### Galactic Grunt (Iron Island, 1): Iron Island B2F, optional, tag beside Riley, cap 53

Paired with the other grunt: Kaizo's Levitate trio, Claydol's Stealth Rock, Magneton and Bronzong's Reflect.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 50 | Leftovers | Levitate | default | Earth Power, Psychic, Ice Beam, Stealth Rock |
| Magneton | 50 | Magnet | Analytic | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Bronzong | 51 | Sitrus Berry | Levitate | default | Gyro Ball, Psychic Noise, Earthquake, Reflect |

Today's team: Yanmega 46 (AncientPower, Silver Wind, Giga Drain, Tailwind), Kecleon 46 (Slash, Ice Punch, Substitute, Sucker Punch), Solrock 46 (Earthquake, Stone Edge, Iron Head, Zen Headbutt). Expected: not readable yet (a tag battle).

### Galactic Grunt (Iron Island, 2): Iron Island B2F, optional, tag beside Riley, cap 53

Paired with the first grunt: Kaizo's Ground and Flying trio, a Poison Heal Gliscor, Aerodactyl and Flygon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gliscor | 50 | Toxic Orb | Poison Heal | default | Earthquake, Knock Off, U-turn, Lunge |
| Aerodactyl | 50 | Sharp Beak | Rock Head | default | Stone Edge, Earthquake, Crunch, Dual Wingbeat |
| Flygon | 51 | Soft Sand | Levitate | default | Earthquake, Dragon Claw, U-turn, Fire Punch |

Today's team: Purugly 46 (Fake Out, Slash, Sucker Punch, Shadow Claw), Skuntank 46 (Toxic, Dark Pulse, Flamethrower, Sludge Bomb), Toxicroak 46 (Poison Jab, Sucker Punch, Focus Punch, X-Scissor). Expected: not readable yet (a tag battle).

### Swimmer Adrian: Route 220, optional, single, cap 53

Scald everywhere: Octillery's Gunk Shot steadied by a Zoom Lens (Adrian's reward), Tentacruel, Golduck's Yawn and Sharpedo.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golduck | 49 | Leftovers | Damp | default | Scald, Ice Beam, Psychic, Yawn |
| Sharpedo | 49 | Mystic Water | Speed Boost | default | Crunch, Waterfall, Ice Fang, Aqua Jet |
| Tentacruel | 51 | Black Sludge | Clear Body | default | Scald, Sludge Bomb, Knock Off, Rapid Spin |
| Octillery | 50 | Zoom Lens | Sniper | default | Gunk Shot, Scald, Ice Beam, Signal Beam |

Today's team: Octillery 44 (Octazooka, Ice Beam, Flamethrower, Signal Beam), Tentacruel 44 (Poison Jab, Waterfall, Knock Off, Confuse Ray). Expected: 95 / 1.40 / 28 blind in my simulator, about 71 clean in the scorer's terms.

### Swimmer Erik: Route 220, optional, single, cap 53

Bulk: a Regenerator Slowking with Foul Play, Lapras's Ice Shard, Walrein's Snarl and Encore, Golduck.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golduck | 49 | Sitrus Berry | Damp | default | Scald, Ice Beam, Psychic, Low Sweep |
| Walrein | 50 | Leftovers | Ice Body | default | Ice Beam, Surf, Snarl, Encore |
| Slowking | 51 | Sitrus Berry | Regenerator | default | Surf, Psychic, Slack Off, Foul Play |
| Lapras | 50 | Sitrus Berry | Shell Armor | default | Ice Beam, Surf, Thunderbolt, Ice Shard |

Today's team: Slowking 45 (Surf, Psychic, Nasty Plot, Power Gem). Expected: 97 / 1.33 / 25 blind in my simulator, about 70 clean in the scorer's terms.

### Swimmer Vincent: Route 220, optional, single, cap 53

The route's one rain team: Pelipper's Drizzle lasts the whole fight, so Lanturn's Thunder cannot miss and Kabutops swims at double speed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pelipper | 51 | Leftovers | Drizzle | default | Scald, Air Slash, U-turn, Roost |
| Kabutops | 49 | none | Swift Swim | default | Waterfall, Stone Edge, Aqua Jet, Low Sweep |
| Quagsire | 48 | Leftovers | Water Absorb | default | Earthquake, Waterfall, Yawn, Toxic |
| Lanturn | 48 | none | Volt Absorb | default | Thunder, Surf, Ice Beam, Thunder Wave |

Today's team: Pelipper 44 (Rain Dance, Tailwind, Sky Attack), Kabutops 44 (Stone Edge, Waterfall, Knock Off, Superpower). Expected: 93 / 1.48 / 28 blind in my simulator, about 71 clean in the scorer's terms.

### Swimmer Jessica: Route 220, optional, single, cap 53

Water Spout from a Mirror Herb Wailord (Jessica's reward), Seaking's Megahorn and Throat Chop, Gorebyss and Lumineon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 49 | Leftovers | Water Veil | default | Waterfall, U-turn, Ice Beam, Dazzling Gleam |
| Gorebyss | 49 | Sitrus Berry | Hydration | default | Scald, Psychic, Ice Beam, Shadow Ball |
| Seaking | 51 | Mystic Water | Lightning Rod | default | Waterfall, Megahorn, Throat Chop, Aqua Jet |
| Wailord | 51 | Mirror Herb | Water Veil | default | Water Spout, Surf, Ice Beam, Earthquake |

Today's team: Seaking 44 (Aqua Ring, Fury Attack, Waterfall), Wailord 44 (Rest, Brine, Water Spout, Amnesia). Expected: 99 / 1.10 / 32 blind in my simulator, about 73 clean in the scorer's terms.

### Swimmer Erica: Route 220, optional, single, cap 53

Simple: Bibarel's Curse counts double, beside Dewgong's Drill Run, Seadra and Lumineon's Alluring Voice.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Seadra | 49 | Leftovers | Sniper | default | Octazooka, Dragon Pulse, Ice Beam, Flash Cannon |
| Dewgong | 50 | Sitrus Berry | Thick Fat | default | Ice Beam, Aqua Tail, Drill Run, Encore |
| Lumineon | 49 | Mystic Water | Water Veil | default | Waterfall, U-turn, Ice Beam, Alluring Voice |
| Bibarel | 51 | Sitrus Berry | Simple | default | Curse, Hyper Fang, Waterfall, Aqua Jet |

Today's team: Bibarel 45 (Defense Curl, Rollout, Quick Attack). Expected: 98 / 0.92 / 51 blind in my simulator, about 80 clean in the scorer's terms.

### Swimmer Katelyn: Route 220, optional, single, cap 53

Politoed's Hypnosis and Scald, Ludicolo's Fake Out, a Pure Power Medicham and Whiscash.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Medicham | 48 | Leftovers | Pure Power | default | Hi Jump Kick, Zen Headbutt, Bullet Punch, Ice Punch |
| Whiscash | 49 | Sitrus Berry | Hydration | default | Earthquake, Aqua Tail, Zen Headbutt, Stone Edge |
| Ludicolo | 49 | Leftovers | Own Tempo | default | Fake Out, Scald, Energy Ball, Ice Beam |
| Politoed | 51 | Sitrus Berry | Water Absorb | default | Scald, Hyper Voice, Ice Beam, Hypnosis |

Today's team: Politoed 43 (Rain Dance, Perish Song, Surf), Medicham 43 (ThunderPunch, Hi Jump Kick, Bullet Punch, Psycho Cut), Ludicolo 43 (Seed Bomb, Waterfall, ThunderPunch, Zen Headbutt). Expected: 97 / 1.16 / 36 blind in my simulator, about 74 clean in the scorer's terms.

### Swimmer Claire: Route 220, optional, single, cap 53

Spikes from Omastar, then Cloyster's Icicle Spear and Razor Shell, Kingler's Crabhammer and Lumineon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 49 | Leftovers | Water Veil | default | Waterfall, U-turn, Ice Beam, Dazzling Gleam |
| Kingler | 49 | Sitrus Berry | Hyper Cutter | default | Crabhammer, Knock Off, X-Scissor, StompingTantrum |
| Cloyster | 49 | Sitrus Berry | Shell Armor | default | Icicle Spear, Razor Shell, Drill Run, Rock Blast |
| Omastar | 51 | Leftovers | Swift Swim | default | Spikes, Scald, Ice Beam, Earth Power |

Today's team: Omastar 45 (Brine, Rain Dance, AncientPower, Ice Beam). Expected: 98 / 0.85 / 54 blind in my simulator, about 82 clean in the scorer's terms.

### Swimmer Dillon: Route 221, optional, single, cap 53

Vaporeon's Scald, Wish and Yawn, Tentacruel's Toxic Spikes, Golduck and a Speed Boost Sharpedo with Poison Fang.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sharpedo | 49 | Mystic Water | Speed Boost | default | Crunch, Waterfall, Poison Fang, Aqua Jet |
| Golduck | 50 | Sitrus Berry | Damp | default | Scald, Ice Beam, Psychic, Low Sweep |
| Tentacruel | 50 | Black Sludge | Clear Body | default | Scald, Sludge Bomb, Knock Off, Toxic Spikes |
| Vaporeon | 51 | Leftovers | Water Absorb | default | Scald, Ice Beam, Wish, Yawn |

Today's team: Vaporeon 46 (Surf, Ice Beam, Toxic, Aqua Ring). Expected: 97 / 1.10 / 36 blind in my simulator, about 74 clean in the scorer's terms.

### Swimmer Vanessa: Route 221, optional, single, cap 53

Healers: Milotic's Recover behind a Covert Cloak, Corsola's Regenerator and Aqua Cutter, Starmie, Gorebyss.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gorebyss | 49 | Leftovers | Hydration | default | Scald, Psychic, Ice Beam, Shadow Ball |
| Starmie | 49 | Sitrus Berry | Analytic | default | Surf, Thunderbolt, Dazzling Gleam, Recover |
| Corsola | 50 | Leftovers | Regenerator | default | Aqua Cutter, Power Gem, Recover, Toxic |
| Milotic | 51 | Covert Cloak | Marvel Scale | default | Surf, Ice Beam, Recover, Alluring Voice |

Today's team: Corsola 46 (Ice Beam, Earth Power, Surf, Power Gem). Expected: 100 / 0.50 / 58 blind in my simulator, about 83 clean in the scorer's terms.

### Fisherman Cory: Route 221, optional, single, cap 53

Dragons from the deep: Gyarados holds the Clear Amulet Cory awards, beside Dragonair's Thunder Wave, Seadra and Sharpedo.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Seadra | 49 | Leftovers | Sniper | default | Octazooka, Dragon Pulse, Ice Beam, Flash Cannon |
| Dragonair | 50 | Sitrus Berry | Marvel Scale | default | Dragon Rush, Aqua Tail, Iron Tail, Thunder Wave |
| Sharpedo | 49 | Sitrus Berry | Speed Boost | default | Crunch, Waterfall, Poison Fang, Aqua Jet |
| Gyarados | 51 | Clear Amulet | Intimidate | default | Waterfall, Ice Fang, Earthquake, Stone Edge |

Today's team: Seadra 44 (Dragon Pulse, Twister, Brine, Hydro Pump), Sharpedo 44 (Crunch, Slash, Aqua Jet, Taunt), Dragonair 44 (Dragon Rush, Headbutt, Aqua Tail, Thunder Wave). Expected: 97 / 1.16 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Ace Trainer Jake: Route 221, optional, single, Ace Trainer, cap 53

Ghosts and blades: Dusknoir's Will-O-Wisp, Banette, a Super Luck Absol with a Scope Lens and Swords Dance, Weavile's Ice Shard, a Calm Mind Mismagius and a Gallade ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 50 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Banette | 51 | Spell Tag | Cursed Body | Adamant | Shadow Claw, Sucker Punch, Knock Off, Thunder Wave |
| Absol | 51 | Scope Lens | Super Luck | Adamant | Knock Off, Superpower, Stone Edge, Swords Dance |
| Weavile | 51 | NeverMeltIce | Technician | Jolly | Ice Shard, Night Slash, Ice Punch, Brick Break |
| Mismagius | 51 | Wise Glasses | Levitate | Timid | Shadow Ball, Thunderbolt, Energy Ball, Calm Mind |
| Gallade | 52 | Lum Berry | Justified | Adamant | Psycho Cut, Leaf Blade, Drain Punch, Night Slash |

Today's team: Banette 46 (Night Slash, Shadow Sneak, Sucker Punch, Embargo), Gallade 46 (Psycho Cut, Leaf Blade, Night Slash, Aerial Ace). Expected: about 94 / 1.8 / 5 with a planned six; read blind, 22 / 5.2 / 1.

### Ace Trainer Shannon: Route 221, optional, single, Ace Trainer, cap 53

Sun: Victreebel leads with Sunny Day on a Heat Rock and Sleep Powder, then Cherrim's Flower Gift, Ninetales, Miltank, Lopunny's Fake Out and an Arcanine ace with ExtremeSpeed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Victreebel | 50 | Heat Rock | Chlorophyll | Modest | Sunny Day, SolarBeam, Sludge Bomb, Sleep Powder |
| Cherrim | 51 | Miracle Seed | Flower Gift | Modest | SolarBeam, Energy Ball, Leech Seed, Growth |
| Ninetales | 51 | Charcoal | Magic Guard | Timid | Flamethrower, SolarBeam, Energy Ball, Nasty Plot |
| Miltank | 51 | Leftovers | Thick Fat | Impish | Body Slam, Earthquake, Milk Drink, Ice Punch |
| Lopunny | 51 | Lum Berry | Scrappy | Jolly | Jump Kick, Dizzy Punch, Ice Punch, Fake Out |
| Arcanine | 52 | Sitrus Berry | Intimidate | Adamant | Flare Blitz, ExtremeSpeed, Crunch, Thunder Fang |

Today's team: Cherrim 45 (Energy Ball, Weather Ball, Leech Seed, Sunny Day), Miltank 45 (Hammer Arm, Fire Punch, Headbutt, Milk Drink), Lopunny 45 (Jump Kick, Quick Attack, Fire Punch, Dizzy Punch). Expected: about 93 / 1.7 / 10 with a planned six; read blind, 31 / 4.9 / 2.

### Collector Ivan: Route 221, optional, single, cap 53

Rare finds: Carnivine's Petal Blizzard and Sleep Powder, Chandelure, Mawile and a Super Luck Togekiss.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Carnivine | 51 | Leftovers | Levitate | default | Petal Blizzard, Crunch, Sleep Powder, Knock Off |
| Mawile | 50 | Sitrus Berry | Intimidate | default | Play Rough, Iron Head, Sucker Punch, Crunch |
| Chandelure | 48 | Sitrus Berry | Flash Fire | default | Shadow Ball, Flamethrower, Energy Ball, Will-O-Wisp |
| Togekiss | 50 | none | Super Luck | default | Air Slash, Dazzling Gleam, Aura Sphere, Roost |

Today's team: Togekiss 47 (Hidden Power, Shadow Ball, Aura Sphere, Air Slash). Expected: 96 / 1.12 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Worker Dillan: Fuego Ironworks, optional, single, cap 53

Kaizo's ironworks team scaled from level 90: Skarmory's Stealth Rock and Whirlwind, a Guts Machamp on a Flame Orb, Camerupt and Magcargo's Scorching Sands.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 51 | Leftovers | Filter | default | Stealth Rock, Brave Bird, Roost, Whirlwind |
| Camerupt | 48 | Sitrus Berry | Solid Rock | default | Lava Plume, Earth Power, Rock Slide, Yawn |
| Magcargo | 48 | Sitrus Berry | Solid Rock | default | Lava Plume, Scorching Sands, Earth Power, Recover |
| Machamp | 50 | Flame Orb | Guts | default | Facade, Close Combat, Knock Off, Stone Edge |

Today's team: Machamp 46 (Flame Orb; Close Combat, ThunderPunch, Bulk Up, SmellingSalt). Expected: 96 / 1.42 / 26 blind in my simulator, about 70 clean in the scorer's terms.

### Worker Holden: Fuego Ironworks, optional, single, cap 53

Kaizo's fire squad scaled: Blaziken, Rapidash's Drill Run, Arcanine's Extreme Speed and Mawile.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mawile | 48 | Sitrus Berry | Intimidate | default | Play Rough, Iron Head, Sucker Punch, Crunch |
| Arcanine | 49 | Sitrus Berry | Intimidate | default | Flare Blitz, ExtremeSpeed, Wild Charge, Crunch |
| Rapidash | 49 | none | Flame Body | default | Flare Blitz, Megahorn, Drill Run, Wild Charge |
| Blaziken | 51 | Sitrus Berry | Blaze | default | Blaze Kick, Sky Uppercut, Brave Bird, Protect |

Today's team: Magneton 44 (Tri Attack, Thunderbolt, Flash Cannon, Thunder Wave), Aggron 44 (Head Smash, Iron Head, ThunderPunch, Outrage). Expected: 97 / 1.63 / 21 blind in my simulator, about 68 clean in the scorer's terms.

### Worker Conrad: Fuego Ironworks, optional, single, cap 53

Kaizo's double scaled to a single: Toxicroak's Fake Out and Foul Play, Lucario, Houndoom and Blastoise.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Toxicroak | 49 | Black Sludge | Dry Skin | default | Fake Out, Poison Jab, Drain Punch, Foul Play |
| Lucario | 48 | Sitrus Berry | Adaptability | default | Aura Sphere, Flash Cannon, Dark Pulse, Dragon Pulse |
| Houndoom | 48 | Leftovers | Flash Fire | default | Dark Pulse, Flamethrower, Sludge Bomb, Sucker Punch |
| Blastoise | 51 | Leftovers | Shell Armor | default | Surf, Ice Beam, Aura Sphere, Rapid Spin |

Today's team: Magmortar 46 (Confuse Ray, Flare Blitz, ThunderPunch, Mach Punch). Expected: 98 / 0.82 / 48 blind in my simulator, about 79 clean in the scorer's terms.

