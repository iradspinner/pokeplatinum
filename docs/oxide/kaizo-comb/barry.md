# The comb: Barry's split

The bosses of Barry's split are combed: Ace Trainer Mariah and Lucas and
Dawn 3 on Victory Road, the optional Ace Trainers Sydney, Omar and Henry on
its upper and lower floors, Barry 6 at the League's gate, and the Fight
Area's Volkner and Flint tag. All 15 files pass the checker and the rule
audit. The split's ordinary trainers follow in the later pass.

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
15 reading decides whether to even it. Lucas and Dawn 3 keep today's sets and
read 93 to 99 won to today's 92 to 99.8. Mariah, whom the player must pass,
reads 87 won with a planned six; the optional Sydney, Omar and Henry read 97
to 98 planned and 25 to 49 met blind.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Barry 6 takes today's roster idea | My Barry 3 to 5 grew one skeleton (Ambipom, Staraptor, Heracross, Floatzel, Snorlax, starter). At 71 it read softer than today's Barry 6, so Barry 6 keeps the Ambipom Fake Out lead and adds today's Dragonite and Ninetales (Starmie in the Turtwig version, to avoid two Fire types), with a Curse Snorlax and his starter at the cap with a setup move. | `rival_pokemon_league_*.json`; the scorer's reading at step 15. | Accept (recommended), or keep the earlier skeleton. |
| 2 | Lucas and Dawn 3 keep today's sets | Ian's six per file, with natures added and Tangrowth's Power Whip (no longer in its lists) as Leaf Storm. The Piplup version keeps the Chimchar line, as Ian ruled. | `dummy_779.json` to `dummy_784.json`. | Accept (recommended). |
| 3 | Fight Area tag | Volkner and Flint bring four each at 68 to 69. | The scorer cannot read tag battles yet. | Nothing now. |

## What comes next

The League's bosses are in `league.md`; then the ordinary trainers from
Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Ace Trainer Mariah | Victory Road 1F | gym-like stretch, on the path | single, Ace Trainer | 6 | 66 to 68 | Glalie's Spikes behind a Focus Sash | about 87 / 2.5 / 3 with a planned six |
| Dawn 3 (player chose Turtwig) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | Today's six (Ian's design) kept | about 93 / 3.4 / 0 in my simulator, where today's file reads 92 / 3.0 / 0 |
| Dawn 3 (player chose Chimchar) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | Today's six (Ian's design) kept | about 97 / 2.2 / 12 in my simulator, where today's file reads 100 / 1.1 / 31 |
| Dawn 3 (player chose Piplup) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | Today's six (Ian's design) kept | about 99 / 1.5 / 14 in my simulator, where today's file reads 100 / 1.3 / 18 |
| Lucas 3 (player chose Turtwig) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | The same six as Dawn's file for this starter | about 93 / 3.4 / 0 in my simulator, where today's file reads 92 / 3.0 / 0 |
| Lucas 3 (player chose Chimchar) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | The same six as Dawn's file for this starter | about 97 / 2.2 / 12 in my simulator, where today's file reads 100 / 1.1 / 31 |
| Lucas 3 (player chose Piplup) | Victory Road battleground | on the path | single, rival | 6 | 69 to 71 | The same six as Dawn's file for this starter | about 99 / 1.5 / 14 in my simulator, where today's file reads 100 / 1.3 / 18 |
| Ace Trainer Sydney | Victory Road 2F | optional | single, Ace Trainer | 6 | 66 to 68 | Torkoal's Stealth Rock and Yawn behind a Focus Sash | about 98 / 0.8 / 34 with a planned six |
| Ace Trainer Omar | Victory Road 2F | optional | single, Ace Trainer | 6 | 66 to 68 | Rock and Bug | about 98 / 1.6 / 11 with a planned six |
| Ace Trainer Henry | Victory Road B1F | optional | single, Ace Trainer | 6 | 66 to 68 | Crawdaunt's Swords Dance | about 97 / 2.2 / 4 with a planned six |
| Barry 6 (player chose Piplup) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | Today's roster idea at the cap | about 96 / 3.1 / 0 in my simulator, where today's file reads 92 / 2.9 / 0 |
| Barry 6 (player chose Turtwig) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | The same roster with Starmie in Ninetales' place and Infernape as his starter | about 99 / 3.1 / 0 in my simulator |
| Barry 6 (player chose Chimchar) | Pokemon League gate | on the path | single, rival | 6 | 70 to 71 | The same roster with Empoleon as his starter | about 83 / 3.0 / 0 in my simulator |
| Volkner (Fight Area) | Fight Area | on the path | tag with Flint, beside a partner | 4 | 68 to 69 | Four Electric types two and three under the cap | not readable yet (a tag battle) |
| Flint (Fight Area) | Fight Area | on the path | tag with Volkner, beside a partner | 4 | 68 to 69 | Four Fire types | not readable yet (a tag battle) |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

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

### Dawn 3 (player chose Turtwig): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Empoleon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 69 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 70 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Empoleon | 71 | Chople Berry | Torrent | Modest | Surf, Blizzard, Roar, Stealth Rock |

Today's team: Nidoqueen 69 (Black Sludge; Earthquake, Poison Jab, Ice Punch, Toxic Spikes), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 69 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Empoleon 71 (Chople Berry; Surf, Blizzard, Roar, Stealth Rock). Expected: about 93 / 3.4 / 0 in my simulator, where today's file reads 92 / 3.0 / 0.

### Dawn 3 (player chose Chimchar): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Torterra.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 69 | Life Orb | Regenerator | Quiet | Surf, Psychic, Trick Room, Slack Off |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 70 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Torterra | 71 | Yache Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Leech Seed |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Life Orb; Surf, Psychic, Trick Room, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Torterra 71 (Yache Berry; Wood Hammer, Earthquake, Stone Edge, Leech Seed). Expected: about 97 / 2.2 / 12 in my simulator, where today's file reads 100 / 1.1 / 31.

### Dawn 3 (player chose Piplup): Victory Road battleground, on the path, single, rival, cap 71

Today's six (Ian's design) kept, with natures added: Nidoqueen's Toxic Spikes, Umbreon's Curse and Wish, a Life Orb Tangrowth with Sleep Powder or a Trick Room Slowbro, a Toxic Orb Lickilicky, Magmortar, and the counterpart's starter at the cap. Her starter is Infernape, the Chimchar line Ian kept for this version.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 69 | Wise Glasses | Regenerator | Modest | Surf, Psychic, Ice Beam, Slack Off |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 70 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Infernape | 71 | Passho Berry | Blaze | Jolly | Flare Blitz, Close Combat, U-turn, Slack Off |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Wise Glasses; Surf, Psychic, Ice Beam, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 70 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Infernape 71 (Passho Berry; Flare Blitz, Close Combat, U-turn, Slack Off). Expected: about 99 / 1.5 / 14 in my simulator, where today's file reads 100 / 1.3 / 18.

### Lucas 3 (player chose Turtwig): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 69 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 70 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Empoleon | 71 | Chople Berry | Torrent | Modest | Surf, Blizzard, Roar, Stealth Rock |

Today's team: Nidoqueen 69 (Black Sludge; Earthquake, Poison Jab, Ice Punch, Toxic Spikes), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 69 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Empoleon 71 (Chople Berry; Surf, Blizzard, Roar, Stealth Rock). Expected: about 93 / 3.4 / 0 in my simulator, where today's file reads 92 / 3.0 / 0.

### Lucas 3 (player chose Chimchar): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 69 | Life Orb | Regenerator | Quiet | Surf, Psychic, Trick Room, Slack Off |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Magmortar | 70 | Wise Glasses | Flame Body | Modest | Lava Plume, Thunderbolt, Focus Blast, Psychic |
| Torterra | 71 | Yache Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Leech Seed |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Life Orb; Surf, Psychic, Trick Room, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Magmortar 70 (Wise Glasses; Lava Plume, Thunderbolt, Focus Blast, Psychic), Torterra 71 (Yache Berry; Wood Hammer, Earthquake, Stone Edge, Leech Seed). Expected: about 97 / 2.2 / 12 in my simulator, where today's file reads 100 / 1.1 / 31.

### Lucas 3 (player chose Piplup): Victory Road battleground, on the path, single, rival, cap 71

The same six as Dawn's file for this starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoqueen | 69 | Black Sludge | Battle Armor | Adamant | Earthquake, Poison Jab, Ice Punch, Toxic Spikes |
| Slowbro | 69 | Wise Glasses | Regenerator | Modest | Surf, Psychic, Ice Beam, Slack Off |
| Umbreon | 69 | Leftovers | Synchronize | Calm | Payback, Curse, Wish, Protect |
| Tangrowth | 70 | Life Orb | Magic Guard | Brave | Leaf Storm, Earthquake, Rock Slide, Sleep Powder |
| Lickilicky | 70 | Toxic Orb | Guts | Adamant | Body Slam, Power Whip, Ice Punch, Earthquake |
| Infernape | 71 | Passho Berry | Blaze | Jolly | Flare Blitz, Close Combat, U-turn, Slack Off |

Today's team: Nidoqueen 69 (Black Sludge; Poison Jab, Earthquake, Ice Punch, Toxic Spikes), Slowbro 69 (Wise Glasses; Surf, Psychic, Ice Beam, Slack Off), Umbreon 69 (Leftovers; Payback, Curse, Wish, Protect), Tangrowth 70 (Life Orb; Power Whip, Earthquake, Rock Slide, Sleep Powder), Lickilicky 70 (Toxic Orb; Body Slam, Power Whip, Ice Punch, Earthquake), Infernape 71 (Passho Berry; Flare Blitz, Close Combat, U-turn, Slack Off). Expected: about 99 / 1.5 / 14 in my simulator, where today's file reads 100 / 1.3 / 18.

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

