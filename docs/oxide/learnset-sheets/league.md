# League's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in League's split, whose cap is 78. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 78, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 78 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 45 | Oxide | Bug Buzz, Aurora Veil, Blizzard, Tailwind | Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 45 | Rewrite | Aurora Beam, Aurora Veil, Ice Beam, Tailwind | Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56, Dazzling Gleam 60, Calm Mind 65 | Frosmoth |
| Galvantula | honey | 45 | Oxide | Discharge, Signal Beam, Energy Ball, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | honey | 45 | Rewrite | Energy Ball, Swift, Giga Drain, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Screech 54, Agility 56, Sticky Web 60, Sludge Bomb 62, Volt Switch 65 | Galvantula |
| Heracross | honey | 45 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 45 | Rewrite | Leech Life, Close Combat, Throat Chop, Reversal | Skitter Smack 46, Lunge 49, Bulldoze 54, Megahorn 55, Upper Hand 60, Earthquake 65 | Heracross |
| Larvesta | honey | 45 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65, Heat Wave 66, Pollen Puff 72, Roost 77 | Volcarona (from 59) |
| Larvesta | honey | 45 | Rewrite | Flame Wheel, Bug Bite, Fire Spin, Roost | Take Down 50, Poison Jab 53, Skitter Smack 54, Lunge 56; as Volcarona: Mystical Fire 59, Flamethrower 60, Bug Buzz 61, Rage Powder 62, Overheat 65, Heat Wave 66, Psychic 68, Quiver Dance 69, Giga Drain 70, Pollen Puff 72, Air Slash 74, Roost 77 | Volcarona (from 59) |
| Leavanny | honey | 45 | Oxide | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 45 | Rewrite | Leaf Blade, X-Scissor, Poison Jab, Entrainment | Swords Dance 46, Leaf Storm 50, Shadow Claw 54, Lunge 56, Throat Chop 58, Skitter Smack 60, Take Down 62, Slash 65 | Leavanny |
| Scizor | honey | 45 | Oxide | Razor Wind, Iron Defense, X-Scissor, Night Slash | Double Hit 49, Iron Head 53, Swords Dance 57, Feint 61 | Scizor |
| Scizor | honey | 45 | Rewrite | Skitter Smack, Iron Defense, X-Scissor, Night Slash | Double Hit 49, Iron Head 53, Leech Life 54, Brick Break 55, Swords Dance 57, Rock Tomb 60, U-turn 62, Lunge 65, Double-Edge 66, Close Combat 68 | Scizor |
| Skarmory | honey | 45 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | honey | 45 | Rewrite | Steel Wing, Air Slash, Slash, Night Slash | Iron Defense 48, Body Press 54, Drill Peck 56, Iron Head 58, Brave Bird 60, Rock Tomb 62, Double-Edge 65, Drill Run 68 | Skarmory |
| Snorlax | honey | 45 | Oxide | Body Slam, Block, Rollout, Crunch | Giga Impact 49 | Snorlax |
| Snorlax | honey | 45 | Rewrite | Block, Bulldoze, Rollout, Crunch | Giga Impact 49, Body Press 53, Slam 56, Hammer Arm 61, Superpower 66, Earthquake 68 | Snorlax |
| Toucannon | honey | 45 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | honey | 45 | Rewrite | Facade, Bullet Seed, Throat Chop, FeatherDance | Take Down 47, Hyper Voice 50, Brick Break 54, Temper Flare 56, Rock Climb 60, Brave Bird 65, Beak Blast 68 | Toucannon |
| Vespiquen | honey | 45 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | honey | 45 | Rewrite | Attack Order, Swagger, U-turn, Air Slash | Poison Jab 48, Psychic Noise 53, Take Down 54, Sludge Bomb 56, Secret Power 60, Brave Bird 65 | Vespiquen |
| Vikavolt | honey | 45 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | honey | 45 | Rewrite | Bite, Spark, Signal Beam, Pollen Puff | Discharge 48, Energy Ball 54, Bug Buzz 55, Air Slash 57, Flash Cannon 60, Agility 62, Thunderbolt 65, Iron Defense 66, Volt Switch 68 | Vikavolt |
| Yanmega | honey | 45 | Oxide | Pursuit, AncientPower, Feint, Slash | Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 45 | Rewrite | AncientPower, Hypnosis, Ominous Wind, Slash | Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54, Pollen Puff 55, Bug Buzz 57, Giga Drain 60, Shadow Ball 62, Psychic 65 | Yanmega |
