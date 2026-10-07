# The comb: Barry's split

**Every trainer of Barry's split is now combed.** The bosses were combed
earlier. On 2026-10-07 I added all 23 ordinary trainers in walking order:
the swimmers and sailor of Route 223 and the Victory Road trainers. Every
file passes the checker and the rule audit; the checker's only remarks are
the moves outside a species' lists that Ian's late-game ruling allows. The
same day, by Ian's ruling, Lucas and Dawn 3 dropped three levels.

Seven of these trainers have Kaizo teams (Wesley, Francisco, Miranda, Aubree,
Paige, Zachariah and Clinton); each keeps its idea without the evasion items,
trades and one-hit KO moves. The rest are mine, from today's files. Every
team is moved fully into Oxide's Generation 5+ pool, since a move need not be
legal for the species this late (Ian, 2026-10-07), then scaled to the dial.

| Check | Result |
|---|---|
| Single battles read blind (21) | 89 to 100 won, mean 94.8 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 63 to 78, mean 73 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.5 to 1.3, mean 0.81 |
| Doubles (2) | not readable yet |
| Move slots that are Generation 5+ | 74 of 365, 20 percent |
| Teams with no modern move | none |
| Hidden abilities | 34, on 21 of 23 teams |
| Element 7 items held | 7: four Eviolites, a Rocky Helmet, an Assault Vest and a Punching Glove |

These trainers read harder than Ian's band, about as hard as the Galactic
split's: the box at 71 knows no TMs, and against it this split's Ace Trainers
read 25 to 49 won blind. I softened each team, mostly by keeping its top
level (69) on the lead or wall and its hitters at 66 to 67, until most won 92
percent or more; Troy, Hana and Edgar still read 89 to 93, within the
readings' noise of each other. Two lessons held from the Galactic split: a
Dragon Dance on an ordinary trainer reads far past the band, and swapping
Outrage or Dragon Rush for a move without recoil makes a dragon stronger,
since the recoil wears it down. Crystal awards TM54 (False Swipe), which no
trainer would use, so no team carries it.

## The bosses, combed earlier

The bosses of Barry's split are combed: Ace Trainer Mariah and Lucas and
Dawn 3 on Victory Road, the optional Ace Trainers Sydney, Omar and Henry on
its upper and lower floors, Barry 6 at the League's gate, and the Fight
Area's Volkner and Flint tag.

The cap is 71, and no map here has its own weather. My simulator reads the
bosses against the scorer's box at this split, which knows no TMs, after its
order fix and the legality sweep, so they read harsher than they will once the
TM pass's box is read. Rivals keep their aces at the cap, and the Ace Trainers
sit three under it with sharper sets, as Ian's rule on levels asks. From this
split on, a trainer's move need not be legal for the species (Ian,
2026-10-07); no file here needed that. Ian ruled that every draft goes into
step 12 as drafted, and he chooses any retunes from the scorer's step 15
reading; my candidates are in `../retune-proposals-not-approved/`.

Barry 6 reads 99 won with a Turtwig player, 96 with a Piplup player (today's
file 92) and 83 with a Chimchar player, whose rival brings the Empoleon line;
the spread comes from how each starter meets the box, and the scorer's step
15 reading decides whether to even it. Lucas and Dawn 3 keep today's sets,
three levels down (Ian, 2026-10-07: three under the cap, the ace at 68 and
the gaps kept), and now read 99 to 100 won to today's 92 to 100: 99 / 1.8 / 7
with a Turtwig player, 100 / 0.9 / 42 with a Chimchar player and 100 / 0.6 /
53 with a Piplup player. At the cap they read 93 to 99. Mariah, whom the player must pass,
reads 87 won with a planned six; the optional Sydney, Omar and Henry read 97
to 98 planned and 25 to 49 met blind.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Barry 6 takes today's roster idea | My Barry 3 to 5 grew one skeleton (Ambipom, Staraptor, Heracross, Floatzel, Snorlax, starter). At 71 it read softer than today's Barry 6, so Barry 6 keeps the Ambipom Fake Out lead and adds today's Dragonite and Ninetales (Starmie in the Turtwig version, to avoid two Fire types), with a Curse Snorlax and his starter at the cap with a setup move. | `rival_pokemon_league_*.json`; the scorer's reading at step 15. | Accept (recommended), or keep the earlier skeleton. |
| 2 | Lucas and Dawn 3 keep today's sets | Ian's six per file, with natures added and Tangrowth's Power Whip (no longer in its lists) as Leaf Storm, now three under the cap (Ian, 2026-10-07). The Piplup version keeps the Chimchar line, as Ian ruled. | `dummy_779.json` to `dummy_784.json`. | Answered (2026-10-07). |
| 3 | Fight Area tag | Volkner and Flint bring four each at 68 to 69. | The scorer cannot read tag battles yet. | Nothing now. |
| 4 | Ordinary trainers past the band | They win 89 to 100 percent blind but cost about 0.81 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25, against a box at 71 that knows no TMs. | The scorer's step 15 reading. | Accept for now (recommended), or soften them further now. |

## What comes next

Nothing in this split; the League has no ordinary trainers.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Swimmer Wesley | Route 223 | optional | single | 4 | 67 to 69 | Toxic Spikes from Tentacruel | 98 / 1.08 / 33 blind in my simulator, about 73 clean in the scorer's terms |
| Swimmer Ricardo | Route 223 | optional | single | 4 | 66 to 69 | Spikes from an Intimidate Qwilfish | 92 / 1.32 / 37 blind in my simulator, about 75 clean in the scorer's terms |
| Swimmer Francisco | Route 223 | optional | single | 4 | 66 to 69 | Kaizo's odd crew without its trades | 93 / 1.38 / 36 blind in my simulator, about 75 clean in the scorer's terms |
| Swimmer Colton | Route 223 | optional | single | 4 | 66 to 69 | Regenerator Slowbro's Scald and Psyshock | 96 / 1.04 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Swimmer Troy | Route 223 | optional | single | 4 | 66 to 69 | An Intimidate Gyarados behind Milotic's Scald and Dragon Tail | 89 / 1.47 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Swimmer Oscar | Route 223 | on the path | single | 4 | 66 to 69 | Rain from Mantine's Rain Dance on a Damp Rock | 98 / 1.00 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Swimmer Miranda | Route 223 | optional | single | 4 | 67 to 69 | Kaizo's slow waters without its BrightPowders and Lax Incenses | 100 / 0.80 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Swimmer Aubree | Route 223 | optional | single | 4 | 66 to 69 | Spikes from a Rocky Helmet Skarmory | 96 / 1.55 / 19 blind in my simulator, about 68 clean in the scorer's terms |
| Swimmer Paige | Route 223 | optional | single | 4 | 66 to 69 | Milotic's Mirror Coat | 92 / 1.72 / 22 blind in my simulator, about 69 clean in the scorer's terms |
| Swimmer Crystal | Route 223 | optional | single | 4 | 66 to 69 | Stealth Rock from a Regenerator Corsola | 98 / 0.92 / 42 blind in my simulator, about 77 clean in the scorer's terms |
| Swimmer Cassandra | Route 223 | optional | single | 4 | 66 to 69 | Eeveelutions | 93 / 1.25 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Swimmer Gabrielle | Route 223 | on the path | single | 4 | 66 to 69 | Golduck's Scald and Psyshock | 100 / 0.90 / 32 blind in my simulator, about 73 clean in the scorer's terms |
| Sailor Zachariah | Route 223 | optional | single | 4 | 66 to 69 | Kaizo's sailor | 95 / 1.54 / 24 blind in my simulator, about 70 clean in the scorer's terms |
| Ace Trainer Mariah | Victory Road 1F | gym-like stretch, on the path | single, Ace Trainer | 6 | 66 to 68 | Glalie's Spikes behind a Focus Sash | about 87 / 2.5 / 3 with a planned six |
| Veteran Edgar | Victory Road 1F | on the path | single | 4 | 66 to 69 | Empoleon's Scald and Knock Off | 93 / 1.36 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Dragon Tamer Clinton | Victory Road 1F | on the path | single | 4 | 66 to 69 | Tropius | 96 / 0.99 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Bird Keeper Hana | Victory Road 1F | on the path | single | 4 | 66 to 69 | A Super Luck Togekiss (not Serene Grace beside Air Slash) | 92 / 1.17 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Psychic Bryce | Victory Road 1F | on the path | single | 4 | 66 to 69 | Grumpig's Thunder Wave | 92 / 1.76 / 20 blind in my simulator, about 68 clean in the scorer's terms |
| Black Belt Miles | Victory Road 1F | on the path | single | 4 | 66 to 69 | The three Hitmons with Mienshao | 92 / 1.63 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Dawn 3 (player chose Turtwig) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | Today's six (Ian's design) kept | about 99 / 1.8 / 7 in my simulator, where today's file reads 92 / 3.0 / 0 |
| Dawn 3 (player chose Chimchar) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | Today's six (Ian's design) kept | about 100 / 0.9 / 42 in my simulator, where today's file reads 100 / 1.1 / 31 |
| Dawn 3 (player chose Piplup) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | Today's six (Ian's design) kept | about 100 / 0.6 / 53 in my simulator, where today's file reads 100 / 1.3 / 18 |
| Lucas 3 (player chose Turtwig) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | The same six as Dawn's file for this starter | about 99 / 1.8 / 7 in my simulator, where today's file reads 92 / 3.0 / 0 |
| Lucas 3 (player chose Chimchar) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | The same six as Dawn's file for this starter | about 100 / 0.9 / 42 in my simulator, where today's file reads 100 / 1.1 / 31 |
| Lucas 3 (player chose Piplup) | Victory Road battleground | on the path | single, rival | 6 | 66 to 68 | The same six as Dawn's file for this starter | about 100 / 0.6 / 53 in my simulator, where today's file reads 100 / 1.3 / 18 |
| Veteran Clayton | Victory Road 2F | optional | single | 4 | 66 to 69 | Poison Heal Lickilicky on a Toxic Orb | 97 / 1.48 / 21 blind in my simulator, about 68 clean in the scorer's terms |
| Ace Trainer Sydney | Victory Road 2F | optional | single, Ace Trainer | 6 | 66 to 68 | Torkoal's Stealth Rock and Yawn behind a Focus Sash | about 98 / 0.8 / 34 with a planned six |
| Ace Trainer Omar | Victory Road 2F | optional | single, Ace Trainer | 6 | 66 to 68 | Rock and Bug | about 98 / 1.6 / 11 with a planned six |
| Double Team Al and Kay | Victory Road 2F | optional | double | 4 | 66 to 68 | Fake Out and Helping Hand | not readable yet (a double) |
| Dragon Tamer Ondrej | Victory Road B1F | optional | single | 4 | 66 to 69 | Altaria's Will-O-Wisp | 94 / 2.15 / 8 blind in my simulator, about 63 clean in the scorer's terms |
| Psychic Valencia | Victory Road B1F | optional | single | 4 | 66 to 69 | Chimecho's Yawn and Heal Bell | 95 / 1.72 / 17 blind in my simulator, about 67 clean in the scorer's terms |
| Ace Trainer Henry | Victory Road B1F | optional | single, Ace Trainer | 6 | 66 to 68 | Crawdaunt's Swords Dance | about 97 / 2.2 / 4 with a planned six |
| Double Team Jo and Pat | Victory Road B1F | optional | double | 4 | 67 to 68 | Earthquake beside a Levitate Claydol | not readable yet (a double) |
| Barry 6 (player chose Piplup) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | Today's roster idea at the cap | about 96 / 3.1 / 0 in my simulator, where today's file reads 92 / 2.9 / 0 |
| Barry 6 (player chose Turtwig) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | The same roster with Starmie in Ninetales' place and Infernape as his starter | about 99 / 3.1 / 0 in my simulator |
| Barry 6 (player chose Chimchar) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | The same roster with Empoleon as his starter | about 83 / 3.0 / 0 in my simulator |
| Volkner (Fight Area) | Fight Area | on the path | tag with Flint, beside a partner | 4 | 68 to 69 | Four Electric types two and three under the cap | not readable yet (a tag battle) |
| Flint (Fight Area) | Fight Area | on the path | tag with Volkner, beside a partner | 4 | 68 to 69 | Four Fire types | not readable yet (a tag battle) |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Swimmer Wesley: Route 223, optional, single, cap 71

Toxic Spikes from Tentacruel, then Kaizo's divers: an Eviolite Seadra with Sniper, Huntail and Floatzel's Ice Spinner. Kaizo's BrightPowder is gone (evasion stays rare).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tentacruel | 69 | Leftovers | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Rapid Spin |
| Seadra | 67 | Eviolite | Sniper | default | Hydro Pump, Dragon Pulse, Ice Beam, Focus Energy |
| Huntail | 67 | none | Water Veil | default | Liquidation, Ice Fang, Crunch, Sucker Punch |
| Floatzel | 68 | Mystic Water | Water Veil | default | Liquidation, Ice Spinner, Crunch, Aqua Jet |

Today's team: Floatzel 60 (Crunch, Agility, Waterfall, Razor Wind), Cloyster 60 (Ice Beam, Protect, Surf, Spike Cannon). Expected: 98 / 1.08 / 33 blind in my simulator, about 73 clean in the scorer's terms.

### Swimmer Ricardo: Route 223, optional, single, cap 71

Spikes from an Intimidate Qwilfish, then Lanturn's Volt Switch, Seaking's Megahorn and Crawdaunt's Crabhammer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 69 | Black Sludge | Intimidate | default | Spikes, Poison Jab, Waterfall, Thunder Wave |
| Seaking | 67 | none | Lightning Rod | default | Waterfall, Megahorn, Drill Run, Knock Off |
| Crawdaunt | 66 | none | Shell Armor | default | Crabhammer, Knock Off, Aqua Jet, X-Scissor |
| Lanturn | 67 | Leftovers | Volt Absorb | default | Scald, Volt Switch, Ice Beam, Thunder Wave |

Today's team: Tentacruel 61 (Poison Jab, Screech, Hydro Pump, Wring Out). Expected: 92 / 1.32 / 37 blind in my simulator, about 75 clean in the scorer's terms.

### Swimmer Francisco: Route 223, optional, single, cap 71

Kaizo's odd crew without its trades: Raichu's Lightning Rod and Fake Out, Pelipper's Hurricane, Qwilfish, and Tyranitar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 69 | Leftovers | Intimidate | default | Poison Jab, Aqua Jet, Taunt, Waterfall |
| Raichu | 68 | Magnet | Lightning Rod | default | Thunderbolt, Surf, Grass Knot, Fake Out |
| Pelipper | 67 | Sitrus Berry | Unburden | default | Hurricane, Scald, U-turn, Roost |
| Tyranitar | 66 | none | Unnerve | default | Stone Edge, Crunch, Earthquake, Ice Punch |

Today's team: Kingler 60 (Guillotine, Slam, Brine, Crabhammer), Quagsire 60 (Toxic, Earthquake, Waterfall, Ice Punch). Expected: 93 / 1.38 / 36 blind in my simulator, about 75 clean in the scorer's terms.

### Swimmer Colton: Route 223, optional, single, cap 71

Regenerator Slowbro's Scald and Psyshock, Starmie's Psyshock, a Sniper Octillery on a Scope Lens, and Lanturn's Volt Switch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Slowbro | 69 | Leftovers | Regenerator | default | Scald, Psyshock, Slack Off, Thunder Wave |
| Octillery | 67 | Scope Lens | Sniper | default | Hydro Pump, Ice Beam, Fire Blast, Energy Ball |
| Starmie | 67 | Sitrus Berry | Analytic | default | Surf, Psyshock, Ice Beam, Recover |
| Lanturn | 66 | none | Water Absorb | default | Scald, Volt Switch, Ice Beam, Thunder Wave |

Today's team: Slowbro 59 (Surf, Slack Off, Amnesia, Psychic), Octillery 59 (Surf, Signal Beam, Ice Beam, Hyper Beam), Pelipper 59 (Fly, Ice Beam, Tailwind, Hydro Pump). Expected: 96 / 1.04 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Swimmer Troy: Route 223, optional, single, cap 71

An Intimidate Gyarados behind Milotic's Scald and Dragon Tail, with Kingler and Lumineon. Today's Dragon Dance read 56 won, far past the band.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Milotic | 69 | Leftovers | Marvel Scale | default | Scald, Ice Beam, Recover, Dragon Tail |
| Kingler | 66 | none | Hyper Cutter | default | Crabhammer, Knock Off, X-Scissor, Rock Slide |
| Lumineon | 66 | Sitrus Berry | Water Veil | default | Scald, Ice Beam, U-turn, Alluring Voice |
| Gyarados | 66 | none | Intimidate | default | Waterfall, Ice Fang, Crunch, Thunder Wave |

Today's team: Gyarados 61 (Dragon Dance, Waterfall, Ice Fang, Earthquake). Expected: 89 / 1.47 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Swimmer Oscar: Route 223, on the path, single, cap 71

Rain from Mantine's Rain Dance on a Damp Rock, then Hurricane that cannot miss in it, Wailord's Water Spout, Ludicolo and Politoed's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mantine | 69 | Damp Rock | Water Absorb | default | Rain Dance, Scald, Hurricane, Roost |
| Politoed | 66 | Sitrus Berry | Water Absorb | default | Scald, Ice Beam, Hypnosis, Encore |
| Ludicolo | 67 | none | Own Tempo | default | Giga Drain, Hydro Pump, Ice Beam, Leech Seed |
| Wailord | 67 | Leftovers | Water Veil | default | Water Spout, Ice Beam, Hydro Pump, Rest |

Today's team: Mantine 60 (Confuse Ray, Rain Dance, Aqua Ring, Hydro Pump), Wailord 60 (Water Spout, Amnesia, Earthquake, Hidden Power). Expected: 98 / 1.00 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Swimmer Miranda: Route 223, optional, single, cap 71

Kaizo's slow waters without its BrightPowders and Lax Incenses: Lumineon's U-turn, Phione's Toxic and Rest, Gorebyss and Slowking's Slack Off.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 69 | Leftovers | Water Veil | default | U-turn, Scald, Ice Beam, Alluring Voice |
| Phione | 67 | Sitrus Berry | Hydration | default | Scald, Toxic, Rest, Grass Knot |
| Gorebyss | 67 | none | Hydration | default | Hydro Pump, Psychic, Ice Beam, Aqua Ring |
| Slowking | 68 | Leftovers | Regenerator | default | Scald, Psychic, Flamethrower, Slack Off |

Today's team: Lumineon 61 (Sweet Kiss, Air Cutter, Surf, Silver Wind). Expected: 100 / 0.80 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Swimmer Aubree: Route 223, optional, single, cap 71

Spikes from a Rocky Helmet Skarmory, then Kaizo's power pair: a Simple Bibarel's Curse and a Huge Power Azumarill. Politoed's Perish Song and Baton Pass are gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 69 | Rocky Helmet | Filter | default | Spikes, Brave Bird, Iron Head, Roost |
| Politoed | 66 | none | Water Absorb | default | Scald, Ice Beam, Encore, Hypnosis |
| Azumarill | 66 | none | Huge Power | default | Liquidation, Play Rough, Aqua Jet, Knock Off |
| Bibarel | 66 | none | Simple | default | Curse, Liquidation, Return, Aqua Jet |

Today's team: Bibarel 60 (Defense Curl, Rollout, Waterfall, Quick Attack), Azumarill 60 (Focus Blast, Grass Knot, Blizzard, Hydro Pump). Expected: 96 / 1.55 / 19 blind in my simulator, about 68 clean in the scorer's terms.

### Swimmer Paige: Route 223, optional, single, cap 71

Milotic's Mirror Coat, Cloyster's Spikes, Weavile's Fake Out and Triple Axel, and Snorlax. Today's Sheer Cold is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Milotic | 69 | Leftovers | Marvel Scale | default | Scald, Ice Beam, Recover, Mirror Coat |
| Cloyster | 66 | none | Shell Armor | default | Spikes, Icicle Crash, Liquidation, Rapid Spin |
| Weavile | 67 | none | Pickpocket | default | Fake Out, Triple Axel, Knock Off, Ice Shard |
| Snorlax | 67 | none | Thick Fat | default | Body Slam, Earthquake, Crunch, Rest |

Today's team: Lapras 59 (Brine, Safeguard, Hydro Pump, Sheer Cold), Dewgong 59 (Dive, Aqua Tail, Ice Beam, Safeguard), Slowking 59 (Hydro Pump, Psychic, Power Gem, Flamethrower). Expected: 92 / 1.72 / 22 blind in my simulator, about 69 clean in the scorer's terms.

### Swimmer Crystal: Route 223, optional, single, cap 71

Stealth Rock from a Regenerator Corsola, then Kingdra's Draco Meteor, Seaking's Megahorn and Dewgong's Flip Turn. Crystal's reward, False Swipe, is no use to a trainer, so no team carries it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Corsola | 69 | Leftovers | Regenerator | default | Stealth Rock, Scald, Power Gem, Recover |
| Dewgong | 67 | Sitrus Berry | Thick Fat | default | Ice Beam, Surf, Flip Turn, Encore |
| Seaking | 67 | none | Lightning Rod | default | Waterfall, Megahorn, Drill Run, Knock Off |
| Kingdra | 66 | Scope Lens | Sniper | default | Draco Meteor, Surf, Ice Beam, Flip Turn |

Today's team: Seaking 60 (Fury Attack, Waterfall, Horn Drill, Agility), Corsola 60 (Surf, Power Gem, Mirror Coat, Earth Power). Expected: 98 / 0.92 / 42 blind in my simulator, about 77 clean in the scorer's terms.

### Swimmer Cassandra: Route 223, optional, single, cap 71

Eeveelutions: Vaporeon's Scald and Wish, Jolteon's Volt Switch, a Magic Guard Leafeon and Glaceon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Vaporeon | 69 | Leftovers | Water Absorb | default | Scald, Ice Beam, Wish, Protect |
| Jolteon | 66 | Magnet | Volt Absorb | default | Thunderbolt, Volt Switch, Shadow Ball, Thunder Wave |
| Leafeon | 67 | Miracle Seed | Magic Guard | default | Leaf Blade, Knock Off, X-Scissor, Synthesis |
| Glaceon | 66 | none | Ice Body | default | Ice Beam, Shadow Ball, Water Pulse, Yawn |

Today's team: Vaporeon 61 (Ice Beam, Aqua Ring, Surf, Shadow Ball). Expected: 93 / 1.25 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Swimmer Gabrielle: Route 223, on the path, single, cap 71

Golduck's Scald and Psyshock, an Unaware Quagsire, Whiscash and Floatzel's Ice Spinner.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golduck | 69 | Leftovers | Cloud Nine | default | Scald, Ice Beam, Psyshock, Encore |
| Quagsire | 67 | Sitrus Berry | Unaware | default | Scald, Earthquake, Recover, Toxic |
| Whiscash | 66 | none | Anticipation | default | Earthquake, Liquidation, Stone Edge, Zen Headbutt |
| Floatzel | 67 | Mystic Water | Water Veil | default | Liquidation, Ice Spinner, Crunch, Aqua Jet |

Today's team: Golduck 61 (Ice Punch, Zen Headbutt, Aqua Jet, Waterfall). Expected: 100 / 0.90 / 32 blind in my simulator, about 73 clean in the scorer's terms.

### Sailor Zachariah: Route 223, optional, single, cap 71

Kaizo's sailor: an Analytic Magnezone's Thunder Wave on a Chople Berry, a No Guard Machamp's Cross Chop, Gastrodon's Yawn and Starmie.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magnezone | 69 | Chople Berry | Analytic | default | Thunder Wave, Thunderbolt, Flash Cannon, Volt Switch |
| Gastrodon | 67 | Leftovers | Dry Skin | default | Scald, Earth Power, Yawn, Recover |
| Starmie | 67 | Sitrus Berry | Analytic | default | Scald, Psyshock, Ice Beam, Recover |
| Machamp | 66 | none | No Guard | default | Cross Chop, Stone Edge, Knock Off, Bullet Punch |

Today's team: Poliwrath 59 (Belly Drum, Poison Jab, DynamicPunch, Ice Punch), Machamp 59 (Earthquake, ThunderPunch, Poison Jab, DynamicPunch), Gastrodon 59 (Toxic, Waterfall, Earthquake, Recover). Expected: 95 / 1.54 / 24 blind in my simulator, about 70 clean in the scorer's terms.

### Ace Trainer Mariah: Victory Road 1F, gym-like stretch, on the path, single, Ace Trainer, cap 71

Glalie's Spikes behind a Focus Sash, Blissey's Sing, Dusknoir's Will-O-Wisp, Hippowdon, Starmie's Thunder Wave and a Dragon Dance Tyranitar ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 66 | Focus Sash | Ice Body | Jolly | Spikes, Ice Shard, Crunch, Earthquake |
| Blissey | 66 | Leftovers | Natural Cure | Bold | Ice Beam, Sing, Softboiled, Light Screen |
| Dusknoir | 67 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Hippowdon | 66 | Sitrus Berry | Thick Fat | Impish | Earthquake, Crunch, Ice Fang, Slack Off |
| Starmie | 67 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Thunder Wave |
| Tyranitar | 68 | Chople Berry | Unnerve | Adamant | Stone Edge, Crunch, Earthquake, Dragon Dance |

Today's team: Blissey 63 (Hyper Beam, Sing, Softboiled, Light Screen), Glalie 63 (Ice Beam, Crunch, Headbutt, Shadow Ball), Tyranitar 63 (Stone Edge, Crunch, Thunder Fang, Earthquake). Expected: about 87 / 2.5 / 3 with a planned six; read blind, 26 / 5.1 / 1.

### Veteran Edgar: Victory Road 1F, on the path, single, cap 71

Empoleon's Scald and Knock Off, an Eviolite Porygon2, a vested Tangrowth and Porygon-Z.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Empoleon | 69 | Leftovers | Competitive | default | Scald, Flash Cannon, Ice Beam, Knock Off |
| Porygon2 | 66 | Eviolite | Download | default | Tri Attack, Ice Beam, Thunderbolt, Recover |
| Tangrowth | 66 | Assault Vest | Regenerator | default | Giga Drain, Sludge Bomb, Knock Off, Rock Tomb |
| Porygon Z | 66 | none | Analytic | default | Tri Attack, Shadow Ball, Signal Beam, Thunder Wave |

Today's team: Porygon Z 63 (Hyper Beam, Signal Beam, Psychic, Thunderbolt), Tangrowth 63 (Power Whip, Mega Drain, Toxic, Slam), Empoleon 63 (Brine, Drill Peck, Flash Cannon, Growl). Expected: 93 / 1.36 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Dragon Tamer Clinton: Victory Road 1F, on the path, single, cap 71

Tropius, a Magic Bounce Espeon, Aerodactyl's Dual Wingbeat and an Eviolite Dragonair. Kaizo's six included Muk's Minimize and Explosion and Dragonite; a Dragonite here read 82 won, far past the band.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tropius | 69 | Sitrus Berry | Harvest | default | Air Slash, Giga Drain, Dragon Pulse, Synthesis |
| Espeon | 66 | Leftovers | Magic Bounce | default | Psyshock, Dazzling Gleam, Shadow Ball, Morning Sun |
| Aerodactyl | 67 | none | Rock Head | default | Stone Edge, Earthquake, Crunch, Dual Wingbeat |
| Dragonair | 66 | Eviolite | Shed Skin | default | Dragon Rush, ExtremeSpeed, Thunder Wave, Aqua Tail |

Today's team: Garchomp 63 (Flamethrower, Dragon Pulse, Surf, Earth Power), Flygon 63 (Earth Power, Draco Meteor, Silver Wind, Flamethrower), Aerodactyl 63 (Crunch, Stone Edge, Iron Head, Dragon Claw). Expected: 96 / 0.99 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Bird Keeper Hana: Victory Road 1F, on the path, single, cap 71

A Super Luck Togekiss (not Serene Grace beside Air Slash), Dodrio's Drill Run, Pidgeot and Noctowl's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Togekiss | 69 | Leftovers | Super Luck | default | Air Slash, Dazzling Gleam, Aura Sphere, Roost |
| Noctowl | 66 | Wide Lens | Tinted Lens | default | Moonblast, Air Slash, Hypnosis, Roost |
| Dodrio | 66 | none | Quick Feet | default | Drill Peck, Drill Run, Knock Off, Quick Attack |
| Pidgeot | 66 | none | Big Pecks | default | Air Slash, Heat Wave, Roost, U-turn |

Today's team: Dodrio 63 (Mirror Move, Quick Attack, Drill Peck, Roost), Togekiss 63 (Shock Wave, Water Pulse, Aura Sphere, Air Slash), Pidgeot 63 (Roost, Heat Wave, Mirror Move, Air Slash). Expected: 92 / 1.17 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Psychic Bryce: Victory Road 1F, on the path, single, cap 71

Grumpig's Thunder Wave, then Gardevoir's Moonblast, Gengar and a Magic Guard Alakazam. Today's Destiny Bond is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Grumpig | 69 | Leftovers | Thick Fat | default | Psychic, Power Gem, Dazzling Gleam, Thunder Wave |
| Alakazam | 66 | none | Magic Guard | default | Psychic, Shadow Ball, Focus Blast, Dazzling Gleam |
| Gardevoir | 66 | none | Trace | default | Moonblast, Psyshock, Mystical Fire, Shadow Ball |
| Gengar | 66 | none | Levitate | default | Shadow Ball, Sludge Bomb, Focus Blast, Will-O-Wisp |

Today's team: Grumpig 63 (Psychic, Psychic, Power Gem, Hidden Power), Gardevoir 63 (Psychic, Calm Mind, Hidden Power, Hypnosis), Gengar 63 (Shadow Ball, Dark Pulse, Destiny Bond, Sludge Bomb). Expected: 92 / 1.76 / 20 blind in my simulator, about 68 clean in the scorer's terms.

### Black Belt Miles: Victory Road 1F, on the path, single, cap 71

The three Hitmons with Mienshao: Hitmontop's Fake Out and Triple Axel, a Punching Glove Hitmonchan, Hitmonlee's High Jump Kick.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 69 | Leftovers | Steadfast | default | Fake Out, Close Combat, Triple Axel, Sucker Punch |
| Hitmonchan | 66 | Punching Glove | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Hitmonlee | 67 | none | Reckless | default | Hi Jump Kick, Knock Off, Blaze Kick, Stone Edge |
| Mienshao | 66 | none | Regenerator | default | Drain Punch, U-turn, Knock Off, Stone Edge |

Today's team: Hitmonchan 63 (Ice Punch, ThunderPunch, Ice Punch, Close Combat), Hitmonlee 63 (Blaze Kick, Mega Kick, Close Combat, Earthquake), Hitmontop 63 (Bullet Punch, Sucker Punch, Close Combat, Mach Punch). Expected: 92 / 1.63 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Dawn 3 (player chose Turtwig): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Empoleon, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 66 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 67 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Empoleon | 68 | Chople Berry | Torrent | Modest | Surf, Blizzard, Roar, Stealth Rock |

Today's team: Nidoqueen 69 (Black Sludge; Earthquake, Poison Jab, Ice Punch, Toxic Spikes), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 69 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Empoleon 71 (Chople Berry; Surf, Blizzard, Roar, Stealth Rock). Expected: about 99 / 1.8 / 7 in my simulator, where today's file reads 92 / 3.0 / 0.

### Dawn 3 (player chose Chimchar): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Torterra, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 66 | Life Orb | Regenerator | Quiet | Surf, Psychic, Trick Room, Slack Off |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 67 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Torterra | 68 | Yache Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Leech Seed |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Life Orb; Surf, Psychic, Trick Room, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Torterra 71 (Yache Berry; Wood Hammer, Earthquake, Stone Edge, Leech Seed). Expected: about 100 / 0.9 / 42 in my simulator, where today's file reads 100 / 1.1 / 31.

### Dawn 3 (player chose Piplup): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Infernape, the Chimchar line Ian kept for this version, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 66 | Wise Glasses | Regenerator | Modest | Surf, Psychic, Ice Beam, Slack Off |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 67 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Infernape | 68 | Passho Berry | Blaze | Jolly | Flare Blitz, Close Combat, U-turn, Slack Off |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Wise Glasses; Surf, Psychic, Ice Beam, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 70 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Infernape 71 (Passho Berry; Flare Blitz, Close Combat, U-turn, Slack Off). Expected: about 100 / 0.6 / 53 in my simulator, where today's file reads 100 / 1.3 / 18.

### Lucas 3 (player chose Turtwig): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 66 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 67 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Empoleon | 68 | Chople Berry | Torrent | Modest | Surf, Blizzard, Roar, Stealth Rock |

Today's team: Nidoqueen 69 (Black Sludge; Earthquake, Poison Jab, Ice Punch, Toxic Spikes), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 69 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Empoleon 71 (Chople Berry; Surf, Blizzard, Roar, Stealth Rock). Expected: about 99 / 1.8 / 7 in my simulator, where today's file reads 92 / 3.0 / 0.

### Lucas 3 (player chose Chimchar): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 66 | Life Orb | Regenerator | Quiet | Surf, Psychic, Trick Room, Slack Off |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 67 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Torterra | 68 | Yache Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Leech Seed |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Life Orb; Surf, Psychic, Trick Room, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Torterra 71 (Yache Berry; Wood Hammer, Earthquake, Stone Edge, Leech Seed). Expected: about 100 / 0.9 / 42 in my simulator, where today's file reads 100 / 1.1 / 31.

### Lucas 3 (player chose Piplup): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter, three under the cap (Ian, 2026-10-07: the ace at 68, the gaps kept).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 66 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 66 | Wise Glasses | Regenerator | Modest | Surf, Psychic, Ice Beam, Slack Off |
| Umbreon | 66 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 67 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 67 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Infernape | 68 | Passho Berry | Blaze | Jolly | Flare Blitz, Close Combat, U-turn, Slack Off |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Wise Glasses; Surf, Psychic, Ice Beam, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 70 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Infernape 71 (Passho Berry; Flare Blitz, Close Combat, U-turn, Slack Off). Expected: about 100 / 0.6 / 53 in my simulator, where today's file reads 100 / 1.3 / 18.

### Veteran Clayton: Victory Road 2F, optional, single, cap 71

Poison Heal Lickilicky on a Toxic Orb, Golem's Stealth Rock, Relicanth's Rock Head Head Smash and Staraptor. Today's Double Team is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lickilicky | 69 | Toxic Orb | Poison Heal | default | Body Slam, Knock Off, Earthquake, Power Whip |
| Golem | 66 | Sitrus Berry | Shell Armor | default | Stealth Rock, Stone Edge, Earthquake, Sucker Punch |
| Relicanth | 66 | none | Rock Head | default | Head Smash, Liquidation, Earthquake, Yawn |
| Staraptor | 66 | none | Reckless | default | Brave Bird, Close Combat, U-turn, Quick Attack |

Today's team: Staraptor 63 (Brave Bird, Quick Attack, Double Team, Close Combat), Lickilicky 63 (Slam, Power Whip, Earthquake, Brick Break), Relicanth 63 (Stone Edge, Waterfall, Earthquake, Yawn). Expected: 97 / 1.48 / 21 blind in my simulator, about 68 clean in the scorer's terms.

### Ace Trainer Sydney: Victory Road 2F, optional, single, Ace Trainer, cap 71

Torkoal's Stealth Rock and Yawn behind a Focus Sash, Clefable, Torterra, Vaporeon's Wish, Togekiss and a Calm Mind Espeon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Torkoal | 66 | Focus Sash | Shell Armor | Relaxed | Stealth Rock, Lava Plume, Earth Power, Yawn |
| Clefable | 66 | Leftovers | Magic Guard | Bold | Moonblast, Flamethrower, Thunderbolt, Moonlight |
| Torterra | 67 | Miracle Seed | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Crunch |
| Vaporeon | 66 | Leftovers | Water Absorb | Bold | Surf, Ice Beam, Wish, Protect |
| Togekiss | 66 | Sitrus Berry | Serene Grace | Modest | Air Slash, Aura Sphere, Flamethrower, Roost |
| Espeon | 68 | TwistedSpoon | Synchronize | Timid | Psychic, Shadow Ball, Signal Beam, Calm Mind |

Today's team: Clefable 63 (Metronome), Torterra 63 (Earthquake, Crunch, Leech Seed, Wood Hammer), Torkoal 63 (Heat Wave, Sludge Bomb, Earth Power, Will-O-Wisp). Expected: about 98 / 0.8 / 34 with a planned six; read blind, 35 / 4.8 / 1.

### Ace Trainer Omar: Victory Road 2F, optional, single, Ace Trainer, cap 71

Rock and Bug: Aerodactyl's Stealth Rock behind a Focus Sash, Mothim, a Life Orb Rampardos, a Rock Polish Armaldo, Scizor's Bullet Punch and a Mamoswine ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Aerodactyl | 66 | Focus Sash | Rock Head | Jolly | Stealth Rock, Stone Edge, Earthquake, Ice Fang |
| Mothim | 66 | SilverPowder | Tinted Lens | Modest | Bug Buzz, Air Slash, Psychic, Energy Ball |
| Rampardos | 67 | Life Orb | Rock Head | Adamant | Head Smash, Zen Headbutt, Earthquake, Fire Punch |
| Armaldo | 66 | Sitrus Berry | Hyper Cutter | Adamant | X-Scissor, Stone Edge, Earthquake, Rock Polish |
| Scizor | 66 | Metal Coat | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Superpower |
| Mamoswine | 68 | Lum Berry | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |

Today's team: Mamoswine 63 (Earthquake, Ice Fang, Rock Slide, Giga Impact), Mothim 63 (Bug Buzz, Air Slash, Psychic, Toxic), Rampardos 63 (Head Smash, Zen Headbutt, Iron Head, ThunderPunch). Expected: about 98 / 1.6 / 11 with a planned six; read blind, 25 / 5.2 / 0.

### Double Team Al and Kay: Victory Road 2F, optional, double, cap 71

Fake Out and Helping Hand: Kangaskhan opens, Miltank helps, Tauros's Rock Slide hits both sides, and Ditto copies a threat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kangaskhan | 68 | Silk Scarf | Scrappy | default | Fake Out, Double-Edge, Sucker Punch, Drain Punch |
| Miltank | 67 | Leftovers | Thick Fat | default | Body Slam, Milk Drink, Helping Hand, Play Rough |
| Tauros | 68 | none | Intimidate | default | Double-Edge, Rock Slide, Zen Headbutt, Iron Head |
| Ditto | 66 | Quick Claw | Imposter | default | Transform |

Today's team: Ditto 63 (Transform), Tauros 63 (Giga Impact, Zen Headbutt, Earthquake, Stone Edge), Miltank 63 (Double-Edge, Earthquake, Seismic Toss, Milk Drink), Kangaskhan 63 (Sucker Punch, Mega Punch, Fire Punch, Ice Punch). Expected: not readable yet (a double).

### Dragon Tamer Ondrej: Victory Road B1F, optional, single, cap 71

Altaria's Will-O-Wisp, an Eviolite Dragonair, Kingdra's Draco Meteor and Salamence. Today's Perish Song is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Altaria | 69 | Leftovers | Cloud Nine | default | Moonblast, Dragon Pulse, Roost, Will-O-Wisp |
| Dragonair | 66 | Eviolite | Shed Skin | default | Dragon Rush, ExtremeSpeed, Thunder Wave, Aqua Tail |
| Kingdra | 67 | Scope Lens | Sniper | default | Draco Meteor, Scald, Ice Beam, Flip Turn |
| Salamence | 66 | none | Intimidate | default | Outrage, Earthquake, Fire Blast, Roost |

Today's team: Altaria 63 (Dragon Dance, Outrage, Sky Attack, Perish Song), Salamence 63 (Draco Meteor, Hidden Power, Heat Wave, Tailwind), Kingdra 63 (Ice Beam, Hydro Pump, Agility, Dragon Pulse). Expected: 94 / 2.15 / 8 blind in my simulator, about 63 clean in the scorer's terms.

### Psychic Valencia: Victory Road B1F, optional, single, cap 71

Chimecho's Yawn and Heal Bell, Dusknoir's Will-O-Wisp, Absol's Psycho Cut and Mismagius's Mystical Fire.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chimecho | 69 | Leftovers | Levitate | default | Psyshock, Dazzling Gleam, Heal Bell, Yawn |
| Mismagius | 66 | none | Levitate | default | Shadow Ball, Mystical Fire, Dazzling Gleam, Thunderbolt |
| Absol | 67 | none | Justified | default | Night Slash, Psycho Cut, Sucker Punch, Play Rough |
| Dusknoir | 67 | none | Levitate | default | Shadow Punch, Shadow Sneak, Will-O-Wisp, Pain Split |

Today's team: Chimecho 63 (Heal Bell, Safeguard, Extrasensory, Shadow Ball), Absol 63 (X-Scissor, Night Slash, Zen Headbutt, Psycho Cut), Dusknoir 63 (Shadow Punch, ThunderPunch, Ice Punch, Fire Punch). Expected: 95 / 1.72 / 17 blind in my simulator, about 67 clean in the scorer's terms.

### Ace Trainer Henry: Victory Road B1F, optional, single, Ace Trainer, cap 71

Crawdaunt's Swords Dance, Magmortar's Will-O-Wisp, Electivire, a Moxie Gyarados, Weavile's Ice Shard and a Rhyperior ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Crawdaunt | 66 | Mystic Water | Adaptability | Adamant | Crabhammer, Night Slash, Brick Break, Swords Dance |
| Magmortar | 66 | Charcoal | Flame Body | Modest | Fire Blast, Psychic, Focus Blast, Will-O-Wisp |
| Electivire | 66 | Magnet | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |
| Gyarados | 67 | Wacan Berry | Moxie | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Weavile | 66 | NeverMeltIce | Technician | Jolly | Ice Shard, Night Slash, Ice Punch, Brick Break |
| Rhyperior | 68 | Passho Berry | Solid Rock | Adamant | Earthquake, Stone Edge, Hammer Arm, Ice Punch |

Today's team: Rhyperior 63 (Stone Edge, Earthquake, Hammer Arm, Poison Jab), Crawdaunt 63 (Crabhammer, Night Slash, Brick Break, Swords Dance), Magmortar 63 (Fire Blast, Psychic, Focus Blast, Will-O-Wisp). Expected: about 97 / 2.2 / 4 with a planned six; read blind, 49 / 4.7 / 1.

### Double Team Jo and Pat: Victory Road B1F, optional, double, cap 71

Earthquake beside a Levitate Claydol, with the Sheer Force Nidos' spread Sludge Wave and Nidoqueen's Stealth Rock. Today's Fissure is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 68 | Leftovers | Levitate | default | Psychic, Earth Power, Ice Beam, Rapid Spin |
| Nidoqueen | 67 | Sitrus Berry | Sheer Force | default | Earth Power, Sludge Wave, Ice Beam, Stealth Rock |
| Dugtrio | 67 | none | Sand Veil | default | Earthquake, Sucker Punch, Rock Slide, Stone Edge |
| Nidoking | 68 | Life Orb | Sheer Force | default | Earth Power, Sludge Wave, Ice Beam, Flamethrower |

Today's team: Claydol 63 (Psychic, AncientPower, Sandstorm, Selfdestruct), Nidoqueen 63 (Earth Power, Sludge Bomb, Sandstorm, Stealth Rock), Dugtrio 63 (Fissure, Earthquake, Sucker Punch, Rock Slide), Nidoking 63 (Poison Jab, Earthquake, Megahorn, Brick Break). Expected: not readable yet (a double).

### Barry 6 (player chose Piplup): Pokemon League gate, on the path, single, rival, cap 71

Today's roster idea at the cap: Ambipom's Fake Out lead, a Focus Sash Staraptor, Dragonite with Thunder Wave, a Hypnosis Ninetales (Starmie in the Turtwig version), a Curse Snorlax, and his starter at 71 with a Life Orb and a setup move (Torterra, Infernape or Empoleon by the player's choice).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 70 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 70 | Focus Sash | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Dragonite | 70 | Yache Berry | Inner Focus | Adamant | Outrage, Earthquake, Fire Punch, Thunder Wave |
| Ninetales | 70 | Charcoal | Magic Guard | Timid | Fire Blast, Energy Ball, Extrasensory, Hypnosis |
| Snorlax | 70 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Curse |
| Torterra | 71 | Life Orb | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Swords Dance |

Today's team: Staraptor 70 (Focus Sash; Close Combat, Brave Bird, Quick Attack, U-turn), Starmie 70 (Sitrus Berry; Hydro Pump, Psychic, Ice Beam, Recover), Dragonite 70 (Yache Berry; Outrage, Waterfall, Earthquake, Thunder Wave), Ninetales 70 (Wide Lens; Fire Blast, Energy Ball, Hypnosis, Nasty Plot), Snorlax 70 (Chesto Berry; Body Slam, Zen Headbutt, Earthquake, Rest), Torterra 71 (Leftovers; Wood Hammer, Earthquake, Crunch, Leech Seed). Expected: about 96 / 3.1 / 0 in my simulator, where today's file reads 92 / 2.9 / 0.

### Barry 6 (player chose Turtwig): Pokemon League gate, on the path, single, rival, cap 71

The same roster with Starmie in Ninetales' place and Infernape as his starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 70 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 70 | Focus Sash | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Dragonite | 70 | Yache Berry | Inner Focus | Adamant | Outrage, Earthquake, Fire Punch, Thunder Wave |
| Starmie | 70 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Thunder Wave |
| Snorlax | 70 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Curse |
| Infernape | 71 | Life Orb | Blaze | Jolly | Flare Blitz, Close Combat, Mach Punch, Swords Dance |

Today's team: Staraptor 70 (Focus Sash; Close Combat, Brave Bird, Quick Attack, U-turn), Starmie 70 (Sitrus Berry; Hydro Pump, Psychic, Ice Beam, Recover), Dragonite 70 (Yache Berry; Outrage, Waterfall, Earthquake, Thunder Wave), Shiftry 70 (Tanga Berry; Seed Bomb, Sucker Punch, Low Kick, Tailwind), Snorlax 70 (Chesto Berry; Body Slam, Zen Headbutt, Earthquake, Rest), Infernape 71 (Life Orb; Fire Punch, Close Combat, ThunderPunch, Swords Dance). Expected: about 99 / 3.1 / 0 in my simulator.

### Barry 6 (player chose Chimchar): Pokemon League gate, on the path, single, rival, cap 71

The same roster with Empoleon as his starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 70 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 70 | Focus Sash | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Dragonite | 70 | Yache Berry | Inner Focus | Adamant | Outrage, Earthquake, Fire Punch, Thunder Wave |
| Ninetales | 70 | Charcoal | Magic Guard | Timid | Fire Blast, Energy Ball, Extrasensory, Hypnosis |
| Snorlax | 70 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Curse |
| Empoleon | 71 | Life Orb | Torrent | Adamant | Waterfall, Drill Peck, Earthquake, Swords Dance |

Today's team: Staraptor 70 (Focus Sash; Close Combat, Brave Bird, Quick Attack, U-turn), Shiftry 70 (Tanga Berry; Seed Bomb, Sucker Punch, Low Kick, Tailwind), Dragonite 70 (Yache Berry; Outrage, Waterfall, Earthquake, Thunder Wave), Ninetales 70 (Wide Lens; Fire Blast, Energy Ball, Hypnosis, Will-O-Wisp), Snorlax 70 (Chesto Berry; Body Slam, Zen Headbutt, Earthquake, Rest), Empoleon 71 (Salac Berry; Flail, Waterfall, Swords Dance, Endure). Expected: about 83 / 3.0 / 0 in my simulator.

### Volkner (Fight Area): Fight Area, on the path, tag with Flint, beside a partner, cap 71

Four Electric types two and three under the cap: Jolteon's Thunder Wave, a Nasty Plot Raichu, Luxray and a Life Orb Electivire.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jolteon | 68 | Magnet | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Volt Switch, Thunder Wave |
| Raichu | 68 | Lum Berry | Static | Timid | Thunderbolt, Focus Blast, Surf, Nasty Plot |
| Luxray | 68 | Expert Belt | Guts | Adamant | Thunder Fang, Crunch, Ice Fang, Superpower |
| Electivire | 69 | Life Orb | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Luxray 74 (Ice Fang, Thunder Fang, Crunch, Fire Fang), Jolteon 74 (Thunder, Shadow Ball, Signal Beam, Thunder Wave), Electivire 75 (Sitrus Berry; ThunderPunch, Fire Punch, Cross Chop, Giga Impact). Expected: not readable yet (a tag battle).

### Flint (Fight Area): Fight Area, on the path, tag with Volkner, beside a partner, cap 71

Four Fire types: a Nasty Plot Houndoom, Arcanine's ExtremeSpeed, a Life Orb Infernape and Magmortar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Houndoom | 68 | Charcoal | Flash Fire | Timid | Flamethrower, Dark Pulse, Sludge Bomb, Nasty Plot |
| Arcanine | 68 | Sitrus Berry | Intimidate | Adamant | Flare Blitz, ExtremeSpeed, Crunch, Thunder Fang |
| Infernape | 68 | Life Orb | Blaze | Jolly | Flare Blitz, Close Combat, U-turn, Mach Punch |
| Magmortar | 69 | Wise Glasses | Flame Body | Modest | Flamethrower, Thunderbolt, Focus Blast, Psychic |

Today's team: Houndoom 74 (Flamethrower, Sludge Bomb, Dark Pulse, Sunny Day), Arcanine 74 (Flare Blitz, Thunder Fang, Iron Head, Crunch), Magmortar 75 (Sitrus Berry; Fire Blast, Thunderbolt, SolarBeam, Hyper Beam). Expected: not readable yet (a tag battle).

