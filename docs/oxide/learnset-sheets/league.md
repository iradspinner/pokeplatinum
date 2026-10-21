# League's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in League's split, whose cap is 78. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 78, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 78 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 45 | Oxide | Bug Buzz, Aurora Veil, Blizzard, Tailwind | Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 45 | Rewrite | Aurora Veil, Aurora Beam, Ice Beam, Tailwind | Wide Guard 48, Quiver Dance 52, Calm Mind 61 | Frosmoth |
| Galvantula | honey | 45 | Oxide | Discharge, Signal Beam, Energy Ball, Sucker Punch | Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | honey | 45 | Rewrite | Signal Beam, Energy Ball, Sucker Punch, Swift | Thunderbolt 48, Bug Buzz 51, Agility 54, Sludge Bomb 58, Volt Switch 65, Dark Pulse 67, Screech 69, Sticky Web 74 | Galvantula |
| Heracross | honey | 45 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 45 | Rewrite | Bulldoze, Close Combat, Reversal, Rock Tomb | Megahorn 55, Leech Life 59, Lunge 61 | Heracross |
| Larvesta | honey | 45 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65, Heat Wave 66, Pollen Puff 72, Roost 77 | Volcarona (from 59) |
| Larvesta | honey | 45 | Rewrite | Flame Wheel, Bug Bite, Fire Spin, Screech | Poison Jab 47, Take Down 50; as Volcarona: Mystical Fire 59, Flamethrower 60, Bug Buzz 61, Rage Powder 62, Fiery Dance 63, Overheat 65, Heat Wave 66, Psychic 68, Giga Drain 70, Pollen Puff 72, Roost 77, Air Slash 78 | Volcarona (from 59) |
| Leavanny | honey | 45 | Oxide | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 45 | Rewrite | Helping Hand, Leaf Blade, X-Scissor, Entrainment | Swords Dance 46, Throat Chop 48, Leaf Storm 50, Lunge 54, Poison Jab 58, Skitter Smack 60, Shadow Claw 66 | Leavanny |
| Scizor | honey | 45 | Oxide | Razor Wind, Iron Defense, X-Scissor, Night Slash | Double Hit 49, Iron Head 53, Swords Dance 57, Feint 61 | Scizor |
| Scizor | honey | 45 | Rewrite | Iron Defense, X-Scissor, Dual Wingbeat, Night Slash | Double Hit 49, Iron Head 53, Brick Break 55, Swords Dance 57, Lunge 62, Skitter Smack 64, U-turn 70, Strength 72 | Scizor |
| Skarmory | honey | 45 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | honey | 45 | Rewrite | Agility, Slash, Swift, Night Slash | Dual Wingbeat 54, Iron Head 56, Rock Tomb 62, Body Press 64, Drill Run 70, Iron Defense 72 | Skarmory |
| Snorlax | honey | 45 | Oxide | Body Slam, Block, Rollout, Crunch | Giga Impact 49 | Snorlax |
| Snorlax | honey | 45 | Rewrite | Body Slam, Block, Rollout, Crunch | Giga Impact 49, Body Press 51, Heat Crash 58, Charm 64 | Snorlax |
| Toucannon | honey | 45 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | honey | 45 | Rewrite | Drill Peck, Bullet Seed, Throat Chop, FeatherDance | Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60, Rock Climb 66 | Toucannon |
| Vespiquen | honey | 45 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | honey | 45 | Rewrite | Swagger, Dual Wingbeat, U-turn, Pounce | Psychic Noise 51, Secret Power 53, Low Sweep 59, Agility 67 | Vespiquen |
| Vikavolt | honey | 45 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | honey | 45 | Rewrite | Signal Beam, Rising Voltage, Bug Buzz, Air Slash | Discharge 48, Agility 50, Energy Ball 56, Iron Defense 57, Thunderbolt 65, Volt Switch 67, Flash Cannon 72 | Vikavolt |
| Yanmega | honey | 45 | Oxide | Pursuit, AncientPower, Feint, Slash | Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 45 | Rewrite | Pursuit, AncientPower, Ominous Wind, Slash | Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54, Bug Buzz 57, Giga Drain 59, Roost 64 | Yanmega |
