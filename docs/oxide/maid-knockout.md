# The Pokemon Mansion's maid knockout

Ian's design of 2026-10-31, built on `overseer-maid-knockout` as a draft for him to look at. The mansion is on Route 212 North in Wake's split (cap 44), and will sit behind Darach and Caitlin once their gate is built.

**Outcome.** The knockout is now one clear and one prize. The five maids and then Lady Celeste fight back to back with no healing, and the win over Celeste gives the game's one Ability Capsule. After that the challenge is closed for good. Pastoria's Capsule ball is gone. Ian answered the five questions of the first draft on 2026-10-31, and every answer is applied. The six teams are below: four maids with one Pokemon each, Clare and Celeste with two, from 40 to 42. Nothing has been seen in game, and no fight has been scored.

| Trainer | Idea | Pokemon | Lv | Item | Nature | Ability | Moves |
|---|---|---|---|---|---|---|---|
| Maid Belinda | the laundress (Water) | Araquanid | 40 | Big Root | Brave | Water Bubble | Waterfall, X-Scissor, Poison Jab, Aqua Ring |
| Maid Sophie | the gardener (Grass) | Lurantis | 40 | Miracle Seed | Careful | Leaf Guard | Leaf Blade, Knock Off, Brick Break, Synthesis |
| Maid Emily | the duster (Normal) | Cinccino | 41 | Wide Lens | Naive | Skill Link | Tail Slap, Rock Blast, Triple Axel, Tickle |
| Maid Elena | the cook (Fire) | Torkoal | 41 | Charcoal | Rash | Drought | Eruption, Solar Beam, Earth Power, Yawn |
| Maid Clare | the head maid, with the keys | Klefki | 41 | Sitrus Berry | Impish | Prankster | Thunder Wave, Reflect, Play Rough, Foul Play |
| | | Gothitelle | 42 | Tanga Berry | Quiet | Competitive | Psychic, Shadow Ball, Thunderbolt, Calm Mind |
| Lady Celeste | the lady of the house, who undoes a sweep | Clefable | 42 | Pixie Plate | Calm | Unaware | Moonblast, Flamethrower, Thunderbolt, Moonlight |
| | | Milotic | 42 | Leftovers | Bold | Filter | Surf, Ice Beam, Dragon Pulse, Haze |

**What the script does now.** The maid at the west of the hall explains the challenge once and then asks whether to try it. On a yes, the five maids come out one by one, as in vanilla, each naming her household job, and Lady Celeste follows. There is no turn target, no count of turns and no Rich Boy Liam. Straight after the win over Celeste she gives an Ability Capsule, guarded by `FLAG_UNUSED_0x03CC`, and then leaves. That flag is the one the reward tool hands out next, freed by Pastoria's ball, which used it before. The maid then says the challenge is complete. She never offers it again, because there is no daily reset any more. If a full Medicine pocket refuses the Capsule, talking to the maid later hands it over. A loss blacks out as before and leaves the challenge open to try again.

**Ian's answers (2026-10-31), as applied.**

1. The sizes stand at eight Pokemon: 1, 1, 1, 1, 2, 2.
2. The challenge closes after the first clear, with no daily repeat. A Capsule a full Bag refused can still be collected from the maid.
3. Celeste's Full Restore is gone from her bag.
4. Carried status and Torkoal's sun stay. Celeste's order is swapped, so Clefable leads and Milotic follows.
5. The five maids' intros name their jobs in place of vanilla's colours: laundry, the gardens, dusting, cooking, and the head maid's keys.

**Action items for Ian.** None are open. The in-game check is in `ingame-checklist.md` section 4, and the run of six fights takes about 20 minutes.

**Next steps.** The Overseer lands the branch through `merge-branch.sh`, which takes about half an hour with the build and the gate.

## How the chain is meant to play

The danger is attrition. Each maid alone is beatable, but the player's HP, PP and status carry from fight to fight, and nothing heals between them. So each maid tests a different answer and chips at it, and the closer punishes the plan a player would most likely use against one-Pokemon teams: setting up a stat boost early and sweeping the rest.

Belinda's Araquanid hits hard for a level 40 lead. Water Bubble doubles its Water moves and halves Fire damage, and Aqua Ring with Big Root lets it outlast slow chip damage. Sophie's Lurantis is slow and bulky, removes held items with Knock Off and heals with Synthesis. Emily's Cinccino is the fastest of the eight (121 Speed), and Skill Link lands all five hits of Tail Slap and Rock Blast and all three of Triple Axel, which beats Substitute and Focus Sash. Tickle softens whatever would wall it. Elena's Torkoal is the cook's kettle: it is the slowest of the eight (32 Speed), so the player always moves first, and its sun Eruption punishes anything that cannot knock it out quickly. Yawn can put the next Pokemon to sleep inside the fight. Clare is the head maid. Klefki keeps the keys, paralysing and setting Reflect with Prankster priority, and Gothitelle behind it sets up Calm Mind under that screen. Tanga Berry covers its four-times weakness to Bug. Celeste closes the chain. Her Clefable leads, and its Unaware ignores every boost the player built up through the maids, with Moonlight to outlast a tired team. Milotic behind it uses Haze to wipe whatever boosts are left. She has no bag item.

Every member is at least two levels under the cap of 44, as an ordinary trainer should be. No item or nature repeats anywhere in the chain. There is no one-hit KO move, forced trade, trap or evasion move. Oxide's later species are Araquanid, Lurantis, Cinccino, Klefki and Gothitelle.

## Stats at level

From the game's own team builder (`calc_trainers.build_trainer`), with no effort values. The IVs follow each team's iv_scale (220 to 232, about 26 to 28).

| Pokemon | Lv | HP | Speed | Attack | Sp. Atk |
|---|---|---|---|---|---|
| Araquanid | 40 | 114 | 44 | 78 | 55 |
| Lurantis | 40 | 116 | 51 | 99 | 71 |
| Cinccino | 41 | 123 | 121 | 93 | 69 |
| Torkoal | 41 | 119 | 32 | 85 | 93 |
| Klefki | 41 | 108 | 77 | 81 | 72 |
| Gothitelle | 42 | 130 | 63 | 62 | 114 |
| Clefable | 42 | 143 | 71 | 67 | 96 |
| Milotic | 42 | 143 | 84 | 60 | 100 |

## The changes, by file

`res/field/scripts/scripts_pokemon_mansion.s` loses the random turn target, the turn count and Liam. It also loses vanilla's daily reset, which rolled the target and cleared the closers' trainer flags each day. Celeste's trainer flag is now set only when she is beaten, so it means "cleared", and nothing clears it again. The prize is given from one routine, which is reached straight after the win and again from the maid when a full Bag refused it. `res/text/pokemon_mansion.json` loses the turn and Liam lines and gains three: Celeste's gift, her leaving, and the maid's kept-gift line. The maid's "visit again tomorrow" becomes a line saying the challenge is complete, and the five intros name the maids' jobs. Every new line is within 37 characters, as the bank's longest vanilla lines are.

Pastoria's ball was the last object event on its map, and visible item entry 473 was the last entry in `scripts_visible_items.s`, so both came out without moving any other object id or script number.

The reward table's row for the Capsule (`reward-placements.tsv` and the `ADDED` list in `balance/rewards.py`) is now a gift on the mansion's map header. It names the Capsule as the item it replaces, which is how `place_rewards.py` checks a hand-scripted gift. The divergences are registered where the bulk tools keep them: `scripts_pokemon_mansion` in `bulk_scripts.py`, text bank 490 in `import_base_rom.TEXT_BANKS_SKIPPED`, and the Pastoria entry in `bulk_events.py` extended. The base ROM never changed the mansion's script or text, so the dry runs would skip them anyway; the entries record why they differ from vanilla.

Three small edge cases follow from reusing the flag and from the trainer flag's new meaning:

- A save that picked up Pastoria's ball already has the flag set, so its mansion clear gives no second Capsule. The game still has exactly one.
- The reward tool's spare-flag count reads 46 of 85, one under the truth, because it counts reward trainers and new balls but not hand-scripted gifts. `SpareFlags` still treats the flag as taken, since it scans the tree for every flag name.
- A save that ever started vanilla's challenge has Celeste's trainer flag set, since vanilla set it when the challenge began, so its maid would hand over the Capsule without the fight. Only a save from before this change can meet this.

## What was checked

On the branch merged with `origin/oxide`: `make rom` builds. The built mansion script decodes fully, and `scriptdis --verify` finds no movement block colliding with code. `place_rewards.py check` finds every one of the table's 168 rows exactly once with no problems, `test_place_rewards` passes, and `rewards check` has 0 failures. `checkmap.py` shows the mansion's events byte-identical to the base ROM and its script changed, as intended. On Pastoria it reports only the registered differences: the hidden Abra and the Scorbunny check, with the ball now gone too. Every team was saved through `trainers.save`, which runs the trainer lint and the real packer, and the lint is clean on all six. Every move is on its species' Oxide list at its level (`learnsets.oxide_list`). Celeste's bag was edited by hand, since the team builder does not edit it, and is registered in `trainers_diverged.json`. The script index is regenerated. Rich Boy Liam is now fought nowhere, so his row left `trainer-roles.tsv` and `test_b1` lists him as a trainer taken out of play; his team file is unchanged.

Not checked: no in-game look, no scorer reading (Ian has named no fight), and no AI-picks probe. The simulator reads one fight at a time, so it cannot model a chain where HP and status carry over.
