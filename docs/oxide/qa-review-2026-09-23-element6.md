# QA review: element 6's second batch (2026-09-23)

## What was reviewed

Element 6 (battle AI) merged into `oxide` on 2026-09-22 as `10782dd04` without a QA pass, on Ian's word, because the machine kept crashing. This pass covers exactly the commits that merge brought in, `git log 10782dd04^1..10782dd04^2`: 26 commits plus one merge of `oxide` into the branch, 16 files, 312 lines added and 49 removed. The first ten element 6 commits had their own pass, `qa-review-2026-09-22-element6.md`; the first four commits here act on its findings.

| Commit | What it does |
|---|---|
| f421eac1b | Vanilla fix: four AI paths read Weather Ball's weather type, not its listed Normal |
| 3fe957ac6 | Vanilla fix: the post-knockout pick costs Weather Ball at double power and the weather's type |
| 4f162c233 | Docs: the earlier pass's corrections, and the two fixes above recorded |
| cae736528 | battle_edits: Basic's water immunity check tests Dry Skin |
| 3a6c37ff0 | battle_edits: Basic's Sunny Day check looks for Leaf Guard |
| 6d03a46f6 | battle_edits: Expert's Foresight reads the target's types |
| fb999558d | battle_edits: Expert's Leaf Guard Sunny Day test is no longer inverted |
| 9d99cd0a0 | battle_edits: semi-invulnerable moves take -1 into a resisting target |
| 0b3c2eab6 | battle_edits: Facade checks the user's status |
| 65a76ecc7 | battle_edits: Water Spout and Eruption check the user's HP |
| ab57dd9b2 | battle_edits: Expert reaches its Thunder routine |
| a20cd3b5c | battle_edits: Discharge checks a Ground partner first |
| 0f8d7a66f | battle_edits, engine: Fire Fang no longer bypasses Wonder Guard |
| 67f219adb | battle_edits, engine: leaving Rage clears only Rage |
| ff1f6519c | Docs: the eleven battle_edits fixes recorded |
| 87aa84272 | Vanilla fix: trainer form Pokemon get their form's stats |
| 186735fe7 | Docs: the form stats fix and its in-game check |
| c6f61ebe2 | Docs: the doubles review, `battle-ai/doubles.md` |
| cd2676891 | Merge of `oxide` into the branch |
| 001dfaff6 | Vanilla fix: spread moves stop reading a fainted partner |
| 33ba4d182 | Vanilla fix: Steel in Earthquake's partner check, Rock in Surf's |
| 11278e299 | Vanilla fix: Mold Breaker gets past the partner's ability |
| 13eddbfb0 | Vanilla fix: Follow Me with no partner scores -10 |
| a1ef98af2 | Change: Explosion and Self-Destruct penalised beside a partner |
| effc209fb | Data: Poison Gas hits both foes, registered in `verify_narcs.py` |
| 29d508cc4 | Docs: the doubles rulings applied |

Nothing in the range is vendored or generated. The merge `cd2676891` has no hand-resolved hunks (`git show --cc` prints none), so it was not read line by line.

The gate was run once on the current `oxide` head, `a0efaf8ec`, which contains all 26 commits, by the Overseer rather than by this pass: `bash tools/oxide/integrate.sh --verify-only --rom ~/oxide-playtest/pokeplatinum-oxide-a0efaf8ec.nds` passed 27 of 27 with no warnings, and the ROM's SHA-1 `57a4f055` matches GitHub's build of that commit (checked again here with `sha1sum` against the downloaded `.sha1`).

No finding is serious. Every code change does what its message says. One fix was incomplete in a way that contradicted its own message and element 6's other Weather Ball fix, and is fixed; one gap in the form stats fix needs Ian.

## Findings, most serious first

### 1. The post-knockout Weather Ball fix missed deep fog (low, fixed in 45ad243a6, VANILLA FIX)

`3fe957ac6` doubles a bench Weather Ball's power only when `Move_CalcVariableType` gives it a type other than Normal, and its message says that is "exactly when there is weather and no Cloud Nine or Air Lock, as BtlCmd_CalcWeatherBallParams sets it". It is not. The battle doubles the power whenever `fieldConditionsMask & FIELD_CONDITION_WEATHER` is set (`battle_script.c`, `BtlCmd_CalcWeatherBallParams`), and that mask includes `FIELD_CONDITION_DEEP_FOG` (`include/constants/battle/condition.h:131` to `135`), where the move stays Normal at 100 power. So in fog the pick still costed it at 50, while element 6's other fix, the Weather Ball case in `TrainerAI_CalcDamage`, already doubles it there.

Fixed as its own commit on `worktree-element6`: the test is now the battle's own (Weather Ball, `NO_CLOUD_NINE`, any weather), and the type passed stays `moveType`, which in fog is 0, meaning the listed Normal. Outside fog nothing changes. Checked by reading the three places side by side and by compiling `battle_lib.c` (`ninja -j1` on its object). The ROM was built on GitHub (see "Build of the fix" below). Because the underlying bug is vanilla, this is flagged for Ian as a vanilla fix, although it only completes one he already approved.

### 2. Trainer form Pokemon keep their base form's ability (low, Ian's call)

`87aa84272` recalculates a trainer form Pokemon's stats after the form is set, as pret's fix does, and says only that. The ability is chosen earlier, from the base form's record, and nothing recalculates it. In vanilla that is harmless, because every form of Rotom and Wormadam shares its ability. In Oxide it is not: the base ROM import (`c69ef83a6`) gave the Sandy and Trash Wormadam records Snow Cloak, where the base form has Anticipation (`res/pokemon/wormadam/forms/sandy/data.json` and `trash/`, against `main`'s Anticipation). So Beauty Devon's two Wormadam and Worker Jackson's Wormadam-Trash fight with Anticipation, while the player's Burmy that evolves into one of those forms gets Snow Cloak, because evolution recalculates the ability through `BoxPokemon_CalcAbility`, which does read the form (`evolution.c`, after the species is set). The damage calculator's trainer export also says Anticipation, which matches the game as it is.

Two questions for Ian, and nothing is changed until he answers: whether Snow Cloak on those two forms is intended at all (it looks like a base ROM slip, since the forms share Anticipation in every official game), and, if it is, whether the party builder should also call `Pokemon_CalcAbility` after setting the form for a member with no ability request. Rotom's forms all have Levitate, so Volkner's and Fantina's Rotom are unaffected either way.

### 3. doubles.md's line numbers predated its own fixes (nit, fixed in c789a1629)

The file said its line numbers were the branch's, but they were taken at `c6f61ebe2`, before the doubles fixes, which then moved the four spread-move routines down by 7 to 72 lines (`TagStrategy_Earthquake` 7148 to 7155, `TagStrategy_SpreadFireMove` 7340 to 7412). The note now names the commit and says to search by label.

### 4. Two small inaccuracies in the element 6 docs and code (nit, open, element 6's)

`README.md` line 85 says every vanilla fix "is marked in `script.s`" with an "Oxide, vanilla fix" comment. Several are in C (in `trainer_ai.c`, `battle_lib.c`, `battle_controller_player.c` and `trainer_data.c`) and are marked there instead. And `9d99cd0a0` made `Expert_ChargeTurnWithInvuln_ScorePlus1` score -1 but kept the label's name (`script.s:4078`), which will mislead the next reader of that routine; renaming it touches three branches, so it is left to the track.

### 5. One commit message's species list is short by one (nit, no action)

`cae736528` names the Dry Skin Pokemon in Oxide as Croagunk, Toxicroak, Parasect, Shellos and Gastrodon; Paras has it too (`res/pokemon/paras/data.json`). The fix itself is by ability, so it covers Paras.

## Claims re-checked

| Claim | Where | Result |
|---|---|---|
| The base ROM's overlay 14 carries exactly the seven guide AI edits, thirteen bytes | `ff1f6519c` and the seven commits | Confirmed. Overlay 14 of `~/roms/base.nds` differs from `~/roms/vanilla.nds` in 13 bytes at the ten guide offsets (0x4DAC, 0x6308, 0x6310, 0x9DC8, 0x9DDC, 0xA190, 0xA708, 0xA7EC, 0xB108, 0xB120), each with the guide's new value, and nowhere else |
| Thunder, Discharge, Fire Fang and Rage were not in the base ROM | four commits | Confirmed: overlay 14 at 0x7884 is still 0x97 in the base ROM, and overlay 16 at 0x205D4 and 0x11574 still holds vanilla's 0x11 and 0x01 |
| Each guide offset holds the vanilla byte it expects | `ff1f6519c` | Confirmed for all twelve single-byte edits above plus Fire Fang and Rage. The Discharge reorder at 0xE188 was not byte-checked |
| The guide's bytes are what the source edits assemble to | the eleven commits | Rerun against the built ROM `a0efaf8ec` instead of a fresh assembly: all eleven single-byte AI edits (the ten base-ROM ones and Thunder's 0x98) sit in its overlay 14 at the vanilla offset plus 0xE0, the shift the earlier fixes introduced. The "seven edits alone reproduce the base overlay exactly" build was not repeated, since it needs a local assemble of a throwaway tree |
| The effect ids behind Thunder and Fire Fang | `ab57dd9b2`, `0f8d7a66f` | Confirmed from `generated/move_battle_effects.txt`: Skip Charge Turn In Sun 151 (0x97), Thunder 152 (0x98), Shadow Force 272 (0x110), Flinch Burn Hit 273 (0x111) |
| Vanilla lines 962, 2523 and 3665 of `trainer_ai.c` | `f421eac1b` | Confirmed on `main` |
| Six trainer Pokemon change with the form stats fix; Tuber Jared and Mariel do not | `87aa84272` | Confirmed from `res/trainers/data/`: Volkner (both), Fantina's rematch, Beauty Devon (two), Worker Jackson; the dummies' Rotom and Deoxys are unused. Four `Pokemon_CalcStats` calls are in the current source. "All four reach it in the built ROM" was not rerun at the binary level |
| Rotom-Mow's and Wormadam-Trash's stats with and without the fix | `186735fe7` | Confirmed: all twelve "with" figures and all eight "before" figures recomputed from the form records, level, IVs (241 and 225 scale to 29 and 27) and the natures `calc_trainers.py` rolls (Modest, Relaxed) |
| Poison Gas's range is now 0x4, like Smog's, and `pl_waza_tbl` differs from the base ROM only where registered | `effc209fb` | Confirmed on the built ROM: member 139's range bytes read `0400` (base `0800`), Smog's `0400`; across the 471 shared members the only other differing bytes are offset 11 (95 members, the King's Rock flag) and offset 4 (3 members, the Fairy retypes), both registered. `MOVES_DIVERGED` in `import_base_rom.py` covers the same field, and the gate's importer dry run reads 0 |
| 37 double battles and 112 AI Pokemon | `c6f61ebe2` | Not rerun. Spot checks hold: Lady Kylie's Clefairy defaults to Follow Me and Rich Boy Roman has one Pokemon; the Jubilife grunt's Stunky knows Poison Gas; Jo and Pat's Claydol knows Self-Destruct and their Nidoking Earthquake |
| 52 moves reach the immunity checks | `4f162c233` | Not rerun; the figure is the earlier pass's own count, carried into the README |
| The build succeeds with every fix | `3fe957ac6`, `ff1f6519c` | Confirmed by the gate on `a0efaf8ec` |

The engine reading behind the fixes was also checked where a fix depends on it: `AI_BATTLER_ATTACKER`'s ability is read as its real one by `LoadBattlerAbility`, so the Mold Breaker test sees it; `IfBattlerFainted` tests `battlersSwitchingMask`, as the doubles fixes say; every one of the six abilities the Mold Breaker fix skips goes through `Battler_IgnorableAbility` in `battle_lib.c`; and `moveHitType` is written from the battle's own move type in `BattleControllerPlayer_UpdateFlagsWhenHit`.

## Build of the fix

`worktree-element6` was pushed so GitHub could build it, and `tools/oxide/fetch-rom 45ad243a6` built and downloaded the fix's ROM (SHA-1 `c8b51b43`, checked by the script against the build's record). Compared with the gate's ROM of `a0efaf8ec`, no data file differs. Overlay 16, which holds `battle_lib.c`, is 64 bytes longer, and arm9 and overlays 13 and 14 differ by a few dozen bytes, which is the relink moving addresses behind the grown code (design doc findings log, 2026-09-21). The full gate was not rerun on this ROM; the fix touches no table any gate check reads. What the fix changes in play needs deep fog, a trainer whose bench Pokemon knows Weather Ball, and a knockout, and was not tested in the game.
