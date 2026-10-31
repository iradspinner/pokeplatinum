# The Pokemon Mansion's maid knockout

Ian's design of 2026-10-31, built on `overseer-maid-knockout` as a draft for him to look at. The mansion is on Route 212 North in Wake's split (cap 44), and will sit behind Darach and Caitlin once their gate is built.

**Outcome.** The knockout is now one clear and one prize. The five maids and then Lady Celeste fight back to back with no healing, every time, and the first win over Celeste gives the game's one Ability Capsule. Pastoria's Capsule ball is gone. The six teams below are drafts: four maids with one Pokemon each, Clare and Celeste with two, from 40 to 42. The ROM builds and the gate's checks are listed at the end. Nothing has been seen in game, and no fight has been scored.

| Trainer | Idea | Pokemon | Lv | Item | Nature | Ability | Moves |
|---|---|---|---|---|---|---|---|
| Maid Belinda | the laundress (Water) | Araquanid | 40 | Big Root | Brave | Water Bubble | Waterfall, X-Scissor, Poison Jab, Aqua Ring |
| Maid Sophie | the gardener (Grass) | Lurantis | 40 | Miracle Seed | Careful | Leaf Guard | Leaf Blade, Knock Off, Brick Break, Synthesis |
| Maid Emily | the duster (Normal) | Cinccino | 41 | Wide Lens | Naive | Skill Link | Tail Slap, Rock Blast, Triple Axel, Tickle |
| Maid Elena | the cook (Fire) | Torkoal | 41 | Charcoal | Rash | Drought | Eruption, Solar Beam, Earth Power, Yawn |
| Maid Clare | the head maid, with the keys | Klefki | 41 | Sitrus Berry | Impish | Prankster | Thunder Wave, Reflect, Play Rough, Foul Play |
| | | Gothitelle | 42 | Tanga Berry | Quiet | Competitive | Psychic, Shadow Ball, Thunderbolt, Calm Mind |
| Lady Celeste | the lady of the house, who undoes a sweep | Milotic | 42 | Leftovers | Bold | Filter | Surf, Ice Beam, Dragon Pulse, Haze |
| | | Clefable | 42 | Pixie Plate | Calm | Unaware | Moonblast, Flamethrower, Thunderbolt, Moonlight |

**What the script does now.** The maid at the west of the hall explains the challenge once and then asks whether to try it. On a yes, the five maids come out one by one, as in vanilla, and Lady Celeste follows every time. There is no turn target, no count of turns and no Rich Boy Liam. Straight after the first win over Celeste she gives an Ability Capsule, guarded by `FLAG_UNUSED_0x03CC`, and then leaves. That flag is the one the reward tool hands out next, freed by Pastoria's ball, which used it before. The daily repeat stays, because it was the smallest change: once Celeste is beaten the maid asks the player back tomorrow, and the next day the whole chain runs again with no prize. If a full Medicine pocket refuses the Capsule, talking to the maid the same day hands it over. A loss blacks out as before, and the player may try again the same day.

**Action items for Ian.** Answer these in a line each.

1. Team sizes run 1, 1, 1, 1, 2, 2, eight Pokemon over six fights. Should Elena carry a second Pokemon too, making nine?
2. The daily repeat makes the whole chain a daily source of experience at 40 to 42, and of prize money, after the Capsule is won. Keep it, or close the challenge for good after the first clear? Closing it is a few lines of script.
3. Celeste keeps vanilla's Full Restore in her bag, which the AI uses once. Keep it, or drop it so the closer carries held items only?
4. Status carries through a chain with no healing. Klefki's Prankster Thunder Wave can leave a Pokemon paralysed for Celeste. Torkoal's Drought sun lasts its whole fight, as Generation 4 weather does, so Solar Beam is a one-turn move and Eruption hits at 150 while Torkoal is healthy. Torkoal is very slow, so it is always hit first. Are both fine, or should Elena trade Eruption for Lava Plume?
5. The maids' intro lines still name vanilla's colours (blue, green, yellow, pink, red). Belinda's blue and Sophie's green fit their jobs; Emily's "sunshine girl", Elena's pink and Clare's red do not. Should the five intros be rewritten to name the household jobs?

**Next steps.** Ian's answers take minutes. A session then applies them on this branch, which takes 30 minutes to an hour with a rebuild and the gate. The in-game check is in `ingame-checklist.md` section 4, and the run of six fights takes about 20 minutes. The Overseer lands the branch once Ian is happy with the teams.

## How the chain is meant to play

The danger is attrition. Each maid alone is beatable, but the player's HP, PP and status carry from fight to fight, and nothing heals between them. So each maid tests a different answer and chips at it, and the closer punishes the plan a player would most likely use against one-Pokemon teams: setting up a stat boost early and sweeping the rest.

Belinda's Araquanid hits hard for a level 40 lead. Water Bubble doubles its Water moves and halves Fire damage, and Aqua Ring with Big Root lets it outlast slow chip damage. Sophie's Lurantis is slow and bulky, removes held items with Knock Off and heals with Synthesis. Emily's Cinccino is the fastest of the eight (121 Speed), and Skill Link lands all five hits of Tail Slap and Rock Blast and all three of Triple Axel, which beats Substitute and Focus Sash. Tickle softens whatever would wall it. Elena's Torkoal is the cook's kettle: it is the slowest of the eight (32 Speed), so the player always moves first, and its sun Eruption punishes anything that cannot knock it out quickly. Yawn can put the next Pokemon to sleep inside the fight. Clare is the head maid. Klefki keeps the keys, paralysing and setting Reflect with Prankster priority, and Gothitelle behind it sets up Calm Mind under that screen. Tanga Berry covers its four-times weakness to Bug. Celeste closes the chain. Milotic's Haze wipes the boosts a player built up through the maids, and Clefable's Unaware ignores any boost the player makes afterwards, with Moonlight to outlast a tired team.

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
| Milotic | 42 | 143 | 84 | 60 | 100 |
| Clefable | 42 | 143 | 71 | 67 | 96 |

## The changes, by file

`res/field/scripts/scripts_pokemon_mansion.s` loses the random turn target, the turn count and Liam. Celeste's trainer flag is now set only when she is beaten, so it means "cleared today", and the day's reset (the old turn-target daily flag, kept under its vanilla name) clears it. The prize is given from one routine, which is reached straight after the win and again from the maid when a full Bag refused it. `res/text/pokemon_mansion.json` loses the turn and Liam lines and gains three: Celeste's gift, her leaving, and the maid's kept-gift line.

Pastoria's ball was the last object event on its map, and visible item entry 473 was the last entry in `scripts_visible_items.s`, so both came out without moving any other object id or script number.

The reward table's row for the Capsule (`reward-placements.tsv` and the `ADDED` list in `balance/rewards.py`) is now a gift on the mansion's map header. It names the Capsule as the item it replaces, which is how `place_rewards.py` checks a hand-scripted gift. The divergences are registered where the bulk tools keep them: `scripts_pokemon_mansion` in `bulk_scripts.py`, text bank 490 in `import_base_rom.TEXT_BANKS_SKIPPED`, and the Pastoria entry in `bulk_events.py` extended. The base ROM never changed the mansion's script or text, so the dry runs would skip them anyway; the entries record why they differ from vanilla.

Three small edge cases follow from reusing the flag and from the trainer flag's new meaning:

- A save that picked up Pastoria's ball already has the flag set, so its mansion clear gives no second Capsule. The game still has exactly one.
- The reward tool's spare-flag count reads 46 of 85, one under the truth, because it counts reward trainers and new balls but not hand-scripted gifts. `SpareFlags` still treats the flag as taken, since it scans the tree for every flag name.
- A save that started vanilla's challenge earlier the same day has Celeste's trainer flag set already, so the maid would hand over the Capsule that day without the fight. Only a save from before this change can meet this, and only until the next day.

## What was checked

`make rom` builds the branch. The built mansion script decodes fully, and `scriptdis --verify` finds no movement block colliding with code. `place_rewards.py check` finds every one of the table's 168 rows exactly once with no problems, and `apply --dry-run` would write 0 files. `rewards check` has 0 failures. `checkmap.py` shows the mansion's events byte-identical to the base ROM and its script changed, as intended. On Pastoria it reports only the registered differences: the hidden Abra and the Scorbunny check, with the ball now gone too. Every team was saved through `trainers.save`, which runs the trainer lint and the real packer, and every move is on its species' Oxide list at its level (`learnsets.oxide_list`). The script index is regenerated. The gate's result is in the branch's last commit.

Not checked: no in-game look, no scorer reading (Ian has named no fight), and no AI-picks probe. The simulator reads one fight at a time, so it cannot model a chain where HP and status carry over.
