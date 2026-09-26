# Friendship evolutions: a proposal for Ian

Written 2026-09-27 by the encounter track, from Ian's Pocket PC rulings of the
same day as relayed by the Overseer: Happiness Up is gone, and every
friendship evolution moves to a method that cannot be ground as easily. The
data has sixteen friendship evolutions over fifteen lines. This proposes one
method each, says the split it lands in, and measures what it changes in the
encounter tables and the box simulator. Nothing here is built; the main
track edits the evolution data once Ian rules.

A level is the default. Oxide has hard level caps, and the Pocket PC hands
out Rare Candies without limit, so a level evolution happens the moment the
cap allows it and never earlier. There is nothing left to grind, and the
level alone decides the split. Hardlove had already moved seven of these
lines to a plain level, and its numbers are used wherever they land in a
sensible split. Two lines take a place instead, because Platinum already has
a place that suits them and a place is gated by progress. Eevee takes stones,
since five of its other six evolutions are already stones or places. Every
method is one Platinum's engine already runs, so none of this needs engine
work.

| Line | Evolution | Now | Proposed | First possible | Wanted |
|---|---|---|---|---|---|
| Zubat | Golbat to Crobat | friendship | level 36, Hardlove's | Maylene, cap 38 | no |
| Happiny | Chansey to Blissey | friendship | level 40 | Wake, cap 44 | no |
| Pichu | Pichu to Pikachu | friendship | level 10, Hardlove's | Roark (the Sandgem clown) | no |
| Cleffa | Cleffa to Clefairy | friendship | level 10 | Gardenia (Coronet's north room) | no |
| Togepi | Togepi to Togetic | friendship | level 10, Hardlove's | Fantina, as Cynthia's egg hatches | yes |
| Azurill | Azurill to Marill | friendship | level 10, Hardlove's | Fantina (Amity Square) | no |
| Budew | Budew to Roselia | friendship by day | level up at the Moss Rock | Gardenia (Eterna Forest) | yes |
| Buneary | Buneary to Lopunny | friendship | level 20, Hardlove's | Gardenia, cap 26 | yes |
| Chingling | Chingling to Chimecho | friendship by night | level 20 | Gardenia (Route 211 west) | no |
| Munchlax | Munchlax to Snorlax | friendship | level 36 | Maylene, cap 38 | no |
| Riolu | Riolu to Lucario | friendship by day | level 28, Hardlove's | Byron, as Riley's egg hatches | no |
| Eevee | Eevee to Espeon | friendship by day | Sun Stone | Fantina (Bebe's Eevee) | yes |
| Eevee | Eevee to Umbreon | friendship by night | Moon Stone | Fantina (Bebe's Eevee) | yes |
| Luvdisc | Luvdisc to Alomomola | friendship, Oxide's own | level 30 | Byron (the Old Rods) | no |
| Snom | Snom to Frosmoth | friendship by night | level up at the Ice Rock | Candice (Route 217) | no |
| Igglybuff | Igglybuff to Jigglypuff | friendship | level 10 | off the pick-list | no |

Notes on the choices, line by line where there is a choice to make.

Crobat at 36 keeps an A-rated line out of Fantina's split. Zubat is in nearly
every early cave, so an earlier Crobat would sit in almost every box; 40
would push it to Wake if Ian wants it later still. Blissey at 40 lands in
Wake. Chansey itself still needs the Oval Stone held by day, which is on
Lost Tower 2F and in the Underground, and Happiny's only table is Route 208
at 8%. Snorlax at 36 matters because Munchlax is in the honey trees from
one badge; the trees give Snorlax itself from six badges.

The four babies go to 10, which is Hardlove's rule, so each evolves at its
first level-up after capture. Togekiss still needs a Shiny Stone (Iron Island
B3F and Route 228), so the egg's line stays gated where it is now.

Budew at the Moss Rock puts Roselia in Gardenia's split, on the road through
Eterna Forest. Hardlove's level 16 is the alternative, but 16 is Roark's cap,
so Roselia would be ready for Roark's gym. Frosmoth at the Ice Rock matches
the tables, which already place Frosmoth from Candice's split on, and it
means the one early Snom (Coronet 1F south, 1%) stays a Snom until Route 217.

Espeon and Umbreon by stone depend on where the stones are. Today the Sun and
Moon Stones come only from digging in the Underground, which the Explorer Kit
opens before Bebe's gift. The item pass may want to place one of each as a
fixed find, so a wanted line does not wait on the luck of the dig. Eevee
keeps eight of its nine evolution slots, as now.

Luvdisc to Alomomola is Oxide's own evolution, not canon's or Hardlove's.
Level 30 leaves it where the tables and the simulator already have it.

## What it changes in the tables

Ian's rule of 2026-09-21 is that a wild Pokemon stands at the stage its level
has earned, and `cli evolve` applies it. Under these methods its next run,
which is already due for Maylene's final cap, would evolve nine slots:

| Table | Now | Becomes | Level |
|---|---|---|---|
| Route 205 south | Pichu | Pikachu | 12 |
| Valley Windworks | Pichu | Pikachu | 12 |
| Amity Square | Pichu | Pikachu | 11 |
| Trophy Garden | Pichu | Pikachu | 22 |
| Mt. Coronet 1F north room 1 | Cleffa | Clefairy | 14 |
| Great Marsh 1 | Azurill | Azumarill | 30 |
| Route 212 north | Buneary | Lopunny | 22 |
| Trophy Garden | Buneary | Lopunny | 23 |
| Valor Lakefront | Buneary | Lopunny | 27 |

Four Crobat slots sit below a level-36 Crobat: Mt. Coronet 1F north room 2
and B1F at 33, Route 216 at 34, and Turnback Cave at 35. The evolve pass only
moves a slot forward, so those need a hand edit. My pick is Golbat, which
leaves every level ladder alone; raising their floors to 36 is the other way.

## What it changes in the box simulator

The simulator scores a Pokemon by the stage it reaches by each split's cap.
Only these differ, all below the worth of 85 that Ian's scarcity rule
watches:

| Line | Split | Now | Proposed |
|---|---|---|---|
| Zubat | Fantina | Crobat, 76.9 | Golbat, 61.8 |
| Happiny | Fantina and Maylene | Blissey, 74.8 | Chansey, 59.2 |
| Munchlax | Fantina | Snorlax, 82.8 | Munchlax, 54.6 |
| Pichu | Roark and Gardenia | Pichu, 23.4 | Pikachu, 34.5 |
| Cleffa | Roark and Gardenia | Cleffa, 24.2 | Clefairy, 38.8 |
| Togepi | Roark and Gardenia | Togepi, 31.5 | Togetic, 63.2 |
| Azurill | Gardenia | Azurill, 24.9 | Azumarill, 59.4 |
| Buneary | Gardenia | Buneary, 32.1 | Lopunny, 57.7 |
| Chingling | Gardenia | Chingling, 28.1 | Chimecho, 55.2 |

The evolve pass and the simulator have both been reading every friendship
evolution as level 32, not the 20 their shared code comment promises, because
the table of judged levels names methods the data spells differently. The
same slip reads a held-item trade as 32 rather than 38. The numbers above
compare against what the tools do today. Once Ian rules, the friendship
entries go and the trade one is corrected in the same commit, and the
simulator's suite is rerun.
