# Lucas and Dawn's pool, and Jubilife at four a side

Ian, 2026-11-01: "I'd also like to do a Dawn/Lucas team pool similar to how we made the Barry pool, as their team is pretty static across the entire game", and, on the Jubilife tag battle reading easier than Officer Somnu 1, "Have lucas/dawn go to 4 members (and not lead with their starters) and phobos/deimos go to 4 members." Part 1 is the pool, in the shape of `barry-pool.md`'s Part 1. Part 2 is Jubilife, built from the pool. Part 3 is what Ian's answers changed: Pal Park's partner and Lucas and Dawn 3. All of it is on the branch `overseer-lucas-dawn-pool`; nothing has been seen in game, and nothing lands until the Overseer lands the branch.

## Ian's answers (2026-11-01)

To the six questions at the end of this page:

1. Jubilife stays as built, with Totodile (question 6).
2. The pool stands as drafted (question 1).
3. Rotation B (question 2): at Pal Park the partner fields Nidoqueen in Gastrodon's seat and Slowbro in Pachirisu's, at that partner's levels, with sets as plain as the rest of it. The Veilstone partner and Lucas and Dawn 2 do not change.
4. Lucas and Dawn 3 takes Typhlosion's line in place of Magmortar as its Fire member, in every file (question 3).
5. The nature fix for Lucas and Dawn 3: Lickilicky Impish in all six files, Empoleon Quiet in the Turtwig player's version, Torterra Brave in the Scorbunny player's (question 4).
6. Lucas's Route 202 Chimchar lists Scratch, Leer, Ember and Taunt (question 5).

All six are applied on this branch.

## Summary

**Outcome.** The counterpart's team is static from Route 207 to Pal Park: Lucas and Dawn 2, the Veilstone partner and the Pal Park partner are one six (Umbreon, Scyther, Lopunny, Pachirisu, Gastrodon and the starter) raised by ten levels a time, and only Scyther evolves. Lucas and Dawn 3 then brings a new six that keeps only Umbreon and the starter. The pool keeps every line Ian had chosen, with Typhlosion's in Magmortar's place, eleven in all, in seats: the early lines hand their seats on to Lucas and Dawn 3's lines, and Pal Park's partner now fields two of them early. It reads the pair as Professor Rowan's assistant: Rowan studies evolution, and Lucas and Dawn 3 is built on Sinnoh's evolutions of older lines (Lickilicky, Tangrowth) and, with Typhlosion, on Hisui, Sinnoh's own past.

Jubilife is now four a side in all eight files. Phobos adds Totodile and Deimos adds Snorunt, the young of Pal Park's Feraligatr and Froslass, so every Pal Park member but Mawile and Absol grows out of a Jubilife one. Lucas or Dawn brings Eevee, Buneary and Pachirisu at 16 and the starter last at 17. The trainer lint, the packer, test_b1 (50 of 50, with a new check on the sizes), test_trainers (44 of 44) and the learnset tests (6 of 6 and 18 of 18) pass; no move needed an egg list. The matchup screen reads each officer's member about as before, so the fight is harder by numbers (eight against ten, where it was six against eight) and by a second spread Icy Wind, which the screen does not count.

| Jubilife on the screen, per officer member | Reading |
|---|---:|
| Four a side, this branch | 2.96 |
| Three and two, as set on 2026-10-31 | 2.79 |
| Somnu 1 | 1.71 |

Lucas and Dawn 3 now fields Typhlosion at 67 (Modest, Wise Glasses, Flash Fire; Lava Plume, Infernal Parade, Will-O-Wisp, Focus Blast) and has no repeated nature. On the matchup screen it reads a little easier than before, mostly because the new six has no answer to the Water types Magmortar's Thunderbolt hit (Part 3). Every move is legal at its level, no item or nature repeats, the trainer lint and the packer pass on all fifteen changed files, and test_b1, test_trainers and the learnset tests pass.

**What Ian decides.** One question, from the new readings: Typhlosion has nothing for the box's Water walls (Milotic, Mantine, Wailord, Primarina), which now join the screen's best sixes. Keep the burn set, or swap Will-O-Wisp for Solar Beam? Recommended: keep it, since the screen counts neither the burn nor Infernal Parade's doubled power, and the burn plan is the set's idea.

**Next steps.** Ian's in-game checks: Jubilife from a save after Roark (about 15 minutes), Pal Park from one after Celestic (about 15 minutes), and Lucas and Dawn 3 at Victory Road from the test kit (about 15 minutes). A Typhlosion swap, if he wants one, is 15 minutes and a re-run of the checks, about 50 minutes.

## Part 1: the pool

### How static the team is

Every Lucas and Dawn file on `oxide`, read on 2026-11-01. Dawn's and Lucas's copies of a version are the same team.

| Fight (split) | Files | Members |
|---|---|---|
| Lucas and Dawn 1, Route 202 (Roark) | `dummy_787` to `792` | the starter alone at 9 |
| Jubilife partner (Gardenia) | `lucas_` and `dawn_jubilife_city_*` | until this branch, the starter at 17 and Pachirisu at 16 |
| Lucas and Dawn 2, Route 207 (Fantina) | `dummy_793`, `794`, `799` to `802` | Umbreon 29, Scyther 29, Lopunny 30, Pachirisu 28, Gastrodon 29, the starter's second stage at 31 |
| Veilstone partner, beside the player against Tyche and Hermes 1 (Wake) | `lucas_` and `dawn_veilstone_city_*` | the same six at 39 to 41, with new sets, the starter now final |
| Pal Park partner, against Phobos and Deimos 2 (Byron) | `dummy_051`, `052`, `054`, `062` to `064` | the same six at 47 to 49, Scyther now Scizor |
| Lucas and Dawn 3, Victory Road (Barry) | `dummy_779` to `784` | Nidoqueen 66, Umbreon 66, Lickilicky 67, two of Slowbro, Tangrowth and Magmortar at 66 or 67, the starter at 68 |

So one six spans three fights in three splits, and the last fight replaces four of its six at once. The scripts call no other Lucas or Dawn file. The table is the record of the files before Ian's answers; since then Pal Park's partner fields Nidoqueen and Slowbro, and Lucas and Dawn 3 fields Typhlosion where it had Magmortar.

### How the versions work

The scripts pick the file by the player's starter, and the counterpart takes the line the player's own starter beats (`lucas-dawn-2-redesign.md`, "Which starter meets which team"): Piplup's line for a Turtwig player, Turtwig's for a Scorbunny player, Chimchar's for a Piplup player. Lucas and Dawn 3 adds the two elements the starter lacks, as Barry's pool does: Tangrowth and Typhlosion beside Empoleon, Slowbro and Typhlosion beside Torterra, Slowbro and Tangrowth beside Infernape (Typhlosion in Magmortar's place since Ian's answer of 2026-11-01). The pool keeps both rules.

### The fights, and the bosses around them

| Fight | Bosses around it | Kept out of the pool there, or rested |
|---|---|---|
| Lucas and Dawn 1 (Route 202, 9) | Barry 1 and 2, Roark | nothing: the starter alone |
| Jubilife partner (16, 17) | Roark; the officers themselves; Somnu 1, Mars 1, Gardenia | the officers' eight lines, Somnu 1's Munchlax and Butterfree, Mars's cats, Gardenia's Grass types |
| Lucas and Dawn 2 (Route 207, cap 31) | Jupiter 1, Moira 1, Fantina, Barry 3 | Tangela (Jupiter 1, one fight before), the Slowpoke line (Moira 1's Psychic types, next to it in play order) |
| Veilstone partner (39 to 41) | Maylene, Tyche and Hermes 1, Barry 4, Wake | Nidoqueen (Wake's Clodsire, Poison and Ground, comes next) |
| Pal Park partner (47 to 49) | Cyrus 1, Thorton, Phobos and Deimos 2, Barry 5, Byron; Mars 2 and Saturn 1 just after | Lickilicky (Saturn 1, one split later) |
| Lucas and Dawn 3 (Victory Road, 66 to 68) | Volkner, Flint and Volkner, Barry 6, the Elite Four | Scizor (Aaron); Magmortar (Flint, at the Fight Area and in the League), so Typhlosion took its seat |

Three overlaps remain in Lucas and Dawn 3, Ian's own six, and he kept them. Magmortar's, with Flint's at the Fight Area and in the League, was a fourth, and Typhlosion took its seat. Slowbro shares its line with Lucian's Slowking. Umbreon is on Mars 2 and on Mars and Jupiter at Spear Pillar, and Ian kept it on 2026-10-21. Tangrowth is on Mars and Jupiter, two splits earlier. The starter is the exception Barry's pool makes too: the Piplup player's counterpart keeps Infernape, which Flint carries.

### The pool

Eleven lines in six seats. A seat is a role a line holds, and a later line takes it over. The early lines are Sinnoh natives and first stages, the mid lines the six Ian built for Route 207, and the late lines Lucas and Dawn 3's, most of them Sinnoh's evolutions of older lines.

| Seat | Line | Fights | Role | Why Lucas or Dawn |
|---|---|---|---|---|
| Ace | the starter (Piplup, Turtwig or Chimchar line) | all | the ace, the line the player's starter beats | canon |
| Lead | Eevee line (Umbreon) | Jubilife on | the bulky Dark lead: Yawn, Reflect, Foul Play | Eevee is the textbook subject of evolution research, the field of Professor Rowan, whose assistant the pair is; Ian kept Umbreon for both later fights |
| Normal | Buneary line (Lopunny) | Jubilife to Pal Park | the fast threat off the lead: Fake Out, Scrappy's Jump Kick | a Sinnoh native, the anime Dawn's Buneary |
| Normal, late | Lickitung line (Lickilicky) | Lucas and Dawn 3 | the slow bulky attacker, Toxic Orb and Guts | an evolution Sinnoh revealed, by learning Rollout |
| Electric | Pachirisu | Jubilife to Veilstone | Electroweb and Spark into the Flying and Water types | a Sinnoh native, the anime Dawn's Pachirisu; Ian kept it on 2026-10-21 |
| Bug | Scyther line (Scizor) | Lucas and Dawn 2 to Pal Park | Technician's Wing Attack and Pursuit | a held-item evolution, Metal Coat |
| Ground | Shellos line (Gastrodon) | Lucas and Dawn 2, Veilstone | Dry Skin, Earth Power, Stealth Rock | Sinnoh's East and West Sea forms, the region's own research subject |
| Ground, late | Nidoran line (Nidoqueen) | Pal Park, Lucas and Dawn 3 | Toxic Spikes and Earthquake | a Moon Stone evolution, and Lucas and Dawn 3's first member |
| Water partner | Slowpoke line (Slowbro) | Pal Park (in Pachirisu's seat), Lucas and Dawn 3 (two versions) | the slow special wall, Trick Room in one version | a line with two evolutions, by two different means |
| Grass partner | Tangela line (Tangrowth) | Lucas and Dawn 3 (two versions) | Leaf Storm and Sleep Powder behind a Defense of 125 | an evolution Sinnoh revealed, by learning Ancient Power |
| Fire partner | Cyndaquil line (Typhlosion) | Lucas and Dawn 3 (two versions) | special Fire: Lava Plume and Will-O-Wisp burn, and Infernal Parade hits a burned foe twice as hard | Hisui is Sinnoh's own past, which the pair's research reaches into, and Infernal Parade is the Hisuian form's move; the anime Dawn trained a Cyndaquil |

The pool grows harder by entry, in Oxide's stat totals: Jubilife's first stages are 325 to 350 beside Pachirisu's 445, Route 207's six are 475 to 525, and Lucas and Dawn 3's late lines are 490 to 535. That is eleven of the brief's nine to twelve. Ian can name a twelfth; none is needed to fill the fights.

### The pool against the fights

Each column is what the counterpart brings, on this branch since Ian's answers. A member that changed on 2026-11-01 is in bold.

| Seat | L&D 1 (9) | Jubilife (16, 17) | L&D 2 (28 to 31) | Veilstone (39 to 41) | Pal Park (47 to 49) | L&D 3 (66 to 68) |
|---|---|---|---|---|---|---|
| Ace | first stage | second stage (the Scorbunny player's partner: Turtwig, first stage) | second stage | final | final | final |
| Lead | | Eevee | Umbreon | Umbreon | Umbreon | Umbreon |
| Normal | | Buneary | Lopunny | Lopunny | Lopunny | |
| Normal, late | | | | | | Lickilicky |
| Electric | | Pachirisu | Pachirisu | Pachirisu | | |
| Water partner | | | | | **Slowbro** | Slowbro (two versions) |
| Bug | | | Scyther | Scyther | Scizor | |
| Ground | | | Gastrodon | Gastrodon | **Nidoqueen** | Nidoqueen |
| Other partners | | | | | | Tangrowth (two versions), **Typhlosion** (two versions) |

So the player meets four of Lucas and Dawn 3's lines before Victory Road (Umbreon, Nidoqueen, Slowbro in two versions, and the starter). Lickilicky stays out of Pal Park for Saturn 1, one split later. A partner's strength is a dial on a double's difficulty, and the two new members make Pal Park a little easier for the player (Part 3).

### Legality by level

Every stage in the table is one a trainer can have at that fight's level. The close ones:

| Member | Fight | Level | Evolves at |
|---|---|---|---|
| Turtwig (the Scorbunny player's partner) | Jubilife | 17 | Grotle at 18 |
| Buneary | Jubilife | 16 | Lopunny at 20 |
| Gastrodon | Lucas and Dawn 2 | 29 | Shellos at 30 |
| Grotle, Monferno, Prinplup | Lucas and Dawn 2 | 31 | Torterra at 32, the others at 36 |
| Nidoqueen | Pal Park | 48 | Nidorina at 16, then a Moon Stone |
| Slowbro | Pal Park | 47 | Slowpoke at 37 |
| Typhlosion | Lucas and Dawn 3 | 67 | Quilava at 36 |

Umbreon (a Moon Stone in Oxide), Scizor (a Metal Coat) and Lickilicky (knowing Rollout) have no level bar. Tangrowth evolves at 35 or on learning Ancient Power.

Every move in all thirty files is on its species' Oxide list at its level but two, both in Lucas and Dawn 3: Umbreon's Protect in all six files and the Turtwig version's Empoleon's Roar. Neither move is on any Oxide list. Both are legal by the ruling that lets trainers use any move from Cyrus 3's split on.

### Faults found, fixed on Ian's answers

Lucas and Dawn 3 repeated natures in every version; its items did not repeat. Ian took the fix on 2026-11-01, one or two natures a version and no move:

| Files | Repeats before | Now |
|---|---|---|
| `dummy_779`, `782` (Turtwig player) | Adamant: Nidoqueen and Lickilicky; Modest: Magmortar and Empoleon | Lickilicky Impish; Empoleon Quiet |
| `dummy_780`, `783` (Scorbunny player) | Adamant: Nidoqueen, Lickilicky and Torterra | Lickilicky Impish; Torterra Brave |
| `dummy_781`, `784` (Piplup player) | Adamant: Nidoqueen and Lickilicky | Lickilicky Impish |

Impish keeps Lickilicky's Attack neutral and raises its Defense, which suits a Toxic Orb Guts wall. Quiet and Brave lower Empoleon's and Torterra's Speed, which is already under most of a level 71 box.

`dummy_792`, Lucas's Route 202 Chimchar, listed no moves. Chimchar's last four by level 9 are Scratch, Leer, Ember and Taunt, the four Dawn's `dummy_789` lists, and the file now lists them, so nothing changes in play.

## Part 2: Jubilife at four a side

Gardenia's split, after Roark and before Somnu 1 and Mars 1. Mars 1's honour cap of 20 is in force, so the officers' aces stay at 18 and the rest at 17. Every officer member has iv_scale 255, its own item and its own nature. Both officers keep Basic, Evaluate Attack, Expert and Harassment by `battle-ai/flags-guide.md`: each still carries two or more of Harassment's status moves, and neither new member brings a trade move, a crit idea or a weather move.

Officer Phobos, fear:

| Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|
| Growlithe (lead) | 17 | Intimidate | Sitrus Berry | Careful | Flamethrower, Crunch, Will-O-Wisp, Leer | 30 |
| Houndour | 17 | Unnerve | BlackGlasses | Mild | Snarl, Dark Pulse, Ember, Taunt | 32 |
| Totodile (new) | 17 | Torrent | Rindo Berry | Lonely | Waterfall, Bite, Ice Punch, Scary Face | 24 |
| Snubbull (ace) | 18 | Intimidate | Oran Berry | Sassy | Charm, Play Rough, Ice Fang, Stomping Tantrum | 18 |

Officer Deimos, dread:

| Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|
| Joltik (lead) | 17 | Unnerve | Oran Berry | Hasty | Electroweb, Giga Drain, String Shot, Light Screen | 35 |
| Surskit | 17 | Swift Swim | Mystic Water | Quiet | Icy Wind, Scary Face, Water Pulse, Struggle Bug | 28 |
| Snorunt (new) | 17 | Snow Cloak | Eviolite | Naive | Icy Wind, Shadow Ball, Water Pulse, Bite | 29 |
| Ekans (ace) | 18 | Unnerve | Poison Barb | Naughty | Glare, Poison Jab, Bite, Rock Tomb | 30 |

The partner, in all six files: Lucas and Dawn 2's order with each member a stage young, plain sets (iv_scale 200, a simple berry each, no nature set).

| Member | Level | Item | Moves |
|---|---|---|---|
| Eevee (lead) | 16 | Rawst Berry | Swift, Dig, Yawn, Helping Hand |
| Buneary | 16 | Cheri Berry | Double Kick, Double Hit, Quick Attack, Baby-Doll Eyes |
| Pachirisu | 16 | Sitrus Berry | Spark, Electroweb, Quick Attack, Charm |
| Prinplup (`_turtwig`) | 17 | Oran Berry | Chilling Water, Metal Claw, Peck, Growl |
| Turtwig (`_chimchar`, the Scorbunny player) | 17 | Oran Berry | Razor Leaf, Bullet Seed, Rock Blast, Withdraw |
| Monferno (`_piplup`) | 17 | Oran Berry | Flame Wheel, Mach Punch, Fury Swipes, Leer |

Why these two officers' members. Totodile and Snorunt are the first stages of Feraligatr and Froslass, two of Pal Park's four new members, with the same natures they have there. Totodile's Water covers the Rock and Ground types that wall Phobos's two Fire types (Nosepass, Nacli and Phanpy draw it in, and so do the Fire types Ponyta and Raboot), and Bite, Waterfall's flinch and Scary Face keep it on the fear theme. Snorunt adds Deimos's second spread Icy Wind. In a first set it carried Ice Beam and Never-Melt Ice, and the probe showed the AI choosing Ice Beam over Icy Wind nearly every time (Icy Wind 1 to 32 picks in 100 fights). With Icy Wind its only Ice move, the AI picks it 20 to 79 times. The Eviolite keeps it in long enough to fire. Snow Cloak does nothing without hail; Snorunt's other ability, Moody, is a luck ability, so it was left out.

Why these partner members. Ian asked for four that do not lead with the starter. Eevee, Buneary and Pachirisu are the first stages of the Route 207 six, so the pair's team now grows out of Jubilife as Pal Park grows out of the officers. Their stat totals (325, 350, 445) are low, so the partner adds numbers more than power, which suits a fight Ian wants harder.

### The cheap checks

The box is goal 3's, built with its own pieces from Somnu 1's row and cut to the catches of earlier splits, at level 18, as `phobos-deimos.md` built it; the partner's four join it, so the screen may take them into a six. Seeds 1 to 3 start with Turtwig, Scorbunny and Piplup and meet the partner file for that starter. The screen scores the best six of a box against a team by damage alone, one on one from full HP, higher meaning easier for the player. It counts no stat drop, no Intimidate and no double. Per member is the score divided by the officers' member count.

| Team | Box 1 | Box 2 | Box 3 | Per member |
|---|---:|---:|---:|---:|
| Four a side (this branch), with the partner's four | 23.05 | 23.20 | 24.70 | 2.96 |
| The same with Croconaw in Totodile's place | 23.05 | 23.20 | 24.70 | 2.96 |
| Three and two (2026-10-31), with the partner's two, run again on 2026-11-01 | 16.15 | 16.00 | 18.10 | 2.79 |
| Somnu 1 (four members), run again on 2026-11-01 | 5.70 | 7.70 | 7.15 | 1.71 |
| Mars 1 (five members), from `phobos-deimos.md`, not run again | 1.1 | -2.1 | 9.5 | 0.6 |

Catches in the screen's top 20 that beat each member one on one, boxes 1, 2 and 3:

| Member | Beaten by |
|---|---|
| Totodile | 9, 5, 8 |
| Croconaw (the variant) | 4, 3, 2 |
| Snorunt | 7, 6, 7 |
| Snubbull | 5, 2, 3 |
| Ekans | 8, 7, 8 |
| The other four | 5 to 14 |

Speed tiers. The officers run from Joltik 35 down through Houndour 32, Growlithe and Ekans 30, Snorunt 29, Surskit 28 and Totodile 24 to Snubbull 18. The boxes' fastest are Raboot 41, Ponyta 40, Pawmo 38 and Fletchinder 37, and most of each box sits at 25 to 36, so one Electroweb or Icy Wind puts most of it under the officers' 28 to 32 tier. The partner's Pachirisu (39) and Buneary (36) are faster than every officer, and its Eevee (26) slower than all but Totodile and Snubbull.

The replacement trace (who the AI sends in after a faint, by the engine's own rule, on a stand-in single team). Nosepass, Nacli, Ponyta, Raboot, Phanpy and the partner's Monferno draw Totodile. Onix and Geodude draw Surskit, and Grotle, Budew and Turtwig draw Growlithe, or Snorunt once Growlithe is gone. Bibarel, in every box, draws Joltik. Each reads as intended.

The AI-picks probe (a greedy player, 100 rough fights a six against the screen's best six and its six most taken, the officers read as one single team; win numbers mean nothing). Every move on every member was picked. The new members:

| Member | Picks per 100 fights | Note |
|---|---|---|
| Totodile | Waterfall 117 to 179, Scary Face 75 to 163, Bite 24 to 46, Ice Punch 18 to 48 | knocked out 67 to 108 of the player's Pokemon while in; its Rindo Berry fired 1 to 4 times |
| Snorunt | Bite 49 to 121, Water Pulse 48 to 105, Icy Wind 20 to 79, Shadow Ball 26 to 113 | knocked out 51 to 64 while in |

Growlithe still opens with Will-O-Wisp or Leer about nine times in ten.

What the screen cannot show. The double has eight officers' Pokemon against the player's six and the partner's four, where it had six against eight. Two Intimidates, Charm and Snarl cut the player's side, and Electroweb, two Icy Winds and two Scary Faces slow it, each spread move reaching the player's Pokemon and the partner's at once. So the fight plays harder than the screen reads, and harder than it did, though each member reads as no stronger one on one.

### How the numbers were made

All on this branch, with scratch scripts that write nothing under `res/`: `phobos-deimos.md`'s harness (`h.py` and `checks.py`, which build the box, read both officers as one trainer, and add the partner's members to the box), and the Fantina page's AI-picks probe on that harness. The teams went in through the OxiDex's own save (`trainers.save`: the trainer lint, the real packer and the registry of edited fields). Legality is the OxiDex's own list (`learnsets.oxide_list`) at each member's level. For Lucas and Dawn 3, the screen is `plgoal3 --run ld3-study --box lucas_dawn_3 <seed> --screen` and the probe is the Fantina page's on that fight, both run on the files before and after the change.

## Part 3: Ian's answers in the files

### Pal Park's partner, rotation B

Nidoqueen takes Gastrodon's seat and Slowbro takes Pachirisu's, each at the seat's level and IVs, in the partner's plain style. Every move hits one target, so neither hurts the player's Pokemon beside it.

| Member | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen (for Gastrodon) | 48 | Battle Armor | Black Sludge | Modest | Earth Power, Sludge Bomb, Ice Beam, Toxic Spikes |
| Slowbro (for Pachirisu) | 47 | Regenerator | Sitrus Berry | Calm | Psychic, Water Pulse, Yawn, Slack Off |

How the sides weigh now. The partner gains about a hundred points of stat total and two slow, bulky members, and it loses Pachirisu's Electroweb and Gastrodon's Stealth Rock. Slowbro resists the Fire of Arcanine and Houndoom and the Ice of Froslass, but it takes the Dark moves of Absol, Houndoom and Granbull and Galvantula's Electric hits super-effectively. So the player's side has a little more bulk and less speed control against the officers' fast half, and the double reads a little easier for the player.

### Lucas and Dawn 3 with Typhlosion

Plain Typhlosion, because it is the only form Oxide has: the game carries no Hisuian Typhlosion, and adding a species is far outside this change. The Hisuian form's own move, Infernal Parade, is on Oxide's Typhlosion list at 48, so the set carries the Hisui idea anyway. Infernal Parade hits a foe with a status twice as hard, and Lava Plume and Will-O-Wisp give the status. Focus Blast is kept from Magmortar's set for the Rock types. Typhlosion takes Magmortar's level (67), item (Wise Glasses) and nature (Modest), none of them repeated in its team. Flash Fire, its hidden ability, takes the player's Fire moves. The AI flags stay as Ian set them (Basic, Evaluate Attack, Expert, Setup First Turn, Prioritize Extremes, Check HP); Prioritize Extremes lifts Will-O-Wisp, which suits the plan.

No boss carries the Cyndaquil line. Two ordinary trainers do: Collector Douglas in Wake's split and Ace Trainer Abel, a mini-boss, in the Galactic split, two splits before Victory Road.

| Files | Fire member | Nature fix |
|---|---|---|
| `dummy_779`, `782` (Turtwig player) | Typhlosion in Magmortar's place | Lickilicky Impish, Empoleon Quiet |
| `dummy_780`, `783` (Scorbunny player) | Typhlosion in Magmortar's place | Lickilicky Impish, Torterra Brave |
| `dummy_781`, `784` (Piplup player) | none (Slowbro and Tangrowth) | Lickilicky Impish |

The checks, on goal 3's boxes at 68; box 1 meets the Turtwig player's version, box 2 the Scorbunny player's and box 3 the Piplup player's, so box 3 shows the nature fix alone. Per member is the score divided by six; higher is easier for the player.

| Box | Before (Magmortar, old natures) | Per member | After | Per member |
|---|---:|---:|---:|---:|
| 1 | 20.35 | 3.39 | 22.00 | 3.67 |
| 2 | 17.95 | 2.99 | 20.10 | 3.35 |
| 3 | 19.75 | 3.29 | 19.90 | 3.32 |

Box 3 moves by 0.15, so Lickilicky's nature counts for little. On boxes 1 and 2 the rest comes from Typhlosion and from the slower Empoleon and Torterra (Speed 107 to 96 and 102 to 91). Water walls join the best sixes (Milotic and Mantine on box 1, Wailord and Primarina on box 2), since Typhlosion has no Thunderbolt for them as Magmortar had. The screen counts damage alone, so neither the burn nor Infernal Parade's doubled power reaches it; that is the summary's one question.

The AI-picks probe (a greedy player, 100 rough fights a six against the screen's best six and its six most taken; win numbers mean nothing):

| Member | Box | Picks per 100 fights | The player's Pokemon knocked out while in |
|---|---|---|---:|
| Magmortar, before | 1 | Focus Blast 167, Lava Plume 115, Thunderbolt 24, Psychic 10 | 107 |
| Magmortar, before | 2 | Focus Blast 134 to 145, Lava Plume 93 to 115, Thunderbolt 52 to 72, Psychic 18 to 20 | 118 to 159 |
| Typhlosion, after | 1 | Will-O-Wisp 93 to 109, Lava Plume 96 to 101, Infernal Parade 75 to 83, Focus Blast 62 to 64; switches 21 to 22 | 127 to 129 |
| Typhlosion, after | 2 | Infernal Parade 100 to 108, Lava Plume 96 to 99, Focus Blast 66 to 71, Will-O-Wisp 33 to 53 | 116 to 120 |

Every move on Typhlosion is picked, and Infernal Parade most where the burns have landed. Typhlosion's Speed at 67 is 159, against Magmortar's 150. Lickilicky still leads with Body Slam and Ice Punch after the fix.

## The six questions, as put on 2026-11-01

1. The pool: the eleven lines in the seats below, as drafted, or name changes. Recommended: as drafted; it adds no line Ian has not chosen.
2. How far the partner fights rotate. A: Pal Park's Nidoqueen takes Gastrodon's Ground seat, so Lucas and Dawn 3's first member is met once before Victory Road; Veilstone stays as set. B: A, and Slowbro takes Pachirisu's seat at Pal Park as well. C: both partners stay as set. Recommended: A, the smallest change that makes the team grow, and the one that moves each double's difficulty least.
3. Magmortar in Lucas and Dawn 3 sits one fight after Flint's Magmortar at the Fight Area and before Flint's in the League. Keep it, or take Typhlosion's line as the Fire partner? Recommended: keep it, since it is the clearest fit to the pair's evolution theme and two versions of three carry it.
4. Lucas and Dawn 3's files repeat natures, which the rule of 2026-10-12 forbids: Adamant twice or three times in every version, Modest twice in one. Fix them as the table in Part 1 proposes (Lickilicky Impish everywhere, Empoleon Quiet, Torterra Brave), or leave them? Recommended: fix.
5. Lucas's Route 202 Chimchar file lists no moves, so the game fills them; they come out as Dawn's four (Scratch, Leer, Ember, Taunt). List them in the file? Recommended: yes, nothing changes in play.
6. Jubilife's Totodile could be a Croconaw at 17, one level before Totodile's evolution. Croconaw is beaten one on one by two to four catches a box where Totodile is beaten by five to nine, but the screen's best six reads the same. Recommended: Totodile, since Ian softened both of Jubilife's walls on 2026-10-31.
