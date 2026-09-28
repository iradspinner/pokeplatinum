#ifndef POKEPLATINUM_EASY_CHAT_DEFS_H
#define POKEPLATINUM_EASY_CHAT_DEFS_H

#include "res/text/bank/ability_names_uppercase.h"
#include "res/text/bank/feelings.h"
#include "res/text/bank/greetings.h"
#include "res/text/bank/lifestyle_words.h"
#include "res/text/bank/move_names_uppercase.h"
#include "res/text/bank/people_words.h"
#include "res/text/bank/pokemon_type_names.h"
#include "res/text/bank/species_name.h"
#include "res/text/bank/tough_words.h"
#include "res/text/bank/trainer_words.h"

enum EasyChatType {
    EASY_CHAT_TYPE_ONE_WORD = 0,
    EASY_CHAT_TYPE_TWO_WORDS,
    EASY_CHAT_TYPE_SENTENCE,
};

enum EasyChatMode {
    GROUP_MODE = 0,
    ABC_MODE,
};

enum EasyChatGroup {
    GROUP_POKEMON = 0,
    GROUP_POKEMON_2,
    GROUP_MOVE,
    GROUP_MOVE_2,
    GROUP_STATUS,
    GROUP_TRAINER,
    GROUP_PEOPLE,
    GROUP_GREETINGS,
    GROUP_LIFESTYLE,
    GROUP_FEELINGS,
    GROUP_TOUGH_WORDS,
    GROUP_UNION,
    EASY_CHAT_GROUP_COUNT,
    GROUP_MODE_CANCEL_INDEX = EASY_CHAT_GROUP_COUNT,
};

enum ABCModeChars {
    A = 0,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    X,
    Y,
    Z,
    EXCLAMATION,
    ABC_MODE_CHAR_COUNT,
};

// Platinum Oxide: the species group is held at 655 words, the size it reached
// with the 159 new species, instead of following the species name bank. Word
// ids run on from one group to the next and are saved in mail and trainer
// messages, so a longer bank (Meloetta made it 656 names) would move every word
// after the species. Nothing is lost: the new species are not in the Easy Chat
// list (sPokemonWords stops at the natives), and the Egg words past the new
// species were never offered.
#define EASY_CHAT_SPECIES_WORD_COUNT 655

#if EASY_CHAT_SPECIES_WORD_COUNT > TEXT_BANK_SPECIES_NAME_ENTRY_COUNT
#error "the Easy Chat species group has more words than the species name bank has names"
#endif

#define MOVE_WORD(move)           (EASY_CHAT_SPECIES_WORD_COUNT + move)
#define TYPE_WORD(type)           (MOVE_WORD(TEXT_BANK_MOVE_NAMES_UPPERCASE_ENTRY_COUNT) + type)
#define ABILITY_WORD(ability)     (TYPE_WORD(TEXT_BANK_POKEMON_TYPE_NAMES_ENTRY_COUNT) + ability)
#define TRAINER_WORD(bankEntry)   (ABILITY_WORD(TEXT_BANK_ABILITY_NAMES_UPPERCASE_ENTRY_COUNT) + bankEntry)
#define PEOPLE_WORD(bankEntry)    (TRAINER_WORD(TEXT_BANK_TRAINER_WORDS_ENTRY_COUNT) + bankEntry)
#define GREETING_WORD(bankEntry)  (PEOPLE_WORD(TEXT_BANK_PEOPLE_WORDS_ENTRY_COUNT) + bankEntry)
#define LIFESTYLE_WORD(bankEntry) (GREETING_WORD(TEXT_BANK_GREETINGS_ENTRY_COUNT) + bankEntry)
#define FEELINGS_WORD(bankEntry)  (LIFESTYLE_WORD(TEXT_BANK_LIFESTYLE_WORDS_ENTRY_COUNT) + bankEntry)
#define TOUGH_WORD(bankEntry)     (FEELINGS_WORD(TEXT_BANK_FEELINGS_ENTRY_COUNT) + bankEntry)
#define UNION_WORD(bankEntry)     (TOUGH_WORD(TEXT_BANK_TOUGH_WORDS_ENTRY_COUNT) + bankEntry)

#define MAX_EASY_CHAT_WORDS 2

#define EASY_CHAT_NOTHING_CHOSEN 0xFF
#define EASY_CHAT_CANCEL         0xFE

#endif // POKEPLATINUM_EASY_CHAT_DEFS_H
