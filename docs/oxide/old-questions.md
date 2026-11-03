# The tracker's older questions, settled or put as decisions (2026-11-02)

## Ian's answers (2026-11-02)

Ian answered all sixteen open questions on 2026-11-02. The numbers are the sheet's.

1. The AI and held items: only the moves that fail (Safety Goggles against powder, the Air Balloon in the AI's Ground checks). Being built on `overseer-ai-items`.
2. The plain-English account of the AI: after alpha 1 (a Scheduled entry in the tracker).
3. Element 7's placeholder prices: they stand as they are.
4. The fourteen item descriptions: they stand as they are.
5. The seventeen dialogue drafts: they all stand.
6. The regional dex order: the question is closed, and the national dex stays.
7. The zone-by-zone land pass and the water re-authoring: both dropped; today's tables stand.
8. The honey tree tables: they stand as drafted.
9. The Box sim's line ratings: kept as the tab's interim until the encounter worth is built at Ian's word.
10. The Amity Square and Snowpoint casts: they stand.
11. The calculator check: done from the alpha's battle recorder as part of Ian's QA checks (five recorded hits compared with the calculator; `ingame-checklist.md`, section 2).
12. The line tester: Ian looks once now. The check 4 snippet was rerun on 2026-11-02 and still prints Solrock's Stealth Rock 75 and Zen Headbutt 25 percent.
13. The weather rocks: swap ten now, the list going to Ian first on `overseer-weather-rocks`. Flint's waits for the League's pass, and Moira's on Mt. Coronet 5F for her next pass.
14. The Kaizo study's retune list: retired, with its Scheduled entry.
15. Charjabug's Thunder Stone evolution: kept.
16. The `plgoal3.py` docstring fix: yes. It is done on `overseer-ai-items`.

The nine the sheet found settled or overtaken (Justified and Rattled, Sand Force and Sand Rush, Wonder Room, Octolock and Teatime, the Kaizo study's six decisions, the QA pass's first decision, the four leftover worktrees, the Veilstone Elekid, the Frontier Brain teams) are closed on the tracker. The Elekid's own line closes when `overseer-elekid-gift` lands.

Ian asked on 2026-11-02 to settle the tracker's older open questions, "a lot has been set in stone since then". This sheet takes every question the tracker's "Waiting on Ian" list names that is older than the current split work, follows each to its entry and its archive wording, and checks it against the standing rulings, the landings since it was asked and today's files on `origin/oxide` (9447ef458). The Overseer puts the open ones to Ian in dialogs from the sections below. Nothing in game data, tools or `res/` changed for this sheet.

## Summary

Nine of the 25 questions are already settled by a later ruling or overtaken by the work, each with its evidence below; the Overseer can close them on the tracker without asking. Sixteen are left. Each is one decision with its options, the recommended one first:

1. Element 6, the AI and the new held items: teach it only the two cases where the engine makes the move fail (Safety Goggles against powder, the Air Balloon beside Levitate's checks).
2. Element 6, the plain-English account of how Oxide's AI decides: write it now, while the four changes of play are settled.
3. Element 7's placeholder prices: keep them as final, since no new item is sold and money is loose.
4. Element 7's fourteen draft descriptions: approve them as they stand.
5. The dialogue drafts of `main-scripts` and `main-production` (seventeen entries): approve them as they stand.
6. The regional dex order: close the question, since the game always shows the national dex and nothing reads the order.
7. The water biome draft and the zone-by-zone land pass: the unworked splits take their zones in their own passes, and the worked zones wait for after alpha 1.
8. The eight honey tree tables: approve them as drafted.
9. The Box sim's line ratings: keep them as the tab's interim until the encounter worth is built at Ian's word.
10. The Amity Square and Snowpoint City casts: approve them as they stand.
11. The one damage roll against the calculator: let the alpha's battle recorder supply it.
12. The line tester's checks 1 and 4: Ian looks once, about ten minutes, now that its tests pass on today's tree.
13. The weather rocks that do nothing: there are twelve today, not three; swap the ten outside Ian's current designs for working items.
14. The Kaizo study's retune candidates: retire the list, since the drafts it softens no longer land.
15. Charjabug's second evolution by Thunder Stone (the QA pass's finding 15): keep it.
16. A one-line docstring fix in the scorer file `plgoal3.py` (the same finding): yes.

Next steps: Ian answers the sixteen in dialogs (a few minutes each, about an hour in all), the Overseer records the answers, closes the nine settled entries on the tracker, and books the work the answers start (a few hours for items 1, 2 and 13; the rest are a tracker line or a small data commit).

## Settled or overtaken (nine)

**Element 6's first change of play, Justified and Rattled (overtaken).** The question was whether the AI should avoid Dark, Bug and Ghost attacks into a known Justified or Rattled holder, which gains a stage from them. Every one of the fifteen species, in twelve lines, that has either ability has it in its hidden slot (Absol, Growlithe and Arcanine, Lucario, Gallade, Bonsly and Sudowoodo, Snubbull and Granbull, Poochyena, Ledyba, Magikarp, Dunsparce, Clamperl, Whismur). The player gets a hidden ability only through the game's one Ability Patch, so the AI would meet such a target almost never. Revisit only if a scripted hidden-ability gift of one of these lines is ever added.

**Element 6's second, Sand Force and Sand Rush in the doubles Sandstorm check (overtaken).** The AI's double-battle check for using Sandstorm counts Sand Veil and Rock types, as vanilla does, and the question was whether to count Sand Force and Sand Rush too. Of the 34 double-battle trainers, two carry Sandstorm (Double Team Jo and Pat, Twins Emma and Lil), and neither has a Sand Force or Sand Rush partner; the scorer reads no double battle. Revisit if a doubles team is built around either ability.

**Element 6's fourth, when to use Wonder Room (overtaken).** No trainer knows Wonder Room. The one Wonder Room fight is Dahlia's permanent room, where the AI already scores the move -10 (443023c845), so the question has no fight to act in. Revisit if a team is given the move.

**Octolock and Teatime's new AI command (overtaken).** The AI cannot see that a target is already octolocked, or that no one holds a Berry for Teatime, without a new command. No trainer knows either move, so the command would change nothing. Revisit if a team is given either move.

**The Kaizo study's six decisions on the later ordinary trainers (settled by the rulings of 2026-10-13 and 2026-10-29, and overtaken).** The study's comb (`task4-summary.md`, 2026-10-07) asked six things, each recommended "accept". The comb's batch landing is retired and each split's pass designs its own trainers (Ian, 2026-10-29), which settles the first, ordinary trainers reading past the faint band "until step 15", since step 15 is dropped too. Rocco's Clefable (Maylene's split) landed with that split's pass, and a move off a species' list now goes on its egg list (Ian, 2026-10-29). Wake's split and Byron's split were rebuilt by their passes (2026-10-31 and 11-01), so the comb's weather teams, Brennan's Shedinja and Vincent's rain team are not in the game; the rain teams those splits have today (on Route 213 and in Pastoria's gym) are the passes' own, and the standing rulings let trainers keep weather. HQ's grunts with two Pokemon fall under the standing rule of 3 to 5 Pokemon, which HQ's split pass applies. Somnu and Tyche and Hermes were superseded on 2026-10-13 and are in the game as Ian's designs.

**The QA pass's first decision, how the resumed readings build their boxes (settled on 2026-10-21).** The waiting list still names it, but Ian answered it the same day: a fight read alone builds its box without the seed's earlier fights, accepted, "that's just something I can account for when I see the analysis". The full readings it served were dropped on 2026-10-29.

**The QA pass's four leftover worktrees (overtaken).** `study-gardenia-base`, `balance-variants`, `sf17/base` and `sf17/stage` are no longer in `git worktree list`; only the local branch `study-gardenia-base` remains, which the QA pass found holds nothing outside `oxide` or git's history. The Overseer may delete that branch with the tracker's other unlanded branches.

**The Veilstone Elekid (settled by Ian today).** The worktree `overseer-elekid-gift` is removing the gift on 2026-11-02: the man in Veilstone's north-east house gives nothing, with its in-game check written. The tracker's line closes when that branch lands.

**The Frontier Brain teams (overtaken).** "He builds them": four are built, placed and landed (Dahlia, Darach and Caitlin, Thorton, Argenta). Palmer's place waits on the Battle Zone's or the League's split, which the Scheduled list already holds.

## Open (sixteen)

### 1. The AI and the new held items

The AI does not see most of element 7's held items on its target, so it plays as if they were not there: it will hit a Rocky Helmet with contact moves, hit a Weakness Policy holder super effectively, use a powder move into Safety Goggles, and so on. Each fix would make it play differently, so each is Ian's. The player can win one each of the Rocky Helmet, Weakness Policy, Absorb Bulb, Cell Battery, Eject Button, Safety Goggles, Covert Cloak, Clear Amulet, Loaded Dice, Binding Band and Air Balloon behind optional trainers (`reward-placements.tsv`); the Red Card and Mirror Herb are placed nowhere for the player. The AI's damage figure already sees the Air Balloon (`battle_lib.c` reads it in the type chart walks). Any AI change also needs its mirror in the simulator's AI, which Ian's yes here would approve.

Question: what should the AI learn about the player's held items?

| Option | What it does | Cost |
|---|---|---|
| A (recommended) | Only the cases where the engine makes the move fail: a powder move into Safety Goggles scores -10, beside Grass and Overcoat in Basic's powder check, and the Air Balloon joins Levitate in the script's Ground checks | about an hour of a worker helper: two script rules, their simulator mirror, a test each |
| B | Everything on the list, including the judgement calls (avoid contact into a Rocky Helmet, avoid a super-effective hit into Weakness Policy, the absorbers, Covert Cloak and Clear Amulet against added effects) | about a day; it makes each of the player's eleven items worth less, so it is a small rise in difficulty wherever the player uses one |
| C | Nothing; the player's single copy of each item keeps its edge | none |

A is recommended because it is the same kind of rule as Basic's existing refusals of moves that cannot work, while B's judgement calls take value from items the player earns once each.

### 2. The plain-English account of Oxide's AI

Ian asked on 2026-09-27 for a step-by-step account of how Oxide's trainer AI decides, in the manner of pokemow.com's Gen 4 AI pages, with every change from vanilla marked, "once the element is finished". The raw material is in `docs/oxide/battle-ai/` (about 75,000 words across ten files); nothing reader-sized exists. With this sheet settling the element's last changes of play, the element is finished.

Question: when should the account be written?

| Option | Cost |
|---|---|
| Now, before alpha 1 (recommended), so Ian plays the alpha knowing what the AI will do | about two to three hours of a worker helper, one doc of a few thousand words |
| After alpha 1 | the same, later |
| Not at all; the README and the flags guide stand | none |

### 3. Element 7's prices

The new items carry placeholder prices on Platinum's scale, set "until shops stock them". Since then Ian ruled that new held items go behind optional fights and are not sold (2026-09-29), the Game Corner sells only its gated TMs and old prizes (2026-10-06), and the Mints, Capsule, Patch and Bottle Caps are rewards. No shop stocks any of them, so a price shows only when the player sells the item, for half. Money is already loose: the Pocket PC's Rare Candies sell (the backlog's money note).

| Price | Items | Sells for |
|---|---|---|
| 20 | Roseli Berry | 10 |
| 200 | the 19 held items (Ability Shield, Absorb Bulb, Air Balloon, Assault Vest, Binding Band, Cell Battery, Clear Amulet, Covert Cloak, Eject Button, Eviolite, Fairy Feather, Loaded Dice, Mirror Herb, Punching Glove, Red Card, Ring Target, Rocky Helmet, Safety Goggles, Weakness Policy) | 100 |
| 1,000 | Pixie Plate | 500 |
| 2,100 | Ice Stone | 1,050 |
| 10,000 | Ability Capsule, Ability Patch | 5,000 |
| 20,000 | the 21 Mints, Bottle Cap | 10,000 |
| 60,000 | Gold Bottle Cap | 30,000 |

Question: do these prices stand as final?

| Option | Cost |
|---|---|
| Yes, as they stand (recommended): nothing is bought, and a sale only adds money the player already has plenty of | none |
| Set them to 0 so nothing earned can be sold for money | one data commit, a few minutes; the Bag then refuses to sell them, as for key items |
| Ian names different prices | a few minutes per price |

### 4. Element 7's draft descriptions

The Bag's description box is 216 pixels across three lines, narrower than HeartGold's, so the cloud job rewrote the descriptions that did not fit. Fourteen of the new items' descriptions differ from hg-engine's text today: the ten rewritten to fit, the two Bottle Caps, which now say what they do where hg-engine's say "certain people are delighted to be given one", and the Air Balloon and Fairy Feather, for which the local hg-engine copy has no text. Each was measured with `textfit.py`; none has been looked at in game. A slash marks a line break, and hg-engine's double hyphens are shown as commas.

| Item | Oxide's draft | hg-engine's text, where it has one |
|---|---|---|
| Ability Patch | A patch that changes the Ability of a / Pokémon to its rarer hidden Ability. | A patch that can be used to change the regular Ability of a Pokémon to a rarer Ability. |
| Ability Shield | An item to be held by a Pokémon. This / cute shield stops others from changing / the holder’s Ability. | ...This cute shield protects the holder from having its Ability changed by others. |
| Absorb Bulb | An item to be held by a Pokémon. It / raises Sp. Atk if the holder is hit by a / Water-type attack, but only once. | ...Boosts Sp. Atk if the holder is hit by a Water-type attack, but only once. |
| Air Balloon | An item to be held by a Pokémon. The / holder floats in the air until it is hit. / Once hit, the balloon bursts. | |
| Bottle Cap | A lovely silver bottle cap. It maxes out / one stat of a Pokémon, as if its IV for / that stat were 31. | A lovely silver bottle cap. Certain people are delighted to be given one of these. |
| Cell Battery | An item to be held by a Pokémon. It / raises Attack if the holder is hit by an / Electric-type attack, but only once. | ...Boosts Attack if the holder is hit by an Electric-type attack, but only once. |
| Covert Cloak | An item to be held by a Pokémon. This / cloak conceals the holder, shielding it / from moves’ added effects. | ...This cloak conceals the holder, protecting it from the additional effects of moves. |
| Fairy Feather | An item to be held by a Pokémon. This / faintly gleaming feather boosts the / power of Fairy-type moves. | |
| Gold Bottle Cap | A lovely gold bottle cap. It maxes out / every stat of a Pokémon, as if all its / IVs were 31. | A lovely gold bottle cap. Certain people are delighted to be given one of these. |
| Loaded Dice | An item to be held by a Pokémon. These / dice always roll high, so multistrike / moves hit more times. | ...This dice always rolls a good number, ensuring multistrike moves hit more times. |
| Mirror Herb | An item to be held by a Pokémon. The / holder copies a foe’s stat increases, / but only once. | ...This herb allows the holder to mirror an opponent’s stat increases, but only once. |
| Roseli Berry | If held by a Pokémon, it weakens a / foe’s supereffective Fairy-type / attack. | If a Pokémon holding this Berry is hit with a supereffective Fairy-type move, the power of that move will be weakened. |
| Safety Goggles | An item to be held by a Pokémon. These / goggles protect the holder from / weather damage and from powder. | ...These goggles protect the holder from both weather-related damage and powder. |
| Weakness Policy | An item to be held by a Pokémon. Attack / and Sp. Atk sharply rise if the holder / is hit by a move it’s weak to. | ...Attack and Sp. Atk sharply increase if the holder is hit by a move it’s weak to. |

Question: do the fourteen descriptions stand?

| Option | Cost |
|---|---|
| Yes, as they stand (recommended); the Bag's look is checked when the item kit is next opened in game | none |
| Ian edits the ones he names | a few minutes each, a fit check with `textfit.py`, and a rebuild |

### 5. The dialogue drafts

Two branches reworded lines for Oxide's story order, both landed long since and in the game today. `main-scripts` (2026-09-26) rewrote the lines that no longer fit once the Battle Zone opened after Galactic HQ, the legendary pool drew the lake species at random, the Underground closed and the free stones went; `main-production` (2026-09-30) wrote the Mining Museum researcher's refusal before Cycling Road, in his own word order. Each line as the game has it today:

| Where | Who | Line |
|---|---|---|
| Snowpoint City | the sailor, before Galactic HQ | The Battle Zone? Not while Team Galactic has the whole region on edge! Put a stop to them at their base in Veilstone City, and I’ll sail you there! |
| Snowpoint City | Cynthia, first voyage | Cynthia: Cyrus has his Red Chain now. He will make for Mt. Coronet soon. He wants a world that answers to him alone. No one would want that. The world I want to see is one where everyone can share their joy. Where Pokémon and the people around them can be happy for each other. When Cyrus makes his move, we will need to be ready to stop him. |
| Snowpoint City | Cynthia, after | So I want you to grow even stronger. The Battle Zone is full of tough Trainers. It’s the best place to train. I came all the way here just so I could say that to you. Your horizons will expand again if you visit the Fight Area. I hope our paths cross again! |
| Fight Area | Barry, the team-up | (Barry): (player), I tried to get into the Battle Frontier, which happens to be right here. Then these guys came along and got in my face about it. Like, they’re saying they want to test me if I’m good enough and all that. Like, as if I need to prove anything. So, let’s team up, you and me. Let’s show those guys how good we are! |
| Fight Area | Volkner, battle line | Volkner: I don’t know how I managed to get myself into this, but... Show me the skills that won you my Beacon Badge! |
| Fight Area | Volkner, without the Badge | Volkner: Hold on, Flint. This Trainer hasn’t been to my Gym. Come to Sunyshore City and win my Beacon Badge first. Then Flint and I will take you both on. |
| Fight Area | Barry, then | (Barry): What? Seriously?! (player), go get that Badge, and get it fast! I’ll wait right here. If you’re late, I’m fining you $100 million! |
| Fight Area | Barry, waiting | (Barry): You still don’t have Volkner’s Badge? Go to Sunyshore City and win it! I’m not getting into the Frontier till you do! |
| Fight Area | Buck, introducing himself | Hey, hey. Howdy, Trainer. The name’s Buck. I’m usually training at the Survival Area or Stark Mountain. You should come up there. You’ll get toughened up for sure! |
| Victory Road 1F | Dawn | Dawn: (player)! I knew you’d come through here. You’re going to take on the Pokémon League, aren’t you? Then you’ll have to get past me first! I’ve been training hard for this! |
| Victory Road 1F | Lucas | Lucas: (player)! I knew you’d come through here. You’re off to the Pokémon League, right? Let’s see if you’re ready! I’ve been training hard for this! |
| Victory Road 1F | Dawn and Lucas, after | Dawn: Wow... You really are ready. Go show the Elite Four your stuff! I’ll be cheering for you! / Lucas: Yeah, you’re ready, all right. Go take on the Elite Four! I’ll be rooting for you! |
| Acuity Cavern, Lake Verity | the lake scenes | UXIE and MESPRIT replaced by the drawn species' name ("(species) disappeared deep into its...", "(species) flew off somewhere...", "that was (species)") |
| Eterna City | the woman, and the Underground Man | The man next door to the Pokémon Center dug tunnels under Sinnoh. They’re all sealed off now. What a shame! / You can call me the Underground Man. Everyone else does. I dug tunnels all under Sinnoh, but they’ve been sealed off for good. Sigh... I get so lonely sometimes... |
| Route 207 | the woman, without the stones | I have seen a young girl going into Wayward Cave, north of here below the Cycling Road. She hasn’t come back yet! Would you please go look for her? / Oh, you found her! Thank you so much! |
| Mining Museum | the researcher, before Cycling Road (`main-production`) | On the verge of a breakthrough, I am, to achieve extraction from Fossils. Parts for my machine, Eterna sends by way of Cycling Road. Come back after riding that road, and ready my machine will be! |
| Location names | the starter's met location | Rowan’s Briefcase |

Every line still fits the rulings since: the Battle Zone still opens after Galactic HQ, before Volkner, so the Badge path is the one the player meets, and fossils still wait for Cycling Road. The one known gap stays cosmetic: the Poketch's Marking Map shows a drawn roamer with Mesprit's icon.

Question: do the drafts stand?

| Option | Cost |
|---|---|
| Yes, all as they stand (recommended) | none |
| Ian rewords the lines he names | a few minutes a line, a fit check and a rebuild |

### 6. The regional dex order

On 2026-09-26 the pick-list grew by 51 lines, appended at its end, and their place in the regional dex was left to Ian (`docs/oxide/encounters/regional-dex-proposal.md`, 2026-09-30). The proposal places each by the curated dex's own rule, lines together in national dex order of their first member. Since then the game shows the national dex always (element 8), the in-game Sinnoh dex is still vanilla's 210, and nothing in the game or the tools reads this order.

Question: what happens to the regional order?

| Option | Cost |
|---|---|
| Close the question; the 51 stay at the end of the pick-list, since nothing reads the order (recommended) | none |
| Adopt the proposal's rule as a `regional` column in the pick-list | about an hour of OxiDex work, no game change |
| A Sinnoh-style order by where the player meets each line, for all 463 | a few hours, and a real in-game regional dex would be separate, unplanned work |

### 7. The water biome draft and the zone-by-zone land pass

The blind encounter review of 2026-09-29 led Ian to two pieces of encounter work that never ran. The land tables were to come to him zone by zone, with the late game's few new lines, Fairy in Wake's and Byron's land, Starly's line evolving in the wild, Delibird earlier, and Grimer and Muk on Fuego Ironworks' water and Bibarel on Routes 205 south and 218. The water was to be re-authored afterwards, once he had read the biome draft (`docs/oxide/encounters/water-lint-draft.md`), which asks one decision: each capture area's water biome. The lint carries 854 water warnings, none acted on. The tables have hardly changed since 2026-09-30, and every boss from Roark to Candice has since been designed and checked against boxes rolled from today's tables, so changing a worked zone's catches now reopens those checks.

Question: when is the encounter work done?

| Option | Cost |
|---|---|
| Split it (recommended): each unworked split's pass, HQ's onward, takes its zones' land swaps and water with it, with the biome draft's rows for those zones put to Ian then; the worked zones (Roark to Candice) wait for after alpha 1, with the alpha's notes showing which feel thin | a session or two per split, inside passes already planned; a Scheduled entry for the early zones |
| All of it after alpha 1, in one pass | a few sessions with Ian later, and each early boss's counterpiece rechecked where a swap reaches its box |
| All of it now, before alpha 1 | the same sessions now, delaying the alpha, and the checks of Roark's to Candice's bosses repeated |
| Drop both; today's tables stand and the water warnings stay warnings | none |

### 8. The honey trees

Since 2026-09-26 the eight honey tree tables read one table per badge count, each rolled 10 percent nothing, 70 common and 20 uncommon; the four Munchlax trees and their rare tier are gone. A tree's catch counts for the capture area its map stands on. The tables are a first draft, bugs and tree dwellers with Heracross climbing from a 1 percent to the head of the uncommon tier. Their levels sit well under each split's cap, by 12 at one badge to 28 at eight; with soft caps and the Pocket PC's Rare Candies, a low catch level costs only time, and the catch learns its list on the way up. The two shakes at one badge and at five stay in the in-game checklist whatever the answer.

| Badges | Split (cap) | Levels | Common | Uncommon |
|---|---|---|---|---|
| 1 | Gardenia (26) | 10 to 14 | Combee, Sewaddle, Grubbin, Aipom, Dottler, Burmy | Seedot, Shroomish, Bounsweet, Cherubi, Munchlax, Heracross |
| 2 | Fantina (33) | 14 to 18 | Combee, Sewaddle, Grubbin, Aipom, Joltik, Burmy | Nuzleaf, Shroomish, Steenee, Munchlax, Fomantis, Heracross |
| 3 | Maylene (38) | 19 to 23 | Combee, Sewaddle, Grubbin, Joltik, Aipom, Fomantis | Yanma, Nuzleaf, Munchlax, Steenee, Scyther, Heracross |
| 4 | Wake (44) | 23 to 27 | Vespiquen, Swadloon, Charjabug, Joltik, Yanma, Fomantis | Munchlax, Nuzleaf, Scyther, Trumbeak, Snom, Heracross |
| 5 | Byron (53) | 28 to 32 | Vespiquen, Swadloon, Charjabug, Joltik, Yanma, Emolga | Scyther, Nuzleaf, Toucannon, Snom, Larvesta, Heracross |
| 6 | Candice (56) | 32 to 36 | Vespiquen, Leavanny, Vikavolt, Galvantula, Yanma, Frosmoth | Scizor, Snorlax, Shiftry, Toucannon, Larvesta, Heracross |
| 7 | HQ to Volkner (60 to 68) | 40 to 45 | Vespiquen, Leavanny, Vikavolt, Galvantula, Yanmega, Frosmoth | Heracross, Scizor, Snorlax, Toucannon, Larvesta, Skarmory |
| 8 | Barry and the League (71 to 78) | 45 to 50 | Vespiquen, Leavanny, Vikavolt, Galvantula, Yanmega, Scizor | Heracross, Larvesta, Snorlax, Toucannon, Frosmoth, Skarmory |

Question: do the tables stand?

| Option | Cost |
|---|---|
| Yes, as drafted (recommended) | none |
| Keep the species and raise the levels to ride the land tables (about 8 to 2 under the cap) | eight level pairs in one JSON and a rebuild, about half an hour; no box moves, since the boxes stage a catch by the cap |
| Ian edits the species in the OxiDex | his time, then a rebuild and the availability counts rerun |

### 9. The Box sim's line ratings

The OxiDex's Box sim tab rates each of the 240 pick-list lines S to D (`docs/oxide/encounters/values.json`), a first draft of 2026-09-26 from nuzlocke tier lists and Smogon tiers, which it mixes with base stats and the pick-list tier to pick a best box. Today 20 lines are S, 62 A, 84 B, 54 C and 20 D. The ratings reach no reading: the scorer's boxes are rolled by each area's odds and never read them. On 2026-10-15 Ian asked for each encounter's worth from the scorer instead of broad approximations, and the Scheduled list holds that build "at Ian's word".

Question: what happens to the ratings?

| Option | Cost |
|---|---|
| Keep them as the tab's interim, replaced when the encounter worth is built at Ian's word (recommended) | none now |
| Ian corrects the ratings he disagrees with | his time, a file edit per change |
| Build the encounter worth now | about a day of a worker helper plus machine time, put to Ian first as checks, as the Scheduled entry says |

### 10. The Amity Square and Snowpoint City casts

Two capture areas were built on 2026-09-25 ahead of their maps and are in use: Amity Square's lawn in Fantina's split, at very low levels because only small Pokemon walk in with you, and Snowpoint City's harbour in Candice's split, rods only (its land table has a rate of 0, so its land list is never met). Both were drafts for Ian to change in the tool; neither has changed since. Amity Square has been in goal 3's boxes since 506b11dbec, so the bosses from Fantina's split on were checked with it.

| Area | Method | Levels | Cast |
|---|---|---|---|
| Amity Square (cap 33) | grass, morning | 8 to 11 | Snubbull, Swablu, Azurill, Buneary, Glameow, Fomantis, Klefki, Pikachu |
| | day slots | | Minccino, Smoochum |
| | night slots | | Drifloon, Purrloin |
| Snowpoint City (cap 56) | Old Rod | 16 to 22 | Spheal, Seel, Shellos, Snorunt |
| | Good Rod | 28 to 38 | Spheal, Seel, Snover, Lapras |
| | Super Rod | 38 to 52 | Sealeo, Dewgong, Froslass, Lapras |

Question: do the casts stand?

| Option | Cost |
|---|---|
| Yes, both as they stand (recommended) | none |
| Ian changes them in the OxiDex | his time, a rebuild, and a recheck of the bosses whose boxes the change reaches (Fantina's split on for Amity) |

### 11. One damage roll against the calculator

The OxiDex's calculator, which the scorer and Ian's planning both lean on, has never been compared with a hit in the running game. The checklist asks Ian to note one hit's levels, stats and damage in melonDS and check it falls in the calculator's range. The calculator has had many fixes since (the move reworks, Reckless, Fury Cutter, Thunderous Kick's contact), each against the engine's code, never against the game.

Question: how is the calculator checked against the game?

| Option | Cost |
|---|---|
| From the alpha's battle recorder (recommended): after Ian's first recorded session, the Overseer compares five recorded hits with the calculator | about an hour of the Overseer's time, nothing for Ian; it needs the recorder's bridge to log stats and HP, which the first page already lists for checking before the alpha |
| Ian does the one roll by hand in his next playtest | about five minutes of his time |
| Drop it | none, and the calculator stays unchecked against the game |

### 12. The line tester's checks 1 and 4

The line tester (an OxiDex Battle tab where Ian plays a hand-made line on the readings' simulator and AI) landed on 2026-10-21 with its checks 2, 3, 5 and 6 passing. Check 1 is Ian pressing the calculator's Fight button once; check 4 is Ian looking at his Gardenia box 3 line on the page against the snippet's printout. The tester's own suite passes on today's tree, 11 of 11 (run for this sheet). Since 2026-10-22 the scorer only spot-checks, so the tester is a tool for the fights Ian finds too hard.

Question: how is the line tester closed?

| Option | Cost |
|---|---|
| Ian looks once now (recommended): the Overseer reruns the snippet for check 4 and sends him the link | about ten minutes of his time |
| Close it as tested; any fault he meets in use is a bug | none |
| Retire the tester | none, and the Battle tab is left unmaintained |

### 13. The weather rocks that do nothing

In Oxide, as in Platinum, weather from Drought, Drizzle, Sand Stream or Snow Warning lasts the whole battle, and a rock extends only weather set by a move, so a rock on an ability setter does nothing. The tracker named three (Flint's Torkoal, Moira's Abomasnow on Mt. Coronet, Ace Trainer Jonah's Hippowdon). Today there are twelve, none of whose holders knows the weather move:

| Trainer | Pokemon | Ability | Rock |
|---|---|---|---|
| Ace Trainer Dalton | Abomasnow | Snow Warning | Icy Rock |
| Ace Trainer Jonah | Hippowdon | Sand Stream | Smooth Rock |
| Ace Trainer Shannon | Ninetales | Drought | Heat Rock |
| Double Team Zac and Jen | Pelipper | Drizzle | Damp Rock |
| Elite Four Flint | Torkoal | Drought | Heat Rock |
| Fisherman Walter | Politoed | Drizzle | Damp Rock |
| Moira, Mt. Coronet 5F (`galactic_grunt_mt_coronet_5f_1`) | Abomasnow | Snow Warning | Icy Rock |
| Sailor Damian | Pelipper | Drizzle | Damp Rock |
| Skier Edward | Abomasnow | Snow Warning | Icy Rock |
| Swimmer Evan | Politoed | Drizzle | Damp Rock |
| Tuber Chelsea | Pelipper | Drizzle | Damp Rock |
| Worker Conrad | Torkoal | Drought | Heat Rock |

Question: what happens to the dead rocks?

| Option | Cost |
|---|---|
| Swap the ten outside Ian's current designs for working items, each picked for its team under the no-repeats and variety rulings, the list shown to Ian before it lands; Flint's goes with the League's pass and Moira's with Ian's Somnu and Moira draft (recommended) | about an hour, one data commit; not material for the ordinary trainers, and a one-item change on the three Ace Trainers |
| Swap each as its split is worked | none now; the ones in worked splits stay dead until touched |
| Make ability weather last five turns, eight with a rock, as in Generation 6 | an engine change and a simulator change; it softens every weather team, Gardenia's sun six among them, so it is material for every weather fight |
| Leave them; each holder plays as if itemless | none |

### 14. The Kaizo study's retune candidates

On 2026-10-07 the study proposed softer versions of its own drafts that read too hard on its simulator: Cynthia, Maylene, Flint, Lucian, Aaron, Bertha, Barry 3, Saturn 1, Argo, Barry 6 and Ace Trainers Jose, Saul and Mariah (`~/oxide-trials/kaizo-teams/out/retune-proposals-not-approved/`). Ian approved none, and the Scheduled list weighs them as each split is worked. Since then the comb's drafts no longer land (2026-10-29), and Maylene, Barry 3 and Argo 1 are in the game as Ian's own designs, with Saturn 1 his next draft. A retune of a draft that will never land has nothing to tune.

Question: what happens to the retune list?

| Option | Cost |
|---|---|
| Retire it and its Scheduled entry; each later split's pass may still read the proposals for ideas, as it reads the drafts (recommended) | a tracker edit |
| Keep weighing each as its split is worked | a few minutes per split, as today |

### 15. Charjabug's Thunder Stone

The QA pass of 2026-10-21 (finding 15) found that Charjabug evolves into Vikavolt by a Thunder Stone as well as by Mt. Coronet's magnetic field, the donor's later-generation rule. Stones are scarce on purpose, so a second path costs the player a stone another line could use, which is the kind of choice Ian wants.

Question: does Charjabug keep the Thunder Stone?

| Option | Cost |
|---|---|
| Keep it (recommended) | none |
| Remove it; Vikavolt comes only from the magnetic field | one data line, a rebuild, and the OxiDex's availability rerun |

### 16. A docstring in the scorer

The same finding: `plgoal3.py`'s opening docstring points at the handoff's section "Goal 3's reading", which is titled "Goal 3's driver". The scorer's files change only with Ian's yes, even for a comment.

Question: may the Overseer fix that one line?

| Option | Cost |
|---|---|
| Yes (recommended) | a one-line commit; no result changes |
| No | none |

## Other calls marked Ian's in the tracker's body

These are not on the waiting list, so they are left out of the dialogs above, but each is older than a week and could join a later sheet: whether a tutor pass is still wanted (Item and learnset passes); whether Stark Mountain is open before the League, and whether Iron Island's Metal Coat and Rock Peak Ruins' Hard Stone can be reached before it (from 2026-10-22); moving `goal3_fights.py` into the repo (Tidying); repinning `test_plgoal3`'s box sizes (a scorer test, Backlog); King's Shield's missing Attack drop before alpha 1 (Backlog); Barry 2's interim honour cap; and the four evolution stones that come later than planned, held for the item pass.
