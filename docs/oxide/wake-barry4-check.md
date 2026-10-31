# Wake and Barry 4: a short check

Ian built Wake's six and the three Pastoria Barry versions (Barry 4) in the OxiDex on 2026-10-31 and asked for the check Maylene's six had on 2026-10-29: anything that invalidates a fight, and the weakest crux in each with the top replacement picks for it. His natures are his choice; a repeat inside a team is reported. The teams are on branch `overseer-wake-barry4`. The only change this check makes to the game's data is the egg-list commit below. Every number comes from cheap checks; no scorer reading was run.

## Ian's answers (2026-10-31)

Wake keeps his six exactly as it is: Jellicent stays ("it can't read it correctly", meaning the simulator undervalues it), and so does Goodra at 40 (questions 1 and 2). In all three Barry 4 versions, Luxray takes the Hasty set of Howl, Crunch, Wild Charge and Ice Fang, which ends the Turtwig version's repeated Jolly (questions 3 and 4). Greninja, in the Piplup and Turtwig versions, swaps Mat Block for Feint Attack (question 7). Snorlax, Serperior's Contrary with Scale Shot, and Turtonator's Shell Trap stay (questions 5, 6 and 9). Barry 4 comes down a step (question 10): "it will be an intermediate split of 42", so his honour cap is 42, his ace starter drops two levels to it and every other member drops three. The cap is recorded where Tyche and Hermes's 41 is. He approved both simulator fixes (question 8: "Fix both"), the Air Balloon and Scale Shot's stat change, which are in `simulator-gaps.md`. Every move of the new Barry sets is on its species' list at its new level, so no egg list changed. The numbers in the sections after this one are the check's, from before these answers.

The cheap checks were run once more on the teams as they now stand, with both simulator fixes in: the screen, the replacement trace and the probe, on the same boxes. Barry 4's box now stands at 42, his ace's level. Each cell is the player's wins in 150 rough fights against the best six and then the most-taken six, as in Part 3; one number means the two were the same six.

| Fight | Box 1 | Box 2 | Box 3 | Screen's best-six score |
|---|---|---|---|---|
| Wake, before the fixes | 85, 60 | 33, 56 | 54, 64 | 16.30, 14.85, 14.15 |
| Wake, with the fixes | 95, 67 | 28, 66 | 55, 67 | 16.30, 14.85, 14.15 |
| Barry 4, Ian's first six at 44 | 53, 43 | 57, 53 | 66, 29 | 14.85, 15.25, 16.00 |
| Barry 4 as answered, at 42 | 52, 80 | 71, 45 | 59 | 12.90, 16.70, 16.35 |

The fixes work in the fights. Clodsire's balloon now bursts in 141 to 150 of 150 fights, and Wake reads a little easier for it. Every Scale Shot now moves Serperior's stages: +1 Defense and -1 Speed in 108 to 216 uses a run, with a handful at a limit already. Greninja used Feint Attack 14 to 31 times a run. Luxray's Hasty set knocked out 36 to 52 of the player's Pokemon on box 1 and 124 to 128 on boxes 2 and 3. Barry 4 at 42 reads about as hard as before on these checks; the screen's scores are against a box at 42 rather than 44, so they do not compare cell for cell.

## Summary

**Outcome for Wake.** Nothing invalidates the fight. Pastoria Gym's map gives a permanent rain (the engine's overworld rain, which never ends), and every Wake check here ran in it. The rain is the fight. Floatzel's and Ludicolo's Swift Swim double their Speed to 258 and 150, so Floatzel outspeeds every catch the screen takes. Goodra's Thunder cannot miss, and its Weather Ball is a 100-power Water move. Hydration wakes Goodra at the end of the turn it Rests, so each Rest is a full heal with no sleep. Taken away for contrast, the rain is worth about 27 more wins in 150 rough fights to the player. Clodsire's Air Balloon is where the simulator is wrong: its damage rows ignore the balloon, and the balloon never bursts, so the Ground answers to Clodsire are misread both ways (question 8). Six of Wake's 24 moves were on no Oxide list at their levels; they are now on egg lists, as he ruled.

**The weakest crux in Wake is Jellicent's slot.** It knocks out the fewest of the player's Pokemon of the five non-leads (27 to 87 per 150 rough fights, against 84 to 275). Every common Grass catch knocks it out from full HP in one hit (Abomasnow's Wood Hammer 220 to 260 percent, Tsareena's Trop Kick 150 to 176, Leavanny's Leaf Blade 134 to 162), and it has nothing for them. Wake's six has no setup move, so no lead passes Ian's bait test in full: the Grass answers to Clodsire, in 18 to 20 of the screen's top 20 sixes on every box, draw in Floatzel or Goodra, which lose to them.

**Outcome for Barry 4.** Nothing invalidates the fight. Pastoria City's sky is clear, so Barry fights without rain. Four of Barry's moves were off-list (Shell Trap, Glare, Scale Shot and Gunk Shot) and are now on egg lists. The Turtwig version has Jolly twice (Luxray and Infernape). Three things play differently from how the set reads: Greninja's Mat Block, Serperior's Contrary and Scale Shot, and Turtonator's Shell Trap (questions 6, 7 and 9). The six follow the pool doc's Barry 4 column exactly, but Snorlax carries the very Barry 3 set Ian called too optimal (question 5).

**The weakest crux in Barry 4 is Luxray, shared, and only narrowly.** It is the lowest non-lead in the Turtwig and Piplup versions (93 to 121 knockouts per 150 fights) and second lowest for a Scorbunny player, where Turtonator is lower (23 to 119). No Barry member is as weak as Jellicent. Neither pick I tried clearly improves the slot, so keeping Luxray is a fair answer.

**On the cheap checks, both fights read harder than Maylene's and about as hard as Dahlia's** (the table in Part 3). Barry 4, a rival before the gym, reads about as hard as Wake.

**What Ian decides.**

1. Wake, Jellicent's slot: Tentacruel (my first pick), Araquanid, Kingdra, or keep Jellicent?
2. Wake's Goodra is level 40, ten under Sliggoo's evolution at 50: keep it, or is that too early?
3. Barry 4, Luxray's slot: keep Luxray, take Luxray with Howl (Hasty, which also ends the repeated Jolly), or take Primeape?
4. If Luxray stays as it is, which of the Turtwig version's two Jolly members changes?
5. Barry 4's Snorlax is Barry 3's old set, which Ian called too optimal; the Turtwig version's Staraptor is close to its old set too. Intended?
6. In the game, Contrary turns each Scale Shot into +1 Defense and -1 Speed for Serperior. Intended?
7. Greninja's Mat Block works only on its first turn out, yet 84 to 98 percent of the AI's Mat Blocks come later and fail. Keep it, or swap it?
8. Approve two simulator fixes: the Air Balloon (its immunity in the rows, and its bursting), and Scale Shot's stat change.
9. Barry 4's Turtonator leans on Shell Trap, whose in-game check 82 is still open. Keep it on the team while that check waits?
10. Barry 4 reads about as hard as Wake on these checks. Is that the step Ian wants from a rival one fight before the gym?

**Next steps.** Ian answers in a line each. A session then writes the chosen sets on this branch and reruns the legality check and the probes, which takes about 45 minutes. Each approved simulator fix is about an hour, with a test that fails before it, and lands through the Overseer. The in-game checks are the rain, the Air Balloon, Hydration's Rest and Shell Trap (check 82); they take about 20 minutes with Ian driving. A spot-check reading happens only if Ian names one, and takes two and a half to four hours.

## Part 1: what could invalidate the fights

### Legality, and the egg-list commit

Two checkers read the four files: the OxiDex's own list, which reads only today's TMs, and the Kaizo study's checker at level 44, which counts the TMs from before the TM pass. These moves were on neither list at their members' levels, or only on the OxiDex's when the Kaizo checker passed them. Each went on the egg list of its line's first stage, as Ian ruled on 2026-10-29, in commit a9413bd1b60.

| Team | Member | Move | Where Oxide had it | Egg list now |
|---|---|---|---|---|
| Wake | Clodsire 41 | Gunk Shot | nowhere | Wooper |
| Wake | Clodsire 41 | Muddy Water | Clodsire's level 47 | Wooper |
| Wake | Clodsire 41 | Toxic Spikes | Clodsire's level 58 | Wooper |
| Wake | Jellicent 41 | Strength Sap | nowhere | Frillish |
| Wake | Gyarados M 43 | Waterfall | Gyarados M's level 48; Gyarados's HM (the Kaizo checker passed it) | Magikarp, and Gyarados M's own list, since the OxiDex gives Gyarados M no earlier stage |
| Wake | Goodra 40 | Rest | a TM before the TM pass | Goomy |
| Barry 4, two versions | Turtonator 41 and 42 | Shell Trap | nowhere | Turtonator |
| Barry 4, two versions | Serperior 41 and 42 | Glare | Serperior's level 48 | Snivy |
| Barry 4, two versions | Serperior 41 and 42 | Scale Shot | Serperior's level 57 | Snivy |
| Barry 4, two versions | Greninja 42 | Gunk Shot | Greninja's level 51 | Froakie |

After the commit the OxiDex's list gives every move of the four teams at its level, and the Kaizo checker's only note is Goodra's level (question 2). Each move is in `learnrewrite.IAN_EGG_MOVES`, and Turtonator's hand-set line in `learnsets_by_hand.txt` says so too. Magikarp's file had no egg list, so it gained one, and the built table carries it. The trainer lint finds nothing on the four files, test_learnrewrite passes 5 of 5, test_learncheck passes 18 of 18, and `make rom` builds.

Shell Trap's place on Turtonator's egg list is for trainers only. The player's level-up home for it still waits on in-game check 82, as the tracker's Scheduled list says.

### The rain, and what it does to Wake's fight

The engine starts every battle on a map whose header weather is rain with `subscript_overworld_rain`, which sets the permanent rain flag; Pastoria Gym's header is `OVERWORLD_WEATHER_HEAVY_RAIN`. The scorer's tools read the same header (`calc.fight_weather`), so the Wake fight here started in rain without any change, and its damage rows were all made in rain. Pastoria City's header is clear, so Barry 4 has no weather.

What the rain does, from the probes with and without it:

| Piece | In rain | Without rain |
|---|---|---|
| Floatzel (Swift Swim, Jolly, Life Orb) Speed | 258 | 129 |
| Ludicolo (Swift Swim) Speed | 150 | 75 |
| Goodra's Rest (Hydration) | awake at the end of the same turn, in all but one of 69 to 108 Rests per 150 fights | asleep after it; 190 to 406 turns a run asleep in front |
| Goodra's Thunder, uses that took HP (the Ground types' immunity included) | 96 to 100 percent | 51 to 65 percent |
| Goodra's Weather Ball | a 100-power Water move, boosted by the rain | a 50-power Normal move |
| Water moves (Scald, Hydro Pump, Muddy Water, Waterfall, Aqua Tail, Aqua Jet) | half as strong again | plain |
| The player's Fire moves | halved | plain |
| Goodra's knockouts per 150 fights | 128 to 202 | 69 to 94 |
| Player's rough wins per 150 fights (best six, most-taken six) | 85 and 60, 33 and 56, 54 and 64 | 121 and 106, 96, 62 and 47 |

The rain helps the player's side too. Box 3's Empoleon (in 18 of its top 20 sixes) and the Seaking and Lombre some boxes hold have Swift Swim, Whiscash's Hydration works, and Araquanid's Water Bubble hits as hard as it does anywhere. None of the player's catches outruns Floatzel.

### What each piece does

I checked every ability slot against Oxide's species data, and every item and unusual move in the engine and the simulator.

- Abilities. Wake: Clodsire's slot 2 is Water Absorb, Ludicolo's slot 1 Swift Swim, Jellicent's slot 2 Cursed Body, Gyarados M's slot 1 Mold Breaker, Goodra's slot 2 Hydration, Floatzel's slot 1 Swift Swim. Barry 4: Staraptor's slot 1 is Reckless (slot 3, Intimidate, in the Turtwig version), Turtonator's Shell Armor, Luxray's Tinted Lens, Serperior's slot 3 Contrary (its hidden ability, which the engine gives after the Pokemon is built), Snorlax's slot 2 Thick Fat, Empoleon's and Greninja's Torrent, Torterra's slot 2 Thick Fat, and Infernape's Iron Fist.
- Gyarados M is Oxide's Water and Dark Gyarados, made by levelling a Gyarados holding a Dragon Scale. The calculator calls it Gyarados-Mega, but the simulator builds it from Oxide's own stats.
- The Air Balloon. In the engine a Ground move does not affect its holder, and the balloon bursts when any damaging move hits it. With Water Absorb, Clodsire's only weaknesses while it floats are Psychic and Ice. In the simulator the player's move filter treats the balloon as a permanent Ground immunity, but the damage rows ignore it: a forced Earthquake from Quagsire took Clodsire from 169 HP to 41. And the balloon never bursts. So the screen counts Whiscash, Quagsire and Torterra as beating Clodsire by Ground moves (+3.0) that would fail in the game, while the fights never let the player Earthquake it even after a hit. This gap is not in the gaps list.
- Shell Trap, reworked in October: 150-power Fire, priority -3, and it fails unless a physical move hit its user that turn. The engine and the simulator agree (`fightsim.move_fails_first`; the AI's Expert_ShellTrap scores it -2 unless the target's last move was physical). In the probes it took HP in 85 percent of its uses, but the probe's player attacks blindly; a player who knows the move answers it with special moves or status. In-game check 82 has not run yet.
- Scale Shot is Oxide's 25-power, two to five hit move. The engine lowers its user's Defense one stage and raises its Speed one stage after the last hit (`subscript_hit_x_times`), and Contrary turns both round, so Barry's Serperior gains Defense and loses Speed with each use. The simulator applies neither: in 354 uses across the probes its stages never moved. This gap is not in the gaps list either.
- Mat Block guards the user's side from damaging moves on its first turn out only, in the engine and the simulator alike. Neither the engine's AI script nor the simulator's AI has a routine for it, so the AI scores it as a plain status move and picks it again on later turns, where it fails. In the probes Greninja used it 108 to 188 times per 150 fights, and 91 to 172 of those uses (84 to 98 percent) came after its first turn.
- Water Shuriken is a special Water move of two to five hits at 25 power, with +1 priority. Drum Beating lowers Speed and Body Press hits with Defense, and both run in the engine (`battle_lib.c` for Body Press) and the simulator.
- Strength Sap, Leech Seed with the Big Root, Dragon Tail, Glare, Toxic Spikes, Spikes, Rest, the Life Orb, the Assault Vest, the Focus Band, the Lum Berry and the Shell Bell all run in the simulator. Sharp Beak, BlackGlasses, Thick Fat, Iron Fist and Tinted Lens change damage only, and the calculator's rows apply them; I did not check them one by one.

### The rulings

- Items: no item repeats in any of the four teams.
- Natures: no repeat in Wake's six or the Scorbunny and Piplup versions. The Turtwig version has Jolly on both Luxray and Infernape.
- No one-hit KO move, no evasion move and no trapping move. No forced trade anywhere. Muddy Water's accuracy drop is a 30 percent side effect, not an evasion setup.
- Levels: Wake's ace Floatzel and every Barry ace sit at the cap of 44. Goodra at 40 is ten levels under Sliggoo's 50, which the Kaizo checker notes; the ruling allows a member under its evolution level "though not egregiously early", so that is question 2. Every other member is past its evolution level.
- Barry's pool: every version brings exactly the pool doc's Barry 4 column (the starter, its two partners, Staraptor, Snorlax and Luxray), with the partners the doc gives each player. Two sets fall back on what Ian criticised in Barry 3. Snorlax is Body Slam, Earthquake, Curse and Ice Punch on Leftovers, Thick Fat and Careful in all three versions, which is Barry 3's old set exactly. The Turtwig version's Staraptor (Adamant, Intimidate, Sharp Beak, Brave Bird, Close Combat) is close to Barry 3's old one. The pool gives Staraptor the role of an Intimidate lead and pivot with Tailwind, and none of the three versions has a pivot. That is question 5, since Ian may have changed his mind.
- Wake has no entry in `boss-shapes.md`, so this check judges materiality by eye.

## Part 2: the weakest crux

### Wake: Jellicent's slot

Knockouts of the player's Pokemon while each member was in, per 150 rough fights. Each box has two runs, against the screen's best six and against its most-taken six.

| | Clodsire | Ludicolo | Jellicent | Gyarados M | Goodra | Floatzel |
|---|---|---|---|---|---|---|
| Box 1 | 6, 6 | 180, 185 | 58, 87 | 136, 161 | 128, 149 | 211, 187 |
| Box 2 | 34, 20 | 157, 228 | 27, 40 | 138, 122 | 202, 173 | 275, 192 |
| Box 3 | 38, 50 | 176, 180 | 75, 77 | 84, 88 | 157, 151 | 259, 238 |
| Catches in the top 20 that beat it one on one | 12 to 13 | 4 to 5 | 11 to 14 | 5 to 6 | 9 to 13 | 5 to 7 |

Clodsire's low count is its job. It opened with Spikes or Toxic Spikes in 90 to 144 of 150 fights, and Goodra's Dragon Tail (93 to 291 uses a run) then drags the player's Pokemon in over them. That hazard stack is the fight's one tactic, and the nearest thing it has to setup.

Jellicent is the crux for three reasons:

1. Every Grass catch the screen takes knocks it out from full HP in one hit: Abomasnow's Wood Hammer 220 to 260 percent (20 of 20 sixes on box 1), Tangrowth's Bullet Seed 114 to 144 (19 of 20), Tsareena's Trop Kick 150 to 176 (20 of 20 on box 2), Leavanny's Leaf Blade 134 to 162 (18 to 20 of 20 on boxes 2 and 3), and Breloom's Bullet Seed 204 to 252. Its own moves do nothing special to Grass.
2. The AI's replacement rule rarely sends it in: only against Dhelmise, Luxray and Orbeetle when Clodsire leaves, and Whiscash and Quagsire when Ludicolo leaves.
3. Its Strength Sap was used 1 to 41 times a run. It spends its turns on Hydro Pump in the rain, which the Grass catches resist.

Clodsire against Ian's lead rule: its answers draw these members in, by the AI's replacement rule.

| Clodsire's answer (its margin on Clodsire, sixes of 20) | Drawn in | Does it beat the answer? |
|---|---|---|
| Abomasnow (+0.5, 20), box 1 | Floatzel | no: Abomasnow +1.5 on Floatzel |
| Tangrowth (19), Torterra, Whiscash, Quagsire on box 1; Leafeon on box 3 | Ludicolo | yes, by Ice Beam and Giga Drain |
| Tentacruel (+1.5, 10 to 12), every box | Goodra | narrowly no (+0.5) |
| Dhelmise (+2.5, 10), Luxray, box 1 | Jellicent | no |
| Tsareena (20), box 2 | Goodra | no: Tsareena +2.5 on Goodra |
| Leavanny (18 to 20), boxes 2 and 3 | Floatzel | no (+0.5) |
| Empoleon (+3.0, 18), box 3 | Gyarados M | no (+0.5) |
| Breloom (12), box 3 | Goodra | no (+0.5) |
| Bronzong, Corviknight | Gyarados M | yes |
| Araquanid, boxes 2 and 3 | Goodra | yes |
| Cinderace, box 2 | Floatzel | yes |

No drawn member carries a setup move, since Wake's six has none. So the most-taken answers, the Grass types, are safe for the player to lead with.

### Wake: the picks

Each pick replaces Jellicent at 41 and keeps Ian's other five, with an item and a nature no other member uses. Each was swapped in memory and run through the screen, the replacement trace and the probe on all three boxes.

| Set | Legal | Knocked out while in | Setup used, per run | Player's rough wins | Who draws it in | Catches in the top 20 that beat it |
|---|---|---|---|---|---|---|
| Ian's: Jellicent 41, Sitrus Berry, Gentle, Cursed Body; Hydro Pump, Strength Sap, Confuse Ray, Dazzling Gleam | yes, after the egg-list commit | 27 to 87 | Strength Sap 1 to 41 | 33 to 85 | Dhelmise, Luxray, Orbeetle; Whiscash, Quagsire | 11 to 14 |
| 1. Tentacruel 41, Black Sludge, Naughty, Rain Dish; Swords Dance, Poison Jab, Waterfall, Knock Off | Swords Dance through its pre-TM-pass TM; Tentacool's egg list would need it for the OxiDex | 132 to 200 | Swords Dance 88 to 124 | 23 to 53 | every Grass answer to Clodsire: Abomasnow, Tangrowth, Lurantis, Tsareena, Breloom, Leafeon | 12 (Quagsire in 20 of 20 at +3.0; Empoleon on box 3) |
| 2. Araquanid 41, Mystic Water, Impish, Water Bubble; Iron Defense, Waterfall, Lunge, Poison Jab | yes | 64 to 143 | Iron Defense 64 to 104 | 16 to 65 | Abomasnow, Tangrowth, Lurantis, Luxray, Torterra on box 1; Arboliva on box 2; Leafeon, Leavanny on box 3 | 4 to 8 |
| 3. Kingdra 41, Lum Berry, Adamant, Swift Swim; Dragon Dance, Waterfall, Outrage, Iron Head | yes | 101 to 200 | Dragon Dance 28 to 82 | 15 to 49 | Abomasnow on box 1 only | 1 to 2 (Torterra, Primarina, Dubwool) |

Tentacruel is my first pick because it alone meets Ian's lead rule in full. Every Grass answer to Clodsire draws it in. Its Poison Jab does 86 to 104 percent to Abomasnow, 74 to 90 to Lurantis, 84 to 98 to Breloom and 68 to 84 to Tsareena, and Swords Dance sits behind it at 1 PP. Grass hits it only neutrally. Rain Dish heals it a sixteenth a turn in the permanent rain, on top of the Black Sludge. Its answers are Quagsire (Earthquake 120 to 144 percent, and Water Absorb eats its Waterfall) and box 3's Empoleon, which is immune to Poison Jab. The price: it more than doubles the slot's output and makes the fight clearly harder. It also shares a species with a catch common in the player's sixes. Tentacool's egg list would take Swords Dance, under the same ruling.

Araquanid is the smaller step. Water Bubble doubles its Waterfall, so in the rain it does 94 to 112 percent to Torterra. Lunge does 72 to 86 to Abomasnow and lowers Attack. The Grass answers draw it in on boxes 1 and 3, and Iron Defense gives it a setup turn. Tsareena on box 2 still beats it narrowly and draws in Goodra instead.

Kingdra is the upper bound, as Dusknoir was in Maylene's slot study. Swift Swim and Dragon Dance in a rain that never ends leave the player one or two catches in any top 20 that beat it. It is drawn in only once, and it would give Wake a second Dragon and a third Swift Swim member.

### Barry 4: Luxray's slot, shared

Knockouts of the player's Pokemon while each member was in, per 150 rough fights, two runs a box. Box 1 meets the Turtwig player's file, box 2 the Scorbunny player's (`_chimchar`), box 3 the Piplup player's.

| Box | Staraptor | Partner 1 | Luxray | Partner 2 | Snorlax | Ace |
|---|---|---|---|---|---|---|
| 1 (Serperior, Greninja, Infernape) | 94, 96 | Serperior 148, 142 | 93, 121 | Greninja 167, 173 | 161, 103 | Infernape 163, 214 |
| 2 (Turtonator, Serperior, Empoleon) | 94, 86 | Turtonator 23, 119 | 142, 80 | Serperior 178, 220 | 89, 116 | Empoleon 292, 182 |
| 3 (Turtonator, Greninja, Torterra) | 103, 100 | Turtonator 151, 136 | 105, 109 | Greninja 126, 120 | 118, 157 | Torterra 181, 233 |

Luxray is the lowest non-lead in boxes 1 and 3 and second lowest in box 2. Its answers are the Ground and Rock catches (Golem, Hippowdon, Quagsire, Glimmora), which also answer Staraptor. The team is flat: Luxray's numbers are close to Staraptor's and Snorlax's, so the slot is weak only by a little.

Staraptor against Ian's lead rule: its answers are Glimmora (20 of 20 sixes on boxes 1 and 2), Golem and Corviknight. Glimmora and Golem draw in Greninja (box 1), Empoleon (box 2) or Torterra (box 3), each of which beats them. Only box 2's Empoleon carries a setup move (Swords Dance, 25 to 65 uses a run). Corviknight draws in Infernape on box 1, which narrowly loses to it, and Turtonator on box 3, which beats it. So the lead passes in full only for a Scorbunny player.

The Scorbunny version's Turtonator is that version's weakest member: 23 knockouts against the best six, which leads with Glimmora, Hippowdon, Primarina and Golem. Shell Trap is its main hit and needs a physical move into it, so a careful player who sees it can starve it.

### Barry 4: the picks

Each pick replaces Luxray in all three versions, at 42, with the other five as Ian set them.

| Set | Legal | Knocked out while in | Setup used, per run | Player's rough wins | Who draws it in | Catches in the top 20 that beat it |
|---|---|---|---|---|---|---|
| Ian's: Luxray 42 (41 for a Piplup player), BlackGlasses, Jolly, Tinted Lens; Crunch, Thunder Fang, Play Rough, Quick Attack | yes | 80 to 142 | none | 29 to 66 | Corviknight after Infernape (box 1); Rotom and Staravia (box 2); Corviknight after Turtonator, Empoleon after Torterra (box 3) | 6 to 10 |
| 1. Luxray 42, BlackGlasses, Hasty, Tinted Lens; Howl, Crunch, Wild Charge, Ice Fang | yes | 62 to 199 | Howl 35 to 71 | 30 to 57 | the same as Ian's | 8 to 9 |
| 2. Primeape 42, Liechi Berry, Impish, Defiant; Bulk Up, Drain Punch, Rage Fist, Rock Slide | yes | 31 to 271 | Bulk Up 23 to 118 | 9 to 77 | Bibarel and Staravia (box 2), Empoleon (box 3); never Staraptor's walls | 11 to 14 (Granbull enters 16 to 20 of 20 sixes, at +2.5) |

Neither pick is clearly better than Ian's Luxray. The Howl set adds setup and an Ice Fang for the Ground answers, and its Hasty nature ends the Turtwig version's repeated Jolly. Its output swings by box but averages close to Ian's set. Primeape is the pool's own Barry 3 member, a fight later, with Barry 3's item and nature. It was meant to boost on the Rock, Steel and Ground walls that stop Staraptor, but the AI's replacement rule never sends it into them: those walls draw in the Water or Fire member instead. It makes the fight much harder on box 3 (230 to 271 knockouts) and weaker on box 2 (31 to 55), and it pulls Granbull into every top six. So my first pick is to keep Luxray, with the Howl set if Ian wants setup on the slot or the nature repeat gone.

## Part 3: the fights beside Maylene and Dahlia

The probe's player is greedy and the same for every trainer, so its win counts mean nothing on their own. Beside each other on goal 3's boxes, they order the fights. Higher means easier for the player.

| Fight (goal 3's boxes, seeds 1 to 3) | Box 1 | Box 2 | Box 3 | Screen's best-six score, by box |
|---|---|---|---|---|
| Maylene, today's six, on her own boxes (cap 39) | 97, 106 | 109, 123 | 59, 33 | 16.30, 17.15, 17.30 |
| Dahlia, on Wake's boxes (her check of 2026-10-31) | 101, 106 | 17, 19 | 30, 40 | not comparable (her room) |
| Wake, in rain | 85, 60 | 33, 56 | 54, 64 | 16.30, 14.85, 14.15 |
| Wake, rain taken away (contrast only) | 121, 106 | 96 | 62, 47 | 18.25, 18.45, 19.10 |
| Barry 4, on its own boxes (cut just before Barry) | 53, 43 | 57, 53 | 66, 29 | 14.85, 15.25, 16.00 |

Each cell gives the player's wins in 150 rough fights against the screen's best six, then against its most-taken six; one number means the two sixes were the same. The screen's score is the best six's, and a lower score means the player's best six answers the trainer less well. On both measures Wake and Barry 4 sit with Dahlia and below Maylene. Barry 4 reads as hard as Wake, and harder on box 1.

## How the numbers were made

Every number comes from a run in the worktree `.claude/worktrees/wake-barry4` on this branch, at a9413bd1b60 for the probes. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/wake-barry4/`, each with its own usage line, and none writes to `res/`.

- The boxes and the matchup screen come from `plgoal3 --run wake-barry4-study --box wake <seed> --screen` and `--box barry_4 <seed>`, seeds 1 to 3. The run name had no earlier results. Barry 4 is read on its own goal 3 box, cut just before Barry in Wake's split (46 to 47 catches against Wake's 50), and each seed's starter picks the version.
- `h.py` is the harness. It loads a box and its fight (`plgoal3.setup` and `fight_state`), reports the weather a real battle of the fight starts in, swaps a pick into a party slot in memory (`CAND=name`, the sets in `cands.py`), and with `NORAIN=1` starts Wake's fight in a clear sky for the contrast row.
- `checks.py SLUG SEED [N]` runs, in one pass, what the Maylene check's five scripts ran. That is the six as the simulator builds them, the screen's top 20 sixes with every catch's margins, the catches that beat each member, and the replacement trace (`fightai.replacement`) against every catch the top 20 take five or more times. It adds damage both ways and the probe: 150 rough fights against the best and the most-taken six, a greedy player, counting picks, real uses and how often they took HP, setup, items, knockouts while each member was in, the first member in after the lead, and this study's Rest, Mat Block and Scale Shot counts. The player's replacement look-ahead is never counted. `runall.sh`, `runcands.sh` and `runnorain.sh` run it on every box under the memory cap, and `summarise.py` gathers the tables.
- `balloon.py` forces a Ground move into the Air Balloon Clodsire to see what the simulator does with it.
- Legality comes from the OxiDex's `learnsets.lists` (`legal.py`, `legal_cands.py`) and the Kaizo checker (`oxide.py check 44`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`); `palette.py` lists a species' legal moves at a level. `simcheck.py` is the rough check that each move's effect, ability and item is named in the simulator.
- Damage is the calculator's lowest to highest roll in percent of the target's HP, at no stat stages, in the fight's weather.

Where the screen's bias bites: it counts only a clean one-on-one from full HP with no status move and no hazard, so it never sees Clodsire's Spikes or Goodra's Dragon Tail, and it counts the Ground moves into the Air Balloon at full. The probe's greedy player never plays around Shell Trap, Swords Dance or Dragon Dance, so it flatters Shell Trap and the setup picks. It never switches to dodge the hazards either.
