# Barry's pool, and three shapes for Barry 3

Ian, 2026-10-29: "given we fight him so many times, having him take from a pool of 9-12 pokemon that gets progressively harder as the game goes on seems fair to me", matched neither exactly backwards nor forwards ("there's only so early in a game you can fairly fight a turtonator"), and the pool outlined before Barry 3's sets are made. On Barry 3 he named three faults (the "optimalness" of the Staraptor and Snorlax sets, an Empoleon set that "thinks that it is still a special attacker", an Ambipom that "can almost-literally never use last resort") and a team shape "very reminiscent of that Hyper-Offense" he wants to get away from, and he is "pretty all ears" for ideas. This page is a proposal only: no trainer file changed. It has the pool (part 1) and Barry 3's evidence, diagnosis and three shapes (part 2), with no sets.

## Summary

**Outcome.** A pool of twelve slots for each player: Barry's Sinnoh starter, two starters from other regions that cover the elements his own lacks (Ian's Barry 4 pattern), and nine shared lines. Seven of a player's twelve lines end in a Generation 5 or later Pokemon. Ian's Barry 4 is one draw from it unchanged. For Barry 3, three shapes trade the current team's speed and damage for tactics: speed control, hazards with forced switches, and a lead built to be countered by an answer that hands a setup member its turn. I recommend the second, hazards and forced switches, because it is the only shape whose tactics the trainer AI plays in nearly every fight and because it taxes the switching every baiting plan needs. All three read easier than today's team on the matchup screen, which counts only damage and Speed, so the chosen shape needs the margin the standing rulings give status and stall teams, or a spot check.

**The twelve.**

| Slot | Line | Fights | Role | Why Barry |
|---|---|---|---|---|
| 1 | His starter: Turtwig, Chimchar or Piplup line | all | the ace | canon: the starter strong against the player's |
| 2 | First element partner: Greninja or Serperior line | Barry 3 on | Water or Grass cover, special damage, Spikes or screens | Ian's Barry 4: Barry took the other regions' starters too, as vanilla Barry carried the two elements his starter lacked |
| 3 | Second element partner: Serperior line or Turtonator | Barry 4 on | the third element | as above; Turtonator only from Barry 4 (Ian's "only so early") |
| 4 | Starly line | Barry 2, 3, 4, 6 | Intimidate pivot, phazing or Tailwind | his first catch, in every vanilla Barry fight |
| 5 | Munchlax line | Barry 2, 3, 4, Spear Pillar, 6 | the slow anchor: Yawn, Body Slam, Curse | canon; the one patient Pokemon on an impatient trainer's team |
| 6 | Shinx line | Barry 2, 3, 4 | fast physical Electric and Dark, Roar | Ian's pick for Barry 4 |
| 7 | Togedemaru | Fight Area (Barry 3's shape A) | Fake Out, Nuzzle, U-turn; Lightning Rod | a spiky ball that rolls into things, as Barry runs into the player |
| 8 | Snom line (Frosmoth) | Barry 5 (shapes A and C) | Ice, the slow special setup threat (Quiver Dance, Ice Scales) | chosen for its role: the pool has no other Ice |
| 9 | Mankey line (Primeape, Annihilape) | Barry 3, 5 | Stealth Rock and Taunt lead, later a Bulk Up attacker | always angry, Barry's temper |
| 10 | Dratini line | Spear Pillar, Barry 6 | the late power member | Palmer, Barry's father, carries a Dragonite; so did the base ROM's late Barry |
| 11 | Goomy line | Barry 5, Fight Area | bulky special Dragon that takes Fire and Electric | chosen for its role, chiefly the Fight Area |
| 12 | Flabebe line (Florges) | Spear Pillar, Fight Area | Wish, Helping Hand, Aromatherapy: a partner's support | takes the place of canon Barry's Roserade, the flower on his vanilla team |

Which partners each player meets:

| Player's starter (file suffix) | Barry's starter | First partner (Barry 3 on) | Second partner (Barry 4 on) |
|---|---|---|---|
| Turtwig (`_turtwig`) | Infernape | Greninja | Serperior |
| Scorbunny (`_chimchar`) | Empoleon | Serperior | Turtonator |
| Piplup (`_piplup`) | Torterra | Greninja | Turtonator |

**The pool against the fights.** Each column is the six he brings, at the stage the line can be at that level. Barry 3 shows the recommended shape; Barry 4 is Ian's.

| Slot | Barry 1 (5) | Barry 2 (cap 11) | Barry 3 (36) | Barry 4 (44) | Barry 5 (Byron's split) | Spear Pillar (partner, 59) | Fight Area (partner, 75) | Barry 6 (71) |
|---|---|---|---|---|---|---|---|---|
| Starter | first stage | first stage | final | final | final | final | final | final |
| First partner | | | Greninja or Serperior 35 | final | final | final | final | final |
| Second partner | | | | final | final | final | final | final |
| Starly line | | Starly | Staraptor | Staraptor | | | | Staraptor |
| Munchlax line | | Munchlax | Snorlax 35 | Snorlax | | Snorlax | | Snorlax |
| Shinx line | | Shinx | Luxray | Luxray | | | | |
| Togedemaru | | | | | | | Togedemaru | |
| Snom line | | | | | Frosmoth | | | |
| Mankey line | | | Primeape | | Annihilape or Primeape | | | |
| Dratini line | | | | | | Dragonite | | Dragonite |
| Goomy line | | | | | Goodra or Sliggoo | | Goodra | |
| Flabebe line | | | | | | Florges | Florges | |

The pool grows harder by entry: Barry 2 is four first stages, Barry 3 is mid-power (base stat totals of 505 for Primeape, 523 for Luxray, 535 for the starters' finals), Barry 5 brings Goodra (600), Annihilape (535) and a Quiver Dance Frosmoth, and Dragonite (600) arrives for the last two fights. Barry 1 keeps his lone starter and does not count for deaths. Barry 2 swaps Buizel for Shinx, since Floatzel is Wake's ace.

**Barry 3, in a line each** (cap 36, ace at 36; one element partner per version):

- A, speed control: Togedemaru leads with Nuzzle and Fake Out, Staraptor's Tailwind and Snorlax's Body Slam and Yawn follow, and Frosmoth's Quiver Dance is the win condition. The AI mostly skips its speed control for damage.
- B, hazards and forced switches (recommended): Primeape leads with Stealth Rock and Taunt, Greninja lays Spikes (Serperior's screens for a Scorbunny player), and Staraptor's Whirlwind, Luxray's Roar and Snorlax's Yawn drag the player's six over them.
- C, bait and setup: Staraptor leads to be countered by the Rock and Steel walls, which draw Primeape's Bulk Up; Frosmoth's Quiver Dance and Snorlax's Curse wait behind. Closest of the three to the offense Ian wants to leave.

**What Ian decides.**

1. Twelve slots for each player (fifteen lines over the three versions), or twelve lines in all?
2. Turtonator only from Barry 4, so Barry 3 carries one partner per version, or at 34 in Barry 3 as well?
3. Barry 3's shape: B, A, C, or a mix.
4. Barry 3 at six members (today's has five)?
5. Luxray rests from Barry 5 on, because Mars carries one in her three later fights and Volkner at the Fight Area: keep that?
6. Buizel out of Barry 2 for Shinx?
7. Frosmoth, Goodra and Florges are picked for their roles more than Barry's character: keep them, or name lines he would rather have?
8. The Fight Area partner sits at 74 and 75, over the Barry split's cap of 71: bring it to 71?

**Next steps.** Ian answers in a line each. Then Barry 3's sets for the chosen shape, with the legality check and the AI-picks probe: about an hour. Barry 2's swap: minutes. Barry 5, the two partner fights and Barry 6 from the pool: an hour or two each, after Ian's Barry 4 lands. A spot-check reading only if he names one: two and a half to four hours.

## Part 1: the pool

### How the versions work

The scripts pick Barry's file by the player's starter. The suffix names the starter Platinum had in that seat, so `_chimchar` is the Scorbunny player's file (Scorbunny took Chimchar's place in the briefcase, and Barry keeps the Chimchar line for a Turtwig player; `lucas-dawn-2-redesign.md`, "Which starter meets which team"). Barry takes the starter strong against the player's: Infernape for a Turtwig player, Empoleon for a Scorbunny player, Torterra for a Piplup player.

Ian's Barry 4 (his OxiDex, not committed and not final) is Staraptor, Snorlax, Luxray and the starter in every version, with two of Serperior, Greninja and Turtonator: the two whose types the starter lacks. So every version carries one Fire, one Water and one Grass member, which is vanilla Platinum's pattern (Barry carried two of Floatzel, Rapidash and Roserade beside his starter) with other regions' Pokemon in place of the canon three. The pool keeps that: slots 1 to 3 change by version, slots 4 to 12 are shared.

The first partner at Barry 3 is the one a trainer can have at 35: Greninja (Frogadier evolves at 36) for the Turtwig and Piplup players and Serperior (Servine at 36) for the Scorbunny player. Turtonator has no evolution, so it is legal at any level; it waits for Barry 4 on Ian's word that a Turtonator can come only so early.

### The fights, and the bosses around them

The fights in play order (`tools/oxide/balance/fights.json`), with the boss fights near each and the lines the pool keeps out for them. Lines on ordinary trainers were not counted.

| Fight | Bosses around it | Kept out of the pool, or rested there |
|---|---|---|
| Barry 2 (Route 203, Roark's split) | Lucas and Dawn 1, Roark | Buizel's line (Floatzel is Wake's ace later) |
| Barry 3 (Route 209 gate, Maylene's split) | Fantina, Lucas and Dawn 2, Maylene, Tyche and Hermes 1 | Floatzel (Wake), Heracross (Maylene, Aaron), Decidueye (Fantina), Scyther and Lopunny (Lucas and Dawn) |
| Barry 4 (Pastoria, Wake's split) | Tyche and Hermes 1, Wake | Ian's six as it is |
| Barry 5 (Canalave, Byron's split) | Cyrus 1, Argo 1, Byron; Mars 2 just after | Luxray rested (Mars 2 carries one); Salamence, Gyarados, Bronzong, Metagross are the bosses' |
| Spear Pillar, beside the player | Tyche and Hermes 2, Mars and Jupiter, Cyrus 3 | Luxray rested (Mars carries one in the same battle); Shiftry out (Tyche and Hermes 2 field one in the double before) |
| Fight Area, beside the player | Volkner and Flint, the foes | Luxray rested (Volkner's), Ninetales out (Flint's in the League) |
| Barry 6 (League gate, Barry's split) | Volkner, Lucas and Dawn 3, the Elite Four | Ninetales (Flint), Heracross (Aaron), Roserade (Cynthia) |

Mars's cat theme takes the Litten and Sprigatito lines (Mars 1 fields Torracat and Floragato), so neither is a candidate partner. The starter slot is the one exception to the rule: the Turtwig player's Barry keeps Infernape, which Flint also carries at the Fight Area and in the League, as in vanilla.

Today's late Barry fields Ambipom, Floatzel, Heracross, Ninetales, Shiftry and Starmie; all six leave the pool, the first four for the reasons above or Ian's own Barry 4 choices, Starmie for room (Greninja holds the Water seat).

### Legality by level

Every stage in the pool table is one a trainer can have at that fight's level. The close ones are within two levels of an evolution, which is inside Ian's "not egregiously early":

| Member | Level | Evolves at |
|---|---|---|
| Snorlax, Barry 3 | 35 | Munchlax at 36 |
| Greninja, Serperior, Barry 3 | 35 | Frogadier, Servine at 36 |
| Annihilape, Goodra, Barry 5 | Barry 5's level, not set yet (its file's ace is 53) | Primeape, Sliggoo at 50 |

Frosmoth evolves from Snom by levelling near an Ice Rock and Florges from Floette with a Shiny Stone, so neither has a level bar. Barry 5 has no honour cap yet; if it lands under 50, Annihilape and Goodra become Primeape and Sliggoo there.

### The later fights, in a sentence each

Barry 5 is the first fight of the late pool: the three elements, Annihilape with Bulk Up, Goodra and a Quiver Dance Frosmoth, with Staraptor and Snorlax rested for once. At Spear Pillar, Barry fights beside the player against Mars and Jupiter with Snorlax, Dragonite and Florges, whose Wish and Helping Hand suit a partner. At the Fight Area his Togedemaru's Lightning Rod draws Volkner's Electric moves away from the player (the game redirects them in doubles; the simulator does not, as `simulator-gaps.md` lists), and Goodra takes both foes' types. Barry 6 is his canon core with Palmer's Dragonite: the three elements, Staraptor, Snorlax and Dragonite, with Frosmoth and Annihilape as the swap-ins if Ian wants it harder.

The post-game Survival Area rematches (Battleground files at 65 and 85, from the base ROM) are outside the road to the alpha; the late pool can fill them later, and the 85 sits past the game's 78.

## Part 2: Barry 3

### The evidence

The three files (cap 36 since 2026-10-29, ace at 36), with Speed as the scorer builds them. iv_scale 255, AI flags Basic, Evaluate Attack and Expert.

| Member | Level | Item | Ability | Nature | Speed | Moves |
|---|---|---|---|---|---|---|
| Ambipom | 34 | Silk Scarf | Technician | Jolly | 102 | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 35 | Sharp Beak | Intimidate | Adamant | 89 | Brave Bird, Close Combat, U-turn, Roost |
| Floatzel | 34 | Mystic Water | Swift Swim | Adamant | 93 | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 35 | Leftovers | Thick Fat | Careful | 36 | Body Slam, Earthquake, Curse, Ice Punch |
| Infernape (Turtwig player) | 36 | Sitrus Berry | Blaze | Jolly | 102 | Close Combat, Fire Punch, Mach Punch, U-turn |
| Empoleon (Scorbunny player) | 36 | Sitrus Berry | Torrent | Modest | 59 | Surf, Drill Peck, Ice Beam, Flash Cannon |
| Torterra (Piplup player) | 36 | Sitrus Berry | Thick Fat | Adamant | 56 | Wood Hammer, Earthquake, Crunch, Stone Edge |

The matchup screen (`plgoal3 --box barry_3 <seed> --screen`, seeds 1 to 3, the box at 36) gives these answers. Box 1 meets the Turtwig player's file, box 2 the Scorbunny player's, box 3 the Piplup player's.

| Box | In all 20 top sixes | Often |
|---|---|---|
| 1 | Glimmora | Kingler (Krabby held to 35) 13, Quagsire 12, Granbull 11, Probopass 10, Staraptor 9, Tentacruel 9 |
| 2 | Rotom | Staraptor 16, Seaking 10, Bastiodon 10, Cofagrigus 10, Arboliva 9, Cinderace (held to 34) 8 |
| 3 | Kingler (held), Breloom, Rotom | Machoke 15, Hariyama 6 |

The boxes' speed lines at 36: Talonflame 101, a held Cinderace 96, Salazzle 94, Liepard 93, Haunter 89, Staraptor 86, Tentacruel and Alolan Ninetales 82, Luxray, Pachirisu and Leafeon 78, Leavanny and Tsareena 76, Rotom, Golbat and Orbeetle 75, Glimmora 72, Kingler 64, Breloom 60, Hariyama 46, Machoke 42, Probopass 39, Quagsire 35, Bastiodon 32. The soft-cap box will sit lower once Ian approves that method, so every margin here leans a little toward the player.

### The diagnosis

The three faults Ian named are in the files. Staraptor's and Snorlax's sets are the textbook ones. Oxide's Empoleon has Attack 111 and Sp. Atk 86, so its Modest set of four special and mixed moves runs on its weaker stat. Last Resort works only after every other move has been used in one stay, and Ambipom's U-turn ends the stay, so it almost never fires.

The shape is hyper offense in the balance plan's sense (goal 1: high threat, few tactics, most turns called). Ambipom (102), Floatzel (93) and Staraptor (89) move before all but one or two catches in each box, and so does the Turtwig player's Infernape (102). That version carries three U-turns, two Close Combats and a Fake Out, and every damaging move on the team but Empoleon's is physical. It also has five members, not six.

The boxes answer it with typing. Rotom, in every top six of boxes 2 and 3, is immune to Normal, Fighting and Ground, nearly half the team's moves. Glimmora, in every top six of box 1, lays a layer of Toxic Spikes on Barry's side each time a physical move hits it. Kingler's Hyper Cutter, Granbull's Intimidate and the Rock and Steel walls (Probopass, Bastiodon) take the physical hits. Floatzel is Wake's ace one split later, the reason Ian dropped it from Barry 4. Natures repeat in every version: Adamant twice (three times for a Piplup player), and Jolly twice for a Turtwig player.

On the screen today's team is the hardest of anything here, because damage and Speed are all the screen counts. That is the signature of hyper offense, and the reason the shapes below read easier on it.

### Three shapes

Each shape was screened with provisional sets (moves only so the screen and the calculator have something to read; these are not proposed sets) and probed on box 1, with box 2 and 3 probes for the recommended one. The screen's score below is the top six's score divided by Barry's members: per member, the best answer's margin capped at 3, plus a little for a second answer, less 2 for a member nothing answers. Lower means the player's best six answers Barry less well.

| Team | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Today's five | 1.61 | 1.27 | 1.90 |
| Shape A | 2.68 | 3.16 | 2.86 |
| Shape B | 2.06 | 2.61 | 2.38 |
| Shape C | 2.99 | 2.98 | 2.56 |

The screen counts no status move, hazard or boost. Every shape trades damage for those, so these numbers say how much damage was given up, not how hard the fight is.

Damage figures are the calculator's lowest to highest roll as a share of the target's HP: Barry's members at their levels with top IVs, the player's catches at 36, Hardy, IVs of 15.

| Attacker | Move | Target | Damage |
|---|---|---|---|
| Primeape 34 | Close Combat | Bastiodon | 91 to 110% |
| Primeape 34 | Close Combat | Probopass | 116 to 137% |
| Primeape 34 | Rage Fist (a plain 50-power hit in Oxide) | Rotom | 34 to 41% |
| Luxray 34 | Crunch | Rotom | 90 to 106% |
| Greninja 35 | Night Slash | Rotom | 64 to 78% |
| Greninja 35 | Surf | Bastiodon | 41 to 50% |
| Snorlax 35 | Earthquake | Bastiodon | 55 to 66% |
| Staraptor 34 | Double-Edge | Breloom | 71 to 84% |
| Frosmoth 34 | Giga Drain | Quagsire | 98 to 117% |
| Frosmoth 34 | Ice Beam | Breloom | 140 to 166% |
| Togedemaru 34 | Zing Zap | Kingler | 61 to 73% |
| Rotom 36 | Shock Wave | Staraptor | 77 to 93% |
| Golbat 36 | Dual Wingbeat | Primeape | 61 to 72% |
| Togetic 36 | Dazzling Gleam | Primeape | 57 to 69% |
| Probopass 36 | Rock Blast (the runner's total) | Frosmoth | 141 to 176% |

#### Shape A: speed control

Barry cannot stand being slower, so his team makes the player slower.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Togedemaru 34 | Fake Out, Nuzzle and Zing Zap to paralyse and chip, U-turn out; Lightning Rod takes the Electric moves aimed at Staraptor and the Water members | 80 |
| 2 | Greninja 35, or Serperior 35 for a Scorbunny player | Icy Wind's Speed drop; Serperior sets Light Screen and Reflect | 111, 103 |
| 3 | Staraptor 34 | Tailwind, Intimidate, Double-Edge | 94 |
| 4 | Snorlax 35 | the slow anchor that paralysis and Tailwind let act first: Body Slam, Yawn, Rest | 32 |
| 5 | Frosmoth 34 | Quiver Dance behind the slowed field; Ice Scales halves special hits; Ice Beam, Giga Drain, Stun Spore | 59 |
| Ace | the starter, 36 | Infernape with Will-O-Wisp and Grass Knot, Empoleon with Icy Wind, Torterra with Zen Headbutt for the Fighting answers | 102, 59, 50 |

What it asks: keep the six's Speed, with Ground types (immune to Nuzzle), Natural Cure and hard hits before the slowed field turns. Cover: Frosmoth takes the Grass and Ground answers, Staraptor the Fighting ones, Snorlax the special hitters. The lead test: Togedemaru's counters are the Ground types (margins of 1.5 to 3.0 against it: Quagsire, Whiscash, Donphan, Graveler, Onix, Torterra), and the AI can send Frosmoth into them, with Giga Drain and Quiver Dance. That holds for Quagsire, but the Ground types with Rock moves (Graveler, Onix, Torterra's Rock Blast, Whiscash's Rock Tomb) knock Frosmoth out first, so the rule holds only in part. Against the answers: Rotom stays in every top six on boxes 2 and 3, and Bastiodon in 10 to 16. The probe's weakness is the shape's whole idea: the AI used Nuzzle 15 to 19 times in 100 fights, Tailwind 6 to 31, Quiver Dance 17 to 24, and took Zing Zap's damage instead.

#### Shape B: hazards and forced switches (recommended)

Barry will not let the player's Pokemon stay in.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Primeape 34 | Stealth Rock and Taunt on turn one; Close Combat for the Rock and Steel walls, Rage Fist for the Ghosts; Defiant punishes Granbull's Intimidate | 80 |
| 2 | Greninja 35, or Serperior 35 for a Scorbunny player | Spikes, Night Slash for Rotom, Surf, Ice Beam; Serperior sets Light Screen and Reflect, with Giga Drain and Knock Off | 111, 103 |
| 3 | Staraptor 34 | Whirlwind over the hazards, Intimidate, Double-Edge, Roost | 94 |
| 4 | Snorlax 35 | Yawn forces switches; Body Slam, Earthquake for the walls, Rest | 32 |
| 5 | Luxray 34 | Roar, Crunch for Rotom, Thunder Fang for the Flying and Water answers | 80 |
| Ace | the starter, 36 | Infernape with Knock Off, Empoleon with Knock Off and Earthquake, Torterra with Crunch and Synthesis | 102, 59, 50 |

What it asks: a plan with few switches. Every forced switch costs an eighth to a half of a Pokemon's HP to Stealth Rock, plus Spikes, and the player's answers to it are the boxes' Taunt users (Probopass, Bastiodon, Bibarel, Cinderace, Tsareena) and Defog where a catch has it. Cover: Primeape takes Bastiodon and Probopass, Luxray and Greninja take Rotom, Snorlax takes Fire and the special hits, Staraptor the Fighting and Grass answers. The lead test: Primeape's counters are the Flying, Fairy and Psychic catches (Golbat, Togetic, Mothim, Orbeetle, Granbull), which draw Luxray, and Luxray has no setup move, so Ian's permission for a wholly countered lead does not apply. The lead does its job anyway: it outspeeds Golbat (75) and Togetic (39), and its first move against them was Stealth Rock in 11 to 13 of the 16 or 17 fights each led. Against the answers: the hardest of the three on the screen; Rotom stays in every top six on boxes 2 and 3, Bastiodon in 8 to 16, Golbat 9 to 14, Togetic 8 to 15. The probe, on all three boxes: Stealth Rock was picked 78 to 89 times in 100 fights, Spikes 67 to 89, Roar 32 to 95, Whirlwind 9 to 145, Yawn 141 to 243, and every other move too except Knock Off, which went unpicked on all three members that carried it (Infernape, Serperior, Empoleon).

#### Shape C: bait and setup

The lead is meant to be countered, and its counters hand a setup member its turn.

| Slot | Member | Role and defining moves | Speed |
|---|---|---|---|
| Lead | Staraptor 34 | Intimidate, U-turn, Double-Edge, Steel Wing for Glimmora and Granbull | 94 |
| 2 | Primeape 34 | Bulk Up, Drain Punch, Rage Fist, Stone Edge | 80 |
| 3 | Frosmoth 34 | Quiver Dance, Ice Beam, Giga Drain | 59 |
| 4 | Snorlax 35 | Curse, Body Slam, Yawn, Rest | 32 |
| 5 | Greninja 35, or Serperior 35 for a Scorbunny player | Taunt against the player's own setup; Serperior with Calm Mind | 111, 103 |
| Ace | the starter, 36 | Infernape with Nasty Plot, Empoleon with Agility, Torterra with Rock Polish | 102, 59, 50 |

What it asks: never give a free turn, and beat each boosting member before it boosts. The lead test holds best here: Staraptor's counters are Bastiodon, Probopass and Rotom (a margin of 3.0 each), and the first two draw Primeape, whose Fighting moves hit them four times over, with Bulk Up on the turn the player switches out. Rotom draws Primeape too, but Rage Fist takes only a third of its HP. Against the answers: Rotom drops to 9 and 14 of the top sixes on boxes 2 and 3, but Bastiodon is in 17 to 20 and box 1 takes Tentacruel and Sylveon in all 20, the Water and Fairy answers to Frosmoth and Primeape. The probe used Curse about 250 times in 100 fights, Bulk Up 34, Quiver Dance 22. With four members that boost, the fight turns on one setup turn won or lost, which is the nearest of the three to the offense Ian wants to leave, only slower.

### Recommendation

Shape B. It is the only one whose tactics the AI plays in nearly every fight: hazards, phazing and Yawn are picked over and over on all three boxes, where shape A's AI skips its own speed control. It taxes switching, which is what a planned fight runs on, and it reads hardest of the three on the screen while doing it. It also leads into Ian's Barry 4, whose Glare, screens and Drum Beating are tactics of the same kind.

Its gaps are known. Rotom stays in every top six on boxes 2 and 3; Luxray's Crunch and Greninja's Night Slash answer it, but the Scorbunny player's version has Serperior in Greninja's seat, and the AI never picked the Knock Off its Serperior and Empoleon carried, so Luxray is that version's one sure answer until the sets stage finds another. It has no setup member, so a counter to the lead is safe once the rocks are down. And Primeape is a Fighting type one fight before Maylene's Fighting gym, so the Flying, Fairy and Psychic catches a player brings for her are already its answers.

### How the numbers were made

All on this branch at db48fd8ea, writing nothing under `res/`:

- The boxes and the screen: `PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgoal3 --run barry-pool-study --box barry_3 <seed> --screen`, seeds 1 to 3.
- The shapes: a scratch script that swaps each shape's six into all three Route 209 files in memory (wrapping `data.oxide_trainers` and `plscore.with_genders`, as the Fantina lead study did) and runs `plteam.screen` and `plteam.matchups`; the probe is the Fantina page's AI-picks probe (a greedy player, 100 rough fights a six, against the screen's best six and its six most taken; its win numbers mean nothing).
- Damage: `calc.run_node`, the runner every reading uses.
- Legality: the OxiDex's own list (`learnsets.oxide_list`) at each member's level. Every defining move on this page is in it.
