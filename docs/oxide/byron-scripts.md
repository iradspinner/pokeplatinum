# Byron's split: the scripts, gates and tools

Ian set Byron's split on 2026-10-31 (`byron-split-map.md`, the tracker's Scheduled entry). This page covers the script, gate and tool parts of that plan, built on the branch `overseer-byron-scripts`; another helper rebuilt the split's ordinary teams beside it. Nothing here has been seen in game.

## Summary

Outcome. All six parts are in. Pal Park's lobby now holds a partner double: once Oak's first-entry scene is over, Lucas or Dawn walks in, two Galactic officers follow, and the player and the counterpart fight them in a tag battle. Barry on Canalave's bridge fights only once that double is won, and before it he sends the player to Pal Park, so the gym and the ferry to Iron Island wait for it too. Cyrus 1's honour cap is 47 and Barry 5's 50. Eterna's Oak gives the Upgrade and frees the Kanto birds only after the Hall of Fame. Lake Valor's table counts in Volkner's split. Lake Verity's grunts 3 and 4 count as mandatory. The gate passes 53 checks; its one failure is sync-docs, which refuses off `oxide` by design. A goal 3 check run outside the gate fails the same way on `oxide` (below).

What waits on Ian:

1. Which two officers fight at Pal Park. They are placeholders named "Officer" in free trainer slots 9 and 50, a grunt of each sex, four Pokemon each at 46 to 48 with their level-up moves and no items. Name them and give their sixes, and the scene's "Officer:" labels follow.
2. Cyrus 1's and Barry 5's teams still have their aces at 53. The level check lets that stand until their redesign and names them; their teams are for the boss stages.
3. Somnu and Moira, now mandatory, are a named Galactic boss double, so they count for the field model but not among Candice's 10 to 15 ordinary fights.

Ian's answers (2026-10-31). Lucas and Dawn keep one shared text at Pal Park. The partner's Scyther evolves into Scizor, at 48 in all six partner slots, and holds a Muscle Band in place of the Eviolite: no other member of the team holds one, and it lifts every one of Scizor's four physical moves, where a Metal Coat would lift none, since the set has no Steel move. The rest of the six stay as built. One thing carried over from Veilstone: Brick Break is on neither Scyther's nor Scizor's lists at 48 (Scizor learns it at 55), so the Veilstone partner already holds it off-list; Wing Attack and Pursuit come from Scyther's level-up list and Knock Off from the tutor. The officers stay placeholders while Ian chooses them.

Next steps. Ian's in-game checks of the three new pieces (below), about 30 minutes from a save after Celestic. Ian's picks for the officers, then their teams in a later pass.

## What changed

| Part | Files | What |
|---|---|---|
| The Pal Park double | `scripts_pal_park_lobby.s`, `scripts_init_pal_park_lobby.s`, `events_pal_park_lobby.json`, `pal_park_lobby.json`, `dummy_009`, `_050`, `_051`, `_052`, `_054`, `_062`, `_063`, `_064` | The scene and tag battle; the two officers and six partner teams in free slots, registered in `trainers_diverged.json` with name, class and messages; `fights.json`'s `pal_park_double`, a story tag fight; Pal Park placed in Byron's split |
| Barry 5 waits | `scripts_canalave_city.s`, `canalave_city.json` | Before the double, Barry says "Have you been to Pal Park yet?", the player steps back off the bridge's trigger, and Barry walks away |
| The stretch caps | `fights.json`, `test_b1.py`, `test_savefile.py` | `honour_cap` 47 for Cyrus 1 (won when `VAR_CELESTIC_TOWN_STATE` reaches 1) and 50 for Barry 5 (won when `VAR_CANALAVE_CITY_STATE` reaches 1), which the OxiDex reads |
| Oak waits | `scripts_eterna_city_south_house.s`, `eterna_city_south_house.json`, `gates.py` | Oak checks `FLAG_GAME_COMPLETED` first and asks the player back; the census's gate reader now reads a flag test's fall-through right, so the Upgrade counts as post-game |
| Lake Valor | `progression.py`, `design.json`, `availability.md`, `splits.py` | The full lake's table is Volkner's; the drained lake keeps Byron's split, which it took from the full lake's name |
| Lake Verity | `required.py`, `test_b1e.py` | A short honour list makes grunts 3 and 4 required; the totals move from 68 to 70 required, Candice's split from 7 to 9 |

The win of the double sets both officers' trainer flags, and Barry checks the first. The scene's three objects are hidden by `FLAG_UNUSED_0x054F`, a flag no script used, kept under its pret name so the reward placer counts it as taken. Nothing in the save moves (`save-layout.md`). Each map's divergence from the base ROM is registered in `bulk_scripts.py`, `bulk_events.py` and `import_base_rom.py`.

The field model's check of the order, in `test_b1e`: the south's three routes from Sandgem to Pal Park's door open with Surf and not before; with Barry's trigger shut, Route 218's gate reaches neither the harbor's sailor nor the gym's door, and with it open both. Iron Island is still read room by room from the boat, since the ferry is a script.

The census reader's fix changes one gift only, Oak's Upgrade, which moved from Byron to post-game. Before it, a flag test's fall-through needed nothing, so a gift behind `GoToIfUnset` counted from the split the jump allowed.

## The in-game checks

The three new checks are in `ingame-checklist.md`, section 4, after Iron Island's.

1. The Pal Park double: Oak's scene, then the counterpart and the officers, the tag battle with the right partner and ace, the scene ending, and no replay on re-entry; once from a save that saw Oak before this ROM.
2. Barry on the bridge before and after the double, on each of the bridge's four rows.
3. Eterna's Oak before and after the Hall of Fame, with no birds roaming before it.

## What could not be checked

Nothing was played. The scene's walking was read off the lobby's collision map, not watched. The goal 3 check that the box sizes hold over 20 seeds fails on this branch and on `oxide` alike (Maylene's 41 and Wake's 51 against 40 and 50 pinned), so it is not this branch's.
