# The simulator against Ian: one pair worked through

Pair 38 of `pairwise-candidates.md`: Dragon Tamer Ondrej (Victory Road B1F)
against Veteran Edgar (Victory Road 1F). Ian named Ondrej harder, "comical":
"almost as scary as you can make a three-Pokemon team with no items". The
simulator reads it the other way round. Both fights are in the Barry split,
so the player is at the cap of 71 and both trainers' Pokemon are at 63.

| Fight | Pokemon lost a battle | Lost three or more | HP spent | Battles won |
|---|---|---|---|---|
| Ondrej | 0 | 0% | 3.6% | 100% |
| Edgar | 0.005 | 0% | 14.1% | 100% |

These are 200 battles each, with the planned team (the rebuild's design:
the six a player prepared for this fight would bring), after the sleep fix
of 2026-09-27.

## The teams

Ondrej's (AI flags Basic, Evaluate Attack and Expert; no items):

| Pokemon | Level | Ability | Moves | Speed |
|---|---|---|---|---|
| Altaria | 63 | Serene Grace | Dragon Dance, Outrage, Sky Attack, Perish Song | 137 |
| Salamence | 63 | Intimidate | Draco Meteor, Hidden Power, Heat Wave, Tailwind | 150 |
| Kingdra | 63 | Swift Swim | Ice Beam, Hydro Pump, Agility, Dragon Pulse | 116 |

The planned team, all at 71. The pre-pass tried 40 random sixes from the
strongest third of the Barry split's side for 10 battles each: they lost
0.61 Pokemon a battle on average, the best none and the worst 2.2. The five
best then played 40 more battles each; three of them lost nothing, and the
one kept spent the least HP (3.2%). Each Pokemon has its three strongest
attacks of different types and its best status move by Ian's tiers, and
the side's usual item.

| Pokemon | Item | Ability | Moves | Speed |
|---|---|---|---|---|
| Primarina | Choice Specs | Torrent | Hydro Pump, Moonblast, Hyper Voice, Encore | 100 |
| Feraligatr | Life Orb | Intimidate | Hydro Pump, Giga Impact, Focus Blast, Substitute | 130 |
| Hawlucha | Life Orb | Limber | High Jump Kick, Fly, Tailwind | 183 |
| Castform | Choice Specs | Forecast | Solar Beam, Blizzard, Fire Blast, Substitute | 157 |
| Tsareena | Life Orb | Leaf Guard | High Jump Kick, Leaf Storm, Stomp, Aromatherapy | 146 |
| Gallade | Life Orb | Hyper Cutter | Close Combat, Giga Impact, Psychic, Taunt | 129 |

All 200 battles on this team lost nothing. The typical one and the worst one
(the most HP spent) follow. The AI's scores are the ones its flags gave each
move that turn; the highest wins, ties at random.

## A typical battle

```
Ondrej sends out Altaria; you send out Primarina (the best answer to lead).
Turn 1  Altaria: Dragon Dance. Scores: Dragon Dance 100, Sky Attack 100,
        Perish Song 100, Outrage 90 (Primarina is immune to Dragon, so
        Basic takes 10). Altaria +1 Attack, +1 Speed.
        Primarina: Moonblast, 187. Altaria 0/187, faints.
Turn 2  Ondrej sends out Kingdra.
        Kingdra: Hydro Pump, 32. Scores: Hydro Pump 100 (its strongest),
        Ice Beam 99, Agility 97, Dragon Pulse 89. Primarina 173/205.
        Primarina: Moonblast, 185. Kingdra 0/185, faints.
Turn 3  Ondrej sends out Salamence.
        Salamence: Hidden Power, 17. Scores: Hidden Power 100, Heat Wave 100,
        Tailwind 100, Draco Meteor 88. Primarina 156/205.
        Primarina: Moonblast, 212. Salamence 0/212, faints. You win.
```

## The worst battle

```
Turn 1  Altaria: Dragon Dance (same scores). Primarina: Moonblast, 187; faints.
Turn 2  Kingdra: Hydro Pump, a critical hit, 68. Primarina 137/205.
        Primarina: Moonblast, 185; Kingdra faints.
Turn 3  Salamence: Heat Wave, 23, and burns Primarina. Primarina 114/205.
        Primarina: Moonblast, 212; Salamence faints. Burn: Primarina 89/205.
        You win, nothing lost.
```

## Why the simulator reads it easier than Ian

Mostly the team, partly the play, and a little it does not model. The
planned six brings Primarina, whose Moonblast is super-effective on all
three Dragons, and at 71 against 63 it knocks each out in one hit before
any of their speed setup matters: Altaria's Dragon Dance on turn one is
wasted, and Salamence never gets Tailwind up. Such an answer is common, not
lucky: 39 of the 147 Pokemon in the strongest third carry a Fairy, Ice or
Dragon attack, and even random strong sixes, unplanned, lose only 0.58
Pokemon a battle, and three or more 3% of the time. Planning from a
realistic box (one run's catches by the Barry split) changes nothing here,
since by then a box holds an answer too. What Ian fears is the battle where
that answer is missing or slower: a Dragon Dance Altaria's Outrage, a
Tailwind Salamence's Draco Meteor or an Agility Kingdra sweeping a team
that cannot knock them out first. The simulator plays the player's side
well, leading with the best answer every time. It also leaves one thing
out that makes Ondrej easier than he is: Perish Song does nothing in the
simulator, yet his AI scores it level with his best moves and picks it now
and then, wasting a turn. So the gap is that the reading asks "how badly
can it go for a prepared player", and for this fight the honest answer is
"hardly at all", while Ian judges the threat a team poses to a box that
might lack the answer.
