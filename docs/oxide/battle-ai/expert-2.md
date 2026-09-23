# The Expert flag, second half

This file covers the per-effect routines of the Expert flag from `Expert_BellyDrum` to `Expert_HealingWish`, lines 3803 to 6352 of `src/battle/trainer_ai/script.s`. None of these routines is called by anything except the dispatch table at the top of `Expert_Main` (lines 1627 to 1808, described in `expert-1.md`), which tests the move's effect id against a list and jumps to the first match; a routine then ends with `PopOrEnd`, which finishes the Expert flag for that move. The routines are grouped below by what the move does, not by line order. Each group has one table, where the chance is the chance that the change happens once the routine has reached that check, and a paragraph for anything the table cannot show. After the groups come the apparent bugs, the battle_edits fixes that land here, and what Oxide's additions do to this half. `script.s` is byte-identical to vanilla on `main` (commit `7a0637607`), so every script line number below is also the vanilla line number.

## How to read the checks

These semantics come from the C functions in `src/battle/trainer_ai/trainer_ai.c`; they apply to every table below.

**Random rolls.** `IfRandomLessThan N, label` draws a number from 0 to 255 and jumps when it is below N (lines 528 to 538). Almost every roll in this half jumps *past* the score change, so the change happens with chance (256 - N) / 256.

| N in the script | Chance the change happens |
|---|---|
| 10 | 96.1% |
| 25 | 90.2% |
| 30 | 88.3% |
| 32 | 87.5% |
| 50 | 80.5% |
| 60 | 76.6% |
| 64 | 75% |
| 70 | 72.7% |
| 80 | 68.75% |
| 96 | 62.5% |
| 100 | 60.9% |
| 128 | 50% |
| 150 | 41.4% |
| 164 | 35.9% |
| 180 | 29.7% |
| 192 | 25% |
| 200 | 21.9% |
| 230 | 10.2% |

**HP.** The HP percentage is `curHP * 100 / maxHP`, rounded down (lines 588 to 646). So "HP below 90%" includes 89.9%, and "HP equal to 100%" means exactly full. In the tables, "HP > 50" means the rounded percentage is above 50.

**Stat stages** are stored 0 to 12 with 6 as neutral. `IfStatStageGreaterThan ..., 8` means +3 or higher; `IfStatStageLessThan ..., 7` means +0 or lower.

**Speed.** `IfSpeedCompareEqualTo` calls `BattleSystem_CompareBattlerSpeed` (`src/battle/battle_lib.c` line 1188) with priority ignored. It returns faster (0), slower (1) or tie (2). A speed tie returns faster or tie on a coin flip, never slower, so every "if slower" branch treats a tie as faster. Trick Room reverses the comparison, so "slower" means "moves second on the field as it stands".

**What the AI knows about the opponent.** Three commands do not read the truth.

1. "Opponent knows move X" (`IfMoveKnown` / `IfMoveEffectKnown` on the defender, lines 1666 and 1763) means the opponent has *used* X in front of this AI; it reads `battlerMoves`, which records moves as they are used.
2. "Opponent's ability" (`LoadBattlerAbility` on the defender, lines 1170 to 1210) is the ability the AI has seen announced, or else a coin-flip guess between the species' two abilities (Shadow Tag, Magnet Pull and Arena Trap are always known). A suppressed ability reads as none.
3. "Opponent's item" (`LoadHeldItemEffect` and `IfHeldItemEqualTo` on the defender, lines 1901 to 1934) is the item the AI has seen named in a battle message, and nothing until then. pokemow.com says the AI always knows the player's item; in this code it does not, for these two commands.

The attacker's own ability and item are always read directly.

**Effectiveness.** `IfMoveEffectivenessEquals` (lines 1311 to 1346) runs the real type chart for the move against the defender, starting from 40, and compares the result with a fixed value: immune 0, quarter 10, half 20, double 80, quadruple 160. STAB's 1.5 is undone for the four doubled and halved values but not for neutral. Four consequences show up in this half.

* Immunity also covers Levitate and Magnet Rise against Ground moves.
* An Adaptability user's neutral STAB move comes out at 80 and reads as super effective, and its resisted STAB move comes out at 40 and does not read as resisted.
* Tinted Lens turns a resisted move into 40, which does not read as resisted.
* Filter, Solid Rock and Expert Belt move a super-effective result off 80, so it no longer reads as super effective.

**The opponent's last move.** `LoadBattlerPreviousMove` and `LoadDefenderLastUsedMoveClass` read `movePrevByBattler`. Before the opponent has moved this is move 0, which the data gives power 0 and class physical (`res/moves/none/data.json`). So "last move was a status move (power 0)" is also true before the opponent has moved, and "last move was physical" is also true then.

**Score limits.** No routine in this half adds more than +5 in one pass except Punishment, which can add +10 (see bug 2). Starting from 100, nothing here can push a score past 127 on its own. Scores are clamped at 0 from below after every change.

## Dispatch into this half

| Routine | Effect ids (vanilla names) | `Expert_Main` line |
|---|---|---|
| `Expert_BellyDrum` | 142 max Attack, lose half HP | 1712 |
| `Expert_PsychUp` | 143 copy stat changes | 1713 |
| `Expert_MirrorCoat` | 144 | 1714 |
| `Expert_ChargeTurnNoInvuln` | 39 Razor Wind, 75 Sky Attack, 145 Skull Bash, 151 Solar Beam | 1657, 1682, 1715, 1716 |
| `Expert_Thunder` | 151 again (meant to be 152 Thunder), so never reached | 1719 |
| `Expert_ChargeTurnWithInvuln` | 155 Fly, 255 Dive, 256 Dig, 263 Bounce | 1721, 1797, 1798, 1803 |
| `Expert_ShadowForce` | 272 Shadow Force | 1808 |
| `Expert_FakeOut` | 158 | 1723 |
| `Expert_SpitUp` | 161 | 1724 |
| `Expert_Hail` | 164 | 1726 |
| `Expert_Facade` | 169 | 1729 |
| `Expert_FocusPunch` | 170 | 1730 |
| `Expert_SmellingSalts` | 171 | 1731 |
| `Expert_Trick` | 177 | 1732 |
| `Expert_ChangeUserAbility` | 178 Role Play, 191 Skill Swap | 1733, 1743 |
| `Expert_Ingrain` | 181 | 1734 |
| `Expert_Superpower` | 182 | 1735 |
| `Expert_MagicCoat` | 183 | 1736 |
| `Expert_Recycle` | 184 | 1737 |
| `Expert_Revenge` | 185 Revenge, Avalanche | 1738 |
| `Expert_BrickBreak` | 186 | 1739 |
| `Expert_KnockOff` | 188 | 1740 |
| `Expert_Endeavor` | 189 | 1741 |
| `Expert_WaterSpout` | 190 Water Spout, Eruption | 1742 |
| `Expert_Imprison` | 192 | 1744 |
| `Expert_Refresh` | 193 | 1745 |
| `Expert_Snatch` | 195 | 1746 |
| `Expert_RecoilMove` | 48 quarter, 198 third, 253 Flare Blitz, 262 Volt Tackle, 269 half | 1661, 1747, 1796, 1802, 1806 |
| `Expert_MudSport` | 201 | 1749 |
| `Expert_Overheat` | 204 user Sp. Atk down 2 | 1750 |
| `Expert_WaterSport` | 210 | 1755 |
| `Expert_DragonDance` | 212 | 1757 |
| `Expert_Gravity` | 215 | 1759 |
| `Expert_MiracleEye` | 216 | 1760 |
| `Expert_WakeUpSlap` | 217 | 1761 |
| `Expert_HammerArm` | 218 | 1762 |
| `Expert_GyroBall` | 219 | 1763 |
| `Expert_HealingWish` | 220 Healing Wish, 270 Lunar Dance | 1764, 1807 |
| `Expert_Brine` | 221 | 1765 |
| `Expert_Feint` | 223 | 1766 |
| `Expert_Pluck` | 224 | 1767 |
| `Expert_Tailwind` | 225 | 1768 |
| `Expert_Acupressure` | 226 | 1769 |
| `Expert_MetalBurst` | 227 | 1770 |
| `Expert_UTurn` | 228 | 1771 |
| `Expert_CloseCombat` | 229 | 1772 |
| `Expert_Payback` | 230 | 1773 |
| `Expert_Assurance` | 231 | 1774 |
| `Expert_Embargo` | 232 | 1775 |
| `Expert_Fling` | 233 | 1776 |
| `Expert_PsychoShift` | 234 | 1777 |
| `Expert_TrumpCard` | 235 | 1778 |
| `Expert_HealBlock` | 236 | 1779 |
| `Expert_WringOut` | 237 | 1780 |
| `Expert_PowerTrick` | 238 | 1781 |
| `Expert_GastroAcid` | 239 | 1782 |
| `Expert_LuckyChant` | 240 | 1783 |
| `Expert_MeFirst` | 241 | 1784 |
| `Expert_Copycat` | 242 | 1785 |
| `Expert_PowerSwap` | 243 | 1786 |
| `Expert_GuardSwap` | 244 | 1787 |
| `Expert_Punishment` | 245 | 1788 |
| `Expert_LastResort` | 246 | 1789 |
| `Expert_WorrySeed` | 247 | 1790 |
| `Expert_SuckerPunch` | 248 | 1791 |
| `Expert_ToxicSpikes` | 249 | 1792 |
| `Expert_HeartSwap` | 250 | 1793 |
| `Expert_AquaRing` | 251 | 1794 |
| `Expert_MagnetRise` | 252 | 1795 |
| `Expert_Defog` | 258 | 1799 |
| `Expert_TrickRoom` | 259 | 1800 |
| `Expert_Blizzard` | 260 | 1801 |
| `Expert_Captivate` | 265 | 1804 |
| `Expert_StealthRock` | 266 | 1805 |

Four routines jump out of this half to shared score labels near the top of the Expert section: `ScorePlus5` (line 1615), `ScoreMinus5` (1579), `ScoreMinus10` (1591) and `ScoreMinus2` (1571). Each adds its amount and ends.

## Charge-turn and semi-invulnerable moves

`Expert_ChargeTurnNoInvuln` (3933 to 3973) serves Razor Wind, Sky Attack, Skull Bash and Solar Beam. Each row ends the routine when it fires, except where the table says it continues.

| Check | Change | Chance | Lines |
|---|---|---|---|
| Move is immune, quarter or half effective | -2 | always | 3943 to 3945, 3970 |
| Move is Solar Beam's effect and the weather is sun | +2 | always | 3946, 3950 to 3953 |
| AI holds Power Herb | +2 | always | 3956, 3960 |
| Opponent has used a Protect-effect move | -2 | always | 3964, 3970 |
| AI HP 38% or less | -1 | always | 3965 to 3966 |

`Expert_Thunder` (3975 to 3990) is never reached, because its dispatch line tests Solar Beam's effect a second time (bug 1). If it were reached, it would do this:

| Check | Change | Chance | Lines |
|---|---|---|---|
| Move is immune, half or quarter effective | -3 | 80.5% | 3976 to 3978, 3986 to 3987 |
| Weather is sun | -3 | 80.5% | 3980, 3986 to 3987 |
| Weather is rain | +1 | always | 3981 to 3982 |

`Expert_ChargeTurnWithInvuln` (3992 to 4066) serves Fly, Dive, Dig and Bounce; Shadow Force enters part-way down, at `Expert_ShadowForce` (4014). Rows are in the order they are tested.

| Check | Change | Chance | Lines |
|---|---|---|---|
| Fly group only: AI holds Power Herb | +2, end | always | 4009 (jumps to 3959 to 3961) |
| Fly group only: opponent has used a Protect-effect move | -1, end | always | 4010 to 4012 |
| Move is immune, quarter or half effective | +1, end | always | 4017 to 4019, 4064 to 4066 |
| Shadow Force only in effect (Fly group already left): AI holds Power Herb | +1, end | always | 4020, 4023 to 4025 |
| Opponent badly poisoned, cursed, or seeded | +1, end | 68.75% | 4028 to 4030, 4057 to 4059 |
| Sandstorm and the AI is Ground, Rock or Steel | +1, end | 68.75% | 4032, 4036 to 4040 |
| Hail and the AI is Ice | +1, end | 68.75% | 4033, 4043 to 4047 |
| AI not slower, and the opponent's last move was not Lock-On or Mind Reader | +1 | 68.75% | 4050 to 4054 |

The resisted and immune row gives a bonus where the rest of the family gives a penalty; that is bug 3 and the battle_edits charge-turn fix. In sandstorm or hail with a non-immune AI, the routine goes on to the speed row.

## Stat setup and stat swapping

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| BellyDrum | AI HP below 90% | -2 | always | 3805, 3809 |
| PsychUp | Opponent has no stat (Atk, Def, SpA, SpD, evasion) at +3 or more | -2 | always | 3823 to 3828, 3847 |
| PsychUp | Otherwise, AI has Atk, Def, SpA or SpD at +0 or lower | +1 | always | 3831 to 3834, 3843 |
| PsychUp | Otherwise, AI evasion at +0 or lower | +2 | always | 3835, 3840 to 3843 |
| PsychUp | Otherwise | -2 | 80.5% | 3836 to 3837 |
| DragonDance | AI slower | +1, end | 50% | 4769, 4776 to 4777 |
| DragonDance | AI not slower and HP 50% or less | -1 | 72.7% | 4770 to 4772 |
| Acupressure | AI HP 50% or less | -1 | always | 5014, 5024 |
| Acupressure | AI HP above 90% | +1 | 75% | 5015, 5019 to 5020 |
| Acupressure | AI HP 51% to 90% | +1 | 37.5% | 5016, 5019 to 5020 |
| PowerTrick | AI HP above 90% | +1 | 62.5% | 5448, 5454 to 5455 |
| PowerTrick | AI HP 61% to 90% | +1 | 50% | 5449, 5459 to 5460 |
| PowerTrick | AI HP 31% to 60% | +1 | 35.9% | 5450, 5464 to 5465 |
| PowerTrick | AI HP 30% or less | -2 | always | 5451 (to 1571) |
| HeartSwap | Opponent has no stat (Atk, Def, SpA, SpD, evasion) at +2 or more and no Focus Energy | -2 | always | 6050 to 6056, 6076 |
| HeartSwap | Otherwise, AI has Atk, Def, SpA or SpD at +0 or lower | +1 | always | 6059 to 6062, 6072 |
| HeartSwap | Otherwise, AI evasion at +0 or lower | +2 | always | 6063, 6069 to 6072 |
| HeartSwap | Otherwise, AI has no Focus Energy | +1 | always | 6064, 6072 |
| HeartSwap | Otherwise | -2 | 80.5% | 6065 to 6066 |

Psych Up and Heart Swap test the four main stats before evasion, so the +2 only happens when all four of the AI's stats are already at +1 or more. The decomp comment and the gist describe the +2 first, which reads as if it came first.

`Expert_PowerSwap` (5632 to 5764) and `Expert_GuardSwap` (5766 to 5898) are the same routine on different stats: Power Swap uses Attack then Special Attack, Guard Swap uses Defense then Special Defense. `DiffStatStages` (line 2259) gives the opponent's stage minus the AI's, so a positive number means the opponent has more to give. The first difference picks a row, the second picks a column, and the cell names a starting rung of a ladder.

| First difference | Second > 3 | Second 2 or 3 | Second = 1 | Second = 0 | Second < 0 |
|---|---|---|---|---|---|
| > 3 | +5 rung | +4 rung | nothing | +3 rung | nothing |
| 2 or 3 | +4 rung | +3 rung | nothing | +2 rung | nothing |
| 1 | +3 rung | +2 rung | nothing | +1 rung | nothing |
| 0 | +3 rung | +2 rung | +1 rung | nothing | nothing |
| < 0 | nothing | nothing | nothing | nothing | nothing |

Lines 5703 to 5736 for Power Swap, 5837 to 5870 for Guard Swap. A ladder starting at +N adds N with 50%, otherwise tries N - 1 with 50%, and so on down to +1; it stops at the first success (5738 to 5761, 5872 to 5895). So a +5 rung gives +5 50%, +4 25%, +3 12.5%, +2 6.25%, +1 3.125%, nothing 3.125%. The "second = 1 gives nothing" column is bug 5.

## Counter-style and timing moves

`Expert_MirrorCoat` (3852 to 3931), in the order tested:

| Check | Change | Chance | Lines |
|---|---|---|---|
| Opponent asleep, infatuated or confused | -1, end | always | 3869 to 3871, 3917 |
| AI HP 30% or less | -1, continue | 96.1% | 3872 to 3874 |
| AI HP 50% or less | -1, continue | 60.9% | 3877 to 3879 |
| AI knows Counter | +4, end | 60.9% | 3882, 3910 to 3911 |
| Opponent's last move has power 0 (status, or none yet) and the opponent is taunted | +1, continue | 60.9% | 3885, 3898 to 3900 |
| Same branch: neither of the opponent's types is Fire, Water, Grass, Electric, Psychic, Ice, Dragon or Dark | +4 | 49.0% (80.5% then 60.9%) | 3903 to 3911 |
| Last move has power and the opponent is taunted | +1, continue | 60.9% | 3886 to 3888 |
| Same branch: last move was not special | -1, end | always | 3891 to 3892, 3917 |
| Same branch: last move was special | +1 | 60.9% | 3893 to 3894 |

The "special types" list is the Generation 3 type split, kept from Emerald for the case where the opponent has not attacked yet.

`Expert_MetalBurst` (5029 to 5083):

| Check | Change | Chance | Lines |
|---|---|---|---|
| Opponent asleep, infatuated or confused, or has used a Revenge, Focus Punch or Vital Throw effect | -1, end | always | 5046 to 5051, 5080 |
| AI HP 30% or less | -1 | 96.1% | 5052 to 5054 |
| AI HP 50% or less | -1 | 60.9% | 5057 to 5059 |
| Every case that reaches here | +1 | 25% | 5062 to 5063 |
| Opponent's last move has power and the opponent is taunted | +1 | 60.9% | 5066 to 5071 |
| Opponent is taunted | +1 | 60.9% | 5074 to 5076 |

Both taunt rows skip when the opponent is *not* taunted (`IfTargetIsNotTaunted` jumps past them). The decomp comment and the gist say the opposite for the last row, and say the 25% row needs HP above 50%; it does not.

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| Revenge | Opponent asleep, infatuated or confused | -2 | always | 4546 to 4548, 4554 |
| Revenge | Otherwise | -2, or else +2 | 70.3% / 29.7% | 4549 to 4550 |
| FocusPunch | Move immune, quarter or half effective | -1 | always | 4139 to 4141, 4153 |
| FocusPunch | AI behind a Substitute | +5 | always | 4142 (to 1615) |
| FocusPunch | Opponent asleep | +1 | always | 4143, 4160 |
| FocusPunch | Opponent infatuated or confused | +1 | 60.9% | 4144 to 4145, 4157 |
| FocusPunch | Not the AI's first turn out | +1 | 21.9% | 4146 to 4149 |
| Payback | Move immune, half or quarter effective | -1 | always | 5174 to 5176, 5184 |
| Payback | AI not faster (a tie counts) and HP 30% or more | +1 | 75% | 5177 to 5180 |
| Assurance | Move immune, half or quarter effective | -1 | always | 5196 to 5198, 5208 |
| Assurance | AI not faster and has Rough Skin | +1 | 50% | 5199 to 5201, 5212 to 5213 |
| Assurance | AI not faster, holding Jaboca or Rowap Berry | +1 | 50% intended, never fires | 5202 to 5203 |
| Assurance | AI not faster, otherwise | +1 | 25% | 5204, 5212 to 5213 |
| SuckerPunch | Move immune, half or quarter effective | -1 | always | 5999 to 6001, 6007 |
| SuckerPunch | Otherwise | +1 | 75% | 6002 to 6003 |

The Jaboca and Rowap row compares an item's hold effect with item ids, so it never matches (bug 4).

`Expert_MeFirst` (5519 to 5550) and `Expert_Copycat` (5552 to 5630) both use `IfBattlerDealsMoreDamage` on the defender. That command (C lines 2187 to 2241) computes the AI's best damage against the opponent, then the damage of the opponent's last move *against the opponent itself*, with the AI's IVs, and jumps when the second is larger (bug 6). The table calls this "the opponent's self-hit beats the AI's best". The decomp comments read it as "the AI deals more damage", which is the reverse.

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| MeFirst | AI slower | -2, end | always | 5527, 5547 |
| MeFirst | Opponent's self-hit beats the AI's best | +1 | 87.5% | 5528, 5532 to 5533 |
| MeFirst | Opponent's last move is a status move | +1 | 75% | 5536 to 5537, 5542 to 5543 |
| MeFirst | Opponent's last move is damaging (or none yet) | +1, then +1 | 50%, then 75% | 5538 to 5543 |
| Copycat | AI slower: self-hit does not beat, and the last move is not in the list | -1 | 68.75% | 5559, 5573 to 5577 |
| Copycat | AI not slower: self-hit beats | +2 | 87.5% | 5560, 5568 to 5569 |
| Copycat | AI not slower: last move in the list | +2 | 50% | 5561 to 5564 |
| Copycat | AI not slower: neither | -1 | 68.75% | 5562 (to 5572 to 5577) |

The Copycat list (5582 to 5630) is 47 vanilla move ids: sleep, confusion, accuracy and stat-lowering moves, the four OHKO moves, Toxic, Thunder Wave, Glare, Poison Powder, and a handful of strong or awkward attacks and item or ability swaps. It reads the *opponent's* last move, though Copycat copies the last move used by anyone.

## Damaging moves with conditions

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| FakeOut | Always (Basic refuses it after the first turn) | +2 | always | 4076 |
| SpitUp | AI Stockpile count 2 or more | +2 | 68.75% | 4081 to 4084 |
| Facade | Opponent poisoned, badly poisoned, burned or paralysed | +1 | always | 4123 to 4124 |
| SmellingSalts | Opponent paralysed | +1 | always | 4167, 4171 |
| WakeUpSlap | Move immune, half or quarter effective | -1 | always | 4833 to 4835, 4840 |
| WakeUpSlap | Opponent asleep | +1 | always | 4836, 4844 |
| HammerArm | Move immune, half or quarter effective | -1 | always | 4853 to 4855, 4860 |
| HammerArm | AI slower | +1 | always | 4856, 4864 |
| GyroBall | nothing | 0 | | 4869 to 4871 |
| Brine | Move immune, half or quarter effective | -1 | always | 4877 to 4879, 4887 |
| Brine | Opponent HP 50% or less | +1, then +1 | always, then 50% | 4880 to 4883 |
| WringOut | Move immune, half or quarter effective | -1 | always | 5416 to 5418, 5437 |
| WringOut | Opponent HP below 50% | -1 | always | 5419, 5437 |
| WringOut | Opponent at full HP, AI not slower | +2, then +1 | always, then 90.2% | 5420, 5425 to 5433 |
| WringOut | Opponent at full HP, AI slower | +1, then +1 | always, then 90.2% | 5425, 5429 to 5433 |
| WringOut | Opponent HP 86% to 99% | +1 | 90.2% | 5421, 5432 to 5433 |
| WaterSpout | Move immune, quarter or half effective | -1 | always | 4618 to 4620, 4629 |
| WaterSpout | AI slower and *opponent* HP 70% or less | -1 | always | 4621, 4626, 4629 |
| WaterSpout | AI not slower and *opponent* HP 50% or less | -1 | always | 4622 to 4623, 4629 |
| Endeavor | Opponent HP below 70% | -1 | always | 4593, 4605 |
| Endeavor | AI slower: HP above 50% gives -1, else +1 | -1 or +1 | always | 4594, 4600 to 4601 |
| Endeavor | AI not slower: HP above 40% gives -1, else +1 | -1 or +1 | always | 4595 to 4596 |
| TrumpCard | Move immune, half or quarter effective | -1 | always | 5324 to 5326, 5356 |
| TrumpCard | 1 PP left | +3, end | always | 5328, 5352 |
| TrumpCard | 2 PP left | +1, then +1, end | always, then 60.9% | 5329, 5344 to 5348 |
| TrumpCard | 3 PP left | +1, end | 60.9% | 5330, 5347 to 5348 |
| TrumpCard | Opponent's ability is (or is guessed to be) Pressure | +1 | 88.3% | 5331 to 5334 |
| TrumpCard | Opponent evasion +5 or more, or AI accuracy -5 or less | +1, then +1 | always, then 60.9% | 5337 to 5338, 5344 to 5348 |
| TrumpCard | Else opponent evasion +3 or more, or AI accuracy -3 or less | +1 | 60.9% | 5339 to 5340, 5347 to 5348 |
| Punishment | Move immune, half or quarter effective | 0, end | | 5923 to 5925 |
| Punishment | Opponent's positive stages sum to 7 or more | +4 rung | see below | 5926 to 5927 |
| Punishment | Sum is 6 | +3 rung | | 5928 |
| Punishment | Sum is 5 | +2 rung | | 5929 |
| Punishment | Sum is 3 or 4 | +1 rung | | 5930 to 5931 |
| LastResort | Move immune, half or quarter effective | -1 | always | 5957 to 5959, 5964 |
| LastResort | AI has used every other move | +1 | always | 5960, 5968 |
| Superpower | Move immune, quarter or half effective | -1 | always | 4475 to 4477, 4487 |
| Superpower | AI Attack at -1 or lower | -1 | always | 4478, 4487 |
| Superpower | AI slower and HP 60% or more | -1 | always | 4479, 4484, 4487 |
| Superpower | AI not slower and HP above 40% | -1 | always | 4480, 4487 |
| Overheat | Move immune, quarter or half effective | -1 | always | 4728 to 4730, 4739 |
| Overheat | AI slower and HP 80% or less | -1 | always | 4731, 4736, 4739 |
| Overheat | AI not slower and HP 60% or less | -1 | always | 4732 to 4733, 4739 |
| CloseCombat | same three checks as Overheat | -1 | always | 5153 to 5164 |
| RecoilMove | Move immune, half or quarter effective | 0, end | | 6293 to 6295 |
| RecoilMove | AI has Rock Head or Magic Guard | +1 | always | 6296 to 6298, 6302 |
| KnockOff | Opponent HP 30% or more and not the AI's first turn out | +1 | 29.7% | 4574 to 4578 |
| BrickBreak | Opponent's side has Reflect or Light Screen | +1 | always | 4561 to 4562, 4566 |
| Pluck | Move immune, half or quarter effective | -1 | always | 4963 to 4965, 4977 |
| Pluck | AI's first turn out | +1 | 75% | 4966 to 4969 |
| Pluck | Otherwise continuing | +1 | 50% | 4972 to 4973 |
| Blizzard | Move immune, half or quarter effective | -3 | 80.5% | 6220 to 6222, 6229 to 6230 |
| Blizzard | Weather is hail | +1 | always | 6223 to 6225 |

Punishment's rungs do not stop at the first success the way the stat-swap ladders do: each rung from the starting one down to +1 is its own 50% roll and they add up (bug 2). From the +4 rung that is 0 to +10, averaging +5; from +3, 0 to +6; from +2, 0 to +3; from +1, 0 or +1.

The Facade row reads the opponent's status where the move cares about the AI's own (bug 7, battle_edits). The Water Spout rows read the opponent's HP where the move's power depends on the AI's (bug 8, battle_edits).

`Expert_Feint` (4892 to 4955):

| Check | Change | Chance | Lines |
|---|---|---|---|
| Opponent has not used a Protect-effect move | end, no change | 75% | 4911 to 4913 |
| AI badly poisoned, cursed, under Perish Song, infatuated, seeded or drowsy (Yawn) | +1 | 50% | 4916 to 4921, 4927 to 4928 |
| Else the opponent is below full HP and the AI has seen it holding Leftovers or Black Sludge | +1 | 50% | 4922 to 4928 |
| Opponent's Protect chain is 0 | +1 | 50% | 4932, 4937 to 4938 |
| Chain is 1 | +1 | 25% | 4933, 4942 to 4943 |
| Chain is 3 or more | -2 | always | 4934, 4947 |
| Chain is exactly 2 | falls into the chain-0 row: +1 | 50% | 4934 to 4938 |

The chain comes from `LoadProtectChain` (C lines 2538 to 2552), which is 0 unless the opponent's last protecting move was Protect, Detect or Endure by move id. The chain-2 row is bug 9.

`Expert_UTurn` (5085 to 5145):

| Check | Change | Chance | Lines |
|---|---|---|---|
| Move immune, quarter or half effective | -1, end | always | 5101 to 5103, 5110 |
| No other living Pokemon in the AI's party | end, no change | always | 5104 to 5105 |
| AI has a super-effective move on the Pokemon opposite it | -2, continue | 75% | 5106, 5114 to 5115 |
| No bench member out-damages the AI | -2, end | 75% | 5118 to 5121 |
| Opponent HP above 70% | +1, then the next row | 75% | 5124, 5130 to 5131 |
| Opponent HP above 30% (and the row above) | +1 | 50% | 5125, 5134 to 5135 |
| Opponent HP 30% or less | +1 | 25% | 5126 to 5135 |
| AI faster | +1 | always | 5138, 5142 |
| AI not faster | +1 | 50% | 5139, 5142 |

With no bench member the routine adds nothing; the decomp comment and the gist both say +2. The bench comparison (`IfPartyMemberDealsMoreDamage`, C lines 2106 to 2174) runs each bench member's moves, item, IVs and ability through the *active* Pokemon's stats, level and types (bug 10). "Super-effective move" (`AI_HasSuperEffectiveMove`, C line 3560) counts any move, status moves included, and looks at the Pokemon across from the AI rather than the current target.

`Expert_Fling` (5231 to 5294):

| Check | Change | Chance | Lines |
|---|---|---|---|
| Move immune, half or quarter effective, item is not King's Rock, Razor Fang, Poison Barb, Toxic Orb, Flame Orb or Light Ball | -1, end | always | 5250 to 5252, 5281 to 5283 |
| Same, item is one of those | end, no change | always | 5282 |
| Fling power below 30 (no item is 0) | -2 | always | 5254, 5262 |
| Power above 90, move super effective | +4, then +1 | always, then 75% | 5255, 5266 to 5277 |
| Power above 90, not super effective | +1, then +1 | 50%, then 75% | 5268 to 5277 |
| Power 61 to 90 | +1 | 75% | 5256, 5276 to 5277 |
| Power 30 to 60 | -1 | 50% | 5257 to 5258 |

## Items and abilities

`Expert_Trick` (4176 to 4413) serves Trick and Switcheroo. It sorts by the AI's own held item's hold effect (4222 to 4227). An item in none of the five lists, or no item, falls through to -3 (4229 to 4230). The "bad item" list is Macho Brace, the three Choice items, Iron Ball, Lagging Tail, Sticky Barb, the six Power items, Toxic Orb, Flame Orb and Black Sludge (4396 to 4413).

| AI's item | Check | Change | Lines |
|---|---|---|---|
| Choice item, Iron Ball, Lagging Tail, Sticky Barb or Power item | Opponent holds a bad item | -3 | 4233 to 4235 |
| same | otherwise | +5 | 4236 |
| Toxic Orb | Opponent holds a bad item | -3 | 4240 to 4241 |
| same | Opponent could be badly poisoned (no status, no Safeguard, not Steel or Poison, not Immunity, Magic Guard or Poison Heal) | +5 | 4242 to 4254 |
| same | Else the AI is immune in the same ways or has Klutz | -3 | 4257 to 4270 |
| same | Else | +5 | 4271 |
| Flame Orb | Opponent holds a bad item | -3 | 4275 to 4276 |
| same | Opponent could be burned (not Water Veil or Magic Guard, no status, no Safeguard, not Fire) | +5 | 4277 to 4286 |
| same | Else the AI has Water Veil or Magic Guard | -3 | 4290 to 4292 |
| same | Else the AI has Klutz | -5 | 4293 (to 1579) |
| same | Else the AI has a status, Safeguard, or is Fire | -3 | 4294 to 4299 |
| same | Else | +5 | 4300 |
| Black Sludge | Opponent holds a bad item | -3 | 4304 to 4305 |
| same | Opponent is Poison | go to the AI checks below | 4306 to 4309 |
| same | Opponent has Magic Guard | go to the Toxic Orb AI checks | 4310 to 4311 |
| same | Otherwise | +5 | 4312 |
| same | AI is Poison, or has Magic Guard or Klutz | -3 | 4315 to 4322 |
| same | Else | +5 | 4323 |
| Spicy, Dry, Sweet, Bitter or Sour pinch berry | Opponent holds a bad item or one of those berries | -3 | 4327 to 4328 |
| same | otherwise | +2 at 80.5% | 4329 to 4330 |

The opponent's item here is the one the AI has seen named, so an unrevealed bad item reads as no item. Bugs 11, 12 and 13 are in this routine.

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| ChangeUserAbility | AI's own ability is on the list | -1 | always | 4419 to 4420, 4425 |
| ChangeUserAbility | Opponent's ability (known or guessed) is on the list | +2 | 80.5% | 4421 to 4422, 4429 to 4430 |
| ChangeUserAbility | Neither is on the list | -1 | always | 4422 falls into 4425 |
| Recycle | The item Recycle would restore is not Chesto, Lum or Starf Berry (or there is none) | -2 | always | 4524 to 4525, 4531 |
| Recycle | It is one of those | +1 | 80.5% | 4526 to 4527 |
| Embargo | Always | +1 | 50% | 5225 to 5226 |
| GastroAcid | 25% of the time nothing | 0 | 25% | 5481 |
| GastroAcid | Otherwise, first | +1 | 75% | 5482 |
| GastroAcid | then opponent HP 70% or less | -1 | 50% | 5483 to 5485 |
| GastroAcid | then opponent HP 50% or less | -1 | always | 5488 to 5489 |
| GastroAcid | then opponent HP 30% or less | -1 | always | 5490 to 5491 |
| WorrySeed | Opponent has used Rest | +1 | always | 5979 to 5980 |
| WorrySeed | AI HP 50% or more | +1 | 50% | 5983 to 5985 |
| WorrySeed | Always | +1 | 75% | 5988 to 5989 |
| Ingrain | nothing | 0 | | 4463 to 4465 |

The desirable-ability list for Role Play and Skill Swap (4435 to 4461) is Speed Boost, Battle Armor, Sand Veil, Static, Flash Fire, Wonder Guard, Effect Spore, Swift Swim, Huge Power, Rain Dish, Cute Charm, Shed Skin, Marvel Scale, Pure Power, Chlorophyll, Shield Dust, Adaptability, Magic Guard, Mold Breaker, Super Luck, Unaware, Tinted Lens, Filter, Solid Rock and Reckless. The "neither" row is not mentioned by the decomp comment or the gist; it is how Emerald wrote it too.

Gastro Acid's net result, once past the 25% gate, by the opponent's HP:

| Opponent HP | Net change |
|---|---|
| above 70% | +1 |
| 51% to 70% | +1 or 0, even odds |
| 31% to 50% | 0 or -1, even odds |
| 30% or less | -1 or -2, even odds |

The decomp comment lists these one lower, because it leaves out the first +1.

## Field, weather and hazards

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| Hail | AI HP below 40% | -1, end | always | 4096, 4115 |
| Hail | Weather is sun, rain or sandstorm | +1 | always | 4097 to 4104 |
| Hail | and the AI knows Blizzard | +2 | always | 4105 to 4106 |
| Hail | and the AI has Ice Body | +2 | always | 4109 to 4111 |
| MudSport | AI HP below 50% | -1 | always | 4705, 4717 |
| MudSport | Opponent is Electric | +1 | always | 4706 to 4709, 4713 |
| MudSport | Opponent is not Electric | -1 | always | 4710, 4717 |
| WaterSport | same as Mud Sport with Fire | as above | | 4748 to 4760 |
| Gravity | Opponent has (or is guessed to have) Levitate, is under Magnet Rise, or is Flying | +1 | 75% | 4787 to 4793, 4799 to 4800 |
| Gravity | Else AI HP 60% or more | +1 | 37.5% | 4794 to 4800 |
| Tailwind | 25% of the time nothing | 0 | 25% | 4992 |
| Tailwind | AI faster (a tie is not) | -1 | always | 4993, 5003 |
| Tailwind | AI HP 30% or less | -1 | always | 4994, 5003 |
| Tailwind | AI HP above 75% | +1 | always | 4995, 4999 |
| Tailwind | AI HP 31% to 75% | +1 | 75% | 4996, 4999 |
| TrickRoom | Double battle | nothing | | 6198 to 6199 |
| TrickRoom | AI HP 30% or less and no other living party member | nothing | | 6200 to 6202 |
| TrickRoom | AI slower on the current field | +3 | 75% | 6205, 6210 to 6211 |
| TrickRoom | AI not slower | -1 | always | 6206 |
| LuckyChant | AI HP below 70% | -1 | always | 5502, 5514 |
| LuckyChant | Opponent has used a high-critical move | +1 | always | 5503 to 5505, 5510 |
| LuckyChant | Otherwise | +1 | 25% | 5506, 5510 |
| ToxicSpikes | 50% of the time nothing | 0 | 50% | 6018 |
| ToxicSpikes | Otherwise | +1 | always | 6019 |
| ToxicSpikes | and the AI knows Roar or Whirlwind | +1 | 75% | 6020 to 6026 |
| StealthRock | same as Toxic Spikes | as above | | 6274 to 6282 |
| MagnetRise | AI HP below 50% | nothing | | 6099 |
| MagnetRise | Opponent has used Earthquake, Earth Power or Fissure | +1 | always | 6100 to 6106 |
| MagnetRise | Opponent is Ground | +1 | always | 6109 to 6112, 6116 |
| MagnetRise | Opponent is not Ground | +1 | 50% | 6113, 6116 |

Hail only looks at Blizzard and Ice Body when another weather is up; in clear weather it adds nothing at all. The decomp comment and the gist list Ice Body as a separate bonus. Because the speed comparison already accounts for Trick Room, a fast AI under an active Trick Room reads as slower and is encouraged to use Trick Room again, which ends it; that is the right call. The Tailwind numbers in the table are after the 25% gate, so the +1 at full HP is 75% overall and the 75% case is 56% overall.

`Expert_Defog` (6125 to 6188) works on the opponent's side of the field.

| Check | Change | Chance | Lines |
|---|---|---|---|
| Opponent's side has Light Screen or Reflect, AI HP 30% or less, no other living AI party member | go to the -2 roll below, skipping the +1 | | 6145 to 6155 |
| Screens, otherwise | +1 | always | 6158 |
| Screens, opponent has living bench members and hazards (Spikes, Stealth Rock, Toxic Spikes) on its side | -1 | 50% | 6159 to 6163, 6171 to 6172 |
| No screens, hazards on the opponent's side | -2 | always | 6147 to 6149, 6167 |
| Then: AI HP below 70%, or opponent evasion -3 or lower | -2 | 80.5% | 6176 to 6181 |
| Then: opponent HP 70% or less | -2 | always | 6184 to 6185 |

## Status and utility

| Routine | Check | Change | Chance | Lines |
|---|---|---|---|---|
| MagicCoat | Opponent HP 30% or less | -1 | 60.9% | 4498 to 4500 |
| MagicCoat | AI's first turn out | +1 | 41.4% | 4503 to 4506 |
| MagicCoat | Not the first turn | -1 | 88.3% | 4504, 4511 to 4512 |
| Imprison | Not the AI's first turn out | +2 | 60.9% | 4636 to 4639 |
| Refresh | *Opponent* HP below 50% | -1 | always | 4646, 4650 |
| MiracleEye | Opponent is Dark | +2 | 47.3% (68.75% twice) | 4811 to 4814, 4820 to 4824 |
| MiracleEye | Else opponent evasion +3 or more | +2 | 68.75% | 4815, 4823 to 4824 |
| MiracleEye | Else | -2 | always | 4816 |
| PsychoShift | AI has no status | -10 | always | 5300 (to 1591) |
| PsychoShift | Otherwise, opponent HP 30% or more | +1 | 50% | 5301 to 5303 |
| HealBlock | Opponent has used a healing effect (list below), or the AI is seeded, or the opponent has Aqua Ring or Ingrain | +1 | 90.2% | 5379 to 5394, 5399 to 5400 |
| HealBlock | Otherwise | +1 | 33.8% (37.5% then 90.2%) | 5395, 5399 to 5400 |
| AquaRing | AI HP 30% or more | +1 | 50% | 6083 to 6085 |
| Captivate | Opponent's Sp. Atk is not at +0 | -1 | always | 6245 to 6246 |
| Captivate | and AI HP 90% or less | -1 | always | 6247 to 6248 |
| Captivate | and opponent's Sp. Atk at -3 or lower | -2 | 80.5% | 6251 to 6253 |
| Captivate | Opponent HP 70% or less | -2 | always | 6256 to 6257 |
| Captivate | Opponent's last move physical (or none yet) | -1 | 75% | 6260 to 6263 |

Magic Coat's line 4508 sits after an unconditional jump and never runs. Refresh reads the opponent's HP, as Emerald's did. Heal Block's healing list is Dream Eater, Recover-type, Roost, the Synthesis group, Rest, Swallow, the draining moves, Ingrain, Aqua Ring, Leech Seed, Healing Wish, Lunar Dance and the unused effect 157. The decomp comment and the gist give 56.4% for the last Heal Block row; the code gives 33.8%, because the roll at 5395 jumps *to* the bonus rather than past it.

`Expert_Snatch` (4655 to 4699):

| Check | Change | Chance | Lines |
|---|---|---|---|
| AI's first turn out | +2, end | 41.4% | 4669 to 4670, 4685 to 4686 |
| Otherwise, 11.7% of the time nothing | 0 | 11.7% | 4671 |
| AI slower, opponent HP above 25% | -2 | 88.3% | 4679, 4695 to 4696 |
| AI slower, opponent HP 25% or less, opponent has used Recover-type or Defense Curl | +2 | 41.4% | 4680 to 4686 |
| AI slower, otherwise | +1, else -2 | 10.2%, else 79.3% | 4682, 4690 to 4696 |
| AI not slower, AI below full HP or opponent HP below 70% | -2 | 88.3% | 4673 to 4674, 4695 to 4696 |
| AI not slower, otherwise | -2 | 67.6% | 4675 to 4676, 4695 to 4696 |

`Expert_HealingWish` (6307 to 6351) serves Healing Wish and Lunar Dance.

| Check | Change | Chance | Lines |
|---|---|---|---|
| AI HP 80% or more and not slower | -5, else end with nothing | 25% / 75% | 6319 to 6322 (to 1579) |
| AI HP above 50% | -1 | 80.5% | 6325, 6347 to 6348 |
| AI HP 50% or less: pass a 25% gate, then | +1 | 25% | 6326 to 6327 |
| after the gate, AI has no super-effective move | +1 | 25% | 6328 to 6330 |
| after the gate, a bench member out-damages the AI | +1 | 50% | 6333 to 6338 |
| AI HP 30% or less | +1 | 50% | 6341 to 6343 |

## Apparent bugs

Fixed on 2026-09-22: bug 2, Punishment (vanilla fix, approved by Ian), bugs 3, 7 and 8 (charge-turn, Facade, Water Spout and Eruption; battle_edits, vanilla fixes approved by Ian on 2026-09-15), and bug 14, the ability byte (Oxide). Bug 10, the bench damage check, was put to Ian and kept as vanilla has it. The rest stand as vanilla has them.

Every entry is present in vanilla Platinum except bug 14, which Oxide introduced. For script bugs the vanilla line is the same line on `main`, since the file is unchanged; for C bugs the vanilla line is given.

1. **Thunder never reaches its routine.** Present in vanilla, `Expert_Main` line 1719. The line tests `BATTLE_EFFECT_SKIP_CHARGE_TURN_IN_SUN` (151), which line 1716 has already sent to `Expert_ChargeTurnNoInvuln`, so `Expert_Thunder` (3975 to 3990) has no way in. Thunder's own effect, `BATTLE_EFFECT_THUNDER` (152), matches no dispatch line and gets nothing from the Expert flag. The decomp flags it at 1718.
2. **Punishment's ladder adds every rung.** Present in vanilla, lines 5934 to 5948. Each `AddToMoveScore` falls into the next rung's roll instead of jumping to the end, unlike the identical-looking ladders in Power Swap (5738 to 5761) and Guard Swap. The decomp comment and the gist describe a stop-at-first ladder (50% +4, 25% +3 and so on). The code gives the sum of independent coins: up to +10, averaging +5, from the top rung. This is the largest single bonus in this half; it cannot on its own push a score past 127.
3. **Semi-invulnerable moves get a bonus when resisted.** Present in vanilla, lines 4017 to 4019 (the decomp marks it "Bug?" at 3997). Fly, Dig, Dive and Bounce (when the opponent has not used Protect and the AI has no Power Herb), and Shadow Force always, score +1 and stop when the move is immune, quarter or half effective. The sibling routine does -2 in the same case (3943 to 3945), and the jump also skips every later check.
4. **Assurance's berry check can never match.** Present in vanilla, lines 5202 to 5203 and the table at 5218 to 5221. The routine loads the AI's hold effect (`LoadHeldItemEffect`) and compares it with `ITEM_JABOCA_BERRY` and `ITEM_ROWAP_BERRY`, which are item ids 211 and 212; hold effects run only to about 145. An AI holding either berry gets the 25% case instead of 50%.
5. **Power Swap and Guard Swap give nothing for a second difference of exactly 1.** Present in vanilla, lines 5714, 5721, 5728 and 5848, 5855, 5862. In the three rows where the first difference is positive, the second test is `IfLoadedEqualTo 0`; in the row where the first difference is 0 it is `IfLoadedGreaterThan 0`. So a second difference of +1 scores nothing while +0 scores up to +3, which puts a bigger advantage below a smaller one.
6. **`IfBattlerDealsMoreDamage` measures the opponent hitting itself.** Present in vanilla, `trainer_ai.c` lines 2228 to 2236 (same lines on `main`). `TrainerAI_CalcDamage` always uses `AI_CONTEXT.defender` as the target, and this command passes the defender as the attacker too, with the AI's IVs. So Me First and Copycat compare "the opponent's last move used on itself" with "the AI's best move on the opponent". A Water-type opponent's Water move is resisted by itself, for example, so it rarely wins the comparison.
7. **Facade checks the opponent's status.** Present in vanilla, line 4123 (flagged at 4122). See the battle_edits section.
8. **Water Spout and Eruption check the opponent's HP.** Present in vanilla, lines 4622 and 4626 (flagged at 4617). See the battle_edits section.
9. **Feint treats a Protect chain of 2 like a chain of 0.** Present in vanilla, line 4934. The label is `Expert_Feint_ProtectChain2OrMore` but the test is `IfLoadedGreaterThan 2`, so a chain of exactly 2 falls through into the chain-0 case (50% +1) instead of -2.
10. **The bench damage comparison uses the active Pokemon's body.** Present in vanilla, `trainer_ai.c` lines 2156 to 2165 (same on `main`). `IfPartyMemberDealsMoreDamage` passes the bench member's moves, item, IVs and ability but the active battler's id, and `TrainerAI_CalcDamage` takes stats, level, types and STAB from that battler. It compares move sets, not Pokemon. Used by U-turn (5118) and Healing Wish (6333).
11. **Trick with Black Sludge against Magic Guard jumps to the Toxic Orb checks.** Present in vanilla, line 4311. It goes to `Expert_Trick_CheckAttackerForPoison` rather than `Expert_Trick_CheckAttackerForSludge`. A non-Poison AI that is statused, under Safeguard, Steel, or has Immunity or Poison Heal then scores -3 instead of +5, although Black Sludge would still hurt it.
12. **Trick with Flame Orb and Klutz gives -5, not -3.** Present in vanilla, line 4293. Every other "keep the item" outcome in the routine is -3 (4230); this one jumps to the shared `ScoreMinus5`.
13. **Trick's disruptive list leaves out Macho Brace and lists one Power item twice.** Present in vanilla, lines 4343 to 4358 (flagged at 4344). `HOLD_EFFECT_LVLUP_DEF_EV_UP` appears at 4352 and 4354, which is harmless. Macho Brace (`HOLD_EFFECT_EVS_UP_SPEED_DOWN`) is on the opponent-side bad list but not here, so an AI holding it falls through to -3 instead of +5.
14. **Revealed abilities above 255 are stored truncated.** Introduced by Oxide. Oxide widened `BattleMon.ability` and the parameter of `BattleAI_SetAbility` (`battle_script.c` line 12176) to u16, but `AIContext.battlerAbilities` is still `u8` (`include/battle/ai_context.h` line 28, the same line on `main`, where every ability fitted). An announced ability id is stored modulo 256, and `LoadBattlerAbility` then returns the wrong ability for the opponent. In this half that affects Gravity (Levitate, 4787), Trick (Immunity, Magic Guard, Poison Heal, Water Veil, 4250 and 4277), Role Play and Skill Swap (4421) and Trump Card (Pressure, 5331). Examples from `generated/abilities.txt`: Quark Drive (282) reads as Levitate (26), Protosynthesis (281) as Wonder Guard (25), Earth Eater (297) as Water Veil (41), Well-Baked Body (273) as Immunity (17), Embody Aspect 2 (302) as Pressure (46).

Three smaller things are dead code rather than wrong behaviour: line 4508 in Magic Coat sits after a `GoTo`, and the extra `PopOrEnd` lines at 6120 to 6123, 6234 and 6286 to 6287 can never run.

The decomp comments (and the gist, which copies them) disagree with the code in these places, all covered in the tables above: U-turn's last-Pokemon case (no change, not +2), Heal Block's default (33.8%, not 56.4%), Metal Burst's taunt rows and 25% row, Me First and Copycat's damage comparison, Psych Up and Heart Swap's order, Power Trick's -2 at low HP, Role Play's -1 when neither ability is listed, Gastro Acid's net values, Hail's Ice Body, and Punishment's ladder. The gist also gives Smelling Salts +2; the code gives +1 (line 4171). pokemow.com's per-move Expert pages sit behind a menu that could not be read, so only its general notes were checked; its claim that the AI always knows the player's held item does not hold for the item checks in this half.

## The battle_edits fixes

| Fix | In this half? | Where |
|---|---|---|
| Fire Fang vs Wonder Guard | No | battle engine, not the AI script |
| Rage glitch | No | battle engine, not the AI script |
| Water immunity vs Dry Skin check | No | Basic, line 78 (`basic.md`) |
| Sunny Day check | No | before line 3803 (`basic.md` and `expert-1.md`) |
| Foresight / Odor Sleuth Ghost check | No | `Expert_Foresight`, lines 3607 to 3620 (`expert-1.md`) |
| Facade status check | Yes | line 4123 |
| Leaf Guard Sunny Day logic | No | `Expert_SunnyDay`, line 3790 (`expert-1.md`) |
| Water Spout / Eruption HP check | Yes | lines 4622 and 4626 |
| Charge-turn scoring fix | Yes, as far as the code shows | lines 4017 to 4019 |
| Thunder scoring fix | The routine is here, the fault is in `Expert_Main` | line 1719, routine 3975 to 3990 |
| Discharge double-battle scoring fix | No | Tag Strategy, around line 7255 (`other-flags.md`) |

The guide itself was not read for this file, so the charge-turn entry is matched from the code: lines 4017 to 4019 are the only charge-turn scoring the decomp marks as doubtful.

**Facade** (4120 to 4127). `IfNotStatus AI_BATTLER_DEFENDER, MON_CONDITION_FACADE_BOOST` gives +1 when the *opponent* is poisoned, badly poisoned, burned or paralysed. Facade doubles when the *user* has one of those. The fix reads `AI_BATTLER_ATTACKER` on line 4123. Scores after it: +1 when the AI is statused, whatever the opponent has; nothing when only the opponent is. The status mask is already right (sleep and freeze are excluded, as the move excludes them).

**Water Spout and Eruption** (4610 to 4632). The -1 fires when the *opponent's* HP is 50% or less (AI not slower) or 70% or less (AI slower). The move's power falls with the *user's* HP. The fix changes `AI_BATTLER_DEFENDER` to `AI_BATTLER_ATTACKER` on lines 4622 and 4626. Scores after it: -1 when the AI's own HP is 50% or less and it moves first, or 70% or less when it moves second (it will take a hit before attacking). The resisted and immune -1 is unchanged.

**Charge-turn** (4017 to 4019). Fly, Dig, Dive and Bounce reach these lines when the opponent has not used Protect and the AI has no Power Herb; Shadow Force always reaches them. An immune, quarter or half effective move then gets +1 and the routine ends. The consistent fix is to send these three lines to a penalty, as `Expert_ChargeTurnNoInvuln` does with -2. Scores after it: resisted moves go from +1 to the penalty (a swing of 3 with -2), and they still skip the later bonuses. Basic already punishes immunity heavily, so the change matters most for resisted moves.

**Thunder** (dispatch line 1719). The fix changes the effect on that line to `BATTLE_EFFECT_THUNDER`. Solar Beam's scoring does not change, because line 1716 already catches it. Thunder today gets no Expert adjustment at all; after the fix it gets -3 at 80.5% when resisted or immune, -3 at 80.5% in sun (where its accuracy drops to 50%), and +1 in rain.

## Oxide consequences

**Effect ids.** Every routine in this half is reached only through `Expert_Main`'s list of vanilla effect ids (0 to 276). A move with one of Oxide's effects 277 to 406 matches nothing and gets no Expert adjustment, the same as a plain attack. A new move that reuses a vanilla effect gets that effect's routine, assumptions included. Examples from `res/moves`:

| Move | Effect | What this half does with it |
|---|---|---|
| Solar Blade | 151 | Solar Beam's charge-turn routine, sun bonus included |
| Phantom Force | 272 | `Expert_ShadowForce`, including bug 3 |
| Volt Switch, Flip Turn | 228 | `Expert_UTurn` |
| Armor Cannon | 229 | `Expert_CloseCombat` |
| Draco Meteor, Leaf Storm, Fleur Cannon | 204 | `Expert_Overheat` |
| Wild Charge, Head Charge, Brave Bird, Wood Hammer | 198 | `Expert_RecoilMove` |
| King's Shield, Spiky Shield, Baneful Bunker | 111 Protect | seen by every "has used Protect" check, but Feint's chain (by move id) reads 0 |
| Shore Up | 132 (Synthesis group) | counted by Heal Block's list |
| Meteor Beam, Electro Shot, Geomancy, Freeze Shock, Ice Burn | 324, 325, 318, 363, 364 | nothing: no Power Herb bonus, no resisted penalty |
| Hurricane | 341 | nothing (Thunder's routine is unreachable anyway) |
| Snowscape | 319 | nothing, where Hail would get `Expert_Hail` |
| V-create, Clanging Scales | 291, 342 | nothing, where Close Combat gets its routine |
| Hex, Venoshock, Infernal Parade | 287, 280, 321 | nothing, where Facade gets its routine |
| Fishious Rend, Bolt Beak | 382 | nothing, where Payback gets its routine |
| Parting Shot | 389 | nothing |
| Power Split, Guard Split | 279, 278 | nothing |

The "opponent has used" lists inside routines also name vanilla effects only. Lucky Chant does not see the always-critical effects (282, 366) or 368; Heal Block does not see Strength Sap (378), Life Dew (383), Draining Kiss-style effects 315, 347 and 348, or Pollen Puff (380); Feint's Protect check does not see Wide Guard or Quick Guard (371).

**Move ids.** Several checks name moves directly and so ignore Oxide's additions: Mirror Coat's Counter (3882), Hail's Blizzard (4105), Worry Seed's Rest (5979), Magnet Rise's Earthquake, Earth Power and Fissure (6100 to 6102, not High Horsepower, Drill Run, Bulldoze, Stomping Tantrum and the rest), Toxic Spikes' and Stealth Rock's Roar and Whirlwind (6020, 6276, not Dragon Tail or Circle Throw), the Copycat list, and Feint's Protect chain (Protect, Detect, Endure only, C line 2545).

**Abilities.** All ability comparisons here load the id into a 32-bit value and compare with `.long` constants, so a u16 id compares correctly. The problem is the stored copy of a revealed opponent ability, bug 14. The ability lists (Role Play's, Trick's, Recoil's Rock Head and Magic Guard) name vanilla abilities only, so, for example, Rock Head's Oxide relatives get no recoil bonus. The opponent-ability guess uses the species' two regular abilities, so a hidden ability is never guessed.

**Types.** The Fairy type is 18 and sits in the type chart ahead of the Foresight marker, so every "immune, quarter or half effective" check in this half sees Fairy's resistances and its Dragon immunity. The type lists do not mention Fairy and mostly do not need to (sand immunity, hail immunity, Trick's Poison, Steel and Fire, Mud Sport's Electric, Gravity's Flying, Miracle Eye's Dark, Magnet Rise's Ground). Mirror Coat's "special types" list (3922 to 3931) leaves Fairy out, so a Fairy opponent that has not attacked yet counts as a physical attacker, and a taunted or not-yet-attacking Fairy draws the 49% +4 for Mirror Coat. `LoadTypeFrom` reads only type 1 and type 2.
