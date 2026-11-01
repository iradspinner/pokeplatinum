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
| Argenta, Hall Matron | Byron (53), in Barry 5's stretch | Pal Park lobby's north gallery, once the Pal Park partner double is won | A Gold Bottle Cap and three Bottle Caps, once (Ian, 2026-11-01; `argenta-place.md`) | Ordinary |
| Palmer, Tower Tycoon (undecided, Ian 2026-10-31) | Galactic (65) or League (78) | The Battle Zone, or a Route 224 opened as the last optional boss before the Champion | Large rewards | Ordinary |

Dahlia's, Darach's, Thorton's and Argenta's placements are settled;
Palmer's is tentative.

## Ian's draft teams (2026-09-27)

Levels are placeholders until Ian sets them.

| Brain | Pokemon |
|---|---|
| Palmer | Dragonite, Heatran, Cresselia, Milotic, Rhyperior, Xurkitree |
| Thorton | Toxapex, Bronzong, Dusclops, Ferrothorn, Turtonator, Guzzlord, all at 47 (Ian's six and his answers, 2026-10-31, `byron-brains-check.md`; free slot `dummy_077`) |
| Dahlia | Cloyster, Slowbro, Rapidash, Togekiss, Leafeon, Lopunny, all at 40 (Ian's six, 2026-10-31, `dahlia-check.md`; free slot `dummy_007`) |
| Darach (double) | Galarian Rapidash, Corviknight, Sinistcha, Armarouge, Galarian Articuno, Entei, all at 44 (Ian's six, 2026-10-31, `darach-check.md`; free slot `dummy_008`), at about Wake's difficulty |
| Argenta | Skarmory, Annihilape, Dubwool, Diancie, Meowscarada, Pheromosa, all at 50 (Ian's six and his answers, 2026-10-31, `byron-brains-check.md`; free slot `dummy_086`) |

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
- Thorton: placed (`overseer-thorton-place`, 2026-10-31). He stands in
  Mr. Fuego's room at the heart of Ironworks Hall, beside the one tile
  where the moving floor lets the player in, and asks before his fight,
  which opens in the permanent Trick Room (`sPermanentTrickRoomTrainers`,
  which the simulator reads too). His six are Ian's, all at 47
  (`byron-brains-check.md`). Straight after the win a menu offers the final
  stages of the two starter lines the player did not choose, at 40, given
  at Ironworks Hall as a capture of its own; a full party or "Not now"
  leaves it with him until the player comes back. The OxiDex counts it as
  a real source after his fight, and `fights.json` lists his fight in
  Barry 5's stretch. Needs: Ian's in-game check.
- Argenta: placed (`overseer-argenta-place`, 2026-11-01;
  `argenta-place.md` has the summary and the reward question). She stands
  at the west end of Pal Park lobby's north gallery once the partner
  double is won, appearing as it ends, and asks before her fight, an
  ordinary single battle. Her six are Ian's, all at 50. Her win gives a
  Gold Bottle Cap and three Bottle Caps once, under `FLAG_UNUSED_0x054D`
  (Ian's choice, 2026-11-01). Needs: Ian's in-game check.
- Dahlia, Darach and Argenta joined Thorton in `fights.json` (Ian,
  2026-11-01: "Add her along with Dahlia and Darach"), each in its split's
  story order with no honour cap of its own. Goal 3 reads Dahlia and
  Argenta as bosses and drops Darach and Caitlin as a double, marked tag
  as the tag battles are. Dahlia's permanent Wonder Room is not modelled by
  the simulator, and goal 3 places Dahlia's and Argenta's fights at their
  split's start (`argenta-place.md`, "What could not be checked").
- All five: trainer records in the free trainer slots, the gate scripts, and
  the standing rules that bind any trainer team: Choice items nearly gone,
  weather free to trainers, and no Brain's reward handing out a weather
  ability.
