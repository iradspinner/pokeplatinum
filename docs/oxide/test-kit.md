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
| `TestKitSetPartyMonForm`, the kit's one script command | `#ifdef` blocks at the end of `include/data/scripts/scrcmd.h`, `src/scrcmd_party.c` and `asm/macros/scrcmd.inc`, so no existing opcode moves |

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
| 27 | Sticky Web, Spikes, Stealth Rock, Defog | this batch; Sticky Web prints the foe's-side line and fails a second time, and Defog blows it away with the other two. The switch-in Speed drop needs a trainer battle, so it waits for kit trainers |

**When a batch of effect scripts lands, add its sets in the same commit**: a
`TestKit_MoveSetN` block, an `AddListMenuEntry` line in `TestKit_MoveSets`, and
a `TestKit_Text_MenuSetN` message in `res/testkit/twinleaf_town_player_house_2f.json`.
Pair a move that needs a condition with the move that sets it up, as sets 3, 5,
8 and 9 do.

## Not built yet

Kit-only trainers whose teams use the new moves, so the AI's side gets seen too.
Ian chose move sets first; trainers are the next step when he wants them.
Whether an appended trainer needs rows elsewhere, such as the trainer message
table, is to be checked before they are built.
