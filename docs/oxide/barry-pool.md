# Barry's pool, and Barry 3's sets

Ian, 2026-10-29: "given we fight him so many times, having him take from a pool of 9-12 pokemon that gets progressively harder as the game goes on seems fair to me", matched neither exactly backwards nor forwards ("there's only so early in a game you can fairly fight a turtonator"), and the pool outlined before Barry 3's sets are made. On Barry 3 he named three faults (the "optimalness" of the Staraptor and Snorlax sets, an Empoleon set that "thinks that it is still a special attacker", an Ambipom that "can almost-literally never use last resort") and a team shape "very reminiscent of that Hyper-Offense" he wants to get away from. Part 1 is the pool, refined on Ian's answers below. Part 2 is Barry 3: the sets of shape C, which Ian picked, written into the three Route 209 files on this branch, then the first draft's evidence, diagnosis and three shapes as the record.

## Ian's answers

On the first draft (2026-10-29):

1. Twelve slots for each starter version, as drafted.
2. Turtonator joins in Barry 3 too, not only from Barry 4, and Barry 3 brings six.
3. Luxray rests from Barry 5 on, and Shinx replaces Buizel in Barry 2.
4. "I want to scale his threats a bit more. Goodra I like the idea of, but I have given it to Wake's new team; switch frosmoth for volcarona and drop the goodra for Stakataka." Volcarona's line takes Frosmoth's slot and Stakataka takes Goodra's. Florges stays.
5. Barry 3's shape waits: "Let's revisit this after we refine the pool."

Wake's new team, in Ian's OxiDex and not yet committed, is Clodsire, Ludicolo, Jellicent, Gyarados, Goodra and Floatzel. No line of the refined pool is on it.

On the refined pool (2026-10-29):

1. Quiver Dance goes on Larvesta's egg list, the trainers' palette (done on this branch, with its entry in `learnrewrite.IAN_EGG_MOVES`; Larvesta has no hand-set line in `learnsets_by_hand.txt`, so nothing changes there).
2. Two Fire types from Spear Pillar on: fine.
3. Stakataka is held to Spear Pillar, so Barry 5 takes another pool member: Snorlax (below).
4. Barry 3's third shared slot is Snorlax, and Snorlax does not return in Barry 6; both tentative.
5. Barry 3 takes shape C, bait and setup.
6. The Fight Area partner comes down to the cap of 71 (done: the ace at 71, the other five at 70, sets untouched).

## Summary

**Outcome.** Barry 3's three files now carry shape C (the sets are in part 2): six members in every version, the ace at 36, one at 35 and four at 34, every item and nature its own, every move legal at its level. The trainer lint, the packer, the legality check, test_b1, test_trainers and test_m8 all pass. The AI plays the setup: in 100 rough fights a six, Snorlax's Curse is picked 136 to 190 times, Serperior's Calm Mind 71 to 148, Empoleon's Agility 79 to 94, Infernape's Nasty Plot 38 to 61, Primeape's Bulk Up 33 to 51, Turtonator's Iron Defense 36 to 56 and Torterra's Rock Polish 18 to 24. The bait works only in part. When a Rock or Steel wall stops Staraptor, the AI keeps attacking rather than U-turning (U-turn 0 to 43 picks), so the hand-off comes when Staraptor faints. Once Primeape comes in on a Rock or Steel wall, it attacks first more often than it boosts.

**The twelve.**

| Slot | Line | Fights | Role | Why Barry |
|---|---|---|---|---|
| 1 | His starter: Turtwig, Chimchar or Piplup line | all | the ace | canon: the starter strong against the player's |
| 2 | First element partner: Greninja or Serperior line | Barry 3 on | Water or Grass cover, special damage | Ian's Barry 4: Barry took the other regions' starters too, as vanilla Barry carried the two elements his starter lacked |
| 3 | Second element partner: Serperior line or Turtonator | Barry 3 on | the third element | as above |
| 4 | Starly line | Barry 2, 3, 4, 5, 6 | Intimidate lead and pivot, Tailwind | his first catch, in every vanilla Barry fight |
| 5 | Munchlax line | Barry 2, 3, 4, 5 | the slow anchor: Curse, Body Slam, Yawn | canon; the one patient Pokemon on an impatient trainer's team |
| 6 | Shinx line | Barry 2, 4 | fast physical Electric and Dark | Ian's pick for Barry 4 |
| 7 | Togedemaru | Fight Area | Fake Out, Nuzzle, U-turn; Lightning Rod draws Volkner's Electric moves away from the player | a spiky ball that rolls into things, as Barry runs into the player |
| 8 | Larvesta line (Volcarona) | Spear Pillar, Barry 6 | special Fire and Bug with Quiver Dance | Ian's pick |
| 9 | Mankey line (Primeape, Annihilape) | Barry 3, 5 | Bulk Up attacker | always angry, Barry's temper |
| 10 | Dratini line | Spear Pillar, Barry 6 | the late power member | Palmer, Barry's father, carries a Dragonite; so did the base ROM's late Barry |
| 11 | Stakataka | Spear Pillar, Fight Area | Rock and Steel wall, Beast Boost; Trick Room, Stealth Rock and Iron Defense in its palette | Ian's pick |
| 12 | Flabebe line (Florges) | Fight Area | Wish, Helping Hand, Aromatherapy: a partner's support | takes the place of canon Barry's Roserade, the flower on his vanilla team |

Which partners each player meets, both from Barry 3:

| Player's starter (file suffix) | Barry's starter | Partners |
|---|---|---|
| Turtwig (`_turtwig`) | Infernape | Serperior, Greninja |
| Scorbunny (`_chimchar`) | Empoleon | Serperior, Turtonator |
| Piplup (`_piplup`) | Torterra | Greninja, Turtonator |

**The pool against the fights.** Each column is the six he brings, at the stage the line can be at that level. Barry 3 is in the files on this branch; Barry 4 is Ian's six.

| Slot | Barry 1 (5) | Barry 2 (cap 11) | Barry 3 (36) | Barry 4 (42) | Barry 5 (Byron's split) | Spear Pillar (partner, 59) | Fight Area (partner, 71) | Barry 6 (71) |
|---|---|---|---|---|---|---|---|---|
| Starter | first stage | first stage | final, 36 | final | final | final | final | final |
| First partner | | | Serperior 35, or Greninja 35 for a Piplup player | final | final | final | final | final |
| Second partner | | | Greninja 34, or Turtonator 34 | final | final | final | final | final |
| Starly line | | Starly | Staraptor 34 | Staraptor | Staraptor | | | Staraptor |
| Munchlax line | | Munchlax | Snorlax 34 | Snorlax | Snorlax | | | |
| Shinx line | | Shinx | | Luxray | | | | |
| Togedemaru | | | | | | | Togedemaru | |
| Larvesta line | | | | | | Volcarona 59 | | Volcarona |
| Mankey line | | | Primeape 34 | | Annihilape or Primeape | | | |
| Dratini line | | | | | | Dragonite | | Dragonite |
| Stakataka | | | | | | Stakataka | Stakataka | |
| Flabebe line | | | | | | | Florges | |

Barry 5 takes Snorlax in Stakataka's place. It is the strongest pool line open there that no nearby boss uses: Luxray rests for Mars 2, Volcarona is not fair before 59, Dragonite would still be a Dragonair, and Togedemaru (a base stat total of 465 against Snorlax's 540) is weaker. And since Snorlax sits out Barry 6, Barry 5 is its last fight. Spear Pillar takes Stakataka in Florges's place, so Florges now plays only at the Fight Area. The pool still grows harder by entry: Barry 2 is four first stages, Barry 3 is mid-power (505 for Primeape, 485 for Turtonator, about 530 for the starters' finals), Barry 5 brings Annihilape (535), and Volcarona (550), Stakataka (570) and Dragonite (600) arrive at Spear Pillar. Barry 1 keeps his lone starter and does not count for deaths.

**What Ian decides.**

1. Primeape's most-picked move is Stone Edge, which the AI fires at the Fairy and Flying answers, so it boosts in only about half the fights. Keep it, or swap it for a move that leaves Bulk Up the better pick (Taunt or Ice Punch, both in its palette)?
2. The AI does not U-turn out of a Rock or Steel wall, so the bait hands off on a faint. Accept that, or give Staraptor a reason to pivot (dropping Steel Wing leaves Double-Edge as its pick into those walls, so that alone would not do it)?
3. Setup First Turn on Barry's AI: tried, it raises Bulk Up only to 36 to 57 picks and mainly doubles Tailwind (71 to 83). I left it off.
4. Empoleon's Knock Off was never picked: swap it for Drill Peck (on Piplup's egg list) or Icy Wind?
5. The Fight Area files' Shiftry carries Swords Dance and Low Kick, which no list gives it. That was already so at 74 and is allowed from Cyrus 3's split on, so I left it.

**Next steps.** Ian checks the sets in his OxiDex and answers in a line each; any swap is minutes. Barry 2's Shinx swap and Barry 5, the two partner fights and Barry 6 from the pool: an hour or two each, after Ian's Barry 4 lands. The in-game check for Barry 3 is in `ingame-checklist.md`. A spot-check reading only if he names one: two and a half to four hours.

## Part 1: the pool

### How the versions work

The scripts pick Barry's file by the player's starter. The suffix names the starter Platinum had in that seat, so `_chimchar` is the Scorbunny player's file (Scorbunny took Chimchar's place in the briefcase, and Barry keeps the Chimchar line for a Turtwig player; `lucas-dawn-2-redesign.md`, "Which starter meets which team"). Barry takes the starter strong against the player's: Infernape for a Turtwig player, Empoleon for a Scorbunny player, Torterra for a Piplup player.

Ian's Barry 4 (his OxiDex, not committed and not final) is Staraptor, Snorlax, Luxray and the starter in every version, with two of Serperior, Greninja and Turtonator: the two whose types the starter lacks. So every version carries one Fire, one Water and one Grass member, which is vanilla Platinum's pattern (Barry carried two of Floatzel, Rapidash and Roserade beside his starter) with other regions' Pokemon in place of the canon three. The pool keeps that: slots 1 to 3 change by version, slots 4 to 12 are shared.

### The fights, and the bosses around them

The fights in play order (`tools/oxide/balance/fights.json`), with the boss fights near each and the lines the pool keeps out for them. Lines on ordinary trainers were not counted.

| Fight | Bosses around it | Kept out of the pool, or rested there |
|---|---|---|
| Barry 2 (Route 203, Roark's split) | Lucas and Dawn 1, Roark | Buizel's line (Floatzel is Wake's ace later) |
| Barry 3 (Route 209 gate, Maylene's split) | Fantina, Lucas and Dawn 2, Maylene, Tyche and Hermes 1 | Floatzel (Wake), Heracross (Maylene, Aaron), Decidueye (Fantina), Scyther and Lopunny (Lucas and Dawn) |
| Barry 4 (Pastoria, Wake's split) | Tyche and Hermes 1, Wake (Ian's new six, with Goodra) | Goodra (Wake), as Ian ruled; Ian's six as it is |
| Barry 5 (Canalave, Byron's split) | Cyrus 1, Argo 1, Byron; Mars 2 just after | Luxray rested (Mars 2 carries one); Stakataka held back (Ian); Salamence, Gyarados, Bronzong, Metagross are the bosses' |
| Spear Pillar, beside the player | Tyche and Hermes 2, Mars and Jupiter, Cyrus 3 | Luxray rested (Mars carries one in the same battle); Shiftry out (Tyche and Hermes 2 field one in the double before) |
| Fight Area, beside the player | Volkner and Flint, the foes | Luxray rested (Volkner's), Ninetales out (Flint's in the League) |
| Barry 6 (League gate, Barry's split) | Volkner, Lucas and Dawn 3, the Elite Four | Ninetales (Flint), Heracross (Aaron), Roserade (Cynthia) |

No boss file on `oxide` or Wake's new six carries Volcarona, Larvesta or Stakataka. Mars's cat theme takes the Litten and Sprigatito lines (Mars 1 fields Torracat and Floragato), so neither is a candidate partner. The starter slot is the one exception to the rule: the Turtwig player's Barry keeps Infernape, which Flint also carries at the Fight Area and in the League, as in vanilla.

Today's late Barry fields Ambipom, Floatzel, Heracross, Ninetales, Shiftry and Starmie; all six leave the pool, the first four for the reasons above or Ian's own Barry 4 choices, Starmie for room (Greninja holds the Water seat).

### Legality by level

Every stage in the pool table is one a trainer can have at that fight's level. The close ones:

| Member | Level | Evolves at |
|---|---|---|
| Snorlax, Barry 3 | 34 | Munchlax at 36 |
| Serperior, Barry 3 | 35 | Servine at 36 |
| Greninja, Barry 3 | 34 (Turtwig player), 35 (Piplup player) | Frogadier at 36 |
| Annihilape, Barry 5 | Barry 5's level, not set yet (its file's ace is 53) | Primeape at 50 |
| Volcarona, Spear Pillar | 59 | Larvesta at 59 |

Volcarona is fair from 59, its evolution level, which is where Spear Pillar's partner sits; the Fight Area and Barry 6 (both 71) are well past it. Larvesta would be the only stage open at Barry 5, and with a base stat total of 360 it would be the weakest member of a late fight, against Ian's wish to scale the threats. Stakataka and Florges have no level bar (Florges comes from Floette with a Shiny Stone). If Barry 5's honour cap lands under 50, Annihilape is Primeape there.

What the late lines' palettes give them, by the OxiDex's own list: Volcarona at 59 has Mystical Fire, Fire Spin, U-turn and Screech by level, Calm Mind, Flamethrower, Fire Blast, Giga Drain, Psychic, Will-O-Wisp and Light Screen by TM, and now Quiver Dance through Larvesta's egg list. Stakataka has Iron Defense, Autotomize, Rock Blast, Block and Wide Guard by level and Trick Room, Stealth Rock, Gyro Ball, Stone Edge, Earthquake, Meteor Beam and both screens by TM. With 13 base Speed, a Trick Room Stakataka is the clearest new threat in the pool.

### Florges beside the stronger pool

Florges is the one support line left. Its base stats in Oxide (78, 65, 68, 112, 154, 75) make it a special wall with a middling attack, and it has no Moonblast until 57. Next to Volcarona, Stakataka and Dragonite it would read weak in a fight against the player, so it plays only at the Fight Area, beside the player, where Wish, Helping Hand and Aromatherapy help the player and its bulk keeps a partner alive. If Ian wants every slot a threat, Florges is the one to swap, for a line he names.

### The later fights, in a sentence each

Barry 5 is the first fight of the late pool: the three elements, Staraptor, Snorlax and Annihilape. At Spear Pillar, Barry fights beside the player against Mars and Jupiter with Dragonite, Volcarona and Stakataka. At the Fight Area his Togedemaru's Lightning Rod draws Volkner's Electric moves away from the player (the game redirects them in doubles; the simulator does not, as `simulator-gaps.md` lists), and Stakataka and Florges take the physical and special sides. Barry 6 is the three elements, Staraptor, Dragonite and Volcarona, with Annihilape and Stakataka as the swap-ins. Today's Fight Area files keep their old sets at the new levels until that fight's turn comes.

The post-game Survival Area rematches (Battleground files at 65 and 85, from the base ROM) are outside the road to the alpha; the late pool can fill them later, and the 85 sits past the game's 78.

## Part 2: Barry 3

### The sets (shape C, on this branch)

Ian picked shape C: Staraptor leads, and the Rock and Steel walls that stop it draw in a Fighting or Ground member with a setup move behind it. Every member holds its own item and has its own nature, with no repeats in a version, and most of the natures are not the textbook one for the set. iv_scale 255, AI flags Basic, Evaluate Attack and Expert (unchanged). Speed is as the scorer builds the files.

The three shared members, the same in every version:

| Member | Level | Ability | Item | Nature | Speed | Moves | Role |
|---|---|---|---|---|---|---|---|
| Staraptor (lead) | 34 | Intimidate | Charti Berry | Hasty | 94 | Double-Edge, Steel Wing, U-turn, Tailwind | the bait: Intimidate on the physical box, Steel Wing for the Fairy and Ice answers, Tailwind for the slow setup members; the Charti Berry takes the edge off the first Rock hit |
| Primeape | 34 | Defiant | Liechi Berry | Impish | 80 | Bulk Up, Drain Punch, Rage Fist, Stone Edge | the Rock and Steel walls' answer: Drain Punch takes 58 to 69% of Bastiodon and 74 to 89% of Probopass before a boost; Defiant punishes Granbull's Intimidate |
| Snorlax | 34 | Immunity | Chesto Berry | Relaxed | 31 | Curse, Body Slam, Yawn, Rest | the slow win condition: Curse, Body Slam's paralysis, Yawn to force switches, one quick Rest; Immunity shrugs off Glimmora's Toxic Debris and Tentacruel's Toxic Spikes |

By version:

| Version | Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---|---|---|---|---|---|---|
| Turtwig player (`_turtwig`) | Serperior | 35 | Overgrow | Big Root | Calm | 94 | Calm Mind, Giga Drain, Dragon Pulse, Reflect |
| | Greninja | 34 | Torrent | Expert Belt | Rash | 98 | Taunt, Surf, Dark Pulse, Ice Beam |
| | Infernape (ace) | 36 | Blaze | Wise Glasses | Mild | 93 | Nasty Plot, Flamethrower, Vacuum Wave, Grass Knot |
| Scorbunny player (`_chimchar`) | Serperior | 35 | Overgrow | Big Root | Calm | 94 | Calm Mind, Giga Drain, Dragon Pulse, Reflect |
| | Turtonator | 34 | Shell Armor | Shuca Berry | Bold | 40 | Iron Defense, Body Press, Flamethrower, Will-O-Wisp |
| | Empoleon (ace) | 36 | Torrent | Sitrus Berry | Naughty | 59 | Agility, Aqua Tail, Earthquake, Knock Off |
| Piplup player (`_piplup`) | Greninja | 35 | Torrent | Expert Belt | Rash | 101 | Taunt, Surf, Dark Pulse, Ice Beam |
| | Turtonator | 34 | Shell Armor | Shuca Berry | Bold | 40 | Iron Defense, Body Press, Flamethrower, Will-O-Wisp |
| | Torterra (ace) | 36 | Shell Armor | Yache Berry | Careful | 56 | Rock Polish, Wood Hammer, Earthquake, Crunch |

What each fixes of Ian's three faults. Empoleon plays as Oxide makes it: Attack 111 against Sp. Atk 86, so a physical Agility set on a Naughty nature. Last Resort and Ambipom are gone. Staraptor and Snorlax carry neither the old sets nor their textbook natures: no Brave Bird, Close Combat or Roost on Staraptor, which is there to be walled, and Snorlax is a Curse and Rest sleeper with Immunity rather than Thick Fat and Earthquake.

Each version has four setup members (Primeape, Snorlax, one partner or the second partner, and the ace), which is what shape C asks. Only Greninja and Staraptor carry no boost, and the team's fast members are Staraptor (94), Serperior (94), Greninja (98 to 101) and Infernape (93). Ambipom (102), Floatzel (93) and Infernape (102) were the old team's.

Legality: every move is on its species' Oxide list at its level (the Kaizo study's checker, run over this branch's `res/`, and the OxiDex's list agree). Torterra's Crunch is on Turtwig's egg list, put there for Barry 3 on 2026-10-29 (its hand-set line), and Double-Edge is Starly's egg move. The checker's only notes are three members under their evolution level: Serperior at 35, Greninja at 34 and 35, Snorlax at 34, against 36 each.

### The cheap checks on the sets

The matchup screen on goal 3's three boxes (at 36), the screen's score per Barry member (lower is harder for the player), and the most-taken catches:

| Box | Score per member | Taken most |
|---|---|---|
| 1 (Turtwig player) | 2.97 | Sylveon 20, Tentacruel 16, Bastiodon 16, Probopass 14, Togetic 10 |
| 2 (Scorbunny player) | 3.27 | Tsareena 18, Primarina 17, Bastiodon 15, Rotom 14 |
| 3 (Piplup player) | 2.38 | Vikavolt 18, Hariyama 16, Bastiodon 15, Rotom 14, Granbull 10 |

For comparison, today's five on `oxide` read 1.61, 1.27 and 1.90, and the first draft's shape C 2.99, 2.98 and 2.56. The screen counts damage and Speed only, so a setup team reads easier on it than it plays. This fight is the case the standing rulings give a margin or a spot check.

Damage, the calculator's lowest to highest roll as a share of the target's HP (Barry's members as the files have them; the player's catches at 36, Hardy, IVs of 15):

| Attacker | Move | Target | Damage |
|---|---|---|---|
| Staraptor | Double-Edge | Sylveon | 66 to 79% |
| Staraptor | Steel Wing | Bastiodon | 13 to 16% |
| Primeape | Drain Punch | Probopass | 74 to 89% |
| Primeape | Stone Edge | Togetic | 75 to 90% |
| Greninja 35 | Dark Pulse | Rotom | 99 to 118% |
| Greninja 35 | Surf | Bastiodon | 53 to 66% |
| Turtonator | Flamethrower | Vikavolt | 79 to 96% |
| Infernape | Vacuum Wave | Bastiodon | 44 to 58% |
| Empoleon | Earthquake | Bastiodon | 61 to 74% |
| Empoleon | Knock Off | Rotom | 55 to 67% |
| Torterra | Earthquake | Bastiodon | 85 to 102% |
| Torterra | Earthquake | Tentacruel | 127 to 150% |
| Bastiodon | Take Down | Staraptor | 21 to 25% |
| Rotom | Shock Wave | Staraptor | 77 to 93% |
| Togetic | Dazzling Gleam | Primeape | 57 to 69% |
| Tentacruel | Poison Jab | Serperior | 52 to 63% |

So Bastiodon and Probopass stop Staraptor by walling it (Steel Wing 13 to 16%), not by knocking it out; Rotom is the one that beats it outright.

The AI-picks probe on all three boxes (a greedy player, 100 rough fights a six, against the screen's best six and its six most taken; win numbers mean nothing). Every move on every member was picked except Empoleon's Knock Off, which the AI also skipped in the first draft's probes. Setup picks per 100 fights:

| Member | Setup move | Picks |
|---|---|---|
| Snorlax | Curse | 136 to 190 |
| Serperior | Calm Mind | 71 to 148 |
| Empoleon | Agility | 79 to 94 |
| Infernape | Nasty Plot | 38 to 61 |
| Turtonator | Iron Defense | 36 to 56 |
| Primeape | Bulk Up | 33 to 51 |
| Torterra | Rock Polish | 18 to 24 |
| Staraptor | Tailwind | 25 to 42 |

Whether the bait plays as intended, from what each member did first on coming in:

- Staraptor attacks the wall in front of it. U-turn was picked 0 to 43 times a six, mostly against Vikavolt and Bronzong, so the hand-off to the member behind comes on a faint.
- On box 1, Primeape came in on Probopass 23 times in one six and 18 in the other. It opened with Drain Punch 17 and 18 times, and with Bulk Up 6 times and none. The Infernape version sends Infernape into Bastiodon instead (Vacuum Wave 19 to 20 times, Nasty Plot 3 to 10), since its Fighting and Fire types read as the harder hit.
- On box 3, Primeape came in on Bastiodon 18 times in the best six: Bulk Up 10, Drain Punch 8.
- On box 2, Bastiodon draws Empoleon's Earthquake (19 to 21 times), and Primeape mostly meets Rotom (Rage Fist 6 to 13, Bulk Up 5 to 12).
- Primeape's most-picked move overall is Stone Edge (73 to 154), at the Fairy, Bug and Flying answers.
- The other setup members boost on entry far more readily. Serperior opened with Calm Mind 26 to 36 times against Tentacruel or Primarina, Snorlax with Curse 5 to 16, and Empoleon with Agility 16 to 29 against Rotom.

So the fight is setup-heavy as Ian asked, and the AI plays it, but the specific bait (Staraptor walled, Primeape boosting on the wall) happens in a minority of fights. Questions 1 and 2 of the summary are the two levers.

### The first draft's shapes and the refined pool

The shapes below are the first draft's, made with one element partner per version and with Frosmoth in the pool; shape C above is what came of them. Two things in the refined pool changed all three: Barry 3 carries both partners in every version, so each shape keeps three shared members instead of four, and Frosmoth left the pool, so shapes A and C lost their Quiver Dance member, whose place in the written shape C goes to the second partner and to Snorlax's Curse.

### The evidence

The three files (cap 36 since 2026-10-29, ace at 36), with Speed as the scorer builds them. iv_scale 255, AI flags Basic, Evaluate Attack and Expert.

| Member | Level | Item | Ability | Nature | Speed | Moves |
|---|---|---|---|---|---|---|
| Ambipom | 34 | Silk Scarf | Technician | Jolly | 102 | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 35 | Sharp Beak | Intimidate | Adamant | 89 | Brave Bird, Close Combat, U-turn, Roost |
| Floatzel | 34 | Mystic Water | Swift Swim | Adamant | 93 | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 35 | Leftovers | Thick Fat | Careful | 36 | Body Slam, Earthquake, Curse, Ice Punch |
| Infernape (Turtwig player) | 36 | Sitrus Berry | Blaze | Jolly | 102 | Close Combat, Fire Punch, Mach Punch, U-turn |
| Empoleon (Scorbunny player) | 36 | Sitrus Berry | Torrent | Modest | 59 | Surf, Drill Peck, Ice Beam, Flash Cannon |
| Torterra (Piplup player) | 36 | Sitrus Berry | Thick Fat | Adamant | 56 | Wood Hammer, Earthquake, Crunch, Stone Edge |

The matchup screen (`plgoal3 --box barry_3 <seed> --screen`, seeds 1 to 3, the box at 36) gives these answers. Box 1 meets the Turtwig player's file, box 2 the Scorbunny player's, box 3 the Piplup player's.

| Box | In all 20 top sixes | Often |
|---|---|---|
| 1 | Glimmora | Kingler (Krabby held to 35) 13, Quagsire 12, Granbull 11, Probopass 10, Staraptor 9, Tentacruel 9 |
| 2 | Rotom | Staraptor 16, Seaking 10, Bastiodon 10, Cofagrigus 10, Arboliva 9, Cinderace (held to 34) 8 |
| 3 | Kingler (held), Breloom, Rotom | Machoke 15, Hariyama 6 |

The boxes' speed lines at 36: Talonflame 101, a held Cinderace 96, Salazzle 94, Liepard 93, Haunter 89, Staraptor 86, Tentacruel and Alolan Ninetales 82, Luxray, Pachirisu and Leafeon 78, Leavanny and Tsareena 76, Rotom, Golbat and Orbeetle 75, Glimmora 72, Kingler 64, Breloom 60, Hariyama 46, Machoke 42, Probopass 39, Quagsire 35, Bastiodon 32. The soft-cap box will sit lower once Ian approves that method, so every margin here leans a little toward the player.

### The diagnosis

The three faults Ian named are in the files. Staraptor's and Snorlax's sets are the textbook ones. Oxide's Empoleon has Attack 111 and Sp. Atk 86, so its Modest set of four special and mixed moves runs on its weaker stat. Last Resort works only after every other move has been used in one stay, and Ambipom's U-turn ends the stay, so it almost never fires.

The shape is hyper offense in the balance plan's sense (goal 1: high threat, few tactics, most turns called). Ambipom (102), Floatzel (93) and Staraptor (89) move before all but one or two catches in each box, and so does the Turtwig player's Infernape (102). That version carries three U-turns, two Close Combats and a Fake Out, and every damaging move on the team but Empoleon's is physical. It also has five members, not six.

The boxes answer it with typing. Rotom, in every top six of boxes 2 and 3, is immune to Normal, Fighting and Ground, nearly half the team's moves. Glimmora, in every top six of box 1, lays a layer of Toxic Spikes on Barry's side each time a physical move hits it. Kingler's Hyper Cutter, Granbull's Intimidate and the Rock and Steel walls (Probopass, Bastiodon) take the physical hits. Floatzel is Wake's ace one split later, the reason Ian dropped it from Barry 4. Natures repeat in every version: Adamant twice (three times for a Piplup player), and Jolly twice for a Turtwig player.

On the screen today's team is the hardest of anything here, because damage and Speed are all the screen counts. That is the signature of hyper offense, and the reason the shapes below read easier on it.

### Three shapes

Each shape was screened with provisional sets (moves only so the screen and the calculator have something to read; these are not proposed sets) and probed on box 1, with box 2 and 3 probes for the recommended one. The screen's score below is the top six's score divided by Barry's members: per member, the best answer's margin capped at 3, plus a little for a second answer, less 2 for a member nothing answers. Lower means the player's best six answers Barry less well.

| Team | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Today's five | 1.61 | 1.27 | 1.90 |
| Shape A | 2.68 | 3.16 | 2.86 |
| Shape B | 2.06 | 2.61 | 2.38 |
| Shape C | 2.99 | 2.98 | 2.56 |

The screen counts no status move, hazard or boost. Every shape trades damage for those, so these numbers say how much damage was given up, not how hard the fight is.

Damage figures are the calculator's lowest to highest roll as a share of the target's HP: Barry's members at their levels with top IVs, the player's catches at 36, Hardy, IVs of 15.

| Attacker | Move | Target | Damage |
|---|---|---|---|
| Primeape 34 | Close Combat | Bastiodon | 91 to 110% |
| Primeape 34 | Close Combat | Probopass | 116 to 137% |
| Primeape 34 | Rage Fist (a plain 50-power hit in Oxide) | Rotom | 34 to 41% |
| Luxray 34 | Crunch | Rotom | 90 to 106% |
| Greninja 35 | Night Slash | Rotom | 64 to 78% |
| Greninja 35 | Surf | Bastiodon | 41 to 50% |
| Snorlax 35 | Earthquake | Bastiodon | 55 to 66% |
| Staraptor 34 | Double-Edge | Breloom | 71 to 84% |
| Frosmoth 34 | Giga Drain | Quagsire | 98 to 117% |
| Frosmoth 34 | Ice Beam | Breloom | 140 to 166% |
| Togedemaru 34 | Zing Zap | Kingler | 61 to 73% |
| Rotom 36 | Shock Wave | Staraptor | 77 to 93% |
| Golbat 36 | Dual Wingbeat | Primeape | 61 to 72% |
| Togetic 36 | Dazzling Gleam | Primeape | 57 to 69% |
| Probopass 36 | Rock Blast (the runner's total) | Frosmoth | 141 to 176% |

#### Shape A: speed control

Barry cannot stand being slower, so his team makes the player slower.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Togedemaru 34 | Fake Out, Nuzzle and Zing Zap to paralyse and chip, U-turn out; Lightning Rod takes the Electric moves aimed at Staraptor and the Water members | 80 |
| 2 | Greninja 35, or Serperior 35 for a Scorbunny player | Icy Wind's Speed drop; Serperior sets Light Screen and Reflect | 111, 103 |
| 3 | Staraptor 34 | Tailwind, Intimidate, Double-Edge | 94 |
| 4 | Snorlax 35 | the slow anchor that paralysis and Tailwind let act first: Body Slam, Yawn, Rest | 32 |
| 5 | Frosmoth 34 | Quiver Dance behind the slowed field; Ice Scales halves special hits; Ice Beam, Giga Drain, Stun Spore | 59 |
| Ace | the starter, 36 | Infernape with Will-O-Wisp and Grass Knot, Empoleon with Icy Wind, Torterra with Zen Headbutt for the Fighting answers | 102, 59, 50 |

What it asks: keep the six's Speed, with Ground types (immune to Nuzzle), Natural Cure and hard hits before the slowed field turns. Cover: Frosmoth takes the Grass and Ground answers, Staraptor the Fighting ones, Snorlax the special hitters. The lead test: Togedemaru's counters are the Ground types (margins of 1.5 to 3.0 against it: Quagsire, Whiscash, Donphan, Graveler, Onix, Torterra), and the AI can send Frosmoth into them, with Giga Drain and Quiver Dance. That holds for Quagsire, but the Ground types with Rock moves (Graveler, Onix, Torterra's Rock Blast, Whiscash's Rock Tomb) knock Frosmoth out first, so the rule holds only in part. Against the answers: Rotom stays in every top six on boxes 2 and 3, and Bastiodon in 10 to 16. The probe's weakness is the shape's whole idea: the AI used Nuzzle 15 to 19 times in 100 fights, Tailwind 6 to 31, Quiver Dance 17 to 24, and took Zing Zap's damage instead.

#### Shape B: hazards and forced switches (the first draft's recommendation)

Barry will not let the player's Pokemon stay in.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Primeape 34 | Stealth Rock and Taunt on turn one; Close Combat for the Rock and Steel walls, Rage Fist for the Ghosts; Defiant punishes Granbull's Intimidate | 80 |
| 2 | Greninja 35, or Serperior 35 for a Scorbunny player | Spikes, Night Slash for Rotom, Surf, Ice Beam; Serperior sets Light Screen and Reflect, with Giga Drain and Knock Off | 111, 103 |
| 3 | Staraptor 34 | Whirlwind over the hazards, Intimidate, Double-Edge, Roost | 94 |
| 4 | Snorlax 35 | Yawn forces switches; Body Slam, Earthquake for the walls, Rest | 32 |
| 5 | Luxray 34 | Roar, Crunch for Rotom, Thunder Fang for the Flying and Water answers | 80 |
| Ace | the starter, 36 | Infernape with Knock Off, Empoleon with Knock Off and Earthquake, Torterra with Crunch and Synthesis | 102, 59, 50 |

What it asks: a plan with few switches. Every forced switch costs an eighth to a half of a Pokemon's HP to Stealth Rock, plus Spikes, and the player's answers to it are the boxes' Taunt users (Probopass, Bastiodon, Bibarel, Cinderace, Tsareena) and Defog where a catch has it. Cover: Primeape takes Bastiodon and Probopass, Luxray and Greninja take Rotom, Snorlax takes Fire and the special hits, Staraptor the Fighting and Grass answers. The lead test: Primeape's counters are the Flying, Fairy and Psychic catches (Golbat, Togetic, Mothim, Orbeetle, Granbull), which draw Luxray, and Luxray has no setup move, so Ian's permission for a wholly countered lead does not apply. The lead does its job anyway: it outspeeds Golbat (75) and Togetic (39), and its first move against them was Stealth Rock in 11 to 13 of the 16 or 17 fights each led. Against the answers: the hardest of the three on the screen; Rotom stays in every top six on boxes 2 and 3, Bastiodon in 8 to 16, Golbat 9 to 14, Togetic 8 to 15. The probe, on all three boxes: Stealth Rock was picked 78 to 89 times in 100 fights, Spikes 67 to 89, Roar 32 to 95, Whirlwind 9 to 145, Yawn 141 to 243, and every other move too except Knock Off, which went unpicked on all three members that carried it (Infernape, Serperior, Empoleon).

#### Shape C: bait and setup

The lead is meant to be countered, and its counters hand a setup member its turn.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Staraptor 34 | Intimidate, U-turn, Double-Edge, Steel Wing for Glimmora and Granbull | 94 |
| 2 | Primeape 34 | Bulk Up, Drain Punch, Rage Fist, Stone Edge | 80 |
| 3 | Frosmoth 34 | Quiver Dance, Ice Beam, Giga Drain | 59 |
| 4 | Snorlax 35 | Curse, Body Slam, Yawn, Rest | 32 |
| 5 | Greninja 35, or Serperior 35 for a Scorbunny player | Taunt against the player's own setup; Serperior with Calm Mind | 111, 103 |
| Ace | the starter, 36 | Infernape with Nasty Plot, Empoleon with Agility, Torterra with Rock Polish | 102, 59, 50 |

What it asks: never give a free turn, and beat each boosting member before it boosts. The lead test holds best here: Staraptor's counters are Bastiodon, Probopass and Rotom (a margin of 3.0 each), and the first two draw Primeape, whose Fighting moves hit them four times over, with Bulk Up on the turn the player switches out. Rotom draws Primeape too, but Rage Fist takes only a third of its HP. Against the answers: Rotom drops to 9 and 14 of the top sixes on boxes 2 and 3, but Bastiodon is in 17 to 20 and box 1 takes Tentacruel and Sylveon in all 20, the Water and Fairy answers to Frosmoth and Primeape. The probe used Curse about 250 times in 100 fights, Bulk Up 34, Quiver Dance 22. With four members that boost, the fight turns on one setup turn won or lost, which is the nearest of the three to the offense Ian wants to leave, only slower.

### The first draft's recommendation

Shape B, before Ian paused the shapes. It is the only one whose tactics the AI plays in nearly every fight: hazards, phazing and Yawn are picked over and over on all three boxes, where shape A's AI skips its own speed control. It taxes switching, which is what a planned fight runs on, and it reads hardest of the three on the screen while doing it. It also leads into Ian's Barry 4, whose Glare, screens and Drum Beating are tactics of the same kind.

Its gaps are known. Rotom stays in every top six on boxes 2 and 3; Luxray's Crunch and Greninja's Night Slash answer it, but the Scorbunny player's version has Serperior in Greninja's seat, and the AI never picked the Knock Off its Serperior and Empoleon carried, so Luxray is that version's one sure answer until the sets stage finds another. It has no setup member, so a counter to the lead is safe once the rocks are down. And Primeape is a Fighting type one fight before Maylene's Fighting gym, so the Flying, Fairy and Psychic catches a player brings for her are already its answers.

### How the numbers were made

All on this branch at db48fd8ea, writing nothing under `res/`:

- The boxes and the screen: `PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgoal3 --run barry-pool-study --box barry_3 <seed> --screen`, seeds 1 to 3.
- The shapes: a scratch script that swaps each shape's six into all three Route 209 files in memory (wrapping `data.oxide_trainers` and `plscore.with_genders`, as the Fantina lead study did) and runs `plteam.screen` and `plteam.matchups`; the probe is the Fantina page's AI-picks probe (a greedy player, 100 rough fights a six, against the screen's best six and its six most taken; its win numbers mean nothing).
- Damage: `calc.run_node`, the runner every reading uses.
- Legality: the OxiDex's own list (`learnsets.oxide_list`) at each member's level. Every defining move on this page is in it.
