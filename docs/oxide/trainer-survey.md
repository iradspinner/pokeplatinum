# The trainer list, surveyed

A read-through of all 928 trainer files on `oxide` (2026-09-27, the Overseer, at
Ian's request), for material the Frontier Brains, the trainer pass and the
gauntlets can reuse, and for what it shows about the base ROM. Nothing was
changed. 587 trainers are placed in a split; the other 341 are 160 dummy
slots, 149 rematch teams, 12 unused early teams and 20 others.

## The Frontier Brains already have teams

The base ROM fields all five Brains after the Champion, six Pokemon each at
levels 88 to 90. Moving each to its new place means lowering the levels to its
split's cap, taking the Choice items off (seven among them), and swapping the
slots that are too strong for the split, mostly the legendaries.

| Brain | New place (cap) | Base ROM team, level 88 to 90 (item) |
|---|---|---|
| Dahlia | Maylene (39) | Ludicolo (Salac Berry), Medicham (Choice Scarf), Dusknoir (Expert Belt), Zapdos (Leftovers), Blaziken (Life Orb), Togekiss (Choice Specs) |
| Darach | Wake (44) | Meganium (Light Clay), Gallade (Choice Scarf), Entei (Life Orb), Houndoom (Passho Berry), Staraptor (Choice Band), Empoleon (Petaya Berry) |
| Thorton | Byron (53) | Alakazam (Choice Specs), Arcanine (Life Orb), Gyarados (Wacan Berry), Exeggutor (Leftovers), Machamp (Flame Orb), Pidgeot (Choice Band) |
| Argenta | Byron (53) | Nidoqueen (Focus Sash), Persian (Silk Scarf), Kangaskhan (Choice Band), Rhyperior (Leftovers), Nidoking (Black Sludge), Mewtwo (Life Orb) |
| Palmer | Galactic (65) | Milotic (Salac Berry), Rhyperior (Life Orb), Dragonite (Lum Berry), Regigigas (Chople Berry), Heatran (Focus Sash), Cresselia (Leftovers) |

Palmer's is Ian's draft with Regigigas where the draft has Xurkitree. The other
four differ from his drafts, so each is a second option to pick from. Darach's
is a single-battle team; the double battle with Caitlin needs her three added.
Their moves and natures are in the files, and the team builder opens each one
(for example `#trainers/tower_tycoon_palmer_dummy`).

## Five level 100 superbosses, post-game

Cyrus (Houndoom, Honchkrow, Salamence, Rotom, Weavile, Darkrai), Red (Pikachu,
Lapras, Snorlax, Venusaur, Charizard, Blastoise), Gold (Typhlosion, Togekiss,
Celebi, Suicune, Lugia, Ho-Oh), May (Swampert, Blaziken, Sceptile, Latias,
Deoxys, Rayquaza) and Steven (Skarmory, Claydol, Aggron, Cradily, Armaldo,
Metagross). The scripts start them by number at the Resort Area, Stark
Mountain, Turnback Cave and Mt. Coronet. The base ROM's PC reset that let
them be fought again is gone from every PC (Ian's Pocket PC rulings,
4e6209dab). Stark Mountain's last room has lost its
legendary; Steven, in its first room, stays.

## 149 rematch teams nobody can reach

Every Vs. Seeker rematch team is still in the data, most at levels 50 to 64
with two or three Pokemon, but no map or script reaches them since the Vs.
Seeker became the Pocket PC. They are ready-made stronger versions of the
route trainers, which is raw material for the trainer pass's rise in ordinary
trainers' power; the Battle Zone's route trainers could borrow from them too.
Like every other team in the data, they hold only Generation 1 to 4 species,
so building on them keeps the trainer side Generation 4 unless the pass brings
the newer species in on purpose (Ian, 2026-09-27).

## Other teams worth knowing

- Barry's Spear Pillar teams (58 to 59, one per starter) are his side of the
  tag battle against Mars and Jupiter: the script picks the partner through a
  variable, so no tool sees them by name or number. The Fight Area teams (74
  to 75) are most likely the same kind of partner team, and the Survival Area
  has an unused set (69 to 75) beside the placed fights at 59 to 65 and 79 to
  85.
- The Battleground's five (Buck, Cheryl, Marley, Riley at 80 to 82, Mira at 71
  to 75) and the Elite Four's and Cynthia's rematches (83 to 90) are post-game.
- The Maids called "Experiencia" (slots 208 to 222) are the base ROM's
  experience and Day Care training battles: Blissey teams from level 12 to
  100, and level 1 teams.
- The 12 "unused" early teams (levels 3 to 7) are Platinum's own leftovers.

## What the placed teams show

- **Choice items:** 43 on placed trainers, 19 of them in the League: every
  Elite Four member and Cynthia carries two to four. The Choice ruling's work
  is mostly there and on the Brains.
- **Legendaries on story trainers:** Mars's Mesprit and Saturn's Azelf at the
  lakes, Saturn's Uxie and Cresselia and Cyrus's Suicune at Galactic HQ,
  Cyrus's Heatran and Regirock in the Distortion World, Candice's Articuno,
  and two Mt. Coronet 5F grunts with Celebi and Darkrai.
- **No new species on any placed trainer.** None of the 159 species added from
  later generations appears in a placed party, so the trainer pass is where
  the player first meets them on the other side.

## For the tools

The balance data finds a script's trainer by name or, since 2026-09-27, by a
dummy slot's number. The five superbosses have no split because they are
post-game, and the Maids are skipped on purpose; no other script-started
trainer is missed.
