# Restart checks

How to confirm the tree's state after a restart, and what a clean result looks like now that Phase 4 has changed the base ROM's tables. Moved out of the tracker on 2026-10-02 verbatim, since it is reference, not open work; keep it current when an element changes a table the gate compares.

**To confirm the state after a restart**, from the repo root, `bash tools/oxide/integrate.sh --verify-only` runs all of this plus the encounter suites, and checks the ROM's hash against GitHub's build of `HEAD`. One by one:

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

**What "clean" looks like now that Phase 4 has changed these tables.** `verify_narcs.py` carries a `DIVERGED` list for Phase 4 changes, and any element that changes a base-ROM table must add its members there or the gate fails. The three per-species archives no longer line up with the reference member for member, so the tool maps indices and reports each archive as a sentence. Expect exactly this:

- `pl_personal.narc`: 669 members against the reference's 508; **0 disagree**, 42 differ only at the intended bytes (the twenty Fairy retypes, the seventeen pick-list retypes of 2026-09-29, the base ROM's stat slips in Metapod, Kakuna and Shedinja corrected the same day, and Wormadam's Sandy and Trash forms back to Anticipation), 161 are new species and their forms (element 3's 159, Meloetta and its Pirouette form record)
- `wotbl.narc`: 669 against 508; 0 disagree, 161 new, 3 differ on purpose (Sneasel, Houndour and Houndoom lose Beat Up), compared as decoded `(level, move)` lists since element 4 widened the entry
- `evo.narc`: 669 against 508; 0 disagree, 161 new; 34 members differ on purpose (seven natives that gain an evolution, twelve whose friendship evolution became a level, a place or a stone, and sixteen that lost their trade entries in element 8, Scyther being in two lists) and 474 differ only in trailing zero padding, the record having gone from 44 bytes to 56
- `pl_waza_tbl.narc`: 923 members against the reference's 471; **0 disagree**, 452 are new moves, 146 differ only at the intended bytes (the three Fairy retypes, the 95 natives given the King's Rock flag, Poison Gas's range, the 66 natives given modern numbers, 45 of which are in none of the other groups, and Barrier and Tailwind at 1 PP); 178 once `cloud/element4-kaizo-move-data` merges. Both are worked out from the lists, not yet seen against the base ROM
- the base ROM importer reports every count 0 and lists those same 22 species' evolutions as not carried over
- once `carry-over` lands, the visual overhaul's archives: `mmodel`, `trfgra`, `pl_batt_bg`, `titledemo`, `box`, `pl_plist_gra`, `pl_b_plist_gra`, `batt_obj`, `waza_particle` identical; `pl_otherpoke` 253 identical, 4 appended (Pirouette's sprites and palettes); `pl_batt_obj` 293 identical and 50 by content or padding, plus the Fairy icon appended; `item_icon` 710 identical and 1 by content; `pl_pokegra` 592 identical, 2,372 by content, 960 appended; `height` 1,812 identical, 164 zero padding, 640 appended; `pl_poke_data` grown by the new species' records

Anything else is a regression. The encounter tool's own checks are in its build plan.
