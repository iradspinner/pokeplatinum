# Platinum Kaizo against Oxide: moves and learnsets, as ideas

Written 2026-09-27 by a cloud session for Ian, as ideas for Oxide's move and learnset passes, not a plan to follow (Ian, 2026-09-27). Nothing in `res/`, `src/` or the tools was changed. The sources are Kaizo's move change list (`kaizo-move-changes.md`, 338 lines) and its level-up learnsets (`kaizo-learnsets.tsv`), set against Oxide's tree at `b775fc8c`, vanilla Platinum (the `main` branch), and the ruling lists the gate keeps in `tools/oxide/verify_narcs.py`.

Ian answered its eight questions on 2026-09-27 (the section before the appendices), and the moves short list and answers 2 to 4 are in the tree: `cloud/element4-kaizo-move-data`, merged, whose last commit (cc7023bdc) names every field it set. So every "Oxide now" value in this file, Appendix A included, is the tree at `b775fc8c`, before that work; a move's current numbers are in its `res/moves/<move>/data.json`. The learnset findings still hold at `HEAD`: the same thirteen natives differ from vanilla, since nothing has rewritten a level-up list yet.

Two limits first. The cloud has no base ROM, so where Oxide's value differs from vanilla and from every ruling list, this file calls it a base ROM edit by inference. And Kaizo's list describes some effects in a word or two ("Sharply lowers Spd", "0% chance to 100% chance" on a move whose effect has no chance), so a few lines are read as best they can be and say so.

The short answer. Oxide already carries 66 of Kaizo's 338 move lines in full and part of 41 more, mostly through the base ROM: the 95-power punches, the 90-power fangs and most of the 1 to 3 PP setup moves came from Kaizo. It has something else by a ruling for 31 lines, and lacks 173 outright. What it lacks is dominated by very large buffs: trapping moves at 90 power, recoil in place of recharge turns, a dozen attacks at 120 or more, and priority up to +7. Kaizo's learnsets are the bigger source of ideas, because Oxide's native learnsets are still vanilla for 480 of 493 species. The recommended short lists and Ian's questions are at the end, before the two appendices.

## Moves

Every Kaizo line gets one verdict in Appendix A. The counts:

| Verdict | Lines |
|---|---|
| Oxide has it | 66 |
| Oxide has it, with a ruling setting the rest of the line | 8 |
| Oxide has something else, by a ruling | 23 |
| Oxide has part of it and lacks the rest | 41 |
| Oxide lacks it | 173 |
| Kaizo rebuilt the slot as a move Oxide has no copy of | 17 |
| Kaizo's version of a real move Oxide already has | 8 |
| Teleport, which leaves every learnset in Oxide | 1 |
| Not traced in Oxide's engine (Magic Coat on Stealth Rock) | 1 |

Six of the 66 lines Oxide has match only because the modern numbers of 2026-09-26 happen to equal Kaizo's (Bullet Seed and Icicle Spear 25, Drain Punch 75, Will-O-Wisp 85, Scary Face and Psycho Shift at 100%). The rest are Kaizo's own values that the base ROM took, apart from Teeter Dance, whose line only restates its effect.

### Where a ruling gives Oxide something else

The modern numbers (staples survey, answer 1, 2026-09-26) set 24 fields that Kaizo sets differently. Kaizo is higher on most of them:

| Move | Kaizo | Oxide (modern) |
|---|---|---|
| Jump Kick | 120 power | 100 |
| Hi Jump Kick | 150 power | 130 |
| Crabhammer | 120 power | 100 |
| Fire Spin, Whirlpool, Sand Tomb | 90 power | 35 |
| Smelling Salts | 90 power | 70 |
| Luster Purge, Mist Ball | 100 power | 95 |
| Rock Tomb | 70 power | 60 |
| Doom Desire | 250 power | 140 |
| Feint | 80 power | 30 |
| Power Gem | 90 power | 80 |
| Chatter | 120 power | 65 |
| Wrap, Bone Rush, Meteor Mash | 100 accuracy | 90 |
| Gunk Shot | 100 accuracy | 80 |
| Magma Storm | 100 accuracy | 75 |
| Submission | 8 PP | 20 |
| Petal Dance | 100 power | 120 |
| Overheat, Leaf Storm | 120 power | 130 |
| Fury Cutter | 30 power | 40 |

The base ROM's own values, which answer 1 keeps, differ from Kaizo's on 21 fields. Most are status-move PP set a step lower or higher than Kaizo's (Tail Whip, Growth, Meditate, Withdraw and Charge at 3 where Kaizo has 1 or 5; Light Screen, Reflect and Amnesia at 1 where Kaizo has 2 or 3). The rest are attacks the base ROM buffed less than Kaizo: Slam 100 (Kaizo 120), Twineedle 40 (50), Lick 40 (80), Smog 55 with 30% poison (60, 50%), Poison Fang 75 (90), Hyper Voice 100 (110), Block at +1 (+7) and Metal Burst at -5 (-2). Three accuracy values run the other way, with the base ROM more generous than Kaizo: Double Slap, Fury Swipes and Aqua Tail at 100 (Kaizo 90, 90 and 85). Crabhammer's is the base ROM's 95 against Kaizo's 100.

Six more rulings cover the rest. Answer 2 keeps Swagger at 90 and Dark Void at 80 (Kaizo 100 and 90). Answer 7 keeps Knock Off at a flat 70 (Kaizo 80) and Rapid Spin as hazard removal with a Speed raise, where Kaizo turned the slot into a fixed Fire Hidden Power. Answer 3 keeps Hidden Power on the IV formula, which rules out all eleven of Kaizo's fixed-type Hidden Powers. Barrier is at 1 PP as a setup move (Kaizo 5). Poison Gas hits both foes only (Ian, 2026-09-22), where Kaizo hits the partner too. And the move pool's first cut (2026-09-27) takes Teleport and Splash out of every learnset, so Kaizo's +1 Teleport and its Splash slot (a Water Hidden Power) have nothing to attach to.

### What Oxide lacks, by kind

Accuracy, 58 fields. Kaizo raises most 90% attacks to 100 (Rock Slide, Steel Wing, Metal Claw, Air Slash, Heat Wave, Hyper Fang, Super Fang, Triple Kick, Double Hit, Sky Uppercut, Blaze Kick, Rock Climb, Bone Club, Present, Sacred Fire, Aeroblast, Spacial Rend, Roar of Time, Psycho Boost, Seed Flare) and lifts the shaky big attacks: Mega Kick and Iron Tail to 90, Hydro Pump, Cross Chop and Focus Blast to 85, Dragon Rush and Head Smash to 100. It makes six moves never miss (Aurora Beam, Silver Wind, Ominous Wind, Water Pulse, Dragon Pulse, Leech Seed). The status side is the sharpest: Sing, Hypnosis and Grass Whistle to 70, Lovely Kiss to 90, Poison Powder to 100, Stun Spore to 90, Supersonic to 70, and Yawn becomes a 70% sleep that lands at once. Three go down: Jump Kick to 90, Leaf Storm to 85, Ice Ball to 70.

Weak attacks buffed. The ones still weak in Oxide get the most: Octazooka 65 to 95 at 100%, Mirror Shot 65 to 120, Magnet Bomb 60 to 100, Force Palm 60 to 85, Avalanche to a flat 100 at normal priority, Cross Poison 70 to 95, Psycho Cut 70 to 90, Ancient Power 60 to 80, Silver Wind and Ominous Wind 60 to 80, Needle Arm 60 to 80, Double Hit 35 to 60, Triple Kick 10 to 30, Fury Swipes 18 to 30, Beat Up 10 to 30, Pursuit 40 to 70, Vital Throw 70 to 90, Dizzy Punch 70 to 100 with 50% confusion, Poison Tail 50 to 120, Crush Claw 75 to 120, Clamp 35 to 120 and Constrict 10 to 100. Return and Frustration become a flat 121, and Wring Out a flat 75 doubled at half HP.

Strong attacks buffed further. Hyper Beam and Giga Impact go to 180, Mega Kick and Double-Edge to 140, Volt Tackle to 150 with 30% paralysis, and Aqua Tail, Iron Tail, Stone Edge, Aeroblast, Sacred Fire, Dynamic Punch, Spacial Rend and Judgment to 120. Crunch, Hyper Fang, Tri Attack, Signal Beam, Sludge Bomb and Sky Uppercut go to 95, Leaf Blade to 95, Shadow Ball, Extrasensory, Dragon Claw and Body Slam to 90. Kaizo cuts a few in return, each paired with a change that is a buff overall: Aurora Beam to 60 but never missing, Dig to 60 in one turn, Sky Attack to 120 in one turn, Leaf Storm and Overheat to 120 with no Sp. Atk drop, Rock Wrecker to three rising hits with no recharge. Pluck (50, 5 PP), Shadow Claw (25 hitting two to five times) and Thief (no item theft) are plain cuts.

PP, 66 fields in three groups. Big attacks get more (Hydro Pump, Hyper Beam, Mega Kick, Guillotine, Gunk Shot, Gyro Ball, Rock Wrecker and Extreme Speed at 8, Ancient Power 10, Giga Drain 15), as do Detect (10), Soft-Boiled (25), Sleep Talk (20), Recycle (15), Assist (35) and Metronome (40). Strong or priority attacks get fewer (Slam, Double-Edge, Flare Blitz and Roost 8; Poison Tail, Volt Tackle, Aqua Jet, Fake Out and Pluck 5; Bullet Punch, Ice Shard, Shadow Sneak and Aura Sphere 10; Sing 8; eight more to 15). And the disruptive status moves drop to setup levels: Screech, Smokescreen, Focus Energy, Safeguard, Foresight and Flash 5, Tickle and Cosmic Power 6, Charm, Feather Dance, Fake Tears, Metal Sound, Captivate, Encore, Bulk Up, Power Swap and Guard Swap 3, Sweet Scent 2, and Heal Bell, Aromatherapy, Natural Gift, Trump Card, Defog and Trick Room 1. Stockpile and Refresh go to 10 and Dark Void to 5.

Priority, 21 fields besides Teleport's. Kaizo gives +1 to the hazards (Spikes, Toxic Spikes, Stealth Rock), to Baton Pass, Transform, Spider Web, Magnet Rise, Gravity, Lunar Dance, Sleep Talk and Rollout; +2 to Extreme Speed, Sucker Punch (which then works whatever the target does), Tail Glow and Lucky Chant; +3 to Fake Out; +5 to Tailwind; and +7 to Trick Room, which it also makes permanent, as it does Gravity. Revenge and Avalanche lose their -4, and Bide goes to -1.

Recoil and secondary effects. The largest single family swaps a drawback for recoil: Hyper Beam, Giga Impact and Hydro Cannon lose the recharge turn for 1/2 recoil, as Draco Meteor loses its Sp. Atk drop and Outrage and Superpower lose their lock and drops; Blast Burn, Frenzy Plant, Overheat, Sky Attack, Thrash and Eruption take 1/3 recoil with a 10 to 30% status chance; Close Combat takes 1/4 recoil in place of its drops, and Brave Bird drops to 1/4. Eruption becomes a flat 150. Five attacks gain a high critical ratio (Drill Peck, Megahorn, Dragon Claw, X-Scissor, Power Whip). Twister and Submission become trapping moves, and every trapping move goes to 90 power (Clamp to 120, Crush Grip to 150). Status chances rise across the board, among them Slam 30% paralysis, Blizzard 20% freeze, Confusion 30%, Dizzy Punch 50%, Chatter 50%, Charge Beam 100%, Hyper Fang, Tri Attack, Volt Tackle, Dragon Rush and Rock Climb 30%, Aeroblast a 30% chance of any of three statuses. Minimize raises evasion two stages, Kinesis lowers accuracy two, Poison Gas badly poisons, Captivate ignores gender, and Lunar Dance heals half the user's HP in place of fainting. Fourteen moves gain a spread target (Sing, Supersonic, Screech, Smokescreen, Kinesis, Spider Web, Cotton Spore, Attract, Metal Sound, Petal Dance, Avalanche, Chatter, Attack Order, Roar of Time), and Thrash and Outrage lose theirs.

Type changes, 16 moves. Egg Bomb becomes Grass, Bone Club, Bonemerang and Rock Climb Rock, Glare, Super Fang, Bide and Absorb Dark, Stomp Ground, Rage Fighting, Vise Grip and Heart Swap Water, Constrict Ice and Swallow Poison. Endeavor and Nasty Plot become the ??? type, which would let Endeavor hit Ghosts.

Dead moves rebuilt as new attacks. Kaizo reuses 25 slots under new names and rebuilds about twenty more in place. Oxide has real moves for eight of the renamed ones and nothing for the rest:

| Kaizo's move | Slot | In Oxide |
|---|---|---|
| Mystical Fire | Bind | Mystical Fire, the real move (Kaizo's never misses, 20 PP) |
| Hurricane | Barrage | Hurricane (Kaizo 120, 70%) |
| Triple Axel | Psywave | Triple Axel (Kaizo's is special, 40 rising by 10) |
| Bulldoze | Magnitude | Bulldoze, the same |
| Wild Charge | Spark | Wild Charge (Kaizo 120 with paralysis) |
| Drill Run | Snatch | Drill Run, the same |
| Aqua Cutter | Heal Block | Aqua Cutter, the same |
| Scald | Water Sport | Scald, the same |
| Water Ball, Fire Ball, Rock Ball, Hail Ball | Comet Punch, Horn Attack, Defense Curl, Spike Cannon | none; plain 100-power attacks, special but for Fire Ball |
| Solar-Beam | Skull Bash | none; a 120 Grass attack with no charge turn |
| HP Water, Ice, Ghost, Fire, Rock, Dark, Psychic, Fighting, Ground, Grass, Electric, Flying | Splash, Conversion, Nightmare, Rapid Spin, Spit Up, Taunt, Trick, Arm Thrust, Mud Sport, Covet, Healing Wish, Switcheroo | none; Hidden Power keeps the IV formula (answer 3) |
| Swallow, Memento, Heart Swap, Rage, Absorb, Constrict, Vise Grip, Stomp, Lick | the same names | none; see the learnset section for what each became |

Taunt and Trick are worth a separate line. Kaizo deleted both to make room; Oxide keeps them.

### The very large buffs

These change what a fight looks like, and each would want a rescore on its own:

- Memento as a 255-power special self-KO, and Doom Desire at 250.
- Every trapping move at 90 power or more (Clamp 120, Crush Grip 150), which adds four or five turns of chip and a lock on switching to a solid hit.
- Hyper Beam and Giga Impact at 180 and 100% with no recharge, and Blast Burn, Frenzy Plant and Hydro Cannon without their recharge.
- Draco Meteor at 100% without its drop, Outrage and Superpower at 140 without their drawbacks, Overheat and Leaf Storm without their drops, and Eruption at a flat 150.
- The 120-power line: Volt Tackle 150, Hi Jump Kick 150, Mega Kick and Double-Edge 140, then Slam, Poison Tail, Crush Claw, Mirror Shot, Aqua Tail, Iron Tail, Stone Edge and Ice Ball at 120.
- Weak moves made strong: Constrict 10 to 100, Clamp 35 to 120, Mirror Shot 65 to 120, Magnet Bomb 60 to 100, Avalanche to a spread 100 at normal priority.
- Priority: Trick Room at +7 and permanent, Tailwind +5, Block +7, Fake Out +3, Extreme Speed at 100 power and +2, Sucker Punch +2 with no condition.
- Gravity permanent, Yawn as an instant 70% sleep, and Sheer Cold as a 70-power attack with a 100% effect chance.

## Learnsets

The first finding is the baseline. Oxide's native level-up learnsets are vanilla Platinum's for 480 of the 493 natives; the thirteen that differ are the base ROM's edits (Arbok, Vulpix, Ninetales, Poochyena, Mightyena, Beautifly, Delcatty, Empoleon, Luxray, Lugia) and element 4's Beat Up removal (Sneasel, Houndour, Houndoom). Kaizo rewrote nearly every line, and only six Kaizo lists match Oxide's. So this section compares Kaizo with vanilla.

Kaizo's names map cleanly. Every move in its learnsets names a real move Oxide has except Water Ball (Articuno, Zapdos, Moltres, Castform and Drifblim) and HP Water (the two Egg records). The renamed slots that appear (Mystical Fire, Hurricane, Triple Axel, Bulldoze, Wild Charge, Drill Run, Aqua Cutter, Scald) map to Oxide's real moves of those names. Moves Kaizo rebuilt under their own names (Swallow, Lick, Stomp and the rest) appear too, and are counted apart below, because Oxide's move of that name is a different move.

The comparison covers the 312 natives the player can own before the League, from the balance tool's own pool (`tools/oxide/balance/pool.py`, every split, evolutions reached at each cap included), in 145 evolution lines. A move Kaizo puts on an evolved stage below that stage's evolution level, or at level 1, is counted as a relearner move, since the player can only get it from the Move Relearner. Five patterns were checked by rule, and Appendix B lists every hit by line:

| Pattern | Rule | Species | Moves |
|---|---|---|---|
| Early coverage | an attack of 60 power or more, not Normal, of a type the species lacks, by level 26 (Gardenia's cap), where Oxide teaches that type no sooner than ten levels later and not by 36 | 102 | 131 |
| Given earlier | the same attack of 70 power or more, ten or more levels sooner than Oxide | 89 | 119 |
| Strong STAB Oxide lacks | a STAB attack of 85 power or more by level 78, where Oxide's list has none | 37 | 45 |
| Relearner moves | an attack of 80 power or more at level 1 or below the evolution level, which Oxide's list lacks | 122 | 304 |
| Kaizo-only moves | one of Kaizo's rebuilt moves with 60 power or more | 67 | 84 |

Power here is Oxide's power for the real move, since the idea is to teach Oxide's version.

### Early coverage

The commonest early gifts are cheap and narrow: Bite on thirteen lines, Signal Beam on eight, Aurora Beam on seven Water lines, Aerial Ace on seven, Rock Slide on six, and Dig, Crunch and Brick Break on five each. The Water starters' lines all get Ice early (Squirtle Ice Punch 22, Piplup Aurora Beam 16, Prinplup 13). Gligar gets Brick Break 9, X-Scissor 12 and Rock Slide 23; Nidoran M Earth Power 21; Nidoran F Dig 19; Zubat Steel Wing 17; Tentacool Psybeam 8 and Signal Beam 15; Pikachu Iron Tail 21.

The elemental punches need care. Oxide already has them at 95, from the base ROM, so Kaizo's Fire Punch on Machop at 22, Geodude at 25 and Plusle and Minun at 17, or Thunder Punch on Magby at 25, is a 95-power coverage move in Gardenia's split, where the cap is 26.

### Moves given earlier

The most common are Double-Edge (eight lines), Extrasensory (seven), Future Sight (six), and Power Gem, Hydro Pump, Rock Slide, Crunch and Earth Power (five each). The ones that matter most are where Oxide's level sits past the split the line is used in: Kadabra's Psycho Cut at 18 (Oxide 34), Koffing's Sludge Bomb at 28 (42), Croagunk's at 17 (43), Shinx's Discharge at 17 (41), Nosepass's Rock Slide at 7 (31) and Power Gem at 25 (49), Wooper's Muddy Water at 29 (47), Gabite's Dragon Claw at 19 (33), Larvitar's Dark Pulse at 5 (28), the lake trio's Extrasensory at 16 (51) and Relicanth's Hydro Pump at 15 (71). Three of Oxide's levels are past the League cap of 78 and so never reached before it: Nosepass and Probopass learn Earth Power at 79, and Giratina Aura Sphere at 90.

### Strong STAB on lines that lack it

Thirty-seven species have no STAB attack of 85 power by level 78 in Oxide and get one from Kaizo. They fall into a few groups:

| Group | Kaizo gives |
|---|---|
| Water lines stuck on weak Water moves | Hydro Pump to Starmie 55, Politoed 65, Octillery 57, Remoraid 50, Shellder 40, Wingull 47, Surskit 43 and Manaphy 54; Aqua Tail to Buizel 75 and Lumineon 53; Muddy Water to Corsola 28 and Luvdisc 46 |
| Flying lines | Brave Bird to Zubat 41, Golbat 65, Murkrow 55, Honchkrow 35 and Skarmory 45 |
| Ground lines | Earthquake to Phanpy 42, Vibrava 57 and Gliscor 55; Earth Power 49 and Dragon Pulse 57 to Flygon |
| Poison and Ice | Sludge Bomb 38 and Gunk Shot 44 to Stunky, Gunk Shot 62 to Skuntank, Sludge Bomb 56 to Gastly; Ice Fang 10 and Ice Punch 28 to Sneasel, Ice Punch 42 to Weavile, Ice Beam 29 and Blizzard 34 to Delibird |
| The rest | Bug Buzz to Scyther 17 and Scizor 13, and to Surskit 31; Mega Kick to Buneary 65 and Lopunny 73; Thunder Fang 35 and Thunder 55 to Pachirisu; Head Smash 53 to Corsola; Stone Edge 53 to Solrock; Meteor Mash 51 to Mawile; Psychic 30 to Chimecho; Leaf Blade 43 to Nuzleaf; Volt Tackle 65 to Pichu |

A second group sits under this one: the evolutions whose Oxide learnset stops when they evolve. Starmie (its best STAB is a 40-power move), Ludicolo (40), Floatzel (40), Mismagius (30), Roserade (60), Politoed and Cloyster (65) are all vanilla learnsets that give almost nothing after a stone or a late evolution. Kaizo gives each a real list, most of it at level 1, which in Oxide means the relearner. The Fairy retypes are a separate gap Kaizo cannot help with, since Kaizo has no Fairy moves: Clefairy, Clefable, Togetic and Granbull have no Fairy attack by level in either game.

### Relearner moves

Kaizo loads its evolved stages' level 1 with strong moves: Body Slam on 26 of them, Double-Edge on 16, Fire Punch on 12, Iron Head and Dig on 10, Ice Punch, Ice Beam, Thunder Punch and Poison Jab on 9. Charizard's Earthquake, Raichu's Surf and Focus Blast, Nidoqueen's Thunderbolt and Ice Beam, Machamp's Close Combat, Abomasnow's Stone Edge and Probopass's Head Smash are typical. In Oxide each would be a Move Relearner option in Pastoria (Wake's split, cap 44) at one Heart Scale each, and Heart Scales became scarcer when the Underground closed (Ian, 2026-09-27).

### Kaizo-only moves in the learnsets

Eleven of Kaizo's rebuilt moves appear 84 times in the lists of obtainable species (Heatran is counted, though Stark Mountain's last room no longer gives it). Each is an idea for a real Oxide move, not a move to copy:

| Kaizo move | What it is in Kaizo | Lines | Nearest real move in Oxide |
|---|---|---|---|
| Vise Grip | physical Water 90, traps | Krabby, Corphish and Shellder lines, Croconaw, Feraligatr, Gligar, Scizor, Gyarados, Huntail, Gorebyss, Carvanha, Mawile, Drapion (16 species) | Crabhammer, Liquidation or Aqua Cutter |
| Swallow | physical Poison 90, traps, ignores Protect | Tangela and Wailmer lines, Steelix, Slowpoke, Carnivine, Pelipper, Whiscash, Dusknoir, Lickilicky, Munchlax, Mawile, Huntail, Heatran (15 species) | Poison Jab |
| Lick | physical Ghost 80 | Gastly and Lickitung lines, Snorlax, Munchlax, Jynx, Smoochum, Snubbull, Granbull (11 species) | Shadow Claw |
| Stomp | physical Ground 90 | Ponyta, Rhyhorn and Lickitung lines, Grotle, Girafarig (8 species) | High Horsepower (95) or Stomping Tantrum (75) |
| Memento | special Dark 255, faints the user | Hoppip line, Duskull, Dusclops, Uxie (6 species) | Explosion |
| Absorb | special Dark 60, drains | Hoppip, Skiploom, Lotad, Lombre, Seedot, Tentacruel, Tangela (7 species) | none: Oxide has no draining Dark move |
| Rage | physical Fighting 70, Pursuit's effect | Primeape, Carvanha, Sharpedo, Vespiquen (4 species) | none with the effect; Brick Break for the type |
| Heart Swap | special Water 95, drains | Ralts line, Luvdisc, Manaphy (5 species) | none: Oxide has no draining Water move |
| Egg Bomb, Water Ball, Bonemerang | Grass 100; special Water 100; Rock 60 twice | Chansey and Blissey; Castform and Drifblim; Lucario | Seed Bomb; Surf; none |

### Where Kaizo's lists clash with Ian's rulings

Weather: none. Kaizo's level-up lists teach no weather move to any species. Castform gets Hydro Pump, Flamethrower and Ice Beam at 20, which is Kaizo covering its forms; in Oxide the player never sets weather, so for Castform they would be plain coverage.

The move pool's first cut: Kaizo gives Teleport to 47 species, 85 times, often two or three times in one list (Gastly at 1, 39 and 53; Mr. Mime four times). Its line gives Teleport only +1 priority, so in a trainer battle it presumably still fails, and it reads as filler. Oxide removes Teleport, so there is nothing to take.

Setup PP: Kaizo teaches setup early to seven species (Iron Defense to Silcoon and Cascoon at 7, Barrier to Mr. Mime at 8, Glaceon at 21 and Mime Jr. at 22, Cosmic Power to Clefairy at 19, Curse to Spiritomb at 20). Oxide's 1 to 3 PP blunts these. Cosmic Power, the one exception at `b775fc8c` with its vanilla 20 PP, has been at 3 since answer 2 (d63b39aed).

Level caps and splits: an early Kaizo move can put 85 power or more in Roark's or Gardenia's split. Ponyta's Stomp (Ground 90) at 6 and Gligar's Vise Grip (Water 90) at 5 land in Roark's split, as do Self-Destruct on Geodude, Seedot and Corsola at 13 to 15. In Gardenia's split Snover gets Ice Punch 5, Ice Beam 13, Focus Blast 21 and Blizzard 26; the punch users above get 95-power coverage; Nidoran M gets Earth Power at 21, Houndour and Togepi Double-Edge at 22 and 24, Barboach Future Sight at 26 and Bronzor Explosion at 26. Any of these taken into Oxide needs the balance track's rescore of those splits. Kaizo's moves past level 78 (51 species) are out of reach before the League and were left out.

A finding outside the comparison: Kaizo's view that setup is expensive, which Oxide shares, was applied unevenly in Oxide at `b775fc8c`. Bulk Up, Cosmic Power and Stockpile are at 20 PP, Focus Energy at 30 and Defend Order at 10, all vanilla, while Swords Dance, Nasty Plot, Dragon Dance and the rest are at 1 to 3. The new moves' setup is at modern PP (Quiver Dance and Coil 20, Shell Smash and Hone Claws 15, Work Up 30, Shift Gear 10). Answer 1 ("no setup move's PP changes") protects the low values; it does not say whether these should join them. Ian's answer 2 said they should, and all of them are now at 1 to 3 PP (d63b39aed).

## Recommended short lists

For moves, the modern scale of answer 1 is the frame: any Kaizo number taken is a deliberate exception, as the base ROM's own values are. These are the changes that fix a real gap without being one of the very large buffs:

1. Bring every setup move to the setup PP: Bulk Up, Cosmic Power, Stockpile, Focus Energy and Defend Order, and the new moves' Quiver Dance, Coil, Shell Smash, Hone Claws, Work Up, Shift Gear and the rest. Kaizo cuts Bulk Up to 3 and Cosmic Power to 6. Data only.
2. Fake Out at +3 and Extreme Speed at +2, which are both Kaizo's and, from memory, the modern values, since answer 1 covered power, accuracy and PP but not priority. Minimize at +2 evasion and Cotton Spore on both foes are Kaizo's and, again from memory, modern too. Not checked against hg-engine, which the cloud does not have.
3. Kaizo's low PP on the stat-lowering status moves (Screech, Metal Sound, Fake Tears, Charm, Feather Dance, Tickle, Captivate at 3 to 6, Sweet Scent at 2), which treats them like setup in reverse and fits the same ruling.
4. The high critical ratio on Drill Peck, Megahorn, Dragon Claw, X-Scissor and Power Whip: a modest buff to five mid-tier attacks that many lines use.
5. The weak signature attacks that Oxide keeps at a level no line wants: Octazooka (65, 85%), Mirror Shot (65, 85%), Magnet Bomb (60), Needle Arm (60), Poison Tail (50), Crush Claw (75), each to about 80 to 90 rather than Kaizo's 95 to 120.
6. Accuracy for the unreliable mid attacks where the modern value is still below 100: Hyper Fang, Octazooka, Rock Climb, Sky Uppercut, Double Hit and Dragon Rush. Kaizo's 100 is an exception to the modern scale.

Left off on purpose: the trapping moves at 90, the recoil-for-recharge family, every 120-plus buff, Trick Room and Tailwind priority, Memento, Doom Desire, and the fixed-type Hidden Powers (ruled out by answer 3).

For learnsets, the ideas worth the balance track's learnset pass, in order:

1. A real level-up tail for the evolutions that stop learning: Starmie, Politoed, Ludicolo, Floatzel, Cloyster, Mismagius and Roserade, with Kaizo's lists as the model and the moves placed at levels the player reaches rather than at level 1.
2. STAB of 85 power or more by the League for the 37 species that lack one, starting with the ones people use: Hydro Pump for Starmie, Politoed and Octillery, Brave Bird for Honchkrow and Skarmory, Earthquake for Gliscor and Flygon, Ice Punch for Sneasel and Weavile, Gunk Shot for Skuntank, Bug Buzz for Scyther.
3. Early coverage that stays under the split's power: Bite, Aurora Beam, Signal Beam, Steel Wing and Aerial Ace at Kaizo's levels are 60 to 75 power and safe. The 95-power punches and Earth Power by level 26 are not, and belong one split later.
4. Moves Oxide teaches past the League cap: Earth Power for Nosepass and Probopass at 79 (Kaizo 43 and 7), and Aura Sphere for Giratina at 90.
5. Moves given much earlier where Oxide's level is past the line's split: Kadabra's Psycho Cut, Koffing's and Croagunk's Sludge Bomb, Shinx's Discharge, Gabite's Dragon Claw, the lake trio's Extrasensory and Relicanth's Hydro Pump.
6. Kaizo's rebuilt moves turned into real ones: Ground coverage for Ponyta and Rhyhorn (High Horsepower at a later level than Kaizo's 6), a Water attack for Krabby and Corphish sooner than Crabhammer, Seed Bomb for Chansey.

## Questions for Ian (answered in the next section)

1. Should any Kaizo number come into Oxide as a deliberate exception to the modern scale of answer 1, as the base ROM's own values did, or only the items in the moves short list?
2. Should every setup move be at the low setup PP, including Bulk Up, Cosmic Power, Stockpile, Focus Energy and Defend Order (still at vanilla PP) and the new moves' setup such as Quiver Dance, Shell Smash and Coil (at modern PP)?
3. Should the stat-lowering status moves (Screech, Metal Sound, Fake Tears, Charm, Feather Dance, Tickle, Captivate, Sweet Scent) get setup-level PP as well?
4. Does answer 1 cover priority, so that Fake Out goes to +3 and Extreme Speed to +2?
5. Kaizo makes sleep and powders reliable (Sing, Hypnosis and Grass Whistle 70, Lovely Kiss 90, Poison Powder 100, Stun Spore 90). Answer 2 kept Thunder Wave, Dark Void and Swagger at Generation 4 accuracy. Does the same stance hold for these?
6. For the learnset pass, should Kaizo's lists serve as a line-by-line template, or only as the source of the short list above?
7. Should strong moves sit at level 1 on evolved stages, as Kaizo does, now that each costs a Heart Scale at Pastoria and Heart Scales are scarcer?
8. Is there a ceiling on coverage power per split? Kaizo's lists would put 95-power punches and 90-power Earth Power and Ice Beam in Gardenia's split, where the cap is 26.

## Ian's answers (2026-09-27)

1. Only the moves short list above comes in as exceptions to answer 1's modern scale. The very large buffs stay out.
2. Every setup move goes to the 1 to 3 PP band: Bulk Up, Cosmic Power, Stockpile, Focus Energy and Defend Order, and the new moves' setup (Quiver Dance, Coil, Shell Smash, Hone Claws, Work Up, Shift Gear and the rest).
3. The stat-lowering status moves take Kaizo's low PP: Screech, Metal Sound, Fake Tears, Charm, Feather Dance, Tickle and Captivate at 3 to 6, and Sweet Scent at 2.
4. Answer 1 covers priority: every Generation 4 move whose priority changed in later games takes the modern value, Fake Out +3 and Extreme Speed +2 among them, each checked against hg-engine.
5. Sleep moves and powders keep their accuracy, the same stance as answer 2.
6. Kaizo's level-up lists are studied, not copied (Ian, 2026-09-27, correcting the first reading of "line-by-line template"): relate each move's level to its real strength as Kaizo has the move, same-type or coverage, evolution stage and the split it lands in; write the findings as rules tested by how well they predict Kaizo's own lists; and build a generator that applies them to any species and any move, later-generation moves included, proposing lists inside Oxide's caps and dropping dead-weight moves. Nothing is written to the game data until Ian chooses a sweeping pass, after the broken moves are fixed. The copy made on `cloud/balance-learnset-pass` stays unmerged as reference. Ian confirmed the study's rules (2026-09-27), added Astonish, Rollout, Fire Spin, Fury Cutter, Whirlpool, Sand Tomb, Bind, Sky Attack and Skull Bash to the dead weight, and asked for three more analyses: delays (a pre-evolution given a strong move a split or more before its evolution), the four moves each wild Pokemon carries in Kaizo's tables and Oxide's (and so the risk, such as a Growlithe that may Roar, since wild Pokemon choose at random), and fully evolved catches that lack good moves without the relearner.
7. Strong moves may sit at level 1 on evolved stages, as Kaizo has them, which makes each a Heart Scale's worth at the Move Relearner.
8. No split has a ceiling on coverage power; the rescore judges each move.

Later answer (2026-10-06, from the learnset insight sessions): the rampage
moves come in as one-turn moves. Thrash, Petal Dance and Outrage take Kaizo's
versions from the short list above; Uproar and Raging Fury, which Kaizo
lacks, get one-turn versions on the same pattern. A two- or three-turn lock is
too dangerous in a permadeath run.

## Appendix A: every Kaizo move line

One row per line of `kaizo-move-changes.md`, in its order. "Kaizo" gives the values Kaizo sets, "Oxide now" the same fields in Oxide's tree, and "Detail" each field's verdict. A ruling named "base ROM" means Oxide's value differs from vanilla and from every ruling list, so it is taken to be the base ROM's own. A "chance" change on a move whose effect reads no chance (Seed Bomb, Wake-Up Slap, Bulk Up) would do nothing in battle unless Kaizo also changed the effect.

| Move | Kaizo | Oxide now | Verdict | Detail |
|---|---|---|---|---|
| DoubleSlap | Hits twice; power 30; accuracy 90 | 15, 100 | partly | hits exactly twice; Oxide still hits 2 to 5 times: lacks; power lacks; accuracy ruling: base ROM 100 |
| Comet Punch (Kaizo: Water Ball) | power 100; type Water; accuracy 100 | 18, Normal, 85 | Kaizo-only | Kaizo-only move (Water Ball, special Water 100, no effect); Oxide has no such move |
| Fire Punch | power 95 | 95 | has | power has |
| Ice Punch | power 95 | 95 | has | power has |
| ThunderPunch | power 95 | 95 | has | power has |
| ViceGrip | Whirlpool effect; power 90; type Water | 55, Normal | lacks | rebuilt as a Water trapping move; lacks; power lacks; type lacks |
| Guillotine | PP 8 | 5 | lacks | PP lacks |
| Cut | accuracy 100 | 100 | has | accuracy has |
| Bind (Kaizo: Mystical Fire) | power 75; type Fire; accuracy never misses; effect chance 100% | 15, Normal, 85, 0% | real move | real move: Oxide has Mystical Fire (75, 100 accuracy, 10 PP); Kaizo's never misses and has 20 PP |
| Slam | Chance to Paralyze; power 120; accuracy 100; PP 8; effect chance 30% | 100, 100, 20, 0% | partly | 30% paralysis; lacks; power ruling: base ROM 100; accuracy has; PP lacks; effect chance lacks |
| Stomp | power 90; type Ground | 65, Normal | lacks | power lacks; type lacks |
| Mega Kick | power 140; accuracy 90; PP 8 | 120, 75, 5 | lacks | power lacks; accuracy lacks; PP lacks |
| Jump Kick | power 120; accuracy 90 | 100, 95 | partly | power ruling: modern 100; accuracy lacks |
| Rolling Kick | accuracy 100 | 100 | has | accuracy has |
| Sand-Attack | PP 5 | 5 | has | PP has |
| Horn Attack (Kaizo: Fire Ball) | power 100; type Fire | 65, Normal | Kaizo-only |  |
| Fury Attack | accuracy 100 | 100 | has | accuracy has |
| Tackle | accuracy 100 | 100 | has | accuracy has |
| Body Slam | power 90 | 85 | lacks | power lacks |
| Wrap | Whirlpool effect; accuracy 100 | 90 | has, by ruling | trapping, as Oxide already has; accuracy ruling: modern 90 |
| Take Down | accuracy 100 | 100 | has | accuracy has |
| Thrash | Chance of causing Paralysis; 1/3 damage dealt recoil; power 120; effect chance 20%; hits one opponent | 120, 0% | partly | rebuilt: 20% paralysis and 1/3 recoil in place of the rampage, one target; lacks; power has (modern); effect chance lacks; lacks (Oxide hits a random foe) |
| Double-Edge | power 140; PP 8 | 120, 15 | lacks | power lacks; PP lacks |
| Tail Whip | PP 1 | 3 | ruling | PP ruling: base ROM 3 |
| Poison Sting | power 40 | 40 | has | power has |
| Twineedle | power 50; effect chance 30% | 40, 20% | partly | power ruling: base ROM 40; effect chance lacks |
| Pin Missile | power 25; accuracy 100; PP 15 | 25, 100, 20 | partly | power has (modern); accuracy has; PP lacks |
| Sing | accuracy 70; PP 8; hits both opponents and ally | 55, 15 | lacks | accuracy lacks; PP lacks; lacks (one target) |
| Supersonic | accuracy 70; hits both opponents | 55 | lacks | accuracy lacks; lacks (one target) |
| SonicBoom | accuracy 100 | 100 | has | accuracy has |
| Disable | accuracy 100 | 100 | has | accuracy has |
| Mist | PP 3 | 3 | has | PP has |
| Hydro Pump | accuracy 85; PP 8 | 80, 5 | lacks | accuracy lacks; PP lacks |
| Blizzard | effect chance 20% | 10% | lacks | effect chance lacks |
| Aurora Beam | Always hits; power 60; accuracy never misses; effect chance 0% | 65, 100, 10% | lacks | never misses, no Attack drop; lacks; power lacks; accuracy lacks; effect chance lacks |
| Hyper Beam | 1/2 damage dealt recoil, fixed AI; power 180; accuracy 100; PP 8 | 150, 90, 5 | lacks | 1/2 recoil in place of the recharge turn; lacks; power lacks; accuracy lacks; PP lacks |
| Peck | power 40 | 40 | has | power has |
| Drill Peck | High crit ratio |  | lacks | high critical ratio; lacks |
| Submission | Whirlpool effect; power 90; accuracy 100; PP 8 | 80, 80, 20 | partly | trapping in place of recoil; lacks; power lacks; accuracy lacks; PP ruling: modern 20 |
| Absorb | power 60; type Dark | 20, Grass | lacks | power lacks; type lacks |
| Leech Seed | accuracy never misses | 90 | lacks | accuracy lacks |
| Growth | PP 5 | 3 | ruling | PP ruling: base ROM 3 |
| Razor Leaf | power 60; accuracy 100 | 55, 100 | partly | power lacks; accuracy has |
| PoisonPowder | accuracy 100 | 75 | lacks | accuracy lacks |
| Stun Spore | accuracy 90 | 75 | lacks | accuracy lacks |
| Petal Dance | Chance to Confuse; power 100; effect chance 20%; hits both opponents | 120, 0% | partly | 20% confusion on the target in place of the rampage, both foes; lacks; power ruling: modern 120; effect chance lacks; lacks (a random foe) |
| String Shot | accuracy 100 | 100 | has | accuracy has |
| Fire Spin | Whirlpool effect; power 90; accuracy 100 | 35, 100 | has, by ruling | trapping, as Oxide already has; power ruling: modern 35; accuracy has |
| Rock Throw | accuracy 100 | 100 | has | accuracy has |
| Dig | No Effect; power 60 | 80 | lacks | one-turn attack, no semi-invulnerable turn; lacks; power lacks |
| Toxic | accuracy 100 | 100 | has | accuracy has |
| Confusion | effect chance 30% | 10% | lacks | effect chance lacks |
| Hypnosis | accuracy 70 | 60 | lacks | accuracy lacks |
| Meditate | PP 1 | 3 | ruling | PP ruling: base ROM 3 |
| Agility | PP 1 | 1 | has | PP has |
| Rage | Pursuit effect; power 70; type Fighting | 20, Normal | lacks | rebuilt as a Fighting Pursuit; lacks; power lacks; type lacks |
| Teleport | priority +1 | 0 | cut | Teleport leaves every learnset in Oxide (the move pool's first cut); priority lacks |
| Screech | accuracy 100; PP 5; hits both opponents | 100, 40 | partly | accuracy has; PP lacks; lacks (one target) |
| Double Team | PP 6 | 6 | has | PP has |
| Harden | PP 5 | 5 | has | PP has |
| Minimize | Sharply raises Evasion, Status; PP 3 | 3 | partly | +2 evasion; Oxide gives +1: lacks; PP has |
| SmokeScreen | PP 5; hits both opponents and ally | 20 | lacks | PP lacks; lacks (one target) |
| Withdraw | PP 5 | 3 | ruling | PP ruling: base ROM 3 |
| Defense Curl (Kaizo: Rock Ball) | power 100; type Rock; accuracy 100; PP 15 | 0, Normal, never misses, 3 | Kaizo-only | Kaizo-only move (Rock Ball, special Rock 100); Oxide has no such move |
| Barrier | PP 5 | 1 | ruling | PP ruling: setup PP 1 |
| Light Screen | PP 2 | 1 | ruling | PP ruling: base ROM 1 |
| Reflect | PP 2 | 1 | ruling | PP ruling: base ROM 1 |
| Focus Energy | PP 5 | 30 | lacks | PP lacks |
| Bide | Damage= 1.5x damage dealt by the target's last attack; type Dark; priority -1 | Normal, +1 | lacks | Dark, 1.5x the last hit taken, one target, -1 priority; lacks; type lacks; priority lacks |
| Metronome | PP 40 | 10 | lacks | PP lacks |
| Egg Bomb | type Grass; accuracy 100 | Normal, 100 | partly | type lacks; accuracy has |
| Lick | power 80; PP 15 | 40, 30 | partly | power ruling: base ROM 40; PP lacks |
| Smog | power 60; accuracy 100; effect chance 50%; hits both opponents | 55, 100, 30% | has, by ruling | power ruling: base ROM 55; accuracy has; effect chance ruling: base ROM 30%; has (both foes, a base ROM edit) |
| Sludge | power 70 | 65 | lacks | power lacks |
| Bone Club | type Rock; accuracy 100 | Ground, 85 | lacks | type lacks; accuracy lacks |
| Clamp | Whirlpool effect; power 120 | 35 | partly | trapping, as Oxide already has; power lacks |
| Skull Bash (Kaizo: Solar-Beam) | power 120; type Grass; effect chance 0% | 130, Normal, 100% | Kaizo-only | Kaizo-only move (Solar-Beam, special Grass 120 with no charge turn); Oxide has no such move |
| Spike Cannon (Kaizo: Hail Ball) | power 100; type Ice; PP 10 | 20, Normal, 15 | Kaizo-only | Kaizo-only move (Hail Ball, special Ice 100); Oxide has no such move |
| Constrict | No Effect, Special; power 100; type Ice; PP 15; effect chance 0% | 10, Normal, 35, 10% | lacks | rebuilt as a special Ice 100 with no effect; lacks; power lacks; type lacks; PP lacks; effect chance lacks |
| Amnesia | PP 3 | 1 | ruling | PP ruling: base ROM 1 |
| Kinesis | Sharply lowers Accuracy, Status; accuracy 100; hits both opponents | 100 | partly | -2 accuracy; lacks; accuracy has; lacks (one target) |
| Softboiled | PP 25 | 10 | lacks | PP lacks |
| Hi Jump Kick | power 150 | 130 | ruling | power ruling: modern 130 |
| Glare | type Dark; accuracy 100 | Normal, 100 | partly | type lacks; accuracy has |
| Poison Gas | Badly Poisons; accuracy 85; hits both opponents and ally | 85 | partly | badly poisons; lacks; accuracy has; ruling: both foes only (Ian, 2026-09-22) |
| Barrage (Kaizo: Hurricane) | power 120; type Flying; accuracy 70; PP 8; effect chance 10% | 15, Normal, 85, 20, 0% | real move | real move: Oxide has Hurricane (110, 80%, 10 PP, 30% confusion); Kaizo's is 120, 70%, 8 PP, 10% confusion |
| Leech Life | power 80 | 80 | has | power has |
| Lovely Kiss | accuracy 90 | 75 | lacks | accuracy lacks |
| Sky Attack | Chance of causing Paralysis; 1/3 damage dealt recoil; power 120; accuracy 100; effect chance 20% | 140, 100, 30% | partly | one turn, 20% paralysis and 1/3 recoil in place of the charge turn; lacks; power lacks; accuracy has; effect chance lacks |
| Transform | priority +1 | 0 | lacks | priority lacks |
| Bubble | power 40; effect chance 20% | 40, 10% | partly | power has; effect chance lacks |
| Dizzy Punch | power 100; effect chance 50% | 70, 20% | lacks | power lacks; effect chance lacks |
| Flash | PP 5 | 20 | lacks | PP lacks |
| Psywave (Kaizo: Triple Axel) | power 40; type Ice; accuracy 100 | 1, Psychic, 100 | real move | real move: Oxide has Triple Axel (physical, 20 rising by 20, 90%); Kaizo's is special, 40 rising by 10, 100% |
| Splash (Kaizo: HP Water) | power 70; type Water; accuracy 100; PP 20 | 0, Normal, never misses, 40 | Kaizo-only | Kaizo-only move (HP Water, special Water 70); Splash leaves every learnset in Oxide (first cut) |
| Acid Armor | PP 1 | 1 | has | PP has |
| Crabhammer | power 120; accuracy 100 | 100, 95 | ruling | power ruling: modern 100; accuracy ruling: base ROM 95 |
| Fury Swipes | power 30; accuracy 90 | 18, 100 | partly | power lacks; accuracy ruling: base ROM 100 |
| Bonemerang | power 60; type Rock; accuracy 100 | 50, Ground, 100 | partly | power lacks; type lacks; accuracy has |
| Rest | PP 3 | 3 | has | PP has |
| Rock Slide | accuracy 100 | 90 | lacks | accuracy lacks |
| Hyper Fang | power 95; accuracy 100; effect chance 30% | 80, 90, 10% | lacks | power lacks; accuracy lacks; effect chance lacks |
| Sharpen | PP 3 | 3 | has | PP has |
| Conversion (Kaizo: HP Ice) | power 70; type Ice; accuracy 100 | 0, Normal, never misses | Kaizo-only | Kaizo-only move (HP Ice, special Ice 70); Hidden Power keeps its IV formula (ruling 3) |
| Tri Attack | power 95; effect chance 30% | 80, 20% | lacks | power lacks; effect chance lacks |
| Super Fang | type Dark; accuracy 100 | Normal, 90 | lacks | type lacks; accuracy lacks |
| Substitute | PP 2 | 2 | has | PP has |
| Triple Kick | power 30; accuracy 100 | 10, 90 | lacks | power lacks; accuracy lacks |
| Thief | Splash effect |  | lacks | no item theft; lacks (a nerf) |
| Spider Web | hits both opponents; priority +1 | 0 | lacks | lacks (one target); priority lacks |
| Nightmare (Kaizo: HP Ghost) | power 70 | 0 | Kaizo-only | Kaizo-only move (HP Ghost, special Ghost 70); Hidden Power keeps its IV formula (ruling 3) |
| Flame Wheel | power 70 | 60 | lacks | power lacks |
| Snore | power 80 | 80 | has | power has |
| Curse | PP 3 | 3 | has | PP has |
| Aeroblast | Chance of either Paralyzing; Burning; or Freezing target; power 120; accuracy 100; effect chance 30% | 100, 95, 0% | lacks | 30% paralysis, burn or freeze in place of the high critical ratio; lacks; power lacks; accuracy lacks; effect chance lacks |
| Cotton Spore | accuracy 100; hits both opponents | 100 | partly | accuracy has (modern); lacks (one target) |
| Mach Punch | PP 15 | 30 | lacks | PP lacks |
| Scary Face | accuracy 100 | 100 | has | accuracy has (modern) |
| Sweet Kiss | accuracy 100 | 100 | has | accuracy has |
| Belly Drum | PP 1 | 1 | has | PP has |
| Sludge Bomb | power 95 | 90 | lacks | power lacks |
| Octazooka | power 95; accuracy 100 | 65, 85 | lacks | power lacks; accuracy lacks |
| Spikes | priority +1 | 0 | lacks | priority lacks |
| Foresight | PP 5 | 40 | lacks | PP lacks |
| Detect | PP 10 | 5 | lacks | PP lacks |
| Bone Rush | accuracy 100 | 90 | ruling | accuracy ruling: modern 90 |
| Outrage | 1/2 damage dealt recoil, fixed AI; power 140; hits one opponent | 120 | lacks | 1/2 recoil in place of the rampage, one target; lacks; power lacks; lacks (a random foe) |
| Sandstorm | PP 1 | 1 | has | PP has |
| Giga Drain | power 75; PP 15 | 75, 10 | partly | power has (modern); PP lacks |
| Charm | PP 3 | 20 | lacks | PP lacks |
| Rollout | No Effect; power 40; accuracy 100; PP 5; priority +1 | 30, 90, 20, 0 | partly | a plain 40 power +1 priority Rock attack; Oxide has this as Accelerock; power lacks; accuracy lacks; PP lacks; priority lacks |
| Swagger | accuracy 100 | 90 | ruling | accuracy ruling: Gen 4 accuracy kept (answer 2) |
| Spark (Kaizo: Wild Charge) | power 120; effect chance 20% | 65, 30% | real move | real move: Oxide has Wild Charge (90, 100%, 15 PP, recoil); Kaizo's is 120 with 20% paralysis and 1/3 recoil |
| Fury Cutter | Hits the target up to 3 times; increases power by 10 with each hit; power 30; accuracy 100 | 40, 95 | partly | three hits rising by 10, like Triple Axel; lacks; power ruling: modern 40; accuracy lacks |
| Steel Wing | power 80; accuracy 100 | 70, 90 | lacks | power lacks; accuracy lacks |
| Mean Look | priority +1 | +1 | has | priority has |
| Attract | hits both opponents |  | lacks | lacks (one target) |
| Sleep Talk | PP 20; priority +1 | 10, 0 | lacks | PP lacks; priority lacks |
| Heal Bell | PP 1 | 5 | lacks | PP lacks |
| Return | No Effect; power 121 | 1 | lacks | flat 121 power, no friendship; lacks; power lacks |
| Present | accuracy 100 | 90 | lacks | accuracy lacks |
| Frustration | No Effect; power 121 | 1 | lacks | flat 121 power, no friendship; lacks; power lacks |
| Safeguard | PP 5 | 25 | lacks | PP lacks |
| Sacred Fire | power 120; accuracy 100 | 100, 95 | lacks | power lacks; accuracy lacks |
| Magnitude (Kaizo: Bulldoze) | power 60; effect chance 100% | 1, 0% | real move | real move: Oxide has Bulldoze (60, 100%, 20 PP, Speed drop), which matches Kaizo but for its 30 PP |
| DynamicPunch | power 120 | 100 | lacks | power lacks |
| Megahorn | High crit ratio |  | lacks | high critical ratio; lacks |
| DragonBreath | power 70 | 60 | lacks | power lacks |
| Baton Pass | priority +1 | 0 | lacks | priority lacks |
| Encore | PP 3 | 5 | lacks | PP lacks |
| Pursuit | power 70; PP 15 | 40, 20 | lacks | power lacks; PP lacks |
| Rapid Spin (Kaizo: HP Fire) | power 70; type Fire; PP 15 | 60, Normal, 40 | Kaizo-only | Kaizo-only move (HP Fire); Oxide keeps Rapid Spin as hazard removal with a Speed raise (ruling 7) |
| Sweet Scent | PP 2 | 20 | lacks | PP lacks |
| Iron Tail | power 120; accuracy 90 | 100, 75 | lacks | power lacks; accuracy lacks |
| Metal Claw | accuracy 100 | 95 | lacks | accuracy lacks |
| Vital Throw | Always hits; power 90 | 70 | partly | never misses, as Oxide already has; power lacks |
| Cross Chop | accuracy 85 | 80 | lacks | accuracy lacks |
| Twister | Whirlpool effect; power 90; PP 15; effect chance 0% | 40, 20, 20% | lacks | trapping in place of flinch; lacks; power lacks; PP lacks; effect chance lacks |
| Rain Dance | PP 1 | 1 | has | PP has |
| Sunny Day | PP 1 | 1 | has | PP has |
| Crunch | power 95 | 80 | lacks | power lacks |
| ExtremeSpeed | No Effect; power 100; PP 8; priority +2 | 80, 5, +1 | partly | plain hit, as Oxide already has; power lacks; PP lacks; priority lacks |
| AncientPower | power 80; PP 10 | 60, 5 | lacks | power lacks; PP lacks |
| Shadow Ball | power 90 | 80 | lacks | power lacks |
| Future Sight | power 120; accuracy 100 | 120, 100 | has | power has (modern); accuracy has |
| Whirlpool | power 90; accuracy 100 | 35, 100 | has, by ruling | power ruling: modern 35; accuracy has |
| Beat Up | power 30 | 10 | lacks | power lacks |
| Fake Out | PP 5; priority +3 | 10, +1 | lacks | PP lacks; priority lacks |
| Stockpile | Raises user's Def and SpDef; PP 10 | 20 | partly | raises Defense and Sp. Def, as Oxide already has; PP lacks |
| Spit Up (Kaizo: HP Rock) | power 70; type Rock; PP 15 | 1, Normal, 10 | Kaizo-only | Kaizo-only move (HP Rock, Rock 70); Hidden Power keeps its IV formula (ruling 3) |
| Swallow | Whirlpool effect, Physical; power 90; type Poison; accuracy 100 | 0, Normal, never misses | lacks | rebuilt as a physical Poison 90 trapping move that ignores Protect; lacks; power lacks; type lacks; accuracy lacks |
| Heat Wave | accuracy 100 | 90 | lacks | accuracy lacks |
| Hail | PP 1 | 1 | has | PP has |
| Will-O-Wisp | accuracy 85 | 85 | has | accuracy has (modern) |
| Memento | Selfdestruct/ Explosion effect, Special; power 255 | 0 | lacks | rebuilt as a 255 power special self-KO; lacks; power lacks |
| Facade | power 80 | 70 | lacks | power lacks |
| SmellingSalt | power 90 | 70 | ruling | power ruling: modern 70 |
| Charge | PP 1 | 3 | ruling | PP ruling: base ROM 3 |
| Taunt (Kaizo: HP Dark) | power 70; PP 15 | 0, 20 | Kaizo-only | Kaizo-only move (HP Dark); Oxide keeps Taunt |
| Trick (Kaizo: HP Psychic) | power 70; PP 15 | 0, 10 | Kaizo-only | Kaizo-only move (HP Psychic); Oxide keeps Trick |
| Assist | PP 35 | 20 | lacks | PP lacks |
| Ingrain | PP 1 | 1 | has | PP has |
| Superpower | 1/2 damage dealt recoil, fixed AI; power 140 | 120 | lacks | 1/2 recoil in place of the stat drops; lacks; power lacks |
| Recycle | PP 15 | 10 | lacks | PP lacks |
| Revenge | 2x Power if user moves after target; priority 0 | -4 | lacks | 2x power when moving second, normal priority; lacks; priority lacks |
| Yawn | Causes Sleep; accuracy 70; effect chance 100% | never misses, 0% | lacks | sleep at once, 70% accuracy; lacks; accuracy lacks; effect chance lacks |
| Knock Off | power 80 | 70 | ruling | power ruling: flat 70 (answer 7) |
| Endeavor | type ??? | Normal | lacks | type lacks |
| Eruption | Chance of causing Burn; 1/3 damage dealt recoil; effect chance 20% | 0% | lacks | rebuilt: flat 150 with 20% burn and 1/3 recoil in place of HP-based power; lacks; effect chance lacks |
| Skill Swap | PP 2 | 2 | has | PP has |
| Refresh | PP 10 | 20 | lacks | PP lacks |
| Snatch (Kaizo: Drill Run) | power 80; type Ground; accuracy 100; priority 0 | 0, Dark, never misses, +4 | real move | real move: Oxide has Drill Run (80, 100%, 10 PP, high critical ratio), which matches Kaizo |
| Secret Power | power 85 | 70 | lacks | power lacks |
| Dive | No Effect |  | lacks | one-turn attack; lacks |
| Arm Thrust (Kaizo: HP Fighting) | power 70; PP 15 | 15, 20 | Kaizo-only | Kaizo-only move (HP Fighting); Hidden Power keeps its IV formula (ruling 3) |
| Tail Glow | priority +2 | 0 | lacks | priority lacks |
| Luster Purge | power 100 | 95 | ruling | power ruling: modern 95 |
| Mist Ball | power 100 | 95 | ruling | power ruling: modern 95 |
| FeatherDance | PP 3 | 15 | lacks | PP lacks |
| Teeter Dance | Guaranteed Confusion, Status |  | has | confuses, as Oxide already has |
| Blaze Kick | power 100; accuracy 100; effect chance 20% | 85, 90, 10% | lacks | power lacks; accuracy lacks; effect chance lacks |
| Mud Sport (Kaizo: HP Ground) | power 70; accuracy 100 | 0, never misses | Kaizo-only | Kaizo-only move (HP Ground); Hidden Power keeps its IV formula (ruling 3) |
| Ice Ball | Always hits in Hail; power 120; accuracy 70 | 30, 90 | lacks | flat 120, never misses in hail; lacks (the hail part is moot for the player, who never sets weather); power lacks; accuracy lacks |
| Needle Arm | No Effect; power 80 | 60 | lacks | no flinch; lacks; power lacks |
| Hyper Voice | power 110 | 100 | ruling | power ruling: base ROM 100 |
| Poison Fang | power 90; effect chance 40% | 75, 30% | partly | power ruling: base ROM 75; effect chance lacks |
| Crush Claw | power 120 | 75 | lacks | power lacks |
| Blast Burn | Chance of causing Burn; 1/3 damage dealt recoil; accuracy 95; effect chance 30% | 90, 0% | lacks | 30% burn and 1/3 recoil in place of the recharge turn; lacks; accuracy lacks; effect chance lacks |
| Hydro Cannon | 1/2 damage dealt recoil, fixed AI; accuracy 95 | 90 | lacks | 1/2 recoil in place of the recharge turn; lacks; accuracy lacks |
| Meteor Mash | accuracy 100 | 90 | ruling | accuracy ruling: modern 90 |
| Astonish | power 40 | 30 | lacks | power lacks |
| Aromatherapy | PP 1 | 5 | lacks | PP lacks |
| Fake Tears | Sharply lowers Spd, Status; PP 3 | 20 | lacks | Kaizo's note reads "sharply lowers Spd": a Speed drop would be a change, a Sp. Def drop is what Oxide has; PP lacks |
| Air Cutter | power 60; accuracy 100 | 60, 100 | has | power has (modern); accuracy has |
| Overheat | Chance of causing Burn; 1/3 damage dealt recoil; power 120; accuracy 100; effect chance 10% | 130, 90, 100% | partly | 10% burn and 1/3 recoil in place of the Sp. Atk drop; lacks; power ruling: modern 130; accuracy lacks; effect chance lacks |
| Rock Tomb | power 70; accuracy 100 | 60, 100 | has, by ruling | power ruling: modern 60; accuracy has |
| Silver Wind | power 80; accuracy never misses | 60, 100 | lacks | power lacks; accuracy lacks |
| Metal Sound | Sharply lowers Spd, Status; accuracy 100; PP 3; hits both opponents | 100, 40 | partly | Kaizo's note reads "sharply lowers Spd", as for Fake Tears; accuracy has; PP lacks; lacks (one target) |
| GrassWhistle | accuracy 70 | 55 | lacks | accuracy lacks |
| Tickle | PP 6 | 20 | lacks | PP lacks |
| Cosmic Power | PP 6 | 20 | lacks | PP lacks |
| Signal Beam | power 95 | 75 | lacks | power lacks |
| Shadow Punch | power 95 | 95 | has | power has |
| Extrasensory | power 90 | 80 | lacks | power lacks |
| Sky Uppercut | 2x Damage on Pokemon using Bounce/Fly; power 95; accuracy 100 | 85, 90 | lacks | 2x power on a Pokemon using Fly or Bounce; lacks; power lacks; accuracy lacks |
| Sand Tomb | Whirlpool effect; power 90; accuracy 100 | 35, 100 | has, by ruling | trapping, as Oxide already has; power ruling: modern 35; accuracy has |
| Sheer Cold | Always hits in Hail; power 70; accuracy 50; effect chance 100% | 1, 30, 0% | lacks | rebuilt from a one-hit KO into a 70 power attack with a 100% effect chance, never missing in hail; lacks; power lacks; accuracy lacks; effect chance lacks |
| Muddy Water | accuracy 100 | 100 | has | accuracy has |
| Bullet Seed | power 25 | 25 | has | power has (modern) |
| Icicle Spear | power 25 | 25 | has | power has (modern) |
| Iron Defense | PP 3 | 3 | has | PP has |
| Block | priority +7 | +1 | ruling | priority ruling: base ROM +1 |
| Howl | PP 3 | 3 | has | PP has |
| Dragon Claw | High crit ratio; power 90 | 80 | lacks | high critical ratio; lacks; power lacks |
| Frenzy Plant | Chance of causing Paralysis; 1/3 damage dealt recoil; accuracy 95; effect chance 20% | 90, 0% | lacks | 20% paralysis and 1/3 recoil in place of the recharge turn; lacks; accuracy lacks; effect chance lacks |
| Bulk Up | PP 3; effect chance 1% | 20, 0% | lacks | PP lacks; effect chance lacks |
| Bounce | Chance to Paralyze; accuracy 100 | 100 | has | paralysis chance, as Oxide already has; accuracy has |
| Mud Shot | accuracy 100 | 100 | has | accuracy has |
| Poison Tail | power 120; PP 5 | 50, 25 | lacks | power lacks; PP lacks |
| Covet (Kaizo: HP Grass) | power 70; type Grass; PP 15 | 60, Normal, 25 | Kaizo-only | Kaizo-only move (HP Grass); Hidden Power keeps its IV formula (ruling 3) |
| Volt Tackle | power 150; PP 5; effect chance 30% | 120, 15, 10% | lacks | power lacks; PP lacks; effect chance lacks |
| Magical Leaf | PP 15 | 20 | lacks | PP lacks |
| Water Sport (Kaizo: Scald) | power 80; accuracy 100; effect chance 30% | 0, never misses, 0% | real move | real move: Oxide has Scald (80, 100%, 15 PP, 30% burn), which matches Kaizo |
| Calm Mind | PP 3 | 3 | has | PP has |
| Leaf Blade | power 95 | 90 | lacks | power lacks |
| Dragon Dance | PP 1 | 1 | has | PP has |
| Rock Blast | accuracy 100; PP 8 | 100, 8 | has | accuracy has; PP has |
| Shock Wave | PP 15 | 20 | lacks | PP lacks |
| Water Pulse | accuracy never misses | 100 | lacks | accuracy lacks |
| Doom Desire | power 250; accuracy 100 | 140, 100 | has, by ruling | power ruling: modern 140; accuracy has (modern) |
| Psycho Boost | No Effect; accuracy 100 | 90 | lacks | no Sp. Atk drop; lacks; accuracy lacks |
| Roost | PP 8 | 10 | lacks | PP lacks |
| Gravity | priority +1; permanent | 0 | lacks | priority lacks; lacks (five turns) |
| Wake-Up Slap | effect chance 100% | 0% | lacks | effect chance lacks |
| Hammer Arm | accuracy 100 | 100 | has | accuracy has |
| Gyro Ball | PP 8 | 5 | lacks | PP lacks |
| Healing Wish (Kaizo: HP Electric) | power 70; type Electric; accuracy 100; PP 15 | 0, Psychic, never misses, 10 | Kaizo-only | Kaizo-only move (HP Electric); Hidden Power keeps its IV formula (ruling 3) |
| Natural Gift | PP 1 | 15 | lacks | PP lacks |
| Feint | power 80 | 30 | ruling | power ruling: modern 30 |
| Pluck | power 50; PP 5 | 60, 20 | lacks | power lacks; PP lacks |
| Tailwind | priority +5 | 0 | lacks | priority lacks |
| Metal Burst | priority -2 | -5 | ruling | priority ruling: base ROM -5 |
| U-turn | power 80 | 70 | lacks | power lacks |
| Close Combat | 1/4 damage dealt recoil |  | lacks | 1/4 recoil in place of the defence drops; lacks |
| Payback | power 60 | 60 | has | power has |
| Assurance | power 70 | 70 | has | power has |
| Psycho Shift | accuracy 100 | 100 | has | accuracy has (modern) |
| Trump Card | PP 1 | 5 | lacks | PP lacks |
| Heal Block (Kaizo: Aqua Cutter) | power 70; type Water | 0, Psychic | real move | real move: Oxide has Aqua Cutter (70, 100%, 20 PP, high critical ratio), which matches Kaizo |
| Wring Out | 2x power if target is at or below 1/2 HP; power 75 | 1 | lacks | flat 75, doubled at half HP or less, in place of HP-based power; lacks; power lacks |
| Lucky Chant | priority +2 | 0 | lacks | priority lacks |
| Me First | priority +1 | +1 | has | priority has |
| Copycat | priority +1 | +1 | has | priority has |
| Power Swap | PP 3 | 10 | lacks | PP lacks |
| Guard Swap | PP 3 | 10 | lacks | PP lacks |
| Sucker Punch | No Effect; priority +2 | +1 | lacks | a plain +2 priority hit that works whatever the target does; lacks; priority lacks |
| Toxic Spikes | priority +1 | 0 | lacks | priority lacks |
| Heart Swap | Damages target; heals user up to 50% of damage dealt, Special; power 95; type Water | 0, Psychic | lacks | rebuilt as a special Water 95 draining attack; lacks; power lacks; type lacks |
| Magnet Rise | hits user's side of field; priority +1 | 0 | lacks | lacks (the user only); priority lacks |
| Flare Blitz | PP 8 | 15 | lacks | PP lacks |
| Force Palm | power 85 | 60 | lacks | power lacks |
| Aura Sphere | PP 10 | 20 | lacks | PP lacks |
| Rock Polish | PP 1 | 1 | has | PP has |
| Aqua Tail | power 120; accuracy 85 | 90, 100 | partly | power lacks; accuracy ruling: base ROM 100 |
| Seed Bomb | effect chance 100% | 0% | lacks | effect chance lacks |
| Air Slash | accuracy 100 | 95 | lacks | accuracy lacks |
| X-Scissor | High crit ratio |  | lacks | high critical ratio; lacks |
| Dragon Pulse | Always hits; accuracy never misses | 100 | lacks | never misses; lacks; accuracy lacks |
| Dragon Rush | accuracy 100; effect chance 30% | 75, 20% | lacks | accuracy lacks; effect chance lacks |
| Power Gem | power 90 | 80 | ruling | power ruling: modern 80 |
| Drain Punch | power 75 | 75 | has | power has (modern) |
| Focus Blast | accuracy 85 | 70 | lacks | accuracy lacks |
| Brave Bird | 1/4 damage dealt recoil |  | lacks | 1/4 recoil; Oxide has 1/3: lacks |
| Switcheroo (Kaizo: HP Flying) | power 70; type Flying; PP 15 | 0, Dark, 10 | Kaizo-only | Kaizo-only move (HP Flying); Hidden Power keeps its IV formula (ruling 3) |
| Giga Impact | 1/2 damage dealt recoil, fixed AI; power 180; accuracy 100 | 150, 90 | lacks | 1/2 recoil in place of the recharge turn; lacks; power lacks; accuracy lacks |
| Nasty Plot | type ???; PP 1 | Dark, 1 | partly | type lacks; PP has |
| Bullet Punch | PP 10 | 30 | lacks | PP lacks |
| Avalanche | Chance of causing Freeze; chance of causing Flinch; power 100; effect chance 20%; hits both opponents; priority 0 | 60, 0%, -4 | lacks | flat 100, 20% freeze or flinch, both foes, normal priority; lacks; power lacks; effect chance lacks; lacks (one target); priority lacks |
| Ice Shard | PP 10 | 30 | lacks | PP lacks |
| Shadow Claw | Hits target 2-5 times; power 25 | 70 | lacks | hits 2 to 5 times at 25; lacks; power lacks |
| Thunder Fang | power 90; accuracy 100 | 90, 100 | has | power has; accuracy has |
| Ice Fang | power 90; accuracy 100 | 90, 100 | has | power has; accuracy has |
| Fire Fang | power 90; accuracy 100 | 90, 100 | has | power has; accuracy has |
| Shadow Sneak | PP 10 | 30 | lacks | PP lacks |
| Mud Bomb | accuracy 100 | 100 | has | accuracy has |
| Psycho Cut | power 90 | 70 | lacks | power lacks |
| Zen Headbutt | accuracy 100 | 100 | has | accuracy has |
| Mirror Shot | power 120; accuracy 100 | 65, 100 | partly | power lacks; accuracy has |
| Rock Climb | type Rock; accuracy 100; effect chance 30% | Normal, 85, 20% | lacks | type lacks; accuracy lacks; effect chance lacks |
| Defog | PP 1 | 15 | lacks | PP lacks |
| Trick Room | PP 1; priority +7; permanent | 5, -7 | lacks | PP lacks; priority lacks; lacks for the player; Oxide has a permanent room only for Saturn 2 |
| Draco Meteor | 1/2 damage dealt recoil, fixed AI; accuracy 100; effect chance 0% | 90, 100% | lacks | 1/2 recoil in place of the Sp. Atk drop; lacks; accuracy lacks; effect chance lacks |
| Leaf Storm | No Effect; power 120; accuracy 85 | 130, 90 | partly | no Sp. Atk drop; lacks; power ruling: modern 130; accuracy lacks |
| Power Whip | High crit ratio |  | lacks | high critical ratio; lacks |
| Rock Wrecker | Hits the target up to 3 times; increases power by 10 with each hit; power 40; accuracy 100; PP 8 | 150, 90, 5 | lacks | three hits rising by 10 in place of the recharge turn; lacks; power lacks; accuracy lacks; PP lacks |
| Cross Poison | power 95; effect chance 20% | 70, 10% | lacks | power lacks; effect chance lacks |
| Gunk Shot | accuracy 100; PP 8 | 80, 5 | partly | accuracy ruling: modern 80; PP lacks |
| Magnet Bomb | power 100 | 60 | lacks | power lacks |
| Stone Edge | power 120 | 100 | lacks | power lacks |
| Captivate | Sharply lowers SpAtk, Status; PP 3 | 20 | lacks | no gender condition; lacks; PP lacks |
| Stealth Rock | priority +1 | 0 | lacks | priority lacks |
| Chatter | power 120; effect chance 50%; hits both opponents and ally | 65, 0% | partly | power ruling: modern 65; effect chance lacks; lacks (one target) |
| Judgment | power 120 | 100 | lacks | power lacks |
| Charge Beam | accuracy 100; effect chance 100% | 100, 70% | partly | accuracy has; effect chance lacks |
| Aqua Jet | PP 5 | 20 | lacks | PP lacks |
| Attack Order | Chance to Poison; power 120; effect chance 30%; hits both opponents | 120, 30% | partly | 30% poison, as Oxide already has; power has; effect chance has; lacks (one target) |
| Defend Order | priority +1 | +1 | has | priority has |
| Head Smash | accuracy 100; 1/2 recoil | 80 | partly | accuracy lacks; 1/2 recoil, as Oxide already has |
| Double Hit | power 60; accuracy 100 | 35, 90 | lacks | power lacks; accuracy lacks |
| Roar of Time | accuracy 100; hits both opponents | 90 | lacks | accuracy lacks; lacks (one target) |
| Spacial Rend | power 120; accuracy 100 | 100, 95 | lacks | power lacks; accuracy lacks |
| Lunar Dance | Restores up to 50% max HP; priority +1 | 0 | lacks | restores half of the user's HP in place of fainting; lacks; priority lacks |
| Crush Grip | Whirlpool effect; power 150 | 1 | lacks | flat 150 with trapping in place of HP-based power; lacks; power lacks |
| Magma Storm | Whirlpool effect; accuracy 100 | 75 | has, by ruling | trapping, as Oxide already has; accuracy ruling: modern 75 |
| Dark Void | accuracy 90; PP 5 | 80, 10 | partly | accuracy ruling: Gen 4 accuracy kept (answer 2); PP lacks |
| Seed Flare | accuracy 100; effect chance 50% | 85, 40% | lacks | accuracy lacks; effect chance lacks |
| Ominous Wind | power 80; accuracy never misses | 60, 100 | lacks | power lacks; accuracy lacks |
| Magic Coat | Bounces Stealth Rock in singles |  | not traced | not traced in Oxide's engine |

## Appendix B: learnset findings by line

One row per evolution line with at least one finding, in national dex order of its first member. "Obtained" is the first split in which the player can own any member. Each entry names the species, the move and Kaizo's level; "Given earlier" adds Oxide's level, and "Kaizo-only moves" gives what the Kaizo move is. Relearner moves are left out here for length; the rule that finds them is in the learnsets section.

| Line | Obtained | Early coverage | Given earlier | Strong STAB Oxide lacks | Kaizo-only moves |
|---|---|---|---|---|---|
| Charmander / Charmeleon / Charizard | Roark | Charmander: Bite 10 |  |  |  |
| Squirtle / Wartortle / Blastoise | Roark | Squirtle: Ice Punch 22 |  |  |  |
| Pikachu / Raichu / Pichu | Roark | Pikachu: Iron Tail 21 |  | Pichu: Volt Tackle 65 |  |
| Nidoran F / Nidorina / Nidoqueen | Roark | Nidoran F: Dig 19; Nidoran F: Drill Run 25; Nidorina: Dig 20; Nidoqueen: Crunch 23 |  |  |  |
| Nidoran M / Nidorino / Nidoking | Roark | Nidoran M: Earth Power 21; Nidoran M: Drill Peck 25; Nidorino: Earth Power 23 | Nidoking: Megahorn 43 (Oxide 58) |  |  |
| Vulpix / Ninetales | Roark | Vulpix: Aurora Beam 19 | Vulpix: Fire Blast 34 (Oxide 47) |  |  |
| Zubat / Golbat / Crobat | Roark | Zubat: Steel Wing 17; Crobat: Steel Wing 21 |  | Zubat: Brave Bird 41; Golbat: Brave Bird 65 |  |
| Psyduck / Golduck | Roark |  | Psyduck: Zen Headbutt 22 (Oxide 40) |  |  |
| Primeape | Byron |  |  |  | Primeape: Rage 28 (Fighting 70); Primeape: Rage 47 (Fighting 70) |
| Poliwag / Poliwhirl / Poliwrath / Politoed | Roark | Poliwhirl: Brick Break 25 |  | Politoed: Hydro Pump 65 |  |
| Abra / Kadabra / Alakazam | Roark |  | Kadabra: Psycho Cut 18 (Oxide 34); Kadabra: Future Sight 30 (Oxide 42) |  |  |
| Machop / Machoke / Machamp | Roark | Machop: Fire Punch 22 | Machop: Wake-Up Slap 13 (Oxide 34) |  |  |
| Tentacool / Tentacruel | Roark | Tentacool: Psybeam 8; Tentacool: Signal Beam 15 | Tentacool: Poison Jab 19 (Oxide 33) |  | Tentacruel: Absorb 12 (Dark 60) |
| Geodude / Graveler / Golem | Roark | Geodude: Fire Punch 25 |  |  |  |
| Ponyta / Rapidash | Roark | Ponyta: Bounce 24 | Ponyta: Bounce 24 (Oxide 42) |  | Ponyta: Stomp 6 (Ground 90); Rapidash: Stomp 6 (Ground 90) |
| Slowpoke / Slowbro | Wake |  |  |  | Slowpoke: Swallow 60 (Poison 90) |
| Magnemite / Magneton / Magnezone | Byron | Magnezone: Signal Beam 17 |  |  |  |
| Seel / Dewgong | Fantina | Seel: Bite 13 | Seel: Take Down 17 (Oxide 37) |  |  |
| Shellder / Cloyster | Byron |  |  | Shellder: Hydro Pump 40 | Shellder: Vise Grip 28 (Water 90); Cloyster: Vise Grip 28 (Water 90) |
| Gastly / Haunter / Gengar | Fantina |  | Gastly: Dark Pulse 19 (Oxide 36) | Gastly: Sludge Bomb 56 | Gastly: Lick 5 (Ghost 80); Haunter: Lick 1 (Ghost 80); Gengar: Lick 1 (Ghost 80) |
| Onix / Steelix | Roark | Onix: Bite 17; Steelix: Aqua Tail 14; Steelix: Crunch 25 | Onix: Double-Edge 38 (Oxide 49); Steelix: Slam 6 (Oxide 25); Steelix: Iron Tail 17 (Oxide 41); Steelix: Crunch 25 (Oxide 46) |  | Steelix: Swallow 1 (Poison 90) |
| Krabby / Kingler | Roark | Krabby: Ice Punch 19; Krabby: Rock Slide 25 | Kingler: Slam 32 (Oxide 44) |  | Krabby: Vise Grip 31 (Water 90); Kingler: Vise Grip 37 (Water 90) |
| Lickitung / Lickilicky | Maylene | Lickitung: Water Pulse 21 |  |  | Lickitung: Lick 1 (Ghost 80); Lickitung: Stomp 9 (Ground 90); Lickilicky: Lick 1 (Ghost 80); Lickilicky: Swallow 5 (Poison 90); Lickilicky: Stomp 9 (Ground 90); Lickilicky: Lick 29 (Ghost 80); Lickilicky: Lick 63 (Ghost 80) |
| Koffing / Weezing | Maylene | Koffing: Psybeam 6 | Koffing: Sludge Bomb 28 (Oxide 42) |  |  |
| Rhyhorn / Rhydon / Rhyperior | Roark | Rhyhorn: Bite 13; Rhyperior: Aqua Tail 9; Rhyperior: Submission 13 |  |  | Rhyhorn: Stomp 25 (Ground 90); Rhydon: Stomp 21 (Ground 90) |
| Chansey / Blissey / Happiny | Fantina |  | Chansey: Double-Edge 9 (Oxide 46); Chansey: Double-Edge 34 (Oxide 46); Blissey: Double-Edge 12 (Oxide 46); Blissey: Double-Edge 34 (Oxide 46) |  | Chansey: Egg Bomb 46 (Grass 100); Blissey: Egg Bomb 46 (Grass 100) |
| Tangela / Tangrowth | Wake | Tangela: Sludge Bomb 26 | Tangela: Slam 15 (Oxide 43); Tangela: Power Whip 33 (Oxide 54) |  | Tangela: Swallow 1 (Poison 90); Tangela: Absorb 8 (Dark 60); Tangrowth: Swallow 29 (Poison 90) |
| Horsea / Seadra / Kingdra | Wake | Horsea: Aurora Beam 18; Horsea: Dragon Breath 26; Kingdra: Aurora Beam 14 | Kingdra: Hydro Pump 23 (Oxide 40) |  |  |
| Goldeen / Seaking | Roark | Goldeen: Psybeam 11 |  |  |  |
| Staryu / Starmie | Maylene |  | Staryu: Power Gem 33 (Oxide 46) | Starmie: Hydro Pump 55 |  |
| Mr. Mime / Mime Jr. | Wake | Mime Jr.: Magical Leaf 11 |  |  |  |
| Scyther / Scizor | Maylene | Scyther: Brick Break 21; Scizor: Wing Attack 9; Scizor: Brick Break 25 |  | Scyther: Bug Buzz 17; Scizor: Bug Buzz 13 | Scizor: Vise Grip 5 (Water 90) |
| Jynx / Smoochum | Wake |  |  |  | Jynx: Lick 8 (Ghost 80); Smoochum: Lick 5 (Ghost 80) |
| Electabuzz / Elekid / Electivire | Maylene |  | Electivire: Thunderbolt 7 (Oxide 43) |  |  |
| Magmar / Magby / Magmortar | Roark | Magby: Thunder Punch 25; Magmortar: Cross Chop 19 | Magby: Fire Punch 16 (Oxide 28); Magmortar: Lava Plume 16 (Oxide 37) |  |  |
| Magikarp / Gyarados | Galactic |  |  |  | Gyarados: Vise Grip 52 (Water 90) |
| Eevee / Vaporeon / Jolteon / Flareon / Espeon / Umbreon / Leafeon / Glaceon | Fantina | Jolteon: Bite 22; Espeon: Bite 8; Leafeon: Aerial Ace 8 | Eevee: Take Down 15 (Oxide 43); Leafeon: Leaf Blade 21 (Oxide 71) |  |  |
| Snorlax / Munchlax | Gardenia | Snorlax: Submission 17; Munchlax: Submission 20 | Snorlax: Body Slam 4 (Oxide 33) |  | Snorlax: Lick 12 (Ghost 80); Munchlax: Lick 1 (Ghost 80); Munchlax: Swallow 100 (Poison 90) |
| Totodile / Croconaw / Feraligatr | Wake |  |  |  | Croconaw: Vise Grip 42 (Water 90); Feraligatr: Vise Grip 47 (Water 90) |
| Sentret / Furret | Roark |  | Sentret: Hyper Voice 36 (Oxide 47); Furret: Hyper Voice 36 (Oxide 56) |  |  |
| Hoothoot / Noctowl | Gardenia | Hoothoot: Steel Wing 9 | Hoothoot: Zen Headbutt 13 (Oxide 33); Hoothoot: Extrasensory 25 (Oxide 37); Noctowl: Extrasensory 22 (Oxide 42) |  |  |
| Chinchou / Lanturn | Roark | Chinchou: Aurora Beam 23 |  |  |  |
| Togepi / Togetic / Togekiss | Gardenia | Togetic: Shadow Ball 19 | Togepi: Double-Edge 24 (Oxide 46); Togetic: Double-Edge 10 (Oxide 46) |  |  |
| Mareep / Flaaffy / Ampharos | Gardenia | Flaaffy: Iron Tail 25 | Ampharos: Power Gem 30 (Oxide 59) |  |  |
| Marill / Azumarill / Azurill | Fantina | Marill: Brick Break 25; Azumarill: Iron Tail 25; Azurill: Bubble Beam 10 | Azumarill: Hydro Pump 37 (Oxide 54) |  |  |
| Sudowoodo / Bonsly | Fantina |  | Sudowoodo: Rock Slide 17 (Oxide 33) |  |  |
| Hoppip / Skiploom / Jumpluff | Gardenia |  |  |  | Hoppip: Absorb 1 (Dark 60); Hoppip: Memento 34 (Dark 255); Skiploom: Absorb 1 (Dark 60); Skiploom: Memento 7 (Dark 255); Skiploom: Memento 40 (Dark 255); Jumpluff: Memento 12 (Dark 255); Jumpluff: Memento 48 (Dark 255) |
| Aipom / Ambipom | Gardenia | Ambipom: Water Pulse 22 |  |  |  |
| Yanma / Yanmega | Maylene |  | Yanma: Uproar 17 (Oxide 27) |  |  |
| Wooper / Quagsire | Roark |  | Wooper: Muddy Water 29 (Oxide 47); Quagsire: Muddy Water 31 (Oxide 53) |  |  |
| Murkrow / Honchkrow | Gardenia |  |  | Murkrow: Brave Bird 55; Honchkrow: Brave Bird 35 |  |
| Misdreavus / Mismagius | Fantina |  | Misdreavus: Power Gem 28 (Oxide 50) |  |  |
| Girafarig | Wake |  | Girafarig: Crunch 28 (Oxide 46) |  | Girafarig: Stomp 1 (Ground 90) |
| Gligar / Gliscor | Roark | Gligar: Brick Break 9; Gligar: X-Scissor 12; Gligar: Rock Slide 23 | Gligar: X-Scissor 12 (Oxide 42) | Gliscor: Earthquake 55 | Gligar: Vise Grip 5 (Water 90) |
| Snubbull / Granbull | Gardenia |  | Snubbull: Crunch 37 (Oxide 49); Granbull: Crunch 43 (Oxide 59) |  | Snubbull: Lick 1 (Ghost 80); Granbull: Lick 1 (Ghost 80) |
| Qwilfish | Maylene | Qwilfish: Shadow Ball 13; Qwilfish: Payback 25 | Qwilfish: Hydro Pump 33 (Oxide 57); Qwilfish: Poison Jab 37 (Oxide 49) |  |  |
| Heracross | Gardenia | Heracross: Rock Slide 13 |  |  |  |
| Sneasel / Weavile | Maylene |  | Sneasel: Slash 21 (Oxide 35) | Sneasel: Ice Fang 10; Sneasel: Ice Punch 28; Weavile: Ice Punch 42 |  |
| Slugma / Magcargo | Gardenia |  | Slugma: Rock Slide 21 (Oxide 41); Slugma: Body Slam 25 (Oxide 46); Slugma: Lava Plume 25 (Oxide 38); Slugma: Earth Power 46 (Oxide 56); Magcargo: Earth Power 52 (Oxide 66) |  |  |
| Swinub / Piloswine / Mamoswine | Gardenia | Swinub: Rock Slide 25 |  |  |  |
| Corsola | Roark |  | Corsola: Power Gem 20 (Oxide 44) | Corsola: Muddy Water 28; Corsola: Head Smash 53; Corsola: Muddy Water 55 |  |
| Remoraid / Octillery | Roark |  | Remoraid: Signal Beam 19 (Oxide 36) | Remoraid: Hydro Pump 50; Octillery: Hydro Pump 57 |  |
| Delibird | Candice | Delibird: Drill Run 25 |  | Delibird: Ice Beam 29; Delibird: Blizzard 34 |  |
| Mantine / Mantyke | Wake | Mantyke: Aurora Beam 13 |  |  |  |
| Skarmory | Byron |  |  | Skarmory: Brave Bird 45 |  |
| Houndour / Houndoom | Roark |  | Houndoom: Crunch 32 (Oxide 54) |  |  |
| Phanpy / Donphan | Roark | Phanpy: Rock Slide 19 |  | Phanpy: Earthquake 42 |  |
| Suicune | Candice |  | Suicune: Extrasensory 36 (Oxide 64) |  |  |
| Larvitar / Pupitar / Tyranitar | Fantina |  | Larvitar: Dark Pulse 5 (Oxide 28); Larvitar: Hyper Beam 32 (Oxide 50) |  |  |
| Treecko / Grovyle / Sceptile | Gardenia | Treecko: Bite 11; Treecko: Crunch 26; Grovyle: Dig 23 |  |  |  |
| Torchic / Combusken / Blaziken | Gardenia | Torchic: Aerial Ace 17; Combusken: Aerial Ace 19 |  |  |  |
| Mudkip / Marshtomp / Swampert | Roark | Mudkip: Mud Bomb 24 | Marshtomp: Take Down 16 (Oxide 31); Marshtomp: Muddy Water 25 (Oxide 37) |  |  |
| Poochyena / Mightyena | Roark |  | Mightyena: Assurance 22 (Oxide 32) |  |  |
| Wurmple / Silcoon / Beautifly / Cascoon / Dustox | Roark | Beautifly: Giga Drain 24 | Beautifly: Giga Drain 24 (Oxide 38); Beautifly: Bug Buzz 28 (Oxide 41); Dustox: Bug Buzz 27 (Oxide 41) |  |  |
| Lotad / Lombre / Ludicolo | Roark |  |  |  | Lotad: Absorb 13 (Dark 60); Lombre: Absorb 15 (Dark 60) |
| Seedot / Nuzleaf / Shiftry | Roark | Seedot: Leech Life 3; Nuzleaf: Extrasensory 25 | Nuzleaf: Extrasensory 25 (Oxide 49) | Nuzleaf: Leaf Blade 43 | Seedot: Absorb 7 (Dark 60) |
| Wingull / Pelipper | Roark | Wingull: Bite 11 |  | Wingull: Hydro Pump 47 | Pelipper: Swallow 53 (Poison 90) |
| Ralts / Kirlia / Gardevoir | Fantina |  | Ralts: Future Sight 21 (Oxide 34) |  | Ralts: Heart Swap 45 (Water 95); Kirlia: Heart Swap 53 (Water 95); Gardevoir: Heart Swap 63 (Water 95) |
| Surskit / Masquerain | Roark | Masquerain: Giga Drain 26 | Masquerain: Bug Buzz 40 (Oxide 61) | Surskit: Bug Buzz 31; Surskit: Hydro Pump 43 |  |
| Nosepass / Probopass | Roark | Nosepass: Iron Head 19; Probopass: Earth Power 7 | Nosepass: Rock Slide 7 (Oxide 31); Nosepass: Power Gem 25 (Oxide 49); Nosepass: Discharge 31 (Oxide 55); Nosepass: Earth Power 43 (Oxide 79); Probopass: Earth Power 7 (Oxide 79); Probopass: Rock Slide 19 (Oxide 31); Probopass: Discharge 31 (Oxide 55) |  |  |
| Mawile | Byron | Mawile: Fire Fang 21; Mawile: Poison Fang 26 | Mawile: Iron Head 31 (Oxide 56) | Mawile: Meteor Mash 51 | Mawile: Swallow 51 (Poison 90); Mawile: Vise Grip 56 (Water 90) |
| Plusle | Gardenia | Plusle: Fire Punch 17 |  |  |  |
| Minun | Gardenia | Minun: Fire Punch 17 |  |  |  |
| Carvanha / Sharpedo | Gardenia | Carvanha: Bug Bite 8 |  |  | Carvanha: Rage 6 (Fighting 70); Carvanha: Vise Grip 66 (Water 90); Sharpedo: Rage 1 (Fighting 70) |
| Wailmer / Wailord | Fantina |  | Wailmer: Dive 31 (Oxide 41); Wailmer: Bounce 34 (Oxide 44) |  | Wailmer: Swallow 27 (Poison 90); Wailord: Swallow 31 (Poison 90) |
| Trapinch / Vibrava / Flygon | Maylene | Trapinch: Bug Bite 17 |  | Vibrava: Earthquake 57; Flygon: Earth Power 49; Flygon: Dragon Pulse 57 |  |
| Swablu / Altaria | Gardenia | Swablu: Steel Wing 23 |  |  |  |
| Lunatone | Maylene | Lunatone: Signal Beam 9 |  |  |  |
| Solrock | Maylene | Solrock: Flare Blitz 9 | Solrock: Rock Slide 31 (Oxide 45) | Solrock: Stone Edge 53 |  |
| Barboach / Whiscash | Roark | Barboach: Bounce 22; Barboach: Future Sight 26 | Barboach: Future Sight 26 (Oxide 43); Whiscash: Future Sight 33 (Oxide 51) |  | Whiscash: Swallow 18 (Poison 90) |
| Corphish / Crawdaunt | Roark | Corphish: Aerial Ace 20 |  |  | Corphish: Vise Grip 38 (Water 90); Crawdaunt: Vise Grip 26 (Water 90); Crawdaunt: Vise Grip 44 (Water 90) |
| Castform | Maylene | Castform: Hydro Pump 20; Castform: Flamethrower 20; Castform: Ice Beam 20 |  |  | Castform: Water Ball 30 (Water 100) |
| Duskull / Dusclops / Dusknoir | Fantina | Duskull: Payback 9; Duskull: Future Sight 25; Dusknoir: Aura Sphere 9; Dusknoir: Payback 25 | Duskull: Future Sight 25 (Oxide 46) |  | Duskull: Memento 30 (Dark 255); Dusclops: Memento 51 (Dark 255); Dusknoir: Swallow 1 (Poison 90) |
| Tropius | Wake |  | Tropius: Body Slam 7 (Oxide 37) |  |  |
| Chimecho / Chingling | Gardenia |  |  | Chimecho: Psychic 30 |  |
| Absol | Wake | Absol: Aerial Ace 12; Absol: Rock Slide 20; Absol: Shadow Ball 22 | Absol: Slash 17 (Oxide 36); Absol: Future Sight 28 (Oxide 41) |  |  |
| Spheal / Sealeo / Walrein | Candice | Spheal: Bounce 19 | Spheal: Body Slam 7 (Oxide 19) |  |  |
| Clamperl / Huntail / Gorebyss | Gardenia | Gorebyss: Leech Life 10; Gorebyss: Aurora Beam 19 | Huntail: Hydro Pump 10 (Oxide 51); Gorebyss: Psychic 24 (Oxide 42) |  | Huntail: Vise Grip 1 (Water 90); Huntail: Vise Grip 28 (Water 90); Huntail: Swallow 51 (Poison 90); Gorebyss: Vise Grip 1 (Water 90) |
| Relicanth | Byron |  | Relicanth: Take Down 8 (Oxide 29); Relicanth: Hydro Pump 15 (Oxide 71); Relicanth: Double-Edge 29 (Oxide 50); Relicanth: Dive 43 (Oxide 57) |  |  |
| Luvdisc | Wake |  |  | Luvdisc: Muddy Water 46 | Luvdisc: Heart Swap 51 (Water 95) |
| Metang / Metagross | Byron |  | Metang: Zen Headbutt 36 (Oxide 52) |  |  |
| Turtwig / Grotle / Torterra | Roark | Turtwig: Dig 25 |  |  | Grotle: Stomp 16 (Ground 90) |
| Piplup / Prinplup / Empoleon | Roark | Piplup: Aurora Beam 16; Prinplup: Aerial Ace 21 | Prinplup: Drill Peck 28 (Oxide 46) |  |  |
| Bidoof / Bibarel | Roark | Bidoof: Bite 5; Bidoof: Bubble Beam 17; Bidoof: Dive 25 |  |  |  |
| Kricketot / Kricketune | Roark |  | Kricketune: Slash 14 (Oxide 26); Kricketune: Bug Buzz 30 (Oxide 46) |  |  |
| Shinx / Luxio / Luxray | Roark |  | Shinx: Discharge 17 (Oxide 41) |  |  |
| Combee / Vespiquen | Gardenia | Vespiquen: Poison Jab 25 |  |  | Vespiquen: Rage 7 (Fighting 70) |
| Pachirisu | Roark | Pachirisu: Bite 5; Pachirisu: Fire Fang 17; Pachirisu: Crunch 21; Pachirisu: Ice Fang 25 |  | Pachirisu: Thunder Fang 35; Pachirisu: Thunder 55 |  |
| Buizel / Floatzel | Roark | Buizel: Bite 23 |  | Buizel: Aqua Tail 75 |  |
| Drifloon / Drifblim | Maylene |  | Drifloon: Shadow Ball 27 (Oxide 38); Drifloon: Explosion 30 (Oxide 43); Drifblim: Explosion 32 (Oxide 51) |  | Drifblim: Water Ball 1 (Water 100) |
| Buneary / Lopunny | Roark | Buneary: Bite 6; Lopunny: Dig 16 |  | Buneary: Mega Kick 65; Lopunny: Mega Kick 73 |  |
| Glameow / Purugly | Roark | Glameow: Aerial Ace 13 | Glameow: Slash 20 (Oxide 37) |  |  |
| Stunky / Skuntank | Gardenia |  | Stunky: Explosion 27 (Oxide 44) | Stunky: Sludge Bomb 38; Stunky: Gunk Shot 44; Skuntank: Gunk Shot 62 |  |
| Spiritomb | Maylene | Spiritomb: Silver Wind 19 | Spiritomb: Dark Pulse 37 (Oxide 49) |  |  |
| Gible / Gabite / Garchomp | Fantina | Gible: Bite 3; Gible: Crunch 13 |  |  |  |
| Riolu / Lucario | Byron | Riolu: Thunder Punch 6; Riolu: Iron Head 11; Riolu: Extrasensory 24 |  |  | Lucario: Bonemerang 37 (Rock 60) |
| Hippopotas / Hippowdon | Wake | Hippopotas: Ice Fang 19 |  |  |  |
| Skorupi / Drapion | Wake |  | Skorupi: Cross Poison 28 (Oxide 50) |  | Drapion: Vise Grip 49 (Water 90) |
| Croagunk / Toxicroak | Maylene |  | Croagunk: Sludge Bomb 17 (Oxide 43) |  |  |
| Carnivine | Fantina |  |  |  | Carnivine: Swallow 31 (Poison 90) |
| Finneon / Lumineon | Roark | Finneon: Signal Beam 26 | Finneon: U-turn 28 (Oxide 42); Finneon: Bounce 33 (Oxide 45); Lumineon: U-turn 34 (Oxide 48); Lumineon: Bounce 42 (Oxide 53) | Lumineon: Aqua Tail 53 |  |
| Snover / Abomasnow | Gardenia | Snover: Focus Blast 21 | Snover: Blizzard 26 (Oxide 41) |  |  |
| Uxie | Candice | Uxie: Signal Beam 6 | Uxie: Extrasensory 16 (Oxide 51) |  | Uxie: Memento 76 (Dark 255) |
| Mesprit | Candice | Mesprit: Signal Beam 6 | Mesprit: Extrasensory 16 (Oxide 51) |  |  |
| Azelf | Candice | Azelf: Signal Beam 6 | Azelf: Extrasensory 16 (Oxide 51); Azelf: Last Resort 46 (Oxide 61) |  |  |
| Heatran | Galactic |  | Heatran: Magma Storm 9 (Oxide 96); Heatran: Earth Power 41 (Oxide 73) |  | Heatran: Swallow 5 (Poison 90) |
| Manaphy | Wake | Manaphy: Signal Beam 9 |  | Manaphy: Hydro Pump 54 | Manaphy: Heart Swap 76 (Water 95) |
