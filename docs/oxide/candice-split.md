# Candice's split: mandatory fights and the level climb

Candice's split runs from Byron's badge (cap 53) to Candice's (cap 56). Ian answered the map's nine questions on 2026-11-01 (`candice-split-map.md`): no honour cap inside the split, the caps kept at 53, 56 and 60, Saturn 1's ace at 53 and Mars 2's at 54, Officer Hesperid's ace at 53 with his difficulty in his sets, Officers Somnu and Moira at 52, the recommended count of 12, Route 216's four Rock Climb trainers left for HQ's split, no gauntlet, Lake Acuity's table moved to HQ's split, and Azelf and Mesprit kept. This page is the split's trainer pass, done as Byron's was, on the branch `overseer-candice-pass`. Nothing lands until Ian says yes.

## Summary

The split now counts 12 mandatory fights, gym trainers apart, mini-bosses included and a pair counted once. Six were mandatory already; this branch fixes one trainer in place, moves four to necks, and makes Lake Verity's talking grunt a trainer in free slot 131. Twenty-nine ordinary, mini-boss and gym teams were built, the new grunt's among them, each with one idea, three to five Pokemon, its own item and nature on every member, and its AI flags set by the guide. The ordinary teams climb from 52 at the lakes to 55 at Route 217's north neck, where only Black Belt Luke reaches 55; the route Ace Trainers' aces sit at 54, two under the cap; Snowpoint Gym's six climb from 54 to 55. The bosses and officers took Ian's levels and the rule fixes and nothing more. Skier Lexie's Sheer Cold is gone. Nothing was seen in game, and the scorer read nothing.

| Area | Mandatory fights | Of them, this branch's |
|---|---:|---:|
| Lake Valor | 2 (Officer Hesperid; Grunt 1) | 1 |
| Lake Verity | 3 (the new grunt; the grunt pair; Somnu and Moira) | 1 |
| Route 216 | 2 (Skier Edward; Ace Trainer Laura) | 1 |
| Route 217 | 5 (Skier Shawn; Ace Trainer Dalton; Ninja Boy Ethan; Black Belt Luke; Ace Trainer Olivia) | 3 |
| In all | 12 | 6 |

Ian's decisions:

1. Mars 2's and Candice's Baton Pass flag: neither team knows Baton Pass, and through the flag's bug it pushes every status move and Explosion (below). Drop it from both (my pick), drop it from Mars 2 only, or keep it on both?
2. Saturn 1's Setup First Turn flag does nothing, since his lead, Azelf, knows no move in its table: drop it (my pick) or keep it?
3. Hesperid's sets: keep them as they stand at 53 for now (my pick), with a checked-stage redesign to his theme later; or have that redesign drafted now?
4. Candice's five Blizzards with no hail: her Abomasnow's first ability is Adaptability in Oxide, not Snow Warning. Keep it (my pick, since the fight already reads a little harder than Byron's), or give it Snow Warning, which makes every Blizzard sure and the fight harder?
5. The 29 teams below: a yes for the whole set, or the trainers to change.

Next steps:

| Step | Who | Time |
|---|---|---|
| Answer the five questions | Ian | 15 minutes |
| Apply the answers on this branch, rerun the checks, land it with `merge-branch.sh` | the Overseer | 1 hour |
| Walk the split's mandatory fights with the test kit or a save after Byron | Ian | 40 minutes |

What is unverified:

- Nothing has been seen in game. The moves come from the tile model.
- No fight was read by the scorer, under the standing ruling.
- The Lake Verity grunt pair and the Somnu and Moira double were checked as files only; the probe cannot play a double.
- The speed check reads eight reference species at the cap, not goal 3's boxes, and only the bosses and Hesperid had the screen and the probe.
- The simulator does not model BrightPowder, so no Hesperid candidate built on his theme's items could be read.

## The mandatory fights

Ian's rules apply: every mandatory fight that is not a boss counts, mini-bosses included; a trainer who turns, spins or walks is optional; a pair is one fight; gym trainers do not count. A trainer with a reward stays optional (Lake Valor's Grunt 3, Ace Trainer Blake, Skier Lexie).

| # | Fight | Map | How it is known |
|---:|---|---|---|
| 1 | Galactic Grunt 1 (moved) | Lake Valor, drained | required.py, after the move |
| 2 | Officer Hesperid, a mini-boss | Lake Valor, drained | required.py, unchanged |
| 3 | The new grunt at the lake's mouth (free slot 131) | Lake Verity | required.py |
| 4 | Grunts 1 and 2, a pair | Lake Verity | required.py, unchanged |
| 5 | Officers Somnu and Moira, a double, mini-bosses | Lake Verity | Ian's honour rule (required.py's honour list) |
| 6 | Skier Edward (moved) | Route 216 | required.py, after the move |
| 7 | Ace Trainer Laura, a mini-boss | Route 216 | required.py, unchanged |
| 8 | Skier Shawn (moved) | Route 217 | required.py, after the move |
| 9 | Ace Trainer Dalton, a mini-boss | Route 217 | required.py, unchanged |
| 10 | Ninja Boy Ethan (moved) | Route 217 | required.py, after the move |
| 11 | Black Belt Luke (fixed) | Route 217 | required.py, after the change |
| 12 | Ace Trainer Olivia, a mini-boss | Route 217 | required.py, unchanged |

The bosses are Saturn 1, Mars 2 and Candice. Snowpoint's six gym trainers are gym trainers. The split holds no gauntlet section, as Ian answered.

### The trainers moved

Each keeps its class and script, and now looks one fixed way. A tile is written (x, z).

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Lake Valor's Grunt 1 | (19, 28), looking north into open ground, sight 5 | (21, 23), looking east, sight 3 | The way from the lakefront to Valor Cavern passes the one-tile neck at (22, 23), which he sees. The tile west of him, (20, 23), becomes a dead end and holds nothing. |
| The talking grunt at Lake Verity, made a trainer | (47, 51), on the shore, only talking ("Ow! Ouch!") | (46, 53), looking east, sight 2 | The lake's mouth is two tiles wide above its two entrance warps; he stands on the west one and sees the east one. He keeps his hide flag, so he is there only in the Galactic version of the lake, and Mars's win removes him with the other grunts. His old script is now reached by nothing. |
| Skier Edward | Route 216 (311, 402), walking about, sight 1 | (304, 385), looking east, sight 2 | The west neck north of Snowbound Lodge, which every way to Route 217 crosses. |
| Skier Shawn | Route 217 (318, 344), walking about, sight 3 | (304, 371), looking east, sight 3 | The south neck just north of Maylene's scene. Ace Trainer Dalton's line, two rows up, shares no tile with his. |
| Ninja Boy Ethan | Route 217 (290, 321), disguised in the snow, seeing every way, sight 1 | (289, 272), looking east, sight 1, undisguised | The north neck by the signpost. A sight of 2 would share a tile with Luke's line and make a double, so it is 1. |
| Black Belt Luke | (291, 273), walking north and south | the same tile, standing still, looking north, sight 2 | North covers the route's last crossing before Acuity Lakefront. |

The checks, each run on the edited files:

- required.py reads all six required. `test_b1e` passes 11 of 11, its totals repinned from 85 required and 99 avoidable to 90 and 95.
- From every warp of the four maps, in Candice's, HQ's and Volkner's splits, the player still reaches every tile reached before, but for the moved trainers' own tiles and the dead-end tile behind Lake Valor's Grunt 1.
- No moved trainer stands on a warp, sign, hidden item, trigger or another object.
- `pairs.py`'s list of pairs is unchanged: no new double, and none lost.
- No scripted walk crosses the new tiles: Lake Verity's scenes move Rowan and the counterpart only near Mars, and Route 217's Maylene scene runs on its trigger south of Shawn.
- The four maps are declared in `bulk_events.py`'s DIVERGED, and the new slot's name, class, lines, flags and team in `trainers_diverged.json`.

### Rewards

No reward sits on a trainer now mandatory, so none moved: the split's three rewards stay with Lake Valor's Grunt 3 (Metronome), Ace Trainer Blake (Ring Target) and Skier Lexie (Ability Shield), all optional. `rewards.py write` regenerated `trainer-roles.tsv`, and `rewards.py check` has 0 failures.

## The level climb

With no honour cap inside the split, ordinary trainers climb in play order under Candice's 56: the lakes at 52 to 53, the north at 53 to 55, with 55 only on Black Belt Luke, the last ordinary fight before Acuity Lakefront. The route Ace Trainers keep their aces two under the cap, at 54. The gym's six climb from the door, 54 to 55. Route 216's four Rock Climb trainers are first met in HQ's split, so they are levelled for its cap of 60, at 56 to 57. In the table, "Old" and "New" are each team's highest level, and "Size" is the old size, then the new one.

| # | Trainer | Area | Stretch | Kind | Old | New | Size |
|---:|---|---|---|---|---:|---:|---|
| 1 | Galactic Grunt 1 | Lake Valor, drained | 1, the lakes | mandatory (moved) | 50 | 52 | 1 to 4 |
| 2 | Galactic Grunt 3 | Lake Valor, drained | 1, the lakes | optional (Metronome reward) | 50 | 53 | 1 to 3 |
| 3 | Galactic Grunt, new | Lake Verity, the mouth | 1, the lakes | mandatory (new) | none | 53 | 0 to 3 |
| 4 | Galactic Grunt 1 | Lake Verity | 1, the lakes | mandatory, pair with Grunt 2 | 50 | 53 | 1 to 3 |
| 5 | Galactic Grunt 2 | Lake Verity | 1, the lakes | mandatory, pair with Grunt 1 | 50 | 53 | 1 to 3 |
| 6 | Skier Edward | Route 216 | 2, the north | mandatory (moved) | 50 | 54 | 1 to 4 |
| 7 | Ace Trainer Laura | Route 216 | 2, the north | mandatory, mini-boss | 55 | 54 | 6 to 5 |
| 8 | Ace Trainer Blake | Route 216 | 2, the north | optional, mini-boss (Ring Target reward) | 55 | 54 | 6 to 5 |
| 9 | Ace Trainer Garrett | Route 216 | 2, the north | optional, mini-boss | 55 | 54 | 6 to 5 |
| 10 | Ace Trainer Maria | Route 216 | 2, the north | optional, mini-boss | 55 | 54 | 6 to 4 |
| 11 | Skier Shawn | Route 217 | 2, the north | mandatory (moved) | 51 | 54 | 1 to 4 |
| 12 | Ace Trainer Dalton | Route 217 | 2, the north | mandatory, mini-boss | 55 | 54 | 6 to 5 |
| 13 | Skier Lexie | Route 217 | 2, the north | optional (Ability Shield reward) | 51 | 54 | 2 to 3 |
| 14 | Skier Bjorn | Route 217 | 2, the north | optional | 51 | 54 | 1 to 3 |
| 15 | Skier Madison | Route 217 | 2, the north | optional | 51 | 54 | 1 to 3 |
| 16 | Ninja Boy Matthew | Route 217 | 2, the north | optional | 51 | 54 | 1 to 3 |
| 17 | Ninja Boy Ethan | Route 217 | 2, the north | mandatory (moved) | 51 | 54 | 1 to 4 |
| 18 | Black Belt Luke | Route 217 | 2, the north | mandatory (fixed) | 51 | 55 | 3 to 4 |
| 19 | Ace Trainer Olivia | Route 217 | 2, the north | mandatory, mini-boss | 55 | 54 | 6 to 5 |
| 20 | Ace Trainer Brenna | Snowpoint Gym | gym | gym, first from the door | 55 | 54 | 6 to 3 |
| 21 | Ace Trainer Isaiah | Snowpoint Gym | gym | gym | 55 | 55 | 6 to 4 |
| 22 | Ace Trainer Sergio | Snowpoint Gym | gym | gym | 55 | 54 | 6 to 3 |
| 23 | Ace Trainer Savannah | Snowpoint Gym | gym | gym | 55 | 55 | 6 to 4 |
| 24 | Ace Trainer Alicia | Snowpoint Gym | gym | gym | 55 | 55 | 6 to 3 |
| 25 | Ace Trainer Anton | Snowpoint Gym | gym | gym, the last guard | 55 | 55 | 6 to 5 |
| 26 | Skier Bradley | Route 216, above Rock Climb | HQ's split (60) | optional | 54 | 56 | 3 to 3 |
| 27 | Skier Kaitlyn | Route 216, above Rock Climb | HQ's split (60) | optional | 54 | 57 | 2 to 3 |
| 28 | Skier Andrea | Route 216, above Rock Climb | HQ's split (60) | optional | 55 | 57 | 1 to 3 |
| 29 | Black Belt Philip | Route 216, above Rock Climb | HQ's split (60) | optional | 56 | 57 | 1 to 4 |

Not climbed, and why:

- Bosses: Saturn 1, Mars 2 and Candice, given Ian's levels below.
- The officers Hesperid, Somnu and Moira, given Ian's levels below.
- The Rock Climb four are climbed, for HQ's split, as the table says.

### The teams

Each line gives the team in send-out order, its one idea, and any AI flag it carries beyond Basic, Evaluate Attack and Expert.

| Trainer | Team | The idea | Flags beyond the base |
|---|---|---|---|
| Galactic Grunt 1 | Clodsire 52, Muk 52, Nidoqueen 52, Gastrodon 52 | Mud of the drained lake: an Unaware Clodsire lays Toxic Spikes, then Muk, a Sheer Force Nidoqueen and a Gastrodon. | none |
| Galactic Grunt 3 | Liepard 52, Arbok 52, Banette 53 | Paralysis, then the bite: Prankster Thunder Wave and Glare, then a Cursed Body Banette whose Hex doubles on the paralysed. | Harassment |
| Galactic Grunt, new | Gyarados 52, Staraptor 52, Arcanine 53 | The sore guard at the lake's mouth: Intimidate on all three, so the player's physical hits land weak, with Thunder Wave and Taunt to keep them so. | none |
| Galactic Grunt 1 | Weezing 52, Drapion 52, Nidoking 53 | With his partner across the shore, poison in three shapes: Weezing's burns, Drapion's Knock Off, and a Sheer Force Nidoking with a Life Orb. | none |
| Galactic Grunt 2 | Honchkrow 52, Weavile 52, Houndoom 53 | With her partner: a night raid of Dark types that strike first, Sucker Punch and Heat Wave over both of the player's Pokemon. | none |
| Skier Edward | Abomasnow 53, Glalie 53, Walrein 53, Mamoswine 54 | Downhill in the hail: Snow Warning Abomasnow, then Blizzard that never misses from Glalie and Walrein, and an Ice Body to heal. | none |
| Ace Trainer Laura | Roserade 52, Tropius 52, Breloom 53, Tangrowth 52, Venusaur 54 | A garden in the snow: Spikes and sleep from Roserade, Breloom's Spore and Technician, a Regenerator Tangrowth, and a Venusaur ace. | none |
| Ace Trainer Blake | Kangaskhan 52, Miltank 52, Exploud 53, Porygon-Z 53, Snorlax 54 | No immunity holds: Scrappy Kangaskhan, Miltank and Exploud hit Ghosts with Normal moves beside a Porygon-Z and a Snorlax, the idea his Ring Target prize carries on. | none |
| Ace Trainer Garrett | Bronzong 52, Espeon 52, Alakazam 53, Gallade 53, Metagross 54 | Minds of steel: Psychic and Steel together, Magic Guard and Magic Bounce under Metagross's Meteor Mash. | none |
| Ace Trainer Maria | Chandelure 52, Arcanine 53, Magmortar 53, Typhlosion 54 | Fire against the ice ahead: Flash Fire and Flame Body on four fire types, Will-O-Wisp, and a Typhlosion's Eruption to close. | none |
| Skier Shawn | Weavile 53, Absol 54, Scizor 54, Dewgong 54 | First on the ice: priority from four sides, Ice Shard, Sucker Punch, Bullet Punch and Aqua Jet. | none |
| Ace Trainer Dalton | Abomasnow 52, Glalie 52, Dewgong 53, Magmortar 53, Electivire 54 | Hail and two sparks: Snow Warning hail, so Blizzard cannot miss, beside an Electivire and a Magmortar that hit the Steel, Water and Fire types an ice team fears. | none |
| Skier Lexie | Dewgong 54, Walrein 54, Glaceon 54 | Snowbound walls: Thick Fat and Ice Body stall with Toxic, Yawn, Encore and Wish. | Prioritize Extremes |
| Skier Bjorn | Piloswine 54, Snorlax 54, Mamoswine 54 | Tusks and thick hide: Thick Fat on three heavy hitters. | none |
| Skier Madison | Jynx 54, Mismagius 54, Gengar 54 | Lullabies on the slope: Lovely Kiss and Hypnosis, then a Hex on the sleepers and a Calm Mind. | Harassment |
| Ninja Boy Matthew | Ninjask 54, Scizor 54, Shedinja 54 | Speed passed down the line: Ninjask boosts and Baton Passes to a Scizor, and a Shedinja waits behind them. | Baton Pass |
| Ninja Boy Ethan | Froslass 54, Banette 54, Sableye 54, Dusknoir 54 | Ghosts in the snow: a Cursed Body Froslass lays Spikes, then ghosts that burn, sneak in first and strip items. | none |
| Black Belt Luke | Hitmonchan 54, Pawmot 54, Infernape 55, Machamp 55 | Iron fists at the north neck: Iron Fist punches, then Machamp's No Guard Dynamic Punch. | none |
| Ace Trainer Olivia | Lapras 52, Gyarados 52, Kingdra 53, Goodra 53, Dragonite 54 | Dragons that fear no ice: a singing Lapras, then Dragon Dance from Gyarados, Kingdra and a Multiscale Dragonite, with a Goodra the ice barely scratches. | none |
| Ace Trainer Brenna | Alolan Ninetales 54, Glaceon 54, Walrein 54 | The first guard: Ice Body in hail from a Snow Warning Ninetales, healing while it chips. | none |
| Ace Trainer Isaiah | Piloswine 54, Quagsire 54, Swampert 54, Mamoswine 55 | Ground under the ice: Thick Fat and Earthquake, Stealth Rock, and an Unaware Quagsire. | none |
| Ace Trainer Sergio | Mr. Rime 54, Jynx 54, Frosmoth 54 | Moths and mimes: an Ice Scales Frosmoth Quiver Dances behind Mr. Rime's screens. | none |
| Ace Trainer Savannah | Froslass 54, Jellicent 54, Mismagius 54, Weavile 55 | Ghosts of the snowfield: a Cursed Body Froslass and a Jellicent, then Hex on the burned and frozen. | Harassment |
| Ace Trainer Alicia | Dewgong 54, Lapras 55, Cloyster 55 | Shells and sea ice: a Skill Link Cloyster with a King's Rock behind a Dewgong's Encore and a Lapras. | none |
| Ace Trainer Anton | Glalie 54, Articuno 55, Delibird 54, Mamoswine 55, Weavile 55 | The last guard: Candice's ice in five shapes, from an Articuno's Roost to a Weavile's Ice Shard. | none |
| Skier Bradley | Furret 56, Stantler 56, Linoone 56 | Normal tricks on the high slope: an Adaptability Furret, an Intimidate Stantler, and a Gluttony Linoone that Belly Drums into its Salac Berry. | none |
| Skier Kaitlyn | Delibird 56, Cloyster 56, Mamoswine 57 | Presents from the peak: an Adaptability Delibird, a Skill Link Cloyster that lays Spikes behind its Focus Sash, and a Mamoswine. | none |
| Skier Andrea | Drifblim 56, Froslass 57, Chandelure 57 | A ghost story on the summit: Froslass and Chandelure burn and haunt, and a Drifblim passes the night along. | none |
| Black Belt Philip | Hitmonlee 56, Lucario 57, Hariyama 56, Machamp 57 | Training on the cliff: No Guard Dynamic Punch, Reckless kicks and a Justified Lucario. | none |

No rebuilt team carries a one-hit KO move, an evasion move or item, a Choice item, or trapping. Skier Lexie's Dewgong loses Sheer Cold. Skier Madison's Jynx loses Perish Song: her team's idea is sleep, and Perish Song without a trap does little against a player who switches. No ordinary team carries a trade move. Four set weather by ability, as trainers may: Skier Edward's and Ace Trainer Dalton's Abomasnow and Ace Trainer Brenna's Alolan Ninetales bring hail by Snow Warning, and no team carries a weather move. No member is Modest, Adamant, Timid or Jolly: each takes a nature that raises the same stat as the textbook one, or a neutral one, by the variety ruling, and no nature repeats inside a team. The comb's drafts were read for ideas only, and nothing was drawn from Kaizo's data.

### The AI flags

Every rebuilt team runs Basic, Evaluate Attack and Expert, and adds a flag only where the guide's rule fits its idea:

| Flag | Rule | Teams |
|---|---|---|
| Check HP | a trade move | none among the rebuilt teams |
| Risky | critical hits are the idea | none: the Scope Lens and Razor Claw holders (Lake Verity's Grunt 2, Skier Shawn, Ace Trainers Garrett, Olivia and Anton) carry high-critical moves as coverage |
| Harassment | status or hazards are the idea, with two of its table's moves | Lake Valor's Grunt 3 (Thunder Wave, Glare, Will-O-Wisp), Skier Madison (Lovely Kiss, Hypnosis, Will-O-Wisp), Ace Trainer Savannah (Will-O-Wisp twice, Spikes) |
| Weather | a lead with a weather move | none |
| Prioritize Extremes | most members lean on status moves | Skier Lexie (Toxic, Yawn, Encore, Wish, Protect) |
| Baton Pass | not in the guide; the idea is a Baton Pass chain | Ninja Boy Matthew, whose Ninjask sets up on its first turn and passes it on |

Black Belt Luke loses the Prioritize Extremes he carried from the base ROM: his team attacks, and Bulk Up is its one setup move.

### Speed against the box

Eight fast answers a box is likely to hold, at the cap, IV 15, neutral natures:

| Cap | Box answers |
|---|---|
| 53 | Crobat 150, Talonflame 146, Weavile 145, Greninja 142, Mienshao 124, Staraptor 124, Garchomp 121, Lucario 108 |
| 56 | Crobat 159, Talonflame 154, Weavile 153, Greninja 150, Mienshao 131, Staraptor 131, Garchomp 127, Lucario 114 |
| 60 | Crobat 170, Talonflame 165, Weavile 164, Greninja 160, Mienshao 140, Staraptor 140, Garchomp 136, Lucario 122 |

Each team's fastest member, at its own IVs and nature, fastest first: Matthew's Ninjask 211; Savannah's and Anton's Weavile 173; Lake Verity's Grunt 2's Weavile 163; Andrea's Froslass 159; Lake Valor's Grunt 3's Liepard 152; Shawn's Weavile, Luke's Infernape, Madison's Gengar and Ethan's Froslass 151; Garrett's Espeon 148; Kaitlyn's Delibird 145; Maria's Typhlosion 141; Brenna's Alolan Ninetales 140; Dalton's Glalie 137; Philip's Lucario 134; Bradley's Furret 132; the new grunt's Staraptor 128; Blake's Porygon-Z 127; Laura's Roserade 125; Edward's Glalie 125; Sergio's Jynx 123; Lake Verity's Grunt 1's Drapion 117; Bjorn's Mamoswine and Olivia's Gyarados 115; Isaiah's Mamoswine 108; Alicia's Cloyster 97; Lexie's Dewgong 95; Lake Valor's Grunt 1's Nidoqueen 88.

So a Ninjask and four Weavile outspeed every answer at 56, and about half the teams have one member near Crobat's tier; the rest sit under the box's fast answers, as Byron's did.

## The bosses and officers

Ian's levels, and the rule fixes, with no other change to their sets:

| Fight | Levels | Rule fixes |
|---|---|---|
| Saturn 1 | 51 to 53, as before, the ace at 53 | Mr. Mime Hasty, Lickilicky Brave, Toxicroak Lonely, so Timid and Adamant appear once |
| Mars 2 | 52, four at 53, Luxray 54 (each one up, the ace to 54) | Purugly Hasty; Bronzong holds a Sitrus Berry for its second Leftovers; Check HP for Bronzong's Explosion |
| Candice | 54 to 56, as before, the ace at the cap | Articuno Mild, Abomasnow Brave |
| Officer Hesperid 1 | 51, four at 52, Sceptile 53 (each three down) | Chatot Hasty |
| Officer Somnu | 51, 51, 52 (each two down) | none needed |
| Officer Moira | 51, 51, 52 (each two down) | Abomasnow Quiet |

Every move is still legal at its new level. `fights.json` now lists Hesperid 1 and Argo 1 as fights, so the OxiDex shows them; Somnu and Moira's note no longer calls them a boss, and Mars 2's gives her ace of 54.

### How they read

Each cell is the player's wins in 150 rough fights against the matchup screen's best six, then against the six it takes most; one number means the two were the same six. The player is the Byron check's greedy probe player, who never switches, never sets up and holds no items, so only the comparison between rows means anything. Byron's row matches the Byron check's own numbers exactly, which says the harness reads as that one did. Fewer wins means a harder fight.

| Fight, on its own boxes | Box 1 | Box 2 | Box 3 | Screen's best score, by box |
|---|---|---|---|---|
| Cyrus 1 (47), for scale | 61, 29 | 44, 20 | 44 | 17.30, 17.20, 17.70 |
| Byron (53), for scale | 69, 81 | 67, 81 | 41, 86 | 18.15, 18.60, 19.75 |
| Hesperid 1 (53) | 68, 59 | 67, 70 | 96, 52 | 20.25, 19.60, 19.60 |
| Saturn 1 (53) | 40 | 29 | 28, 40 | 19.10, 17.95, 17.80 |
| Mars 2 (54) | 67, 61 | 109, 132 | 118, 126 | 21.15, 22.30, 21.00 |
| Candice (56) | 57, 59 | 62, 48 | 30, 48 | 17.55, 21.05, 20.05 |

Saturn 1 reads the hardest of the split's fights, harder than Byron and about as hard as Cyrus 1. His Rhyperior makes the most knockouts (198 to 244 a six), and his Azelf lead passes Ian's lead test: its common answers, Bastiodon, Metagross and Probopass, draw Rhyperior, which beats them. His Wobbuffet has Shadow Tag in Oxide, a trap, which the named Galactic fights may carry; it uses Counter about 350 times a six.

Hesperid 1 at 53 reads easier than Saturn and about as Byron, so he sits under his commander, as Ian asked. At his old levels, 54 to 56, he read 44 and 103, 68, and 113 and 81: within the probe's spread of today's numbers, so the three levels cost him little on this check. His Sudowoodo lead passes the lead test (its answers draw Tangrowth, Chatot with Nasty Plot, or Girafarig with Agility).

Mars 2 reads the easiest of the split's bosses, well under Saturn, though her ace is one level higher. Her Mesprit lead mostly passes the lead test (its answers draw Bronzong, which beats most of them), but Bronzong itself, in 14 of the top 20 sixes on box 2, draws her own Bronzong and beats it. Her Bronzong explodes above 70 percent HP in 32 to 48 fights of 150, although it has Check HP now: the Baton Pass flag cancels it (question 1).

Candice reads a little harder than Byron. Mamoswine, Abomasnow and Walrein make most of her knockouts; her Froslass lead makes the fewest (20 to 52 a six) and fails the lead test on box 2, where Bronzong and Heracross, each in all 20 of the top sixes, draw Glaceon and Articuno, which lose to them. Her team holds five Blizzards and no hail (question 4).

Speeds in battle: Saturn's Azelf 151, Toxicroak 111, the rest 55 to 125; Mars's Crobat 174, Purugly 154, Luxray 124, Mesprit 114, Umbreon 90, Bronzong 50; Candice's Froslass 154, Articuno 115, Mamoswine 110, the rest 80 to 93. Against the box's Crobat at 159 and Weavile at 153 for Candice's cap, only Mars's Crobat outspeeds them.

The Somnu and Moira double could not be probed, since the probe plays single battles only; its two files were checked for legality, items and natures.

### The questions, with their numbers

Question 1, the Baton Pass flag on Mars 2 and Candice. Neither team knows Baton Pass. By the flag's bug (O2 in `battle-ai/other-flags.md`), it adds 3, then 1 more at 60 percent HP or more, to every move the damage check skips, 68.75 percent of the time: every status move, and Explosion. So it pushes their leads to open with Stealth Rock, Spikes or Thunder Wave, and it cancels the Check HP that Mars 2's Bronzong took for its Explosion. Without it:

| | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Mars 2, as it stands | 67, 61 | 109, 132 | 118, 126 |
| Mars 2, no Baton Pass flag | 62, 43 | 90, 114 | 124, 99 |
| Bronzong's Explosions above 70 percent HP a six, as it stands | 36 to 43 | 32 to 42 | 47 to 48 |
| The same, no Baton Pass flag | 2 | 2 to 3 | 6 to 7 |
| Candice, as she stands | 57, 59 | 62, 48 | 30, 48 |
| Candice, no Baton Pass flag | 43, 37 | 51, 56 | 48, 54 |

Without the flag both read a little harder for the probe player, since the leads attack more (Candice's Froslass Blizzards 19 to 47 times a six where it did 1 to 6) and Bronzong keeps its Explosion for low HP, where the player can see it coming. Mars 2's lead still opens with Stealth Rock in about half its fights, where it did in two of three. I would drop the flag from both: it does no job its name says on either team, and on Mars 2 it undoes the Check HP fix.

Question 2, Saturn 1's Setup First Turn. It adds 2 on the battle's first turn to the moves in its table, and Azelf, his lead, knows none of them (Stealth Rock is not in it). Later members never get it, since the turn is the battle's. It does nothing in this fight, so I would drop it; the check needs no run.

Question 3, Hesperid's sets. Ian asked for his difficulty to be in his sets, and his theme (boss-shapes.md) names BrightPowder, a Petaya Berry, Explosion with Pursuit and Baton Pass, and Choice items on rarely used Pokemon. Today he has the Explosion, the Baton Pass and a Starf Berry, and reads about as Byron and easier than Saturn, which fits "no higher than his commander". The simulator does not model BrightPowder, so a draft built on the theme's items could not be read, and a Choice item makes an AI team weaker in play than on paper (the standing ruling on Choice items). I would keep him as he stands and give him the checked-stage redesign his theme asks for when Ian has a picture of it; the Overseer can start one in about two hours.

Question 4, Candice's Blizzards. Five of her six carry Blizzard, and none sets hail: in Oxide her Abomasnow's first ability is Adaptability, not Snow Warning, which is its third. Snow Warning would make every Blizzard sure-hitting for five turns from Abomasnow's entry, and Abomasnow comes in second in 37 to 69 fights of 150 on the boxes. That is a material change to a leader's fight and the fight reads a little harder than Byron already, so I would keep it as it is unless Ian wants her to be the hail gym in play as well as in name.

## The census

The OxiDex moves Lake Acuity's table from Candice's split to HQ's (Ian's answer 8), in `design.json` and `progression.py`'s default table; `availability.md` is regenerated, and no line's first split moves. Route 216's four Rock Climb trainers are tagged HQ's in `splits.py` (answer 6). The map's item 6, that the OxiDex reads Lake Valor's full map as reachable in this split, is out of this pass's scope and is unchanged.

## The in-game checks

The check is in `ingame-checklist.md`, section 4, **Mandatory fights, Candice's split**: walk from Byron's badge to Snowpoint without dodging anyone, and see each of the six fights below meet you where this page says, with the Ethan and Luke fights two singles, never a double.

1. Lake Valor's Grunt 1 by the one-tile gap on the way to Valor Cavern.
2. The new grunt at Lake Verity's mouth, with his own lines, gone after Mars.
3. Skier Edward at Route 216's west neck.
4. Skier Shawn at Route 217's south neck, with Maylene's scene still running and Dalton fought alone.
5. Ninja Boy Ethan and Black Belt Luke at Route 217's north neck, two battles.
6. The Rock Climb four still out of reach before the Icicle Badge.

## How the numbers were made

The mandatory verdicts are `tools.oxide.balance.required`'s field model on the edited events; the necks came from the map's search (`candice-split-map.md`). The teams were written as data and checked before saving by the Kaizo study's legality reader (`out/tools/oxide.py`), pointed at this branch's `res/` and at the export from before the TM pass. Every team was saved through `tools.oxide.encounters.trainers.save`, which runs the trainer lint and the real packer and records the file in `trainers_diverged.json`. The boss numbers come from the Byron check's scripts, pointed at this branch, in `/home/ian/.claude/jobs/382760ce/tmp/candice-pass/` (`checks/bc.py` is the harness; `AIBITS` swaps a trainer's flags and `CAND` a level set in memory, and nothing writes to `res/`). Goal 3's boxes come from `plgoal3.setup` with the run name `candice-pass-study`, seeds 1 to 3, each fight on its own boxes: Saturn 1 and Hesperid 1 at 53, Mars 2 at 54, Candice at 56, Byron at 53 and Cyrus 1 at 47.

| Check | Result |
|---|---|
| required.py on the four maps | the six changed fights all required |
| `test_b1e` | 11 of 11, totals repinned to 90, 95 and 12 |
| `pairs.py` | the list unchanged |
| Reach from every warp, three splits | unchanged but the moved trainers' tiles and one dead end |
| Trainer lint, every changed team | no findings |
| The real packer, through `trainers.save` | every team packed |
| Moves legal at their level (Kaizo checker) | all legal |
| Item or nature repeated in a team, nature unnamed | none |
| One-hit KO, trapping, evasion, Choice item | none on the rebuilt teams |
| `test_trainers` | 44 of 44 |
| `test_b1` | 49 of 49 |
| `test_learncheck`, `test_learnrewrite` | 18 of 18, 6 of 6 |
| The encounter tool's 21 suites | all pass; test_trainers failed once while a save ran beside it, and passes alone |
| `rewards.py check` | 0 failures |
| `make rom`, then `integrate.sh --verify-only` | {GATE} |
