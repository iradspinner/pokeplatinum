#include "macros/scrcmd.inc"
#include "res/text/bank/fuego_ironworks_building.h"
#include "res/text/bank/menu_entries.h"


    ScriptEntry FuegoIronworksBuilding_OnTransition
    ScriptEntry FuegoIronworksBuilding_MrFuego
    ScriptEntry FuegoIronworksBuilding_Thorton
    ScriptEntryEnd

FuegoIronworksBuilding_OnTransition:
    SetFlag FLAG_FIRST_ARRIVAL_FUEGO_IRONWORKS
    End

FuegoIronworksBuilding_MrFuego:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfSet FLAG_MR_FUEGO_ASKED_FOR_TRADE, FuegoIronworksBuilding_CheckStarPieceForTradeAgain
    GoToIfSet FLAG_RECEIVED_FUEGO_IRONWORKS_BUILDING_STAR_PIECE, FuegoIronworksBuilding_CheckStarPieceForTrade
    Message FuegoIronworksBuilding_Text_HeresASouvenir
    SetVar VAR_0x8004, ITEM_STAR_PIECE
    SetVar VAR_0x8005, 1
    GoToIfCannotFitItem VAR_0x8004, VAR_0x8005, VAR_RESULT, FuegoIronworksBuilding_BagIsFull
    SetFlag FLAG_RECEIVED_FUEGO_IRONWORKS_BUILDING_STAR_PIECE
    Common_GiveItemQuantity
    GoTo FuegoIronworksBuilding_CheckStarPieceForTrade
    End

FuegoIronworksBuilding_CheckStarPieceForTrade:
    CheckItem ITEM_STAR_PIECE, 1, VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, FuegoIronworksBuilding_AskTradeStarPieceForShards
    Message FuegoIronworksBuilding_Text_TradeStarPiecesForShards
    GoTo FuegoIronworksBuilding_MrFuegoEnd
    End

FuegoIronworksBuilding_AskTradeStarPieceForShards:
    SetFlag FLAG_MR_FUEGO_ASKED_FOR_TRADE
    Message FuegoIronworksBuilding_Text_AskTradeStarPiecesForShards
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, FuegoIronworksBuilding_TryTrade
    GoToIfEq VAR_RESULT, MENU_NO, FuegoIronworksBuilding_YoureNotTrading
    End

FuegoIronworksBuilding_CheckStarPieceForTradeAgain:
    CheckItem ITEM_STAR_PIECE, 1, VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, FuegoIronworksBuilding_AnyStarPieces
    Message FuegoIronworksBuilding_Text_WantToTrade
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, FuegoIronworksBuilding_TryTrade
    GoToIfEq VAR_RESULT, MENU_NO, FuegoIronworksBuilding_YoureNotTrading
    End

FuegoIronworksBuilding_AnyStarPieces:
    Message FuegoIronworksBuilding_Text_AnyStarPieces
    GoTo FuegoIronworksBuilding_MrFuegoEnd
    End

FuegoIronworksBuilding_MrFuegoEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

FuegoIronworksBuilding_YoureNotTrading:
    Message FuegoIronworksBuilding_Text_YoureNotTrading
    GoTo FuegoIronworksBuilding_MrFuegoEnd
    End

FuegoIronworksBuilding_TryTrade:
    GetItemQuantity ITEM_STAR_PIECE, VAR_0x8000
    GoToIfGe VAR_0x8000, 10, FuegoIronworksBuilding_AskTrade10StarPieces
    GoTo FuegoIronworksBuilding_Trade1StarPiece
    End

FuegoIronworksBuilding_Trade1StarPiece:
    IncrementGameRecord RECORD_STAR_PIECES_TRADED
    RemoveItem ITEM_STAR_PIECE, 1, VAR_RESULT
    AddItem ITEM_RED_SHARD, 1, VAR_RESULT
    AddItem ITEM_BLUE_SHARD, 1, VAR_RESULT
    AddItem ITEM_YELLOW_SHARD, 1, VAR_RESULT
    AddItem ITEM_GREEN_SHARD, 1, VAR_RESULT
    GoTo FuegoIronworksBuilding_ThereYouAre
    End

FuegoIronworksBuilding_AskTrade10StarPieces:
    Message FuegoIronworksBuilding_Text_WantToTrade10StarPieces
    InitGlobalTextMenu 31, 11, 0, VAR_0x8001
    SetMenuXOriginToRight
    AddMenuEntry MenuEntries_Text_StarPieces_1, 0
    AddMenuEntry MenuEntries_Text_StarPieces_10, 1
    AddMenuEntry MenuEntries_Text_Exit2, 2
    ShowMenu
    SetVar VAR_0x8007, 10
    SetVar VAR_0x8008, VAR_0x8001
    GoToIfEq VAR_0x8008, 0, FuegoIronworksBuilding_Trade1StarPiece
    GoToIfEq VAR_0x8008, 1, FuegoIronworksBuilding_Trade10StarPieces
    GoTo FuegoIronworksBuilding_YoureNotTrading
    End

FuegoIronworksBuilding_Trade10StarPieces:
    SubVar VAR_0x8007, 1
    IncrementGameRecord RECORD_STAR_PIECES_TRADED
    AddItem ITEM_RED_SHARD, 1, VAR_RESULT
    AddItem ITEM_BLUE_SHARD, 1, VAR_RESULT
    AddItem ITEM_YELLOW_SHARD, 1, VAR_RESULT
    AddItem ITEM_GREEN_SHARD, 1, VAR_RESULT
    RemoveItem ITEM_STAR_PIECE, 1, VAR_RESULT
    GoToIfEq VAR_0x8007, 0, FuegoIronworksBuilding_ThereYouAre
    GoTo FuegoIronworksBuilding_Trade10StarPieces
    End

FuegoIronworksBuilding_ThereYouAre:
    Message FuegoIronworksBuilding_Text_ThereYouAre
    Message FuegoIronworksBuilding_Text_NothingIfNoIron
    WaitButton
    CloseMessage
    ReleaseAll
    End

FuegoIronworksBuilding_BagIsFull:
    Common_MessageBagIsFull
    CloseMessage
    ReleaseAll
    End

@ Platinum Oxide (Ian, 2026-09-27 and 2026-10-31): Thorton, the Factory Head,
@ an optional boss in Barry 5's stretch of Byron's split. He stands in the
@ heart of the ironworks, beside the tile where the moving floor brings the
@ player into Mr. Fuego's room, and fights only when spoken to. He asks
@ first, since a loss ends an Oxide run, and his fight opens in a permanent
@ Trick Room (battle_lib.c). Straight after the win the player picks one of
@ the two starter lines they did not choose, fully evolved at level 40, as a
@ Battle Factory rental. GivePokemon writes the map's location name, so the
@ prize is Ironworks Hall's own capture. FLAG_UNUSED_0x054E is set once it
@ is given; until then a full party, or a player who cannot decide, leaves
@ it with Thorton, who offers the pick again when spoken to.
FuegoIronworksBuilding_Thorton:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfDefeated TRAINER_DUMMY_077, FuegoIronworksBuilding_ThortonBeaten
    Message FuegoIronworksBuilding_Text_ThortonIntro
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, FuegoIronworksBuilding_ThortonDeclined
    Message FuegoIronworksBuilding_Text_ThortonBegin
    CloseMessage
    StartTrainerBattle TRAINER_DUMMY_077
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, FuegoIronworksBuilding_ThortonBlackOut
    SetTrainerFlag TRAINER_DUMMY_077
    Message FuegoIronworksBuilding_Text_ThortonWin
    GoTo FuegoIronworksBuilding_ThortonOffer
    End

FuegoIronworksBuilding_ThortonDeclined:
    Message FuegoIronworksBuilding_Text_ThortonDeclined
    GoTo FuegoIronworksBuilding_ThortonEnd
    End

FuegoIronworksBuilding_ThortonBeaten:
    GoToIfSet FLAG_UNUSED_0x054E, FuegoIronworksBuilding_ThortonBeatenLine
    Message FuegoIronworksBuilding_Text_ThortonKeptRental
    GoTo FuegoIronworksBuilding_ThortonOffer
    End

FuegoIronworksBuilding_ThortonBeatenLine:
    Message FuegoIronworksBuilding_Text_ThortonBeaten
    GoTo FuegoIronworksBuilding_ThortonEnd
    End

@ The menu offers the final stages of the two starter lines the player did
@ not choose. The starter is read as Barry's battles read it: Turtwig,
@ Scorbunny (in Chimchar's place since 2026-09-21), and otherwise Piplup.
FuegoIronworksBuilding_ThortonOffer:
    GetPartyCount VAR_RESULT
    GoToIfEq VAR_RESULT, MAX_PARTY_SIZE, FuegoIronworksBuilding_ThortonPartyFull
    Message FuegoIronworksBuilding_Text_ThortonPickRental
    GetPlayerStarterSpecies VAR_0x8004
    GoToIfEq VAR_0x8004, SPECIES_TURTWIG, FuegoIronworksBuilding_ThortonMenuAfterTurtwig
    GoToIfEq VAR_0x8004, SPECIES_SCORBUNNY, FuegoIronworksBuilding_ThortonMenuAfterScorbunny
    InitLocalTextMenu 31, 11, 0, VAR_RESULT
    SetMenuXOriginToRight
    AddMenuEntryImm FuegoIronworksBuilding_Text_Torterra, 0
    AddMenuEntryImm FuegoIronworksBuilding_Text_Cinderace, 1
    GoTo FuegoIronworksBuilding_ThortonShowMenu
    End

FuegoIronworksBuilding_ThortonMenuAfterTurtwig:
    InitLocalTextMenu 31, 11, 0, VAR_RESULT
    SetMenuXOriginToRight
    AddMenuEntryImm FuegoIronworksBuilding_Text_Cinderace, 1
    AddMenuEntryImm FuegoIronworksBuilding_Text_Empoleon, 2
    GoTo FuegoIronworksBuilding_ThortonShowMenu
    End

FuegoIronworksBuilding_ThortonMenuAfterScorbunny:
    InitLocalTextMenu 31, 11, 0, VAR_RESULT
    SetMenuXOriginToRight
    AddMenuEntryImm FuegoIronworksBuilding_Text_Torterra, 0
    AddMenuEntryImm FuegoIronworksBuilding_Text_Empoleon, 2
    GoTo FuegoIronworksBuilding_ThortonShowMenu
    End

FuegoIronworksBuilding_ThortonShowMenu:
    AddMenuEntryImm FuegoIronworksBuilding_Text_NotNow, 3
    ShowMenu
    SetVar VAR_0x8008, VAR_RESULT
    GoToIfEq VAR_0x8008, 0, FuegoIronworksBuilding_ThortonPickTorterra
    GoToIfEq VAR_0x8008, 1, FuegoIronworksBuilding_ThortonPickCinderace
    GoToIfEq VAR_0x8008, 2, FuegoIronworksBuilding_ThortonPickEmpoleon
    Message FuegoIronworksBuilding_Text_ThortonNotNow
    GoTo FuegoIronworksBuilding_ThortonEnd
    End

FuegoIronworksBuilding_ThortonPickTorterra:
    SetVar VAR_0x8005, SPECIES_TORTERRA
    GoTo FuegoIronworksBuilding_ThortonConfirm
    End

FuegoIronworksBuilding_ThortonPickCinderace:
    SetVar VAR_0x8005, SPECIES_CINDERACE
    GoTo FuegoIronworksBuilding_ThortonConfirm
    End

FuegoIronworksBuilding_ThortonPickEmpoleon:
    SetVar VAR_0x8005, SPECIES_EMPOLEON
    GoTo FuegoIronworksBuilding_ThortonConfirm
    End

@ A no at the confirmation goes back to the menu.
FuegoIronworksBuilding_ThortonConfirm:
    BufferSpeciesNameFromVar 0, VAR_0x8005, 0, 0
    Message FuegoIronworksBuilding_Text_ThortonConfirm
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, FuegoIronworksBuilding_ThortonOffer
    BufferSpeciesNameFromVar 1, VAR_0x8005, 0, 0
    BufferPlayerName 0
    PlayFanfare SEQ_FANFA4_sseq
    Message FuegoIronworksBuilding_Text_ThortonReceived
    WaitFanfare
    GoToIfEq VAR_0x8005, SPECIES_TORTERRA, FuegoIronworksBuilding_ThortonGiveTorterra
    GoToIfEq VAR_0x8005, SPECIES_CINDERACE, FuegoIronworksBuilding_ThortonGiveCinderace
    GivePokemon SPECIES_EMPOLEON, 40, ITEM_NONE, VAR_RESULT
    GoTo FuegoIronworksBuilding_ThortonGiven
    End

FuegoIronworksBuilding_ThortonGiveTorterra:
    GivePokemon SPECIES_TORTERRA, 40, ITEM_NONE, VAR_RESULT
    GoTo FuegoIronworksBuilding_ThortonGiven
    End

FuegoIronworksBuilding_ThortonGiveCinderace:
    GivePokemon SPECIES_CINDERACE, 40, ITEM_NONE, VAR_RESULT
    GoTo FuegoIronworksBuilding_ThortonGiven
    End

FuegoIronworksBuilding_ThortonGiven:
    SetFlag FLAG_UNUSED_0x054E
    Message FuegoIronworksBuilding_Text_ThortonGiveNickname
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, FuegoIronworksBuilding_ThortonNickname
    Message FuegoIronworksBuilding_Text_ThortonBeaten
    GoTo FuegoIronworksBuilding_ThortonEnd
    End

FuegoIronworksBuilding_ThortonNickname:
    CloseMessage
    GetPartyCount VAR_0x8006
    SubVar VAR_0x8006, 1
    FadeScreenOut
    WaitFadeScreen
    OpenPokemonNamingScreen VAR_0x8006, VAR_RESULT
    CallIfNe VAR_RESULT, 1, FuegoIronworksBuilding_ThortonRecordNickname
    FadeScreenIn
    WaitFadeScreen
    ReleaseAll
    End

FuegoIronworksBuilding_ThortonRecordNickname:
    IncrementGameRecord RECORD_POKEMON_NICKNAMED
    Return

FuegoIronworksBuilding_ThortonPartyFull:
    Message FuegoIronworksBuilding_Text_ThortonPartyFull
FuegoIronworksBuilding_ThortonEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

FuegoIronworksBuilding_ThortonBlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

    .balign 4, 0
