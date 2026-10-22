# Lucas and Dawn 2's redesign: the evidence and the diagnosis

Ian asked on 2026-10-21 for Lucas and Dawn 2 (Route 207, Fantina's split, the next story fight after Jupiter 1) to be redesigned in Roark's and Gardenia's checked stages. This page holds stages 1 and 2, the evidence and the diagnosis. No team has changed, and no candidate or set is picked here: those are stages 3 and 4, after Ian checks this.

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
