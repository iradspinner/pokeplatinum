# Part two: the rules applied to the rest of the cast

The rules are in `rules.md` (with Ian's answers at its top) and in short in `principles.md`. This file applies them to every species the changes have not reached: the untouched natives and the species added from later generations. Suggestions are grouped by confidence, then the lines to leave alone, then the unobtainable species in one place. Splits are the split in which the player first has the form, from `availability.csv` and the evolution levels against the caps in `splits.md`; "Fantina (33)" means the form arrives in Fantina's split because the evolution level fits under its cap of 33.

Stat lines read HP/Atk/Def/SpA/SpD/Spe. Every ability named exists in Oxide's ability list (`res/text/ability_names.json`).

## A. Fixes Ian has already ruled on

These follow from his answers and the weather ruling, so they come before any new suggestion.

### The sheet slips

Oxide's data should carry the sheet for these (Ian: "slips").

| Species | Oxide now | Sheet (Kaizo) |
|---|---|---|
| Tentacruel | 80/70/65/80/120/100 | 80/80/65/90/120/100 (535) |
| Houndoom | 75/90/50/110/80/95 | 75/90/50/120/80/105 (520) |
| Weezing | 65/90/120/85/70/60 | 65/90/120/90/85/60 (510) |
| Skarmory | 85/80/140/40/70/70 | 85/85/140/40/80/70 (500) |
| Noctowl | SpA 76 | SpA 86 (488) |
| Banette | Spe 65 | Spe 85 (485) |
| Fearow | SpA 61 | SpA 31 (442) |
| Cascoon | SpD 25 | SpD 55 (235) |
| Graveler | Spe 35 | Spe 45 (440) |
| Metapod, Kakuna | SpA 55, SpD 25 | SpA 25, SpD 55 |
| Shedinja | SpD 5 | SpD 10 |
| Raichu | Static | Lightning Rod |
| Pikachu | Static | Reckless |
| Hypno | Insomnia \| Forewarn | Insomnia |

Four more sheet rows differ from the data and were not in the question. By Ian's own ability rule (keep a useful vanilla ability) the data's version is the better one for Drapion (Battle Armor | Hyper Cutter, the sheet has Kaizo's Sand Veil, which is evasion junk without sand) and for Blissey (Natural Cure | Serene Grace, the sheet drops Natural Cure). Armaldo is a coin toss (data: Swift Swim | Hyper Cutter; sheet: Swift Swim | Battle Armor). Wormadam's sheet value, Snow Cloak, is hail-only evasion and worse than the data's Anticipation; Overcoat, its hidden ability, is the one that does something, so I would put Anticipation | Overcoat there rather than follow the sheet. Ho-Oh's Magic Guard (sheet) is unobtainable and harmless to apply. Donphan SpA 55 is noise; apply it for fidelity. Onix and Sudowoodo losing Sturdy (sheet) depends on the Sturdy question below. Mamoswine SpD 85, Bastiodon 95/4 and Swinub's buff are later decisions of Ian's and stand.

### Weather abilities to the hidden slot

| Line | Regular slot after | Hidden |
|---|---|---|
| Snover, Abomasnow | Adaptability | Snow Warning |
| Hippopotas, Hippowdon | Thick Fat | Sand Stream |
| Tyranitar | Solid Rock (Kaizo's first slot for it) | Sand Stream |
| Psyduck, Golduck | Damp \| Swift Swim (Swift Swim is the modern hidden ability) | Cloud Nine |

Tyranitar's filler is the one choice here. Kaizo gave it Solid Rock | Battle Armor; Solid Rock fits the walls Ian has already given it to (Steelix, Glalie, Corsola, Probopass, Bastiodon) and Tyranitar's role at Candice's split. Damp on Golduck is a leftover junk slot; with Cloud Nine gone, Swift Swim is the only ability in its family that does anything, and the tolerance for trainer-weather abilities (rule A4) covers it.

### The junk-ability oversights

Ian confirmed these were missed. I have paired each removal with the line's most useful other ability rather than leaving one slot, following his "keep a useful vanilla ability" answer.

| Line | Now | Suggested regular slots | Hidden |
|---|---|---|---|
| Chinchou, Lanturn | Volt Absorb \| Illuminate | Volt Absorb \| Water Absorb | Water Absorb (duplicate; could become Illuminate) |
| Hoothoot | Insomnia \| Keen Eye | Insomnia \| Tinted Lens (matches Noctowl) | Tinted Lens |
| Wooper, Quagsire | Damp \| Water Absorb | Water Absorb \| Unaware | Unaware |
| Swinub, Piloswine | Oblivious \| Snow Cloak | Snow Cloak \| Thick Fat (matches Mamoswine) | Thick Fat |
| Skitty, Delcatty | Cute Charm \| Normalize | Cute Charm (Kaizo's) | Wonder Skin |
| Sneasel | Keen Eye \| Inner Focus | Technician \| Inner Focus (matches Weavile) | Pickpocket |
| Corvisquire | Keen Eye \| Unnerve | Keen Eye \| Big Pecks | Big Pecks |
| Corviknight | Pressure \| Unnerve | Pressure \| Mirror Armor | Mirror Armor |
| Sinistcha | Hospitality | Heatproof | Cursed Body or Hospitality |
| Alomomola | Healer \| Hydration | Regenerator \| Hydration | Healer |
| Mr Rime | Tangled Feet \| Screen Cleaner | Vital Spirit \| Screen Cleaner (Galarian Mr Mime keeps Vital Spirit) | Ice Body |
| Jumpluff (and Hoppip, Skiploom) | Chlorophyll \| Leaf Guard | Chlorophyll \| Infiltrator | Infiltrator |
| Glaceon | Snow Cloak | see B below | Ice Body |

Hospitality (heals an ally on entry), Healer, Tangled Feet, Unnerve, Pressure and Leaf Guard do nothing for a nuzlocke player in singles; Snow Cloak and Ice Body need hail the player never gets. Corviknight and Alomomola each had two dead regular slots, which is the strongest case for a change in this whole file.

### The Sturdy question

Kaizo strips Sturdy because Generation 4's Sturdy only blocks one-hit KO moves. Oxide's ability description still says exactly that, so I could not confirm from `res/` whether Oxide's Sturdy is the modern one (survive any hit from full HP). If it is modern, Sturdy is one of the best abilities a nuzlocke wall can have in a first-and-only-attempt game, and the removals from Golem, Aggron's line, Donphan, Bastiodon's line, Nosepass's line, Forretress, Skarmory, Magnezone, Steelix and Shuckle took away something real; the sheet's Onix and Sudowoodo removals would compound it. Suggested rule: if Sturdy is modern, restore it as the second regular slot wherever Kaizo removed it and the line has one slot free (Golem Shell Armor | Sturdy, Aggron Rock Head | Sturdy, Donphan Battle Armor | Sturdy, Probopass Solid Rock | Sturdy, Forretress Heatproof | Sturdy, Skarmory Filter | Sturdy, Shuckle Solid Rock | Sturdy) and leave the rest. If it is still Generation 4's, nothing needs doing.

### The possible misses Ian asked to have flagged

Rotom (Fantina gift, 440): Kaizo's 50/65/107/105/107/91 (525) is a sound buff if the Rotom forms are not reachable until late; if the Secret Key is early, the forms (520) are the buff and the base needs nothing. Delibird, Kadabra and Haunter: taken up in B and C. Tyranitar SpA 100, Electabuzz Atk 87, Lickitung Atk 60, Hoothoot Atk 36: noise, skip. Blissey Def 30 and Chansey Def 25: skip; Blissey is SS tier in every Platinum nuzlocke list and needs no help. Tangela SpD 50: apply, it is harmless and Tangela is a Maylene-split catch. Politoed Atk 85: apply, it is a Gardenia-split final and Kaizo's number is the source. Dugtrio Atk 100, Farfetch'd, Jigglypuff's line, Grimer SpD 75, Ledyba, Spinarak, the birds and the beasts: unobtainable, so trainer palette only; apply Kaizo's numbers for fidelity or leave, it changes nothing in play.

## B. High confidence

The rule applies squarely and either a source number exists or the change is forced by a ruling.

| Species | Split | Change | Total |
|---|---|---|---|
| Swablu | Fantina | Normal/Flying to Fairy/Flying | 310 |
| Altaria | Maylene (35) | Dragon/Flying to Dragon/Fairy | 510 |
| Luvdisc | Roark | Water to Water/Fairy | 330 |
| Alomomola | Fantina (30) | Water to Water/Fairy; Healer to Regenerator | 470 |
| Delibird | Candice | 45/55/45/65/45/75 to 65/90/60/85/60/100; Vital Spirit \| Adaptability | 330 to 460 |
| Kricketune | Roark (10) | 77/85/51/55/51/65 to 87/105/61/55/61/75; Hyper Cutter \| Technician | 384 to 444 |
| Mawile | Byron | HP 50 to 70, SpD 55 to 75 | 400 to 440 |
| Quagsire | Gardenia (20) | HP 95 to 105, SpD 65 to 75; Water Absorb \| Unaware | 430 to 450 |
| Slowbro, Slowking | Maylene (37) | Oblivious to Regenerator (Regenerator \| Own Tempo) | 490 |
| Glaceon | Fantina | Snow Cloak to Ice Scales | 525 |
| Cinccino | Roark (stone) | Cute Charm to Skill Link (Technician \| Skill Link) | 470 |
| Kadabra | Roark (16) to Wake | Kaizo's 55/35/45/120/85/120 | 400 to 460 |

Swablu and Altaria are the three Renegade retypes Ian said he missed, so this is the change he has already made in spirit. Altaria arrives in Maylene's split as the first Dragon the player can raise from a catch (Gible's Gabite is the other), and Dragon/Fairy with Kaizo's Serene Grace and 80/80/90/80/105/80 gives it a niche no other line has there: a Dragon that resists Fighting, Bug and Dark and is immune to Dragon, into Byron's split and the Galactic Dragons. It follows T2 (a type that names the creature: a cloud bird), T4 (the whole line, since Swablu shows the trait). The risk is defensive: Dragon/Fairy is weak to Steel and Poison, so Altaria goes from neutral into Byron to weak, and it loses the Ground immunity of Flying. Against that, the 4x Ice weakness into Candice becomes 2x. On balance it is a better Altaria for a nuzlocke, and the bulk is what carries it.

Luvdisc and Alomomola: Ian missed Renegade's Luvdisc Water/Fairy. In Oxide Luvdisc evolves into Alomomola at 30, so T4 says the line changes together. Alomomola as a Water/Fairy wall with Regenerator (its defining ability, moved in because both regular slots were dead) is a Fantina-split find that no other line matches: 165 HP, Wish, a Fighting and Dragon resistance. Risk: Regenerator on a 165 HP wall in gauntlets is a lot of free healing; but it has 40 Special Attack and 65 Speed, and walls are exactly what a no-retry game rewards. Luvdisc itself stays a 330 Roark catch; the Fairy type only makes it the Fairy answer to Roark-split Fighting types until it evolves.

Delibird is the weakest obtainable final in the game and the latest weak catch (Candice's split, cap 56). Kaizo's +70 with Adaptability was skipped and Ian did not list Delibird among his deliberate skips, so it is a miss; Kaizo's 400 was also too little for a level-56 catch, so this goes to 460 by S1's band, keeps Vital Spirit (useful against the Snowpoint hypnotists and Bronzong) and adds Kaizo's Adaptability (A2, A3). Smogon's own analysis calls its stats "some of the worst of any fully evolved Pokemon" and its typing terrible; at 460 with 100 Speed and Adaptability Ice Shard and Drill Peck it becomes a fast Ice/Flying pivot for Candice, the Galactic fights and Aaron. Risk: Ice/Flying stays a bad defensive type, and Flint's Fire is next; 460 still leaves it below every other late catch, which is the point.

Kricketune is the only Roark-split final under 400 and Kaizo left it, so S1 applies at its lowest band. Technician (its modern hidden ability) beside Kaizo's Hyper Cutter makes Fury Cutter and Bug Bite real damage at level 10 to 26. Risk: none of consequence; it remains a Bug that falls off by Fantina, which is its natural life.

Mawile is a 400 final at Byron's split with Kaizo's +20 Attack and nothing else; S1 says a final under 450 gets bulk. HP and Special Defense are its two holes and Intimidate Steel/Fairy is a role (a pivot into Candice, Aaron and Cynthia's Garchomp) that nothing else at Byron fills. Risk: none; it stays the lowest total at its split.

Quagsire: the Damp removal is one of the oversights Ian confirmed; Unaware is its identity and the answer to a boss that sets up. The bulk brings it to S1's band and matches Odyssey's numbers exactly (100/85/90/65/75/35 was Odyssey's; I have moved the Defense point to HP to keep Ian's round numbers). Niche: from Gardenia's split to Wake's, the Water/Ground wall that ignores Dragon Dance and Calm Mind. Risk: Unaware undercuts the setup bosses, but Oxide already starves setup of PP.

Slowbro and Slowking: Oblivious is junk (A1); Regenerator is the modern hidden ability, and Ian has already moved a hidden ability into a regular slot for Mamoswine and Munchlax (A5's exceptions). Niche: the Maylene-split special wall that comes back from a gauntlet fight healed. Risk: Regenerator is the strongest healing ability in the game; on a 30 Speed Pokemon with no player-set Trick Room it is manageable, and the Slow line is exactly where Kaizo tried Simple and Ian refused it, so a gentler answer is due.

Glaceon is the one Eeveelution left with a dead regular ability while Leafeon got Magic Guard | Natural Cure and Flareon got Adaptability. Snow Cloak needs hail the player never gets (A1). Ice Scales halves special damage and gives Glaceon the role its stats already suggest, a special tank with 130 Special Attack, mirroring Leafeon's Magic Guard on the physical side. The line is super-wanted, so a small bias is allowed. Risk: Ice Scales is strong; Glaceon's 65 Speed, Ice typing and Fantina's Ghost and Steel neighbours keep it a tank rather than a sweeper. If Ice Scales feels too much, Refrigerate (Normal moves become Ice) is the damage-ability alternative under A3.

Cinccino: Cute Charm is junk (A1) and Skill Link is its identity, moved in on the Mamoswine precedent. Technician stays as the useful vanilla ability (A2). Risk: Skill Link Tail Slap from level 16 is strong, but Cinccino costs the Roark-split Shiny Stone that Roserade, Togekiss and Florges also want, so it competes for a scarce item rather than a free slot.

Kadabra is had from Roark's split (Abra at 16) and is not Alakazam until Wake's, four splits later; S4 says a stint that long gets a buff, and Kaizo's numbers exist. Kadabra with 120 Speed and Special Attack is still Psychic-locked and paper-thin on the physical side. Risk: 120 Special Attack from level 16 walks through Gardenia; but Fantina's Ghosts and Maylene's Fighting types are next, and vanilla Kadabra already has the same Special Attack.

## C. Medium confidence

The rule applies, but a judgement is involved: which stat, which ability, or whether the line's niche needs it.

| Species | Split | Change | Total |
|---|---|---|---|
| Haunter | Fantina (25) to Wake | Kaizo's 60/50/60/115/75/110 | 405 to 470 |
| Machoke | Fantina (28) to Wake | 90/100/80/50/70/45 | 405 to 435 |
| Gabite | Fantina (24) to Byron | 68/90/75/50/65/82 | 400 to 430 |
| Rhyhorn | Roark to Wake (42) | 90/95/95/30/30/25 | 345 to 365 |
| Litwick | Fantina to Wake (41) | 60/30/65/75/65/20 | 275 to 315 |
| Sandygast | Fantina to Wake (42) | 65/55/90/80/55/15 | 320 to 360 |
| Lunatone | Byron | SpA 95 to 110, SpD 85 to 95 | 470 to 495 |
| Solrock | Byron | Atk 95 to 110, Def 85 to 95 | 470 to 495 |
| Seaking | Fantina (33) | Odyssey's 85/105/70/65/80/70 | 450 to 475 |
| Lanturn | Fantina (27) | Def 58 to 68, SpA and SpD 76 to 86 | 460 to 490 |
| Kingler | Fantina (28) | HP 55 to 65, SpD 50 to 65; consider Hyper Cutter \| Sheer Force | 475 to 500 |
| Sudowoodo | Fantina | 85/110/115/30/80/30 | 410 to 450 |
| Bibarel | Roark (15) | Def and SpD 60 to 70 | 410 to 430 |
| Emolga | Gardenia | 70/75/70/95/60/103 | 428 to 473 |
| Mothim | Gardenia (20) | 80/94/60/94/60/76 | 424 to 464 |
| Togedemaru | Byron | 75/108/73/40/73/96 | 435 to 465 |
| Dewgong | Maylene (34) | Odyssey's 100/70/90/70/100/70 | 475 to 500 |
| Ludicolo | Roark (stone) | SpA 90 to 100, Def 70 to 80 | 480 to 500 |
| Toucannon | Fantina (28) | Keen Eye to Sheer Force (Sheer Force \| Skill Link) | 485 |
| Talonflame | Maylene (36) | Flame Body \| Gale Wings | 499 |
| Florges | Maylene (stone) | Flower Veil to Magic Guard | 552 |
| Frosmoth | Fantina | Shield Dust to Ice Scales | 475 |

Haunter, Machoke and Gabite follow Kadabra's logic (S4): each is carried for three or four splits before its final. Kaizo has a number for Haunter; for Machoke I have used Ian's Loudred pattern (+10 to the bulk stats) and for Gabite the same. Gabite matters most: Gible is a Fantina catch and Garchomp needs level 48, so the player fights Maylene, Wake and Byron with a 400 Gabite; +30 of bulk keeps it alive without touching Garchomp. Risk: none to the finals, which are unchanged.

Rhyhorn, Litwick and Sandygast are pre-evolutions with long stints and low totals (Rhyhorn from Roark to Wake's cap of 42, Litwick and Sandygast from Fantina to Wake). Flat +20 or +40 on the Loudred pattern. Risk: Rhyhorn at 95 Attack in Roark's split is a strong early Rock; Rhydon at 42 is the real fix if Ian would rather move the evolution level, which is outside this brief.

Lunatone and Solrock are the twin pair Ian named for the Plusle and Minun treatment (S7). They already split special against physical; Odyssey pushed each by +60. Pushing the specialised side by +15 and the matching defence by +10 makes the difference the player feels at Byron's split, where both are wild: Lunatone the Rock/Psychic special attacker with Calm Mind, Solrock the physical one with Rock Polish. Risk: none; 495 sits in band for a Byron catch.

Seaking and Dewgong take Odyssey's numbers because Ian named Odyssey as a source he trusts and neither Kaizo nor Renegade touched either. Seaking keeps Swift Swim | Water Veil (Water Veil stops the burn that ruins a physical attacker; A2) with Lightning Rod hidden; its niche at Fantina is Megahorn and Drill Run coverage on a Water body. Dewgong at 500 is the Thick Fat Water/Ice wall for Flint and the Galactic fights. Risk: both stay mid-table; that is the target.

Lanturn: the Illuminate fix is in A; the stats bring a 460 final to 490 and its role (the Electric-immune special sponge, useful against Volkner and Lucian) is real in Smogon's UU analysis but needs the bulk to survive repeated hits. Kingler's holes are HP and Special Defense; Sheer Force (its modern hidden ability) with Crabhammer is the damage ability A3 would give an attacker, but Kingler's 75 Speed and 130 Attack already threaten at Fantina, so the ability is the optional half.

Sudowoodo is a 410 final Ian left; Smogon calls it "entirely outclassed" by Rhydon, which Oxide has. The buff gives it Rock Head Head Smash from real bulk at Fantina, before Rampardos and Bastiodon are evolved. Keep Sturdy in the second slot if Sturdy is modern (the sheet's Rock Head-only follows Kaizo's Generation 4 reasoning).

Bibarel is nuzlocke A-tier by the forums' ranking for its Simple boosts; with Oxide's setup at 1 to 3 PP a single Curse is still +4, so the ability carries it. Only bulk is needed to get the boost off. Emolga is "too weak to break anything and too frail" in Smogon's words; +45 into HP, Defense and Special Attack makes it the Gardenia-split Electric with a Ground immunity. Mothim is the male Burmy's payoff and sits at 424 with Tinted Lens; +40 of bulk and Speed keeps it usable through Fantina. Togedemaru is a Byron wild at 435; +30 into HP, Attack and Defense gives the Lightning Rod Electric/Steel a body for Volkner. Ludicolo's Special Attack is "not especially impressive" even in rain (Smogon), and the player has no rain; +20 keeps a Water Stone choice honest against Poliwrath and Starmie.

Toucannon: Keen Eye is marginal and Sheer Force is its modern hidden ability. Talonflame: at 499 with Flame Body it is a fast Fire/Flying with nothing else; Gale Wings (the Generation 7 version, priority only at full HP) is what makes it a Pokemon, and it beats Maylene outright, which is the niche. This one sits closest to A5's line on boss-killers; the full-HP condition is what keeps it on the right side. Florges: Flower Veil does nothing in singles (A1); Magic Guard is the ability Ian gives Fairy special attackers (Clefable, Gardevoir, Ninetales) and makes Florges the passive-damage-proof special wall for Maylene's split onward. Frosmoth: Shield Dust is marginal and Ice Scales is its identity; Quiver Dance at 1 to 3 PP keeps it from running away.

## D. Low confidence, worth testing

Sylveon: Cute Charm to Pixilate (Fantina, via Charm). Pixilate Hyper Voice at Fantina is the kind of thing Ian keeps hidden on the added starters, but Sylveon is a super-wanted line with a dead regular slot; if it proves too strong, Cute Charm to Pixilate could wait for the Ability Patch as it does now.

Espeon: Synchronize to Magic Bounce (Fantina, Sun Stone). Same shape: the identity ability into a junk slot, on a super-wanted line; strong against bosses' status and hazards, frail otherwise.

Lurantis: Leaf Guard to Contrary (Maylene, 34), or to Chlorophyll if Contrary reads as a boss-killer. Leaf Guard is junk without sun (A1); Contrary Leaf Storm is what Lurantis is for.

Pupitar: +10 HP and +10 Attack (60/94/70/65/70/51, 410) for the Fantina-to-Candice stint. Ian used a type change instead of stats for this line (T5), which is why this is low.

Volbeat and Illumise: unobtainable in Oxide, so palette only, but Ian's twin rule invites an Odyssey-style split for trainer use: Volbeat Bug/Electric special (Renegade's 65/33/75/107/85/100, 465, Tinted Lens) and Illumise Bug/Fairy physical (65/97/85/33/85/100, 465, Tinted Lens; Renegade's Illumise is special too, the reversal is mine), Renegade's types onto Ian's Tinted Lens.

Ampharos Electric/Dragon (Renegade): Ian is lukewarm on the line; the type would give Fantina's split a Dragon with Electric STAB and a Fire, Water, Grass and Flying resistance set, if he warms to it.

Sturdy restoration (see A) if Oxide's Sturdy is modern.

## E. Lines to leave alone, and why

Obtainable natives and added species with no suggestion.

| Line | Split | Why |
|---|---|---|
| Houndoom, Alakazam, Gengar, Machamp, Crobat, Kingdra, Yanmega, Hariyama, Relicanth, Blissey, Manaphy, Giratina | various | Already carry their split (S6); Blissey is SS in the nuzlocke lists. Alakazam's Magic Guard stays hidden for the Ability Patch. |
| Snorlax, Ampharos, Blaziken | Wake, Fantina, Maylene | Lines Ian is lukewarm on; a change is an invitation he does not want to make. |
| Turtwig, Chimchar, Piplup lines; Charmander, Squirtle, Treecko, Torchic, Mudkip, Totodile lines | various | Already changed or fine; the vanilla starters are Kaizo's. |
| Snivy, Fennekin, Froakie, Rowlet, Litten, Popplio, Scorbunny, Sprigatito lines | various | Added starters keep Contrary, Magician, Protean, Long Reach, Intimidate, Liquid Voice, Libero hidden: the A5 pattern Ian has applied to all of them. Cinderace is a Byron gift. |
| Vaporeon, Jolteon, Umbreon, Leafeon, Flareon | Fantina | Fine as they are; Leafeon and Flareon already changed. |
| Clodsire, Carbink, Araquanid, Dubwool, Pawmot, Vikavolt, Galvantula, Klefki, Salazzle, Runerigus, Leavanny, Orbeetle, Polteageist, Cofagrigus, Crustle, Garganacl, Kleavor, Arboliva, Mienshao, Dhelmise, Glimmora, Toxapex, Jellicent, Palossand, Ferrothorn, Chandelure, Annihilape, Goodra, Hisuian Goodra, Kommo-o, Volcarona, Hawlucha, Turtonator, Grapploct, Lopunny M, Galarian Rapidash, Galarian Weezing, Alolan Ninetales, Tsareena, Liepard, Gothitelle | various | Added species whose totals sit in band for their split and whose regular abilities work. Polteageist's Weak Armor and Shell Smash (1 PP) is a design, as is Palossand's Water Compaction. |
| Floatzel, Ludicolo (abilities), Poliwrath, Politoed, Swampert, Barboach line, Anorith line, Mantyke line, Finneon line | various | Swift Swim and Rain Dish stay: trainers keep their weather, and Ian gives these abilities freely (A4). |
| Cherrim, Castform | Gardenia, Maylene | Flower Gift and Forecast need weather the player lacks; Ian buffed Castform's stats and left Cherrim at Kaizo's. Both are weather-trainer specialists by design. |
| Scyther, Yanma, Murkrow, Remoraid, Horsea, Seadra, Mantine, Makuhita, Ralts line, Machop, Magnemite line, Geodude line, Onix, Growlithe | various | The second abilities are useful ones (Swarm, Sniper, Water Absorb, Guts, Trace, Sturdy). |
| Beautifly, Dustox, Chatot, Purugly, Staraptor, Medicham, Wormadam, Girafarig, Mismagius, Golem, Rapidash, Absol | various | Kaizo's numbers stand; still on the weak side (Beautifly 395, Chatot 466) but Ian took Kaizo's view. |
| Golduck (type) | Fantina | Renegade's Water/Psychic passed on; Slowbro and Starmie already fill that role. |
| Feraligatr (type), Noctowl (type), Misdreavus and Mismagius (type) | various | Passed on by Ian; each got its buff another way. |
| Rotom forms, Wormadam forms, Deoxys and Shaymin forms | various | Form data exists in `res/pokemon`; forms change the base's picture and were outside this data. |

## F. Species the player cannot obtain

Two hundred and fourteen species have no wild, gift or evolution route in Oxide: most of Kanto and Johto's non-Sinnoh cast, the Regis, the Kanto birds and Johto beasts, the box legendaries, and among the added species the Ultra Beasts, the Tapus, the Galarian birds, Meloetta, Magearna, Diancie, Xerneas, Yveltal, Zygarde, Gyarados's Mega form, Mandibuzz's line, the Popplio, Scorbunny and Sprigatito lines (their finals arrive as gifts or not at all) and Flabebe (Floette is a gift). For these the rules apply only as trainer-team palette: a buff changes only what a trainer can field. Ian has already taken Kaizo's numbers for many of them (Pidgeot, Fearow, Ledian, Ariados, Dunsparce, Sableye, Kecleon, the Regis, Deoxys), which keeps trainer rosters in step with Kaizo's; the possible misses among them (Dugtrio, Farfetch'd, Jigglypuff's line, Grimer, Ledyba, Spinarak, the birds, the beasts, Ho-Oh's Magic Guard) can take Kaizo's numbers on the same basis or be left, with no effect on the player's game.
