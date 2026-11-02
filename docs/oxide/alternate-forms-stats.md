# Alternate forms: a thematic stat pass

A proposal for Ian (2026-11-02), nothing applied. No file under `res/` changed; the spreads go in only after his yes.

## Summary

**Outcome.** Eight of the sixteen Pokemon change (one side of six pairs and both sides of Weezing's), and eight stay as they are. Every change moves points between stats, and no total changes. Each pair ends with one twin that is fast or hits hard and one that is slower and takes hits, and each change was checked against its learnset, its trainers and the power flags. Where one twin is core to many fights or is a core answer to a boss, its twin carries the change: Alolan Ninetales (an answer at Gardenia and elsewhere), Lopunny (Lucas and Dawn's fast threat), Gyarados (Cyrus 3, Thorton and sixteen other trainers) and Goodra (Wake's core) are all kept. Two facts change the brief's premise. The Magikarp line is cut from the player's game, so the Gyarados pair is trainer-only. And Mars 2's team carries none of these Pokemon; the two grunts before it at Lake Verity carry Weezing and Gyarados.

Spreads are HP / Attack / Defense / Speed / Sp. Atk / Sp. Def, as in the brief. A dash in the Proposed column means no change.

| Species | Today | Total | Proposed | Total | Move |
|---|---|---|---|---|---|
| Ninetales | 79/89/79/100/109/99 | 555 | 85/65/84/95/109/117 | 555 | Atk into HP, Def and Sp. Def; Spe -5 |
| Alolan Ninetales | 79/89/79/100/109/99 | 555 | (no change) | 555 | |
| Rapidash | 70/105/75/110/85/85 | 530 | (no change) | 530 | |
| Galarian Rapidash | 70/105/75/110/85/85 | 530 | 80/100/85/95/75/95 | 530 | Spe and Sp. Atk into HP, Def and Sp. Def |
| Weezing | 65/90/120/60/90/85 | 510 | 65/90/110/60/100/85 | 510 | Def -10, Sp. Atk +10 |
| Galarian Weezing | 65/90/120/60/85/70 | 490 | 70/65/115/50/85/105 | 490 | Atk and Spe into Sp. Def |
| Gyarados | 95/125/79/81/60/100 | 540 | (no change) | 540 | |
| Gyarados M | 95/125/79/81/75/100 | 555 | 95/125/105/65/65/100 | 555 | Spe and Sp. Atk into Def |
| Lopunny | 65/86/84/105/54/116 | 510 | (no change) | 510 | |
| Lopunny M | 65/106/84/105/54/96 | 510 | 75/106/94/90/54/91 | 510 | Spe and Sp. Def into HP and Def |
| Mr. Mime | 65/25/95/90/100/120 | 495 | (no change) | 495 | |
| Galarian Mr. Mime | 50/65/65/100/90/90 | 460 | (no change) | 460 | |
| Goodra | 90/100/70/80/110/150 | 600 | (no change) | 600 | |
| Hisuian Goodra | 80/100/100/60/110/150 | 600 | 80/100/130/60/110/120 | 600 | 30 from Sp. Def to Def |
| Sliggoo | 68/75/53/60/83/113 | 452 | (no change) | 452 | |
| Hisuian Sliggoo | 58/75/83/40/83/113 | 452 | 58/75/105/40/83/91 | 452 | 22 from Sp. Def to Def |

**What Ian decides.** Each has a recommendation, the first option.

1. Ninetales: (a) change Kanto Ninetales only, into the slow, bulky special caster; (b) also shift Alolan Ninetales to a physical lean, which is material for Gardenia, Fantina, Maylene and Cyrus 1; (c) keep both.
2. Rapidash: (a) Galarian Rapidash becomes the slower, sturdy unicorn, which is material for Darach; (b) the same bulk but Speed kept at 110; (c) keep both.
3. Weezing: (a) both as proposed, material and small for Hesperid 1 and 2 and for Jupiter 1; (b) Galarian Weezing only, which leaves Hesperid untouched; (c) keep both.
4. Gyarados: (a) Gyarados M becomes the slow brute, which is not material; (b) keep both.
5. Lopunny: (a) Lopunny M becomes slower and sturdier, which is material for Dahlia; (b) keep both.
6. Mr. Mime: (a) keep both, since the pair is already distinct by Ian's own choices; (b) ask for a pass on it anyway.
7. Goodra and Sliggoo: (a) the Hisuian side swaps its Sp. Def emphasis into Defense, which is not material; (b) keep both.
8. The material fights (Darach, Dahlia, Hesperid 1 and 2, Jupiter 1): (a) no scorer reading, judged in Ian's playtest; (b) spot-read Darach and Dahlia, about three hours each.

**Next steps.**

| Step | Who | Time |
|---|---|---|
| Ian answers the eight decisions | Ian | 10 minutes |
| Apply the approved spreads to `res/pokemon/` | a `routine` helper | 20 minutes |
| Build, gate and land on `oxide` | the Overseer | 40 minutes |
| Retune any trainer set Ian wants after the change (none is required) | a `worker` helper | 30 minutes a team |

A stat change does not move the save, so it needs no new game. The OxiDex reads stats from `res/` and follows on its own.

Findings beside the proposal, none fixed here: Gyarados M and Lopunny M have empty TM lists; Lopunny M's Iron Fist has one punch to work with; Hydration on Goomy's line does nothing for the player, who can never set rain; the splits tool files Lucas and Dawn 2 and the Lake Verity grunts under Roark's split; and `encounters/availability.md` still dates Galarian Rapidash's Moon Stone to Gardenia's split, where the stone census now gives Byron's. Each is described under its pair or at the end.

## How each pair was judged

Each twin should give the player a reason to choose it, so the pairs split along one line: one twin is fast or hits hard, and the other is slower and takes hits. Points move between stats, never into two attacking stats and Speed together (Ian's warning, 2026-11-02). Each change was checked against these points:

- the learnset, level-up and TM, which must fit the attacking side the spread favours;
- every trainer team that carries the Pokemon, from `res/trainers/data/`, with the fight's kind, and whether the change is material by `boss-shapes.md` and the fight's own check doc;
- the balance rules' power flags (base Speed over 100, or base Attack or Sp. Atk over 100 with a move of 100 power or more of that kind) at the split the player first has it;
- where and when the player has it, from the OxiDex's availability data, the wild tables and the stone census (`tools/oxide/balance/stones.py`);
- canon's spread (the OxiDex's `canon.json`) and Kaizo's (`kaizo-stat-type-changes.csv`), as reference only.

Kaizo has no regional forms and no Gyarados M or Lopunny M, so its numbers bear only on the base forms. Nothing new is drawn from Kaizo here, so the rule that Kaizo data is translated twice has nothing to act on. The five base forms Kaizo changed (Ninetales, Rapidash, Weezing, Mr. Mime, Lopunny) already carry Kaizo's spreads in Oxide, and Ian's sheet copied two of them onto the regional twins, which is why Ninetales and Rapidash match their twins exactly today.

One reading problem runs through the trainer lists. The splits tool (`splits.trainer_split`) files a trainer under the split in which its map is first reached, so a fight on a revisited map lands too early. It puts Lucas and Dawn 2 (Route 207, Fantina's split) and the level-52 grunts at Lake Verity (Byron's split, before Mars 2) under Roark. The splits below follow the fight docs where the tool is wrong.

## 1. Ninetales and Alolan Ninetales

**Today** both carry Kaizo's Ninetales, 79/89/79/100/109/99, so the two foxes differ only in type and ability. Canon gives Ninetales 73/76/75/100/81/100 and Alolan Ninetales 73/67/75/109/81/100.

**Proposed.** Ninetales 85/65/84/95/109/117; Alolan Ninetales unchanged.

**Theme.** Kanto Ninetales becomes the old mystic fox: a patient special caster that burns, sets Nasty Plot behind Magic Guard and outlasts special attackers. It is slower than its twin and gives up the Attack it never used. Alolan Ninetales stays the quick snow fox, mixed and slightly frailer: its early attacks are physical (Ice Shard, Payback and Icicle Spear by 21, then Play Rough 27 and Triple Axel 37), its first strong special move, Dazzling Gleam, comes at 35, and it is the one to choose when speed and Ice coverage matter. Fire against Ice already splits their matchups; the spread now splits how they play.

**Where the player has them.** Vulpix is wild from Roark's split (Route 207 at 6, Verity Lakefront at 4 or 5). The game's one Fire Stone before the League is hidden in the Solaceon Ruins in Maylene's split, and Eevee wants it for Flareon, so a Kanto Ninetales costs the player a Flareon. Wild Ninetales comes only at Route 225 at 50, in Galactic's split. Alolan Ninetales is wild on Route 211 West at 13 to 16 and Mt. Coronet North at 15, in Gardenia's split, and later on Routes 216 and 217 and around Acuity. The one Ice Stone, in Wayward Cave in Fantina's split, makes another from Vulpix.

**Learnset fit.** Kanto Ninetales evolves by stone, so it keeps Vulpix's moves: Flamethrower at 24, Will-O-Wisp, Incinerate and Icy Wind. It then learns Alluring Voice 33, Energy Ball 54, Extrasensory 56 and Mystical Fire 62, with Fire Blast, Overheat, Dark Pulse, Shadow Ball, Energy Ball and Calm Mind by TM. All of it is special, so the spread fits. Flare Blitz at 40 and Bite at 64, both physical, lose their use at Attack 65; the list would be cleaner with a special move there, which is noted and not changed.

**Trainers.** Kanto Ninetales is on twenty trainer files, all with special sets:

| Trainer | Split | Kind | Level |
|---|---|---|---|
| Twins Emma and Lil; Belle and Pa | Maylene | ordinary doubles | 31, 35 |
| Policeman Alex | Wake | ordinary | 40 |
| Ace Trainer Shannon | Byron | mini-boss | 46 |
| Ace Trainer Sandra | Galactic | mini-boss | 62 |
| Barry at Spear Pillar (partner) and the Fight Area | Galactic, Barry | partner | 58, 70 |
| Barry 6 (League gate), both versions | Barry | boss | 70 |
| Elite Four Flint, and his rematch | League, Post | boss | 73, 85 |
| Barry at the Survival Area, Ace Trainer Clarice | Post | rematches, ordinary | 59 to 79 |

None of the written shapes names Ninetales, and neither Flint's nor Barry 6's shape is written. Ninetales is one of six in both and neither one's ace. Its Speed falls about 8 points at Flint's level (Timid at 73, from about 190 to 182), and its special bulk rises. By judgement this is not material: it changes how long Ninetales stays in, not what the player brings. Alolan Ninetales is on one trainer, Ace Trainer Brenna (Candice's split, hail and Aurora Veil), and is unchanged.

**Power flags.** Kanto Ninetales keeps Sp. Atk 109, flagged as today by the Fire Blast and Overheat TMs from Maylene's split, and its Speed falls to 95, below the Speed flag. Alolan Ninetales keeps today's flag: Sp. Atk 109 with Blizzard by TM, from Gardenia's split.

**Why Alolan Ninetales stays.** It is a core answer at Gardenia (`boss-shapes.md`: in every six whose box has it, Icicle Spear hitting four of her five). The fight docs put it in the screen's sixes at Fantina, Maylene (its Dazzling Gleam knocks out Hakamo-o) and Cyrus 1 (Salamence's answer). Any change to its Attack or Sp. Atk is material for all four. Option (b) is for Ian if he wants both foxes to move: Alolan Ninetales at 79/99/79/100/94/104 (Attack +10, Sp. Atk -15, Sp. Def +5), a physical lean its early list supports. Icicle Spear gains about 11 percent at Gardenia and Dazzling Gleam loses about 14 at Maylene.

**Abilities.** Magic Guard fits a caster that burns and is burned. Drought, Kanto Ninetales' hidden slot, serves the trainers who use it.

## 2. Rapidash and Galarian Rapidash

**Today** both carry Kaizo's Rapidash, 70/105/75/110/85/85. Canon gives both 65/100/70/105/80/80. Oxide types Galarian Rapidash Fairy and Fire; canon has it Psychic and Fairy.

**Proposed.** Rapidash unchanged; Galarian Rapidash 80/100/85/95/75/95.

**Theme.** Rapidash stays the racer: the fastest Fire type the player has, with Reckless Flare Blitz and Agility, and frail. Galarian Rapidash becomes the steady unicorn: a physical Fairy that takes hits, heals a partner with Heal Pulse, and keeps poison off its side with Pastel Veil. It is slower than its twin, so it does not double as a second fast Fire attacker.

**Where the player has them.** Ponyta is wild from Roark's split on (Route 207 at 5), and becomes Rapidash at 40, in Wake's split. The two Moon Stones before the League are hidden at Eterna City (Byron's split) and on Mt. Coronet's north side (Galactic's). Six other lines compete for them: the two Nidos, Skitty, Clefairy, Eevee (for Umbreon) and Koffing. A player who wants Galarian Rapidash before Galactic's split must cancel Ponyta's evolution at 40 and carry it into Byron's split. Wild Galarian Rapidash is on Route 230 and in the Resort Area at 47 to 50, in Galactic's split.

**Learnset fit.** Galarian Rapidash is made by stone, late, so it keeps Ponyta's physical moves (Flame Wheel, Stomp, Take Down, Bounce, Fire Lash 44, and Flare Blitz at 46 if it waits that long). It then learns Spirit Break 46, Throat Chop 48, Wild Charge 58 and Zen Headbutt 66, with Play Rough, Wild Charge and Iron Tail by TM. The physical lean fits. Its special moves (Mystical Fire 50, Psychic 56, Moonblast 72) fall to second place. One gap stays as it is today: a Galarian Rapidash evolved after 17 has no Fairy move of its own before Spirit Break at 46, unless it takes Play Rough by TM.

**Trainers.**

| Trainer | Split | Kind | Level | Set |
|---|---|---|---|---|
| Cyclist Rachel (Rapidash) | Fantina | ordinary | 27 | physical |
| Arcade Star Dahlia (Rapidash) | Maylene | boss | 40 | Flare Blitz, Swords Dance, Double-Edge, Baton Pass |
| Rancher Marco, Veteran Brian (Rapidash) | rematches | ordinary | 44 to 60 | mixed |
| Cowgirl Shelley (Galarian) | Maylene | ordinary | 33 | Play Rough, Flame Charge, Psycho Cut, Megahorn |
| Castle Valet Darach (Galarian) | Wake | boss, a double | 44 | Heal Pulse, Fire Lash, Play Rough, High Horsepower; Focus Sash |

Rapidash is unchanged, so Dahlia's fight is untouched by this pair. Darach's Galarian Rapidash drops from about 115 Speed to about 102 at 44, and its partner Corviknight's Tailwind doubles it on the turns it is up. The Focus Sash makes its new bulk count only after the first hit. `darach-check.md` calls this slot the fight's weakest crux, so the change is material for Darach. It makes his lead a little slower and a little harder to remove. Shelley's set keeps working.

**Power flags.** Rapidash keeps today's Speed flag (110), from Wake's split, unchanged. Galarian Rapidash at Speed 95 and Attack 100 carries no flag. Option (b) keeps its Speed at 110 and takes the bulk from Sp. Atk alone (75/100/85/110/65/95); that removes the Darach change but leaves the twins equally fast.

**Abilities.** Run Away in Galarian Rapidash's first slot does nothing in a trainer battle. Abilities are out of scope, but a sturdy support horse would want something in that slot.

## 3. Weezing and Galarian Weezing

**Today** Weezing carries Kaizo's 65/90/120/60/90/85 and Galarian Weezing canon's 65/90/120/60/85/70. Canon gives Weezing the same 65/90/120/60/85/70.

**Proposed.** Weezing 65/90/110/60/100/85; Galarian Weezing 70/65/115/50/85/105.

**Theme.** Weezing becomes the gunner: a physically sturdy Levitate Poison type that hits with the widest coverage of the pair (Sludge Wave, Heat Wave, Shadow Ball, Thunderbolt, Flamethrower, Dark Pulse), and keeps the Attack the trainers' Explosions use. Galarian Weezing becomes the purifier: a Fairy support wall that takes special hits and spreads Will-O-Wisp, Toxic Spikes, Pain Split, Defog and Neutralizing Gas. Ian found in the learnset exam (2026-10-06) that Galarian Weezing's moves made Weezing hardly worth choosing. Koffing is one of his super-wanted lines, so the pass gives the plain branch the stronger offence and the stone branch the stronger defence.

**Where the player has them.** Koffing is wild from Maylene's split (Route 209 and the Lost Tower at 18 or 19, Route 212 South at 21, the Great Marsh at 28 to 31), and becomes Weezing at 35, in Maylene's split. Galarian Weezing needs a Moon Stone, first in Byron's split (above), so Koffing's evolution has to be cancelled at 35 and again until then. Galarian Weezing is wild on Stark Mountain at 51 to 54, in Galactic's split; wild Weezing is on Route 227 at 52.

**Learnset fit.** Both lists are special. Weezing learns Sludge 24, Sludge Wave 40, Psybeam 42, Sludge Bomb 48, Heat Wave 50, Shadow Ball 56, Thunderbolt 64, Flamethrower 66 and Dark Pulse 72, with Thunder and Fire Blast by TM, and its Attack serves only Assurance, Double Hit and Poison Fang at 58. Galarian Weezing learns Belch 18 and Dazzling Gleam 21 (both below any level a stone-made one can have, so the relearner's only), Sludge 26, Sludge Bomb 42, Strange Steam 48, Thunderbolt 54 and Heat Wave 62, among its status moves. Galarian Weezing loses Attack it had no use for. Weezing's gain in Sp. Atk meets its list.

**Trainers.**

| Trainer | Split | Kind | Level | Set |
|---|---|---|---|---|
| Galactic Officer Tyche (Weezing) | Wake | Tyche and Hermes 1, a named fight | 40 | Protect, Will-O-Wisp, Sludge Bomb, Pain Split |
| Galactic Officer Hesperid (Weezing), Lake Valor | Byron | Hesperid 1, the lead | 51 | Sludge Bomb, Payback, Thunder, Explosion |
| Galactic Grunt, Lake Verity (Weezing) | Byron | ordinary, before Mars 2 | 52 | Will-O-Wisp, Sludge Bomb, Fire Blast, Pain Split |
| Galactic Grunt, Galactic HQ B2F (Weezing) | HQ | ordinary | 54 | Toxic, Flamethrower, Explosion, Sludge Bomb |
| Galactic Officer Hesperid (Weezing), Mt. Coronet 6F | Galactic | Hesperid 2, the lead | 63 | Sludge Bomb, Will-O-Wisp, Thunderbolt, Explosion |
| Commander Jupiter (Galarian), Eterna building | Fantina | Jupiter 1, a named fight | 28 | Will-O-Wisp, Pain Split, Strange Steam, Toxic Spikes |
| Jogger Scott (Galarian) | Maylene | ordinary | 36 | Will-O-Wisp, Sludge Bomb, Dazzling Gleam, Pain Split |
| Collector Ivan (Galarian) | Byron | ordinary | 46 | Strange Steam, Sludge Bomb, Will-O-Wisp, Defog |

Hesperid's Weezing is his lead and the centre of his check (`hesperid-check.md`): its Sludge Bomb and Thunder rise by about a tenth, its Defense falls by a twelfth, and its Explosion is unchanged. That is material for Hesperid 1 and 2, and small. Tyche's Weezing is one member of five, so it is not material there. Jupiter 1's shape names Tangela and Skuntank as its core, so by the rule a change to Galarian Weezing is not material. But a Sp. Def of 105 in place of 70 makes it last half as long again against special attackers, behind Black Sludge and Pain Split. By judgement that is material for Jupiter 1, and the fight gets a little longer. Option (b) changes only Galarian Weezing and leaves Hesperid untouched.

**Power flags.** Weezing's Sp. Atk of 100 sits at the bar, not over it, so it carries no flag; at 105 it would be flagged by Fire Blast and Thunder from Maylene's split. Galarian Weezing carries none.

**Abilities.** Levitate, Neutralizing Gas and Misty Surge all suit a wall, so none fights the spread.

## 4. Gyarados and Gyarados M

**Today** Gyarados carries the base ROM's 95/125/79/81/60/100 (Kaizo's has Sp. Atk 75) and Gyarados M the same with Sp. Atk 75. Canon's Mega Gyarados is 95/155/109/81/70/130.

**Proposed.** Gyarados unchanged; Gyarados M 95/125/105/65/65/100.

**The player never has either.** The species pick-list cuts the Magikarp line, no wild table places it, and no Dragon Scale is placed. The pair matters only for the trainers who carry it, so the power flags do not apply.

**Theme.** Gyarados stays the Dragon Dance flyer with Intimidate or Moxie, the sweeper that has to set up. Gyarados M becomes the brute: a slow Water and Dark Mold Breaker that walks through Sturdy, Levitate and Multiscale and takes physical hits rather than outrunning them. Its Mega form in canon had Defense 109 and Sp. Def 130; this keeps the Defense half of that and none of the extra Attack.

**Learnset fit.** Gyarados M's list is physical (Bite, Ice Fang 28, Take Down 34, Crunch 38, Waterfall 48, Outrage 53, Bounce 55, Thrash 60, Aqua Tail 61, with Earthquake, Stone Edge and Power Whip at level 1), with Surf 31 and Ice Beam 42 beside them. A physical brute fits. Its TM list is empty, which matters only for the legality checkers.

**Trainers.** Gyarados is on eighteen files: Cyrus 3 in the Distortion World (a boss, Galactic's split), Factory Head Thorton's spare file (Post), Wake's rematch, Ace Trainers Olivia, Abel, Deanna, Henry and Ruben, the Lake Verity grunt before Mars 2 (Byron's split, level 52), and fishermen, sailors and swimmers. That reach, and Ian's lukewarm view of the line, are why Gyarados stays. Gyarados M is on one team, Wake's six at 43 (Assault Vest, Lonely; Waterfall, Earthquake, Power Whip, Crunch). Wake's core in `wake-barry4-check.md` is the rain, the Swift Swim pair and Goodra, so Gyarados M is a one-off there and the change is not material. Its damage is unchanged, it takes physical hits about a third better, and it moves later (about 74 Speed at 43, from 87), which matters little beside Swift Swim.

**Abilities.** Mold Breaker in both slots suits the brute.

## 5. Lopunny and Lopunny M

**Today** Lopunny carries Kaizo's 65/86/84/105/54/116, and Lopunny M Ian's own 65/106/84/105/54/96: twenty points moved from Sp. Def to Attack. Canon has Lopunny at 65/76/84/105/54/96 and Mega Lopunny at 65/136/94/135/54/96.

**Proposed.** Lopunny unchanged; Lopunny M 75/106/94/90/54/91.

**Theme.** Lopunny stays the fast pest: Fake Out, Scrappy's Jump Kick, Baton Pass, Charm and Encore, with a Sp. Def that lets it stay in against special attackers. Lopunny M becomes the kickboxer: Normal and Fighting, Ian's Attack kept, slower, and sturdier to physical hits, so it trades blows where its twin darts in and out. Ian's twenty-point shift is kept and taken further, in the same direction.

**Where the player has them.** Buneary is wild from Roark's split (Lake Verity and Verity Lakefront at 4 or 5, Eterna Forest at 10), and becomes Lopunny at 20, in Gardenia's split. Wild Lopunny is at Trophy Garden (23) and Valor Lakefront (27). Lopunny M needs the game's one Fist Plate, in a ball on Route 215 in Maylene's split, which otherwise serves as a Fighting booster.

**Learnset fit.** Lopunny M's list is physical: Dizzy Punch 20, Bounce 22, Jump Kick 25, Fake Out 38, Double-Edge 48, Close Combat 55, High Jump Kick 60, with Triple Axel and U-turn at level 1. It fits. It has no TM list at all, so it cannot take Ice Punch, Drain Punch or Earthquake as Lopunny can; this is a finding, not part of the change.

**Trainers.** Lopunny is on 28 files. It is the fast threat off the lead in Lucas and Dawn 2 (Route 207, Fantina's split, level 30, six files; `lucas-dawn-2-redesign.md`), in their Veilstone and Pal Park partner files (39 and 47), on Ace Trainers Brenda and Natasha, and on Lass Cassidy, Beauty Cyndy, Young Couple Ty and Sue, Ranger Felicia, Beauty Nicola and rematches. A change to Lopunny would be material for Lucas and Dawn 2 and would touch every partner fight, which is why it stays. Lopunny M is on one team, Arcade Star Dahlia's six at 40 (Maylene's split; Jolly, Assault Vest; High Jump Kick, Dizzy Punch, Triple Axel, Fake Out). `dahlia-check.md` finds it the most frequent receiver of her Baton Passes, so it is core, and the change is material for Dahlia. Its Speed falls from about 111 to about 97 at 40, so it outruns fewer of the box's lines after a pass. Her Wonder Room swaps the two defences, so the gain in Defense guards it against special hits while the room is up.

**Power flags.** Lopunny keeps today's Speed flag (105) from Gardenia's split. Lopunny M keeps today's Attack flag (106, with Jump Kick at 25 and Close Combat at 55) from Maylene's split, and loses its Speed flag. A flagged stage in Maylene's split is one to look at very closely; this pass makes it weaker, not stronger.

**Abilities.** Iron Fist powers punching moves, and Lopunny M has one: Dizzy Punch. With no TM list it cannot learn another, so the ability does almost nothing for the player. That is a learnset or ability question for later. Inner Focus suits a brawler.

## 6. Mr. Mime and Galarian Mr. Mime

**Today** Mr. Mime carries Kaizo's 65/25/95/90/100/120 (495), and Galarian Mr. Mime canon's 50/65/65/100/90/90 (460). Canon's Mr. Mime is 40/45/65/90/100/120.

**Proposed.** Both unchanged.

**Why.** The pair is already distinct, by Ian's own choices. Mr. Mime is a Psychic and Fairy screen-setter with Filter and a Sp. Def of 120, a fully evolved special wall. Galarian Mr. Mime is an Ice and Psychic middle stage with Speed 100 and little bulk, which becomes Mr. Rime at 42 and is meant to be outgrown. The types differ, the roles differ, and the totals differ by 35, which is right for a final stage against a middle one. Both learnsets fit: Mr. Mime's attacks are all special (Psybeam, Mystical Power, Psychic, Signal Beam, Thunderbolt, Mystical Fire, Moonblast). Galarian Mr. Mime's are mostly special (Confusion, Icy Wind, Psybeam, Freeze-Dry 44, Psychic 48), with Rapid Spin, Double Kick and Sucker Punch for its 65 Attack.

**Where the player has them.** Mime Jr. is wild at Trophy Garden (23) in Wake's split, and becomes Mr. Mime when it levels up knowing Mimic, which it learns at 18, so the player has Mr. Mime in Wake's split. Galarian Mr. Mime is wild at Trophy Garden (24) in Wake's split, on Route 218 (28 to 31) in Byron's, and later around Routes 216 and 217 and Lake Acuity.

**Trainers.** Mr. Mime: Commander Saturn's Valor Cavern six (Saturn 1, Candice's split, level 52, screens with Light Clay), Cameraman Darryl, and rematches. Galarian Mr. Mime: Officer Moira's Eterna building six (Moira 1, Fantina's split, level 25, the Future Sight theme), Psychic Kody and Breeder Albert. Nothing changes, so nothing is material.

**Power flags.** Galarian Mr. Mime's Speed of 100 is at the bar, not over it. Mr. Mime's Sp. Atk of 100 is the same. Neither is flagged.

## 7. Goodra and Hisuian Goodra

**Today** both carry canon's spreads: Goodra 90/100/70/80/110/150, Hisuian Goodra 80/100/100/60/110/150. Kaizo has neither.

**Proposed.** Goodra unchanged; Hisuian Goodra 80/100/130/60/110/120.

**Theme.** Canon already parts them by HP and Speed against Defense, but both remain special walls with the same two attacks. Goodra stays the special sponge: pure Dragon, Sap Sipper and Gooey, Sp. Def 150, the faster of the two. Hisuian Goodra becomes the physical wall: Steel and Dragon, with its defensive peak moved to Defense. Its two weaknesses, Fighting and Ground, are mostly physical, so Defense 130 is where a Steel wall wants its points, and Sp. Def 120 is still high. Its attacks are untouched, so its learnset fits as it does today. The total is unchanged, so this adds no power; it only moves which hits the wall shrugs off.

**Where the player has them.** Goomy is wild on Route 212 South at 24 (Wake's split) and in Mt. Coronet B1F at 32 (Candice's), and becomes Sliggoo at 40 and Goodra at 50, from Byron's split at the earliest. Hisuian Sliggoo needs a Metal Coat held while Goomy levels. The Metal Coat in Iron Island's Iron Ruins ball is reachable before the League only if Ian rules it so (an open question in the tracker); otherwise the first is the Iron Island house's gift after the League. Onix and Scyther want the same item.

**Trainers.** Goodra: Leader Wake at 40 (a boss, Wake's split; Hydration with Rest in permanent rain, Thunder, Weather Ball, Dragon Tail; core to Wake) and Ace Trainer Olivia at 53 (a mini-boss, Candice's split, all special). Goodra is unchanged, so neither fight moves. Hisuian Goodra is on no team, so the change is not material anywhere.

**Power flags.** As today: Goodra and Hisuian Goodra both carry Sp. Atk 110, flagged by Draco Meteor and by the Hydro Pump, Blizzard, Thunder and Fire Blast TMs, from the split each first evolves in.

**Abilities.** Hydration heals status only in rain, and the player can never set rain, so for the player Goodra's and Sliggoo's second slot does nothing. Wake's Goodra uses it in his permanent rain. Shell Armor suits the Hisuian wall.

## 8. Sliggoo and Hisuian Sliggoo

**Today** both carry canon's spreads: Sliggoo 68/75/53/60/83/113, Hisuian Sliggoo 58/75/83/40/83/113.

**Proposed.** Sliggoo unchanged; Hisuian Sliggoo 58/75/105/40/83/91.

**Theme.** Each middle stage follows its final form: Sliggoo the special sponge, Hisuian Sliggoo the physical wall, shell and all. The move is a straight 22 points from Sp. Def to Defense, so the total and both attacks are unchanged. Its list (Water Pulse 25, Dragon Pulse 35, Flash Cannon 42, Iron Head 49) and its TMs (Gyro Ball, which a 40-Speed wall uses well, Rock Slide, Flash Cannon, Dragon Pulse) fit as before, and Shelter and Acid Armor at level 1 and Curse at 43 already belong to a physical wall.

**Trainers.** Neither Sliggoo is on any trainer team, so nothing is material. No power flag applies to either.

## Findings beside the proposal

These came up while checking the pairs. None is fixed on this branch.

| Finding | Where | What it would take |
|---|---|---|
| Gyarados M and Lopunny M have empty TM lists | `res/pokemon/gyarados_m`, `lopunny_m` | a TM compatibility rerun that reads the base form's list for an alt evolution |
| Lopunny M's Iron Fist has one punching move | its level-up list and TM list | a learnset or ability choice by Ian |
| Hydration does nothing for the player's Goomy line | the player can never set rain | an ability choice by Ian |
| Kanto Ninetales' Flare Blitz 40 and Bite 64 suit no special spread | its level-up list | a learnset choice, only if the spread lands |
| The splits tool files revisit fights by the map's first split | `splits.trainer_split`: Lucas and Dawn 2, the Lake Verity grunts | a revisit entry for each, in its `TRAINER_SPLITS` or `STORY_REVISITS` |
| `availability.md` gives Galarian Rapidash's Moon Stone from Gardenia's split | the generated availability plan | a rerun of `cli availability --write` after the item pass |
| Mars 2 carries none of these Pokemon | `commander_mars_lake_verity.json` | nothing; the brief's carrier list was off |

The old perfect-line results of 2026-09-30, from the scoring system retired on 2026-10-13, put Kanto Ninetales in the player's teams from Maylene's split on and Galarian Rapidash in Gardenia's and Maylene's. The Galarian Rapidash entries come from before the stone census moved the Moon Stone to Byron's split. Neither is a core counterpiece in any written shape.
