# The rules behind Platinum Oxide's Pokemon changes

A fresh reading of `changes.csv`, `species.csv`, `availability.csv`, the Kaizo files and Ian's own sheet, checked against Renegade Platinum, Pokemon Odyssey, Smogon's in-game and competitive analyses and the nuzlocke community's Platinum rankings. Part two (`suggestions.md`) applies the rules to the rest of the cast; `principles.md` is the rulebook on its own.

## Questions to Ian and his answers (2026-09-29)

**Where did the seventeen "own" type changes come from?** Fourteen match Renegade Platinum's Complete version. Ian: mostly from Renegade, each one "vibes" checked. The Renegade retypes he passed on (Golduck, Feraligatr, Noctowl, Ampharos, Misdreavus and Mismagius) were ones he was neither excited for nor against. Swablu, Altaria and Luvdisc were misses rather than skips. The two he altered (Vibrava Bug/Flying instead of Bug/Dragon, Milotic Water/Dragon instead of Water/Fairy) were his own ideas.

**Are the gaps between Ian's sheet and Oxide's data reversals or slips?** The sheet carries Kaizo values that Oxide does not: Tentacruel Atk 80 and SpA 90, Houndoom SpA 120 and Spe 105, Weezing SpA 90 and SpD 85, Skarmory Atk 85 and SpD 80, Noctowl SpA 86, Banette Spe 85, Fearow SpA 31, Cascoon SpD 55, Graveler Spe 45, Raichu Lightning Rod, Pikachu Reckless, Hypno Insomnia only. Ian: slips; Oxide should carry the sheet.

**Weather abilities in regular slots of catchable lines (Snover, Hippopotas, Larvitar's Tyranitar)?** Ian: pending; the weather ability becomes the hidden ability. The Overseer confirmed this is now a ruling, and it also covers Psyduck's Cloud Nine (weather-cancelling).

**What was the Plusle and Minun rebuild for, and does it extend to other twins?** Ian: copied from Pokemon Odyssey, whose Plusle is a support tank and whose Minun is a special sweeper; he thought it was a very good design. Yes, extrapolate to the other pairs.

**Is "a strong line or a legendary gets no buff" a rule?** Ian: Ditto, Unown and Smeargle were skipped because he dislikes them. Gyarados, Snorlax, Dragonite, Ampharos, Blaziken and Typhlosion were skipped because he is lukewarm on playing them. The rest (Rotom, Tyranitar, Electabuzz, Blissey, the legendary birds and beasts) may simply have been missed: flag them.

**What decides whether a vanilla ability stays beside Kaizo's, and why were some junk-ability removals skipped?** Ian: keep a vanilla ability that is genuinely useful; the skipped removals (Chinchou's Illuminate, Hoothoot's Keen Eye, Wooper's Damp, Swinub's Oblivious, Skitty's Normalize) are oversights.

**Wailord Speed 5, Tangrowth Speed 10, Registeel Speed 5 (Kaizo's Trick Room numbers)?** Ian: kept on purpose.

**Gothitelle (Psychic/Dark, +40), Tsareena (Grass/Fighting, Speed 92) and Liepard (+50, Prankster in a regular slot): Hardlove's or Ian's?** Ian: his. He named no source beyond Kaizo, Renegade and Odyssey.

## 1. The changes as a whole

`changes.csv` has 655 rows over 276 species: 416 stat rows on 169 species, 203 ability rows and 36 type rows. The tag column says 552 rows match Kaizo alone, 20 match both Kaizo and the later games, 20 match the later games alone (the Generation 6 Fairy retypes and the Corsola, Mantine, Lunatone and Solrock HP updates), and 63 are tagged as Ian's own. That last tag over-counts. Fourteen of the seventeen own type rows are Renegade Platinum's Complete-version retypes. Eleven own stat rows are Odyssey's Plusle and Minun. And the Kaizo ability document (`kaizo-abilities.md`) disagrees with the Kaizo column in `species.csv` on several species: by the document, Armaldo's Swift Swim | Hyper Cutter, Gallade's Hyper Cutter, Tangrowth's Magic Guard | Unaware and Tropius's Overgrow are Kaizo's, and Slugma's, Magcargo's and Camerupt's Solid Rock is Kaizo's second slot with its Drought dropped. What is left as Ian's own is short: Larvitar and Pupitar Dark/Ground, Vibrava Bug/Flying, Milotic Water/Dragon, Swinub's +65, Loudred's +60, Graveler's scaled-down numbers, Castform SpA 120, Bastiodon 95/4, Mamoswine SpD 85, Primeape No Guard, Meowth and Persian Super Luck | Technician, Flareon's Adaptability beside Flash Fire, Politoed's Swift Swim beside Water Absorb, Noctowl's Tinted Lens beside Insomnia, Drapion's Hyper Cutter beside Battle Armor, Turtwig and Grotle Shell Armor, and, among the added species, Gothitelle, Tsareena, Liepard and Purrloin.

Of the 276 changed species, 187 are obtainable in Oxide (wild, gift or evolution) and 89 are not; those 89 matter only as trainer-team palette.

### Who was changed, and by how much

The stat changes land on finished forms. Of the 169 species with a stat change, 133 are fully evolved; their median vanilla total is 479 and the median change is +30. The buff scales with how weak the Pokemon was:

| Vanilla total | Species | Mean change | Mean result |
|---|---|---|---|
| under 450 | 38 | +44 | 449 |
| 450 to 499 | 49 | +33 | 505 |
| 500 and up | 46 | +21 | 558 |

Attack is the stat raised most often (99 of 102 rows go up), then Special Attack (69 up, 24 down), Special Defense (67 up), Defense (57 up) and HP (51 up). Speed is touched least (38 rows, 33 up) and never by more than what reaches a benchmark (Delcatty 112, Chatot 110, Raichu 110, Glalie 100, Castform 100, Seviper 100, Absol 95, Luxray 95, Honchkrow 91, Poliwrath 90, Politoed 90, Piloswine 80, Ariados 70, Carnivine 70, Vespiquen 70). Special Attack is the stat most often lowered, because Kaizo drains the attacking stat a Pokemon does not use: Feraligatr, Empoleon, Luxray, Seviper, Sandslash, Onix, Steelix, Ursaring, Torterra, Dusclops, Dusknoir, Rampardos, Shieldon, Bastiodon, Primeape, Honchkrow and Huntail all lose Special Attack while gaining elsewhere, and Blastoise, Mr. Mime and Plusle lose Attack.

### When the changed Pokemon are had

By split of first availability (wild or gift, with evolutions placed at the split whose cap reaches the evolution level), the changed finished forms are spread over the whole game, thickest in the first three splits where the cast is largest: Roark 21 of 23 finals changed or added, Gardenia 33 of 38, Fantina 37 of 51, Maylene 45 of 51, Wake 19 of 27, Byron 18 of 19. The untouched finals at those splits are the lines Ian is lukewarm on (Blaziken, Ampharos, Snorlax), lines already strong (Houndoom, Alakazam, Gengar, Machamp, Crobat, Kingdra, Blissey, Yanmega), a few walls whose vanilla form already does the job (Hariyama, Quagsire, Slowbro, Slowking, Relicanth), and a handful that look like misses (Bibarel, Ludicolo, Sudowoodo, Seaking, Jumpluff, Lanturn, Kingler, Golduck, Dewgong, Delibird, Glaceon's ability).

### What Ian did not take from Kaizo

Kaizo changed the stats of 216 species and the abilities of about 300. Ian's skips fall into clear groups, and each group says something.

Weather. Every weather-setting ability Kaizo added was dropped: Drought on Slugma, Magcargo, Numel, Camerupt and Moltres; Drizzle on Zapdos, Dragonair and Bronzong; Snow Warning on Articuno; Sand Stream on Flygon. Where Kaizo paired weather with a second ability, Ian kept the second one alone (Slugma, Magcargo and Camerupt Solid Rock). Alolan Ninetales got Magic Guard rather than its official Snow Cloak | Snow Warning.

Kaizo's compensation for its own evolution levels. Kaizo's Abra evolves at 45, its Geodude and Machop at 48, its Haunter and Bronzor very late, so Kaizo buffed Kadabra, Haunter, Geodude, Graveler, Machoke and Bronzor heavily. Oxide keeps sane evolution levels, and Ian skipped all of those except Graveler, which he took at about half of Kaizo's numbers. He also skipped Kaizo's Machoke Huge Power gimmick and its Machop and Mudkip nerfs.

Gimmick abilities. Shadow Tag on Gengar and Ditto, Simple and Unaware on the Psyduck and Slowpoke lines, Huge Power on Machoke and Mudkip, Wonder Guard on Unown, Bad Dreams on Drowzee, No Guard on Ampharos, Insomnia on Mewtwo, Magic Guard on Mew: all skipped. Where the new ability is the species' modern hidden ability, it usually stayed hidden (Abra line Magic Guard, Golduck Swift Swim, Vaporeon Hydration, Voltorb Aftermath), though not always (Mamoswine Thick Fat and Munchlax Gluttony went into regular slots).

Lines Ian does not enjoy. Gyarados, Snorlax, Dragonite, Ampharos, Blaziken and Typhlosion (lukewarm); Ditto, Unown and Smeargle (dislike). This is his own answer, and it is the one group that no rule would have predicted.

Slips. Twelve Kaizo values on his sheet never reached the data (the list is in the answers above), and the Metapod, Kakuna and Shedinja rows already being checked. Ian wants all of them applied.

Possible misses (Ian: "flag them"). Rotom's +65 (Def and SpD 107, SpA 105), Tyranitar SpA 100, Electabuzz Atk 87, Blissey Def 30, the Kanto birds' and Johto beasts' +20s, and by the same token Chansey Def 25, Tangela SpD 50, Lickitung Atk 60, Grimer SpD 75, Jigglypuff's and Igglybuff's bulk, Dugtrio Atk 100 (also the later games' value), Farfetch'd's +90, Delibird's +70 with Adaptability, Hoothoot, Ledyba and Spinarak's pre-evo nudges, Politoed Atk 85, Skarmory's Atk and SpD (on the sheet), and the Deoxys and Rotom form rows. Most of these are unobtainable or tiny; Delibird, Rotom and Kadabra are the ones that change play, and part two picks them up.

## 2. The rules

Confidence is high where Ian confirmed the rule or the data shows it without exception, medium where the data shows it with a few unexplained exceptions, low where I am reading intent into a handful of cases.

### Rules about stats

**S1. Buff the finished form, to the 450 to 560 band, in proportion to how far below it sits.** A fully evolved Pokemon under 450 gets about +45, one in the 450s and 460s about +30, one over 500 about +20 or nothing. Shown by the whole table above and by Pidgeot (469 to 529), Fearow (442 to 472), Ledian (390 to 440), Ariados (390 to 455), Dunsparce (415 to 490), Delcatty (380 to 492), Sableye (380 to 480), Corsola (380 to 470), Spinda (360 to 480), Kecleon (440 to 525), Tropius (460 to 550), Vespiquen (474 to 558), Magcargo (410 to 509), Chatot (411 to 466), Girafarig (455 to 520). Exceptions: Kricketune (384, ability only), Beautifly and Dustox (395 and 405, +10 and +20), Mawile (380 to 400), Pachirisu (405 to 445), Mothim (424, ability only), Delibird (330, nothing), Sudowoodo (410, nothing): all lines Kaizo itself left or barely touched, so these are Kaizo's gaps inherited rather than Ian's choices. Confidence high.

**S2. Points go where the Pokemon already attacks from; the other attacking stat pays for it.** Kaizo's specialisation reshuffles are taken wholesale even when they flip an identity: Empoleon becomes physical (Atk 111, SpA 86), Blastoise becomes a slow special tank (SpA 110, Spe 60), Feraligatr and Ursaring go all-physical, Seviper becomes a fast physical snake (SpA 60, Spe 100), Luxray trades Special Attack for Speed, Shedinja goes to 1/100/5/100/5/80, Rampardos to 180 Attack and 15 Special Attack, Bastiodon to 95 Attack and 4 Special Attack. The one mixed result is Sceptile (Atk 100, SpA 100), and Hypno, Girafarig, Stantler, Vespiquen, Pelipper and Octillery are raised on both sides because they use both. A nerf never appears alone: Kaizo's standalone nerfs (Machop, Machoke, Mudkip) were skipped, and Honchkrow's SpA 100, Wailord's HP 165, Meganium's Def and SpD 90 are each the price of a bigger gain elsewhere. Confidence high.

**S3. Bulk before Speed.** HP, Defense and Special Defense carry most of the buff; Speed rises only to a benchmark that changes a matchup, and Speed nerfs are accepted as Trick Room design (Wailord 5, Tangrowth 10, Registeel 5, Blastoise 60, Plusle 55: Ian confirms on purpose). Confidence high.

**S4. A pre-evolution is buffed when the player will fight with it for a split or more.** Kaizo's pre-evo buffs were taken where Oxide's evolution level leaves a long stint (Slugma to 38, Surskit to 22 then a weak Masquerain, Shellder until a scarce Water Stone, Duskull to 37, Cranidos and Shieldon to 30 from a Fantina gift, Spoink to 32, Cacnea and Aron to 32, Sealeo to 44, Snorunt to 42, Shuppet to 37, Stunky to 34, Meditite to 37, Wailmer to 40, Vibrava to 45, Metang to 45, Onix until a Metal Coat) and skipped where the stint is short or Kaizo's reason was its own late evolution (Kadabra, Haunter, Machoke, Geodude, Bronzor). Ian's two own pre-evo buffs follow the same logic with flat numbers: Swinub +15/+20/+20/+10 (to 33) and Loudred +10 across (to 40). Exceptions the rule does not explain: Kadabra (16 to 40), Haunter (25 to 40), Machoke (28 to 40) and Gabite (24 to 48) all have long stints and no buff. Confidence medium.

**S5. Numbers are round, and Kaizo's are rounded up when Ian touches them.** Ian's own numbers are multiples of 5 and mostly of 10 (Swinub, Loudred, Graveler, Plusle, Minun). Where he adjusted a Kaizo number he went up to the next round figure: Castform SpA 110 to 120, Bastiodon Atk 92 to 95 and SpA 7 to 4, Mamoswine SpD 80 to 85. Kaizo's odd increments (+1 Charizard, +1 Infernape, +3 Octillery, +2 Torterra) were taken verbatim rather than cleaned, which is consistent with copying a source faithfully and adjusting only when a judgement is made. Confidence high.

**S6. A line that already carries its split gets nothing, and the +5 on Garchomp, Salamence and Metagross is a signature rather than a buff.** Houndoom (a Gardenia-split Fire type in Oxide), Alakazam, Gengar, Machamp, Crobat, Kingdra, Blissey, Yanmega, Hariyama, Relicanth, Manaphy, Giratina: untouched. Ian's answer refines this: some untouched strong lines are simply lines he does not enjoy, and some are misses. The rule as he would restate it is "a buff has to open a niche the line lacks", with taste allowed to leave a line alone. Confidence medium (the principle holds, the boundary is his taste).

**S7. Twins are split into two Pokemon (from Odyssey).** Plusle became a physical wall (80/40/95/50/95/55, Plus) and Minun a fast special attacker (65/40/55/95/55/105, Minus), copied from Odyssey. Ian says to extrapolate to Volbeat and Illumise and to Lunatone and Solrock. Kaizo's Huntail and Gorebyss (Atk 114 versus SpA 114) and its Nidoking and Nidoqueen already follow the idea. Confidence high (confirmed).

### Rules about types

**T1. The official Fairy retypes are taken in full.** Twenty species in eight lines (Clefairy, Jigglypuff, Mr. Mime, Togepi, Marill, Snubbull, Ralts, Mawile and their stages) carry the Generation 6 types; nothing else from the later games' type changes exists for Platinum's cast, so this is complete. Confidence high.

**T2. Beyond canon, a type is added that names what the creature is, taken from Renegade's menu and filtered by enthusiasm.** Charizard, Sceptile, Flygon and Milotic become dragons; Luxray and Larvitar get Dark; Electivire gets Fighting; Trapinch's line gets Bug; Glalie gets Rock; Masquerain gets Water; Ninetales and the lake trio get Fairy. Renegade's Golduck Water/Psychic, Feraligatr Water/Dark, Noctowl Psychic/Flying, Ampharos Electric/Dragon, Misdreavus and Mismagius Ghost/Fairy were passed because they did not excite; Swablu, Altaria and Luvdisc were missed (so they are live suggestions). A type is added, not swapped, except where the swapped type was the weak point: Charizard, Vibrava and Flygon lose Flying or Ground, Larvitar loses Rock. Confidence high (confirmed), with the boundary being taste.

**T3. Dragon and Dark are the additions Ian reaches for; Fairy is for canon and one favourite.** Of the Renegade Fairy additions he took only Ninetales (a super-wanted line, mirroring Alolan Ninetales) and the lake trio; Milotic got Dragon where Renegade gave Fairy. Confidence medium.

**T4. The whole line changes together when the pre-evolution shows the trait; otherwise only the final.** Larvitar and Pupitar, Trapinch, Vibrava and Flygon, and the lake trio change as lines; Charizard, Sceptile, Luxray, Electivire, Milotic, Glalie, Masquerain and Ninetales change alone because Charmander has no wings and Shinx no darkness. Vibrava's Bug/Flying is a stepping stone to Flygon's Bug/Dragon. Confidence high.

**T5. A type change can stand in for a stat buff, and it stacks with Kaizo's stats when both exist.** Larvitar and Pupitar got Dark/Ground and no stats: the change resists Fantina's Ghost moves, keeps Psychic immunity and halves Wake's Water damage compared with Rock/Ground, which carries the pre-evo through the two splits it spends unevolved. Milotic and Electivire got a type and only an ability or +10 Speed. Everywhere else the type sits on top of Kaizo's numbers (Flygon SpA 110, Glalie 520, Luxray's reshuffle, Masquerain +40, Ninetales +50, Sceptile's reshuffle). Sources are combined rather than chosen between. Confidence medium (the Larvitar reading is mine; Ian was not asked).

### Rules about abilities

**A1. One capture rolls one ability, so no regular slot holds junk.** Run Away, Pickup, Illuminate, Keen Eye, Stench, Klutz, Early Bird, Frisk, Forewarn, Anticipation, Own Tempo, Oblivious, Damp, Honey Gather, Normalize and Cute Charm were removed from about 60 lines (Rattata, Sentret, Aipom, Seedot, Zigzagoon, Wingull, Roselia, Shroomish, Poochyena, Electrike, Corsola, Nosepass, Shellos, Drifloon, Buneary, Glameow, Stunky, Bonsly, Budew, Croagunk, Mantyke, Riolu, Munchlax, Snubbull, Girafarig, Dunsparce, Hitmontop, Stantler, Absol, Ambipom, Porygon-Z, Rhyperior, Gulpin, Sharpedo and more). Ian confirmed the ones left behind (Chinchou, Hoothoot, Wooper, Swinub, Skitty) are oversights. Note that Kaizo's junk list assumed Generation 4 effects: Sturdy was stripped from Golem, Aggron's line, Donphan, Bastiodon's line, Nosepass's line, Forretress, Skarmory, Magnezone, Steelix, Shuckle and Bonsly, and from Onix and Sudowoodo on the sheet, because Generation 4 Sturdy only blocks one-hit KO moves. Oxide's ability text still reads that way, so whether Oxide's Sturdy is the modern one is unverified from `res/`; if it is, those removals took away a real ability. Confidence high on the rule, open question on Sturdy.

**A2. A genuinely useful vanilla ability stays beside the new one.** Flareon Flash Fire | Adaptability, Politoed Water Absorb | Swift Swim, Meowth and Persian Super Luck | Technician, Noctowl Insomnia | Tinted Lens, Drapion Battle Armor | Hyper Cutter, Corphish Adaptability | Hyper Cutter, Torkoal White Smoke | Shell Armor, Zangoose Hyper Cutter | Immunity, Seviper Hyper Cutter | Shed Skin, Weavile Technician | Inner Focus, Lucario Iron Fist | Adaptability, Gible Sand Veil | Rough Skin, Whiscash Hydration | Swift Swim. Where the vanilla ability was weak it went (Rapidash Reckless alone, Pidgeot Intimidate alone, Golem Shell Armor alone, Jynx Snow Cloak alone). Ian confirmed. Confidence high.

**A3. Weak attackers get a damage ability; walls get a damage-reducing one; special attackers get Magic Guard.** Tinted Lens to Noctowl, Beautifly, Dustox, Volbeat, Illumise, Mothim, Vespiquen, Sharpedo, Luxray and Vibrava. Adaptability to Sentret's line, Pachirisu, Riolu's line, Electivire, Corphish's line, Snover's line and Flareon. Technician to Aipom's line, Breloom, Weavile and Scizor. Sniper to Spearow's line; Super Luck to Meowth's line, Absol and Honchkrow; Reckless to Rapidash, Staravia's line and Luxray; Iron Fist to Ledian, Infernape and Lucario; Scrappy to Buneary's line, Chatot and Whismur's line; Hyper Cutter to Kricketune, Luxio, Gallade, Drapion, Armaldo, Zangoose and Seviper; Intimidate to Pidgeot, Ekans, Ariados, Feraligatr, Mawile, Stantler, Mightyena, Tauros and Snubbull. Solid Rock or Filter to Corsola, Nosepass's line, Shuckle, Steelix, Glalie, Lileep's line, Regirock, Shieldon's line, Slugma's line, Camerupt, Skarmory, Milotic, Walrein, Regice, Registeel and Mr. Mime. Magic Guard to Ninetales, Natu's line, Staryu's line, Gardevoir, Clefairy's line, Leafeon, Tangrowth, Mesprit and Deoxys. Confidence high.

**A4. No weather-setting or weather-cancelling ability in a regular slot of an obtainable line; abilities that need the player's own weather are tolerated only because trainers keep theirs.** Every Kaizo weather addition was dropped and the vanilla ones are moving to hidden slots. Swift Swim, Chlorophyll, Solar Power, Rain Dish, Hydration, Ice Body and Snow Cloak stay in regular slots (Poliwag's line, Prinplup, Empoleon, Swampert, Barboach's line, Anorith's line, Mantyke, Finneon's line, Sunkern's line, Venusaur, Charizard) because trainers' weather still triggers them. Confidence high on the ban, medium on the tolerance (it is what the data does, not something Ian stated).

**A5. Gimmick abilities that would define a boss-killer are refused, and a species' strong modern hidden ability mostly stays hidden.** Shadow Tag, Huge Power outside Marill, Simple, Wonder Guard, Bad Dreams and No Guard on Ampharos were refused; the added starters keep Protean, Libero, Contrary, Speed Boost and Intimidate hidden; Alakazam's Magic Guard stays hidden. Exceptions: Primeape's own No Guard (with Dynamic Punch, a deliberate design), Klefki's and Liepard's Prankster in regular slots, Mamoswine's Thick Fat and Munchlax's Gluttony moved in. Confidence medium.

**A6. A regular ability may duplicate the hidden one.** Noctowl, Mamoswine, Munchlax, Ledian, Poliwag, Whiscash, Crawdaunt, Breloom, Spearow and Wailord all carry the same ability twice. Nothing in the data avoids it, so it is not a rule, only a cleanup opportunity. Confidence high that it is unregulated.

### How the three interact

A Pokemon is changed once, in the layer that fixes its problem. If the problem is raw numbers (a 380 to 460 final), it gets Kaizo's stats and usually Kaizo's ability. If the problem is a role nobody at that split fills, it gets a type (Larvitar the Ghost-resisting Ground type at Fantina, Luxray a Dark STAB, Milotic a Dragon, Glalie a Rock). If the problem is a dead slot, it gets an ability. When a line has two problems the layers stack rather than compete (Flygon, Glalie, Luxray, Masquerain, Ninetales). A stat buff is never used to make up for a bad ability or a bad type, and a type is never used to make up for a bad ability: each layer addresses its own kind of weakness.

The point of every change is the nuzlocke frame in `environment.md`: one capture per area rolls one ability, so junk slots are worth removing; a hard cap per split means a middle stage must hold its own for a whole split, so long stints get buffs; a first and only attempt at each fight means walls and Magic Guard are worth more than they are in a game with retries; and no player weather means Swift Swim is only ever a bonus against a trainer's rain.

## 3. Where Ian departs from Kaizo, and what it says about his taste

Kaizo changes no types at all; Ian added a whole type layer from Renegade and his own head, and it is where his enthusiasm shows most clearly. He likes a creature to be what it looks like (Charizard and Sceptile as dragons, Luxray as a dark predator, Electivire as a brawler, Trapinch as a bug) and prefers Dragon and Dark to Fairy as the "cool" addition.

Kaizo hands out weather and trapping; Ian refuses both, because the player never controls weather and a trap ability makes a fight a foregone conclusion rather than a first attempt.

Kaizo replaces abilities; Ian keeps the good vanilla one beside the new one. He treats an ability slot as something the player owns rather than as a design lever.

Kaizo buffs the middle of a line when its own evolution levels force a long stint; Ian buffs the middle of a line when Oxide's levels do (Swinub, Loudred, Graveler), and skips Kaizo's compensations. He edits for his own game's schedule rather than the source's.

Kaizo's numbers are sometimes precise to the point of noise; Ian copies them faithfully but rounds up when he intervenes, and his own numbers are flat +10s and +20s. He is not tuning damage rolls; he is moving a Pokemon into a band.

Kaizo buffs almost everything; Ian leaves alone what he does not want to play (Gyarados, Snorlax, Dragonite, Ampharos, Blaziken, Typhlosion, Ditto, Unown, Smeargle). A change in Oxide is an invitation to use the line, and he declines to invite lines he would not use.

Kaizo builds boss gimmicks (Shadow Tag Gengar, Huge Power Machoke); Ian's one gimmick is a player-side one, Primeape's No Guard, and his one identity flip of his own, the Odyssey Plusle and Minun, is about making two catches in the same grass into two different Pokemon. His taste is for distinctness over power.

## Sources

Smogon's Platinum in-game tier list (Jubilee's guide and the v2 thread) gave the community view of which Platinum natives are weak and why, and the tier definitions used to weigh "shallow movepool" against "poor stats". Nuzlocke University's Platinum tier list (the image) and the Nuzlocke Forums viability thread (via search excerpts: Blissey and Garchomp SS, Gyarados S, Bronzong A+, Floatzel and Gastrodon A, Houndoom A, Togekiss A+, Staraptor debated between S and A) gave the nuzlocke weighting: bulk, typing and early availability over movepool. Smogon's competitive analyses, read through its data endpoint for Delibird, Sudowoodo, Bibarel, Serperior, Emolga, Yanmega, Ludicolo, Lanturn and Alomomola, gave each species' known problems (translated down to Oxide's caps and item ban in part two). Renegade Platinum's archived wiki (the `pokemon_changes.md` in `zhenga8533/renegade-platinum-wiki`) identified the source of the type changes and Drayano's own buffs. Pokemon Odyssey's stats spreadsheet (linked from its guide) identified the Plusle and Minun source and Odyssey's other twin splits. Platinum Kaizo's documentation (the local files) plus the retrododo and pokehackdb summaries gave Kaizo's design frame: permanent weather and Trick Room areas, every trainer with an item and four moves, and late evolution levels, which explain several of Kaizo's changes that Oxide rightly skipped.
