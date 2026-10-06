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
