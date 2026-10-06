# Learnset insight sessions: Ian's verdicts and the rules drawn from them

Step 2 of `docs/oxide/learnset-checks.md`. Each session shows Ian one line as
a player meets it, and he says what is wrong and why. His words are kept
verbatim. The rules drawn from them are general, for the generator and for
new checks, never patches for one species. The fifteen other lines come
first; then the rules are locked; only then does Ian judge the five held out
as the exam (Scorbunny, Treecko, Eevee, Koffing, Skorupi), so his verdicts on
them cannot shape the rules they test (Ian, 2026-10-06).

## 1. Charmander (2026-10-06)

Shown: Oxide's lists today. Charmander caught at 8 on Route 207 knows
Scratch, Growl and Ember; Smokescreen 10 and Dragon Rage 16; Charmeleon at 16
learns only Scary Face (21) in Gardenia's split, then Fire Fang 28 and Slash
32; Charizard (Fire/Dragon) at 36 learns Wing Attack 36, Flamethrower 42,
Fire Spin 49, Heat Wave 59 and Flare Blitz 66; its Dragon Claw, Shadow Claw
and Air Slash sit only at level 1.

Ian's verdict, verbatim:

1. Not enough move choices before Roark when Dragon Rage is removed; ideally
   5-6 moves by 16 so that choices are made in the first split.
2. Charmeleon learning only scary face is farcical, it should learn 2-3
   moves by 26 (or if it is delayed could learn those moves).
3. Charmeleon/Charizard is primarily a special attacker, so it getting fire
   fang in Gardenia split is totally fine.
4. Wing attack being delayed until Maylene split is ridiculous, that should
   come in gardenia split.
5. As it stands, the line learns precisely 0 coverage moves, which is not
   tenable (debatably wing attack is coverage).
6. Fire spin after flamethrower is redundant.
7. In Kaizo, the line learns the following coverage moves (ignoring lvl 1
   moves for charizard as those are likely trainer only, TMs not included):
   bite, metal claw, crunch, dragon pulse, wing attack, dragon claw, steel
   wing, air slash, seismic toss.
8. The line has access to 3 (debatably 4) utility moves total: growl
   (relatively useless), smokescreen (relatively useless), scary face
   (good), and fire spin (pretty bad but sometimes niche). While this isn't
   much better in Kaizo, these utility moves on a not-as-offensive pokemon
   would be slim pickings at best.
9. The charmeleon charizard delay is meaningless because 36 and 39 are
   within the same split, ergo it is always better to delay.

The rules drawn from it:

- **R1, choice from the first split.** By its first split's cap a line knows
  or has learned about five or six usable moves, more than its four slots,
  so the player chooses a moveset from the start.
- **R2, steady learning.** Every stage learns two or three new moves in each
  split it spends at the cap. A split that brings one status move is a
  failure. A stage reached late may learn the moves it would have missed.
- **R3, the off-side stat fills early gaps.** An early own-type attack on the
  line's weaker attacking stat (a physical Fire Fang on a special Charmeleon)
  is a safe way to fill a gap, because it does not hit as hard as its power
  says. Power is judged against the stat the move uses.
- **R4, coverage starts early.** A line's first coverage move comes by its
  second split, not with its last evolution.
- **R5, coverage breadth.** Every line learns several coverage moves by
  level-up over the game; none is untenable. Kaizo's list for the line is
  the reference for which types (here Dark, Steel, Dragon, Flying,
  Fighting), weaker early and stronger later.
- **R6, no dominated moves.** A move of the same type and role, weaker than
  one already learned (Fire Spin after Flamethrower), is wasted. A binding or
  other distinct effect can earn a place, but rarely.
- **R7, utility has quality.** Status moves differ in worth: Scary Face is
  good, Growl and Smokescreen nearly useless, Fire Spin niche. A line needs
  at least one good utility move, and a less offensive line needs more.
- **R8, evolution choices cross a split.** Holding an evolution, or a move
  learned at a different level by two stages, is only a choice if the two
  options fall in different splits. Inside one split the later option always
  wins, so it is no choice.
- Confirmed: Dragon Rage leaves the line's early list, and an evolved
  form's level-1 moves are the trainers' palette.

Checks these imply, to add to `learncheck.py` (checks 7 to 11): moves by the
first cap (R1); new moves per stage per split (R2); coverage count and the
split of the first coverage move (R4, R5); dominated moves (R6); utility
quality against a tier list of status moves (R7); evolution and learn-level
choices that stay inside one split (R8).

## 2. Budew (2026-10-06)

Shown: Budew caught at 3 to 5 on Route 204 knows Absorb (and Growth); it
learns Growth 4, Water Sport 7, Stun Spore 10, Mega Drain 13 and Worry Seed
16, then nothing. Roselia (by levelling beside Eterna Forest's Moss Rock)
learns Poison Sting 7, Leech Seed 16, Magical Leaf 19, Grass Whistle 22, Giga
Drain 25, Toxic Spikes 28, Sweet Scent 31, Ingrain 34, Toxic 37, Petal Dance
40, Aromatherapy 43 and Synthesis 46, but none below the level it evolves
at. Roserade (Shiny Stone) has only level-1 moves. The table shown left out
Poison Sting and Synthesis, which Ian pointed out.

Ian's verdict, verbatim:

1. No poison move as buden is disappointing, but okay.
2. Water sport, stun spore, worry seed, and growth are a fantastic set of
   utility moves early: The line has 0 coverage moves ever; same feedback
   from charmander.
3. Giga Drain, Toxic Spikes, Stun Spore, (coverage move/poison move) seems
   like a very good moveset for most of the game with Toxic and Petal Dance
   as options as well; one thing to keep in mind with Petal
   Dance/Outrage/Uproar/etc. is that they lock you in for 2 to 3 turns which
   makes them extraordinarily dangerous to use in a nuzlocke with
   permadeath. Kaizo changes them to one-turn-use moves for a reason. As it
   stands, I would personally never ever use them in a run.
4. Sweet scent is nearly useless, water sport is mostly useless, growth is
   mostly useless (too slow), ingrain is too dangerous (can't be switched
   out), aromatherapy is quite niche but usable, worry seed is very niche
   and mostly not usable.
5. Its fine to have roserade learn moves very late in the game (probably
   3+splits after roselia) to make it not feel as bad evolving it early and
   to make it not be as awful if you catch roserade later in the game with a
   bad learnset.
6. FYI you call out Synthesis and Poison Sting but they don't show up on
   your table, so I don't know when they are learned; synthesis is fantastic
   and poison sting should be in Roark split.

Point 2's "fantastic" reads as ironic beside point 4, which rates three of
its four moves as mostly useless; Stun Spore is the one of them in his good
moveset in point 3.

The rules drawn from it:

- **R5 again, coverage.** No coverage ever is the same failure as
  Charmander's.
- **R7, the utility tiers so far.** Fantastic: Synthesis. Good: Scary Face,
  Stun Spore, Toxic Spikes, Toxic. Niche but usable: Aromatherapy, Fire Spin.
  Very niche, mostly unusable: Worry Seed. Mostly useless: Growth (too slow),
  Water Sport, Growl, Smokescreen. Nearly useless: Sweet Scent. Too
  dangerous: Ingrain (it stops the player switching out).
- **R9, rampage moves are unusable as they stand.** Petal Dance, Outrage,
  Thrash, Uproar and the like lock the user in for two or three turns, which
  Ian would never risk in a permadeath run. Until he rules on Kaizo's
  one-turn versions, they do not count as a usable attack in any check.
- **R10, stone-evolved final forms keep learning, late.** A final form
  reached by a stone (Roserade) learns new moves starting about three splits
  after the previous stage's window, so using the stone early costs little
  and a late catch of the final form is not stuck with a bad list.
- **R11, both types get an attack early.** A dual-type line has an attack of
  each type by its first split's cap where it can (Budew's Poison Sting in
  Roark's split).
- **R12, a good mid-game kit.** One strong own-type attack, a hazard or
  status spreader, a second status move, and a coverage or second-type
  attack (Giga Drain, Toxic Spikes, Stun Spore and a coverage move), with
  more options beside them.
