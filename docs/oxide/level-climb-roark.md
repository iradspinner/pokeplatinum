# The level climb in Roark's split

Ian answered the cleanup's questions on 2026-10-31 (`cleanup-five-splits.md`), and this page is what came of them, on the branch `overseer-roark-pass`. Roark's split gets the pass the other four splits had, which reverses "Roark's split is left as it is" of 2026-10-29. Barry 2 and Beauty Devon lose their repeats, and fourteen off-list moves on the Galactic fights and two other teams go on egg lists.

## Summary

All 16 ordinary and gym teams of Roark's split were rebuilt, from Route 202 to the Oreburgh gym. Two caps are in force: Barry 2's honour cap of 11 on Route 202 and in the Trainers' School, then Roark's 16 from Route 203 on. The teams now climb from 7 to 15 in play order, where 8 of the 16 stood at 15 and Route 202 stood at 9 and 10, one under Barry 2's cap. Only Youngster Darius, the gym's last guard, is one under a cap, and none is at one.

The 60 members are now 60 different species, 19 of them from after Platinum, where before one (Nacli) was. Every member holds its own plain early item and names its own nature, where 44 held nothing and 47 named none. No member is Adamant, Jolly, Modest or Timid. Team sizes stay 3 to 5 and vary, and no trainer moved, so the mandatory count stays at 8, as Ian said.

| # | Trainer | Area | Kind | Cap in force | Old top | New top |
|---:|---|---|---|---:|---:|---:|
| 1 | Youngster Tristan | Route 202 | mandatory | 11 | 9 | 7 |
| 2 | Lass Natalie | Route 202 | mandatory | 11 | 10 | 8 |
| 3 | Youngster Logan | Route 202 | mandatory | 11 | 10 | 8 |
| 4 | School Kid Harrison | Trainers' School, Jubilife | optional | 11 | 10 | 9 |
| 5 | School Kid Christine | Trainers' School, Jubilife | optional | 11 | 9 | 9 |
| | Barry 2, ace at 11 | Route 203 | boss | | | |
| 6 | Youngster Michael | Route 203 | optional | 16 | 15 | 11 |
| 7 | Youngster Dallas | Route 203 | optional | 16 | 15 | 11 |
| 8 | Youngster Sebastian | Route 203 | mandatory | 16 | 15 | 12 |
| 9 | Lass Madeline | Route 203 | mandatory | 16 | 14 | 12 |
| 10 | Lass Kaitlin | Route 203 | optional, wanders | 16 | 14 | 13 |
| 11 | Camper Curtis | Oreburgh Gate 1F | mandatory | 16 | 14 | 13 |
| 12 | Picnicker Diana | Oreburgh Gate 1F | mandatory | 16 | 15 | 13 |
| 13 | Worker Mason | Oreburgh Mine B2F | mandatory | 16 | 15 | 14 |
| 14 | Worker Colin | Oreburgh Mine B2F | optional | 16 | 15 | 14 |
| 15 | Youngster Jonathon | Oreburgh Gym | gym | 16 | 15 | 14 |
| 16 | Youngster Darius | Oreburgh Gym | gym | 16 | 15 | 15 |

Route 202's order is the one `test_b1e` traces on the collision map (Tristan's column, then Natalie's, then Logan's). Route 203's is west to east from Barry 2's tile, the mine's is Mason on the way down and Colin off to the side by Roark, and the gym's is Jonathon by the door and Darius by Roark.

What Ian decides:

1. The teams below, as a set. Any team can go back to its old species without touching the levels.
2. Whether Route 202's drop is the right size. Its three trainers came down two levels each, to 7 and 8, so that a player who reaches the route at 6 or 7 meets each a level or so above them, and the school's two sit at 9 under Barry 2's 11.
3. Whether Darius at 15 stands. He is the split's one trainer one under its cap, as the last guard before the leader, the place Maylene's Jeffery and Wake's Samson hold in their gyms.

Next steps: the Overseer lands the branch (one merge and the gate, about half an hour), then Ian plays the fights he wants to see. No scorer reading was run, and none is needed unless Ian names a fight.

What is unverified:

- Nothing has been seen in game. The real packer accepted every team.
- The trainer AI's choices with the new sets (the AI probe was not run).
- No speed or damage table was made against the box, unlike the Gardenia climb. The sets were judged against the moves the box has at these levels, and the strongest threats are named under the teams.
- The school's two are placed before Barry 2, where they are first in reach; a player who visits after him meets them a few levels under his own team.
- Lass Kaitlin wanders, so she is read as optional, and her place in the order is her starting tile.

## Barry 2

Ian, on question 3: change them, but "keep the items very simple though". In all three versions Buizel, Munchlax and the starter each held an Oran Berry. The starter keeps it, Buizel now holds a Cheri Berry and Munchlax a Pecha Berry. In the Piplup version Buizel and Turtwig were both Adamant, and Turtwig is now Brave, which keeps the raised Attack and lowers a Speed the slow Turtwig loses little by. Nothing else changed.

| Version | Member | Item | Nature |
|---|---|---|---|
| all three | Starly 10 | Sharp Beak, as before | Jolly, as before |
| all three | Buizel 10 | Cheri Berry, was Oran | Adamant, as before |
| all three | Munchlax 10 | Pecha Berry, was Oran | Careful, as before |
| Piplup | Turtwig 11 | Oran Berry, as before | Brave, was Adamant |
| Chimchar | Piplup 11 | Oran Berry, as before | Modest, as before |
| Turtwig | Chimchar 11 | Oran Berry, as before | Naive, as before |

## Beauty Devon

Ian, on question 4: "Sure". Devon's Spinda is now Lonely, where both members were Gentle. Its set is all physical beside Teeter Dance (Fake Out, Faint Attack, Last Resort), so the raised stat moves from Special Defense to Attack, and Lonely keeps the lowered Defense Ian chose. Clefable stays Gentle, which suits a Follow Me partner that takes the hits.

## The egg lists

Ian, on question 9: each move goes on its line's first-stage egg list, under his ruling of 2026-10-29, and no level-up entry moves. Each is in `learnrewrite.IAN_EGG_MOVES` but Koffing's: Koffing's line is one of the generator's five held-out lines, which `learnrewrite.py` may not name, so it has a line in `learnsets_by_hand.txt`, as Eevee's does. Lunatone had no egg list and now has one. The OxiDex's list gives all 21 member moves at their levels now; it gave none before.

| Fight | Member | Move | First stage |
|---|---|---|---|
| Mars 1 | Liepard 18 | Faint Attack | Purrloin |
| Mars 1 | Torracat 19 | Flame Wheel | Litten |
| Somnu 1 | Gastly 17 | Nightmare, Sludge | Gastly |
| Somnu 1 | Munchlax 17 | Yawn, Body Slam, Crunch | Munchlax |
| Jupiter 1 | Lanturn 26 | Discharge | Chinchou |
| Jupiter 1 | Galarian Weezing 28 | Strange Steam, Toxic Spikes | Koffing (in `learnsets_by_hand.txt`) |
| Eterna building 3F grunt | Snover 25 | Ice Shard | Snover |
| the same | Xatu 25 | Future Sight, Air Slash | Natu |
| the same | Galarian Mr. Mime 25 | Freeze-Dry, Future Sight | Galarian Mr. Mime, its own first stage |
| the same | Lunatone 25 | Future Sight, Icy Wind | Lunatone |
| the same | Kadabra 26 | Future Sight, Icy Wind | Abra |
| Lucas and Dawn 1, the Turtwig versions | Turtwig 9 | Absorb | Turtwig |
| Collector Jamal | Noctowl 38 | Tailwind | Hoothoot |

## The teams

Each line gives the team in the order it is sent out, each member with its ability, item and nature. An asterisk marks a species from after Platinum.

| Trainer | Idea | Team | Species changes |
|---|---|---|---|
| Tristan | Tailwind, then priority from an Adaptability Sentret | Rookidee* 6 (Unnerve, Oran Berry, Naive), Sentret 7 (Adaptability, Quick Claw, Quirky), Fletchling* 7 (Big Pecks, Charcoal, Hasty) | +Rookidee, +Fletchling, minus Zigzagoon and Starly |
| Natalie | Thunder Wave, then Defense Curl into Rollout, doubled by a Simple Bidoof | Wooloo* 7 (Fluffy, Silk Scarf, Docile), Bidoof 7 (Simple, Hard Stone, Relaxed), Spheal 8 (Thick Fat, Oran Berry, Sassy) | +Wooloo, minus Phanpy |
| Logan | Sticky Web, String Shot and Stun Spore slow the player for the bugs | Grubbin* 7 (Swarm, Persim Berry, Bashful), Wurmple 7 (Shield Dust, Poison Barb, Naughty), Kricketot 7 (Shed Skin, Oran Berry, Lax), Sewaddle* 8 (Swarm, SilverPowder, Sassy) | +Grubbin, +Kricketot, +Sewaddle, minus Weedle, Kakuna and Beedrill |
| Harrison | Encore locks a setup or a wasted turn, beside Sing, Thunder Wave and Stun Spore | Pichu 8 (Static, Oran Berry, Naive), Cleffa 8 (Magic Guard, Persim Berry, Calm), Abra 8 (Inner Focus, Magnet, Rash), Shroomish 9 (Poison Heal, Miracle Seed, Lax) | +Cleffa (three became four) |
| Christine | psychic tricks: Confuse Ray, Tickle, Disable and a Calm Mind Ralts | Natu 8 (Magic Guard, Sharp Beak, Hasty), Gothita* 8 (Competitive, TwistedSpoon, Quiet), Ralts 9 (Synchronize, Oran Berry, Serious) | +Gothita, minus Chingling and Meditite (four became three) |
| Michael | grass that wears the player down: Stun Spore, Poison Powder, Leech Seed, a Harvest Smoliv | Budew 10 (Natural Cure, Poison Barb, Mild), Lotad 10 (Own Tempo, Big Root, Docile), Paras 10 (Dry Skin, SilverPowder, Brave), Smoliv* 11 (Harvest, Oran Berry, Serious) | +Lotad, +Smoliv, minus Zubat and Oddish |
| Dallas | a Compound Eyes Thunder Wave, then electric hits | Joltik* 10 (Compound Eyes, Magnet, Hasty), Mareep 10 (Static, Oran Berry, Quiet), Pawmi* 11 (Static, Chople Berry, Naive) | +Joltik, +Pawmi, minus Shinx, Pikachu and Elekid (four became three) |
| Sebastian | priority fighters (Fake Out, Mach Punch, Bullet Punch), then a Bulk Up Makuhita | Tyrogue 11 (Steadfast, Persim Berry, Hardy), Clobbopus* 11 (Technician, Oran Berry, Impish), Mankey 11 (Vital Spirit, Black Belt, Naughty), Makuhita 12 (Thick Fat, Sitrus Berry, Brave) | +Tyrogue, +Clobbopus, minus Machop (three became four) |
| Madeline | Toxic Spikes into a Merciless Mareanie, with Yawn and Confuse Ray | Wooper 11 (Unaware, Soft Sand, Relaxed), Psyduck 11 (Damp, Mystic Water, Mild), Mareanie* 11 (Merciless, Poison Barb, Naughty), Chinchou 12 (Volt Absorb, Sitrus Berry, Bashful) | +Mareanie (three became four) |
| Kaitlin | five Intimidates with Glare, Will-O-Wisp and Thunder Wave against a physical box | Ekans 12 (Intimidate, Pecha Berry, Lax), Growlithe 12 (Intimidate, Charcoal, Gentle), Snubbull 12 (Intimidate, Oran Berry, Brave), Litten* 13 (Intimidate, Rawst Berry, Quirky), Mawile 13 (Intimidate, BlackGlasses, Docile) | +Litten, +Mawile, minus Taillow and Spoink |
| Curtis | poison that punishes contact: Poison Point, Toxic Debris, Spikes | Nidoran M 13 (Poison Point, Oran Berry, Hardy), Glimmet* 12 (Toxic Debris, Shuca Berry, Quiet), Qwilfish 13 (Poison Point, Mystic Water, Impish) | +Glimmet, minus Nidoran F and Roselia (four became three) |
| Diana | four Technician users behind Fake Out | Minccino* 12 (Technician, Silk Scarf, Naive), Meowth 12 (Technician, Oran Berry, Lonely), Kricketune 12 (Technician, Cheri Berry, Serious), Aipom 13 (Technician, Sitrus Berry, Hasty) | +Minccino, minus Skitty |
| Mason | Stealth Rock, then a work crew of rocks and burns | Diglett 13 (Sand Force, Soft Sand, Naive), Geodude 13 (Sturdy, Oran Berry, Impish), Charcadet* 13 (Flash Fire, Charcoal, Mild), Rhyhorn 13 (Rock Head, Quick Claw, Brave), Larvitar 14 (Guts, BlackGlasses, Lonely) | +Charcadet, minus Makuhita |
| Colin | hard to break: Iron Defense, Recover, a Defense Curl Rollout and a No Guard Machop | Sandygast* 13 (Water Compaction, Spell Tag, Quiet), Nacli* 13 (Purifying Salt, Sitrus Berry, Sassy), Bonsly 13 (Rock Head, Hard Stone, Impish), Machop 14 (No Guard, Black Belt, Naughty) | +Sandygast, +Bonsly, minus Whismur and Geodude |
| Jonathon | Stealth Rock and screens, then a Sturdy Onix's Defense Curl Rollout | Nosepass 13 (Solid Rock, Sitrus Berry, Relaxed), Onix 13 (Sturdy, Hard Stone, Docile), Carbink* 14 (Clear Body, Light Clay, Bashful) | +Onix, +Carbink, minus Geodude and Lileep |
| Darius | fossil shells that set up: Spikes, Rock Polish and Iron Defense | Omanyte 14 (Shell Armor, Mystic Water, Rash), Kabuto 14 (Battle Armor, Passho Berry, Naughty), Dwebble* 14 (Sturdy, Oran Berry, Serious), Shieldon 15 (Solid Rock, Chople Berry, Sassy) | +Omanyte, +Dwebble, minus Anorith and Cranidos |

The gym's two no longer carry Lileep, Anorith or Cranidos, which Roark himself fields, so the player meets his fossils first in his own fight. Worker Colin was the one team of the split on the basic AI alone; it now has the other fifteen's three flags.

Moves were kept to the rung the split sits on: before Barry 2 the attacks run 40 to 55 in power, with Rollout's climb the one that grows; after him 50 to 70, with Rock Slide (75) on Mason's Larvitar alone. The members a player must answer first are Natalie's Bidoof (+2 Defense from one Curl, then Rollout), Curtis's Glimmet (Ancient Power off a high Special Attack, though frail and four times weak to Ground), Diana's Kricketune (Technician Karate Chop off 105 Attack), Kaitlin's Mawile and Mason's Larvitar.

## How the teams were checked

| Check | Result |
|---|---|
| The trainer lint, on every changed team (the 16, Barry 2's three and Devon) | no errors, no warnings |
| The packer, through the team builder's save | every team packed |
| Every move on Oxide's list at its level, or a TM the species had before the TM pass | all legal |
| No item or nature repeated in a team, every nature named, every item a real one | none repeated, none missing |
| No one-hit KO, forced trade, trapping or evasion move; no trapping or evasion ability | none (Diglett takes Sand Force, not Arena Trap) |
| No ordinary trainer at its cap; one under it | none at a cap; one under, Darius |
| Pairs fought alone (`pairs.pairs()`) | none in the split |
| `test_trainers` | 44 of 44 |
| `test_learnrewrite` and `test_learncheck` | 6 of 6 and 18 of 18 |
| `rewards.py write`, then `rewards.py check` | six team sizes moved in the role table, nothing else; 0 failures |

## Out of scope and left alone

Roark, Barry 1 and Barry 2's species, levels and moves, Lucas and Dawn, every named Galactic file, the comb's never-overwrite list, and the rematch files of Tristan, Madeline and Dallas are untouched. The first fight with Barry, on Route 201, stays ignorable, as Ian wants.
