# Tyche and Hermes 1: the Veilstone tag battle

Ian asked on 2026-10-29 for the two Veilstone warehouse grunts to become Officers Tyche and Hermes, for Lucas and Dawn to bring six Pokemon built on their Route 207 team, and for a 10 against 12 fight at officer difficulty: Protect used heavily, no Self-Destruct or Explosion, and classic villain-team Pokemon. This page holds stage 1 (the rename, the split, the partner's six and three shapes) and stage 2 (Ian's answers and the sets), on the branch `overseer-tyche-hermes-1`. Nothing lands from it until the Overseer lands the branch.

## Summary of stage 2

**Outcome.** The ten sets are in the two Veilstone files, built on Ian's pick, shape A made faster and frailer: Tyche's Golbat, Murkrow, Weezing and Haunter, with an Ariados using Silk Trap, and Hermes's Electrode and Sharpedo, with a Mightyena using Obstruct, a Seviper and Giovanni's Dugtrio as the ace. The partner has Scyther with its Eviolite again and Lopunny keeps Jump Kick. The scene's text names the officers. The lint, the packer and both legality checks pass on every changed team. The AI-picks probe was not run, because the simulator reads only single battles; no reading of a tag double is possible. Goal 3's count is fixed the repo's own way, in its own commit: both Tyche and Hermes fights are story fights in `fights.json` marked as doubles, as Somnu and Moira's is, so goal 3 reads 39 bosses again and leaves both out as doubles (`test_plgoal3` 72 of 72).

Three findings change what stage 1 said. Oxide's Nidoking has no Poison Point (its abilities are Mold Breaker and Sheer Force), so it could not be softened as Ian asked, and a Mold Breaker Earthquake would hit Tyche's Levitating Pokemon; Dugtrio took the ace's place. No classic villain Pokemon in Oxide is fast, frail and immune to Ground without repeating a line already on the team, so Tyche's fifth, Ariados, is the one member Hermes's Earthquake hits. And in the engine Obstruct and Silk Trap run as a plain Protect, without their stat drop on contact, while Spiky Shield, Baneful Bunker and Burning Bulwark run in full; stage 1 had that partly the wrong way round.

**What Ian decides**, one line each:

1. Dugtrio's Arena Trap stops the player's grounded Pokemon from switching while it stands, the rare trapping the trainer rules allow. Keep it, or take Sand Veil, which does nothing without sand?
2. Ariados as Tyche's fifth, though Earthquake hits it, or a Ground-immune pick that breaks a rule: Gyarados (bulky, and one of Cyrus's canon five), Bronzong back (slow), or a second stage of a line already there (Crobat, Honchkrow or Gengar)?
3. The text changes below: read before landing.

**Next steps.** An in-game check of the fight, now on the checklist: about twenty minutes of Ian's play, from a save before Maylene's badge or from the test kit. The scorer cannot read it.

## Ian's answers (2026-10-29)

1. Shape A, "but speedier and frailer; I like the golbat murkrow weezing haunter electrode & sharpedo". The other four slots are faster, frailer picks in the same idea, classic villain-team Pokemon, no Self-Destruct or Explosion; a Nidoking, if it stays, is softened to Poison Point and a Soft Sand ("Soften it").
2. Protect's later cousins are approved through the egg-list rule: Silk Trap on Ariados, Spiky Shield on Cacturne, Burning Bulwark on Camerupt, Obstruct on the Mightyena line, used where they fit.
3. The partner has Scyther with its Eviolite, as on Route 207; Umbreon leads; Lopunny keeps Jump Kick ("Keep Jump Kick").
4. Change the text now: the speaker labels, "run like the grunts we are", and Tyche's Spear Pillar defeat line.
5. Goal 3's count: first "leave it failing", then the same day "Let's just fix this now", with his approval of the scorer data change: both Tyche and Hermes fights become story fights in `fights.json` marked as doubles, as Somnu and Moira's is.

## Summary of stage 1

**Outcome.** One test failed on the branch at stage 1 (fixed in stage 2): since the rename, goal 3's fight list counts the four officer files as single fights, and `test_plgoal3` reads 43 bosses where it expects 39 (question 7 has the fix). The rename, the split and the partner's six are in the files on the branch. The Veilstone grunts are Officer Tyche (female grunt class, and the north warehouse object now wears the female grunt's sprite) and Officer Hermes; the Spear Pillar pair carry the same names. The OxiDex and the balance tools place both officers and all six partner files in Wake's split, where the partner files had no split at all before. Each partner file holds six Pokemon at 39 to 41: Ian's Route 207 core grown on (Umbreon, Scizor, Lopunny, Pachirisu, Gastrodon) and the rival's starter at 41. Tyche's and Hermes's teams are untouched: three shapes for them are below, as proposals.

**Recommendation.** Shape A, "the quake beside the shield". Hermes brings Ground and Rock attackers whose Earthquakes and Rock Slides hit everything on the field, and Tyche brings five Protect users that Earthquake cannot touch (Flying or Levitate). It is Spear Pillar's "Protect beside Explosion" at a lower level, with Earthquake in Explosion's place, and Oxide's trainer AI already plays it: it scores Earthquake up beside a partner immune to it, and scores Protect up in every double. Every member is legal today and nine of the ten are classic villain-team Pokemon.

**What Ian decides**, one line each (the questions section has the reasoning):

1. Which shape for Tyche and Hermes: A (recommended), B or C, or a mix.
2. Nidoking, Hermes's ace in shape A, one-shots five of the boxes' core answers with Sheer Force and an Expert Belt. Keep that, or soften it to Poison Point with a Soft Sand?
3. Scizor in the partner's six (the line evolved, by its Metal Coat) or Scyther with its Eviolite, as on Route 207?
4. Lopunny's Jump Kick became Drain Punch, since a Jump Kick into Protect crashes for half its HP. Agree?
5. Partner lead: Umbreon, as on Route 207 (Reflect on turn 1), or Lopunny (Fake Out on turn 1)?
6. Five lines of the Veilstone scene still call the pair grunts (below). Change them to "Tyche:" and "Hermes:" and drop "run like the grunts we are"?
7. Since the rename, goal 3's fight list reads the four officer files (Veilstone and Spear Pillar) as single named Galactic fights, and its test fails (43 bosses where it expects 39). Fix it as Somnu and Moira are done, two story fights marked as doubles in `fights.json`, or in goal 3's own list?
8. Protect's later cousins on villain Pokemon through the egg-list rule: Silk Trap on Ariados, Spiky Shield on Cacturne, Obstruct on Mightyena, Burning Bulwark on Camerupt. Any of them?

**Next steps.** Stage 2 writes the shape Ian picks into the two files, with every member's set checked by the legality checker and the packer, and the cheap checks rerun on the final sets: about an hour. A spot-check reading is not possible for this fight, since the scorer and goal 3 do not read doubles; the judgement is the cheap checks and Ian's, and then an in-game check of the battle.

## What changed in the files

| File | Change |
|---|---|
| `galactic_grunt_veilstone_city_1` | named Officer Tyche, class female grunt; party unchanged |
| `galactic_grunt_veilstone_city_2` | named Officer Hermes; party unchanged |
| `galactic_grunt_spear_pillar_1` and `_2` | named Officer Tyche and Officer Hermes (were Grunt Tyche and Grunt Hermes) |
| `lucas_veilstone_city_*`, `dawn_veilstone_city_*` (six) | three Pokemon at 35 and 36 became the six below |
| `events_veilstone_city.json` | the north warehouse grunt (object 7, Tyche, who speaks as "Grunt 1") uses `OBJ_EVENT_GFX_GRUNT_F`; its local id is `LOCALID_GRUNT_F_WAREHOUSE_NORTH`, which nothing else names |
| `bulk_events.py` | the Veilstone events entry in DIVERGED gains the sprite and Ian's ruling |
| `splits.py` | `TRAINER_SPLITS` places the eight trainers in Wake's split, with Ian's ruling |
| `test_b1.py` | a check that the eight sit in Wake's split; it failed before the override (both officers in Maylene's, the six partners in none) and passes after |
| `test_trainers.py` | the OxiDex's pairs check finds the Spear Pillar pair by its file, since the Veilstone tag battle's row also carries both names now |
| `trainers_diverged.json` | the six partner parties, the four names and Tyche's class registered, so the base ROM importer leaves them |
| `script-index.md` | regenerated: the partner files' levels and sizes, and the Spear Pillar names |

The scorer's own split table (`plscore.SPLIT_OVERRIDE`) needs no entry. It falls back to the census placement, which now reads Wake for both officers, and then to `trainer_split`, which reads Wake for the partners.

## The scene's text

Tyche is the north grunt, who speaks as "Grunt 1", and Hermes the south one, "Grunt 2". These lines now read wrong with officers in them; none was changed.

| Message | Line | What reads wrong |
|---|---|---|
| 11, 12, 14, 16 | "Grunt 1: ..." | the speaker label |
| 13, 15, 18 | "Grunt 2: ..." | the speaker label |
| 16 | "Our Pokémon are chumps! We should get new ones from headquarters." | odd from an officer, though it passes as bluster |
| 18 | "And run like the grunts we are." | wrong for officers |
| Spear Pillar Tyche's defeat line | "The toughest of all the grunts! That was me..." | wrong now that she is titled Officer |

The rest (Lucas's and Dawn's lines, the officers' defeat lines at Veilstone, Looker's) reads fine.

## The partner's six

One core in all six files; the ace follows the player's starter as vanilla's does, the line the player's starter beats. Dawn's and Lucas's files of one version are the same but for the trainer and the genders. All IVs are the highest (iv_scale 255), and the AI flags stay Basic, Evaluate Attack and Expert; the engine adds its doubles strategy in any double. Speed is each member's own at its level.

| Slot | Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|---|
| Lead | Umbreon | 39 | Inner Focus (hidden) | Light Clay | Timid | Foul Play, Snarl, Reflect, Yawn | 73 |
| 2 | Scizor | 40 | Technician | Metal Coat | Adamant | Bullet Punch, X-Scissor, Knock Off, Brick Break | 69 |
| 3 | Lopunny | 39 | Scrappy | Lum Berry | Jolly | Fake Out, Drain Punch, Ice Punch, Dizzy Punch | 107 |
| 4 | Pachirisu | 39 | Adaptability | Sitrus Berry | Hasty | Electroweb, Wild Charge, Seed Bomb, Super Fang | 100 |
| 5 | Gastrodon | 40 | Dry Skin | Leftovers | Modest | Muddy Water, Earth Power, Ice Beam, Stealth Rock | 48 |
| Ace, Turtwig player (`_turtwig`) | Empoleon | 41 | Torrent | Mystic Water | Brave | Aqua Tail, Drill Peck, Knock Off, Aqua Jet | 59 |
| Ace, Scorbunny player (`_chimchar`) | Torterra | 41 | Thick Fat | Miracle Seed | Brave | Wood Hammer, Rock Slide, Crunch, Curse | 56 |
| Ace, Piplup player (`_piplup`) | Infernape | 41 | Iron Fist | Charcoal | Naive | Fire Punch, Close Combat, Mach Punch, Thunder Punch | 116 |

The Route 207 core stays, with the Flareon and Jolteon of today's Veilstone files gone, and each set is turned toward a double beside the player. Nothing in the six hits its own side: Snarl, Electroweb, Muddy Water and Rock Slide hit only the foes, and Earthquake, Discharge and Surf are left out. Umbreon keeps Reflect with Light Clay for eight turns over both the player's Pokemon and its own, and its Yawn also stops a foe's Protect: the trainer AI marks Protect down on a Pokemon that is drowsy or badly poisoned. Lopunny's Fake Out opens a turn for the player, and Pachirisu's Electroweb slows both foes. Scizor is Scyther evolved by its Metal Coat; Ian chose Scyther on Route 207 for its Flying type as bait against Fighting leads, a reason that does not carry to an ally (question 3). Oxide's Empoleon is the physical one (Attack 111 to Special Attack 86), so the Turtwig version's ace loses Prinplup's special set. Torterra takes Thick Fat, which halves its four-times Ice weakness. Infernape's Iron Fist powers three punches. Every move is on its species' lists at its level (the Kaizo study's checker with the pre-TM-pass lists, and `learnsets.oxide_list`); no item or nature repeats in a file; the lint and the packer pass on all six.

## Three shapes for Tyche and Hermes

Every shape has five Pokemon a side, each ace at 41 and the rest at 39 or 40, no repeated item or nature within a trainer, and no Self-Destruct or Explosion. The officers would take Spear Pillar's AI flags (Basic, Evaluate Attack, Expert, Risky, Check HP; the doubles strategy comes from the engine). Every move but the four marked in shape C is legal now, Protect through the TM lists of before the TM pass. Engine notes, corrected in stage 2: Spiky Shield, Baneful Bunker and Burning Bulwark run in full, their damage, poison and burn on contact included (the move-pool survey's notes that they are plain Protects are out of date), while Obstruct, Silk Trap and King's Shield run as a plain Protect, their stat drop on contact missing. Every Protect cousin shares Protect's effect, so the AI treats them all as Protect.

### Shape A: the quake beside the shield (recommended)

Tyche is the shield: five Protect users, every one immune to Ground by a Flying type or Levitate. Hermes is the quake: Ground and Rock attackers and the speed control for them.

| Side | Member | Level | Ability | Item | Nature | Moves | Speed | Role | Villain team |
|---|---|---|---|---|---|---|---|---|---|
| Tyche | Golbat | 40 | Inner Focus | Eviolite | Impish | Protect, Toxic, Poison Fang, Taunt | 89 | bulky Toxic and Protect stall; grows into Spear Pillar's Crobat | the Zubat line, the grunts' staple of Rocket, Magma, Aqua and Galactic |
| Tyche | Murkrow | 39 | Prankster (hidden) | Sitrus Berry | Calm | Protect, Thunder Wave, Foul Play, Taunt | 88 | first-move Thunder Wave and Taunt for the slow quakers | Rocket's Ariana in HeartGold; the line is Cyrus's |
| Tyche | Haunter | 39 | Levitate | Focus Sash | Timid | Protect, Will-O-Wisp, Shadow Ball, Sludge Bomb | 112 | burns the player's physical answers; grows into Spear Pillar's Gengar | none; a continuity pick |
| Tyche | Bronzong | 40 | Levitate | Leftovers | Relaxed | Protect, Gyro Ball, Toxic, Stealth Rock | 38 | hazard and wall | Galactic: Mars, Jupiter and Saturn all carry the Bronzor line |
| Tyche | Weezing (ace) | 41 | Levitate | Rocky Helmet | Bold | Protect, Will-O-Wisp, Sludge Bomb, Pain Split | 66 | physical wall that punishes contact | Rocket: its grunts, James, and Petrel in HeartGold |
| Hermes | Electrode | 39 | Soundproof | Light Clay | Timid | Light Screen, Thunder Wave, Thunderbolt, Taunt | 138 | fastest on the field: screens and paralysis | Rocket's Mahogany hideout; Hermes's Spear Pillar Electrode, without Explosion |
| Hermes | Camerupt | 40 | Solid Rock | Passho Berry | Quiet | Earthquake, Heat Wave, Rock Slide, Protect | 44 | spread damage, all three moves hitting both foes | Magma: Maxie and Tabitha |
| Hermes | Rhydon | 40 | Lightning Rod | Eviolite | Adamant | Earthquake, Rock Slide, Ice Fang, Protect | 49 | the main quake; draws in the player's single-target Electric moves | Giovanni |
| Hermes | Sharpedo | 39 | Speed Boost (hidden) | Mystic Water | Jolly | Protect, Crunch, Waterfall, Earthquake | 100, then 150 | Protect on turn 1 for a free Speed Boost | Aqua: Archie, Shelly and Matt |
| Hermes | Nidoking (ace) | 41 | Sheer Force (hidden) | Expert Belt | Naive | Earthquake, Sludge Bomb, Ice Beam, Thunderbolt | 95 | the hardest hitter | Giovanni |

**How the sides work together.** In the engine's doubles strategy (`TagStrategy_Earthquake`, `script.s`), an Earthquake scores +2 when the user's partner is Flying, Levitating or under Magnet Rise, and -3 or -10 when the partner would be hit. Beside any of Tyche's five, Hermes's Earthquake is therefore his favourite move, and it hits the player's Pokemon and the partner's together. Expert_Protect gives Protect +2 in every double (less after one in a row), so Tyche protects often while Golbat's and Bronzong's Toxic ticks. Nidoking must not carry Mold Breaker: the same routine knows Mold Breaker gets past Levitate, and its Earthquake would then hit Haunter, Bronzong and Weezing.

**Cheap checks.** The answers are goal 3's three boxes as Maylene's reading builds them (`plgoal3 --run <scratch> --box maylene <seed> --screen`, seeds 1 to 3): the catches the player brings to Veilstone, raised to the honour cap of 41, Hardy, IVs of 15, first ability, no item. Across the three boxes the screen's top sixes lean on Tentacruel, Togetic, Bastiodon, Granbull and Alolan Ninetales, with Dusclops on box 1, Heracross on box 2, and Delphox (in every six), Breloom and a held Machoke on box 3. Damage is the scorer's calculator, lowest roll to highest as a share of the defender's HP, with spread moves at three quarters.

Speed against the boxes' tiers: Electrode outspeeds everything. Haunter (112) is passed only by the player's Crobat (117). Nidoking (95) sits one point under Delphox (96) and two over Tentacruel and Alolan Ninetales (93), a knife edge of the kind that swung Gardenia. Golbat and Murkrow (89 and 88) sit over Heracross (80). Rhydon, Camerupt and Bronzong (49, 44, 38) move after nearly everything; Electrode's Thunder Wave and Murkrow's Prankster one are their speed control. The partner's Electroweb takes Nidoking from 95 to 63.

| Hermes's best hit | Damage |
|---|---|
| Rhydon's Earthquake on Tentacruel, Delphox | 118 to 140, 112 to 133 |
| Rhydon's Earthquake on the partner's Pachirisu | 139 to 164 |
| Rhydon's Rock Slide on Alolan Ninetales | 76 to 90 |
| Camerupt's Heat Wave on Breloom, Heracross | 116 to 137, 68 to 81 |
| Camerupt's Heat Wave on the partner's Scizor | 153 to 183 |
| Nidoking's Sludge Bomb on Togetic, Granbull, Breloom | 126 to 150, 157 to 188, 192 to 230 |
| Nidoking's Ice Beam on Staraptor | 125 to 148 |
| Sharpedo's Waterfall on Delphox | 114 to 134 |

| The player's and partner's best hit | Damage |
|---|---|
| Delphox's Psyshock on Golbat, Weezing, Haunter | 54 to 64, 53 to 63, 114 to 136 |
| Alolan Ninetales's Triple Axel on Golbat, Murkrow | 70 to 87, 183 to 221 |
| Granbull's Spirit Break on Murkrow | 146 to 174 |
| Tentacruel's Scald on Rhydon | 110 to 132 |
| Heracross's Close Combat on Sharpedo | 226 to 268 |
| Partner's Infernape, Fire Punch on Bronzong | 87 to 103 |
| Partner's Gastrodon, Muddy Water on Rhydon | 111 to 132 |
| Partner's Torterra, Wood Hammer on Rhydon | 132 to 156 |
| Best box answer on Bronzong (Delphox's Mystical Fire) | 53 to 65 |

The read: Hermes's side is lethal and frail, and Tyche's side is hard to hurt and does little damage itself (her biggest hits are Haunter's and Weezing's Sludge Bombs on Granbull, 108 to 129 and 98 to 117; the rest is small). The player wins by killing the quakers fast with Water, Grass and Fighting moves, and by bringing Flying or Levitating Pokemon (Togetic, Crobat, Staraptor, a Bronzong of their own) that the quakes cannot touch. The player's own Ground moves, and the partner's Gastrodon's, are blanked against Tyche. The likely cost is a Pokemon or two to the Earthquakes and to Nidoking, which fits an officer: close to 100 percent won, with deaths that are not trivial. Nidoking is the dial (question 2): with Poison Point and a Soft Sand its Sludge Bomb on Togetic falls to about 81 to 96.

### Shape B: poison and patience

Tyche spreads poison and stalls behind Protect; Hermes waits out the ticks with Intimidate, paralysis, priority and his own Protects.

| Side | Member | Level | Ability | Item | Nature | Moves | Speed | Villain team |
|---|---|---|---|---|---|---|---|---|
| Tyche | Toxapex (ace) | 41 | Merciless | Black Sludge | Bold | Baneful Bunker, Toxic, Venoshock, Recover | 46 | none in canon; an Alolan poison pick in Team Skull's spirit |
| Tyche | Weezing | 40 | Levitate | Rocky Helmet | Calm | Protect, Will-O-Wisp, Sludge Bomb, Pain Split | 65 | Rocket |
| Tyche | Muk | 40 | Poison Touch (hidden) | Shuca Berry | Adamant | Protect, Poison Jab, Knock Off, Shadow Sneak | 57 | Rocket's grunts |
| Tyche | Ariados | 39 | Intimidate | Focus Sash | Jolly | Protect, Toxic Spikes, Sucker Punch, Poison Jab | 78 | Guzma, Team Skull |
| Tyche | Cacturne | 39 | Water Absorb (hidden) | Sitrus Berry | Naughty | Protect, Leech Seed, Sucker Punch, Seed Bomb | 59 | James of the anime's Team Rocket |
| Hermes | Mightyena | 39 | Intimidate | Scope Lens | Impish | Protect, Yawn, Sucker Punch, Crunch | 71 | Magma and Aqua |
| Hermes | Seviper | 40 | Infiltrator (hidden) | Poison Barb | Hasty | Protect, Glare, Poison Fang, Sucker Punch | 106 | Jessie of the anime's Team Rocket |
| Hermes | Sharpedo | 39 | Speed Boost (hidden) | Mystic Water | Jolly | Protect, Crunch, Waterfall, Ice Fang | 100 | Aqua |
| Hermes | Salazzle | 40 | Corrosion | Charcoal | Timid | Toxic, Flamethrower, Sludge Bomb, Taunt | 122 | Plumeria (Team Skull) and Oleana (Macro Cosmos) |
| Hermes | Drapion (ace) | 41 | Battle Armor | Leftovers | Adamant | Protect, Knock Off, Poison Fang, Ice Fang | 95 | Ghetsis, in Black 2 and White 2 |

How they work together: Protect scores +2 in any double, so both sides protect often while Tyche's Toxic, Toxic Spikes and Leech Seed tick, and every Protect turn costs the player HP. The counterplay is the same rule turned round: the AI marks Protect down on a Pokemon that is itself badly poisoned, seeded or drowsy, so the player's own Toxic or Yawn stops it. Salazzle's Corrosion poisons the Steel and Poison answers (Bastiodon, Bronzong, Tentacruel, Crobat) that would otherwise wall a poison team; Corrosion runs in Oxide's poison subscripts. Two Intimidates, Glare and Yawn blunt the player's physical side. There is no spread-move pairing between the sides, so the two halves fight side by side more than together. Cheap checks: the team's damage is spread out (Seviper's Poison Fang on Togetic and Breloom, 125 to 149; Salazzle's Flamethrower on Breloom, 166 to 198), and its weak points are Psychic and Ground (Delphox's Psyshock takes Seviper 112 to 132 and Salazzle 103 to 124; the partner's Earth Power takes Salazzle 221 to 262). The checks underrate status and stall in long fights, so this shape would read easier on paper than it plays.

### Shape C: the modern villains

The shape for Ian's wish for more Generation 5 and later Pokemon. Tyche's shields are the modern ones: Wide Guard, Crafty Shield and Queenly Majesty.

| Side | Member | Level | Ability | Item | Nature | Moves | Speed | Villain team |
|---|---|---|---|---|---|---|---|---|
| Tyche | Toxapex (ace) | 41 | Regenerator | Black Sludge | Bold | Baneful Bunker, Wide Guard, Toxic, Recover | 46 | as in shape B |
| Tyche | Cofagrigus | 40 | Mummy | Leftovers | Relaxed | Crafty Shield, Will-O-Wisp, Hex, Haze | 36 | Ghetsis, in Black and White and in Black 2 and White 2 |
| Tyche | Ferrothorn | 40 | Iron Barbs | Rocky Helmet | Sassy | Protect\*, Gyro Ball, Stealth Rock, Thunder Wave | 29 | Chairman Rose (Macro Cosmos) |
| Tyche | Tsareena | 39 | Queenly Majesty | Lum Berry | Jolly | Protect\*, Trop Kick, Knock Off, Play Rough | 96 | Oleana (Macro Cosmos) |
| Tyche | Froslass | 39 | Cursed Body (hidden) | Focus Sash | Timid | Protect, Will-O-Wisp, Icy Wind, Shadow Ball | 112 | Oleana |
| Hermes | Liepard | 39 | Prankster | Sitrus Berry | Naive | Fake Out, Foul Play, Thunder Wave, Snarl | 117 | Team Plasma's grunts and Marnie |
| Hermes | Salazzle | 40 | Corrosion | Charcoal | Modest | Protect\*, Flamethrower, Sludge Bomb, Toxic | 111 | Plumeria and Oleana |
| Hermes | Drapion | 40 | Battle Armor | Leftovers | Adamant | Protect, Knock Off, Poison Fang, Ice Fang | 93 | Ghetsis |
| Hermes | Ariados | 39 | Intimidate | Kebia Berry | Careful | Protect, Sucker Punch, Poison Jab, X-Scissor | 78 | Guzma |
| Hermes | Mienshao (ace) | 41 | Regenerator | Expert Belt | Jolly | Protect\*, Drain Punch, Knock Off, Stone Edge | 113 | Lysandre (Team Flare) |

\* Not on the species' lists today: Ferroseed, Bounsweet, Salandit and Mienfoo would take Protect on their egg lists, by Ian's rule for moves on teams he builds.

How they work together: Toxapex's Wide Guard blocks the spread moves the player's side leans on (the partner's Muddy Water, Electroweb, Snarl and Rock Slide); Cofagrigus's Crafty Shield blocks status moves aimed at its side (Yawn, Thunder Wave, Will-O-Wisp); and Tsareena's Queenly Majesty stops priority moves against her and her partner, the partner's Fake Out, Bullet Punch, Mach Punch and Aqua Jet among them. Hermes's side carries the damage: Mienshao's Stone Edge takes Togetic 110 to 131 and Delphox 108 to 128, and Salazzle's Flamethrower takes Heracross 108 to 128. Its weak point is Ground and Fire: the partner's Earth Power takes Salazzle 221 to 262 and the Infernape's Fire Punch takes Ferrothorn 172 to 208. Whether the AI uses Wide Guard and Crafty Shield at sensible times is not checked; their effect is not Protect's, so Expert_Protect's scoring does not apply to them.

### Why A

A carries Ian's theme most clearly: Spear Pillar's fight is Protect while the partner fires a move that hits the whole field, and A is the same fight with Earthquake in Explosion's place, a first taste the later fight builds on. The engine's AI plays it without help, which shapes B and C need more luck for. It rises into Spear Pillar's teams (Golbat into Crobat, Haunter into Gengar, Electrode kept), uses no member of Cyrus's canon five (though Golbat and Murkrow are the first stages of two of them), and needs no list changes. Its cost is Ian's wish for later Pokemon: it has none. A mix could take C's Liepard (Prankster Thunder Wave) in Murkrow's place, though Liepard is hit by the Earthquakes, so Hermes's AI would quake less beside it.

## Questions for Ian, with their reasoning

1. **The shape.** A, B or C, or a mix (above).
2. **Nidoking's power.** Sheer Force raises Sludge Bomb, Ice Beam and Thunderbolt by 1.3 and the Expert Belt raises super-effective hits by 1.2, so Nidoking one-shots Togetic, Granbull, Alolan Ninetales, Breloom and Staraptor, five of the boxes' core answers, and outspeeds all of them but Crobat, Salazzle, Staraptor and Delphox. Poison Point with a Soft Sand keeps its Earthquake and cuts the rest by about a third.
3. **Scizor or Scyther.** Scizor is the line grown on and the stronger ally (Technician Bullet Punch with a Metal Coat); Scyther with its Eviolite keeps Ian's Flying type from Route 207.
4. **Jump Kick.** In a fight built on Protect, a Jump Kick into Protect crashes for half of Lopunny's HP, and the AI does not foresee it; Drain Punch hits nearly as hard (75 against 100) and heals.
5. **The partner's lead.** Umbreon sets Reflect for both sides on turn 1; Lopunny leads with Fake Out, the usual doubles opener, which also takes the turn Sharpedo would spend on its Protect.
6. **The text.** The speaker labels and two lines (the scene's text above); changing them is a separate commit.
7. **Goal 3's list.** `goal3_fights.py` in `~/oxide-trials/scorer-stage2` takes a trainer named "Galactic Officer" as a named Galactic fight and finds tag battles only through the partner flag, which the Veilstone script does not use. Since the rename it lists both Veilstone officers (Wake's split) and both Spear Pillar ones (Galactic) as single fights, so the milestone reading would read each alone, and `test_plgoal3` fails its count (43 bosses, 41 Ace Trainers, against 39 and 41). The repo's own pattern is the Somnu and Moira double: a story fight in `tools/oxide/balance/fights.json` marked `"tag": true`, which goal 3 drops as a double. Two such entries (Tyche and Hermes 1 in Wake's split with the six partner files, 2 in Galactic's) would also need the reference hacks' empty seats and `test_b1`'s name and under-cap lists. This branch does neither, since both reach past stage 1.
8. **Protect's cousins.** Silk Trap (Ariados, a spider), Spiky Shield (Cacturne, a cactus), Obstruct (Mightyena) and Burning Bulwark (Camerupt) all run in Oxide's engine. Stage 2 found that Obstruct and Silk Trap run as a plain Protect, without their stat drop on contact, and that Spiky Shield runs in full; stage 1 had the two the wrong way round. None of these Pokemon learns them today; each would go on its line's egg list.

## Stage 2: the sets

Both officers take Spear Pillar's AI flags (Basic, Evaluate Attack, Expert, Risky, Tag Strategy, Check HP) and the highest IVs (iv_scale 255). Each ace is at the honour cap of 41 and the rest at 39 or 40; no item or nature repeats within a trainer, and the natures lean away from the textbook pick. Speed is each member's own at its level.

### Officer Tyche, the shield

| Member | Level | Ability | Item | Nature | Moves | Speed | Villain team |
|---|---|---|---|---|---|---|---|
| Golbat | 40 | Inner Focus | Eviolite | Impish | Protect, Toxic, Poison Fang, Taunt | 89 | the Zubat line, the grunts' staple of Rocket, Magma, Aqua and Galactic |
| Murkrow | 39 | Prankster (hidden) | Sitrus Berry | Calm | Protect, Thunder Wave, Foul Play, Taunt | 88 | Rocket's Ariana in HeartGold |
| Ariados | 39 | Intimidate | Mental Herb | Lax | Silk Trap, Toxic Spikes, Sucker Punch, Poison Jab | 71 | Guzma, Team Skull |
| Weezing | 40 | Levitate | Rocky Helmet | Relaxed | Protect, Will-O-Wisp, Sludge Bomb, Pain Split | 58 | Rocket |
| Haunter (ace) | 41 | Levitate | Focus Sash | Rash | Protect, Will-O-Wisp, Shadow Ball, Sludge Bomb | 107 | none; it grows into Spear Pillar's Gengar |

### Officer Hermes, the quake

| Member | Level | Ability | Item | Nature | Moves | Speed | Villain team |
|---|---|---|---|---|---|---|---|
| Electrode | 39 | Soundproof | Light Clay | Modest | Light Screen, Thunder Wave, Thunderbolt, Taunt | 126 | Rocket's Mahogany hideout; Hermes's Spear Pillar Electrode |
| Mightyena | 39 | Intimidate | Chople Berry | Lonely | Obstruct, Throat Chop, Bulldoze, Ice Fang | 71 | Magma and Aqua |
| Seviper | 40 | Infiltrator (hidden) | Poison Barb | Hasty | Protect, Earthquake, Poison Fang, Glare | 106 | Jessie of the anime's Team Rocket |
| Sharpedo | 40 | Speed Boost (hidden) | Mystic Water | Naughty | Protect, Crunch, Waterfall, Earthquake | 93, then 139 | Aqua: Archie, Shelly and Matt |
| Dugtrio (ace) | 41 | Arena Trap | Soft Sand | Naive | Earthquake, Rock Slide, Sucker Punch, Protect | 127 | Giovanni's gym |

**How the sides work together.** Four of Tyche's five are immune to Ground (Golbat and Murkrow fly, Weezing and Haunter levitate), and the engine's doubles strategy scores an Earthquake or a Bulldoze +2 beside such a partner, so Dugtrio, Seviper and Sharpedo quake and Mightyena bulldozes while Tyche protects; Protect scores +2 in any double. Beside Ariados, which Earthquake hits, the AI marks Earthquake -3, and Dugtrio's Rock Slide, which hits only the foes, carries the turn. Every member but Electrode has a Protect, and Mightyena's Obstruct and Ariados's Silk Trap act as plain Protects in the engine. Speed control: Electrode's Thunder Wave and Light Screen, Murkrow's Prankster Thunder Wave, Seviper's Glare, and Sharpedo's Speed Boost after a Protect. Dugtrio's Arena Trap holds the player's grounded Pokemon in while it stands (question 1).

**Why these four.** Nidoking could not stay softened: Oxide's has Mold Breaker or Sheer Force and no Poison Point, and the AI's own routine knows Mold Breaker carries Earthquake through Levitate. Dugtrio is Giovanni's, the fastest quake in Oxide's villain pool, and folds to one good hit. Seviper and Mightyena are fast or frail Earthquake and Bulldoze users from the classic teams, Mightyena with Ian's Obstruct. For Tyche's fifth no classic villain Pokemon is fast, frail and immune to Ground without repeating a line (question 2), so Ariados brings Silk Trap and Toxic Spikes instead.

### The cheap checks

The answers are goal 3's three boxes as in stage 1 (Maylene's reading, `plgoal3 --box maylene <seed> --screen`, seeds 1 to 3), raised to the honour cap of 41: Hardy, IVs of 15, first ability, no item. Damage is the scorer's calculator, lowest roll to highest as a share of HP, spread moves at three quarters. The partner is the six below at its own levels.

Speeds against the boxes' tiers: Dugtrio (127) and Electrode (126) outspeed everything. Haunter (107) ties Lopunny and box 3's Salazzle and sits under the player's Crobat (117). Seviper (106) is over Staraptor (97) and Delphox (96). Sharpedo starts at 93, a tie with Tentacruel and Alolan Ninetales, and passes everything after one Speed Boost. Golbat and Murkrow (89 and 88) sit over Heracross (80); Ariados and Mightyena (71) over Breloom (68); Weezing (58) over Granbull and Togetic.

| The officers' best hit | Damage |
|---|---|
| Seviper's Poison Fang on Togetic, Breloom, Alolan Ninetales | 125 to 149, 126 to 149, 111 to 134 |
| Haunter's Sludge Bomb on Togetic, Granbull, Breloom | 106 to 125, 131 to 157, 160 to 192 |
| Dugtrio's Earthquake on Tentacruel, Delphox | 105 to 125, 100 to 119 |
| Dugtrio's Earthquake on the partner's Pachirisu, Infernape | 122 to 144, 89 to 105 |
| Sharpedo's Waterfall on Delphox | 134 to 159 |
| Electrode's Thunderbolt on Staraptor, Crobat | 105 to 124, 71 to 86 |
| Mightyena's Throat Chop on Delphox | 88 to 107 |
| Golbat's Poison Fang on Togetic | 82 to 100 |

| The player's and partner's best hit | Damage |
|---|---|
| on Dugtrio: Alolan Ninetales's Triple Axel, Breloom's Bullet Seed, Tentacruel's Scald | 183 to 217, 163 to 196, 104 to 124 |
| on Dugtrio: the partner's Empoleon, Torterra, Scyther | 222 to 263, 293 to 348, 91 to 108 |
| on Sharpedo: Heracross's Close Combat, Granbull's Spirit Break | 215 to 256, 132 to 158 |
| on Seviper: Delphox's Psyshock, the partner's Gastrodon's Earth Power | 112 to 132, 107 to 127 |
| on Haunter: Delphox's Psyshock, Dusclops's Shadow Punch, the partner's Umbreon's Foul Play | 104 to 125, 102 to 120, 66 to 80 |
| on Murkrow: Granbull's Spirit Break, Alolan Ninetales's Triple Axel, the partner's Scyther's Wing Attack | 146 to 174, 183 to 221, 93 to 109 |
| on Golbat: Alolan Ninetales's Triple Axel, Delphox's Psyshock | 70 to 87, 54 to 64 |
| on Weezing: Delphox's Psyshock, the best of the rest (Tentacruel's Psybeam) | 58 to 68, 37 to 44 |

The read: Hermes's side now hits as hard as shape A did and dies faster. Seviper and Haunter one-shot Togetic and Breloom, and Dugtrio's first Earthquake can take one of the player's Pokemon and the partner's Pachirisu at once before it falls to nearly any hit. Tyche's Golbat and Weezing remain the slow part of the fight. Against the officer band (close to 100 percent won, deaths not trivial), I expect the fight to be won nearly always with a faint or two, most of them on the first turns, when Dugtrio, Electrode and Seviper move first. That is judgement from these checks; nothing reads the double.

### The partner's changes

| Slot | Member | Level | Ability | Item | Nature | Moves | Speed |
|---|---|---|---|---|---|---|---|
| 2 | Scyther | 40 | Technician | Eviolite | Adamant | Wing Attack, Pursuit, Knock Off, Brick Break | 101 |
| 3 | Lopunny | 39 | Scrappy | Lum Berry | Jolly | Fake Out, Jump Kick, Ice Punch, Dizzy Punch | 107 |

Scyther keeps Ian's Route 207 set but for Steel Wing, which became Knock Off for Tyche's Ghost and Dark members (68 to 80 on Haunter). Umbreon still leads; the rest of the six is as in stage 1.

### The egg lists

Each first stage takes the move on its egg list, in its file's style, with an entry in `learnrewrite.IAN_EGG_MOVES`; none of these species has a hand-set line in `learnsets_by_hand.txt`.

| First stage | Move | For |
|---|---|---|
| Poochyena | Obstruct | Hermes's Mightyena (Ian's approval) |
| Spinarak | Silk Trap | Tyche's Ariados (Ian's approval) |
| Zubat, Murkrow, Gastly | Protect | Tyche's Golbat, Murkrow, Haunter |
| Seviper, Carvanha, Diglett | Protect | Hermes's Seviper, Sharpedo, Dugtrio |

Protect was a TM before the TM pass and so already legal for these trainers; it goes on the egg lists so the OxiDex's list agrees, as the level climb's egg-list commit of today did. Koffing's line is left out: it is one of the learnset generator's five held-out lines, which its source may not name (`test_learnrewrite`), so Weezing's Protect stays legal through the pre-TM-pass TM alone and the OxiDex's list flags it. Spiky Shield on Cacturne and Burning Bulwark on Camerupt are not added, since neither species is in the ten.

### The text

| Where | Old | New |
|---|---|---|
| Veilstone, messages 11, 12, 14 and 16 | "Grunt 1: ..." | "Tyche: ..." |
| Veilstone, messages 13, 15 and 18 | "Grunt 2: ..." | "Hermes: ..." |
| Veilstone, message 18 | "And run like the grunts we are." | "And make ourselves scarce." |
| Spear Pillar, Tyche's defeat line | "The toughest of all the grunts!" / "That was me..." | "The toughest of all the officers!" / "That was me..." |

Every new line is shorter than the longest line already in its box ("I should have kept my head down and", 35 characters, in the same kind of message). The message ids do not move, so no script changes. The Veilstone bank is registered in the base ROM importer's `TEXT_BANKS_SKIPPED` and Tyche's defeat message in `trainers_diverged.json`, so neither import carries the old lines back.

### The five-minute check

- The lint and the packer pass on all ten changed teams (the team builder's save runs both, and a pack of the whole folder passes).
- Legality: the Kaizo study's checker with the pre-TM-pass lists finds nothing off in the eight Veilstone files, and the OxiDex's own list (`learnsets.oxide_list`) finds only Weezing's Protect off once the egg lists above are in; that Protect is legal through the pre-TM-pass TM.
- No item or nature repeats within any of the eight files. (The Spear Pillar files set no natures, as before this branch.)
- Not run: the AI-picks probe, and any reading. The simulator, its AI probe and goal 3 read single battles only.
- To check in the game: the fight is on `ingame-checklist.md`, section 4.

### Goal 3's count

Ian's ruling of 2026-10-29 ("Let's just fix this now", approving the scorer data change): both fights are story fights in `tools/oxide/balance/fights.json`, marked `"tag": true` as Somnu and Moira's double is. Tyche and Hermes 1 is in Wake's split with the six Veilstone partner files as its partners; Tyche and Hermes 2 is in Galactic's split with no partner, since the Spear Pillar script starts that double with both opponents and no partner flag. Each reference hack seats neither (their slots hold vanilla's plain grunts), `test_b1` takes "Tyche" or "Hermes" as the fights' names and holds Tyche and Hermes 1's ace at the honour cap of 41, and Spear Pillar's levels are left out of that check, as drafted. Nothing outside the repo changed.

| Suite | Result |
|---|---|
| `test_plgoal3` | 72 of 72; goal 3 reads 80 single battles, 39 bosses and 41 Ace Trainers |
| `test_b1` | 47 of 47; 35 story fights resolve in Oxide, 28 in each Platinum hack; 31 boss aces keep the boss-level ruling |
| `test_b3` | 12 of 12 |
| `test_trainers` | 44 of 44 |
| `test_b1e`, `test_difficulty`, `test_linetester` | 8 of 8, 3 of 3, 11 of 11 |
