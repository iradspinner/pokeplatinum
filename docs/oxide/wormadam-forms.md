# Wormadam's Sandy and Trash cloaks: draft learnsets

Drafts for Ian (2026-10-14), on the branch `overseer-form-learnsets`. Nothing in
the game changes until he says yes, so for now the two cloak records still carry
vanilla's lists.

## Summary

Both cloaks get their own level-up and TM lists, built the way the learnset
rewrite built Plant's. Their tutor lists stay as they are. I ran the rewrite's
own generator with each cloak in Plant's place, as the stage a female Burmy
becomes at 20. I then read Sandy's result as a player and made one change:
Earthquake at 53. Every rewrite check passes on both drafts except the
late-game move count, which falls short from 67 on. Plant's falls short from
75 on, and the tracker already holds that shortfall for after the alpha.

Ian decides three things:

1. Whether the two lists below are right, or what to change in them.
2. Sandy's Earthquake at 53, my one change. He can keep it, move it to 47
   (Fissure's old level), or drop it. Dropping it leaves Bulldoze as Sandy's
   only Ground attack all game.
3. Trash's Quiver Dance at 36, which the generator picked. Mothim also learns
   it at 36, and Plant at 69.

Once he says yes, writing the two files, rebuilding and running the checks
takes about half an hour. The landing commit says "Difficulty: not material",
because no reading's box holds a cloak.

In the table, a plain entry is one of vanilla's that stays. "New" is one the
generator added, and "mine" is my change. A struck entry leaves the list.

| Level | Plant (today) | Sandy draft | Trash draft | Why |
|---|---|---|---|---|
| 1 | Tackle | Tackle | Tackle | |
| 10 | | ~~Protect~~ | ~~Protect~~ | Protect leaves every player list (Ian, R24) |
| 15 | Bug Bite | Bug Bite | Bug Bite | |
| 20 | Hidden Power | Hidden Power | Hidden Power | |
| 21 | | Bulldoze (new) | | a Ground attack within a split of evolving (R11), and a move from after Generation 4 (R16) |
| 23 | Confusion | Confusion | Confusion | |
| 26 | Razor Leaf | Rock Blast | Mirror Shot | each cloak's own vanilla move |
| 28 | Dig | | | |
| 29 | | Harden | Metal Sound | each cloak's own vanilla move |
| 32 | Psybeam | Psybeam | Psybeam | |
| 35 | Captivate | Captivate | Captivate | |
| 36 | Swagger | | Quiver Dance (new) | a good utility move, two over the game for an attacker under 85 (R7), and a newer move (R16) |
| 37 | Pollen Puff | | | |
| 38 | Flail | Flail | Flail | |
| 40 | Growth | | | |
| 41 | Attract | Attract | Attract | |
| 44 | Psychic | Psychic | Psychic | |
| 46 | | Sucker Punch (new) | | a third coverage type (R5) |
| 47 | Leaf Storm | ~~Fissure~~ | Iron Head | Fissure is a one-hit KO move, which leaves every list (Ian) |
| 51 | Iron Head | Skitter Smack (new) | Sucker Punch (new) | Sandy: two new moves per eight levels (R2); Trash: coverage (R5) |
| 53 | Leech Life | Earthquake (mine) | Bug Buzz (new) | Sandy: a strong Ground attack, as Plant has Leaf Storm and Trash has Iron Head; Trash: R2 |
| 59 | Sucker Punch | Leech Life (new) | Shadow Ball (new) | Sandy: a strong same-type attack on the final form (R30); Trash: coverage (R5) |
| 61 | Giga Drain | Zen Headbutt (new) | Leech Life (new) | Sandy: Psychic coverage on its Attack (R5); Trash: R2; both: the late move |
| 67 | Lunge | Lunge (new) | Giga Drain (new) | Sandy: R2; Trash: coverage (R5) |
| 69 | Quiver Dance | | | |

The splits, for reading the levels: Gardenia's runs to 26, Fantina's to 33,
Maylene's to 39, Wake's to 44, Byron's to 53, Candice's to 56, HQ's to 60, the
Galactic split to 65, Volkner's to 68 and Barry's to 71. Entries under 20, the
evolution level, are the relearner's menu. A cloak already learned them as
Burmy.

The TM pass's own rule gives both cloaks 18 of Plant's 21 TMs. They lose
Plant's Bullet Seed, Energy Ball and Grass Knot. Sandy gains Earthquake, Rock
Tomb and Stealth Rock. Trash gains Iron Defense, Gyro Ball, Stealth Rock and
Flash Cannon. Each cloak keeps its own vanilla tutor list, as every species in
Oxide still does.

These are the rules the drafts were checked against, one at a time:

| Rule | How the drafts meet it |
|---|---|
| What a move is worth at capture | Neither cloak is met wild, because a wild Wormadam is always Plant. A cloak comes from a female Burmy that reaches 20 in a battle in the right place. A cave, sand, a mountain or plain ground gives Sandy; a building or a bridge gives Trash. Both are open by Gardenia's split. The cloak arrives knowing four of Burmy's Roost, Confusion, Tackle, Bug Bite and Hidden Power. Its first new move comes at 21 (Sandy's Bulldoze) or 26 (Trash's Mirror Shot). |
| The type's ladder by split | Sandy's Ground moves are Bulldoze (60) at 21, then Earthquake (100) at 53. Trash's Steel moves are Mirror Shot (80 in Oxide) at 26, then Iron Head (80) at 47. Each added attack is within the generator's ceiling for its split: 75 in Gardenia's, and 100 up to Candice's. |
| Power flags | Neither cloak is flagged. Attack is 79 and 69, Special Attack 59 and 69, and Speed 36. |
| No Protect, Double Team or one-hit KO move | Protect leaves both cloaks and Fissure leaves Sandy. The TM list no longer teaches any of these moves. |
| A real move at 61 or later | Sandy learns Zen Headbutt at 61 and Lunge at 67. Trash learns Leech Life at 61 and Giga Drain at 67. |
| Setup at its PP | Quiver Dance has 1 PP and Harden 3. Metal Sound and Captivate, which lower a stat, have 3. |
| The TM pass's rules | A TM goes to a cloak when it teaches a move the cloak's lists before the pass taught it, by machine or tutor, or a move a later game teaches it. Run as written, the same rule gives Plant exactly the TM list Plant has today. |
| Branches close in worth where the player chooses (check 24) | At Gardenia's cap, Wormadam's best four moves score 295 as Sandy, 300 as Trash and 262.5 as Plant, against Mothim's 240. All pass the 80% bar. |
| The rewrite's other checks | Checks 1, 4, 7 and 9 to 23 pass on both drafts. Check 8 falls short only from 67 on, where Plant's falls short from 75. |
| Kaizo, translated twice | Kaizo's own cloak lists are vanilla's, except Head Smash at 47 on Sandy and Earthquake at 45 in Kaizo's calculator. The generator reads them as links only and takes its moves from Oxide's whole pool, newer moves included. Earthquake comes at 53, later than Kaizo's 45, and Head Smash stays out, since it is 80% accurate and the player's attacks are held to 90%. |
| Trainers that carry a cloak | Worker Jackson's Trash Wormadam (level 49) keeps a legal set. Gyro Ball is TM74, Bug Bite comes at 15, Sucker Punch at 51 and by tutor, and Stealth Rock is TM76. |

## Detail

### How the drafts were made

The rewrite's generator (`tools/oxide/balance/learnrewrite.py`) and its checks
walk species, and the cloaks are form records, so neither ever saw them. That
is why the cloaks kept vanilla's lists after the rewrite and the TM pass. To
see what the rewrite would have built, I ran the generator in memory, with
nothing written, and pointed four of its reads at the cloak in place of Plant:

1. Wormadam's record: types, stats, abilities, and its lists before and after
   the rewrite.
2. Its later-game lists, under the form's own Showdown name.
3. Its Kaizo list, from Kaizo's own cloak row (499 for Sandy, 500 for Trash).
4. Its catches. A wild Wormadam is always Plant, because the engine changes a
   Burmy's cloak after a battle (BattleSystem_SetBurmyForm) but never a
   Wormadam's. So I dropped Wormadam's wild rows (Route 215 at 20 and 21,
   Victory Road at 49 and 50), leaving the cloak reached only by evolving
   Burmy.

Burmy's list came out of both runs exactly as it is today, so the drafts work
with the Burmy every player has. Mothim's list came out a little differently in
each run, because the generator plans a line's branches together. Mothim's real
list stays as it is. The drafts were then checked against the real Mothim,
which is what check 24 above compares.

The checks were run on each final draft the same way: in memory, with the cloak
in Plant's place and the draft as its list.

### Each move the generator added, with its rule and score

| Cloak | Level | Move | Rule | Generator's score |
|---|---|---|---|---|
| Sandy | 21 | Bulldoze | R11, R16 | 239 |
| Sandy | 46 | Sucker Punch | R5 | 58 |
| Sandy | 51 | Skitter Smack | R2 | 22 |
| Sandy | 59 | Leech Life | R30 | 164 |
| Sandy | 61 | Zen Headbutt | R5 | 32 |
| Sandy | 67 | Lunge | R2 | 25 |
| Trash | 36 | Quiver Dance | R7, R16 | 203 |
| Trash | 51 | Sucker Punch | R5 | 102 |
| Trash | 53 | Bug Buzz | R2 | 79 |
| Trash | 59 | Shadow Ball | R5 | 87 |
| Trash | 61 | Leech Life | R2 | 64 |
| Trash | 67 | Giga Drain | R5 | 48 |

The generator removed Protect from both cloaks and Fissure from Sandy (R24, and
the one-hit KO ruling). It kept every other vanilla entry where it was, as the
rewrite does with Oxide's own entries.

### Why Sandy gets Earthquake

Read as a player, the generator's Sandy has one Ground attack in its whole
level-up list, Bulldoze at 21. The rules ask only for a same-type attack of 50
within a split of evolving, which Bulldoze meets, and for a strong same-type
attack on the final form, which Leech Life meets as a Bug move. So the
generator had no reason to climb Sandy's Ground ladder. Plant gets Leaf Storm at
47 and Trash keeps Iron Head at 47, each a strong attack of its second type.
Sandy's own move at 47 in vanilla was Fissure, which leaves the game's lists.

I chose Earthquake because it is linked to Sandy twice: the later games teach it
to Sandy by TM, and Kaizo gives it at 45. At 100 power it is within the
generator's ceiling for Byron's split. I placed it at 53, Byron's cap, rather
than at Fissure's 47. At 53 it fills the band from 51 to 58, where the
generator's list had only Skitter Smack and so fell short of R2's two new moves
for eight levels held. It also climbs from Bulldoze (60) at 21 through four
splits, about a rung a split.

Sandy learning it by level-up also leaves TM26 for another Pokemon. The
reward table places one copy of that TM, in Byron's split.

Sandy's middle is thin for a physical attacker. From 26 to 46 it learns Harden,
Psybeam, Captivate, Flail, Attract and Psychic, and its Special Attack (59) is
low for the two Psychic moves. Those are vanilla's own entries, which the
rewrite keeps. If Ian wants that stretch stronger, the next rung of the Ground
ladder fits it: Stomping Tantrum (75) somewhere from Maylene's split to Wake's.
I have not put it in the draft.

### Trash's Quiver Dance

The generator added Quiver Dance at 36 as Trash's second good utility move.
R7 asks for two over the game when the better attacking stat is under 85, and
Trash's is 69; Burmy's Roost is the first. The later games give Wormadam this
move on evolving, and it has 1 PP in Oxide. With 36 base Speed, one use still
leaves Trash slow, so its value is as a bulky special attacker. Its special
moves are Mirror Shot from 26, Psybeam from 32, Psychic at 44, Bug Buzz at 53,
Shadow Ball at 59 and Giga Drain at 67. Mothim learns Quiver Dance at 36 too.

### The TM lists in full

The TM pass's rule (`tmcompat.new_by_tm` over `rewards.compat`) was applied to
each cloak's record as it stood before the pass. It reads that record's TMs
through the TM records of that time, adds its tutor moves, and adds what the
later games teach the cloak by TM, tutor or level-up. On Plant the same rule
reproduces today's list exactly. The cloaks' lists today still use the numbers
from before the pass, and those numbers now teach other moves: Sandy's TM17
was Protect.

| TM | Move | Plant | Sandy | Trash |
|---|---|---|---|---|
| TM06 | Toxic | yes | yes | yes |
| TM09 | Bullet Seed | yes | | |
| TM10 | Hidden Power | yes | yes | yes |
| TM15 | Hyper Beam | yes | yes | yes |
| TM19 | Giga Drain | yes | yes | yes |
| TM20 | Safeguard | yes | yes | yes |
| TM21 | Frustration | yes | yes | yes |
| TM22 | Solar Beam | yes | yes | yes |
| TM26 | Earthquake | | yes | |
| TM27 | Return | yes | yes | yes |
| TM28 | Dig | yes | yes | yes |
| TM29 | Psychic | yes | yes | yes |
| TM30 | Shadow Ball | yes | yes | yes |
| TM37 | Signal Beam | yes | yes | yes |
| TM39 | Rock Tomb | | yes | |
| TM42 | Facade | yes | yes | yes |
| TM43 | Secret Power | yes | yes | yes |
| TM48 | Iron Defense | | | yes |
| TM53 | Energy Ball | yes | | |
| TM68 | Giga Impact | yes | yes | yes |
| TM74 | Gyro Ball | | | yes |
| TM76 | Stealth Rock | | yes | yes |
| TM78 | Captivate | yes | yes | yes |
| TM86 | Grass Knot | yes | | |
| TM87 | Swagger | yes | yes | yes |
| TM91 | Flash Cannon | | | yes |
| TM94 | Psybeam | yes | yes | yes |

The cloaks' Giga Drain and Solar Beam come from the later games, which teach
both cloaks those TMs.

### The tutor lists

No species' tutor list in Oxide differs from vanilla's (all 496 vanilla species
match), so the cloaks keep theirs.

| Plant | Sandy | Trash |
|---|---|---|
| Snore, Endeavor, Synthesis, Signal Beam, Seed Bomb, Sucker Punch, Uproar | Mud-Slap, Rollout, Snore, Endeavor, Signal Beam, Earth Power, Sucker Punch, Uproar | Iron Head, Snore, Endeavor, Signal Beam, Gunk Shot, Iron Defense, Magnet Rise, Sucker Punch, Uproar |

### Outside these drafts

Plant's record carries the base ROM's stats, Attack 79 against vanilla's 59,
as Kaizo has it. The two cloak records keep vanilla's stats (Sandy
60/79/105/59/85/36, Trash 60/69/95/69/95/36) and their abilities, Anticipation
and Overcoat. These drafts leave the stats alone.

The eleven other form records now mirror their base forms, with the moves Sky
Shaymin and the Deoxys forms kept on Ian's word. Those changes are the two
commits before this doc on the same branch. Their background is in
[move-access.md](move-access.md), and the rewrite's rules are in
[learnset-rewrite.md](learnset-rewrite.md).
