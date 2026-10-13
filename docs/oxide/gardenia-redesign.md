# Gardenia's redesign: the evidence, the comparisons and Ian's six

Ian asked on 2026-10-13, before an overnight run, for the Roark process on Gardenia. The first stage (the end of this page) read today's team against a version with fixed move pools and offered two team shapes. Ian then designed his own six-member sun team, which the scorer read the same afternoon; this page opens with that reading and why it comes out as it does.

## Summary: Ian's six-member sun team

**Outcome.** Ian's team reads far harder than any version so far: won 52 percent of fights at real odds over goal 3's three boxes (65, 64 and 27), with 4.4 faints a fight and a difficulty of 23.6. Today's team reads 96 percent (3.5), and the Roark Ian accepted 86 (8.2). His rulings put Oxide's hardest bosses at about 80 percent won, so this is well past them, and box 3, which has no Alolan Ninetales, wins about one fight in four. Before the reading I forecast 75 to 88 percent, about 30 points too kind; the section on my forecast says what I missed.

**Why it reads so hard.** The sun never ends, so each Weather Ball is a 100-power Fire move with the sun's boost on top: the Solar Beam Ian left out, by another name. Cherrim's and Roserade's together landed a quarter of all the player's faints. Exeggutor's Harvest regrows its Occa Berry every turn, so its Fire Natural Gift repeats. Five of the six also have a super-effective move on each of the player's two counterpieces, Golbat and Alolan Ninetales, and the trainer AI's replacement rule feeds them to that counterpiece one after another: after a faint it sends the member whose own types hit the player's Pokemon hardest, if that member has a super-effective move on it.

**What decides a fight.** Two exchanges, and Golbat. The lead has to remove Solrock before its Stealth Rock and Zen Headbutt land: box 1 wins 84 percent of the fights in which Solrock falls by turn 2 and 46 percent of the rest. Alolan Ninetales, the one Pokemon in any box that outspeeds Roserade and knocks it out in one hit, has to outlive it: boxes 1 and 2 win 76 and 84 percent when it does, 25 and 35 when it falls first. All 66 fights in which Golbat survived were won.

**Lumineon** is fifth of six by faints. No six takes a Fire type, because the team's three Rock Tombs and Solrock's Ground Natural Gift already beat them, so Lumineon has no Fire type to punish, which is how it was the hardest member in the base ROM; and the sun halves Aqua Tail. Swagger was used 280 times in 225 fights and shows no effect on the win rate.

**A finding for the simulator.** It halves every hit of a two-to-five-hit move when the target holds a resist berry; the game halves only the first, because the battle script that halves the hit also uses the berry up. Here that makes Breloom's Coba Berry stronger than in the game: Golbat's Dual Wingbeat knocks out a full-health Breloom in the game and leaves it at a tenth of its HP in the reading. The fix is Ian's to approve, and it would make the next reading a little easier.

**What waits on Ian:**
1. The dials for the next reading (the table at the end). I recommend the five non-aces at level 22 with Roserade at the cap, and Cherrim's Weather Ball for Leech Seed. The first keeps every design choice; the second leaves the sun's Fire hammer on the ace alone, as his Solar Beam call did.
2. Whether the simulator fix goes in first.

**Next steps:** on his pick, the change on the study branch and the checks (about 20 minutes), the reading on the same three boxes (about 70 minutes), and the comparison here. A quicker probe can come first: 25 fights a box on the same sixes, about 15 minutes a variant.

## Ian's six

The team, as allocated on the study branch `study-gardenia-ian` (commit 7b88c32bc, not for landing). Every member has the highest IVs. Natural Gift is 60 power with these berries, and Breloom's Technician makes its 90.

| Member | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Solrock (lead) | 25 | Drought (hidden) | Shuca Berry | Timid | Zen Headbutt, Stealth Rock, Natural Gift (Ground), Rock Tomb |
| Cherrim | 25 | Flower Gift | Kebia Berry | Docile | Petal Blizzard, Synthesis, Rock Tomb, Weather Ball |
| Lumineon | 25 | Chlorophyll | Wacan Berry | Brave | Aqua Tail, Natural Gift (Electric), U-turn, Swagger |
| Exeggutor | 25 | Harvest (hidden) | Occa Berry | Naive | Sleep Powder, Zen Headbutt, Natural Gift (Fire), Egg Bomb |
| Breloom | 25 | Technician | Coba Berry | Hasty | Mach Punch, Bullet Seed, Rock Tomb, Natural Gift (Flying) |
| Roserade (ace) | 26 | Natural Cure | Payapa Berry | Calm | Sludge Bomb, Giga Drain, Weather Ball, Stun Spore |

Ian's notes with the team: the berries and a weather move on every member are deliberate, as are the six members, the physical Exeggutor on a weaker nature, Harvest, the Timid Solrock and no Solar Beam or Solar Blade in a fight whose sun never ends. Allocating it needed Drought as Solrock's hidden ability and Petal Blizzard, Weather Ball and Rock Tomb on Cherubi's egg list. Exeggutor's Egg Bomb is the level-up move it learns at 27, which Ian ruled a trainer may know.

### The reading

Read as the first stage's teams were: goal 3's boxes 1 to 3 at level 26, each box's six chosen by the team search, 75 fights at real odds and 25 very unlucky.

| Won at real odds | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 100% | 99% | 89% | 96% |
| Version B | 100% | 100% | 85% | 95% |
| Ian's six | 65% | 64% | 27% | 52% |

| Faints a fight (difficulty) | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 1.40 (1.4) | 1.52 (2.1) | 2.76 (7.0) | 1.89 (3.5) |
| Version B | 1.12 (1.1) | 0.77 (0.8) | 2.83 (8.7) | 1.57 (3.5) |
| Ian's six | 4.01 (17.9) | 3.91 (18.3) | 5.40 (34.7) | 4.44 (23.6) |

| Very unlucky, won (faints) | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 88% (2.28) | 92% (2.40) | 56% (4.52) | 79% (3.07) |
| Version B | 100% (1.44) | 100% (1.00) | 76% (3.36) | 92% (1.93) |
| Ian's six | 56% (4.44) | 48% (4.84) | 20% (5.52) | 41% (4.93) |

Clean wins were 1, 4 and 0 percent. Where the faints fell over the three boxes, by the member that made them:

| Exeggutor | Cherrim | Roserade | Breloom | Lumineon | Solrock |
|---|---|---|---|---|---|
| 216 | 210 | 199 | 162 | 120 | 92 |

The scorer's sixes, lead first:

| Box | Six |
|---|---|
| 1 | Cherrim, Grotle, Corvisquire, Golbat, Probopass, Alolan Ninetales |
| 2 | Tsareena, Staravia, Liepard, Vullaby, Golbat, Alolan Ninetales |
| 3 | Tsareena, Corvisquire, Dubwool, Vullaby, Golbat, Breloom |

Golbat is in every six and Alolan Ninetales in both whose box has it, as against today's team. No six takes a Fire type, though boxes 1 and 2 hold Fletchinder, Raboot and Ponyta, and Raboot and Ponyta are in the screen's top ten sixes on box 2. Each box took 62 to 73 minutes.

### How the fights go

The reading's 225 fights at real odds were replayed on its own seeds with every turn written down, and the replay reproduces the reading's results exactly. Most fights follow the same course.

**The lead.** Solrock leads, and Drought's sun lasts the fight. Box 1 leads with its own Cherrim, whose Petal Dance knocks Solrock out by turn 2 in 38 of 75 fights. Boxes 2 and 3 lead with Tsareena, which needs two Razor Leafs and takes Zen Headbutts in return (Tsareena is Grass and Fighting in Oxide), so Solrock lasts to turn 3.6 and 4.7 on average there, and Stealth Rock goes up in 62 and 59 of the 75 fights.

**The order.** The player picks the next foe by picking who lands each knockout, which is how Ian baits a boss; but with this team's coverage nearly every pick brings in a member with a super-effective hit. The usual order, with the player's Pokemon each member first meets (the counts are fights of 75):

| Box | Second | Third | Then |
|---|---|---|---|
| 1 | Roserade, on Cherrim or Alolan Ninetales (71) | Cherrim, on Ninetales (33) | Exeggutor on Golbat or Ninetales; Breloom and Lumineon last |
| 2 | Exeggutor, on Tsareena (52) | Lumineon, on Golbat or Staravia (36) | Cherrim and Roserade on Ninetales or Golbat |
| 3 | Exeggutor, on Tsareena or Breloom (66) | Lumineon, on Golbat (57) | Cherrim and Breloom on Golbat (their Rock Tomb); Roserade last |

**The middle.** Box 1's fight turns on Roserade, which comes second. Probopass takes its Weather Balls at 39 percent a hit while Rock Blast chips it, and Alolan Ninetales finishes it with Icicle Spear: Ninetales is out for 48 of Roserade's 73 falls. Golbat then carries most of the rest with Dual Wingbeat and Leech Life, out for about half the falls of Exeggutor, Cherrim and Breloom. Box 2 runs the same way with Exeggutor first. Box 3 has no Ninetales, and its three Flying types carry the fight into three Rock Tombs, two Zen Headbutts, Lumineon's Electric Natural Gift and Stealth Rock.

**The losses.** In box 1's 26 losses the player got past Solrock and Roserade and ran out against the back three: Lumineon was left standing in 24, Cherrim and Breloom in 16 each. In box 3's 55, Roserade was still at 95 percent of its HP in 52: the player never reached it.

### What decides a fight

| Box | When | Won | Otherwise | Won |
|---|---|---|---|---|
| 1 | Solrock down by turn 2 (38 fights) | 84% | it lasts longer (37) | 46% |
| 2 | Solrock down by turn 2 (29) | 79% | it lasts longer (46) | 54% |
| 1 | Alolan Ninetales outlives Roserade (59) | 76% | Ninetales falls first (16) | 25% |
| 2 | Alolan Ninetales outlives Roserade (44) | 84% | Ninetales falls first (31) | 35% |
| 1 | Golbat survives (33) | 100% | Golbat faints (42) | 38% |
| 2 | Golbat survives (26) | 100% | Golbat faints (49) | 45% |
| 3 | Golbat survives (7) | 100% | Golbat faints (68) | 19% |

The moves the player's 998 faints fell on (a faint to Stealth Rock on a switch-in counts under the move used that turn, so the counts are close rather than exact):

| Move | Faints | Share |
|---|---|---|
| Cherrim's Weather Ball | 127 | 13% |
| Roserade's Weather Ball | 114 | 11% |
| Exeggutor's Zen Headbutt | 95 | 10% |
| Breloom's Rock Tomb | 73 | 7% |
| Lumineon's Aqua Tail | 68 | 7% |
| Solrock's Zen Headbutt | 65 | 7% |
| Exeggutor's Natural Gift (Fire) | 63 | 6% |
| Breloom's Mach Punch | 63 | 6% |
| Roserade's Sludge Bomb | 58 | 6% |
| Exeggutor's Egg Bomb | 57 | 6% |

### Each member's part

| Member | Faints made | Falls on turn (boxes 1, 2, 3) | Its part |
|---|---|---|---|
| Solrock | 92 | 2.7, 3.6, 4.7 | Sets the sun and Stealth Rock. On box 3 its Zen Headbutt makes one faint a fight, on Tsareena, Breloom and Golbat. |
| Cherrim | 210 | 12.7, 15.5, 14.5 | Comes in on Alolan Ninetales, where Weather Ball and Rock Tomb are both super-effective, and on Golbat for Rock Tomb. Weather Ball is the top killing move on boxes 2 and 3. |
| Lumineon | 120 | 18.2, 17.3, 16.6 | Chlorophyll makes it the fastest Pokemon in the fight (104 Speed), but the sun halves Aqua Tail. It comes in on Golbat for its Electric Natural Gift and finishes weakened Pokemon late. |
| Exeggutor | 216 | 14.5, 10.4, 9.4 | The bulkiest member, second on boxes 2 and 3 against Tsareena. Zen Headbutt takes 95 percent of Golbat's HP, and Harvest keeps its Fire Natural Gift coming. |
| Breloom | 162 | 15.6, 13.5, 14.5 | Technician's Rock Tomb one-shots Corvisquire and Staravia, Mach Punch picks off what is weakened, and the Coba Berry carries it through the first Flying attack. |
| Roserade | 199 | 8.9, 14.7, 17.4 | Outspeeds everything but Alolan Ninetales and Liepard, and in the sun its Weather Ball one-shots or two-shots nearly every Pokemon in the boxes. In box 1's fight 18, after Ninetales fell, one at 23 HP took Probopass, Grotle, Cherrim and Corvisquire before Golbat finished it. |

The turns count only the fights in which the member fell.

### Why box 3 collapses

Box 3 has no Alolan Ninetales, so nothing in it outspeeds Roserade, and its answers to the other five are its three Flying types and Breloom. Ian's team is built against exactly that. Solrock's Zen Headbutt and Rock Tomb meet the lead and the Flying types, and it lives to turn 4.7 with Stealth Rock taxing every Flying switch-in. Exeggutor comes in on Tsareena and makes 111 faints in 75 fights, the most of any member on any box. When Golbat knocks Exeggutor out, the AI's rule sends Lumineon at it (48 of 64 times), and Cherrim or Breloom after that, each with a super-effective move. Golbat fainted in 68 of the 75 fights, and the 7 in which it survived were all won.

### Lumineon and Swagger, against the base ROM

Ian's experience of the base ROM is that Lumineon is the hardest member to manage: Aqua Tail still hits hard in the sun, Swagger can turn a fight, and killing Cherrim with the sun up almost always baits it next. The conditions for that are gone here. The base ROM's natural answer to its own sun team is a Fire type, and against a Fire type Lumineon is the AI's first pick, with Water still super-effective at half power. In this team no six takes a Fire type, so Lumineon meets Golbat and Corvisquire, where Aqua Tail is neutral and halved, and killing Cherrim baits Exeggutor on box 1 (44 of 59 times) and Breloom or Roserade on boxes 2 and 3. Swagger's target fainted within two turns 48 times of 280, but the fights with more Swaggers are not lost more often, partly because Lumineon comes out late and only in fights that last. It decides single fights (box 1's fight 4, where Swagger and Aqua Tail took Alolan Ninetales), not the totals.

### How far to trust the reading

The replay shows the planner's weak spots: it sometimes switches a Pokemon into a hit when a trade was better, as in box 3's fight 0, where it sent a full-health Breloom into Exeggutor's Zen Headbutt to spare a Tsareena at a third of its HP. A player who plans the baits would win more often than the scorer does. But the same planner read Roark at 86 percent, so the order of the two fights holds: this Gardenia is far harder than the Roark Ian accepted. The simulator finding in the summary points the same way, and its fix would help the player a little against Breloom.

### Where my forecast went wrong

Before the reading I forecast 75 to 88 percent won, box 3 at 60 to 75, Lumineon and Roserade as the members that make the most faints, and Corvisquire leaving the sixes. Each was wrong. What I missed, as checks to run on a team sheet before the scorer does:

1. Count each counterpiece's threats. For the player's likely answers (here Golbat and Alolan Ninetales), count the members that knock it out in one or two hits and how many of those move first. Five of six threaten each of them.
2. Read the AI's next pick. After a knockout the next member is the one typed best against the Pokemon that landed it, if it has a super-effective move. When most members carry one against most of the box, every knockout brings in a counter, and on box 3 the rule lines three members up against Golbat in a row.
3. Speed decides more than power. A fast attacker that one-shots is lethal at any HP: only Alolan Ninetales outspeeds and one-shots Roserade, so once it falls Roserade sweeps.
4. A weather that never ends turns its moves into hammers. Count Weather Ball as a 100-power move of the weather's type with the weather's boost, as Ian counted Solar Beam.
5. Harvest in a sun that never ends is an endless berry: Natural Gift every turn, and the resist berry back.
6. A resist berry matters most on a member that also moves first against the answer it resists, as Breloom does against Corvisquire and Vullaby.
7. When a team covers the player's natural answer (Fire against Grass) so well that the player leaves it at home, the member built to punish that answer, Lumineon here, has nothing to do.

### The dials, for Ian to pick

Each dial keeps the six members, their berries and the sun. Ian said the levels may move.

| Dial | What it changes | Against Ian's design |
|---|---|---|
| The five non-aces at level 22, Roserade at 26 | About a fifth less damage from each of the five and a tenth less bulk. Golbat, Staravia and Tsareena then outspeed Cherrim, Solrock and Breloom, and Corvisquire outspeeds Solrock and Breloom. | Nothing; the ace stays at the cap, as his level ruling has it |
| Cherrim's Weather Ball for Leech Seed | One Fire hammer instead of two. Cherrim keeps Flower Gift, Synthesis, Petal Blizzard and Rock Tomb, so it still comes in on Alolan Ninetales, with less to hit it with. | Cherrim's weather move becomes Synthesis |
| Roserade from Calm to Sassy | Its Speed falls from 59 to 53, under Golbat, Tsareena, Dubwool and Alolan Ninetales, so the player moves first against the ace | None; Sassy is a nature the team does not use yet |
| Breloom's Coba Berry for another resist berry | The first Flying hit is no longer halved, and its Natural Gift changes type with the berry | Its Flying Natural Gift goes |
| Exeggutor with Chlorophyll for Harvest | Natural Gift once only, and a faster Exeggutor | Ian chose Harvest |
| Five members, Lumineon out | One trade fewer | Ian chose six |

My forecast, to be checked as the last one was: the levels alone read about 65 to 75 percent won on the mean, boxes 1 and 2 near 80 and box 3 near 45; with Cherrim's Weather Ball swapped too, about 72 to 82 percent, box 3 near 55. Box 3 stays the hardest, because without Alolan Ninetales nothing in it outspeeds Roserade; the Sassy nature is the dial for that.

## The first stage: today's team and version B (overnight, 2026-10-13)

The first stage read today's team and version B, the same five with fixed move pools and sun. Its summary, as Ian read it that morning:

**Outcome.** Today's Gardenia reads too easy: won 96 percent of the time at real odds (100, 99 and 89 by box), difficulty 3.5. That is above Ian's 95 percent ceiling for a boss, and softer than the Roark he accepted (86 percent, 8.2), though his rulings count Gardenia among the game's hardest fights. Version B, the same five with fixed move pools and sun, reads the same within noise (95 percent, 3.5) and far easier very unlucky (92 against 79). Move pools alone do not move this fight.

**The crux.** Two of the player's Pokemon decide it, and Gardenia has no answer to either. Golbat is in every six the scorer took, with Dual Wingbeat; Alolan Ninetales is in every six whose box has it, and sweeps four of her five with Icicle Spear. On box 3, which lacks it, Corvisquire and Vullaby take its place, and that box is the only one with real losses. Her lead, Roselia, made no faint in 300 fights. The sun as version B sets it costs more than it gives: Exeggutor spends its first turn on Sunny Day, loses its Leftovers, and falls by turn 3, while only Roserade's Weather Ball gains.

Ian's answers (2026-10-13): Solar Beam may go on a boss as a conditional move, with his okay when it comes early, and he left it off his own team because its sun never ends; a member a little under its evolution level is fine, not egregiously so, and Slugma should evolve by Fantina's split; and in place of either shape he designed the six read above.

### The readings

Each team is read on goal 3's boxes 1 to 3 at level 26, with each box's best six chosen by the scorer's team search, 75 fights at real odds and 25 very unlucky. The difficulty number is the faints a fight plus 40 times the losing rate. A box's numbers move by about five points from noise alone.

| Won at real odds | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 100% | 99% | 89% | 96% |
| Version B | 100% | 100% | 85% | 95% |

| Faints a fight (difficulty) | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 1.40 (1.4) | 1.52 (2.1) | 2.76 (7.0) | 1.89 (3.5) |
| Version B | 1.12 (1.1) | 0.77 (0.8) | 2.83 (8.7) | 1.57 (3.5) |

| Very unlucky, won (faints) | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's team | 88% (2.28) | 92% (2.40) | 56% (4.52) | 79% (3.07) |
| Version B | 100% (1.44) | 100% (1.00) | 76% (3.36) | 92% (1.93) |

Where the faints fell, by the member of Gardenia's that made them, over the three boxes:

| | Exeggutor | Breloom | Roserade | Ludicolo | Roselia |
|---|---|---|---|---|---|
| Today's team | 145 | 127 | 104 | 50 | 0 |
| Version B | 53 | 99 | 109 | 85 | 8 |

Version B's sixes: box 1 Bibarel, Golbat, Probopass, Cherrim, Plusle and Alolan Ninetales; box 2 Masquerain, Liepard, Golbat, Dubwool, Alolan Ninetales and Bronzor; box 3 Goldeen, Corvisquire, Dottler, Bibarel, Golbat and Breloom. Each reading took 40 to 70 minutes on this machine.

### The player's answers

Golbat is in every six the scorer took to today's Gardenia, with Dual Wingbeat. Alolan Ninetales is in the two sixes whose box has it (boxes 1 and 2), and the player's own Cherrim in two. The rest change by box: a Steel Pokemon (Probopass or Bronzor), a Bug (Dustox, Masquerain or Dottler), and on box 3, which has no Alolan Ninetales, two more Flying types (Corvisquire and Vullaby).

| Box | Today's six |
|---|---|
| 1 | Barboach, Dustox, Golbat, Probopass, Cherrim, Alolan Ninetales |
| 2 | Masquerain, Liepard, Golbat, Tsareena, Alolan Ninetales, Bronzor |
| 3 | Corvisquire, Dottler, Bibarel, Vullaby, Golbat, Cherrim |

The search's other finalists lean the same way: four-Flying sixes (Staravia, Corvisquire, Vullaby, Golbat) on boxes 1 and 3, and the Fire pair Raboot and Ponyta on box 2.

### The baiting patterns

From the three traced fights (one per box) and where the faints fell over all 300:

1. **The lead does nothing.** Roselia's Spikes and Sleep Powder took no faint in any fight. The player's lead either knocks it out at once (Alolan Ninetales' Icicle Spear) or sets up on it: box 3's Dottler uses Calm Mind twice, is put to sleep twice and wakes each time, while Roselia spends its turns on Spikes and never threatens it.
2. **Flying attacks carry the fight.** Golbat, Corvisquire and Vullaby meet Exeggutor, Breloom (four times weak), Roserade and Ludicolo with Dual Wingbeat and Pluck. Ludicolo's Ice Beam is the team's only real answer to them, and Breloom's Rock Tomb the other.
3. **Alolan Ninetales sweeps when the box has it.** On box 1 it takes Roserade, Exeggutor and Breloom in four turns with Icicle Spear, and its Fairy typing turns Breloom's Fighting moves.
4. **Steel pivots take the Poison moves.** Bronzor and Probopass come in on Roserade's Sludge Bomb for nothing.
5. **Spikes punish the switch dance**, which box 2's six plays anyway (Golbat, Masquerain and Tsareena trading places against Breloom's Rock Tomb and Bullet Seed).

Today's faints, by the member of Gardenia's that made them: Exeggutor 145, Breloom 127, Roserade 104, Ludicolo 50, Roselia 0.

### Modern moves

The player's sixes carry six Generation 5+ moves: Dual Wingbeat on every Golbat and on Corvisquire (four of eighteen slots), Draining Kiss on both Cherrims, Disarming Voice on both Alolan Ninetales, Struggle Bug, Snarl and Smack Down. Dual Wingbeat is the one that matters: a two-hit Flying move on the Pokemon every six takes.

Version B's sixes add Trailblaze (Plusle), Guard Split (Dubwool) and Scald (Goldeen). The player's modern moves are useful rather than decisive: the fight turns on typing (Flying, Ice and Fairy, Steel), and the one modern move every six carries, Dual Wingbeat, is the Flying attack the scorer gives Golbat and Corvisquire.

### The crux

Gardenia's members, today and in version B, share two blind spots, and the player's six is built on both:

1. **Golbat** (Poison and Flying, in every six): only Ludicolo's Ice Beam, Exeggutor's Psychic and the two Rock moves (Breloom's Rock Tomb, Exeggutor's Ancient Power) hit it hard, and it resists her Grass and Fighting moves four times over. Dual Wingbeat takes Breloom (four times weak), Exeggutor and Roserade.
2. **Alolan Ninetales** (Ice and Fairy, caught wild from Route 211 West in this split): Icicle Spear hits four of her five super-effectively (all but Ludicolo), Fairy turns Breloom's Fighting moves, and only Roserade's Sludge Bomb and Breloom's Rock Tomb hit it hard. It is usually the player's Pokemon that faints most, and it still sweeps.

Without Alolan Ninetales (box 3), the player brings Corvisquire and Vullaby with Golbat, and Gardenia wins 11 to 15 percent of fights: the only box with real losses. Her passive lead makes it worse on every box: Roselia's Spikes and Sleep Powder give the player's lead free turns.

So the redesign's job is an answer to Flying (Electric or Rock), an answer to Alolan Ninetales (Fire, Rock, Steel or Poison, ideally resisting Ice), and a lead that threatens. The sun is worth having only if it costs no turn (Drought) and more than one member uses it.

### Version B: today's five with fixed move pools

| Slot | Member | Today | Version B |
|---|---|---|---|
| Lead | Exeggutor 25 (Chlorophyll) | third, Leftovers, Modest: Psychic, Giga Drain, Ancient Power, Leech Seed | Heat Rock, Mild: Sunny Day, Giga Drain, Psychic, Ancient Power |
| 2 | Roselia 24 | lead: Spikes, Sleep Powder, Giga Drain, Extrasensory | Magical Leaf for Giga Drain |
| 3 | Ludicolo 25 | Ice Beam, Water Pulse, Giga Drain, Fake Out | Knock Off for Giga Drain |
| 4 | Breloom 25 | Mach Punch, Rock Tomb, Bullet Seed, Stun Spore | unchanged |
| 5 | Roserade 26 | Sludge Bomb, Giga Drain, Shadow Ball, Cotton Spore | Weather Ball for Cotton Spore |

Two Giga Drains are left of five. Exeggutor leads because the trainer AI gives Sunny Day the Weather flag's +5 only on the battle's first turn, and it is the only one of the five that may learn Sunny Day (from its palette before the TM pass). The Heat Rock makes the sun last eight turns. Its nature moves from Modest to Mild, since Roserade is Modest too (no repeats, Ian 2026-10-12). Drought is on none of the five.

Checked before the reading, on Roark's lessons: the Kaizo study's checker passes every move under the boss ceiling of 90 for borrowed attacks; the scorer prepares sun rows and doubles Exeggutor's Speed in sun (40 to 80); and the AI's exact odds give Sunny Day on the first turn against every lead tried, and Weather Ball in sun against Probopass and Golbat.

Not done, and Ian's to decide: Solar Beam is a TM move at 120 power, over the ceiling, so no member carries it.

### Candidates for the species stage

This is the third stage of the Roark process: candidates from the whole Pokedex, any stage, with no filter by evolution level or stats total (Roark's Naclstack sits ten levels under its own), Grass or sun-themed as Ian asked, each picked for a weakness the readings show. The team shape is Ian's to choose; sets and a reading follow his pick.

The weaknesses, from the readings:

1. **Flying** (Golbat in every six; Corvisquire, Vullaby, Staravia, Masquerain): only Ludicolo's Ice Beam and Breloom's Rock Tomb answer it, and Breloom is four times weak to it. Corvisquire takes nothing super-effective at all; that needs Fire or Electric.
2. **Alolan Ninetales** (Ice and Fairy) sweeps Grass and turns Breloom's Fighting moves.
3. **Steel pivots** (Bronzor, Probopass) take the Poison moves for nothing.
4. **A passive lead**: Roselia made no faint in 300 fights, and gives a setup Pokemon free turns.
5. **Bug and Fire baits** (Dustox, Dottler, Masquerain; Raboot and Ponyta among the search's finalists), which sun would make stronger.

Each candidate below has a legal set at level 25 under the boss ceiling of 90 for borrowed attacks (the Kaizo study's checker, with the palette from before the TM pass). The rough matchup numbers are the study's damage estimate at the top roll with no weather, good for a bait test, not for a fight's level: the candidate's best hit on the answer, then the answer's best hit back, in percent of HP.

| Candidate | Typing and ability | Covers | Fears | Golbat | Corvisquire | Alolan Ninetales | Bronzor |
|---|---|---|---|---|---|---|---|
| Magcargo | Fire and Rock, Drought (hidden) | 1, 2, 3, 4, 5: sets sun on entry, resists Flying, Poison, Ice, Fairy, Bug and Fire | Water and Ground four times over (Barboach) | 77 / 16 | 96 / 16 | 105 / 17 | 135 / 16 |
| Torkoal | Fire, Drought (hidden) | 3, 4, 5, and the sun | Water, Ground, Rock | 62 / 14 | 75 / 23 | 86 / 14 | 113 / 16 |
| Rotom-Mow | Electric and Grass, Levitate | 1 hardest of all, a Grass type of the gym's own | Ice, Fire, Poison, Bug | 131 / 48 | 172 / 31 | 51 / 45 | 65 / 18 |
| Meganium | Grass, Thick Fat or Leaf Guard | 2 and 5 (Thick Fat halves Ice and Fire), Sunny Day and Synthesis legal | Flying, Poison, Bug | 51 / 39 | 69 / 51 | 45 / 34 | 29 / 15 |
| Venusaur | Grass and Poison, Chlorophyll | 2 (Sludge Bomb on Fairy), a sun sweeper with Growth and Sunny Day legal | Flying, Psychic, Ice, Fire | 32 / 37 | 82 / 62 | 98 / 40 | 32 / 29 |
| Solrock | Rock and Psychic, Levitate | 1 and 4 (Rock Slide, Psychic on Golbat, Stealth Rock) | Steel, Water, Grass | 127 / 41 | 148 / 32 | 150 / 34 | 28 / 21 |
| Houndoom | Fire and Dark, Flash Fire | 3 and 5 (Flash Fire swallows the Fire baits), Dark on Dottler | Water, Fighting, Rock, Ground | 67 / 34 | 88 / 45 | 101 / 26 | 135 / 8 |
| Cradily | Rock and Grass, Solid Rock | 1 (Rock moves) on a Grass type | Ice, Steel, Bug, Fighting | 77 / 40 | 96 / 31 | 71 / 35 | 22 / 21 |
| Sinistcha | Grass and Ghost, Heatproof (hidden) | 5 (Heatproof halves Fire), Matcha Gotcha's burns, Will-O-Wisp | Flying, Ice, Dark, Ghost | 97 / 35 | 86 / 54 | 51 / 38 | 65 / 17 |
| Roselia, today | Grass and Poison | none | | 69 / 67 | 45 / 112 | 38 / 76 | 25 / 40 |
| Ludicolo, today | Water and Grass | 1, with Ice Beam | Flying, Poison | 77 / 49 | 101 / 62 | 38 / 22 | 39 / 13 |

Not in Oxide, so not offered: Heliolisk, Whimsicott, Lilligant, Scovillain, Toedscruel, Brambleghast, Gogoat, Sawsbuck, Comfey. Cherrim, the base ROM's sun setter, can no longer learn Sunny Day.

#### Two team shapes, for Ian to pick

**Shape 1, a sun team with two swaps (recommended).** Keep Exeggutor, Breloom and Roserade; replace Roselia and Ludicolo.

| Slot | Member | Job |
|---|---|---|
| Lead | Magcargo (Drought, Heat Rock for 8 turns) | Sun on entry with no turn spent; Stealth Rock; Rock Slide on Golbat and Alolan Ninetales, Flamethrower on Corvisquire, Bronzor and the Bugs; resists Dual Wingbeat, Poison, Icicle Spear and Disarming Voice |
| 2 | Exeggutor (Chlorophyll) | Doubled Speed in sun; Psychic on Golbat; Synthesis heals two thirds in sun; Leftovers back |
| 3 | Rotom-Mow (Electric and Grass, Levitate) | Thunderbolt on every Flying answer; Will-O-Wisp on Golbat's and Corvisquire's physical attacks |
| 4 | Breloom (Technician) | As today: Mach Punch, Rock Tomb, Bullet Seed, Stun Spore |
| Ace | Roserade | Weather Ball (Fire in sun) on Steel and Bug, Sludge Bomb on Alolan Ninetales |

Its risk is Barboach (Water and Ground, four times super-effective on Magcargo; the sun halves the Water half), and the sun helps the player's Fire types (Raboot, Ponyta, Fletchinder). Torkoal is the gentler Drought lead (only Fire, so Water and Ground hit it twice over instead of four times).

**Shape 2, a Grass gym without sun.** Rotom-Mow leads (Thunderbolt on the Flying leads), Meganium takes Alolan Ninetales and the Fire baits on Thick Fat, and Exeggutor, Breloom and Roserade stay with today's sets less two Giga Drains. Every member is a Grass type, and nothing depends on the sun.

Further candidates for either shape, if Ian wants a different flavour: Venusaur (Chlorophyll, Growth, Sludge Bomb on Fairy), Houndoom (Flash Fire against the Fire baits), Solrock (Rock and Psychic, Stealth Rock), Sinistcha (Heatproof, Matcha Gotcha) and Cradily (Rock on a Grass type).
