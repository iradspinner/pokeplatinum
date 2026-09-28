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
| Eevee with Charm | Eevee, Lv. 15, Charm in its first slot (Lv. 20 until element 8, and lowered so a new game's cap of 16 takes the candy) | Sylveon: one Rare Candy should evolve it |
| Klefki, Lv. 5 | Klefki, which learns Fairy Wind (move 587) at Lv. 6 | the widened learnset: one Rare Candy teaches a move the old format could not hold; then the Move Relearner |
| Gible vs. Clefairy | Gible, Lv. 20, with Dragon Claw, then a wild Clefairy, Lv. 10 | Fairy: the Dragon move does nothing |
| New move sets | a Lv. 50 Mew knowing four of the new moves (sets below) | the battle effect scripts, from the player's side |
| Wild Chansey | a wild Chansey, Lv. 50 | a target for special moves |
| Wild Shuckle | a wild Shuckle, Lv. 50 | a target for physical moves: Chansey faints before an extra like Sappy Seed's seed, Axe Kick's confusion or a flinch can show, and Shuckle is slower than Mew |
| Wild Lugia | a wild Lugia, Lv. 2, which knows only Whirlwind | an attacker that uses Whirlwind every turn, for the Roar and Whirlwind Ingrain fix (set 25) |
| Wild Skarmory | a wild Skarmory, Lv. 50 | a Flying target bulky enough to survive Smack Down and Thousand Arrows (set 26) |
| Wild Horsea | a wild Horsea, Lv. 1, which knows only Bubble | a spread move every turn, for Wide Guard (set 30) |
| Wild Glameow | a wild Glameow, Lv. 1, which knows only Fake Out | a priority move on the first turn, for Quick Guard (set 30) |
| Abilities | a Lv. 50 Pokemon that carries one of the new abilities, set on it whatever its personality rolls, with four moves, over three pages, the third for the natives' hidden abilities (entries below) | element 5's ability effects |
| Modern rules | a Lv. 50 Pokemon with four moves, and a wild foe, for each of the staples survey's engine rulings (entries below) | the later games' native abilities, type immunities, critical hits, Defog and Rapid Spin |
| Sprite heights | four wild Pokemon at Lv. 5 in turn: Wooloo, Sinistea, Rookidee, Fletchling | the new species' placement: the first, third and fourth stand on their shadows, Sinistea hovers just above |
| Level caps | puts the player in any of the thirteen level-cap splits, from Roark's (cap 16, where a new game starts) to none, including an earlier one than now (entries below) | element 8's level caps |
| Element 7 items | one of each of the 46 new items, and a battle for each held item (entries below) | element 7's items |
| Warp | Twinleaf, Sandgem, Sandgem's Pokemon Center, Jubilife, Pastoria, Veilstone | the Sandgem UNLOCK FPS crash, the nurse, Route 202's trainers, the Move Relearner, the TM shop |

Warps to a town land on its fly point, and the Pokemon Center warp lands where
a whiteout does. A warp ahead of the story can meet story scripts in the
destination; that is the kit's nature, not a defect.

## The level caps

Element 8 holds each Pokemon at the level cap of the player's split. The
kit's own Pokemon are mostly Lv. 50, above a new game's cap of 16, so they
gain no Exp. and refuse Rare Candies until "Level caps" moves the split on;
"No cap" puts back the vanilla rules. The Level caps menu, after "Which
split?", lists Roark 16, Gardenia 26, Fantina 33, Maylene 39, Wake 44,
Byron 53, Candice 56, Galactic HQ 60, Galactic 65, Volkner 68, Barry 71,
League 78 and No cap, and sets the split outright, which the game's own `RaiseLevelCap`
never does downwards.

With the cap at 16, what to look for:

- Klefki, Lv. 5, takes Rare Candies up to Lv. 16, and the next one "won't
  have any effect" and is not used up.
- A Lv. 50 Pokemon beats a wild Chansey with no Exp. message at all, and its
  effort values still rise (the summary's stats move at its next level).
- A Pokemon one level under the cap stops at the cap however much Exp. it
  earns. Take Klefki to Lv. 15, lead with it against the wild Chansey,
  switch to a Lv. 50 Mew and win: Klefki's message still names the whole
  gain, but it grows to Lv. 16 only, its Exp. bar sits at the start of the
  level, and it is still Lv. 16 after a trip into the PC and back.
- Raising the cap to Gardenia's 26 lets the same Pokemon gain Exp. again.

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
| 32 | Electro Ball, Thunderbolt, Agility, Recover | the Electro Ball fix; the power from the Speed ratio. Against the wild Shuckle, which Mew outpaces four times over, Electro Ball (150) does clearly more than Thunderbolt (90). Against the wild Chansey it does less (60 or 80), until one Agility makes it more (120 or 150). Before the fix it did 1 or 2 HP |
| 33 | Stored Power, Power Trip, Agility, Iron Defense | the Stored Power fix; 20 power and 20 more per raised stage. After one Agility, Stored Power does about three times what it did before (20 to 60), though Agility does not raise Sp. Atk; one Iron Defense does the same for Power Trip, and each further stage adds another 20. Before the fix neither changed |
| 34 | Retaliate, Splash, Recover, Swords Dance, plus a Jirachi with Memento, Healing Wish, Splash, Recover | the Retaliate fix; needs two free party slots, and starts a battle with a wild Chansey that knows only Splash. Switch Jirachi in and use Memento; when it faints, send Mew out. Mew's first Retaliate does about twice what its second does (140 power, then 70). Before the fix the two were the same |
| 35 | Echoed Voice, Hyper Voice, Splash, Recover | the Echoed Voice fix; against the wild Chansey, Echoed Voice used turn after turn does 40, 80, 120, 160 and then 200 power, so the third use already does more than Hyper Voice (90). A turn of Splash (or Recover) in between sets it back to 40. Before the fix it stayed at 40 |
| 36 | Stomping Tantrum, Temper Flare, Snore, Recover | the Stomping Tantrum fix; starts a battle with a wild Chansey that knows only Splash. Snore while awake says "But it failed!", and a Stomping Tantrum (or Temper Flare) the turn after does about twice what one after Recover does (150 power, then 75). Before the fix the two were the same |
| 37 | Last Respects, Splash, Recover, Swords Dance, plus a Jirachi with Memento, Healing Wish, Splash, Recover | the Last Respects fix; needs two free party slots and no fainted Pokemon in the party, and starts a battle with a wild Chansey that knows only Splash. Switch Mew in and use Last Respects; then switch Jirachi in and use Memento, send Mew out again, and Last Respects now does about twice as much (100 power, from 50). Before the fix it stayed at 50 |
| 38 | Hard Press, Body Slam, Recover, Splash | the Hard Press fix; against the wild Chansey at full HP, Hard Press (100) does a little more than Body Slam (85), and once Chansey is below about 85% of its HP it does less, falling as Chansey's HP falls. Before the fix it did almost nothing |
| 39 | Pika Papow, Veevee Volley, Recover, Splash | the Pika Papow fix; against the wild Skarmory, Pika Papow says "It's super effective!", and against the wild Shuckle, Veevee Volley says "It's not very effective...". Before the fix neither message showed, though the damage was already right |
| 40 | Lash Out, Crunch, Recover, Splash | the Lash Out fix; starts a battle with a wild Klefki given Prankster that knows only Tail Whip, so its Tail Whip always goes first. While "MEW's Defense fell!" shows each turn, Lash Out (150 power) does about twice what Crunch (80) does; after six Tail Whips Mew's Defense cannot fall further, and Lash Out (75) does a little less than Crunch. Before the fix it was always the latter |
| 41 | Grav Apple, Seed Bomb, Gravity, Recover | the Grav Apple fix; starts a battle with a wild Chansey given Clear Body, so Grav Apple's Defense drop is blocked, that knows only Splash. Grav Apple (90) does a little more than Seed Bomb (80); after Gravity ("Gravity intensified!"), Grav Apple (135) does about two thirds more than Seed Bomb, until Gravity ends five turns later. Before the fix the two stayed the same |
| 42 | Foul Play, Crunch, Swords Dance, Recover | the Foul Play fix; starts a battle with a wild Shuckle that knows only Swords Dance. Foul Play takes Shuckle's Attack, which is tiny, so it does well under half what Crunch does; Mew's own Swords Dance raises Crunch and leaves Foul Play alone, and each of Shuckle's Swords Dances raises Foul Play. Before the fix Foul Play did a little more than Crunch and rose with Mew's Swords Dance |
| 43 | Body Press, Brick Break, Iron Defense, Swords Dance | the Body Press fix; starts a battle with a wild Shuckle that knows only Splash. Body Press (80) and Brick Break (75) start close; one Iron Defense doubles Body Press and leaves Brick Break alone, and Swords Dance does the opposite. Before the fix Body Press followed Swords Dance and ignored Iron Defense |
| 44 | Psyshock, Psychic, Recover, Splash | the Psyshock fix, which Psystrike and Secret Sword share; starts a battle with a wild Chansey that knows only Calm Mind. Psyshock hits Chansey's tiny Defense and takes most of its HP, where Psychic takes a small share; after a few Calm Minds Psychic does very little and Psyshock is unchanged. Before the fix Psyshock did a little less than Psychic and fell with it |
| 45 | Sacred Sword, Brick Break, Darkest Lariat, Crunch | the Sacred Sword and Darkest Lariat fixes, which Chip Away shares; starts a battle with a wild Skarmory that knows only Iron Defense and Double Team. Use Sacred Sword and Darkest Lariat on the first turn to see their damage, then Brick Break and Crunch once Skarmory has used both a few times: those two do much less and sometimes miss, while Sacred Sword and Darkest Lariat do what they did at first and never miss. Dark is not very effective on Steel here, so the Dark moves do about half. Before the fix Sacred Sword and Darkest Lariat fell and missed with the others |
| 46 | Freeze-Dry, Ice Beam, Flying Press, Close Combat | the Freeze-Dry and Flying Press fixes; starts a battle with a wild Poliwrath (Water and Fighting) that knows only Splash. Freeze-Dry says "It's super effective!" and does about three times what Ice Beam does, which says "It's not very effective..."; Flying Press says "It's super effective!", from its Flying half, and Close Combat says neither. Before the fixes Freeze-Dry was not very effective and Flying Press neutral |
| 47 | Flying Press, Close Combat, Recover, Splash | the Flying Press fix; starts a battle with a wild Probopass (Rock and Steel) that knows only Splash. Close Combat says "It's super effective!" and does about five times what Flying Press does, which says nothing: its Fighting half doubles twice and its Flying half halves twice. Before the fix Flying Press was super effective too |
| 48 | Rage Fist, Substitute, Recover, Splash | the Rage Fist rule (Ian, 2026-09-26); starts a battle with a wild Registeel that knows only Double Kick, which hits Mew twice a turn ("Hit 2 time(s)!"). Ghost is not very effective on Steel here, so every hit is small, but the steps show: Rage Fist used turn after turn does 50 power on the first turn, before Mew has been hit, then 150, 250 and 350, where it stops growing. Hits on Mew's Substitute add nothing, and switching Mew out and back keeps the count, though kicks the other Pokemon takes do not count for Mew. Before the fix it was always 100 |
| 49 | Transform, Recover, Splash, Tackle | the Transform fix (the open bug of 2026-09-26); starts a battle with a wild Rattata given Toxic Debris, ability 295, that knows only Tackle. Once Mew has used Transform, the next Tackle it takes brings "Poison spikes were scattered all around the enemy team's feet!", and a second one another layer. Before the fix a transformed Mew got Inner Focus (39, the low byte of 295) and no spikes came |
| 50 | Wonder Room, Tackle, Swift, Splash | Wonder Room (2026-09-27); starts a battle with a wild Cloyster (high Defense, low Sp. Def) that knows only Recover, so it outlasts the room. Swift does several times what Tackle does; after "It created a bizarre area in which the Defense and Sp. Def stats are swapped!" Tackle does several times what Swift does. Five turns later "Wonder Room wore off, and the Defense and Sp. Def stats returned to normal!" and they trade back, as they do at once if Mew uses Wonder Room again while it is up. Before this the move did nothing |
| 51 | Shore Up, Sandstorm, Sunny Day, Rain Dance | the Shore Up fix; starts a battle with a wild Chansey that knows only Seismic Toss, which takes a fixed 50 HP a turn. Set a weather, use the same move again (it fails) to lose another 50, then use Shore Up and read the HP it gives back: half Mew's maximum in sun or rain, two thirds in a sandstorm (a Lv. 50 Mew has about 170 HP, so about 85 against about 113). Before the fix it healed as Synthesis does, two thirds in sun and a quarter in rain or sand |
| 52 | Meteor Beam, Power Gem, Recover, Splash | the Meteor Beam fix; starts a battle with a wild Chansey that knows only Splash, and puts a Power Herb in the bag. Meteor Beam's first turn prints "MEW is overflowing with space power!" and "MEW's Sp. Atk rose!" and does no damage; the next turn it hits, harder than Power Gem. Given the Power Herb, Mew charges, raises Sp. Atk, prints "became fully charged due to its Power Herb!" and hits in the same turn, and the herb is gone. Before the fix it hit at once with no charge and no raise |
| 53 | Electro Shot, Rain Dance, Thunderbolt, Recover | the Electro Shot fix; starts a battle with a wild Chansey that knows only Splash. Out of rain, Electro Shot's first turn prints "MEW absorbed electricity!" and "MEW's Sp. Atk rose!" and does no damage, and the next turn it hits. After Rain Dance it prints both lines and hits in the same turn, and a Sp. Atk already raised makes it hit harder each time. Rain that starts while Mew is charging does not raise Sp. Atk a second time. The Power Herb from set 52 skips the wait out of rain too. Before the fix it hit at once with no charge and no raise |
| 54 | Mind Blown, Flamethrower, Recover, Splash | Mind Blown's cost (2026-09-27); starts a battle with a wild Chansey that knows Protect and Splash. Each Mind Blown takes half of Mew's HP with "MEW is hit with recoil!" once the attack is over, also when Chansey protects itself; Flamethrower costs nothing. Before this Mind Blown cost nothing |
| 55 | Mind Blown, Flamethrower, Recover, Splash | Damp and Mind Blown; starts a battle with a wild Politoed given Damp that knows only Splash. Mind Blown fails with "POLITOED's Damp prevents MEW from using Mind Blown!" and Mew keeps its HP |
| 56 | Nature's Madness, Splash, Recover, Tackle | Nature's Madness's power (2026-09-27); starts a battle with a wild Chansey that knows only Taunt. Once Mew is taunted, Splash and Recover cannot be chosen, and Nature's Madness still can and halves Chansey's HP each time. Before the fix Taunt blocked Nature's Madness too, since its power of 0 marked it as a status move |
| 57 | Scale Shot, Double Hit, Recover, Splash | Scale Shot's stat changes (2026-09-27); starts a battle with a wild Shuckle that knows only Splash. After "Hit 2 time(s)!" (or up to 5), "MEW's Defense fell!" and "MEW's Speed rose!", once a use whatever the number of hits; Double Hit changes nothing. At -6 Defense only the Speed rises. Before this Scale Shot changed no stat |
| 58 | Spiky Shield, Recover, Splash, Tackle | Spiky Shield's spikes (2026-09-27); starts a battle with a wild Rattata that knows Tackle and Swift. When a Tackle meets the shield, "MEW protected itself!" and then "The wild RATTATA was hurt!", and it loses an eighth of its HP; a Swift, which makes no contact, brings only the first message. Before this it was a plain Protect. It never fails when used turn after turn, the open bug of 2026-09-26 |
| 59 | Baneful Bunker, Recover, Splash, Tackle | Baneful Bunker's poison (2026-09-27); starts a battle with a wild Rattata that knows Tackle and Swift. When a Tackle meets the bunker, "MEW protected itself!" and then "The wild RATTATA was poisoned!"; once it is poisoned, later Tackles bring only the first message, as does a Swift, which makes no contact. Before this it was a plain Protect. It never fails when used turn after turn, the open bug of 2026-09-26 |
| 60 | Salt Cure, Soak, Recover, Splash | Salt Cure (2026-09-27); starts a battle with a wild Chansey that knows only Splash. The first Salt Cure brings "The wild CHANSEY is being salt cured!", and from then "The wild CHANSEY is hurt by Salt Cure!" at the end of every turn, an eighth of its HP each time; a second Salt Cure brings no new message. After Soak makes Chansey a Water type, each loss is a quarter. Before this Salt Cure was a plain hit |
| 61 | Octolock, Tackle, Swift, Recover | Octolock (2026-09-27); starts a battle with a wild Chansey that knows only Splash. Octolock brings "The wild CHANSEY can no longer escape because of Octolock!", then at the end of every turn "The wild CHANSEY's Defense fell!" and "The wild CHANSEY's Sp. Def fell!", so Tackle and Swift do more each turn; at -6 each says it won't go any lower. A second Octolock fails. The trap itself shows only on the player's side, which a wild foe cannot do to Mew. Before this it did nothing |
| 62 | Magic Room, Substitute, Splash, Tackle, on a Mew holding Leftovers | Magic Room (2026-09-27); starts a battle with a wild Chansey that knows only Splash. After a Substitute, Leftovers restores a little HP at the end of each turn; after "It created a bizarre area in which Pokémon's held items lose their effects!" it does not, until "Magic Room wore off, and held items' effects returned to normal!" five turns later, or at once if Mew uses Magic Room again. Before this the move did nothing |
| 63 | Teatime, Splash, Recover, Tackle, on a Mew holding a Liechi Berry | Teatime (2026-09-27); starts a battle with a wild Chansey that knows only Splash. At full HP, Teatime brings "It's teatime! Everyone dug in to their Berries!" and then the Liechi Berry raising Mew's Attack, which it would not do by itself above a quarter of Mew's HP. A second Teatime says "But it failed!", since no Berry is left. Every Berry on the field, the foe's included, needs a double battle or a trainer to show. Before this the move did nothing |
| 64 | Core Enforcer, Thunderbolt, Recover, Splash | Core Enforcer (2026-09-27); starts a battle with a wild Jolteon given Volt Absorb that knows only Splash, faster than Mew. Thunderbolt does nothing to it, since Volt Absorb takes it; after a Core Enforcer, "The wild JOLTEON's ability was suppressed!", and from then Thunderbolt hurts it. A target that has not moved yet this turn keeps its ability, which needs a foe slower than Mew to see. Before this Core Enforcer was a plain hit |
| 65 | Beak Blast, Recover, Splash, Tackle | Beak Blast's heat (2026-09-27); starts a battle with a wild Rattata that knows Tackle and Swift. On a turn Mew chooses Beak Blast, "MEW started heating up its beak!" comes before anyone moves, and a Tackle into Mew brings "The wild RATTATA was burned!" before Beak Blast strikes (it moves last). A Swift makes no contact and burns nothing, and neither does a Tackle on a turn Mew chooses something else. Before this Beak Blast was a plain hit |
| 66 | Sky Drop, Recover, Splash, Protect | Sky Drop (2026-09-27); starts a battle with a wild Chansey that knows only Tackle, slower than Mew. The first turn brings "MEW took the wild CHANSEY into the sky!", both vanish, and Chansey does not tackle that turn; the next turn the drop hits before Chansey can move, both reappear, and Chansey tackles later that same turn. A target of 200 kg or more (Snorlax) makes it fail, as does Gravity. Before this Sky Drop was a plain hit |
| 67 | Sky Drop, Recover, Splash, Protect | Sky Drop against a Flying type; starts a battle with a wild Skarmory that knows only Splash. Skarmory is lifted ("MEW took the wild SKARMORY into the sky!"), and on the second turn, once both have landed, "It doesn't affect the wild SKARMORY..." |

**When a batch of effect scripts lands, add its sets in the same commit**: a
`TestKit_MoveSetN` block, an `AddListMenuEntry` line in `TestKit_MoveSets2`, and
a `TestKit_Text_MenuSetN` message in `res/testkit/twinleaf_town_player_house_2f.json`.
Sets 1 to 27 fill the first page, whose last entry, "More sets", opens the
second: a field menu holds 28 entries (`FIELD_MENU_ENTRIES_MAX`), and a
29th is written past the end of the menu's arrays. Sets 28 to 31 were
added that way on 2026-09-25 and moved to the second page on 2026-09-26.
The second page ends the same way at set 54, and set 55 on (2026-09-27) is
on the third, `TestKit_MoveSets3`.
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
`TestKit_Abilities2` (the field menu holds 28 entries, so the first page is
full) and a `TestKit_Text_MenuAbility<Name>` message.

An entry for an ability that works when its holder is hit also names a foe,
in `VAR_0x8000` (species), `VAR_0x8001` (its ability, `ABILITY_NONE` to keep
the rolled one) and `VAR_0x8002` (one move, which it then uses every turn, or
`MOVE_NONE` to keep its own), and, for a foe that should show a contrast,
`VAR_0x8003` (a second move). The kit fights it straight after the gift, a
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
| Competitive | Gothitelle: Psychic, Calm Mind, Thunderbolt, Thunder Wave; foe a wild Chansey that knows only Growl | After "GOTHITELLE's Attack fell!", "GOTHITELLE's Competitive sharply raised its Sp. Atk!" every time | 6c408f31 |
| Defiant | Galarian Zapdos: Thunderous Kick, Brave Bird, Bulk Up, Close Combat; foe a wild Chansey that knows only Tail Whip | After its Defense falls, "ZAPDOS's Defiant sharply raised its Attack!"; its own Close Combat lowering its stats does not set it off | 6c408f31 |
| Big Pecks | Mandibuzz: Foul Play, Roost, Toxic, Brave Bird; foe a wild Chansey that knows only Tail Whip | "MANDIBUZZ's Big Pecks prevents Defense loss!" every time | 6c408f31 |
| Flower Veil | Tsareena, given Flower Veil because none of its carriers is Grass: Trop Kick, Power Whip, Knock Off, Trailblaze; foe a wild Chansey that knows only Growl | "TSAREENA surrounded itself with a veil of petals!" and its Attack stays. A Florges's Flower Veil guarding a Grass-type partner needs a double battle | 6c408f31 |
| Contrary | Serperior: Leaf Storm, Giga Drain, Coil, Glare; any foe | Leaf Storm: "SERPERIOR's Sp. Atk sharply rose!"; Coil: its Attack, Defense and accuracy each fall | 6c408f31 |
| Mirror Armor | Corviknight: Iron Defense, Body Press, Roost, Iron Head; foe a wild Chansey that knows only Growl | Each Growl lowers the wild Chansey's own Attack, and Corviknight's stays | 6c408f31 |
| Prankster | Klefki: Thunder Wave, Spikes, Swagger, Foul Play; foe a wild Weavile, faster than Klefki and a Dark type | Klefki's status moves go before Weavile. Thunder Wave and Swagger print "It doesn't affect the wild WEAVILE..."; Spikes, aimed at its side, still works; Foul Play is not raised and goes second | ab20c71e |
| Gale Wings | Talonflame: Brave Bird, Flare Blitz, Roost, Swords Dance; foe a wild Jolteon, faster than Talonflame | At full HP Brave Bird goes before Jolteon; after Brave Bird's recoil, or any damage, it goes second, and Flare Blitz always does | ab20c71e |
| Queenly Majesty | Tsareena: Trop Kick, Power Whip, Knock Off, Trailblaze; foe a wild Rattata that knows only Quick Attack | "TSAREENA's Queenly Majesty prevents the wild RATTATA from using Quick Attack!" every time | ab20c71e |
| Iron Barbs | Ferrothorn: Iron Defense, Leech Seed, Gyro Ball, Spikes; foe a wild Rattata that knows only Tackle | After each Tackle, "FERROTHORN's Iron Barbs hurt the wild RATTATA!" and Rattata loses an eighth of its HP | 2eb320f4 |
| Weak Armor | Crustle: Shell Smash, Rock Slide, X-Scissor, Stealth Rock; foe a wild Rattata that knows only Tackle | After each Tackle, "CRUSTLE's Weak Armor lowered its Defense!" then "CRUSTLE's Weak Armor sharply raised its Speed!"; at -6 Defense only the Speed message shows | 2eb320f4 |
| Cursed Body | Jellicent: Scald, Recover, Will-O-Wisp, Shadow Ball; foe a wild Rattata that knows only Tackle | About one Tackle in three is followed by "The wild RATTATA's Tackle was disabled!", and Rattata struggles for the next three turns | 2eb320f4 |
| Water Compaction | Palossand: Shore Up, Shadow Ball, Earth Power, Iron Defense; foe a wild Psyduck that knows only Water Gun | After each Water Gun, "PALOSSAND's Water Compaction sharply raised its Defense!" | 2eb320f4 |
| Toxic Debris | Glimmora: Power Gem, Sludge Wave, Mortal Spin, Earth Power; foe a wild Rattata that knows only Tackle | After each of the first two Tackles, "Poison spikes were scattered all around the enemy team's feet!"; the third brings no message, since two layers is the most | 2eb320f4 |
| Berserk | Galarian Moltres: Fiery Wrath, Nasty Plot, Air Slash, Roost; foe a wild Rhydon that knows only Rock Slide | On the Rock Slide that takes Moltres from above half its HP to half or less, "MOLTRES's Berserk raised its Sp. Atk!"; a later hit below half brings nothing until Roost takes it back above | 2eb320f4 |
| Gooey | Goodra: Dragon Pulse, Sludge Bomb, Thunderbolt, Rest; foe a wild Rattata that knows only Tackle | After each Tackle, "GOODRA's Gooey cuts the wild RATTATA's Speed!" | 2eb320f4 |
| Mummy | Cofagrigus: Shadow Ball, Will-O-Wisp, Protect, Nasty Plot; foe a wild Rattata that knows only Tackle | After the first Tackle, "The wild RATTATA acquired Mummy!"; nothing after later ones | 711bb8df |
| Wandering Spirit | Runerigus: Earthquake, Shadow Claw, Protect, Stealth Rock; foe a wild Rattata with Guts that knows only Tackle | After the first Tackle, "RUNERIGUS swapped abilities with its target!": Runerigus now has Guts and Rattata Wandering Spirit, so later Tackles bring nothing | 711bb8df |
| Entrainment | Leavanny with Swarm: Entrainment, Skill Swap, Role Play, Worry Seed; foe a wild Rattata with Guts that knows only Tackle | Entrainment: "The wild RATTATA acquired Swarm!"; used again, it fails, since both now have Swarm. Skill Swap, Role Play and Worry Seed work as before | 711bb8df |
| Ability list | Leavanny with Swarm: Entrainment, Skill Swap, Role Play, Gastro Acid; foe a wild Rattata given Disguise that knows only Tackle | All four moves fail ("But it failed!"), since Disguise is on the list of abilities that cannot be passed, copied, swapped or suppressed. Before this batch Skill Swap, Role Play and Gastro Acid worked on it | 711bb8df |
| Fluffy (second page, as are all below) | Dubwool: Cotton Guard, Body Press, Wild Charge, Swords Dance; foe a wild Eevee that knows Tackle and Ember | Ember hits around twice as hard as Tackle; without Fluffy it would hit about half as hard | 6510658b |
| Ice Scales | Frosmoth: Quiver Dance, Ice Beam, Bug Buzz, Giga Drain; foe a wild Porygon that knows Tackle and Swift | Swift does less than Tackle; without Ice Scales it would do more | 6510658b |
| Water Bubble | Araquanid: Liquidation, Leech Life, Protect, Mirror Coat; foe a wild Gengar that knows only Will-O-Wisp | "ARAQUANID's Water Bubble prevents burns!" every time | 6510658b |
| Merciless | Toxapex: Toxic, Scald, Recover, Protect; foe a wild Rattata that knows only Growl | Once Toxic has poisoned Rattata, every Scald is "A critical hit!" | 6510658b |
| Long Reach | Decidueye: Leaf Blade, Shadow Sneak, Swords Dance, Roost; foe a wild Ferrothorn with Iron Barbs that knows only Iron Defense | Leaf Blade brings no Iron Barbs message and costs Decidueye nothing | 6510658b |
| Pixilate | Sylveon: Hyper Voice, Quick Attack, Calm Mind, Wish; foe a wild Misdreavus, a Ghost type, that knows only Growl | Hyper Voice and Quick Attack hit Misdreavus, where a Normal move would bring "It doesn't affect..." | 9b681d08 |
| Liquid Voice | Primarina: Hyper Voice, Moonblast, Calm Mind, Sparkling Aria; foe a wild Vaporeon with Water Absorb that knows only Growl | Hyper Voice does no damage: Vaporeon's Water Absorb takes it, as it takes Sparkling Aria | 9b681d08 |
| Sheer Force | Toucannon: Flame Charge, Brave Bird, Bullet Seed, Roost; foe a wild Chansey that knows only Growl | Flame Charge never brings "TOUCANNON's Speed rose!"; Brave Bird's recoil, not a secondary effect, stays | 9b681d08 |
| Auras | Xerneas with Fairy Aura: Moonblast, Geomancy, Psyshock, Focus Blast; foe a wild Yveltal with Dark Aura that knows only Dark Pulse | "The wild YVELTAL is radiating a dark aura!" as the battle starts, and "XERNEAS is radiating a fairy aura!" when Xerneas comes in | 71bfc90f |
| Aura Break | Zygarde (50% Forme) with Aura Break: Thousand Arrows, Dragon Dance, Coil, Rest; foe a wild Yveltal with Dark Aura that knows only Dark Pulse | "ZYGARDE reversed all other Pokémon's auras!" when Zygarde comes in; from then on Dark Aura weakens Dark moves by a quarter in place of raising them, which has no message | 71bfc90f |
| Unnerve | Galvantula: Thunder, Bug Buzz, Energy Ball, Sticky Web; foe a wild Rattata that knows only Growl | "The foe's team is too nervous to eat Berries!" when Galvantula comes in. The wild foe holds no Berry, so the Berry block itself does not show here | 71bfc90f |
| Screen Cleaner | Mr. Rime: Freeze-Dry, Psychic, Rapid Spin, Slack Off; foe a wild Chansey that knows Reflect and Light Screen | Once Chansey has a screen up, switch Mr. Rime in: "All screens on the field were cleansed!", and Freeze-Dry's damage goes back up | 71bfc90f |
| Regenerator | Toxapex: Scald, Toxic, Haze, Recover; foe a wild Rattata that knows only Tackle | Let Tackle hurt Toxapex, switch it out, and bring it back: it has a third of its HP back, with no message | 71bfc90f |
| Pastel Veil | Galarian Rapidash: Play Rough, High Horsepower, Morning Sun, Quick Attack; foe a wild Grimer that knows only Toxic | "RAPIDASH's Pastel Veil prevents poisoning!" every time | a51b0af3 |
| Sweet Veil | Tsareena with Sweet Veil: Trop Kick, Power Whip, Triple Axel, Quick Attack; foe a wild Jigglypuff that knows only Sing | "TSAREENA stayed awake because of its Sweet Veil!" whenever Sing hits | a51b0af3 |
| Harvest | Arboliva holding a Sitrus Berry: Substitute, Hyper Voice, Leech Seed, Protect; foe a wild Rattata that knows only Growl | Use Substitute twice: below half HP Arboliva eats the Sitrus Berry, and at the end of later turns, about one in two, "ARBOLIVA harvested one Sitrus Berry!" (every turn in sunshine) | a51b0af3 |
| Protean | Greninja: Surf, Dark Pulse, Ice Beam, U-turn; foe a wild Rattata that knows only Growl | The first move brings "GRENINJA's Protean made it the Water type!" (or the move's type); later moves bring nothing until Greninja switches out and back in | a51b0af3 |
| Libero | Cinderace: Pyro Ball, Court Change, Sucker Punch, U-turn; foe a wild Rattata that knows only Growl | As Protean, for Cinderace | a51b0af3 |
| Infiltrator | Chandelure: Shadow Ball, Flamethrower, Fake Tears, Energy Ball; foe a wild Chansey that knows only Mist | After Chansey's Mist, Fake Tears still brings "The wild CHANSEY's Sp. Def harshly fell!" and not "is protected by Mist!" | a51b0af3 |
| Neutralizing Gas | Galarian Weezing: Sludge Bomb, Strange Steam, Will-O-Wisp, Protect; foe a wild Chansey given Pressure that knows only Growl | "The wild CHANSEY is exerting its Pressure!" as the battle starts. Switch Weezing in: "Neutralizing gas filled the area!", and each of its moves aimed at Chansey now costs 1 PP, not 2. Switch Weezing out: after "Go!", "The effects of the neutralizing gas wore off!", then Chansey's Pressure message again, and moves cost 2 PP once more | 0eb1b2e9 |

## The hidden-ability entries

The seventeen abilities the natives carry as hidden abilities, which element 5
left for a follow-up (`cloud/element5-hidden-abilities`), are on a third page
of the Abilities menu, reached from "More abilities" at the end of the second.
They are built as the entries above are. Where an ability changes the damage
a foe does, the foe carries it and the new Pokemon is a Snorlax or another
Pokemon with its own ability, so the HP it loses can be read off its own
health box. As before, switch the new Pokemon in on the first turn.

| Entry | Pokemon and moves | What to look for | Commit |
|---|---|---|---|
| Analytic | Snorlax: Quick Attack, Splash, Rest, Protect; foe a wild Magnezone given Analytic that knows only Thunderbolt | Magnezone is always faster, so Thunderbolt does about a third more on the turns Snorlax uses Quick Attack (Magnezone moves last) than on the turns it uses Splash | 8cc670a3 |
| Flare Boost | Snorlax: Will-O-Wisp, Splash, Rest, Protect; foe a wild Drifblim given Flare Boost that knows only Swift | Once Will-O-Wisp burns Drifblim, Swift takes about half again as much of Snorlax's HP | 8f4316b4 |
| Heavy Metal | Machamp: Karate Chop, Splash, Rest, Protect; foe a wild Aggron given Heavy Metal that knows Heavy Slam and Iron Head | Heavy Slam does about half again what Iron Head does (power 120 against 80); without Heavy Metal it would be 60 | 1e08badc |
| Justified | Lucario: Aura Sphere, Splash, Calm Mind, Flash Cannon; foe a wild Poochyena that knows only Bite | Each Bite brings "LUCARIO's Justified raised its Attack!"; nothing at +6 | 82f44582 |
| Light Metal | Garchomp: Dragon Claw, Splash, Rest, Protect; foe a wild Metagross given Light Metal that knows Heavy Slam and Iron Head | Heavy Slam does less than Iron Head (power 60 against 80); without Light Metal it would be 120 | 734e4583 |
| Magic Bounce | Espeon: Psychic, Calm Mind, Morning Sun, Protect; foe a wild Chansey that knows only Toxic | Each Toxic brings "ESPEON bounced the Toxic back!", and Chansey is badly poisoned | a766752f |
| Moody | Bibarel: Splash, Protect, Rest, Waterfall; foe a wild Chansey that knows only Splash | At the end of each turn, "BIBAREL's Moody sharply raised its {stat}!" and "BIBAREL's Moody lowered its {another stat}!"; never accuracy or evasion | 3eebbfc9 |
| Moxie | Honchkrow: Night Slash, Brave Bird, Sucker Punch, Roost; any wild Pokemon | Knock it out: straight after "fainted!", "HONCHKROW's Moxie raised its Attack!" | 9763435f |
| Multiscale | Dragonite: Roost, Dragon Dance, Extreme Speed, Protect; foe a wild Graveler that knows only Rock Throw | The first Rock Throw, at full HP, takes about half what the next does; Roost back to full and the next is halved again | fc8e6233 |
| Pickpocket | Snorlax holding Leftovers: Tackle, Splash, Rest, Protect; foe a wild Sneasel given Pickpocket that knows only Splash | The first Tackle brings "The wild SNEASEL stole SNORLAX's Leftovers!"; after the battle Snorlax holds its Leftovers again | 025b933c |
| Poison Touch | Toxicroak: Drain Punch, Sucker Punch, Vacuum Wave, Protect; foe a wild Chansey that knows only Tackle | About one Drain Punch or Sucker Punch in three poisons Chansey, with a message naming Poison Touch; Vacuum Wave, which makes no contact, never does | 37392948 |
| Rattled | Dunsparce: Splash, Roost, Body Slam, Protect; foe a wild Poochyena that knows only Bite | Each Bite brings "DUNSPARCE's Rattled raised its Speed!" | 5164626f |
| Sand Force | Shellos, a Water type: Sandstorm, Earth Power, Recover, Protect; foe a wild Chansey that knows only Splash | With Sandstorm up, Chansey is buffeted at the end of each turn and Shellos is not. The power rise has no message | a7048f51 |
| Sand Rush | Sandslash: Sandstorm, Splash, Earthquake, Protect; foe a wild Charizard that knows only Growl | Charizard moves first until Sandstorm is up, and Sandslash first while it lasts (only a rare pairing of natures and IVs keeps Charizard ahead) | 336364da |
| Toxic Boost | Snorlax: Toxic, Splash, Rest, Protect; foe a wild Zangoose given Toxic Boost that knows only Mega Punch | Once Toxic poisons Zangoose, Mega Punch takes about half again as much of Snorlax's HP | d2359a88 |
| Wonder Skin | Delcatty: Splash, Body Slam, Rest, Protect; foe a wild Chansey that knows only Growl | Once Delcatty is in, about one Growl in two misses | 9b00e08f |

Friend Guard has no entry, since it works only in a double battle. Rattled's
answer to Intimidate has none either: it needs the Intimidate holder to come
in against the Rattled Pokemon, which a wild battle cannot arrange.

## The modern rules entries

The staples survey's engine rulings (Ian, 2026-09-26) have their own menu,
"Modern rules", built as the ability entries are: a `TestKit_Staple<Name>`
block in the kit script, an `AddListMenuEntry` line in `TestKit_Staples` and a
`TestKit_Text_MenuStaple<Name>` message. As with the ability entries, the new
Pokemon is not in the lead, so switch it in on the first turn.

| Entry | Pokemon and moves | What to look for | Commit |
|---|---|---|---|
| Sturdy | Geodude with Sturdy: Rest, Rock Slide, Defense Curl, Magnitude; foe a wild Vaporeon that knows only Surf | Switched in, Geodude takes the Surf at full HP and is left at 1 HP with "GEODUDE endured the hit!"; the next Surf knocks it out unless Rest has put it back at full HP first | d65b4e83 |
| Lightning Rod | Raichu with Lightning Rod: Thunderbolt, Nasty Plot, Surf, Focus Blast; foe a wild Jolteon that knows only Thunderbolt | Once Raichu is in, each Thunderbolt does nothing: "RAICHU's Lightning Rod raised its Sp. Atk!", and at +6 "made Thunderbolt useless!" | 7df8a7fd |
| Storm Drain | Gastrodon with Storm Drain: Earth Power, Ice Beam, Recover, Toxic; foe a wild Vaporeon that knows only Surf | As Lightning Rod, for Surf: "GASTRODON's Storm Drain raised its Sp. Atk!" | 7df8a7fd |
| Intimidate blocked | Staraptor with Intimidate: Brave Bird, Close Combat, Roost, U-turn; foe a wild Lucario given Inner Focus that knows only Splash | When Staraptor comes in, "The wild LUCARIO's Inner Focus suppressed STARAPTOR's Intimidate!" and Lucario's Attack stays. Own Tempo, Oblivious and Scrappy do the same | ebfc976f |
| Oblivious and Taunt | Weavile: Taunt, Night Slash, Ice Shard, Swords Dance; foe a wild Slowbro given Oblivious that knows only Growl | Taunt: "The wild SLOWBRO's Oblivious made Taunt ineffective!", and Slowbro goes on using Growl | b325871c |
| Keen Eye, Illuminate | Starmie with Illuminate: Surf, Thunderbolt, Ice Beam, Recover; foe a wild Chansey that knows Double Team and Sand Attack | Sand Attack: "STARMIE's Illuminate prevents accuracy loss!". However many Double Teams Chansey stacks, Starmie's Surf never misses. Keen Eye does both the same way | 5e5014c6 |
| Synchronize | Espeon with Synchronize: Psychic, Calm Mind, Morning Sun, Protect; foe a wild Chansey that knows only Toxic | Once Toxic lands on Espeon, "ESPEON's Synchronize poisoned the wild CHANSEY!", and from then Chansey loses more HP to poison each turn, as Espeon does: bad poison, where Platinum passed on plain poison | 41dd402c |
| Leaf Guard and Rest | Leafeon with Leaf Guard: Sunny Day, Rest, Leaf Blade, Swords Dance; foe a wild Rattata that knows only Tackle | Let Tackle hurt Leafeon, then Rest: it sleeps and heals. Wake it, take another Tackle, use Sunny Day, then Rest: "LEAFEON stayed awake because of its Leaf Guard!" | d89092a0 |
| Stench | Skuntank with Stench: Fury Swipes, Scratch, Protect, Night Slash; foe a wild Snorlax that knows only Splash | Skuntank is faster: about one Scratch in ten makes Snorlax flinch ("The wild SNORLAX flinched!"), and Fury Swipes rolls for each hit | 3c54ea0d |
| Water Absorb and Soak | Lapras: Soak, Thunderbolt, Ice Beam, Sing; foe a wild Vaporeon given Water Absorb that knows only Growl | Soak does not take: Water Absorb takes it, restoring HP if Vaporeon has lost any, or with "made Soak useless!" at full HP. Dry Skin does the same | c4f682b9 |
| Magic Guard, paralysis | Clefable with Magic Guard: Moonblast, Calm Mind, Soft-Boiled, Flamethrower; foe a wild Jolteon that knows only Thunder Wave | Once paralysed, Clefable is sometimes "fully paralyzed!" (about one turn in four), where before Magic Guard kept it moving | 2f32c59e |
| Liquid Ooze, Dream Eater | Gengar: Hypnosis, Dream Eater, Shadow Ball, Giga Drain; foe a wild Tentacruel given Liquid Ooze that knows only Splash | Once Hypnosis lands, Dream Eater hurts Gengar with "It sucked up the liquid ooze!", as Giga Drain does, where before it healed Gengar | 666758f7 |
| Simple | Bibarel with Simple: Defense Curl, Swords Dance, Return, Waterfall; foe a wild Chansey that knows only Growl | Defense Curl: "BIBAREL's Defense sharply rose!" (two stages); Swords Dance: "rose drastically!" (four); Growl: "BIBAREL's Attack harshly fell!" (two). Two Swords Dances reach +6 | d683c10e |
| Grass and powder | Venusaur: Giga Drain, Sludge Bomb, Body Slam, Synthesis; foe a wild Parasect given Effect Spore that knows Spore and Stun Spore | Spore and Stun Spore: "It doesn't affect VENUSAUR..."; and Body Slam, a contact move, never sets off Effect Spore | 19e9741f |
| Electric and paralysis | Luxray: Spark, Crunch, Roar, Charge; foe a wild Arbok that knows Glare and Thunder Wave | Glare and Thunder Wave: "It doesn't affect LUXRAY...", and Luxray is never paralysed. Luxray's Spark can still paralyse Arbok | e6641e1f |
| Ghosts and trapping | Mismagius: Shadow Ball, Mystical Fire, Protect, Teleport; foe a wild Umbreon that knows Mean Look and Fire Spin | Switch Mismagius in on the first turn. Mean Look: "It doesn't affect MISMAGIUS..."; Fire Spin still hurts it each turn, but Mismagius can switch out, Run gets away and Teleport works | 42fd4ae3 |
| Critical hits | Mew: Focus Energy, Slash, Tackle, Recover; foe a wild Snorlax that knows only Splash | Before Focus Energy, Slash is a critical hit about one time in eight and Tackle about one in 24. After it, every Slash is "A critical hit!" (three stages), and Tackle one time in two. A critical Slash does about half as much again as a normal one, not double | dc60da30 |
| Defog, both sides | Mew: Defog, Stealth Rock, Reflect, Recover; foe a wild Skarmory that knows Spikes and Toxic Spikes | Let Skarmory lay Spikes and Toxic Spikes on your side, and lay Stealth Rock on its side and Reflect on yours. Defog blows away Stealth Rock, Spikes and Toxic Spikes, each named once, and your Reflect stays: Defog clears screens only on the target's side. It still clears fog | 72252c48 |
| Rapid Spin | Starmie: Rapid Spin, Surf, Thunderbolt, Recover; foe a wild Skarmory that knows only Spikes | Each Rapid Spin ends with "STARMIE's Speed rose!", after "STARMIE blew away Spikes!" when Skarmory has laid some; at +6 it says nothing more | 349e0f45 |
| Protect in a row | Mew: King's Shield, Spiky Shield, Protect, Recover; foe a wild Rattata that knows only Tackle | Use King's Shield every turn: the first always works, the second about one time in two, the third about one in four, each failure "But it failed!". Spiky Shield the same, and mixing them with Protect keeps the run going. Before the fix both worked every turn | a11da24d |
| Hidden ability gift | Litten, Lv. 15, given with `FLAG_NEXT_MON_HIDDEN_ABILITY` set (element 8) | Its summary reads Intimidate, its hidden ability, where both ordinary slots are Blaze. One Rare Candy evolves it into a Torracat that still reads Intimidate | element 8, hidden abilities |
| Hidden ability wild | a wild Litten, Lv. 15, fought with the flag set | "The wild LITTEN's Intimidate cuts ...'s Attack!" as the battle starts. The flag clears itself, so the next scripted wild Pokemon rolls as usual | element 8, hidden abilities |
| Items restored | Mew holding a Sitrus Berry: Belly Drum, Tackle, Recover, Splash; foe a wild Chansey that knows only Splash | Belly Drum halves Mew's HP and it eats the Sitrus Berry. After the battle, won or run from, Mew's summary shows the Sitrus Berry again | element 8, held items restored |
| Kaizo move data | Mew: Extreme Speed, Minimize, Protect, Recover; foe a wild Shuckle that knows only Fake Out | Switch Mew in on the first turn. From then Shuckle's Fake Out ("But it failed!") comes before Mew's Extreme Speed every turn, though Mew is far faster: Fake Out is +3 and Extreme Speed +2 (Ian, 2026-09-27), where both were +1 and Mew went first. Minimize: "MEW's evasiveness sharply rose!", two stages where it was one | cloud/element4-kaizo-move-data |

## The item entries

Element 7's items have their own menu, "Element 7 items". Its first entry,
"All new items", puts one of each of the 46 in the Bag, for their names,
icons, pockets and descriptions. The Items, Medicine and Berries pockets
were widened to hold one of every item of their kind, so all 46 arrive
unless those pockets were already holding other items near their size. The
entries after it are built as the ability entries are, from a
`TestKit_Item<Name>` block, but each goes through `TestKit_GiveItemPair`:
two Lv. 50 copies of one Pokemon with the same four moves, the first holding
the item and the second holding nothing, so every effect is seen beside a
baseline. Two free party slots are needed, and neither new Pokemon is in the
lead, so switch the one you want in on the first turn. The kit's Pokemon
have random IVs and natures, so "about" in the table below is loose.

| Entry | Pokemon and moves | What to look for | Commit |
|---|---|---|---|
| Eviolite | Chansey: Splash, Softboiled, Protect, Seismic Toss; foe a wild Machamp that knows only Karate Chop | Each Karate Chop takes about two thirds as much from the Chansey holding the Eviolite as from the other, since Chansey can still evolve | element 7, damage items |
| Assault Vest | Mew: Psychic, Swords Dance, Recover, Tackle; foe a wild Magmortar that knows only Flamethrower | On the Mew wearing it, choosing Swords Dance or Recover brings "The effects of the Assault Vest prevent the use of status moves!" and nothing happens; each Flamethrower takes about two thirds as much from it as from the other Mew | element 7, damage items |
| Punching Glove | Hitmonchan: Ice Punch, Mach Punch, Close Combat, Bulk Up; foe a wild Ferrothorn given Iron Barbs that knows only Iron Defense | The gloved Hitmonchan's Ice Punch and Mach Punch do about a tenth more than the other's and bring no Iron Barbs damage; its Close Combat, a kick, still does, as every contact move from the other Hitmonchan does | element 7, damage items |
| Fairy Feather | Clefable: Moonblast, Dazzling Gleam, Calm Mind, Moonlight; foe a wild Chansey that knows only Splash | Moonblast and Dazzling Gleam from the Clefable holding it do about a fifth more than from the other | element 7, damage items |
| Ring Target | Skarmory: Roost, Spikes, Brave Bird, Protect; foe a wild Dugtrio that knows only Earthquake | The Skarmory holding it takes Earthquake, "It's super effective!" through its Steel type; the other gets "It doesn't affect SKARMORY..." | element 7, protective items |
| Safety Goggles | Snorlax: Sandstorm, Body Slam, Rest, Protect; foe a wild Parasect given Effect Spore that knows Spore and Stun Spore | Against the Snorlax wearing them, Spore and Stun Spore bring "SNORLAX is protected by its Safety Goggles!"; its Body Slam never sets off Effect Spore, and it takes no damage from its own Sandstorm, where the other Snorlax sleeps, is sometimes poisoned or paralysed, and is buffeted | element 7, protective items |
| Covert Cloak | Snorlax: Rest, Body Slam, Protect, Splash; foe a wild Jolteon that knows only Nuzzle | The cloaked Snorlax takes Nuzzle's damage and is never paralysed; the other is paralysed at once | element 7, protective items |
| Clear Amulet | Mew: Swords Dance, Tackle, Recover, Splash; foe a wild Chansey that knows Growl and Sticky Web | Each Growl at the Mew wearing it brings "MEW's Clear Amulet prevents stat loss!"; the other Mew's Attack falls. Its own Swords Dance still works. Once Chansey has laid the web, the Mew wearing it switched in is "caught in a sticky web!" and then the amulet prevents the loss; the other Mew's Speed falls | element 7, protective items; Sticky Web, element 7 follow-up |
| Ability Shield | Bronzong given Levitate: Splash, Iron Defense, Recover, Protect; foe a wild Chansey given Mold Breaker that knows Worry Seed and Earthquake | "The wild CHANSEY has Mold Breaker!" on the way in. Against the Bronzong holding the shield, Worry Seed says "But it failed!" and Earthquake "It doesn't affect BRONZONG...", since Mold Breaker cannot reach past the shield to Levitate; the other Bronzong takes Earthquake, super effective, and Worry Seed gives it Insomnia | element 7, protective items; Mold Breaker, element 7 follow-up |
| Rocky Helmet | Skarmory: Roost, Iron Defense, Protect, Splash; foe a wild Rattata that knows Tackle and Swift | Each Tackle into the helmeted Skarmory brings "The wild RATTATA is hurt by SKARMORY's Rocky Helmet!" and takes a sixth of Rattata's HP, and the helmet stays; Swift, which makes no contact, does not, nor does a Tackle into the other Skarmory | element 7, on-hit items |
| Absorb Bulb | Chansey: Softboiled, Splash, Protect, Seismic Toss; foe a wild Psyduck that knows only Water Gun | The first Water Gun into the Chansey holding it brings "The Absorb Bulb raised CHANSEY's Sp. Atk!", and the bulb is gone from its summary until the battle ends | element 7, on-hit items |
| Cell Battery | Chansey, as above; foe a wild Pikachu that knows only Thunder Shock | As the Absorb Bulb, for Attack | element 7, on-hit items |
| Weakness Policy | Snorlax: Rest, Body Slam, Protect, Splash; foe a wild Machamp that knows only Karate Chop | The first chop into the Snorlax holding it (super effective) brings "The Weakness Policy sharply raised SNORLAX's Attack!" and the same for its Sp. Atk, and the policy is gone | element 7, on-hit items |
| Air Balloon | Snorlax: Rest, Body Slam, Protect, Splash; foe a wild Dugtrio that knows Earthquake and Scratch | Switched in, the Snorlax holding it "floats in the air with its Air Balloon!"; Earthquake: "It doesn't affect SNORLAX..."; the first Scratch brings "SNORLAX's Air Balloon popped!", and from then Earthquake hits. It also misses Spikes and Toxic Spikes on the way in | element 7, on-hit items |
| Binding Band | Mew: Wrap, Splash, Recover, Protect; foe a wild Chansey that knows only Splash | After the banded Mew's Wrap, Chansey loses a sixth of its HP at the end of each turn ("is hurt by Wrap!"); after the other Mew's, an eighth, the later games' rate for every binding move | element 7, Binding Band, Loaded Dice, Mirror Herb; the rates, element 7 follow-up |
| Loaded Dice | Mew: Bullet Seed, Triple Axel, Population Bomb, Recover; foe a wild Chansey that knows only Splash | From the Mew holding them, Bullet Seed always ends "Hit 4 time(s)!" or 5, Population Bomb 4 to 10, and Triple Axel never misses its second or third kick; from the other, Bullet Seed mostly hits 2 or 3 times | element 7, Binding Band, Loaded Dice, Mirror Herb |
| Mirror Herb | Mew: Tackle, Splash, Recover, Protect; foe a wild Chansey that knows only Swords Dance | After Chansey's first Swords Dance, "MEW's Mirror Herb copied its foe's stat changes!" for the Mew holding it, whose Tackle then does about twice as much, and the herb is gone; the other Mew gets nothing | element 7, Binding Band, Loaded Dice, Mirror Herb |
| Eject Button | Chansey: Softboiled, Splash, Protect, Seismic Toss; foe a wild Rattata that knows only Tackle | When a Tackle hits the Chansey holding it, "CHANSEY is switched out with the Eject Button!" and the party list opens for a replacement; the other Chansey stays in | element 7, Red Card and Eject Button |
| Red Card | Chansey, as above; foe a wild Rattata that knows only Tackle | When a Tackle hits the Chansey holding it, "CHANSEY held up its Red Card against the wild RATTATA!" and the battle ends, as Dragon Tail ends a wild battle. In a trainer battle the attacker would be sent back and a random teammate dragged out ("was dragged out!"), which needs kit trainers | element 7, Red Card and Eject Button |
| Pixie Plate | Arceus: Judgment, Moonblast, Recover, Splash, the first holding the plate and set to the Fairy form (as giving it the plate from the Bag does); foe a wild Dragonite that knows only Dragon Claw | The first Arceus is pink in its summary and in battle and its type reads Fairy; its Judgment is a Fairy move, "It's super effective!" on Dragonite, and Moonblast does about a fifth more than the second's; Dragon Claw brings "It doesn't affect ARCEUS...". The second is a Normal Arceus whose Judgment is Normal. Taking the plate off in the Bag turns the first back to Normal | element 7, Pixie Plate |
| Roseli Berry | Dragonite: Roost, Splash, Protect, Dragon Claw; foe a wild Clefable that knows only Moonblast | The first Moonblast into the Dragonite holding it brings "The Roseli Berry weakened Moonblast's power!" and does about half what it does to the other, and the berry is gone. In the Bag's Berries pocket (from "All new items") it has no number, no Check Tag, cannot be planted ("can't be used") and cannot be chosen for a Poffin | element 7, Roseli Berry |
| Ability Capsule, Patch | A Machamp and a Ditto, both with no item and their personality's ability, and two Ability Capsules and the Ability Patch in the Medicine pocket | A Capsule on the Machamp first asks "Change MACHAMP's Ability to No Guard?" (or Guts, whichever it does not have); No leaves the Capsule in the Bag and goes back to "Use on which Pokémon?", and Yes brings "MACHAMP's Ability changed to No Guard!", and the summary agrees; the second Capsule swaps it back. The Patch then makes it Steadfast, after which a Capsule has no effect. The Patch asks the same way, naming Steadfast. On the Ditto, whose species has one ordinary ability, a Capsule has no effect, without asking, and stays in the Bag | element 7, Ability Capsule and Ability Patch; the prompt, element 7 follow-up |
| Mints, Bottle Caps | A Lv. 20 Machamp (below the later games' level 50, as the caps work at any level), with two Adamant Mints, a Modest and a Serious Mint, two Bottle Caps and a Gold Bottle Cap in the Medicine pocket | An Adamant Mint: "The Adamant Mint changed how MACHAMP's stats grow!"; Attack rises and Sp. Atk falls by a tenth against the Machamp's own nature, which its summary still names; a second Adamant Mint has no effect. A Bottle Cap asks "Hyper Train which stat?" with a list of six; on a stat below 31, "MACHAMP's Attack was maxed out by Hyper Training!", the IV viewer (R on the stat page) shows 31 and the stat rises; on a stat already at 31 it has no effect and stays in the Bag; B on the list goes back to choosing a Pokemon. The Gold Bottle Cap does all six | element 7, Mints and Bottle Caps |
| TM Case check | TM92, HM08, TM01 and HM01, added in that order, and no Pokemon | The TM Case sorts them No. 01 (Focus Punch), No. 92 (Trick Room), HM 01 (Cut), HM 08 (Rock Climb), exactly as before the TM cap came off; using one shows ABLE and NOT ABLE beside the party, and a move taught by an HM still cannot be forgotten. Nothing past TM92 exists yet, so this checks that nothing moved | element 7, the TM mechanism |
| Contrary on items | Snorlax given Contrary: Rest, Body Slam, Protect, Splash; foe a wild Machamp that knows only Karate Chop | The first chop into the Snorlax holding the policy (super effective) brings "SNORLAX's Attack harshly fell!" and the same for its Sp. Atk, and the policy is gone; the other Snorlax's stats stay. The Absorb Bulb, the Cell Battery, the stat Berries and the Mirror Herb follow the same rule | Contrary, element 7 follow-up |

## Not built yet

Seven of the staples rulings have no Modern rules entry. Frisk naming
every foe's item, Plus and Minus with either partner and Pressure
ignoring allies show only in a double battle. Flash Fire while frozen
needs its holder frozen, which the kit cannot do on demand. Normalize's
1.2x, Shed Skin's one in three and the 1.5x critical hit change numbers
with no message; the Critical hits entry shows the new rates instead.

Steelworker, Sharpness and Battery change only a move's power, with no
message, and the kit's Pokemon have random IVs and natures, so there is no
fixed number to look for; they have no entry. Battery also needs a double
battle, as do Hospitality, Healer and Telepathy, which have no entry either.
Magician needs a foe holding an item, which the kit's wild battles cannot
give, so it has no entry.

Kit-only trainers whose teams use the new moves, so the AI's side gets seen too.
Ian chose move sets first; trainers are the next step when he wants them.
Whether an appended trainer needs rows elsewhere, such as the trainer message
table, is to be checked before they are built.
