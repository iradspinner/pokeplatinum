#include "macros/scrcmd.inc"
#include "res/text/bank/sandgem_town_house.h"


    ScriptEntry SandgemTownHouse_BreederM
    ScriptEntry SandgemTownHouse_BreederF
    ScriptEntryEnd

@ Oxide: the gift clown that stood here is gone (Ian, 2026-09-27; the encounter track's
@ clown-replacements.md): its object, its script entry and its lines, with the
@ orphaned pick-menu names. Where the town had no other capture, new grass
@ outside takes its place.

SandgemTownHouse_BreederM:
    NPCMessage SandgemTownHouse_Text_GrowStrongerFromBattling
    End

SandgemTownHouse_BreederF:
    NPCMessage SandgemTownHouse_Text_GoodTrainerTakesCare
    End

