# Double battles in Oxide: which faults are live

Element 6's doubles review (2026-09-22). `other-flags.md` reads the double-battle code line by line: the driver, Tag Strategy's two halves, and the bugs O1 to O19. `switching-and-items.md` does the same for switching. This file asks a narrower question. Given the trainers, parties and flags Oxide actually has, which of those faults and gaps does a player meet, and in which battles? The answer is a short list, and the fixes it proposes wait on Ian, since each one changes how a fight plays.

Line numbers here are the element 6 branch's, since the fixes below would be made there.

## The double battles

The inventory was built from the trainer files and the field scripts, with each party member's moves, ability and types worked out the way the game does (the damage calculator's export, `calc_trainers.py`).

| Kind | Count | Examples |
|---|---|---|
| Trainers who fight a double battle alone | 17, not counting one unused | the Double Teams, Twins, Young Couples, Belle & Pa, Roxy & Oli |
| Two enemy trainers set by a script | 11 pairs | the nine Hotel Grand Lake restaurant pairs, the Iron Island and Spear Pillar Galactic grunts |
| Tag battles, player and partner against two trainers | 4 | Jubilife grunts, Veilstone grunts, Mars and Jupiter, Volkner and Flint |
| AI partners on the player's side | 5 | Cheryl, Riley, Marley, Buck, Mira |

That is 37 battles and 112 AI Pokemon. Two things are not in the count. The field's generic script also starts a double battle when two trainers spot the player at the same time, so more pairs exist, set by where trainers stand on the maps; the findings below apply to any trainer with the moves named, wherever that happens. And wild double battles do not run the AI at all (README, first section), so they are not part of this review.

Three facts narrow the field. No double battle carries the Check HP or Weather flags, so the partner routine never runs twice (other-flags.md) and the Weather flag fix does not reach doubles. Eleven of the battles run on Basic alone, and Tag Strategy, which every double battle forces on, is their only doubles logic. And no double-battle party has any move Oxide added: every move in them exists in vanilla. So the gaps for Oxide's new spread moves (Bulldoze, Sludge Wave, Boomburst and the rest, other-flags.md "Oxide consequences") are real but not yet reachable; they belong with teaching the AI the new moves, once parties use them.

## Live findings

### 1. A lone Pokemon reads its fainted partner's types

Present in vanilla Platinum. Tag Strategy's checks for a move that also hits the partner (Earthquake and Magnitude at line 7148, Surf at 7302, Discharge at 7259, Lava Plume at 7340) never ask whether the partner is still there. When a partner faints and its side has nothing left to send in, its slot stays empty for the rest of the battle, but its types and ability stay in memory, and the checks read them. The code's own comment at 7154 notes half of this ("a solo battler will score Earthquake and Magnitude an additional -3"). The other half is worse: if the fainted partner was Fire, Electric, Poison or Rock, a lone Earthquake user takes -10, which all but rules out its best move for the rest of the fight.

This reaches fourteen Pokemon in ten of the battles. The ones where it bites hardest:

| Battle | Pokemon | Move | After the partner's side is out |
|---|---|---|---|
| Spear Pillar grunts | Golem, Nidoking | Earthquake | -10 if the last partner was Nidoqueen (Poison), -3 if Forretress |
| Double Team Jo and Pat (Victory Road) | Dugtrio, Nidoking | Earthquake | -10 if the last to faint beside them was Nidoqueen or Nidoking, +2 if it was Claydol (Levitate) |
| Mars and Jupiter | Drapion | Earthquake | -3 after Delcatty, Persian, Bronzong or Purugly, +2 after Solrock (Levitate) |
| Iron Island grunts | Solrock | Earthquake | -10 if the second grunt's last Pokemon was Skuntank or Toxicroak (Poison) |
| Double Team Al and Kay, Roxy and Oli's rematches | Tauros, Miltank; Magneton, Magnezone | Earthquake; Discharge | -3, where an empty slot should cost nothing |

The fix is one line at the top of each of the four handlers: `IfBattlerFainted AI_BATTLER_ATTACKER_PARTNER` jumps past the partner checks. That command tests exactly "this slot is permanently empty" (`battlersSwitchingMask`, set in `battle_controller_player.c` at 4137 and 4161 when a fainted battler has no replacement), and at move selection a partner is either alive or permanently gone, since replacements come in at the end of a turn. Partner routine line 7359 already uses it for the same purpose. It is a vanilla fix: the checks plainly mean "the partner", and an empty slot has none.

### 2. Earthquake next to a Steel partner

Present in vanilla Platinum, bug O7. Earthquake's partner check names Fire, Electric, Poison and Rock as weak but not Steel, so a Steel partner gets -3 instead of -10. Live at Spear Pillar: Mars's Bronzong rolls Heatproof, not Levitate, so Jupiter's Drapion can Earthquake it for double damage at only -3. Surf's check has the matching hole for Rock (the code's own comment says so), which reaches Marley's Starmie with a Rock Pokemon of the player's beside it. The fix adds the missing type to each list, with the partner's second type checked as the lists already do. A Bug and Steel partner such as Forretress takes neutral damage from Earthquake, so for accuracy the Steel test should skip a partner that is also Bug or Grass; the simpler version (Steel always -10) is also defensible, and is Ian's call.

### 3. Mold Breaker Earthquake next to a Levitate partner

Present in vanilla Platinum, not in the earlier write-up. Earthquake's partner check gives +2 for a partner with Levitate (line 7157) without asking whether the user has Mold Breaker, which makes Earthquake hit a Levitate ally too. Live in Double Team Jo and Pat: their Nidoking has Mold Breaker and their Claydol has Levitate, so when the two stand together the AI thinks its Earthquake is free and hits Claydol. The fix tests the attacker's Mold Breaker before the Levitate test and, if present, skips to the type checks. The same gap exists for Discharge into a Volt Absorb or Motor Drive partner, Surf into Water Absorb or Dry Skin, and Lava Plume into Flash Fire, but no Oxide party has Mold Breaker alongside those moves, so only Earthquake is live.

### 4. Explosion and Self-Destruct ignore the partner

Present in vanilla Platinum. Both moves hit the user's partner too, but no routine knows it: Basic and Expert look only at the target (`Basic_CheckCannotExplode`, `Expert_Explosion`), and Tag Strategy has no case for them. Live in two battles: the Spear Pillar grunts, where Golem and Forretress both carry Explosion beside Nidoking, Nidoqueen and each other, and Double Team Jo and Pat, where Claydol's Self-Destruct hits Nidoqueen. Nothing in the code intended a partner check here, so adding one is a change, not a fix. The natural shape is the Earthquake table: no change beside a Ghost partner, a penalty otherwise, and nothing when the slot is empty. How large a penalty is a design choice.

### 5. Poison Gas now hits the partner, and the AI does not know

Introduced by Oxide's data, not by its code. Ian's base ROM changed Poison Gas's range from one target to "all adjacent" (`res/moves/poison_gas/data.json`, imported in the Phase 3 carry-over), so in a double battle it poisons the user's own partner too. From Generation 5 on, Poison Gas hits both foes and never the ally; the base ROM changed Smog to "both foes" in the same pass, so the Poison Gas value may be a slip. Live in the Jubilife tag battle, where the first grunt's Stunky (level 13) knows Poison Gas beside the second grunt's Glameow. The AI scores it as if it hit only the target. There are two ways out: correct the range to "both foes" (a data change outside element 6, and Ian's call on whether the base ROM meant it), or teach Tag Strategy a partner check for it as in finding 4.

### 6. Follow Me with no partner left

Present in vanilla Platinum, bug O9. Follow Me's partner bands treat a fainted partner as badly hurt, so a lone Follow Me user scores its largest bonus (+3 at 75% when the user is above 90% HP) for a move that does nothing alone. Live in the restaurant pair Rich Boy Roman and Lady Kylie: Roman has one Pokemon, and once it faints Kylie's Clefairy is alone and favours Follow Me. The fix is the same empty-slot test as finding 1, sending Follow Me to a penalty (-10 would match how Basic treats other moves that cannot work).

## Documented but not live

These are real faults in the doubles code that no current Oxide double battle reaches. They stay on file for when parties change: O4 (Skill Swap to give Levitate), O5 (Solar Power and Sunny Day), O8 (Future Sight's speed ties), O10 (Helping Hand's bonus skipping Electric, Fire and Water moves), O15 and O16 (driver faults behind flags no double battle sets), and O17 (an AI partner's Acupressure; no partner knows it). O18, where a Pokemon on 1 HP out of more than 100 counts as absent, can reach any double battle but only for a turn at a time.

From the switching write-up, two doubles faults can fire in these battles but rarely: an AI partner's "nothing can hit" check tests its moves against itself and the player's Pokemon (switching fault 8), and after a partner's Earthquake hits it, an AI Pokemon may switch to a counter of its own partner (fault 11). Both need an unusual board, and neither is proposed for fixing now.

The AI partners on the player's side (Cheryl, Riley, Marley, Buck, Mira) run Tag Strategy with the player's Pokemon as their partner. Two of their partner cases are deliberate rather than faults: Buck's Torkoal may Will-O-Wisp the player's healthy Guts Pokemon (+5), and any partner may attack the player's Flash Fire, Volt Absorb or Water Absorb Pokemon with the matching type to power it up or heal it, which is what the partner routine is for.

## Proposed, awaiting Ian

| Finding | Kind | Reach in Oxide |
|---|---|---|
| 1. Lone Pokemon reads a fainted partner | vanilla fix | 14 Pokemon in 10 battles, Earthquake and Discharge users once alone |
| 2. Steel missing from Earthquake, Rock from Surf | vanilla fix | Jupiter's Drapion beside Mars's Bronzong; Marley beside a Rock Pokemon |
| 3. Mold Breaker ignored beside Levitate | vanilla fix | Jo and Pat's Nidoking beside their Claydol |
| 4. Explosion and Self-Destruct ignore the partner | change | Spear Pillar grunts, Jo and Pat |
| 5. Poison Gas hits the partner | data (base ROM) or change | the Jubilife tag battle's Stunky |
| 6. Follow Me with no partner | vanilla fix | Lady Kylie's Clefairy |

Each would be its own commit, marked as the earlier fixes are. None is applied yet.
