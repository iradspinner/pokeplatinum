# Byron: Ian's redraft and its last looks

Ian redrafted Byron (Canalave Gym, cap 53) himself on 2026-11-02, and the scorer read it at 97, 96 and 100 percent won over goal 3's three boxes, with 2.27, 1.71 and 1.17 faints a fight (run `byron-ian-64ad14736`). Today's Byron read 100 with 0.7 faints. Ian, 2026-11-02: "I genuinely don't think I could easily conceive a harder team than the one I made (improving Kartana's moves and maybe adding magearna excepted)." This page answers those two last looks. Under the ruling of 2026-11-02 the scorer is a ceiling and a boss need only be clearly harder than before, so faints a fight count here as much as the percent won. No trainer file changes until Ian picks. No scorer reading was run, and the simulator was not touched.

## Summary

Both looks make Byron harder, and they make it clearly harder together. Kartana's best new set (Sacred Sword, Leaf Blade, Night Slash, Aerial Ace, Adamant) adds about half a faint a fight, nearly all of it on box 2. Magearna in Metagross's place adds about a quarter of a faint on its own. The two together read 92 percent won with 2.57 faints a fight over the three boxes, against the draft's 98 and 1.72, and are the only version harder on every box.

The counterpiece check, the draft against the sixes the scorer chose to beat it (won, faints and clean in percent and faints a fight, 75 fights a box at real odds):

| Version | Box 1 (Turtwig) | Box 2 (Scorbunny) | Box 3 (Piplup) | All three |
|---|---|---|---|---|
| Ian's draft, the reading itself | 97, 2.27, 1 | 96, 1.71, 23 | 100, 1.17, 0 | 98, 1.72, 8 |
| Kartana K1 | 97, 2.29, 0 | 81, 3.23, 4 | 99, 1.15, 0 | 92, 2.22, 1 |
| Kartana K2 | 97, 2.53, 0 | 88, 2.73, 3 | 100, 1.55, 1 | 95, 2.27, 1 |
| Magearna for Metagross | 93, 2.56, 1 | 97, 1.96, 15 | 100, 1.49, 19 | 97, 2.00, 12 |
| K2 and Magearna together | 89, 3.11, 0 | 89, 2.84, 5 | 99, 1.76, 13 | 92, 2.57, 6 |

Ian's decisions:

1. Kartana's set. (a) K2: Sacred Sword, Leaf Blade, Night Slash, Aerial Ace, Adamant, Focus Sash (recommended). (b) K1: Sacred Sword, Leaf Blade, Smart Strike, Swords Dance, Adamant, Focus Sash. (c) Keep today's set. I recommend K2 over K1 because the two tie on faints over the three boxes (2.27 and 2.22), and K2 is the one harder on box 3 (1.55 faints against 1.15), where its Kartana made 33 knockouts and K1's almost none. K1 leans on box 2 alone.
2. Magearna in for Metagross. (a) Yes, with Kartana's new set (recommended). (b) Yes, with today's Kartana. (c) No, Metagross stays. I recommend (a): the pair adds 0.85 faints a fight over the three boxes and is harder on every box, where K2 alone adds 0.55 and Magearna alone 0.28. Together Kartana made 24, 51 and 22 knockouts and Magearna 11, 6 and 3.

Either pick of K1 or K2 puts Sacred Sword and Leaf Blade on Kartana's egg list by the egg-list rule; they are its level 60 and 55 moves, and Night Slash, Aerial Ace, Smart Strike and Swords Dance are already in its palette. Magearna's four are all legal at 50 without any change. Every candidate passes the trainer lint.

Ian's answer on the legendary count, 2026-11-03: "This was before we started running into issue pumping up the difficulty, and I consider ultra beasts approximately similar to mythicals; two or 3 in a boss fight is still acceptable." So Magearna beside Kartana and Celesteela, three in all, is within the limit.

Two notes. These rows are on the old type chart, where Steel resists Ghost and Dark; Steel's later chart, landing on `oxide` now, makes both neutral on Steel, which softens Byron a little on every version. And one finding, recorded only: Fleur Cannon's data gives it 100 accuracy, where the later games give 90; whether to change it is the Overseer's call, as its own commit.

Next step. Once Ian picks, the Overseer or a helper writes his pick into `leader_byron.json` with the OxiDex's save, puts the egg moves on Kartana's list, and rebuilds; about half an hour. The check plays the draft's sixes only, with no team search, so a full reading could find a better six; Ian asked for none.

## Kartana

Kartana's job is a fast physical hitter with a Sash, and in the reading it did the least of the six: 4, 15 and 6 knockouts over each box's fights. In all three traced fights it came in late, on Empoleon's Flip Turn or after a faint, used only Brick Break and Aerial Ace, never Swords Dance, and landed its first hit on a Fire type for 34 to 51 percent (Talonflame on box 1, Cinderace on box 2, Salazzle on box 3) before a Fire hit it is four times weak to finished it. Its set reaches too few of the sixes: on the calculator Ian's set two-hits 3, 1 and 3 of each box's six members at the lowest roll.

| Set | Two-hits, box 1, 2, 3 | Knock-outs in one hit | Kartana's knockouts in the check |
|---|---|---|---|
| Today's | 3, 1, 3 | Houndoom, Heracross | 4, 15, 6 |
| K1 | 4, 5, 4 | Luxray, Houndoom, Manaphy, Wailord, Lucario | 5, 29, 0 |
| K2 | 4, 6, 5 | the same five and Heracross, and Delphox at the top roll | 5, 56, 33 |

Sacred Sword replaces Brick Break: 90 power against 75, and it ignores Acid Armor, Iron Defense and Bulk Up. It knocks out Luxray (101 to 121), Houndoom (157 to 185) and Lucario (121 to 143), and takes 77 to 92 from Bastiodon. Leaf Blade is the Grass hit the set lacked: Manaphy 110 to 130 and Wailord 115 to 137, and the trainer AI then sends Kartana in against both on box 2, where it was sent in against nothing before. Night Slash, K2's third, hits Delphox for 89 to 105 and Rotom for 78 to 92, and Aerial Ace stays for Heracross (144 to 170) and Hariyama. K1 keeps Smart Strike and Swords Dance in their place; Smart Strike has few targets in these boxes, and the AI never chose Swords Dance in a trace.

Impish raises Defense and lowers Special Attack, which Kartana never uses. The Defense buys almost nothing here: what kills Kartana is a Fire hit it is four times weak to, and the Sash covers the first. Adamant, free in the team, adds a tenth to every hit, and it is what keeps the Luxray knockout. Naive, the only free Speed nature (Jolly is Empoleon's and Hasty Galvantula's), puts Kartana at 144 Speed against 131, past Cinderace (139) and Salazzle (136) but not Talonflame (146), and costs that tenth; with the Sash and the Fire hits it meets, moving first gains little.

## Magearna

Set: Magearna, level 50, Soul-Heart, Sitrus Berry, Modest; Fleur Cannon, Flash Cannon, Thunderbolt, Calm Mind, in Metagross's place as the lead. It is in Oxide's species data (Steel and Fairy, 80, 95, 115, 130, 115, 65). Fleur Cannon is its level 49 move, with the same battle effect as Overheat (the user's Special Attack down two), which the engine and the simulator both run; Flash Cannon, Thunderbolt and Calm Mind are TMs 91, 24 and 04. Sitrus Berry and Modest repeat nothing in the team.

Which member it replaces was judged by each member's job in the reading. Galvantula (the Water and Flying answer, with Sticky Web) and Empoleon (the Flip Turn pivot) stay by Ian's answers of 2026-11-02, Celesteela is the ace, and Kartana is the other look. Hisuian Goodra is the team's bulk against Fire: Earthquake knocks out Houndoom and Magmar, Fire hits it for 24 to 58 percent, and it made 33 knockouts on box 1; Magearna has nothing for Fire and is weak to it. Metagross leads with Stealth Rock, Earthquake and Explosion, and its lead is the job done worst: the player's Fire lead beat it on turn one or two in two traces of three (Houndoom's Flamethrower does 98 to 116 percent to it), and it made 9, 11 and 6 knockouts. Magearna has the same base stat total of 600 and takes Metagross's level, so the swap weighs the same by stats. It takes 61 to 74 percent from the same Fire hits, and Fleur Cannon knocks out Luxray, Heracross and Hariyama and two-hits Houndoom, Lucario, Vikavolt, Rotom and Manaphy. What it gives up is Stealth Rock and the Explosion threat, which matter against these Fire-heavy sixes.

On its own Magearna moves box 1 (93 won, 2.56 faints) and adds about a quarter of a faint on boxes 2 and 3 at an unchanged percent won, with more clean wins there (15 and 19 against 23 and 0). It made 7, 0 and 12 knockouts.

## The boxes and the sixes that played

Every row on this page is the same three boxes and the same three sixes, those the scorer chose against Ian's draft in run `byron-ian-64ad14736`; each six plays with that reading's moves and items.

Box 1 (Turtwig) holds 85 catches, counting each held-back version apart, from 58 lines: Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox, Nidorino, Pawmo, Corviknight, Vullaby, Crobat, Talonflame, Probopass, Seaking, Quagsire, Kingler, Tentacruel, Cherrim, Sharpedo, Plusle, Leavanny, Lombre, Ninetales-Alola, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis, Granbull, Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Arboliva, Drifblim, Jynx, Crustle, Palossand, Altaria, Grapploct, Tangrowth, Seadra, Manaphy, Pachirisu, Jellicent, Houndoom, Magmar, Cinderace, Lumineon, Metagross, Toxapex, Tsareena.

| The six of box 1 | Moves | Item |
|---|---|---|
| Luxray | Wild Charge, Fire Fang, Crunch, Double Kick | Black Glasses |
| Talonflame | Flare Blitz, Tailwind, Aerial Ace, U-turn | Sitrus Berry |
| Houndoom | Flamethrower, Nasty Plot, Dark Pulse, Mud Shot | Sitrus Berry |
| Magmar | Flamethrower, Karate Chop, Confuse Ray, Lava Plume | Sitrus Berry |
| Cinderace | Blaze Kick, Jump Kick, Super Fang, U-turn | Sitrus Berry |
| Metagross | Hammer Arm, Psychic Fangs, Iron Defense, Take Down | Mind Plate |

Box 2 (Scorbunny) holds 94 catches, counting each held-back version apart, from 59 lines: Cinderace, Whiscash, Staraptor, Masquerain, Lombre, Bibarel, Orbeetle, Liepard, Nidorino, Vullaby, Crobat, Rapidash, Donphan, Seaking, Garganacl, Lumineon, Tentacruel, Vespiquen, Arboliva, Tsareena, Leavanny, Primarina, Ninetales-Alola, Bronzong, Nuzleaf, Rotom, Togetic, Bastiodon, Onix, Sylveon, Glimmora, Heracross, Granbull, Glalie, Pachirisu, Gothitelle, Floette, Murkrow, Golem, Weavile, Mienshao, Rhydon, Hippowdon, Crustle, Absol, Araquanid, Quagsire, Greninja, Seadra, Manaphy, Pikachu, Jellicent, Gliscor, Delphox, Empoleon, Gastrodon, Mantine, Wailord, Palossand.

| The six of box 2 | Moves | Item |
|---|---|---|
| Cinderace | Blaze Kick, Jump Kick, Taunt, Super Fang | Sitrus Berry |
| Rapidash | Overheat, Drill Run, Double Kick, Take Down | Sitrus Berry |
| Heracross | Close Combat, Rock Tomb, Bulk Up, Pin Missile | Fist Plate |
| Manaphy | Aura Sphere, Bubble Beam, Icy Wind, Acid Armor | Mystic Water |
| Delphox | Flamethrower, Will-O-Wisp, Mud Shot, Psyshock | Mind Plate |
| Wailord | Water Spout, Iron Head, Astonish, Rest | Sitrus Berry |

Box 3 (Piplup) holds 89 catches, counting each held-back version apart, from 59 lines: Empoleon, Seaking, Corviknight, Orbeetle, Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Vullaby, Crobat, Hariyama, Onix, Roselia, Golem, Kingler, Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom, Lombre, Mothim, Carbink, Vikavolt, Rotom, Togetic, Bastiodon, Salazzle, Leafeon, Crustle, Leavanny, Granbull, Bronzong, Gothitelle, Sinistea, Floette, Happiny, Cofagrigus, Delphox, Drifblim, Masquerain, Hippowdon, Palossand, Absol, Araquanid, Quagsire, Jellicent, Arboliva, Manaphy, Skitty, Milotic, Lucario, Crawdaunt, Cinderace, Octillery, Metagross, Seadra, Toucannon.

| The six of box 3 | Moves | Item |
|---|---|---|
| Hariyama (Makuhita held to 43) | Close Combat, Rock Tomb, Belly Drum, Reversal | Sitrus Berry |
| Vikavolt | Discharge, Bug Buzz, Mud Shot, Sticky Web | Silver Powder |
| Rotom | Discharge, Signal Beam, Uproar, Substitute | Magnet |
| Bastiodon | Rock Blast, Bulldoze, Hard Press, Taunt | Rock Incense |
| Salazzle | Flamethrower, Toxic, Dragon Rage, Mud Shot | Sitrus Berry |
| Lucario | Close Combat, Swords Dance, Bone Rush, Dragon Pulse | Fist Plate |

## How the numbers were made

The counterpiece check (`tools/oxide/balance/plcounter.py`, on `overseer-counterpiece`) played each candidate against run `byron-ian-64ad14736`'s own boxes and sixes, one trial on the reading's dice, 75 fights a box at real odds and 25 very unlucky, with no team search. Each candidate's tree was made by `plcounter tree` from `~/oxide-trials/goal3/tree-byron-ian` (`tree-byron-last-k1`, `-k2`, `-mag`, `-k2-mag`), and each ran under `tools/oxide/capped --max 10G` with 8 processes, two at a time. The results are `~/oxide-trials/goal3/counterpiece/byron-ian-64ad14736-last-<name>.json`. The calculator rows and the trainer AI's replacement rule came from the scorer's own state for the same boxes, with each party swapped in memory (`~/oxide-trials/goal3/byron-last-looks/calc.py`, `cands.py`, `digest.py`); nothing wrote to `res/`. Legality is from the OxiDex's lists and the Kaizo study's checker, and each candidate file passes the trainer lint.

## The record: the Galvantula question of 2026-11-02

Ian redrafted Byron (Canalave Gym, cap 53) himself on 2026-11-02. This branch, `overseer-byron-ian`, holds his six for the full scorer reading he asked for. Ian's last answer, on 2026-11-02 after the Vikavolt rows below: "Galvantula, change Deimos." Byron keeps Galvantula exactly as he drafted it, and Officer Deimos's Pal Park lead changes instead, on its own branch (`overseer-deimos-lead`). His six is in the branch's file as he drafted it, and the Overseer reads it as it stands (Ian: "No, read it as it is", to tuning box 2 first). This page keeps the replacement question and the Vikavolt check as the record of why Vikavolt was not taken. No scorer reading was run here and the simulator was not touched.

### Summary

Ian's answers of 2026-11-02:

1. The target is 80 to 88 percent won over the three boxes, with no box under 70.
2. His draft goes forward to a full scorer reading.
3. Check HP stays off ("Leave it off"), though Metagross carries Explosion.
4. Empoleon stays, though it is Barry 5's ace for a Scorbunny player.
5. "Propose any galvantula replacements": Galvantula with Sticky Web is Deimos's lead at Pal Park, a few fights earlier in the same split.
6. Vikavolt takes the slot, from the options below (Ian's pick, later the same day).
7. After the counterpiece check read Vikavolt easier: "Galvantula, change Deimos." Galvantula is back, and Deimos's lead changes.
8. "No, read it as it is": the full reading goes ahead without tuning box 2 first.

His six, as the branch now holds it, flags Basic, Evaluate Attack and Expert:

| Member | Level | Item | Nature | Moves |
|---|---:|---|---|---|
| Metagross (lead) | 50 | Shuca Berry | Naughty | Meteor Mash, Earthquake, Explosion, Stealth Rock |
| Galvantula | 51 | Occa Berry | Hasty | Sticky Web, Thunder, Energy Ball, Bug Buzz |
| Hisuian Goodra (hidden ability, Gooey) | 50 | Leftovers | Brave | Dragon Claw, Earthquake, Muddy Water, Curse |
| Kartana | 51 | Focus Sash | Impish | Brick Break, Smart Strike, Aerial Ace, Swords Dance |
| Empoleon | 52 | Mystic Water | Jolly | Aqua Jet, Flip Turn, Triple Axel, Drill Peck |
| Celesteela (ace) | 53 | Power Herb | Hardy | Flamethrower, Meteor Beam, Air Slash, Flash Cannon |

The question was which Pokemon takes Galvantula's slot, each option keeping the other five as he built them. Ian picked the first, then kept Galvantula once the check below read Vikavolt easier.

1. Vikavolt (recommended). Bug and Electric, with Galvantula's own four moves (Thunderbolt for Thunder), Occa Berry, Modest, Levitate. It keeps the whole job and does it better on the cheap checks, but it is slow, and it keeps the Sticky Web that Deimos also leads with.
2. Magnezone. Electric and Steel, Byron's own line (his Magneton in vanilla Platinum): Thunderbolt, Flash Cannon, Thunder Wave, Tri Attack, Occa Berry, Modest, Levitate. The best fit for a Steel gym. It drops the Sticky Web and the Grass hit, so Thunder Wave is its only Speed control and Quagsire goes to Empoleon and Metagross.
3. Togedemaru. Electric and Steel, fast, Sturdy in its hidden slot: Nuzzle, Zing Zap, Fake Out, Electroweb, Occa Berry, Adamant. It keeps Speed control by paralysis and Electroweb, but it hits too softly. The screen reads it the easiest of the four, Galvantula included.

My recommendation is Vikavolt if Ian's objection is to the species, and Magnezone if he also wants Sticky Web gone from Byron. The slot's work is against the Water and Flying walls, and Vikavolt is the only option the AI sends into every one of them, Quagsire and Luxray included.

The counterpiece check, Ian's draft (run `ian-final`) and the Vikavolt pick (run `ian-vikavolt`), against the sixes that beat today's Byron:

| Box (starter) | Ian's draft: won, faints, clean | Very unlucky: won, faints | With Vikavolt: won, faints, clean | Very unlucky: won, faints |
|---|---|---|---|---|
| 1 (Turtwig) | 79, 3.24, 1 | 88, 3.48 | 92, 3.44, 0 | 96, 3.44 |
| 2 (Scorbunny) | 93, 2.56, 4 | 88, 2.48 | 96, 2.20, 7 | 100, 2.40 |
| 3 (Piplup) | 88, 2.55, 15 | 60, 4.04 | 87, 2.81, 0 | 76, 3.40 |
| All | 87, 2.78, 7 | 79, 3.33 | 92, 2.82, 2 | 91, 3.08 |

The check plays the old reading's sixes only, with no team search, so a number over the target means too easy for certain, and a lower one leaves the decision to the full reading. Box 2 at 93 is over the target on Ian's draft. With Vikavolt, boxes 1 and 2 are over it, at 92 and 96, so that six is too easy for certain on those two boxes, and only box 3 (87) leaves the decision to the reading. This runs against the cheap checks, which read Vikavolt as the harder pick on every box. Vikavolt itself made more knockouts than Galvantula did (94, 52 and 80 over each box's 75 fights, against 47, 19 and 40), but the rest of the six made fewer: on box 1 Hisuian Goodra's fell from 64 to 16. The check does not say why; the likeliest cause is the Speed Vikavolt gives up, since Galvantula laid Sticky Web before the player moved and Vikavolt lays it after taking a hit. On these rows Ian kept Galvantula.

Action items for Ian on Byron: none. His answers are applied, Galvantula is in the file, and the four off-list moves of his draft are on egg lists by the rule. Deimos's new lead is a question of its own, on `overseer-deimos-lead`.

Next step. The Overseer runs the full scorer reading of this six on this branch, two and a half to four hours of machine time.

### The slot's job

Galvantula is the team's answer to the Water and Flying walls. Against every likely answer from goal 3's three boxes at 53 (`byron-redesign.md` has how they are chosen), the trainer AI's own replacement rule, `fightai.replacement`, sends Galvantula in against 10 or 11 answers a box, whichever other member leaves: Manaphy, Corviknight, Quagsire, Whiscash, Kingler, Jellicent, Empoleon, Luxray and the Flying types among them. Its Thunder, Energy Ball and Bug Buzz hit each of those for 51 to 153 percent at the lowest roll, and at 143 Speed it moves first against all but one to four Pokemon of each box. Sticky Web then cuts every switch-in's Speed by a stage. The screen and the calculator do not see that, though it may be much of what the slot gives the rest of the six: after one stage down, Manaphy (118 to 79), Houndoom (124 to 83), Luxray (113 to 75), Delphox (123 to 82) and Rapidash (129 to 86) fall under Metagross (90) and Empoleon (91), and Cinderace (139 to 93) only just stays above them.

In the check, Galvantula made the third most knockouts on box 1 (47 over 75 fights, behind Celesteela and Hisuian Goodra) and the second most on box 3 (40, behind Celesteela), and the fewest on box 2 (19), whose six is mostly Fire and Ground types it hurts little.

What a replacement must keep, then: an Electric hit the Water walls cannot answer, a Grass hit for Quagsire and Whiscash if possible, and Speed control. It must also be off the nearby bosses' teams. Barry 5 fields Staraptor, Primeape, Serperior, Snorlax, Turtonator, Empoleon, Greninja, Torterra and Infernape across his three files, and Riley fields Steelix, Mienshao, Hawlucha, Poliwrath, Kommo-o and Lucario. Thorton's six are Toxapex, Bronzong, Dusclops, Ferrothorn, Turtonator and Guzzlord; Argenta's are Skarmory, Annihilape, Dubwool, Diancie, Meowscarada and Pheromosa. Cyrus 1 brings Swampert, Honchkrow, Porygon-Z, Electivire, Magmortar and Salamence. Phobos and Deimos 2 bring Granbull, Houndoom, Mawile, Feraligatr, Arcanine, Galvantula, Absol, Masquerain, Arbok and Froslass, and Mars 2 Liepard, Crobat, Incineroar, Galarian Zapdos, Mesprit and Purugly. All three options are on none of these teams.

Left out: Forretress has hazards and Thunder Wave but no Electric hit, and is four times weak to Fire, which every box carries. Probopass has Thunderbolt and Thunder Wave, but is four times weak to Ground and Fighting and moves at 40 base Speed. Klefki and Heatran are the old team's, which Ian replaced. Durant is not in Oxide. Magearna, Jirachi and Registeel, weighed by their stats as Ian ruled on 2026-11-01, would be a fifth member of 570 or more, and none answers the Water walls better than Magnezone or Vikavolt.

### The options on the cheap checks

Each option was swapped into Ian's six in memory and checked on the same three boxes: each member's best hit on each likely answer and the answer's best hit back, from the scorer's own calculator rows with Byron's items and the player's left out; who the replacement rule sends in, actually run on a battle built by `perfectline.make_battle`; and the matchup screen. A meeting is "beats" when the member two-hits the answer and takes under half back, or one-hits it moving first; "trades" when both sides take half or more.

| Slot 2 | Speed | Outspeeds, box 1, 2, 3 | Sent in against | Beats, trades, loses | Screen best, box 1, 2, 3 |
|---|---:|---|---|---|---|
| Galvantula (Ian's) | 143 | 81 of 85, 90 of 94, 88 of 89 | 10, 11, 10 | 6/4/0, 6/5/0, 5/5/0 | 16.75, 17.2, 15.5 |
| Vikavolt | 64 | 19, 23, 25 | 10, 11, 10 | 8/2/0, 9/2/0, 9/1/0 | 15.1, 15.4, 13.0 |
| Magnezone | 82 | 36, 44, 48 | 8, 8, 8 | 7/1/0, 6/2/0, 8/0/0 | 15.4, 15.7, 13.0 |
| Togedemaru | 118 | 72, 73, 83 | 8, 8, 8 | 5/3/0, 4/4/0, 5/3/0 | 17.65, 17.35, 16.1 |

Lower on the screen means the player's best six wins its one-on-ones by less. No screen figure turns into a percent won, and the screen counts no Sticky Web and no paralysis.

The counterpiece sixes' members that the slot meets, its hit and the hit back at the lowest roll:

| Answer (box) | Galvantula | Vikavolt | Magnezone | Togedemaru |
|---|---|---|---|---|
| Manaphy (all) | Thunder 71, back 38 | Thunderbolt 89, back 30 | Thunderbolt 82, back 45 | Zing Zap 62, back 50 |
| Corviknight (1) | Thunder 82, back 68 | Thunderbolt 104, back 42 | Thunderbolt 96, back 25 | Zing Zap 59, back 35 |
| Quagsire (1) | Energy Ball 98, back 56 | Energy Ball 149, back 29 | not sent; Tri Attack 30 | not sent |
| Luxray (1) | Bug Buzz 82, back 68 | Bug Buzz 125, back 42 | not sent; Tri Attack 34 | not sent |
| Empoleon (3) | Thunder 76, back 63 | Thunderbolt 98, back 40 | Thunderbolt 90, back 34 | Zing Zap 72, back 47 |

Vikavolt takes Galvantula's place in all but one or two rows of the replacement rule a box, and wins each meeting by more: its Special Attack (145 against 97) and its bulk (77, 90, 75 against 70, 60, 60) outweigh the Speed it gives up, and Levitate turns Quagsire's and Whiscash's Earthquake, 51 to 66 percent into Galvantula, into nothing. The cost is Speed: it moves after Manaphy, Luxray and every Fire type, so it takes a hit before it lays Sticky Web, where Galvantula laid it first.

Magnezone is the strongest pure Electric answer (Corviknight hits it for 25 percent back), and Levitate makes it immune to the Ground moves that hit Galvantula and Metagross for double. It has no Grass or Bug move in its legal palette, so the rule sends Empoleon or Metagross into Quagsire and Hisuian Goodra into Luxray, where Galvantula went before. Thunder Wave is in its four for Speed control; it paralyses one target, where the Web slows every switch-in. Magnezone is also on Cyrus 2's team at Galactic HQ, and on three Workers in Byron's own split; Cyrus 1's answer 4 allowed a species that a later fight uses.

Togedemaru keeps the slot fast and adds Electroweb and Nuzzle, but its one strong hit is Zing Zap, an Electric move, so it has nothing for Quagsire or Luxray and trades with Manaphy where Galvantula beat it. It reads the easiest of the four on the screen.

Speed neighbours, within three points, on each box:

| Slot 2 | Speed | Neighbours |
|---|---:|---|
| Galvantula | 143 | Talonflame (box 1), Greninja and Weavile (box 2) |
| Vikavolt | 64 | Carbink, Lickilicky, Lombre, Donphan, Hippowdon, Hariyama, Octillery |
| Magnezone | 82 | Corviknight, Gothitelle, Nidorino |
| Togedemaru | 118 | Manaphy, Tentacruel, Alolan Ninetales |

Togedemaru's Adamant ties Manaphy at 118; Hasty, freed by Galvantula, would put it at 129.

### The sets

Each set is legal at 51 on both checkers (the OxiDex's lists and the Kaizo checker), the trainer lint finds nothing in a file with it in place, and none repeats an item or a nature of the other five. Occa Berry is Galvantula's own, and every option is weak to Fire.

| Pick | Ability | Item | Nature | Moves |
|---|---|---|---|---|
| Vikavolt | Levitate | Occa Berry | Modest | Sticky Web, Thunderbolt, Energy Ball, Bug Buzz |
| Magnezone | Levitate | Occa Berry | Modest | Thunderbolt, Flash Cannon, Thunder Wave, Tri Attack |
| Togedemaru | Sturdy (hidden) | Occa Berry | Adamant | Nuzzle, Zing Zap, Fake Out, Electroweb |

### What this branch holds and what was checked

Ian's draft is saved into `res/trainers/data/leader_byron.json` through the OxiDex's own save, `tools.oxide.encounters.trainers.save`, which lints the file and records the change in the divergence registry. The file matches his snapshot field for field.

Four of his moves were off-list, and each now sits on its line's first stage's egg list by the egg-list rule (Ian, 2026-10-29), in `learnrewrite.IAN_EGG_MOVES` and in the species files. Kartana takes Smart Strike, which no Oxide list gives it, and Swords Dance, its level 65 move. Piplup takes Flip Turn, which Empoleon learns at 56; Piplup's list is set by hand, so its line in `learnsets_by_hand.txt` says so too. Celesteela takes Air Slash, on no Oxide list for it. Kartana and Celesteela are first stages of their own. The player never reaches an egg list.

The rules: every member holds its own item and has its own nature, with no repeats, and Celesteela, the ace, is at the cap of 53.

Checked on this branch:

| Check | Result |
|---|---|
| The OxiDex's lists, every move at its level | 0 off-list; four before the egg lists (Smart Strike, Swords Dance, Flip Turn, Air Slash) |
| The Kaizo study's checker at 53, with the TMs from before the TM pass | 0 problems; the same four before |
| The trainer lint | nothing found |
| The real packer | packs the file |
| test_b1 | 50 of 50 |
| test_learnrewrite, test_learncheck | 6 of 6, 18 of 18 |
| test_trainers | 44 of 44 |
| `make rom` | builds |
| The gate, `integrate.sh --verify-only` | 53 checks pass with no warning; sync-docs fails, since it refuses to mirror from any branch but `oxide`, by design |

### How the numbers were made

The cheap checks ran in this branch's worktree, on the tree of `origin/oxide` at 9447ef458, with the redesign helper's `shape.py` and its likely answers (`walls.json`, from the run `byron-redesign-study`, seeds 1 to 3 at 53), copied to the job folder `/home/ian/.claude/jobs/382760ce/tmp/byron-ian/` with this page's parties in `shapes.py`; `digest.py` reads their output. None writes to `res/`. Legality comes from the OxiDex's `learnsets.lists` and the Kaizo checker (`oxide.py check 53`, with `OXIDE_OLD_RES` set to an export of `res/` from before the TM pass).

The counterpiece check ran as `ian-final` did: `plcounter read` against the reading `byron-0db1aeaee`, one trial at the reading's dice, target 88, in a tree made by `plcounter tree` from `tree-counter-base-0744cd243` with the Vikavolt file in place (`~/oxide-trials/goal3/tree-counter-byron-ian-vikavolt`). The three boxes ran as three jobs of five processes each, under `tools/oxide/capped`, so they finished sooner; each box's result is in `~/oxide-trials/goal3/counterpiece/byron-0db1aeaee-ian-vikavolt-box<n>.json`.
