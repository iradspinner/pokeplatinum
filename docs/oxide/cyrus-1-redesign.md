# Cyrus 1's redesign: the evidence and the diagnosis

Ian asked on 2026-11-01 for Cyrus 1 (the Celestic ruins, Byron's split, honour cap 47) to be redesigned in Roark's and Lucas and Dawn 2's checked stages, because its first scorer reading reads far too easy. This page holds stages 1 and 2, the evidence and the diagnosis, for Ian to check before any candidate or set is drafted. The team in the game is unchanged.

## Summary

The scorer wins Cyrus 1 on 98 percent of fights over goal 3's three boxes (96, 100 and 97), above Ian's 95 percent ceiling for a boss and easier than any boss read so far; only Moira 1's earlier team, an officer fight, read easier. The player loses about one Pokemon a fight. The reading is run `cyrus-1-61b9d0391`, on the team in the game today.

The fight is easy because every member is walled by a type each box holds eight to ten of. Cyrus's six are three Flying types, an Electric, a Fire and a Normal type, and the box at Celestic is full of Rock, Steel and Ground Pokemon. Rock and Steel resist almost all of his attacks, and Ground is immune to Electric and knocks out the Electric and Fire members with one Earthquake, or nearly. Of his 24 moves, none is super effective on Quagsire or Crustle, and only Electivire's Ice Punch is on Hippowdon, whose Thick Fat halves it. Palossand takes nothing at all from Porygon-Z. The trainer AI then makes it worse: against a pure Ground type, Electivire is the only member with a super-effective move, so the AI sends it in, and the wall knocks it out at once.

Golem is in all three of the scorer's sixes, and nearly every six the search played out won 84 percent of its fights or more. Salamence makes half the knockouts and Honchkrow a fifth. Crobat, Electivire and Porygon-Z together make an eighth. The softening of 2026-10-31 removed Brick Break, Adaptability, Ice Beam and Shadow Ball, the moves that reached the walls. That softening was judged on the outcome probe, whose player never switches, and this fight is won by switching each member into its wall.

What Ian decides, one line each:

1. The shape and diagnosis below: do they match how he would plan the fight? Yes, or yes with changes he names.
2. The target, percent won over the three boxes. (a) 85 to 92, beside Roark, Gardenia and Jupiter 1; (b) 75 to 85, the band of the hardest bosses, with no box under about 60; (c) 55 to 75, toward the 52 that Gardenia's first whole reading gave, which the Cyrus fights are allowed. Recommended: (b), since this is the first of three Cyrus fights and the split's first boss.
3. Crobat: keep it as the lead (Ian's ruling of 2026-10-31), keep it on the team with its slot and set open, or drop it. Recommended: keep it, slot and set open. As a lead into a Rock wall its current set does 6 to 18 percent a hit.
4. Which members are open to stage 3: (a) all but Salamence and the two canon picks; (b) only Electivire and Porygon-Z; (c) sets only, no new species. Recommended: (a), so Electivire, Porygon-Z and Magmortar may change species.
5. Cyrus's other canon picks: may Cyrus 1 take Gyarados, Weavile or Houndoom from Cyrus 2 or 3, neither of which is redesigned yet? Yes, or no. Recommended: yes. A Water canon pick answers both kinds of wall.
6. The softening's dials (no Download, Adaptability, Expert Belt, Brick Break or Speed natures): do they stay ruled out, or are they open again? Recommended: open. They were judged on the probe, and the scorer shows they were what made the fight.
7. Salamence: keep its Lum Berry, take the Yache Berry back, or leave it to stage 3. Recommended: leave it to stage 3. The Yache Berry answers the Ice attackers that now beat it, and its worth depends on the rest of the team.
8. Argo 1, read beside him: (a) not redesigned, and read by the scorer beside the new Cyrus 1; (b) redesigned in the same stages now; (c) read alone now. Recommended: (a). His team hits these same walls through Earth Power, Ice Beam, Waterfall, Giga Drain and three Earthquakes, so it does not share Cyrus's fault, and the probe cannot say how hard he reads.
9. A scorer reading of the redesigned team on the three boxes before it lands: yes or no. Recommended: yes, since the cheap checks misjudged this fight once.

Next steps once Ian has answered. Stage 3, candidates from the whole Pokedex against the needs listed at the end of stage 2, checked on the calculator, the Speed tiers and the AI's replacement rule, and built into two or three team shapes: about three to four hours of a session. Stage 4, the sets for his pick: about an hour. A scorer reading of the new team: about four hours of machine time, as this one took (14:20 to 18:25), with Argo 1's beside it if Ian picks 8 (a). Once Ian checks this page, Cyrus 1's shape goes into `boss-shapes.md`.

## Stage 1: the evidence

### The team as read

The file `galactic_boss_cyrus_celestic_town_ruins.json`, identical in the reading's tree and on `oxide` today. Every member has the highest IVs (iv_scale 255); the AI flags are Basic, Evaluate Attack and Expert. Speed and HP are at the member's level.

| Member | Level | Item | Ability | Nature | Speed | HP | Moves |
|---|---|---|---|---|---|---|---|
| Crobat | 45 | Razor Fang | Inner Focus | Jolly | 148 | 145 | Cross Poison, Brave Bird, U-turn, Taunt |
| Honchkrow | 46 | Black Glasses | Super Luck | Adamant | 102 | 162 | Crunch, Brave Bird, Sucker Punch, Heat Wave |
| Porygon-Z | 44 | Leftovers | Analytic | Bold | 97 | 142 | Tri Attack, Thunderbolt, Thunder Wave, Recover |
| Electivire | 44 | Sitrus Berry | Vital Spirit | Hardy | 111 | 133 | Thunder Punch, Ice Punch, Fire Punch, Earthquake |
| Magmortar | 44 | Charcoal | Flame Body | Timid | 110 | 133 | Flamethrower, Focus Blast, Psychic, Will-O-Wisp |
| Salamence (ace) | 47 | Lum Berry | Intimidate | Naughty | 113 | 160 | Dragon Dance, Dragon Claw, Earthquake, Fire Fang |

### The reading, beside the other bosses

Each box is read with its best six, 75 fights at real odds and 25 very unlucky. The difficulty number is the faints a fight plus 40 times the losing rate.

| Box (player's starter) | Won, real odds | Faints | Clean | Difficulty | Very unlucky, won |
|---|---|---|---|---|---|
| 1 (Turtwig) | 96% | 1.55 | 28% | 3.2 | 88% |
| 2 (Scorbunny) | 100% | 0.48 | 67% | 0.5 | 96% |
| 3 (Piplup) | 97% | 1.19 | 44% | 2.3 | 92% |

| Fight | Kind | Percent won (by box) |
|---|---|---|
| Moira 1, the earlier team | officer | 100 (100, 100, 100) |
| Cyrus 1 | boss | 98 (96, 100, 97) |
| Somnu 1 | officer | 94 (88, 96, 97) |
| Gardenia, locked | leader | 89 (99, 87, 83) |
| Jupiter 1, the earlier team | commander | 89 (99, 75, 93) |
| Roark, in the game | leader | 86 (81, 77, 99) |
| Mars 1, the earlier team | commander | 58 (57, 17, 100) |
| Gardenia, Ian's six, first reading (the barometer is its box 3) | leader | 52 (box 3: 27) |

Roark and Gardenia lose 2.55 and 2.58 Pokemon a fight; Cyrus 1 loses 1.07.

### The sixes the scorer chose

| Box | Six | Items |
|---|---|---|
| 1 | Luxray, Probopass, Quagsire, Golem, Palossand, Manaphy | Black Glasses, Metal Coat, Sitrus Berry, Rock Incense, Spell Tag, Mystic Water |
| 2 | Donphan, Garganacl, Alolan Ninetales, Bastiodon, Golem, Hippowdon | Sitrus Berry on Donphan, Garganacl and Hippowdon; Fairy Feather, Metal Coat, Rock Incense |
| 3 | Golem, Bastiodon (Shieldon held to 43), Crustle, Hippowdon, Palossand (Sandygast held to 47), Manaphy | Rock Incense, Metal Coat, Silver Powder, Sitrus Berry, Spell Tag, Mystic Water |

Their abilities matter here: Bastiodon and Probopass have Solid Rock (a quarter off super-effective hits), Hippowdon Thick Fat (Fire and Ice halved), Quagsire Water Absorb, Garganacl Purifying Salt, Crustle Sturdy, Golem Shell Armor, and Alolan Ninetales Magic Guard. The Rock and Steel walls carry Defences of 129 to 169; the Ground walls are bulky physically but carry Special Defences of only 68 to 82.

Each box holds eight to ten such walls, so no single catch is the problem:

| Box | Rock, Steel and Ground walls in the box | Also |
|---|---|---|
| 1 | Golem, Bastiodon, Probopass, Garganacl, Crustle, Quagsire, Palossand, Whiscash | Manaphy, Alolan Ninetales |
| 2 | Golem, Bastiodon, Garganacl, Crustle, Hippowdon, Quagsire, Donphan, Whiscash, Onix, Rhydon | Manaphy, Alolan Ninetales |
| 3 | Golem, Bastiodon, Crustle, Hippowdon, Quagsire, Palossand, Whiscash, Onix | Manaphy |

### Where the faints fell

The player's Pokemon knocked out by each member, over each box's 75 fights at real odds:

| Member | Box 1 | Box 2 | Box 3 | All | Share |
|---|---|---|---|---|---|
| Salamence | 59 | 6 | 58 | 123 | 51% |
| Honchkrow | 24 | 11 | 15 | 50 | 21% |
| Magmortar | 18 | 9 | 10 | 37 | 15% |
| Porygon-Z | 4 | 9 | 2 | 15 | 6% |
| Electivire | 9 | 1 | 0 | 10 | 4% |
| Crobat | 2 | 0 | 4 | 6 | 2% |

The player's Pokemon that fell most: on box 1 Quagsire (34), Manaphy (27) and Luxray (24); on box 2 Hippowdon and Alolan Ninetales (11 each); on box 3 Manaphy (21) and Hippowdon (20). Box 1 reads hardest because it has no Hippowdon or Donphan: its Ground wall is Quagsire, which Brave Bird hits harder.

### What each six did against each member

Damage from the vendored calculator's rows, which the scorer's fight state holds (sixteen rolls each; the player's held item is left out, so a boosted move hits a fifth harder). Each cell is the attacker's best move on the defender as a percent of the defender's HP, lowest to highest roll. Intimidate is not in the rows: once Salamence is in, the player's physical hits fall by a third. Rock Blast is as the calculator counts its hits. The catches are the same species at the same level and stats on every box.

Cyrus's best hit on each catch the sixes took:

| Catch (boxes) | Crobat | Honchkrow | Porygon-Z | Electivire | Magmortar | Salamence |
|---|---|---|---|---|---|---|
| Golem (1, 2, 3) | Brave Bird 14 to 18 | Crunch 35 to 42 | Tri Attack 25 to 30 | Earthquake 40 to 48 | Focus Blast 95 to 113 | Earthquake 54 to 64 |
| Bastiodon (2, 3) | Brave Bird 6 to 7 | Heat Wave 15 to 20 | Thunderbolt 20 to 25 | Earthquake 53 to 64 | Focus Blast 77 to 92 | Earthquake 71 to 84 |
| Probopass (1) | Brave Bird 7 to 9 | Crunch 19 to 23 | Thunderbolt 20 to 24 | Earthquake 65 to 79 | Focus Blast 79 to 93 | Earthquake 88 to 104 |
| Garganacl (2) | Brave Bird 14 to 17 | Crunch 34 to 41 | Thunderbolt 26 to 31 | Earthquake 39 to 46 | Focus Blast 65 to 78 | Earthquake 51 to 62 |
| Crustle (3) | Brave Bird 37 to 44 | Brave Bird 54 to 65 | Thunderbolt 38 to 45 | Thunder Punch 35 to 42 | Flamethrower 65 to 76 | Dragon Claw 39 to 47 |
| Hippowdon (2, 3) | Brave Bird 30 to 36 | Brave Bird 45 to 53 | Tri Attack 40 to 49 | Earthquake or Ice Punch 20 to 24 | Focus Blast 38 to 45 | Dragon Claw 32 to 38 |
| Quagsire (1) | Brave Bird 41 to 50 | Brave Bird 61 to 72 | Tri Attack 40 to 48 | Earthquake 27 to 33 | Focus Blast 38 to 45 | Dragon Claw 45 to 53 |
| Donphan (2) | Brave Bird 30 to 35 | Brave Bird 43 to 52 | Tri Attack 51 to 61 | Ice Punch 37 to 45 | Flamethrower 65 to 77 | Dragon Claw 33 to 39 |
| Palossand (1, 3) | Brave Bird 37 to 44 | Crunch 89 to 106 | nothing | Ice Punch 47 to 57 | Flamethrower 58 to 69 | Dragon Claw 40 to 48 |
| Manaphy (1, 3) | Brave Bird 36 to 43 | Brave Bird 53 to 64 | Thunderbolt 49 to 58 | Thunder Punch 69 to 83 | Focus Blast 30 to 36 | Dragon Claw 39 to 47 |
| Alolan Ninetales (2) | Cross Poison 60 to 73 | Brave Bird 76 to 91 | Tri Attack 36 to 44 | Fire Punch 65 to 78 | Flamethrower 95 to 113 | Fire Fang 82 to 98 |
| Luxray (1) | U-turn 40 to 48 | Brave Bird 38 to 45 | Tri Attack 45 to 53 | Earthquake 69 to 82 | Focus Blast 83 to 99 | Earthquake 92 to 109 |

The catches' best hit on each member, with the moves the scorer gave them:

| Catch | Crobat | Honchkrow | Porygon-Z | Electivire | Magmortar | Salamence |
|---|---|---|---|---|---|---|
| Golem | Rock Blast 78 to 99 | Rock Blast 88 to 103 | Earthquake 54 to 65 | Earthquake 135 to 159 | Earthquake 135 to 159 | Rock Blast 71 to 90 |
| Bastiodon, box 2's set | Zen Headbutt 42 to 51 | Hard Press 42 to 50 | Hard Press 40 to 49 | Zen Headbutt 54 to 64 | Bulldoze 42 to 49 | Hard Press 34 to 41 |
| Probopass | Rock Blast 53 to 66 | Rock Blast 55 to 66 | Rock Blast 27 to 33 | Bulldoze 33 to 40 | Rock Blast 67 to 81 | Rock Blast 45 to 56 |
| Garganacl | Rock Slide 63 to 75 | Rock Slide 66 to 79 | Heavy Slam 35 to 41 | Bulldoze 43 to 52 | Rock Slide 81 to 96 | Rock Slide 53 to 65 |
| Crustle | Rock Slide 66 to 78 | Rock Slide 70 to 82 | X-Scissor 36 to 44 | Stomping Tantrum 55 to 66 | Rock Slide 82 to 99 | Rock Slide 57 to 68 |
| Hippowdon | Take Down 27 to 33 | Take Down 29 to 35 | Earthquake 48 to 57 | Earthquake 117 to 139 | Earthquake 117 to 139 | Take Down 24 to 28 |
| Quagsire | Rock Slide 37 to 44 | Rock Slide 38 to 45 | Earthquake 38 to 45 | Earthquake 91 to 109 | Earthquake 91 to 109 | Rock Slide 32 to 38 |
| Donphan | Slam 33 to 39 | Slam 34 to 41 | Earthquake 51 to 61 | Earthquake 126 to 148 | Earthquake 126 to 148 | Ice Shard 47 to 57 |
| Palossand, box 3's set | Shadow Ball 33 to 40 | Shadow Ball 17 to 20 | Earth Power 40 to 49 | Earth Power 81 to 96 | Earth Power 73 to 87 | Shadow Ball 31 to 37 |
| Manaphy | Icy Wind 30 to 37 | Icy Wind 33 to 39 | Bubble Beam 29 to 35 | Bubble Beam 29 to 34 | Bubble Beam 54 to 64 | Icy Wind 57 to 70 |
| Alolan Ninetales | Triple Axel 92 to 113 | Triple Axel 101 to 122 | Triple Axel 48 to 58 | Play Rough 87 to 103 | Payback 38 to 45 | Triple Axel 167 to 202 |
| Luxray | Wild Charge 88 to 104 | Wild Charge 93 to 111 | Wild Charge 46 to 54 | Wild Charge 55 to 66 | Wild Charge 56 to 66 | Wild Charge 38 to 45 |

Speed: every member of Cyrus's team outspeeds every wall, which run 40 to 59. The fastest catches are Manaphy and Alolan Ninetales at 106, over Honchkrow's 102 and Porygon-Z's 97, and Luxray at 101, over Porygon-Z. The walls do not need to move first: they take two to sixteen hits from most members.

Member by member:

Crobat leads every fight. Into a Rock lead (Golem, Bastiodon, Probopass) it does 6 to 18 percent a hit, and its Taunt stops nothing, since the walls attack. It U-turns out, and the replacement rule (below) sends Electivire in. Its Razor Fang flinches matter only when it does damage, which here it seldom does.

Honchkrow is the second real threat. Its Crunch knocks out Palossand in one or two hits, and its Brave Bird takes most of Quagsire, Manaphy, Crustle and Alolan Ninetales. Golem's Rock Blast and Luxray's Wild Charge nearly knock it out in one hit, and Bastiodon takes 15 to 20 percent from it. It sits at 102 Speed, four points under Manaphy and Alolan Ninetales, so those two move first; Ninetales's Triple Axel knocks it out in one hit (101 to 122).

Porygon-Z does almost nothing. Its Normal and Electric moves are resisted by every Rock and Steel wall, Electric does not touch the Ground walls, and Palossand, a Ghost and Ground type, is immune to its whole set, Thunder Wave included. Analytic only works when it moves last, and it outspeeds every wall, so the ability never fires. Bold puts its nature on Defence while its attacks are special.

Electivire does almost nothing either. Thunder Punch is dead on every Ground wall. Its Earthquake does 53 to 79 percent to Bastiodon and Probopass (Solid Rock and their Defences blunt the four-times hit), and every Ground wall, Golem included, knocks it out with one Earthquake or nearly (91 to 159). Its Ice Punch on Hippowdon is halved by Thick Fat. Vital Spirit only blocks Yawn.

Magmortar carries the team's only special hit on the Rock and Steel walls, Focus Blast (77 to 113 percent on Golem, Bastiodon and Probopass), but it is 70 percent accurate, and Hippowdon and Quagsire take 38 to 45 percent from it and knock Magmortar out in one Earthquake. Its Flamethrower takes most of Palossand, Donphan, Crustle and Alolan Ninetales.

Salamence is the fight. It comes last, so it meets a worn six. Its Earthquake takes most of Probopass and Bastiodon and half of Golem; it is immune to the Ground walls' Earthquake; and Intimidate cuts every physical reply by a third. The six keep its answers for it: Manaphy's Icy Wind (57 to 70, special, so Intimidate does not touch it), Alolan Ninetales's Triple Axel (167 to 202), Golem's Rock Blast and Donphan's Ice Shard. Its Lum Berry clears one Yawn from Quagsire or Hippowdon.

### The traced lines

Each box's search keeps one traced fight. Boxes 2 and 3 show the fight as it usually goes; box 1's is one of its few losses.

On box 2, Golem leads into Crobat and switches to Hippowdon. Crobat U-turns into Electivire, which takes a fifth of Hippowdon's HP with Earthquake and falls to Hippowdon's. Magmortar's Focus Blast misses and it falls to the next Earthquake. Honchkrow comes in, and Alolan Ninetales, faster, knocks it out with Triple Axel. Bastiodon takes Crobat's Taunt and Brave Bird for 10 HP while Hard Press wears it down. Salamence comes in on Golem, Donphan switches in, Salamence spends a turn on Dragon Dance, and two Ice Shards knock it out. Garganacl's Recover outheals Porygon-Z's Thunderbolt until Heavy Slam finishes it. The player wins with no faints.

On box 3, the same opening runs: Golem leads, Hippowdon takes Crobat's U-turn, and Hippowdon's Earthquake knocks out Electivire and then Magmortar. Bastiodon takes a Brave Bird and four Heat Waves from Honchkrow and knocks it out with Iron Head. Manaphy's two Icy Winds knock out Salamence. Palossand then walls Porygon-Z for most of twenty turns: Tri Attack and Thunderbolt do nothing to it, Iron Defense takes it to plus four, Shadow Ball knocks out Crobat, and Earth Power outlasts Porygon-Z's Recover. The player wins with no faints.

On box 1, the traced fight is lost. Probopass leads, Crobat chips Palossand and Manaphy as the player switches, and Honchkrow's Crunch lowers Probopass's Defence twice. Salamence then arrives on a worn six and knocks out all six, with Earthquake, Dragon Claw and Fire Fang and no Dragon Dance, after Golem's Rock Blast has taken it to a third of its HP. It shows what the reading's losses are made of: Salamence closing on a team the earlier members have chipped.

### Which members never mattered, and why

Crobat (2 percent of the faints), Electivire (4) and Porygon-Z (6) together make one faint in eight. Each is walled by the box's commonest types: Crobat's Poison and Flying by Rock and Steel, Electivire's Electric by Ground, and Porygon-Z's Normal and Electric by Rock, Steel and Ground at once, with Palossand immune to all of it.

The AI's replacement rule makes Electivire's case worse. After a knockout or a U-turn, the engine's rule (`fightai.replacement`, BattleAI_PostKOSwitchIn) takes the member whose types score highest on the player's active Pokemon and that has any super-effective move on it, setting aside those without one. Worked by hand from the type chart, against a pure Ground wall (Hippowdon, Donphan) no member but Electivire has a super-effective move (Ice Punch), and the chart does not see Thick Fat, so Electivire is sent in. Against Golem and the Rock and Steel walls, Electivire scores highest by type (Fighting) and has Earthquake. So in front of most walls the AI sends Electivire, and the wall's Earthquake knocks it out in one hit. Both winning traced lines open this way. Against Palossand it sends Honchkrow (Crunch), and against Manaphy Electivire (Thunder Punch), which are its two good entries.

### What the search tried and dropped

The search races sixes from the matchup screen's top choices, plays off held-back versions, plays out three finalists, and loops on two more. The won figures are the network's estimate over 75 fights, then the play-outs over 25.

| Box | Six | Network | Play-outs |
|---|---|---|---|
| 1 | Luxray, Probopass, Quagsire, Golem, Palossand, Manaphy (chosen) | 97% | 96% |
| 1 | Probopass, Quagsire (Wooper held to 43), Golem, Palossand, Manaphy, Jellicent | 89% | 92% |
| 1 | Luxray, Quagsire, Golem, Palossand (Sandygast held to 47), Manaphy, Pachirisu | 72% | 96% |
| 1 | loop: Alolan Ninetales, Gengar, Garganacl, Golem, Crustle, Manaphy | | 84% |
| 1 | loop: Probopass, Gengar, Golem, Crustle, Palossand, Manaphy | | 92% |
| 2 | Donphan, Garganacl, Bastiodon, Hippowdon, Araquanid, Manaphy | 84% | 100% |
| 2 | Donphan, Garganacl, Rotom, Bastiodon, Hippowdon, Araquanid | 85% | 96% |
| 2 | Garganacl (Nacli held to 45), Rotom, Bastiodon, Golem, Hippowdon, Manaphy | 92% | 96% |
| 2 | loop: Donphan, Garganacl, Alolan Ninetales, Bastiodon, Golem, Hippowdon (chosen) | | 100% |
| 2 | loop: Rapidash, Donphan, Bastiodon, Sylveon, Glalie, Golem | | 100% |
| 2 | loop: Rapidash, Garganacl, Alolan Ninetales, Bastiodon, Sylveon, Golem | | 92% |
| 3 | Bibarel, Golem, Bastiodon, Hippowdon, Palossand, Manaphy | 93% | 100% |
| 3 | Empoleon (Piplup held to 43), Golem, Bastiodon (Shieldon held to 43), Hippowdon, Palossand, Manaphy | 95% | 96% |
| 3 | Golem, Bastiodon (held), Crustle, Hippowdon, Palossand (held), Manaphy (chosen) | 99% | 100% |
| 3 | loop: Golem, Kingler, Crustle, Hippowdon, Manaphy, Milotic | | 84% |
| 3 | loop: Golem, Kingler, Crustle, Palossand, Manaphy, Milotic | | 84% |

Box 3 was also read without its held-back versions, at 97 percent won and 1.77 faints, so the holds do not make the fight. What the search dropped tells as much as what it kept. On box 1 it dropped Bastiodon, in 7 of the screen's top 10 sixes and in the race's best six for three rounds, and still won 96 percent. On box 2 it dropped Rotom, in 9 of the screen's top 10, and a loop six with Rapidash, Sylveon and Glalie in it won all 25 play-outs. Apart from one six on box 3's run without holds (Empoleon, Golem, Bastiodon, Crustle, Palossand, Manaphy, at 72 percent), no six the search played out won fewer than 84 percent: almost any team built on two or three of the walls wins.

### How the draft and each softening step changed things

From `cyrus-argo-check.md` and the file's history. The probe column is the rough wins of 900 on the outcome probe (150 fights against each of two sixes on each box), whose greedy player takes its hardest hit and never switches; Wake reads 378 on it.

| Step | Date | What changed | Probe |
|---|---|---|---|
| Drafted (745ebf383) | 2026-10-13 | Built for Byron's cap of 53, at 51 to 53: Porygon-Z with Download, a Silk Scarf, Modest, Ice Beam and Shadow Ball; Electivire with Adaptability, an Expert Belt, Naive and Brick Break; Salamence with a Yache Berry; Honchkrow with Night Slash, then Crunch | none recorded |
| Re-levelled (956439f9f) | 2026-10-31 | The same sets at 44 to 47, for the honour cap of 47 | 52 |
| One dial tried | 2026-10-31 | Porygon-Z with Analytic for Download | 75 |
| Softened (8d5ffd05f), in the game | 2026-10-31 | Porygon-Z to 44, Analytic, Leftovers, Bold, Thunder Wave and Recover; Electivire Vital Spirit, a Sitrus Berry, Hardy, Fire Punch for Brick Break; Salamence a Lum Berry | 242 |
| The scorer | 2026-11-01 | the softened team | 98% won |

The softening was aimed at the members the probe said made most knockouts, Porygon-Z and Electivire, and it took away the moves that reached the walls. Brick Break was Electivire's answer to Bastiodon, Probopass, Garganacl and Glimmora on the earlier check's screen. Shadow Ball was Porygon-Z's only move that touched Palossand, and Ice Beam its only move super effective on Golem, Donphan and Palossand. Fourteen variants of those two were tried and stopped near 242, because Salamence and Honchkrow then made most of the probe's knockouts, which the scorer confirms.

The probe misjudged the fight because its player never switches. A greedy player that leaves Golem in against Magmortar, or Manaphy in against Electivire, loses those exchanges; the scorer's player switches each member into its wall, and then most members cannot hurt it. The probe put Cyrus 1 at 40 a box, between Roark (45) and Gardenia (29), which read 86 and 89 percent won; the scorer puts it above both, and above Somnu 1, which the probe called twice as winnable (`probe-ranking.md`). The drafted team was never read by the scorer, so whether it would have been right cannot be said from this evidence.

## Stage 2: the diagnosis

### The fight's shape

Written as `boss-shapes.md` frames the others. How sure: from one scorer reading of today's team on three boxes, and the calculator's figures.

Identity. Cyrus's theme is power: 18 different Pokemon over his three fights, no repeats, with his canon picks (Weavile, Honchkrow, Houndoom, Gyarados, Crobat) spread among them. Cyrus 1 is the first six: fully evolved, high in raw stats, faster than every catch, three of them Flying types. Its power is aimed at the types the player at Celestic does not bring.

The boss's core, by the reading:

- Salamence, the ace, half the faints: Earthquake on the Rock and Steel walls, immunity to the Ground walls' Earthquake, Intimidate, and Dragon Dance as a closer.
- Honchkrow, a fifth of the faints: Crunch for Palossand, Brave Bird for the Water, Ice and Bug types.
- Magmortar's Focus Blast, the one special hit on the Rock and Steel walls.

The player's core counterpieces, from the scorer's sixes:

- A Ground wall that takes the Electric and Fire members and knocks them out with one Earthquake: Hippowdon (boxes 2 and 3), Quagsire (box 1), Donphan (box 2), and Golem.
- A Rock or Steel wall that resists the Flying, Poison and Normal moves: Bastiodon (boxes 2 and 3), Probopass (box 1), Garganacl (box 2), Crustle (box 3), and Golem. Golem, a Rock and Ground type, is in all three sixes.
- Palossand (boxes 1 and 3), immune to Porygon-Z's whole set.
- A special Ice or Water attacker faster than Honchkrow, kept for Salamence: Manaphy (boxes 1 and 3), Alolan Ninetales (box 2).

Material for this fight: the availability by Celestic of Golem, Bastiodon, Probopass, Garganacl, Crustle, Hippowdon, Quagsire, Donphan, Palossand, Manaphy and Alolan Ninetales; Thick Fat, Solid Rock and Purifying Salt on them; any Water, Grass, Ice, Ground or Fighting move on a Cyrus member; Speed near 102 to 106, where Honchkrow meets Manaphy and Ninetales; Salamence's item and moves.

### Why the fight is easy

1. Each member is walled by a type the box holds five to eight of. Counting Cyrus's 24 moves, those super effective on each wall:

   | Wall | Cyrus's super-effective moves on it |
   |---|---|
   | Quagsire (Water, Ground) | none |
   | Crustle (Bug, Rock) | none |
   | Hippowdon, Donphan (Ground) | Ice Punch only, halved on Hippowdon by Thick Fat |
   | Palossand (Ghost, Ground) | Crunch, Sucker Punch, Ice Punch |
   | Bastiodon, Probopass (Rock, Steel) | two Earthquakes and Focus Blast, each cut by Solid Rock |
   | Garganacl (Rock) | two Earthquakes and Focus Blast |
   | Golem (Rock, Ground) | two Earthquakes, Focus Blast and Ice Punch |

   For comparison, Argo 1's six, met just before in Celestic Town, carry Earth Power, Ice Beam, Waterfall, Ice Fang, Giga Drain, Shadow Ball and three Earthquakes.

2. The special attackers have the wrong types. The Ground walls have Special Defences of 68 to 82, low for this level, but Cyrus's special moves are Porygon-Z's Normal and Electric and Magmortar's Fire and Psychic: resisted, ignored or halved. No member has a Water, Grass or Ice special move.

3. The trainer AI feeds Electivire into the walls. In front of a Ground type, Electivire is the only member the replacement rule will send, for an Ice Punch that does a fifth of Hippowdon's HP; in front of a Rock or Steel wall it scores highest by type. The wall's Earthquake then knocks it out in one hit. Crobat's U-turn sets this up on turn one.

4. The softening removed exactly the moves that reached the walls (Brick Break, Shadow Ball, Ice Beam), and some of what replaced them does nothing here. Analytic never fires, because Porygon-Z outspeeds every wall; Thunder Wave fails on the Ground walls; Vital Spirit only blocks Yawn; Bold suits a special attacker poorly.

5. The lead has no job. Crobat does a tenth of a Rock lead's HP a hit, its Taunt meets a box that only attacks, and its U-turn brings in Electivire's worst matchup. Ian's lead test (a lead may be wholly countered if the answer draws in a member that beats it with setup) fails: the answer to Crobat, a Rock or Ground wall, draws in Electivire, which loses.

6. One win condition, met last and expected. Salamence makes half the faints, but the player knows it comes last and keeps Manaphy, Alolan Ninetales, Golem or Donphan for it. With the Lum Berry it has nothing against the Ice answers; the earlier check found that the Yache Berry was what turned them away.

7. Speed buys nothing against a wall. Every member outspeeds every wall, but the walls take two or more hits from all but Salamence, Magmortar's Focus Blast and Honchkrow's Crunch. The one Speed tier that decides a matchup is Honchkrow at 102 under Manaphy and Alolan Ninetales at 106, where the player moves first.

### What a redesign has to answer

1. The Ground walls (Hippowdon, Quagsire, Donphan, Golem, Palossand): special Water, Grass or Ice moves, or members whose own types hit Ground, strong enough through Thick Fat and Water Absorb, so that a Ground switch-in costs the player something.
2. The Rock and Steel walls (Bastiodon, Probopass, Garganacl, Crustle, Golem): Ground, Fighting or Water hits with enough power to get through Solid Rock and Defences of 129 to 169, on more than one member and not only at 70 percent accuracy.
3. Palossand: an answer besides Honchkrow's Crunch, since it is immune to Normal, Fighting and Electric and resists Poison and Rock.
4. The bait order. For each wall, which member the replacement rule draws in, and that member beating it. This is Ian's lead test, and it decides whether the AI walks into the walls again.
5. The lead: a member with a job against a Rock or Ground lead (chip, a hazard, a status, a pivot into the right member).
6. Salamence's answers: Manaphy's Icy Wind, Alolan Ninetales's Triple Axel and Donphan's Ice Shard. Either a teammate removes or weakens them first, or the Yache Berry comes back.
7. The Honchkrow tier: whether it stays under Manaphy and Ninetales at 102, or a nature moves it over them. That choice is material, as Gardenia's tiers were.
8. What stays, unless Ian says otherwise: the theme (power, no repeats over the three fights), Salamence as the ace at 47, Mars 1's shape (the ace at the cap, one member right below it, the rest two or three under), no item or nature repeated, at most one forced trade, and the Cyrus fights allowed to read harder than other bosses.

## How the numbers were made

The reading's files are in `~/oxide-trials/goal3/cyrus-1-61b9d0391/cyrus_1/box1` to `box3`: each box's `result.json` and `log.txt`, and its search's `line.txt`. The reading ran at 61b9d0391 from the tree `~/oxide-trials/goal3/tree-cyrus-1`, whose Cyrus 1 file matches `oxide`'s. Boxes 2 and 3 reused box 1's networks without labels or training of their own, as their logs say. Nothing here ran the scorer or the probe, and nothing changed the simulator or `res/`.

The damage and Speed figures come from three short scripts in `/home/ian/.claude/jobs/cyrus-1-redesign/`, run from this branch's worktree under `tools/oxide/capped`. Each builds the reading's fight with goal 3's own setup (`plgoal3.setup` and `fight_state`, seeds 1 to 3, the box at 47, a fresh run name) and reads the calculator rows the scorer reads. `dmg.py` gives each Cyrus member's best move on each chosen catch and the reverse, `pair.py` every move of a named pair, and `abil.py` the catches' abilities and stats. Cyrus's members are limited to their four moves; the player's to the moves the scorer gave them. The replacement rule's picks were worked by hand from `fightai.replacement` and the type chart, not run.
