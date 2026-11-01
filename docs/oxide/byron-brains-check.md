# Byron, Thorton and Argenta: a short check

Ian built three boss drafts in the OxiDex on 2026-10-31: Byron, who closes his split at Canalave Gym (cap 53), and two optional Frontier Brains in Barry 5's stretch (cap 50), Thorton the Factory Head at Fuego Ironworks and Argenta the Hall Matron at Pal Park. He asked for the check Maylene's six had: anything that invalidates a fight, and the weakest crux in each with the top replacement picks for it. His natures are his choice; none repeats inside a team. The teams are on branch `overseer-boss-checks` (Byron's from `overseer-byron-leader`, the Brains' from `overseer-brains-seed`), and no team changed. The only change to the game's data is the egg-list commit below. Every number comes from cheap checks; no scorer reading was run.

## Ian's answers (2026-10-31)

Byron's Klefki keeps the lead and holds Leftovers in place of the Light Clay (questions 1 and 2), and his difficulty stays as it is (question 3). Thorton's six all drop to 47 (question 4). His Turtonator takes Shell Trap for Shell Smash and Will-O-Wisp for Heat Crash (question 5), his Ferrothorn takes Power Whip for Grassy Glide (question 10), and his flags drop Setup First Turn, Risky and Prioritize Extremes, keeping Check HP and Harassment (question 6). Argenta's flags drop Setup First Turn and Risky and keep Prioritize Extremes (question 7), and she keeps Diancie and stays at 50 (questions 8 and 9). The Rocky Helmet fix landed on `oxide` at 3d070be1a (question 11), and this branch has merged it. The sections after this one are the check's, from before these answers.

The edits went through `trainers.save`, in commit 07d323fbdd3. No item and no nature repeats in any of the three teams. Power Whip is on no Ferrothorn list at 47, so it went on Ferroseed's egg list; Grassy Glide, which this pass had put there and no trainer now uses, came off. Every other move of the three teams is on its species' list at its new level: Shell Trap on Turtonator's egg list since Barry 4, Will-O-Wisp by its TM. Both checkers then find nothing, the trainer lint finds nothing, test_learnrewrite passes 6 of 6, test_learncheck 18 of 18, test_trainers 44 of 44 and test_b1 48 of 48, and `make rom` builds.

The probe was run again on the teams as they now stand, with the helmet in the simulator and Thorton's room held on as before. Each cell is the player's wins in 150 rough fights against the best six and then the most-taken six; one number means the two were the same six.

| Fight, on which boxes | Box 1 | Box 2 | Box 3 | Before the answers |
|---|---|---|---|---|
| Wake, on Wake's boxes (44) | 95, 67 | 28, 66 | 55, 67 | the same |
| Barry 4, on his own boxes (42) | 52, 80 | 71, 45 | 59 | the same |
| Byron, on Byron's boxes (53) | 69, 81 | 67, 81 | 41, 86 | 69, 90; 69, 78; 49, 91 |
| Thorton at 47, on Barry 5's boxes (50) | 44, 42 | 28, 44 | 118, 73 | 9; 4, 3; 39, 22 |
| Thorton at 47, on Cyrus 1's boxes (47) | 1, 2 | 3, 3 | 3, 0 | not run |
| Thorton at 47, on Byron's boxes (53) | 87 | 82, 85 | 142, 90 | 40, 76; 49, 32; 44 |
| Argenta, on Barry 5's boxes (50) | 14, 60 | 46, 63 | 35, 58 | 17, 51; 50, 59; 33, 51 |
| Argenta, on Byron's boxes (53) | 79 | 89, 86 | 83 | 95; 83, 84; 81 |

Byron and Argenta read as before, within the probe's spread. Thorton in Barry 5's stretch now reads about as hard as Wake and Barry 4 do on their own boxes, and on Byron's boxes he is easier than Byron. The one thing to see is the row for Cyrus 1's boxes. His fight first opens at Cyrus 1, and a player who walks in then, with a box at 47 and fewer catches, is beaten nearly every time. That is the shape Dahlia has in Maylene's split, and an optional fight may have it, but it is said here so that it is a choice.

What the answers changed in play, on Barry 5's boxes:

- Shell Trap struck in 14 to 74 of its 90 to 143 uses a six, since it fails unless a physical move hits Turtonator first. The screen counts it as a sure hit, so the lead test below reads it kindly. Will-O-Wisp burned 23 to 63 times a six.
- Ferrothorn used Power Whip 359 to 584 times a six. Its Self-Destruct now goes almost only at 30 percent HP or less (13 to 37 times a six, with 0 to 5 from 31 to 70 percent and one above 70 in all), as the guide expects of Check HP alone.
- Guzzlord's Protect fell from 125 to 533 picks a six to 190 to 272, with Dragon Tail its most-picked move.
- The Rocky Helmet took its sixth on 77 to 299 contact hits a six. The player's attacker fainted during its own contact move into Toxapex 5 to 31 times a six, the helmet's chip among the causes.
- Toxapex's lead now passes Ian's test against Corviknight, Torterra, Bronzong and Empoleon, which draw a Turtonator that beats them. Bastiodon, in 19 or 20 of the top 20 sixes, still beats the Turtonator it draws (+1.5), and Hariyama does the same to Bronzong on box 3.

## Summary

### Byron

**Outcome.** Nothing breaks the fight. His levels are Mars 1's shape exactly: Celesteela at the cap of 53, Dhelmise at 52, Klefki and Bastiodon at 51, Heatran and Metagross at 50. One item does nothing: Klefki holds a Light Clay and knows no screen. Four moves were off-list and are now on egg lists. The Power Herb works as meant: Meteor Beam fires at once in 68 to 140 fights of 150. The rest of Celesteela's combination is used less than it reads. The AI picks Autotomize only 1 to 37 times per 150 fights, because Expert takes 3 from it whenever Celesteela is already the faster, which it is against most of the box. And Acrobatics often comes while the herb is still held, at half power: 0 to 134 times a six, against 13 to 47 at full power. The Iron Ball does what Ian meant: Dhelmise's Speed falls from 55 to 27, Gyro Ball's power runs at a median of 71 to 148 by box, and Payback doubles. The AI still picks Power Whip about two turns in three. His flags match the guide: with Check HP, Metagross explodes at 30 percent HP or less in all but a handful of fights. On these checks Byron reads a little easier than Wake does on Wake's own boxes.

**The weakest crux is Klefki's slot.** It knocks out 4 to 62 of the player's Pokemon per 150 fights, against 52 to 223 for the other five. Its answers mostly draw a member that beats them, but none of those members has a setup move. Adding Reflect, so that the Light Clay works, changes almost nothing on the probe. Magnezone in the slot knocks out 68 to 131 and makes the fight a little harder.

### Thorton

**Outcome.** Nothing breaks the fight, but two pieces are dead and his level reads high. Shell Smash is never used: under the permanent room the AI's Basic routine scores it 10 lower, in the engine and in the simulator alike, and its +2 Speed would put Turtonator last anyway. Grassy Glide has no priority, since Oxide has no terrain; it is a plain 55-power Grass hit. The Rocky Helmet is not in the simulator, so the checks read him a little easier than he is. Three of his flags do nothing or work against the guide (decision 6). At 50 he is far harder than his stretch's other bosses: the probe's player beats him 3 to 39 times in 150, against 28 to 95 for Wake and 45 to 80 for Barry 4, each on its own boxes. On Byron's boxes, at 53, he still reads harder than Byron. That is Dahlia's shape (too hard in her own split, fair in the next), only heavier. The room alone is worth about 20 to 60 wins of 150 to him.

**The weakest crux is Toxapex's lead, through Turtonator.** Toxapex knocks out the fewest (27 to 83), and it fails Ian's lead test. Its common answers are Torterra, Corviknight, Bastiodon and Bronzong, in 19 or 20 of the screen's top 20 sixes. Every one of them draws Turtonator, which loses to every one. Its Heat Crash is a 40-power move into those heavy answers, and its setup move is dead. With Flamethrower in place of Shell Smash, the answers draw a Turtonator that beats all of them but Bastiodon.

### Argenta

**Outcome.** Nothing breaks the fight. Four moves were off-list and are now on egg lists. Two of her flags do nothing or have no idea to serve (decision 7). Rage Fist is a plain 50-power hit in Oxide, since its rise is not ported. The Focus Sash on her lead, with no trade, is the case Ian kept on Darach's lead; it fired in one six of twelve. Her lead passes Ian's test on every box: Skarmory's answers draw Annihilape or Meowscarada, which beat them. On Barry 5's boxes she reads harder than Wake and Barry 4 on theirs (the player wins 17 to 59 times in 150), and on Byron's boxes she reads easier than Byron (81 to 95). That is Dahlia's shape, which suits an optional fight with a big reward, so I see no reason to shift her level.

**The weakest crux is Diancie's slot.** It knocks out the fewest of her five non-leads (60 to 125 on her boxes, 81 to 120 on Byron's). The Steel walls the screen takes most (Bastiodon in every six, Probopass and Bronzong in many) resist both its attacks. Earth Power in Diamond Storm's place does not help (52 to 88). Whiscash, from Ian's first list for her, knocks out 93 to 178 and makes her far harder, so I would keep Diancie.

### What Ian decides

1. Byron's lead: Magnezone (my pick), Klefki with Reflect for Foul Play, or keep Klefki?
2. If Klefki stays, its Light Clay does nothing without a screen: add Reflect, or change the item?
3. Byron reads a little easier than Wake on these checks. Is that right for the closing boss of the split?
4. Thorton's level: Mars 1's shape (Guzzlord 50, Turtonator 49, Toxapex and Bronzong 48, Dusclops and Ferrothorn 47; my pick), all six at 47, or keep all at 50?
5. Thorton's Turtonator: Flamethrower for Shell Smash (my pick), Shell Trap, or keep Shell Smash, which the AI never uses under the room?
6. Thorton's flags: drop Setup First Turn (it does nothing), Risky (it spends Self-Destruct freely) and Prioritize Extremes (Guzzlord's Protect), keeping Check HP and Harassment?
7. Argenta's flags: drop Setup First Turn (it does nothing) and Risky (she has no critical-hit idea), and keep Prioritize Extremes, the one flag that pushes her lead's hazards?
8. Argenta's Diancie slot: keep Diancie (my pick), or Whiscash, which makes her far harder?
9. Argenta's level: keep all six at 50 (my read)?
10. Ferrothorn's Grassy Glide has no priority in Oxide: keep it, or swap it?
11. Approve a simulator fix for the Rocky Helmet, so that a reading of Thorton sees it?

**Next steps.** Ian answers in a line each, which takes about 15 minutes. A session then applies his choices on this branch and reruns the legality checks and the probes, which takes about an hour. A level shift for Thorton below 50 puts Turtonator's Heat Crash, its level 50 move, on its egg list. A Rocky Helmet fix, if approved, is about an hour with a test that fails before it, landing through the Overseer. Thorton still needs his entry on the engine's permanent Trick Room list, which is the placement job in the tracker's Frontier Brains entry. A spot-check reading happens only if Ian names one, and takes two and a half to four hours.

## How the three read against the other bosses

Each cell is the player's wins in 150 rough fights against the screen's best six, then against the six it takes most; one number means the two were the same six. The player is the greedy probe player of the Maylene and Wake checks, who never switches, never sets up and has no items, so only the comparison between rows means anything. The screen's score is its best six's; a lower score means the player's best six answers the trainer less well. Wake's and Barry 4's rows come from this study's scripts and match the Wake check's own numbers exactly.

| Fight, on which boxes | Box 1 | Box 2 | Box 3 | Screen's best score, by box |
|---|---|---|---|---|
| Wake, on Wake's boxes (44) | 95, 67 | 28, 66 | 55, 67 | 16.30, 14.85, 14.15 |
| Barry 4, on his own boxes (42) | 52, 80 | 71, 45 | 59 | 12.90, 16.70, 16.35 |
| Barry 5 as he stands (51 to 53, not yet rebuilt), on Barry 5's boxes (50) | 5, 16 | 32, 44 | 7, 8 | 8.85, 9.80, 9.70 |
| Thorton, on Barry 5's boxes | 9 | 4, 3 | 39, 22 | 19.80, 19.80, 19.40 |
| Argenta, on Barry 5's boxes | 17, 51 | 50, 59 | 33, 51 | 18.10, 17.50, 18.50 |
| Byron, on Byron's boxes (53) | 69, 90 | 69, 78 | 49, 91 | 18.15, 18.60, 19.75 |
| Thorton, on Byron's boxes | 40, 76 | 49, 32 | 44 | 21.00, 21.90, 21.00 |
| Argenta, on Byron's boxes | 95 | 83, 84 | 81 | 21.70, 19.80, 20.05 |

Barry 5's boxes stand at his honour cap of 50 (below). His own row is today's team, at 51 to 53 with a Life Orb, so it is a ceiling, not a target. Thorton's and Argenta's screen scores run high because the screen sees no status move and no hazard: it misses Toxic Spikes, Baneful Bunker, Confuse Ray, Mean Look, Swagger and Spikes, and it reads Thorton's room only through the Speeds.

Ian's other two Brains, from their checks of 2026-10-31. Dahlia, on Maylene's boxes, was beaten 5 to 18 times in 150 against Maylene's 87 to 131, and on Wake's boxes she read about as hard as Wake. Darach and Caitlin read at about Wake's level in Wake's own split, on proxies for a double, and Ian kept them there. So Argenta has Dahlia's shape, and Thorton has it more strongly: harder in his own stretch than any boss of it but today's unbuilt Barry 5, and still harder than Byron after it.

## Byron

### What could invalidate the fight

Legality. Two checkers read the file: the OxiDex's own lists, which read only today's TMs, and the Kaizo study's checker at 53, which counts the TMs from before the TM pass. Four moves failed the first, and two of them the second too. Each is now on its line's first stage's egg list (the egg-list commit below).

| Member | Move | Where Oxide had it | Egg list |
|---|---|---|---|
| Bastiodon 51 | Roar | a TM before the TM pass | Shieldon |
| Dhelmise 52 | Power Whip | nowhere | Dhelmise's own |
| Metagross 50 | Explosion | a TM before the TM pass | Beldum |
| Celesteela 53 | Acrobatics | nowhere | Celesteela's own |

The rest passes. No item repeats and no nature repeats. Every member is a final stage. No move is a one-hit KO, an evasion move or a trap; Anchor Shot traps for as long as Dhelmise stays in, which the ruling allows now and then. Explosion is the team's one trade, which Byron's split allows. Bastiodon's Focus Sash sits off the lead, on a member with no trade. Ian kept a Sash on Darach's lead with no trade, so I read this as fine; it fired in 0 to 8 fights of 150.

Klefki's Light Clay. It lengthens Reflect and Light Screen from five turns to eight, and Klefki knows neither, so the item does nothing. That is decision 2.

Celesteela's Power Herb, Autotomize and Acrobatics. Read together, the set means Autotomize for Speed, then Meteor Beam at once with the herb for +1 Sp. Atk, then Acrobatics at 110 power once the herb is gone. In the engine each part works: the herb skips the charge and raises Sp. Atk, Acrobatics doubles with no item held, and the AI's Expert gives Meteor Beam +2 while the herb is held and Acrobatics +1 once it is gone. In play the order rarely comes together.

| Per 150 fights, by six | Range |
|---|---|
| Fights where the herb was spent on an instant Meteor Beam | 68 to 140 |
| Meteor Beams with no herb, which charge for a turn first | 46 to 141 |
| Acrobatics with the herb still held (55 power) | 0 to 134 |
| Acrobatics with no item (110 power) | 13 to 47 |
| Autotomize | 1 to 37 |

Autotomize is rare because Expert takes 3 from a Speed raise when its user is already the faster, and Celesteela's 86 outspeeds most of the box's common catches (Corviknight 83, Whiscash 76 and the slow walls). It gains 3, at 72.7 percent, only against faster ones such as Manaphy (118), Luxray and Pachirisu (113), and Check HP also discourages it below 70 percent HP. Its weight change matters to nothing here: at 900 kg Celesteela still takes full Low Kick and Grass Knot. Acrobatics at half power is often a fair pick, since against a Grass type a 55-power Flying move still beats Flash Cannon. None of this breaks the fight, and Celesteela is the team's ace by the probe (158 to 223 knockouts).

Dhelmise's Iron Ball with Gyro Ball. The Iron Ball halves Dhelmise's Speed from 55 to 27, in the engine and in the simulator, and Gyro Ball's power is 1 plus 25 times the target's Speed over the user's, at most 150. Steelworker raises it by half. So its power runs high against fast foes:

| Box | Gyro Ball's power at its uses (median, range) |
|---|---|
| 1 | 132 (101 to 150) and 149 (105 to 150) |
| 2 | 71 (53 to 115) and 71 (17 to 150) |
| 3 | 71 (44 to 150) and 86 (71 to 105) |

Moving last also doubles Payback. The AI picks Power Whip in about two turns in three (190 to 264 picks a six, against 6 to 57 for Gyro Ball), because Power Whip is Dhelmise's strongest move into most of the box's Water and Ground catches. The combination works; it just has a stronger move beside it.

The AI flags. Byron runs Basic, Evaluate Attack, Expert and Check HP. Check HP is the guide's flag for a team whose idea uses Explosion, and Metagross explodes as the guide predicts: at 30 percent HP or less in 3 to 46 fights a six, from 31 to 70 percent in 0 to 6, and above 70 percent at most once. No Risky, which the guide keeps off a trade team. Klefki's Thunder Wave and Spikes and Heatran's Will-O-Wisp are three of Harassment's table moves, but the team's idea is Steel, not status, so the guide does not call for it.

### The fight against the boxes

The player's Pokemon knocked out while each member was in, per six of 150 fights, over the six sixes on Byron's boxes:

| Klefki | Heatran | Bastiodon | Dhelmise | Metagross | Celesteela |
|---|---|---|---|---|---|
| 4 to 62 | 154 to 198 | 52 to 133 | 104 to 154 | 88 to 188 | 158 to 223 |

Speeds at no stage: Heatran 97, Metagross 90, Klefki 87, Celesteela 86 (172 after an Autotomize), Bastiodon 45, Dhelmise 27. The fastest common catches are Manaphy 118, Luxray and Pachirisu 113, and Magmar 111.

### The weakest crux: Klefki's slot

Klefki opens with Spikes in about half its first turns and Thunder Wave in a fifth to two fifths, and lays Spikes 192 to 316 times a six. Its paralysis landed 42 to 81 times. The probe's player never switches, so Spikes bite only the Pokemon sent in after a knockout or a Roar, and the probe undercounts the lead for that. Even so, it knocks out the fewest by far.

The lead test. Each common answer to Klefki draws in a member, and on boxes 1 and 3 that member beats the answer almost every time. Box 2 is the exception: its Ground and fast catches beat what they draw, though narrowly.

| Box | Klefki's answers (margin on Klefki) | Drawn in | That member on them |
|---|---|---|---|
| 1 | Corviknight (+3.0), Luxray, Metagross, Pachirisu, Torterra | Heatran | beats each (-0.5 to -3.5 on it) |
| 1 | Manaphy (+1.5), Whiscash, Quagsire | Dhelmise | beats each (-1.5 to -2.5) |
| 1 | Magmar (+2.5) | Bastiodon | beats it (-1.5) |
| 2 | Wailord (+1.5), Manaphy | Dhelmise | beats each (-2.5) |
| 2 | Hippowdon, Donphan (+3.0) | Dhelmise | loses to each (+0.5) |
| 2 | Staraptor (+1.5), Cinderace (+2.5) | Bastiodon | loses to each (+0.5) |
| 2 | Empoleon (+3.0), Bronzong | Heatran | beats each (-0.5, -3.5) |
| 3 | Corviknight, Empoleon, Pachirisu, Metagross | Heatran | beats each (-0.5 to -3.5) |
| 3 | Rotom (+0.5) | Dhelmise | beats it (-0.5) |
| 3 | Hippowdon (+3.0) | Dhelmise | loses (+0.5) |

None of the drawn members carries a setup move, so the lead meets the test's first half and not its second. The team's only setup sits on Celesteela, which the rule draws in only against a few catches: Cinderace, Rapidash, Araquanid and Magmar after Bastiodon leaves, and Torterra after Heatran.

### The picks

Each pick keeps the other five as Ian built them, swapped into the slot in memory, and ran through the screen, the replacement trace and the probe on the same three boxes.

| Set | Legal at 51 | Lead's knockouts per 150 | Greedy wins, box 1 | Box 2 | Box 3 |
|---|---|---|---|---|---|
| Ian's: Klefki, Light Clay, Relaxed, Prankster; Thunder Wave, Play Rough, Foul Play, Spikes | yes, after the egg lists | 4 to 62 | 69, 90 | 69, 78 | 49, 91 |
| 1. Magnezone, Light Clay, Calm, Levitate; Thunder Wave, Light Screen, Thunderbolt, Flash Cannon | yes | 68 to 131 | 80, 43 | 63, 83 | 47, 48 |
| 2. Klefki with Reflect for Foul Play | yes (its TM) | 5 to 41 | 83 | 66, 74 | 57, 100 |
| 3. Klefki with Reflect and Light Screen for Foul Play and Play Rough | yes | 0 to 2 | 67 | 69, 81 | 53, 104 |

Magnezone is my first pick. It gives the Light Clay a screen, keeps the lead's paralysis, and hits: Thunderbolt took HP 136 to 142 times a six. Its answers draw a member that beats them on every box but two (Cinderace on box 2 and Milotic on box 3, each by +0.5), and on box 2 Heracross draws Celesteela, which carries setup. It makes the fight harder on four sixes of six, the most on box 1's and box 3's most-taken sixes, which matters if Ian wants Byron above Wake (decision 3). The price is Klefki's Spikes; Bastiodon's Stealth Rock and Roar stay. Levitate rather than Magnet Pull, which would trap the box's Steel answers.

Pick 2 is the smallest change: one move, so that the item works. Klefki used Reflect 83 to 126 times a six, and the fight moved both ways by up to 14 wins, which is no clear change. Pick 3, a pure screen lead, reads the same.

## Thorton

### What could invalidate the fight

Legality. Three moves failed both checkers at 50 and are now on egg lists: Ferrothorn's Grassy Glide on Ferroseed's, and Guzzlord's Protect and Body Press on its own, a new list. Protect stays off every list the player can use. The rest passes. No item repeats and no nature repeats. Dusclops is a middle stage holding an Eviolite, which works since it still evolves. Self-Destruct is the one trade. Dusclops's Mean Look is a trap, which the trainer rules allow now and then, and a Brain is an optional boss.

The permanent room. His trainer is not yet on the engine's list (`sPermanentTrickRoomTrainers`); that is the placement job. The engine opens a listed trainer's fight in a Trick Room that never counts down, by the same subscript as the Battle Arcade's, and the move Trick Room fails under it. The simulator reads the same list, so every number here comes from a harness that adds Thorton to it in memory. The matchup screen, which reads Speeds and not a battle, was given every Speed turned over, so that the slower counts as moving first.

| Member | Speed | Under the room |
|---|---|---|
| Bronzong (Iron Ball) | 23 | first against everything the box takes |
| Ferrothorn | 36 | first against everything the box takes |
| Dusclops | 45 | after Bastiodon (42), tied with Bronzong (45) |
| Toxapex | 55 | after the slow walls, which run 42 to 52 |
| Turtonator | 56 | after the slow walls |
| Guzzlord | 63 | after the slow walls and the middling catches |

Shell Smash is dead. The AI's `Basic_CheckShellSmash` takes 10 from it whenever the Trick Room mask is set, and the permanent room sets the same timer bits as the move does. The simulator mirrors it, and Turtonator picked Shell Smash in no fight at all. Its +2 Speed would also put Turtonator last under the room. That is decision 5.

Grassy Glide. Oxide has no terrain, so Grassy Glide is a plain 55-power Grass hit with no priority (the move-pool survey lists it so). Ferrothorn used it 164 to 374 times a six. That is decision 10.

Turtonator's Heat Crash. Its power is set by the two weights: 40 against a target more than half Turtonator's 212 kg, rising to 120 against a light one. Toxapex's common answers are heavy (Torterra 310 kg, Bronzong 187, Bastiodon 150), so Heat Crash hits them at 40, and at 60 against Corviknight.

The Rocky Helmet, a gap. The simulator does not model it. In the engine every contact hit on Toxapex costs the attacker a sixth of its maximum HP, and the trainer AI does not see the item either. The probe counted the contact hits it left out:

| Six | Contact hits on Toxapex per 150 fights | Hits after which the helmet would have knocked the attacker out |
|---|---|---|
| Box 1, best six | 209 | 3 |
| Box 2, best six | 93 | 4 |
| Box 2, most-taken six | 13 | 1 |
| Box 3, best six | 470 | 22 |
| Box 3, most-taken six | 366 | 46 |

So on box 3 the player's contact attackers lose about half of one Pokemon's HP a fight to the helmet in the game, and none in the checks. Every Thorton number here reads him a little easier than he is, most on box 3. Ferrothorn's Iron Barbs and Toxapex's Baneful Bunker are modelled. A fix is decision 11.

The AI flags. Thorton runs Basic, Evaluate Attack, Expert, Setup First Turn, Risky, Prioritize Extremes, Check HP and Harassment. Against the guide:

| Flag | What it does here | The guide |
|---|---|---|
| Check HP | holds Self-Destruct for low HP | right: his team has a trade move |
| Harassment | pushes Toxic Spikes and Confuse Ray | right: two of its table's status moves |
| Setup First Turn | nothing: it acts on the battle's first turn only, and Toxapex's Toxic Spikes and Baneful Bunker are not in its table | does nothing |
| Risky | pushes Self-Destruct, both Gyro Balls and Confuse Ray | kept off a team with a trade move unless it should spend it freely |
| Prioritize Extremes | pushes every status move, Self-Destruct among them | the guide prefers the flag for the push a team wants, which Harassment already is |

With all three on, Ferrothorn's Self-Destruct is spent freely. It went off 67 to 126 times per 150 fights on Barry 5's boxes: above 70 percent HP 11 to 30 times, from 31 to 70 percent 25 to 62, and at 30 percent or less 28 to 50. With Check HP alone, the guide expects nearly all of them at 30 percent or less. Prioritize Extremes also has Guzzlord pick Protect 125 to 533 times a six, its most-picked move by far. That is decision 6.

### The fight against the boxes

Knockouts while each member was in, per six of 150 fights, on Barry 5's boxes:

| Toxapex | Bronzong | Dusclops | Ferrothorn | Turtonator | Guzzlord |
|---|---|---|---|---|---|
| 27 to 83 | 143 to 241 | 54 to 228 | 166 to 315 | 139 to 197 | 42 to 155 |

The room's worth, for contrast only: with Thorton taken off the list, the player's wins on Barry 5's boxes rise from 9; 4, 3; and 39, 22 to 29, 41; 34, 44; and 58, 81. The screen takes different sixes with the room off, so the pairs do not match six for six.

### The level

All six stand at the cap of 50, so he has no ace above the rest. Two shifts were tried, each swapped in memory:

| Levels | Greedy wins, box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Ian's, all at 50 | 9 | 4, 3 | 39, 22 |
| Mars 1's shape: Guzzlord 50, Turtonator 49, Toxapex and Bronzong 48, Dusclops and Ferrothorn 47 | 39, 29 | 54, 29 | 37 |
| All at 47, Cyrus 1's honour cap, where his fight first opens | 53, 69 | 75, 27 | 42, 65 |
| Mars 1's shape with the Flamethrower Turtonator | 23, 27 | 40, 24 | 43, 25 |

Ian levelled Thorton for his own stretch, and at 50 he reads like a fight from a later one. Mars 1's shape puts him between Barry 4 and today's Barry 5, which I read as hard but fair for an optional Brain with a prize. All at 47 puts him at about Wake's and Barry 4's level. Below 50, Turtonator's Heat Crash, its level 50 move, goes on its egg list; every other move stays legal at those levels. Lower levels also mean lower Speeds, which helps him under the room, so the shift costs him less than the levels suggest.

### The weakest crux: Toxapex's lead, through Turtonator

Toxapex opens with Toxic Spikes in about 105 of 150 fights and Baneful Bunker in the rest, and after that picks Baneful Bunker about as often as Toxic Spikes. It knocks out the fewest. Its four common answers are Steel types it cannot touch (Poison Jab does nothing to Steel) and Torterra's Headlong Rush (98 to 116 percent). Each draws Turtonator, and Turtonator loses to each:

| Box | Toxapex's answer (margin on it) | Turtonator on that answer |
|---|---|---|
| 1 | Torterra (+2.5), Corviknight (+3.0), Bastiodon (+3.0) | loses (+1.5, +2.5, +0.5) |
| 2 | Bronzong (+3.0), Bastiodon (+3.0) | loses (+3.0, +0.5) |
| 2 | Gastrodon (+3.0) | draws Ferrothorn, which beats it (-3.5) |
| 3 | Bastiodon, Corviknight, Bronzong (+3.0 each) | loses (+0.5, +2.5, +3.0) |

Turtonator's only hits on them are Dragon Pulse (18 to 55 percent), Earthquake (nothing on Corviknight and Bronzong) and a 40-power Heat Crash, and its one setup move is dead. So the lead fails the test, and the fault is in the member it draws.

### The picks

| Set | Legal at 50 | Turtonator's knockouts per 150 | Greedy wins, box 1 | Box 2 | Box 3 |
|---|---|---|---|---|---|
| Ian's: Dragon Pulse, Shell Smash, Earthquake, Heat Crash | yes | 139 to 197 | 9 | 4, 3 | 39, 22 |
| 1. Flamethrower for Shell Smash | yes (its level 38) | 129 to 223 | 3, 3 | 2, 4 | 7, 19 |
| 2. Shell Trap for Shell Smash | yes (its egg list since Barry 4) | 125 to 184 | 5, 19 | 5, 6 | 6, 25 |

With Flamethrower, Torterra, Corviknight and Bronzong draw a Turtonator that beats them (-0.5 to -1.5 on it), on every box; Bastiodon still beats it (+0.5). Flamethrower took HP 103 to 195 times a six. It makes the fight harder at 50, which is why I pair it with Mars 1's shape in decisions 4 and 5. Shell Trap reads close, but it struck in only 61 to 86 of its 100 to 212 uses, since it fails when Turtonator is not hit by a physical move first, and its in-game check (82) is still open. Guzzlord, the other low member (42 to 155), is mostly a Prioritize Extremes problem: its Protect picks fall if decision 6 drops the flag.

## Argenta

### What could invalidate the fight

Legality. Four moves failed both checkers at 50 and are now on egg lists: Annihilape's Acrobatics on Mankey's, Diancie's Moonblast (its level 64 move) and Diamond Storm (its 71) on its own, and Pheromosa's Triple Kick (its 53) on its own; Pheromosa's hand-set line says so too. The rest passes. No item and no nature repeats, every member is a final stage, and the team has no trade, no trap, no one-hit KO and no evasion move.

The pieces. Annihilape's Sitrus Berry was eaten in 105 to 116 fights of 150, and its Acrobatics then struck at 110 power 9 to 38 times a six, against 1 to 13 at 55 power before. Rage Fist is a plain 50-power hit in Oxide: the move-pool survey lists it so, and its rise with each hit taken is not ported. Dubwool's Swagger confused 66 to 109 times a six. Defiant, Fluffy, Protean, Beast Boost, Filter and Clear Body are all modelled. Triple Axel is on two members, Meowscarada and Pheromosa, which is overlap the player sees, not a fault. The Focus Sash on Skarmory, a lead with no trade, is Darach's case, which Ian kept; it fired in one six of twelve, since little knocks Skarmory out from full HP.

The AI flags. Argenta runs Basic, Evaluate Attack, Expert, Setup First Turn, Risky and Prioritize Extremes.

| Flag | What it does here | The guide |
|---|---|---|
| Setup First Turn | nothing: Skarmory's Spikes, Stealth Rock and Toxic are not in its table | does nothing |
| Risky | pushes Dubwool's Swagger and Payback | goes on a team whose idea is critical hits, which hers is not (Flower Trick has its own effect) |
| Prioritize Extremes | pushes Skarmory's hazards and Toxic, Cotton Guard, Swagger, Calm Mind and Rock Polish | the guide prefers a specific flag, but none pushes Stealth Rock and Toxic, so here it does a job nothing else does |
| no Check HP | | right: she has no trade move |

Skarmory opened with Spikes or Stealth Rock in 121 to 143 fights of 150. That is decision 7.

### The fight against the boxes

Knockouts while each member was in, per six of 150 fights:

| Boxes | Skarmory | Annihilape | Dubwool | Diancie | Meowscarada | Pheromosa |
|---|---|---|---|---|---|---|
| Barry 5's (50) | 30 to 88 | 169 to 230 | 68 to 119 | 60 to 125 | 134 to 187 | 188 to 270 |
| Byron's (53) | 17 to 38 | 89 to 135 | 134 to 160 | 81 to 120 | 107 to 164 | 134 to 199 |

Speeds at no stage: Pheromosa 171, Meowscarada 143, Annihilape 110, Dubwool 108, Skarmory 99, Diancie 63 (Quiet; 126 after a Rock Polish). Crobat, at 142, is in all 20 of the screen's top sixes on box 1 and outspeeds all but Pheromosa.

Her lead passes the test. Bastiodon, the answer to Skarmory in every six, and Probopass on box 1, draw Annihilape, which beats them (-2.5 and -4.5); Golem and Rhydon draw Meowscarada (-1.5); Salazzle draws Diancie, which carries Calm Mind and Rock Polish. The one miss is Glimmora on box 2, in 5 of 20 sixes, which beats Diancie narrowly (+1.5).

### The weakest crux: Diancie's slot

Diancie knocks out the fewest of the five non-leads on Byron's boxes in three sixes of four, and on Barry 5's boxes in half of them, where Dubwool is lowest in the rest. Its two attacks are Fairy and Rock, and the boxes' Steel walls resist both: Bastiodon is in every top six, Probopass in 19 of 20 on box 1 and Bronzong in 15 and 7 of 20 on boxes 2 and 3. Diancie is four times weak to Steel. Its answers draw Annihilape, which beats them, so the slot does not fail the lead test; it simply does little.

| Set | Legal at 50 | Slot's knockouts per 150 | Greedy wins, box 1 | Box 2 | Box 3 |
|---|---|---|---|---|---|
| Ian's: Diancie, Leftovers, Quiet, Clear Body; Moonblast, Calm Mind, Diamond Storm, Rock Polish | yes, after the egg lists | 60 to 125 | 17, 51 | 50, 59 | 33, 51 |
| 1. Diancie with Earth Power for Diamond Storm | Earth Power would go on its egg list | 52 to 88 | 27, 30 | 50, 39 | 47, 75 |
| 2. Whiscash, Leftovers, Adamant, Hydration; Curse, Earthquake, Waterfall, Stone Edge | yes | 93 to 178 | 3, 7 | 33 | 26, 35 |

Earth Power does not help: Diancie used it only 21 to 69 times a six and knocked out fewer, so the move was never the problem. Whiscash, from Ian's first list for her (2026-09-27), fixes the slot: its Ground and Water moves hit the Steel walls, and Curse is reliable setup. But it makes her far harder, about as hard as Thorton at 50, and she already reads harder than Wake and Barry 4. So I would keep Diancie (decision 8), and offer Whiscash only if Ian wants her fight harder.

## The egg-list commit

Every off-list move above went on its line's first stage's egg list in commit 3109c41339a on this branch, by Ian's ruling of 2026-10-29, and into `learnrewrite.IAN_EGG_MOVES`. No level-up entry moved, and none of the lines is held out from the generator. After it the OxiDex's lists give every move of the three teams at its level, the Kaizo checker finds no problem in any of the three files, and the trainer lint finds nothing. test_learnrewrite passes 6 of 6, test_learncheck 18 of 18 and test_trainers 44 of 44, and `make rom` builds.

## How the numbers were made

Every number comes from a run in the worktree `.claude/worktrees/boss-checks` on this branch, on the tree of 3109c41339a; the probes ran just before that commit, whose egg lists no fight reads. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/boss-checks/`, each with its own usage line, and none writes to `res/`. They are the Wake check's scripts, pointed at these fights.

- The boxes come from `plgoal3.setup` with the run name `boss-checks-study`, which has no earlier results, seeds 1 to 3. Byron's are goal 3's Byron boxes at 53. The Brains are read on Barry 5's boxes, cut just before Barry 5 in Byron's split. Goal 3 would stand those at Barry 5's ace's 53, since his team is not rebuilt yet, so the harness stands them at his honour cap of 50, the cap the Brains are levelled for. Wake's and Barry 4's are their own boxes at 44 and 42.
- `bc.py` is the harness. It adds the two Brains' constants to the trainers the balance tools read, sets their split to the box's for the player's items, adds Thorton to the simulator's reading of the permanent Trick Room list (`NOTR=1` leaves him off), turns the screen's Speeds over under the room, and swaps a pick into the party in memory (`CAND=name`, the sets in `cands.py`).
- `checks.py FIGHT PLACE SEED [N]` runs, in one pass, the six as the simulator builds them, the screen's top 20 sixes with every catch's margins, the catches that beat each member, the replacement trace (`fightai.replacement`), damage both ways, and the probe: 150 rough fights against the best and the most-taken six with a greedy player. It counts picks, real uses and what each did, items, knockouts while each member was in, the lead's first pick and the first member in after it, and for this study Meteor Beam and Acrobatics by the item held, Gyro Ball's power, the HP at each Explosion and Self-Destruct, each attack's order under the room, and the contact hits on a Rocky Helmet's holder. The player's replacement look-ahead is never counted. `runall.sh`, `runcands.sh` and `runmore.sh` run it under the memory cap; `summarise.py`, `ranges.py` and `bait.py` (the lead test) gather the tables.
- Legality comes from the OxiDex's `learnsets.lists` (`legal.py`) and the Kaizo checker (`oxide.py check`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`); `palette.py` lists a species' legal moves at a level.
- Damage is the calculator's lowest to highest roll in percent of the target's HP, at no stat stages.

Where the screen's bias bites: it counts only a clean one-on-one from full HP with no status move and no hazard, so it misses most of what Thorton and Argenta do, and it counts Shell Trap as a sure hit. The probe's greedy player never switches, so hazards bite only after a knockout or a Roar, Mean Look and Anchor Shot change nothing, and Swagger and Confuse Ray land on a player who never plays round them.
