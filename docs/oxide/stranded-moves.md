# Stranded moves

This answers Ian's request of 2026-10-14. He asked for the working moves among those `move-access.md` found no player can learn, with the lines or trainers each would fit on the learnset rules' ladder, for him to pick from before any list changes. Nothing in `res/` changes here. It was read from origin/oxide at 59b0dae66d, after the form-learnset and Wormadam changes and the first two batches of simulator fixes landed.

## Summary

**Outcome.** The request covers 88 moves: the audit's 53 ordinary moves that no species learns, and the 35 that only unobtainable species learn. The day's changes gave none of them a learner, so all 88 are still stranded. 82 run in Oxide's engine as written. This page proposes player homes for 48 of them, about a hundred homes in all. It keeps 6 for trainers only and recommends leaving the other 28 unused. Each home gives a line, a level, where the move stands on its type's ladder, and what it changes for that line.

**The ten homes that matter most.** Each fills a gap the line has in the main run, with a move that fits it. Five of them (Gallade, Floatzel, Jynx, Kleavor, Leafeon) sit a rung or more over the generator's ladder or ceiling; their tables say by how much, and why the gap is worth it.

| Home | Move, level | Why |
|---|---|---|
| Gallade | Sacred Sword, 46 | Gallade has no Fighting move at all before Close Combat at 53. Sacred Sword is its own move in Legends Z-A |
| Floatzel | Triple Dive, 54 | Its only physical Water move is Aqua Jet until Waterfall's HM in Galactic's split |
| Jynx | Freezing Glare, 47 | A wild Jynx (met at 35 or later) never learns Psychic. Its own list stops at Psybeam |
| Kleavor | Mighty Cleave, 48 | Its Rock moves stop at Rock Blast, and its Stone Edge TM is 80% accurate. An accurate 95 is also a slicing move for its Sharpness |
| Magnemite line | Rising Voltage, 28 | Met at 29 in Byron's split, the catch knows no special Electric move and learns none until Discharge at 38 |
| Pelipper | Aeroblast, 55 | A special Pokemon whose Flying moves are all physical. This is the accurate alternative to Hurricane, which R37 bars |
| Minun | Electro Ball, 28 | It has no special Electric move before Thunderbolt at 38; Spark at 15 is physical |
| Palkia | Origin Pulse, 50 in place of Heal Block | Met at 70, it has no Water move beyond Water Pulse. The catch would know this one |
| Leafeon | Horn Leech, 47 | Its strongest physical Grass move is Grassy Glide (28) until Leaf Blade at 71 |
| Snorunt line | Frost Breath, 34 | Its special Ice moves jump from Icy Wind at 13 to Ice Beam at 37 to 51 |

**Best left unused (28).** Nine are settled already: the multi-hit cut, Psywave's cut, the named dead weight, terrain, and Struggle, which needs no learner. Bone Club is barred by R37 and is weak anyway. Eight are copies or worse versions of moves the lines already have: Supercell Slam beside Oxide's ThunderPunch, Dragon Hammer beside Oxide's Dragon Rush, Ice Hammer, False Surrender, Land's Wrath, Branch Poke, Autotomize and Tera Blast. Seven are status moves Ian's tiers rate niche or bad: Work Up, Laser Focus, Sharpen, Power Shift, Wonder Room, Spotlight and Conversion 2. The last three are weak or ruled out: Beat Up, Pay Day and Cut. The last table gives each one's reason.

**What Ian picks.**
1. Strike or keep homes in the tables below. Every player pick is a level-up entry and needs no new mechanic.
2. Hurricane: grant Pelipper an exception to R37 at 58, as the rewrite kept Head Smash, or take Aeroblast instead.
3. Upper Hand and Burning Jealousy: their homes wait for in-game checks 81 and 83.
4. Trainer homes: each one changes a boss's team, so each is a question about that fight, asked once Ian wants it.

**Difficulty.** The earliest homes sit in Gardenia's split. They go to lines that are not counterpieces to Roark or Gardenia in `boss-shapes.md`, so none is material for those two fights. A trainer home is material for its boss.

**Next steps and time.**
- Ian's read of the summary and the tables he cares about: about half an hour.
- Placing his picks: one session, about an hour of data work, then a rebuild and the gate.
- Each trainer home Ian takes: that boss's team change, then its reading, at 1 to 2 hours of machine time a boss.

## How the homes were chosen

Obtainability is `pool.obtainable()`, 468 species, as the audit used. The ladder is the learnset generator's (`learnrewrite.py`). A line meets a type at its split's ceiling less 20: 40 in Roark's split, 55 in Gardenia's, 60 in Fantina's, 70 in Maylene's and Wake's, 80 in Byron's and Candice's, and higher after. Each new move may stand one or two rungs above the best of its type the line already has, one rung for a power-flagged line. A pivot stands at least at the middle of its ladder. "Climbs" in the tables means the generator's own check passes. "A rung over" or "jumps" means it does not, and why. The generator reads a multi-hit move by its power a hit and an always-critical move by its listed power, so the tables also say what such a move really lands.

Later games' level-up lists (hg-engine's per-game files, Black and White to Legends Z-A) were the inspiration for which lines a move fits. Where they gave no obtainable home, the line's type, ability and role decided. Levels were chosen free on each list, since no two moves share a level. A move a late, low-level catch learns before its catch level is judged at the split where the player meets it: the Magnemite line is met only at 29, in Byron's split. A legendary met at a high level is judged by the four moves it knows at capture.

Seven legendaries the main run never meets were set aside. Regice, Regirock, Registeel, Darkrai and Shaymin come only after the League, and Moltres and Zapdos are post-game roamers. Their lists matter only for the post-game.

Oxide's numbers are used throughout. Several of these moves came from Hardlove's data with values that differ from the later games: Fire Lash at 90, Dragon Hammer at 100, Triple Dive at 35 a hit, Misty Explosion at 200, and several accuracies raised to 100.

## Engine and simulator notes

82 of the 88 run in the engine as written. Six do not:

| Move | Why it is out |
|---|---|
| Snap Trap | a plain 35-power hit; the binding is missing |
| Steel Beam | a plain 140-power hit; the user's loss of half its HP is missing |
| Synchronoise | a plain hit; the rule that it hits only a foe sharing a type is missing |
| Eerie Spell | a plain 80-power sound move; its record promises a 3 PP drain that nothing in the engine does (the audit's column says it runs) |
| Burning Bulwark | a plain Protect: the engine punishes contact only for Spiky Shield and Baneful Bunker (subscript_missed), so its burn never happens (the audit's column says it runs) |
| Teleport | flees a wild battle and fails against a trainer |

Upper Hand and Burning Jealousy were broken when the balance rules were written. The move reworks made both work on 2026-10-07, but their in-game checks (81 and 83 in `ingame-checklist.md`) still wait on Ian, and the generator holds both off player lists until then. Their homes below are for after those checks.

The generator reads Mighty Cleave as not working. Its effect script is a plain hit, which is right, since the Protect bypass comes from its missing Protect flag. The stub check (`pokedex.stub_effects`) takes any donor effect whose script copies the plain hit's for a placeholder unless it is listed as done in C, and IGNORE_PROTECT is not listed. Until it is, Mighty Cleave can only be placed by hand.

The simulator gaps these moves meet are listed with each move. Several are fixed since 2026-10-14: the two-hit moves land hit by hit, Mighty Cleave passes Protect, Psychic Fangs breaks a screen before the readings halve it, and Doom Desire strikes two turns later. Four gaps were found while reading for this page and are approved and being fixed in batch 2. `simulator-gaps.md` did not list them, because each move's effect is a plain hit and the engine does its work in code keyed on the move:
- Sacred Sword and Chip Away (and Darkest Lariat, open to the player already) ignore the target's stat stages in the engine, but not in the readings.
- Power Trip (and Stored Power) read at 20 whatever the user's stages.
- Hard Press reads at full power whatever the target's HP.
- Electro Ball keeps the opening Speeds for the whole fight.

## The moves with homes

Each table lists the proposed homes. "Ladder" is the generator's reading at that level against the line's best move of the type before it. "For" says whether the move suits the player or a trainer better; the late and Galactic teams may carry anything.

### Fire

#### Fiery Dance
Special, 80 power, 100%, 10 PP; raises the user's Sp. Atk a stage half the time. Volcarona's move in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Volcarona | 63, Galactic | climbs from Flamethrower (60) | A second strong Fire move beside Flamethrower. The boost makes it the better move over a long fight. Volcarona evolves at 59, so nothing comes early | player |
| Litwick, Lampent, Chandelure | 48, Byron | climbs from Mystical Fire (45 or 46) | Fills the long gap between Mystical Fire and Heat Wave (62 to 72); the line has no Flamethrower. Chandelure (Sp. Atk 145) gets an 80 that snowballs from Byron's split on | player |

#### Fire Lash
Physical, 90 in Oxide, 100%, 15 PP; lowers the target's Defense a stage every hit. Salazzle's in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Ponyta, Rapidash | 44, Wake | climbs from Flame Wheel | The line's only physical Fire between Flame Wheel (15) and Flare Blitz (46 or 56). Once its first hit lowers Defense, the next lands harder than Flare Blitz, with no recoil. Rapidash already has Blaze Kick at 40 | player |
| Flareon | 50, Byron | climbs from Fire Punch | A sidegrade to Fire Punch (47); worth it only for the Defense drop. Low value | player |
| Salazzle | | | Its later-game home, but Salazzle is special (Sp. Atk 111, Attack 64), so a physical move is off its better stat. A trainer's Salazzle in a double battle could soften a target for a physical partner | trainer |

#### Burning Jealousy
Special, 70, 100%, 5 PP; burns every target whose stats rose that turn. Works in the engine since 2026-10-07; check 83 waits on Ian. A TM for most Fire and Dark lines in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Jupiter's Spiritomb (Spear Pillar, Stark Mountain), or Flint's Houndoom | | | It punishes the player's setup turn, which the player plans around. Material for that fight | trainer |
| Mismagius | 50, Byron | by hand | Fire coverage for a Ghost type, whose Ghost moves Steel resists on Oxide's chart. Its first Fire move is Mystical Fire at 63. The burn lands only on a turn the foe set up | player |

#### Heat Crash
Physical; power from the user's weight against the target's, 120 at five times down to 40. A TM for heavy lines in the later games. Gap: the calculator gives it no row, so the readings never let it hurt anything (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Snorlax | 58, HQ | by hand | At 460 kg it hits most foes for 120, Fire coverage against the Steel types that wall its Normal moves. It is also the real late move its list lacks: after Body Press at 51 it learns only Charm | player |
| Turtonator | 50, Byron | by hand | Its only physical Fire move. At 212 kg it hits most foes for 80 to 120, which suits its Shell Smash at 45 | player |
| Saturn's slow giants (Wailord, Rhyperior) | | | A weight move fits the HQ fight's theme of slow giants in permanent Trick Room. Material for Saturn 2 | trainer |

### Electric

#### Electro Ball
Special; power from the user's Speed against the target's: 150 at four times, 120 at three, 80 at two, 60 at even, 40 below. Most Electric lines learn it by level in the later games. Gap: the readings keep the opening Speeds (batch 2).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Pachirisu | 23, Gardenia | by hand: 60 to 80 against most of the split's foes | A weak line's step between Electroweb (4) and Discharge (29). Adaptability doubles its type bonus, so against slow foes it hits hard | player |
| Minun | 28, Fantina | by hand | Nothing special between Spark (15, physical, off its better stat) and Thunderbolt at 38. At Speed 105 it reaches 80 against most foes; flagged by Speed, so after Gardenia's split | player |
| Emolga | 30, Fantina | by hand | Between Shock Wave (21) and Volt Switch (40). Flagged by Speed, hence 30 rather than the later games' 26 | player |

Jolteon was set aside: at Speed 130 it would reach 120 to 150 against most foes.

#### Parabolic Charge
Special, 65, 100%, 20 PP, hits every adjacent Pokemon; heals half the damage dealt. Rotom's in Legends Z-A. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Rotom (its five forms copy the list) | 38, Maylene | climbs from Shock Wave | A sustain move between Shock Wave (22) and Discharge (50) for a bulky, flagged line | player |
| Chinchou | 25, Gardenia | climbs from Spark | A drain for the 125-HP Lanturn line between Spark (20) and Discharge (34) | player |
| Plusle | 31, Fantina | climbs from Spark | Oxide's Plusle is a defensive Pokemon (Defense and Sp. Def 95, Sp. Atk 50); healing suits it better than damage. Low power | player |

#### Rising Voltage
Special, 70, 100%, 20 PP; a plain hit, since its terrain boost cannot happen. A TM in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Magnemite, Magneton, Magnezone | 28 | by catch: the line is met only at 29, in Byron's split | The catch at 29 would know a special Electric move. Today it has only Spark (physical, off Sp. Atk 95) until Discharge at 38. The generator reads a jump only because level 28 falls in Fantina's split, which this line never sees | player |
| Vikavolt | 38, Maylene | climbs | Vikavolt can come at 20, since the Magnetic Field opens in Gardenia's split. Its own list then has no special Electric move until Discharge at 48; its level-1 Thunderbolt is relearner only | player |

### Ice

#### Frost Breath
Special, 60, 100% in Oxide, 10 PP; always a critical hit, at 1.5 times, ignoring the target's raised Sp. Def and screens. It lands like a 90-power move. The Snorunt line learns it at 30 in Scarlet and Violet. Gap: the readings apply stages and screens to it and can roll a second critical hit (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Snorunt, Glalie | 34, Maylene | reads 60, one rung over Icy Wind; lands like 90 | Fills the special Ice gap between Icy Wind (13) and Ice Beam (46 on Snorunt, 37 on Glalie). Placed after Fantina's split, not at the later games' 30, because it lands like Ice Beam | player |
| Froslass | 40, Wake | the same | Bridges Icy Wind (13) and Ice Beam (51) on a flagged line | player |

#### Glaciate
Special, 65, 100% in Oxide, 10 PP, hits both foes; always lowers Speed. Kyurem's. Ian rates sure speed control as incredible. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Spheal, Sealeo, Walrein | 36 | climbs from Aurora Beam | The line has no Icy Wind. A sure Speed drop for a slow tank, between Aurora Beam (25) and Ice Beam (43 to 52). Speed control is strong (Ian, 2026-10-13), so it comes after Fantina's split | player |
| Articuno | 54, Candice | climbs from Ice Beam | Met at 50 from Acuity Cavern's draw, Articuno learns no move newer than Generation 4; this would be its first. Take this or Freezing Glare, not both | player |
| Candice's Froslass or Articuno | | | Speed control against the player's answers to her. Material for Candice | trainer |

Regice would take it at 45, between Icy Wind at 9 and Ice Beam at 73, but only for the post-game.

### Fighting

#### Power-Up Punch
Physical, 40, 100%, 20 PP; raises the user's Attack a stage every hit. A punch, so Iron Fist raises it. The Machop line, Lucario and Lopunny learn it in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Riolu | 9 | climbs (its first Fighting move) | The Iron Island egg hatches at 1 in Byron's split, so this comes while it is raised, with no early boss in reach | player |
| Machop | 18, Gardenia | climbs | A setup-on-hit beside Low Sweep (17). Kept after Roark's cap on purpose: at the later games' 12 it would change Machop's Roark fight, where Fighting beats Rock | player |
| Pawmo | 20, Gardenia | climbs | Pawmo's only Fighting move is Arm Thrust (25) until Pawmot's Close Combat at 49. With Iron Fist, its third slot, it hits for 48 | player |

#### Upper Hand
Physical, 65, 100%, 15 PP, priority +3; works only when the target chose a priority move, and flinches it. Works in the engine since 2026-10-07; check 81 waits on Ian. A TM for most Fighting lines in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Mienfoo, Mienshao | 41, 42, Wake | by hand | An answer to trainers' priority (Fake Out, Sucker Punch, Aqua Jet, Bullet Punch, ExtremeSpeed), which Ian counts as part of planning. It adds no raw power | player |
| Hawlucha | 30, Fantina | by hand | The same answer on a fast wrestler | player |

#### Circle Throw
Physical, 60, 95% in Oxide, 10 PP, priority -6; drags the target out for a random member of its party. Poliwrath and the Clobbopus line learn it in Legends Z-A. Gap: the readings never drag the target out (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Poliwrath | 38, Maylene | climbs | Ends a boss's setup sweeper's run, on a bulky Water and Fighting line between Wake-Up Slap (35) and Brick Break (43) | player |
| Clobbopus, Grapploct | 30, Fantina | climbs | The octopus's throw, with the same use against setup | player |

#### Storm Throw
Physical, 60, 100%, 10 PP; always a critical hit, so it lands like 90 and ignores the target's raised Defense and Reflect. Throh's and Pinsir's; a TM or tutor move for the Mankey line in the later games. Gap: as Frost Breath's (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Primeape | 42, Wake | reads 60, climbs; lands like 90 | Primeape's Fighting moves run from Karate Chop (13) to Close Combat (59). This fills the gap, after Maylene's split | player |
| Hariyama | 46, Byron | the same | A sumo throw between Wake-Up Slap (42) and Close Combat (52) | player |

Not on a Technician holder (Breloom, Scizor, Grapploct's third slot): 60 is Technician's limit, so it would land like 135.

#### Thunderous Kick
Physical, 90, 100%, 10 PP; lowers the target's Defense a stage every hit. Galarian Zapdos's. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Blaziken | 53, Byron | climbs from Combusken's Sky Uppercut (50); jumps from Double Kick for a Blaziken evolved at 36 | Blaziken's own list has only Double Kick (16) for Fighting until Sky Uppercut at 59. A kick for the kicking line, which makes a strong line stronger at Byron's end | player |
| Pawmot | 46, Byron | jumps: Arm Thrust is its only Fighting move before | Electric and Fighting in one name. Pawmot has no real Fighting move until Close Combat at 49, which is already the bigger jump. Pick it only if that gap should close before 49 | player |
| Lopunny | 56, Candice | climbs from Jump Kick | Jump Kick (23) without the crash. Little new | player |

#### Sacred Sword
Physical, 90, 100%, 15 PP; ignores the target's stat stages and evasion. A slicing move. Gallade's in Legends Z-A. Gap: the readings let the target's stages count (batch 2).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Gallade | 46, Byron | jumps: Gallade has no Fighting move before | Gallade's first Fighting move, seven levels before Close Combat (53), which is the bigger jump. Gallade's Byron split gets stronger, and that is the gap it fills | player |
| Absol | 56, Candice | climbs | Fighting coverage before Superpower (69), on a line whose horn is a blade | player |

#### Victory Dance
Status, 1 PP in Oxide; raises Attack, Defense and Speed a stage. Hisuian Lilligant's. Ian rates a move that raises Speed and an attacking stat with Dragon Dance, so it comes no earlier than Maylene's split. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Poliwrath | 50, Byron | utility, allowed | Pairs with Body Press (45), which reads Defense. A planned setup for a bulky line with none before Belly Drum at 70 | player |
| Mienshao | 52, Byron | utility, allowed | A fast fighter with no setup move; it makes a flagged line a sweeper | player |
| Maylene's Medicham or Lucario | | | A setup threat. Material for Maylene | trainer |

### Psychic

#### Heart Stamp
Physical, 60, 100%, 25 PP; flinches 30% of the time. Smoochum, Jynx and Luvdisc learn it in the later games. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Meditite | 27, Fantina | climbs | Its first physical Psychic move; Confusion is special, off Pure Power. Pure Power makes it hit like 120, which is why it sits after Gardenia's split | player |
| Luvdisc | 20, Gardenia | climbs | Its later-game move, as coverage before it evolves at 30. Attack 30 keeps the damage small; the flinch is the point. Low value | player |

#### Psychic Fangs
Physical, 85, 100%, 10 PP; breaks Reflect and Light Screen. A TM for biting lines in the later games. Fixed: the readings no longer halve it through the screen it breaks.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Metang, Metagross | 42, Wake | climbs on Metang | A physical Psychic move before Zen Headbutt (52); its Psychic at 36 is special, off its better stat | player |
| Granbull | 54, Candice | climbs | Psychic coverage against the Poison types that resist Fairy, and a screen breaker against Byron's, Lucian's and Saturn's screens | player |
| Luxray | 58, HQ | climbs | Coverage against the Fighting types an Electric and Dark line fears, and a screen breaker | player |

#### Twin Beam
Special, 40 twice (80 in two hits), 100%, 10 PP. Girafarig's at 32 in Legends Z-A. Fixed: the readings land it hit by hit.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Girafarig | 34, Maylene | reads 40 a hit, climbs | Between Psybeam (19) and Psychic (37), its later-game home. Two hits break Sturdy and a Focus Sash. Flagged, so 34 rather than 32 | player |
| Lunatone | 35, Maylene | the same | Between Psybeam (23) and Psychic (45), for the twin-moon line | player |

Not on Mr. Mime: its third slot is Technician, under which 40 a hit lands like 120.

#### Mystical Power
Special, 70, 90%, 10 PP; raises the user's Sp. Atk a stage every hit. The lake trio's in Legends Arceus; the player can obtain none of them. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Chimecho | 36, Maylene | climbs from Psybeam | A weak, flagged line's mid-game Psychic between Psybeam (30) and Extrasensory (46) | player |
| Mime Jr., Mr. Mime | 33, Fantina | climbs | Between Psybeam (25) and Psychic (39) | player |
| Espeon | 50, Byron | climbs | Espeon's own Psychic moves run from Psybeam (36) to Psychic (64); this bridges them, one rung over Psybeam | player |
| Mars's Mesprit (Lake Verity), Saturn's Azelf and Uxie | | | Their own move. Material for Mars 2, Saturn 1 and Saturn 2 | trainer |

#### Take Heart
Status, 3 PP in Oxide; raises Sp. Atk and Sp. Def a stage and cures the user's status. Manaphy's at 76 in Scarlet and Violet. Gap: the readings leave the status (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Cresselia | 54, Candice | utility | Met at 50 from Acuity Cavern's draw, Cresselia has no Calm Mind; this one also cures a burn or poison. Strong on a bulky legendary | player |
| Manaphy | 72, League | utility | Its home game's move, as a late move. Manaphy already has Tail Glow at 1. Little change | player |

#### Freezing Glare
Special, 90, 100%, 10 PP; freezes 10% of the time. Galarian Articuno's. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Jynx | 47, Byron | climbs from Smoochum's Psychic; a wild Jynx jumps from Psybeam | Jynx's own list has only Psybeam (41) for its Psychic type. Smoochum's Psychic at 35 is lost when it evolves at 30, and a wild Jynx is met at 35 or later | player |
| Articuno | 60, HQ | climbs | Psychic coverage that nods to its Galarian form. Take this or Glaciate, not both | player |

#### Luster Purge
Special, 95, 100%, 5 PP; lowers the target's Sp. Def half the time. Latios's; a strict upgrade on Psychic. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Alakazam | 58, HQ | climbs | A late upgrade on Psychic (40) and its first real move after 53 | player |
| Starmie | 61, Galactic | jumps from Psybeam | Starmie's own Psychic moves never pass Psybeam (24). A middle rung first (Mystical Power at about 40) would make it a climb | player |

#### Mist Ball
Special, 95, 100%, 5 PP; lowers the target's Sp. Atk half the time. Latias's. Gap: the readings never lower Sp. Atk (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Gardevoir | 62, Galactic | climbs | A late upgrade on Psychic (33) | player |
| Lunatone | 59, HQ | climbs | Between Psychic (45) and Moonblast (62) | player |

#### Psycho Boost
Special, 140, 90%, 5 PP; lowers the user's Sp. Atk two stages. Deoxys's. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Lucian's Alakazam or Espeon | | | A late nuke that fits the Psychic Elite. Material for Lucian | trainer |
| Alakazam | 66, Volkner | climbs | A late nuke for a frail, fast line. Take this or Luster Purge | player |

### Dark

#### Jaw Lock
Physical, 80, 100%, 10 PP; traps both the user and the target. The Chewtle line's. Gap: the readings trap neither (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Mawile | 44, Wake | climbs from Crunch | The iconic jaw: Dark coverage beside Crunch (36) that keeps a foe from switching out, at the cost of Mawile staying in too | player |
| Mightyena | 46, Byron | climbs | The same on a hyena, beside Crunch (34) and Throat Chop (39) | player |

#### Power Trip
Physical, 20 power plus 20 for each of the user's raised stages, 100%, 10 PP. The Rookidee line's in Scarlet and Violet. Gap: the readings keep it at 20 (batch 2).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Corviknight | 47, Byron | by hand | Its home game's line. It pays off after the Bulk Up or Iron Defense TM in Volkner's split, and little before. Corvisquire has no setup to use it | player |
| Liepard | 29, Fantina | by hand | After Hone Claws (27) it is 60 at two raised stages | player |
| Vullaby, Mandibuzz | 38, Maylene | by hand | After Iron Defense (30) and Nasty Plot (35), 60 to 100 | player |

#### Fiery Wrath
Special, 90, 100%, 10 PP, hits both foes; flinches 20% of the time. Galarian Moltres's; a strict upgrade on Dark Pulse. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Houndoom | 56, Candice | climbs from Dark Pulse (50) | Its name fits; six levels after Dark Pulse on a flagged line | player |
| Spiritomb | 60, HQ | climbs from Dark Pulse (49) | An upgrade for the hundred and eight spirits | player |
| Cyrus's Houndoom at Galactic HQ, or Flint's | | | Material for that fight | trainer |

Darkrai's list has no special Dark move at all, but Darkrai comes only in the post-game.

### Dragon

#### Dragon Darts
Physical, 50 twice (100 in two hits), 100%, 10 PP. Dragapult's. Fixed: the readings land it hit by hit.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Flygon | 54, Candice | reads 50 a hit, climbs | Between Dragon Claw (45) and Dragon Rush (56); two hits break Sturdy and Sashes. Flagged, so Candice's split | player |
| A Dragon Tamer's Flygon or Kingdra | | | Fits the class | trainer |

#### Core Enforcer
Special, 100, 100%, 10 PP, hits both foes; suppresses the ability of a target that already moved. Zygarde's. Gap: the readings never suppress the ability (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Goodra | 64, Galactic | climbs | A late Dragon move between Dragon Pulse (58) and Draco Meteor (70), without Draco Meteor's drop | player |
| Kingdra | 62, Galactic | climbs | Between Dragon Pulse (57) and Draco Meteor (67) | player |
| Cyrus 3's Salamence | | | Ability suppression as a last-boss tool. Material for Cyrus 3 | trainer |

### Grass

#### Leaf Tornado
Special, 65, 100% in Oxide, 10 PP; lowers the target's accuracy 30% of the time. The Snivy line, Tropius, Carnivine and Shiftry learn it in the later games. No simulator gap. The generator gives an accuracy drop no weight, since it makes fights random.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Shiftry | on evolving | climbs | Shiftry's own list, a Leaf Stone evolution's, has no special Grass move before Leaf Storm at 49. As in Legends Z-A it would be an evolution move, which Ian approves one by one | player |
| Carnivine | 28, Fantina | climbs from Vine Whip | Between Vine Whip (11) and Petal Blizzard (47) | player |
| Tropius | 26, Gardenia | climbs | Its Brilliant Diamond level, between Razor Leaf (11) and Magical Leaf (31) | player |

#### Horn Leech
Physical, 75, 100%, 10 PP; heals half the damage dealt. Sawsbuck's and Gogoat's; none of its learners is obtainable. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Leafeon | 47, Byron | a rung over Grassy Glide, for a flagged line | Leafeon's strongest physical Grass move is Grassy Glide (28) until Leaf Blade at 71. The leaf on its head serves as the horn | player |
| Torterra | 47, Byron | two rungs over Razor Leaf for a flagged line; its Wood Hammer at 1 is relearner only | A tank's drain between Razor Leaf (13) and Seed Bomb (59) | player |

### Ground

#### Thousand Arrows
Physical, 90, 100%, 10 PP, hits both foes; reaches Flying and Levitate Pokemon and grounds them. Zygarde's. Gap: the readings never ground the target (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Bertha's Hippowdon or Rhyperior | | | Takes away the player's Flying and Levitate answers to a Ground team. Material for Bertha | trainer |
| Hippowdon | 61, Galactic | climbs | A late move for the player's Hippowdon that hits the fliers Earthquake cannot | player |

#### Thousand Waves
Physical, 90, 100%, 10 PP, hits both foes; traps the target. Zygarde's. Gap: the readings never trap (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Quagsire | 45, Byron | climbs | With Unaware, trapping a boss's setup sweeper is a planned counter | player |
| Gastrodon | 52, Byron | climbs | A trap beside Earth Power (43) | player |
| Wake's Quagsire | | | Trapping is allowed but rare on trainers. Material for Wake | trainer |

### Rock

#### Mighty Cleave
Physical, 95, 100%, 5 PP; goes through Protect. A slicing move. Fixed: the readings let it through Protect. The generator cannot place it (see the engine notes), so these are by hand.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Kleavor | 48, Byron | by hand: a jump from Rock Blast | Kleavor's Rock moves stop at Rock Blast (32) until Accelerock at 55. With Sharpness, its third slot by the Ability Patch, it lands like 142. Rock Slide first would make it a climb | player |
| Sudowoodo | 44, Wake | by hand: one rung over Rock Slide | Its Rock moves stop at Rock Slide (33, 90%). This is an accurate 95 | player |
| Tyranitar | 61, Galactic | by hand: one rung over Rock Slide | Tyranitar's own list has only Rock Slide (14) and Rock Tomb. A late accurate Rock move in place of Stone Edge's 80% | player |

#### Diamond Storm
Physical, 100, 100% in Oxide, 5 PP, hits both foes; raises the user's Defense two stages half the time. Diancie's. Gap: the readings never raise Defense (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Carbink | 56, Candice | climbs | Diancie's own line. The hit is weak (Attack 50), but the Defense it stacks feeds Body Press at 61 | player |
| Garganacl | 52, Byron | climbs | Salt crystals for diamonds: a strong accurate Rock move beside Rock Slide (34), and its Defense rises make Body Press (64) better. Strong on an already sturdy line | player |

### Steel

#### Hard Press
Physical; power 100 times the target's remaining share of its HP. A TM for heavy lines in Scarlet and Violet. Gap: the readings keep it at full power (batch 2).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Steelix | 44, Wake | by hand | A heavy opener between Iron Head (41) and Crunch (46): 100 against a foe at full HP | player |
| Bastiodon | 44, Wake | by hand | A Steel move before Iron Head (52) for a wall with Attack 95 | player |

#### Tachyon Cutter
Special, 50 twice (100 in two hits), never misses, 10 PP. A slicing move. Iron Crown's. Fixed: the readings land it hit by hit.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Magnemite, Magneton, Magnezone | 35 | reads 50 a hit, climbs | The line's first special Steel move, eight levels before Mirror Shot (43 to 46). The line is met at 29 in Byron's split | player |
| Dialga | 50, in place of Heal Block | by capture | Met at 70 at the Spear Pillar, Dialga knows its last four moves by 70. This gives it a special Steel move at capture, in place of a Heal Block it does not need | player |

#### Shift Gear
Status, 1 PP in Oxide; raises Speed two stages and Attack one. The Klink line's. Rated with Dragon Dance. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Corviknight | 57, HQ | utility, allowed | A mechanical bird with no setup move becomes a fast sweeper late. A large change for an unflagged line | player |
| Metagross | 60, HQ | utility, allowed | A better Agility (44) for a flagged line, late | player |
| Byron's Metagross | | | A setup threat. Material for Byron | trainer |

#### Doom Desire
Special, 140, 100%, 5 PP; strikes two turns later. Jirachi's. Fixed: the readings land it two turns later. The generator never adds a delayed move, so this is by hand.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Bronzong | 66, Volkner | climbs | The Steel twin of its Future Sight (43), for a slow wall whose Steel moves are Mirror Shot (45) and Iron Head (52) | player |
| Officer Moira's team, or Byron's Bronzong | | | Moira's theme is Future Sight on every member that can learn it; this is its Steel version. Material for that fight | trainer |

### Water

#### Triple Dive
Physical, 35 three times (105 in three hits), 95%, 10 PP. Wugtrio's. Gap: the readings land its three hits as one, so Sturdy, a Focus Sash and a resist berry hold all three (open; the hit-by-hit fix left this effect out).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Floatzel | 54, Candice | reads 35 a hit; lands 105, five over the flagged ceiling until Galactic's split | Floatzel's only physical Water move is Aqua Jet (21) until Waterfall's HM. This is its real one | player |
| Sharpedo | 54, Candice | the same | The same gap: Aqua Jet only | player |

#### Origin Pulse
Special, 110, 100% in Oxide, 10 PP, hits both foes. Kyogre's: a Hydro Pump that never misses. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Palkia | 50, in place of Heal Block | by capture | Met at 70 at the Spear Pillar knowing Spacial Rend, Heal Block, Earth Power and Slash. This swaps Heal Block for its only strong Water move; its list has Water Pulse at 10. The Origin Forme ties it to the name | player |
| Suicune | 75, League | climbs from Surf (71) | A late best move. Suicune's real gap is its Water moves from BubbleBeam (8) to Scald (66), which Scald placed earlier would fix better | player |
| Cyrus's Suicune at Galactic HQ | | | Material for Cyrus 2 | trainer |

#### Fillet Away
Status, 1 PP in Oxide; raises Attack, Sp. Atk and Speed two stages for half the user's maximum HP. Veluza's. Rated with Dragon Dance. Gap: nothing happens in the readings (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Lumineon | 45, Byron | utility, allowed | A weak, fast fish with both attacking stats near 80. One turn and half its HP make it a sweeper; the cost is real in a permadeath run | player |
| Seaking | 46, Byron | utility, allowed | A weak line with Liquidation (52) and Megahorn (63) to use the boost | player |

### Normal

#### Chip Away
Physical, 70, 100%, 20 PP; ignores the target's stat stages. Many lines learn it in Generations 5 to 7. Gap: the readings let the target's stages count (batch 2).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Croconaw, Feraligatr | 32, 35 | climbs | Near its Ultra Sun and Moon levels (33 and 37), beside Slash and Crunch: an answer to a foe's Defense setup | player |
| Lickitung, Lickilicky | 37, Maylene | climbs | Its Ultra Sun and Moon level: an anti-setup tool for a weak Normal line, between Slam (29) and Power Whip (49) | player |

### Flying

#### Aeroblast
Special, 100, 95%, 5 PP; a high critical-hit ratio. Lugia's. It is the accurate strong special Flying move the player lacks: Hurricane is 80% and Air Slash 75 power. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Pelipper | 55, Candice | climbs | A Pelipper evolved at 25 never learns Air Slash, and its Flying moves (Wing Attack, Fly, Acrobatics) are physical on a special Pokemon. This answer passes R37; Hurricane, its later-game move, does not | player |
| Noctowl | 63, Galactic | climbs from Air Slash | A late upgrade for a weak line on Air Slash (32) | player |
| Cynthia's Togekiss | | | Material for Cynthia | trainer |

#### Oblivion Wing
Special, 80, 100%, 10 PP; heals three quarters of the damage dealt. Yveltal's. Gap: the readings heal off a Liquid Ooze target, where the engine hurts the user (open).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Togekiss | 61, Galactic | climbs from Air Slash, or two rungs from Togetic's Air Cutter | Togekiss's own list has nothing real after Shadow Ball (57); this is its late move, with healing | player |
| Honchkrow | 50, Byron | climbs | Honchkrow's own list has Wing Attack only at 1, which an evolved Honchkrow never learns. A dark bird's drain | player |
| Drifblim | 46, Byron | two rungs over Gust | Its Flying moves run from Gust (11) to Air Slash (64). With 150 HP the drain heals a lot. Air Cutter between would make it a climb | player |

### Poison

#### Coil
Status, 3 PP in Oxide; raises Attack, Defense and accuracy a stage. Furret learns it at 1 in Legends Z-A; the Snivy line and Milotic learn it too. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Furret | 25, Gardenia | utility, allowed | A weak line's niche: Adaptability doubles its type bonus, and Coil makes Slam (28) and Body Slam (34) hit harder | player |
| Onix, Steelix | 36, Maylene | utility, allowed | The rock snake: a Curse (Steelix, 38) without the Speed loss, with accuracy for the Iron Tail TM (75%). Take this or keep Curse | player |

### Fairy

#### Nature's Madness
Special; halves the target's HP, 100% in Oxide, 10 PP. The Tapus'. The readings handle it by its effect. No simulator gap.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Floette, Florges | 44, 45 | by hand | A defensive Fairy's answer to bulky aces, beside Dazzling Gleam and Moonblast. Floette comes as the Day Care gift at 30 | player |
| Clefable | 53, Candice | by hand | A Moon Stone evolution with a sparse list. Halving suits its support role beside Moonblast (50) | player |

Shaymin would fit too, but only in the post-game.

## Moves for trainers only

| Move | Why not the player | Trainer homes |
|---|---|---|
| Hurricane | 80% (R37): the generator never adds an attack under 90%. Ian may except Pelipper at 58, where it climbs | Jupiter's planned Drizzle Zapdos, or an ordinary rain team's Pelipper: in rain it never misses |
| Zap Cannon | 50% (R37); Ian named it welcome on trainers (2026-10-06) | A trainer's Magnezone with Lock-On (Byron's, Volkner's or Cyrus's at Galactic HQ). The readings do not yet model Lock-On's sure hit |
| Inferno | 50% (R37) | A late Fire trainer's Magmortar (Ace Trainers Keenan and Henry) or Flint's Ninetales: a coin-flip sure burn |
| Misty Explosion | it knocks its user out (R26). Its Oxide power is 200, from Hardlove's data; Sword and Shield's is 100 | The Tyche and Hermes double, whose theme is Protect beside Explosion, or Saturn's Mr. Mime as his one forced trade |
| Mind Blown | 150 power for half the user's HP: half a forced trade in a permadeath run, and the generator never adds it. Gap: the readings take no HP (open) | Cyrus 3's Heatran, or Flint's Magmortar |
| Geomancy | a charge turn, then two stages each of Sp. Atk, Sp. Def and Speed: too strong for a player list. Gap: nothing happens in the readings (open) | A late boss's special attacker with a Power Herb, or a weird set on Officer Hesperid's team |

## Moves best left unused

| Move | Reason |
|---|---|
| Barrage, Comet Punch | left the game with the multi-hit ruling (Ian, 2026-10-06): one two-to-five-hit move per type |
| Psywave | cut, its lines given Psybeam (Ian, 2026-10-06) |
| Constrict, Wrap, Submission, Comeuppance | dead weight, named in the balance rules |
| Ice Spinner | terrain is not ported; Ian ruled on 2026-09-27 that Steel Roller and Ice Spinner stay dead and leave every obtainable line |
| Struggle | every Pokemon falls back on it with no PP left; it needs no learner |
| Bone Club | 85% (R37), and Bulldoze and Stomping Tantrum do its work. Cubone and Marowak are not obtainable |
| Supercell Slam | Oxide's ThunderPunch is 95 and never misses, and Thunder Fang is 90; this adds five power and a crash |
| Ice Hammer | Oxide's Ice Punch is 95 with no Speed drop. Abomasnow, its Legends Z-A learner, already has Ice Punch |
| Dragon Hammer | Oxide's Dragon Rush is the same 100 and 100%, with a 20% flinch |
| False Surrender | Crunch is the same 80, with a Defense drop; never missing matters only against evasion, which is rare |
| Land's Wrath | a weaker Earthquake |
| Branch Poke | an exact copy of Leafage, which already fills the foot of the physical Grass ladder |
| Autotomize | Agility and Rock Polish do the same. Steelix and Skarmory, its Brilliant Diamond learners, have Rock Polish and Agility |
| Tera Blast | Oxide has no Terastallizing; as a plain 80 it is Tri Attack without the status chance. The generator holds it off by name |
| Beat Up | weak in a single battle, and the readings count it as one small hit (open). A doubles trick for a trainer at most |
| Pay Day | a 40-power hit whose effect is prize money; the balance rules add no weak attacks |
| Cut | Ian ruled on 2026-09-27 that Cut leaves wherever it was only an HM; HM01 is not placed |
| Work Up | rated niche: Growth without the sun |
| Laser Focus | rated niche: a turn spent to make the next hit critical. Nothing happens in the readings (open) |
| Sharpen | rated bad: Howl and Hone Claws do more |
| Power Shift | rated bad: Power Trick's swap. Nothing happens in the readings (open) |
| Wonder Room | rated bad. Nothing happens in the readings (open) |
| Spotlight | does nothing in a single battle, and Follow Me covers the doubles use |
| Conversion 2 | rated niche, and its learners (the Porygon line) are not obtainable. Nothing happens in the readings (open) |

Officer Hesperid's theme of weird sets is the one place several of these could go on purpose.
