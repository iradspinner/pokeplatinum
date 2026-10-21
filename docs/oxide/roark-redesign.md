# Roark's redesign: the comparison and what it taught

The scorer read today's Roark and the new team on goal 3's boxes 1 to 3 on 2026-10-12, and the uncut team with Recover on 2026-10-13 (its section below). With the three cuts, the new team reads easier than today's, at 98 to 100 percent won, above Ian's 95 percent ceiling for a boss. The cuts overshot, because they were chosen on the Kaizo study's rough simulator, which here got even the direction wrong. Ian then accepted the uncut team with Recover, read at 86 percent won (the last sections).

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

## The uncut team with Recover (read 2026-10-13)

Ian's next pick: the three cuts undone, and Naclstack with Stealth Rock, Salt Cure, Harden and Recover (Recover is legal from Nacli's new egg list). Read on the same three boxes, with the Nacli line's new lists (89a1100b3).

| | Box 1 | Box 2 | Box 3 | Mean |
|---|---|---|---|---|
| Won at real odds | 81% | 77% | 99% | 86% |
| Faints a fight (difficulty) | 3.08 (10.5) | 3.59 (12.7) | 0.99 (1.5) | 2.55 (8.2) |
| Very unlucky, won | 68% | 84% | 92% | 81% |

Where the faints fell, over the three boxes: Cranidos 171, Lileep 169, Naclstack 117 (95 of them on box 2), Sandshrew 68 (45 on box 1), Anorith 49. Against the cut team (b), the two members that moved most are Naclstack, which Recover keeps on the field to salt, and Sandshrew, with Rapid Spin's Speed raise back. Each box is read on 75 fights at real odds and 25 very unlucky, so a box's numbers move by about five points from noise alone (box 2's very unlucky reading above its real one is that noise).

## The decision

Ian accepted the uncut team with Recover on 2026-10-13 as the right difficulty for Roark, and it is in the game. Gardenia's redesign followed, and her team was locked in the same day (`gardenia-redesign.md`).
