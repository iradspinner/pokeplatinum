# Proposal: a test kit for in-game checks

Written 2026-09-22 for Ian to accept, change or turn down. Nothing here is built.

Element 4 has 116 battle effect scripts to see in battle, and "Waiting on Ian" holds about ten emulator checks. Each one costs a play-through to reach. The proposal is a build of the game with a helper in the player's house, so reaching any of those checks takes a new game and a few menu choices.

## The switch

A meson option, `oxide_testkit`, boolean, default off, beside the two debug options already in `meson.options`. Meson remembers an option in the build folder once it is set, so the kit never shares `build/`: a new `make testkit` target sets it up in `build-testkit/` and writes `build-testkit/pokeplatinum.us.nds`. `make rom`, GitHub's workflow and the private builder behind `fetch-rom` never pass it, so the ROM of record and its hash do not change. The check that proves it: after the kit lands, `make rom` still matches GitHub's hash for the same commit.

The option becomes one define, `OXIDE_TESTKIT`, for the C code and for the field scripts. The scripts already run through the C preprocessor (`make_script_bin.sh` calls `gcc -E -x assembler-with-cpp`), so an `#ifdef OXIDE_TESTKIT` block vanishes from a normal build; the script tool needs one new argument to pass the define through. Two things have no preprocessor, the map's events JSON and the text banks, so the kit carries its own copy of the house's events file in `res/testkit/`, which `res/field/events/meson.build` uses in place of the real one when the option is on, and a text bank of its own appended at the end of the bank list, so no other bank's number moves.

## The helper in the player's house

One NPC in the bedroom (`twinleaf_town_player_house_2f`), with a list menu (`InitGlobalTextListMenu`, `AddListMenuEntry`, `ShowListMenu`) offering:

- Rare Candies, 99 (`AddItem`), which also covers the Rare Candy chaining check
- a Rotom, and a Giratina holding the Griseous Orb, for the form fix (`GivePokemon`)
- an Eevee that already knows Charm, so one Rare Candy should offer Sylveon (`GivePokemon`, then `ResetPartyMonMoveSlot_Unused` to put Charm in a slot)
- a Pokemon one level below a level-up move whose id is above 511, the old format's cap, for the widened learnset; the species is picked from the 361 such entries when the kit is built
- a Ralts and a Pokemon with a Dragon move, for the Fairy checks
- a warp list (`Warp`): Route 202 for trainers, Sandgem Town for the UNLOCK FPS crash, a Pokemon Center, the Move Relearner in Pastoria, the Veilstone Department Store's TM floor, and the Rotom room in the Galactic building in Eterna

Rotom's form is the one open question. The game changes it only through the appliances in that room, so the warp tests the real path. Whether the appliances work without the story flags that normally lead there is not known yet. If they do not, the fallback is a kit-only script command that sets a party Pokemon's form, registered at the end of the command table inside the same `#ifdef`.

## Trainers for the new moves

Two stages, since the player's side and the AI's side both need seeing. First, move sets: the menu gives a Pokemon loaded with one batch of new moves (the same move-slot command), so the player uses each effect against anything. Second, trainers: kit-only trainer files in `res/testkit/trainers/`, appended after the 928 real ones only when the option is on, one trainer per batch of effects, fought from the same menu with `StartTrainerBattle`. Each new batch of effect scripts adds its move set and its trainer in the same commit. Whether an appended trainer needs rows anywhere else, such as the trainer message table, is checked before the trainers are built.

## Cost and risk

The first stage (switch, NPC, items, gifts, warps) is roughly a session. The trainers are an hour a batch after that. The risk to the real game is only that something leaks into the normal build, and the hash check above catches that on every push.

## For Ian

Three questions:

- build it at all, or keep testing by play-through
- the bedroom, or somewhere else in the house
- move sets only at first, or move sets and trainers together
