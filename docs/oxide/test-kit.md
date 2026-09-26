# The test kit

A build of the game with a helper in the player's bedroom, so an emulator check
takes a new game and a few menu choices instead of a play-through. Proposed on
2026-09-22 and approved by Ian the same day, with these choices: build it, put
the NPC in the bedroom, start with move sets rather than trainers, and give the
kit its own form command rather than warping to Rotom's room.

## Getting the ROM

```
tools/oxide/fetch-rom --testkit [commit]   # the playtest copy, built on GitHub
make testkit                               # a local build, for development only
```

`fetch-rom --testkit` asks the private builder for `make testkit` instead of
`make rom` and downloads `pokeplatinum-oxide-testkit-<commit>.nds`, checked
against the builder's SHA-1, as it does for the ordinary ROM. Hand Ian that
copy, not one built on this CPU. The local build writes
`build-testkit/pokeplatinum.us.nds`.

## Why the ROM of record cannot change

The kit is a meson option, `oxide_testkit`, off by default. Meson remembers an
option in the build folder once set, so `make testkit` sets it up in its own
folder, `build-testkit/`, and `build/` never carries it. GitHub's workflow and
the builder's ordinary builds run `make rom`, so the ROM whose hash they print
is the same with or without the kit's source in the tree. That is checked by
building `make rom` on the kit's branch and matching the hash GitHub printed
for its base commit.

With the option on:

| Piece | How it stays out of a normal build |
|---|---|
| The NPC's script, at the end of `scripts_twinleaf_town_player_house_2f.s` | an `#ifdef OXIDE_TESTKIT` block; field scripts run through the C preprocessor, and `make_script_bin.sh --define` passes the symbol |
| The NPC's object event and its text | fragments in `res/testkit/`, appended to the bedroom's real events file and text bank at build time by `tools/oxide/testkit_merge.py`, so the kit never keeps a copy that could drift |
| `TestKitSetPartyMonForm`, `TestKitSetPartyMonAbility` and `TestKitStartWildBattle`, the kit's three script commands | `#ifdef` blocks at the end of `include/data/scripts/scrcmd.h` and `asm/macros/scrcmd.inc`, and in `src/scrcmd_party.c`, `src/scrcmd.c`, `src/encounter.c` and `include/encounter.h`, so no existing opcode moves |

## What the NPC hands out

The NPC stands in the bedroom's bottom-left corner. Its menu:

| Entry | What it gives | The check it serves |
|---|---|---|
| 99 Rare Candies | the item | Rare Candy chaining: after one, the party menu reopens |
| Rotom and Giratina | Rotom in Wash form (Lv. 30), Giratina in Origin form holding the Griseous Orb (Lv. 50) | the element 3 form fix: each summary shows its form's stats and types |
| Eevee with Charm | Eevee, Lv. 20, Charm in its first slot | Sylveon: one Rare Candy should evolve it |
| Klefki, Lv. 5 | Klefki, which learns Fairy Wind (move 587) at Lv. 6 | the widened learnset: one Rare Candy teaches a move the old format could not hold; then the Move Relearner |
| Gible vs. Clefairy | Gible, Lv. 20, with Dragon Claw, then a wild Clefairy, Lv. 10 | Fairy: the Dragon move does nothing |
| New move sets | a Lv. 50 Mew knowing four of the new moves (sets below) | the battle effect scripts, from the player's side |
| Wild Chansey | a wild Chansey, Lv. 50 | a target for special moves |
| Wild Shuckle | a wild Shuckle, Lv. 50 | a target for physical moves: Chansey faints before an extra like Sappy Seed's seed, Axe Kick's confusion or a flinch can show, and Shuckle is slower than Mew |
| Wild Lugia | a wild Lugia, Lv. 2, which knows only Whirlwind | an attacker that uses Whirlwind every turn, for the Roar and Whirlwind Ingrain fix (set 25) |
| Wild Skarmory | a wild Skarmory, Lv. 50 | a Flying target bulky enough to survive Smack Down and Thousand Arrows (set 26) |
| Wild Horsea | a wild Horsea, Lv. 1, which knows only Bubble | a spread move every turn, for Wide Guard (set 30) |
| Wild Glameow | a wild Glameow, Lv. 1, which knows only Fake Out | a priority move on the first turn, for Quick Guard (set 30) |
| Abilities | a Lv. 50 Pokemon that carries one of the new abilities, set on it whatever its personality rolls, with four moves (entries below) | element 5's ability effects |
| Warp | Twinleaf, Sandgem, Sandgem's Pokemon Center, Jubilife, Pastoria, Veilstone | the Sandgem UNLOCK FPS crash, the nurse, Route 202's trainers, the Move Relearner, the TM shop |

Warps to a town land on its fly point, and the Pokemon Center warp lands where
a whiteout does. A warp ahead of the story can meet story scripts in the
destination; that is the kit's nature, not a defect.

## The move sets

One set per four moves, a batch of effect scripts at a time. Each is a block in
the kit script that loads four move ids into `VAR_0x8006` to `VAR_0x8009` and
jumps to `TestKit_GiveMew`, or sets a species in `VAR_0x800A` and jumps to
`TestKit_GivePokemonWithMoves` when a move needs a particular user.

| Set | Moves | Batch |
|---|---|---|
| 1 | Population Bomb, Triple Dive, Sappy Seed, Zippy Zap | 388331c51 |
| 2 | Glitzy Glow, Baddy Bad, Freezy Frost, Sparkly Swirl | 388331c51 |
| 3 | Toxic, Infernal Parade, Barb Barrage, Psychic Noise | 388331c51 |
| 4 | Dire Claw, Spin Out, Guardian of Alola, Esper Wing | 388331c51 |
| 5 | Toxic, Venoshock, Hex, Acrobatics | 2f84be2ef |
| 6 | Flame Charge, Axe Kick, Double Iron Bash, Triple Axel | 2f84be2ef |
| 7 | Relic Song, Surging Strikes, Spin Out, Bolt Beak | 2f84be2ef; Spin Out slows Mew so Bolt Beak can be seen moving second |
| 8 | Rain Dance, Hurricane, Wildbolt Storm, Bleakwind Storm | 5d1d1a970 |
| 9 | Sunny Day, Sandsear Storm, Diamond Storm, First Impression | 5d1d1a970 |
| 10 | Hone Claws, Quiver Dance, Coil, Shift Gear | 7a7df8b7d to 59e966cf0 |
| 11 | Shell Smash, Work Up, Victory Dance, Cotton Guard | same |
| 12 | Fillet Away, Clangorous Soul, Geomancy, Take Heart | same |
| 13 | V-create, Clanging Scales, Hyperspace Fury, Spicy Extract | same |
| 14 | Poltergeist, Fickle Beam, Matcha Gotcha, Anchor Shot | same; Poltergeist fails against a target holding nothing |
| 15 | Jaw Lock, Stone Axe, Ceaseless Edge, Mortal Spin | same |
| 16 | Freeze Shock, Ice Burn, Fell Stinger, Double Shock, on Electivire | same; Double Shock needs an Electric user |
| 17 | Burn Up, Clear Smog, Final Gambit, Chloroblast, on Magmortar | same; Burn Up needs a Fire user |
| 18 | Draining Kiss, Oblivion Wing, Noble Roar, Tearful Look | 9664a529a |
| 19 | Toxic, Venom Drench, Heal Pulse, Life Dew | 9664a529a; Venom Drench needs a poisoned target |
| 20 | Pollen Puff, Strength Sap, Guard Split, Power Split | 9664a529a and a32b5ab7d |
| 21 | Soak, Thunderbolt, Incinerate, Coaching | same; Coaching needs a double battle, so here it should fail |
| 22 | Heavy Slam, Heat Crash, Autotomize, Swords Dance, on Metagross | a32b5ab7d; weight-based power needs a heavy user |
| 23 | Dragon Tail, Circle Throw, Parting Shot, Roar | 38766c70a; against a wild Pokemon Dragon Tail and Circle Throw end the battle, and Roar checks its reshaped code behaves as before |
| 24 | Laser Focus, Tackle, Lock-On, Zap Cannon | 7f36c7172; against Shuckle, Tackle lands a critical hit on the turn after Laser Focus and only then, and Zap Cannon still never misses the turn after Lock-On, which counts down beside Laser Focus |
| 25 | Ingrain, Aqua Ring, Splash, Recover | the vanilla Ingrain fix; against the wild Lugia, Ingrain then Aqua Ring, and Lugia's Whirlwind should fail every turn with "anchored itself with its roots", where vanilla ended the battle once Aqua Ring was up |
| 26 | Smack Down, Earthquake, Thousand Arrows, Recover | fe6cc4437; against the wild Skarmory, Earthquake does nothing until Smack Down prints "fell straight down!", then hits; Thousand Arrows hits it at once, super effective through Steel, and grounds it too |
| 27 | Sticky Web, Spikes, Stealth Rock, Defog | a3b9dc1c; Sticky Web prints the foe's-side line and fails a second time, and Defog blows it away with the other two. The switch-in Speed drop needs a trainer battle, so it waits for kit trainers |
| 28 | After You, Trick Room, Tackle, Recover | e55fd3cf; against the wild Shuckle, After You prints "took the kind offer!" and Shuckle moves next; with Trick Room up, Shuckle moves first and After You fails. Moving an ally's turn needs a double battle |
| 29 | Aurora Veil, Hail, Recover, Splash | 256a4d8b; Aurora Veil fails before Hail, then goes up with "raised your team's Defense and Special Defense!", fails a second time, and wears off five turns later. Brick Break and Defog clearing it need a foe that sets one, which the kit does not have |
| 30 | Wide Guard, Quick Guard, Mat Block, Crafty Shield | 43043ccb; each guard prints "protected your team!" and then "protected MEW!" against its foe: Wide Guard against the wild Horsea's Bubble, Quick Guard against the wild Glameow's Fake Out, Mat Block against the wild Skarmory on the first turn only (it fails after that), and Crafty Shield against the wild Lugia's Whirlwind. Each guard lets the other kinds through. Guarding an ally needs a double battle |
| 31 | Belch, Belly Drum, Recover, Splash | 7b704a8c; the set also puts a Sitrus Berry in the bag, for Ian to give to Mew. Before Mew has eaten it, choosing Belch prints "hasn't eaten a Berry, so it can't possibly belch!" and Belch cannot be picked; Belly Drum halves Mew's HP, the Berry heals it, and from then Belch can be chosen, still after switching out and back |

**When a batch of effect scripts lands, add its sets in the same commit**: a
`TestKit_MoveSetN` block, an `AddListMenuEntry` line in `TestKit_MoveSets`, and
a `TestKit_Text_MenuSetN` message in `res/testkit/twinleaf_town_player_house_2f.json`.
Pair a move that needs a condition with the move that sets it up, as sets 3, 5,
8 and 9 do.

## The ability entries

One entry per new ability (element 5), under "Abilities". Each gives a Lv. 50
Pokemon of a species that carries the ability, with the ability set by the
kit's `TestKitSetPartyMonAbility` so the personality roll cannot give it the
species' other ability, and four moves chosen to show it. Each entry is a
`TestKit_Ability<Name>` block that sets the species in `VAR_0x800A`, the
ability in `VAR_0x800B` and the moves in `VAR_0x8006` to `VAR_0x8009`, then
jumps to `TestKit_GivePokemonWithMoves`, with an `AddListMenuEntry` line in
`TestKit_Abilities` and a `TestKit_Text_MenuAbility<Name>` message.

An entry for an ability that works when its holder is hit also names a foe,
in `VAR_0x8000` (species), `VAR_0x8001` (its ability, `ABILITY_NONE` to keep
the rolled one) and `VAR_0x8002` (one move, which it then uses every turn, or
`MOVE_NONE` to keep its own). The kit fights it straight after the gift, a
wild Lv. 50 battle through `TestKitStartWildBattle`, a kit-only command that
sets the foe's ability and moves after `Encounter_NewVsSpeciesAtLevel`'s steps.
The new Pokemon is not in the lead, so switch it in on the first turn.

| Entry | Pokemon and moves | What to look for | Batch |
|---|---|---|---|
| Beast Boost | Kartana: Leaf Blade, Sacred Sword, Swords Dance, Night Slash | Knock out any wild Pokemon: straight after "fainted!", "KARTANA's Beast Boost raised its Attack!" (Attack is Kartana's highest stat). Nothing on a turn it does not knock anything out | 2f8d27c3 |
| Soul Heart | Magearna: Fleur Cannon, Flash Cannon, Dazzling Gleam, Calm Mind | When the wild Pokemon faints, "MAGEARNA's Soul Heart raised its Sp. Atk!"; it also fires when one of your own Pokemon faints with Magearna on the field, which needs a double battle | 2f8d27c3 |
| Sap Sipper | Goodra: Dragon Pulse, Sludge Bomb, Thunderbolt, Rest; foe a wild Bellsprout that knows only Vine Whip | Vine Whip does no damage: "GOODRA's Sap Sipper raised its Attack!", and at +6 "made Vine Whip useless!" | 78628e1e |
| Bulletproof | Kommo-o: Clanging Scales, Dragon Dance, Close Combat, Iron Defense; foe a wild Chansey that knows only Egg Bomb | "KOMMO-O's Bulletproof blocks Egg Bomb!" every turn | 78628e1e |
| Overcoat | Mandibuzz: Sandstorm, Roost, Foul Play, Toxic; foe a wild Paras that knows only Spore | "MANDIBUZZ's Overcoat blocks Spore!"; with Sandstorm up, Paras is buffeted by the sandstorm at the end of each turn and Mandibuzz is not | 78628e1e |
| Purifying Salt | Garganacl: Rest, Salt Cure, Stealth Rock, Recover; foe a wild Gengar that knows only Will-O-Wisp | Will-O-Wisp fails with "GARGANACL's Purifying Salt prevents burns!"; Garganacl's own Rest fails with "stayed awake because of its Purifying Salt!". Its halving of Ghost damage does not show here | 78628e1e |
| Corrosion | Salazzle: Toxic, Poison Gas, Flamethrower, Sludge Bomb; foe a wild Skarmory with its own moves | Toxic and Poison Gas poison the Steel-type Skarmory, where without Corrosion they would not affect it | 78628e1e |
| Competitive | Gothitelle: Psychic, Calm Mind, Thunderbolt, Thunder Wave; foe a wild Chansey that knows only Growl | After "GOTHITELLE's Attack fell!", "GOTHITELLE's Competitive sharply raised its Sp. Atk!" every time | this batch |
| Defiant | Galarian Zapdos: Thunderous Kick, Brave Bird, Bulk Up, Close Combat; foe a wild Chansey that knows only Tail Whip | After its Defense falls, "ZAPDOS's Defiant sharply raised its Attack!"; its own Close Combat lowering its stats does not set it off | this batch |
| Big Pecks | Mandibuzz: Foul Play, Roost, Toxic, Brave Bird; foe a wild Chansey that knows only Tail Whip | "MANDIBUZZ's Big Pecks prevents Defense loss!" every time | this batch |
| Flower Veil | Tsareena, given Flower Veil because none of its carriers is Grass: Trop Kick, Power Whip, Knock Off, Trailblaze; foe a wild Chansey that knows only Growl | "TSAREENA surrounded itself with a veil of petals!" and its Attack stays. A Florges's Flower Veil guarding a Grass-type partner needs a double battle | this batch |
| Contrary | Serperior: Leaf Storm, Giga Drain, Coil, Glare; any foe | Leaf Storm: "SERPERIOR's Sp. Atk sharply rose!"; Coil: its Attack, Defense and accuracy each fall | this batch |
| Mirror Armor | Corviknight: Iron Defense, Body Press, Roost, Iron Head; foe a wild Chansey that knows only Growl | Each Growl lowers the wild Chansey's own Attack, and Corviknight's stays | this batch |

## Not built yet

Kit-only trainers whose teams use the new moves, so the AI's side gets seen too.
Ian chose move sets first; trainers are the next step when he wants them.
Whether an appended trainer needs rows elsewhere, such as the trainer message
table, is to be checked before they are built.
