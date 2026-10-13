# Roark's redesign: the comparison and what it taught

The scorer read today's Roark and the new team on goal 3's boxes 1 to 3 on 2026-10-12. With the three cuts, the new team reads easier than today's, at 98 to 100 percent won, above Ian's 95 percent ceiling for a boss. The cuts overshot, because they were chosen on the Kaizo study's rough simulator, which here got even the direction wrong. The next step, and what waits on Ian, is at the end.

## The readings

Each team is read with each box's best six, 75 fights at real odds and 25 very unlucky. The difficulty number is the faints a fight plus 40 times the losing rate.

| Won at real odds | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's Roark | 87% | 91% | 100% | 92% |
| New, Naclstack as drafted (a) | 99% | 100% | 100% | 100% |
| New, Naclstack salting (b) | 96% | 97% | 100% | 98% |

| Faints a fight (difficulty) | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Today's Roark | 2.68 (8.0) | 3.59 (7.3) | 1.17 (1.2) | 2.48 (5.5) |
| New (a) | 2.32 (2.9) | 1.45 (1.5) | 0.41 (0.4) | 1.40 (1.6) |
| New (b) | 2.31 (3.9) | 2.00 (3.1) | 0.40 (0.4) | 1.57 (2.5) |

Very unlucky, today's team is won 69 percent of the time on average, and the new ones 95 to 96.

Both new versions carry the three cuts: Anorith with X-Scissor, Water Gun, Rock Tomb and Iron Defense at a Hardy nature (Harden is not legal for it); Sandshrew with Defense Curl for Rapid Spin; Cranidos with a Chople Berry for its Lum. Version (a)'s Naclstack has Stealth Rock, Salt Cure, Smack Down and Mud Shot; version (b)'s has Stealth Rock, Salt Cure and Harden. Both are read with Salt Cure's Expert routine (9a6defeb4e), and the Eviolite fix for later species (e1e547e3a6).

Where the faints fell, summed over the three boxes:

| | Lileep | Cranidos | Others |
|---|---|---|---|
| Today's Roark | 350 | 137 | Larvitar 50, Nosepass 12, Geodude 9 |
| New (a) | 79 | 122 | Naclstack 57, Anorith 44, Sandshrew 12 |
| New (b) | 77 | 153 | Anorith 64, Naclstack 49, Sandshrew 10 |

Nidorino is in all six of the new team's sixes, Bibarel in five and Barboach in four. Today's sixes take Barboach and Bibarel in two of three.

## What it taught

1. **Today's Roark is Lileep.** Its Giga Drain, Big Root and Recover made 350 of the 558 faints the readings charge to a member. The new Lileep (Mega Drain, Toxic, Mirror Coat, Storm Drain) makes about 78, and Nidorino answers it. Cranidos's share is about the same in both. A boss's difficulty can sit in one member, and moving that member's teeth elsewhere moves the fight more than any set elsewhere.
2. **The rough simulator ranks broken sets, not difficulty.** Its player looks one matchup ahead and never plans switches, so the new team's attrition hurt it far more than it hurts the scorer. It read the cut team at 81 to 95 percent on the scorer's boxes, against the scorer's 96 to 100, and today's at 93 to 100, against 87 to 100. Use it for bait tests and to catch a set that does nothing; set a fight's level with the scorer.
3. **Read on the scorer's boxes.** The study read Roark on an old box of its own, built before the learnset rewrite, and its 47 to 65 percent came mostly from that box. The study now reads goal 3's boxes (`~/oxide-trials/kaizo-teams/out/boxes/`).
4. **A move whose worth is its side effect needs an AI routine, or it never fires.** Evaluate Attack docks every attack but the strongest by a point, so the drafted Naclstack never used Salt Cure. It now has a routine, and even so it salts a fresh Barboach only one turn in five, because Mud Shot carries Platinum's own Speed-drop routine. Before a boss is read, check that the AI uses each of its moves.
5. **Check that the scorer reads every new piece before a long reading.** A five-minute check of the prepared fight showed the scorer dropping Naclstack's Eviolite, since its calculator knew no Generation 5+ species as able to evolve. That would have cost a whole reading.

## The next step

Ian decides the next reading. The proposal is to undo the three cuts, since they were chosen on the rough simulator's numbers, and read the team as the study drafted it, with Naclstack as in (b), so that the salt that was the reason for picking it lands. The target is today's level or a little above: high 80s to low 90s won, under the 95 percent ceiling. One reading of three boxes takes about 1.5 to 2 hours on the free machine.
