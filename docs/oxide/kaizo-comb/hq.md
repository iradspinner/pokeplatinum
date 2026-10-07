# The comb: the Galactic headquarters split

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The two bosses of the headquarters split are combed: Cyrus on 4F and Saturn
in the control room. Both files pass the checker and the rule audit. The
split's grunts and scientists follow in the later pass, as the building's
gauntlet.

The cap is 60, and no map here has its own weather. My simulator reads the
bosses against the scorer's box at HQ, which knows no TMs, so they read
harsher than they will once the TM pass lands. Saturn fights under permanent
Trick Room for the whole battle (Ian's design of 2026-09-26, in the battle
code), so his six is built slow and bulky, on natures that lower Speed, and
both his file and today's are read under the room. Cyrus reads about 95 won
to today's 99.6, and Saturn about 93 to today's 99. Each carries one legendary
(Suicune, Uxie) where today's Saturn carried two. No conditional attack
appears.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Cyrus 2's setup move sits on Houndoom, not his ace | The dial puts a boss's setup move on its ace. A Swords Dance Weavile ace read 65 to 74 won, far past a step harder, so Weavile keeps today's Fake Out and Ice Shard and the Nasty Plot sits on Houndoom. Today's Mean Look and Rest Dusknoir and Curse Suicune are gone; Magnezone's Magnet Pull stays as the trap. | `galactic_boss_cyrus_galactic_hq.json`; the scorer's reading later. | Accept (recommended), or a Swords Dance Weavile with the rest a level lower. |
| 2 | Saturn 2 is built for his permanent Trick Room | Uxie leads with Stealth Rock and Thunder Wave behind a Focus Sash, then a Shadow Tag Wobbuffet with Counter (the trap the dial asks of him, and his one trade), Lickilicky, today's Wailord with Water Spout, Rhyperior and a Toxicroak ace, all on natures that lower Speed. Cresselia is out, so he keeps one legendary. A Curse Snorlax ace read 48 won under the room, and a Bronzong with Light Clay screens in Lickilicky's place read 97. | `commander_saturn_galactic_hq.json`, read under Trick Room; the scorer's reading later, which must model the room. | Accept (recommended). |

## What comes next

The Galactic split's bosses (Spear Pillar, the Distortion World and Stark
Mountain), then Volkner's, Barry's and the League's, then the ordinary
trainers from Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Cyrus 2 | Galactic HQ 4F | on the path | single, boss | 6 | 58 to 60 | Two hazards and a trap | about 95 / 1.5 / 17 in my simulator, where today's file reads 100 / 0.9 / 21 |
| Saturn 2 | Galactic HQ control room | on the path | single, boss, permanent Trick Room | 6 | 58 to 60 | Slow and bulky for his permanent Trick Room | about 93 / 2.7 / 0 in my simulator, where today's file reads 99 / 1.5 / 1 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file.

## The bosses

### Cyrus 2: Galactic HQ 4F, on the path, single, boss, cap 60

Two hazards and a trap: Skarmory lays Stealth Rock and Spikes behind a Focus Sash and phazes with Whirlwind, Magnezone's Magnet Pull traps Steel types (the fight's one trade), then Dusknoir's Will-O-Wisp, a Nasty Plot Houndoom, Suicune as the legendary, and Weavile at the cap with Fake Out and Ice Shard.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 58 | Focus Sash | Filter | Impish | Stealth Rock, Spikes, Whirlwind, Brave Bird |
| Magnezone | 58 | Shuca Berry | Magnet Pull | Modest | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Dusknoir | 58 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Houndoom | 58 | Sitrus Berry | Flash Fire | Timid | Flamethrower, Dark Pulse, Sludge Bomb, Nasty Plot |
| Suicune | 58 | Leftovers | Pressure | Bold | Surf, Ice Beam, Roar, Toxic |
| Weavile | 60 | Lum Berry | Technician | Jolly | Night Slash, Ice Punch, Ice Shard, Fake Out |

Today's team: Skarmory 57 (Sitrus Berry; Stealth Rock, Steel Wing, Pluck, Tailwind), Dusknoir 57 (Chesto Berry; Shadow Punch, Brick Break, Mean Look, Rest), Houndoom 57 (Charcoal; Flamethrower, Sludge Bomb, Will-O-Wisp, Dark Pulse), Suicune 57 (Leftovers; Aqua Ring, Curse, Waterfall, Avalanche), Magnezone 57 (Shuca Berry; Magnet Rise, Flash Cannon, Charge Beam, Natural Gift), Weavile 58 (NeverMeltIce; Night Slash, Ice Punch, Ice Shard, Fake Out). Expected: about 95 / 1.5 / 17 in my simulator, where today's file reads 100 / 0.9 / 21.

### Saturn 2: Galactic HQ control room, on the path, single, boss, permanent Trick Room, cap 60

Slow and bulky for his permanent Trick Room: Uxie leads with Stealth Rock and Thunder Wave behind a Focus Sash, the Shadow Tag Wobbuffet returns with Counter (the trap and the trade), then a Poison Heal Lickilicky, Wailord's Water Spout, Rhyperior and a Swords Dance Toxicroak ace, all on natures that lower Speed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Uxie | 58 | Focus Sash | Levitate | Relaxed | Stealth Rock, U-turn, Psychic, Thunder Wave |
| Lickilicky | 59 | Toxic Orb | Poison Heal | Brave | Body Slam, Earthquake, Knock Off, Power Whip |
| Wobbuffet | 59 | Leftovers | Shadow Tag | Relaxed | Counter, Encore, Safeguard, Charm |
| Wailord | 59 | Leftovers | Pressure | Quiet | Water Spout, Surf, Ice Beam, Toxic |
| Rhyperior | 59 | Passho Berry | Solid Rock | Brave | Earthquake, Stone Edge, Hammer Arm, Ice Punch |
| Toxicroak | 60 | Life Orb | Dry Skin | Brave | Gunk Shot, Cross Chop, Sucker Punch, Swords Dance |

Today's team: Uxie 57 (Lum Berry; Hypnosis, Future Sight, U-turn, Foul Play), Lickilicky 57 (Toxic Orb; Slam, Curse, Gyro Ball, ThunderPunch), Wailord 57 (Leftovers; Water Spout, Earthquake, Aqua Ring, Avalanche), Rhyperior 57 (Expert Belt; Earthquake, Stone Edge, Aqua Tail, Fire Punch), Cresselia 57 (Leftovers; Moonlight, Charge Beam, Calm Mind, Ice Beam), Toxicroak 58 (Life Orb; Gunk Shot, Cross Chop, Sucker Punch, Fire Punch). Expected: about 93 / 2.7 / 0 in my simulator, where today's file reads 99 / 1.5 / 1.

