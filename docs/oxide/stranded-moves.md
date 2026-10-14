# Stranded moves

This answers Ian's request of 2026-10-14: of the moves `move-access.md` found that no player can learn, a list of the working ones with the lines or trainers each would fit, on the learnset rules' ladder, for him to pick from before any list changes. Nothing in `res/` changes here. It was read from origin/oxide at 0db0d8f8b3.

**This page is unfinished.** Work stopped on 2026-10-14 at Ian's word (helpers run one at a time while the simulator fixes go first). The scope, the engine verdicts, the moves the standing rulings already settle, and the simulator gaps each move has are done and below. The homes for the remaining moves, the ten that matter most and the one-page summary are not written yet; the last section says what is left and how to resume.

## What is done so far

The request covers 88 moves: the 53 ordinary moves of the audit's group (a) that no species learns, and the 35 of group (b) that only species the player cannot obtain learn. Obtainability is `obtainable()` in `tools/oxide/balance/pool.py`, as the audit used: 468 species.

83 of the 88 run in Oxide's engine as written. The other five are out of this proposal:

| Move | Why it is out |
|---|---|
| Snap Trap | a plain 35-power hit; the binding is missing |
| Steel Beam | a plain 140-power hit; the user's loss of half its HP is missing |
| Synchronoise | a plain hit; the rule that it hits only a foe sharing a type is missing |
| Eerie Spell | a plain 80-power sound move; its record says it drains 3 PP from the foe's last move, and nothing in the engine does (the audit's engine column says it runs) |
| Teleport | flees a wild battle and fails against a trainer |

Two of the 83 need a word. Upper Hand and Burning Jealousy were broken when the balance rules were written (Upper Hand an unconditional priority hit, Burning Jealousy always burning). The move reworks made both work on 2026-10-07, but their in-game checks (numbers 81 and 83 in `ingame-checklist.md`, section 2) still wait on Ian. Until he ticks them, the learnset generator holds both off player lists (`UNCHECKED` in `learncheck.py`). A home for either is therefore a proposal for after those checks.

### Moves a standing rule already settles

Fifteen of the 83 are settled for the player by a rule Ian has already made, before any judgement of fit. Nine should stay unused by anyone:

| Move | The rule |
|---|---|
| Barrage | left the game with the multi-hit ruling (Ian, 2026-10-06: one two-to-five-hit move per type, Normal keeping Fury Swipes and Tail Slap) |
| Comet Punch | the same ruling |
| Psywave | cut, its lines given Psybeam in its place (Ian, 2026-10-06) |
| Constrict | dead weight, named in the balance rules |
| Wrap | dead weight, named in the balance rules |
| Submission | dead weight, named in the balance rules (and 80% accurate) |
| Comeuppance | dead weight, named in the balance rules |
| Ice Spinner | terrain is not ported, and Ian ruled on 2026-09-27 that Steel Roller and Ice Spinner stay dead and leave every obtainable line; as a plain hit it would be Ice Punch at 80 power without the freeze |
| Struggle | every Pokemon falls back on it with no PP left; it needs no learner |

Six are ruled out for the player but open to trainers, who may carry anything the late and Galactic teams need:

| Move | The rule that keeps it from the player | For trainers |
|---|---|---|
| Burning Bulwark | it carries Protect's effect, and every Protect-effect move is out of every player list (R24) | open; whether its burn on contact runs in the engine was not checked |
| Misty Explosion | it knocks its user out, so it belongs to the trainers' palette only (R26) | a forced trade, at most one a boss and none before Fantina |
| Zap Cannon | 50% accurate; the 90% bar (R37) is for the player's movesets only | Ian named it as welcome on trainers (2026-10-06) |
| Inferno | 50% accurate, the same | the same reasoning as Zap Cannon |
| Bone Club | 85% accurate (R37), and Cubone and Marowak are not obtainable | weak for a trainer too: Bulldoze and Stomping Tantrum do its work |
| Hurricane | 80% accurate (R37): the generator never adds an attack under 90% | strong on a rain team, where it never misses |

Hurricane is the one of these Ian may want to overrule, since the audit named it first. The rewrite kept Head Smash under 90% as the fossils' signature, so an exception has a precedent; the player's lines would need his word for it. Its trainer homes are still to be written.

That leaves 68 working moves for which homes are to be proposed, with the trainer homes for the six above.

### The simulator gaps each move has

Ian approved fixing every gap in `simulator-gaps.md` on 2026-10-14, so a gap does not disqualify a move. These are the gaps the 83 working moves meet in the readings today. Moves with no gap are left out.

| Moves | The gap |
|---|---|
| Heat Crash | the calculator's row is an error, so it never deals damage in a reading |
| Mighty Cleave | Protect stops it, where the engine lets it through |
| Jaw Lock | a plain hit: neither Pokemon is trapped |
| Thousand Waves | a plain hit: the target is not trapped |
| Thousand Arrows | the hit runs, but nothing grounds a Flying or Levitate target |
| Core Enforcer | a plain hit: the target keeps its ability |
| Diamond Storm | a plain hit: the user's Defense never rises |
| Mind Blown | a plain 150-power hit: the user pays nothing |
| Ice Hammer | it lowers the target's Speed instead of the user's |
| Supercell Slam | it crashes only on a missed accuracy roll, for half the user's own HP |
| Frost Breath, Storm Throw | the critical hit is in the row, but stages and screens then apply as to an ordinary hit, and a second critical roll can stack |
| Dragon Darts, Twin Beam, Tachyon Cutter | two hits counted as one against Sturdy and the Focus Sash (the fix is approved and being built), with one critical roll and one contact chance |
| Triple Dive | three hits counted as one against Sturdy, the Focus Sash and a resist berry |
| Psychic Fangs | the readings halve it through a screen it should break first |
| Mist Ball | the hit lands, but the Sp. Atk drop never happens |
| Circle Throw | the target is never dragged out |
| Power Shift | nothing happens |
| Fillet Away, Autotomize, Geomancy, Laser Focus, Conversion 2, Wonder Room | nothing happens |
| Take Heart | the two stages rise, but the user's status stays |
| Oblivion Wing | it heals off a Liquid Ooze target, where the engine hurts the user |
| Doom Desire | lands at once at full power (the fix is approved and being built) |
| Beat Up | one small hit from the user alone, not one for each party member |
| Burning Bulwark | Protect's chances run approximately, and no variant punishes contact |
| Spotlight | redirects nothing in a double battle |
| Wrap | a bind takes a sixteenth a turn, where Oxide's engine takes an eighth |
| Barrage, Comet Punch | one critical roll and one contact chance cover every hit |
| Struggle | no recoil in a double battle, whose path lacks perfectline's branch for it |

Four more gaps were found while reading for this page. `simulator-gaps.md` does not list them, because each move's battle effect is a plain hit and the engine does its work in code keyed on the move. They were read from the code on 2026-10-14 and not tested with a battle:

| Moves | Oxide's engine | The simulator |
|---|---|---|
| Sacred Sword, Chip Away, and Darkest Lariat (open to the player already) | ignore the target's defensive and evasion stages (battle_lib.c 8536, battle_controller_player.c 3174) | perfectline.damage_of applies the target's Defense or Sp. Def stage to every move but an Unaware attacker's |
| Power Trip, and Stored Power (open to the player already) | 20 power more for each of the user's raised stages (battle_script.c 1463) | the row's listed 20, whatever the stages |
| Hard Press | its power falls with the target's HP (battle_script.c 1429) | the row at the target's full HP, every turn |
| Electro Ball | its power comes from both Speeds at the time (battle_script.c 1370) | the row at the starting Speeds; nothing reads it again as the fight runs, as state_mult does for Gyro Ball |

Each is a small branch in perfectline.damage_of or fightsim.state_mult, as Gyro Ball's is. They need Ian's approval as new entries before anyone fixes them, since his approval of 2026-10-14 covers the listed gaps.

## Not done yet

This part is unwritten. Tomorrow's session picks up here:

1. Homes for the 68 moves: two or three obtainable lines each, with the split and level on its type's ladder, what the home changes for that line (saying so when it makes a strong line stronger early), and whether the move suits trainers better. The ladder is the generator's (`learnrewrite.py`): a line meets a type at its split's ceiling less 20 (Roark 40, Gardenia 55, Fantina 60, Maylene and Wake 70, then higher), climbs one or two rungs a split, one for a power-flagged line, and a pivot stands at least mid-ladder. Later games' level-up lists in `~/hg-engine/data/learnsets/base/` (Black and White to Legends Z-A) are the inspiration for which lines a move fits. The Kaizo comparison is for the ladder only, since none of these moves is in Kaizo's data.
2. Trainer homes for the six moves above that the player cannot have.
3. The judgement calls among the 68 that may end unused: signatures of species Oxide lacks (Aeroblast, Origin Pulse, Psycho Boost, the Zygarde, Latias and Latios, Galarian bird and Tapu moves among them), and weak or outclassed copies (Cut, Pay Day, Sharpen, Beat Up, Laser Focus, Conversion 2, Spotlight).
4. The one-page summary: the counts, the ten homes that matter most and why, the moves best left unused, and what Ian picks.
