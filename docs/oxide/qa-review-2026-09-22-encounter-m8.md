# QA: the encounter branch before it merges (M8, the dex and the visual design)

A `/qa-pass` on 2026-09-22 over `worktree-encounter-step0` against its merge base
with `oxide`, `500df0ce9`, run by the Overseer with the encounter agent stopped.
Nothing here was fixed: every defect is in the encounter track's files, so each
is left to that track, and one question is Ian's.

## What was reviewed

22 commits: M8's scope, the vendored calculator, the dex (D1 to D3 and three
fixes), the six visual design steps and two fixes, Ravaged Path's move to
Roark's split, and three rounds of table-view changes from Ian's notes.

| Part | Size | How it was checked |
|---|---|---|
| Vendored: the Dynamic Calc calculator (`calc/`), 190 files | 344,344 lines | provenance, licence, and what it loads |
| Vendored: `canon_src/data/species.js` from @smogon/calc 0.12.0 | 10,961 lines | provenance, licence, and the comparison built on it |
| Authored: the dex, server routes, UI, tests and docs, 27 files | about 3,200 lines | read, with the claims rerun |

The branch is 218 files and about 358,000 changed lines, almost all vendored,
so the cloud review's limits (500 files, 8,000 lines) rule out the whole range.
The last 12 commits alone (`3d7ed04ed..`, 21 files, about 1,800 lines) would
fit, if Ian wants that part reviewed in the cloud as well.

## Findings

### 1. Nidoran♂ is treated as a mega, so it drops out of its own line

`pokedex._mega_of` calls any species whose constant ends in `_M` a mega of the
species without the suffix. Three constants end that way: `SPECIES_GYARADOS_M`,
`SPECIES_LOPUNNY_M` and `SPECIES_NIDORAN_M`. So Nidoran♂ reads as a mega of a
`SPECIES_NIDORAN` that does not exist, and `server.dex_detail` removes it from
the line as a forme. Checked through the function the page calls:

```
SPECIES_NIDORINO   line: NIDOKING, NIDORINO
SPECIES_NIDORAN_M  line: NIDOKING, NIDORINO    mega_of: SPECIES_NIDORAN
SPECIES_NIDORINA   line: NIDOQUEEN, NIDORAN_F, NIDORINA
```

The fix is to name the two megas rather than infer them from a suffix, or to
require that the base species exist. For the encounter track.

### 2. Evolution lines are drawn in alphabetical order, with stage arrows between them

`dex_detail` builds the line from `dex.members_of_line`, which returns the
members sorted by constant, and the page joins them with the stage chevron. So
Litten's line reads Incineroar › Litten › Torracat and Gyarados' reads
Gyarados › Magikarp. It happens to be right for Bulbasaur. The line needs
ordering by stage (walk the evolutions from the member nothing evolves into),
with branches such as Eevee's shown as siblings. For the encounter track.

### 3. The vendored calculator is not offline as it stands

M8 vendored the calculator so the tool would work offline, but its page loads
jQuery and other libraries from Google's, jsDelivr's and unpkg's CDNs, a Google
Tag Manager analytics tag, and its game data from `hzla.github.io` (about 100
references). None of it runs today, because the server only serves `ui/` and
`calc/` sits outside it. The step that wires the calculator in (D5) plans one
patch, pointing the data loader at this server. It needs the rest in its patch
list too: vendor or drop the CDN scripts, remove the analytics tag, and remove
every remote data URL. For the encounter track, before D5.

### 4. Nit: the dex caches what the server says it never caches

`pokedex.load`, `moves` and `species_list` are `lru_cache`d for the life of the
server, while the server marks every response `no-store` on the stated grounds
that a stale page is indistinguishable from a missing feature. An edit to a
species or move file while the server runs does not show until a restart. The
tool does not edit those files itself, so this only bites someone editing them
by hand. Either say so in the header or key the cache on the files' mtimes.

### 5. Nit: `/api` alone answers 500

`do_GET` reads `parts[1]` before checking there is one, so a bare `/api` raises
`IndexError` and returns a 500 with that message rather than the 404 every other
unknown path gets.

## A question for Ian, from the main track's data

**The type chart keeps Generation 4's Steel.** M8's type-chart reader found it
and `src/battle/battle_lib.c` confirms it: Fairy's twelve matchups are in and
correct, and Steel still resists Ghost and Dark, which Generation 6 removed when
it added Fairy. Element 1 ported Fairy onto the Generation 4 chart. Keeping
Steel's two resistances is defensible for balance, but it was never decided. The
dex and a future damage calculator will show whatever the chart says either way.

## Checked and correct

- **The three type differences from canon are deliberate.** Galarian Rapidash
  Fairy/Fire, Gothitelle Psychic/Dark and Tsareena Grass/Fighting all match
  `docs/oxide/species-pick-list.csv`, which came from Ian's sheet. The commit
  that found them left open whether they were slips; they are not.
- **Clefairy's missing Cute Charm is the base ROM's.** It has Magic Guard in
  both slots, carried over in Phase 3 (`c69ef83a6`). It is one of the 228
  duplicated second slots the ability balance pass will look at.
- **The canon comparison reproduces:** 181 species differ in stats, the same 3
  in type, and every one of the 652 lands on a canonical entry (test_m8).
- **Every suite passes on the branch:** test_m1 13/13, m2 23/23, m3 18/18, m4
  50/50, m5 15/15, m6 19/19, m8 43/43, step0 35/35, step1 21/21, step2 18/18,
  step3 28/28, step5 16/16. `cli audit --fail-on-leak` exits 0, and lint has no
  errors with R12 ignored. R12 itself stands at 27; the tracker's encounter
  paragraph says 22.
- **The two table edits** (Ravaged Path's Wooper to Lotad, and Oreburgh Mine
  B2F's unused swarm field) change only the lines they mean to, in the files'
  own style, and the sidecar agrees with them.
- **The server** binds 127.0.0.1 only. The new sprite route refuses a folder
  containing `/` or `..`, and nothing under `calc/` is served.
- **Provenance and licences:** the calculator is MIT with its licence and
  `VENDORED.md` (upstream commit, what was pruned, how to update); the canon
  table is @smogon/calc 0.12.0, MIT, with a README; Pixelify Sans is OFL with
  its licence and source. hzla/ddex, which has no licence, contributed no code.
- **The type chart reader** matches the battle table, Steel included.

## Not verified here

- The rebuild with all 184 tables matching their JSON. `integrate.sh` builds and
  checks this at the merge, and GitHub's build gives the hash.
- The visual claims: the headless Chrome renders, the contrast figures in the
  design's section 10, and the animation timings. None of them affects the ROM.
