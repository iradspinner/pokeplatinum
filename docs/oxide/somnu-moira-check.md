# Somnu and Moira 2: a check of Ian's first draft

Ian drafted the Lake Verity double against Officers Somnu and Moira in his OxiDex on 2026-11-02. They are named Galactic officers, so mini-bosses, fought together in one double at Lake Verity in Candice's split (cap 56), just before Mars 2, with their aces at 52 as Ian ruled on 2026-11-01 (`candice-split.md`). Both see the player from opposite ends of one row, so the player always meets them together. Somnu's theme is sleep, Moira's Future Sight with Ice and hail, and the pair's is sleep beside Future Sight and hail (`boss-shapes.md`). This is the check Mars 2's and Hesperid's drafts had: anything in the engine, the simulator or the AI that invalidates the fight, the rules, each member's job, and how the pair reads beside Mars 2. The draft is saved on branch `overseer-somnu-moira-check` as it stands; the only other change to the game's data is the egg-list commit below. No scorer reading was run, and the simulator was not touched.

## Summary

**What could not be checked, first.** No reading can read a double battle, and the probe of the earlier checks plays single battles only. Every number below comes from two stand-ins, the doubles proxy of the Darach check and a single-battle proxy, and neither has ever been checked against a scorer reading of a double. Mars 2 is a single battle in the game, so the doubles comparison plays her six as if her fight were a double. Nothing was seen in game.

**Outcome.** Nothing breaks the fight. Every move, item and ability does in Oxide's engine what the draft means, in a double, and the simulator models each the same way. Dream Eater was only ever aimed at a sleeping target. Destiny Bond took a foe down with Swalot in 22 to 56 fights of 300 a box. Mr. Rime's Future Sight landed its delayed hit on whichever Pokemon stood in the slot. Snow Warning's hail never ended, so Blizzard never missed, and Snow Cloak made 20 to 22 percent of the player's moves at Glaceon miss. Gardevoir's Magic Guard spares it both the Life Orb's recoil and the hail. Three moves were on no list at their levels, and each is now on its line's first stage's egg list. Every rule holds: six Pokemon between the two, no item or nature repeated within either trainer, and both aces at 52 with the rest at 51.

One slip, in two places: Stantler and Mr. Rime are Adamant, which raises Attack and lowers Sp. Atk, on sets that are all special (Stantler) or three special attacks of four (Mr. Rime). In Oxide, Hyper Beam is special. Decisions 1 and 2 ask about each.

**Against Mars 2.** On the doubles proxy the pair reads clearly easier than Mars 2's six played as a double on boxes 2 and 3, and about the same on box 1. It reads harder than the pair's old teams on every box. With both natures fixed it reads harder than the draft on two boxes of three, and still easier than Mars 2 on average. Played one at a time as a single battle, it reads level with Mars 2. So the pair does not read harder than its commander, as drafted or with the fix.

**What Ian decides.**

1. Stantler's nature: Mild, which raises the Sp. Atk all three of its attacks use and repeats no nature in the six (my pick); or keep Adamant.
2. Mr. Rime's nature: Rash, which raises Sp. Atk for Focus Blast, Icy Wind and Future Sight and leaves Stomping Tantrum's Attack neutral, the Assault Vest covering the Sp. Def it lowers (my pick); or keep Adamant, if Stomping Tantrum is meant as its main hit.

**Next steps.**

| Step | Who | Time |
|---|---|---|
| Answer the two questions, a line each | Ian | five minutes |
| Apply the answers on this branch, rerun legality, the lint, the tests and the proxies | a session | about 45 minutes |
| See the fight in game: the pair meets the player together, hail on from the first turn | Ian, in his playtest | a few minutes |

## Each member's job

Each count is over 300 rough doubles a box, the stand-in playing every lead pair of the matchup screen's best six 20 times. A knockout is counted for both of the pair's Pokemon on the field, so the counts overlap.

| Member | Its job | Does it | Player's Pokemon knocked out while it stood, boxes 1, 2, 3 |
|---|---|---|---|
| Swalot 51 (Somnu) | Lead with Yawn, eat sleepers, and take one foe with it by Destiny Bond | Yes. Yawn is its pick 652 to 946 times a box, Dream Eater goes only at sleepers, and Destiny Bond takes a foe in 22 to 56 fights | 355, 277, 358 |
| Stantler 51 (Somnu) | Intimidate the box's physical attackers, sleep a foe with Hypnosis, hit hard with Hyper Beam | Yes, though Adamant weakens every hit (decision 1). Hypnosis 361 to 501 a box, Hyper Beam 123 to 331 | 468, 453, 327 |
| Gardevoir 52 (Somnu) | The special attacker: Life Orb with no recoil, coverage for the Steel types | Yes. Focus Blast leads its picks, into the box's Steel core | 525, 412, 261 |
| Abomasnow 51 (Moira) | Set hail on entry for the whole fight | Yes, in every fight: Snow Warning's hail lasts until another weather replaces it, and the player has none. It rarely lives past its first turn (45 to 115 turn ends on the field a box), so its own hits are few | 127, 44, 2 |
| Mr. Rime 51 (Moira) | Future Sight beside Icy Wind's speed control, healing by Ice Body in the hail | Yes, though Adamant weakens three of its four attacks (decision 2). Future Sight is set 31 to 95 times a box | 206, 179, 138 |
| Glaceon 52 (Moira) | The hail sweeper: sure-hit Blizzard, Calm Mind, Protect, Snow Cloak | Yes, and it is the fight's core. It stays longest and makes the most knockouts | 1015, 919, 806 |

Abomasnow's low count is the Sudowoodo case of Hesperid's check: it is judged by its job, which is done the moment it is sent out, and by Ian's ruling of 2026-11-01 a member is not judged by its knockouts alone.

## How the pair reads beside Mars 2

Each cell is the stand-in's wins of 300 rough doubles, every lead pair of the screen's best six played 20 times; fewer wins means a harder fight. The boxes are goal 3's at Mars 2, seeds 1 to 3, at level 54. The stand-in picks the attack worth the most or a major status, never switches and never sets up, so only the comparisons between rows mean anything.

| Fight, as a double | Box 1 | Box 2 | Box 3 | Average | Best lead pair's wins of 20, by box |
|---|---|---|---|---|---|
| Somnu and Moira, Ian's draft | 173 | 238 | 249 | 220 | 18, 19, 19 |
| The draft with Stantler Mild and Mr. Rime Rash | 143 | 253 | 203 | 200 | 14, 20, 19 |
| Their old teams, before the draft | 237 | 277 | 264 | 259 | 19, 20, 20 |
| Mars 2's six, played as if her fight were a double | 182 | 128 | 154 | 155 | 18, 16, 17 |

The single-battle proxy plays the pair's six one at a time, Somnu's three and then Moira's, on Somnu's flags, with no partner, no spread and no Tag Strategy, against the greedy player of the earlier checks (150 fights against the screen's best six, no items, never switching or setting up). Mars 2 is her own single battle on the same boxes.

| Fight, as one single battle | Box 1 | Box 2 | Box 3 | Average |
|---|---|---|---|---|
| Somnu and Moira, Ian's draft | 86 | 98 | 124 | 103 |
| The draft with Stantler Mild and Mr. Rime Rash | 78 | 129 | 87 | 98 |
| Their old teams | 51 | 58 | 54 | 54 |
| Mars 2, her real fight | 107 | 97 | 87 | 97 |

One at a time the draft reads level with Mars 2, inside the probe's blur of about 35 wins, and the old teams read far harder. The two proxies disagree about the old teams because the old six was built for singles: two of its members carried Earthquake, which in a double hits their own partner, and its Skuntank and Mamoswine hit hard one-on-one. The draft is built for the double, with partner-safe spread moves and the hail, so the doubles proxy, which keeps those, is the better guide to it.

How far to trust this. The doubles proxy is the Darach check's, and has never been held against a reading, since no reading reads a double. Its stand-in never switches, so a Yawn always lands and a sleeping Pokemon always stays in, which makes a sleep team read harder than a player who switches finds it. It never plays round Snow Cloak or Future Sight either. The simulator's double battle has the gaps the simulator gaps doc lists for doubles (no Lightning Rod or Storm Drain draw, a spread move's three quarters judged once for the whole move, no switching by choice). Mars 2 played as a double is a yardstick only, not her real fight. On the singles probe a gap under about 35 wins of 150 has not ordered two fights reliably (`probe-ranking.md`); nothing that strong is known for the doubles proxy, so I read only the larger gaps. Box 1's gap of 9 says the two are level there, and boxes 2 and 3's gaps of 110 and 95 say the pair is easier. The screen's best score (19.55 to 20.05 for the pair, 16.80 to 17.25 for Mars 2; higher is easier) points the same way, though it sees no partner, no spread move and no hail.

The nature fix moves the proxy by 30 and 46 wins harder on boxes 1 and 3 and 15 easier on box 2, where the screen picked a different six. Mr. Rime's knockouts rise on box 1, from 206 to 343. Either way the pair stays easier than Mars 2 on average.

## Part 1: what could invalidate the fight

### The rules

| Trainer | Member | Level | Item | Nature | Ability (slot) |
|---|---|---|---|---|---|
| Somnu | Swalot | 51 | Sitrus Berry | Calm | Gluttony (1) |
| Somnu | Stantler | 51 | Shell Bell | Adamant | Intimidate (1) |
| Somnu | Gardevoir (ace) | 52 | Life Orb | Modest | Magic Guard (1) |
| Moira | Abomasnow | 51 | Occa Berry | Quiet | Snow Warning (3, hidden) |
| Moira | Mr. Rime | 51 | Assault Vest | Adamant | Ice Body (3, hidden) |
| Moira | Glaceon (ace) | 52 | NeverMeltIce | Modest | Snow Cloak (1) |

The two field six between them. No item repeats in the six, and no nature repeats within either trainer; across the two, Adamant and Modest each appear twice, as Skuntank and Mamoswine, and Glaceon and Gardevoir, did on the old teams. Both aces are at 52 and the other four at 51, under Candice's 56 and under Mars 2's ace of 54. The named Galactic fights are mostly anything goes, and nothing here is a one-hit KO move or a trap. Destiny Bond is a trade the player plays round with status or by not striking the last blow. Snow Cloak is an evasion ability, which the trainer rules keep rare for ordinary trainers; the named Galactic fights are freer, and it is the core of Moira's hail theme.

Oxide's Swalot has Gluttony in all three slots, and Gluttony does nothing for a Sitrus Berry, which already fires at half HP. So Swalot's ability is idle, and no other is available to it; the Sitrus Berry is still the right item.

Three moves were on no list at their levels, by the OxiDex's reading:

| Member | Move | Where it was | Now |
|---|---|---|---|
| Stantler 51 | Dream Eater | a TM in Generation 4 only; Stantler's TM before the TM pass, so the Kaizo checker passed it | Stantler's own egg list, a first stage |
| Abomasnow 51 | Earth Power | a TM in the latest game only; no Oxide list for the line | Snover's egg list |
| Glaceon 52 | Protect | a TM before the TM pass, so the Kaizo checker passed it | Eevee's egg list |

Both checkers then find nothing: the OxiDex's lists give all 24 moves at their levels, and the Kaizo checker (with the pre-TM-pass TMs, at 56) finds 0 problems. The trainer lint finds nothing on either file.

### The engine and the simulator, in a double

Each piece was read in the engine and the battle scripts, and in the simulator.

- Tag Strategy. In any double the engine adds Tag Strategy to every trainer's flags, so the flag in both files changes nothing. Each officer's AI reads her own flags for her own slot. Nothing in either six hits its partner: Blizzard and Icy Wind hit both foes only, and the draft's Earth Power, single-target, replaces the old Abomasnow's Earthquake, which hit its partner.
- The spread moves. Blizzard (110 power, 70 percent) and Icy Wind (55, lowering Speed) hit both of the player's Pokemon at three quarters each. In hail Blizzard skips its accuracy check entirely, in the engine and the simulator alike, and the hail never ends here, so both Blizzards are sure hits, each with a 10 percent freeze on each target.
- Dream Eater. It fails on a target that is awake, and the AI's Basic routine marks it down by 8 against one, while Expert lifts it by 3, four times in five, against a sleeper it does not resist. In a double the AI scores it against each foe and takes the best, so it went to a sleeping target in every one of 65 to 178 picks a box. Hypnosis landed 58 to 61 percent of the time, Generation 4's 60.
- Future Sight. Oxide keeps Generation 4's version: 120 power, the damage worked out as it is used, from Mr. Rime's Sp. Atk and the target's Sp. Def, with no type chart and no critical hit, and kept on the target's slot. Two turn ends later it lands on whatever stands in that slot, so a switch does not dodge it, and it hits Dark types. The AI marks it down by 12 while one already waits on that side, so Mr. Rime keeps one going at a time. It was set 31 to 95 times a box. Adamant lowers the Sp. Atk its damage is worked out from.
- Destiny Bond with Check HP. Expert gives Destiny Bond nothing when its user is slower than the target, and in a double that is judged against each foe in turn, so Swalot (Speed 76) bonds mostly against the box's slow walls. It picked it 69 to 93 times a box, almost always at 70 percent HP or less, and it took a foe in 22, 56 and 27 fights of 300. Check HP marks Destiny Bond down only above 70 percent, and then matters only beside Risky, which Somnu does not carry, so it changes nothing here; it does keep Hypnosis off a target at 30 percent or less, and Calm Mind off Glaceon below 70 percent if Moira carried it.
- Snow Warning, Snow Cloak and Ice Body. Snow Warning sets Generation 4's lasting hail, which stays until another weather replaces it, so once Abomasnow leads the hail holds every turn of the fight. The probe found it up at every turn end of every fight. Snow Cloak cuts the accuracy of every move aimed at Glaceon by a fifth in hail: 20 to 22 percent of the player's accuracy checks on it missed, against 1 to 3 percent for the old team's Glaceon. Ice Body heals Mr. Rime a sixteenth in hail in place of the hail's bite. The hail also bites Somnu's Swalot and Stantler a sixteenth a turn, since neither is an Ice type; Gardevoir is spared by Magic Guard.
- Magic Guard with a Life Orb. The engine skips the Life Orb's tenth of HP for a Magic Guard holder, and the simulator does the same, so Gardevoir has the 1.3 times power free. Magic Guard also spares it the hail.
- The rest. Hyper Beam is Oxide's rework, 180 power, special, no recharge turn, half the damage as recoil, which the Shell Bell partly repays. Freeze-Dry is super effective on Water in the engine and the calculator. The Occa Berry halves one Fire hit on Abomasnow, which takes Fire four times over. The Assault Vest bars status moves, and Mr. Rime has none.

### The AI flags

Somnu has Basic, Evaluate Attack, Expert, Tag Strategy, Check HP and Harassment; Moira has Basic, Evaluate Attack, Expert and Tag Strategy. By the guide (`battle-ai/flags-guide.md`):

- Harassment fits Somnu. Her idea is sleep, and she carries three moves from its table: Swalot's Yawn and the Hypnosis of Stantler and Gardevoir. It lifts each half the time, and Yawn is Swalot's first pick in most fights.
- Check HP fits Somnu by the guide's rule for a team with Destiny Bond, though here it changes Destiny Bond itself not at all (above).
- The Weather flag is rightly off Moira. It acts only for a weather move used on the battle's first turn, and Moira's hail comes from Snow Warning, which needs no flag.
- Moira needs no Check HP or Harassment: she has no trade move and no move from Harassment's table.

## The egg-list commit

The second commit on this branch puts Dream Eater on Stantler's egg list and Earth Power on Snover's, each under that species' one entry in `learnrewrite.IAN_EGG_MOVES`, by Ian's ruling of 2026-10-29. Eevee is a held-out line the generator may not name, so its Protect is in the species data and in `learnsets_by_hand.txt`, as Dahlia's Baton Pass and Substitute were. No level-up entry moved, and the player never reaches an egg list. The draft itself is the first commit, saved through `trainers.save` and equal to both snapshots.

## How the numbers were made

Every number comes from the worktree `.claude/worktrees/somnu-moira-check` on this branch. The scripts are in `/home/ian/.claude/jobs/382760ce/tmp/somnu-moira/`, and none writes to `res/`. `sm.py` is the harness: since goal 3 refuses a double, it builds the states from the simulator's own preparation with goal 3's box at Mars 2 (run `somnu-moira-check-study`, seeds 1 to 3) as the player's side, a tag battle with each officer in her own slot on her own flags, as the doubles helper builds a tag fight. `VARIANT=old` reads the pair's files from `origin/oxide` before the draft, and `CAND=natures` swaps Stantler to Mild and Mr. Rime to Rash, both in memory. `dfights.py` plays the simulator's double battle with the trainer side on the AI's doubles chooser and the player on the stand-in, over every lead pair of the screen's best six, and counts every pick with its target, Dream Eater's target's status, Destiny Bond by HP and by Speed, Future Sight set, the player's accuracy checks on Glaceon, the trainers' Hypnosis, the weather at each turn end, and the knockouts while each member stood. `compare.py` is the single-battle proxy. `runall.sh` and `runc.sh` ran the jobs under `tools/oxide/capped`. Legality comes from the OxiDex's `learnsets.lists` and the Kaizo checker (`oxide.py check`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`). The trainer lint finds nothing, the real packer packs both files, test_b1 passes 50 of 50, test_learnrewrite 6 of 6, test_learncheck 18 of 18 and test_trainers 44 of 44, and `make rom` builds. `integrate.sh --verify-only` passes 53 checks at 35f74940d86, with sync-docs failing off `oxide` by design.
