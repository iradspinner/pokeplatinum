# The learnset exam: Ian's verdicts on the five held-out lines

Step 3 of `docs/oxide/learnset-checks.md`. Ian judged these five lines after
the rules from the other fifteen were locked (`learnset-insights.md`, "The
locked rules", committed at 03ad8fdf41). **The generator and any session
writing learnsets must not read this file.** It is read only in step 5, to
judge whether the rewritten learnsets satisfy what Ian said about lines whose
verdicts never shaped the rules.

## 1. Scorbunny (2026-10-06)

Shown: Scorbunny, a starter at 5 in Roark's split, knows Ember and Growl and
learns Quick Attack 6, Sand-Attack 11 and Double Kick 14; Raboot at 16 learns
Headbutt 21, Blaze Kick 28, Super Fang 32, Jump Kick 38, Double-Edge 44 and
Flare Blitz 52; Cinderace at 36 learns Jump Kick 40, Bounce 45, Flare Blitz
55, Acrobatics 64, High Jump Kick 66 and Pyro Ball 72, with U-turn at level 1
only. Shown as facts: Ember (special) its only Fire attack until Blaze Kick
at 28 on a physical line; coverage Double Kick, Jump Kick, High Jump Kick,
Bounce, Acrobatics, Headbutt and Double-Edge; utility Growl, Sand-Attack,
Quick Attack's priority and Super Fang, with no setup move; no
later-generation move but Pyro Ball at 72 (Flame Charge, Court Change and
Sucker Punch exist in Oxide).

Ian's verdict, verbatim:

Ember being its best move at gardenia feels pretty bad; could use an
inbetween move like flame wheel/flame charge. Otherwise, I agree with your
analysis broadly.

What the rewrite must show for it: a physical Fire attack between Ember and
Blaze Kick, in Gardenia's split (Flame Wheel or Flame Charge), and the points
shown as facts addressed.

## 2. Treecko (2026-10-06)

Shown: Treecko caught at 9 in Gardenia's split knows Pound, Leer and Absorb
and learns Quick Attack 11; Grovyle at 16 learns Fury Cutter 16, Pursuit 17,
Screech 23, Leaf Blade 29 and Agility 35; Sceptile (Grass/Dragon) at 36
learns Slam 43, Detect 51, False Swipe 59 and Leaf Storm 67, with X-Scissor
at 16 lost below its evolution level and Night Slash at level 1 only; a
Treecko held learns Mega Drain 26, Agility 31, Slam 36, Detect 41, Giga Drain
46 and Energy Ball 51. Shown as facts: Absorb its only Grass attack through
Gardenia's split; no Dragon attack by level-up; physical Grass power on a
mixed line until Leaf Storm; coverage Pursuit and Fury Cutter; utility
Agility, Screech, priority, False Swipe, Leer and Detect; no
later-generation moves.

Ian's verdict, verbatim:

Absorb until Leaf Blade is rough; Detect should go like Protect; False swipe
is an okay move but is a meme that late, and fury cutter is a terrible move
that should either be reworked or removed. You broadly got the analysis
correctly though.

Two of these are rulings for the whole game, applied at once and so not
counted in the exam: Detect leaves the player's lists with Protect, and Fury
Cutter is reworked or removed (the tracker's move reworks). What the rewrite
must show for the line itself: a Grass attack between Absorb and Leaf Blade
in good time, False Swipe early if at all, and the points shown as facts
addressed.

## 3. Eevee (2026-10-06)

Shown: Eevee, Bebe's gift at 20 in Fantina's split, knows Tackle, Helping
Hand, Sand-Attack and Growl, and learns Quick Attack 22, Bite 29, Baton Pass
36, Take Down 43, Last Resort 50 and Trump Card 57. Every evolution's first
own-type attack sits at 15, below the gift's level, so it is lost; their
strong own-type attacks mostly come around 71 (Vaporeon's first Water attack
is Hydro Pump at 71). Sylveon needs Charm, which Eevee has only on its egg
list, so the player can never have it. Shown as facts as well: Baton Pass
with nothing to pass, the same filler on every list, and later-generation
moves only on Sylveon.

Ian's verdict, verbatim:

Eeveelutions should be the major exception to the evolution stone rule of
limited/no moves learned after evolving via stone; eevee will almost
cerainly be kept at 20 until it is ready to be evolved, so it will need
complete moveset reworks for the eeveelutions from 20-onwards. Otherwise,
your analysis is correct.

What the rewrite must show for it: each Eeveelution with a complete moveset
from level 20 onward, as the exception to the stone rule (R10's late, sparse
lists do not apply), Sylveon reachable, and the points shown as facts
addressed. Sylveon's reachability is a defect for the whole game and is in the
tracker now.

## 4. Koffing (2026-10-06)

Shown: Koffing caught at 18 to 19 in Maylene's split knows Tackle, Smog,
Smokescreen and Assurance. Weezing (at 35) learns Self-Destruct 19, Sludge 24,
Haze 28, Gyro Ball 33, Explosion 40, Sludge Bomb 48, Destiny Bond 55 and
Memento 63, its Double Hit lost below its evolution level; Galarian Weezing
(Moon Stone, Poison/Fairy) learns Payback 23, Sludge 26, Toxic 29,
Self-Destruct 34, Will-O-Wisp 38, Sludge Bomb 42, Pain Split 45, Strange Steam
48 and Explosion 55. Shown as facts: up to three ways to faint on purpose and
Destiny Bond on the player's list; Sludge until Sludge Bomb; coverage
Assurance, Gyro Ball and Payback; utility Toxic, Will-O-Wisp, Haze, Pain
Split, Smokescreen and Poison Gas; later-generation moves only on the
Galarian branch.

Ian's verdict, verbatim:

Your analysis is apt, and memento is a terrible move. Haze is also a
terrible move. Its coverage is pretty awful, and Galarian Weezing's moveset
is significantly better than weezing to the point where IDK if someone would
ever choose to have weezing unless they didn't have an available moon stone.

Whole-game tier rulings, applied at once and not counted in the exam:
Memento and Haze are terrible (`learnset-insights.md`'s tier table).

What the rewrite must show for the line itself: real coverage, and the two
branches close enough in worth that Weezing is a choice and not only the
fallback without a Moon Stone, with the points shown as facts addressed.

## 5. Skorupi (2026-10-06)

Shown: Skorupi caught at 29 in Wake's split knows Pin Missile, Acupressure,
Scary Face and Toxic Spikes (Knock Off at 6, Bite and Poison Sting lie below
the catch level); it learns Bug Bite 34 and Poison Fang 39; Drapion
(Poison/Dark) at 40 learns Crunch 49 and Cross Poison 58, then nothing, with
the three elemental fangs at level 1 only. Poison Fang was shown at 50 power;
Oxide's data has it at 75 (the base ROM's value), which the Overseer
corrected afterwards.

Ian's verdict, verbatim:

Knock off being below the catch level is a travesty with how good it is;
check poison fang's power as I believe it should be buffed. Agreed on the
rest of the analysis, and its total move pool is very slim given no
elemental fang coverage. One final note, gunk shot is a high inaccuracy
move; anything below 90% accuracy is very difficult for me to justify given
how random it can make fights.

A whole-game ruling, applied at once and not counted in the exam: an attack
below 90 percent accuracy is very hard to justify for the player, since it
makes fights random (`learnset-insights.md`). Poison Fang's power was put to
Ian, who answered the same day: it takes Kaizo's version, 90 power with a 40%
chance to badly poison (a move change, not counted in the exam).

What the rewrite must show for the line itself: Knock Off reachable at or
after capture, a fuller pool with elemental fang coverage by level-up, and the
points shown as facts addressed.

## Step 5: the exam's result (2026-10-06)

An independent reviewer, who wrote none of the lists, judged the rewrite at
47503db009 on `balance-learnset-rewrite` against every point above. **The
rewrite does not reproduce Ian's verdicts as a whole.** It passes where his
verdict asked for something the locked rules already held (an early
own-type attack), and misses where the verdict carried an idea no rule held:
an Eevee kept at 20, a strong move below the catch level, and two branches of
one line close in worth.

| Line | Pass | Partial | Fail |
|---|---|---|---|
| Scorbunny | 5 | 0 | 0 |
| Treecko | 6 | 1 | 1 |
| Eevee | 2 | 2 | 3 |
| Koffing | 2 | 3 | 1 |
| Skorupi | 1 | 1 | 1 |

What decided each line:

- **Scorbunny passes.** Flame Charge at 8 fills the gap before Blaze Kick;
  Acrobatics moves to Raboot at 17, U-turn to 41, Iron Head at 50 is new.
- **Treecko mostly passes.** Giga Drain moves from 46 to 13, Dragon Breath at
  10, X-Scissor and real coverage later. False Swipe stays late (Grovyle 53,
  Sceptile 59): a fail. Utility only loses moves: partial.
- **Eevee fails its main point.** The checks evolve an Eevee by stone at the
  cap of the split before the stone, so they assume one levelled to 33 or 44,
  the opposite of Ian's premise that it is kept at 20. Only Umbreon's list
  works from 20; the others' first own-type attack is at 30 to 44, with Quick
  Attack and Bite before. Sylveon is now reachable (Charm at Eevee 27). The
  same filler sits on every Eeveelution (Quick Attack, Last Resort, Moonlight,
  Mean Look, Morning Sun, Confuse Ray), and Baton Pass stays at 36.
- **Koffing is partial.** Weezing gains Shadow Ball, Psybeam and Flamethrower;
  Galarian Weezing has only Dark coverage until 56. The branches come close
  in worth only from Candice's split. Sludge stays until Sludge Bomb. The
  forced-faint moves went to level 1, so a Koffing caught at 18 to 22 knows
  Destiny Bond.
- **Skorupi fails its main point.** Knock Off stays at 6, below the catch level
  of 29. The pool is fuller (Crunch 40, Aqua Tail 45, Brick Break 55 and more),
  but of the fangs only Fire Fang (65) comes by level-up.

Regressions the reviewer found on these lines: an Espeon evolved at 20 learns
nothing new but Quick Attack until 43; moves parked at level 1 for trainers
land in a wild catch's four; Glaceon and Sylveon each carry four recovery
moves; Umbreon (60 Special Attack) gets Leaf Storm, Psychic and Moonblast;
Upper Hand is placed though the engine runs it as a plain 65-power +3 hit;
Raboot's Acrobatics at 17 hits for 110 with no item, which may overcorrect
Gardenia's split. Nothing here relies on a move awaiting its rework.

The plan's answer to a failure is to understand it, adjust the rules (never a
patch for one species) and run the loop again. The exam has now been read, so
it can no longer test rules drawn from it.
