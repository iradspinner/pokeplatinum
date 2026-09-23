# The Expert flag, part one: dispatch and routines up to Sunny Day

The Expert flag (bit 2, `AI_FLAG_EXPERT`) is the AI's move-by-move judgement. Basic has already thrown out moves that cannot work; Expert then nudges each remaining move up or down by a few points according to what that particular move is for. It looks up the move's battle effect, jumps to one routine written for that effect, and that routine reads the situation (HP, speed order, stat stages, statuses, the foe's last move) and adds or subtracts a small amount, often with a random roll. A move whose effect has no routine gets nothing from Expert. Expert now runs for 559 of Oxide's 747 trainers, so these routines are most of the game's AI personality.

This file covers `src/battle/trainer_ai/script.s` lines 1623 to 3802: the dispatcher `Expert_Main` and the 64 routines from `Expert_StatusSleep` to `Expert_SunnyDay`. `expert-2.md` covers lines 3803 to 6352. `script.s` is byte-identical to vanilla `main`, so every script line number here is also the vanilla line. The C line numbers are from `src/battle/trainer_ai/trainer_ai.c` in this tree, whose only change from vanilla is two lines in `AI_HasAbsorbAbilityInParty` (3645 to 3646), outside anything used here.

## Reading the tables

**Chances.** Every random check is `IfRandomLessThan N, label`, which draws a number from 0 to 255 and jumps past the change when the draw is below N (`AICmd_IfRandomLessThan`, C lines 528 to 538). So the change happens with chance (256 minus N) out of 256. The values used in this half:

| N | Chance the change happens |
|---|---|
| 10 | 96.1% |
| 20 | 92.2% |
| 30 | 88.3% |
| 32 | 87.5% |
| 40 | 84.4% |
| 50 | 80.5% |
| 51 | 80.1% |
| 60 | 76.6% |
| 64 | 75.0% |
| 70 | 72.7% |
| 80 | 68.75% |
| 96 | 62.5% |
| 100 | 60.9% |
| 128 | 50.0% |
| 180 | 29.7% |
| 192 | 25.0% |
| 200 | 21.9% |

Two rolls in a row multiply: a 68.75% roll that leads into another 68.75% roll gives 47.3%. In two places the jump goes *to* the change instead of past it, so the chance is N out of 256: line 2623 (Conversion, N 200, 78.1%) and line 3564 (Protect, N 85, 33.2%).

**The user and the foe.** "User" is the AI's Pokemon (`AI_BATTLER_ATTACKER`), "foe" is the target being scored against (`AI_BATTLER_DEFENDER`).

**HP.** Percentages are `curHP * 100 / maxHP` rounded down (C lines 588 to 646). "Above 50%" therefore means the computed figure is 51 or more, and "full HP" (exactly 100) means no damage at all.

**Stat stages.** The engine stores a stage as 0 to 12 with 6 as neutral. The script compares the stored number, so `IfStatStageLessThan ..., 9` means "below +3" and `IfStatStageGreaterThan ..., 8` means "+3 or higher". The tables give the stage in the usual plus and minus form.

**Speed.** "Slower" means `BattleSystem_CompareBattlerSpeed(user, foe)` returned `COMPARE_SPEED_SLOWER` (C lines 1102 to 1112; `battle_lib.c` lines 1188 onwards). It is a real turn-order check with move priority ignored: it counts Trick Room (under which the faster Pokemon is "slower"), Stall, Lagging Tail, Quick Claw and Custap Berry as the engine would. A speed tie comes back as faster or as tie, never as slower, so every "if slower" check treats a tie as faster.

**What the AI knows about the foe.** "The foe knows move X" (`IfMoveKnown` and `IfMoveEffectKnown` on the defender, C lines 1627 to 1821) means the foe has used X in front of the AI since it came in (`battlerMoves`, filled by `TrainerAI_RecordLastMove`, C lines 2706 to 2717). For the user it means any of its four moves, PP or not. The foe's held item is likewise only the item the battle has revealed (`battlerHeldItems`, C lines 1901 to 1913). The foe's last move (`LoadBattlerPreviousMove`) is `movePrevByBattler`, which is 0 until the foe has moved since switching in.

**Type effectiveness.** `IfMoveEffectivenessEquals` (C lines 1311 to 1346) runs the engine's type chart for this move against the foe and compares the result with one exact value. Plain STAB (1.5) is divided back out, and Levitate or Magnet Rise against a Ground move counts as immune. Nothing else is normalised: an Adaptability user's neutral STAB move comes out equal to "double damage", an Expert Belt or Filter changes the number so that a super-effective move matches nothing, and Wonder Guard does not count as immune. "Resisted" in the tables means the result equalled quarter, half or immune.

**How a routine ends.** Every routine ends with `PopOrEnd`. Expert never pushes onto the script stack, so `PopOrEnd` always ends Expert's work on this move (C lines 2568 to 2577). "End" in the tables means that.

## How Expert_Main dispatches (lines 1623 to 1811)

Line 1625 (`IfTargetIsPartner Terminate`) ends Expert at once when the target is on the user's own side, which only happens in doubles (C lines 2630 to 2639 compare the low bit of the two battler ids). Expert adds nothing to moves aimed at the partner.

Lines 1628 to 1808 are 181 tests of the form `IfCurrentMoveEffectEqualTo EFFECT, Routine`. Each reads the `effect` field of the current move's data (C lines 1441 to 1451) and, if it matches, jumps (not calls) to the routine. The tests run top to bottom and the first match wins, so a move reaches exactly one routine or none. Line 1811 ends Expert for any effect not listed. The consequences:

1. Routines are shared. Several effects point at one routine (Memento uses the Explosion routine; Tickle uses Defense Down; Calm Mind, Cosmic Power and Defend Order use Special Defense Up; Mean Look, Block and Spider Web use the binding-move routine). The table below lists every mapping.
2. A second test for an effect already tested is dead. Line 1719 repeats line 1716's effect, so it never fires (the Thunder bug below).
3. Effects that no move has are harmless dead entries: `UNUSED_133`, `UNUSED_134` (1708, 1709), `UNUSED_157` (1722), and `ACC_UP`, `ACC_UP_2`, `SPEED_UP`, `SP_DEF_UP`, `SP_DEF_DOWN`, `EVA_UP_2`, `EVA_DOWN_2` and `ACC_DOWN_2`, which no move uses in vanilla or in Oxide. `SP_ATK_DOWN` and `SP_ATK_DOWN_2` had no move in vanilla but do in Oxide.
4. The routine names are the decomp's, not the game's, and one misleads: `Expert_Nightmare` is reached only by `DAMAGE_WHILE_ASLEEP`, which is Snore. Nightmare itself (`STATUS_NIGHTMARE`) has no Expert routine.

The mapping for routines in this half. The last column is moves Oxide added to an effect that already had a routine (checked against every `res/moves/*/data.json` here and on `main`); they inherit the routine unchanged.

| Routine (line) | Dispatch lines | Effects | Vanilla moves | Oxide additions |
|---|---|---|---|---|
| StatusSleep (1813) | 1628 | STATUS_SLEEP | Dark Void, Grass Whistle, Hypnosis, Lovely Kiss, Sing, Sleep Powder, Spore | |
| DrainMove (1827) | 1629 | RECOVER_HALF_DAMAGE_DEALT | Absorb, Drain Punch, Giga Drain, Leech Life, Mega Drain | Bitter Blade, Horn Leech, Parabolic Charge |
| Explosion (1841) | 1630, 1728 | HALVE_DEFENSE, FAINT_AND_ATK_SP_ATK_DOWN_2 | Explosion, Selfdestruct, Memento | Misty Explosion |
| DreamEater (1886) | 1631 | RECOVER_DAMAGE_SLEEP | Dream Eater | |
| MirrorMove (1907) | 1632 | COPY_MOVE | Mirror Move | |
| StatusAttackUp (1978) | 1633, 1663 | ATK_UP, ATK_UP_2 | Howl, Meditate, Sharpen, Swords Dance | |
| StatusDefenseUp (2009) | 1634, 1664, 1753 | DEF_UP, DEF_UP_2, ATK_DEF_UP | Harden, Withdraw, Acid Armor, Barrier, Iron Defense, Bulk Up | Shelter |
| StatusSpeedUp (2066) | 1635, 1665 | SPEED_UP, SPEED_UP_2 | Agility, Rock Polish | |
| StatusSpAttackUp (2081) | 1636, 1666 | SP_ATK_UP, SP_ATK_UP_2 | Growth, Nasty Plot, Tail Glow | |
| StatusSpDefenseUp (2112) | 1637, 1667, 1752, 1756 | SP_DEF_UP, SP_DEF_UP_2, DEF_SPD_UP, SP_ATK_SP_DEF_UP | Amnesia, Cosmic Power, Defend Order, Calm Mind | |
| StatusAccuracyUp (2169) | 1638, 1668 | ACC_UP, ACC_UP_2 | none | |
| StatusEvasionUp (2184) | 1639, 1669, 1699 | EVA_UP, EVA_UP_2, EVA_UP_2_MINIMIZE | Double Team, Minimize | |
| BypassAccuracyMove (2256) | 1640 | BYPASS_ACCURACY | Aerial Ace, Aura Sphere, Faint Attack, Magical Leaf, Magnet Bomb, Shadow Punch, Shock Wave, Swift | Disarming Voice, False Surrender, Kowtow Cleave, Smart Strike |
| StatusAttackDown (2277) | 1641, 1670 | ATK_DOWN, ATK_DOWN_2 | Growl, Charm, Feather Dance | Baby-Doll Eyes, Play Nice |
| StatusDefenseDown (2318) | 1642, 1671, 1751 | DEF_DOWN, DEF_DOWN_2, ATK_DEF_DOWN | Leer, Tail Whip, Screech, Tickle | |
| SpeedDownOnHit (2338) | 1681 | LOWER_SPEED_HIT | Bubble, Bubble Beam, Constrict, Icy Wind, Mud Shot, Rock Tomb | Bulldoze, Drum Beating, Electroweb, Glaciate, Low Sweep, Max Strike, Pounce |
| StatusSpeedDown (2353) | 1643, 1672 | SPEED_DOWN, SPEED_DOWN_2 | String Shot, Cotton Spore, Scary Face | |
| StatusSpAttackDown (2368) | 1644, 1673 | SP_ATK_DOWN, SP_ATK_DOWN_2 | none | Confide, Eerie Impulse |
| StatusSpDefenseDown (2411) | 1645, 1674 | SP_DEF_DOWN, SP_DEF_DOWN_2 | Fake Tears, Metal Sound | |
| StatusAccuracyDown (2431) | 1646, 1675 | ACC_DOWN, EVA_DOWN_2 | Flash, Kinesis, Sand-Attack, Smokescreen | |
| StatusEvasionDown (2500) | 1647, 1676 | EVA_DOWN, ACC_DOWN_2 | Sweet Scent | |
| Haze (2520) | 1648 | RESET_STAT_CHANGES | Haze | |
| Bide (2566) | 1649 | BIDE | Bide | |
| ForceSwitch (2574) | 1650 | FORCE_SWITCH | Roar, Whirlwind | |
| Conversion (2613) | 1651 | CONVERSION | Conversion | |
| Synthesis (2628) | 1707, 1708, 1709 | HEAL_HALF_MORE_IN_SUN, UNUSED_133, UNUSED_134 | Moonlight, Morning Sun, Synthesis | Shore Up |
| Recovery (2640) | 1652, 1722, 1725, 1758 | RESTORE_HALF_HP, UNUSED_157, SWALLOW, HEAL_HALF_REMOVE_FLYING_TYPE | Heal Order, Milk Drink, Recover, Slack Off, Softboiled, Swallow, Roost | |
| ToxicLeechSeed (2680) | 1653, 1686 | STATUS_BADLY_POISON, STATUS_LEECH_SEED | Toxic, Leech Seed | |
| LightScreen (2710) | 1654 | SET_LIGHT_SCREEN | Light Screen | |
| Rest (2745) | 1655 | REST | Rest | |
| OHKOMove (2792) | 1656 | ONE_HIT_KO | Fissure, Guillotine, Horn Drill, Sheer Cold | |
| SuperFang (2800) | 1658 | HALVE_HP | Super Fang | Nature's Madness, Ruination |
| BindingMove (2808) | 1659, 1698 | BIND_HIT, PREVENT_ESCAPE | Bind, Clamp, Fire Spin, Magma Storm, Sand Tomb, Wrap, Block, Mean Look, Spider Web | Infestation |
| HighCritical (2827) | 1660, 1748, 1754 | HIGH_CRITICAL, HIGH_CRITICAL_BURN_HIT, HIGH_CRITICAL_POISON_HIT | Aeroblast, Air Cutter, Attack Order, Crabhammer, Cross Chop, Karate Chop, Leaf Blade, Night Slash, Psycho Cut, Razor Leaf, Shadow Claw, Slash, Spacial Rend, Stone Edge, Blaze Kick, Cross Poison, Poison Tail | Aqua Cutter, Drill Run, Snipe Shot (Oxide moved Attack Order to POISON_HIT) |
| Swagger (2845) | 1680 | ATK_UP_2_STATUS_CONFUSION | Swagger | |
| Flatter (2854) | 1727 | SP_ATK_UP_CAUSE_CONFUSION | Flatter | |
| StatusConfuse (2861) | 1662 | STATUS_CONFUSE | Confuse Ray, Supersonic, Sweet Kiss | |
| Reflect (2893) | 1677 | SET_REFLECT | Reflect | |
| StatusPoison (2929) | 1678 | STATUS_POISON | Poison Gas, Poison Powder | |
| StatusParalyze (2940) | 1679 | STATUS_PARALYZE | Glare, Stun Spore, Thunder Wave | |
| VitalThrow (2956) | 1683 | PRIORITY_NEG_1_BYPASS_ACCURACY | Vital Throw | |
| Substitute (2976) | 1684 | SET_SUBSTITUTE | Substitute | |
| RechargeTurn (3044) | 1685 | RECHARGE_AFTER | Blast Burn, Frenzy Plant, Giga Impact, Hydro Cannon, Hyper Beam, Roar of Time, Rock Wrecker | Eternabeam, Meteor Assault, Prismatic Laser |
| Disable (3075) | 1687 | DISABLE | Disable | |
| Counter (3095) | 1688 | COUNTER | Counter | |
| Encore (3177) | 1689 | ENCORE | Encore | |
| PainSplit (3287) | 1690 | AVERAGE_HP | Pain Split | |
| Nightmare (3314) | 1691 | DAMAGE_WHILE_ASLEEP | Snore | |
| LockOn (3319) | 1692 | NEXT_ATTACK_ALWAYS_HITS | Lock-On, Mind Reader | |
| SleepTalk (3327) | 1693 | USE_RANDOM_LEARNED_MOVE_SLEEP | Sleep Talk | |
| DestinyBond (3335) | 1694 | KO_MON_THAT_DEFEATED_USER | Destiny Bond | |
| Reversal (3362) | 1695 | INCREASE_POWER_WITH_LESS_HP | Flail, Reversal | |
| HealBell (3398) | 1696 | CURE_PARTY_STATUS | Aromatherapy, Heal Bell | |
| Thief (3408) | 1697 | STEAL_HELD_ITEM | Covet, Thief | |
| Curse (3452) | 1700 | CURSE | Curse | |
| Protect (3502) | 1701 | PROTECT | Detect, Protect | Baneful Bunker, Burning Bulwark, King's Shield, Max Guard, Obstruct, Silk Trap, Spiky Shield |
| Spikes (3591) | 1702 | SET_SPIKES | Spikes | |
| Foresight (3608) | 1703 | FORESIGHT | Foresight, Odor Sleuth | |
| Endure (3633) | 1704 | SURVIVE_WITH_1_HP | Endure | |
| BatonPass (3651) | 1705 | PASS_STATS_AND_STATUS | Baton Pass | |
| Pursuit (3706) | 1706 | HIT_BEFORE_SWITCH | Pursuit | |
| RainDance (3737) | 1710 | WEATHER_RAIN | Rain Dance | |
| SunnyDay (3773) | 1711 | WEATHER_SUN | Sunny Day | |

Dispatch entries whose routines are in `expert-2.md` (routine line in brackets): Belly Drum 1712 (3803); Psych Up 1713 (3814); Mirror Coat 1714 (3852); the non-invulnerable charge moves 1657, 1682, 1715, 1716 (ChargeTurnNoInvuln, 3933: Razor Wind, Sky Attack, Skull Bash, Solar Beam, plus Oxide's Solar Blade); the dead Thunder entry 1719 (3975); Fly, Dive, Dig, Bounce 1721, 1797, 1798, 1803 (3992); Shadow Force 1808 (4014, plus Oxide's Phantom Force); the recoil moves 1661, 1747, 1796, 1802, 1806 (RecoilMove, 6289); Healing Wish and Lunar Dance 1764, 1807 (6307); and one entry each at lines 1723, 1724, 1726, 1729 to 1746, 1749, 1750, 1755, 1757, 1759 to 1795, 1799 to 1801, 1804 and 1805, for Fake Out through Stealth Rock.

Vanilla move effects with no Expert entry at all, so Expert leaves them alone: every plain damaging effect and every "chance of X on hit" effect (burn, freeze, paralysis, poison, flinch, confusion and stat-drop on hit), multi-hit and fixed-damage moves, priority moves, and these status or special moves: Mist, Focus Energy, Transform, Mimic, Metronome, Splash, Conversion 2, Sketch, Spite, Nightmare, Perish Song, Sandstorm, Rollout and Ice Ball, Fury Cutter, Attract, Safeguard, Rapid Spin, Hidden Power, Future Sight and Doom Desire, Teleport, Beat Up, Defense Curl, Uproar, Stockpile, Torment, Will-O-Wisp, Follow Me, Nature Power, Charge, Taunt, Helping Hand, Wish, Assist, Yawn, Grudge, Teeter Dance, Weather Ball, Camouflage, Natural Gift, Whirlpool, Chatter, Judgment, Seed Flare, Charge Beam, Thunder (see the bug) and the three elemental fangs.

## The routines

### Sleep and moves that need sleep

**StatusSleep (1813 to 1825).** Sleep-inducing moves.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User knows a Dream Eater or Nightmare move | +1 | 50% | 1816 to 1822 |

**DreamEater (1886 to 1905).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe resists or is immune | -1, end | always | 1890 to 1892, 1901 to 1902 |
| Otherwise, foe asleep | +3 | 80.1% | 1893, 1896 to 1898 |

**Nightmare (3314 to 3317), which is Snore.** Always +2 (line 3316). Basic already punishes Snore when the user is awake, so this bonus only matters while asleep.

**SleepTalk (3327 to 3333).** User asleep: +10 through the shared `ScorePlus10` at lines 1619 to 1621 (jump at 3331). Otherwise -5 (3332).

### Draining and self-KO moves

**DrainMove (1827 to 1839).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe resists or is immune | -3 | 80.5% | 1829 to 1836 |

**Explosion (1841 to 1884).** Explosion, Selfdestruct and Memento. The rows add up; the HP rows are exclusive except the last.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe's evasion +1 or higher | -1 | always | 1856 to 1857 |
| Foe's evasion +4 or higher (on top of the row above) | -1 | 50% | 1858 to 1860 |
| User HP 80% or more and user not slower | -3, end | 80.5% | 1863 to 1866 (shared `ScoreMinus3`, 1575) |
| Otherwise, user HP above 50% | -1 | 80.5% | 1869, 1879 to 1881 |
| User HP 50% or less | +1 | 50% | 1870 to 1871 |
| User HP 30% or less (as well as the row above) | +1 | 80.5% | 1874 to 1876 |

At 30% HP or less the two bonuses are independent, so the routine gives +2 with 40.2% chance, +1 with 50%, and nothing with 9.8%.

### Copying

**MirrorMove (1907 to 1926).** The table at 1928 to 1976 holds 47 move ids (the sleep moves, Toxic, the OHKO moves, accuracy and stat-lowering moves, Shadow Ball, Hyper Beam, Extreme Speed, Superpower, Thief, Covet, Swagger, Trick, Skill Swap, Sucker Punch, the swap moves, Dark Void and others).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not slower and the foe's last move is in the table | +2 | 50% | 1912 to 1916 |
| The foe's last move is not in the table (either speed) | -1 | 68.75% | 1919 to 1923 |
| User slower and the foe's last move is in the table | none | | 1921 |

### Raising the user's stats

**StatusAttackUp (1978 to 2007).** Howl, Meditate, Sharpen, Swords Dance.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Own Attack +3 or higher (skips the next row) | -1 | 60.9% | 1988 to 1991 |
| Own Attack below +3 and full HP | +2 | 50% | 1993 to 1996 |
| HP above 70% | no more changes | | 1999 |
| HP below 40% | -2 | always | 2000, 2003 to 2004 |
| HP 40% to 70% | -2 | 84.4% | 2001 to 2004 |

**StatusSpAttackUp (2081 to 2110).** Growth, Nasty Plot, Tail Glow. Identical in shape to Attack Up on the Special Attack stage (2091 to 2099), except that the 40% to 70% band gives -2 with 72.7% chance (line 2104), not 84.4%.

**StatusDefenseUp (2009 to 2052).** Harden, Withdraw, Acid Armor, Barrier, Iron Defense, Bulk Up (and Oxide's Shelter).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Own Defense +3 or higher (skips the next row) | -1 | 60.9% | 2022 to 2025 |
| Own Defense below +3 and full HP | +2 | 50% | 2027 to 2030 |
| HP 70% or more: stop here with 78.1% chance, otherwise carry on to the rows below | | | 2033 to 2034 |
| HP below 40% | -2 | always | 2037, 2048 to 2049 |
| Foe's last move had power 0 (a status move, or no move yet) | -2 | 76.6% | 2038 to 2040, 2046 to 2049 |
| Foe's last move was special | -2 | always | 2041 to 2042 |
| Foe's last move was physical | -2 | 58.6% (two 76.6% rolls) | 2043 to 2049 |

The label `Expert_StatusDefenseUp_UserAtLowHP` (2045) is misnamed; it is the status-move case.

**StatusSpDefenseUp (2112 to 2155).** Amnesia, Cosmic Power, Defend Order, Calm Mind. The same as Defense Up on the Special Defense stage (2125 to 2133), with physical and special swapped: foe's last move physical gives -2 always (2144 to 2145), special gives -2 with 58.6% (2146 to 2152). Calm Mind and Cosmic Power are judged purely as Special Defense boosts. `Expert_StatusSpDefenseUp_TryScoreMinus2` (2151) is an unconditional -2 despite its name.

**StatusSpeedUp (2066 to 2079).** Agility, Rock Polish.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not slower | -3 | always | 2070 to 2071 |
| User slower | +3 | 72.7% | 2074 to 2076 |

**StatusAccuracyUp (2169 to 2182).** No move in vanilla or Oxide reaches it.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Own accuracy +3 or higher | -2 | 80.5% | 2173 to 2175 |
| HP 70% or less | -2 | always | 2178 to 2179 |

**StatusEvasionUp (2184 to 2254).** Double Team, Minimize. All rows add.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| HP 90% or more | +3 | 60.9% | 2203 to 2205 |
| Own evasion +3 or higher | -1 | 50% | 2208 to 2210 |
| Foe badly poisoned, user HP above 50% | +3 | 80.5% | 2213 to 2214, 2217 to 2219 |
| Foe badly poisoned, user HP 50% or less | +3 | 55.3% | 2215 to 2219 |
| Foe seeded by Leech Seed | +3 | 72.7% | 2222 to 2224 |
| User has Ingrain | +2 | 50% | 2227 to 2230 |
| Otherwise, user has Aqua Ring | +2 | 50% | 2232 to 2236 |
| Foe cursed (Ghost Curse) | +3 | 72.7% | 2239 to 2241 |
| Final block, only if HP 70% or less and own evasion is not exactly +0: user or foe HP below 40% | -2 | always | 2244 to 2247, 2250 to 2251 |
| Final block otherwise | -2 | 72.7% | 2248 to 2251 |

"Badly poisoned" is the Toxic status bit only; ordinary poison does not count. The best case is +14, the largest single gain in this half.

### Moves that cannot miss

**BypassAccuracyMove (2256 to 2275).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe's evasion +5 or higher, or own accuracy -5 or lower | +1, then a further +1 | always, then 60.9% | 2261 to 2262, 2267 to 2272 |
| Otherwise, foe's evasion +3 or higher, or own accuracy -3 or lower | +1 | 60.9% | 2263 to 2264, 2270 to 2272 |

### Lowering the foe's stats

**StatusAttackDown (2277 to 2307).** Growl, Charm, Feather Dance (and Oxide's Baby-Doll Eyes, Play Nice).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe's Attack stage anything but +0 (raised or lowered) | -1 | always | 2286 to 2287 |
| That, and user HP 90% or less | -1 | always | 2288 to 2289 |
| That, and foe's Attack -3 or lower | -2 | 80.5% | 2292 to 2294 |
| Foe HP 70% or less | -2 | always | 2297 to 2298 |
| Foe's last move was special | -2 | 50% | 2301 to 2304 |

**StatusSpAttackDown (2368 to 2398).** No move reached it in vanilla; in Oxide, Confide and Eerie Impulse do. The same shape on the Special Attack stage (2377 to 2389), with the last row reading "foe's last move was physical" (2392 to 2395). Because "no move yet" reads as physical (see the bugs), this routine gives a 50% chance of -2 whenever the foe has not yet moved.

**StatusDefenseDown (2318 to 2336).** Leer, Tail Whip, Screech, Tickle.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User HP below 70% | -2 | 80.5% | 2324, 2327 to 2329 |
| Otherwise, foe's Defense -3 or lower | -2 | 80.5% | 2325, 2327 to 2329 |
| Foe HP 70% or less | -2 | always | 2332 to 2333 |

**StatusSpDefenseDown (2411 to 2429)** (Fake Tears, Metal Sound) and **StatusEvasionDown (2500 to 2518)** (Sweet Scent) have exactly the Defense Down shape, on the Special Defense stage (2417 to 2426) and the evasion stage (2506 to 2515).

**SpeedDownOnHit (2338 to 2351).** Every damaging move with a chance to lower Speed.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe resists or is immune | none, end | | 2342 to 2344 |
| The move is Icy Wind, Rock Tomb or Mud Shot (by move id) | scored as Speed Down below | | 2345 to 2347 |
| Any other such move | none | | 2348 |

**StatusSpeedDown (2353 to 2366).** String Shot, Cotton Spore, Scary Face, and the three moves above.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not slower | -3 | always | 2357 to 2358 |
| User slower | +2 | 72.7% | 2361 to 2363 |

**StatusAccuracyDown (2431 to 2498).** Flash, Kinesis, Sand-Attack, Smokescreen. All rows add.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User HP below 70%, or foe HP 70% or less | -1 | 60.9% | 2449 to 2454 |
| User's own accuracy -2 or lower | -2 | 68.75% | 2457 to 2459 |
| Foe badly poisoned | +2 | 72.7% | 2462 to 2464 |
| Foe seeded | +2 | 72.7% | 2467 to 2469 |
| User has Ingrain, or otherwise Aqua Ring | +1 | 50% | 2472 to 2480 |
| Foe cursed | +2 | 72.7% | 2483 to 2485 |
| Final block, only if user HP 70% or less and the foe's accuracy is not exactly +0: user or foe HP below 40% | -2 | always | 2488 to 2491, 2494 to 2495 |
| Final block otherwise | -2 | 72.7% | 2492 to 2495 |

### Haze

**Haze (2520 to 2564).** Both of the first two rows can apply.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Any of the user's Attack, Defense, Sp. Atk, Sp. Def, evasion at +3 or higher, or any of the foe's Attack, Defense, Sp. Atk, Sp. Def, accuracy at -3 or lower | -3 | 80.5% | 2528 to 2542 |
| Any of the foe's Attack, Defense, Sp. Atk, Sp. Def, evasion at +3 or higher, or any of the user's Attack, Defense, Sp. Atk, Sp. Def, accuracy at -3 or lower | +3 | 80.5% | 2545 to 2554, 2559 to 2561 |
| Neither of the second row's conditions | -1 | 80.5% | 2555 to 2556 |

Speed stages are never looked at, on either side.

### Bide, phazing, Conversion

**Bide (2566 to 2572).** User HP 90% or less: -2 (2568 to 2569).

**ForceSwitch (2574 to 2611).** Roar, Whirlwind. "Turns on the field" is `LoadBattlerTurnCount`, the battle's turn counter minus the foe's Fake Out marker (C lines 2096 to 2104), which counts the full turns the foe has been in: 0 on its first turn.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe on the field more than 3 turns | +2, then another +2 | 75%, then 50% (independent) | 2589 to 2590, 2602 to 2608 |
| Otherwise, Spikes, Stealth Rock or Toxic Spikes on the foe's side, or any of the foe's Attack, Defense, Sp. Atk, Sp. Def, evasion at +3 or higher | +2 | 50% | 2591 to 2598, 2606 to 2608 |
| None of those | -3 | always | 2599 |

**Conversion (2613 to 2626).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User HP 90% or less | -2 | always | 2617 to 2618 |
| Not the battle's first turn (battle-wide counter, not the user's) | -2 | 78.1% | 2621 to 2623 (shared `ScoreMinus2`, 1571) |

### Healing

**Synthesis (2628 to 2638).** Synthesis, Morning Sun, Moonlight (and Oxide's Shore Up). Hail, rain or sandstorm: -2 (2631 to 2638). Then it runs the Recovery routine below. Fog is not checked.

**Recovery (2640 to 2678).** Recover, Softboiled, Milk Drink, Slack Off, Heal Order, Roost, Swallow, and the Synthesis group.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Full HP | -3, end | always | 2649, 2659 to 2661 |
| User not slower | -8, end | always | 2650 to 2652 |
| User slower, HP 70% or more | -3, end | 88.3% | 2663 to 2667 |
| Otherwise (slower and HP below 70%, or the 11.7% that escaped the row above), foe has not shown a Snatch | +2 | 92.2% | 2670, 2673 to 2675 |
| As above, but the foe has shown Snatch | +2 | 56.2% | 2670 to 2675 |

Lines 2654 to 2657 (`Expert_Recovery_Unused`) are never reached; see the bugs.

**Rest (2745 to 2790).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not slower, full HP | -8, end | always | 2758 to 2761 |
| User not slower, HP above 50% | -3, end | always | 2765, 2768 to 2770 |
| User not slower, HP 40% to 50% | -3, end | 72.7% | 2766 to 2770 |
| User slower, HP above 70% | -3, end | always | 2774, 2777 to 2779 |
| User slower, HP 60% to 70% | -3, end | 80.5% | 2775 to 2779 |
| Everything that reached the Snatch check (not slower with HP below 40%, slower with HP below 60%, or escaped a roll above), foe has not shown Snatch | +3 | 96.1% | 2764, 2773, 2782, 2785 to 2787 |
| As above, foe has shown Snatch | +3 | 77.3% | 2782 to 2787 |

### Residual damage

**ToxicLeechSeed (2680 to 2708).** Toxic, Leech Seed.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User has a damaging move, and user HP 50% or less | -3 | 80.5% | 2688 to 2691 |
| User has a damaging move, and foe HP 50% or less | -3 | 80.5% | 2694 to 2696 |
| User knows a SP_DEF_UP move (none exists) or a Protect-family move | +2 | 76.6% | 2699 to 2705 |

"Has a damaging move" is any of its four moves with nonzero base power, PP or not (C lines 913 to 929).

**BindingMove (2808 to 2825).** The binding moves and the trapping status moves (Mean Look, Block, Spider Web).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe badly poisoned, cursed, under Perish Song, or infatuated | +1 | 50% | 2814 to 2822 |

### Screens

**LightScreen (2710 to 2732).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User HP below 50% | -2, end | always | 2716, 2728 to 2729 |
| User HP 90% or more | +1 | 50% | 2717 to 2719 |
| Foe's last move was special | +1 | 75% | 2722 to 2725 |

**Reflect (2893 to 2915).** The same, with "foe's last move was physical" (2905 to 2908). Because "no move yet" reads as physical, Reflect gets this bonus before the foe has moved and Light Screen does not.

The tables `Expert_LightScreen_PreSplitSpecialTypes` (2734), `Expert_Reflect_PreSplitPhysicalTypes` (2917), and the three like them after Defense Up (2054), Special Defense Up (2157), Attack Down (2309) and Special Attack Down (2400) are never referenced. They are left over from Gen 3, where a move's type decided whether it was physical or special.

### Fixed and critical-hit damage

**OHKOMove (2792 to 2798).** +1 with 25% chance (2794 to 2795).

**SuperFang (2800 to 2806).** Foe HP 50% or less: -1 (2802 to 2803).

**HighCritical (2827 to 2843).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe resists or is immune | none, end | | 2831 to 2833 |
| Super effective (double or quadruple) | +1 | 50% | 2834 to 2835, 2838 to 2840 |
| Anything else (neutral, or an effectiveness value that matches nothing) | +1 | 25% | 2836 to 2840 |

**RechargeTurn (3044 to 3073).** Hyper Beam and the other recharge moves.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe resists or is immune | -1, end | always | 3052 to 3054, 3069 to 3070 |
| User's own ability is Truant | +1, end | 68.75% | 3055 to 3056, 3061 to 3063 |
| User slower, HP 60% or more | -1 | always | 3057, 3066 to 3070 |
| User not slower, HP above 40% | -1 | always | 3058, 3069 to 3070 |

**VitalThrow (2956 to 2974).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User slower, or HP above 60% | none | | 2964 to 2965 |
| HP below 40% | -1 | 80.5% | 2966, 2969 to 2971 |
| HP 40% to 60% | -1 | 23.9% | 2967 to 2971 |

### Confusion

**Swagger (2845 to 2852, 2879 to 2891).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User knows Psych Up and the foe's Attack is -2 or higher | -5, end | always | 2852, 2880, 2887 to 2888 |
| User knows Psych Up and the foe's Attack is -3 or lower | +3, and +2 more on the battle's first turn | always | 2880 to 2884 |
| User does not know Psych Up | scored as Flatter below | | 2852 falls through to 2854 |

**Flatter (2854 to 2859).** +1 with 50% chance, then the confusion routine below.

**StatusConfuse (2861 to 2877).** Confuse Ray, Supersonic, Sweet Kiss, and the tail of Flatter and Swagger.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe HP above 70% | none, end | | 2863 |
| Foe HP 70% or less | -1 | 50% | 2864 to 2865 |
| Foe HP 50% or less | -1 | always | 2871 to 2872 |
| Foe HP 30% or less | -1 | always | 2873 to 2874 |

### Poison and paralysis

**StatusPoison (2929 to 2938).** User HP below 50%, or foe HP 50% or less: -1 (2931 to 2935).

**StatusParalyze (2940 to 2954).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User slower | +3 | 92.2% | 2944, 2949 to 2951 |
| User not slower and HP 70% or less | -1 | always | 2945 to 2946 |

### Substitute, Disable, Counter, Encore

**Substitute (2976 to 3042).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User knows Focus Punch (by move id) | +1 | 62.5% | 2994 to 2996 |
| User HP 71% to 90% | -1, one roll | 60.9% | 3000, 3009 to 3011 |
| User HP 51% to 70% | -1, two rolls | 60.9% each | 3001, 3005 to 3011 |
| User HP 50% or less | -1, three rolls | 60.9% each | 3002 to 3011 |
| User not slower, foe's last move was a sleep, poison, Toxic, paralysis or burn status move, and the foe has no status | +1 | 60.9% | 3014 to 3021, 3026 to 3027, 3037 to 3039 |
| Same, foe's last move was a confusion move and the foe is not confused | +1 | 60.9% | 3022, 3030 to 3031, 3037 to 3039 |
| Same, foe's last move was Leech Seed and the foe is not seeded | +1 | 60.9% | 3023, 3034 to 3039 |

The last three rows read the foe's own condition; see the bugs.

**Disable (3075 to 3093).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User slower | none | | 3081 |
| Foe's last move had power 0 (status, or no move yet) | -1 | 60.9% | 3082 to 3084, 3088 to 3090 |
| Foe's last move was damaging | +1 | always | 3085 |

**Counter (3095 to 3163).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe asleep, infatuated or confused | -1, end | always | 3112 to 3114, 3159 to 3160 |
| User HP 30% or less | -1 | 96.1% | 3115 to 3117 |
| User HP 50% or less (stacks with the row above) | -1 | 60.9% | 3120 to 3122 |
| User also knows Mirror Coat | +4, end | 60.9% | 3125, 3152 to 3154 |
| Foe's last move had power 0, and the foe is taunted | +1 | 60.9% | 3128, 3140 to 3143 |
| Foe's last move had power 0, and neither of the foe's types is in the "physical types" list | +4 | 49.0% | 3145 to 3154 |
| Foe's last move was damaging, and the foe is taunted | +1 | 60.9% | 3129 to 3131 |
| Foe's last move was damaging and not physical | -1, end | always | 3134 to 3135, 3159 to 3160 |
| Foe's last move was physical | +1 | 60.9% | 3136 to 3137 |

The physical-types list (3165 to 3175) is Normal, Fighting, Flying, Poison, Ground, Rock, Bug, Ghost, Steel.

**Encore (3177 to 3285).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe is currently Disabled | +3 | 88.3% | 3185, 3191 to 3193 |
| Otherwise, user slower | -2 | always | 3186, 3196 to 3197 |
| Otherwise, the effect of the foe's last move is not in the list | -2 | always | 3187 to 3189, 3196 to 3197 |
| Otherwise | +3 | 88.3% | 3191 to 3193 |

The list (3202 to 3285) has 82 entries, the status and setup effects that are bad to be locked into (stat boosts, screens, weather, Protect, Rest, Toxic, Leech Seed, Splash and so on). `SWITCH_ABILITIES` is listed twice (3229, 3256), which is harmless. Before the foe has moved, its "last move" is move 0, whose effect is plain `HIT`, so Encore scores -2.

### HP-based moves

**PainSplit (3287 to 3312).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe HP below 80% | -1, end | always | 3297, 3308 to 3309 |
| User slower, HP above 60% | -1 | always | 3298, 3303 to 3304 |
| User slower, HP 60% or less | +1 | always | 3305 |
| User not slower, HP above 40% | -1 | always | 3299 |
| User not slower, HP 40% or less | +1 | always | 3300 |

**DestinyBond (3335 to 3360).** Starts at -1 (3343). If the user is slower, or its HP is above 70%, that is all (3344 to 3345). Otherwise: +1 with 50% (3346 to 3347); if HP is also 50% or less, another +1 with 50% (3350 to 3352); if HP is also 30% or less, +2 with 60.9% (3355 to 3357).

**Reversal (3362 to 3396).** Flail, Reversal.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not slower, HP above 33% | -1 | always | 3374, 3392 to 3393 |
| User not slower, HP 21% to 33% | none | | 3375 |
| User not slower, HP 8% to 20% | +1 | 60.9% | 3377, 3387 to 3389 |
| User not slower, HP below 8% | +1, then another +1 | always, then 60.9% | 3376, 3384 to 3389 |
| User slower, HP above 60% | -1 | always | 3380, 3392 to 3393 |
| User slower, HP 41% to 60% | none | | 3381 |
| User slower, HP 40% or less | +1 | 60.9% | 3382, 3387 to 3389 |

**Endure (3633 to 3649).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| HP below 4% | -1 | always | 3637, 3640 to 3641 |
| HP 4% to 34% | +1 | 72.7% | 3638, 3644 to 3646 |
| HP 35% or more | -1 | always | 3638 falls through to 3640 to 3641 |

### Party and item moves

**HealBell (3398 to 3406).** Heal Bell, Aromatherapy. -5 (3403) unless the user has a status (3401) or some other living party member does (3402). "Other party member" leaves out every Pokemon now on the field for that side, so in doubles a statused partner does not count (C lines 1348 to 1379).

**Thief (3408 to 3422).** Thief, Covet.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| The foe's revealed item's hold effect is not in the list | -2 | always | 3412 to 3413, 3418 to 3419 |
| It is in the list | +1 | 80.5% | 3414 to 3415 |

The list (3424 to 3450): Chesto and Lum type berries, HP berries, BrightPowder and Lax Incense, Leftovers, Light Ball, Thick Club, the 17 type-resist berries including Chilan, and Black Sludge. An item the battle has not revealed reads as no item, so Thief and Covet get -2 until the foe's item has been seen.

### Curse, Protect, Spikes, Foresight

**Curse (3452 to 3500).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User is Ghost type (either slot), HP above 80% | none, end | | 3467 to 3470, 3495 to 3496 |
| User is Ghost type, HP 80% or less | -1, end | always | 3495 to 3497 |
| Not Ghost, own Defense +4 or higher | none, end | | 3471 |
| Not Ghost, knows Gyro Ball or Trick Room | +1 | 87.5% | 3472 to 3473, 3476 to 3478 |
| Not Ghost (every case that got this far) | +1 | 50% | 3480 to 3482 |
| Own Defense +1 or lower | +1 | 50% | 3485 to 3487 |
| Own Defense +0 or lower | +1 | 50% | 3490 to 3492 |

**Protect (3502 to 3589).** Protect, Detect (and Oxide's seven Protect variants). "Protect chain" is `LoadProtectChain` (C lines 2538 to 2552): the user's count of consecutive successful protections, but only if the user's last protecting move was Protect, Detect or Endure by move id; otherwise 0.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Foe has shown Feint or Shadow Force | -2 | 50% | 3536 to 3542 |
| Protect chain above 1 | -2, end | always | 3545 to 3546, 3585 to 3586 |
| User badly poisoned, cursed, under Perish Song, infatuated, seeded or drowsy (Yawn), or the foe has shown a RESTORE_HALF_HP move or Defense Curl; and the user is not under a foe's Lock-On | -2, end | always | 3547 to 3554, 3582 to 3586 |
| The same, but the user is under a foe's Lock-On | none, end | | 3583 |
| Foe badly poisoned, cursed, under Perish Song, infatuated, seeded or drowsy | +2 | always | 3555 to 3560, 3567 to 3568 |
| Otherwise, a double battle | +2 | always | 3561 to 3562 |
| Otherwise, user is under a foe's Lock-On | +2 | always | 3563 |
| Otherwise | +2 | 33.2% | 3564 |
| Every case that reached here | -1 | 50% | 3570 to 3572 |
| Protect chain is 1 | -1, then another -1 | always, then 50% | 3575 to 3579 |

The Lock-On flag sits on the Pokemon that was aimed at (`subscript_lock_on.s` sets it on the defender), so "the user is under a foe's Lock-On" is what the code tests.

**Spikes (3591 to 3606).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Always | +1 (otherwise end with nothing) | 50% | 3595 to 3596 |
| That, and the user knows Roar or Whirlwind (by move id) | +1 | 75% | 3597 to 3603 |

**Foresight (3608 to 3631).** Foresight, Odor Sleuth.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| The **user** is Ghost type | +2 | 47.3% (two 68.75% rolls) | 3615 to 3618, 3623 to 3628 |
| Otherwise, foe's evasion +3 or higher | +2 | 68.75% | 3619, 3626 to 3628 |
| Otherwise | -2 | always | 3620 |

### Baton Pass and Pursuit

**BatonPass (3651 to 3704).** The stats looked at are Attack, Defense, Sp. Atk, Sp. Def and evasion; Speed and accuracy boosts are ignored.

| Condition | Change | Chance | Lines |
|---|---|---|---|
| Any of them +3 or higher, user not slower, HP 60% or less | +2 | 68.75% | 3664 to 3668, 3673 to 3674, 3679 to 3681 |
| Any +3 or higher, user slower, HP 70% or less | +2 | 68.75% | 3672, 3677, 3679 to 3681 |
| Any +3 or higher, HP above those limits | none | | 3673, 3677 |
| Highest is +2, user not slower, HP above 60% | -2 | always | 3685 to 3689, 3694, 3700 to 3701 |
| Highest is +2, user slower, HP 70% or more | -2 | always | 3693, 3698, 3700 to 3701 |
| Highest is +2, HP below those limits | none | | 3695, 3698 |
| None of them above +1 | -2 | always | 3690, 3700 to 3701 |

**Pursuit (3706 to 3735).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| This is the user's first turn on the field | +1 | 50% | 3713 to 3714, 3725 to 3727 |
| Otherwise, the foe is Ghost or Psychic type (either slot) | +1 | 50% | 3715 to 3727 |
| Foe has shown U-turn (by move id) | +1 | 50% | 3730 to 3732 |

"First turn" is `LoadIsFirstTurnInBattle` on the user (C lines 2480 to 2492): true while the user's Fake Out marker is not behind the turn counter, which is its first turn after coming in.

### Weather

**RainDance (3737 to 3771).** Only the user's own ability is read, through `LoadBattlerAbility` on the attacker, which returns the real ability or none if it is suppressed (C lines 1170 to 1210).

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User not faster (slower or tie) and has Swift Swim | +1, end | always | 3747 to 3749, 3763 to 3764 |
| User HP below 40% | -1, end | always | 3752, 3767 to 3768 |
| Weather is hail, sun or sandstorm | +1, end | always | 3753 to 3756, 3763 to 3764 |
| User has Rain Dish | +1 | always | 3757 to 3758 |
| User has Hydration and has a status | +1 | always | 3759 to 3760 |

**SunnyDay (3773 to 3801).**

| Condition | Change | Chance | Lines |
|---|---|---|---|
| User HP below 40% | -1, end | always | 3782, 3797 to 3798 |
| Weather is hail, rain or sandstorm | +1, end | always | 3783 to 3786, 3793 to 3794 |
| User has Flower Gift | +1 | always | 3787 to 3788 |
| User has Leaf Guard and has a status | +1 | always | 3789 to 3790 |

Sunny Day has no speed check and does not look at Chlorophyll, although Rain Dance looks at Swift Swim. Neither looks at Dry Skin or Solar Power. Basic already punishes either move when its weather is already up.

### Remaining small routines

**LockOn (3319 to 3325).** Lock-On, Mind Reader: +2 with 50% (3321 to 3322).

## Where the source comments and the gist disagree with the code

The comments above each routine in `script.s` were written for the decomp, and lhearachel's gist reproduces them nearly word for word. So wherever a comment is wrong, the gist is wrong in the same way. pokemow.com's Trainer AI page loads its per-move detail interactively and could not be read from here, so it was not checked routine by routine; its one Expert note that could be read (Facade reading the foe's status) is in `expert-2.md`'s range. The code is right by definition; the tables above follow the code.

| Routine | Comment or gist says | Code does |
|---|---|---|
| Explosion | extra -1 at foe's evasion +3 | at +4 (stage 10, line 1858) |
| Explosion | at HP 30% or less, 80.5% chance of +1 | both the 50% and the 80.5% rolls apply |
| StatusSpAttackUp | 84.4% chance of -2 at HP 40% to 70% | 72.7% (line 2104) |
| StatusDefenseUp | special last move 58.6%, otherwise always | special always, physical 58.6% |
| StatusSpDefenseUp | physical last move 58.6%, otherwise always | physical always, special 58.6% |
| BypassAccuracyMove | +3 evasion or -3 accuracy: +1 | 60.9% chance of +1 |
| StatusAttackDown | -2 when the last move was not special | when it was special |
| StatusSpAttackDown | -2 when the last move was not physical | when it was physical |
| StatusAccuracyDown | first -1 needs target HP low and user HP low | either one is enough |
| StatusAccuracyDown | final block skipped if the user's stage is +0 | the foe's accuracy stage |
| Haze | otherwise -1 | 80.5% chance of -1 |
| ForceSwitch | 75% chance of +2 | 75% +2 and then a separate 50% +2 |
| Rest | 60.9% chance of -8 at full HP | always -8 |
| StatusParalyze | HP 70% or less: -1 | only when not slower |
| Substitute | +1 when the foe is currently statused, confused or seeded | when the foe is not |
| PainSplit | last case -1 | +1 (line 3300) |
| Swagger | -5 when the foe's Attack is -3 or higher | -2 or higher (stage above 3) |
| Curse | end at Defense +3 | at +4 (stage above 9) |
| Endure | no change at HP 35% or more | -1 |
| BatonPass | +2 stage case: -2 when HP is low | -2 when HP is high, none when low |
| Pursuit | attacker's first turn in battle | first turn on the field |

## Apparent bugs

Fixed on 2026-09-22 in other parts: the Oxide ability byte (see `basic.md` B11). Fixed on 2026-09-22 in this half: bugs 1, 2 and 3 (Thunder, Foresight and Leaf Guard; battle_edits, vanilla fixes approved by Ian on 2026-09-15). Bug 4, the faster-heal branch, was put to Ian and kept as vanilla has it.

Every entry is present in vanilla Platinum: `script.s` is identical to `main`, so the vanilla line is the same number, and the C commands involved are unchanged from `main`. None is introduced by Oxide in this half (Oxide's own problems are in the last section). Fixing any of them changes vanilla behaviour and is Ian's call. Where an entry says a bug is inherited from Gen 3, that is from memory of pokeemerald's AI script and was not re-checked for this file.

1. **Thunder never reaches its routine.** Present in vanilla, line 1719. The test reads `BATTLE_EFFECT_SKIP_CHARGE_TURN_IN_SUN`, the same effect as line 1716, which is tested first and sends Solar Beam to the charge-turn routine. So line 1719 can never fire, `Expert_Thunder` (3975) is unreachable, and Thunder (`BATTLE_EFFECT_THUNDER`, id 152, which has no other entry) gets nothing from Expert. The source comment at 1718 says the same. This is a battle_edits fix, below.

2. **Foresight checks the user's type instead of the foe's.** Present in vanilla, lines 3615 to 3618. `LoadTypeFrom LOAD_ATTACKER_TYPE_1` and `_2` read the AI's own Pokemon. Foresight is for hitting a Ghost-type foe with Normal and Fighting moves, and the rest of the routine is about the foe (its evasion). The source comment at 3610 agrees. A battle_edits fix, below.

3. **Leaf Guard rewards Sunny Day when the user already has a status.** Present in vanilla, line 3790. Leaf Guard only prevents new statuses in sun; it does nothing for one the user already has. The check should be for no status. The source comment at 3780 agrees. A battle_edits fix, below.

4. **A faster user never heals with Recover-type moves.** Present in vanilla, lines 2650 to 2657. When the user is not slower, line 2651 subtracts 8 and ends. The block right after it, `Expert_Recovery_Unused` (2654 to 2657), is referenced by nothing and so can never run, yet it is written exactly as a "faster user" branch: heal below 50% HP, refuse above 80%, and a 72.7% roll between. Rest (2758 to 2770) has such a branch and uses it. The shape strongly suggests the -8 was meant to be a jump into that block. The effect is large: with Expert set, a Recover, Roost, Slack Off, Softboiled, Milk Drink, Heal Order, Swallow or Synthesis user that outspeeds its foe loses 8 points on the healing move whatever its HP, so it almost never picks it over a usable attack. This is not on the battle_edits list, so a fix would be a behaviour change. The same shape is in Gen 3's script, so it is inherited.

5. **Two dispatch entries are swapped.** Present in vanilla, lines 1675 and 1676. `EVA_DOWN_2` goes to the accuracy-down routine and `ACC_DOWN_2` to the evasion-down routine, against the pattern of every other pair. No move in vanilla or Oxide uses either effect, so nothing is affected today; it matters if a move is ever given one.

6. **"No move yet" reads as a physical move.** Present in vanilla, C lines 2050 to 2054. `LoadDefenderLastUsedMoveClass` reads the class of `movePrevByBattler`, which is 0 until the foe has moved since coming in, and move 0's data (`res/moves/none/data.json`) says `CLASS_PHYSICAL`. So before the foe has moved, Reflect gets its 75% +1 (2905 to 2908) and Light Screen does not. Special Attack Down moves would take their 50% -2 (2392 to 2395); no vanilla move reaches that routine, but Oxide's Confide and Eerie Impulse do. The routines that check the move's power first (Defense Up, Special Defense Up, Counter, Disable) avoid this, which suggests the others were meant to.

7. **Substitute reads the foe's condition where the user's is meant.** Present in vanilla, lines 3027, 3031 and 3035. After finding that the foe's last move was a status, confusion or Leech Seed move, the routine checks whether the *foe* is statused, confused or seeded. The question that makes sense is whether the *user* already has that condition (if not, the foe will likely try again, and a Substitute blocks it). Gen 3's script has the same target, so this is inherited; the intent is less certain than items 1 to 3, but the check as written has no bearing on Substitute's value.

8. **Accuracy Down looks at the user's own accuracy.** Present in vanilla, line 2457. The -2 for "accuracy -2 or lower" reads `AI_BATTLER_ATTACKER`, the user's own stage, while the same routine's final block (2489) reads the foe's accuracy, which is what an accuracy-lowering move changes. Probably meant to be the foe. Also inherited from Gen 3.

9. **Swagger with Psych Up rewards almost the opposite case.** Present in vanilla, line 2880. The combo is Swagger to raise the foe's Attack, then Psych Up to copy it. The routine gives -5 whenever the foe's Attack is -2 or higher and +3 to +5 only when it is -3 or lower, which a Swagger user rarely sees. The comparison value (3, meaning -3) looks wrong, but the intended value cannot be read from the code. Inherited from Gen 3.

10. **Counter's type heuristic looks inverted.** Present in vanilla, lines 3145 to 3150. When the foe last used a status move, Counter gets its 49% +4 only if the foe is *not* one of the "physical" types, which is when Counter is least likely to work. Mirror Coat (3852 onwards, `expert-2.md`) is built the same way with special types, so it may be deliberate; either way the type list itself predates the physical/special split and no longer predicts anything.

No score in this half can pass 127 on its own: the largest gain any routine gives is +14 (Evasion Up, from a base of 100), and Sleep Talk's +10 is next. An overflow would need at least another +14 from other flags on the same move, which is for the combined write-up to check.

## The eleven battle_edits fixes

Three fall in this half, and a fourth has its dispatch line here.

**Thunder scoring fix.** Line 1719 should test `BATTLE_EFFECT_THUNDER`. The routine it would then reach (3975 to 3991, in `expert-2.md`) gives Thunder -3 with 80.5% chance when the foe resists it or the sun is out, and +1 in rain. Today Thunder gets 0 from Expert in every case. Solar Beam is unaffected, since line 1716 already catches it.

**Foresight and Odor Sleuth Ghost check.** Lines 3615 and 3617 should load `LOAD_DEFENDER_TYPE_1` and `LOAD_DEFENDER_TYPE_2`. Score change: against a Ghost-type foe (evasion below +3), the move goes from a certain -2 to a 47.3% chance of +2. A Ghost-type AI Pokemon using Foresight against a non-Ghost foe goes from a 47.3% chance of +2 to a certain -2, unless the foe's evasion is +3 or higher. The double roll for the Ghost case (two 68.75% rolls against one for high evasion) stays as it is.

**Leaf Guard Sunny Day logic.** Line 3790 should be `IfNotStatus AI_BATTLER_ATTACKER, MON_CONDITION_ANY, Expert_SunnyDay_ScorePlus1`. A Leaf Guard user without a status then gets +1 for Sunny Day (it gets 0 today), and one with a status gets 0 (it gets +1 today). Basic's own Sunny Day check (lines 802 to 822) is separate.

**Charge-turn scoring fix.** The dispatch lines 1657, 1682, 1715 and 1716 are correct; whatever the fix changes is in `Expert_ChargeTurnNoInvuln` (3933), in `expert-2.md`.

Not in this half: Fire Fang against Wonder Guard, the Rage glitch, the Dry Skin water-immunity check (Basic, line 78), the Sunny Day check (most likely Basic's Hydration check at lines 812 to 814), the Facade status check (line 4122), the Water Spout and Eruption HP check (line 4617), and the Discharge double-battle scoring (Tag Strategy, lines 7221 and 7235).

## Oxide consequences

**New effects get nothing.** None of the effects 277 to 406 has a dispatch entry, so the 136 moves on them get no Expert scoring at all. Several are close relatives of routines in this half and would naturally share them:

| Oxide effect (id) | Moves | Natural routine here |
|---|---|---|
| ATK_ACC_UP (277), ATK_SP_ATK_UP (295) | Hone Claws, Work Up | StatusAttackUp |
| ATK_DEF_ACC_UP (286), DEF_UP_3 (328) | Coil, Cotton Guard | StatusDefenseUp |
| SP_ATK_SP_DEF_SPEED_UP (283) | Quiver Dance | StatusSpAttackUp or SpDefenseUp |
| RECOVER_THREE_QUARTERS_DAMAGE_DEALT (347), RECOVER_FULL_DAMAGE_DEALT (315), RECOVER_HALF_DAMAGE_DEALT_BURN_HIT (348) | Draining Kiss, Oblivion Wing, Bouncy Bubble, Matcha Gotcha | DrainMove |
| PREVENT_ESCAPE_HIT (351), PREVENT_ESCAPE_BOTH_HIT (352) | Anchor Shot, Spirit Shackle, Thousand Waves, Jaw Lock | BindingMove |
| ALWAYS_CRITICAL (282), HIGH_CRITICAL_RAISE_SPEED_HIT (368), HIT_THREE_TIMES_ALWAYS_CRITICAL (366) | Flower Trick, Frost Breath, Storm Throw, Wicked Blow, Esper Wing, Surging Strikes | HighCritical |
| FORCE_SWITCH_HIT (395) | Circle Throw, Dragon Tail | ForceSwitch |
| RESET_STAT_CHANGES_HIT (313), CLEAR_SMOG (390) | Freezy Frost, Clear Smog | Haze |
| CURE_PARTY_STATUS_HIT (314) | Sparkly Swirl | HealBell |
| STRENGTH_SAP (378), LIFE_DEW (383) | Strength Sap, Life Dew | Recovery |
| SET_AURORA_VEIL (377) | Aurora Veil | Reflect or LightScreen |
| STICKY_WEB (326), SET_SPIKES_HIT (354), STEALTH_ROCK_HIT (353) | Sticky Web, Ceaseless Edge, Stone Axe | Spikes |
| TEARFUL_LOOK (362), PARTING_SHOT (389) | Noble Roar, Tearful Look, Parting Shot | StatusAttackDown |
| PROTECT_USER_SIDE (371) | Wide Guard, Quick Guard, Mat Block, Crafty Shield | Protect |
| SHED_TAIL (304) | Shed Tail | Substitute or BatonPass |
| FINAL_GAMBIT (402) | Final Gambit | Explosion |

**New moves on old effects inherit the routine**, listed in the dispatch table. Most inherit sensibly. Three do not:

1. The seven new Protect moves (King's Shield, Spiky Shield, Baneful Bunker, Obstruct, Silk Trap, Burning Bulwark, Max Guard) reach `Expert_Protect`, but `LoadProtectChain` (C lines 2545 to 2547) recognises only Protect, Detect and Endure by move id. After a King's Shield the chain reads 0, so lines 3546 and 3575 to 3579 never penalise using it again, and the AI will try to repeat it as if it had never protected.
2. The seven new Speed-lowering attacks (Bulldoze, Electroweb, Low Sweep, Glaciate, Drum Beating, Pounce, Max Strike) reach `Expert_SpeedDownOnHit`, which only scores Icy Wind, Rock Tomb and Mud Shot by move id (2345 to 2347), so they get nothing. Bubble and Bubble Beam were already treated that way in vanilla.
3. Confide and Eerie Impulse make `Expert_StatusSpAttackDown` live for the first time, including the "no move yet reads as physical" penalty (bug 6), which vanilla never exercised.

Shore Up reaches the Synthesis routine and is penalised in sandstorm. That matches what Oxide's engine does with it today (it uses the sun-boosted healing effect and has no sand code), so the AI and the engine agree; if Shore Up is later given its real sand bonus, line 2634 will be backwards for it.

**Checks keyed on move ids.** These name vanilla moves and will not see Oxide's equivalents: the Mirror Move table (1928 to 1976), Psych Up in Swagger (2852), Focus Punch in Substitute (2994), Mirror Coat in Counter (3125), Gyro Ball and Trick Room in Curse (3472 to 3473), Feint and Shadow Force in Protect (3536 to 3537, so Phantom Force, Hyperspace Hole and Hyperspace Fury are not feared), Roar and Whirlwind in Spikes (3597 to 3598, so Dragon Tail and Circle Throw are not seen), U-turn in Pursuit (3730, so Volt Switch, Flip Turn and Parting Shot are not seen), and Icy Wind, Rock Tomb, Mud Shot (2345 to 2347). Vanilla move ids are unchanged in Oxide (the new moves are appended from 468), so every existing check still names the right move.

**Checks keyed on effect ids.** Besides the dispatch, the Encore list (3202 to 3285), the Substitute effect checks (3017 to 3023), the Snatch checks in Recovery and Rest (2670, 2782), the Toxic and Leech Seed checks for SP_DEF_UP and PROTECT (2699 to 2700), and the Protect checks for RESTORE_HALF_HP and Defense Curl (3553 to 3554). Oxide's new status effects are absent from all of them; in particular Encore scores -2 against a foe whose last move was any Oxide-only status move.

**Abilities.** This half reads only the user's own ability, through `LoadBattlerAbility` on the attacker, which returns `battleMons[].ability` directly. That field is u16 in Oxide and the script's values are 32-bit words, so the comparisons hold for any id. The abilities named are all vanilla and below 256: Truant (3056), Swift Swim (3749), Rain Dish (3758), Hydration (3759), Flower Gift (3788), Leaf Guard (3789). New abilities that bear on these moves are not considered: Sand Rush and Slush Rush would not change anything here, but for Sunny Day, Chlorophyll and Solar Power (vanilla omissions) and Harvest, Protosynthesis and Orichalcum Pulse (Oxide) are ignored, and for Rain Dance so are Dry Skin (a vanilla omission) and Steam Engine.

One Oxide change outside this half affects every routine that reads the foe's ability: `battlerAbilities` in `include/battle/ai_context.h` line 28 is still `u8`, while `BattleAI_SetAbility` (`battle_script.c` line 12176) now takes a u16 and stores it there. Any revealed foe ability with an id above 255 is truncated to the wrong ability. This is introduced by Oxide (on `main` both are u8). Nothing in this half reads a foe's ability, so it does not change the tables above, but Basic and `expert-2.md` do.

**Types.** Type 18 (Fairy) appears in none of this half's type lists. Counter's physical-types list (3165 to 3175) therefore treats every Fairy foe as "not physical", so Counter can get its 49% +4 against one; Mirror Coat's special list (`expert-2.md`) does the same. The six unused pre-split tables do not matter. Type checks by name (Ghost in Curse and Foresight, Ghost and Psychic in Pursuit) are unaffected. `LoadTypeFrom` reads only the two type slots, so a third type added by Oxide's Forest's Curse or Trick-or-Treat (if the engine stores one) is invisible to Curse, Foresight and Pursuit. Oxide retyped Charm, Moonlight and Sweet Kiss to Fairy; none of their routines looks at the move's type, so their scoring is unchanged. Type effectiveness itself comes from the engine's chart, so Fairy matchups count wherever `IfMoveEffectivenessEquals` is used, provided the chart has them.
