# QA: the encounter branch before it merges (M8 D4, D5 and trainer natures)

A `/qa-pass` on 2026-09-22 over `worktree-encounter-step0` against its merge
base with `oxide`, `458a34f59`, run read-only in the encounter-step0 worktree.
Nothing was fixed: each defect below is in the encounter track's files or in
the one engine change it took on, so each goes back to that track. Step 4 (the
gate) was skipped because the integration runs it on the merged tree. No build
was made; the worktree's existing ROM was used where a check needed one.

## What was reviewed

| Commit | What it does |
|---|---|
| `5cc5c08af` | D4: a Moves view with the reverse index, and the stub-effect flag |
| `79ac5651b` | A species in a table opens its dex page; Back via browser history |
| `030c4a8ed` | Species page in two columns, fewer facts, sentence case |
| `e8a7ce09f` | D5: the vendored calculator runs on Oxide's data, offline |
| `80ca7f228` | D5: the calculator's generated skin, and the shared theme toggle |
| `897e2c17e` | Docs: D5 and the visual design sign-off |
| `67f520edf` | The calculator's picker offers Oxide's species and 32 forms |
| `217734b2d` | Every trainer's party in the calculator, natures included |
| `94e97cbbc` | The calculator's picker opens at the species already picked |
| `40dc96cd2` | Engine: a trainer Pokemon can name its nature |

The range is 42 files and about 9,900 added lines. About 7,000 of those are
vendored (seven libraries and eleven theme images under `calc/js/vendor/oxide/`)
or generated (`oxide-skin.css`, `calc_names.json`); those got a provenance,
licence and regeneration check rather than a line read. The authored code, and
`40dc96cd2` above all, got the time. The visual claims (headless Chrome renders,
Back and forward, the frame following the toggle) were not rechecked.

## Findings

### 1. A trainer file can name `NATURE_COUNT`, and the game then hangs

`trainerproc` looks the nature up in `enum Nature`, and `generated/natures.txt`
ends with `NATURE_COUNT`, so `"nature": "NATURE_COUNT"` packs without a word as
nature 26 in the high byte. `TrainerMon_Personality` then steps until the
personality mod 25 equals 25, which never happens, so building that party loops
forever. Shown on a scratch copy of `res/trainers/data` run through the
worktree's own `trainerproc`, and with the helper lifted from `src/trainer_data.c`
into a host harness:

```
[NATURE_COUNT] rc=0           member 246 packs fa1a0f00 (was fa000f00)
echo "250 15 299 246 62 0 136 26" | timeout 5 ./h   ->  exit 124, never returned
```

In the same probe a nature given as a number or `true` is dropped without an
error and the member rolls as before, where the neighbouring `gender` field
refuses anything it does not know. A misspelt name (`"Adamant"`) is refused
correctly. The fix is a range check in `tools/dataproc/src/trainerproc.c`
(nature below `NATURE_COUNT`) and an error for a non-string, non-null value.
No trainer names a nature yet, so this does not block the merge, but it should
be fixed before Phase 5 starts using the field. Status: open, for the encounter
track (it owns this engine change by Ian's decision).

### 2. The calculator orders a dual type's two factors differently from the game

The calculator's Generation 4 mechanics (`calc/calc/mechanics/gen4.js`, lines
643 and 644) apply the defender's first type, then its second, flooring each
time. The game walks `sTypeMatchupMultipliers` in table order
(`src/battle/battle_lib.c`, the loop at 2630, `ApplyTypeMultiplier` at 7604),
so for Crunch into Bronzor (Steel/Psychic) the Psychic entry comes first. When
the rolled damage is odd, the two orders differ by one:

| Crunch into Bronzor, level 50 | Low | High |
|---|---|---|
| Calculator, and D5's hand check | 42 | 50 |
| The game's chart order | 43 | 51 |

So D5's claim that five matchups "match hand-computed Generation 4 rolls, roll
for roll" holds for the four single-typed defenders, and the fifth hand check
used the calculator's order rather than the game's. This is upstream's
behaviour, not an Oxide patch, and it only moves damage by one point when one
type resists and the other is weak. Ian's pending in-game roll would settle it
if he uses this exact matchup. Status: Ian's call (accept and note it in
`VENDORED.md`, or patch `gen4.js` to apply the two factors in chart order).

### 3. The "unscripted" flag will be wrong for four moves once this merges

`pokedex.stub_effects` calls a donor effect a placeholder when its script is a
copy of effect 0's plain hit or of Splash's. On `oxide`, element 4 implemented
`BATTLE_EFFECT_ALWAYS_CRITICAL` in C (`2f84be2ef`, `battle_lib.c:7160`) and left
its script as a plain hit, which is correct, since the crit is decided in C.
Run over the `oxide` checkout with this branch's code:

```
stub effects: branch 130, oxide 53
flagged on oxide but named in C: ALWAYS_CRITICAL
moves: MOVE_FLOWER_TRICK, MOVE_FROST_BREATH, MOVE_STORM_THROW, MOVE_WICKED_BLOW
```

After the merge the Moves view marks those four as doing nothing extra, and
`calc_export`'s report lists them as modelled with an effect the game lacks,
when the game has it. Every other flagged effect on `oxide` has no C reference,
so this is the only false positive today. Any C-only effect element 4 adds
later will hit the same thing. The fix is an exception list of C-implemented
effects, or a check for the effect's name in `src/battle/`. Status: open, for
the encounter track; it does not block the merge.

### 4. Two vendored libraries arrive with no licence notice

All seven vendored libraries and the eleven jQuery UI images are byte-identical
to the CDN URLs upstream loaded (checked by fetching each and comparing
SHA-256), and all are MIT or MIT and Zlib, as `VENDORED.md` says. But MIT asks
for the copyright and permission notice to travel with the copy, and no licence
file was added under `js/vendor/oxide/`. jQuery, jQuery UI, ag-grid and pako
carry a header naming their licence. `object_hash-3.0.0.min.js` (jsDelivr's
wrapper header only) and `ag-theme-alpine-dark-28.2.1.css` carry none. A
`LICENSES` file beside them, or the notices appended to `VENDORED.md`, would
close it. Status: open, for the encounter track.

### 5. Small things

- The build plan's D4 paragraph says 96 natives "differ only in the King's
  Rock flag". Rerun: 95 gained it (the same 95 as `verify_narcs`'
  `KINGS_ROCK_NATIVES`), and 80 differ in that flag alone.
- `calc_export.species_entry` says weight is "stored as tenths of a pound",
  but `weight_pounds` is pounds (Bulbasaur 15.2), and the code treats it as
  pounds. Only the comment is wrong.
- `VENDORED.md` still says the calculator "shows broken images" until Oxide's
  sprites are wired up; the server now answers those requests.
- The 18 Z-moves Oxide holds as physical and special twins map to one
  calculator name each, so the special silently replaces the physical in the
  blob (919 moves in, 901 out). Harmless while nothing learns them and their
  power is 0.
- The importer now skips a re-tuned member's IV scale without saying so. The
  dry run counts `AUTHORED` tables it leaves alone; a matching count of members
  left alone for naming a nature would keep the divergence visible once natures
  are in use.

Status for all five: open, for the encounter track.

### Out of scope, surfaced by the new Moves view

Fire Fang differs from vanilla by gaining the Snatch flag. `verify_narcs` against
the base ROM passes it, so the base ROM carries the same flag. It looks like a
stray DSPRE edit rather than a design choice, and it is harmless in battle,
since Snatch only steals status moves. For Phase 5 to decide.

## The engine change, `40dc96cd2`, in detail

It is a feature, not a vanilla bug fix. Vanilla ties a trainer Pokemon's nature
to its IV scale through the seed. That is a design constraint rather than a
defect, and the change leaves it in place for every member that does not name a
nature.

A member with no nature gets exactly the old nature and personality. The new
helper and the removed inline code were compiled side by side on the host, the
helper lifted verbatim from `src/trainer_data.c`. Over 20,000 random inputs with
no nature named, plus 756 more in a mixed run, they agreed every time. Over
20,000 inputs they also agreed with the calculator's Python, every named nature
landed, and the low byte (gender and ability) never moved. Each run was done
twice with the same result. The nature steps change only the local `rnd`, not
the LCRNG state, so the draws `Pokemon_InitWith` makes afterwards (the not-shiny
OT id) are unchanged too.

The data format is backward compatible with all 928 trainer files. Every
`iv_scale` is between 0 and 255, so the new range check refuses none of them. No
file names a nature. The strongest evidence: `trpoke.narc` and `trdata.narc`
from the main checkout's build, made by a `trainerproc` without the nature code,
are byte-identical to the worktree's, made by the new one. The only other reader
of the party records, `BattleScript_CalcPrizeMoney`, reads the level alone.

The base ROM's trainer tables are still reproduced. `verify_narcs` compares no
trainer archive. The trainer check is the importer's dry run, which reads all 0
in the worktree. A member naming a nature is exempt there by the new
`_party_differs` and `_keep_oxide_tuning`, and not through an `AUTHORED` entry.
Exercised on a scratch copy of Roark's file: a re-tuned member's IV scale is
left alone, its level is still imported, and a party resize keeps its nature
and IV scale.

## Claims rerun

| Claim | Result |
|---|---|
| 63% of natures reachable at IV 28 or better over 1,758 members | 62.8% |
| 111 members have a nature no IV scale reaches | 111 |
| trdata and trpoke byte-identical with no nature named | yes, old and new `trainerproc` |
| ROM hash ab517390 | the worktree's ROM is `ab5173905caf`, built after the source edits |
| Importer dry run all 0 | all 0 |
| Encounter source check 184/184 | all 184 tables match |
| `verify_narcs` against the base ROM unchanged | 0 disagree in every archive |
| Nosepass Adamant packs as `0x04ff` | `0x04fa` at IV 250, so `0x04ff` at 255 |
| test_m8 82/82, test_m4 51/51, test_step0 35/35 | all pass |
| 130 stub effects, 136 moves | 130 and 136 on the branch |
| 190 natives differ from vanilla, 464 moves learnt | 190 and 464 |
| 1,758 sets for 747 trainers | 1,758 and 747, no set overwritten |
| Every ability and move lands on a calculator name; 26 aliases | 0 unknown; all 26 land |
| 550 skin rules, no colour literal left | 550; the generator reproduces the file |
| `calc_names.json` from `make_calc_names.js` | reproduced byte for byte |
| Five level 50 matchups | four reproduce; see finding 2 for the fifth |

The export agrees with `res/`. For all 652 species, the stats and types in the
blob match each `data.json`. For all 919 named moves, the type, category,
priority and power match their `data.json`, apart from the Z-move twins in
finding 5. The nature order matches `generated/natures.txt`. A sample of 40
trainers (79 members) matches its files on species, level, IVs and moves.

Every suite passes in the worktree: m1 13/13, m2 23/23, m3 18/18, m4 51/51,
m5 15/15, m6 19/19, m8 82/82, step0 35/35. `cli audit --fail-on-leak` exits 0.
The calculator's page loads no remote script or stylesheet. What remains remote
is links and the romhack picker's options, as `VENDORED.md` says.

## Not verified here

- Anything in the game. No trainer names a nature, and no emulator was run.
- "Two complete builds agree". Only one ROM exists to compare. GitHub's build
  at the merge gives the second.
- Agreement with upstream's vanilla trainer data (1,872 of 1,873 natures, and
  the 1,180 default movesets that differ). It needs upstream's hosted data,
  which is not in the repo. The three natures `test_m8` pins do pass.
- The calculator's on-page numbers. The five matchups were recomputed from the
  exported data with the Generation 4 formula, not read off the page.
- The headless Chrome claims: renders, Back and forward, no page errors, and no
  remote request while the page is used.
