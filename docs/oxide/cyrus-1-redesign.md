# Cyrus 1's redesign: the evidence, the diagnosis, the shapes and the sets

Ian asked on 2026-11-01 for Cyrus 1 (the Celestic ruins, Byron's split, honour cap 47) to be redesigned in Roark's and Lucas and Dawn 2's checked stages, because its first scorer reading reads far too easy. This page holds stages 1 and 2, the evidence and the diagnosis, which Ian checked the same day, stage 3, the candidates and three team shapes, which he checked the same day, and stage 4, the sets of the shape he picked, now in Cyrus 1's file and waiting on the Overseer's scorer reading.

## Ian's answers (2026-11-01)

1. The shape and the diagnosis match how he would plan the fight.
2. The target is 75 to 85 percent won over the three boxes, with no box under 60.
3. Every member is open but Salamence and Honchkrow. The page's question named Honchkrow and Crobat as the two canon picks that would stay; Ian opened Crobat too: "seeing as that is still 3 flying types you can change up the crobat as well if needed."
4. Cyrus 1 takes none of Gyarados, Weavile or Houndoom, which stay for Cyrus 2 and 3.
5. Every dial the softening of 2026-10-31 turned off is open again: Download, Adaptability, the Expert Belt, Brick Break, Speed natures and Salamence's item.
6. Argo 1 is not redesigned. The scorer reads him beside the new Cyrus 1.
7. The new team gets a scorer reading before it lands, which the Overseer runs.

## Ian's answers to stage 3 (2026-11-01)

1. Shape C: Swampert leads, then Honchkrow, Porygon-Z and Electivire with the draft's sets, Magmortar and Salamence.
2. The lead's job is Swampert's Stealth Rock.
3. Salamence's Yache Berry comes back.
4. A species that a later or optional fight also uses is allowed (Swampert is on May).

## Summary

Shape C is written into Cyrus 1's file, and every check passes. The AI flags stay Basic, Evaluate Attack and Expert. No move needed an egg-list addition. The next step is the Overseer's scorer reading, with Argo 1 beside it. Nothing waits on Ian before then.

| Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---|---|---|---|---|---|
| Swampert (lead) | 45 | Torrent | Leftovers | Brave | 64 | Stealth Rock, Earthquake, Waterfall, Ice Punch |
| Honchkrow | 46 | Super Luck | Black Glasses | Adamant | 102 | Crunch, Brave Bird, Sucker Punch, Heat Wave |
| Porygon-Z | 45 | Download | Silk Scarf | Modest | 99 | Tri Attack, Thunderbolt, Ice Beam, Shadow Ball |
| Electivire | 44 | Adaptability | Expert Belt | Naive | 122 | Thunder Punch, Brick Break, Ice Punch, Earthquake |
| Magmortar | 44 | Flame Body | Charcoal | Timid | 110 | Flamethrower, Focus Blast, Psychic, Will-O-Wisp |
| Salamence (ace) | 47 | Intimidate | Yache Berry | Naughty | 113 | Dragon Dance, Dragon Claw, Earthquake, Fire Fang |

The levels take Mars 1's shape at the honour cap of 47: the ace at 47, Honchkrow right below it at 46, and the rest two or three below. No item or nature repeats.

C risks a box under Ian's floor of 60, since it is the shape the screen reads hardest. If the reading shows one, these are the two dials to soften it, in this order. Neither is applied.

1. Porygon-Z's Download for its hidden Analytic. Download raises its Sp. Atk on entry against nearly every wall, and that raise turns Ice Beam into a one-hit knockout on Golem, Palossand and Donphan and lets Tri Attack and Thunderbolt knock out Quagsire, Hippowdon and Manaphy on a high roll. Analytic never fires here, since Porygon-Z outspeeds every wall.
2. Electivire's Adaptability for Vital Spirit, keeping Brick Break. Adaptability is what lets Brick Break take Bastiodon, the box's most common wall, in one hit or nearly (97 to 118 percent), and Thunder Punch knock out Manaphy (112 to 133).

Swampert's Leftovers are a third dial if one box stays low after those two. No answer in the boxes takes half of Swampert's HP with its lowest roll.

## Stage 4: the sets and their checks

### Why each set is as it is

Swampert carries Stealth Rock for its job, Earthquake and Waterfall for the Rock, Steel and Ground walls, and Ice Punch for the Grass types that are its only real answers (Tsareena, Leavanny, Breloom, Leafeon). Brave suits a physical set whose Speed hardly matters: at 64 or at a neutral 72, it is over every wall and under Tsareena, Leavanny and Leafeon. Leftovers keep it in for a second layer of damage after the hazard.

Honchkrow, Magmortar and Salamence keep their sets, with Salamence's Yache Berry back by Ian's answer. Porygon-Z and Electivire take the draft's sets of 2026-10-13 whole, at the levels of 2026-10-31.

### The AI flags, by the flags guide

The team keeps Basic, Evaluate Attack and Expert, and takes no other flag.

- Weather: no member carries a weather move, so the flag would do nothing.
- Harassment: the team's only move in its table is Will-O-Wisp; a status team carries two or more.
- Risky: Honchkrow's Super Luck is one member's idea, not the team's, and the flag would push Sucker Punch as a gamble.
- Prioritize Extremes: Stealth Rock and Will-O-Wisp are pieces of an attacking plan, and the guide keeps the flag off a team holding Sucker Punch.
- Check HP: no member carries a trade move.

On the base flags Expert already gives Stealth Rock a 75 percent chance against Swampert's best attack on its first turns, which is the lead's job.

### Legality

The OxiDex's own check (`learnsets.lists`) finds every move of the six in Oxide's lists at its member's level. Swampert has its four by TM and HM (Stealth Rock is TM 76). Honchkrow's Crunch and Brave Bird come from Murkrow's egg list, added on 2026-10-31. Porygon-Z has Tri Attack by egg and the rest by TM. Electivire has Thunder Punch at level 28, Brick Break and Earthquake by TM, and Ice Punch by egg. Nothing went into `learnrewrite.IAN_EGG_MOVES`.

### Speed tiers, against each whole box at 47

| Member | Speed | Outspeeds (box 1, 2, 3) | Within three points |
|---|---|---|---|
| Electivire | 122 | 86 of 91, 86 of 93, 85 of 88 | Cinderace 123 and Liepard 121 (box 2); Salazzle 122, a tie (box 3) |
| Salamence | 113 | 84, 80, 85 | Gengar 115 (box 1) and Rapidash 115 (box 2) over it; Staraptor and Mienshao 110 under |
| Magmortar | 110 | 82, 77, 85 | ties with Staraptor (boxes 1 and 2) and Mienshao (box 2); Delphox 109 (box 3) |
| Honchkrow | 102 | 78, 72, 81 | one point over Luxray, Absol, Leafeon, Pachirisu, Jynx and Sharpedo at 101; under Manaphy and Alolan Ninetales at 106 |
| Porygon-Z | 99 | 69, 70, 78 | over Rotom 97 and Leavanny and Tsareena 98; under Luxray, Absol and Leafeon 101 |
| Swampert | 64 | 31, 28, 35 | ties Torterra (box 1); Machamp 63 (box 3) |

The boxes' fastest catch is Crobat at 134. Three tiers sit on a knife edge, and stage 4 leaves them as set. Magmortar ties Staraptor and Mienshao. Honchkrow sits one point over six catches. Porygon-Z sits between the Rotom and Tsareena tier and the Luxray tier.

### Porygon-Z with Download

Download raises one stat a stage as Porygon-Z comes in. It raises Sp. Atk when the Pokemon in front has a Defense no lower than its Sp. Def, and Attack otherwise, which this all-special set never uses. Against the likely answers, from the calculator's own runner, with the player's item left out:

| The Pokemon in front | Raised | Best move without Download | With it |
|---|---|---|---|
| Golem | Sp. Atk | Ice Beam 90 to 107 | 135 to 160 |
| Palossand | Sp. Atk | Ice Beam 81 to 96 | 121 to 144 |
| Donphan | Sp. Atk | Ice Beam 91 to 108 | 137 to 162 |
| Quagsire | Sp. Atk | Tri Attack 57 to 68 | 85 to 101 |
| Hippowdon | Sp. Atk | Tri Attack 58 to 69 | 87 to 103 |
| Manaphy | Sp. Atk | Thunderbolt 56 to 68 | 86 to 101 |
| Crustle | Sp. Atk | Thunderbolt 44 to 53 | 67 to 79 |
| Garganacl | Sp. Atk | Thunderbolt 31 to 37 | 46 to 55 |
| Bastiodon | Sp. Atk | Thunderbolt 24 to 29 | 36 to 43 |
| Corviknight | Sp. Atk | Thunderbolt 66 to 79 | 101 to 119 |
| Rotom | Sp. Atk | Shadow Ball 70 to 82 | 102 to 122 |
| Probopass, Alolan Ninetales, Jellicent, Araquanid, Empoleon, Abomasnow | Attack (no use) | Thunderbolt or Tri Attack, 24 to 75 | the same |

So Download is the set's power against the Ground walls, and the first dial to soften. Against Probopass and Alolan Ninetales it does nothing.

### The replacement trace

The trace was run on the file as written, on all three boxes, with the trainer AI's own rule. It matches stage 3's run of shape C exactly. While Swampert stands, the rule sends it into every Rock, Steel and Ground wall, and into Palossand. Once Swampert is gone, Electivire comes in against Golem, Quagsire and the Rock and Steel walls, and Golem and Quagsire knock it out with one Earthquake or nearly. Against Hippowdon and Donphan Porygon-Z comes in instead, with Ice Beam and Tri Attack in range. Manaphy draws in Electivire, whose Thunder Punch knocks it out. Alolan Ninetales and Corviknight draw in Magmortar. Rotom, Jellicent and Araquanid draw in Honchkrow. The matchup screen reads 11.7, 11.6 and 10.9, as in stage 3.

### Checks

| Check | Result |
|---|---|
| The trainer lint, through `trainers.save` | no findings |
| The real packer | packed (re-run once the build made it) |
| The OxiDex's legality check | every move in Oxide's lists at its level; no egg-list addition |
| test_b1 (Cyrus 1's ace at his honour cap among them) | 50 of 50 |
| test_learncheck | 18 of 18 |
| test_learnrewrite | 6 of 6 (its note on five species files differing from the generator was there before) |
| test_trainers | 44 of 44 |
| `make rom` | builds |
| the gate (`integrate.sh --verify-only` on the built ROM) | 53 of 54 pass; the one failure is sync-docs, which refuses to run on any branch but `oxide`, so the Overseer's merge runs it |

## Stage 3: the summary as Ian read it

Stage 3 gives three team shapes. Each was built from a sweep of 267 species on the vendored calculator against 32 of the player's likely answers, and each was checked with the trainer AI's own replacement rule on all three boxes. No shape has a scorer reading, so how hard each reads is a forecast from cheap checks. My pick is shape A.

| Shape | The six (lead first, ace last) | New species | Flying types |
|---|---|---|---|
| A, Spikes and the walls' own weaknesses | Cloyster, Honchkrow, Hariyama, Swampert, Meganium, Salamence | 4 | 2 |
| B, Crobat's U-turn into the answer | Crobat, Honchkrow, Machamp, Nidoking, Meganium, Salamence | 3 | 3 |
| C, the draft's dials back, Swampert for Crobat | Swampert, Honchkrow, Porygon-Z, Electivire, Magmortar, Salamence | 1 | 2 |

The matchup screen's best six, by box, as background only, since the screen and the probe misjudged this fight. Lower means the player's best six wins its one-on-ones by less. The order is C, then A, then B, then today's team, but no screen figure can be turned into a percent won.

| Screen's best six | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Today's team (read at 96, 100 and 97 percent won) | 17.3 | 17.2 | 17.7 |
| A | 13.6 | 13.6 | 12.2 |
| B | 16.3 | 15.7 | 16.7 |
| C | 11.7 | 11.6 | 10.9 |

I recommend A for four reasons. Every member beats a class of wall, and the replacement rule sends it into that class. Cloyster's Spikes make each switch cost an eighth of the player's HP, and switching into walls is how the player wins today. No answer in the boxes takes half of Swampert's HP with its lowest roll, and only two take half of Meganium's, so the walls cannot simply sit in front of them. And A carries two Flying types and no species from a nearby boss. C is the harder fallback: the smallest change, but it brings back the draft's Porygon-Z and Electivire, which the probe read as far harder than any accepted fight, so it risks a box under 60. B barely moves the screen and keeps three Flying types, so I do not recommend it.

What Ian decided on (his answers are at the top of the page):

1. Which shape goes to stage 4: A (recommended), C, or B.
2. For A, the lead's job: Cloyster's Spikes (recommended, a cost on every switch, Ground types included), or Stealth Rock from Swampert, which barely touches the Rock and Steel walls.
3. Salamence's item: the Yache Berry back (A and C; recommended, since the Ice attackers are its main answers) or the Lum Berry (B).
4. A species a later or optional fight also uses: allowed, or not. A's Cloyster is on Dahlia (an optional Brain), Swampert on May, and Hariyama on Maylene's rematch; none is a mandatory fight near Cyrus 1. Recommended: allowed.

Next steps once Ian has answered. Stage 4, the sets for his pick, with legality, items and natures, and the Speed tiers named below: about an hour. The Overseer's scorer reading of the new team, with Argo 1 beside it: about four hours of machine time. If the reading lands outside 75 to 85, the first dials to turn are named in each shape's section.

## Stage 3: the candidates and three shapes

### How the candidates were found

Every Oxide species that is fully evolved, has a base stat total of 455 or more and is not a legendary went through the sweep: 267 species. Ultra Beasts and Megas were then left out of the ranking. Each was built at 45 (31 IVs, no EVs, a neutral nature, no item) in each of its three ability slots. Its moves were its legal trainer palette at 45, from the Kaizo study's checker: level-up moves, egg moves, TMs, tutor moves and the TMs from before the TM pass. The calculator gave its best move on each of 32 answers from the three boxes (at 47, Hardy, IVs 15, with the four moves the reading's search gave them), and each answer's best hit on it. Conditional, charging and half-recoil moves were left out of the ranking: Solar Beam without sun, Meteor Beam, Water Spout, Eruption, and the beams that cost half the damage dealt.

Two things came out of it. Damage is not what limits the team. Any strong species with a special Grass, Water or Ice move takes half or more off the Ground walls, which are specially frail, and Focus Blast, an old TM many palettes keep, takes half off Bastiodon and Probopass for many of them. What limits it is what the walls do back, with Earthquake, Rock moves and Golem's Fire Punch, and which member the AI sends into which wall. So the useful picks are those the walls cannot hurt, and each was then checked inside a whole team.

### The candidates by need

Figures are the lowest to highest roll as a percent of the answer's HP, from the shape runs (with the shape's items; the player's item left out). An asterisk marks a sure one-hit knockout.

| Need (from stage 2) | Candidates looked at | What the kept picks do |
|---|---|---|
| The Ground walls: Hippowdon, Quagsire, Donphan, Golem, Palossand | Grass: Meganium, Venusaur, Tangrowth, Roserade, Sceptile, Ludicolo. Water: Swampert, Cloyster. Ice: Porygon-Z's Ice Beam | Meganium's Energy Ball: Quagsire 187 to 222*, Golem*, Palossand*, Donphan*, Hippowdon half or more. Swampert's Waterfall on Golem 95 to 117. Cloyster's Hydro Pump on Golem 187 to 220* |
| The Rock and Steel walls: Bastiodon, Probopass, Garganacl, Crustle | Hariyama, Machamp, Swampert, Nidoking, Electivire with Adaptability, Kommo-o, Lucario, Mamoswine, Metagross | Hariyama's Close Combat: Bastiodon 125 to 148*, Probopass 153 to 181*. Swampert's Earthquake: Bastiodon 77 to 92, Probopass 97 to 113. Electivire's Adaptability Brick Break: Bastiodon 97 to 118 |
| Palossand | Cloyster, Meganium, Porygon-Z's Shadow Ball, Honchkrow | Cloyster's Icicle Spear 104 to 125*, Meganium's Energy Ball one hit, Honchkrow's Crunch 89 to 106 |
| Salamence's answers: Manaphy and Alolan Ninetales | Meganium, Hariyama, Electivire, Magmortar, Cloyster, Crobat | Meganium's Energy Ball on Manaphy 73 to 87, and Thick Fat halves Ninetales's Triple Axel to 43 to 53. Electivire's Thunder Punch on Manaphy 112 to 133*. Magmortar's Flamethrower on Ninetales 95 to 113, at 110 Speed over its 106 |
| A lead with a job | Spikes: Cloyster, Forretress, Froslass, Glalie, Omastar, Qwilfish, Greninja, Cacturne, Klefki. Stealth Rock: Swampert, Mamoswine, Ferrothorn. Toxic Spikes: Nidoking, Drapion, Glimmora | Cloyster sets Spikes; Swampert sets Stealth Rock in C |

Left out, and why:

- Gyarados, Weavile and Houndoom: Ian keeps them for Cyrus 2 and 3. The species now on those two files (Skarmory, Magnezone, Dusknoir, Suicune, Heatran, Flygon, Regirock) were set aside too, for the no-repeat theme, though neither file is redesigned yet.
- Lucario and the Kommo-o line (Maylene, and Riley in this same split), Poliwrath (Riley), Ludicolo (Wake), Metagross (Byron), Decidueye (Fantina), Roserade and Exeggutor (Gardenia; Roserade also Cynthia), Tangrowth (Jupiter's theme), Mamoswine and Abomasnow (Candice, and Moira's Ice): each is on a boss the player meets near Cyrus 1. Kommo-o took half its HP from only one core answer in the sweep (Alolan Ninetales), and is the first swap if Ian wants one.
- Ferrothorn: Oxide's palette gives it no Spikes, so as a lead it needs an egg-list addition.
- Rhyperior and Steelix: Saturn's slow giants.
- Legendaries: one before Cyrus 3 would be a ruling of its own, and no need above calls for one.

### Shape A: Spikes, then the walls' own weaknesses

| Member | Level | Ability | Item | Nature | Speed | The moves the shape needs |
|---|---|---|---|---|---|---|
| Cloyster (lead) | 45 | Skill Link | Never-Melt Ice | Impish | 81 | Spikes, Icicle Spear, Rock Blast, Hydro Pump |
| Honchkrow | 46 | Super Luck | Black Glasses | Adamant | 102 | as today |
| Hariyama | 44 | Thick Fat | Black Belt | Brave | 55 | Close Combat, Bullet Punch, Knock Off, Bulk Up |
| Swampert | 45 | Torrent | Leftovers | Hardy | 72 | Earthquake, Waterfall, Ice Punch, Rock Slide |
| Meganium | 44 | Thick Fat | Miracle Seed | Modest | 89 | Energy Ball, Earthquake, Iron Tail, Synthesis |
| Salamence (ace) | 47 | Intimidate | Yache Berry | Naughty | 113 | as today |

The lead's job is Spikes. Against the leads the player brings today, Cloyster wins or works freely. Golem takes 187 to 220 percent from Hydro Pump. Bastiodon and Probopass take 36 to 45 and hit back for 23 to 47, so Cloyster lays Spikes in front of them; the Taunt both of them carry is what stops it. Its answers are the Electric types, Luxray (Wild Charge 53 to 63) and Rotom, and special hits on its low Special Defence. Luxray draws in Hariyama, whose Close Combat knocks it out (159 to 189) and who carries Bulk Up, so the player's switch hands it a free turn: Ian's lead test passes there. Rotom draws in Honchkrow, whose Crunch knocks Rotom out in one hit, though without setup.

Who the replacement rule sends in, on all three boxes:

| The player's Pokemon in front | Comes in |
|---|---|
| Golem, Crustle, Hippowdon, Donphan, Onix, Palossand, Corviknight | Cloyster while it stands; once it is gone, Swampert (Golem, Crustle, Onix), Meganium (Hippowdon, Donphan, Palossand) or Honchkrow (Corviknight) |
| Bastiodon, Probopass | Swampert |
| Garganacl, Luxray, Empoleon, Alolan Ninetales | Hariyama |
| Quagsire, Manaphy, Whiscash, Jellicent | Meganium |
| Rotom, Bronzong, Araquanid | Honchkrow (Salamence against Bronzong once Honchkrow is gone) |

Each member drawn in takes half or more off the Pokemon it is drawn into with its lowest roll, except Honchkrow against Bronzong and Corviknight (Heat Wave, 46 to 55 on Corviknight). No answer in the three boxes takes half of Swampert's HP with its lowest roll. Meganium takes half or more only from Crustle's X-Scissor and Corviknight's Dual Wingbeat. Against A the screen's sixes move to Bastiodon and Crustle (all 20 of the top 20 on boxes 2 and 3), the player's own Crobat (14 to 20 of 20; Poison and Flying resist Fighting and Grass and ignore Earthquake, and Cloyster's Ice and Rock moves and Honchkrow are its checks), Heracross, Glimmora and Corviknight. That is a new plan for the player to find, with type answers, rather than one wall class that beats the whole team.

Speed tiers to settle in stage 4. Hariyama, Brave, sits at 55, one point over Golem and Crustle (54) and under Hippowdon (56) and Donphan (59); a neutral nature puts it at 62, over every wall. Cloyster (81) and Meganium (89) sit under Rotom (97), Luxray (101), and Manaphy and Ninetales (106). The first dials if A reads too easy: Hariyama's nature, a second layer of Spikes, and Meganium's item. If it reads too hard: Cloyster's Spikes for Stealth Rock, and Swampert's Leftovers.

Tried and dropped: A with Venusaur in Meganium's place. The rule sent Venusaur into Alolan Ninetales, which outspeeds it and takes 97 to 118 percent with Triple Axel; Meganium's Thick Fat halves that hit, and the rule then sends Hariyama, with Bullet Punch, instead. The screen read the same (13.6, 13.0, 12.2).

### Shape B: Crobat's U-turn into the answer

| Member | Level | Ability | Item | Nature | Speed | The moves the shape needs |
|---|---|---|---|---|---|---|
| Crobat (lead) | 45 | Inner Focus | Razor Fang | Jolly | 148 | as today |
| Honchkrow | 46 | Super Luck | Black Glasses | Adamant | 102 | as today |
| Machamp | 45 | No Guard | Black Belt | Brave | 61 | Dynamic Punch, Stone Edge, Ice Punch, Bulk Up |
| Nidoking | 44 | Sheer Force | Soft Sand | Modest | 93 | Earth Power, Sludge Bomb, Ice Beam, Surf |
| Meganium | 44 | Thick Fat | Leftovers | Calm | 89 | Energy Ball, Earthquake, Knock Off, Synthesis |
| Salamence (ace) | 47 | Intimidate | Lum Berry | Naughty | 113 | as today |

The lead's job is to pivot. Crobat's answers, the Rock and Steel leads, now draw in Machamp against Golem, Crustle and Garganacl (with Bulk Up, so the lead test passes there) and Nidoking against Bastiodon and Probopass, which Earth Power and Earthquake knock out in one hit. Meganium is drawn into the Ground and Water walls. The fault is what the screen finds: Gengar and Bronzong (Levitate), Corviknight, Staraptor and Orbeetle, which Nidoking's Ground moves and Machamp's Fighting moves miss or barely touch. Crobat itself still takes half off only Ninetales, Jellicent and Araquanid, and Nidoking falls to one Earthquake from Golem. The screen hardly moves (16.3, 15.7, 16.7).

Tried and dropped: B with today's Magmortar in Nidoking's place, so that only two species are new. The screen read as today's (17.8, 16.7, 17.5).

### Shape C: the draft's dials back, Swampert for Crobat

| Member | Level | Ability | Item | Nature | Speed | The moves the shape needs |
|---|---|---|---|---|---|---|
| Swampert (lead) | 45 | Torrent | Leftovers | Brave | 64 | Stealth Rock, Earthquake, Waterfall, Ice Punch |
| Honchkrow | 46 | Super Luck | Black Glasses | Adamant | 102 | as today |
| Porygon-Z | 45 | Download | Silk Scarf | Modest | 99 | Tri Attack, Thunderbolt, Ice Beam, Shadow Ball (the draft's) |
| Electivire | 44 | Adaptability | Expert Belt | Naive | 122 | Thunder Punch, Brick Break, Ice Punch, Earthquake (the draft's) |
| Magmortar | 44 | Flame Body | Charcoal | Timid | 110 | as today |
| Salamence (ace) | 47 | Intimidate | Yache Berry | Naughty | 113 | as today |

The lead's job is Stealth Rock and damage. No answer in the boxes takes half of Swampert's HP with its lowest roll, and it hits most walls hard; Golem, Probopass, Luxray and Onix fall to one hit. Its answers are Grass types (Tsareena, Leavanny, Breloom, Leafeon and Abomasnow, which the screen now favours), and they draw in Magmortar, which beats them without setup, so the lead test passes only by half.

The bait order has one weak point. While Swampert stands, the rule sends it into every Rock, Steel and Ground wall. Once it is gone, it sends Electivire, and Golem, Hippowdon and Donphan still knock Electivire out with one Earthquake. So the old trap returns late in the fight. Manaphy draws in Electivire, whose Thunder Punch knocks it out (112 to 133); Ninetales draws in Magmortar, which outspeeds it. Quagsire stays in all 20 of box 1's top sixes, beside Abomasnow. Porygon-Z's figures leave out Download's raise, which the battle applies on entry.

This shape reads hardest on the screen (11.7, 11.6, 10.9). Its two drafted members, with today's other four, read on the probe as far harder than any accepted fight at these levels (52 rough wins of 900, against Wake's 378). With Swampert on top, it is the shape likeliest to put a box under Ian's floor of 60.

### An engine rule the shapes meet

The replacement rule adds the candidate's two type scores into one byte, as the engine does, so a total over 255 wraps. A pure Fighting type against Bastiodon or Probopass scores 160 twice, 320, which wraps to 64, so the rule passes over Hariyama and Machamp there even though their Fighting moves hit four times. A shape that wants its Fighting member drawn into Bastiodon needs a Fighting dual type. This is the engine's own rule, which the simulator mirrors; nothing here changes it.

## Stages 1 and 2: the summary as Ian read it

The scorer wins Cyrus 1 on 98 percent of fights over goal 3's three boxes (96, 100 and 97), above Ian's 95 percent ceiling for a boss and easier than any boss read so far; only Moira 1's earlier team, an officer fight, read easier. The player loses about one Pokemon a fight. The reading is run `cyrus-1-61b9d0391`, on the team in the game today.

The fight is easy because every member is walled by a type each box holds eight to ten of. Cyrus's six are three Flying types, an Electric, a Fire and a Normal type, and the box at Celestic is full of Rock, Steel and Ground Pokemon. Rock and Steel resist almost all of his attacks, and Ground is immune to Electric and knocks out the Electric and Fire members with one Earthquake, or nearly. Of his 24 moves, none is super effective on Quagsire or Crustle, and only Electivire's Ice Punch is on Hippowdon, whose Thick Fat halves it. Palossand takes nothing at all from Porygon-Z. The trainer AI then makes it worse: against a pure Ground type, Electivire is the only member with a super-effective move, so the AI sends it in, and the wall knocks it out at once.

Golem is in all three of the scorer's sixes, and nearly every six the search played out won 84 percent of its fights or more. Salamence makes half the knockouts and Honchkrow a fifth. Crobat, Electivire and Porygon-Z together make an eighth. The softening of 2026-10-31 removed Brick Break, Adaptability, Ice Beam and Shadow Ball, the moves that reached the walls. That softening was judged on the outcome probe, whose player never switches, and this fight is won by switching each member into its wall.

What Ian decided on (his answers are at the top of the page):

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

Stage 1's damage and Speed figures come from three short scripts in `/home/ian/.claude/jobs/cyrus-1-redesign/`, run from this branch's worktree under `tools/oxide/capped`. Each builds the reading's fight with goal 3's own setup (`plgoal3.setup` and `fight_state`, seeds 1 to 3, the box at 47, a fresh run name) and reads the calculator rows the scorer reads. `dmg.py` gives each Cyrus member's best move on each chosen catch and the reverse, `pair.py` every move of a named pair, and `abil.py` the catches' abilities and stats. Cyrus's members are limited to their four moves; the player's to the moves the scorer gave them. The replacement rule's picks were worked by hand from `fightai.replacement` and the type chart, not run.

Stage 3's figures come from scripts in `/home/ian/.claude/jobs/cyrus-1-redesign/s3/`, run the same way. `walls.py` takes the 32 answers from the three boxes with the reading's four moves for each. `sweep.py` runs the whole-Pokedex sweep through the calculator's own runner in one Node process, and `rank.py` and `detail.py` read it. `shape.py` swaps a whole party into the trainer file in memory and builds the reading's fight on each box with it. It prints each member's best move on each answer and the reverse, from the scorer's own calculator rows with the shape's items, and who `fightai.replacement` sends in against each answer as each member leaves, run on a battle built by `perfectline.make_battle`. It also prints the matchup screen's top sixes. `digest.py` condenses its output. Legality was checked with the Kaizo study's checker (`oxide.legal_moves`, with the TMs from before the TM pass); every move the shapes name is in its species' palette at its level. No scorer, probe or simulator change was run, and `res/` was not written.

Stage 4's sets were written by `/home/ian/.claude/jobs/cyrus-1-redesign/s4/apply.py` through `trainers.save`, from `sets.json` beside it. `legal.py` there runs the OxiDex's check, `tiers.py` gives the Speed tiers against each whole box and Porygon-Z's Download figures (the calculator's runner with the stage given as a boost), and the replacement trace is `s3/shape.py today`, which reads the file as written.
