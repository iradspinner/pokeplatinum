# League's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in League's split, whose cap is 78. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 78, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 78 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 45 | Oxide | Bug Buzz, Aurora Veil, Blizzard, Tailwind | Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 45 | Rewrite | Aurora Veil, Psybeam, Ice Beam, Tailwind | Wide Guard 48, Giga Drain 50, Quiver Dance 52, Air Slash 58, Dazzling Gleam 60, Calm Mind 66 | Frosmoth |
| Galvantula | honey | 45 | Oxide | Discharge, Signal Beam, Energy Ball, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | honey | 45 | Rewrite | Signal Beam, Energy Ball, Sucker Punch, Giga Drain | Thunderbolt 48, Bug Buzz 51, Agility 54, Screech 58, Volt Switch 65, Sludge Bomb 67, Sticky Web 69 | Galvantula |
| Heracross | honey | 45 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 45 | Rewrite | Leech Life, Close Combat, Reversal, Throat Chop | Lunge 51, Megahorn 55, Bulldoze 59, Earthquake 67 | Heracross |
| Larvesta | honey | 45 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65, Heat Wave 66, Pollen Puff 72, Roost 77 | Volcarona (from 59) |
| Larvesta | honey | 45 | Rewrite | Flame Wheel, Bug Bite, Fire Spin, Screech | Poison Jab 47, Take Down 50; as Volcarona: Mystical Fire 59, Flamethrower 60, Bug Buzz 61, Rage Powder 62, Overheat 65, Heat Wave 66, Psychic 68, Giga Drain 70, Pollen Puff 72, Roost 77, Air Slash 78 | Volcarona (from 59) |
| Leavanny | honey | 45 | Oxide | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 45 | Rewrite | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Poison Jab 48, Leaf Storm 50, Slash 54, Shadow Claw 58, Lunge 60, Skitter Smack 66, Throat Chop 68, Take Down 74 | Leavanny |
| Scizor | honey | 45 | Oxide | Razor Wind, Iron Defense, X-Scissor, Night Slash | Double Hit 49, Iron Head 53, Swords Dance 57, Feint 61 | Scizor |
| Scizor | honey | 45 | Rewrite | Iron Defense, X-Scissor, Brick Break, Night Slash | Double Hit 49, Iron Head 53, Skitter Smack 55, Swords Dance 57, Double-Edge 62, U-turn 64, Acrobatics 70, Close Combat 72 | Scizor |
| Skarmory | honey | 45 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | honey | 45 | Rewrite | Agility, Slash, Swift, Night Slash | Body Press 54, Drill Peck 56, Brave Bird 62, Iron Head 64, Rock Tomb 70, Double-Edge 72 | Skarmory |
| Snorlax | honey | 45 | Oxide | Body Slam, Block, Rollout, Crunch | Giga Impact 49 | Snorlax |
| Snorlax | honey | 45 | Rewrite | Block, Bulldoze, Rollout, Crunch | Giga Impact 49, Body Press 51, Slam 56, Hammer Arm 64, Earthquake 68, Superpower 72 | Snorlax |
| Toucannon | honey | 45 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | honey | 45 | Rewrite | Facade, Bullet Seed, Throat Chop, FeatherDance | Hyper Voice 50, Take Down 52, Seed Bomb 58, Brick Break 60, Beak Blast 66, Temper Flare 68, Rock Climb 74 | Toucannon |
| Vespiquen | honey | 45 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | honey | 45 | Rewrite | Swagger, Pounce, Air Slash, U-turn | Psychic Noise 51, Poison Jab 53, Sludge Bomb 59, Take Down 61, Acrobatics 67, Secret Power 69 | Vespiquen |
| Vikavolt | honey | 45 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | honey | 45 | Rewrite | Discharge, Signal Beam, Mud Shot, Flash Cannon | Bug Buzz 55, Energy Ball 57, Agility 62, Thunderbolt 65, Volt Switch 70, Air Slash 72 | Vikavolt |
| Yanmega | honey | 45 | Oxide | Pursuit, AncientPower, Feint, Slash | Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 45 | Rewrite | Pursuit, AncientPower, Ominous Wind, Slash | Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54, Bug Buzz 57, Giga Drain 59, Psychic 61, Shadow Ball 64 | Yanmega |
