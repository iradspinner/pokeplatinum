# Dahlia's six: a short check

Ian built a first draft of Dahlia, the Arcade Star, on 2026-10-31: an optional boss in Maylene's split whose fight opens in a permanent Wonder Room. He asked for two things only: anything that invalidates the fight, and the weakest crux with the top replacement picks for it. Her natures and her level of 40 are his choice and are not argued here. The six is in a spare slot (`dummy_007`) on branch `overseer-dahlia`, for study only. Her trainer is not yet on the engine's list of permanent Wonder Room fights, so every number below comes from a harness that holds the room on in memory.

## Summary

**Outcome.** Nothing breaks the fight. Every ability, item and move does what Ian meant, in the engine and in the simulator, and the permanent room swaps the stats as the later games do. Seven moves on four members were on no list at 40, and each is now on its line's first stage's egg list, by his ruling of 2026-10-29 (Part 1). Her difficulty matches his intent on five of six boxes. On Maylene's boxes she is far harder than Maylene herself. On Wake's boxes 2 and 3 she is about as hard as Wake, by the probe's rough fights. Wake's box 1 is the exception, where the probe's player beats her two times in three. The Baton Pass AI sets up on turn 1 and passes late and hurt. The receiver is whoever's types best fit the player's Pokemon in front, which turns out to be Lopunny M most often, a good outcome. The boxes' only answers to a pass are Taunt and Substitute breakers, and nearly every top six carries one.

**The weakest crux is Cloyster's slot.** Cloyster knocks out the fewest of the player's Pokemon in every run (38 to 82 per 150 fights, against 127 to 363 for Lopunny M). Its turn 1 goes on Toxic Spikes 85 percent of the time, and a little under half the switch-ins onto the spikes are poisoned. Under the room its Relaxed Defense guards against special moves while the boxes hit physically. Its King's Rock needs it to move first, which at Speed 65 it does only against the walls. It passes Ian's lead test: every common answer but one (Hariyama, on Wake's box 3) draws in a member that beats it, half of them one with Calm Mind or Swords Dance.

**What Ian decides.**

1. Cloyster's slot: my first pick is his Cloyster with Shell Smash for Toxic Spikes; my second is Omastar with Shell Smash and a White Herb. Or keep his set. The sets and their numbers are in Part 3.
2. Once she is placed, may the simulator gain the permanent Wonder Room, as it has the permanent Trick Room, so that a reading of her fight needs no harness? That changes the simulator, which needs his approval.

**Next steps.** Ian answers in a line each. A session then applies the chosen set on this branch, with Shell Smash on Shellder's egg list if he takes pick 1, and reruns the legality check and the probe below, which takes about an hour. The simulator's permanent room, if approved, is about an hour more with its test. Her placement (the Game Corner gate script and her entry on the engine's list) is the later job in the tracker's Frontier Brains entry. A spot-check reading happens only if Ian names one, and takes two and a half to four hours.

## Part 1: what could invalidate the fight

### Legality

Seven moves on four members were on no Oxide list at 40. Each now sits on the egg list of its line's first stage, by Ian's ruling of 2026-10-29, in commit 1efa311e001 on this branch. No level-up entry moved.

| Member | Move | Where Oxide had it | Egg list it went on |
|---|---|---|---|
| Slowbro | Psyshock | nowhere | Slowpoke |
| Rapidash | Flare Blitz | Rapidash's level 56 | Ponyta |
| Rapidash | Swords Dance | nowhere | Ponyta |
| Rapidash | Baton Pass | nowhere | Ponyta |
| Leafeon | Baton Pass | nowhere | Eevee |
| Leafeon | Substitute | a TM before the TM pass, so the Kaizo checker allows it; the OxiDex reads only today's TMs | Eevee |
| Lopunny M | High Jump Kick | Lopunny M's level 60 | Buneary, and Lopunny M's own |

High Jump Kick is on two lists because the OxiDex gives Lopunny M no earlier stage: its rule for earlier stages skips a parent whose name the species' name starts with, so it reads Lopunny M as a first stage of its own. The Kaizo checker follows the Fist Plate evolution to Buneary. After the edits, both checkers pass every move of the six at 40, the trainer lint finds nothing, and the generator's tests pass 5 of 5.

Eevee's two moves are in the data only, not in the generator's list of Ian's egg moves. Eevee's line is one of the generator's five held-out lines, and its test fails if the generator's source names one (it did, when I tried). A generator write of Eevee would drop Baton Pass and Substitute again. That is a tooling question for the Overseer, not for Ian.

The rest passes. No item repeats and no nature repeats. Every member is a final stage at its own level, and no move is a one-hit KO, an evasion move or a trap. The team carries no forced trade.

### Abilities, items and moves

Each ability is the slot Ian set, read from Oxide's species data:

| Member | Slot | Ability | What it does here |
|---|---|---|---|
| Cloyster | 2 | Skill Link | Icicle Spear and Rock Blast always hit five times, 125 power each |
| Slowbro | 2 | Own Tempo | blocks confusion and Intimidate; slot 1 is Regenerator, which heals only on a switch, and the AI switched Slowbro out once in 1,800 probe fights |
| Rapidash | 1 | Reckless | Flare Blitz and Double-Edge at 1.2 times; both regular slots are Reckless in Oxide, so there is no Run Away |
| Togekiss | 2 | Serene Grace | Ancient Power's, Ominous Wind's and Silver Wind's all-stat raise at 20 percent, not 10 |
| Leafeon | 1 | Magic Guard | no recoil from Giga Impact (the recoil subscript checks for it), no poison or hazard damage; Substitute's cost is still paid |
| Lopunny M | 1 | Iron Fist | raises Dizzy Punch only; High Jump Kick and Triple Axel are not punches |

Every item works with its holder, in the engine and in the simulator:

- King's Rock rolls its 10 percent on each of Skill Link's five hits (the engine's multi-hit flinch check runs per hit, and so does the simulator's), about 41 percent a move, but only when Cloyster moves first. At Speed 65 it does so against the slow walls the boxes take (Bastiodon, Probopass, Garganacl, Araquanid, Maylene's Empoleon and Sylveon). The probe counted 148 flinches from Cloyster in 900 fights on Maylene's boxes and 294 on Wake's.
- The Starf Berry raises one of five stats by two at a quarter of Leafeon's HP. Substitute almost never gets it there: the Baton Pass flag scores Substitute -10 below 60 percent HP, and Basic scores it -10 below 26 percent, so Leafeon subs at most twice. The Berry went off in 270 of 900 fights on Maylene's boxes and 349 on Wake's, nearly always from damage. A raise to Sp. Atk does nothing for Leafeon, but Leafeon then passes it (below).
- The Assault Vest raises the stat a special move meets. Under the room that is Lopunny's raw Defense, 84, which becomes 126. A physical move meets its raw Sp. Def, 94, and Psyshock meets that same 94 with no Vest, as in the later games.
- Leftovers and the Sitrus Berry work as usual. The Sitrus Berry went off in 524 and 703 of 900 fights.
- Charcoal raises Flare Blitz by a fifth, in the calculator's rows with Reckless.

Every move runs in the engine (the move-pool survey, regenerated today, reads "runs" for all 24), and the simulator models each. Trailblaze raises Speed one stage every time. Triple Axel hits at 20, 40 and 60, each hit rolling its own 90 percent and the move stopping at the first miss. Dizzy Punch confuses 20 percent of the time, and Razor Shell lowers Defense 50 percent. Giga Impact hits at 180 with no recharge and half the damage as recoil, which Magic Guard cancels, so Leafeon's is free. Baton Pass hands on the stages and the Substitute with its HP, with confusion, Focus Energy and the rest the engine lists. Toxic Spikes lays up to two layers. Fake Out works only on a member's first turn in.

### The permanent Wonder Room

The engine opens a listed trainer's fight in a Wonder Room that never counts down, and the move Wonder Room fails under it. Under the room only the raw stats trade places. A physical move meets the target's raw Sp. Def, with the Defense stages and the modifiers to Defense, and a special move meets the raw Defense with the Sp. Def ones. Psyshock follows the room, as a physical move does. The simulator's own five-turn room works the same way in its damage, so the study held that room on for the whole fight.

What that does to Ian's three Defense natures:

| Member | Nature | Raw Defense, now met by special moves | Raw Sp. Def, now met by physical moves |
|---|---|---|---|
| Cloyster | Relaxed | 177 | 77 |
| Slowbro | Bold | 115 | 81 |
| Leafeon | Impish | 133 | 69 |
| Lopunny M | Jolly, Assault Vest | 84, raised to 126 by the Vest | 94 |

So the natures' gains guard against special moves, and the three are frail to physical ones. The boxes' common catches are mostly physical, so by the screen the room makes Dahlia a little easier, not harder. Her screen best rises with the room on, from 11.45 to 12.35 without it to 11.95 to 12.95 with it on Maylene's boxes, and from 17.15 to 17.85 to 18.65 to 19.55 on Wake's. Natures are Ian's choice; this is the effect only.

### The Baton Pass flag

The engine's flag, with Basic and Expert, does three things with her three passers. I read `BatonPass_Main` and the Basic and Expert routines in the AI script, and `fightai.py` mirrors all three, the odds included.

1. It sets up on the battle's first turn. A named setup move (Swords Dance, Calm Mind and the rest) takes +5 on turn 1, -10 below 60 percent HP, and +1 otherwise. Any other status move takes +3 at 92 percent, then the same, so Toxic Spikes takes +8 on turn 1. A member that does not know Baton Pass still gets this 68.75 percent of the time. Cloyster led with Toxic Spikes in 747 of 900 fights on Maylene's boxes and 791 on Wake's.
2. It passes late and hurt, not early. Baton Pass takes -2 on turn 1, then +1 to +3 for the user's Attack stage, or failing that its Sp. Atk stage, and nothing for any other stat. Expert adds -2 unless a stage is at +2 or more and the user is hurt (at most 60 percent HP when faster, under 70 when slower), and +2 at 68.75 percent for a +3 stage once hurt. So a healthy member at +2 nets nothing and usually attacks instead. Togekiss passes once two Serene Grace raises have stacked and it has been hit. Rapidash passes its +2 Attack after a Swords Dance. Leafeon passes whatever its Starf Berry gave it, though a Speed raise from Trailblaze earns no score.
3. It does not choose the receiver. Baton Pass's switch goes through the party list, where the AI's post-KO rule picks the member whose types best fit the player's Pokemon in front, with a super effective move. Who most needs the raise plays no part.

### Gaps found

- The simulator models only the five-turn Wonder Room. Holding it on for a whole fight needs the harness this study used (a counter that cannot run out, set on every battle, and the matchup screen's rows rescaled by the simulator's own swap). Once Dahlia joins the engine's list, the simulator needs the permanent form, as it has for Trick Room, and `fightai`'s Wonder Room check needs the flag the permanent form would set. That fix needs Ian's approval.
- The OxiDex reads Lopunny M as a first stage of its own (above).
- The generator's held-out test stops Eevee's egg moves from going in its list (above).

## Part 2: the fight against the boxes

### Her difficulty against Ian's intent

Ian means her to be technically open in Maylene's split, realistically too hard until Wake's, and very hard even then. The cheap checks bear that out on five of the six boxes. Two measures are below. The first is the matchup screen's best six, scored by damage alone from full HP (higher is easier for the player). The second is the probe's greedy player against her and against the split's own gym leader, on the same box, seeds and player. That player never switches, never sets up and has no items, so its wins are far below a real player's on both sides. Only the comparison between the two columns means anything.

| Box | Screen best, Dahlia | Screen best, the leader | Greedy wins of 150, Dahlia | Greedy wins of 150, the leader |
|---|---|---|---|---|
| Maylene 1 | 12.95 | 16.80 | 18 | 99 |
| Maylene 2 | 12.45 | 16.85 | 7 | 131 |
| Maylene 3 | 11.95 | 17.00 | 5 | 87 |
| Wake 1 | 18.95 | 8.55 | 101 | 16 |
| Wake 2 | 18.65 | 7.35 | 17 | 22 |
| Wake 3 | 19.55 | 7.35 | 30 | 24 |

On Maylene's boxes she is far harder than Maylene by both measures, which is what Ian wants. On Wake's boxes the two measures disagree, and the probe is the one to read. The screen counts only one-on-one damage, so it misses her whole plan of raises, passes and Toxic Spikes, and her level of 40 against the box's 44 shows there in full. In play, the greedy player beats her about as often as it beats Wake on boxes 2 and 3. Box 1 is the exception: it beats her two times in three. Box 1's best six is Bibarel, Corviknight, Tentacruel, Sylveon, Glimmora and Dusclops. Bibarel and Corviknight carry Taunt. Tentacruel and Glimmora are Poison types, which soak up Toxic Spikes, and Sylveon's Fury Swipes breaks a Substitute and beats Lopunny M (+3.0).

### What the AI does with three passers

The probe's numbers, summed over the three boxes of each split (two sixes a box, 150 fights each, 900 fights a split):

| | Maylene's boxes | Wake's boxes |
|---|---|---|
| Fights with a Baton Pass | 343 | 229 |
| Passes by Togekiss | 205 | 179 |
| of which with all five stats raised | 186 | 142 |
| Passes by Leafeon | 164 | 145 |
| of which with Attack raised (by the Starf Berry) | 69 | 34 |
| Passes by Rapidash | 84 | 51 |
| of which with Attack at +2 (after Swords Dance) | 79 | 27 |
| Swords Dance used | 310 | 341 |
| Calm Mind used | 415 | 485 |
| Substitute used | 702 | 1053 |
| Cloyster's Toxic Spikes on turn 1 | 747 | 791 |

Who received the passes:

| Passer | Received by, Maylene's boxes | Received by, Wake's boxes |
|---|---|---|
| Togekiss | Lopunny M 141, Leafeon 28, Rapidash 20, Slowbro 14 | Lopunny M 66, Leafeon 53, Rapidash 36, Slowbro 22 |
| Leafeon | Lopunny M 90, Slowbro 26, Togekiss 25, Rapidash 20 | Lopunny M 56, Togekiss 51, Rapidash 20, Slowbro 15 |
| Rapidash | Leafeon 52, Slowbro 16, Togekiss 11 | Leafeon 26, Togekiss 14, Slowbro 5, Lopunny M 5 |

So the chain works, and it mostly lands on the right member. Togekiss's all-stat raise goes to Lopunny M more than to anyone. The replacement rule sends Lopunny M in against the Steel walls the boxes lean on, which are the very catches that beat Togekiss (Probopass and Bastiodon at +3.0 on it). Rapidash's +2 Attack lands on Leafeon most often, whose Giga Impact uses it. A raise also goes to Slowbro now and then, where it is wasted, since Slowbro's attacks are special.

The player's Pokemon knocked out while each member was in, per six of 150 fights:

| | Cloyster | Slowbro | Rapidash | Togekiss | Leafeon | Lopunny M |
|---|---|---|---|---|---|---|
| Maylene's boxes | 46 to 82 | 83 to 232 | 106 to 157 | 103 to 220 | 22 to 209 | 201 to 363 |
| Wake's boxes | 38 to 80 | 84 to 138 | 159 to 173 | 113 to 209 | 74 to 162 | 127 to 248 |

Lopunny M is the ace, and Cloyster does least everywhere.

### Answers to a pass

Taunt and Substitute breakers are the boxes' only answers, and nearly every top six carries one. No catch the screen takes has Haze, Clear Smog, Roar, Circle Throw, Dragon Tail or Unaware among its four. Primarina's Encore appears in 2 of 20 sixes on Wake's box 2, and Hariyama's pool has Whirlwind, though the screen does not pick it.

| Box | Top sixes with an answer in a catch's four | The answers |
|---|---|---|
| Maylene 1 | 20 of 20 | Taunt (Probopass, Bastiodon, Bibarel), Fury Swipes (Sylveon), Rock Blast, Bullet Seed |
| Maylene 2 | 20 of 20 | Taunt (Bastiodon), Fury Swipes (Sylveon) |
| Maylene 3 | 17 of 20 | Taunt (Bastiodon), Icicle Spear (Empoleon) |
| Wake 1 | 20 of 20 | Taunt (Corviknight, Bibarel, Probopass, Bastiodon), Fury Swipes (Sylveon), Rock Blast, Bullet Seed |
| Wake 2 | 20 of 20 | Taunt (Bastiodon, Bibarel), Fury Swipes (Sylveon), Pin Missile (Heracross) |
| Wake 3 | 20 of 20 | Taunt (Bastiodon, Corviknight, Bibarel), Icicle Spear (Empoleon), Arm Thrust (Hariyama) |

Taunt stops Swords Dance, Calm Mind and Substitute, but not Baton Pass's passing of what a member already has. Toxic Spikes fares worse against the same sixes, because so many of the catches are Steel, Poison or airborne. Of the player's switch-ins onto Toxic Spikes in the probe, a little under half were poisoned (44 percent on Maylene's boxes, 49 on Wake's). On Wake's box 1, Tentacruel and Glimmora soaked the layers up two times in three.

### Speed tiers

Her Speeds at no stage, +1 and +2, against the fastest catches the screen takes seven times or more:

| Member | 0 | +1 | +2 |
|---|---|---|---|
| Lopunny M | 111 | 166 | 222 |
| Rapidash | 105 | 157 | 210 |
| Leafeon | 93 | 139 | 186 |
| Togekiss | 89 | 133 | 178 |
| Cloyster | 65 | 97 | 130 |
| Slowbro | 41 | 61 | 82 |

| Split | The common catches' Speeds |
|---|---|
| Maylene's boxes | Haunter 96, Delphox 91, Tentacruel 88, Luxray 84, Leavanny 82, Orbeetle 81, Heracross 77, Glimmora 77, Drifblim 73, and the walls at 34 to 57 |
| Wake's boxes | Tentacruel 99, Glimmora 87, Heracross 86, Drifblim 82, Bibarel 74, Corviknight 70, and the walls at 38 to 64 |

Lopunny M and Rapidash outspeed every common catch on both splits. Leafeon loses only to Haunter and to Wake's Tentacruel, and one Trailblaze fixes both. Togekiss loses to those two and to Delphox on Maylene's box 3, and one raise fixes all three. Cloyster moves first only against the walls, which is where its King's Rock flinches come from.

### Cloyster passes the lead test

Every catch that beats Cloyster one-on-one, among those the top 20 sixes take five or more times, draws in a member that beats it. The one exception is Hariyama on Wake's box 3, in 7 of 20 sixes, which draws Slowbro and beats it narrowly (+0.5).

| Cloyster's answer | Drawn in | That member's setup |
|---|---|---|
| Tentacruel, Glimmora | Slowbro | Calm Mind |
| Heracross, Corviknight | Rapidash | Swords Dance, and its pass |
| Bibarel | Leafeon | Substitute (Bibarel's Taunt stops it) |
| Probopass, Bastiodon, Luxray, Empoleon | Lopunny M | none |

Half the answers draw a member with setup the player has to switch against. The Steel walls draw Lopunny M, which beats them by damage alone.

## Part 3: the weakest crux

### Why it is Cloyster's slot

Cloyster knocks out the fewest of the player's Pokemon of the six in every probe run: 38 to 82 per 150 fights, against 127 to 363 for Lopunny M. It passes the lead test, so its answers are not the problem. Three other things are.

1. Its turn 1 goes on Toxic Spikes, 747 and 791 times in 900 fights, because the Baton Pass flag scores any status move +8 on the battle's first turn. Against these boxes the layers do little. A little under half the switch-ins onto them were poisoned, and on Wake's box 1, Tentacruel and Glimmora soaked them up two times in three. The rest were Steel, airborne, Levitate or already statused.
2. The room turns its bulk the wrong way. Relaxed Cloyster's 177 Defense now guards against special moves, and the boxes' common catches hit physically, into its raw Sp. Def of 77.
3. Its King's Rock needs Cloyster to move first, and at Speed 65 it does so only against the walls.

Wake's box 1, the one box where she reads easier than Wake, is where all three bite at once: two Poison types soak up the spikes, and Taunt from Bibarel and Corviknight stops the rest of her setup.

### The picks

Each pick keeps Ian's other five members as they stand and was swapped into the lead's slot in memory. Each ran through the screen, the replacement trace, the lead test and the probe on the same six boxes, 150 fights per six.

| Set | Legal at 40 | Lead's knockouts per 150, Maylene's boxes | Wake's boxes | Lead's turn 1 | Passes in 900 fights, Maylene, Wake | Greedy wins of 150 against her, Maylene 1, 2, 3 | Wake 1, 2, 3 |
|---|---|---|---|---|---|---|---|
| Ian's: Cloyster, King's Rock, Relaxed, Skill Link; Icicle Spear, Rock Blast, Toxic Spikes, Razor Shell | yes, after the egg lists | 46 to 82 | 38 to 80 | Toxic Spikes, 85 percent | 453, 375 | 18, 7, 5 | 101, 17, 30 |
| 1. Ian's Cloyster with Shell Smash for Toxic Spikes | Shell Smash is Cloyster's level 69 move, so it goes on Shellder's egg list | 155 to 365 | 116 to 291 | Shell Smash, 84 percent | 305, 366 | 10, 6, 7 | 51, 28, 28 |
| 2. Omastar, White Herb, Modest, Shell Armor; Shell Smash, Surf, Ice Beam, Earth Power | yes, every move (Shell Smash at Omanyte's 40) | 334 to 639 | 89 to 121 | Shell Smash, 87 percent | 279, 533 | 7, 1, 2 | 64, 67, 32 |
| Tried and set aside: Ninjask, Focus Band, Adamant, Speed Boost; Swords Dance, Baton Pass, Protect, X-Scissor | Baton Pass and Protect would go on Nincada's egg list | 60 to 141 | 16 to 24 | Swords Dance, 99 percent | 1274, 1319 | 2, 22, 4 | 133, 101, 66 |

Pick 1 is my first choice, because it is the smallest change that fixes the slot. It keeps Ian's member, item, nature and ability, and changes one move. After Shell Smash, at +2 Speed (130), Cloyster outspeeds every catch on both splits. So Skill Link and King's Rock finally work together: the probe counted 671 flinches from it in 900 fights on Maylene's boxes and 658 on Wake's, against 148 and 294 for Ian's set. The Defense and Sp. Def drops are a real price under the room, since physical hits then meet a 77 Sp. Def at -1. That keeps it beatable, and a player who sees Shell Smash has one turn to answer it. It halves the greedy player's wins on Wake's box 1, and leaves boxes 2 and 3 close to Wake's own. The lead test reads exactly as for Ian's Cloyster, since the screen does not see Shell Smash: every common answer draws in a member that beats it, Hariyama on Wake's box 3 again excepted. The Toxic Spikes go, and with them her one way to punish switching.

Pick 2 is a stronger and stranger lead. Under the room, Omastar's 125 Defense guards against special moves and its 70 Sp. Def against physical ones, and the White Herb takes back Shell Smash's drops once. It becomes the fight's ace on Maylene's boxes, where Bastiodon, Probopass and the other walls cannot stop a +2 special attacker. On Wake's boxes Araquanid's Water Bubble and the Water and Ground catches answer it, and the greedy player wins more often there than against pick 1. It makes the gap between the two splits wider, which is the opposite of what Ian asked for. The team also loses its Ice typing, though Ice Beam and Lopunny M's Triple Axel keep the coverage.

Ninjask is the classic Baton Pass lead, and it does what that promises: four passers, Swords Dance on turn 1 nearly every time, and a pass in most fights. But under the room its 50 Sp. Def meets every physical hit, and it is lost almost at once on Wake's boxes (16 to 24 knockouts per 150). Without a lead that survives, the greedy player beats her more often than it beats Wake on every Wake box, so I set it aside.

### A smaller note

Lopunny M's Fake Out is the team's least-used move. The AI picked it 4 to 23 times per 150 fights on ten of the twelve sixes, and about a hundred times only on Wake's box 1. The AI's post-KO rule sends Lopunny M in after a knockout, and on that first turn a harder hit outscores Fake Out's +2. I ran a version with Thunder Punch for Fake Out (Iron Fist raises it, it is on Buneary's egg list, and it hits Corviknight and Empoleon). Lopunny M used it 28 to 162 times per 150 fights and knocked out a few more of the player's Pokemon, but the greedy player's wins moved both ways (Maylene's boxes 9, 6 and 14 against the draft's 18, 7 and 5; Wake's 93, 25 and 60 against 101, 17 and 30). That is no clear gain, so I leave Fake Out as Ian built it and ask nothing about it.

## How the numbers were made

Every number comes from a run in the worktree at 1efa311e001 (Ian's draft at 61e82ab5eed, merged with `origin/oxide` at 4fdb15e921d, plus the egg lists). The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/dahlia/`, each with its own usage line, and none writes to `res/`. They are copies of the Maylene study's, pointed at Dahlia.

- The boxes come from `plgoal3 --run dahlia-study --box maylene <seed> --screen` and `--box wake <seed> --screen` for seeds 1 to 3, a run name with no earlier results. Maylene's boxes are at 39 and Wake's at 44.
- `dahlia.py` is the harness every script loads. It fights each box against trainer 7 (`dummy_007`), which no map battles yet, so it adds her to the trainers the balance tools read. It sets her split to the box's, for the player's items. It holds the permanent Wonder Room on: every battle opens with the simulator's room counter at a million turns and the permanent flag set, and the matchup screen, which reads the calculator's rows and never a battle, gets a copy of the rows rescaled by the simulator's own Wonder Room swap. `NOROOM=1` turns the room off, for the contrast in Part 1.
- `margins.py` prints the screen's top sixes and every taken catch's margins and Speed, with the room on. `beat.py` counts the catches that beat each member.
- `fights.py` (and `fights2.py`, the same with the Toxic Spikes count) is Maylene's AI-picks probe and outcome probe in one: rough fights against a greedy player on two sixes per box (the screen's best and its most common), counting only real turns. It counts picks, uses, flinches, confusions, crashes, items, every Baton Pass with what it carried and who received it, and knockouts while each member was in. Its win and faint numbers mean nothing alone. `tally.py` makes the per-six table.
- `compare.py` runs the same greedy player against Dahlia and against the split's own gym leader, for the side-by-side in Part 2.
- `replace.py` runs `fightai.replacement` for each member leaving against each catch, and `leadtest.py` reads it with the margins for the lead test.
- `answers.py` lists each taken catch's answers to a pass, in its whole pool and in its four, and the Speeds.
- `CAND=name` swaps a pick into the lead's slot in memory (`dahlia.CANDS`), as Maylene's `swap.py` did, before any script runs.
- Legality comes from `oxide.py check 40`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`, and from `legal.py`, which uses the OxiDex's `learnsets.lists`. `palette.py` lists a species' legal moves at a level.

Where the screen's bias bites here. It counts only a clean one-on-one from full HP with no status move, so it sees no Swords Dance, Calm Mind, Substitute, Baton Pass, Toxic Spikes or Shell Smash. That is why it reads her as far easier than Wake on Wake's boxes while the probe does not. The probe's greedy player never switches, so Toxic Spikes poisons only the Pokemon sent in after a knockout, and nothing the player does draws a pass; it also never uses Taunt on purpose, which flatters her setup.
