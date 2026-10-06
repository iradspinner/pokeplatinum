# The learnset baseline: checks 1, 4, 5 and 6

This is step 1 of `docs/oxide/learnset-checks.md`, run on 2026-10-06 for the
Overseer to relay to Ian. It measures Oxide's level-up lists as they stand on
`oxide` (a17624478c) and learnset v3's (the proposal on
`origin/balance-learngen-v2`, b04408cfcb, unlanded) with the same code, so
every difference between the two columns is the lists' doing. Checks 2 and 3
are the scoring track's and have a placeholder below. Nothing here changes a
learnset or a move.

Learnset v3 is not better than Oxide's lists on these checks. On the
own-type rule it mends as many stages as it breaks. It leaves three catches
knowing no move at all, which Oxide's lists never do, and it leaves the early
fixed-damage moves exactly as they are, Charmander's Dragon Rage at 16
included, against Ian's ruling. Its one clear gain is on the TM list, and
that comes from the TM pass draft on the same branch, not from the learnsets.

| Check | Oxide | v3 |
|---|---|---|
| 1. Stages failing the own-type rule, of 448 judged | 51 | 51 |
| 1. Of those, no own-type attack of 50 by 78 at all | 19 | 11 |
| Species with a catch that knows no attack at capture (found on the way) | 10 | 18 |
| Of those, species with a catch that knows no move at all | 0 | 3 |
| 4. Fixed or level damage known or learnt by Gardenia's end | 5 | 5 |
| 4. One-hit KO moves on an obtainable species' lists | 28 | 28 |
| 5. Setup moves off 1 to 3 PP, of 47 | 0 | 0 |
| 5. Stat-lowering status moves off their PP rule, of 27 | 14 | 14 |
| 5. Weather moves and weather abilities on obtainable lines | 0 | 0 |
| 5. Sleep moves, powders, Thunder Wave, Dark Void, Swagger off Generation 4 accuracy, of 12 | 0 | 0 |
| 5. Ian's removed TMs on the TM list, of 14 | 14 | 0 |
| 6. Sheets, one per split | 12 | in the same sheets |

The tables behind each line are at the end, under "The tables".

## What the checks find

### Check 1: an attack of its own type within a split

About one stage in nine fails in either version. v3 mends six (Alolan
Ninetales, Delcatty, Espeon, Shiftry, Sylveon, Yanmega) and breaks six
(Beautifly, Grovyle, Sceptile, Hippowdon, Skiploom, Jumpluff). The six it
breaks are the stages v3's own report already put to Ian, where the moves
that would close the gap were held back by the power flags (Leaf Blade,
Earthquake, Air Slash, Bullet Seed), so the breakage is known rather than
new. v3 also gives eight stages that never had an own-type attack one, but
only Alolan Ninetales' (Icy Wind at 16) comes in time; the other seven come
two to seven splits late.

The failures fall into four kinds, and the kind matters more than the count
for step 2:

- An evolved stage reached by a stone used as soon as it is in reach, whose
  own list sits at level 1, the relearner's: Mismagius, Togekiss, Roserade
  and Clefable have every entry there and Starmie all but Confuse Ray, so
  after the stone they keep only what the pre-evolution had. Gligar and
  Gliscor are a near case: their lists reach no Ground or Flying attack of
  50 by 78 (v3 gives Gliscor Earthquake at 69).
- A stage that waits for one strong move far past the split it is first had
  in: Vaporeon (Hydro Pump at 71), Feraligatr (Aqua Tail at 58), Donphan
  (Earthquake at 46), Tangela and Tangrowth (Power Whip at 54).
- A type with few attacks of 50 early: the middle stages of the Fire
  starters (Charmeleon, Braixen, Raboot) have only Ember, at 40, until
  Fantina's split.
- Support and gimmick lines with no attack by design: Togetic, Happiny,
  Delibird, Duskull and Unown (Hidden Power only). Whether the rule should
  read these at all is a question for Ian, not a defect the check proves.

A TM or tutor on today's placements would close about half of the failures
in time (26 in Oxide, 27 in v3), but the TM pass will move every placement,
and TMs are single-use, so the table names the earliest one only as a lead.

Independently of these numbers, v3's own report counted 65 failing stages on
Oxide's lists by its level-based reading of the same rule. 46 of the 51 here
are on its list. The rest differ because this check reads the split a
Pokemon is caught in from the encounter tables rather than from its catch
level: five fail here that v3's list lacks (Brionne, Nidoqueen,
Polteageist, Roserade, Starmie); seventeen on its list pass here, because
a table first offers them in a later split than their catch level falls
in, and two (Kabuto and Kabutops) are not had before the League by the
current tables.

### Catches that know no attack at capture

This is not one of the six checks; it turned up while checking the capture
rule, and it is the most urgent finding here. v3's lists leave three
catches knowing no move at all: a Budew at 3 on Route 204, a Beautifly at
12 in Eterna Forest, and the Croagunk from Riley's egg on Iron Island at 1.
The dead-weight cut removed each one's only move at or below that level
(Absorb for Budew and Beautifly, Astonish for Croagunk) and nothing replaced
it. v3 also leaves fifteen species with a catch that knows status moves
only (Carvanha, Jumpluff, Masquerain and Snorlax among them, whose earlier
attacks are pushed out by four later status moves). Oxide's lists have no
catch with no move, but ten species with a catch that knows status moves
only. Four of those v3's first-move picks fix (Abra's Teleport, and the
Splash of Feebas, Azurill and Bounsweet); six are the same in both (Poliwag,
Togepi, Happiny, Smoochum, Ralts and Gorebyss).

### Check 4: early run-enders

The same five entries in both versions, and no TM or tutor adds one by
then. Charmander's Dragon Rage at 16 is still in Roark's split, which breaks
Ian's ruling in both. The other four are for Ian: Buizel's Sonic Boom,
known at capture from the Old Rod at Twinleaf Town at 3; Charmeleon's Dragon
Rage at 17; Machop's Seismic Toss at 19; Murkrow's Night Shade at 21. The
check stops at Gardenia's cap, as the plan sets it; Fantina's split adds
eleven more, mostly Ghost lines that know Night Shade at capture at 15, and
they are listed beside the table in case Ian sets the window wider.

One-hit KO moves sit on 28 obtainable species' level-up lists in both
versions, none on a TM or tutor list. Krabby's Guillotine at 31 is the
earliest; two are the relearner's only (Alolan Ninetales' Sheer Cold,
Rhydon's Horn Drill), and Trapinch's Fissure at 89 only reaches a Trapinch
kept from evolving into the post-game.

### Check 5: Ian's standing move rules

All 47 setup moves are at 1 to 3 PP, and all twelve sleep, powder and
status moves the ruling names keep vanilla Platinum's accuracy. No
obtainable line carries a weather move or a weather ability in a regular
slot, in either version. Fourteen stat-lowering status moves are off their
rule: the eleven the tracker's open PP item already names (Growl, String
Shot, Cotton Spore, Flash, SmokeScreen, Kinesis, Play Nice, Baby-Doll Eyes,
Scary Face, Confide, and Defog at 15 against its 1), and three it does not
name, Noble Roar, Tearful Look and Venom Drench. The move data is the same
in both versions.

Oxide's TM list still carries all fourteen of Ian's removed TMs, since the
TM pass has not landed. The TM pass draft on the v3 branch carries none of
them.

### Check 6: the sheets

`docs/oxide/learnset-sheets/` holds one sheet per split, Roark to League,
with a table per capture area: each Pokemon, how it is found, its level
range there, the four moves it knows at capture, every level-up move it
learns by the split's cap (each later stage's under its name), and the
stage it can be at the cap with the next one after. A row reads both
versions when they agree, and splits into an Oxide row and a v3 row when
they do not. This check is Ian's judgment; the sheets are where step 2's
lines can be read as a player would meet them.

## How the checks read the data

A Pokemon's moves follow the capture rule. A catch is one row of the
balance tools' catch census (`pool.catches`: every rolled wild slot, honey
tree, gift, trade, static and fossil, at the split the encounter design
gives it). It knows the last four moves its list gives by its catch level,
by the game's own rule (`calc_trainers.default_moves`); the test checks
that rule against every catch in both versions. After capture it learns its
entries above that level, and it evolves on time: a level evolution at its
level, in the first split whose cap allows it, and an item evolution as
soon as the item is in reach. An evolved stage keeps what it had, learns
its level-0 entries on evolving (v3 has them, Oxide none yet), and then its
own entries from the evolution level on. Its level 1, and every entry below
the level it is had at, is the relearner's and counts for nothing. Egg
lists are never read.

Check 1 judges each stage from the split it is first had in on its line's
earliest route, taking the best of several routes in that split. An attack
counts when it is of one of the stage's types, 50 or more by effective
power, and does not knock the user out. Effective power is v3's own reading
of Ian's rule: the listed power after recoil, a recharge or charging turn
and a self-drop, a multi-hit move at its average total, accuracy left out.
A stage passes when that attack comes in the split it is first had in or the
next, and is exempt when it can evolve by the end of Gardenia's split.
Check 4 counts a move a stage knows at capture or learns by level-up while
the player can have it by Gardenia's end, and counts a move an evolved
stage carries on its pre-evolution only. Check 5 reads setup and
stat-lowering moves by their effects, so a new move with the same effect is
caught; the moves that raise or lower a stat beside something else
(Parting Shot, Strength Sap, Coaching and the like) are listed but not
judged. The splits' caps are fights.json's, with Maylene's at 39, which Ian
confirmed on 2026-09-22.

## Checks 2 and 3: placeholder for the scoring track's results

**Not yet in.** When this was written, `~/oxide-trials/learnset-baseline/`
held only the scoring track's reading of v3 (`build_v3.py` and
`v3_learnsets.json`), no results. This report reads v3 the same way, and its
test checks that the two readings agree for all 653 species. When the
results land, they go here, side by side like the rest, with three rules
from Ian (2026-10-06) on how check 2 is read:

- The matchup screen counts hits, so it cannot see a plan that wins on turns
  (it ranked the Mars 1 PP-stall six 1,831st of 38,760, and only the later
  race recovered it). Check 2's list of lines no boss takes is a list of
  leads, not verdicts.
- Walls, stallers and support lines on that list (Togetic, a Vullaby stall
  and the like) are marked as likely misreads, to be checked with the race
  or a reading.
- A flagged support line is never to be fixed just by giving it more
  attacks.

The same caution applies to check 1's support lines above: Togetic, Happiny
and Delibird fail a rule written about attacks, which says nothing yet about
whether they do their job.

## The 20 lines for Ian's insight sessions

Twenty lines across the splits they are first caught in and across roles,
nine that fail clearly, five borderline or changed by v3, and six that pass,
nine of them Ian's super-wanted lines. The five marked held out were drawn
with `random.Random(20261006)` from the list in this order
(`learncheck.py lines` repeats the draw); they are the exam of step 5 and
are not to be shown to the generator. Roles are rough, read from base stats
and what the line is for.

| # | Line | First caught | Role | Check 1, Oxide and v3 | Held out | Why it is here |
|---|---|---|---|---|---|---|
| 1 | Charmander | Roark | fast special attacker | Charmeleon fails in both | | Ian ruled its Dragon Rage out of Roark's split and both versions still teach it at 16, while Charmeleon goes two splits on Ember, at 40, before Fire Fang at 28. |
| 2 | Budew (super-wanted) | Roark | special attacker | every stage fails in both | | Budew never learns an attack of 50, Roselia waits for Petal Dance at 40, Roserade learns nothing after a Shiny Stone in Oxide, and v3 leaves a Budew caught at 3 with no move at all. |
| 3 | Scorbunny (super-wanted starter) | Roark | fast physical attacker | Raboot fails in both | **held out** | Raboot waits two splits for Blaze Kick at 28, the shortest wait that fails the rule. |
| 4 | Onix | Roark | physical wall | Steelix fails in both | | Steelix, had from a Metal Coat in Gardenia's split, waits three splits for Iron Tail at 41, which asks whether a wall needs an attack by this rule at all. |
| 5 | Shinx | Roark | physical attacker | passes in both | | A plain early line that passes every check in both versions, to show Ian what passing looks like to a player. |
| 6 | Togepi (super-wanted) | Gardenia | support | Togetic and Togekiss fail in both | | Togetic never gets a Fairy or Flying attack of 50 by level-up and Togekiss learns nothing after its Shiny Stone (v3 adds Moonblast at 75), the clearest case of the rule reading a support line. |
| 7 | Treecko | Gardenia | fast mixed attacker | passes in Oxide, Grovyle and Sceptile fail in v3 | **held out** | v3 moves Grovyle's Leaf Blade from 29 to 52, so a line that passes on Oxide's lists waits four and six splits for a Grass attack. |
| 8 | Snorunt (super-wanted) | Gardenia | fast special attacker | passes in both | | Every stage passes, Froslass by a Dawn Stone included, a control among the wanted lines. |
| 9 | Popplio (super-wanted) | Gardenia | special attacker | Brionne fails in both | | Brionne waits two splits for Scald at 34 on Oxide's lists and five in v3, which moves Scald to 65, so a wanted line gets worse. |
| 10 | Eevee (super-wanted) | Fantina | eight branches | Vaporeon and Glaceon fail in both, Espeon and Sylveon in Oxide only | **held out** | One gift that reads every way: Vaporeon waits seven splits for Hydro Pump at 71, Glaceon two, and v3 mends Espeon and Sylveon. |
| 11 | Gible | Fantina | fast physical attacker | passes in both | | A strong line that passes, and knows Dragon Rage at capture at 18, just outside check 4's window. |
| 12 | Swablu (super-wanted) | Fantina | mixed, bulky | Swablu fails in both | | The unevolved Swablu never gets a Fairy or Flying attack of 50 in Oxide and gets Air Slash only at 44 in v3, while Altaria passes. |
| 13 | Totodile | Fantina | physical attacker | Croconaw and Feraligatr fail in both | | Croconaw and Feraligatr wait three and five splits for Aqua Tail, at 48 and 58, in both versions. |
| 14 | Misdreavus | Fantina | fast special attacker | Mismagius fails in both | | Mismagius, evolved by Dusk Stone as soon as one is in reach, learns nothing by level-up in Oxide and Shadow Ball only at 56 in v3, which asks how the check should treat a player who waits to use a stone. |
| 15 | Trapinch | Maylene | fast mixed attacker | Vibrava fails in both | | Vibrava never gets a Bug or Flying attack of 50 in either version, between a Trapinch and a Flygon that both pass. |
| 16 | Koffing (super-wanted) | Maylene | mixed, bulky | passes in both | **held out** | Passes in both, with Galarian Weezing by a Moon Stone as its other branch. |
| 17 | Tangela | Maylene | bulky mixed attacker | Tangela and Tangrowth fail in both | | Both stages wait three splits for Power Whip at 54, with Vine Whip at 45 the best Grass attack before it. |
| 18 | Skorupi (super-wanted) | Wake | physical attacker | passes in both | **held out** | A mid-game line that passes in both versions. |
| 19 | Beldum | Byron | physical attacker | passes in both | | A late pseudo-legendary that passes, the only line here first caught in Byron's split. |
| 20 | Delibird | Candice | gimmick | Delibird fails in both | | It knows only Present in Oxide and gets Freeze-Dry at 63 in v3, a late catch whose role may make the failure the wrong question. |

One caveat on the seal. The module's test ran the draw once on a
placeholder list before the twenty were chosen, so the five positions this
seed picks (the 3rd, 7th, 10th, 16th and 18th) could have been seen then.
The list's order follows the splits and was not arranged around them, but
if Ian wants a seal beyond question, the Overseer can redraw with a seed
Ian picks.

## What this could not settle

- When to use a stone. Check 1 evolves by stone as soon as the stone is in
  reach. A player who waits keeps the pre-evolution's later moves, so for
  Mismagius, Starmie, Togekiss, Roserade and the like the check reads the
  worst timing, not the usual one.
- Which level a catch is read at. The sheets read each Pokemon at the lowest
  level it is found at in an area; a higher one in the same area may know
  different moves.
- Effective power against listed power. Check 1 uses v3's effective power
  for the 50 bar; on listed power a few two-turn and recoil moves would
  count and a few multi-hit moves would not.
- Traded Pokemon. The sources file gives a trade the traded Pokemon's own
  level, which the census reads as 1, so Popplio's line is read from level 1.
- The cap of Maylene's split is 39 in fights.json (Ian, 2026-09-22), not
  the 38 in the job's brief; every reading here uses 39.
- v3's TM column is the TM pass draft on the v3 branch, which the learnset
  proposal does not itself change. The learnset species' TM lists are the
  tree's in both columns.
- Unown knows only Hidden Power, whose type the check cannot read, so it
  fails as having no attack.
- `test_learncheck.py` reads `origin/balance-learngen-v2`, so it needs that
  branch fetched, and it is not in the gate's list of balance tests.

## The tables

Printed by `PYTHONPATH=. python3 -m tools.oxide.balance.learncheck report`
on the tree above and v3 at b04408cfcb.

### Check 1 counts

| | Oxide | v3 |
|---|---|---|
| Stages the player can have by the League | 448 | 448 |
| Pass: an own-type attack within a split | 315 | 315 |
| Fail: two splits or more without one | 51 | 51 |
| of which none by the League's cap | 19 | 11 |
| Exempt: can evolve by the end of Gardenia's split | 82 | 82 |
| Lines | 199 | 199 |
| Lines with a failing stage | 40 | 39 |
| Failing stages a TM or tutor would close in time | 26 | 27 |

### Check 1 by the split the stage is first had in

| Split | Oxide pass | Oxide fail | v3 pass | v3 fail |
|---|---|---|---|---|
| Roark | 37 | 9 | 36 | 10 |
| Gardenia | 54 | 15 | 55 | 14 |
| Fantina | 66 | 14 | 66 | 14 |
| Maylene | 73 | 7 | 72 | 8 |
| Wake | 42 | 4 | 42 | 4 |
| Byron | 31 | 1 | 32 | 0 |
| Candice | 6 | 1 | 6 | 1 |
| HQ | 1 | 0 | 1 | 0 |
| Galactic | 2 | 0 | 2 | 0 |
| Volkner | 3 | 0 | 3 | 0 |
| Barry | 0 | 0 | 0 | 0 |
| League | 0 | 0 | 0 | 0 |

### Check 1: every stage that fails in either version, worst first

| Stage | First had | Route (Oxide's) | Oxide: first own-type attack | Gap | v3: first own-type attack | Gap | Earliest TM or tutor |
|---|---|---|---|---|---|---|---|
| Budew | Roark | wild, Route 204, 3 | none by 78 | never | none by 78 | never | TM09 Bullet Seed (Gardenia) |
| Gligar | Roark | wild, Oreburgh Gate, 8 | none by 78 | never | none by 78 | never | TM26 Earthquake (Fantina) |
| Alolan Ninetales | Gardenia | wild, Route 211, 13 | none by 78 | never | Icy Wind at 16 (Gardenia) | 0, passes | none |
| Clefable | Gardenia | from Clefairy (wild, Mt. Coronet North, 14), at 14 by Moon Stone | none by 78 | never | none by 78 | never | none |
| Feebas | Gardenia | old_rod, Oreburgh Gate, 6 | none by 78 | never | none by 78 | never | tutor Dive (Wake) |
| Floatzel | Gardenia | from Buizel (wild, Route 205, 15), at 26 | none by 78 | never | none by 78 | never | TM55 Brine (Wake) |
| Granbull | Gardenia | from Snubbull (wild, Route 204, 10), at 23 | none by 78 | never | none by 78 | never | none |
| Togetic | Gardenia | from Togepi (egg gift, Eterna City, 1), at 10 | none by 78 | never | none by 78 | never | TM40 Aerial Ace (Wake) |
| Duskull | Fantina | wild, Old Chateau, 15 | none by 78 | never | none by 78 | never | tutor Ominous Wind (Wake) |
| Happiny | Fantina | wild, Route 208, 20 | none by 78 | never | none by 78 | never | TM43 Secret Power (Fantina) |
| Mismagius | Fantina | from Misdreavus (wild, Old Chateau, 15), at 15 by Dusk Stone | none by 78 | never | Shadow Ball at 56 (Candice) | 4 | tutor Ominous Wind (Wake) |
| Swablu | Fantina | wild, Amity Square, 9 | none by 78 | never | Air Slash at 44 (Wake) | 2 | TM88 Pluck (Gardenia) |
| Starmie | Maylene | from Staryu (good_rod, Route 219, 15), at 15 by Water Stone | none by 78 | never | Hydro Pump at 60 (HQ) | 4 | TM29 Psychic (Maylene) |
| Unown | Maylene | unown room, Solaceon Ruins, 20 | none by 78 | never | none by 78 | never | none |
| Vibrava | Maylene | from Trapinch (wild, Solaceon Town, 20), at 35 | none by 78 | never | none by 78 | never | TM89 U-turn (Maylene) |
| Gliscor | Wake | from Gligar (wild, Great Marsh, 28), at 28 by Razor Fang | none by 78 | never | Earthquake at 69 (Barry) | 6 | TM26 Earthquake (Fantina) |
| Roserade | Wake | from Budew (wild, Great Marsh, 29), at 30 by Shiny Stone | none by 78 | never | Sludge Bomb at 60 (HQ) | 3 | TM09 Bullet Seed (Gardenia) |
| Togekiss | Wake | from Togepi (egg gift, Eterna City, 1), at 39 by Shiny Stone | none by 78 | never | Moonblast at 75 (League) | 7 | TM88 Pluck (Gardenia) |
| Delibird | Candice | wild, Acuity Lakefront, 33 | none by 78 | never | Freeze-Dry at 63 (Galactic) | 2 | TM88 Pluck (Gardenia) |
| Vaporeon | Maylene | from Eevee (gift, Hearthome City, 20), at 33 by Water Stone | Hydro Pump at 71 (Barry) | 7 | Hydro Pump at 71 (Barry) | 7 | TM55 Brine (Wake) |
| Polteageist | Fantina | from Sinistea (wild, Old Chateau, 15), at 15 by Dusk Stone | Shadow Ball at 48 (Byron) | 3 | Shadow Ball at 65 (Galactic) | 6 | none |
| Sceptile | Maylene | from Treecko (wild, Route 204, 9), at 36 | Leaf Blade carried (Maylene) | 0, passes | Leaf Storm at 67 (Volkner) | 6 | TM02 Dragon Claw (Gardenia) |
| Feraligatr | Fantina | from Totodile (old_rod, Route 208, 9), at 30 | Aqua Tail at 58 (HQ) | 5 | Aqua Tail at 58 (HQ) | 5 | tutor Dive (Wake) |
| Brionne | Gardenia | from Popplio (in-game trade, Eterna City, 1), at 16 | Scald at 34 (Maylene) | 2 | Flip Turn at 55 (Candice) | 5 | none |
| Donphan | Gardenia | from Phanpy (wild, Mt. Coronet North, 16), at 25 | Earthquake at 46 (Byron) | 4 | Earthquake at 46 (Byron) | 4 | TM26 Earthquake (Fantina) |
| Shiftry | Gardenia | from Seedot (wild, Eterna Forest, 11), at 14 by Leaf Stone | Leaf Storm at 49 (Byron) | 4 | Faint Attack at 31 (Fantina) | 1, passes | TM09 Bullet Seed (Gardenia) |
| Nidoqueen | Gardenia | from Nidoran♀ (wild, Route 201, 4), at 16 by Moon Stone | Earth Power at 43 (Wake) | 3 | Earthquake at 53 (Byron) | 4 | TM26 Earthquake (Fantina) |
| Grovyle | Gardenia | from Treecko (wild, Route 204, 9), at 16 | Leaf Blade at 29 (Fantina) | 1, passes | Leaf Blade at 52 (Byron) | 4 | TM09 Bullet Seed (Gardenia) |
| Dustox | Roark | from Wurmple (wild, Route 204, 4), at 10 | Silver Wind at 34 (Maylene) | 3 | Silver Wind at 34 (Maylene) | 3 | TM89 U-turn (Maylene) |
| Masquerain | Gardenia | from Surskit (wild, Lake Verity, 2), at 22 | Silver Wind at 40 (Wake) | 3 | Silver Wind at 40 (Wake) | 3 | TM89 U-turn (Maylene) |
| Nidoking | Gardenia | from Nidoran♂ (wild, Oreburgh Gate, 7), at 16 by Moon Stone | Earth Power at 43 (Wake) | 3 | Poison Jab at 43 (Wake) | 3 | TM26 Earthquake (Fantina) |
| Steelix | Gardenia | from Onix (wild, Oreburgh Gate, 9), at 9 by Metal Coat | Iron Tail at 41 (Wake) | 3 | Iron Tail at 41 (Wake) | 3 | TM26 Earthquake (Fantina) |
| Carnivine | Fantina | wild, Route 208, 20 | Power Whip at 47 (Byron) | 3 | Power Whip at 47 (Byron) | 3 | TM09 Bullet Seed (Gardenia) |
| Croconaw | Fantina | from Totodile (old_rod, Route 208, 9), at 18 | Aqua Tail at 48 (Byron) | 3 | Aqua Tail at 48 (Byron) | 3 | tutor Dive (Wake) |
| Tangela | Maylene | wild, Route 209, 19 | Power Whip at 54 (Candice) | 3 | Power Whip at 54 (Candice) | 3 | TM09 Bullet Seed (Gardenia) |
| Tangrowth | Maylene | from Tangela (wild, Route 209, 19), at 35 | Power Whip at 54 (Candice) | 3 | Power Whip at 54 (Candice) | 3 | TM09 Bullet Seed (Gardenia) |
| Espeon | Byron | from Eevee (gift, Hearthome City, 20), at 44 by Sun Stone | Psychic at 64 (Galactic) | 3 | Psychic at 53 (Byron) | 0, passes | TM29 Psychic (Maylene) |
| Skiploom | Gardenia | from Hoppip (wild, Floaroma Town, 12), at 18 | Bullet Seed at 20 (Gardenia) | 0, passes | Giga Drain at 44 (Wake) | 3 | TM09 Bullet Seed (Gardenia) |
| Braixen | Roark | from Fennekin (wild, Route 207, 8), at 16 | Flame Burst at 29 (Fantina) | 2 | Flame Burst at 29 (Fantina) | 2 | none |
| Charmeleon | Roark | from Charmander (wild, Route 207, 8), at 16 | Fire Fang at 28 (Fantina) | 2 | Fire Fang at 28 (Fantina) | 2 | TM35 Flamethrower (Maylene) |
| Luvdisc | Roark | old_rod, Route 219, 4 | Water Pulse at 31 (Fantina) | 2 | Water Pulse at 31 (Fantina) | 2 | TM55 Brine (Wake) |
| Magby | Roark | wild, Oreburgh Mine, 8 | Fire Punch at 28 (Fantina) | 2 | Fire Punch at 28 (Fantina) | 2 | TM35 Flamethrower (Maylene) |
| Raboot | Roark | from Scorbunny (starter, Route 201, 5), at 16 | Blaze Kick at 28 (Fantina) | 2 | Blaze Kick at 28 (Fantina) | 2 | none |
| Wartortle | Roark | from Squirtle (old_rod, Route 218, 5), at 16 | Water Pulse at 28 (Fantina) | 2 | Water Pulse at 28 (Fantina) | 2 | TM55 Brine (Wake) |
| Delcatty | Gardenia | from Skitty (wild, Route 205, 10), at 10 by Moon Stone | Hyper Voice at 35 (Maylene) | 2 | Covet on evolving (Gardenia) | 0, passes | TM43 Secret Power (Fantina) |
| Lopunny | Gardenia | from Buneary (wild, Eterna Forest, 10), at 20 | Dizzy Punch at 36 (Maylene) | 2 | Dizzy Punch at 36 (Maylene) | 2 | HM01 Cut (Gardenia) |
| Alomomola | Fantina | from Luvdisc (old_rod, Route 219, 4), at 30 | Brine at 41 (Wake) | 2 | Brine at 41 (Wake) | 2 | none |
| Charcadet | Fantina | wild, Route 206, 17 | Incinerate at 40 (Wake) | 2 | Incinerate at 40 (Wake) | 2 | none |
| Glaceon | Fantina | from Eevee (gift, Hearthome City, 20), at 30 | Ice Fang at 43 (Wake) | 2 | Ice Fang at 43 (Wake) | 2 | TM13 Ice Beam (Maylene) |
| Lileep | Fantina | fossil, Mining Museum, 20 | AncientPower at 43 (Wake) | 2 | AncientPower at 43 (Wake) | 2 | TM09 Bullet Seed (Gardenia) |
| Roselia | Fantina | from Budew (wild, Eterna Forest, 11), at 30 | Petal Dance at 40 (Wake) | 2 | Petal Dance at 40 (Wake) | 2 | TM09 Bullet Seed (Gardenia) |
| Sylveon | Fantina | from Eevee (gift, Hearthome City, 20), at 32 | Moonblast at 43 (Wake) | 2 | Dazzling Gleam at 32 (Fantina) | 0, passes | none |
| Yanmega | Maylene | from Yanma (wild, Route 215, 22), at 35 | U-turn at 49 (Byron) | 2 | Wing Attack at 42 (Wake) | 1, passes | TM89 U-turn (Maylene) |
| Cradily | Wake | from Lileep (fossil, Mining Museum, 20), at 40 | Energy Ball at 56 (Candice) | 2 | Energy Ball at 56 (Candice) | 2 | TM09 Bullet Seed (Gardenia) |
| Beautifly | Roark | from Wurmple (wild, Route 204, 4), at 10 | Air Slash at 26 (Gardenia) | 1, passes | Air Slash at 29 (Fantina) | 2 | TM89 U-turn (Maylene) |
| Hippowdon | Maylene | from Hippopotas (wild, Wayward Cave, 19), at 34 | Earthquake at 40 (Wake) | 1, passes | Earthquake at 53 (Byron) | 2 | TM26 Earthquake (Fantina) |
| Jumpluff | Fantina | from Hoppip (wild, Floaroma Town, 12), at 27 | Bullet Seed carried (Fantina) | 0, passes | Giga Drain at 44 (Wake) | 2 | TM09 Bullet Seed (Gardenia) |

v3 mends 6: Alolan Ninetales, Delcatty, Espeon, Shiftry, Sylveon, Yanmega.

v3 breaks 6: Beautifly, Grovyle, Hippowdon, Jumpluff, Sceptile, Skiploom.

### Catches that know no attack at capture

Oxide: 10 species, 0 of them with no move at all; v3: 18, 3 with no move at all.

| Pokemon | Oxide | v3 |
|---|---|---|
| Abra | Jubilife City, 4 (Roark): Teleport | has an attack |
| Bounsweet | Route 204, 4 (Roark): Splash | has an attack |
| Budew | has an attack | Route 204, 3 (Roark): no move |
| Kricketot | has an attack | Route 201, 3 (Roark): Growl |
| Lotad | has an attack | Lake Verity, 3 (Roark): Growl |
| Poliwag | Route 203, 4 (Roark): Water Sport | Route 203, 4 (Roark): Water Sport |
| Seedot | has an attack | Route 204, 4 (Roark): Harden |
| Beautifly | has an attack | Eterna Forest, 12 (Gardenia): no move |
| Chingling | has an attack | Floaroma Town, 13 (Gardenia): Growl |
| Feebas | Oreburgh Gate, 6 (Gardenia): Splash | has an attack |
| Togepi | Eterna City, 1 (Gardenia): Growl, Charm | Eterna City, 1 (Gardenia): Growl, Charm |
| Azurill | Amity Square, 9 (Fantina): Splash, Charm, Tail Whip | has an attack |
| Happiny | Route 208, 20 (Fantina): Charm, Copycat, Refresh, Sweet Kiss | Route 208, 20 (Fantina): Charm, Copycat, Refresh, Sweet Kiss |
| Joltik | has an attack | Honey trees, 14 (Fantina): String Shot, Thunder Wave, Spider Web |
| Carvanha | has an attack | Great Marsh, 22 (Wake): Focus Energy, Scary Face, Screech, Swagger |
| Jumpluff | has an attack | Great Marsh, 27 (Wake): PoisonPowder, Stun Spore, Sleep Powder, Leech Seed |
| Smoochum | Route 214, 28 (Wake): Sing, Mean Look, Fake Tears, Lucky Chant | Route 214, 28 (Wake): Sing, Mean Look, Fake Tears, Lucky Chant |
| Croagunk | has an attack | Iron Island, 1 (Byron): no move |
| Masquerain | has an attack | Fuego Ironworks, 33 (Byron): Sweet Scent, Water Sport, Scary Face, Stun Spore |
| Ralts | Iron Island, 1 (Byron): Growl | Iron Island, 1 (Byron): Growl |
| Gorebyss | Route 218, 36 (Candice): Amnesia, Aqua Ring, Captivate, Baton Pass | Route 218, 36 (Candice): Amnesia, Aqua Ring, Captivate, Baton Pass |
| Snorlax | has an attack | Honey trees, 32 (Candice): Belly Drum, Yawn, Rest, Sleep Talk |

### Check 4: fixed and level damage by the end of Gardenia's split

Oxide: 5 entries on 5 species; v3: 5 entries on 5 species.

| Pokemon | Move | Oxide | v3 | Ruling |
|---|---|---|---|---|
| Buizel | SonicBoom | known at capture at 3 (Roark) | known at capture at 3 (Roark) | for Ian |
| Charmander | Dragon Rage | level-up at 16 (Roark) | level-up at 16 (Roark) | Oxide broken, v3 broken |
| Charmeleon | Dragon Rage | level-up at 17 (Gardenia) | level-up at 17 (Gardenia) | for Ian |
| Machop | Seismic Toss | level-up at 19 (Gardenia) | level-up at 19 (Gardenia) | for Ian |
| Murkrow | Night Shade | level-up at 21 (Gardenia) | level-up at 21 (Gardenia) | for Ian |

By TM, HM or tutor in reach by then (both versions): 0.

For context, not part of the check: those first known or learnt in Fantina's split (Oxide 11, v3 11): Duskull Night Shade known at capture at 15; Gastly Night Shade known at capture at 15; Litwick Night Shade known at capture at 15; Misdreavus Psywave known at capture at 15; Yamask Night Shade known at capture at 16; Gible Dragon Rage known at capture at 18; Ceruledge Night Shade level-up at 20; Salandit Dragon Rage level-up at 21; Charcadet Night Shade level-up at 30; Chimecho Psywave level-up at 30; Makuhita Seismic Toss level-up at 31.

### Check 4: one-hit KO moves on a player list

| Pokemon | Move | Oxide | v3 |
|---|---|---|---|
| Abomasnow | Sheer Cold | level-up at 58 (HQ) | level-up at 58 (HQ) |
| Alolan Ninetales | Sheer Cold | the relearner's only | the relearner's only |
| Articuno | Sheer Cold | level-up at 78 (League) | level-up at 78 (League) |
| Barboach | Fissure | level-up at 47 (Byron) | level-up at 47 (Byron) |
| Corphish | Guillotine | level-up at 53 (Byron) | level-up at 53 (Byron) |
| Crawdaunt | Guillotine | level-up at 65 (Galactic) | level-up at 65 (Galactic) |
| Dewgong | Sheer Cold | level-up at 34 (Maylene) | level-up at 34 (Maylene) |
| Glalie | Sheer Cold | level-up at 59 (HQ) | level-up at 59 (HQ) |
| Gligar | Guillotine | level-up at 45 (Byron) | level-up at 45 (Byron) |
| Gliscor | Guillotine | level-up at 45 (Byron) | level-up at 45 (Byron) |
| Goldeen | Horn Drill | level-up at 41 (Wake) | level-up at 41 (Wake) |
| Hippopotas | Fissure | level-up at 50 (Byron) | level-up at 50 (Byron) |
| Hippowdon | Fissure | level-up at 60 (HQ) | level-up at 60 (HQ) |
| Kingler | Guillotine | level-up at 37 (Maylene) | level-up at 37 (Maylene) |
| Krabby | Guillotine | level-up at 31 (Fantina) | level-up at 31 (Fantina) |
| Lapras | Sheer Cold | level-up at 55 (Candice) | level-up at 55 (Candice) |
| Nidoran♂ | Horn Drill | level-up at 45 (Byron) | level-up at 45 (Byron) |
| Nidorino | Horn Drill | level-up at 58 (HQ) | level-up at 58 (HQ) |
| Rhydon | Horn Drill | the relearner's only | the relearner's only |
| Rhyhorn | Horn Drill | level-up at 37 (Maylene) | level-up at 37 (Maylene) |
| Rhyperior | Horn Drill | level-up at 52 (Galactic) | level-up at 52 (Galactic) |
| Seaking | Horn Drill | level-up at 47 (Byron) | level-up at 47 (Byron) |
| Sealeo | Sheer Cold | level-up at 55 (Candice) | level-up at 55 (Candice) |
| Snover | Sheer Cold | level-up at 46 (Byron) | level-up at 46 (Byron) |
| Spheal | Sheer Cold | level-up at 49 (Byron) | level-up at 49 (Byron) |
| Trapinch | Fissure | level-up at 89 (Post) | level-up at 89 (Post) |
| Walrein | Sheer Cold | level-up at 65 (Galactic) | level-up at 65 (Galactic) |
| Whiscash | Fissure | level-up at 57 (HQ) | level-up at 57 (HQ) |

### Check 5: PP

Setup moves: 47 read, 47 at 1 to 3 PP. Stat-lowering status moves: 27 read, 13 within their rule. The move data is the same in both versions.

| Move | Kind | PP | Rule |
|---|---|---|---|
| Baby-Doll Eyes | stat-lowering | 10 | 3 to 6 |
| Confide | stat-lowering | 10 | 3 to 6 |
| Cotton Spore | stat-lowering | 40 | 3 to 6 |
| Defog | stat-lowering | 15 | exactly 1 |
| Flash | stat-lowering | 20 | 3 to 6 |
| Growl | stat-lowering | 40 | 3 to 6 |
| Kinesis | stat-lowering | 15 | 3 to 6 |
| Noble Roar | stat-lowering | 10 | 3 to 6 |
| Play Nice | stat-lowering | 10 | 3 to 6 |
| Scary Face | stat-lowering | 10 | 3 to 6 |
| SmokeScreen | stat-lowering | 20 | 3 to 6 |
| String Shot | stat-lowering | 40 | 3 to 6 |
| Tearful Look | stat-lowering | 10 | 3 to 6 |
| Venom Drench | stat-lowering | 20 | 3 to 6 |

Read but not judged (they raise or lower a stat beside something else): Aromatic Mist 20, Coaching 10, Decorate 15, Dragon Cheer 15, Flatter 15, Flower Shield 10, Gear Up 20, Laser Focus 30, Magnetic Flux 20, Octolock 15, Parting Shot 20, Psych Up 10, Rototiller 10, Spicy Extract 15, Strength Sap 10, Swagger 15, Tar Shot 15, Toxic Thread 20.

### Check 5: weather, accuracy and the TM list

| Rule | Oxide | v3 |
|---|---|---|
| Weather moves on an obtainable line's lists | 0 | 0 |
| Weather abilities in an obtainable line's regular slots | 0 | 0 |
| Sleep moves, powders, Thunder Wave, Dark Void, Swagger off Generation 4 accuracy | 0 of 12 | 0 of 12 |
| Ian's removed TMs still on the TM list | 14 of 14 | 0 of 14 |

Oxide's TM list carries: TM01 Focus Punch, TM07 Hail, TM11 Sunny Day, TM17 Protect, TM18 Rain Dance, TM32 Double Team, TM37 Sandstorm, TM46 Thief, TM48 Skill Swap, TM49 Snatch, TM63 Embargo, TM75 Swords Dance, TM85 Dream Eater, TM90 Substitute.

v3's TM pass draft (103 in its set) carries: none of them.
