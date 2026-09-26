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

Every one of them is once only, guarded by a flag of its own (Ian, 2026-09-21).
The conversation checks the flag on the way in and the gift sets it after the
Pokemon is actually handed over, so a full party does not burn the chance. Before
this they all repeated, which meant a player could ask again until the pool gave
them what they wanted and the even odds meant nothing.

| Source | How it picks | Level | Split | Pool |
|---|---|---|---|---|
| Sandgem Town, the house | list menu, 3 | 5 | Roark | Pichu, Grubbin, Fletchling |
| Jubilife City, south house 1F | random, 3 | 10 | Roark | Glameow, Skitty, Purrloin |
| Jubilife City, south house 3F (unused map) | list menu, 3 | 8 | Roark | Glameow, Skitty, Purrloin |
| Oreburgh City, middle house | random, 3 | 15 | Roark | Dwebble, Nosepass, Carbink |
| Floaroma Town, middle house | random, 4 | 18 | Gardenia | Poochyena, Seedot, Stunky, Swablu |
| Floaroma Meadow, the house | random, 3 | 18 | Gardenia | Combee, Budew, Pachirisu |
| Eterna City, condominiums 1F | random, 3 | 23 | Gardenia | Slugma, Charcadet, Yamask |
| Hearthome City, northwest house | once, flagged | 20 | Fantina | Eevee |
| Solaceon Town, northeast house | random, 3 | 30 | Maylene | Lunatone, Trapinch, Solrock |
| Veilstone City, northeast house | random, 3 | 40 | Maylene | Clobbopus, Hawlucha, Masquerain |
| Veilstone City, the Porygon gift | once | 25 | Maylene | Elekid |
| Pastoria City, north house | random, 6 | 45 | Wake | Octillery, Mantine, Crawdaunt, Sharpedo, Lanturn, Whiscash |
| Canalave City, the library 2F | random, 7 | 50 | Byron | Flygon, Cofagrigus, Hariyama, Klefki, Drapion, Dusclops, Primeape |

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

Sandgem and the Fan Club were the last two that let the player pick from a list
rather than rolling, and they roll now too (Ian, 2026-09-21). Each keeps its
question and its yes or no; the list menu is replaced by a `GetRandom` of the
same width, so the dispatch below it is untouched. The species names those menus
used are still in their text banks, unread, because deleting them would renumber
the bank for nothing.

**Ian's second pass (2026-09-26).** A gift that is too strong this early was
swapped for a weaker line: Oreburgh's three became Dwebble, Nosepass and
Carbink; Veilstone's Beldum and Sneasel became Clobbopus and Hawlucha; the
Restaurant pool's Toxapex became Whiscash. The Fan Club's starter gift is
gone, since Hearthome's capture is Bebe's Eevee; its member now only says
goodbye. Valley Windworks' balloon Drifloon, a scripted battle before the
second gym with three immunities, is gone too: Drifloon is a wild line now,
at home on Route 215 and on two Lost Tower floors, and its line moved from
the gate tier to preferred.

A line the player can always have if they want it appears in no table and
no other pool. That covers Togepi (Cynthia's egg), Floette (the Day Care),
Vullaby and Popplio (the two any-Pokemon trades), Eevee (Bebe) and Elekid
(Veilstone), and the fossils, which is why Canalave's Bastiodon became
Klefki and the Meadow's Flabebe became Budew. Each was replaced table by
table with a line of the same kind the table lacked. The Popplio line's
water slots were different: the on-list water pool is too thin to fill
them without flooding two lines, so each went to a neighbour in its own
table until Ian adds water lines to the pick-list. The Route 226 trade's
Magikarp still breaks the rule; that trade is to change (backlog).

## The trades

Ian rebuilt them on 2026-09-21. Both now take **any Pokemon**: the trade asked
for a particular species in the map script rather than in the engine, so the two
lines that compared your choice against it are simply gone.

| Trade | Gives | Nature | IVs | Level |
|---|---|---|---|---|
| Oreburgh, for anything | shiny Vullaby | Hardy, a neutral one | 20 across | 10 |
| Eterna, for anything | shiny Popplio | Bold | 20 across | 20 |

Shininess and nature both come out of one number. Generation 4 makes a Pokemon
shiny when its trainer id, secret id and the two halves of its personality value
exclusive-or to less than 8, and the nature is that same value modulo 25, so the
personality in each trade's data is chosen against that trade's own OT id to
satisfy both. Vanilla asserted that a trade is never shiny, which is true of its
four; that assert is gone. The level is the one thing the trade data cannot
express, because the game hands you a Pokemon at the level of the one you gave
up, which is no longer sensible when it will take anything. A short table in
`src/overlay006/npc_trade.c` names the level per trade, and 0 keeps vanilla's
behaviour for the Snowpoint and Route 226 trades, which are untouched and both
on the list.

The nicknames are unchanged, so the Vullaby is still called Kazza and the
Popplio Charap. Say the word and they move, but each one is a text bank.

## The Day Care's gift

The Day Care man handed over a Ditto. He gives a **shiny Floette** now: perfect
IVs, a neutral nature, level 30, once only like every other gift (Ian,
2026-09-21, after first asking for a winter Sawsbuck and then for Floette; the
Sawsbuck line is not in the species tree). Breeding is out of scope by the same
ruling, so losing the game's only Ditto is intended rather than a side effect.

One part of the ask is **not delivered and cannot be yet**: the white flower.
Floette's flower colours are forms, and this tree has exactly one Floette, with
one sprite and one palette, so a white-flowered one is new art and a new form
record rather than a number in a script. The gift is the Floette there is. The
tracker's backlog carries it.

Designing a gift needed a script command, because `GivePokemon` rolls the
personality value and therefore the nature, and rolls the IVs. `GiveDesignedPokemon`
takes a species, a level, a held item, a nature, one IV value for all six and a
shiny flag, and builds the personality to match: Generation 4 reads the nature
out of that value modulo 25 and calls a Pokemon shiny when the trainer id, the
secret id and the value's two halves exclusive-or to under 8, so choosing the
halves against the player's own id settles both at once. The same value also
decides gender and which ordinary ability the Pokemon has, which a designed gift
simply takes. It is the fork's second script command, after `GiveHiddenAbility`,
and like that one it is registered at the end so no existing opcode moves.
- **The Oreburgh museum's four spare fossils.** The pick-list has three fossil
  lines (Cranidos, Shieldon, Lileep) and the museum revives seven. The Old Amber,
  Helix, Dome and Claw fossils still revive Aerodactyl, Omanyte, Kabuto and
  Anorith. Ian's call of 2026-09-21 is to **delete those four items** rather than
  repoint them, which takes them out of the Underground's dig pools and the route
  drops that hand them out, and leaves the museum's four branches unreachable.
  That is item and script work outside this track, and it is in the tracker's
  backlog. The alternative, four more fossil lines on the list, would need
  Tyrunt, Amaura, Archen or Tirtouga ported first, since none is in the tree.

**Chimchar is settled rather than flagged.** Ian's call of 2026-09-21: Rowan's
briefcase offers Scorbunny in its place, so the third option is on the list like
the other two. That is `STARTER_OPTION_1` in
`src/choose_starter/choose_starter_app.c` and the rival and counterpart mapping
in `src/system_vars.c`. The rival's own teams needed nothing: those trainer files
are named for the player's choice, not the rival's species, so the fire slot is
still picked by the same index. Scorbunny left the wild in the same move, since a
starter is gate tier by rule. Route 204 north was built around it as the delay
prize and Litten takes that place, which gives Litten the wild home it never had,
and Route 207's 1% Litten tail became Torchic so the prize is not already
catchable in Roark's split. Route 206's 1% Scorbunny tail became Froakie.

The eighteen Unown rooms stay off-list by Ian's decision of 2026-09-21.

## Where the edits live

Each gift's species is an operand of `GivePokemon` in the map's script, so the
change is twelve files under `res/field/scripts/`. The guards live in the same
files and use thirteen flags named out of the spare run at 0x03BF in
`generated/vars_flags.txt`, which nothing else refers to; renaming an entry there
keeps its value, because the list is positional. Two of them show the species
name on screen, which is two more files under `res/text/`. All fourteen now
deliberately disagree with the base ROM, which means three tools had to be told:
`bulk_scripts.py`'s `DIVERGED` list, `import_base_rom.py`'s `TEXT_BANKS_SKIPPED`
(which `verify_narcs.py --text` reads too), and `bulk_text.py`, which had no skip
list and now honours the importer's. Without those three the next regeneration
would quietly put the off-list species back, which is the same trap the water
tables fell into at Step 6.

## Captures before the League, by location name (2026-09-25)

A scripted Pokemon's met location is the location name of the map it is handed
over or fought on (`MapHeader_GetMapLabelTextID`, in `ScrCmd_GivePokemon`,
`ScrCmd_GiveDesignedPokemon` and the in-game trade alike), the same name the
map popup shows and the same one a wild catch gets. So under Ian's rule a gift
in a place that also has a table is an alternative to it, not a second
encounter. An egg is the exception: the game stamps the place it hatches, so an
egg counts as its own encounter as long as it hatches somewhere with no table
and no gift (Ian hatches Riley's Riolu at Verity Lakefront). Sixty-two location
names have no table at all, so a free place is never short.

| Share a location with a wild table | Their own location |
|---|---|
| Route 201: the starter | Sandgem Town, Jubilife City, Floaroma Town, Floaroma Meadow, Solaceon Town: the clowns |
| Eterna City: the condo gift and the Popplio trade | Oreburgh City: the clown and the Vullaby trade, one capture |
| Valley Windworks: nothing scripted since 2026-09-26 | Hearthome City: Bebe's Eevee |
| Old Chateau: Rotom | Veilstone City: the clown and Elekid, one capture |
| Route 209: Spiritomb | Mining Museum (fossils), Pokemon Day Care (Floette), Canalave Library |
| Pastoria City: the clown | Acuity Cavern (Uxie), Valor Cavern (Azelf), Distortion World (Giratina) |

The eggs are Cynthia's Togepi (Eterna City), the Manaphy egg (Pokemon Mansion)
and Riley's Riolu (Iron Island). `pokemon_sources.py` lists all three, at
level 1 with the giver named; until 2026-09-25 it read `GiveEgg`'s second
operand, the giver, as a level, which dropped Riley's egg and put Togepi at 11
and Manaphy at 8.
Mesprit takes the name of the route it is caught on. Snowpoint City's trade
wants a Medicham.

The count: 52 wild locations open by the end of the League split, 14 scripted
ones of their own, and 3 eggs, **69**. (Since 2026-09-26 Mt. Coronet counts as
five capture areas, not one, which makes every figure here four higher: 73,
77 and, with the Battle Zone before the League, 85.) It becomes **73** once the four planned
changes exist, all in the tracker's backlog: Verity Lakefront's grass and
header, Amity Square's grass and header, Snowpoint City's header (its rods; the
trade then shares the name), and the Pastoria City clown moved into the
Restaurant on Route 213, which Ian asked for so that Pastoria's water and the
gift stop sharing one capture. The encounter tool already carries the three
tables (`planned_location` in the sidecar). The clown keeps its pool of six
water lines; only its map changes.

Ian's sheet (`My Version RomHack Docs - For Claude.xlsx`, General Encounters)
has 127 blocks, about 80 once its floors and rooms are folded into location
names. Most of the difference is the Battle Zone, which the sheet places in
Candice's split and the game opens only after the Hall of Fame (the Snowpoint
sailor checks `FLAG_GAME_COMPLETED`).
