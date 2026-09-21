---
name: oxide-spreadsheets
description: Where Platinum Oxide's design spreadsheets live on the G: drive, what each sheet holds, and how to read or regenerate from them with the xlsx skill (openpyxl and pandas are installed in WSL2). Use this whenever a session needs New Pokedex.xlsx, the species pick-list's source, Ian's own encounter or boss or level-cap docs, the Hardlove location documentation, base stats or type charts from a sheet, or is asked to update a CSV under docs/oxide that came from a spreadsheet, even if the user just says "the sheet" or "my docs".
---

# Oxide's spreadsheets

Ian designs in spreadsheets on the G: drive and the repo carries generated
CSV snapshots of some of them. When a task starts from a spreadsheet, invoke
the `xlsx` skill (Anthropic's, synced into this account and available in every
session) for the mechanics; this skill says where the files are and what is in
them, which the xlsx skill cannot know.

## Environment

`openpyxl` 3.1 and `pandas` 3.0 are installed for the WSL2 user (installed
2026-09-20 with `pip3 install --user --break-system-packages`). Reading a sheet
needs nothing else. Writing a sheet with formulas needs the xlsx skill's
`recalc.py`, which needs LibreOffice, and LibreOffice is **not** installed;
`sudo apt install libreoffice-calc` is Ian's to run. Until then, produce values
rather than formulas when writing, or hand the file back for Ian to open once.

Read with `data_only=True` so cached values come back instead of formula
strings. The G: drive is at `/mnt/g/`; treat every file there as Ian's
original and write outputs into the repo or next to the source with a new
name, never over it.

## The files

Hub folder: `/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/`

| File | Sheets | What it is for |
|---|---|---|
| `New Pokedex.xlsx` | `New Pokedex` (1,004 species rows: Number, Name, HP, ATK, DEF, SPA, SpDef, SPE, types and more), `Type Stats` (type chart), `Every Mon (Temp)` | **The source of the species pick-list.** `docs/oxide/species-pick-list.csv` and `.md` were generated from it on the chat surface; the generating scripts (`build_pick_list.py`, `find_form_slots.py`, `compare_sheet_vs_base.py`) live in the hub folder's `tools\`, not the repo. The 21-row stat conflict with the base ROM is tabled for a whole-dex balance pass |
| `My Version RomHack Docs - For Claude.xlsx` | `General Encounters` (Ian's own encounter tables by area), `Pokemon Changes` (stat edits), `Boss Documentation`, `Battles To Update`, `Level Caps`, `Every Mon (Temp)` | Ian's design record for the base ROM. `Level Caps` and `Boss Documentation` are the inputs to the Phase 5 level-cap split design; `General Encounters` is what the base ROM's tables were meant to be, useful when an authored table needs to know what a route was for |
| `Platinum Kaizo Docs.xlsx` | `Personal`, `Ability Changes`, `Evolutions`, `Level-Up Learnsets`, `Moves`, `Move Changes` | Reference docs from another Platinum hack; background only, not a source for Oxide values |
| `Hardlove Gold/Hardlove Gold Documentation - Pokemon Locations.xlsx` | `Encounter Tables`, `Game Corner`, `Trades`, `Safari Zone`, `Random Pools`, `Unavailable Pokémon` | The donor's published location docs. The encounter design survey found the donor's tables flat; this is what they look like from the player's side, and `Unavailable Pokémon` is the donor's own availability list |
| `Hardlove Gold/Original Pokemon Locations.xlsx` | same sheets | The same documentation for vanilla HeartGold, for comparison |

The encounter-table sheets are laid out as blocks per area across columns with
merged headers, not one row per encounter; read them as grids and locate area
names in the first rows before trusting a column.

## Regenerating a repo CSV from a sheet

1. Read the sheet with the xlsx skill's approach; keep the row order the sheet
   has, since `dex_pos` order in the pick-list is Ian's designed dex order and
   now also fixes the internal species ids (`docs/oxide/species-id-scheme.md`).
2. Write the CSV with the same columns the existing file has; diff against the
   committed copy and explain every changed row in the commit message. A
   silent regeneration is how a stale sheet row (Swinub's, once) gets into the
   game.
3. Bring the generating script into `tools/oxide/` if it is not there, so the
   next regeneration does not depend on the chat surface.
