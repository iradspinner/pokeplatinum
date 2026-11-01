# Officers Phobos and Deimos

Ian asked on 2026-10-31 for two more named officers, the pair fought in Jubilife, to be the pair fought at Pal Park too. He named them Phobos and Deimos, the moons of Mars: fear and dread, her officers. This page holds both fights as built on the branch `overseer-phobos-deimos`. Nothing here has been seen in game, and nothing lands until the Overseer lands the branch.

## Summary

Outcome. Both fights are built on one theme, "fear saps, dread slows". Phobos lowers what the player hits with (Intimidate, Charm, Snarl, Will-O-Wisp). Deimos lowers how fast the player moves (Electroweb, Icy Wind, Scary Face, Sticky Web, Glare), so the officers' side moves first and the player's hits land weak. In a tag battle every Intimidate and every spread drop reaches the player's Pokemon and the partner's at once, which a single battle cannot do. Every Pal Park member but Mawile and Absol grows out of a Jubilife one, since Jubilife went to four a side (below).

Ian answered the questions on 2026-10-31 (below), and the fights now stand as he set them. Jubilife, with both its walls softened as he asked, reads easier than Officer Somnu 1 on the matchup screen, the earliest officer after it. On 2026-11-01 Ian took Jubilife to four a side ("Have lucas/dawn go to 4 members (and not lead with their starters) and phobos/deimos go to 4 members"), so eight officers' Pokemon now face ten; each member still reads about as before, 2.96 per member against 2.79 and Somnu 1's 1.71 (`lucas-dawn-pool.md`, Part 2). Pal Park reads harder than Tyche and Hermes do on their own boxes. It still reads easier than Argo 1 on the same box, and the gap is the level rule, not the sets (below).

Checked: the trainer lint and the real packer on all ten changed files, no move off its list at its level, `test_b1` 49 of 49, `test_b1e` 11 of 11, `test_learnrewrite` 6 of 6, `test_learncheck` 18 of 18, `test_trainers` 44 of 44, and `test_plgoal3` 71 of 72. Its one failure is the box-size check that fails on `oxide` too. The ROM builds, the bulk tools' dry runs write nothing, and the text check finds no unexpected difference. Not checked: no reading of either fight, since the simulator, the probe and goal 3 read single battles only.

Ian's answers (2026-10-31):

1. Theme A, fear saps and dread slows, as built.
2. Pal Park keeps every member at 47 and the aces at 48, the officer rule's levels.
3. and 4. "Both": both Jubilife walls softened. Deimos's ace is Ekans at 18, below its evolution level, with Arbok's set kept, and Snubbull holds an Oran Berry in place of its Eviolite.
5. Froslass keeps Destiny Bond, with Check HP.
6. The scene's lines (below) are still to read before landing.

Next steps. Ian's in-game check of both fights, about 30 minutes from a save after Roark and one after Celestic, or from the test kit. A spot-check reading is not possible for a tag battle.

## Which is which

Both officers are male grunts. The two Jubilife sprites are both the male grunt's, and Phobos and Deimos are sons of Ares in the myth, so Pal Park's second officer moved from the female grunt's sprite and class to the male's. Phobos is the one who speaks first in each scene and the first opponent in each battle: `galactic_grunt_jubilife_city_1` (trainer 414) and `dummy_009`. Deimos is `galactic_grunt_jubilife_city_2` (415) and `dummy_050`. Both carry the male grunt's class, as Tyche and Hermes carry the grunt classes, under names "Officer Phobos" and "Officer Deimos".

## The themes considered

A, fear saps and dread slows (built). Phobos is Intimidate and the attack drops; Deimos is Speed control. It suits a double best: Intimidate and Electroweb, Icy Wind and Snarl hit both the player and the partner. It grows cleanly from early lines (Growlithe, Snubbull, Houndour, Joltik, Surskit, Ekans) into Arcanine, Granbull, Houndoom, Galvantula, Masquerain and Arbok, all of which keep the idea. The player's answers are clear and fair: special attackers past Intimidate, switching to clear the drops, priority, Clear Body and the like. Its risk is the screen's blind spot: it counts none of the drops, so the fight plays harder than it reads.

B, Ghost and Dark menace. Phobos would bring Ghosts (Will-O-Wisp, Hex, Curse, Confuse Ray) and Deimos Darks (Snarl, Taunt, Sucker Punch, Pursuit). It is the most literal reading of fear, but it overlaps Fantina's gym and Cyrus's canon picks (Honchkrow, Houndoom, Weavile), and its early lines are few and frail.

C, paralysed with fear. Phobos would flinch (Fake Out, Bite, Rock Slide, King's Rock) and Deimos paralyse (Glare, Thunder Wave, Nuzzle, Static). It plays as luck: full paralysis and flinches decide turns, which reads as unfair in a no-loss run more than as difficult.

## Phobos and Deimos 1: Jubilife City

Gardenia's split, after Roark, before Somnu 1 and Mars 1. Mars 1's honour cap of 20 is in force, so the aces sit at 18, two under it. Four a side since 2026-11-01 (Ian: "Have lucas/dawn go to 4 members (and not lead with their starters) and phobos/deimos go to 4 members"); the new members, their reasons and the checks are in `lucas-dawn-pool.md`, Part 2. Every member has iv_scale 255. Both officers carry Basic, Evaluate Attack, Expert and Harassment: each team carries at least two of Harassment's status moves (Charm, Will-O-Wisp, Scary Face; Glare, Scary Face, String Shot), and the flag makes the AI reach for them. No trade move, weather move or crit idea, so no Check HP, Weather or Risky. Tag Strategy is on in every double by the engine.

Officer Phobos, fear:

| Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|
| Growlithe (lead) | 17 | Intimidate | Sitrus Berry | Careful | Flamethrower, Crunch, Will-O-Wisp, Leer | 30 |
| Houndour | 17 | Unnerve | BlackGlasses | Mild | Snarl, Dark Pulse, Ember, Taunt | 32 |
| Totodile | 17 | Torrent | Rindo Berry | Lonely | Waterfall, Bite, Ice Punch, Scary Face | 24 |
| Snubbull (ace) | 18 | Intimidate | Oran Berry | Sassy | Charm, Play Rough, Ice Fang, Stomping Tantrum | 18 |

Officer Deimos, dread:

| Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|
| Joltik (lead) | 17 | Unnerve | Oran Berry | Hasty | Electroweb, Giga Drain, String Shot, Light Screen | 35 |
| Surskit | 17 | Swift Swim | Mystic Water | Quiet | Icy Wind, Scary Face, Water Pulse, Struggle Bug | 28 |
| Snorunt | 17 | Snow Cloak | Eviolite | Naive | Icy Wind, Shadow Ball, Water Pulse, Bite | 29 |
| Ekans (ace) | 18 | Unnerve | Poison Barb | Naughty | Glare, Poison Jab, Bite, Rock Tomb | 30 |

The partner, in all six files (Ian, 2026-10-31: a real team; 2026-11-01: four, not led by the starter). Eevee leads, then Buneary and Pachirisu, the first stages of Lucas and Dawn 2's six, and the starter comes last. The starter is the line the file already had, the one that beats the player's starter, and the sets are plain: iv_scale 200, no tuned items.

| Files | Member | Level | Item | Moves |
|---|---|---|---|---|
| all six (lead) | Eevee | 16 | Rawst Berry | Swift, Dig, Yawn, Helping Hand |
| all six | Buneary | 16 | Cheri Berry | Double Kick, Double Hit, Quick Attack, Baby-Doll Eyes |
| all six | Pachirisu | 16 | Sitrus Berry | Spark, Electroweb, Quick Attack, Charm |
| `_turtwig` | Prinplup | 17 | Oran Berry | Chilling Water, Metal Claw, Peck, Growl |
| `_chimchar` (Scorbunny player) | Turtwig | 17 | Oran Berry | Razor Leaf, Bullet Seed, Rock Blast, Withdraw |
| `_piplup` | Monferno | 17 | Oran Berry | Flame Wheel, Mach Punch, Fury Swipes, Leer |

How it plays. Joltik's, Surskit's and Snorunt's spread drops take the box's Speeds of about 30 to about 20, under Growlithe, Houndour and Ekans. Growlithe's and Snubbull's Intimidate and Snubbull's Charm cut the box's physical side, which is most of it at this point, and Houndour's Snarl and Surskit's Struggle Bug cut the special side. Light Screen covers the special hits that Intimidate does not. Totodile's Water answers the Rock and Ground types that wall Phobos's Fire types. The counterplay is the box's special attackers (Prinplup's and Barboach's Water, Dottler, Budew, Raboot's and Fletchinder's Ember), switching to clear the drops, and the partner's own Electroweb.

A first draft had Arbok at 18, four levels before Ekans evolves, and Snubbull with an Eviolite. They were the fight's two walls, beaten one on one by almost no early catch, and Ian had both softened (2026-10-31).

## Phobos and Deimos 2: Pal Park

Byron's split, Barry 5's stretch, after Cyrus 1. Barry 5's honour cap of 50 is in force, so the aces sit at 48, two under it, and every other member at 47. Five a side against the player's six and the partner's six, ten against twelve, as Tyche and Hermes are counted at Veilstone. Phobos carries Basic, Evaluate Attack, Expert and Harassment (Charm, Will-O-Wisp, Tickle). Deimos adds Check HP for Froslass's Destiny Bond, so it waits until Froslass is low (`flags-guide.md`).

Officer Phobos, fear:

| Member | Level | Ability | Item | Nature | Moves | Speed | From Jubilife |
|---|---|---|---|---|---|---|---|
| Granbull (lead) | 47 | Intimidate | Leftovers | Sassy | Spirit Break, Close Combat, Charm, Crunch | 54 | Snubbull |
| Houndoom | 47 | Unnerve | BlackGlasses | Rash | Snarl, Heat Wave, Dark Pulse, Will-O-Wisp | 118 | Houndour |
| Mawile | 47 | Intimidate | Rocky Helmet | Brave | Iron Head, Play Rough, Sucker Punch, Tickle | 59 | new |
| Feraligatr | 47 | Intimidate | Mystic Water | Lonely | Waterfall, Crunch, Superpower, Dragon Dance | 95 | new |
| Arcanine (ace) | 48 | Intimidate | Shuca Berry | Naive | Flare Blitz, Extreme Speed, Crunch, Thunder Fang | 122 | Growlithe |

Officer Deimos, dread:

| Member | Level | Ability | Item | Nature | Moves | Speed | From Jubilife |
|---|---|---|---|---|---|---|---|
| Galvantula (lead) | 47 | Compound Eyes | Focus Sash | Hasty | Sticky Web, Electroweb, Thunder, Energy Ball | 133 | Joltik |
| Absol | 47 | Super Luck | Black Belt | Adamant | Knock Off, Sucker Punch, Superpower, Stone Edge | 108 | new |
| Masquerain | 47 | Intimidate | Wise Glasses | Modest | Icy Wind, Bug Buzz, Hydro Pump, Air Slash | 75 | Surskit |
| Arbok | 47 | Intimidate | Black Sludge | Impish | Glare, Gunk Shot, Crunch, Rock Slide | 94 | Ekans |
| Froslass (ace) | 48 | Cursed Body | NeverMeltIce | Naive | Ice Beam, Shadow Ball, Thunderbolt, Destiny Bond | 137 | new |

How it plays. Galvantula's Focus Sash buys a Sticky Web on turn 1, so every Pokemon the player's side sends in loses a Speed stage. Electroweb, Icy Wind and Glare do the rest, and Phobos's slow hitters (Granbull, Mawile) and fast ones (Arcanine's Extreme Speed, Houndoom) then move first. Five Intimidates cross the field over the fight. Absol, the disaster Pokemon, and Froslass's Destiny Bond are the dread at the end. The partner's Umbreon, Electroweb and Fake Out answer some of it. The four new members (Mawile, Feraligatr, Absol, Froslass) give the coverage the box's walls asked for: Fighting and Water into Bastiodon, Garganacl and Golem, Fire and Electric into Corviknight.

The placeholder officers' four each (Skuntank, Crobat, Toxicroak, Houndoom; Purugly, Mismagius, Bronzong, Honchkrow) are gone. Persian, Deimos's cat for Mars in a first draft, gave way to Absol, since it read as the softest member by far.

## The cheap checks

The boxes are goal 3's, built with its own pieces, since goal 3 drops tag battles. For Jubilife the box is the seed's catches from Roark's split, at level 18, since the scene starts as the player comes back from Oreburgh, before any of Gardenia's areas; the partner's members are added beside it for the second set of readings. For Pal Park it is Barry 5's box at 50. Seeds 1 to 3 start with Turtwig, Scorbunny and Piplup. The screen scores the best six of a box against a team by damage alone, one on one from full HP, higher meaning easier for the player. It counts no stat drop, no Intimidate, no Sticky Web and no double, so these fights play harder than they read. Per member is the score divided by the team's size, which makes teams of different sizes comparable.

Jubilife, the officers' members read as one team:

| Team | Box 1 | Box 2 | Box 3 | Per member |
|---|---:|---:|---:|---:|
| Four a side (2026-11-01), with the partner's four | 23.05 | 23.20 | 24.70 | 3.0 |
| Three and two, with the partner's two, as Ian set it on 2026-10-31 | 16.2 | 16.0 | 18.1 | 2.8 |
| The same before the walls were softened, with the partner | 12.6 | 9.6 | 16.5 | 2.1 |
| The same, without the partner | 12.6 | 9.6 | 15.2 | 2.1 |
| Somnu 1 (four members) | 5.7 | 7.7 | 7.2 | 1.7 |
| Mars 1 (five members) | 1.1 | -2.1 | 9.5 | 0.6 |
| This page's first draft (levels 16 and 17, weaker moves) | 19.2 | not run | not run | 3.2 |

The partner's Monferno joins box 3's best six, which is why that box reads easier with it. Softened, Snubbull is beaten one on one by two to five catches a box and Ekans by seven or eight, where Snubbull with its Eviolite was beaten by one and Arbok by none to two. Every other member is beaten by five to fourteen. At four a side, Totodile is beaten by five to nine a box and Snorunt by six or seven.

Pal Park, each officer and both together:

| Team | Box 1 | Box 2 | Box 3 | Per member |
|---|---:|---:|---:|---:|
| Phobos | 15.5 | 16.0 | 15.2 | 3.1 |
| Deimos | 17.3 | 17.0 | 16.8 | 3.4 |
| Both | 30.9 | 31.4 | 30.0 | 3.1 |
| Argo 1 (six, at 51 to 53) | 12.6 | 14.3 | 14.6 | 2.3 |
| Barry 5 (six, at 51 to 53) | 9.0 | 8.0 | 9.7 | 1.5 |
| Tyche and Hermes on their own boxes (Barry 4's, at 42) | 36.8 | 37.6 | 36.0 | 3.7 |
| The placeholder officers (four each, no items) | 34.7 | not run | not run | 4.3 |

Why Pal Park cannot read like Argo 1 at these levels. Argo's six and Barry 5's sit at 51 to 53, above the box's 50, and both still await their redesign under the caps of 47 and 50. The officer rule puts Phobos and Deimos 2 to 4 under the cap in force, so at 47 and 48 against a box at 50. The same ten sets raised four levels, to Argo's, read 12.0 for Phobos on box 1, against Argo's 12.6, and 15.2 for Deimos. So the sets are about as strong as Argo's, and the gap is the levels. A box of 89 catches always holds a wall for any one member, so the screen's ceiling bites here more than at Jubilife. Tyche and Hermes, whom Ian accepted as officer difficulty, read easier than these on their own boxes (question 2).

Speed tiers. At Jubilife the box's fastest are Raboot 41, Ponyta 40, Pawmo 38 and Fletchinder 37; Joltik (35) outspeeds most of the box, Houndour (32) and Growlithe and Ekans (30) about half, Snorunt (29) and Totodile (24) fewer, and one Electroweb or Icy Wind puts the box's 30s under Growlithe and Houndour. At Pal Park the box's top is Crobat 142, Talonflame 138, Weavile 137 and Cinderace 131; Froslass (137) and Galvantula (133) sit among them, Arcanine (122) and Houndoom (118) just under, and Sticky Web plus Electroweb puts most of the box under Phobos's fast half.

The replacement trace (who the AI sends in when a member leaves) reads sensibly in every row looked at: Arcanine against Corviknight and Torterra, Feraligatr against Garganacl and Bastiodon, Masquerain against Bastiodon and Probopass, Arbok against the Fairy types, and at Jubilife Surskit against the Rock types and Joltik against Bibarel and Corvisquire. The trace was read on a stand-in single team; in the battle each officer replaces from its own five.

## The scene's text

Every changed line is no longer than the longest line already in its box. No message id moves.

| Bank | Message | Now |
|---|---|---|
| Jubilife | 64, 66 | "Phobos:" in place of "Mystery man:" |
| Jubilife | 69 | Phobos and Deimos trade the lines, then name themselves: "Know the names Phobos and Deimos, officers of Team Galactic!" and "Fear and dread, children." |
| Jubilife | 73 | "Phobos:" and "Deimos:" in place of "Grunt 1:" |
| Pal Park | Phobos's and Deimos's opening lines | the speaker labels, and Phobos knows them: "Wait... You two again? The brats from Jubilife City!" |
| Pal Park | the retreat | "Commander Mars won't like this." |
| Trainers | four defeat lines | Phobos: "Afraid? Me? Of two children?"; Deimos: "The dread was meant to be yours..."; at Pal Park "Since Jubilife, it is always you two!" and "still the dread is ours..." |

## What changed in the files

| Files | Change |
|---|---|
| `galactic_grunt_jubilife_city_1`, `_2`, `dummy_009`, `dummy_050` | names, class, defeat lines, teams and AI flags |
| `lucas_jubilife_city_*`, `dawn_jubilife_city_*` | two Pokemon each in place of one starter at 13; four since 2026-11-01, Eevee leading |
| `events_pal_park_lobby.json`, `scripts_pal_park_lobby.s` | Deimos in the male grunt's sprite; local ids and movements named for the officers |
| `jubilife_city.json`, `pal_park_lobby.json` | the scene lines above |
| `trainers_diverged.json`, `bulk_scripts.py`, `bulk_events.py`, `import_base_rom.py` | every changed field and bank registered, so the base ROM's importers leave them |
| `fights.json` | `phobos_deimos_1`, a story tag fight with its partners, seated by no reference hack; Pal Park's fight named "Phobos and Deimos 2" |
| `splits.py`, `test_b1.py` | the six Jubilife partner files placed in Gardenia's split with a check; the officers' names and aces |
| `scyther/data.json`, `learnrewrite.py` | Brick Break on Scyther's egg list, for the Pal Park partner's Scizor. TM 31 also gives it today, so the entry keeps it legal only if the TM list changes |

Nothing in the save moves.

## Ian's answers, with the reasoning they settled

1. The theme. A was built and taken; B and C are above. A is the one a double rewards and the one the early lines carry best.
2. Pal Park's levels. At the officer rule's levels it reads harder than Tyche and Hermes and easier than Argo 1, whose levels sit above the cap and await their redesign. Raising Phobos and Deimos 2 to 50 and 51 would have read about like Argo; Ian kept 47 and 48 and the rule.
3. and 4. The two walls. Snubbull's Eviolite and Intimidate and Arbok's speed and Glare left an early box almost no one-on-one answer to either. Ian softened both: Ekans at 18 keeps the Glare, and Snubbull with an Oran Berry keeps its Intimidate and Charm.
5. Destiny Bond. Check HP holds it to a low Froslass, and the player plays round it with status or by not striking the last blow. Kept.
6. The text. The lines above are new; read them before landing.
