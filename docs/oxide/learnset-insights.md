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
