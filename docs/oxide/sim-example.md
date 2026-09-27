# The simulator against Ian: one pair worked through

Pair 38 of `pairwise-candidates.md`: Dragon Tamer Ondrej (Victory Road B1F)
against Veteran Edgar (Victory Road 1F). Ian named Ondrej harder, "comical":
"almost as scary as you can make a three-Pokemon team with no items". Both
fights are in the Barry split, so the player is at the cap of 71 and both
trainers' Pokemon are at 63.

This is the second version (2026-09-27). The first gave the planned team
two Choice Specs and four Life Orbs and movesets no player runs, and Ian
found that to be the main cause. The player's side now follows his rules:
no Life Orb and no Choice item; the best offensive item is a type booster
(1.2 times), one per type and only where it is found by the split, with
Leftovers and Sitrus Berries as found; moves are what the Pokemon can have
by the split (the capture rule, TMs and tutors), ranked by their worth in
play (recharge, recoil, lock-in and self-drops weigh them down, and charge
moves are left out); and each Pokemon has one of its two regular abilities
at random, as a catch would. Perish Song and Intimidate now work in the
simulator too.

| Fight | Pokemon lost a battle | Lost three or more | HP spent | Battles won |
|---|---|---|---|---|
| Ondrej | 0.03 | 0% | 5.8% | 100% |
| Edgar | 0.04 | 0% | 8.2% | 100% |

These are 200 battles each with the planned team. The two now read close
together, where the first version read Ondrej far easier (3.6% against
14.1%), but Ian's order is still not reproduced.

## The teams

Ondrej's (AI flags Basic, Evaluate Attack and Expert; no items):

| Pokemon | Level | Ability | Moves | Speed |
|---|---|---|---|---|
| Altaria | 63 | Serene Grace | Dragon Dance, Outrage, Sky Attack, Perish Song | 137 |
| Salamence | 63 | Intimidate | Draco Meteor, Hidden Power, Heat Wave, Tailwind | 150 |
| Kingdra | 63 | Swift Swim | Ice Beam, Hydro Pump, Agility, Dragon Pulse | 116 |

The planned team, all at 71. The pre-pass tried 40 random sixes from the
strongest third of the Barry split's side for 10 battles each (0.24 Pokemon
lost a battle on average, the best none, the worst 1.7). The five best
played 40 more battles each; two lost nothing, and the one kept spent the
least HP (7.9%).

| Pokemon | Item | Ability | Moves | Speed |
|---|---|---|---|---|
| Starmie | Mind Plate | Magic Guard | Psychic, Surf, Ice Beam, Toxic | 178 |
| Flareon | Charcoal | Flash Fire | Overheat, Superpower, Take Down, Toxic | 107 |
| Mismagius | Spell Tag | Levitate | Shadow Ball, Energy Ball, Psychic, Toxic | 164 |
| Yanmega | Silver Powder | Speed Boost | Bug Buzz, Air Slash, Psychic, Toxic | 150 |
| Orbeetle | Sitrus Berry | Swarm | Bug Buzz, Psychic, Body Press, Recover | 143 |
| Gliscor | Soft Sand | Sand Veil | Earthquake, Aerial Ace, Aqua Tail, Toxic | 150 |

Over 200 battles this team lost nothing in 197, one Pokemon once and two
twice. The AI's scores below are the ones its flags gave each move that
turn; the highest wins, ties at random.

## A typical battle

```
Ondrej sends out Altaria; you send out Starmie (the best answer to lead).
Turn 1  Starmie is faster: Ice Beam, 187. Altaria 0/187, faints before it
        moves (it had picked Dragon Dance, 101 to Outrage's 100).
Turn 2  Ondrej sends out Salamence. Starmie: Ice Beam, 212. Salamence
        faints before it moves (it had picked Tailwind).
Turn 3  Ondrej sends out Kingdra. Starmie: Psychic, 86. Kingdra 99/185.
        Kingdra: Agility (Agility 100, Dragon Pulse 100, Ice Beam 99,
        Hydro Pump 99). Kingdra +2 Speed, now faster than Starmie.
Turn 4  Kingdra: Dragon Pulse, 54 (Agility is out of PP, scored -1).
        Starmie 122/176. Starmie: Psychic, 94. Kingdra 5/185.
Turn 5  Kingdra: Dragon Pulse, 58. Starmie 64/176.
        Starmie: Psychic, 5. Kingdra faints. You win, nothing lost.
```

## The worst battle

```
Turns 1 to 3 as above: Starmie's Ice Beam knocks out Altaria and
        Salamence, and Kingdra uses Agility at 99/185.
Turn 4  Kingdra: Dragon Pulse, a critical hit, 116. Starmie 60/176.
        Starmie: Psychic, 87. Kingdra 12/185.
Turn 5  Kingdra: Dragon Pulse, 60. Starmie faints.
Turn 6  You send out Yanmega. Kingdra: Ice Beam, a critical hit, 213.
        Yanmega faints.
Turn 7  You send out Flareon. Kingdra: Hydro Pump, 146. Flareon 37/183.
        Flareon: Superpower, 12. Kingdra faints. You win, two lost.
```

## Why the simulator still reads it easier than Ian

With his item and moveset rules applied, the gap is no longer the items;
it is the eight levels and the preparation. A prepared six at 71 brings an
Ice or Fairy attacker that outspeeds Altaria and Salamence and knocks each
out in one hit before Dragon Dance or Tailwind matters, and 48 of the 147
Pokemon in the strongest third carry such an attack. What makes Ondrej
dangerous is still visible: the worst battle is Kingdra after one Agility,
faster than everything and taking two Pokemon with two critical hits. Even
unprepared, random strong sixes lose only 0.41 Pokemon a battle and three
or more 1.3% of the time, and a planned six from a realistic box (one run's
catches by the Barry split) loses 0.015. So at the cap the simulator finds
Ondrej a short fight for a prepared player, and the threat Ian judges is
what his team does to a box that meets it without that answer, or at
closer levels. Whether the score should read the unprepared case, or the
trainers of Victory Road sit nearer the cap, is his call.

# A boss pair: Lucian against Bertha

Pair 36: Ian named Lucian harder than Bertha, "a lot". Of his 14 pairs of
story fights, 10 now read in his direction with the player-side fixes; this
is the clearest of the four that don't (the Fight Area's fight is a fifth,
set aside until its aces come down to 71). Each Elite Four fight is played
at its own ace's level, as Ian levels: Lucian at 75, Bertha at 73.

| Fight | Pokemon lost a battle | Lost three or more | Wipe | Battles won |
|---|---|---|---|---|
| Lucian | 2.78 | 45% | 13.5% | 86.5% |
| Bertha | 3.43 | 56.5% | 25% | 75% |

Both read as hard fights, and the simulator puts Bertha above Lucian, the
other way round from Ian. The two readings also move between runs by more
than they should: an earlier run of Bertha, before one sandstorm fault was
fixed, lost three or more 95.5% of the time. The planned team is a noisy
pick, which the fit has to address.

Lucian (AI flags Basic, Evaluate Attack, Expert and Setup First Turn):

| Pokemon | Level | Item | Moves | Speed |
|---|---|---|---|---|
| Espeon | 74 | Light Clay | Psychic, Signal Beam, Reflect, Light Screen | 206 |
| Exeggutor | 74 | Choice Specs | Psychic, Leaf Storm, Sludge Bomb, Ancient Power | 108 |
| Metagross | 74 | Choice Band | Zen Headbutt, Meteor Mash, Earthquake, Thunder Punch | 143 |
| Alakazam | 74 | Life Orb | Psychic, Energy Ball, Focus Blast, Recover | 223 |
| Slowking | 74 | Leftovers | Psychic, Surf, Ice Beam, Slack Off | 71 |
| Gallade | 75 | Choice Scarf | Drain Punch, Psycho Cut, Leaf Blade, Stone Edge | 217 |

Bertha (AI flags Basic, Evaluate Attack, Expert and Weather): Hippowdon 72
(Leftovers, Sand Stream; Earthquake, Stone Edge, Thunder Fang, Yawn),
Gliscor 72 (Choice Scarf; Earthquake, U-turn, Fire Fang, Thunder Fang),
Nidoking 72 (Shuca Berry; Earthquake, Stone Edge, Poison Jab, Sucker
Punch), Golem 72 (Passho Berry; Earthquake, Fire Punch, Thunder Punch,
Stone Edge), Flygon 72 (Yache Berry; Outrage, Earthquake, Thunder Punch,
Roost), Rhyperior 73 (Choice Band; Earthquake, Rock Wrecker, Megahorn,
Thunder Punch). The trainers keep their Choice items; Ian's rule is the
player's.

The planned team against Lucian, all at 75: 40 random strong sixes lost
5.18 a battle on average in the pre-pass (the best 1.9), and of the five
best, played 40 more battles each, the kept one lost 2.48.

| Pokemon | Item | Ability | Moves |
|---|---|---|---|
| Jynx | Never-Melt Ice | Snow Cloak | Ice Punch, Psychic, Energy Ball, Toxic |
| Gyarados | Mystic Water | Intimidate | Aqua Tail, Earthquake, Fire Blast, Toxic |
| Steelix | Soft Sand | Rock Head | Earthquake, Flash Cannon, Double-Edge, Toxic |
| Dusknoir | Spell Tag | Levitate | Shadow Punch, Earthquake, Fire Punch, Toxic |
| Kleavor | Silver Powder | Swarm | Leech Life, Stone Edge, Close Combat, Swords Dance |
| Ceruledge | Charcoal | Flash Fire | Flare Blitz, Psycho Cut, Clear Smog, Swords Dance |

Over 200 battles it lost 2.45 on average: none twice, one 42 times, two
71, three 58, four 15, five once, and all six 11 times.

## A typical battle (three lost)

```
Turn 1   Espeon: Reflect (102, over Psychic 100). Dusknoir: Shadow Punch, 154.
Turn 2   Espeon: Psychic, 75 to Dusknoir. Dusknoir: Shadow Punch (critical), Espeon faints.
Turn 3   Exeggutor in; you switch to Ceruledge. Leaf Storm (Choice Specs), 100.
Turn 4   Ceruledge: Flare Blitz, 246, Exeggutor faints; recoil leaves Ceruledge 26/208.
Turn 5   Slowking in. Ceruledge: Flare Blitz, 69, recoil to 3. Slowking: Surf; Ceruledge faints.
Turn 6   Kleavor in: Leech Life (critical), Slowking faints.
Turn 7   Metagross in: Meteor Mash (Choice Band), 201; Kleavor faints.
Turn 8   Steelix in; Meteor Mash, 42. Steelix: Earthquake, 137; Metagross faints.
Turns 9 to 10  Gallade (Choice Scarf) Drain Punch twice, Steelix to 8; two Earthquakes, Gallade faints.
Turn 11  Alakazam in (Life Orb): Energy Ball; Steelix faints.
Turn 12  Gyarados in; Alakazam's Psychic, 136. Gyarados: Aqua Tail, 150; Alakazam faints. Won.
```

## The worst battle (a wipe)

```
Turn 1   Espeon: Reflect. Dusknoir: Shadow Punch (critical), 200; Espeon faints.
Turns 2 to 3  Exeggutor in; you switch to Ceruledge. Leaf Storm, 102. Flare Blitz, 234
         (Exeggutor 12/246, Ceruledge 28 after recoil). Leaf Storm again (critical,
         locked by Choice Specs): Ceruledge faints.
Turn 4   Dusknoir in; Leaf Storm, 51. Shadow Punch, Exeggutor faints.
Turns 5 to 8  Metagross in: Meteor Mash, 130 to Dusknoir; you switch to Steelix. Three
         Meteor Mashes against three Earthquakes; Metagross faints, Steelix at 121.
Turn 9   Slowking in: Surf, 121; Steelix faints.
Turn 10  Kleavor in: Leech Life, 246; Slowking faints.
Turns 11 to 12  Gallade in: Stone Edge twice; Kleavor faints.
Turn 13  Gyarados in; Stone Edge, 200. Aqua Tail; Gallade faints.
Turn 14  Alakazam in: Focus Blast; Gyarados faints.
Turns 15 to 16  Jynx in; Focus Blast misses, Ice Punch, 104. Focus Blast (critical), 193;
         Jynx faints.
Turn 17  Dusknoir in: Psychic, 72; Dusknoir faints. Lost, with Alakazam at 28/186.
```

## Why the simulator reads Bertha harder than Lucian

It reads Lucian much as Ian would expect: Reflect first, a Choice Specs
Leaf Storm, a Choice Band Meteor Mash and the two fastest Pokemon of the
split (the Scarf Gallade and the Life Orb Alakazam) cost a prepared team
about two and a half Pokemon, and a crit or two turns it into a wipe. What
it rates higher in Bertha is mostly her sandstorm and her six Ground hits.
Sand Stream stays up the whole fight and takes a sixteenth a turn from
every one of the player's Pokemon that is not Rock, Ground or Steel, which
over a long fight is most of a Pokemon; and every one of her Pokemon
carries Earthquake and a Rock or Electric answer to the usual Ground
counters, with a Choice Scarf Gliscor to strike first after a faint. Ian
may be judging that her team is predictable and walled by Levitate, Flying
and Water, which is true of a hand-picked six, while the simulator's
prepared six comes from 40 random candidates and may lack enough of them.
Two things the simulator does not do would move the reading toward Ian:
its player never baits a Choice lock and switches to an immune Pokemon
(Ian's own advice against a Choice-locked boss), and its planned team is
not stable enough to rank two hard fights this close. Both are for the
fit: more candidates in the pre-pass, and a Choice-aware player.
