# Vendored: the Smogon calculator's canonical species table

`species.js` is `dist/data/species.js` from **@smogon/calc 0.12.0**, MIT
(Honko and contributors), taken with `npm pack @smogon/calc` on 2026-09-22.

It is here to answer one question: what is a species *supposed* to be? The dex
compares Oxide's numbers against vanilla Platinum through `git show main:`, which
works for the 493 natives and says nothing useful about the 159 species this
project added, since they simply do not exist there. This table does, because it
carries every generation through Generation 9.

**It is deliberately not the copy in `../calc/`.** The vendored calculator ships
whatever data it was last built with, and it loads the real thing at runtime, so
its bundled table is some romhack's: it has Arbok as Dark/Poison, Lapras as
Dragon/Water and Lopunny as Normal/Fighting, none of which is canon. Comparing
against it would have had the dex report changes this project never made. That
is why the baseline comes from upstream instead, and why `canon.py` has a test
that would catch it drifting again.

Regenerate `../canon.json` after updating this file:

    node tools/oxide/encounters/make_canon.js > tools/oxide/encounters/canon.json
