# Lucas and Dawn 2's redesign: the evidence, the diagnosis, the candidates and the sets

Ian asked on 2026-10-21 for Lucas and Dawn 2 (Route 207, Fantina's split, the next story fight after Jupiter 1) to be redesigned in Roark's and Gardenia's checked stages. This page holds stages 1 and 2, the evidence and the diagnosis, which Ian checked the same day, stage 3, the candidates and three team shapes, with the shape Ian picked from them, and stage 4, the sets (the last section). The sets are written into the six trainer files on this branch for study, not for landing.

## Ian's answers (2026-10-21)

1. The shape and the diagnosis match how he would plan the fight.
2. The six files share one core; only the rival's starter changes by version.
3. Umbreon stays, consistent with Lucas and Dawn 3.
4. Lopunny moves off the lead, and the team grows to six.
5. The target is about 90 to 94 percent won.
6. No baseline reading of today's files.

So the six are a lead, Lopunny (its set as it is), Pachirisu (kept, with a fixed nature; its set may change), Umbreon at about 29, one open slot, and the rival's starter line as the ace at 30.

## Summary

**Outcome.** Today's team has never been read by the scorer. The 100 percent won of 2026-10-03 is the base ROM's four-member team, read on the Piplup version only, on goal 2's old box and simulator; Whiscash alone beat three of its four members. Today's five are the Kaizo comb's drafts of 2026-10-07. Their slots 3 and 4 are built against the player's starter, which the matchup screen's sixes mostly leave at home (in 4 or 5 of each box's top 20), and they carry almost nothing for the slow walls the player does bring: a Ground type against the two Electric members, and Rock, Steel or Fairy walls against Lopunny. On box 3, Jolteon and Monferno have no super-effective move on either Pokemon every top six takes; on box 1, neither have Glaceon and Magmar. The files also break Ian's rule of 2026-10-12 six times (missing natures, two repeated natures, one repeated item), and the Lucas and Dawn copies of one team roll different natures, so the two players meet different Speeds.

**The fight's shape, in short.** Lopunny is the fight's one real threat: the fastest Pokemon on the field against every box, with Fake Out, Quick Attack and Scrappy's Jump Kick. Pachirisu's Adaptability Spark is the answer to the Flying and Water types that would otherwise wall Lopunny or the ace. The rest is a per-starter trio (an Eeveelution, one of the Kanto elemental trio, and the starter the player's own beats), and the player's answer to it is typing: an Electric-immune Ground type, a Normal-resisting wall, and bulk (Kingler, Hariyama, Bibarel).

**What Ian checks.**

1. The shape and the diagnosis below, and whether they match how he would plan the fight.
2. Whether the three versions keep a starter-specific trio, or share one core with only the ace changing. Goal 3 reads each version on one box only (box 1 meets the Turtwig version, box 2 Scorbunny's, box 3 Piplup's), so a shared core would let all three boxes read one fight.
3. Whether the counterpart keeps an Eeveelution as part of its identity. The same player meets a different Eeveelution beside them at Veilstone (Flareon for a Turtwig player, against Glaceon here), and Lucas and Dawn 3, Ian's own six, carries Umbreon in every version and Magmortar in two of three.
4. Where Lopunny goes (Ian: better as a non-lead), what leads in front of it, and whether the team grows to six.
5. A target. Jupiter 1's is 94 percent won (a soft guide) and Gardenia reads 90; this fight sits between Jupiter 1 and Fantina, whose current team has no scorer reading.
6. Whether a baseline reading of today's three files comes first, as Gardenia's first stage did.

**Next steps, once Ian has checked this.** Stage 3, candidates from the whole Pokedex against the weaknesses below: a few hours of a session. Stage 4, sets for his pick: about an hour. A reading of the new team on goal 3's three boxes: about two to three and a half hours (Gardenia's boxes took 40 to 70 minutes each), after the Galactic readings now queued (Somnu 1, then Mars 1, Moira 1 and Jupiter 1).

## Stage 1: the evidence

### The six files and their faults

The script on Route 207 picks the file by the player's starter (`GetPlayerStarterSpecies`). Lopunny and Pachirisu are in every file; the other three change with the starter. Every member has the highest IVs (iv_scale 255) and the AI flags Basic, Evaluate Attack and Expert. Speeds are each member's own at its level; a nature in italics is not set in the file and is the one the game rolls from the trainer and species.

| Member | Level | Item | Ability | Nature (Dawn / Lucas) | Speed | Moves |
|---|---|---|---|---|---|---|
| Lopunny | 29 | Lum Berry | Scrappy | Jolly | 81 | Jump Kick, Quick Attack, Bounce, Fake Out |
| Pachirisu, Turtwig version | 28 | Oran Berry | Adaptability | *Mild / Serious* | 66 | Spark, Swift, Charm, Bite |
| Pachirisu, Scorbunny version | 28 | Oran Berry | Adaptability | *Bashful / Hardy* | 66 | as above |
| Pachirisu, Piplup version | 28 | Oran Berry | Adaptability | *Brave / Docile* | 59 / 66 | as above |

| Version (files) | Member | Level | Item | Ability | Nature | Speed | Moves |
|---|---|---|---|---|---|---|---|
| Turtwig (799 Dawn, 802 Lucas) | Glaceon | 29 | Never-Melt Ice | Snow Cloak | Modest | 51 | Icy Wind, Bite, Shadow Ball, Wish |
| | Magmar | 29 | Charcoal | Flame Body | Adamant | 67 | Fire Punch, Confuse Ray, Feint Attack, Smog |
| | Prinplup (ace) | 30 | Mystic Water | Torrent | Modest | 44 | Bubble Beam, Metal Claw, Peck, Brine |
| Scorbunny (793 Dawn, 800 Lucas) | Vaporeon | 29 | Leftovers | Water Absorb | Calm | 51 | Water Pulse, Ice Beam, Bite, Wish |
| | Electabuzz | 29 | Magnet | Static | Adamant | 74 | Thunder Punch, Low Kick, Fire Punch, Light Screen |
| | Grotle (ace) | 30 | Miracle Seed | Shell Armor | Adamant | 35 | Razor Leaf, Bite, Curse, Giga Drain |
| Piplup (794 Dawn, 801 Lucas) | Jolteon | 29 | Magnet | Volt Absorb | Timid | 97 | Thunderbolt, Double Kick, Shadow Ball, Thunder Wave |
| | Jynx | 29 | Oran Berry | Snow Cloak | *Hasty / Naughty* | 75 / 69 | Ice Punch, Confusion, Lovely Kiss, Fake Tears |
| | Monferno (ace) | 30 | Charcoal | Blaze | Naive | 68 | Flame Wheel, Mach Punch, Rock Slide, Taunt |

Faults against the standing rulings (every enemy member its own item and its own nature, with no repeats in the team; Ian, 2026-10-12):

1. Pachirisu has no nature in any of the six files.
2. Jynx has no nature (794, 801).
3. Electabuzz and Grotle are both Adamant (793, 800).
4. Glaceon and Prinplup are both Modest (799, 802).
5. Pachirisu and Jynx both hold an Oran Berry (794, 801).
6. Because two natures are rolled, Dawn's and Lucas's copies of one team differ: Dawn's Piplup-version Pachirisu is Brave (Speed 59) where Lucas's is Docile (66), and her Jynx is Hasty (75) where his is Naughty (69).

Other faults, which no ruling names but which weaken the sets:

- Moves against the nature. Grotle is Adamant with Giga Drain, Prinplup Modest with Metal Claw and Peck, Glaceon Modest and Vaporeon Calm each with Bite, Magmar Adamant with Smog, and Jynx (base Attack 50) carries Ice Punch.
- Dead abilities. Snow Cloak on Glaceon and Jynx does nothing without hail, and nothing here sets it.
- Thin items. An Oran Berry heals 10 HP, little at level 28. Never-Melt Ice powers Glaceon's one Ice move, a 55-power Icy Wind; Magnet powers one move on each of its holders.
- Two Electric types in two versions: Pachirisu with Electabuzz (Scorbunny) and Pachirisu with Jolteon (Piplup). One Ground type walls both.

### Which starter meets which team, and why

The rival's starter is the line the player's own starter beats, as in vanilla Platinum: Barry takes the starter strong against the player's, and the counterpart the one left over. `SystemVars_GetPlayerCounterpartStarter` holds the pairing, and Scorbunny takes only Chimchar's place in the briefcase, so the counterpart keeps the Chimchar line (Ian, 2026-10-07).

| Player's starter | Counterpart's files | Ace | The other two |
|---|---|---|---|
| Turtwig | 799, 802 | Prinplup | Glaceon, Magmar |
| Scorbunny | 793, 800 | Grotle | Vaporeon, Electabuzz |
| Piplup | 794, 801 | Monferno | Jolteon, Jynx |

The Eeveelution is the plain type answer to the player's starter: Ice for Grass, Water for Fire, Electric for Water. Slot 4 counters the starter only in the Turtwig version (Magmar's Fire Punch on Grotle). In the other two it covers the ace's weaknesses: Electabuzz's Thunder Punch and Fire Punch hit the Flying, Ice and Bug types that beat Grotle, and Jynx's Ice Punch hits the Flying and Ground types that beat Monferno.

The comb's note on this fight (`kaizo-comb/fantina.md`) built it as "today's four, each with a fuller set, plus Pachirisu", and its rough simulator read the files at about 99 percent won with 0.15 faints (Piplup), 100 with 0.01 (Scorbunny) and 99 with 1.1 (Turtwig). Roark's redesign showed that simulator ranks broken sets rather than difficulty.

### Where these lines appear on other trainers

Counted over `res/trainers/data/` on `oxide`, with rematches, Lucas and Dawn 2's own files and the Veilstone tag partner left out, and Lucas and Dawn 3's six files counted as one fight. The split is the map's, from the balance tools.

| Line | Fights | Written by the comb | Before Route 207 |
|---|---|---|---|
| Elekid, Electabuzz, Electivire | 11 | 8 | 1: Youngster Dallas's Elekid 15 (Route 203) |
| Magby, Magmar, Magmortar | 9 | 6 | none |
| Smoochum, Jynx | 4 | 2 | none |
| Eevee and its evolutions | 30 | 20 | 1: Somnu 1's Eevee 18, which its redesign drops |

The Galactic drafts add Electivire and Magmortar to Cyrus 1 (Celestic ruins, Byron's split, on `overseer-galactic-teams`) and Glaceon to Moira 3, and drop the Glaceon of Somnu's Lake Verity file. Neither study branch adds any of these lines before Route 207.

So the overlap Ian names is with what comes later, and it is heavy there. The Electivire line is on Ernest, Dalton, Keenan, Destiny, Henry, both Volkner fights and Cyrus 1's draft. Magmortar is on Conrad, Dalton, Keenan, Henry, both Flint fights, Terrell and four of Lucas and Dawn 3's six files. Jynx is on Savannah, Sergio and Madison in Candice's split, and the Eeveelutions are on eight trainers of Candice's split alone (five of them Glaceon, Candice's own among them).

Two fights just before this one in play order share its types, by the drafts being read next: Moira 1 (Snover, Xatu, Galarian Mr. Mime, Kadabra) is Ice and Psychic, as the Piplup version's Jynx is, and Jupiter 1 (Pelipper, Emolga, Lanturn, Tangela, Galarian Weezing, Skuntank) brings two Electric types, as two of the versions here do.

### Goal 3's three boxes

Built with `plgoal3 --box lucas_dawn_2 <seed> --screen` for seeds 1 to 3, at level 30 (the interim soft cap the scorer reads this fight at). The screen ranks sixes by matchups alone, with no simulated fights, so its sixes are a forecast of the player's answers, not the scorer's choice. Each box is 25 catches; held-back versions are left out of the table, and the one the screen used is box 3's Vikavolt, kept as a Grubbin at 30 (Bug, Speed 37), in 6 of its top 20. Speed is at level 30 as goal 3 builds the player's box (Hardy, IVs 15, no EVs); a real player's Pokemon may sit a few points either side.

| Box 1 (Turtwig version) | Types | Speed | Box 2 (Scorbunny version) | Types | Speed | Box 3 (Piplup version) | Types | Speed |
|---|---|---|---|---|---|---|---|---|
| Grotle | Grass | 31 | Raboot | Fire | 65 | Prinplup | Water | 39 |
| Whiscash | Water, Ground | 45 | Whiscash | Water, Ground | 45 | Goldeen | Water | 47 |
| Luxray | Electric, Dark | 66 | Staravia | Normal, Flying | 57 | Corvisquire | Flying | 55 |
| Staravia | Normal, Flying | 57 | Masquerain | Bug, Water | 45 | Orbeetle | Bug, Psychic | 63 |
| Bibarel | Normal, Water | 52 | Lombre | Water, Grass | 39 | Dubwool | Normal | 62 |
| Dustox | Bug, Poison | 48 | Bibarel | Normal, Water | 52 | Bibarel | Normal, Water | 52 |
| Nidorino | Poison | 48 | Orbeetle | Bug, Psychic | 63 | Nidorino | Poison | 48 |
| Pawmo | Electric, Fighting | 60 | Liepard | Dark | 79 | Machoke | Fighting | 36 |
| Corvisquire | Flying | 55 | Nidorino | Poison | 48 | Whiscash | Water, Ground | 45 |
| Vullaby | Dark, Flying | 45 | Vullaby | Dark, Flying | 45 | Vullaby | Dark, Flying | 45 |
| Golbat | Poison, Flying | 63 | Golbat | Poison, Flying | 63 | Golbat | Poison, Flying | 63 |
| Fletchinder | Fire, Flying | 59 | Ponyta | Fire | 63 | Hariyama | Fighting | 39 |
| Probopass | Rock, Steel | 33 | Donphan | Ground | 39 | Onix | Rock, Ground | 51 |
| Goldeen | Water | 47 | Goldeen | Water | 47 | Roselia | Grass, Poison | 48 |
| Quagsire | Water, Ground | 30 | Naclstack | Rock | 30 | Graveler | Rock, Ground | 36 |
| Kingler | Water | 54 | Finneon | Water | 49 | Kingler | Water | 54 |
| Tentacruel | Water, Poison | 69 | Tentacruel | Water, Poison | 69 | Tentacruel | Water, Poison | 69 |
| Cherrim | Grass | 60 | Combee | Bug, Flying | 51 | Pachirisu | Electric | 66 |
| Sharpedo | Water, Dark | 66 | Dolliv | Grass, Normal | 29 | Pawmo | Electric, Fighting | 60 |
| Plusle | Electric | 42 | Tsareena | Grass, Fighting | 64 | Combee | Bug, Flying | 51 |
| Leavanny | Bug, Grass | 64 | Leavanny | Bug, Grass | 64 | Breloom | Grass, Fighting | 51 |
| Lombre | Water, Grass | 39 | Brionne | Water | 39 | Lombre | Water, Grass | 39 |
| Alolan Ninetales | Ice, Fairy | 69 | Alolan Ninetales | Ice, Fairy | 69 | Mothim | Bug, Flying | 55 |
| Snover | Grass, Ice | 33 | Bronzor | Steel, Psychic | 23 | Carbink | Rock, Fairy | 39 |
| Combee | Bug, Flying | 51 | Nuzleaf | Grass, Dark | 45 | Vikavolt | Bug, Electric | 35 |

How often each catch is in the screen's top 20 sixes against today's team:

| Box | In all 20 | In most | Often | The player's starter |
|---|---|---|---|---|
| 1 (Turtwig) | Probopass, Kingler | Quagsire 17 | Golbat 8, Cherrim 8, Alolan Ninetales 6, Luxray 6, Bibarel 6 | Grotle 4 |
| 2 (Scorbunny) | Donphan, Bibarel | Whiscash 13, Tsareena 12 | Golbat 9, Leavanny 8 | Raboot 5 |
| 3 (Piplup) | Hariyama, Carbink | Whiscash 13, Breloom 13 | Goldeen 7, held Grubbin's Vikavolt 6, Machoke 6 | Prinplup 5 |

The likely core answers, by box: a Ground type that ignores the Electric members (Quagsire, Donphan, Whiscash), a wall that resists Lopunny's Normal moves (Probopass, Carbink), and a bulky attacker with a type edge on the starter-specific trio (Kingler's Water on Magmar, Bibarel's Unaware against Grotle's Curse, Hariyama's Thick Fat against Fire and Ice). Which of each box's always-taken pair today's members can hit super-effectively:

| Box | Always taken | Members with a super-effective move on one of them |
|---|---|---|
| 1 | Probopass, Kingler | Lopunny (Jump Kick, four times, on Probopass), Prinplup (Water on Probopass), Pachirisu (Spark on Kingler). Glaceon and Magmar: none |
| 2 | Donphan, Bibarel | Every member: Vaporeon and Grotle on Donphan; Lopunny, Pachirisu, Electabuzz and Grotle on Bibarel |
| 3 | Hariyama, Carbink | Lopunny (Bounce on Hariyama), Jynx (Confusion on Hariyama). Pachirisu, Jolteon and Monferno: none, and nothing at all hits Carbink super-effectively |

### The old reading, and the neighbours

The difficulty store's reading of this fight (goal 2, 2026-10-03: 100 percent won, no faints, 75 fights and 25 very unlucky) is of `TRAINER_DUMMY_794` as it was before step 12: Lopunny 29 (Jump Kick, Thunder Wave, Quick Attack, Mirror Coat), Jolteon 29 (Thunder Wave, Magnet Rise, Shock Wave, Fake Tears), Jynx 30 (Icy Wind, Reflect, Lovely Kiss, Copycat) and Monferno 30 (Mach Punch, Flame Wheel, Fake Out, Torment). Its six were Prinplup, Dubwool, Vulpix, Whiscash, Kingler and Tsareena. In the traced fight Lopunny spent its first two turns on Mirror Coat against Dubwool, Whiscash finished it, and then Whiscash beat Jynx, Monferno and Jolteon alone: Jolteon's one attack was Electric, so against Whiscash it used Fake Tears and Magnet Rise until it fell. That team read trivial because three of its four had passive sets and the only Electric attack met a Ground type. The reading was made on goal 2's box, before the comb's teams and every simulator fix since.

| Fight | Reading | Won | Faints |
|---|---|---|---|
| Gardenia, locked team | goal 3, 2026-10-21 | 89% | 2.58 |
| Jupiter 1 | target (Ian, 2026-10-14; a soft guide) | 94% | |
| Lucas and Dawn 2, the base ROM's team | goal 2, 2026-10-03 | 100% | 0.00 |
| Fantina, the team before the comb | goal 2, 2026-10-03 | 91% | 3.04 |

Fantina's current team (the comb's, since 2026-10-07) and Jupiter 1's draft have no scorer reading yet. The comb's rough simulator put its Fantina a step harder than the one read above.

### Speed tiers

Each member's Speed against the boxes' fastest catches and the core answers (box Speeds as above):

| Speed | Rival members | The player's catches |
|---|---|---|
| 97 | Jolteon | |
| 81 | Lopunny | |
| 79 | | Liepard (box 2) |
| 74 to 75 | Electabuzz, Dawn's Jynx | |
| 69 | Lucas's Jynx | Alolan Ninetales (boxes 1, 2), Tentacruel (all) |
| 66 to 68 | Monferno 68, Magmar 67, Pachirisu 66 | Luxray, Sharpedo, Pachirisu 66, Raboot 65 |
| 59 to 64 | Dawn's Piplup-version Pachirisu 59 | Leavanny, Tsareena 64; Golbat, Orbeetle, Ponyta 63; Dubwool 62; Pawmo, Cherrim 60; Fletchinder 59 |
| 50 to 57 | Glaceon, Vaporeon 51 | Staravia 57; Corvisquire, Mothim 55; Kingler 54; Bibarel 52; Onix, Breloom 51 |
| 44 or under | Prinplup 44, Grotle 35 | Whiscash 45; Hariyama, Donphan, Carbink 39; Graveler 36; Probopass 33; Quagsire 30 |

Lopunny outspeeds every catch in all three boxes, and Jolteon does by far. Every rival member but the two aces and the two bulky Eeveelutions also outspeeds every core answer. Three tiers sit on a knife edge, the kind that swung Gardenia:

- Glaceon and Vaporeon at 51 sit one to three points under Bibarel (52) and Kingler (54), two of the always-taken answers.
- Dawn's Piplup-version Pachirisu, rolled Brave, sits at 59, under Golbat, Orbeetle, Dubwool and Pawmo; with a neutral nature it is at 66, over all of them.
- Magmar (67) and Monferno (68) sit just under Alolan Ninetales and Tentacruel (69).

## Stage 2: the diagnosis

### The fight's shape

Written as `boss-shapes.md` frames the others; how sure: a forecast from the matchup screen and the sets, not from a reading, since today's team has none.

**Identity.** The counterpart is a Pokemon Trainer a step behind the player, with Lopunny and Pachirisu as its constant pair and its starter as the ace. Lopunny is the threat; the rest of the team answers the player's starter.

**The boss's core:**

- Lopunny: Scrappy, Jump Kick, Fake Out and Quick Attack, at 81 Speed, the fastest thing on the field against every box.
- Pachirisu's Adaptability Spark, the team's answer to the Flying and Water types, with Charm against physical walls.
- The starter-specific trio's type edge on the player's starter.

**The player's core counterpieces** (from the screen's sixes, to be confirmed by a reading):

- An Electric-immune Ground type: Quagsire (box 1), Donphan (box 2), Whiscash (box 3, and in many sixes on box 2).
- A wall that resists Normal: Probopass (box 1), Carbink (box 3).
- Bulk with a type edge on the trio: Kingler (box 1), Bibarel (box 2), Hariyama (box 3).
- The player's starter is not one of them: the trio is built to beat it, so the player leaves it out.

**Material for this fight:** Lopunny's and Pachirisu's sets; the Ground types' availability before Route 207 and their immunity to Electric; Probopass's, Carbink's, Kingler's, Bibarel's and Hariyama's availability and moves; and the Speed of any member near the tiers named above.

### What fails under baiting

Ian plans a boss by baiting matchups in the order he wants. Against today's team:

1. **The lead is known.** Lopunny leads every version, so the player leads its check, and Lopunny's Fake Out and Lum Berry are spent on a Pokemon chosen to absorb them. Golbat resists Jump Kick four times over; Carbink resists its Normal moves and shrugs off Jump Kick; Hariyama trades Fighting hits with it and has Fake Out of its own. Bounce's charging turn gives the player a free switch.
2. **The replacement order is predictable.** After a faint, the trainer AI sends the member whose own types hit the player's active Pokemon hardest, if it has a super-effective move on it. With a Ground type out, no Electric member is ever chosen, so Pachirisu, Electabuzz and Jolteon come in last, into whatever the player has kept for them. The starter-countering member comes in only when the player's starter is out, which the player avoids by leaving it home.
3. **The starter-specific trio has nothing for the answers the player brings.** On box 3, Pachirisu, Jolteon and Monferno have no super-effective move on Hariyama or Carbink, and no member at all has one on Carbink. On box 1, Glaceon and Magmar have none on Probopass, Kingler or Quagsire. Only the Scorbunny version's members each hit one of the always-taken pair hard.
4. **Two Electric members in two versions** make one Ground type worth two answers.

### Dead abilities, thin items, lost identity

- Snow Cloak (Glaceon, Jynx) never works.
- Two Oran Berries in the Piplup version, and an Oran Berry in every version, heal too little to matter at this level.
- Never-Melt Ice and both Magnets each boost a single move; Glaceon's boosted move is a 55-power Icy Wind.
- The Eeveelution changes with the starter and does not match the counterpart's other fights. The same Turtwig player meets Glaceon here and Flareon at Veilstone. Ian's own Lucas and Dawn 3 carries Umbreon in every version and Magmortar in two of three, beside Nidoqueen and Lickilicky, with Slowbro, Tangrowth or both. Nothing on today's team builds toward that six except one version's Magmar.
- Electabuzz, Jynx and Magmar are common later (the counts above). None appears before Route 207 apart from Dallas's Elekid, but each is a stock Kanto pick that a Candice-split or Volkner-split trainer also carries, and the Piplup version's Jynx repeats Moira 1's Ice and Psychic one fight later in play order.

### Repeated items and natures

Six faults, listed in stage 1: Pachirisu's nature (all files), Jynx's nature (two files), Adamant twice (Scorbunny version), Modest twice (Turtwig version), Oran Berry twice (Piplup version), and Dawn's and Lucas's copies rolling different natures. Any redesign sets every nature in the file.

### Slot 3, the Eeveelutions

Ian's "a little hamfisted" is what the sets show. Each Eeveelution is the plain type counter to the player's starter, and the player knows which version is coming because it follows their own starter. The sets work against their natures (Bite on Modest Glaceon and Calm Vaporeon), Glaceon's ability does nothing, and Wish on both Glaceon and Vaporeon is a support move on members with no partner set to use it. Jolteon's set is the sound one, but it doubles Pachirisu's Electric typing.

### Slot 4, the elemental trio

Electabuzz has the strongest set of the three (Magnet Thunder Punch and Fire Punch at 95 power, Low Kick, a one-PP Light Screen), but it is the second Electric member of its version. Jynx is a special attacker with Ice Punch, a dead ability and no nature. Magmar is Adamant with Smog. In two versions slot 4 covers the ace's weaknesses rather than adding a threat of its own.

### The ace

The ace is the starter the player's own beats, by design and by the script. Its sets also work against their natures (Adamant Grotle with Giga Drain, Modest Prinplup with Metal Claw and Peck). Its level, 30, is three under Fantina's cap of 33, which fits the mini-boss rule (an officer's or mini-boss's ace sits two to four under the cap; Lucas and Dawn 3's ace is three under its cap of 71). The scorer reads this fight with the player's box at 30, the ace's level. A sixth member fits the rules at 28 to 30.

### What a non-lead Lopunny needs

As a non-lead, Lopunny comes in after a faint, so the player cannot lead its check, and its Fake Out fires on every entry (the simulator and the AI both treat it as usable on each first turn out, with priority 3). Its 81 Speed and Quick Attack then pick off whatever the faint left weakened. To make that work, the Pokemon in front of it needs to do three things:

1. Chip the player's six, so Fake Out and Quick Attack reach knockout range: entry hazards or residual damage, which no member sets today.
2. Weaken Lopunny's checks before it arrives: the Flying types (Golbat resists Jump Kick four times over; Staravia, Corvisquire, Vullaby, Mothim and Combee), Orbeetle, and Carbink. Pachirisu's Spark is the natural answer to the Flying ones.
3. Hold its own against the player's Ground lead, which walls Pachirisu today: Pachirisu has only Bite and Swift for it.

The replacement rule also decides when Lopunny arrives: the AI sends it when its Fighting or Normal moves hit the player's active Pokemon super-effectively (a Normal, Rock, Steel, Ice or Dark type left in). A redesign should check, by the AI's exact odds, that Lopunny enters where Ian wants it to and is not baited into a Flying switch-in.

### What Lopunny and Pachirisu do well, since they stay

Lopunny is the best set on the team. Scrappy lets Jump Kick and its Normal moves hit Ghosts, so no Ghost walls it. Jump Kick at 100 power hits the Normal, Rock, Steel and Ice walls the player brings. Fake Out and Quick Attack give it two priority moves to break a Sash or finish a weakened Pokemon. Bounce hits the Fighting types that would otherwise trade with it (Hariyama, Breloom, Machoke, Tsareena, Pawmo). Jolly puts it over every catch, and the Lum Berry clears the first status the player aims at it (Probopass's Thunder Wave, Bibarel's Yawn, Bronzor's Hypnosis).

Pachirisu's Spark under Adaptability is a 65-power move with double the usual same-type bonus. It hits the Flying types that wall Lopunny and the Water types (Kingler, Bibarel, Goldeen, Tentacruel, Masquerain, the player's Prinplup) that answer the aces. Charm, at three PP, takes two stages from a physical wall's Attack (Kingler, Hariyama, Donphan, Breloom). Bite reaches Orbeetle and Bronzor, and Swift never misses. Its faults are a missing nature, which in Dawn's Piplup file drops it under Golbat's Speed, a weak berry, and nothing for a Ground type.

## Stage 3: the candidates

Drawn from the whole Pokedex, any stage, with no filter by player access, evolution level or stats total. Every tool named below is in the species' trainer palette at 29 (level-up moves to 29, egg moves, and TM and tutor moves, the pre-TM-pass ones included), and every borrowed attack is at 90 power or under. Speeds are at 29 with top IVs, for a neutral nature and for a Speed-raising one. Set aside: the Kanto elemental trio and the Eeveelutions other than Umbreon; Ice and Psychic Pokemon after Moira 1 (Slowbro, though Lucas and Dawn 3 has it, and Bronzong, Cloyster and Froslass); Tangela, Jupiter's line, which Jupiter 1 fields one fight earlier; Lileep and Cradily (Roark's core), the Roselia line (Gardenia's), Clefable (Tyche's), Gligar (on two Route 207 trainers already) and Lickitung (a second Normal type beside Lopunny with nothing for Carbink). Before Route 207 the candidates' lines appear only as two Pinecos, a Ludicolo and a Mawile in Gardenia's split, a Shellos in Roark's and a Nidorina in the Eterna building.

The speed lines that matter, from the boxes: Liepard 79; Alolan Ninetales and Tentacruel 69; Golbat, Orbeetle and Ponyta 63; Kingler 54; Bibarel 52; Whiscash 45; Hariyama, Donphan and Carbink 39. Taunt is on Bibarel (52, every box), Corvisquire (55) and Raboot (65), and Rapid Spin on box 2's Donphan and Tsareena, so a slow hazard lead can be stopped or undone on box 2.

### The shared core

| Member | Level | Role | Speed | What stage 4 must settle |
|---|---|---|---|---|
| Lopunny | 29 | The threat, off the lead: Fake Out on every entry, Quick Attack to finish, Jump Kick and Bounce | 81 (Jolly) | Nothing: its set stays |
| Pachirisu | 28 | Spark on the Flying types that wall Lopunny and the Water types that answer the aces; Charm on a physical wall | 66 neutral, 72 with a Speed-raising nature | A fixed nature: a Speed-raising one puts it over the 69 tier. Seed Bomb is in its palette and would give it a hit on the Ground lead that walls it |
| Umbreon | 29 | The bulky Dark pivot of Lucas and Dawn 3: Wish, Yawn, Toxic, Taunt, Reflect and Light Screen are in its palette | 51 neutral, 56 raised | Its Speed: at 51 it sits under Bibarel (52) and Kingler (54); raised, it is over both. Foul Play is not in its palette at 29 |
| Ace (the rival's starter) | 30 | Changes by version | Grotle 35, Prinplup 44, Monferno 62 (68 with Naive) | Yes, its sets need work (below) |

The aces' sets need work. Each set fights its nature today (an Adamant Grotle with Giga Drain, a Modest Prinplup with Metal Claw and Peck), and with a shared core each ace should fill the gap the core leaves on the box that meets it. Grotle meets box 2, where a physical Grass move (Seed Bomb is in its palette) hits both Donphan and Bibarel. Prinplup meets box 1, where its special Water moves hit Probopass and Quagsire's Water Absorb walls them. Monferno meets box 3, where nothing it carries today hits Hariyama or Carbink super-effectively; Dig (Ground, on Carbink) and Aerial Ace (on Hariyama) are in its palette. Monferno at 62 sits one point under Golbat, and its Naive nature puts it at 68, just over.

### Lead candidates

The lead's three jobs, from the diagnosis: wear the player's six down, weaken Lopunny's checks (Carbink, Probopass and the Flying types), and hold up against the Ground lead that walls Pachirisu.

| Candidate | Typing and ability | Tools at 29 | Hits hard | Against the Ground lead | Speed | Weak to |
|---|---|---|---|---|---|---|
| Forretress | Bug and Steel, Heatproof | Stealth Rock, Spikes, Toxic Spikes, Rapid Spin, Reflect, Light Screen, Thunder Wave | Carbink (Steel, four times); Quagsire and Whiscash (Giga Drain, four times); Flying (Rock Slide) | Holds: Water and Ground land neutral on 140 Defense | 37, 40 | Fire (twice, through Heatproof); Taunt |
| Gastrodon | Water and Ground, Dry Skin | Stealth Rock, Yawn, Toxic | Probopass (Earth Power, four times); Carbink, Donphan and the Fire types (Surf) | Holds fully: Dry Skin heals it off their Water moves | 36, 39 | Grass (four times) |
| Araquanid | Water and Bug, Water Bubble (Water Absorb hidden) | Sticky Web, Reflect, Soak, Aqua Ring | Carbink, Probopass and Donphan (Water, doubled by Water Bubble); Quagsire and Whiscash (Giga Drain) | Holds: resists Water and Ground | 38, 41 | Flying, Rock and Electric: Lopunny's checks hit it hard |
| Skarmory | Steel and Flying, Filter | Stealth Rock, Spikes, Roar, Whirlwind, Roost, Taunt | Carbink (Steel); Flying (Rock Slide) | Holds (immune to Ground) but cannot hurt them | 54, 59: over Bibarel's Taunt | Electric, Fire |
| Klefki | Steel and Fairy, Prankster | Spikes, Reflect, Light Screen and Thunder Wave, all at priority | Carbink (Steel); Hariyama (Fairy) | Fails: Ground hits it twice | 57, 62 | Ground, Fire |
| Ferroseed, with Eviolite | Grass and Steel, Iron Barbs | Stealth Rock, Thunder Wave, Gyro Ball | Carbink (Steel); Quagsire and Whiscash (Grass) | Holds: resists Water | 19 | Fire (four times), Fighting (Hariyama) |

### Open-slot candidates

The open slot answers what the player brings (the Ground types, Kingler, Hariyama, Carbink, Bibarel, Donphan, Probopass) and gives the core the coverage it lacks: Grass in two versions, anything for Carbink, and more for Hariyama than Lopunny's Bounce.

| Candidate | Typing and ability | What it answers | Speed | Weak to |
|---|---|---|---|---|
| Gastrodon | Water and Ground, Dry Skin | Every Water attack the boxes' cores carry (Quagsire, Whiscash, Kingler, Bibarel) heals it; Earth Power on Probopass and Carbink; Surf on the Fire types; immune to Electric | 36, 39 | Grass |
| Mawile | Steel and Fairy, Intimidate (both regular slots) | Intimidate on entry cuts the Attack of Kingler, Hariyama, Donphan, Bibarel and Golbat, every physical answer the screens always take; Iron Head on Carbink (four times); Play Rough on Hariyama; Sucker Punch; resists Grass and Flying | 42, 46 | Ground, Fire |
| Nidoqueen | Poison and Ground, Sheer Force (hidden) | Lucas and Dawn 3's first member, so the pair's later team grows from here; Toxic Spikes, Stealth Rock and Roar; Earth Power on Probopass and Carbink; resists Fighting, Rock and Fairy; immune to Electric | 58, 63 (63 ties Golbat) | Water, Ground, Ice, Psychic |
| Ludicolo | Water and Grass, Own Tempo or Swift Swim | Grass on Quagsire and Whiscash (four times), Kingler, Bibarel, Donphan and Carbink; resists Water and Ground | 54, 59 | Flying and Poison (Golbat), Bug |

### Three team shapes

Each shape is a lead and an open slot around the shared core. "Bait" is how a planning player would play around the member.

**Shape 1, hazards and a sponge (recommended).**

| Member | Role, and why it beats what the player brings | How a planning player baits it | Speed against the boxes | Likely weak point |
|---|---|---|---|---|
| Forretress (lead) | Stealth Rock and Spikes chip every switch, a quarter to a half of a Flying type's HP on each entry; Steel takes Carbink, Giga Drain the Water and Ground leads, Rock Slide the Flying types; takes the Ground lead's hits on 140 Defense | Lead a Fire type (Raboot, the Scorbunny player's own starter, Ponyta, Fletchinder), Taunt it first, or spin the hazards (Donphan on box 2) | 37, under the 39 tier (Hariyama, Donphan, Carbink); 40 with a Speed nature, over it | Fire, and Taunt from Bibarel, Corvisquire or Raboot, all faster |
| Gastrodon (open slot) | Dry Skin turns the Water attacks most of the player's answers carry into healing; Earth Power and Surf on Probopass, Carbink, Donphan and the Fire types that beat Forretress; Yawn forces switches over the hazards | Bring Grass (Tsareena, Breloom, Leavanny, Cherrim; Donphan's Trailblaze; the Turtwig player's Grotle) | 36 or 39: moves before only Probopass and Quagsire | Grass, which Forretress resists four times over |

The pair covers each other: Forretress takes Grass, Gastrodon takes Fire and Water. The open gap is Hariyama, which only Lopunny's Bounce and Pachirisu's Charm answer.

**Shape 2, a sponge and Intimidate.**

| Member | Role, and why it beats what the player brings | How a planning player baits it | Speed against the boxes | Likely weak point |
|---|---|---|---|---|
| Gastrodon (lead) | Stealth Rock and Yawn wear the six down; Dry Skin holds the Ground lead completely; Earth Power and Surf on Probopass and Carbink; Rock Tomb on the Flying types | Lead Grass (Tsareena is in 12 of box 2's top 20, Breloom in 13 of box 3's), or Taunt it | 36 or 39 | Grass; a weaker hand against the Flying types than Forretress's |
| Mawile (open slot) | Intimidate on every physical answer the screens take, Iron Head on Carbink, Play Rough on Hariyama, Sucker Punch to finish; resists Grass and Flying, Gastrodon's weak points | Ground moves (the Ground leads, Donphan) and Fire | 42, over the 39 tier; 46 with a Speed nature, over Whiscash (45) | Ground, which Gastrodon takes |

This shape answers Hariyama and Kingler best, through Intimidate, and its lead is the surest against the Ground lead. Its lead does less of the second job: nothing on it hits a Flying type super-effectively but Rock Tomb.

**Shape 3, the web and the step to Lucas and Dawn 3.**

| Member | Role, and why it beats what the player brings | How a planning player baits it | Speed against the boxes | Likely weak point |
|---|---|---|---|---|
| Araquanid (lead) | Sticky Web takes a Speed stage from every switch-in: Kingler drops from 54 to 36, Bibarel from 52 to 35 and Golbat from 63 to 42, so Umbreon, Pachirisu, the ace and Nidoqueen all move first; Water Bubble doubles its Water moves on Carbink, Probopass and Donphan; resists the Ground lead, Kingler and Hariyama | Lead a Flying type (Golbat, Staravia, Corvisquire) or a Rock move (Carbink, Probopass, Bibarel's Smack Down) | 38 or 41, around the 39 tier | It loses to the Pokemon it should weaken, and the web does no damage |
| Nidoqueen (open slot) | Lucas and Dawn 3's first member; Toxic Spikes and Roar drag the six over the web; Earth Power on Probopass and Carbink; resists Hariyama's Fighting and the Rock moves that hit Araquanid | Water from any Ground lead, Kingler or Bibarel; Ice from Donphan and Whiscash | 58, over Kingler and Bibarel; 63 ties Golbat | Water, which Araquanid takes |

This shape reads most as an earlier step of the pair's later team, and the web is the strongest speed control of the three. Its lead fails the second job: Lopunny's checks are the Pokemon that beat it.

### Recommendation

Shape 1. Forretress is the only lead that does all three jobs at once: hazards for the chip a non-lead Lopunny needs, Steel for Carbink and Rock for the Flying types, and the bulk to stand in front of the Ground lead and hit it back four times over. Gastrodon covers Forretress's one real weakness, Fire, including the Scorbunny player's own starter, and turns the Water attacks of the Ground leads, Kingler and Bibarel into healing. Its known gaps are Hariyama, and the Taunt and Rapid Spin users of box 2; stage 4 can close the first with the ace's and Pachirisu's sets. If Ian wants the link to Lucas and Dawn 3 more than the Water and Fire cover, Nidoqueen can take Gastrodon's place behind Forretress.

The levels fit the mini-boss rule in every shape: the ace at 30, three under Fantina's cap of 33, and the rest at 28 to 29. Forretress at 29 sits two levels under Pineco's evolution at 31 and Gastrodon one under Shellos's at 30, within Ian's "not egregiously early".

### Ian's shape (2026-10-21)

Ian built his own shape from these candidates, with no Forretress: Umbreon leads; Scyther, with Pursuit and Flying moves to punish Fighting and Bug leads; then Lopunny with its set unchanged, Pachirisu, Gastrodon in the open slot, and the rival's starter as the ace by version. His reasons: Scyther is immune to the Ground moves aimed at Pachirisu and at two of the three starters, so it switches in on them and adds power; and with Scyther's Flying moves on the team, a Fighting type no longer baits out Lopunny for its Bounce.

## Ian's last answers (2026-10-22)

Ian approved the stage 4 sets with Seed Bomb on Pachirisu. On the AI flags, the probe showed Setup First Turn and Harassment doubling Umbreon's Yawn but halving its Toxic, whose effect is on neither flag's list, and moving Pachirisu from Seed Bomb to Charm; Ian kept the flags off and swapped Umbreon's Toxic for Confuse Ray, which Umbreon learns at 29, and called the fight good. No reading was run: the cheap checks are the default for every fight since 2026-10-22 (the standing rulings).

## Stage 4: the sets

Every move is in its species' trainer palette at its level (the Kaizo study's checker over this branch, with the pre-TM-pass TM lists), and every borrowed attack is at 90 power or under. No item or nature repeats within a version. Dawn's and Lucas's files of a version are identical but for the trainer's name and class and the Pokemon's genders, as before, so both players meet the same Speeds. All IVs are the highest (iv_scale 255). Speeds are at each member's level; damage figures are the scorer's calculator against goal 3's box Pokemon at 30, as a share of the defender's HP, lowest roll to highest.

### The six

| Slot | Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|---|
| Lead | Umbreon | 29 | Inner Focus (hidden) | Light Clay | Timid | Yawn, Toxic, Reflect, Payback | 56 |
| 2 | Scyther | 29 | Technician | Eviolite | Adamant | Wing Attack, Pursuit, Steel Wing, Brick Break | 74 |
| 3 | Lopunny | 29 | Scrappy | Lum Berry | Jolly | Jump Kick, Quick Attack, Bounce, Fake Out | 81 |
| 4 | Pachirisu | 28 | Adaptability | Sitrus Berry | Hasty | Spark, Seed Bomb, Charm, Bite | 72 |
| 5 | Gastrodon | 29 | Dry Skin | Leftovers | Modest | Earth Power, Brine, Ice Beam, Stealth Rock | 36 |
| Ace, Turtwig version (799, 802) | Prinplup | 30 | Torrent | Mystic Water | Mild | Brine, Ice Beam, Grass Knot, Yawn | 44 |
| Ace, Scorbunny version (793, 800) | Grotle | 30 | Shell Armor | Miracle Seed | Brave | Seed Bomb, Rock Blast, Bulldoze, Curse | 31 |
| Ace, Piplup version (794, 801) | Monferno | 30 | Blaze | Charcoal | Naive | Blaze Kick, Mach Punch, Zen Headbutt, Rock Slide | 68 |

Against the boxes' speed lines (Liepard 79; Alolan Ninetales and Tentacruel 69; Golbat, Orbeetle and Ponyta 63; Kingler 54; Bibarel 52; Whiscash 45; Hariyama, Donphan and Carbink 39): Lopunny and Scyther outspeed every catch but Liepard, which only Lopunny beats. Pachirisu sits over the 69 tier, Monferno over Golbat and under the 69 tier, and Umbreon over Kingler and Bibarel. Prinplup sits one point under Whiscash, Gastrodon three under the 39 tier, and Grotle moves before only Quagsire (30).

### Each member, and its bait test

**Umbreon, the lead.** Its job is to wear the six down and cover the members behind it. Toxic and Yawn chip and force switches, and Reflect, eight turns with Light Clay, halves the physical hits of every answer the screens always take (Kingler, Hariyama, Donphan, Bibarel, Golbat) while Scyther, Lopunny and the ace come in. Inner Focus ignores the Fake Out the player's Hariyama, Liepard or Lombre would open with. Timid puts it at 56, over Bibarel (52) and Kingler (54), so its first status move lands before Bibarel's Taunt. Payback is there so a Taunt does not leave it with nothing; it does little (about a tenth of Hariyama's HP).
*Bait test:* the player leads a Fighting type (Hariyama's Arm Thrust takes 52 to 70 percent unscreened; Breloom's Mach Punch 47 to 54). Umbreon flinches to nothing, sets Reflect or Yawn, and when it falls to the Fighting type the replacement rule sends Scyther, whose Flying type hits Fighting twice, rather than Lopunny.

**Scyther.** Technician raises every move of 60 power or under by half: Wing Attack becomes 90 with the same-type bonus on top, more than X-Scissor's 80, and Pursuit 60 before it doubles on a switching foe. Wing Attack takes Hariyama 88 to 103 percent, knocks out Breloom and Tsareena, and takes Golbat 57 to 67 percent. Steel Wing is there for Carbink (76 to 92 percent) and Alolan Ninetales (a knockout). Brick Break is there for the Rock Blast users (Probopass 56 to 66 percent, Onix 36 to 44, Graveler 43 to 53) and Bibarel (62 to 75). Eviolite applies, since Scyther still evolves.
*The Rock weakness:* every one of the screen's top 20 sixes on every box carries a Rock move: Probopass's Rock Blast on box 1, Bibarel's Smack Down and Donphan's Rollout on box 2, Carbink's Rock Tomb and Smack Down on box 3. No catch has Stealth Rock. A Rock Blast from Probopass, Onix or Graveler takes 84 to 108 of Scyther's 88 HP; Rock Tomb, Smack Down and Ancient Power take 41 to 59 percent, Donphan's first Rollout 32 to 41. Scyther moves first against all of them (74 against 33 to 52), and the replacement rule never sends it into Probopass, Onix or Graveler, where it has no super-effective move. The risk that remains is the AI's immunity switch: Probopass's Bulldoze can draw Scyther in, and the Rock Blast that follows knocks it out.
*Bait test:* the player holds a Rock Blast user back and brings it in on Scyther. Scyther Brick Breaks it first, but needs two hits to Probopass's one.

**Lopunny.** Unchanged. With Scyther behind Umbreon, a Fighting type no longer draws it out after a faint, so it arrives on the Normal, Rock, Steel, Ice and Dark types its Jump Kick hits, with Fake Out on every entry.
*Bait test:* the player keeps Golbat (four times resistant to Jump Kick) or Carbink ready. Pachirisu's Spark answers Golbat (67 to 81 percent), Scyther's Steel Wing answers Carbink.

**Pachirisu.** Swift becomes Seed Bomb, the Oran Berry a Sitrus Berry, and its nature is fixed at Hasty (72, over the 69 tier). Scyther now takes the Ground moves aimed at Pachirisu only when Pachirisu has nothing super-effective on the attacker, which is how the AI's switch rule reads it; with Seed Bomb, Pachirisu stays in and answers the Ground lead itself, which was the diagnosis's main fault in its old set. Seed Bomb takes Quagsire 60 to 71 percent and Whiscash 62 to 76; Donphan, with its Defense of 130, only 22 to 26.
*Bait test:* the player sends Quagsire into it (Mud Bomb takes 45 to 55 percent). Pachirisu Seed Bombs it, and Spark still answers the Flying types and Kingler (48 to 58 percent).

**Gastrodon.** Dry Skin heals it off the Water attacks of the Ground leads, Kingler and Bibarel, and the AI's absorb rule brings it in on a Water hit one time in two. Earth Power takes Probopass 84 to 98 percent and Carbink 65 to 76; Brine finishes a weakened foe; Ice Beam answers the Grass types and the Flying ones; Stealth Rock is the team's one hazard, which the AI picked 91 to 112 times in each probe of 150 fights.
*Bait test:* the player brings Grass (box 2's Tsareena takes 54 to 64 percent with Magical Leaf; Breloom, Leavanny, Cherrim, the Turtwig player's Grotle). Ice Beam hits back 51 to 62 percent on Tsareena, but Grass stays its weak point.

**Prinplup, the Turtwig version's ace, against box 1.** Modest's old physical moves go. Grass Knot answers the two Water walls that blank its Water moves: Quagsire 82 to 97 percent, Kingler 58 to 70. Ice Beam takes Golbat 54 to 65 and the player's Grotle. Brine is its Water hit, and doubles on a foe under half.
*Bait test:* the player sends Probopass in; Brine takes only 28 to 36 percent, so Gastrodon's Earth Power and Scyther's Brick Break are the team's answer there.

**Grotle, the Scorbunny version's ace, against box 2.** A physical set for its nature: Seed Bomb knocks out Bibarel and takes Donphan 59 to 71 percent; Rock Blast covers its own weak points, taking the player's Raboot 80 to 94 percent and Golbat 67 to 81; Bulldoze and Curse fit its low Speed.
*Bait test:* the player leads Raboot or Golbat into it. Rock Blast hits back hard, but Grotle moves last, so it takes the first hit.

**Monferno, the Piplup version's ace, against box 3.** Zen Headbutt takes Hariyama 42 to 49 percent and Machoke 43 to 51; Blaze Kick knocks out Breloom; Mach Punch is priority; Rock Slide covers Golbat and the Bug types. It has nothing for Carbink (Mach Punch 12 to 16 percent) or the Water types.
*Bait test:* the player's own Prinplup, Whiscash or Goldeen. Monferno has no answer, and Carbink walls it; Scyther's Steel Wing and Gastrodon's Earth Power carry Carbink for this version.

### The five-minute check

The scorer builds each version (`tr:793`, `tr:794`, `tr:799`) with every species, ability, item and move resolved, Light Clay and Eviolite included. The legality checker passes all six files; its one note is Gastrodon at 29, one level under Shellos's evolution at 30.

The AI-picks probe ran once per version against its greedy middle-split six, and once more against a six built from each version's own box answers (box 1's Probopass, Kingler, Quagsire, Golbat, Cherrim and Alolan Ninetales against the Turtwig version, and so on), 150 rough fights each. Its win and faint numbers mean nothing. Every move on every member was picked in at least one run.

| Member | Moves, by how often the AI picked them (box-answers probe for the version that meets them) | Note |
|---|---|---|
| Umbreon | Payback 141 to 390, Yawn 105 to 237, Reflect 136 to 144, Toxic 30 to 78 | Payback is its most picked move though it hits for little, and Toxic its least |
| Scyther | Wing Attack 359 to 601, Steel Wing 14 to 184, Brick Break 33 to 126, Pursuit 15 to 67 | Steel Wing comes alive against box 3's Carbink; Hariyama's Knock Off took its Eviolite 25 times there |
| Lopunny | Bounce 35 to 152, Jump Kick 25 to 60, Quick Attack 15 to 65, Fake Out 11 to 33 | Bounce is its most picked move in every run |
| Pachirisu | Spark 170 to 345, Seed Bomb 58 to 208, Charm 33 to 67, Bite 17 to 34 | |
| Gastrodon | Earth Power 184 to 249, Brine 94 to 168, Ice Beam 104 to 151, Stealth Rock 91 to 112 | |
| Prinplup | Brine 113, Grass Knot 105, Yawn 97, Ice Beam 48 | Grass Knot was picked 6 to 25 times against the middle-split six, which has no Quagsire or Kingler |
| Grotle | Seed Bomb 121, Bulldoze 55, Rock Blast 54, Curse 54 | |
| Monferno | Zen Headbutt 41, Blaze Kick 27, Mach Punch 20, Rock Slide 0 | Rock Slide went unpicked against box 3's answers, which have no Flying or Bug type; against the middle-split six it was picked 29 to 36 times |
