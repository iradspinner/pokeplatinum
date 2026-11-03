# Weather rocks that do nothing

## Summary

Ten trainer Pokemon hold a weather rock that cannot work, and this page proposes one working item for each. Nothing in the game has changed yet: the swaps wait on Ian's word (old questions sheet, question 13, "Swap ten now", 2026-11-02).

The twelve the sheet named are confirmed from the trainer files and the engine. In Oxide, as in Platinum, Drizzle, Drought, Sand Stream and Snow Warning set weather that lasts the whole battle, and a rock adds turns only to weather its own holder sets with Rain Dance, Sunny Day, Sandstorm or Hail. None of the twelve knows its weather move. Flint's Torkoal waits for the League's pass and Moira's Abomasnow on Mt. Coronet 5F for her next pass, so ten are swapped here.

Each replacement is an item the engine runs, the simulator runs right (it is on the simulator gaps page's list of items that run right, or among its fixed rows), and at least fifteen trainer files already hold. None repeats an item in its team, nor in the partner's team for the two Ace Trainers who fight in a pair. Five are Berries and five are other items, so the ten do not all read alike.

What Ian decides: yes to the ten as listed, or a different item for any of them. Once he answers, applying them takes a helper about twenty minutes, with a rebuild and the gate. The change is not material to difficulty for the seven ordinary trainers. For the three Ace Trainers it is one item on one member, which this page reads as not material unless Ian reads it otherwise.

Two more dead rocks turned up that the sheet did not name, of a different kind, and are listed after the table as a separate question.

## The ten swaps

| Trainer | Kind, where | Member and set | Rock now | Proposed | Why it suits the set |
|---|---|---|---|---|---|
| Ace Trainer Dalton | mini-boss, Route 217 (Candice) | Abomasnow 52, Mild, Snow Warning: Blizzard, Giga Drain, Ice Shard, Focus Blast | Icy Rock | Occa Berry | Fire hits it four times over, so halving the first Fire hit keeps the hail lead in to fire back a Blizzard. |
| Ace Trainer Jonah | mini-boss beside Brenda, Iron Island B2F (Byron) | Hippowdon 48, Impish, Sand Stream: Stealth Rock, Earthquake, Slack Off, Yawn | Smooth Rock | Passho Berry | Water is the usual answer to it; surviving one Water hit buys the turn for Stealth Rock or Yawn. |
| Ace Trainer Shannon | mini-boss beside Jake, Route 221 (Byron) | Ninetales 46, Calm, Drought: Flamethrower, Energy Ball, Will-O-Wisp, Protect | Heat Rock | Charcoal | Its Flamethrower in its own sun is the pair's one special Fire attack; the Charcoal adds a fifth. |
| Double Team Zac and Jen | ordinary, mandatory, Route 210 North (Byron) | Pelipper 43, Bold, Drizzle: Scald, Ice Beam, Tailwind, Protect | Damp Rock | Lum Berry | A Tailwind setter needs its turn, and the Berry stops one sleep or paralysis from taking it. |
| Fisherman Walter | gym trainer, Pastoria Gym (Wake) | Politoed 41, Bold, Drizzle: Scald, Ice Beam, Hypnosis, Haze | Damp Rock | Quick Claw | A slow old man's Politoed that now and then gets its Hypnosis in first; luck items are allowed on trainers. |
| Sailor Damian | gym trainer, Pastoria Gym (Wake) | Pelipper 41, Calm, Drizzle: Scald, Air Cutter, Roost, U-turn | Damp Rock | Wacan Berry | Electric is the box's answer to a rain gym and hits it four times over; the Berry lets it live to U-turn out. |
| Skier Edward | ordinary, mandatory, Route 216 (Candice) | Abomasnow 53, Quiet, Snow Warning: Blizzard, Wood Hammer, Ice Shard, Earthquake | Icy Rock | Expert Belt | A slow mixed attacker with four types of coverage; the Belt rewards the super-effective hit it is built to find. |
| Swimmer Evan | ordinary, optional, Route 213 by Surf (Byron) | Politoed 45, Bold, Drizzle: Surf, Ice Beam, Hypnosis, Protect | Damp Rock | Rindo Berry | Grass is what the player brings against a rain team; halving one Grass hit lets it sleep the answer. |
| Tuber Chelsea | ordinary, mandatory, Route 213 (Wake) | Pelipper 39, Bashful, Drizzle: Scald, Air Cutter, U-turn, Roost | Damp Rock | Sharp Beak | Air Cutter is its hit on the Grass types that come for a rain team, and the Beak adds a fifth. |
| Worker Conrad | ordinary, optional, Fuego Ironworks (Byron) | Torkoal 45, Relaxed, Drought: Stealth Rock, Lava Plume, Yawn, Rapid Spin | Heat Rock | Rocky Helmet | A slow physical wall that leads; the physical hitters sent to break it pay a sixth per contact hit. |

The items the rest of each team holds, which the proposals avoid: Dalton's Leftovers, Sitrus Berry, Charcoal and Magnet; Jonah's Leftovers, Life Orb and Yache Berry, with Brenda's Sitrus Berry, Eject Button, Expert Belt and Wise Glasses; Shannon's Sitrus and Lum Berries, with Jake's Scope Lens, Razor Claw and Expert Belt; Zac and Jen's Magnet, Leftovers, Life Orb and Wacan Berry; Walter's Never-Melt Ice and Soft Sand; Damian's White Herb and Black Glasses; Edward's Never-Melt Ice, Leftovers and Muscle Band; Evan's Miracle Seed and Dragon Fang; Chelsea's Mystic Water, Wide Lens and Sitrus Berry; Conrad's Wise Glasses, Passho Berry and Charcoal.

## Two more dead rocks, not in the sheet

Two other trainers hold a rock on a Pokemon that never sets that weather by move, so their rocks do nothing either. They fall outside question 13's twelve, which are rocks under the holder's own ability weather, so they are not part of the ten. Each could take one more swap with Ian's yes.

| Trainer | Member and set | Rock now | Possible item | Why |
|---|---|---|---|---|
| Camper Zackary, Route 205 South (Gardenia) | Castform 20, Quirky, Forecast: Icy Wind, Shock Wave, Water Pulse, Amnesia, beside a Snow Warning Snover | Icy Rock | Sitrus Berry | It sets up Amnesia, so a heal at half keeps it in; the team holds Never-Melt Ice and Eviolite. |
| Swimmer Katelyn, Route 220 (Byron) | Ludicolo 46, Calm, Swift Swim: Fake Out, Hydro Pump, Giga Drain, Ice Beam, on a team with no rain | Damp Rock | Mystic Water | Hydro Pump is its strongest hit; the team holds Black Belt and Soft Sand. |

Katelyn's Ludicolo also has Swift Swim on a team that never makes rain, so its ability does nothing as well. That belongs to her split's next look, not to this page.

## How it was checked

The engine's four ability scripts (`subscript_drizzle.s` and its three kin) set the permanent weather flag, and the four weather moves' effect scripts add the rock's turns only when the move's user holds it. A scan of every trainer file found 21 rock holders: the twelve above, the two extra, and seven whose holder knows the rock's weather move, so the rock works (Aroma Lady Elizabeth, Parasol Lady Sabrina, Twins Emma and Lil, Flint's rematch, Gardenia's and Volkner's rematches, and Marley at the Battleground). Each member's ability was read from its slot in the trainer file (slot 3 is the hidden ability, given after the Pokemon is built). Each split and map comes from the balance tools' split census, and each kind from the Byron, Candice and Wake split pages.
