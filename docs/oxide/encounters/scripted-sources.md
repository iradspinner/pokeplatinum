# The scripted sources, sorted into buckets

Written 2026-09-21 from `docs/oxide/pokemon-sources.csv`, which
`tools/oxide/pokemon_sources.py` generates by reading the scripts themselves.

A *source* is one person or one machine, not one species. The clown in the
Sandgem house offers three Pokemon, but he is a single source and you leave with
one of them, so his three are a pool the way a table's slots are a pool, and
every member of it is equally likely. That is the unit this document works in:
Ian's rule for the buckets (2026-09-21) is that each source hands out one member
of its pool at even odds, and that no member may be off the species pick-list.

Most of these sources exist to give a town a capture that it otherwise has no
way to offer. Sandgem, Jubilife, Oreburgh, Floaroma, Eterna, Solaceon, Veilstone,
Pastoria and Canalave have no grass inside them, so under the nuzlocke rule the
gift is the town's only encounter, and its pool is designed the way a route's
table is: a level that suits the split, types that do not repeat each other, and
lines whose wild homes are somewhere else, so that taking the gift is a real
choice rather than a duplicate of the route outside.

## The gifts, as they now stand

Every pool below is on the pick-list. The species that changed are the ones that
were not.

| Source | How it picks | Level | Split | Pool |
|---|---|---|---|---|
| Sandgem Town, the house | list menu, 3 | 5 | Roark | Pichu, Grubbin, Fletchling |
| Jubilife City, south house 1F | random, 3 | 10 | Roark | Glameow, Skitty, Purrloin |
| Jubilife City, south house 3F (unused map) | list menu, 3 | 8 | Roark | Glameow, Skitty, Purrloin |
| Oreburgh City, middle house | random, 3 | 15 | Roark | Rhyhorn, Glimmet, Bronzor |
| Floaroma Town, middle house | random, 4 | 18 | Gardenia | Poochyena, Seedot, Stunky, Swablu |
| Floaroma Meadow, the house | random, 3 | 18 | Gardenia | Combee, Flabebe, Pachirisu |
| Eterna City, condominiums 1F | random, 3 | 23 | Gardenia | Slugma, Charcadet, Yamask |
| Hearthome City, northwest house | once, flagged | 20 | Fantina | Eevee |
| Hearthome City, Pokemon Fan Club | list menu, 9 | 30 | Fantina | Froakie, Charmander, Squirtle, Litten, Turtwig, Piplup, Treecko, Torchic, Mudkip |
| Solaceon Town, northeast house | random, 3 | 30 | Maylene | Lunatone, Trapinch, Solrock |
| Veilstone City, northeast house | random, 3 | 40 | Maylene | Beldum, Sneasel, Masquerain |
| Veilstone City, the Porygon gift | once | 25 | Maylene | Elekid |
| Pastoria City, north house | random, 6 | 45 | Wake | Octillery, Mantine, Crawdaunt, Sharpedo, Lanturn, Toxapex |
| Canalave City, the library 2F | random, 7 | 50 | Byron | Flygon, Cofagrigus, Hariyama, Bastiodon, Drapion, Dusclops, Primeape |

**What each change was for.** Sandgem hands out the three lines its own routes
only show at 4% and 1%, so the starter town is worth stopping in. Jubilife keeps
its two cats and gains a third rather than Meowth, who is off the list. Oreburgh
is a mining town and now gives mining Pokemon whose wild homes are all later:
Rhyhorn in Wake's split, Glimmet in Fantina's, Bronzor in Gardenia's. Floaroma
Town trades Murkrow for Swablu and the Meadow trades Cherubi for Flabebe, both
flowers. Eterna keeps Slugma and gains Charcadet, whose only wild home is Route
227, and Yamask, whose home is the Lost Tower: the old city, the forge and the
ghosts. The Fan Club still offers nine first partners, but the four off-list ones
give way to the two Sinnoh starters you did not choose and to Froakie and Litten,
the two starter lines with no wild home at all. Solaceon's ruins earn the sun and
moon pair, stuck inside Iron Island otherwise. Veilstone has the meteorites, so
Beldum belongs there, and the Porygon slot becomes Elekid, which is the same kind
of prize. Pastoria's roll only ever reached three of its six branches; all six are
on-list water lines now and the roll was widened to match, which is the only
change of behaviour in the batch. Canalave gives Byron's own Bastiodon, plus
Flygon and Cofagrigus in place of Dugtrio and Banette.

**Two things worth knowing about them.** None of these gifts is flag-guarded
except Eevee's, so they repeat: a player who wants a particular member can ask
again until they get it, and it is only the nuzlocke rule of taking the first one
that makes the pool's odds mean anything. And two of them, Sandgem and the Fan
Club, are list menus rather than rolls, so the player picks rather than the game.
Converting those two to a roll is a small edit, and worth doing if the even-odds
rule is meant to bind everywhere.

## Flagged, not changed

Ian asked for the trades to be left alone and brought back later. These four are
the same kind of case: the species is doing a job beyond being an encounter.

- **The in-game trades.** Ditto for Machop in Oreburgh and Chatot for Buizel in
  Eterna are still off-list. Gengar for Medicham in Snowpoint and Magikarp for
  Finneon on Route 226 are on-list, Gengar as of the ghost rows below.
- **The Day Care's Ditto**, handed over on a yes/no prompt with no flag guard. It
  is off-list, and it is also how breeding works, so it is not simply a gift.
- **The Oreburgh museum's four spare fossils.** The pick-list has three fossil
  lines (Cranidos, Shieldon, Lileep) and the museum revives seven. The Old Amber,
  Helix, Dome and Claw fossils still revive Aerodactyl, Omanyte, Kabuto and
  Anorith. The good fix is four more fossil lines on the list, and Tyrunt,
  Amaura, Archen and Tirtouga would be four of them, but none is in the tree, so
  that is a Phase 4 port before it is a table decision.
- **Chimchar**, which Rowan's briefcase still offers although it is not on the
  pick-list, while Turtwig and Piplup are. Changing it reaches into
  `src/choose_starter/choose_starter_app.c` and its art, so it is not a script
  edit like the rest.

The eighteen Unown rooms stay off-list by Ian's decision of 2026-09-21.

## Where the edits live

Each gift's species is an operand of `GivePokemon` in the map's script, so the
change is twelve files under `res/field/scripts/`. Two of them show the species
name on screen, which is two more files under `res/text/`. All fourteen now
deliberately disagree with the base ROM, which means three tools had to be told:
`bulk_scripts.py`'s `DIVERGED` list, `import_base_rom.py`'s `TEXT_BANKS_SKIPPED`
(which `verify_narcs.py --text` reads too), and `bulk_text.py`, which had no skip
list and now honours the importer's. Without those three the next regeneration
would quietly put the off-list species back, which is the same trap the water
tables fell into at Step 6.
