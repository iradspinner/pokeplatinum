# The Galactic drafts, rechecked

The drafts of Mars 1, Moira 1, Jupiter 1, Argo 1 and Cyrus 1 (branch `overseer-galactic-teams`, written on 2026-10-13) were checked on 2026-10-21 against today's simulator, move data and learnsets. Nothing failed. Every simulator gap the drafts met or were bent around is fixed, none of their 75 moves changed in power, accuracy, PP, effect or flags, no species on them changed its abilities, and today's scorer builds all five fights with every species, ability, item and move resolved. Three choices on the drafts were made only because the simulator did not run something, and all three can go back to the designer's first choice. No team was changed; the questions below are Ian's.

## Questions for Ian, in play order

Mars 1 (Valley Windworks, with your three dials):

1. Should Torracat take Parting Shot back in place of U-turn? It had U-turn only because the simulator did not run Parting Shot, which it does since 6f15a0854 (2026-10-15); Litten learns it at 9, so it is legal, and it lowers the target's Attack and Sp. Atk instead of hitting for 70, which leans the way your dials do.
2. Should the second reading go ahead with your three dials as they are, and nothing else? The first reading they answered was bent three ways the simulator no longer is (Protean did nothing, Intimidate counted twice, and it lowered an Inner Focus Zubat), and the trainer AI now rates Double Kick and Dual Wingbeat on both hits, so the net direction is for the reading to show.

Moira 1 (the Eterna building's 3F):

3. Should Moira 1 be read as drafted? Everything her page said she waited on (Future Sight's delay, Ice Body, Encore, Magic Guard against hazards and Leech Seed) runs since 2026-10-14, none of her moves changed, and no new move reaches her members at their levels.

Jupiter 1 (the Eterna building):

4. Should Galarian Weezing take Clear Smog back in place of Strange Steam? Clear Smog left your chat team only because the simulator did not reset stat stages, which it does since e930b3ef2 (2026-10-15), and Weezing learns Clear Smog at 19 but Strange Steam only at 48. If your chat set's other move was not Toxic Spikes, name it and it goes back too.
5. Should Lanturn take Parabolic Charge in place of Discharge? Chinchou learns it at 25 since 2026-10-14 (f5672c246), so a level 26 Lanturn may know it; it hits for 65 and heals half the damage, which suits a Leftovers tank, and it drops a paralysis chance that Thunder Wave already covers. It changes no Speed.
6. Should Jupiter 1 be read against your target of 94 percent won (2026-10-14) as it stands, and softened only if it reads below that? The draft aimed at 75 to 85 before you set the target, and its speed is high: with Unburden now counted once, a Pelipper that has eaten its Sitrus reaches 92 Speed, over every Pokemon in the box (the fastest is 71), and Tailwind lifts all six over the box for three turns.

Argo 1 (Celestic Town):

7. Is the Argo 1 draft below the team to read? It was drafted on 2026-10-13 and never put to you. Mummy, Cursed Body and Unnerve, which it carries, ran nowhere then and all run now, so this reading is the first to show them.

Cyrus 1 (Celestic ruins):

8. Is the Cyrus 1 draft below the team to read? It too was drafted on 2026-10-13 and never put to you.
9. Should Honchkrow take Moxie, its own hidden ability, in place of Super Luck? The draft avoided Moxie only because the simulator did not run it, which it does since 141845f89 (2026-10-14), and with Crunch in place of Night Slash, Super Luck gives Honchkrow only a 1 in 8 critical hit. Salamence keeps Intimidate, since Moxie on a Dragon Dance user would snowball.

What happens next: the Overseer applies the answers on `overseer-galactic-teams` and carries each fight onto today's `oxide`, as Somnu 1 was, before its reading (about 70 minutes each, after Somnu 1's). None of these changes moves a fight's speed tiers but Clear Smog's reset of a player's Speed boost.

## The detail

### How it was checked

The five draft files were checked out over a throwaway copy of `origin/oxide` (60c596fbd), so today's scorer read them as it will at their readings. Three checks ran there, none of them a battle.

| Check | What it read | Result |
|---|---|---|
| Data since 2026-10-13 | every draft move's and species' record at 93ad73726 (the drafts' base) against `origin/oxide` | no move changed; no ability slot changed; learnsets changed on Bronzong, Emolga, Honchkrow, Liepard, Pelipper and Xatu (one move each, past the members' levels but Honchkrow's) and on Chinchou and Mime Jr. |
| Each set resolves | `data.oxide_trainers()`, the calculator's species and abilities, `fightsim.move` (which falls back silently to an empty record for an unknown name) | all 27 species known, all 27 abilities and items named as the simulator reads them (the type boosters through its booster table), all 75 moves resolved to their records |
| Each fight builds | `fightsim.prepare` at each reading's level (Mars 1 at 19, Moira 1 at 26, Jupiter 1 at 27, Argo 1 at 50, Cyrus 1 at 53) | all five built in seconds, with the twins they need (Floragato's Protean, the gas twins); every damaging move has damage rows against every player Pokemon its type can touch |

The probe of 150 fights that showed Somnu 1's AI picking each member's moves was not run; the Overseer runs it as each fight is prepared for its reading.

The trainer AI changed once in a way the drafts meet: since c967e9e04 (2026-10-21, a VANILLA FIX) it rates two-hit moves on both hits, so Torracat's Double Kick and Golbat's Dual Wingbeat score twice what they did at Mars 1's first reading. No other engine change since 2026-10-13 touches a draft's move, ability or item.

What the simulator still runs approximately, by Ian's choice, that the drafts can meet: a Mummy caught secondhand keeps its old rows (Argo 1's Cofagrigus), and a trainer's Pokemon that loses its item to the player while Protean or Roost has changed it keeps the item's rows (Floragato, Pelipper). Both are rare. Nothing a draft carries is open in a single battle.

### Mars 1

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Liepard | 18 | Prankster | Black Glasses | Timid | Thunder Wave, Taunt, Dark Pulse, U-turn |
| Torracat | 18 | Intimidate | Eviolite | Impish | Flame Wheel, Double Kick, Will-O-Wisp, U-turn |
| Floragato | 18 | Protean | Miracle Seed | Adamant | Seed Bomb, Play Rough, Bite, Quick Attack |
| Golbat | 18 | Inner Focus | Leftovers | Hasty | Dual Wingbeat, Leech Life, Bite, Confuse Ray |
| Purugly | 19 | Thick Fat | Sitrus Berry | Jolly | Fake Out, Facade, Knock Off, Shock Wave |

Choices made around a gap: Torracat's U-turn stood in for Parting Shot (b74141f15, "the simulator does not run Parting Shot yet"). Parting Shot runs since 6f15a0854 (2026-10-15, the gaps doc's PARTING_SHOT row) and has been at 5 PP since 014489b98 the same day. Liepard's Foul Play became Dark Pulse for the boss ceiling, not a gap.

What changed for its mechanics since the first reading: Protean (fixed at 74899d5eb, 2026-10-14), so Floragato's Play Rough, Bite and Quick Attack now carry its STAB; Intimidate's double count and its four blockers (74899d5eb); each hit of a two-hit move rolls its own critical hit and contact chance (13ab1f30b); Prankster's status moves fail on a Dark-type target (a544f62d4, 2026-10-20), so Liepard's Thunder Wave and Taunt now fail on a Dark-type player Pokemon such as Vullaby or Nuzleaf; U-turn switches out after a knockout (74899d5eb); Knock Off (aacce7aa6) and Taunt (7fd387f08). The rest of its moves, abilities and items were in the gaps doc's list of what runs right from the start.

Speed: Liepard (57) and Purugly (58) outspeed every Pokemon in the box at 19, whose fastest is 50; Golbat (46) outspeeds 49 of 54. Parting Shot changes none of that.

### Moira 1

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Snover | 25 | Snow Warning | Occa Berry | Calm | Icy Wind, Leech Seed, Magical Leaf, Ice Shard |
| Xatu | 25 | Magic Guard | Leftovers | Bold | Future Sight, Night Shade, Wish, Confuse Ray |
| Galarian Mr. Mime | 25 | Ice Body | Light Clay | Timid | Freeze-Dry, Future Sight, Reflect, Encore |
| Kadabra | 26 | Magic Guard | Colbur Berry | Modest | Future Sight, Psybeam, Shadow Ball, Icy Wind |

No choice on Moira 1 was made around a gap; her reading only waited on fixes. Each is in: Future Sight's delay, untyped damage and slot (74899d5eb), Ice Body (74899d5eb), Encore (74899d5eb), Magic Guard against hazards, recoil and Leech Seed (3ae1c361f, 2026-10-14), Leech Seed itself (dfdf033fd), hail (7fb6af9a2, 2026-10-15), and confusion's checks for Confuse Ray and Psybeam (13ab1f30b). The trainer AI now also sees a Future Sight already pending and an Encore already set (74899d5eb), so it stops choosing them again.

No candidate move is offered. Mime Jr. learns Mystical Power at 33 (since 2026-10-14) and Xatu Esper Wing at 50 (since 2026-10-21), past these levels, and Kadabra could know Stored Power from Abra but has nothing on the team to raise its stats. Aurora Veil, which runs in hail since 4fa2dd2239 (2026-10-15), fits her theme, but no member learns it; it is a candidate for Moira 2 or 3 if one of hers does.

### Jupiter 1

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Pelipper | 26 | Unburden | Sitrus Berry | Bold | Tailwind, Knock Off, Water Pulse, Roost |
| Emolga | 26 | Static | Light Clay | Timid | Nuzzle, Light Screen, U-turn, Thunderbolt |
| Lanturn | 26 | Volt Absorb | Leftovers | Calm | Discharge, Brine, Confuse Ray, Thunder Wave |
| Tangela | 26 | Regenerator | Eviolite | Relaxed | Leech Seed, Sleep Powder, Giga Drain, Ancient Power |
| Galarian Weezing | 26 | Neutralizing Gas | Black Sludge | Sassy | Will-O-Wisp, Pain Split, Strange Steam, Toxic Spikes |
| Skuntank | 27 | Aftermath | Black Glasses | Adamant | Poison Jab, Crunch, Sucker Punch, Taunt |

Choices made around a gap: Clear Smog became Strange Steam and Toxic Spikes (11161ea66, "the simulator does not run Clear Smog's stat reset"). Clear Smog resets its target's stages after the hit since e930b3ef2 (2026-10-15, the CLEAR_SMOG row). The chat set of 2026-10-13 is not recorded in the repo, so which move Toxic Spikes replaced is for Ian to say. Lanturn's Spark became Discharge because Lanturn is a special attacker in Oxide, not for a gap.

What changed for its mechanics: Unburden no longer counts twice (74899d5eb), the fix this fight waited on; Roost drops the Flying type for the turn (74899d5eb); Volt Absorb heals (74899d5eb); Leech Seed (dfdf033fd); Knock Off (aacce7aa6); U-turn after a knockout (74899d5eb); confusion for Confuse Ray, Water Pulse and Strange Steam (13ab1f30b); Taunt (7fd387f08). Neutralizing Gas was fixed just before the draft (93ad73726). Tailwind lasts three turns, the engine's Generation 4 rule, and has run right throughout.

Speed at 27, against a box whose fastest is 71 and whose median is 40:

| Member | Speed | Outspeeds | After Sitrus (Unburden) | Under Tailwind |
|---|---|---|---|---|
| Pelipper | 46 | 158 of 239 | 92 | 92, or 184 with both |
| Emolga | 72 | all | | 144 |
| Lanturn | 47 | 172 of 239 | | 94 |
| Tangela | 39 | 117 of 239 | | 78 |
| Galarian Weezing | 39 | 117 of 239 | | 78 |
| Skuntank | 58 | 216 of 239 | | 116 |

So Tailwind puts the whole team over the box, as the page warned. Neither candidate below touches that. Clear Smog does reach speed indirectly: it wipes a player's Speed boost, which is the counter to Tailwind a box might carry.

Candidates considered and not proposed: Emolga's Electro Ball (learned at 30 since f5672c246, 2026-10-14, inside Fantina's split) would hit for 120 or more under Tailwind, more than Thunderbolt, which pushes away from a 94 percent target.

### Argo 1

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 49 | Levitate | Leftovers | Calm | Stealth Rock, Earth Power, Extrasensory, Ice Beam |
| Bronzong | 49 | Levitate | Light Clay | Sassy | Gyro Ball, Earthquake, Reflect, Payback |
| Cofagrigus | 48 | Mummy | Colbur Berry | Bold | Will-O-Wisp, Hex, Pain Split, Haze |
| Relicanth | 48 | Rock Head | Hard Stone | Adamant | Head Smash, Waterfall, Earthquake, Yawn |
| Aerodactyl | 49 | Unnerve | Wide Lens | Jolly | Stone Edge, Earthquake, Fire Fang, Taunt |
| Polteageist | 50 | Cursed Body | White Herb | Modest | Shell Smash, Shadow Ball, Giga Drain, Psychic |

A team of relics from the ruins, since Ian left Argo free and fossils would repeat Roark's Rock theme. Its commit (745ebf383) says the sets "avoid leaning on" Mummy, Cursed Body and the other abilities that did not run, but none was swapped out: Cofagrigus, Polteageist and Aerodactyl carry Mummy, Cursed Body and Unnerve, which now run (ab05ab1f3, 173debe4c and 8a712d849, all 2026-10-14). Haze now clears the whole field (fa0102258, 2026-10-20) and Payback doubles when its user moves second (e72cde231). The rest ran right throughout.

Speed at 50 (box median 75, fastest 142): Aerodactyl (161) outspeeds the whole box, Claydol (98) four in five, and Polteageist (90) two in three before Shell Smash and all of it after.

No candidate move is offered: no list change since 2026-10-13 reaches these six at their levels (Bronzong's Doom Desire comes at 66), and Stored Power, which Polteageist's Shell Smash would feed, is on none of their lists.

### Cyrus 1

| Pokemon | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Crobat | 51 | Inner Focus | Razor Fang | Jolly | Cross Poison, Brave Bird, U-turn, Taunt |
| Honchkrow | 52 | Super Luck | Black Glasses | Adamant | Crunch, Brave Bird, Sucker Punch, Heat Wave |
| Porygon-Z | 52 | Download | Silk Scarf | Modest | Tri Attack, Thunderbolt, Ice Beam, Shadow Ball |
| Electivire | 51 | Adaptability | Expert Belt | Naive | Thunder Punch, Brick Break, Ice Punch, Earthquake |
| Magmortar | 51 | Flame Body | Charcoal | Timid | Flamethrower, Focus Blast, Psychic, Will-O-Wisp |
| Salamence | 53 | Intimidate | Yache Berry | Naughty | Dragon Dance, Dragon Claw, Earthquake, Fire Fang |

Power, the first six of Cyrus's eighteen, with Honchkrow and Crobat his canon picks. Choices made around a gap: the commit (745ebf383) says Moxie, Analytic and Stored Power do not run, so the sets avoid them. Moxie runs since 141845f89 (2026-10-14), Analytic since 967816972 (2026-10-20) and Stored Power since 4e4acbe53 (2026-10-14). Honchkrow and Salamence have Moxie and Porygon-Z has Analytic in their hidden slots. Honchkrow's Night Slash became Crunch for the critical-hit odds, not a gap, and stays so.

What changed for its mechanics: Download raises one stat once on entry, a real stage, rather than being worked out afresh against each foe (e46352e03); Intimidate counts once (74899d5eb); Brick Break breaks screens in the damage (74899d5eb); U-turn switches out after a knockout (74899d5eb); Taunt (7fd387f08). The rest ran right throughout.

Speed at 53 (box median 79, fastest 150): Crobat (168) outspeeds everything, Electivire (139) all but 9 of 433, and the other four four in five or more.

Candidates considered and not proposed. Moxie on Salamence would stack on Dragon Dance and snowball. Analytic on Porygon-Z adds three tenths only when it moves last, and it outspeeds 376 of 433, so Download's half is worth more. Oblivion Wing reaches Honchkrow at 50 since f5672c246 (2026-10-14), but it is special and this Honchkrow is a physical Adamant set.
