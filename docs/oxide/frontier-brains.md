# The Frontier Brains as optional bosses

Ian's design of 2026-09-27: the five Battle Frontier Brains become optional
boss fights spread through the story, so they are not all in the Battle Zone.
Ian builds the teams; the drafts below are his, with levels, moves, items,
abilities and natures still to come. The scorer reads each team as it firms up
(the double battle once the readings take doubles, which they do not yet), and
the fights are scripted once the teams are final.

## Where each fight is, and what it guards

| Brain | Split (cap) | Place | What it gates or gives | Rule of the fight |
|---|---|---|---|---|
| Dahlia, Arcade Star | Maylene (39) | Inside the Veilstone Game Corner's entrance | Access to the Game Corner's prizes, whose list the balance track reviews | Opens in a permanent Wonder Room |
| Darach, Castle Valet | Wake (44) | The Pokemon Mansion on Route 212 | Access to the Mansion | A double battle as one trainer, Darach's own class (his sprite already shows Caitlin beside him) |
| Thorton, Factory Head | Byron (53) | The heart of Fuego Ironworks, in the building now named "Ironworks Hall" (the name Ian approved) | The player picks one of the two starter lines they did not choose, fully evolved at level 40, a capture of its own | Opens in a permanent Trick Room (Saturn 2's mechanism) |
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
| Dahlia | Cloyster, Slowbro, Rapidash, Togekiss, Leafeon, Lopunny, all at 40 (Ian's six, 2026-10-31, `dahlia-check.md`; free slot `dummy_007`) |
| Darach (double) | Galarian Rapidash, Corviknight, Sinistcha, Armarouge, Galarian Articuno, Entei, all at 44 (Ian's six, 2026-10-31, `darach-check.md`; free slot `dummy_008`), at about Wake's difficulty |
| Argenta | Skarmory, Annihilape, Dubwool, Whiscash, Meowscarada, Pheromosa |

Galarian Articuno replaces Sigilyph, which is not in the game (Ian,
2026-09-27). Every species listed is in the game.

## What each fight needs before it can be scripted

- Dahlia: placed (`overseer-brains-placement`, 2026-10-31). She stands
  inside the Game Corner's door and asks before her fight, which opens in
  the permanent Wonder Room (`sPermanentWonderRoomTrainers`). The gate is
  the prize counter next door, which trades only once she is beaten; the
  slots, the coins clerk and Rocco stay open. Needs: Ian's in-game check.
- Darach and Caitlin: placed (`overseer-brains-placement`, 2026-10-31).
  They stand at the top of the entrance hall's aisle, and a trigger across
  it holds the player until they are beaten, so the office, the maids and
  the Trophy Garden open only on the win (the field model agrees). Darach,
  not Mr. Backlot, hands over the Manaphy egg straight after the win, under
  the office's old received flag, and the office maid no longer offers it.
  The OxiDex counts the egg as the Mansion's own capture after the fight.
  Manaphy's Tail Glow is at 70, and Backlot's daily Trophy Garden Pokemon
  stay behind the National Dex. Needs: Ian's in-game check.
- Thorton: his trainer added to `sPermanentTrickRoomTrainers` in `battle_lib.c`,
  and the prize's scripted capture. Ironworks Hall, the location name that
  makes it a capture of its own, is merged (1902bd197).
- All five: trainer records in the free trainer slots, the gate scripts, and
  the standing rules that bind any trainer team: Choice items nearly gone,
  weather free to trainers, and no Brain's reward handing out a weather
  ability.
