# Candice's split: the map before any change

The Overseer asked on 2026-10-31 for Candice's split to be mapped as Byron's was, so that its pass can be planned with Ian. The split runs from Byron's badge (cap 53) to Candice's (cap 56), only three levels. This page was read on the branch `overseer-candice-map` from `origin/oxide` at 76cdd8cb7c8. No game data changed.

It takes as given what the brief set. Iron Island comes before Byron's gym, so it is in Byron's split. Surf waits on Cyrus 1, Route 214's gate on Maylene's badge, and Strength on the badge alone, so Strength arrives with this split. Named Galactic officers stay outside gauntlets. Lake Verity's grunts 3 and 4, who are Officers Somnu and Moira, count as mandatory by Ian's honour rule. Spring Path, Sendoff Spring and Turnback Cave open only after the Distortion World.

## Summary

What was mapped. Every area the player can reach between the two badges was walked with the story-route study's whole-world tile model, in four stages: the end of Byron's split, Byron's badge with Strength, the library scene, and Mars 2 beaten. Each area's trainers, current top levels, items and wild tables were read from the tree; the mandatory verdicts came from `required.py` with its honour list, the doubles from `pairs.py`. A search over every tile and facing on each crossing found where a fixed trainer would be unavoidable. The experience the split's fights give was summed with Generation 4's formula.

What could not be checked. Nothing was seen in game. Snowpoint's gym has moving parts and is not modelled. The spots for moved trainers are the model's readings, not tested placements. The experience sums assume the whole party shares every fight evenly, with no Exp. Share and no Lucky Egg.

What was found. The split runs one way, with no sequence break. The library scene opens Lake Valor; Saturn's defeat in Valor Cavern turns Verity Lakefront's door to the Galactic version of Lake Verity; Mars's defeat there clears the two grunts in Mt. Coronet's north room, which opens the way to Route 216, Route 217, Snowpoint and the gym. Strength opens nothing with trainers. Lake Acuity, Jupiter's scene and four of Route 216's trainers wait on Rock Climb, so on the Icicle Badge, which puts them in HQ's split, though the OxiDex tags the table and the trainers here. There is no rival fight: Barry and Lucas or Dawn appear at the library, Lake Verity and Acuity Lakefront without battling. Every team in the split but Officer Somnu's still breaks the held-item and nature rule of 2026-10-12.

The levels fit. The mandatory lake fights give about one level for a party of six, and everything to the gym gives about two more, so three levels hold the split's fights with experience to spare. The narrow part is the band: ordinary trainers must sit under the cap and very rarely one under it, which leaves 52 to 55 for the whole split.

| Stretch | Areas, in play order | Closed by | Ordinary band | Experience on offer |
|---|---|---|---|---|
| 1 | the library scene, Lake Valor, Valor Cavern, Lake Verity | Mars 2, honour cap 54 (recommended) | 52 to 53 | 55,000 mandatory, about one level for six |
| 2 | Mt. Coronet B1F, Routes 216 and 217, Acuity Lakefront, Snowpoint, the gym | Candice (56) | 53 to 54, rarely 55 | 40,000 mandatory, 60,000 optional, 79,000 in the gym, against 109,000 for two levels |

Mandatory fights, counted as Ian counts them: every mandatory fight that is not a boss, mini-bosses included, a double against two trainers as one.

| | Count |
|---|---:|
| Today | 6 |
| Fixing Black Belt Luke in place | 7 |
| Adding moves of existing trainers to the necks the search found | 10 to 14 |
| Adding new trainers as well (Lake Verity's mouth, Mt. Coronet B1F, Acuity Lakefront) | up to 19 |

Today's six are Officer Hesperid, the Lake Verity grunt pair, the Somnu and Moira double, and Ace Trainers Laura, Dalton and Olivia. Five of the six are mini-bosses, so the moves below favour ordinary trainers.

Ian's decisions:

1. An honour cap inside the split: none, one stretch to 56; Mars 2 closing the lakes at 54 (recommended); Mars 2 at 55; or the lakes held at Byron's 53?
2. A level shift for more room: keep 53, 56 and 60 (recommended, since the experience covers the three levels with room to spare), or raise Candice's cap to 58 and leave HQ's short split two levels?
3. The commanders' aces: Saturn 1 at 53 and Mars 2 at 54, its own honour cap (recommended); both at 53, as ruled on 2026-10-07; or both at 54?
4. The officers' levels: Hesperid's ace from 56 to 53, no higher than Saturn's, with his difficulty in his sets (recommended), or kept at 56 as the officer excepted; and Somnu and Moira from 54 to 52?
5. Which count candidates (section 3)? Recommended: Luke fixed, Lake Valor's Grunt 1 moved, Skier Edward moved, two of Route 217's middle trainers moved, and Lake Verity's talking grunt made a trainer at the lake's mouth, for 12.
6. Route 216's four Rock Climb trainers (Skiers Bradley, Kaitlyn and Andrea, Black Belt Philip): left for HQ's split and levelled for 60 (recommended), or one or two moved down onto this split's path?
7. A gauntlet section: none (recommended); Mt. Coronet B1F with three new trainers and a refused warp back; or Route 217 with a line at its south end?
8. May the OxiDex move Lake Acuity's table from Candice's split to HQ's, where Rock Climb opens it?
9. Saturn 1 and Mars 2 each field the lake guardian they have just taken (Azelf, Mesprit), which the player cannot catch for now: keep them in the redesigns (recommended), or drop them?

Next steps:

| Step | Who | Time |
|---|---|---|
| Answer the questions above | Ian | 20 to 30 minutes |
| The fixes, moves and new trainers for the count, each checked with `required.py`, and Mars 2's honour cap in `fights.json` and the OxiDex | a worker | 2 to 3 hours |
| The level climb and rebuild of the split's ordinary teams in play order (12 in reach today, 4 more above Route 216's walls) | a worker | half a day |
| The bosses and mini-bosses in checked stages, to Ian's themes: Hesperid 1, Somnu and Moira 2, Saturn 1, Mars 2, Candice, then the six route Aces | the Overseer and a worker | 1 to 2 hours each, plus Ian's look |
| The in-game check of the moved trainers, the honour cap and the gym's cap message | Ian | 30 minutes with the test kit |

## 1. The areas, and what opens each

The split opens in three steps, each a story flag. Byron's badge brings Strength, and the library door, which Barry held until Riley's tag battle, leads to the scene on 3F: Rowan sends the player to Lake Valor, the lake explodes, and the cameramen on Valor Lakefront are hidden (`FLAG_HIDE_VALOR_LAKEFRONT_CAMERAMEN`). Saturn's defeat in Valor Cavern sets `FLAG_DEFEATED_COMMANDER_SATURN_VALOR_CAVERN`, which makes Verity Lakefront's door lead to the Galactic version of Lake Verity instead of the quiet one. Mars's defeat there sets `FLAG_HIDE_MT_CORONET_1F_NORTH_ROOM_1_GRUNTS_M`, which clears the two grunts standing at the stairs down to B1F, and `FLAG_TEAM_GALACTIC_LEFT_LAKE_VERITY`.

### Strength, before the library

| Area | What Strength opens | Trainers | Items |
|---|---|---|---|
| Mt. Coronet 1F North Room 1 | the boulder rooms, joining Route 211 West to Route 211 East, so Eterna to Celestic on foot | none | Rare Candy, TM69, TM02 |
| Oreburgh Gate B1F | one corner | none (Veteran Grant, 47, was Byron's) | TM01, Earth Plate |
| Routes 214, 215, Lake Verity | two tiles each behind a boulder | none | none |

Route 211 East's four trainers (44 and 45) and Veteran Grant were reachable in Byron's split already. Mt. Coronet North Room 1's table is the Mt. Coronet North capture area, first met in Gardenia's split.

### The lakes (the library scene to Mars 2)

| Area | Opens with | Trainers today (top levels) | Mandatory today | Capture area |
|---|---|---|---|---|
| Canalave Library 3F | Byron's badge, with Riley's battle done | none; the scene with Rowan, Barry and Lucas or Dawn | none | none |
| Lake Valor, drained | the library scene | Grunt 1 (Muk 50), Grunt 3 (Arbok 50, Metronome reward), Officer Hesperid (six, 54 to 56) | Hesperid | none: the drained lake has no table |
| Valor Cavern | the drained lake | Commander Saturn (six, 51 to 53) | Saturn 1, a boss | none |
| Lake Verity, Galactic | Saturn beaten | Grunts 1 and 2 (Nidoking 50, Houndoom 50), Officers Somnu and Moira (three each, 53 and 54), Commander Mars (six, 51 to 53) | the grunt pair, a double; Somnu and Moira, a double, on honour; Mars 2, a boss | Lake Verity, Roark's |

Lake Valor's way from the lakefront to the cavern has three necks of one or two tiles. Hesperid stands at (28,33) looking east over one of them, which the base ROM arranged by moving him and lengthening his sight. Grunt 1 looks north into open ground, and Grunt 3 turns and holds a reward, so both are avoidable. Three more grunts on the drained lake only talk.

At Lake Verity the two pairs face each other across the lake's south shore: Grunts 1 and 2 along row 49, six tiles between them, and Somnu and Moira along row 44, beside the base ROM's two boulders. Mars's win removes all four, so a player could surf past Somnu and Moira and still finish the lake; Ian's honour rule counts them. A fifth grunt, who only talks, stands just inside the entrance. Lucas or Dawn has already lost to Mars when the player arrives and does not battle.

The lakes' items are few: a TM25 ball on the drained lake that the model cannot reach (the refilled lake holds the same ball under the same flag), and Lake Verity's TM38, reachable by Surf since Byron's split. Lake Valor's full table belongs to Volkner's split (Ian's answer for Byron's split).

### The north (Mars 2 to Candice)

| Area | Opens with | Trainers today (top levels) | Mandatory today | Capture area |
|---|---|---|---|---|
| Mt. Coronet B1F and North Room 2 | Mars beaten | none | none | Mt. Coronet B1F, new: land 32 to 35, Surf to 48 on B1F |
| Route 216 | through North Room 2 | Ace Trainers Laura (six, 54 to 55), Blake (six, 52 to 55, Ring Target reward), Garrett and Maria (six each, 54 to 55); Skier Edward (Abomasnow 50) | Laura | Route 216, new: land 32 to 35 |
| Route 216, above the Rock Climb walls | the Icicle Badge, so HQ's split | Skiers Bradley (three, 54), Kaitlyn (two, 54), Andrea (Froslass 55), Black Belt Philip (Machamp 56) | none | Route 216 |
| Route 217 | from Route 216's west end | Ace Trainers Dalton (six, 54 to 55) and Olivia (six, 52 to 55); Black Belt Luke (three, 51); Skiers Shawn, Bjorn, Madison (one each, 51) and Lexie (two, 51, Ability Shield reward); Ninja Boys Matthew and Ethan (one each, 51) | Dalton, Olivia; Luke reads required but walks | Route 217, new: land 32 to 35 |
| Acuity Lakefront | Route 217 | none; Barry says Lake Acuity needs the Icicle Badge | none | Acuity Lakefront, new: land 32 to 35 |
| Snowpoint City | Acuity Lakefront | none; the base ROM's maid, who trains a party to 56, and its fisherman, who gives the Super Rod | none | Snowpoint City, new: the Good and Super Rods only |
| Snowpoint Gym | the city | Ace Trainers Anton, Savannah, Alicia, Isaiah, Brenna and Sergio (six each, 54 to 55); Candice (54 to 56) | gym trainers only; Candice, a boss | none |
| Lake Acuity | Rock Climb, so HQ's split | none; Jupiter's scene with Barry, no battle | none | Lake Acuity, tagged Candice's |

The north's items: Mt. Coronet B1F holds a Revive, Soft Sand, Light Clay, Max Elixir, Full Restore and Ultra Ball; Route 216 a Full Heal and a Revive (its TM13, Mental Herb, HP Up and Max Potion wait on Rock Climb); Route 217 HM08, Iron, TM07, a Blue Shard, an Ultra Ball and a Rare Candy; Acuity Lakefront and Snowpoint an Ultra Ball each (the lakefront's Reaper Cloth waits on Rock Climb). The Iceberg Ruins' door in North Room 2 leads to its side room and a NeverMeltIce, since Regice waits for Volkner's split (`story-route.md`). Candice gives a Lum Berry in TM72's place. The Super Rod reaches every earlier water from Snowpoint on, at the very end of the split.

The new wild tables stand at 32 to 35 on land and up to 48 on B1F's water, against the 56 cap. The new capture areas in the split are Mt. Coronet B1F, Routes 216 and 217, Acuity Lakefront and Snowpoint City's rods.

## 2. The play order and its stretches

The order is fixed by the story. Nothing in the split can be reached ahead of its flag: Lake Valor waits on the library, Lake Verity's Galactic event on Saturn, and the whole north on Mars. So earliest-access levelling, which levels each area for the stretch it first opens in, comes to the same thing as the walk here: the climb follows Lake Valor, Valor Cavern, Lake Verity, Mt. Coronet, Route 216, Route 217, Acuity Lakefront, Snowpoint and the gym, in that order. The exceptions are the ones that open later, not earlier: Route 216's four Rock Climb trainers and Lake Acuity's table first open in HQ's split, so by the same rule they are levelled for HQ (question 6) and the table belongs there (question 8). Strength opens nothing with a trainer.

### The room in three levels

Experience is not the constraint. The sums below use Generation 4's formula (base experience times level over seven, half again for a trainer's Pokemon), shared by the whole party.

| Fights | Experience | Running total |
|---|---:|---:|
| The lakes' mandatory fights: Hesperid, Saturn 1, the grunt pair, Somnu and Moira, Mars 2 | 55,101 | 55,101 |
| Lake Valor's two optional grunts | 3,256 | 58,357 |
| Laura, Dalton and Olivia | 39,946 | 98,303 |
| Routes 216 and 217, the optional trainers in reach | 59,468 | 157,771 |
| Snowpoint Gym's six | 78,556 | 236,327 |
| Candice | 14,275 | 250,602 |

What six Pokemon need, on the medium-fast curve (medium-slow is within 3 percent; slow needs a quarter more):

| Climb | Experience for six |
|---|---:|
| 53 to 54 | 51,522 |
| 54 to 56 | 108,912 |
| 53 to 56 | 160,434 |

So the lakes' mandatory fights give one level for six almost exactly, and a full clear to the gym's door gives about the three levels; the gym and Candice give nearly two levels more, which the soft cap boxes. The Snowpoint maid also trains a party up to 56, so no player arrives at Candice short.

The constraint is the band. Ordinary trainers climb under the cap, never at it and very rarely one under. Byron's last stretch puts them at 50 to 52, so Candice's split has 52 to 55 for all of its ordinary fights, with 55 rare. That is enough, because the split has few ordinary fights on its path: the two grunt pairs and Lake Valor's optional grunts at the lakes, and about eight skiers, Ninja Boys and Black Belts in the north. The mini-bosses sit 2 to 4 under their cap and the leader at it.

### Where an honour cap fits

The one natural place is Mars 2. His win ends the lakes, clears the north room's grunts and is the last story fight before the walk to Snowpoint. Saturn 1 sits in the middle of the lakes, one fight before the Lake Verity pairs, and a cap there would leave a stretch of one level on each side. The OxiDex can read Mars's win from `FLAG_TEAM_GALACTIC_LEFT_LAKE_VERITY`, as it reads Barry 5's from Canalave's state.

| Choice | Stretch 1 (the lakes) | Stretch 2 (the north) | What it costs |
|---|---|---|---|
| No inner cap | to 56, ordinary 52 to 53 | to 56, ordinary 53 to 54 | a player may grind to 56 before the lakes, against aces of 53 |
| Mars 2 at 54 (recommended) | ordinary 52 to 53, officers 50 to 52, Saturn 1 53, Mars 2 54 | ordinary 53 to 54, Aces 52 to 54, Candice 56 | none beyond the cap's entry; the lakes' experience fills it |
| Mars 2 at 55 | ordinary 52 to 54 | 55 to 56: the north's ordinary trainers at or over the lakes' cap | stretch 2 has one level |
| The lakes held at 53 | ordinary 51 to 52, officers 49 to 51, both commanders 53 | the full three levels | the lake fights are fought at Byron's level and the officers drop three to five levels |
| Candice's cap to 58 | Mars 2 at 55 | to 58 | HQ's split, cap 60, keeps two levels; the maids, the gym's message and `fights.json` move with it |

The officers' levels follow from the choice. Today Hesperid's ace is 56, three over Saturn's, and Somnu's and Moira's are 54, one over Mars's. Ian allowed Hesperid to read harder than his commander, and the recommendation keeps that in his sets rather than his levels (question 4).

## 3. The mandatory count

Ian's rules apply: every mandatory fight that is not a boss counts, mini-bosses included; a trainer who turns, spins or walks is optional; a pair is one fight; gym trainers do not count. A trainer with a reward stays optional, as Byron's map left them (Lake Valor's Grunt 3, Ace Trainer Blake, Skier Lexie).

| Fight | Map | Kind | Today | What would make it count | Stretch |
|---|---|---|---|---|---|
| Officer Hesperid | Lake Valor | mini-boss | mandatory | | 1 |
| Grunts 1 and 2, a double | Lake Verity | ordinary | mandatory | | 1 |
| Officers Somnu and Moira, a double | Lake Verity | mini-boss | mandatory on honour | | 1 |
| Ace Trainer Laura | Route 216 | mini-boss | mandatory | | 2 |
| Ace Trainer Dalton | Route 217 | mini-boss | mandatory | | 2 |
| Ace Trainer Olivia | Route 217 | mini-boss | mandatory | | 2 |
| Black Belt Luke | Route 217 | ordinary | walks | fixed in place facing north, at the route's north neck: the model reads him required | 2 |
| Grunt 1 | Lake Valor | ordinary | avoidable | moved to (21,23), facing the one-tile neck beside it at (22,23) | 1 |
| Skier Edward, or Ace Trainer Garrett or Maria | Route 216 | ordinary, or mini-boss | avoidable even seeing every way | moved to the neck at the cave mouth, (374,403), or the one by Snowbound Lodge, (304,385); Laura holds the middle | 2 |
| One or two of Skiers Shawn, Bjorn and Madison and Ninja Boys Matthew and Ethan | Route 217 | ordinary | avoidable even seeing every way | moved to the south neck beside Maylene's scene, (304,371), or the north one beside Luke, (289,272); the route's middle is open snow, wider everywhere than a trainer's sight can close | 2 |
| One or two of the four Rock Climb trainers | Route 216 | ordinary | not reached until HQ's split | moved down to the neck by Snowbound Lodge, if Ian does not leave them for HQ (question 6) | 2 |
| The talking grunt, made a trainer | Lake Verity | ordinary | not a trainer | a free trainer slot, moved from (47,51) to (46,53), facing east across the lake's two-tile mouth; where he stands now the shore is six tiles wide | 1 |
| New trainers at Mt. Coronet B1F | B1F | ordinary | none there | free slots, at either stairs: both ends of the floor are necks | 2 |
| A new trainer at Acuity Lakefront | Acuity Lakefront | ordinary | none there | a free slot at the neck by Barry's scene, (310,243) | 2 |

That gives 6 today, 7 with Luke, 10 to 14 with the moves, and up to 19 with new trainers. The recommendation, question 5, comes to 12: Luke fixed; Lake Valor's Grunt 1, Edward and two of Route 217's middle five moved; Lake Verity's talking grunt made a trainer. It leaves the Aces where they are, so that more of the count is ordinary fights. Moving trainers next to Dalton or Olivia needs care, since a shared sight line makes a double, and two Aces with six each would field twelve.

The split holds no gauntlet section today. The lakes cannot hold one, since their mandatory fights are officers and commanders, which stay outside. Route 217 leads to Snowpoint and its gym, but its mandatory fights are two Aces with six Pokemon each, not the easier side of average, and the overworld has no warp to refuse, so it would need a line at its south end like Victory Road's. Mt. Coronet B1F is the natural shape: one floor between two stairs, nine hundred tiles of cave, its way back a refused warp like the Galactic HQ sections'. It has no trainers, so a section there means three new teams (question 7).

## 4. The fights by kind

| Fight | Kind | Where | Today | Settled |
|---|---|---|---|---|
| Saturn 1 | boss (commander) | Valor Cavern | Azelf 51, Mr. Mime, Wobbuffet, Lickilicky, Rhyperior 52, Toxicroak 53 | no: the Kaizo comb's draft of 2026-10-07 at Ian's boss levels. Theme: slow giants (Lickilicky, Rhyperior and Wobbuffet fit; Azelf, Mr. Mime and Toxicroak do not). On the Kaizo study's retune list |
| Mars 2 | boss (commander) | Lake Verity | Mesprit 51, Crobat, Bronzong, Purugly, Umbreon 52, Luxray 53 | no: the comb's draft at Ian's boss levels. Theme: mostly cats with her canon bat; today two cats and the bat |
| Candice | boss (leader) | Snowpoint Gym | Froslass 54, Walrein, Glaceon, Mamoswine, Articuno 55, Abomasnow 56 | no: the comb's draft; no shape written |
| Officer Hesperid 1 | mini-boss (named officer) | Lake Valor | Sudowoodo 54, Weezing, Girafarig, Chatot, Tangrowth 55, Sceptile 56 | no: the comb's draft. Theme: Kaizo teambuilding with no holds barred on rare Pokemon; today Baton Pass, Explosion and odd picks, without the BrightPowder, Petaya Berry or Choice items the theme names |
| Officers Somnu and Moira 2 | mini-boss (a double) | Lake Verity | Swalot, Skuntank 53, Glaceon 54; Abomasnow, Mamoswine 53, Gardevoir 54 | partly: cut to three each on 2026-10-29 for the six-Pokemon rule, otherwise the comb's draft. Themes: sleep (Somnu carries one Yawn) and Future Sight with hail (Moira has the hail and no Future Sight) |
| Ace Trainers Laura, Dalton, Olivia | mini-boss | Routes 216, 217 | six each, 52 to 55 | no: the comb's drafts |
| Ace Trainers Blake, Garrett, Maria | mini-boss, optional | Route 216 | six each, 52 to 55 | no |
| Snowpoint Gym's six Aces | gym trainers | Snowpoint Gym | six each, 54 to 55 | no |

No rival fights in this split, and Jupiter is not fought: her scene at Lake Acuity is after the Icicle Badge, and she does not battle there. Every other fight is an ordinary trainer: 12 in reach (Lake Valor's two optional grunts, the Lake Verity pair, Edward, and Route 217's seven), and four more above Route 216's Rock Climb walls. Of the sixteen, twelve field one Pokemon and two field two, against the rule of three to six.

## 5. Differences no doc accounts for

1. Snowpoint Gym's message after the badge reads "The level cap is now set to 62", where the engine sets 60 for HQ's split. The text is the base ROM's. One other gym's message is off too, outside this split: Sunyshore's says 78 where the engine sets Barry's 71. The other six match.
2. `fights.json` has no entry for Officer Hesperid (nor for Argo), so the OxiDex lists no fight for him. Its Somnu and Moira entry still calls them a boss, where since 2026-10-31 officers are mini-bosses; and Mars 2's note says the tree's ace is 54, where it is 53.
3. Mars 2's Bronzong carries Explosion and her flags lack Check HP, which the AI-flag ruling of 2026-10-31 sets against it. Skier Lexie's Dewgong carries Sheer Cold, a one-hit KO move no trainer may have (the Scheduled list's comb cleanup). Skier Madison's Jynx carries Perish Song.
4. Every team in the split but Somnu's breaks the rule that each member holds its own item and has its own nature, with no repeats; the ordinary teams mostly carry no items or natures at all.
5. Lake Acuity's table and Route 216's four Rock Climb trainers are tagged for Candice's split but open only with the Icicle Badge (questions 6 and 8).
6. The model reads Lake Valor's full map as reachable in this split, because Valor Lakefront's door has warps to both versions on the same tiles and the game picks one by script. The game sends the player only to the drained lake until the Distortion World.

No sequence break was found: every gate in the split is a story flag set by the fight before it, and the gym, the only place without a story check, is reachable only past Mars.

## How this was read

The world walk reused the story-route study's `worldreach.py`, with Byron's split's gates (Route 218's blockade and Celestic's grunt gone) and three stages of this split's own: Strength from the Mine Badge; the cameramen gone with the library scene; and Mt. Coronet North Room 1's two grunts and Lake Verity's Galactic gone with Mars. Its strict reading keeps every other flag-hidden object standing. Each object on every map was marked by the first stage that reaches a tile beside it. The story order was read from the scripts: `scripts_canalave_library_3f.s` for the scene's flags, `scripts_valor_cavern.s` and `scripts_verity_lakefront.s` for Saturn's flag and Lake Verity's two versions, `scripts_lake_verity.s` for Mars's, and `scripts_acuity_lakefront.s` for the Icicle Badge at Lake Acuity. Trainers came from the map events and their files, with the OxiDex's split tags, the census's roles and rewards (`trainer-roles.tsv`), `required.py`'s verdicts and honour list, and `pairs.py`'s doubles. The necks were found by trying a fixed trainer on every standable tile of each crossing in each facing, with sights up to six, and keeping those whose line cuts every way through. Wild tables came from `res/field/encounters/` with the OxiDex's capture names, items from each ball's script number, and the base ROM's changes from the story-route study's diff. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/candice-map/`.
