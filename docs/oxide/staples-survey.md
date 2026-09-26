# Staples survey: what other hacks change in moves, abilities, types and mechanics

Written 2026-09-25 for Ian's question: are there changes that many or most ROM hacks make, which Oxide should take too? Measured against the reference calculators in `~/roms/balance-refs/`, the donor engine and published documentation. Nothing in `res/`, `src/` or the tools was changed.

Yes, and the biggest one is cheap. Five or six of the seven references use the Generation 5 to 7 numbers for the weak Generation 4 moves (25-power multi-hit moves, 40-power Fury Cutter, 75-power Giga Drain and Drain Punch, 120-power Thrash and Petal Dance). Oxide's 452 new moves already carry modern numbers, but 31 of those 40 native moves are still at their Generation 4 values. The second staple is the set of modern battle rules that every expansion engine ships by default: Sturdy works like a Focus Sash, Lightning Rod and Storm Drain grant immunity, Grass is immune to powder, Electric cannot be paralysed, critical hits do 1.5x, and Defog clears both sides. Oxide still runs all of these on Generation 4 rules. Many other staples are already in or planned: Fairy, reusable TMs, trade evolutions replaced, obedient trades and the EV and IV viewer are done, and hidden abilities, Mints, Ability Patch and level caps are planned.

Recommended, most useful first:

1. Give the 31 native moves still at Generation 4 numbers their Generation 5 to 7 buffs (appendix A). Data only.
2. Bring the native abilities up to their modern behaviour, Sturdy, Lightning Rod and Storm Drain first, and add the Generation 6 type immunities. Small C changes, with hg-engine's code as the reference, in element 5.
3. Make Defog clear both sides and give Rapid Spin its Speed raise. Oxide now has Sticky Web and Aurora Veil, which raises the value of hazard removal. Battle-script changes.
4. Give the nine species that still lack them their Generation 6 and 7 stat buffs. Data only.
5. Add field moves without teaching HMs, and a Move Relearner that is free and easy to reach. These are the two common quality-of-life staples Oxide lacks.

Two more bundles are real staples, but they change how hard the game is, so they are Ian's call, not a recommendation. The first is the Generation 6 cut to the strong special attacks: Thunderbolt to 90, Fire Blast to 110 and the rest. The second is the Generation 6 and 7 rules for status and critical hits taken as a set.

## Where Oxide's native data comes from

Ian's early changes are the base ROM's edits to 108 native moves and 409 species, and most of them match Platinum Kaizo's data exactly. Oxide's changes and Kaizo's agree on 187 of the 203 species whose abilities changed, 152 of the 169 whose base stats changed, and 79 of the 110 changed move values. Kaizo sets its own numbers instead of adopting the later-generation ones. That explains why Oxide has setup moves at 1 to 3 PP and elemental punches at 95 power, but still has 10-power Fury Cutter and 60-power Giga Drain. Nothing below proposes undoing those edits. Where Oxide already has a number of its own, the tables treat it as a deliberate choice.

## How this was measured

Each reference's calculator file gives its move numbers and species data. Each value is compared with vanilla (the `main` branch) and with the modern value. The modern baseline is hg-engine's move and species data at commit 5157c50, which is Generation 9. That commit wraps 46 moves in toggles for the 2026 Pokemon Champions changes, and the survey reads the Generation 9 branch of each one. A count such as "6 of 7" means six of the seven references that carry that field use that value.

| Reference | Built on | Move fields read | Species fields read |
|---|---|---|---|
| Renegade Platinum | Platinum, edited in place | power, accuracy, PP, type | types, stats, two abilities |
| Platinum Redux | Platinum, edited in place | the same; 142 native moves are replaced by its own | the same, for the 416 natives it keeps |
| Platinum Kaizo | Platinum, edited in place | power, accuracy, PP, type | types, stats, abilities |
| Hardlove Gold | hg-engine on HeartGold | power, PP, type | types, stats, abilities |
| Pokemon Null 1.2 | Emerald with a modern battle engine | power, accuracy, PP, type | types, stats, three abilities |
| Pokemon Unbound | FireRed with CFRU | power, type | types, stats, abilities |
| Radical Red | FireRed with CFRU | power and type, from the vendored calculator's Radical Red patch over Generation 9 values | none |

A Platinum hack edited in place cannot add move records. That is why all three of those hacks replace old moves and set their own numbers. The expansion engines (hg-engine, CFRU and pokeemerald-expansion) ship modern numbers and rules unless a hack turns them off, so a modern value in those four hacks reflects their engine's default. Calculator data holds numbers, not behaviour, so the rows on ability behaviour and battle rules rest on engine configuration and published documentation instead. Run & Bun's sheet and the Odyssey ROM in the folder hold no usable move or species data, so neither is counted.

## Moves

| Staple | How common | Oxide now | If open: cost and home |
|---|---|---|---|
| Generation 5 to 7 power buffs to 40 weak moves (multi-hit moves to 25, Fury Cutter 40, Giga Drain and Drain Punch 75, Thrash and Petal Dance 120, Future Sight 120, High Jump Kick 130, trapping moves 35, Knock Off 65) | Modern value in Renegade on 35 of 37, Hardlove 38 of 40, Null 40 of 40, Unbound 36 of 40 and Radical Red 37 of 40. Kaizo (10 of 37) and Redux (2 of 31) use numbers of their own | Open. 2 at the modern value (Bubble, Uproar) and 7 at a base-ROM value of their own (Knock Off 70, Rapid Spin 60, Leech Life 65, Smog 55, Assurance 70, Snore 80, Lick 40). The other 31 are still at Generation 4 values (appendix A) | Data only, in `res/moves/`. Phase 5, balance track: a move-data pass beside its design pass 3, not yet in its plan |
| Generation 6 cuts to 19 strong moves (Thunderbolt, Flamethrower, Ice Beam and Surf 95 to 90; Fire Blast, Thunder, Blizzard and Hydro Pump 120 to 110; Draco Meteor, Overheat and Leaf Storm 140 to 130; Aura Sphere 80; Sucker Punch 70; six more) | Renegade 18 of 19. Hardlove, Null and Radical Red 19 of 19. Unbound keeps the old power on 16 (its dex site lists Flamethrower at 95), Kaizo keeps all 19, and Redux cuts the 95s further, to 80 | Open, Ian's call. All 19 are at Generation 4 values, while the new moves already use post-cut numbers (Hurricane 110, Moonblast 95), so the game has two scales side by side | Data only. Same pass |
| Accuracy raised on 26 moves (Will-O-Wisp 85; Cotton Spore, Scary Face, Glare and Disable 100; trapping moves 85; Rock Tomb 95; Gunk Shot 80) | Renegade 25 of 25, Kaizo 9 of 24, Null 10 of 26 (it usually goes to 100 instead) and Redux 3 of 16. Cotton Spore and Scary Face at 100 is the only change all three Platinum hacks share | Partly done. 5 at the modern value and 9 at a base-ROM value of their own (seven to 100, Crabhammer 95, Poison Gas 85). 12 are still at Generation 4 values, including Will-O-Wisp 75, Cotton Spore 85 and Scary Face 90 | Data only. Same pass |
| Accuracy cuts: Thunder Wave 90, Dark Void 50, Swagger 85 (all Generation 7) | Renegade has all three. Kaizo and Null have none, and both raise Dark Void and Swagger instead. Redux has one | Open, Ian's call. All three are at Generation 4 values | Data only. Same pass |
| PP changes to 23 moves (Outrage, High Jump Kick, Thrash, Petal Dance and Drain Punch to 10; Rock Tomb 15; Vine Whip 25; Tailwind 15) | Renegade 22 of 22, Hardlove 22 of 23, Null 23 of 23. Kaizo 0 of 21, Redux 3 of 17 | Open. None at the modern value. Four are lower on purpose (Swords Dance and Acid Armor 1, Growth and Minimize 3), and those stay | Data only. Same pass |
| Generation 9 PP cut on healing moves (Recover, Roost, Slack Off, Soft-Boiled, Milk Drink and Rest to 5) | Only Hardlove and Null, whose engines track Generation 9. None of the three Platinum hacks | Not a staple. Rest is already 3 (base ROM) | Nothing to do |
| Hidden Power at a flat 60 (Generation 6) | Default in all four expansion hacks. None of the Platinum hacks: Renegade adds a Hidden Power teller NPC instead | Open, Ian's call. Oxide keeps the IV formula (30 to 70). Oxide's trainers have high IVs and sit near 70, so a flat 60 would weaken the move slightly | C change, one line in the command that computes it. Phase 4 element 8 |
| Curse becomes Ghost type (Generation 5) | 5 of 7: Renegade and the four expansion hacks | Open. Still the ??? type | Data only. It matters only to type-changing abilities such as Protean, if element 5 brings them in |
| Charm, Sweet Kiss and Moonlight become Fairy | 5 of 7. Kaizo and Redux have no Fairy type | Done (element 1, 2026-09-22) | |
| Old moves replaced by newer ones | Renegade 11, Kaizo 26, Redux 142. None in the expansion hacks, which add moves instead | Done another way: element 4 added the 452 new moves as new records | |
| HM moves made useful: Cut to Grass type, Rock Climb to Rock type, Fly to 100 power and accuracy | Cut is Grass in Renegade, Redux and Null (Steel in Radical Red), with 100 accuracy in four. Rock Climb is Rock in four. Renegade raises Fly. Sacred Gold and Storm Silver document buffs to Cut, Strength and Rock Smash | Cut already has 100 accuracy (base ROM). The type changes are open | Data only. Balance pass |
| Signature and niche moves raised past their modern numbers: Needle Arm (four hacks, 80 to 95), Chatter (three, 80 to 120), Octazooka 80 (three), Mega Drain 60 (three), Shadow Claw 80 (two), Luster Purge and Mist Ball (95 officially since Generation 7; Kaizo 100, Radical Red 85) | No single buff is shared by more than four hacks | The base ROM already did some: Poison Fang 75 (five hacks buff it), Shadow Punch 95, Attack Order 120, the elemental fangs 90. The rest are open | Data only. Balance pass |
| Kaizo-style edits: accuracy rounded up to 100, setup moves cut to 5 PP or less | Accuracy raised past both old and modern: Null on 111 moves, Kaizo 96, Redux 70. PP cut to 5 or less: Kaizo 56, Redux 54 | Done by the base ROM: 40 moves raised past both, 33 cut to 5 PP or less | |
| Pokemon Champions (2026) changes | hg-engine carries them upstream behind toggles, all on by default except the PP one (46 moves, for example Slash 80 and Growth as Grass type). No reference hack has them yet | Not a staple yet | |

## Abilities

| Staple | How common | Oxide now | If open: cost and home |
|---|---|---|---|
| Hidden abilities | Renegade gives 138 native species their modern hidden ability as a regular slot, Hardlove 71, Kaizo 49 and Redux 39. Null has a true third slot, used by 397 natives. Radical Red offers them through DexNav and an ability swapper | Planned: the full mechanic, the encounter flag and Ability Patch (Ian, 2026-09-20). This is element 8, with Ability Capsule and Patch in element 7. The base ROM already gives 35 natives theirs | |
| Ability redistribution | Every Platinum hack reworks many: Redux 402 natives, Kaizo 332, Renegade 194. Only 14 additions agree across four or more of the six. Oxide has 8 of them: Rough Skin on Gible and Garchomp, Scrappy on Loudred and Exploud, Iron Fist on Infernape and Ledian, Thick Fat on Mamoswine and Reckless on Staraptor | Planned: the ability balance pass (Ian, 2026-09-20), the balance track's design pass 3. Oxide has changed 203 natives, 187 of them to Kaizo's abilities | Open within that pass: Magic Guard on the Abra line, Rough Skin on Gabite and Flame Body on Ponyta, each in four hacks. Data only |
| Pelipper with Drizzle and Torkoal with Drought (Generation 7) | Pelipper in Renegade, Redux, Hardlove and Null. Torkoal in Renegade, Redux and Null | Open. Oxide's Pelipper has Unburden, and its Torkoal has White Smoke or Shell Armor, both Kaizo's choices | Data only. Ability pass. It depends on the weather-duration answer below: Pelipper is much stronger under permanent rain than under five turns |
| Modern behaviour of Generation 4 abilities: Sturdy survives any hit from full HP (Gen 5); Lightning Rod and Storm Drain grant immunity and +1 Sp. Atk (Gen 5); Intimidate fails on Inner Focus, Own Tempo, Oblivious and Scrappy (Gen 8); Oblivious blocks Taunt and Overcoat blocks powder (Gen 6); Keen Eye ignores evasion and Frisk reveals every foe's item (Gen 6); Synchronize passes on bad poison, Flash Fire works while frozen and Leaf Guard blocks Rest in sun (Gen 5); Normalize adds 1.2x (Gen 7); Illuminate stops accuracy drops (Gen 9) | Default in every expansion engine. pokeemerald-expansion has a generation toggle for most of these, and each defaults to the latest generation. hg-engine has the modern behaviour built in. No Platinum hack documents a change to ability behaviour, and Renegade's notes say its engine could not carry some move effects | Open. Oxide runs the Generation 4 rules: Sturdy blocks only one-hit KO moves, and Lightning Rod only redirects | C changes, each small, with hg-engine's ability code as the reference. Phase 4 element 5, which already ports that code for the new abilities. The AI has to be taught each change in element 6 |

## Typings and base stats

| Staple | How common | Oxide now | If open: cost and home |
|---|---|---|---|
| Fairy type, with the Generation 6 retypes of 20 native species | 5 of 7: Renegade and the four expansion hacks. Kaizo and Redux have no Fairy type. Sacred Gold and Storm Silver add it through an unofficial mod | Done (element 1) | |
| Steel loses its resistance to Ghost and Dark (Generation 6) | Default in the expansion engines | Ruled out. Oxide keeps the Generation 4 chart with Fairy added, and Steel keeps both resistances (Ian, 2026-09-22) | |
| Rotom's forms take their appliance types (Generation 5) | All four expansion hacks | Done (base ROM) | |
| Custom retypes | Renegade 29 (its wiki says 31 in the Complete version) and Redux 115. The other hacks have none beyond Fairy. No custom retype is shared by three hacks. Renegade and Redux share nine. Four are Mega typings made permanent: Charizard Fire/Dragon, Ampharos Electric/Dragon, Sceptile Grass/Dragon and Lopunny Normal/Fighting. The other five are Feraligatr Water/Dark, Luxray Electric/Dark, Electivire Electric/Fighting, Flygon Bug/Dragon and Volbeat Bug/Electric | Not a staple. Open as an idea for the balance pass | Data only |
| Generation 6 and 7 base stat buffs to 44 native species (Pikachu, Raichu, Pidgeot, Alakazam, Nidoking, Nidoqueen, Clefable, Staraptor, Roserade and 35 more). Cresselia's change is a cut | All 43 buffed species have a higher total in at least five of the six hacks with species data. Hardlove, Null and Unbound use the modern numbers exactly. Renegade adopts them and then buffs further | Mostly done by the base ROM's own edits: 5 exact, 27 at or above the modern total. Open: 9 untouched (Alakazam, Ampharos, Dugtrio, Electrode, Farfetch'd, Jumpluff, Pikachu, Roserade, Swellow), 2 slightly under (Chimecho 450 against 455, Staraptor 480 against 485), and Cresselia's cut | Data only, in `res/pokemon/`. The balance track's design pass 3, together with the 21 native species tabled in Phase 0 |

## Battle mechanics

Every row below was checked in Oxide's battle code. Oxide's battle-code changes so far serve its new moves (always-critical moves, new two-turn moves, Defog clearing Sticky Web and Aurora Veil), so each rule here is still vanilla Generation 4.

| Staple | How common | Oxide now | If open: cost and home |
|---|---|---|---|
| Critical hits do 1.5x instead of 2x (Gen 6), at rates of 1/24, 1/8, 1/2 and always (Gen 7) | Default in every expansion engine (hg-engine's rate table reads 24, 8, 2, 1, 1). None of the Platinum hacks | Open. Oxide: 2x, at rates from 1/16 to 1/2 | C change in the critical-hit function and the damage step that applies it. Sniper's 3x becomes 2.25x. Phase 4 element 8, with the AI in element 6 |
| Paralysis halves Speed instead of quartering it (Gen 7) | Default in every expansion engine | Open | C change at several speed-comparison sites. Element 8 |
| Burn does 1/16 instead of 1/8 (Gen 7) | Default | Open | One divisor in a battle script. Element 8 |
| Sleep lasts 1 to 3 turns instead of 1 to 4 (Gen 5) | Default | Open | C change. Element 8 |
| Confusion self-hits 1/3 of the time instead of 1/2 (Gen 7) | Default | Open | C change. Element 8 |
| Multi-hit moves hit 2, 3, 4 or 5 times at 35, 35, 15 and 15 percent (Gen 5) | Default | Open. Pairs with the 25-power multi-hit buffs | C change. Element 8 |
| Ability weather lasts five turns (Gen 6) | Default in pokeemerald-expansion. hg-engine's Drizzle sets temporary rain | Open, Ian's call. In Oxide it is permanent, and the base ROM puts weather on 57 maps, including the Oreburgh and Pastoria Gyms | C and battle-script change. The balance track's weather pass decides it and element 8 implements it |
| Defog clears hazards from both sides (Gen 6) | Default | Open. Oxide's Defog clears only the target's side (now including Sticky Web and Aurora Veil) | Battle-script change. Element 8, or an element 4 follow-up |
| Rapid Spin has 50 power and raises Speed (Gen 8) | Default in the expansion engines. Redux uses 60 | Partly done: 60 power (base ROM), no Speed raise | Battle-script change. Element 8 |
| Knock Off does 1.5x against a target holding an item (Gen 6) | Default | Open. Oxide's Knock Off is a flat 70 (base ROM) | C change in the power calculation. Element 8 |
| Grass is immune to powder, Electric cannot be paralysed, Ghosts can escape trapping (Gen 6) | Default | Open. Platinum's eight move flags have no powder flag | C change. Powder needs a move list or a new flag. Element 8, with the AI in element 6 |
| Physical and special split | Every hack | Done (vanilla Generation 4) | |
| Frostbite replacing freeze | An option in pokeemerald-expansion, off by default | Not a staple | |
| Level-scaled experience formula (Generation 5 or 7) | Default in the expansion engines | Ruled out. The flat Generation 4 formula stays (Ian, 2026-09-20) | |
| Mega Evolution, Z-moves and gems | Radical Red and Unbound have Megas | Ruled out (Ian, 2026-09-20). Gyarados M and Lopunny M are ordinary evolutions | |
| Choice items | | Ruled: rare in Oxide, because the lock can be baited (Ian, 2026-09-23) | |

## Quality of life

| Staple | Documented in | Oxide now | If open: cost and home |
|---|---|---|---|
| Reusable TMs | Renegade, Radical Red, Inclement Emerald; an option in hg-engine | Done (base ROM, ported 2026-09-20) | |
| HMs can be forgotten | | Done (base ROM) | |
| Field moves without teaching an HM | Radical Red ("no need to teach HMs"), Renegade (HM requirements largely removed), Sacred Gold and Storm Silver (most unneeded Cut trees removed) | Open | C change to the field-move checks (allow the move once its badge is earned and a party member could learn it, or give it to an item), or map edits. Phase 5 or backlog |
| A Move Relearner that is free or easy to reach | Radical Red (Cerulean City), Inclement Emerald (every Pokemon Center, with the Deleter) | Open. Still vanilla: Pastoria City, one Heart Scale per move | Script edit to a carry-over map, registered as an intended divergence. Phase 5 |
| Move Deleter moved early | Renegade (Oreburgh City) | Open. Still in Canalave City | Script and event edit. Phase 5 |
| Free move tutors | Renegade | Open. The new species' tutor lists stay empty until the TM pass | Phase 5 TM pass |
| Nature changing | Radical Red (a Nature Changer in every Pokemon Center), Mints | Planned: Mints (element 7) | |
| Ability changing | Radical Red (an ability swapper, hidden ability included) | Planned: Ability Capsule and Ability Patch (element 7) | |
| EV and IV viewer | Radical Red (IV grades, an EV checker) | Done (the summary screen's Skills page) | |
| IV perfecting | Radical Red (for a steep price) | Planned: Bottle Caps (element 7) | |
| The nature's raised and lowered stats marked on the summary | Renegade, Radical Red | Open | C change in the summary screen's drawing code. Element 8 or backlog |
| Hidden Power's type shown | Renegade (a teller NPC) | Open | A script NPC, or the summary screen |
| Trade evolutions replaced | Renegade, Sacred Gold and Storm Silver | Done (base ROM). Stripping the 17 dead trade entries is planned (element 8) | |
| Traded Pokemon always obey | Renegade | Done (base ROM) | |
| Fast hatching | Renegade (zero egg cycles) | Partly done: the base ROM cut hatch cycles on 228 species | |
| Exp. Share for the whole party | Radical Red (a Generation 6 toggle), Sacred Gold and Storm Silver (early) | Not needed: level caps (element 8) and infinite Rare Candies (ruled 2026-09-26) cover it | |
| Level caps | Radical Red (soft cap), Inclement Emerald (an option) | Planned (element 8). Rare Candy chaining is done | |
| Portable PC | | Planned: the base ROM's Vs. Seeker PC, not ported yet (Phase 3) | |
| Infinite Repel | An option in hg-engine | Partly done: the "use another Repel?" prompt | Open. C change, optional |
| Auto-run | Radical Red | Open, minor | C change |
| Set battle style, fast text, a faster HP bar, 30 boxes, held items restored after battle, the national dex from the start | Common | Done or planned (element 8) | |

## Questions for Ian

1. Native move numbers: take the Generation 5 to 7 buffs only, or the full modern set with the Generation 6 cuts too, so old and new moves share one scale? The survey recommends the full set, keeping every number the base ROM already set on purpose (the 1 to 3 PP setup moves, Knock Off 70 and the rest).
2. The Generation 7 accuracy cuts to Thunder Wave, Dark Void and Swagger: take them or not?
3. Hidden Power: a flat 60, or keep the IV formula?
4. Should element 5 also bring the native abilities up to their modern behaviour? If only some, which? The survey's short list is Sturdy, Lightning Rod, Storm Drain, the Intimidate blockers, Overcoat and Keen Eye.
5. Battle rules: take the Generation 6 type immunities and the 1.5x critical hit? Should the status changes (paralysis, burn, sleep, confusion, multi-hit spread) come as one set, or stay Generation 4?
6. Ability weather: five turns or permanent, given the weather the base ROM puts in gyms and on routes? This is the balance track's weather pass.
7. Defog clearing both sides, Rapid Spin's Speed raise and Knock Off's item bonus: take all three?
8. The nine species still without their modern stat buffs, and Cresselia's cut: take them in design pass 3?
9. Pelipper with Drizzle, Torkoal with Drought, and Magic Guard on the Abra line: consider them in the ability pass?
10. Field moves without HMs, and a free Move Relearner (where, and at what cost)?

## Ian's answers (2026-09-26)

Ian answered all ten questions on 2026-09-26, and the answers replace the recommendations above wherever they differ.

1. Native moves take the full modern set: the Generation 5 to 7 buffs and the Generation 6 cuts, so old and new moves share one scale. Every number the base ROM set on purpose stays (the 1 to 3 PP setup moves, Knock Off 70 and the rest of the "own value" rows).
2. Thunder Wave, Dark Void and Swagger keep their Generation 4 accuracy.
3. Hidden Power keeps the IV formula.
4. Every native ability gets its modern behaviour, Sturdy, Lightning Rod and Storm Drain first.
5. The Generation 6 type immunities are taken: Grass is immune to powder, Electric cannot be paralysed, and Ghosts can escape trapping. Critical hits go to 1.5x at the modern rates. Paralysis, burn, sleep, confusion and the multi-hit spread stay Generation 4.
6. Weather from abilities stays permanent, and **the player has no way to set, change or end weather for the whole game**. There are two exceptions: the game's single Ability Patch (there is to be exactly one), which can give a Pokemon a weather ability as its hidden ability, and Defog, which keeps clearing fog in battle and on the field. Trainers keep their weather. So no weather move (Rain Dance, Sunny Day, Sandstorm, Hail and the newer ones) may be learnable by the player's Pokemon by level, TM, tutor or egg, and no Pokemon the player can obtain may have a weather-setting or weather-cancelling ability (Drizzle, Drought, Sand Stream, Snow Warning, Sand Spit, Cloud Nine, Air Lock and the like) in a regular slot.
7. Defog clears hazards from both sides and Rapid Spin raises Speed. Knock Off stays a flat 70.
8. The nine species without their modern stat buffs get them, and Chimecho and Staraptor are raised to their modern totals. Cresselia is not cut.
9. The ability pass considers Magic Guard on the Abra line, and Drizzle on Pelipper and Drought on Torkoal for trainers' Pokemon only.
10. A field move works once its badge is earned, with no Pokemon needed to know or learn it. The Move Relearner stays in Pastoria City at one Heart Scale per move, and the portable PC does not carry the relearner the base ROM gave it.

## Appendix A: native moves still at their Generation 4 power that four or more references modernise

"References" counts the hacks with data for that move that use the modern value. The last column names the Platinum hacks among them. Accuracy and PP are left out here because only four references carry accuracy and five carry PP. The accuracy and PP rows in the moves table name the ones that matter.

| Move | Change | References | Platinum hacks |
|---|---|---|---|
| Air Cutter | 55 to 60 | 6 of 7 | Renegade, Kaizo |
| Bullet Seed | 10 to 25 | 6 of 7 | Renegade, Kaizo |
| Drain Punch | 60 to 75 | 6 of 7 | Renegade, Kaizo |
| Fury Cutter | 10 to 40 | 6 of 7 | Renegade, Redux |
| Future Sight | 80 to 120 | 6 of 6 | Renegade, Kaizo |
| Giga Drain | 60 to 75 | 6 of 7 | Renegade, Kaizo |
| Icicle Spear | 10 to 25 | 6 of 7 | Renegade, Kaizo |
| Pin Missile | 14 to 25 | 6 of 7 | Renegade, Kaizo |
| Power Gem | 70 to 80 | 6 of 7 | Renegade, Redux |
| Thrash | 90 to 120 | 6 of 7 | Renegade, Kaizo |
| Covet | 40 to 60 | 5 of 6 | Renegade |
| Crabhammer | 90 to 100 | 5 of 7 | Renegade |
| Doom Desire | 120 to 140 | 5 of 7 | Renegade |
| Energy Ball | 80 to 90 | 5 of 7 | Renegade |
| Fire Spin | 15 to 35 | 5 of 7 | Renegade |
| High Jump Kick | 100 to 130 | 5 of 7 | Renegade |
| Jump Kick | 85 to 100 | 5 of 6 | Renegade |
| Last Resort | 130 to 140 | 5 of 7 | Renegade |
| Petal Dance | 90 to 120 | 5 of 7 | Renegade |
| Rock Tomb | 50 to 60 | 5 of 7 | Renegade |
| Skull Bash | 100 to 130 | 5 of 6 | Renegade |
| Smelling Salts | 60 to 70 | 5 of 6 | Renegade |
| Tackle | 35 to 40 | 5 of 7 | Renegade |
| Thief | 40 to 60 | 5 of 6 | Renegade |
| Vine Whip | 35 to 45 | 5 of 7 | Renegade |
| Wake-Up Slap | 60 to 70 | 5 of 6 | Renegade |
| Whirlpool | 15 to 35 | 5 of 7 | Renegade |
| Sand Tomb | 15 to 35 | 4 of 6 | none |
| Aura Sphere | 90 to 80 | 5 of 7 | Renegade |
| Sucker Punch | 80 to 70 | 5 of 7 | Renegade |
| Fire Blast | 120 to 110 | 5 of 7 | Renegade, Redux |
| Thunder | 120 to 110 | 5 of 7 | Renegade, Redux |
| Blizzard | 120 to 110 | 5 of 7 | Renegade, Redux |
| Hydro Pump | 120 to 110 | 5 of 7 | Renegade |
| Leaf Storm | 140 to 130 | 5 of 7 | Renegade, Redux |
| Draco Meteor | 140 to 130 | 4 of 7 | Renegade |
| Overheat | 140 to 130 | 4 of 7 | Renegade |
| Magma Storm | 120 to 100 | 4 of 7 | Renegade |
| Meteor Mash | 100 to 90 | 4 of 7 | Renegade |
| Thunderbolt | 95 to 90 | 4 of 7 | Renegade |
| Flamethrower | 95 to 90 | 4 of 7 | Renegade |
| Ice Beam | 95 to 90 | 4 of 7 | Renegade |
| Surf | 95 to 90 | 4 of 7 | Renegade |
| Muddy Water | 95 to 90 | 4 of 6 | Renegade |
| Heat Wave | 100 to 95 | 4 of 7 | Renegade |
| Dragon Pulse | 90 to 85 | 4 of 7 | Renegade |
| Hidden Power | IV formula to 60 | 4 of 7 | none |

The first 28 rows are buffs recommended in point 1 above. The other three of the 31 are Chatter (60 to 65), Luster Purge and Mist Ball (70 to 95), which fewer references modernise. From Aura Sphere down, the rows are the Generation 6 cuts, which are question 1's second half, followed by Hidden Power.

## Sources

- Renegade Platinum wiki: [home](https://fredericdlugi.github.io/platinum-renegade-wiki/), [Pokemon changes](https://fredericdlugi.github.io/platinum-renegade-wiki/pokemons/general_changes/), [move changes](https://fredericdlugi.github.io/platinum-renegade-wiki/move_changes/), [type changes](https://fredericdlugi.github.io/platinum-renegade-wiki/type_changes/), [changelog](https://fredericdlugi.github.io/platinum-renegade-wiki/changelog/)
- Sacred Gold and Storm Silver: [GameBrew](https://www.gamebrew.org/wiki/Pokemon_Sacred_Gold_and_Storm_Silver)
- Radical Red: [GameBrew](https://www.gamebrew.org/wiki/Pokemon_Radical_Red_GBA); move numbers from the Radical Red patch in the vendored calculator's move data
- Pokemon Unbound: [Flamethrower in the Unbound dex](https://pokemonunboundpokedex.com/moves/Flamethrower)
- Inclement Emerald: [PokeCommunity thread](https://www.pokecommunity.com/threads/pok%C3%A9mon-inclement-emerald-a-decomp-difficulty-hack-version-1-13.457039/). The page itself could not be fetched, so the entries citing it rest on a search summary
- pokeemerald-expansion's battle configuration: [include/config/battle.h](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/include/config/battle.h)
- hg-engine at commit 5157c50 (`~/hg-engine`): move and species data, the hidden ability table, the critical-hit and speed code, and the Drizzle battle script
- Platinum Kaizo's own documentation, `Platinum Kaizo Docs.xlsx` on G:, whose Move Changes and Ability Changes sheets agree with its calculator data
