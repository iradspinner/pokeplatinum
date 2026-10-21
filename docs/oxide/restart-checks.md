# Restart checks

How to confirm the tree's state after a restart, and what a clean result looks like now that Phase 4 has changed the base ROM's tables. Moved out of the tracker on 2026-10-02 verbatim, since it is reference, not open work; keep it current when an element changes a table the gate compares.

**To confirm the state after a restart**, from the repo root, `bash tools/oxide/integrate.sh --verify-only` runs all of this plus every tool suite. Without `--since` it runs every check, and a clean run on `oxide` passes all 54 with no warnings (the full run at 8d633c9d0 on 2026-10-21: the encounter lint on vanilla was cut on 2026-10-13, when the gate also stopped comparing the ROM with GitHub's build, and the line tester's test joined on 2026-10-21). Off `oxide` the docs mirror fails by design, since it refuses to mirror from any other branch. A landing through `merge-branch.sh` passes `--since origin/oxide` and runs only the checks the landing can reach, so its count is lower and its summary ends with "not needed: N checks this landing does not touch"; the always-run four are the build, the doc viewer's test, the scheduled items and the mirror. One by one:

```
make rom
python3 tools/oxide/import_base_rom.py --base ~/roms/base.nds --vanilla ~/roms/vanilla.nds --dry-run   # every count 0
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --ref ~/roms/base.nds
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --encounters --source   # M7: built NARC vs res/ JSON
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --ref ~/roms/base.nds --text
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --ref ~/roms/base.nds --map-headers
python3 tools/oxide/bulk_scripts.py --dry-run   # would write 0; 16 skipped, the deliberate divergences
python3 tools/oxide/bulk_events.py --dry-run    # would write 0
python3 tools/oxide/bulk_text.py --dry-run      # would write 0; 9 skipped
python3 tools/oxide/scriptdis.py --rom ~/roms/vanilla.nds --verify
python3 tools/oxide/scriptdis.py --rom ~/roms/base.nds --verify --base-rom
```

The importer is idempotent, so a non-zero count means something moved. The local checkout must be a full clone, since `scriptindex.py` reads the history (it was shallow at `main` until 2026-09-30, fixed with `git fetch --unshallow origin`); the depth-1 fetch of `main` is for cloud sessions only. Both `scriptdis` runs should report 574 files walked, 0 failed, 550 init scripts read and 0 movement-target collisions.

**What "clean" looks like now that Phase 4 has changed these tables.** `verify_narcs.py` carries a `DIVERGED` list for Phase 4 changes, and any element that changes a base-ROM table must add its members there or the gate fails. The three per-species archives no longer line up with the reference member for member, so the tool maps indices and reports each archive as a sentence that names every intended difference; read those sentences rather than a copy here. The counts at 8808d4b43 (2026-10-21), against `~/roms/base.nds`:

- `pl_personal.narc`: 669 members against the reference's 508; **0 disagree**, 500 differ only at the intended bytes (the hidden abilities, 451 of them, and the TM lists of 2026-10-06 among them), 161 are new species and their forms
- `wotbl.narc`: 669 against 508; 0 disagree, 161 new, 477 differ on purpose, since the learnset rewrite of 2026-10-06 authors every level-up list; compared as decoded `(level, move)` lists since element 4 widened the entry
- `evo.narc`: 669 against 508; 0 disagree, 161 new; 39 members differ on purpose and 469 only in trailing zero padding, the record having gone from 44 bytes to 56
- `pl_waza_tbl.narc`: 923 members against the reference's 471; **0 disagree**, 452 are new moves, 205 differ only at the intended bytes
- the base ROM importer reports every count 0, and its report (`tools/oxide/import_report.md`) names the evolutions it leaves as Phase 4 set them
- the visual overhaul's archives: `mmodel`, `trfgra`, `pl_batt_bg`, `titledemo`, `box`, `pl_plist_gra`, `pl_b_plist_gra`, `batt_obj`, `waza_particle` identical; `pl_otherpoke` 253 identical, 8 appended (Arceus's Fairy form and Meloetta's Pirouette); `pl_batt_obj` 293 identical, 48 by content and 2 by padding, plus the Fairy icon appended; `item_icon` 710 identical, 1 by content and 94 appended (element 7's items and the Ice Stone); `pl_pokegra` 592 identical, 2,372 by content, 960 appended; `height` 1,812 identical, 164 zero padding, 640 appended; `pl_poke_data` grown by the new species' records

Anything else is a regression. The encounter tool's own checks are in its build plan.
