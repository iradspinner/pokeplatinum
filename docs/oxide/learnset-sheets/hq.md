# HQ's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in HQ's split, whose cap is 60. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 60, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 60 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 40 | Oxide | Aurora Beam, Bug Buzz, Aurora Veil, Blizzard | Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 40 | Rewrite | Defog, Aurora Veil, Aurora Beam, Ice Beam | Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Galvantula | honey | 40 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55 | Galvantula |
| Galvantula | honey | 40 | Rewrite | Discharge, Giga Drain, Signal Beam, Energy Ball | Sucker Punch 43, Swift 45, Thunderbolt 48, Bug Buzz 51, Agility 54, Sludge Bomb 58 | Galvantula |
| Heracross | honey | 40 | Oxide | Brick Break, Counter, Take Down, Close Combat | Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 40 | Rewrite | Smack Down, Take Down, Bulldoze, Close Combat | Reversal 43, Rock Tomb 45, Megahorn 55, Leech Life 59 | Heracross |
| Larvesta | honey | 40 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60 | Volcarona (from 59) |
| Larvesta | honey | 40 | Rewrite | Struggle Bug, U-turn, Flame Wheel, Bug Bite | Fire Spin 41, Screech 45, Poison Jab 47, Take Down 50; as Volcarona: Mystical Fire 59, Flamethrower 60 | Volcarona (from 59) |
| Leavanny | honey | 40 | Oxide | Fell Stinger, Helping Hand, Leaf Blade, X-Scissor | Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 40 | Rewrite | Fell Stinger, Helping Hand, Leaf Blade, X-Scissor | Entrainment 43, Swords Dance 46, Throat Chop 48, Leaf Storm 50, Lunge 54, Poison Jab 58, Skitter Smack 60 | Leavanny |
| Scizor | honey | 40 | Oxide | Fury Cutter, Slash, Razor Wind, Iron Defense | X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53, Swords Dance 57 | Scizor |
| Scizor | honey | 40 | Rewrite | Secret Power, Slash, Rock Blast, Iron Defense | X-Scissor 41, Dual Wingbeat 43, Night Slash 45, Double Hit 49, Iron Head 53, Brick Break 55, Swords Dance 57 | Scizor |
| Skarmory | honey | 40 | Oxide | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Skarmory | honey | 40 | Rewrite | Metal Sound, Steel Wing, Air Slash, Air Cutter | Agility 41, Slash 42, Swift 43, Night Slash 45, Dual Wingbeat 54, Iron Head 56 | Skarmory |
| Snorlax | honey | 40 | Oxide | Snore, Sleep Talk, Body Slam, Block | Rollout 41, Crunch 44, Giga Impact 49 | Snorlax |
| Snorlax | honey | 40 | Rewrite | Lick, Yawn, Body Slam, Block | Rollout 41, Crunch 44, Giga Impact 49, Body Press 51, Heat Crash 58 | Snorlax |
| Toucannon | honey | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 40 | Rewrite | Roost, Screech, Drill Peck, Bullet Seed | Throat Chop 42, FeatherDance 44, Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60 | Toucannon |
| Vespiquen | honey | 40 | Oxide | Slash, Captivate, Attack Order, Swagger | Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 40 | Rewrite | Captivate, Confuse Ray, Attack Order, Swagger | Dual Wingbeat 41, U-turn 43, Pounce 45, Psychic Noise 51, Secret Power 53, Low Sweep 59 | Vespiquen |
| Vikavolt | honey | 40 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55 | Vikavolt |
| Vikavolt | honey | 40 | Rewrite | Spark, Signal Beam, Rising Voltage, Bug Buzz | Air Slash 42, Discharge 48, Agility 50, Energy Ball 56, Iron Defense 57 | Vikavolt |
| Yanmega | honey | 40 | Oxide | Uproar, Pursuit, AncientPower, Feint | Slash 43, Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 40 | Rewrite | Uproar, Pursuit, AncientPower, Ominous Wind | Slash 43, Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54, Bug Buzz 57, Giga Drain 59 | Yanmega |
