# QA plan, in order

The in-game checklist (`ingame-checklist.md`) holds 119 open checks, written as a reference. This page is the order to work in. Most of those checks are things you notice while playing, and the OxiDex's Alpha tab already shows each one on the card of the zone where it happens. So QA comes down to one test kit session for the systems added this week, then the run itself with the Alpha tab open. Everything else waits. Use the QA ROM and test kit in `~/oxide-playtest` (today `pokeplatinum-oxide-df365a296.nds` and `pokeplatinum-oxide-testkit-df365a296.nds`), with melonDS's Break on startup off.

## 1. The test kit: this week's systems (about 45 minutes)

Each line is one kit entry: what to do, and what passes. `test-kit.md` has the detail of each set.

| # | Kit entry | Do | Passes when |
|---|---|---|---|
| 1 | Move sets 71 to 84 (third page) | Run each set against the wild foe it names | Hyper Beam's kin recoil half and never recharge; Sky Attack, Dig and Dive hit the turn chosen; two-to-five-hit moves mostly hit 2 or 3, always 5 for the Skill Link Cloyster; Fury Cutter hits three times, rising; Thrash, Petal Dance, Outrage and Uproar hit once with no lock; Bone Rush never misses; Mew stays drawn whole in the Sky Attack, Dig and Dive animations |
| 2 | Abilities, Sheer Force | Toucannon with its Life Orb against Chansey | Flame Charge costs it no HP; Bullet Seed and Brave Bird each cost a tenth |
| 3 | Modern rules, "Infiltrator, Mimic" | Splash while Snorlax's doll goes up, then Psycho Shift and Mimic | Psycho Shift burns Snorlax through the doll, and Mimic copies Substitute |
| 4 | Two TMs | Teach TM01 twice | The case shows x2, then x1, then nothing |
| 5 | Route 208, all badges; then the Warp menu's five gauntlet entries | Step into each section, try to walk back, try the Pocket PC, an Escape Rope, Dig and Fly | The way back says "There's no turning back now!" and walks you off it; the rest refuse with "You can't use that here yet!" |
| 6 | Route 208, all badges; Warp to Veilstone | Talk to the roughneck, buy Earthquake on the store's 3F, beat Rocco by the coins clerk, beat Jogger Scott on Route 215 | Roughneck gives a Sitrus Berry once; Earthquake sells once and leaves the list; Rocco and Scott give their TMs straight after the win |
| 7 | Items menu | Open the Ice Stone, abilities, Mints and Caps, and TMs entries | Each prints its own line |
| 8 | Level caps menu | Feed Rare Candies at the cap of 16 | They stop at 16 and the extra candy is kept |

## 2. The run (play normally, about an hour a split)

Start a new game on the ordinary ROM with the battle recorder running and the OxiDex's Alpha tab open beside it. Play through. Each zone's card lists its trainers, items and in-game checks; tick and note there as you meet them. The first hour covers most of section 3's early checks by itself: the Chimchar-named rival, the Pocket PC and its Rare Candy and Hidden Power lines, rewards straight after wins, gift dialogue, and the level cap of 16.

## 3. Waiting, not part of QA

- **The older move sets 23 to 70** in the kit (48 obscure moves from element 4). Sample them later. I can first cut the list to the moves a trainer or the player's lists actually carry.
- **The seven (live) checks**, which need me attached over the GDB stub. One joint session covers them. Three name today's teams (Camper Zackary's Castform, Worker Jackson's Wormadam, Volkner's Rotom-Mow), which the comb replaces, so they get rewritten first.
- **Section 5, after the League**: only at the end of a run.
- **One check is out of date**: "An HM taught from the case stays" (Single-use TMs). HMs became single-use TMs in the TM pass, so an HM is now used up like any TM.
