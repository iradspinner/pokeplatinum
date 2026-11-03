# Candice's build: an Ice core with two off-types

Ian asked on 2026-11-03 for a helper to build Candice (Snowpoint Gym, cap 56) as the primary team, erring on the side of too hard, beside his own draft. The team is in her file on the branch `overseer-candice-build` (commit 3ff0d0008a3) and waits on the Overseer's full scorer reading before it lands. Nothing was read by the scorer here, so how hard it reads is a forecast from cheap checks, and the screen and the probe misread this range.

## Summary

The six, lead first. Every member holds its own item and has its own nature. Levels follow Mars 1's shape: the ace at the cap, one at 55, the rest at 53 and 54.

| Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---:|---|---|---|---:|---|
| Cloyster (lead) | 53 | Skill Link | Focus Sash | Adamant | 95 | Spikes, Shell Smash, Icicle Spear, Drill Run |
| Alolan Ninetales | 54 | Magic Guard | Life Orb | Timid | 141 | Nasty Plot, Blizzard, Psyshock, Flamethrower |
| Chandelure | 54 | Flash Fire | Passho Berry | Mild | 108 | Shadow Ball, Fire Blast, Energy Ball, Calm Mind |
| Gastrodon | 53 | Dry Skin | Rindo Berry | Bold | 62 | Earth Power, Surf, Recover, Stealth Rock |
| Lapras | 55 | Serene Grace | Leftovers | Modest | 88 | Blizzard, Freeze-Dry, Hydro Pump, Thunderbolt |
| Mamoswine (ace) | 56 | Thick Fat | Never-Melt Ice | Jolly | 122 | Earthquake, Ice Fang, Ice Shard, Stone Edge |

The AI flags are Basic, Evaluate Attack, Expert and Check HP.

Each member's job. Cloyster lays Spikes behind its Sash, so every switch the player makes costs an eighth of its HP on top of the gym's hail, then smashes if it is given the turn. Ninetales is the answer to the Fighting and Grass types, with Nasty Plot for the free turn their switch hands it. Chandelure is the off-type for the Steel walls, the Fire attackers and the Fighting types: Flash Fire takes the Fire moves, it is immune to Fighting, and its Passho Berry lets it beat Manaphy and the special Waters, which the AI sends it into. Gastrodon is the off-type for the Fire, Rock and Steel types and the Waters: Dry Skin heals from Water moves, Earth Power hits the walls, and it lays Stealth Rock as the hub most answers draw in. Lapras is the bulky Ice that hits the Fire and Rock types with Water and Manaphy with Freeze-Dry. Mamoswine is the ace, hitting 24 or 25 of each box's likely answers for half or more.

The bait order. Cloyster opens and lays hazards into whatever leads. The player's Steel, Rock and Fire answers then draw Gastrodon; Bronzong, Metagross and Corviknight draw Chandelure; the Fighting and Grass answers draw Ninetales; Manaphy draws Chandelure, then Lapras. Each switch pays Spikes and, once Gastrodon has been in, Stealth Rock.

What each answer draws in, by the trainer AI's own replacement rule (`fightai.replacement`, run on each box), and whether the member drawn beats it on the calculator:

| Answer in front | Drawn in | Its hit, the answer's hit back (lowest roll, percent of HP) |
|---|---|---|
| Bastiodon, Probopass, Glimmora, Garganacl, Empoleon, Tentacruel | Gastrodon (Mamoswine once Gastrodon is gone) | Bastiodon 71 to 22, Probopass 67 to 28, Glimmora 144 to 56, Garganacl 59 to 26, Tentacruel 52 to 16 |
| Cinderace, Houndoom, Rapidash | Gastrodon | Cinderace 80 to 50, Houndoom 77 to 39, Rapidash 76 to 36 |
| Bronzong, Metagross, Corviknight | Chandelure | Bronzong 166 to 40, Metagross 202 to 57, Corviknight 190 to 52 |
| Heracross, Machamp, Hariyama, Breloom | Ninetales (Chandelure once it is gone) | Heracross 72 to 64, Machamp 64 to 70, Breloom 206 to 67 |
| Grass answers to Gastrodon (Tsareena, Arboliva, Leavanny, Cherrim) | Ninetales or Chandelure | Tsareena 124 to 66, Leavanny 463 to 55 (Chandelure) |
| Manaphy | Chandelure, then Lapras | Chandelure 60 to 30 with the berry; Lapras 53 to 30 |
| Frosmoth, Abomasnow | Chandelure | Frosmoth 221 to 25, Abomasnow 400 to 39 |

Machamp is the one pairing the drawn member does not clearly win; Ninetales outspeeds it and it is close.

The checks, all on the saved file.

| Check | Result |
|---|---|
| Legality | every move legal; Shell Smash added to Shellder's egg list and Freeze-Dry to Lapras's, both in `learnrewrite.IAN_EGG_MOVES` |
| Trainer lint, packer | no findings; packed |
| test_b1, test_trainers, test_learncheck, test_learnrewrite, test_learnstudy | 50/50, 44/44, 18/18, 6/6, 2/2 |
| `make rom` | built |
| Gate (`integrate.sh --verify-only`) on 3ff0d0008a3 | 53 passed; 1 failed, sync-docs, which refuses off `oxide` by design |
| Matchup screen's best six, boxes 1 to 3 (background) | 15.55, 15.35, 14.50; today's team 17.40, 21.05, 20.05 |
| AI-picks probe, rough wins of 150 against the screen's six and the common six (background) | 15 / 12, 17 / 12, 18; today's team 51, 41 / 51 / 60, 63 |
| Speed tiers | below |

The screen falls by 2 to 6 points a box, about Byron's shape C3 and short of Cyrus 1's redesign (11.7, 11.6, 10.9), which read 82. The screen cannot see Spikes, Stealth Rock or the hail, which are much of this team's case. The probe's greedy player never switches, so it overrates every team against a switching player; only the drop from today's team means anything.

What Ian decides is listed at the end. The next step is the Overseer's full reading, two and a half to four hours of machine time. If it reads harder than Ian wants, the dials are listed there too, softest first.

## Why each set is as it is

Ian's theme is four or five Ice types and one or two off-types that answer Ice's counters, chosen with the gym's permanent hail in mind. Four of the six are Ice types and take no hail. Of the two off-types, neither has Overcoat, Magic Guard, Ice Body or Snow Cloak, so each takes a sixteenth a turn; Gastrodon has Recover and Chandelure is in for short stays. No Pokemon on the team has Snow Cloak, so the team carries no evasion at all.

Cloyster's lead job is Kaizo's (Froslass's Sash and Spikes), translated: Froslass is on Deimos's HQ team, and Cloyster gives the same Sash and Spikes with Shell Smash, a Generation 5 move, in Sheer Cold's place. Drill Run hits Bastiodon and Probopass four times over, and Metagross, Empoleon, Glimmora and the Fire types twice. The AI picks Spikes on most first turns and Shell Smash on about a fifth.

Ninetales keeps Magic Guard, so the Life Orb costs it nothing and nothing chips it. Psyshock is for Tentacruel and the Fighting types, Flamethrower for the Steel types. Brenna, the gym's first guard, already carries an Alolan Ninetales with Aurora Veil, so Candice's is the attacker instead.

Chandelure's Passho Berry replaced an Expert Belt after the first runs: with the belt it lost to Manaphy, the special Water every box carries and the answer the AI sends it into. With the berry it takes Manaphy's Water hit at half and wins with Energy Ball.

Gastrodon's Stealth Rock replaced Sludge Bomb, which the AI barely used. It is the member most answers draw in, so the Rocks go down where the player is switching most, and they hit the Fire types and Frosmoth hard.

Lapras took Regice's seat. Regice, with Rock Polish, Blizzard, Thunderbolt and Focus Blast (Kaizo's Regice with Focus Blast for Sheer Cold and no Explosion), was beaten by nine answers a box and rarely drawn in. Lapras hits 20 to 24 answers a box for half or more and is beaten by few. Freeze-Dry is its Manaphy and Tentacruel move; Serene Grace doubles every secondary effect.

Mamoswine took Ice Fang over Icicle Spear for a steady 90, and Stone Edge back over Knock Off, which the AI never picked in 300 fights.

No member carries a trade move, so Check HP is not there for one. The flags guide says Check HP makes setup and healing better timed: the AI stops setting up at 70 percent or less and stops Recovering above it, and this team has Shell Smash, Nasty Plot, Calm Mind and Recover. Weather does nothing (no weather move), Harassment needs two moves from its table (only Spikes is), Risky has no critical-hit idea to serve, and Prioritize Extremes is for teams that lean mostly on status, which this one does not.

Kaizo's Candice, for reference: Froslass (Spikes, Sheer Cold), a Dragon Dance Lapras, Articuno (Sheer Cold), Regice (Rock Polish, Explosion), Mamoswine (Head Smash) and Bronzor. Translated twice: into Oxide's pool (Shell Smash, Freeze-Dry, Chandelure and Gastrodon, Life Orb and the resist berries), and down to Oxide's difficulty (no Sheer Cold, no Explosion, no Snow Cloak).

## Speed tiers

Each member against the whole box, held-back versions included. Box 1 has 87, box 2 93 and box 3 96; each box's fastest is Crobat at 159.

| Member | Speed | Outspeeds, boxes 1 to 3 | Notes |
|---|---:|---|---|
| Cloyster | 95 | 50, 53, 54 | 190 at +2: every catch |
| Ninetales | 141 | 81, 86, 88 | |
| Chandelure | 108 | 60, 56, 60 | |
| Gastrodon | 62 | 11, 17, 15 | |
| Lapras | 88 | 39, 46, 39 | |
| Mamoswine | 122 | 73, 79, 83 | Ice Shard for the rest |

Oxide has no Slush Rush, so the hail gives no Speed. Faster than Mamoswine on most boxes are Cinderace (146), Houndoom (131), Rapidash (136), Tentacruel and Manaphy (125), and Weavile on box 3 (153). Only Cinderace, Talonflame, Floatzel, Liepard, Weavile and Crobat outspeed Ninetales.

## The boxes

Goal 3's boxes for Candice's place (`plgoal3 --box candice <seed>`, run name `candice-build-study`, seeds 1 to 3), on a tree of `origin/oxide` at 291689d989, each at 56 with no earlier reading behind it.

Box 1 (Turtwig), 63 catches: Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox, Nidorino, Pawmo, Corviknight, Mandibuzz, Crobat, Talonflame, Probopass, Seaking, Quagsire, Kingler, Tentacruel, Cherrim, Sharpedo, Plusle, Leavanny, Lombre, Alolan Ninetales, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis, Granbull, Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Scyther, Mienshao, Masquerain, Crustle, Onix, Houndoom, Liepard, Toxicroak, Jellicent, Manaphy, Snorlax, Milotic, Altaria, Gastrodon, Cinderace, Octillery, Metagross, Seadra, Corsola, Goodra, Frosmoth, Mamoswine, Jynx, Dewgong. Held-back versions of Torterra, Dustox, Corviknight (two), Talonflame (two), Seaking, Kingler, Sharpedo, Leavanny (two), Lurantis, Granbull, Crawdaunt, Masquerain (two), Snorlax (two), Altaria, Octillery, Metagross, Seadra, Goodra and Mamoswine.

Box 2 (Scorbunny), 64 catches: Cinderace, Whiscash, Staraptor, Masquerain, Lombre, Bibarel, Orbeetle, Liepard, Nidorino, Mandibuzz, Crobat, Rapidash, Donphan, Seaking, Garganacl, Lumineon, Tentacruel, Vespiquen, Arboliva, Tsareena, Leavanny, Primarina, Alolan Ninetales, Bronzong, Nuzleaf, Rotom, Togetic, Bastiodon, Onix, Glaceon, Glimmora, Heracross, Granbull, Glalie, Pachirisu, Gothitelle, Floette, Murkrow, Golem, Vikavolt, Drifblim, Magcargo, Hippowdon, Palossand, Tropius, Floatzel, Sharpedo, Drapion, Lopunny, Manaphy, Skitty, Jellicent, Toxicroak, Ceruledge, Empoleon, Gastrodon, Corsola, Octillery, Lurantis, Milotic, Frosmoth, Mr. Rime, Absol, Dewgong. Held-back versions of Cinderace, Masquerain (three), Orbeetle (three), Liepard (two), Donphan (two), Seaking, Lumineon, Tsareena, Leavanny (two), Bronzong (two), Nuzleaf, Granbull, Gothitelle, Vikavolt (two), Magcargo (two), Palossand, Sharpedo, Drapion and Lurantis.

Box 3 (Piplup), 64 catches: Empoleon, Seaking, Corviknight, Orbeetle, Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Mandibuzz, Crobat, Hariyama, Onix, Roselia, Golem, Kingler, Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom, Lombre, Mothim, Carbink, Vikavolt, Rotom, Togetic, Bastiodon, Salazzle, Glaceon, Crustle, Leavanny, Granbull, Bronzong, Gothitelle, Sinistea, Floette, Happiny, Glimmora, Yanmega, Castform, Quagsire, Garganacl, Palossand, Lopunny, Grapploct, Sharpedo, Gliscor, Qwilfish, Manaphy, Pikachu, Crawdaunt, Altaria, Gastrodon, Cinderace, Lumineon, Metagross, Octillery, Nuzleaf, Floatzel, Frosmoth, Glalie, Weavile, Dewgong. Held-back versions of Empoleon, Seaking, Corviknight (two), Orbeetle (three), Hariyama, Kingler, Breloom (three), Vikavolt (two), Leavanny (two), Granbull, Bronzong (two), Gothitelle, Yanmega, Palossand, Sharpedo, Gliscor (two), Crawdaunt, Altaria, Lumineon, Metagross and Weavile (three).

No six played a scored fight, since nothing was read by the scorer. The sixes the cheap checks played against the saved team were these.

| Box | The screen's best six (the probe's first six) | The six its top 20 take most (the probe's second) |
|---|---|---|
| 1 | Probopass, Abomasnow, Glimmora, Houndoom, Manaphy, Snorlax | the same six |
| 2 | Cinderace, Arboliva, Bronzong, Glimmora, Heracross, Manaphy | Heracross, Manaphy, Glimmora, Bronzong, Cinderace, Bastiodon |
| 3 | Breloom, Bastiodon, Bronzong, Glimmora, Manaphy, Frosmoth | Glimmora, Manaphy, Bastiodon, Cinderace, Bronzong, Leavanny |

The likely answers, by the kinds the brief names, as each box holds them:

| Kind | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Steel and Rock walls | Corviknight, Probopass, Bastiodon, Metagross, Garganacl, Glimmora, Golem, Carbink, Crustle, Onix | Bronzong, Bastiodon, Empoleon, Garganacl, Glimmora, Golem, Onix | Empoleon, Corviknight, Bronzong, Bastiodon, Metagross, Garganacl, Glimmora, Golem, Carbink, Crustle, Onix |
| Fire attackers | Cinderace, Houndoom, Talonflame | Cinderace, Rapidash, Ceruledge, Magcargo | Cinderace, Salazzle |
| Fighting attackers | Mienshao | Heracross, Lopunny | Machamp, Hariyama, Breloom, Grapploct, Lopunny |
| Special Waters | Manaphy, Tentacruel, Jellicent, Milotic, Octillery, Gastrodon | Manaphy, Primarina, Tentacruel, Jellicent, Milotic, Octillery, Gastrodon | Manaphy, Tentacruel, Octillery, Gastrodon |
| Others the screen takes against this team | Snorlax, Abomasnow, Frosmoth, Cherrim, Crawdaunt | Frosmoth, Tsareena, Arboliva, Leavanny, Glalie, Rotom | Frosmoth, Leavanny, Glalie, Floatzel, Rotom, Weavile |

Manaphy is in 16 to 20 of the screen's top 20 sixes on every box, Glimmora in 10 to 19, Bronzong in 9 to 13 on boxes 2 and 3.

## Species left out

No member repeats a species from the bosses near her, read from each file on `origin/oxide` and, for Byron, Ian's redraft on `origin/overseer-byron-ian`.

| Fight | Species left out |
|---|---|
| Mars 2 | Liepard, Crobat, Incineroar, Galarian Zapdos, Mesprit, Purugly |
| Saturn 1 | Glimmora, Mantine, Naganadel, Tropius, Azelf, Salazzle |
| Hesperid 1 | Weezing, Sceptile, Girafarig, Sudowoodo, Wigglytuff, Chatot |
| Somnu and Moira | Swalot, Stantler, Gardevoir, Abomasnow, Mr. Rime, Glaceon |
| Cyrus 1 | Swampert, Honchkrow, Porygon-Z, Electivire, Magmortar, Salamence |
| Byron (Ian's redraft) | Metagross, Galvantula, Hisuian Goodra, Kartana, Empoleon, Celesteela |
| Barry 5 | Staraptor, Primeape, Greninja, Snorlax, Turtonator, Torterra, Serperior, Infernape |
| Cyrus 2 | Skarmory, Magnezone, Dusknoir, Houndoom, Suicune, Weavile |
| Saturn 2 | Uxie, Lickilicky, Wobbuffet, Wailord, Rhyperior, Toxicroak |
| Phobos and Deimos 3 | Granbull, Mawile, Arcanine, Arbok, Froslass |
| Boreas and Laverna 2 | Talonflame, Pidgeot, Yanmega, Sableye, Kecleon |
| Argo and Hesperid at the HQ | Claydol, Cofagrigus, Bronzong, Relicanth, Polteageist, Spinda, Spiritomb, Pinsir |

That leaves Oxide's fully evolved Ice types as Alolan Ninetales, Articuno, Cloyster, Delibird, Dewgong, Frosmoth, Glalie, Jynx, Lapras, Mamoswine, Regice and Walrein. Of today's team, Froslass, Glaceon and Abomasnow were out by this rule; Walrein and Articuno were left for Lapras, and Articuno also for its Snow Cloak.

## Ian's decisions

1. Chandelure and Gastrodon as the two off-types (recommended), against a Steel type such as Lucario, which Rock and Fire answers would share less with the Ice core but which the hail chips the same.
2. Check HP for timing setup and Recover (recommended), or the three base flags alone.
3. Cloyster leading, with Brenna's Aurora Veil Ninetales already in the gym (recommended), or Ninetales leading with Veil as Brenna's does.
4. If the reading reads harder than he wants, the dials softest first: Stealth Rock back to Sludge Bomb; Ninetales's Life Orb for a Sitrus Berry; Cloyster's Shell Smash for Rock Blast.

## How the numbers were made

The scripts are in `/home/ian/.claude/jobs/382760ce/tmp/candice-build/`, adapted from the Candice pass's `bc.py` and `checks.py` and the Byron redesign's shapes, run under `tools/oxide/capped`; none writes to `res/`. `shapes.py` holds the five shapes tried (A to E; E is the build), and `bc.swap_party` puts one into Candice's file in memory. `checks.py` prints the six as the simulator builds it, the screen's top 20, the margins, the Speed tiers against each whole box, the replacement trace (`fightai.replacement` on a battle from `perfectline.make_battle`), the damage both ways and the AI-picks probe of 150 rough fights against two sixes. `matrix.py` prints each member's best hit on every likely answer and back, from the scorer's own calculator rows, with the screen's four moves for each answer. `apply.py` saved shape E through `trainers.save`. `legal.py` is the Kaizo study's legality checker with the TMs from before the TM pass. The saved file's checks are `out/saved-1.txt` to `out/saved-3.txt` and `out/saved-m-1.txt` to `out/saved-m-3.txt`. The hail is goal 3's own: `plscore.prepare` starts her fight in it (`candice-split.md`).

The shapes on the probe and the screen, box by box, for the record:

| Shape | What changed | Screen, boxes 1 to 3 | Probe rough wins |
|---|---|---|---|
| Today | the file before | 17.40, 21.05, 20.05 | 51, 41 / 51 / 60, 63 |
| A | Regice in Lapras's seat, Rock Blast for Drill Run, Expert Belt Chandelure | 16.30, 17.55, 16.90 | 33 / 60, 56 / 53, 42 |
| B | Lapras for Regice | 16.00, 17.40, 17.25 | 16 / 36, 10 / 37, 7 |
| C | Stealth Rock, Psyshock, Freeze-Dry | 15.55, 16.50, 15.65 | 21, 19 / 29, 25 / 12, 16 |
| D | Passho Berry, Knock Off | 15.55, 15.35, 14.50 | 28 / 17, 16 / 14, 9 |
| E, saved | Stone Edge back, Check HP | 15.55, 15.35, 14.50 | 15 / 12, 17 / 12, 18 |
