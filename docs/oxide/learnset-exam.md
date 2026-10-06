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
