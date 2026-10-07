# The comb: Volkner's split

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of Volkner's split are combed: Ace Trainers Zachery and Destiny in
Sunyshore's gym, and Volkner. All three files pass the checker and the rule
audit. The split's ordinary trainers follow in the later pass.

The cap is 68, and no map here has its own weather. My simulator reads the
bosses against the scorer's box at this split, which knows no TMs, and under
Ian's move reworks of 2026-10-06, so they read harsher than they will once
the TM pass lands. Volkner reads about 97 won with 2.6 faints to today's 100
with 0.6. His two Ace Trainers sit three under the cap with sharper sets, as
Ian's rule on levels asks. No conditional
attack appears. Ian allowed two or three legendaries per boss from Cyrus 3 on
(2026-10-06); Volkner already reads a step harder than today's without one,
so he carries none.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Volkner without rain or Choice items | Today's Volkner has a Damp Rock Rain Dance and three Choice items. Here Forretress leads with Stealth Rock and Spikes behind a Focus Sash and pivots out with Volt Switch, as the dial asks of him (paralysis on several members, Volt Switch); it is a Steel and Bug type carrying an Electric move, under Ian's gym-theme rule. Jolteon, Lanturn and Magnezone carry Thunder Wave, Rotom Volt Switch and Will-O-Wisp, and a Life Orb Electivire is the ace. | `leader_volkner.json`; the scorer's reading later. | Accept (recommended), or bring back the rain on Jolteon's Damp Rock. |

## What comes next

Barry's split's bosses, then the League's, then the ordinary trainers from
Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Ace Trainer Zachery | Sunyshore Gym | gym trainer | single, Ace Trainer | 6 | 63 to 65 | Electric types | about 99 / 1.0 / 20 with a planned six |
| Ace Trainer Destiny | Sunyshore Gym | gym trainer | single, Ace Trainer | 6 | 63 to 65 | Electric types | about 100 / 1.1 / 1 with a planned six |
| Volkner | Sunyshore Gym | on the path | single, boss | 6 | 67 to 68 | Paralysis and Volt Switch | about 97 / 2.6 / 0 in my simulator, where today's file reads 100 / 0.6 / 53 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

### Ace Trainer Zachery: Sunyshore Gym, gym trainer, single, Ace Trainer, cap 68

Electric types: Magnezone's Thunder Wave, Rotom's Will-O-Wisp, Ampharos's Light Screen, Manectric, a Galvantula behind a Focus Sash, and a Nasty Plot Raichu ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magnezone | 64 | Shuca Berry | Levitate | Modest | Thunderbolt, Flash Cannon, Volt Switch, Thunder Wave |
| Rotom | 63 | Spooky Plate | Levitate | Timid | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Ampharos | 63 | Leftovers | Static | Modest | Thunderbolt, Dragon Pulse, Power Gem, Light Screen |
| Manectric | 63 | Life Orb | Lightning Rod | Timid | Thunderbolt, Flamethrower, Signal Beam, Crunch |
| Galvantula | 64 | Focus Sash | Compound Eyes | Timid | Thunderbolt, Bug Buzz, Energy Ball, Thunder Wave |
| Raichu | 65 | Lum Berry | Static | Timid | Thunderbolt, Focus Blast, Surf, Nasty Plot |

Today's team: Magnezone 60 (Thunderbolt, Flash Cannon, Tri Attack, Rain Dance), Rotom 60 (Thunderbolt, Shadow Ball, Light Screen, Will-O-Wisp). Expected: about 99 / 1.0 / 20 with a planned six; read blind, 40 / 4.5 / 4.

### Ace Trainer Destiny: Sunyshore Gym, gym trainer, single, Ace Trainer, cap 68

Electric types: Pachirisu's Super Fang and Thunder Wave, Jolteon, Luxray, Lanturn, Vikavolt and an Electivire ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pachirisu | 63 | Sitrus Berry | Adaptability | Jolly | ThunderPunch, U-turn, Super Fang, Thunder Wave |
| Jolteon | 64 | Magnet | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Signal Beam, Volt Switch |
| Luxray | 63 | Flame Orb | Guts | Adamant | Facade, Thunder Fang, Crunch, Superpower |
| Lanturn | 64 | Leftovers | Volt Absorb | Modest | Scald, Discharge, Ice Beam, Thunder Wave |
| Vikavolt | 63 | SilverPowder | Levitate | Modest | Thunderbolt, Bug Buzz, Energy Ball, Flash Cannon |
| Electivire | 65 | Life Orb | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Electivire 60 (ThunderPunch, Low Kick, Light Screen, Fire Punch), Jolteon 60 (Thunderbolt, Shadow Ball, Thunder Wave, Signal Beam). Expected: about 100 / 1.1 / 1 with a planned six; read blind, 32 / 5.1 / 0.

### Volkner: Sunyshore Gym, on the path, single, boss, cap 68

Paralysis and Volt Switch, as the dial asks of him: Forretress leads with Stealth Rock and Spikes behind a Focus Sash and pivots out with Volt Switch (an off-type member carrying an Electric move), then Jolteon, Lanturn and Magnezone with Thunder Wave, Rotom with Volt Switch and Will-O-Wisp, and a Life Orb Electivire ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Forretress | 67 | Focus Sash | Heatproof | Relaxed | Stealth Rock, Spikes, Volt Switch, Gyro Ball |
| Jolteon | 67 | Shuca Berry | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Volt Switch, Thunder Wave |
| Lanturn | 67 | Leftovers | Volt Absorb | Modest | Scald, Discharge, Ice Beam, Thunder Wave |
| Rotom | 67 | Sitrus Berry | Levitate | Modest | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Magnezone | 67 | Shuca Berry | Levitate | Modest | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Electivire | 68 | Life Orb | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Jolteon 61 (Damp Rock; Thunder, Shadow Ball, Thunder Wave, Rain Dance), Rotom 61 (Leftovers; Thunder, Shadow Ball, Leaf Storm, Thunder Wave), Lanturn 61 (Focus Sash; Surf, Thunder, Ice Beam, Aqua Ring), Magnezone 61 (Choice Specs; Thunder, Tri Attack, Flash Cannon, Signal Beam), Luxray 61 (Choice Band; Ice Fang, Thunder Fang, Crunch, Superpower), Electivire 62 (Choice Scarf; ThunderPunch, Ice Punch, Cross Chop, Giga Impact). Expected: about 97 / 2.6 / 0 in my simulator, where today's file reads 100 / 0.6 / 53.

