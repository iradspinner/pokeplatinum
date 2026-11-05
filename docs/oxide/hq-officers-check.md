# Officers Hesperid and Argo at the HQ: a check of Ian's redrafts

Ian redrafted the two HQ officers in his OxiDex on 2026-11-04. Both are named Galactic officers, so mini-bosses, each a single battle in HQ's split (cap 60, no honour cap): Hesperid in the laboratory by the control room's door, Argo on 4F after Cyrus. Both teams are saved on branch `overseer-hq-officers` exactly as drafted. Nothing in either team was changed; what I think should change is asked below. No scorer reading was run, and nothing was seen in game.

## Ian's answers (2026-11-04)

Ian answered both questions and approved landing both officers. Rampardos becomes Lonely and Sinistcha stays Modest (question 1). Argo's flags gain Check HP and Risky, so they are now Basic, Evaluate Attack, Expert, Check HP and Risky (question 2). Hesperid stays exactly as drafted. Both edits went through `trainers.save`: the lint finds nothing, the packer packs the file, `make rom` builds, test_trainers passes 44 of 44 and test_learncheck 18 of 18, and `scriptindex.py --check` finds the committed index current. No nature now repeats on Argo's team. The probe was not rerun on the two answers together; each was read alone below (90 wins with Lonely, 78 with the two flags, against 72 as drafted, all inside the blur). Argo's table below shows the team as it now stands; the rest of the page is the check as it was put to Ian, before these answers.

## Summary

Both fights read much harder than the helper's drafts they replace, and both still read easier than their commanders on the same boxes. Neither looks trivial. One rule breaks: Argo's Rampardos and Sinistcha share a Modest nature, and Modest also lowers Rampardos's Attack, which every one of its moves uses. Argo's Runerigus has Mean Look and Destiny Bond, but at Speed 49 the AI almost never picks Destiny Bond on Argo's flags. Nine moves were on no list at their levels and are now on egg lists.

### Officer Hesperid, the laboratory

Flags: Basic, Evaluate Attack, Expert, Risky, Check HP.

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---:|---|---|---|---|
| Electrode | 56 | Static | Focus Sash | Hasty | Explosion, Swagger, Mirror Coat, Volt Switch |
| Garganacl | 57 | Purifying Salt | Leftovers | Careful | Salt Cure, Block, Recover, Protect |
| Blaziken | 56 | Speed Boost | Shell Bell | Adamant | Protect, Swords Dance, Flare Blitz, Thunderous Kick |
| Nidoking | 57 | Sheer Force | Life Orb | Timid | Earth Power, Sludge Wave, Thunder, Fire Blast |
| Meowscarada | 56 | Protean | Expert Belt | Naughty | Flower Trick, Triple Axel, Will-O-Wisp, Sucker Punch |
| Exploud | 58 | Scrappy | Silk Scarf | Rash | Boomburst, Focus Blast, Zen Headbutt, Circle Throw |

### Officer Argo, 4F after Cyrus

Flags: Basic, Evaluate Attack, Expert, Check HP, Risky (Ian's answer 2; drafted with the first three).

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---:|---|---|---|---|
| Tyranitar | 56 | Sand Stream | Focus Sash | Sassy | Crunch, Earthquake, Aerial Ace, Stealth Rock |
| Runerigus | 56 | Wandering Spirit | Colbur Berry | Relaxed | Destiny Bond, Mean Look, Will-O-Wisp, Earthquake |
| Blastoise | 56 | Shell Armor | Leftovers | Bold | Shell Smash, Hydro Cannon, Blizzard, Aura Sphere |
| Crustle | 57 | Weak Armor | Custap Berry | Adamant | Shell Smash, Leech Life, Stone Edge, Earthquake |
| Sinistcha | 58 | Heatproof | White Herb | Modest | Shell Smash, Shadow Ball, Giga Drain, Strength Sap |
| Rampardos | 58 | Rock Head | Hard Stone | Lonely (Ian's answer 1; drafted Modest) | Rock Polish, Head Smash, Zen Headbutt, Fire Punch |

### What the checks found

Each cell is the player's wins in 150 rough fights against the matchup screen's best six, then the six it takes most; one number means the two were the same six. Fewer wins means a harder fight. The player is the greedy probe player of the earlier checks, so only the comparison between rows means anything, and the probe does not order fights within about 35 wins of each other ([probe-ranking.md](probe-ranking.md)). The officers' three boxes are goal 3's at their place, at 58, and the two officers meet the same three boxes.

| Fight | Box 1 | Box 2 | Box 3 | Mean | Screen's best score, by box |
|---|---|---|---|---:|---|
| Hesperid, Ian's redraft | 52, 35 | 71, 65 | 31, 53 | 51 | 15.00, 15.35, 14.70 |
| Hesperid, the helper's draft | 108, 128 | 92, 95 | 97, 84 | 101 | 19.70, 18.95, 19.10 |
| Argo, Ian's redraft | 69 | 73, 67 | 79, 78 | 72 | 17.10, 16.75, 15.95 |
| Argo, the helper's draft | 107, 118 | 129, 133 | 108, 110 | 118 | 17.55, 19.05, 18.40 |
| Saturn 2, on the officers' boxes | 18, 25 | 36, 15 | 6, 5 | 18 | 18.30, 16.20, 16.50 |
| Cyrus 2, on the officers' boxes | 27, 25 | 26, 19 | 10, 4 | 18 | 16.65, 15.50, 16.05 |
| Saturn 2, on his own boxes at 60 | 40, 19 | 72, 12 | 20 | 30 | 19.75, 18.20, 17.10 |
| Cyrus 2, on his own boxes at 60 | 25, 37 | 68, 64 | 51, 76 | 54 | 16.90, 17.80, 17.35 |

Hesperid's redraft reads about 50 wins harder than the helper's draft, and Argo's about 46: both gaps are past the probe's blur. On the screen, Hesperid's best answers score lowest of all eight rows, so the box answers him worse one on one than it answers either commander. The probe still reads both commanders far harder: Saturn 2, Hesperid's commander, and Cyrus 2, Argo's (Argo fights beside Cyrus at Celestic and follows him on 4F), read 18 on the same boxes. On their own boxes at 60, where the player meets them, they read 30 and 54. So neither officer reads harder than his commander by either reading, and Hesperid is the closer of the two.

The rules: no one-hit KO move on either team, no evasion move or item, no Choice item. Hesperid's items and natures are all different. Argo's items are all different, but Modest repeats (question 1). Two trapping moves (Garganacl's Block, Runerigus's Mean Look) and two trade moves (Electrode's Explosion, Runerigus's Destiny Bond) are in; the named Galactic fights may carry both. Nidoking's Life Orb is a trainer's item, which the ruling allows, since the Life Orb ban is the player's. The trainer lint finds nothing on either file, and the packer packs both.

The flags. Hesperid's fit what his team does. Check HP holds Electrode's Explosion until Electrode is at 30 percent or less (40 to 60 of its 44 to 62 explosions a six), which its Focus Sash sets up. Risky lifts the gambles in its table, which are Electrode's Explosion, Swagger and Mirror Coat and Meowscarada's Sucker Punch: without Risky, Explosion falls to 16 to 46 picks a six and Sucker Punch to 23 to 30, and the fight reads 55, the same within the blur. Flower Trick is not in Risky's table, and it always crits anyway. Argo's base flags leave his Destiny Bond nearly dead (question 2). Neither team leads with a weather move, so the Weather flag would do nothing; Tyranitar's Sand Stream needs none.

Neither fight looks trivial. The greedy player loses 5.25 to 5.60 Pokemon a fight against Hesperid and 4.89 to 5.16 against Argo, against 3.90 to 4.99 and 3.09 to 4.13 for the helper's drafts. The probe player is far worse than a careful one, but in earlier checks the officers that read 94 to 100 percent won on the scorer sat at 80 to 120 wins on the probe, and these two sit at 51 and 72. Nothing calls for a scorer reading.

### The egg moves added

Under Ian's rule of 2026-10-29, each move no list gives at its member's level went on the first stage's egg list and in `learnrewrite.IAN_EGG_MOVES`. No level-up entry moved, and the player never reaches an egg list.

| Member | Move | Egg list |
|---|---|---|
| Hesperid's Electrode 56 | Volt Switch | Voltorb's, its first egg list |
| Hesperid's Garganacl 57 | Protect | Nacli's |
| Hesperid's Blaziken 56 | Swords Dance | Torchic's |
| Hesperid's Nidoking 57 | Sludge Wave | Nidoran's |
| Hesperid's Meowscarada 56 | Will-O-Wisp, Sucker Punch | Sprigatito's |
| Hesperid's Exploud 58 | Boomburst, Circle Throw | Whismur's |
| Argo's Blastoise 56 | Hydro Cannon | Squirtle's |

### Ian's questions, as they were put (both answered above)

1. Argo's Rampardos and Sinistcha are both Modest, and each member is to have its own nature. Modest also lowers Rampardos's Attack, so its Head Smash runs from 207 Attack where it would have 254 with an Attack-raising nature. Recommended: Rampardos Lonely (Attack up, Defense down), which keeps its Speed for Rock Polish and leaves Sinistcha Modest; Adamant is taken by Crustle. Read on the same boxes, Lonely gives 90 against 72, inside the blur, and the change is that the screen picked other sixes, not anything Rampardos did (its knockouts were 116 to 163 a six against 110 to 151). Or Naughty (Attack up, Sp. Def down), or keep Rampardos Modest and give Sinistcha another nature.
2. Argo's Runerigus carries Mean Look and Destiny Bond, a trap and a trade. At Speed 49 it is slower than nearly every box answer, and Expert never picks Destiny Bond from a slower user, so it picked Destiny Bond 0 to 112 times a six and used it 0 to 69 times, and three of the five sixes saw it picked 10 times or fewer. Recommended: add Check HP and Risky. Risky lifts Destiny Bond for the slower user, and with both flags it was picked 74 to 159 times a six and used 20 to 93 times. Check HP is the guide's flag for a trade move, keeps a healthy Runerigus off Destiny Bond, and times the three Shell Smashes and Strength Sap. Risky also lifts Crustle's Stone Edge, which was already its top pick (203 to 305 picks with Risky, 118 to 259 without). The fight reads 78 with both flags against 72, the same within the blur. Or Check HP alone, the guide's rule, which changed nothing here (Destiny Bond 2 to 84 uses, the fight 77). Or keep the base flags, leaving Destiny Bond as a threat the AI rarely uses.

Nothing on Hesperid's team needs an answer.

### Next steps

| Step | Who | Time |
|---|---|---|
| Answer the two questions, a line each | Ian | done, 2026-11-04 |
| Apply the answers through `trainers.save` | a session | done, 2026-11-04 |
| Land the branch with `merge-branch.sh`, then `sync-docs.sh` on oxide | the Overseer | 30 minutes |
| Play both fights in the HQ | Ian | his time |

## The checks in detail

### What each member does (the AI-picks probe)

Per 150 fights a six, over the screen's best and most-taken six on each of the three boxes (six sixes for Hesperid, five for Argo, whose box 1 gave one six twice):

| Hesperid | Knocked out while it was in | What the AI picks |
|---|---|---|
| Electrode | 136 to 207 | Volt Switch 196 to 321, Swagger 162 to 190, Mirror Coat 83 to 143, Explosion 44 to 62; its Focus Sash held a hit 32 to 88 times |
| Garganacl | 68 to 160 | Salt Cure 215 to 431, Recover 83 to 157, Protect 39 to 119, Block 16 to 35 |
| Blaziken | 95 to 214 | Flare Blitz 124 to 192, Thunderous Kick 26 to 105, Protect 43 to 62, Swords Dance 30 to 60 |
| Nidoking | 140 to 240 | Sludge Wave, Fire Blast and Thunder by target, Earth Power least |
| Meowscarada | 85 to 125 | Triple Axel 61 to 160, Sucker Punch 58 to 102, Flower Trick 24 to 82, Will-O-Wisp 9 to 70 |
| Exploud | 80 to 141 | Boomburst 191 to 231; Focus Blast, Zen Headbutt and Circle Throw rarely (1 to 38 each) |

Electrode leads with Mirror Coat, Swagger or Volt Switch, about a third each, and it came back in at full HP with its Sash 72 to 163 times a six, Volt Switch taking it out. The simulator runs Salt Cure's eighth a turn and charges Nidoking no Life Orb recoil, since Sheer Force takes the recoil off moves with an added effect and all four of his have one. Every member made knockouts.

| Argo | Knocked out while it was in | What the AI picks |
|---|---|---|
| Tyranitar | 53 to 76 | Stealth Rock first in 72 to 106 fights of 150, then Aerial Ace, Earthquake and Crunch by target; its Focus Sash held a hit 23 to 60 times |
| Runerigus | 28 to 153 | Earthquake 151 to 298, Will-O-Wisp 94 to 151, Mean Look 45 to 108, Destiny Bond 0 to 112 picks and 0 to 69 uses |
| Blastoise | 74 to 123 | Hydro Cannon 68 to 179, Blizzard 23 to 104, Shell Smash 44 to 76 |
| Crustle | 155 to 215 | Stone Edge 118 to 259, Earthquake 59 to 94, Shell Smash 40 to 83; its Custap Berry went 14 to 48 times |
| Sinistcha | 112 to 218 | Giga Drain 122 to 151, Shadow Ball 92 to 193, Shell Smash 72 to 92, its White Herb spent 39 to 81 times |
| Rampardos | 110 to 151 | Head Smash 218 to 346; Rock Polish 0 to 6 picks, used at most twice a six |

Stealth Rock hurt the player's Pokemon on entry 514 to 631 times a six, and the sand chips every one that is not Rock, Ground or Steel at each turn's end. Rampardos's Rock Head takes the recoil off Head Smash, so Head Smash is always its best attack and Rock Polish loses to it. I leave that as it stands: a fourth attack in Rock Polish's place would lose to Head Smash too, as Fire Punch (0 to 61 picks) and Zen Headbutt (0 to 26) do. Hydro Cannon is Oxide's version, 150 power with half the damage as recoil.

### The lead test

Ian's test (2026-10-29): a lead may be countered when the answer draws in a member that beats it, best with a setup move. Electrode's common answers mostly draw a Blaziken that beats them with Swords Dance behind it (Torterra, Frosmoth, Metagross, Tsareena, Heracross, Weavile); Snorlax, Milotic, Ceruledge, Cinderace and Machamp draw a member that loses to them. Tyranitar's answers mostly draw a member that beats them: Frosmoth draws Crustle with Shell Smash, Staraptor and Mandibuzz draw Rampardos, Bastiodon draws Runerigus, and Kingler and Manaphy draw Sinistcha with Shell Smash; Mamoswine, Tsareena, Corviknight and Breloom draw one that loses. Both leads pass.

### Speed against the box

Each member's Speed in battle against the likely answers, the catches the screen's top sixes take most, at 58:

| Member | Speed | Box answers it outspeeds | Box answers that outspeed it |
|---|---|---|---|
| Hesperid's Electrode | 196 | all | none |
| Hesperid's Meowscarada | 160 | all but Crobat | Crobat 164 |
| Hesperid's Blaziken | 111, then 166 and 222 by Speed Boost | after one boost, all | before its first boost, everything from Ceruledge 112 up |
| Hesperid's Nidoking | 130 | Manaphy 129, Tsareena 120, Qwilfish, Ceruledge and Heracross 112, Milotic 107 and the slower | Crobat 164, Talonflame 159, Weavile 158, Cinderace 151, Mienshao and Staraptor 135 |
| Hesperid's Exploud | 113 | Qwilfish, Ceruledge and Heracross 112, Milotic and the slower | Tsareena 120 and the faster |
| Hesperid's Garganacl | 62 | Snorlax, Bastiodon and Magcargo 48 | everything else |
| Argo's Sinistcha | 104, then 208 after Shell Smash | Kingler 100, Breloom 94, Corviknight 91, Frosmoth 89, Jellicent 83 and the slower; after Shell Smash, all | Mamoswine and Mandibuzz 106 and the faster |
| Argo's Rampardos | 90, then 180 after Rock Polish | Frosmoth 89, Jellicent 83, Golem 65, Bastiodon 48 | Corviknight 91 and every faster answer |
| Argo's Blastoise | 89, then 178 after Shell Smash | Jellicent, Golem, Bastiodon, and ties Frosmoth 89; after Shell Smash, all | Corviknight 91 and the faster |
| Argo's Tyranitar | 81 | Golem 65, Bastiodon 48 | Jellicent 83 and the faster |
| Argo's Crustle | 73, then 146 after Shell Smash | Golem, Bastiodon; after Shell Smash all but Cinderace 151 and Floatzel 147 | everything else |
| Argo's Runerigus | 49 | Bastiodon 48 | everything else |

The reference set at 58 (Crobat 164, Talonflame 159, Weavile 158, Greninja 155, Mienshao 135, Staraptor 135, Garchomp 132, Lucario 118) gives the same picture. Hesperid's Electrode and Meowscarada outspeed nearly the whole box and his Blaziken does after one turn; Argo's six are slow until a Shell Smash. In battle, Cyrus 2's Weavile runs at 187, and Saturn 2's six all sit under the box's fast answers inside his permanent Trick Room.

### Against the themes

Hesperid's theme ([boss-shapes.md](boss-shapes.md)) is Platinum Kaizo teambuilding with no holds barred, on rarely used Pokemon in weird combinations, the weirder and harder the better. The redraft is a Kaizo team in its pieces: a Focus Sash lead that gambles on Swagger, Mirror Coat and Explosion, a Salt Cure staller that traps with Block, a Speed Boost Blaziken behind Protect, a Sheer Force Life Orb Nidoking, a Protean Meowscarada and a Scrappy Silk Scarf Boomburst. Its weirdness is in the sets rather than the species: Electrode, Garganacl and Exploud are rare picks, while Blaziken, Nidoking and Meowscarada are not. On harder, it reads about 50 wins harder than the draft it replaces. Ian's ruling lets Hesperid alone read harder than his commander, and he still reads easier than Saturn 2.

Argo's theme is the loosest, free to change entirely. The redraft is shells and relics: three Shell Smashers (Blastoise, Crustle, Sinistcha), a Rock Polish fossil, a Sand Stream Tyranitar laying Stealth Rock, and a Runerigus that traps. Its Sinistcha ace keeps the old draft's Polteageist set, Shell Smash behind a White Herb, the set Ian asked to have watched as a sweeper in Argo 1.

## The boxes

The two officers share three boxes, goal 3's at their place under the run name `hq-officers-study`, seeds 1 to 3, at 58. Each list gives a catch once, with any versions held below their evolution at the levels named. Saturn 2's and Cyrus 2's rows "on the officers' boxes" meet these same boxes.

Box 1 (84 entries): Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox (also held at 15), Nidorino, Pawmo, Corviknight (also held at 55 and 50), Mandibuzz, Crobat, Talonflame (also held at 32 and 33), Probopass, Seaking (also held at 51), Quagsire, Kingler (also held at 45), Tentacruel, Cherrim, Sharpedo (also held at 38), Plusle, Leavanny (also held at 36 and 43), Lombre, Ninetales-Alola, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis (also held at 45), Granbull (also held at 49), Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Scyther, Mienshao (also held at 58), Masquerain (also held at 37 and 43), Crustle, Onix, Houndoom, Liepard, Toxicroak, Jellicent, Manaphy, Snorlax (also held at 44 and 49), Milotic, Altaria (also held at 50), Gastrodon, Cinderace, Octillery (also held at 32), Metagross (also held at 52), Seadra, Corsola, Goodra, Frosmoth, Mamoswine (also held at 49), Jynx, Dewgong.

Box 2 (92 entries): Cinderace (also held at 44), Whiscash, Staraptor, Masquerain (also held at 31, 37 and 43), Lombre, Bibarel, Orbeetle (also held at 36, 40 and 48), Liepard (also held at 33 and 35), Nidorino, Mandibuzz, Crobat, Rapidash, Donphan (also held at 37 and 42), Seaking (also held at 51), Garganacl, Lumineon (also held at 49), Tentacruel, Vespiquen, Arboliva, Tsareena (also held at 29), Leavanny (also held at 36 and 43), Primarina (also held at 57), Ninetales-Alola, Bronzong (also held at 49 and 52), Nuzleaf (also held at 21), Rotom, Togetic, Bastiodon, Onix, Glaceon, Glimmora, Heracross, Granbull (also held at 49), Glalie, Pachirisu, Gothitelle (also held at 55), Floette, Murkrow, Golem, Vikavolt (also held at 30 and 40), Drifblim, Magcargo (also held at 53 and 56), Hippowdon, Palossand, Tropius, Floatzel, Sharpedo (also held at 38), Drapion, Lopunny, Manaphy, Skitty, Jellicent, Toxicroak, Ceruledge, Empoleon, Gastrodon, Corsola, Octillery, Lurantis (also held at 45), Milotic, Frosmoth, Mr. Rime, Absol, Dewgong.

Box 3 (93 entries): Empoleon (also held at 51), Seaking (also held at 51), Corviknight (also held at 55 and 50), Orbeetle (also held at 36, 40 and 48), Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Mandibuzz, Crobat, Hariyama, Onix, Roselia, Golem, Kingler (also held at 45), Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom (also held at 29, 33 and 37), Lombre, Mothim, Carbink, Vikavolt (also held at 30 and 40), Rotom, Togetic, Bastiodon, Salazzle, Glaceon, Crustle, Leavanny (also held at 36 and 43), Granbull (also held at 49), Bronzong (also held at 49 and 52), Gothitelle (also held at 55), Sinistea, Floette, Happiny, Glimmora, Yanmega (also held at 43), Castform, Quagsire, Garganacl, Palossand, Lopunny, Grapploct, Sharpedo (also held at 38), Gliscor (also held at 49), Qwilfish, Manaphy, Pikachu, Crawdaunt, Altaria (also held at 50), Gastrodon, Cinderace, Lumineon (also held at 49), Metagross (also held at 52), Octillery, Nuzleaf, Floatzel, Frosmoth, Glalie, Weavile (also held at 49, 51, 56 and 58), Dewgong.

The commanders' own boxes, at 60, hold the same catches with a few changes. Saturn 2's lack the held Granbull at 49, Lumineon at 49 and Gliscor at 49, and box 3's held Empoleon. Cyrus 2's lack the same held versions and add Gorebyss and Machamp on box 1, Abomasnow and Machamp on box 2, and Milotic and Klefki on box 3.

The sixes each version met, the screen's best first, then the six it takes most where that differs:

| Fight | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Hesperid, Ian's redraft | Torterra, Staraptor, Corviknight, Talonflame, Mienshao (held at 58), Snorlax; then Corviknight, Talonflame, Snorlax, Torterra, Frosmoth, Mienshao (held at 58) | Cinderace, Staraptor, Tsareena, Heracross, Ceruledge, Milotic; then Tsareena, Ceruledge, Milotic, Cinderace, Heracross, Crobat | Corviknight, Kingler, Vikavolt, Qwilfish, Frosmoth, Weavile (held at 51); then Corviknight, Qwilfish, Weavile (held at 51), Machamp, Frosmoth, Kingler |
| Hesperid, the helper's draft | Staraptor, Mandibuzz, Tentacruel, Ninetales-Alola, Snorlax, Frosmoth; then Frosmoth, Snorlax, Mandibuzz, Ninetales-Alola, Tentacruel, Houndoom | Mandibuzz, Donphan, Tentacruel, Bronzong (held at 49), Glimmora, Frosmoth; then Bronzong (held at 49), Frosmoth, Mandibuzz, Tentacruel, Glimmora, Primarina (held at 57) | Mandibuzz, Tentacruel, Bastiodon, Salazzle, Altaria, Frosmoth; then Frosmoth, Mandibuzz, Salazzle, Carbink, Tentacruel, Altaria |
| Argo, Ian's redraft | Staraptor, Bastiodon, Houndoom, Jellicent, Frosmoth, Mamoswine | Cinderace, Staraptor, Tsareena, Golem, Jellicent, Frosmoth; then Jellicent, Tsareena, Frosmoth, Staraptor, Golem, Mandibuzz | Corviknight, Mandibuzz, Golem, Tentacruel, Bastiodon, Frosmoth; then Mandibuzz, Frosmoth, Golem, Tentacruel, Bastiodon, Breloom |
| Argo, the helper's draft | Torterra, Staraptor, Bibarel, Corviknight, Mandibuzz, Cherrim; then Torterra, Mandibuzz, Snorlax, Cherrim, Manaphy, Corviknight | Staraptor, Bibarel, Mandibuzz, Tsareena, Bronzong, Gothitelle; then Tsareena, Mandibuzz, Bronzong, Staraptor, Arboliva, Gothitelle | Corviknight, Dubwool, Mandibuzz, Breloom, Gothitelle, Weavile (held at 51); then Mandibuzz, Breloom, Weavile (held at 51), Corviknight, Gothitelle, Bronzong |
| Saturn 2, on the officers' boxes | Staraptor, Corviknight, Probopass, Cherrim, Abomasnow, Jellicent; then Corviknight, Cherrim, Jellicent, Snorlax, Probopass, Staraptor | Staraptor, Orbeetle, Primarina, Bronzong, Bastiodon, Jellicent; then Jellicent, Primarina, Staraptor, Bastiodon, Bronzong, Drapion | Empoleon, Corviknight, Machamp, Bronzong, Gliscor, Frosmoth; then Corviknight, Gliscor, Frosmoth, Bronzong, Bastiodon, Roselia |
| Cyrus 2, on the officers' boxes | Luxray, Probopass, Bastiodon, Crawdaunt, Jellicent, Frosmoth; then Bastiodon, Crawdaunt, Jellicent, Probopass, Frosmoth, Jynx | Cinderace, Garganacl, Primarina (held at 57), Bastiodon, Glaceon, Jellicent; then Primarina (held at 57), Bastiodon, Garganacl, Glaceon, Gastrodon, Jellicent | Golem, Tentacruel, Bastiodon, Crawdaunt, Gastrodon, Frosmoth; then Bastiodon, Crawdaunt, Frosmoth, Gastrodon, Cinderace, Dewgong |
| Saturn 2, his own boxes | Corviknight, Crobat, Probopass, Cherrim, Abomasnow, Jellicent; then Corviknight, Crobat, Cherrim, Abomasnow, Jellicent, Torterra | Crobat, Primarina, Bronzong, Bastiodon, Heracross, Jellicent; then Jellicent, Heracross, Primarina, Crobat, Bastiodon, Drapion | Corviknight, Machamp, Crobat, Bronzong, Gliscor, Frosmoth |
| Cyrus 2, his own boxes | Torterra, Probopass, Tentacruel, Bastiodon, Crawdaunt, Goodra; then Bastiodon, Crawdaunt, Probopass, Goodra, Tentacruel, Jellicent | Tsareena, Primarina (held at 57), Rotom, Bastiodon, Glaceon, Absol; then Tsareena, Absol, Bastiodon, Primarina (held at 57), Glaceon, Magcargo | Whiscash, Hariyama, Rotom, Bastiodon, Glaceon, Crawdaunt; then Hariyama, Bastiodon, Crawdaunt, Glaceon, Rotom, Tentacruel |

The helper's drafts are the HQ pass's (commit ee717064cd1, `hq-split.md`'s "The officers' drafts"): Hesperid's Spinda, Girafarig, Spiritomb, Weezing, Sceptile and Pinsir on Basic, Evaluate Attack, Expert, Baton Pass and Check HP, and Argo's Claydol, Cofagrigus, Bronzong, Relicanth and Polteageist on the base flags. They read 101 and 118 here, against 104 and 124 in the HQ pass on the tree before the evasion fix: inside the probe's spread.

## How the numbers were made

Every number comes from the worktree `.claude/worktrees/hq-officers` on this branch. The scripts are the HQ pass's probe harness, copied to `/home/ian/.claude/jobs/382760ce/tmp/hq-officers/probe/` and pointed at this worktree under the run name `hq-officers-study`; none writes to `res/`. `bc.py` loads goal 3's box for a place and any fight against it; `OLDFILE` swaps a whole trainer file, party and flags, into memory, which is how the helper's drafts from git history met the same boxes; `CAND` swaps one field (Rampardos's nature) and `AIBITS` the flags. `checks.py FIGHT PLACE SEED` runs the screen, the replacement trace, damage both ways and the probe of 150 rough fights against the screen's best and most-taken six, and prints the box. `runjobs.sh` ran every job under `tools/oxide/capped`. `bait.py` is Ian's lead test, `gather.py` the per-six ranges and `table.py` the wins table. Legality comes from the OxiDex's `learnsets.oxide_list` at each member's level, which gives all 48 moves of the two teams since the egg-list commit. The trainer lint finds nothing, the packer packs both files, `make rom` builds, test_trainers passes 44 of 44, test_learncheck 18 of 18 and test_learnrewrite 6 of 6.
