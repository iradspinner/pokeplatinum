# HQ's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in HQ's split, whose cap is 60. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 60, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 60 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 40 | Oxide | Aurora Beam, Bug Buzz, Aurora Veil, Blizzard | Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 40 | v3 | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Galvantula | honey | 40 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55 | Galvantula |
| Galvantula | honey | 40 | v3 | Gastro Acid, Struggle Bug, Discharge, Signal Beam | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Energy Ball 53, Thunder 55 | Galvantula |
| Heracross | honey | 40 | Oxide | Brick Break, Counter, Take Down, Close Combat | Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 40 | v3 | Counter, Brick Break, Take Down, Close Combat | Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Larvesta | honey | 40 | Oxide | Flame Charge, Struggle Bug, Flame Wheel, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60 | Volcarona (from 59) |
| Larvesta | honey | 40 | v3 | Struggle Bug, Flame Wheel, Double-Edge, Bug Bite | Take Down 50; as Volcarona: Flamethrower 60 | Volcarona (from 59) |
| Leavanny | honey | 40 | Oxide | Fell Stinger, Helping Hand, Leaf Blade, X-Scissor | Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 40 | v3 | Struggle Bug, Fell Stinger, Helping Hand, X-Scissor | Entrainment 43, Swords Dance 46, Leaf Storm 50, Leaf Blade 53 | Leavanny |
| Scizor | honey | 40 | Oxide | Fury Cutter, Slash, Razor Wind, Iron Defense | X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53, Swords Dance 57 | Scizor |
| Scizor | honey | 40 | v3 | Agility, Metal Claw, Slash, Iron Defense | Iron Head 44, Night Slash 45, Double Hit 49, X-Scissor 53, Swords Dance 57 | Scizor |
| Skarmory | honey | 40 | both | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Snorlax | honey | 40 | Oxide | Snore, Sleep Talk, Body Slam, Block | Rollout 41, Crunch 44, Giga Impact 49 | Snorlax |
| Snorlax | honey | 40 | v3 | Rest, Sleep Talk, Body Slam, Block | Crunch 44, Giga Impact 49 | Snorlax |
| Toucannon | honey | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 40 | v3 | Roost, Fury Attack, Screech, Bullet Seed | FeatherDance 44, Hyper Voice 56 | Toucannon |
| Vespiquen | honey | 40 | Oxide | Slash, Captivate, Attack Order, Swagger | Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 40 | v3 | Slash, Captivate, Swagger, Attack Order | Destiny Bond 43 | Vespiquen |
| Vikavolt | honey | 40 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55 | Vikavolt |
| Vikavolt | honey | 40 | v3 | Spark, Crunch, Signal Beam, Discharge | Bug Buzz 53, X-Scissor 53 | Vikavolt |
| Yanmega | honey | 40 | Oxide | Uproar, Pursuit, AncientPower, Feint | Slash 43, Screech 46, U-turn 49, Air Slash 54, Bug Buzz 57 | Yanmega |
| Yanmega | honey | 40 | v3 | Uproar, Pursuit, AncientPower, Feint | Wing Attack 42, Slash 43, Screech 46, U-turn 49, Bug Buzz 57 | Yanmega |
