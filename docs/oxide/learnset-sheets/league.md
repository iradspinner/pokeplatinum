# League's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in League's split, whose cap is 78. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 78, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 78 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 45 | Oxide | Bug Buzz, Aurora Veil, Blizzard, Tailwind | Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 45 | v3 | Bug Buzz, Aurora Veil, Tailwind, Blizzard | Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Galvantula | honey | 45 | Oxide | Discharge, Signal Beam, Energy Ball, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | honey | 45 | v3 | Struggle Bug, Discharge, Signal Beam, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Energy Ball 53, Thunder 55, Volt Switch 65 | Galvantula |
| Heracross | honey | 45 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 45 | v3 | Brick Break, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55, Rock Slide 68 | Heracross |
| Larvesta | honey | 45 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65, Heat Wave 66, Pollen Puff 72, Roost 77 | Volcarona (from 59) |
| Larvesta | honey | 45 | v3 | Struggle Bug, Flame Wheel, Double-Edge, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65, Heat Wave 66, Pollen Puff 72, Roost 77 | Volcarona (from 59) |
| Leavanny | honey | 45 | Oxide | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 45 | v3 | Fell Stinger, Helping Hand, X-Scissor, Entrainment | Swords Dance 46, Leaf Storm 50, Leaf Blade 53, Slash 68 | Leavanny |
| Scizor | honey | 45 | Oxide | Razor Wind, Iron Defense, X-Scissor, Night Slash | Double Hit 49, Iron Head 53, Swords Dance 57, Feint 61 | Scizor |
| Scizor | honey | 45 | v3 | Slash, Iron Defense, Iron Head, Night Slash | Double Hit 49, X-Scissor 53, Swords Dance 57, Feint 61 | Scizor |
| Skarmory | honey | 45 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | honey | 45 | v3 | Steel Wing, Air Slash, Slash, Night Slash | Drill Run 68 | Skarmory |
| Snorlax | honey | 45 | Oxide | Body Slam, Block, Rollout, Crunch | Giga Impact 49 | Snorlax |
| Snorlax | honey | 45 | v3 | Sleep Talk, Body Slam, Block, Crunch | Giga Impact 49, Earthquake 75 | Snorlax |
| Toucannon | honey | 45 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | honey | 45 | v3 | Fury Attack, Screech, Bullet Seed, FeatherDance | Hyper Voice 56, Rock Blast 65 | Toucannon |
| Vespiquen | honey | 45 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | honey | 45 | v3 | Captivate, Swagger, Attack Order, Destiny Bond | Bug Buzz 76 | Vespiquen |
| Vikavolt | honey | 45 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | honey | 45 | v3 | Spark, Crunch, Signal Beam, Discharge | Bug Buzz 53, X-Scissor 53, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Yanmega | honey | 45 | Oxide | Pursuit, AncientPower, Feint, Slash | Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 45 | v3 | AncientPower, Feint, Wing Attack, Slash | Screech 46, U-turn 49, Bug Buzz 57, Air Slash 70 | Yanmega |
