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

# Derived: the canon learnsets for the team builder

`../canon_learnsets.json` holds the team builder's Generation IV and
latest-generation move lists (build plan item 28). It is derived from
**pokemon-showdown 0.11.11**, MIT (Guangcong Luo and other contributors),
taken with `npm pack pokemon-showdown@0.11.11` on 2026-09-27; the tarball's
SHA-256 is `49af14aaed1084887f756372c7386c9987905930cc848ed31e9202c10c592d66`.
Only the derived file is vendored: the package is 17 MB packed, and the four
files read from it (`dist/data/learnsets.js`, the `gen8bdsp` and
`gen8legends` mods' learnsets, and `pokedex.js` and `moves.js`) come to
about 6 MB. The derived file is 2 MB, one species a line.

Regenerate it after moving to a newer package:

    npm pack pokemon-showdown@<version> && tar -xzf pokemon-showdown-<version>.tgz
    node tools/oxide/encounters/make_learnsets.js package \
        > tools/oxide/encounters/canon_learnsets.json

`make_learnsets.js` says what goes into each list: a species' own moves, its
earlier stages' in Showdown's chain, a battle form's base, and Brilliant
Diamond and Shining Pearl beside Sword and Shield for Generation 8.
