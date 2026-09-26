# The Frontier Brains as optional bosses

Ian's design of 2026-09-27: the five Battle Frontier Brains become optional
boss fights spread through the story, so they are not all in the Battle Zone.
Ian builds the teams; the drafts below are his, with levels, moves, items,
abilities and natures still to come. The balance track scores each team as it
firms up (all but the double battle, which its tool cannot score), and the main
track scripts the fights once the teams are final.

## Where each fight is, and what it guards

| Brain | Split (cap) | Place | What it gates or gives | Rule of the fight |
|---|---|---|---|---|
| Dahlia, Arcade Star | Maylene (39) | Inside the Veilstone Game Corner's entrance | Access to the Game Corner's prizes, whose list the balance track reviews | Opens in a permanent Wonder Room |
| Darach, Castle Valet | Wake (44) | The Pokemon Mansion on Route 212 | Access to the Mansion | A double battle as one trainer, Darach's own class (his sprite already shows Caitlin beside him) |
| Thorton, Factory Head | Byron (53) | The heart of Fuego Ironworks, in the building now named "Ironworks Hall" (a draft name) | The player picks one of the two starter lines they did not choose, fully evolved at level 40, a capture of its own | Opens in a permanent Trick Room (Saturn 2's mechanism) |
| Argenta, Hall Matron (tentative spot) | Byron (53) | Pal Park, second floor | Items, which the balance track's item pass picks | Ordinary |
| Palmer, Tower Tycoon (tentative spot) | Galactic (65) | The Resort Area's entrance | To be decided | Ordinary |

Dahlia's, Darach's and Thorton's placements are settled; Argenta's and
Palmer's are tentative.

## Ian's draft teams (2026-09-27)

Levels are placeholders until Ian sets them.

| Brain | Pokemon |
|---|---|
| Palmer | Dragonite, Heatran, Cresselia, Milotic, Rhyperior, Xurkitree |
| Thorton | Bronzong, Magnezone, Toxapex, Dhelmise, Turtonator, Guzzlord |
| Dahlia | Ludicolo, Togekiss, Rapidash, Cloyster, Lopunny, Galarian Weezing |
| Darach (double) | Incineroar, Entei, Grapploct (Darach's three), Galarian Articuno, Gallade, Gothitelle (Caitlin's three) |
| Argenta | Skarmory, Annihilape, Dubwool, Whiscash, Meowscarada, Pheromosa |

Galarian Articuno replaces Sigilyph, which is not in the game (Ian,
2026-09-27). Every species listed is in the game.

## What each fight needs before it can be scripted

- Dahlia: Wonder Room's effect and its permanent form (`cloud/element4-wonder-room`,
  running).
- Thorton: his trainer added to `sPermanentTrickRoomTrainers` in `battle_lib.c`,
  and the Ironworks Hall capture (on the main track's branch).
- All five: trainer records in the free trainer slots, the gate scripts, and
  the standing rules that bind any trainer team: Choice items nearly gone,
  weather free to trainers, and no Brain's reward handing out a weather
  ability.
