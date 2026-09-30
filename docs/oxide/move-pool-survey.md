# Platinum Oxide: move pool survey

Written 2026-09-27 on `cloud/balance-move-survey`, for Ian's request of the same day: scope a cull of useless, outclassed and niche moves from learnsets, so the field of moves is easier to balance. It changes no game data. `tools/oxide/move_pool_survey.py` regenerates every count here from the tree, and `move-pool-survey.csv` beside this file is the per-move table for a spreadsheet. The same table closes this file as an appendix.

Ian answered its eight questions on 2026-09-27; the ruling is the tracker's entry "The move pool, first cut" (its archive once done), and it differs from the recommended first cut below: terrain is not ported, so the four Terrain moves go; Magic Room, Teatime, Octolock, Sky Drop, Salt Cure and Steel Roller stay and get their effects; Splash and Teleport go too. The cut is not in the tree yet (Telekinesis is still in the Gothita line's lists); the balance track applies it in its learnset pass. The engine table below is `4297c5ad8`'s: since then `cloud/element4-partial-moves`, merged, has written every partly working move still learnable, Mind Blown's cost and Magic Room's effect among them, and left the status moves the cut removes as plain hits.

## What it found

The recommended first cut is 13 moves off 14 lines, and it costs nothing on any measure the survey takes: no line loses an early attack or its last level-1 move, no trainer's default set changes, and no TM or tutor loses its move. Eleven of the 13 are status moves that never carry out their effect in Oxide, and the other two, Sky Drop and Salt Cure, are plain hits in Oxide that moves the same lines also learn beat outright. If terrain stays out of Oxide, the four Terrain moves and Steel Roller go too, again at no cost, for 18.

Every other group the brief names has a price, and several wait on decisions not yet made, the TM pass first. Four things should be read before the tables.

The pool is 619 moves, not the 716 the brief quotes. That is every move any species or form in the tree learns by level-up, TM, HM, tutor or egg on `origin/oxide` at 4297c5ad8. No unmerged branch that touches a learnset adds a learnable move, so the 716 must have been counted another way; this survey uses 619 throughout.

The 159 new species have empty TM, tutor and egg lists until the Phase 5 TM pass (tracker, element 3), so they learn by level-up only. 84 of the 239 obtainable lines contain a new species. Of the 156 moves that only one or two obtainable lines learn, 113 are learned only by such lines, so most of the niche group will shrink once the TM pass runs.

The survey found 30 learnable moves that Oxide's engine does not run in full. Eight are the terrain moves the tracker already holds back. The other 22 were not on the element 4 list (apart from Flower Shield and Teatime, which the 2026-09-22 QA noted), because the converter's audit works effect by effect, and these moves carry a plain-hit or Platinum effect in their record while hg-engine does their real work in C keyed on the move id, or not at all. One matters for balance at once: Mind Blown is a 150-power Fire special hit with no cost to its user. These are element 4 findings whatever the cull decides; the tracker archive's "Moves the effect audit missed" records how element 4 dealt with them.

Nothing here has been seen in game. The engine claims come from reading Oxide's `src/battle/` and a shallow clone of hg-engine taken on 2026-09-27; the cloud session has neither the base ROM nor the donor ROM, so `convert_battle_scripts.py --audit` could not be run.

## The pool in numbers

| | Count |
|---|---|
| Moves any species or form can learn | 619 |
| learned by at least one obtainable line | 602 |
| learned only by lines the player cannot obtain | 17 |
| Evolution lines in the tree | 327 |
| obtainable (a member is `native` or `new` in the pick-list) | 239 |
| obtainable lines that contain a new species | 84 |
| Moves an obtainable line learns by level-up | 595 |
| by TM or HM (100 machines, all of them used) | 100 |
| by tutor (38 tutor moves, all used) | 38 |
| as an egg move | 253 |
| Obtainable moves that are physical, special, status | 240, 145, 217 |
| Engine runs the move in full | 572 |
| status move that never carries out its effect | 15 |
| runs in part (the table below) | 14 |
| a stub that hits when it should fail (Steel Roller) | 1 |
| Trainers some map in the game fields | 567 |
| whose party takes default level-up moves | 75 |
| Moves in at least one such default set | 159 |

How many obtainable lines learn each move:

| Lines | 0 | 1 | 2 | 3 | 4 | 5 | 6 to 9 | 10 or more |
|---|---|---|---|---|---|---|---|---|
| Moves | 17 | 111 | 45 | 44 | 35 | 24 | 69 | 274 |

## How the survey counts

A line is an evolution family, as the encounter tool builds them from each species' evolutions, and it is obtainable when any member is `native` or `new` in `species-pick-list.csv`. A move counts for a line when any member or form learns it by any route. The first level is the lowest level-up level across the line.

Trainer uses count only the 567 trainers that the balance track's split resolver finds on a map or in a script; a few with `_unused` in their names are among them because a script names them. A party whose first member lists no moves takes default moves, which the game builds by walking the learnset up to the Pokemon's level and keeping the last four. The survey rebuilds those sets with the encounter tool's `default_moves`, so a cut shows exactly which trainers' sets change and to what.

The early-game cost of a cut is measured at the first two level caps, Roark's 16 and Gardenia's 26. For each obtainable line it counts the attacks the line has by level-up at or below the cap, before and after the cut, and flags the line when it drops below two attacks or loses its last attack of its own type. A first stage's level-1 moves count; a later stage's level-1 moves are its evolution and relearner moves, so they do not.

A move is outclassed when another move of the same type and category beats it on power and accuracy, is at least as fast, costs its user nothing (no recoil, recharge, charge turn, self-drop or lock-in), and either the weaker move has no effect or the better one has the same effect at no lower chance. Moves whose effect Oxide's battle C handles by name (Psyshock, Body Press, Echoed Voice, Rage Fist, Retaliate and the rest) are left out of the comparison, since their record understates them. PP is ignored between attacks, and setup moves are never judged on PP, because their low PP is deliberate (staples survey, answer 1).

## Moves the engine does not run in full

Every one of these is learned by level-up only, by new-species lines, and appears in no trainer's party, hand-set or default.

| Move | Lines | First lv | What Oxide does |
|---|---|---|---|
| Electric Terrain, Grassy Terrain, Misty Terrain, Psychic Terrain | 2, 2, 4, 1 | 60, 23, 1, 75 | "But nothing happened!" until terrain is decided |
| Steel Roller | 2 | 1 | a plain 130-power Steel hit; the modern move fails without terrain |
| Telekinesis, Magic Room, Ally Switch, Topsy-Turvy, Flower Shield, Fairy Lock, Aromatic Mist, Magnetic Flux, Speed Swap, Teatime, Octolock | 1 to 3 each | 1 to 55 | a status move running the plain-hit script, so its effect never happens |
| Mind Blown | 1 | 70 | a plain 150 hit; the user's loss of half its HP is missing |
| Scale Shot | 1 | 45 | hits two to five times; the Speed rise and Defense drop are missing |
| Spiky Shield, Baneful Bunker | 2, 1 | 1, 1 | a plain Protect; the contact damage and the poison are missing |
| Beak Blast | 1 | 1 | a priority -3 hit; the burn on contact while it heats up is missing |
| Core Enforcer | 1 | 1 | a plain hit; the ability suppression is missing, in hg-engine too |
| Salt Cure | 1 | 1 | a plain 40 hit; the damage every turn is missing, in hg-engine too |
| Sky Drop | 1 | 20 | a plain 60 hit; the two-turn lift is missing |
| Flame Burst | 3 | 17 | a plain hit; the splash on the target's partner, a doubles effect, is missing |
| Shore Up | 1 | 52 | heals more in sun, as Morning Sun does, instead of in sandstorm |
| Expanding Force, Grassy Glide, Terrain Pulse | 2, 1, 1 | 56, 46, 38 | plain hits; the terrain part waits on terrain |
| Nature's Madness | 4 | 55 | halves HP, but its table power is 0 where every computed power keeps 1, so the type chart reads it as a status move |

What the eleven status moves do exactly was not traced. The plain-hit script runs Platinum's damage command, whose formula adds 2 after the multiply, so each may deal a point or two of damage or none; either way the effect in its text never happens.

## The candidates, by reason

### Dead in Oxide

The eleven status moves above and the four Terrains. The eleven are the core of the first cut: each is on one to three new-species lines by level-up alone, no trainer uses one, none is a TM or a tutor move, and their removal leaves no line short of an early attack or a level-1 move. Porting them instead is C work for each, and hg-engine does not implement several of them either. The four Terrains, and Steel Roller with them, follow Ian's terrain decision.

### Strictly outclassed

Eight moves are beaten, on every obtainable line that learns them, by a move the same line also learns.

| Move | Lines | Beaten by | Lines that have the better move by the same level |
|---|---|---|---|
| Sky Drop | 1 | Aerial Ace | 1 |
| Salt Cure | 1 | Rock Tomb, Rock Throw, Smack Down | 0 |
| Land's Wrath | 1 | Earthquake | 0 |
| Flame Burst | 3 | Mystical Fire, Flamethrower | 0 |
| Sludge | 2 | Sludge Bomb | 0 |
| Leafage | 5 | Razor Leaf, Leaf Blade, Seed Bomb | 1 |
| Vine Whip | 3 | Seed Bomb, Razor Leaf, Leaf Blade | 0 |
| Water Gun | 32 | Water Pulse, Surf, Bubble Beam | 7 |

"Strictly" holds for the whole game but rarely for the moment the weaker move is learned. Water Gun, Vine Whip and Leafage are level-1 moves, and cutting them leaves 11 lines short before Roark: Buizel, Carnivine, Totodile, Finneon, Psyduck, Snivy, Staryu and Tapu Bulu lose their last attack of their own type, and Horsea, Wingull and Tapu Fini fall to a single attack. It also changes three trainers' default sets (a Psyduck and a Marill lose Water Gun for Tail Whip, a Carnivine loses Vine Whip for Bite). Sky Drop and Salt Cure cost nothing, since both are plain hits in Oxide anyway, and they are in the first cut. Land's Wrath (Zygarde's signature), Flame Burst and Sludge are mid-game moves whose loss costs no early attack; they are a question below.

### Outclassed on most lines

Another 29 attacks are beaten on some of their lines but not all. Most are the early game's attacks, beaten on most of their lines: Tackle (36 of 66 lines), Ember (16 of 19), Scratch (14 of 18), Mega Drain (14 of 16), Absorb and Bubble (13 of 16), Peck (12 of 18), Confusion (12 of 31), Wing Attack (11 of 12), Poison Sting, Thunder Shock and Rock Throw (10 of 12, 11 and 13), Powder Snow (8 of 9). The moves that beat them come by TM or at mid levels, and Water Gun, from the table above, is the same case. As a test, cutting the twelve most common of them leaves 74 lines with fewer than two early attacks or none of their own type, 37 first stages with no level-1 move at all, and 12 trainer Pokemon with different default moves. They stay; the survey lists them only so the cull does not reach for them by accident.

### Near-duplicates

These are groups where two or more moves do the same job and differ in type, accuracy or a detail. Setup moves are listed for completeness only, since their PP is set on purpose.

| Job | Moves (obtainable lines) |
|---|---|
| Sleep | Spore 100% (1), Dark Void 80% (1), Sleep Powder 75% (4), Lovely Kiss 75% (1), Hypnosis 60% (26), Sing 55% (13), Grass Whistle 55% (6) |
| Accuracy down one stage | Flash (75, TM70), Sand-Attack (19), Smokescreen (8), Kinesis (1) |
| Attack down one stage | Growl (47), Baby-Doll Eyes (4, priority), Play Nice (3, never misses) |
| Attack down two stages | Charm (29), Feather Dance (11) |
| Defense down one stage | Leer (40), Tail Whip (22) |
| Speed down two stages | Scary Face (29), Cotton Spore (3) |
| Sp. Def down two stages | Fake Tears (15), Metal Sound (9) |
| Paralysis | Thunder Wave (55), Stun Spore 75% (9), Glare (2) |
| Confusion | Confuse Ray (32), Sweet Kiss (12), Supersonic 55% (23) |
| Poison | Poison Powder 75% (4), Poison Gas 85% (2) |
| Phazing | Roar (50), Whirlwind (17) |
| Trapping | Mean Look (14), Block (14), Spider Web (2) |
| Next attack hits | Lock-On (7), Mind Reader (8) |
| Party status cure | Aromatherapy (10), Heal Bell (4) |
| Identify | Foresight (21), Odor Sleuth (9) |
| Heal half | Recover (18), Slack Off (3), Soft-Boiled (1), Heal Order (1) |
| Heal half, more in weather | Synthesis (23), Moonlight (4), Morning Sun (3), Shore Up (1) |
| Protect | Protect (167), Detect (11), and in Oxide Spiky Shield (2) and Baneful Bunker (1) |
| Setup: Defense up two | Iron Defense (36), Barrier (11), Acid Armor (6), Shelter (1) |
| Setup: Speed up two | Agility (44), Rock Polish (27) |
| Setup: Sp. Atk up two | Nasty Plot (23), Tail Glow (1) |
| Setup: Attack up one | Meditate (7), Howl (4), Sharpen (2) |
| 40-power Normal hit | Tackle (66), Scratch (18), Pound (16) |
| Multi-hit Normal | Fury Attack (16), Double Slap (14), Fury Swipes (13), Spike Cannon (3), Tail Slap (1) |
| Binding | Wrap (8), Bind (6) |
| Leave at 1 HP | False Swipe (18), Hold Back (1) |
| Never-miss Steel | Magnet Bomb 60 (2), Smart Strike 70 (2) |
| Fire, burn chance | Flamethrower 90 (47), Heat Wave 95 (23), Lava Plume 80 (5) |
| Electric, paralysis chance | Thunderbolt 90 (61), Discharge 80 (16) |
| Poison, poison chance | Sludge Bomb 90 (30), Sludge Wave 95 (2); Smog 55 (10), Sludge 65 (2) |
| Psychic, Sp. Def drop | Psychic 90 (55), Luster Purge 95 (1) |
| Dark, flinch | Dark Pulse 80 (35), Fiery Wrath 90 (1) |
| Normal, flinch | Headbutt 70 (19), Hyper Fang 80 (1) |
| Grass physical | Seed Bomb 80 (27), Petal Blizzard 90 (2) |

A duplicate cull simplifies the list more than it simplifies balance. Within each status group the balance knob is accuracy, which Ian can set per move whether or not the group shrinks, and a type-flavoured copy (Sing for a Normal line, Grass Whistle for a Grass one) is often the only way its line gets the job at all. The survey recommends leaving this group alone in the first cut; the question below is whether Ian wants one move per job.

### Doubles-only

| Move | Lines | Notes |
|---|---|---|
| Helping Hand | 51 | also the Snowpoint City tutor; 18 lines by level-up, 5 as an egg move |
| Wide Guard | 8 | blocks spread moves, which singles rarely meet |
| Heal Pulse | 4 | in singles its only target is the foe |
| After You | 4 | no use in singles |
| Follow Me | 3 | in the default moves of three trainer Clefairy, Lady Kylie's in Wake's split and Idol Grace's two after the League |
| Rage Powder | 2 | |
| Coaching | 1 | fails without a partner |
| Ally Switch, Aromatic Mist, Flower Shield, Magnetic Flux | 2, 3, 1, 1 | already in the first cut as dead in Oxide |

Oxide fields 16 double battles (Maylene's split 6, the post-game 6, the League 2, Byron's and Gardenia's 1 each), and element 8 was to bring wild double battles (dropped, Ian, 2026-09-29). Cutting all eleven touches 69 lines, empties the Helping Hand tutor and changes those three Clefairy's moves; the question below is whether any should stay.

### Moves that do nothing useful

Splash does nothing and Teleport only flees a wild battle, but each is some first stage's only level-1 move: Splash for Azurill, Bounsweet, Feebas, Hoppip and Wailmer, Teleport for Abra. Cutting them needs a replacement level-1 move for those six, and changes the default moves of four trainer Pokemon (two Feebas, a Ralts and a Kirlia). Celebrate, Hold Hands and Happy Hour are in no learnset.

The HM moves become ordinary attacks once field moves work on their badge alone (element 8, staples survey answer 10). Cut (50 power, HM01, 53 lines) is beaten on 47 of them, and Rock Smash (40 power, HM06) is on 107 lines. With TM70 Flash (75 lines, an accuracy drop) they are the most widespread weak moves in the pool, and the TM pass can turn all three into other moves. Cutting them from learnsets costs three lines an early attack (Clobbopus, Mienfoo and Tapu Bulu, all Rock Smash).

### Niche moves

156 moves are learned by one or two obtainable lines, and 100 of those by exactly one line of all 327. As above, 113 are there because the new species' TM, tutor and egg lists are empty. The 43 native ones are mostly signatures: the legendaries' (Roar of Time, Spacial Rend, Judgment, Seed Flare, Magma Storm, Shadow Force, Crush Grip, Lunar Dance, Luster Purge, Mist Ball), Platinum's own (Chatter, Volt Tackle, the three Orders), and older moves whose other users are not obtainable (Crabhammer, Egg Bomb, Hyper Fang, Dizzy Punch, Tri Attack, Spore, Softboiled, Metal Burst). Rarity alone is not a reason to cut before the TM pass, and a signature is part of its species; the survey recommends cutting a niche move only when it is also dead or outclassed.

### Learned only by lines the player cannot obtain

Seventeen moves (Aeroblast, Barrage, Bone Club, Bonemerang, Comet Punch, Conversion, Conversion 2, Doom Desire, Eruption, Mega Kick, Milk Drink, Needle Arm, Pay Day, Psycho Boost, Sacred Fire, Sketch, Transform) are in no obtainable line's learnset, so they are not in the player's pool at all. Several are in trainers' hand-set parties (Eruption in four), and Sketch is in one default set. Nothing to cut.

### Weather, already leaving

Ian's ruling (staples survey, answer 6) takes every weather move out of player learnsets, TMs, tutors and egg lists. Four are learnable today: Rain Dance (132 lines, TM18), Sunny Day (116, TM11), Sandstorm (54, TM37) and Hail (53, TM07), and 50 trainers, who keep theirs, use one (Rain Dance 25, Sandstorm 12, Sunny Day 11, Hail 2). The TM pass carries this; the survey counts them apart from the cull.

## What a removal costs

| Set | Moves | Lines touched | Lines left short before a cap | First stages left with no level-1 move | Trainer Pokemon whose default moves change | TMs and tutors emptied | One-line moves lost |
|---|---|---|---|---|---|---|---|
| Recommended first cut | 13 | 14 | 0 | 0 | 0 | 0 | 10 |
| The terrain five | 5 | 11 | 0 | 0 | 0 | 0 | 1 |
| Strictly outclassed | 8 | 48 | 11 | 0 | 3 | 0 | 3 |
| The twelve most common early attacks | 12 | 166 | 74 | 37 | 12 | 0 | 0 |
| Doubles-only | 11 | 69 | 0 | 0 | 3 | 1 | 3 |
| Splash and Teleport | 2 | 16 | 0 | 6 | 4 | 0 | 0 |
| The seven partly run, if cut instead of fixed | 7 | 8 | 0 | 0 | 0 | 0 | 5 |
| Cut, Rock Smash and Flash | 3 | 149 | 3 | 0 | 0 | 3 | 0 |

The one-line moves lost in the first cut are ten moves that only one line in the tree learns (Speed Swap is Pheromosa's, Salt Cure the Nacli line's, and so on), so each cut takes something from a species' character even where the move does nothing today. A cut applies to obtainable lines only in every row: a species the player cannot obtain keeps its learnset, so trainers using it keep their default sets.

## Questions for Ian (answered 2026-09-27; see the note at the top)

1. Terrain: is it ported? If not, the four Terrain moves and Steel Roller leave learnsets (five more, at no cost), and Expanding Force, Grassy Glide and Terrain Pulse stay as plain hits.
2. The partly run moves: fix or cut? Mind Blown needs one or the other before the balance scores trust it; Scale Shot, Spiky Shield, Baneful Bunker, Beak Blast and Shore Up are small C each from hg-engine; Core Enforcer and Salt Cure have no hg-engine code to port.
3. Doubles-only moves, with 16 double battles and wild doubles coming: keep all, keep some (Helping Hand and Follow Me are the ones trainers and a tutor use), or cut all.
4. Splash and Teleport: cut them and give Azurill, Bounsweet, Feebas, Hoppip, Wailmer and Abra a level-1 move in their place? If so, which.
5. Once field moves need only a badge, do Cut, Rock Smash and Flash stay as attacks, or does the TM pass turn HM01, HM06 and TM70 into other moves?
6. Near-duplicates: one move per job (one sleep move, one accuracy drop), or keep the type-flavoured copies and balance each by accuracy?
7. The mid-game outclassed moves Land's Wrath, Flame Burst and Sludge: cut, or keep as flavour?
8. Should the rest of the cull wait for the TM pass, since the new species' empty lists make 113 moves look rarer than they will be?

## Recommended first cut

Thirteen moves, off fourteen lines, by level-up only:

| Move | Species that learn it, at level |
|---|---|
| Telekinesis | Gothita 40, Gothorita 43, Gothitelle 45 |
| Magic Room | Gothita 48, Gothorita 55, Gothitelle 61, Fennekin 54, Braixen 58, Delphox 61, Klefki 44 |
| Ally Switch | Galarian Mr. Mime 16, Mr. Rime 16, Armarouge 42, Ceruledge 42 |
| Topsy-Turvy | Grapploct 50 |
| Flower Shield | Florges 1 |
| Fairy Lock | Klefki 1 |
| Aromatic Mist | Bounsweet 33, Steenee 32, Tapu Lele 30, Sinistea 6, Polteageist 1 |
| Magnetic Flux | Magearna 24 |
| Speed Swap | Pheromosa 55 |
| Teatime | Polteageist 1 |
| Octolock | Grapploct 1 |
| Sky Drop | Hawlucha 20 |
| Salt Cure | Naclstack 1, Garganacl 24 |

It is a data change to those species' `learnset.by_level` lists and nothing else. Rerunning `move_pool_survey.py --report` afterwards should show 606 learnable moves and the first cut's cost row all zeros. If Ian leaves terrain out, the terrain five follow (Electric Terrain: Tapu Koko, Xurkitree; Grassy Terrain: Tapu Bulu, Smoliv, Dolliv, Arboliva; Misty Terrain: Galarian Mr. Mime, Mr. Rime, Sylveon, Xerneas, Tapu Fini; Psychic Terrain: Tapu Lele; Steel Roller: Togedemaru, Dhelmise) for 18. The weather four leave by the standing ruling in the TM pass, which would make 22 moves gone from the player's pool. Everything else waits on the questions above.

## Appendix: every learnable move

One row per move any species or form learns, 619 in all, sorted by name. "Lines" counts obtainable lines; the four route columns count the obtainable lines that learn it that way; "First lv" is the lowest level-up level across them; "Trainer defaults" counts trainers whose default set contains it. "Engine" is `runs`, `no effect` (the status moves above and the Terrains), `partial` (the other rows of the engine table) or `stub, hits` (Steel Roller). Accuracy `always` is a move that never misses. The CSV beside this file adds priority, the tutor's location, hand-set trainer uses and the unobtainable lines that learn each move.

| Move | Type | Cat. | Pow. | Acc. | PP | Effect | Engine | Lines | Lv | TM | Tutor | Egg | First lv | Taught by | Trainer defaults |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Absorb | Grass | Spec. | 20 | 100 | 25 | recover half damage dealt | runs | 16 | 16 |  |  |  | 1 |  | 1 |
| Accelerock | Rock | Phys. | 40 | 100 | 20 | priority 1 | runs | 1 | 1 |  |  |  | 55 |  |  |
| Acid | Poison | Spec. | 40 | 100 | 30 | lower sp. def hit (10%) | runs | 4 | 4 |  |  |  | 1 |  |  |
| Acid Armor | Poison | Stat. |  | always | 1 | def up 2 | runs | 6 | 5 |  |  | 1 | 1 |  |  |
| Acid Spray | Poison | Spec. | 40 | 100 | 20 | lower sp. def 2 hit | runs | 2 | 2 |  |  |  | 7 |  |  |
| Acrobatics | Flying | Phys. | 55 | 100 | 15 | double damage without item | runs | 8 | 8 |  |  |  | 22 |  |  |
| Acupressure | Normal | Stat. |  | always | 30 | random stat up 2 | runs | 2 | 1 |  |  | 1 | 17 |  | 1 |
| Aerial Ace | Flying | Phys. | 60 | always | 20 | bypass accuracy | runs | 61 | 7 | 58 |  |  | 1 | TM40 |  |
| Aeroblast | Flying | Spec. | 100 | 95 | 5 | high critical | runs | 0 |  |  |  |  |  |  |  |
| After You | Normal | Stat. |  | always | 15 | after you | runs | 4 | 4 |  |  |  | 1 |  |  |
| Agility | Psychic | Stat. |  | always | 1 | speed up 2 | runs | 44 | 34 |  |  | 12 | 9 |  | 3 |
| Air Cutter | Flying | Spec. | 60 | 100 | 25 | high critical | runs | 28 | 4 |  | 26 |  | 1 | tutor |  |
| Air Slash | Flying | Spec. | 75 | 95 | 15 | flinch hit (30%) | runs | 18 | 18 |  |  |  | 1 |  | 1 |
| Ally Switch | Psychic | Stat. |  | always | 15 | plain hit | no effect | 2 | 2 |  |  |  | 16 |  |  |
| Amnesia | Psychic | Stat. |  | always | 1 | sp. def up 2 | runs | 30 | 15 |  |  | 15 | 9 |  |  |
| Anchor Shot | Steel | Phys. | 90 | 100 | 20 | prevent escape hit | runs | 1 | 1 |  |  |  | 34 |  |  |
| AncientPower | Rock | Spec. | 60 | 100 | 5 | raise all stats hit (10%) | runs | 49 | 26 |  | 42 | 12 | 1 | tutor | 1 |
| Aqua Jet | Water | Phys. | 40 | 100 | 20 | priority 1 | runs | 9 | 7 |  |  | 2 | 1 |  |  |
| Aqua Ring | Water | Stat. |  | always | 20 | restore hp every turn | runs | 18 | 15 |  |  | 6 | 5 |  | 1 |
| Aqua Tail | Water | Phys. | 90 | 100 | 10 | plain hit | runs | 37 | 11 |  | 35 | 4 | 28 | tutor |  |
| Arm Thrust | Fighting | Phys. | 15 | 100 | 20 | multi hit | runs | 2 | 2 |  |  |  | 1 |  |  |
| Armor Cannon | Fire | Spec. | 120 | 100 | 5 | def spd down hit | runs | 1 | 1 |  |  |  | 62 |  |  |
| Aromatherapy | Grass | Stat. |  | always | 5 | cure party status | runs | 10 | 7 |  |  | 3 | 1 |  |  |
| Aromatic Mist | Fairy | Stat. |  | always | 20 | plain hit | no effect | 3 | 3 |  |  |  | 1 |  |  |
| Assist | Normal | Stat. |  | always | 20 | use random ally move | runs | 4 | 3 |  |  | 1 | 1 |  |  |
| Assurance | Dark | Phys. | 70 | 100 | 10 | double power if target hit | runs | 16 | 12 |  |  | 4 | 1 |  | 1 |
| Astonish | Ghost | Phys. | 30 | 100 | 15 | flinch hit (30%) | runs | 31 | 26 |  |  | 5 | 1 |  | 1 |
| Attack Order | Bug | Phys. | 120 | 100 | 15 | poison hit (30%) | runs | 1 | 1 |  |  |  | 37 |  |  |
| Attract | Normal | Stat. |  | 100 | 15 | infatuate | runs | 137 | 9 | 135 |  | 1 | 1 | TM45 |  |
| Aura Sphere | Fighting | Spec. | 80 | always | 20 | bypass accuracy | runs | 8 | 8 |  |  |  | 1 |  |  |
| Aurora Beam | Ice | Spec. | 65 | 100 | 20 | lower attack hit (10%) | runs | 14 | 11 |  |  | 4 | 1 |  |  |
| Aurora Veil | Ice | Stat. |  | always | 20 | set aurora veil | runs | 2 | 2 |  |  |  | 1 |  |  |
| Autotomize | Normal | Stat. |  | always | 15 | autotomize | runs | 2 | 2 |  |  |  | 30 |  |  |
| Avalanche | Ice | Phys. | 60 | 100 | 10 | double power if hit | runs | 35 | 1 | 35 |  |  | 31 | TM72 |  |
| Baby-Doll Eyes | Fairy | Stat. |  | 100 | 10 | atk down | runs | 4 | 4 |  |  |  | 1 |  |  |
| Baneful Bunker | Poison | Stat. |  | always | 5 | protect | partial | 1 | 1 |  |  |  | 1 |  |  |
| Barrage | Normal | Phys. | 15 | 85 | 20 | multi hit | runs | 0 |  |  |  |  |  |  |  |
| Barrier | Psychic | Stat. |  | always | 1 | def up 2 | runs | 11 | 4 |  |  | 7 | 1 |  | 1 |
| Baton Pass | Normal | Stat. |  | always | 40 | pass stats and status | runs | 21 | 14 |  |  | 7 | 1 |  | 8 |
| Beak Blast | Flying | Phys. | 120 | 100 | 5 | plain hit | partial | 1 | 1 |  |  |  | 1 |  |  |
| Belch | Poison | Spec. | 120 | 100 | 10 | belch | runs | 2 | 2 |  |  |  | 18 |  |  |
| Belly Drum | Normal | Stat. |  | always | 1 | max atk lose half max hp | runs | 8 | 3 |  |  | 5 | 17 |  |  |
| Bide | Normal | Phys. | 1 | always | 10 | bide | runs | 10 | 7 |  |  | 3 | 1 |  | 1 |
| Bind | Normal | Phys. | 15 | 85 | 20 | bind hit | runs | 6 | 6 |  |  |  | 1 |  |  |
| Bite | Dark | Phys. | 60 | 100 | 25 | flinch hit (30%) | runs | 36 | 29 |  |  | 7 | 1 |  | 4 |
| Bitter Blade | Fire | Phys. | 90 | 100 | 10 | recover half damage dealt | runs | 1 | 1 |  |  |  | 48 |  |  |
| Blaze Kick | Fire | Phys. | 85 | 90 | 10 | high critical burn hit (10%) | runs | 4 | 3 |  |  | 1 | 26 |  |  |
| Blizzard | Ice | Spec. | 110 | 70 | 5 | blizzard (10%) | runs | 74 | 10 | 72 |  |  | 1 | TM14 |  |
| Block | Normal | Stat. |  | always | 5 | prevent escape | runs | 14 | 10 |  |  | 5 | 1 |  |  |
| Body Press | Fighting | Phys. | 80 | 100 | 10 | plain hit | runs | 4 | 4 |  |  |  | 1 |  |  |
| Body Slam | Normal | Phys. | 85 | 100 | 15 | paralyze hit (30%) | runs | 26 | 13 |  |  | 13 | 18 |  |  |
| Bone Club | Ground | Phys. | 65 | 85 | 20 | flinch hit (10%) | runs | 0 |  |  |  |  |  |  |  |
| Bone Rush | Ground | Phys. | 25 | 90 | 10 | multi hit | runs | 2 | 2 |  |  |  | 1 |  |  |
| Bonemerang | Ground | Phys. | 50 | 100 | 10 | hit twice | runs | 0 |  |  |  |  |  |  |  |
| Boomburst | Normal | Spec. | 140 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 58 |  |  |
| Bounce | Flying | Phys. | 85 | 100 | 5 | bounce (30%) | runs | 30 | 11 |  | 26 | 1 | 16 | tutor |  |
| Brave Bird | Flying | Phys. | 120 | 100 | 15 | recoil third | runs | 10 | 8 |  |  | 2 | 1 |  |  |
| Breaking Swipe | Dragon | Phys. | 60 | 100 | 15 | lower attack hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Brick Break | Fighting | Phys. | 75 | 100 | 15 | remove screens | runs | 71 | 4 | 68 |  |  | 8 | TM31 |  |
| Brine | Water | Spec. | 65 | 100 | 10 | double power when below half | runs | 34 | 13 | 32 |  |  | 1 | TM55 |  |
| Brutal Swing | Dark | Phys. | 60 | 100 | 20 | plain hit | runs | 1 | 1 |  |  |  | 16 |  |  |
| Bubble | Water | Spec. | 40 | 100 | 30 | lower speed hit (10%) | runs | 16 | 16 |  |  |  | 1 |  |  |
| BubbleBeam | Water | Spec. | 65 | 100 | 20 | lower speed hit (10%) | runs | 19 | 17 |  |  | 3 | 1 |  | 1 |
| Bug Bite | Bug | Phys. | 60 | 100 | 20 | eat berry | runs | 16 | 15 |  |  | 1 | 1 |  |  |
| Bug Buzz | Bug | Spec. | 90 | 100 | 10 | lower sp. def hit (10%) | runs | 13 | 12 |  |  | 1 | 32 |  | 3 |
| Bulk Up | Fighting | Stat. |  | always | 20 | atk def up | runs | 18 | 4 | 15 |  |  | 20 | TM08 |  |
| Bulldoze | Ground | Phys. | 60 | 100 | 20 | lower speed hit | runs | 3 | 3 |  |  |  | 1 |  |  |
| Bullet Punch | Steel | Phys. | 40 | 100 | 30 | priority 1 | runs | 7 | 2 |  |  | 5 | 1 |  |  |
| Bullet Seed | Grass | Phys. | 25 | 100 | 30 | multi hit | runs | 21 | 5 | 18 |  |  | 1 | TM09 |  |
| Burn Up | Fire | Spec. | 130 | 100 | 5 | remove user fire type hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Calm Mind | Psychic | Stat. |  | always | 3 | sp. atk sp. def up | runs | 41 | 6 | 39 |  |  | 23 | TM04 | 7 |
| Camouflage | Normal | Stat. |  | always | 20 | camouflage | runs | 3 | 3 |  |  |  | 19 |  |  |
| Captivate | Normal | Stat. |  | 100 | 20 | sp. atk down 2 opposite gender | runs | 137 | 15 | 135 |  | 1 | 25 | TM78 | 3 |
| Charge | Electric | Stat. |  | always | 3 | sp. def up double electric power | runs | 12 | 11 |  |  | 2 | 1 |  | 2 |
| Charge Beam | Electric | Spec. | 50 | 100 | 10 | raise sp. atk hit (70%) | runs | 44 | 3 | 44 |  |  | 49 | TM57 |  |
| Charm | Fairy | Stat. |  | 100 | 20 | atk down 2 | runs | 29 | 22 |  |  | 8 | 1 |  | 2 |
| Chatter | Flying | Spec. | 65 | 100 | 20 | chatter | runs | 1 | 1 |  |  |  | 21 |  |  |
| Clamp | Water | Phys. | 35 | 85 | 15 | bind hit | runs | 2 | 2 |  |  |  | 1 |  |  |
| Clanging Scales | Dragon | Spec. | 110 | 100 | 5 | user def down hit | runs | 1 | 1 |  |  |  | 47 |  |  |
| Clear Smog | Poison | Spec. | 50 | always | 15 | clear smog | runs | 4 | 4 |  |  |  | 1 |  |  |
| Close Combat | Fighting | Phys. | 120 | 100 | 5 | def spd down hit | runs | 16 | 14 |  |  | 3 | 1 |  |  |
| Coaching | Fighting | Stat. |  | always | 10 | coaching | runs | 1 | 1 |  |  |  | 1 |  |  |
| Coil | Poison | Stat. |  | always | 20 | atk def acc up | runs | 1 | 1 |  |  |  | 72 |  |  |
| Comet Punch | Normal | Phys. | 18 | 85 | 15 | multi hit | runs | 0 |  |  |  |  |  |  |  |
| Confuse Ray | Ghost | Stat. |  | 100 | 10 | status confuse | runs | 32 | 23 |  |  | 9 | 1 |  | 1 |
| Confusion | Psychic | Spec. | 50 | 100 | 25 | confuse hit (10%) | runs | 31 | 28 |  |  | 3 | 1 |  | 6 |
| Constrict | Normal | Phys. | 10 | 100 | 35 | lower speed hit (10%) | runs | 5 | 5 |  |  |  | 1 |  |  |
| Conversion | Normal | Stat. |  | always | 30 | conversion | runs | 0 |  |  |  |  |  |  |  |
| Conversion 2 | Normal | Stat. |  | always | 30 | conversion2 | runs | 0 |  |  |  |  |  |  |  |
| Copycat | Normal | Stat. |  | always | 20 | use last used move | runs | 15 | 15 |  |  |  | 1 |  | 3 |
| Core Enforcer | Dragon | Spec. | 100 | 100 | 10 | plain hit | partial | 1 | 1 |  |  |  | 1 |  |  |
| Cosmic Power | Psychic | Stat. |  | always | 20 | def spd up | runs | 5 | 5 |  |  |  | 1 |  | 2 |
| Cotton Guard | Grass | Stat. |  | always | 10 | def up 3 | runs | 1 | 1 |  |  |  | 36 |  |  |
| Cotton Spore | Grass | Stat. |  | 100 | 40 | speed down 2 | runs | 3 | 2 |  |  | 1 | 19 |  |  |
| Counter | Fighting | Phys. | 1 | 100 | 20 | counter | runs | 23 | 7 |  |  | 17 | 1 |  |  |
| Covet | Normal | Phys. | 60 | 100 | 25 | steal held item | runs | 9 | 4 |  |  | 6 | 1 |  |  |
| Crabhammer | Water | Phys. | 100 | 95 | 10 | high critical | runs | 2 | 2 |  |  |  | 38 |  |  |
| Crafty Shield | Fairy | Stat. |  | always | 10 | protect user side | runs | 2 | 2 |  |  |  | 19 |  |  |
| Cross Chop | Fighting | Phys. | 100 | 80 | 5 | high critical | runs | 8 | 2 |  |  | 6 | 22 |  | 3 |
| Cross Poison | Poison | Phys. | 70 | 100 | 20 | high critical poison hit (10%) | runs | 3 | 2 |  |  | 1 | 1 |  |  |
| Crunch | Dark | Phys. | 80 | 100 | 15 | lower defense hit (20%) | runs | 33 | 27 |  |  | 8 | 1 |  | 4 |
| Crush Claw | Normal | Phys. | 75 | 95 | 10 | lower defense hit (50%) | runs | 4 |  |  |  | 4 |  |  |  |
| Crush Grip | Normal | Phys. | 1 | 100 | 5 | increase power with more hp | runs | 1 | 1 |  |  |  | 75 |  |  |
| Curse | Mystery | Stat. |  | always | 3 | curse | runs | 35 | 13 |  |  | 22 | 1 |  |  |
| Cut | Normal | Phys. | 50 | 100 | 30 | plain hit | runs | 53 | 1 | 52 |  |  | 15 | HM01 |  |
| Dark Pulse | Dark | Spec. | 80 | 100 | 15 | flinch hit (20%) | runs | 35 | 11 | 31 |  |  | 1 | TM79 |  |
| Dark Void | Dark | Stat. |  | 80 | 10 | status sleep | runs | 1 | 1 |  |  |  | 66 |  |  |
| Darkest Lariat | Dark | Phys. | 85 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 36 |  |  |
| Dazzling Gleam | Fairy | Spec. | 80 | 100 | 10 | plain hit | runs | 4 | 4 |  |  |  | 1 |  |  |
| Defend Order | Bug | Stat. |  | always | 10 | def spd up | runs | 1 | 1 |  |  |  | 13 |  |  |
| Defense Curl | Normal | Stat. |  | always | 3 | def up double rollout power | runs | 17 | 13 |  |  | 5 | 1 |  | 4 |
| Defog | Flying | Stat. |  | always | 15 | remove hazards screens eva down | runs | 39 | 7 | 32 |  |  | 1 | HM05 |  |
| Destiny Bond | Ghost | Stat. |  | always | 5 | ko mon that defeated user | runs | 12 | 7 |  |  | 6 | 40 |  |  |
| Detect | Fighting | Stat. |  | always | 5 | protect | runs | 11 | 10 |  |  | 2 | 1 |  |  |
| Diamond Storm | Rock | Phys. | 100 | 100 | 5 | raise def 2 hit (50%) | runs | 1 | 1 |  |  |  | 71 |  |  |
| Dig | Ground | Phys. | 80 | 100 | 10 | dig | runs | 61 | 4 | 59 |  | 1 | 13 | TM28 | 1 |
| Disable | Normal | Stat. |  | 100 | 20 | disable | runs | 20 | 10 |  |  | 10 | 1 |  | 4 |
| Disarming Voice | Fairy | Spec. | 40 | always | 15 | bypass accuracy | runs | 3 | 3 |  |  |  | 1 |  |  |
| Discharge | Electric | Spec. | 80 | 100 | 15 | paralyze hit (30%) | runs | 16 | 16 |  |  |  | 28 |  | 10 |
| Dive | Water | Phys. | 80 | 100 | 10 | dive | runs | 43 | 7 |  | 42 |  | 33 | tutor |  |
| Dizzy Punch | Normal | Phys. | 70 | 100 | 10 | confuse hit (20%) | runs | 2 | 2 |  |  |  | 1 |  |  |
| Doom Desire | Steel | Spec. | 140 | 100 | 5 | hit in 3 turns | runs | 0 |  |  |  |  |  |  |  |
| Double Hit | Normal | Phys. | 35 | 90 | 10 | hit twice | runs | 8 | 5 |  |  | 3 | 32 |  | 3 |
| Double Kick | Fighting | Phys. | 30 | 100 | 30 | hit twice | runs | 13 | 9 |  |  | 4 | 1 |  |  |
| Double Shock | Electric | Phys. | 120 | 100 | 5 | remove user electric type hit | runs | 1 | 1 |  |  |  | 61 |  |  |
| Double Team | Normal | Stat. |  | always | 6 | eva up | runs | 163 | 12 | 161 |  |  | 1 | TM32 | 2 |
| Double-Edge | Normal | Phys. | 120 | 100 | 15 | recoil third | runs | 39 | 19 |  |  | 20 | 1 |  |  |
| DoubleSlap | Normal | Phys. | 15 | 100 | 10 | multi hit | runs | 14 | 11 |  |  | 3 | 1 |  | 4 |
| Draco Meteor | Dragon | Spec. | 130 | 90 | 5 | user sp. atk down 2 | runs | 3 | 3 |  |  |  | 1 |  |  |
| Dragon Claw | Dragon | Phys. | 80 | 100 | 15 | plain hit | runs | 14 | 7 | 13 |  | 1 | 1 | TM02 |  |
| Dragon Dance | Dragon | Stat. |  | always | 1 | atk spd up | runs | 7 | 3 |  |  | 4 | 38 |  |  |
| Dragon Pulse | Dragon | Spec. | 85 | 100 | 10 | plain hit | runs | 28 | 10 | 23 |  |  | 1 | TM59 |  |
| Dragon Rage | Dragon | Spec. | 1 | 100 | 10 | 40 damage flat | runs | 4 | 3 |  |  | 1 | 1 |  |  |
| Dragon Rush | Dragon | Phys. | 100 | 75 | 10 | flinch hit (20%) | runs | 7 | 4 |  |  | 3 | 37 |  |  |
| Dragon Tail | Dragon | Phys. | 60 | 100 | 10 | force switch hit | runs | 4 | 4 |  |  |  | 1 |  |  |
| DragonBreath | Dragon | Spec. | 60 | 100 | 20 | paralyze hit (30%) | runs | 14 | 10 |  |  | 4 | 1 |  | 1 |
| Drain Punch | Fighting | Phys. | 75 | 100 | 10 | recover half damage dealt | runs | 20 | 2 | 18 |  |  | 25 | TM60 |  |
| Draining Kiss | Fairy | Spec. | 50 | 100 | 10 | recover three quarters damage dealt | runs | 5 | 5 |  |  |  | 15 |  |  |
| Dream Eater | Psychic | Spec. | 100 | 100 | 15 | recover damage sleep | runs | 47 | 6 | 46 |  | 1 | 19 | TM85 |  |
| Drill Peck | Flying | Phys. | 80 | 100 | 20 | plain hit | runs | 7 | 5 |  |  | 2 | 24 |  |  |
| Dual Chop | Dragon | Phys. | 40 | 100 | 15 | hit twice | runs | 2 | 2 |  |  |  | 1 |  |  |
| Dual Wingbeat | Flying | Phys. | 40 | 100 | 10 | hit twice | runs | 2 | 2 |  |  |  | 28 |  |  |
| DynamicPunch | Fighting | Phys. | 100 | 50 | 5 | confuse hit | runs | 9 | 4 |  |  | 5 | 43 |  | 2 |
| Earth Power | Ground | Spec. | 90 | 100 | 10 | lower sp. def hit (10%) | runs | 37 | 12 |  | 36 |  | 20 | tutor |  |
| Earthquake | Ground | Phys. | 100 | 100 | 10 | double damage dig | runs | 78 | 15 | 74 |  |  | 1 | TM26 | 1 |
| Echoed Voice | Normal | Spec. | 40 | 100 | 15 | plain hit | runs | 2 | 2 |  |  |  | 1 |  |  |
| Eerie Impulse | Electric | Stat. |  | 100 | 5 | sp. atk down 2 | runs | 2 | 2 |  |  |  | 24 |  |  |
| Egg Bomb | Normal | Phys. | 100 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 38 |  |  |
| ElectricTerrain | Electric | Stat. |  | always | 10 | apply terrains | no effect | 2 | 2 |  |  |  | 60 |  |  |
| Electro Ball | Electric | Spec. | 1 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 26 |  |  |
| Electroweb | Electric | Spec. | 55 | 100 | 15 | lower speed hit | runs | 2 | 2 |  |  |  | 15 |  |  |
| Embargo | Dark | Stat. |  | 100 | 15 | prevent item use | runs | 19 | 7 | 17 |  |  | 1 | TM63 |  |
| Ember | Fire | Spec. | 40 | 100 | 25 | burn hit (10%) | runs | 19 | 19 |  |  |  | 1 |  |  |
| Encore | Normal | Stat. |  | 100 | 5 | encore | runs | 22 | 15 |  |  | 9 | 1 |  | 2 |
| Endeavor | Normal | Phys. | 1 | 100 | 5 | set hp equal to user | runs | 20 | 3 |  | 18 | 5 | 17 | tutor |  |
| Endure | Normal | Stat. |  | always | 10 | survive with 1 hp | runs | 165 | 14 | 161 |  | 3 | 1 | TM58 | 2 |
| Energy Ball | Grass | Spec. | 90 | 100 | 10 | lower sp. def hit (10%) | runs | 43 | 8 | 38 |  | 1 | 1 | TM53 |  |
| Entrainment | Normal | Stat. |  | 100 | 15 | entrainment | runs | 3 | 3 |  |  |  | 35 |  |  |
| Eruption | Fire | Spec. | 150 | 100 | 5 | decrease power with less user hp | runs | 0 |  |  |  |  |  |  |  |
| Expanding Force | Psychic | Spec. | 80 | 100 | 10 | plain hit | partial | 2 | 2 |  |  |  | 56 |  |  |
| Explosion | Normal | Phys. | 250 | 100 | 5 | halve defense | runs | 29 | 15 | 25 |  | 3 | 1 | TM64 | 2 |
| Extrasensory | Psychic | Spec. | 80 | 100 | 20 | flinch hit (10%) | runs | 13 | 12 |  |  | 2 | 1 |  | 1 |
| ExtremeSpeed | Normal | Phys. | 80 | 100 | 5 | priority 1 | runs | 3 | 3 |  |  |  | 1 |  |  |
| Facade | Normal | Phys. | 70 | 100 | 20 | double power when statused | runs | 161 |  | 161 |  |  |  | TM42 |  |
| Faint Attack | Dark | Phys. | 60 | always | 20 | bypass accuracy | runs | 30 | 21 |  |  | 10 | 1 |  | 3 |
| Fairy Lock | Fairy | Stat. |  | always | 10 | plain hit | no effect | 1 | 1 |  |  |  | 1 |  |  |
| Fairy Wind | Fairy | Spec. | 40 | 100 | 30 | plain hit | runs | 5 | 5 |  |  |  | 1 |  |  |
| Fake Out | Normal | Phys. | 40 | 100 | 10 | always flinch first turn only | runs | 20 | 11 |  |  | 11 | 1 |  |  |
| Fake Tears | Dark | Stat. |  | 100 | 20 | sp. def down 2 | runs | 15 | 7 |  |  | 8 | 1 |  |  |
| False Swipe | Normal | Phys. | 40 | 100 | 40 | leave with 1 hp | runs | 18 | 6 | 11 |  | 4 | 1 | TM54 |  |
| FeatherDance | Flying | Stat. |  | 100 | 15 | atk down 2 | runs | 11 | 7 |  |  | 4 | 16 |  |  |
| Feint | Normal | Phys. | 30 | 100 | 10 | remove protect | runs | 18 | 15 |  |  | 4 | 1 |  | 3 |
| Fell Stinger | Bug | Phys. | 50 | 100 | 25 | fell stinger | runs | 3 | 3 |  |  |  | 10 |  |  |
| Fiery Dance | Fire | Spec. | 80 | 100 | 10 | raise sp. atk hit (50%) | runs | 1 | 1 |  |  |  | 82 |  |  |
| Fiery Wrath | Dark | Spec. | 90 | 100 | 10 | flinch hit (20%) | runs | 1 | 1 |  |  |  | 45 |  |  |
| Final Gambit | Fighting | Spec. | 1 | 100 | 5 | final gambit | runs | 1 | 1 |  |  |  | 57 |  |  |
| Fire Blast | Fire | Spec. | 110 | 85 | 5 | burn hit (10%) | runs | 42 | 6 | 40 |  |  | 37 | TM38 |  |
| Fire Fang | Fire | Phys. | 90 | 100 | 15 | flinch burn hit (10%) | runs | 17 | 13 |  |  | 6 | 1 |  |  |
| Fire Punch | Fire | Phys. | 95 | 100 | 15 | burn hit (10%) | runs | 37 | 7 |  | 37 | 6 | 1 | tutor |  |
| Fire Spin | Fire | Spec. | 35 | 100 | 15 | bind hit | runs | 15 | 14 |  |  | 1 | 1 |  |  |
| Fissure | Ground | Phys. | 1 | 30 | 5 | one hit ko | runs | 12 | 4 |  |  | 8 | 47 |  |  |
| Flail | Normal | Phys. | 1 | 100 | 15 | increase power with less hp | runs | 33 | 17 |  |  | 18 | 1 |  |  |
| Flame Burst | Fire | Spec. | 70 | 100 | 15 | plain hit | partial | 3 | 3 |  |  |  | 17 |  |  |
| Flame Charge | Fire | Phys. | 50 | 100 | 20 | raise speed hit | runs | 3 | 3 |  |  |  | 6 |  |  |
| Flame Wheel | Fire | Phys. | 60 | 100 | 25 | thaw and burn hit (10%) | runs | 2 | 2 |  |  | 1 | 15 |  |  |
| Flamethrower | Fire | Spec. | 90 | 100 | 15 | burn hit (10%) | runs | 47 | 14 | 41 |  |  | 24 | TM35 |  |
| Flare Blitz | Fire | Phys. | 120 | 100 | 15 | recoil burn hit (10%) | runs | 10 | 9 |  |  | 3 | 40 |  |  |
| Flash | Normal | Stat. |  | 100 | 20 | acc down | runs | 75 | 1 | 74 |  |  | 1 | TM70 |  |
| Flash Cannon | Steel | Spec. | 80 | 100 | 10 | lower sp. def hit (10%) | runs | 27 | 7 | 23 |  |  | 1 | TM91 |  |
| Flatter | Dark | Stat. |  | 100 | 15 | sp. atk up cause confusion | runs | 8 | 6 |  |  | 2 | 1 |  |  |
| Fleur Cannon | Fairy | Spec. | 130 | 100 | 5 | user sp. atk down 2 | runs | 1 | 1 |  |  |  | 90 |  |  |
| Fling | Dark | Phys. | 1 | 100 | 10 | fling | runs | 81 | 8 | 79 |  |  | 1 | TM56 | 4 |
| Flip Turn | Water | Phys. | 60 | 100 | 20 | switch hit | runs | 1 | 1 |  |  |  | 51 |  |  |
| Flower Shield | Fairy | Stat. |  | always | 10 | plain hit | no effect | 1 | 1 |  |  |  | 1 |  |  |
| Flower Trick | Grass | Phys. | 70 | always | 10 | always critical | runs | 1 | 1 |  |  |  | 36 |  |  |
| Fly | Flying | Phys. | 90 | 95 | 15 | fly | runs | 23 | 1 | 22 |  |  | 36 | HM02 |  |
| Flying Press | Fighting | Phys. | 100 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 20 |  |  |
| Focus Blast | Fighting | Spec. | 120 | 70 | 5 | lower sp. def hit (10%) | runs | 58 | 2 | 56 |  |  | 50 | TM52 |  |
| Focus Energy | Normal | Stat. |  | always | 30 | crit up 2 | runs | 21 | 15 |  |  | 6 | 1 |  | 3 |
| Focus Punch | Fighting | Phys. | 150 | 100 | 20 | hit last whiff if hit | runs | 59 | 1 | 58 |  |  | 70 | TM01 |  |
| Follow Me | Normal | Stat. |  | always | 20 | make global target | runs | 3 | 3 |  |  |  | 16 |  | 2 |
| Force Palm | Fighting | Phys. | 60 | 100 | 10 | paralyze hit (30%) | runs | 5 | 5 |  |  |  | 11 |  | 1 |
| Foresight | Normal | Stat. |  | always | 40 | foresight | runs | 21 | 10 |  |  | 11 | 1 |  | 3 |
| Foul Play | Dark | Phys. | 95 | 100 | 15 | plain hit | runs | 3 | 3 |  |  |  | 18 |  |  |
| Freeze-Dry | Ice | Spec. | 70 | 100 | 20 | freeze hit (10%) | runs | 1 | 1 |  |  |  | 44 |  |  |
| Freezing Glare | Psychic | Spec. | 90 | 100 | 10 | freeze hit (10%) | runs | 1 | 1 |  |  |  | 45 |  |  |
| Frustration | Normal | Phys. | 1 | 100 | 20 | power based on low friendship | runs | 161 | 1 | 161 |  |  | 13 | TM21 | 1 |
| Fury Attack | Normal | Phys. | 15 | 100 | 20 | multi hit | runs | 16 | 15 |  |  | 1 | 1 |  | 2 |
| Fury Cutter | Bug | Phys. | 40 | 95 | 20 | double power each turn | runs | 58 | 10 |  | 53 | 2 | 1 | tutor | 1 |
| Fury Swipes | Normal | Phys. | 18 | 100 | 15 | multi hit | runs | 13 | 11 |  |  | 2 | 5 |  | 2 |
| Future Sight | Psychic | Spec. | 120 | 100 | 10 | hit in 3 turns | runs | 26 | 17 |  |  | 9 | 34 |  | 6 |
| Gastro Acid | Poison | Stat. |  | 100 | 10 | suppress ability | runs | 5 | 4 |  | 2 |  | 23 | tutor |  |
| Geomancy | Fairy | Stat. |  | always | 10 | charge turn atk sp. atk speed up 2 | runs | 1 | 1 |  |  |  | 41 |  |  |
| Giga Drain | Grass | Spec. | 75 | 100 | 10 | recover half damage dealt | runs | 31 | 13 | 25 |  |  | 25 | TM19 | 1 |
| Giga Impact | Normal | Phys. | 150 | 90 | 5 | recharge after | runs | 148 | 6 | 146 |  |  | 49 | TM68 |  |
| Glare | Normal | Stat. |  | 100 | 30 | status paralyze | runs | 2 | 2 |  |  |  | 1 |  |  |
| Grass Knot | Grass | Spec. | 1 | 100 | 20 | increase power with weight | runs | 56 | 3 | 53 |  |  | 1 | TM86 |  |
| GrassWhistle | Grass | Stat. |  | 55 | 15 | status sleep | runs | 6 | 4 |  |  | 2 | 1 |  | 1 |
| Grassy Glide | Grass | Phys. | 55 | 100 | 20 | plain hit | partial | 1 | 1 |  |  |  | 46 |  |  |
| Grassy Terrain | Grass | Stat. |  | always | 10 | apply terrains | no effect | 2 | 2 |  |  |  | 23 |  |  |
| Gravity | Psychic | Stat. |  | always | 5 | gravity | runs | 6 | 5 |  |  | 1 | 1 |  | 1 |
| Growl | Normal | Stat. |  | 100 | 40 | atk down | runs | 47 | 47 |  |  |  | 1 |  | 6 |
| Growth | Normal | Stat. |  | always | 3 | sp. atk up | runs | 14 | 12 |  |  | 2 | 1 |  | 1 |
| Grudge | Ghost | Stat. |  | always | 5 | remove all pp on defeat | runs | 10 | 5 |  |  | 5 | 1 |  |  |
| Guard Split | Psychic | Stat. |  | always | 10 | guard split | runs | 5 | 5 |  |  |  | 12 |  |  |
| Guard Swap | Psychic | Stat. |  | always | 10 | swap def sp. def stat changes | runs | 6 | 4 |  |  | 2 | 1 |  |  |
| Guillotine | Normal | Phys. | 1 | 30 | 5 | one hit ko | runs | 4 | 4 |  |  |  | 31 |  |  |
| Gunk Shot | Poison | Phys. | 120 | 80 | 5 | poison hit (30%) | runs | 11 | 2 |  | 10 |  | 1 | tutor |  |
| Gust | Flying | Spec. | 40 | 100 | 35 | double damage fly or bounce | runs | 16 | 13 |  |  | 3 | 1 |  | 2 |
| Gyro Ball | Steel | Phys. | 1 | 100 | 5 | power based on low speed | runs | 21 | 8 | 18 |  |  | 1 | TM74 | 2 |
| Hail | Ice | Stat. |  | always | 1 | weather hail | runs | 53 | 7 | 52 |  |  | 20 | TM07 |  |
| Hammer Arm | Fighting | Phys. | 100 | 100 | 10 | speed down hit | runs | 13 | 10 |  |  | 3 | 1 |  |  |
| Harden | Normal | Stat. |  | always | 5 | def up | runs | 26 | 24 |  |  | 2 | 1 |  |  |
| Haze | Ice | Stat. |  | always | 30 | reset stat changes | runs | 22 | 11 |  |  | 11 | 1 |  |  |
| Head Smash | Rock | Phys. | 150 | 80 | 5 | recoil half | runs | 4 | 4 |  |  |  | 1 |  |  |
| Headbutt | Normal | Phys. | 70 | 100 | 15 | flinch hit (30%) | runs | 19 | 14 |  |  | 5 | 1 |  |  |
| Heal Bell | Normal | Stat. |  | always | 5 | cure party status | runs | 4 | 2 |  |  | 2 | 38 |  |  |
| Heal Block | Psychic | Stat. |  | 100 | 15 | prevent healing | runs | 9 | 9 |  |  |  | 5 |  |  |
| Heal Order | Bug | Stat. |  | always | 10 | restore half hp | runs | 1 | 1 |  |  |  | 25 |  |  |
| Heal Pulse | Psychic | Stat. |  | always | 10 | heal target | runs | 4 | 4 |  |  |  | 1 |  |  |
| Healing Wish | Psychic | Stat. |  | always | 10 | faint and full heal next mon | runs | 11 | 10 |  |  | 1 | 1 |  | 2 |
| Heart Swap | Psychic | Stat. |  | always | 10 | swap stat changes | runs | 1 | 1 |  |  |  | 76 |  |  |
| Heat Wave | Fire | Spec. | 95 | 90 | 10 | burn hit (10%) | runs | 23 | 6 |  | 20 | 2 | 1 | tutor |  |
| Heavy Slam | Steel | Phys. | 1 | 100 | 10 | heavy slam | runs | 6 | 6 |  |  |  | 1 |  |  |
| Helping Hand | Normal | Stat. |  | always | 20 | boost ally power by 50 percent | runs | 51 | 18 |  | 43 | 5 | 1 | tutor |  |
| Hex | Ghost | Spec. | 65 | 100 | 10 | double damage on status | runs | 4 | 4 |  |  |  | 20 |  |  |
| Hi Jump Kick | Fighting | Phys. | 130 | 90 | 10 | crash on miss | runs | 8 | 7 |  |  | 1 | 32 |  |  |
| Hidden Power | Normal | Spec. | 1 | 100 | 15 | random power based on ivs | runs | 161 | 4 | 161 |  |  | 1 | TM10 |  |
| Hold Back | Normal | Phys. | 40 | 100 | 40 | leave with 1 hp | runs | 1 | 1 |  |  |  | 14 |  |  |
| Hone Claws | Dark | Stat. |  | always | 15 | atk acc up | runs | 1 | 1 |  |  |  | 24 |  |  |
| Horn Attack | Normal | Phys. | 65 | 100 | 25 | plain hit | runs | 6 | 6 |  |  |  | 1 |  |  |
| Horn Drill | Normal | Phys. | 1 | 30 | 5 | one hit ko | runs | 6 | 3 |  |  | 3 | 37 |  |  |
| Horn Leech | Grass | Phys. | 75 | 100 | 10 | recover half damage dealt | runs | 2 | 2 |  |  |  | 40 |  |  |
| Howl | Normal | Stat. |  | always | 3 | atk up | runs | 4 | 2 |  |  | 2 | 1 |  |  |
| Hurricane | Flying | Spec. | 110 | 80 | 10 | hurricane (30%) | runs | 3 | 3 |  |  |  | 1 |  |  |
| Hydro Cannon | Water | Spec. | 150 | 90 | 5 | recharge after | runs | 1 | 1 |  |  |  | 65 |  |  |
| Hydro Pump | Water | Spec. | 110 | 80 | 5 | plain hit | runs | 31 | 27 |  |  | 7 | 1 |  |  |
| Hyper Beam | Normal | Spec. | 150 | 90 | 5 | recharge after | runs | 147 | 10 | 146 |  |  | 45 | TM15 | 1 |
| Hyper Fang | Normal | Phys. | 80 | 90 | 15 | flinch hit (10%) | runs | 1 | 1 |  |  |  | 21 |  |  |
| Hyper Voice | Normal | Spec. | 100 | 100 | 10 | plain hit | runs | 8 | 8 |  |  |  | 1 |  |  |
| Hypnosis | Psychic | Stat. |  | 60 | 20 | status sleep | runs | 26 | 18 |  |  | 8 | 1 |  | 1 |
| Ice Ball | Ice | Phys. | 30 | 90 | 20 | double power each turn lock into | runs | 4 | 1 |  |  | 3 | 13 |  |  |
| Ice Beam | Ice | Spec. | 90 | 100 | 10 | freeze hit (10%) | runs | 78 | 9 | 76 |  |  | 1 | TM13 |  |
| Ice Fang | Ice | Phys. | 90 | 100 | 15 | flinch freeze hit (10%) | runs | 19 | 15 |  |  | 5 | 1 |  |  |
| Ice Punch | Ice | Phys. | 95 | 100 | 15 | freeze hit (10%) | runs | 51 | 6 |  | 49 | 10 | 1 | tutor |  |
| Ice Shard | Ice | Phys. | 40 | 100 | 30 | priority 1 | runs | 13 | 11 |  |  | 3 | 1 |  |  |
| Icicle Spear | Ice | Phys. | 25 | 100 | 30 | multi hit | runs | 4 | 1 |  |  | 4 | 13 |  |  |
| Icy Wind | Ice | Spec. | 55 | 95 | 15 | lower speed hit | runs | 84 | 12 |  | 79 |  | 1 | tutor |  |
| Imprison | Psychic | Stat. |  | always | 10 | make shared moves unuseable | runs | 13 | 10 |  |  | 3 | 1 |  | 4 |
| Incinerate | Fire | Spec. | 60 | 100 | 15 | incinerate | runs | 3 | 3 |  |  |  | 20 |  |  |
| Infestation | Bug | Spec. | 20 | 100 | 20 | bind hit | runs | 4 | 4 |  |  |  | 5 |  |  |
| Ingrain | Grass | Stat. |  | always | 1 | ground trap user continuous heal | runs | 12 | 11 |  |  | 1 | 1 |  | 1 |
| Iron Defense | Steel | Stat. |  | always | 3 | def up 2 | runs | 36 | 18 |  | 27 | 2 | 1 | tutor | 1 |
| Iron Head | Steel | Phys. | 80 | 100 | 15 | flinch hit (30%) | runs | 43 | 12 |  | 37 | 2 | 38 | tutor |  |
| Iron Tail | Steel | Phys. | 100 | 75 | 15 | lower defense hit (30%) | runs | 68 | 2 | 67 |  |  | 41 | TM23 |  |
| Judgment | Normal | Spec. | 100 | 100 | 10 | judgement | runs | 1 | 1 |  |  |  | 100 |  |  |
| Jump Kick | Fighting | Phys. | 100 | 95 | 10 | crash on miss | runs | 3 | 3 |  |  |  | 23 |  | 1 |
| Karate Chop | Fighting | Phys. | 50 | 100 | 25 | high critical | runs | 5 | 3 |  |  | 2 | 1 |  | 1 |
| Kinesis | Psychic | Stat. |  | 100 | 15 | acc down | runs | 1 | 1 |  |  |  | 1 |  |  |
| Knock Off | Dark | Phys. | 70 | 100 | 20 | remove held item | runs | 49 | 15 |  | 41 | 5 | 1 | tutor | 1 |
| Land’s Wrath | Ground | Phys. | 90 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 37 |  |  |
| Laser Focus | Normal | Stat. |  | always | 30 | laser focus | runs | 1 | 1 |  |  |  | 45 |  |  |
| Last Resort | Normal | Phys. | 140 | 100 | 5 | fail if not used all other moves | runs | 30 | 13 |  | 26 | 4 | 1 | tutor | 4 |
| Lava Plume | Fire | Spec. | 80 | 100 | 15 | burn hit (30%) | runs | 5 | 5 |  |  |  | 32 |  |  |
| Leaf Blade | Grass | Phys. | 90 | 100 | 15 | high critical | runs | 10 | 9 |  |  | 1 | 1 |  |  |
| Leaf Storm | Grass | Spec. | 130 | 90 | 5 | user sp. atk down 2 | runs | 14 | 12 |  |  | 4 | 44 |  |  |
| Leafage | Grass | Phys. | 40 | 100 | 40 | plain hit | runs | 5 | 5 |  |  |  | 1 |  |  |
| Leech Life | Bug | Phys. | 80 | 100 | 10 | recover half damage dealt | runs | 7 | 6 |  |  | 1 | 1 |  | 1 |
| Leech Seed | Grass | Stat. |  | 90 | 10 | status leech seed | runs | 16 | 9 |  |  | 7 | 1 |  |  |
| Leer | Normal | Stat. |  | 100 | 3 | def down | runs | 40 | 38 |  |  | 3 | 1 |  | 3 |
| Lick | Ghost | Phys. | 40 | 100 | 30 | paralyze hit (30%) | runs | 8 | 7 |  |  | 2 | 1 |  |  |
| Life Dew | Water | Stat. |  | always | 10 | life dew | runs | 3 | 3 |  |  |  | 10 |  |  |
| Light Screen | Psychic | Stat. |  | always | 1 | set light screen | runs | 57 | 20 | 42 |  | 5 | 1 | TM16 | 9 |
| Liquidation | Water | Phys. | 85 | 100 | 10 | lower defense hit (20%) | runs | 3 | 3 |  |  |  | 1 |  |  |
| Lock-On | Normal | Stat. |  | always | 5 | next attack always hits | runs | 7 | 7 |  |  |  | 6 |  | 3 |
| Lovely Kiss | Normal | Stat. |  | 75 | 10 | status sleep | runs | 1 | 1 |  |  |  | 1 |  |  |
| Low Kick | Fighting | Phys. | 1 | 100 | 20 | increase power with weight | runs | 8 | 6 |  |  | 2 | 1 |  | 1 |
| Low Sweep | Fighting | Phys. | 65 | 100 | 20 | lower speed hit | runs | 1 | 1 |  |  |  | 32 |  |  |
| Lucky Chant | Normal | Stat. |  | always | 30 | prevent crits | runs | 12 | 10 |  |  | 2 | 1 |  | 4 |
| Lunar Dance | Psychic | Stat. |  | always | 10 | faint full restore next mon | runs | 1 | 1 |  |  |  | 84 |  |  |
| Lunge | Bug | Phys. | 80 | 100 | 15 | lower attack hit | runs | 3 | 3 |  |  |  | 37 |  |  |
| Luster Purge | Psychic | Spec. | 95 | 100 | 5 | lower sp. def hit (50%) | runs | 1 | 1 |  |  |  | 35 |  |  |
| Mach Punch | Fighting | Phys. | 40 | 100 | 30 | priority 1 | runs | 3 | 2 |  |  | 1 | 23 |  |  |
| Magic Coat | Psychic | Stat. |  | always | 15 | apply magic coat | runs | 4 | 2 |  |  | 2 | 1 |  |  |
| Magic Room | Psychic | Stat. |  | always | 10 | plain hit | no effect | 3 | 3 |  |  |  | 44 |  |  |
| Magical Leaf | Grass | Spec. | 60 | always | 20 | bypass accuracy | runs | 17 | 14 |  |  | 3 | 1 |  | 5 |
| Magma Storm | Fire | Spec. | 100 | 75 | 5 | bind hit | runs | 1 | 1 |  |  |  | 96 |  |  |
| Magnet Bomb | Steel | Phys. | 60 | always | 20 | bypass accuracy | runs | 2 | 2 |  |  |  | 1 |  | 5 |
| Magnet Rise | Electric | Stat. |  | always | 10 | give ground immunity | runs | 20 | 5 |  | 18 |  | 1 | tutor | 3 |
| Magnetic Flux | Electric | Stat. |  | always | 20 | plain hit | no effect | 1 | 1 |  |  |  | 24 |  |  |
| Magnitude | Ground | Phys. | 1 | 100 | 30 | psywave | runs | 7 | 3 |  |  | 4 | 15 |  |  |
| Mat Block | Fighting | Stat. |  | always | 10 | protect user side | runs | 1 | 1 |  |  |  | 1 |  |  |
| Matcha Gotcha | Grass | Spec. | 80 | 90 | 15 | recover half damage dealt burn hit (20%) | runs | 1 | 1 |  |  |  | 1 |  |  |
| Me First | Normal | Stat. |  | always | 20 | use move first | runs | 10 | 7 |  |  | 4 | 29 |  |  |
| Mean Look | Normal | Stat. |  | always | 5 | prevent escape | runs | 14 | 12 |  |  | 2 | 8 |  |  |
| Meditate | Psychic | Stat. |  | always | 3 | atk up | runs | 7 | 2 |  |  | 5 | 1 |  | 1 |
| Mega Drain | Grass | Spec. | 40 | 100 | 15 | recover half damage dealt | runs | 16 | 16 |  |  | 1 | 1 |  |  |
| Mega Kick | Normal | Phys. | 120 | 75 | 5 | plain hit | runs | 0 |  |  |  |  |  |  |  |
| Mega Punch | Normal | Phys. | 80 | 85 | 20 | plain hit | runs | 3 | 1 |  |  | 2 | 35 |  |  |
| Megahorn | Bug | Phys. | 120 | 85 | 10 | plain hit | runs | 9 | 9 |  |  |  | 1 |  |  |
| Memento | Dark | Stat. |  | 100 | 10 | faint and atk sp. atk down 2 | runs | 15 | 9 |  |  | 6 | 38 |  |  |
| Metal Burst | Steel | Phys. | 1 | 100 | 10 | metal burst | runs | 1 | 1 |  |  |  | 37 |  |  |
| Metal Claw | Steel | Phys. | 50 | 95 | 35 | raise attack hit (10%) | runs | 15 | 10 |  |  | 5 | 1 |  |  |
| Metal Sound | Steel | Stat. |  | 100 | 40 | sp. def down 2 | runs | 9 | 9 |  |  |  | 1 |  | 1 |
| Meteor Mash | Steel | Phys. | 90 | 90 | 10 | raise attack hit (20%) | runs | 2 | 2 |  |  |  | 43 |  | 3 |
| Metronome | Normal | Stat. |  | always | 10 | call random move | runs | 5 | 3 |  |  | 3 | 1 |  | 1 |
| Milk Drink | Normal | Stat. |  | always | 10 | restore half hp | runs | 0 |  |  |  |  |  |  |  |
| Mimic | Normal | Stat. |  | always | 10 | copy move for battle | runs | 5 | 4 |  |  | 2 | 1 |  | 3 |
| Mind Blown | Fire | Spec. | 150 | 100 | 5 | plain hit | partial | 1 | 1 |  |  |  | 70 |  |  |
| Mind Reader | Normal | Stat. |  | always | 5 | next attack always hits | runs | 8 | 5 |  |  | 4 | 18 |  | 1 |
| Minimize | Normal | Stat. |  | always | 3 | eva up 2 minimize | runs | 5 | 5 |  |  |  | 1 |  | 2 |
| Miracle Eye | Psychic | Stat. |  | always | 40 | ignore evasion remove dark immune | runs | 2 | 1 |  |  | 1 | 22 |  | 2 |
| Mirror Coat | Psychic | Spec. | 1 | 100 | 20 | mirror coat | runs | 17 | 9 |  |  | 8 | 1 |  |  |
| Mirror Move | Flying | Stat. |  | always | 20 | copy move | runs | 7 | 4 |  |  | 3 | 1 |  |  |
| Mirror Shot | Steel | Spec. | 65 | 100 | 10 | lower accuracy hit (30%) | runs | 3 | 3 |  |  |  | 26 |  | 5 |
| Mist | Ice | Stat. |  | always | 3 | prevent stat reduction | runs | 21 | 16 |  |  | 7 | 1 |  | 1 |
| Mist Ball | Psychic | Spec. | 95 | 100 | 5 | lower sp. atk hit (50%) | runs | 1 | 1 |  |  |  | 35 |  |  |
| Misty Terrain | Fairy | Stat. |  | always | 10 | apply terrains | no effect | 4 | 4 |  |  |  | 1 |  |  |
| Moonblast | Fairy | Spec. | 95 | 100 | 15 | lower sp. atk hit (10%) | runs | 8 | 8 |  |  |  | 43 |  |  |
| Moonlight | Fairy | Stat. |  | always | 5 | heal half more in sun | runs | 4 | 4 |  |  |  | 20 |  | 3 |
| Morning Sun | Normal | Stat. |  | always | 5 | heal half more in sun | runs | 3 | 3 |  |  |  | 20 |  |  |
| Mortal Spin | Poison | Phys. | 30 | 100 | 15 | mortal spin | runs | 1 | 1 |  |  |  | 1 |  |  |
| Mud Bomb | Ground | Spec. | 65 | 100 | 10 | lower accuracy hit (30%) | runs | 8 | 7 |  |  | 2 | 11 |  | 2 |
| Mud Shot | Ground | Spec. | 55 | 100 | 15 | lower speed hit | runs | 9 | 6 |  |  | 4 | 1 |  |  |
| Mud Sport | Ground | Stat. |  | always | 15 | halve electric damage | runs | 20 | 9 |  |  | 12 | 1 |  |  |
| Mud-Slap | Ground | Spec. | 20 | 100 | 10 | lower accuracy hit | runs | 131 | 6 |  | 130 | 4 | 1 | tutor |  |
| Muddy Water | Water | Spec. | 90 | 100 | 10 | lower accuracy hit (30%) | runs | 7 | 6 |  |  | 1 | 37 |  |  |
| Mystical Fire | Fire | Spec. | 75 | 100 | 10 | lower sp. atk hit | runs | 5 | 5 |  |  |  | 1 |  |  |
| Nasty Plot | Dark | Stat. |  | always | 1 | sp. atk up 2 | runs | 23 | 20 |  |  | 5 | 1 |  | 9 |
| Natural Gift | Normal | Phys. | 1 | 100 | 15 | natural gift | runs | 162 | 12 | 161 |  |  | 1 | TM83 |  |
| Nature Power | Normal | Stat. |  | always | 20 | nature power | runs | 7 | 3 |  |  | 4 | 1 |  |  |
| Nature’sMadness | Fairy | Spec. | 0 | 100 | 10 | halve hp | partial | 4 | 4 |  |  |  | 55 |  |  |
| Needle Arm | Grass | Phys. | 60 | 100 | 15 | flinch hit (30%) | runs | 0 |  |  |  |  |  |  |  |
| Night Shade | Ghost | Spec. | 1 | 100 | 15 | level damage flat | runs | 10 | 8 |  |  | 2 | 1 |  |  |
| Night Slash | Dark | Phys. | 70 | 100 | 15 | high critical | runs | 24 | 22 |  |  | 4 | 1 |  | 3 |
| Nightmare | Ghost | Stat. |  | 100 | 15 | status nightmare | runs | 2 | 2 |  |  |  | 38 |  |  |
| Noble Roar | Normal | Stat. |  | 100 | 10 | tearful look | runs | 1 | 1 |  |  |  | 41 |  |  |
| Nuzzle | Electric | Phys. | 20 | 100 | 20 | paralyze hit | runs | 3 | 3 |  |  |  | 1 |  |  |
| Oblivion Wing | Flying | Spec. | 80 | 100 | 10 | recover three quarters damage dealt | runs | 1 | 1 |  |  |  | 38 |  |  |
| Octazooka | Water | Spec. | 65 | 85 | 10 | lower accuracy hit (50%) | runs | 3 | 2 |  |  | 2 | 1 |  |  |
| Octolock | Fighting | Stat. |  | 100 | 15 | plain hit | no effect | 1 | 1 |  |  |  | 1 |  |  |
| Odor Sleuth | Normal | Stat. |  | always | 40 | foresight | runs | 9 | 6 |  |  | 3 | 1 |  |  |
| Ominous Wind | Ghost | Spec. | 60 | 100 | 5 | raise all stats hit (10%) | runs | 40 | 10 |  | 37 | 3 | 1 | tutor | 4 |
| Outrage | Dragon | Phys. | 120 | 100 | 10 | continue and confuse self | runs | 33 | 6 |  | 28 | 3 | 49 | tutor |  |
| Overheat | Fire | Spec. | 130 | 90 | 5 | user sp. atk down 2 | runs | 19 | 4 | 15 |  |  | 60 | TM50 |  |
| Pain Split | Normal | Stat. |  | always | 20 | average hp | runs | 8 | 5 |  |  | 3 | 28 |  |  |
| Parting Shot | Dark | Stat. |  | 100 | 20 | parting shot | runs | 1 | 1 |  |  |  | 42 |  |  |
| Pay Day | Normal | Phys. | 40 | 100 | 20 | increase prize money | runs | 0 |  |  |  |  |  |  |  |
| Payback | Dark | Phys. | 60 | 100 | 10 | double power if moving second | runs | 56 | 12 | 53 |  |  | 5 | TM66 | 1 |
| Peck | Flying | Phys. | 40 | 100 | 35 | plain hit | runs | 18 | 17 |  |  | 1 | 1 |  |  |
| Perish Song | Normal | Stat. |  | always | 5 | all faint 3 turns | runs | 13 | 9 |  |  | 4 | 1 |  | 2 |
| Petal Blizzard | Grass | Phys. | 90 | 100 | 15 | plain hit | runs | 2 | 2 |  |  |  | 1 |  |  |
| Petal Dance | Grass | Spec. | 120 | 100 | 10 | continue and confuse self | runs | 3 | 3 |  |  |  | 25 |  |  |
| Phantom Force | Ghost | Phys. | 90 | 100 | 10 | shadow force | runs | 3 | 3 |  |  |  | 1 |  |  |
| Pin Missile | Bug | Phys. | 25 | 100 | 20 | multi hit | runs | 7 | 6 |  |  | 1 | 12 |  | 1 |
| Play Nice | Normal | Stat. |  | always | 10 | atk down | runs | 3 | 3 |  |  |  | 1 |  |  |
| Play Rough | Fairy | Phys. | 90 | 100 | 10 | lower attack hit (10%) | runs | 4 | 4 |  |  |  | 29 |  |  |
| Pluck | Flying | Phys. | 60 | 100 | 20 | eat berry | runs | 20 | 7 | 15 |  |  | 1 | TM88 |  |
| Poison Fang | Poison | Phys. | 75 | 100 | 15 | badly poison hit (30%) | runs | 5 | 3 |  |  | 2 | 33 |  |  |
| Poison Gas | Poison | Stat. |  | 85 | 40 | status poison | runs | 2 | 2 |  |  |  | 1 |  |  |
| Poison Jab | Poison | Phys. | 80 | 100 | 20 | poison hit (30%) | runs | 32 | 11 | 29 |  | 1 | 1 | TM84 |  |
| Poison Sting | Poison | Phys. | 40 | 100 | 35 | poison hit (30%) | runs | 12 | 12 |  |  |  | 1 |  |  |
| Poison Tail | Poison | Phys. | 50 | 100 | 25 | high critical poison hit (10%) | runs | 1 | 1 |  |  |  | 12 |  |  |
| PoisonPowder | Poison | Stat. |  | 75 | 35 | status poison | runs | 4 | 4 |  |  |  | 12 |  |  |
| Pollen Puff | Bug | Spec. | 90 | 100 | 15 | pollen puff | runs | 1 | 1 |  |  |  | 72 |  |  |
| Poltergeist | Ghost | Phys. | 110 | 90 | 5 | poltergeist | runs | 2 | 2 |  |  |  | 1 |  |  |
| Pound | Normal | Phys. | 40 | 100 | 35 | plain hit | runs | 16 | 16 |  |  |  | 1 |  | 3 |
| Powder Snow | Ice | Spec. | 40 | 100 | 25 | freeze hit (10%) | runs | 9 | 9 |  |  |  | 1 |  |  |
| Power Gem | Rock | Spec. | 80 | 100 | 20 | plain hit | runs | 11 | 11 |  |  |  | 1 |  |  |
| Power Split | Psychic | Stat. |  | always | 10 | power split | runs | 2 | 2 |  |  |  | 25 |  |  |
| Power Swap | Psychic | Stat. |  | always | 10 | swap atk sp. atk stat changes | runs | 5 | 4 |  |  | 1 | 1 |  |  |
| Power Trick | Psychic | Stat. |  | always | 10 | swap atk def | runs | 2 | 1 |  |  | 1 | 39 |  |  |
| Power Whip | Grass | Phys. | 120 | 85 | 10 | plain hit | runs | 8 | 8 |  |  |  | 47 |  |  |
| Power-Up Punch | Fighting | Phys. | 40 | 100 | 20 | raise attack hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Present | Normal | Phys. | 1 | 90 | 15 | random power maybe heal | runs | 7 | 1 |  |  | 6 | 1 |  |  |
| Protect | Normal | Stat. |  | always | 10 | protect | runs | 167 | 21 | 160 |  |  | 1 | TM17 |  |
| Psybeam | Psychic | Spec. | 65 | 100 | 20 | confuse hit (10%) | runs | 21 | 15 |  |  | 6 | 1 |  | 4 |
| Psych Up | Normal | Stat. |  | always | 10 | copy stat changes | runs | 73 | 7 | 68 |  | 10 | 1 | TM77 |  |
| Psychic | Psychic | Spec. | 90 | 100 | 10 | lower sp. def hit (10%) | runs | 55 | 20 | 49 |  | 1 | 28 | TM29 | 10 |
| Psychic Terrain | Psychic | Stat. |  | always | 10 | apply terrains | no effect | 1 | 1 |  |  |  | 75 |  |  |
| Psycho Boost | Psychic | Spec. | 140 | 90 | 5 | user sp. atk down 2 | runs | 0 |  |  |  |  |  |  |  |
| Psycho Cut | Psychic | Phys. | 70 | 100 | 20 | high critical | runs | 8 | 7 |  |  | 1 | 1 |  | 1 |
| Psycho Shift | Psychic | Stat. |  | 100 | 10 | transfer status | runs | 6 | 4 |  |  | 2 | 41 |  |  |
| Psyshock | Psychic | Spec. | 80 | 100 | 10 | plain hit | runs | 5 | 5 |  |  |  | 1 |  |  |
| Psywave | Psychic | Spec. | 1 | 100 | 15 | random damage 1 to 150 level | runs | 8 | 6 |  |  | 2 | 1 |  |  |
| Punishment | Dark | Phys. | 1 | 100 | 5 | increase power with more stat up | runs | 9 | 4 |  |  | 5 | 1 |  |  |
| Pursuit | Dark | Phys. | 40 | 100 | 20 | hit before switch | runs | 30 | 16 |  |  | 15 | 1 |  |  |
| Pyro Ball | Fire | Phys. | 120 | 90 | 5 | burn hit (10%) | runs | 1 | 1 |  |  |  | 72 |  |  |
| Quick Attack | Normal | Phys. | 40 | 100 | 30 | priority 1 | runs | 39 | 32 |  |  | 7 | 1 |  | 6 |
| Quick Guard | Fighting | Stat. |  | always | 15 | protect user side | runs | 3 | 3 |  |  |  | 1 |  |  |
| Quiver Dance | Bug | Stat. |  | always | 20 | sp. atk sp. def speed up | runs | 2 | 2 |  |  |  | 52 |  |  |
| Rage | Normal | Phys. | 20 | 100 | 20 | raise atk when hit | runs | 7 | 5 |  |  | 2 | 1 |  |  |
| Rage Fist | Ghost | Phys. | 50 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 35 |  |  |
| Rage Powder | Bug | Stat. |  | 100 | 20 | make global target | runs | 2 | 2 |  |  |  | 36 |  |  |
| Rain Dance | Water | Stat. |  | always | 1 | weather rain | runs | 132 | 17 | 131 |  |  | 1 | TM18 | 1 |
| Rapid Spin | Normal | Phys. | 60 | 100 | 40 | remove hazards and binding | runs | 11 | 8 |  |  | 3 | 1 |  |  |
| Razor Leaf | Grass | Phys. | 55 | 100 | 25 | high critical | runs | 17 | 13 |  |  | 4 | 1 |  |  |
| Razor Wind | Normal | Spec. | 80 | 100 | 10 | charge turn high crit | runs | 7 | 5 |  |  | 4 | 1 |  |  |
| Recover | Normal | Stat. |  | always | 10 | restore half hp | runs | 18 | 16 |  |  | 2 | 1 |  | 1 |
| Recycle | Normal | Stat. |  | always | 10 | recycle | runs | 27 | 5 | 24 |  |  | 1 | TM67 | 4 |
| Reflect | Psychic | Stat. |  | always | 1 | set reflect | runs | 43 | 10 | 33 |  | 5 | 1 | TM33 | 5 |
| Refresh | Normal | Stat. |  | always | 20 | heal status | runs | 15 | 8 |  |  | 7 | 9 |  |  |
| Rest | Psychic | Stat. |  | always | 3 | rest | runs | 160 | 11 | 160 |  |  | 1 | TM44 |  |
| Retaliate | Normal | Phys. | 70 | 100 | 5 | plain hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Return | Normal | Phys. | 1 | 100 | 20 | power based on friendship | runs | 161 | 1 | 161 |  |  | 13 | TM27 |  |
| Revenge | Fighting | Phys. | 60 | 100 | 10 | double power if hit | runs | 9 | 6 |  |  | 3 | 1 |  | 4 |
| Reversal | Fighting | Phys. | 1 | 100 | 15 | increase power with less hp | runs | 17 | 9 |  |  | 8 | 1 |  |  |
| Roar | Normal | Stat. |  | always | 20 | force switch | runs | 50 | 6 | 49 |  |  | 7 | TM05 | 5 |
| Roar of Time | Dragon | Spec. | 150 | 90 | 5 | recharge after | runs | 1 | 1 |  |  |  | 40 |  |  |
| Rock Blast | Rock | Phys. | 25 | 100 | 8 | multi hit | runs | 13 | 11 |  |  | 3 | 1 |  | 1 |
| Rock Climb | Normal | Phys. | 90 | 85 | 20 | confuse hit (20%) | runs | 43 |  | 43 |  |  |  | HM08 |  |
| Rock Polish | Rock | Stat. |  | always | 1 | speed up 2 | runs | 27 | 8 | 23 |  |  | 1 | TM69 |  |
| Rock Slide | Rock | Phys. | 75 | 90 | 10 | flinch hit (30%) | runs | 78 | 11 | 72 |  | 14 | 14 | TM80 |  |
| Rock Smash | Fighting | Phys. | 40 | 100 | 15 | lower defense hit (50%) | runs | 107 | 6 | 102 |  |  | 1 | HM06 |  |
| Rock Throw | Rock | Phys. | 50 | 100 | 15 | plain hit | runs | 13 | 13 |  |  |  | 1 |  |  |
| Rock Tomb | Rock | Phys. | 60 | 100 | 15 | lower speed hit | runs | 81 | 6 | 78 |  |  | 1 | TM39 |  |
| Rock Wrecker | Rock | Phys. | 150 | 90 | 5 | recharge after | runs | 2 | 2 |  |  |  | 61 |  |  |
| Role Play | Psychic | Stat. |  | always | 10 | copy ability | runs | 4 | 4 |  |  |  | 1 |  | 6 |
| Rolling Kick | Fighting | Phys. | 60 | 100 | 15 | flinch hit (30%) | runs | 2 |  |  |  | 2 |  |  |  |
| Rollout | Rock | Phys. | 30 | 90 | 20 | double power each turn lock into | runs | 46 | 9 |  | 45 | 6 | 1 | tutor | 3 |
| Roost | Flying | Stat. |  | always | 10 | heal half remove flying type | runs | 30 | 12 | 24 |  |  | 1 | TM51 |  |
| Sacred Fire | Fire | Phys. | 100 | 95 | 5 | thaw and burn hit (50%) | runs | 0 |  |  |  |  |  |  |  |
| Sacred Sword | Fighting | Phys. | 90 | 100 | 15 | plain hit | runs | 1 | 1 |  |  |  | 60 |  |  |
| Safeguard | Normal | Stat. |  | always | 25 | prevent status | runs | 60 | 22 | 49 |  | 5 | 1 | TM20 | 4 |
| Salt Cure | Rock | Phys. | 40 | 100 | 15 | plain hit | partial | 1 | 1 |  |  |  | 1 |  |  |
| Sand Tomb | Ground | Phys. | 35 | 100 | 15 | bind hit | runs | 8 | 5 |  |  | 5 | 1 |  | 1 |
| Sand-Attack | Ground | Stat. |  | 100 | 5 | acc down | runs | 19 | 15 |  |  | 4 | 1 |  |  |
| Sandstorm | Rock | Stat. |  | always | 1 | weather sandstorm | runs | 54 | 8 | 51 |  |  | 1 | TM37 | 1 |
| Scald | Water | Spec. | 80 | 100 | 15 | thaw and burn hit (30%) | runs | 4 | 4 |  |  |  | 31 |  |  |
| Scale Shot | Dragon | Phys. | 25 | 100 | 20 | multi hit | partial | 1 | 1 |  |  |  | 45 |  |  |
| Scary Face | Normal | Stat. |  | 100 | 10 | speed down 2 | runs | 29 | 26 |  |  | 3 | 1 |  | 8 |
| Scratch | Normal | Phys. | 40 | 100 | 35 | plain hit | runs | 18 | 18 |  |  |  | 1 |  | 2 |
| Screech | Normal | Stat. |  | 100 | 40 | def down 2 | runs | 37 | 26 |  |  | 12 | 1 |  | 9 |
| Secret Power | Normal | Phys. | 70 | 100 | 20 | secret power (30%) | runs | 161 |  | 161 |  |  |  | TM43 |  |
| Seed Bomb | Grass | Phys. | 80 | 100 | 15 | plain hit | runs | 27 | 5 |  | 23 | 3 | 18 | tutor |  |
| Seed Flare | Grass | Spec. | 120 | 85 | 5 | lower sp. def 2 hit (40%) | runs | 1 | 1 |  |  |  | 100 |  |  |
| Seismic Toss | Fighting | Phys. | 1 | 100 | 20 | level damage flat | runs | 4 | 4 |  |  |  | 1 |  | 3 |
| Selfdestruct | Normal | Phys. | 200 | 100 | 5 | halve defense | runs | 6 | 5 |  |  | 1 | 18 |  | 1 |
| Shadow Ball | Ghost | Spec. | 80 | 100 | 15 | lower sp. def hit (20%) | runs | 76 | 10 | 69 |  |  | 1 | TM30 | 3 |
| Shadow Claw | Ghost | Phys. | 70 | 100 | 15 | high critical | runs | 30 | 5 | 27 |  |  | 1 | TM65 |  |
| Shadow Force | Ghost | Phys. | 120 | 100 | 5 | shadow force | runs | 1 | 1 |  |  |  | 40 |  |  |
| Shadow Punch | Ghost | Phys. | 95 | always | 20 | bypass accuracy | runs | 3 | 3 |  |  |  | 1 |  |  |
| Shadow Sneak | Ghost | Phys. | 40 | 100 | 30 | priority 1 | runs | 7 | 5 |  |  | 3 | 1 |  |  |
| Sharpen | Normal | Stat. |  | always | 3 | atk up | runs | 2 | 2 |  |  |  | 5 |  |  |
| Sheer Cold | Ice | Spec. | 1 | 30 | 5 | one hit ko | runs | 7 | 7 |  |  |  | 1 |  |  |
| Shell Smash | Normal | Stat. |  | always | 15 | atk sp. atk speed up 2 def sp. def down | runs | 1 | 1 |  |  |  | 60 |  |  |
| Shelter | Steel | Stat. |  | always | 10 | def up 2 | runs | 1 | 1 |  |  |  | 1 |  |  |
| Shift Gear | Steel | Stat. |  | always | 10 | speed up 2 atk up | runs | 1 | 1 |  |  |  | 48 |  |  |
| Shock Wave | Electric | Spec. | 60 | always | 20 | bypass accuracy | runs | 65 | 5 | 62 |  |  | 19 | TM34 |  |
| Shore Up | Ground | Stat. |  | always | 5 | heal half more in sun | partial | 1 | 1 |  |  |  | 52 |  |  |
| Signal Beam | Bug | Spec. | 75 | 100 | 15 | confuse hit (10%) | runs | 56 | 6 |  | 54 | 7 | 1 | tutor |  |
| Silver Wind | Bug | Spec. | 60 | 100 | 5 | raise all stats hit (10%) | runs | 19 | 5 | 18 |  | 2 | 24 | TM62 |  |
| Sing | Normal | Stat. |  | 55 | 15 | status sleep | runs | 13 | 10 |  |  | 3 | 1 |  | 5 |
| Sketch | Normal | Stat. |  | always | 1 | learn move permanent | runs | 0 |  |  |  |  |  |  | 1 |
| Skill Swap | Psychic | Stat. |  | always | 2 | switch abilities | runs | 26 | 4 | 23 |  |  | 33 | TM48 |  |
| Skitter Smack | Bug | Phys. | 70 | 100 | 10 | lower sp. atk hit | runs | 1 | 1 |  |  |  | 22 |  |  |
| Skull Bash | Normal | Phys. | 130 | 100 | 10 | charge turn def up | runs | 5 | 4 |  |  | 1 | 31 |  |  |
| Sky Attack | Flying | Phys. | 140 | 100 | 5 | charge turn high crit flinch (30%) | runs | 9 | 7 |  |  | 3 | 1 |  |  |
| Sky Drop | Flying | Phys. | 60 | 100 | 10 | plain hit | partial | 1 | 1 |  |  |  | 20 |  |  |
| Sky Uppercut | Fighting | Phys. | 85 | 90 | 15 | hit fly | runs | 5 | 3 |  |  | 2 | 33 |  |  |
| Slack Off | Normal | Stat. |  | always | 10 | restore half hp | runs | 3 | 2 |  |  | 1 | 1 |  |  |
| Slam | Normal | Phys. | 100 | 100 | 20 | plain hit | runs | 19 | 13 |  |  | 8 | 1 |  | 1 |
| Slash | Normal | Phys. | 70 | 100 | 20 | high critical | runs | 29 | 26 |  |  | 3 | 1 |  | 1 |
| Sleep Powder | Grass | Stat. |  | 75 | 15 | status sleep | runs | 4 | 2 |  |  | 2 | 5 |  |  |
| Sleep Talk | Normal | Stat. |  | always | 10 | use random learned move sleep | runs | 161 | 1 | 161 |  | 6 | 28 | TM82 |  |
| Sludge | Poison | Spec. | 65 | 100 | 20 | poison hit (30%) | runs | 2 | 2 |  |  |  | 24 |  |  |
| Sludge Bomb | Poison | Spec. | 90 | 100 | 10 | poison hit (30%) | runs | 30 | 4 | 28 |  |  | 40 | TM36 |  |
| Sludge Wave | Poison | Spec. | 95 | 100 | 10 | poison hit (10%) | runs | 2 | 2 |  |  |  | 46 |  |  |
| Smack Down | Rock | Phys. | 50 | 100 | 15 | smack down | runs | 6 | 6 |  |  |  | 1 |  |  |
| Smart Strike | Steel | Phys. | 70 | always | 10 | bypass accuracy | runs | 2 | 2 |  |  |  | 16 |  |  |
| SmellingSalt | Normal | Phys. | 70 | 100 | 10 | double power and cure paralysis | runs | 7 | 1 |  |  | 6 | 22 |  |  |
| Smog | Poison | Spec. | 55 | 100 | 20 | poison hit (30%) | runs | 10 | 9 |  |  | 1 | 1 |  |  |
| SmokeScreen | Normal | Stat. |  | 100 | 20 | acc down | runs | 8 | 6 |  |  | 2 | 1 |  |  |
| Snarl | Dark | Spec. | 55 | 100 | 15 | lower sp. atk hit | runs | 1 | 1 |  |  |  | 13 |  |  |
| Snatch | Dark | Stat. |  | always | 10 | steal status move | runs | 27 | 1 | 26 |  |  | 39 | TM49 |  |
| Snore | Normal | Spec. | 80 | 100 | 15 | damage while asleep (30%) | runs | 157 | 3 |  | 157 | 8 | 28 | tutor |  |
| Soak | Water | Stat. |  | 100 | 20 | change to water type | runs | 3 | 3 |  |  |  | 29 |  |  |
| Softboiled | Normal | Stat. |  | always | 10 | restore half hp | runs | 1 | 1 |  |  |  | 12 |  |  |
| Solar Blade | Grass | Phys. | 125 | 100 | 10 | skip charge turn in sun | runs | 3 | 3 |  |  |  | 1 |  |  |
| SolarBeam | Grass | Spec. | 120 | 100 | 10 | skip charge turn in sun | runs | 53 | 7 | 50 |  |  | 1 | TM22 |  |
| SonicBoom | Normal | Spec. | 1 | 100 | 20 | 20 damage flat | runs | 4 | 4 |  |  |  | 1 |  | 2 |
| Spacial Rend | Dragon | Spec. | 100 | 95 | 5 | high critical | runs | 1 | 1 |  |  |  | 40 |  |  |
| Spark | Electric | Phys. | 65 | 100 | 20 | paralyze hit (30%) | runs | 13 | 12 |  |  | 1 | 13 |  | 8 |
| Sparkling Aria | Water | Spec. | 90 | 100 | 10 | plain hit | runs | 1 | 1 |  |  |  | 36 |  |  |
| Speed Swap | Psychic | Stat. |  | always | 10 | plain hit | no effect | 1 | 1 |  |  |  | 55 |  |  |
| Spider Web | Bug | Stat. |  | always | 10 | prevent escape | runs | 2 | 2 |  |  |  | 1 |  |  |
| Spike Cannon | Normal | Phys. | 20 | 100 | 15 | multi hit | runs | 3 | 3 |  |  |  | 29 |  |  |
| Spikes | Ground | Stat. |  | always | 20 | set spikes | runs | 8 | 6 |  |  | 2 | 1 |  |  |
| Spiky Shield | Grass | Stat. |  | always | 5 | protect | partial | 2 | 2 |  |  |  | 1 |  |  |
| Spirit Shackle | Ghost | Phys. | 90 | 100 | 10 | prevent escape hit | runs | 1 | 1 |  |  |  | 34 |  |  |
| Spit Up | Normal | Spec. | 1 | 100 | 10 | spit up | runs | 12 | 7 |  |  | 5 | 25 |  | 2 |
| Spite | Ghost | Stat. |  | 100 | 10 | decrease last move pp | runs | 28 | 4 |  | 27 | 6 | 1 | tutor |  |
| Splash | Normal | Stat. |  | always | 40 | do nothing | runs | 13 | 6 |  |  | 7 | 1 |  | 3 |
| Spore | Grass | Stat. |  | 100 | 15 | status sleep | runs | 1 | 1 |  |  |  | 45 |  |  |
| Stealth Rock | Rock | Stat. |  | always | 20 | stealth rock | runs | 45 | 6 | 39 |  |  | 18 | TM76 |  |
| Steel Roller | Steel | Phys. | 130 | 100 | 5 | end terrain | stub, hits | 2 | 2 |  |  |  | 1 |  |  |
| Steel Wing | Steel | Phys. | 70 | 90 | 25 | raise def hit (10%) | runs | 23 | 2 | 22 |  |  | 20 | TM47 |  |
| Sticky Web | Bug | Stat. |  | always | 20 | sticky web | runs | 5 | 5 |  |  |  | 1 |  |  |
| Stockpile | Normal | Stat. |  | always | 20 | stockpile | runs | 14 | 9 |  |  | 5 | 5 |  | 1 |
| Stomp | Normal | Phys. | 65 | 100 | 20 | flinch minimize double hit (30%) | runs | 19 | 14 |  |  | 5 | 1 |  | 1 |
| StompingTantrum | Ground | Phys. | 75 | 100 | 10 | plain hit | runs | 3 | 3 |  |  |  | 20 |  |  |
| Stone Edge | Rock | Phys. | 100 | 80 | 5 | high critical | runs | 50 | 12 | 45 |  |  | 39 | TM71 |  |
| Strange Steam | Fairy | Spec. | 90 | 100 | 10 | confuse hit (20%) | runs | 1 | 1 |  |  |  | 48 |  |  |
| Strength | Normal | Phys. | 80 | 100 | 15 | plain hit | runs | 96 |  | 96 |  |  |  | HM04 |  |
| Strength Sap | Grass | Stat. |  | 100 | 10 | strength sap | runs | 1 | 1 |  |  |  | 1 |  |  |
| String Shot | Bug | Stat. |  | 100 | 40 | speed down | runs | 5 | 5 |  |  |  | 1 |  |  |
| Struggle Bug | Bug | Spec. | 50 | 100 | 10 | lower sp. atk hit | runs | 6 | 6 |  |  |  | 1 |  |  |
| Stun Spore | Grass | Stat. |  | 75 | 30 | status paralyze | runs | 9 | 8 |  |  | 1 | 1 |  |  |
| Submission | Fighting | Phys. | 80 | 80 | 20 | recoil quarter | runs | 5 | 5 |  |  |  | 1 |  | 2 |
| Substitute | Normal | Stat. |  | always | 2 | set substitute | runs | 161 | 2 | 161 |  | 12 | 29 | TM90 | 2 |
| Sucker Punch | Dark | Phys. | 70 | 100 | 5 | hit first if target attacking | runs | 36 | 17 |  | 29 | 6 | 22 | tutor | 1 |
| Sunny Day | Fire | Stat. |  | always | 1 | weather sun | runs | 116 | 9 | 114 |  |  | 1 | TM11 |  |
| Super Fang | Normal | Phys. | 1 | 90 | 10 | halve hp | runs | 5 | 5 |  |  |  | 29 |  |  |
| Superpower | Fighting | Phys. | 120 | 100 | 5 | lower own atk and def | runs | 33 | 9 |  | 31 | 3 | 25 | tutor |  |
| Supersonic | Normal | Stat. |  | 55 | 20 | status confuse | runs | 23 | 14 |  |  | 10 | 1 |  | 2 |
| Surf | Water | Spec. | 90 | 100 | 15 | double damage dive | runs | 56 | 1 | 55 |  |  | 40 | HM03 |  |
| Swagger | Normal | Stat. |  | 90 | 15 | atk up 2 status confusion | runs | 163 | 17 | 161 |  | 3 | 1 | TM87 | 7 |
| Swallow | Normal | Stat. |  | always | 10 | swallow | runs | 13 | 8 |  |  | 5 | 5 |  | 1 |
| Sweet Kiss | Fairy | Stat. |  | 100 | 10 | status confuse | runs | 12 | 8 |  |  | 4 | 1 |  | 8 |
| Sweet Scent | Normal | Stat. |  | 100 | 20 | eva down | runs | 15 | 13 |  |  | 2 | 1 |  | 1 |
| Swift | Normal | Spec. | 60 | always | 20 | bypass accuracy | runs | 93 | 14 |  | 92 |  | 1 | tutor | 2 |
| Switcheroo | Dark | Stat. |  | 100 | 10 | switch held items | runs | 1 |  |  |  | 1 |  |  |  |
| Swords Dance | Normal | Stat. |  | always | 1 | atk up 2 | runs | 43 | 11 | 40 |  | 4 | 11 | TM75 |  |
| Synthesis | Grass | Stat. |  | always | 5 | heal half more in sun | runs | 23 | 14 |  | 16 | 5 | 1 | tutor |  |
| Tackle | Normal | Phys. | 40 | 100 | 35 | plain hit | runs | 66 | 66 |  |  |  | 1 |  | 7 |
| Tail Glow | Bug | Stat. |  | always | 1 | sp. atk up 2 | runs | 1 | 1 |  |  |  | 1 |  |  |
| Tail Slap | Normal | Phys. | 25 | 100 | 10 | multi hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Tail Whip | Normal | Stat. |  | 100 | 3 | def down | runs | 22 | 21 |  |  | 1 | 1 |  | 6 |
| Tailwind | Flying | Stat. |  | always | 1 | double speed 3 turns | runs | 9 | 9 |  |  |  | 25 |  |  |
| Take Down | Normal | Phys. | 90 | 100 | 20 | recoil quarter | runs | 40 | 33 |  |  | 9 | 1 |  | 3 |
| Taunt | Dark | Stat. |  | 100 | 20 | taunt | runs | 51 | 14 | 46 |  |  | 1 | TM12 | 3 |
| Tearful Look | Normal | Stat. |  | always | 10 | tearful look | runs | 1 | 1 |  |  |  | 6 |  |  |
| Teatime | Normal | Stat. |  | always | 10 | plain hit | no effect | 1 | 1 |  |  |  | 1 |  |  |
| Teeter Dance | Normal | Stat. |  | 100 | 20 | confuse all | runs | 4 | 3 |  |  | 1 | 23 |  |  |
| Telekinesis | Psychic | Stat. |  | always | 15 | plain hit | no effect | 1 | 1 |  |  |  | 40 |  |  |
| Teleport | Psychic | Stat. |  | always | 20 | flee from wild battle | runs | 3 | 3 |  |  |  | 1 |  | 2 |
| Terrain Pulse | Normal | Spec. | 50 | 100 | 10 | plain hit | partial | 1 | 1 |  |  |  | 38 |  |  |
| Thief | Dark | Phys. | 60 | 100 | 25 | steal held item | runs | 66 | 2 | 65 |  |  | 20 | TM46 |  |
| Thousand Arrows | Ground | Phys. | 90 | 100 | 10 | smack down | runs | 1 | 1 |  |  |  | 1 |  |  |
| Thousand Waves | Ground | Phys. | 90 | 100 | 10 | prevent escape hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Thrash | Normal | Phys. | 120 | 100 | 10 | continue and confuse self | runs | 12 | 5 |  |  | 8 | 23 |  |  |
| Thunder | Electric | Spec. | 110 | 70 | 10 | thunder (30%) | runs | 58 | 8 | 57 |  |  | 38 | TM25 | 2 |
| Thunder Fang | Electric | Phys. | 90 | 100 | 15 | flinch paralyze hit (10%) | runs | 13 | 10 |  |  | 6 | 1 |  | 4 |
| Thunder Wave | Electric | Stat. |  | 100 | 20 | status paralyze | runs | 55 | 13 | 52 |  | 1 | 1 | TM73 | 9 |
| ThunderPunch | Electric | Phys. | 95 | 100 | 15 | paralyze hit (10%) | runs | 50 | 7 |  | 49 | 7 | 1 | tutor |  |
| ThunderShock | Electric | Spec. | 40 | 100 | 30 | paralyze hit (10%) | runs | 11 | 11 |  |  |  | 1 |  | 4 |
| Thunderbolt | Electric | Spec. | 90 | 100 | 15 | paralyze hit (10%) | runs | 61 | 5 | 58 |  |  | 1 | TM24 | 3 |
| Thunderous Kick | Fighting | Phys. | 90 | 100 | 10 | lower defense hit | runs | 1 | 1 |  |  |  | 45 |  |  |
| Tickle | Normal | Stat. |  | 100 | 20 | atk def down | runs | 23 | 9 |  |  | 14 | 1 |  | 2 |
| Topsy-Turvy | Dark | Stat. |  | always | 20 | plain hit | no effect | 1 | 1 |  |  |  | 50 |  |  |
| Torment | Dark | Stat. |  | 100 | 15 | torment | runs | 46 | 4 | 43 |  |  | 1 | TM41 |  |
| Toxic | Poison | Stat. |  | 100 | 10 | status badly poison | runs | 166 | 10 | 161 |  |  | 1 | TM06 |  |
| Toxic Spikes | Poison | Stat. |  | always | 20 | toxic spikes | runs | 10 | 10 |  |  |  | 1 |  | 2 |
| Transform | Normal | Stat. |  | always | 10 | transform | runs | 0 |  |  |  |  |  |  |  |
| Tri Attack | Normal | Spec. | 80 | 100 | 10 | tri attack (20%) | runs | 1 | 1 |  |  |  | 1 |  |  |
| Trick | Psychic | Stat. |  | 100 | 10 | switch held items | runs | 32 | 5 |  | 29 | 2 | 1 | tutor | 5 |
| Trick Room | Psychic | Stat. |  | always | 5 | trick room | runs | 25 | 3 | 22 |  |  | 46 | TM92 |  |
| Triple Axel | Ice | Phys. | 20 | 90 | 10 | hit three times increment base power 20 | runs | 3 | 3 |  |  |  | 1 |  |  |
| Triple Kick | Fighting | Phys. | 10 | 90 | 10 | hit three times | runs | 1 | 1 |  |  |  | 30 |  |  |
| Trop Kick | Grass | Phys. | 85 | 100 | 15 | lower attack hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Trump Card | Normal | Spec. | 1 | always | 5 | higher power when low pp | runs | 3 | 3 |  |  |  | 48 |  |  |
| Twineedle | Bug | Phys. | 40 | 100 | 20 | poison multi hit (20%) | runs | 1 | 1 |  |  |  | 8 |  |  |
| Twister | Dragon | Spec. | 40 | 100 | 20 | flinch double damage fly or bounce (20%) | runs | 32 | 2 |  | 31 | 3 | 17 | tutor |  |
| U-turn | Bug | Phys. | 70 | 100 | 20 | switch hit | runs | 35 | 11 | 28 |  |  | 1 | TM89 |  |
| Uproar | Normal | Spec. | 90 | 100 | 10 | uproar | runs | 51 | 7 |  | 49 | 2 | 8 | tutor | 1 |
| Vacuum Wave | Fighting | Spec. | 40 | 100 | 30 | priority 1 | runs | 14 | 3 |  | 11 | 2 | 1 | tutor |  |
| Venom Drench | Poison | Stat. |  | 100 | 20 | venom drench | runs | 4 | 4 |  |  |  | 13 |  |  |
| Venoshock | Poison | Spec. | 65 | 100 | 10 | double power on poisoned | runs | 5 | 5 |  |  |  | 19 |  |  |
| ViceGrip | Normal | Phys. | 55 | 100 | 30 | plain hit | runs | 4 | 4 |  |  |  | 1 |  |  |
| Vine Whip | Grass | Phys. | 45 | 100 | 25 | plain hit | runs | 3 | 3 |  |  |  | 1 |  | 1 |
| Vital Throw | Fighting | Phys. | 70 | always | 10 | priority neg 1 bypass accuracy | runs | 3 | 3 |  |  |  | 10 |  | 2 |
| Volt Switch | Electric | Spec. | 70 | 100 | 20 | switch hit | runs | 2 | 2 |  |  |  | 40 |  |  |
| Volt Tackle | Electric | Phys. | 120 | 100 | 15 | recoil paralyze hit (10%) | runs | 1 | 1 |  |  |  | 64 |  |  |
| Wake-Up Slap | Fighting | Phys. | 70 | 100 | 10 | double power heal sleep | runs | 12 | 9 |  |  | 4 | 22 |  | 5 |
| Water Gun | Water | Spec. | 40 | 100 | 25 | plain hit | runs | 32 | 31 |  |  | 1 | 1 |  | 2 |
| Water Pulse | Water | Spec. | 60 | 100 | 20 | confuse hit (20%) | runs | 76 | 22 | 72 |  |  | 1 | TM03 | 2 |
| Water Shuriken | Water | Spec. | 15 | 100 | 20 | multi hit | runs | 1 | 1 |  |  |  | 1 |  |  |
| Water Sport | Water | Stat. |  | always | 15 | halve fire damage | runs | 21 | 16 |  |  | 8 | 1 |  | 1 |
| Water Spout | Water | Spec. | 150 | 100 | 5 | decrease power with less user hp | runs | 2 | 2 |  |  |  | 34 |  |  |
| Waterfall | Water | Phys. | 80 | 100 | 15 | flinch hit (20%) | runs | 39 | 2 | 38 |  |  | 30 | HM07 |  |
| Weather Ball | Normal | Spec. | 50 | 100 | 10 | change type with weather | runs | 3 | 3 |  |  |  | 1 |  |  |
| Whirlpool | Water | Spec. | 35 | 100 | 15 | whirlpool | runs | 14 | 11 |  |  | 4 | 1 |  |  |
| Whirlwind | Normal | Stat. |  | always | 20 | force switch | runs | 17 | 9 |  |  | 8 | 1 |  |  |
| Wide Guard | Rock | Stat. |  | always | 10 | protect user side | runs | 8 | 8 |  |  |  | 1 |  |  |
| Wild Charge | Electric | Phys. | 90 | 100 | 15 | recoil third | runs | 3 | 3 |  |  |  | 40 |  |  |
| Will-O-Wisp | Fire | Stat. |  | 85 | 15 | status burn | runs | 31 | 10 | 22 |  | 4 | 1 | TM61 |  |
| Wing Attack | Flying | Phys. | 60 | 100 | 35 | plain hit | runs | 12 | 10 |  |  | 3 | 1 |  |  |
| Wish | Normal | Stat. |  | always | 10 | heal in 3 turns | runs | 15 | 6 |  |  | 9 | 1 |  |  |
| Withdraw | Water | Stat. |  | always | 3 | def up | runs | 9 | 9 |  |  |  | 1 |  | 1 |
| Wonder Room | Psychic | Stat. |  | always | 10 | wonder room | runs | 1 | 1 |  |  |  | 65 |  |  |
| Wood Hammer | Grass | Phys. | 120 | 100 | 15 | recoil third | runs | 4 | 4 |  |  |  | 1 |  |  |
| Worry Seed | Grass | Stat. |  | 100 | 10 | set ability to insomnia | runs | 11 | 7 |  |  | 6 | 16 |  |  |
| Wrap | Normal | Phys. | 15 | 90 | 20 | bind hit | runs | 8 | 8 |  |  |  | 1 |  | 1 |
| Wring Out | Normal | Spec. | 1 | 100 | 5 | increase power with more hp | runs | 9 | 9 |  |  | 1 | 1 |  |  |
| X-Scissor | Bug | Phys. | 80 | 100 | 15 | plain hit | runs | 23 | 9 | 18 |  |  | 1 | TM81 | 1 |
| Yawn | Normal | Stat. |  | always | 10 | status sleep next turn | runs | 18 | 11 |  |  | 7 | 1 |  |  |
| Zap Cannon | Electric | Spec. | 120 | 50 | 5 | paralyze hit | runs | 8 | 8 |  |  |  | 54 |  |  |
| Zen Headbutt | Psychic | Phys. | 80 | 100 | 15 | flinch hit (20%) | runs | 41 | 12 |  | 40 | 5 | 1 | tutor |  |
| Zing Zap | Electric | Phys. | 80 | 100 | 10 | flinch hit (30%) | runs | 1 | 1 |  |  |  | 34 |  |  |
