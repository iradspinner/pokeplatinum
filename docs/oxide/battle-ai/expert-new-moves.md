# The new moves' Expert routines

Ian's ruling of 2026-09-27: the moves added since Platinum follow Platinum's own Expert pattern. Each learnable move past Platinum's 467 takes the Expert routine of its nearest Platinum effect, judged by what its effect script does rather than by the effect's name, where that effect has a routine, and gets none where Platinum gives its equivalents none. Platinum's own moves without a routine stay as they are ([expert-gaps.md](expert-gaps.md)). How Expert dispatches is in [expert-1.md](expert-1.md), and element 6's earlier routing in [README.md](README.md). This is a change of play; it acts once the trainer pass gives trainers these moves.

A move is counted as learnable when any species' or form's level, TM, tutor or egg list has it (the move pool survey's reading of `res/pokemon`). Expert dispatches by effect, so a move no species learns is routed too when it shares an effect with one listed here: Circle Throw, on Dragon Tail's effect, is the only one. The learnset rewrite of 2026-10-06 made more moves learnable; the five on effects of their own, which Expert's dispatch did not name, are added here (Relic Song, Throat Chop, Meteor Beam, Axe Kick and Psychic Noise, 2026-10-07), and the other 22 reach Expert through a Platinum effect or an existing line of its dispatch ([other-flags-new-moves.md](other-flags-new-moves.md) names them). The counts, for the moves this page names:

| | Moves |
|---|---|
| learnable moves past id 467 | 161 |
| scored by an Expert routine | 67 |
| with none | 94 |
| of those, judgment calls, left with none by Ian's ruling (below) | 11 |

A move a routine names below is scored as that Platinum move is; the routines are described in [expert-1.md](expert-1.md) and [expert-2.md](expert-2.md), and the ones element 6 wrote in the README. Two are trimmed copies made for this pass, as element 6 made one of Thunder's for the Hisuian storms: `Expert_ClearSmog` keeps Haze's tests of the target's stages and drops those of the user's, and `Expert_MortalSpin` keeps Rapid Spin's clearing and drops its Speed raise.

## Judgment calls, settled

Each of these is left with none, though a Platinum routine is near, because that routine would misjudge the move. Ian ruled on 2026-09-27 that they stay that way ("None, as left"); a routine of its own for any of them would be a new change of play.

- Core Enforcer: A hit that then suppresses an ability; Gastro Acid's routine takes points off against a weakened target, where a hit is worth the most.
- Crafty Shield, Mat Block, Quick Guard and Wide Guard: Each shares Protect's subscript but stops only one kind of move (spread moves, priority moves, first-turn damage or status moves), which Protect's routine does not measure; worth a routine of its own for double battles.
- Final Gambit: Its damage is its user's HP; Explosion's and Endeavor's routines favour a user at low HP, where it does least.
- Guard Split: It averages the two battlers' Defense and Sp. Def; Guard Swap's routine reads stat stages, which it leaves alone, and Pain Split's reads HP.
- Laser Focus: A critical-hit setup, as Focus Energy; Lock-On's routine, a coin flip for +2, is the other candidate.
- Power Split: As Guard Split, for Attack and Sp. Atk.
- Salt Cure: A hit that costs the target HP every turn; Bind's routine values trapping, which Salt Cure does not do, and Leech Seed's is for a status move.
- Wonder Room: Trick Room's routine reads Speed and Power Trick's its user's own stats; neither measures a Defense and Sp. Def swap for everyone.

## Scored by a routine

- Acrobatics: Wake-Up Slap's shape, routed by element 6.
- Anchor Shot: Mean Look's, since it traps.
- Armor Cannon: Close Combat's, by its own Platinum effect.
- Aurora Veil: Reflect's shape, routed by element 6.
- Autotomize: Agility's, routed by element 6.
- Baby-Doll Eyes: Growl's, by its own Platinum effect.
- Baneful Bunker: Protect's, by its own Platinum effect.
- Bitter Blade: Absorb's, by its own Platinum effect.
- Bulldoze: BubbleBeam's, by its own Platinum effect.
- Burn Up: Overheat's: a strong hit that weakens its user afterwards.
- Clanging Scales: Close Combat's, routed by element 6.
- Clear Smog: Haze's, the target's half only, since Clear Smog leaves its user's stages alone.
- Coil: Harden's, routed by element 6.
- Cotton Guard: Harden's, routed by element 6.
- Disarming Voice: Swift's, by its own Platinum effect.
- Double Shock: Overheat's, as Burn Up.
- Dragon Tail: Roar's, since it forces a switch.
- Draining Kiss: Absorb's, routed by element 6.
- Eerie Impulse: `Expert_StatusSpAttackDown`, by its own Platinum effect, which no Platinum move uses.
- Electroweb: BubbleBeam's, by its own Platinum effect.
- Entrainment: Worry Seed's; both overwrite the target's ability, and its script uses Worry Seed's flags.
- Flame Charge: Rapid Spin's Speed part, routed by element 6.
- Fleur Cannon: Overheat's, by its own Platinum effect.
- Flip Turn: U-turn's, by its own Platinum effect.
- Flower Trick: Karate Chop's, routed by element 6.
- Geomancy: Dragon Dance's, routed by element 6.
- Hex: Wake-Up Slap's shape, routed by element 6.
- Hone Claws: Meditate's, routed by element 6.
- Horn Leech: Absorb's, by its own Platinum effect.
- Hurricane: Thunder's, routed by element 6.
- Incinerate: Pluck's; both are hits that take the target's Berry.
- Infestation: Bind's, by its own Platinum effect.
- Life Dew: Recover's, routed by element 6.
- Low Sweep: BubbleBeam's, by its own Platinum effect.
- Magic Room: Embargo's; both stop held items.
- Matcha Gotcha: Absorb's, routed by element 6.
- Meteor Beam: Skull Bash's, which charges for a turn as it does, raising Defense where Meteor Beam raises Sp. Atk; the routine's +2 for a Power Herb applies, since Oxide's Meteor Beam takes the Herb's path (2026-10-07).
- Mind Blown: Head Smash's (recoil). Note: the routine's +1 for Magic Guard is right, its +1 for Rock Head is not, since Rock Head does not spare Mind Blown's cost.
- Mortal Spin: Rapid Spin's clearing half, since it clears as Rapid Spin does but raises no Speed.
- Nature’sMadness: Super Fang's, by its own Platinum effect.
- Noble Roar: Growl's (Attack down); Platinum sends its own two-stat drop, Tickle, to a one-stat routine too.
- Oblivion Wing: Absorb's, routed by element 6.
- Octolock: Mean Look's; it is built on Mean Look's effect.
- Parting Shot: U-turn's, without the resist check, routed by element 6.
- Phantom Force: Shadow Force's, by its own Platinum effect.
- Play Nice: Growl's, by its own Platinum effect.
- Psychic Noise: Heal Block's, since it is a hit that puts Heal Block on its target. Note: the routine's chance of +1 when the target has no way to heal is Heal Block's own, and here it rides on a hit (2026-10-07).
- Quiver Dance: Dragon Dance's, routed by element 6.
- Shell Smash: Dragon Dance's, routed by element 6.
- Shelter: Barrier's, by its own Platinum effect.
- Shift Gear: Dragon Dance's, routed by element 6.
- Shore Up: Recover's (by its move id at the top of Synthesis's routine, since the engine heals it as Recover, or more in a sandstorm).
- Sky Drop: Fly's, a turn in the air. Note: the routine's +2 for a Power Herb does not apply, since Oxide's Sky Drop has no Power Herb path.
- Smack Down: Gravity's, which tests whether the target is airborne, the case where grounding it matters.
- Smart Strike: Swift's, by its own Platinum effect.
- Solar Blade: SolarBeam's, by its own Platinum effect.
- Spiky Shield: Protect's, by its own Platinum effect.
- Spirit Shackle: Mean Look's, since it traps.
- Sticky Web: Spikes', routed by element 6.
- Strength Sap: Recover's, routed by element 6.
- Tearful Look: Growl's (Attack down); Platinum sends its own two-stat drop, Tickle, to a one-stat routine too.
- Thousand Arrows: Gravity's, which tests whether the target is airborne, the case where grounding it matters.
- Thousand Waves: Mean Look's, since it traps.
- Venom Drench: Growl's (Attack down), as Noble Roar. Note: nothing refuses it into an unpoisoned target, where it fails.
- Venoshock: Wake-Up Slap's shape, routed by element 6.
- Volt Switch: U-turn's, by its own Platinum effect.
- Wild Charge: Double-Edge's, by its own Platinum effect.

## Left with none

- Accelerock: none, as Platinum's Quick Attack.
- Acid Spray: none, as Platinum's Seed Flare.
- After You: none, as Platinum's Helping Hand: partner-side support.
- Ally Switch: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Aromatic Mist: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Axe Kick: none, as Platinum's Hi Jump Kick, which crashes on a miss as it does; its chance to confuse is Psybeam's, which has no routine either (2026-10-07).
- Beak Blast: none, a plain hit, as Platinum's Tackle; it heats up first and burns an attacker that touches it, where Focus Punch fails when hit.
- Belch: none, as Platinum's Tackle: a plain hit once its user has eaten a Berry; nothing refuses it before then.
- Body Press: none, a plain hit, as Platinum's Tackle; it attacks with its user's Defense.
- Boomburst: none, a plain hit, as Platinum's Tackle.
- Breaking Swipe: none, as Platinum's Aurora Beam.
- Brutal Swing: none, a plain hit, as Platinum's Tackle.
- Coaching: none, as Platinum's Helping Hand: a move at the partner, where Expert stops.
- Core Enforcer: none; the nearest is Platinum's Gastro Acid, whose routine would misjudge it (a judgment call, above).
- Crafty Shield: none; the nearest is Platinum's Protect, whose routine would misjudge it (a judgment call, above).
- Darkest Lariat: none, a plain hit, as Platinum's Tackle; it ignores the target's stat changes.
- Dazzling Gleam: none, a plain hit, as Platinum's Tackle.
- Diamond Storm: none, as Platinum's Steel Wing: a hit that raises its user's Defense.
- Dual Chop: none, as Platinum's Double Kick.
- Dual Wingbeat: none, as Platinum's Double Kick.
- Echoed Voice: none, a plain hit, as Platinum's Tackle; its power grows with use, as Fury Cutter's, which has no routine either.
- ElectricTerrain: none, as Platinum's Splash: terrain is not in Oxide, so it does nothing; Basic gives it -10.
- Electro Ball: none, a plain hit, as Platinum's Tackle; its power grows with its user's Speed, the reverse of Gyro Ball, whose routine would misjudge it.
- Expanding Force: none, a plain hit, as Platinum's Tackle.
- Fairy Lock: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Fairy Wind: none, a plain hit, as Platinum's Tackle.
- Fell Stinger: none, as Platinum's Metal Claw: a hit that raises its user's Attack.
- Fiery Dance: none, as Platinum's Charge Beam.
- Fiery Wrath: none, as Platinum's Rolling Kick.
- Final Gambit: none; the nearest is Platinum's Explosion, whose routine would misjudge it (a judgment call, above).
- Flame Burst: none, a plain hit, as Platinum's Tackle; its burst hits the target's partner.
- Flower Shield: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Flying Press: none, a plain hit, as Platinum's Tackle; it is Fighting and Flying at once.
- Foul Play: none, a plain hit, as Platinum's Tackle; it attacks with the target's Attack.
- Freeze-Dry: none, as Platinum's Ice Punch.
- Freezing Glare: none, as Platinum's Ice Punch.
- Grassy Glide: none, a plain hit, as Platinum's Tackle.
- Grassy Terrain: none, as Platinum's Splash: terrain is not in Oxide, so it does nothing; Basic gives it -10.
- Guard Split: none; the nearest is Platinum's Guard Swap, whose routine would misjudge it (a judgment call, above).
- Heal Pulse: none, as Platinum's Present: a heal aimed at another battler; Expert stops for a move at its partner, and nothing in Platinum heals a foe on purpose.
- Heavy Slam: none, as Platinum's Low Kick: power from weight, as Low Kick and Grass Knot.
- Hold Back: none, as Platinum's False Swipe.
- Land’s Wrath: none, a plain hit, as Platinum's Tackle.
- Laser Focus: none; the nearest is Platinum's Focus Energy, whose routine would misjudge it (a judgment call, above).
- Leafage: none, a plain hit, as Platinum's Tackle.
- Liquidation: none, as Platinum's Iron Tail.
- Lunge: none, as Platinum's Aurora Beam.
- Magnetic Flux: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Mat Block: none; the nearest is Platinum's Protect, whose routine would misjudge it (a judgment call, above).
- Misty Terrain: none, as Platinum's Splash: terrain is not in Oxide, so it does nothing; Basic gives it -10.
- Moonblast: none, as Platinum's Mist Ball.
- Mystical Fire: none, as Platinum's Mist Ball.
- Nuzzle: none, as Platinum's ThunderPunch.
- Petal Blizzard: none, a plain hit, as Platinum's Tackle.
- Play Rough: none, as Platinum's Aurora Beam.
- Pollen Puff: none, as Platinum's Present: a hit on a foe or a heal on an ally, as Present.
- Poltergeist: none, as Platinum's Tackle: a plain hit once the target holds an item; Basic already gives it -10 into a target with none.
- Power Split: none; the nearest is Platinum's Power Swap, whose routine would misjudge it (a judgment call, above).
- Power-Up Punch: none, as Platinum's Metal Claw.
- Psychic Terrain: none, as Platinum's Splash: terrain is not in Oxide, so it does nothing; Basic gives it -10.
- Psyshock: none, a plain hit, as Platinum's Tackle; it hits the target's Defense.
- Pyro Ball: none, as Platinum's Fire Punch.
- Quick Guard: none; the nearest is Platinum's Protect, whose routine would misjudge it (a judgment call, above).
- Rage Fist: none, a plain hit, as Platinum's Tackle; its power grows each time its user is hit, as Rage's attack grows, with no routine.
- Rage Powder: none, as Platinum's Follow Me.
- Relic Song: none, as Platinum's ThunderPunch: a hit with a chance of a status, here sleep; its form change has no Platinum equivalent (2026-10-07).
- Retaliate: none, a plain hit, as Platinum's Tackle; its power doubles after an ally faints.
- Sacred Sword: none, a plain hit, as Platinum's Tackle; it ignores the target's stat changes.
- Salt Cure: none; the nearest is Platinum's Bind, whose routine would misjudge it (a judgment call, above).
- Scald: none, as Platinum's Flame Wheel.
- Scale Shot: none, as Platinum's DoubleSlap.
- Skitter Smack: none, as Platinum's Mist Ball.
- Sludge Wave: none, as Platinum's Poison Sting.
- Snarl: none, as Platinum's Mist Ball.
- Soak: none, as Platinum's Conversion 2: no Platinum effect changes the target's type; Conversion 2, the nearest, has no routine.
- Sparkling Aria: none, a plain hit, as Platinum's Tackle.
- Speed Swap: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Steel Roller: none, as Platinum's Tackle: a plain hit in Oxide, which has no terrain to end.
- StompingTantrum: none, a plain hit, as Platinum's Tackle; its power doubles after its user's move failed.
- Strange Steam: none, as Platinum's Psybeam.
- Struggle Bug: none, as Platinum's Mist Ball.
- Tail Slap: none, as Platinum's DoubleSlap.
- Teatime: none: no Platinum move makes a battler eat its own Berry.
- Telekinesis: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Terrain Pulse: none, a plain hit, as Platinum's Tackle.
- Throat Chop: none, a plain hit with Taunt's kind of added effect: it bars a class of the target's moves for a few turns, sound moves where Taunt bars status moves, and Platinum gives Taunt no routine (2026-10-07).
- Thunderous Kick: none, as Platinum's Iron Tail.
- Topsy-Turvy: none: cut from every learnset and its effect unwritten; Basic gives it -10.
- Triple Axel: none, as Platinum's Triple Kick.
- Trop Kick: none, as Platinum's Aurora Beam.
- Water Shuriken: none, as Platinum's DoubleSlap.
- Wide Guard: none; the nearest is Platinum's Protect, whose routine would misjudge it (a judgment call, above).
- Wonder Room: none; the nearest is Platinum's Trick Room, whose routine would misjudge it (a judgment call, above).
- Zing Zap: none, as Platinum's Rolling Kick.
