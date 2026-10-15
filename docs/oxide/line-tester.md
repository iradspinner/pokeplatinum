# The line tester

A Battle tab for the OxiDex, planned on 2026-10-14 and not yet built. Ian sets up a party, presses Fight against a trainer's team, and plays his hand-made line turn by turn on the same simulator and trainer AI the readings use, seeing the AI's odds for every move and every way each turn can go. When it is built: the tracker's Scheduled list holds it, once every simulator fix has landed.

## Summary

Ian asked for it on 2026-10-14, the day after the Gardenia testing, when each question about his box 3 line needed a script of its own:

> I want to try to set up a tool in Oxidex for when we're testing lines for fights similar to when I build my Ian-line when we were doing the Gardenia testing yesterday. My idea for this too would be that I use the party funcitonality in the calc tab to set up my party of 6 going into the fight (or you can import a specific box's team to the tool that I can then play with) then click a button to fight a specific trainer's team, where we then play it out turn by turn with full in game AI logic (or the sim equivalent) so I can verify the integrity of hand-made lines. I'd also like to see their likelihood of each move each turn.

His answers the same day to the Overseer's four questions:

| Question | Answer |
|---|---|
| How each turn's luck is settled | A branch tree: after his choice, every way the turn can go with its exact chance; he follows one or rolls at real odds, and every turn stays a point he can return to |
| Whether a reading's box holds him to the scorer's rules | Warn, don't block |
| How much of the scorer the tool shows | Battle only, for now: no planner advice and no line win rate |
| When it is built | After the simulator fixes (the tracker's Scheduled list) |

The tool reads the simulator and never changes it. Nothing in `fightsim.py`, `fightai.py`, `perfectline.py`, `plplan.py` or the other `pl*.py` modules is edited, so the simulator's freeze does not apply and no reading moves. It runs the simulator's copy of the trainer AI, written from the game's AI scripts, which is the AI the scorer trusts; the game's own code could run only in an emulator, and sessions never launch one. Version 1 is singles only, since the turn enumeration and the planner are singles only, and the readings leave tag battles out for the same reason. By the Overseer's estimate it is about half a day of helper work.

Version 1 is done when these checks pass:

1. The calc's Fight button opens a battle of its party against the trainer on the calc's right side (a headless browser test, then Ian once).
2. The page's AI odds equal `plplan.ai_distribution`'s in every position of a test line, mixed over the turn's Quick Claw rolls (a test).
3. The page's outcomes for a turn equal the simulator's own enumeration, and following one continues from exactly that position (a test).
4. Ian's Gardenia box 3 line, built by the snippet at the end, shows the speeds, damage ranges and AI odds the snippet prints on the same tree (the helper checks, then Ian looks).
5. The diff touches only the OxiDex, one new module and one new calc patch, and the simulator, AI and scorer files are unchanged (`git diff --stat`).

## What a turn shows

Each position shows both active Pokemon (HP, status, stat stages, item, ability), both benches, and the field: weather and its turns left, screens, hazards, Tailwind and Trick Room. With it:

- Both Speeds after every modifier, and the turn order, with priority and the Quick Claw's chance.
- The trainer AI's odds for every move and switch, from `plplan.ai_distribution` mixed over `plplan.quick_outcomes`, since the AI reads the turn's Quick Claw rolls.
- Each move's AI score, so Ian can see how close the AI is to changing its pick. `plplan._build` reads each slot's score odds through `fightai.score_slot` and `plplan.outcomes`, and the page reads them the same way.
- The damage rows both ways, from the simulator's own numbers (`Battle.rolls` and `Battle.damage`): every roll as HP and percent, the crit, and the chance to knock out from the current HP. They match the calc, since both use the same damage code.
- A warning on any move or ability in the fight that `simulator-gaps.md` still lists as open. A move is matched through its effect in `res/moves`, since the list's rows name effects and shorten long move lists.

The menu is every move the game would let Ian choose (with PP, and not barred by Taunt, Disable, Encore, Torment or a Choice lock) and every living bench member. `plplan.options` drops the moves that would do nothing, so it is not the menu.

When he picks his action, the page lists the turn's outcomes, most likely first. For each of the AI's choices, weighted by its odds, `plplan.turn_outcomes` gives the positions the turn can reach with their chances, the damage rolls already in bands and like positions merged. Each line says what happened (the AI's move, hits, crits, effects, a sleep's length), both sides' HP after (a band where outcomes merged), and any faint. He follows one, or presses Roll to draw one at real odds. After a faint he picks his replacement, and the trainer's replacement branches the tree by its odds.

He can also set a position by hand (HP, status, stages, weather, field) and read the odds there, as the Gardenia scripts did for Golbat at two-thirds HP.

## The tree

Every position is a node, kept with `plplan.clone`. The path to a node shows its chance (the product of the outcomes followed), and any node can be reopened to choose differently. The tree's summary gives the share of the chance its played branches cover, and the share of that ending in a win, from the played leaves alone; by Ian's answer no planner fills in the rest.

A line saves as a file under `~/oxide-lines/` that reloads to the same tree: the party, the trainer and its branch, and each node's action with the outcome followed, recorded as the enumeration's choices so that a replay reproduces every position exactly. It exports as a plain transcript too, and the Overseer can open the file in Python to check a position.

A button for "the game did something else here" saves the node, the path to it and Ian's note under `~/oxide-lines/mismatches/`. The Overseer turns each into a gap row; a fix to a behaviour outside the approved list still needs Ian's yes.

## The party

From the calc, a Fight button under its party (a new patch in `calc/VENDORED.md`, checked by `test_m8`) sends the six species of `currentParty`, each with its "My Box" set from `customsets` (level, nature, ability, item, moves, IVs, EVs), and the trainer on the calc's right side. A set becomes a simulator record through `plteam.record`, keeping its own IVs and EVs. The held items go in `st["held"]`, which `perfectline.make_battle` uses in place of the scorer's own item rule.

From a reading, Ian picks the fight and box 1, 2 or 3, and the tester loads that box as `plgoal3` reads it (`roll`, `cut`, `met`, `level`, `records`): at the reading's level, with each member's legal pool, and with the scorer's six and movesets as the starting party where a reading has chosen them. The box stays inside the tester and leaves the calc's box alone, since the calc's box follows the live save.

The warnings flag, without blocking, a nature other than the reading's (Hardy), IVs other than 15, an ability other than the reading's slot, a move outside the member's pool at that level, an item the split's stock lacks (`fightsim.player_items`) or more copies than it holds, and a level above the reading's. A calc party gets the level and item warnings against the fight's split, and the move warning against its line's pool from the line's earliest catch in that split.

## The trainer

Any trainer the readings can parse (`plscore.parse_fight`), with the variant that follows the player's starter. The trainer's file may come from any branch, read with `git show`, so a draft such as the Galactic study branch's can be tested before it lands; everything else comes from the current tree.

## Not in version 1

- The planner's advice and a line win rate. Ian chose battle only on 2026-10-14; ask him before adding either. The pieces exist: `Planner.decide` took 5.5 seconds in the measurement below, and its `last_parts` holds each option's chance of losing and expected faints.
- Double and tag battles. There is no doubles turn enumeration yet, and the readings leave tag battles out until a doubles planner exists.
- Gauntlet chains, carrying HP, PP and status from one fight to the next (`plplan.CARRY` holds a section's carried state).

## Measured on 2026-10-14

Gardenia box 3 with Ian's six, at bf04a3fea, in one process:

| Step | Time |
|---|---|
| `ai_distribution`, the AI's odds on turn 1 (Solrock: Stealth Rock 75%, Zen Headbutt 25%) | 4 ms |
| `turn_outcomes` for Razor Leaf against Stealth Rock (3 merged positions) | 1 ms |
| `Planner.decide`, not used in version 1 | 5.5 s |

This snippet builds the fight as the readings do, and is the base of check 4:

```python
from tools.oxide.balance import plgoal3 as g, plscore, plplan, fightsim as fs

f = next(x for x in g.fights() if x["slug"] == "gardenia")
whole = g.roll(f["split"], 3)
caught = g.cut(whole, f)
key, v, trainer = g.met(f, whole[0].species)
recs = g.records(caught, f, g.level(f, trainer), 3)
prep = plscore.prepare(plscore.parse_fight(key), given_side=recs)
st = prep["st"]
st["item_stock"] = dict(fs.player_items(f["split"]))
boss_keys, flags, _s = prep["variants"][v]
keys = {r["species"]: f"p{i}" for i, r in enumerate(recs)}
SETS = {"Tsareena": ["Razor Leaf", "Rapid Spin", "Double Kick", "Taunt"],
        "Carbink": ["Reflect", "Ancient Power", "Draining Kiss", "Rock Throw"],
        "Nuzleaf": ["Fake Out", "Silver Wind", "Snarl", "Bullet Seed"],
        "Golbat": ["Dual Wingbeat", "Leech Life", "Bite", "Poison Sting"],
        "Breloom": ["Bullet Seed", "Mach Punch", "Headbutt", "Leech Seed"],
        "Corvisquire": ["Dual Wingbeat", "Drill Peck", "Steel Wing", "Taunt"]}
for s, mv in SETS.items():
    st["moves"][keys[s]] = mv
b = plplan.make_battle(st, [keys[s] for s in SETS], boss_keys, flags, 0)
b.quick = {}
print(plplan.ai_distribution(b))
```

The two scripts of 2026-10-13 that the tester replaces asked what Ian's line raised: the speeds in the sun, each hit's range as a share of HP with its crit, and the AI's odds at positions set by hand (Golbat in on Natural Gift at two-thirds HP, Exeggutor at three quarters, Nuzleaf confused by Swagger at +2 Attack). The tester answers those questions without a script.
