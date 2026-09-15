# Base ROM import report

base: `base.nds`  vanilla: `vanilla.nds`  dry run: False

Files changed: {'species': 0, 'moves': 0, 'trainers': 534, 'trainers_party_size_changed_skipped': 153}

## res/trainers/data/youngster_tristan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 5 -> 7
- party[0].iv_scale: 0 -> 99

## res/trainers/data/youngster_logan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 5 -> 7
- party[0].moves: ['MOVE_TACKLE', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_PROTECT', 'MOVE_BUG_BITE', 'MOVE_STRING_SHOT', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 112

## res/trainers/data/lass_natalie.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 5 -> 7
- party[0].iv_scale: 0 -> 97

## res/trainers/data/youngster_michael.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 7 -> 9
- party[0].moves: None -> ['MOVE_GROWL', 'MOVE_BIDE', 'MOVE_BUG_BITE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 130
- party[1].level: 6 -> 9
- party[1].moves: None -> ['MOVE_LEECH_LIFE', 'MOVE_SUPERSONIC', 'MOVE_ASTONISH', 'MOVE_PLUCK']
- party[1].iv_scale: 0 -> 121

## res/trainers/data/dummy_005.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_005.json
- class: 'TRAINER_CLASS_CAMPER' -> 'TRAINER_CLASS_GALACTIC_BOSS'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/youngster_tyler.json
- party[0].level: 8 -> 11
- party[0].iv_scale: 10 -> 100

## res/trainers/data/lass_samantha.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 7 -> 8
- party[0].iv_scale: 0 -> 105

## res/trainers/data/lass_sarah.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SHINX' -> 'SPECIES_SENTRET'
- party[0].level: 7 -> 8
- party[0].iv_scale: 0 -> 98

## res/trainers/data/bug_catcher_brandon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 10 -> 15
- party[0].moves: ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_NONE'] -> ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_BUG_BITE']
- party[0].iv_scale: 0 -> 109
- party[1].species: 'SPECIES_KRICKETOT' -> 'SPECIES_SILCOON'
- party[1].level: 11 -> 15
- party[1].moves: ['MOVE_BIDE', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_BUG_BITE', 'MOVE_IRON_DEFENSE', 'MOVE_TACKLE', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 108

## res/trainers/data/aroma_lady_taylor.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BUDEW' -> 'SPECIES_TURTWIG'
- party[0].level: 9 -> 13
- party[0].moves: None -> ['MOVE_RAZOR_LEAF', 'MOVE_WITHDRAW', 'MOVE_TACKLE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 134
- party[1].level: 11 -> 13
- party[1].moves: None -> ['MOVE_BULLET_SEED', 'MOVE_GROWTH', 'MOVE_LEECH_SEED', 'MOVE_SYNTHESIS']
- party[1].iv_scale: 0 -> 101

## res/trainers/data/twins_liv_and_liz.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 11 -> 15
- party[0].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_SPARK', 'MOVE_QUICK_ATTACK', 'MOVE_CHARM']
- party[0].iv_scale: 0 -> 115
- party[1].species: 'SPECIES_PACHIRISU' -> 'SPECIES_PICHU'
- party[1].level: 11 -> 15
- party[1].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_CHARM', 'MOVE_THUNDER_SHOCK', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 104

## res/trainers/data/camper_jacob.json
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_CHIMCHAR'
- party[0].level: 14 -> 15
- party[0].moves: ['MOVE_EMBER', 'MOVE_TACKLE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_EMBER', 'MOVE_TAUNT', 'MOVE_FURY_SWIPES', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 139

## res/trainers/data/picnicker_siena.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_BIDOOF' -> 'SPECIES_ZIGZAGOON'
- party[0].level: 12 -> 15
- party[0].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_TICKLE', 'MOVE_NONE', 'MOVE_HEADBUTT']
- party[0].iv_scale: 0 -> 116
- party[1].species: 'SPECIES_PACHIRISU' -> 'SPECIES_ELECTRIKE'
- party[1].level: 12 -> 15
- party[1].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_THUNDER_WAVE', 'MOVE_LEER', 'MOVE_HOWL']
- party[1].iv_scale: 0 -> 114

## res/trainers/data/hiker_daniel.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_BALTOY'
- party[0].level: 10 -> 15
- party[0].moves: None -> ['MOVE_PSYBEAM', 'MOVE_ROCK_TOMB', 'MOVE_RAPID_SPIN', 'MOVE_MUD_SLAP']
- party[0].iv_scale: 0 -> 115
- party[1].species: 'SPECIES_GEODUDE' -> 'SPECIES_PHANPY'
- party[1].level: 11 -> 15
- party[1].moves: None -> ['MOVE_GROWL', 'MOVE_DEFENSE_CURL', 'MOVE_ROLLOUT', 'MOVE_TAKE_DOWN']
- party[1].iv_scale: 0 -> 125
- party[2].species: 'SPECIES_GEODUDE' -> 'SPECIES_SANDSHREW'
- party[2].level: 12 -> 15
- party[2].moves: None -> ['MOVE_SCRATCH', 'MOVE_DEFENSE_CURL', 'MOVE_SAND_ATTACK', 'MOVE_POISON_STING']
- party[2].iv_scale: 0 -> 107

## res/trainers/data/hiker_nicholas.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_ONIX' -> 'SPECIES_CUBONE'
- party[0].level: 14 -> 16
- party[0].moves: None -> ['MOVE_TAIL_WHIP', 'MOVE_BONE_CLUB', 'MOVE_HEADBUTT', 'MOVE_LEER']
- party[0].iv_scale: 0 -> 113

## res/trainers/data/battle_girl_kelsey.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOP' -> 'SPECIES_MEDITITE'
- party[0].level: 15 -> 16
- party[0].moves: None -> ['MOVE_MEDITATE', 'MOVE_CONFUSION', 'MOVE_DETECT', 'MOVE_HIDDEN_POWER']
- party[0].iv_scale: 20 -> 92

## res/trainers/data/aroma_lady_elizabeth.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 14 -> 16
- party[0].moves: ['MOVE_GROWTH', 'MOVE_MEGA_DRAIN', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_LEECH_SEED', 'MOVE_MEGA_DRAIN', 'MOVE_STUN_SPORE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 142

## res/trainers/data/fisherman_andrew.json
- party[0].iv_scale: 0 -> 150
- party[1].iv_scale: 0 -> 150
- party[2].iv_scale: 0 -> 150
- party[3].iv_scale: 0 -> 150
- party[4].iv_scale: 0 -> 150
- party[5].species: 'SPECIES_MAGIKARP' -> 'SPECIES_FEEBAS'
- party[5].iv_scale: 0 -> 150

## res/trainers/data/fisherman_joseph.json
- party[0].level: 17 -> 18
- party[0].moves: None -> ['MOVE_WATER_SPORT', 'MOVE_SUPERSONIC', 'MOVE_HORN_ATTACK', 'MOVE_WATER_PULSE']
- party[0].iv_scale: 0 -> 110

## res/trainers/data/fisherman_zachary.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGIKARP' -> 'SPECIES_FINNEON'
- party[0].level: 14 -> 18
- party[0].moves: None -> ['MOVE_WATER_GUN', 'MOVE_ATTRACT', 'MOVE_RAIN_DANCE', 'MOVE_GUST']
- party[0].iv_scale: 0 -> 149
- party[1].species: 'SPECIES_GOLDEEN' -> 'SPECIES_CORPHISH'
- party[1].level: 16 -> 18
- party[1].moves: None -> ['MOVE_BUBBLE', 'MOVE_HARDEN', 'MOVE_VICE_GRIP', 'MOVE_KNOCK_OFF']
- party[1].iv_scale: 0 -> 126
- party[2].species: 'SPECIES_MAGIKARP' -> 'SPECIES_CHINCHOU'
- party[2].level: 14 -> 19
- party[2].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_SHOCK_WAVE', 'MOVE_WATER_GUN', 'MOVE_CONFUSE_RAY']
- party[2].iv_scale: 0 -> 136

## res/trainers/data/cyclist_axel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_QUICK_ATTACK', 'MOVE_THUNDER_SHOCK', 'MOVE_SLAM']
- party[0].iv_scale: 0 -> 138

## res/trainers/data/cyclist_james.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_VULPIX'
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_WILL_O_WISP', 'MOVE_CONFUSE_RAY', 'MOVE_EMBER']
- party[0].iv_scale: 0 -> 136

## res/trainers/data/cyclist_john.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARLY' -> 'SPECIES_PIDGEY'
- party[0].level: 18 -> 19
- party[0].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_WHIRLWIND']
- party[0].iv_scale: 0 -> 153
- party[1].species: 'SPECIES_STARAVIA' -> 'SPECIES_PIDGEOTTO'
- party[1].level: 20 -> 21
- party[1].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_WHIRLWIND']
- party[1].iv_scale: 0 -> 113

## res/trainers/data/cyclist_megan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_WING_ATTACK', 'MOVE_DOUBLE_TEAM', 'MOVE_ENDEAVOR']
- party[0].iv_scale: 0 -> 119

## res/trainers/data/cyclist_nicole.json
- party[0].species: 'SPECIES_STARLY' -> 'SPECIES_IGGLYBUFF'
- party[1].species: 'SPECIES_STARLY' -> 'SPECIES_JIGGLYPUFF'
- party[2].species: 'SPECIES_STARLY' -> 'SPECIES_WIGGLYTUFF'

## res/trainers/data/cyclist_kayla.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PIKACHU' -> 'SPECIES_MAGNEMITE'
- party[0].moves: None -> ['MOVE_THUNDER_SHOCK', 'MOVE_SUPERSONIC', 'MOVE_SONIC_BOOM', 'MOVE_THUNDER_WAVE']
- party[0].iv_scale: 0 -> 191

## res/trainers/data/cyclist_rachel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].moves: None -> ['MOVE_TAIL_WHIP', 'MOVE_EMBER', 'MOVE_FLAME_WHEEL', 'MOVE_STOMP']
- party[0].iv_scale: 0 -> 192
- party[1].species: 'SPECIES_SHINX' -> 'SPECIES_VOLTORB'
- party[1].level: 18 -> 21
- party[1].moves: None -> ['MOVE_SONIC_BOOM', 'MOVE_SHOCK_WAVE', 'MOVE_THUNDER_WAVE', 'MOVE_SCREECH']
- party[1].iv_scale: 0 -> 142

## res/trainers/data/youngster_austin.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 18 -> 24
- party[0].moves: None -> ['MOVE_WATER_GUN', 'MOVE_PURSUIT', 'MOVE_SWIFT', 'MOVE_AQUA_JET']
- party[0].iv_scale: 0 -> 151
- party[1].level: 18 -> 24
- party[1].moves: None -> ['MOVE_CHARGE', 'MOVE_SPARK', 'MOVE_BITE', 'MOVE_ROAR']
- party[1].iv_scale: 0 -> 165
- party[2].level: 21 -> 24
- party[2].moves: None -> ['MOVE_KNOCK_OFF', 'MOVE_QUICK_ATTACK', 'MOVE_DIG', 'MOVE_FAINT_ATTACK']
- party[2].iv_scale: 0 -> 178

## res/trainers/data/camper_anthony.json
- party[0].species: 'SPECIES_CHIMCHAR' -> 'SPECIES_MONFERNO'
- party[0].level: 22 -> 24
- party[0].moves: None -> ['MOVE_TAUNT', 'MOVE_MACH_PUNCH', 'MOVE_FURY_SWIPES', 'MOVE_FLAME_WHEEL']
- party[0].iv_scale: 0 -> 143

## res/trainers/data/picnicker_lauren.json
- party[0].level: 22 -> 24
- party[0].moves: ['MOVE_SPARK', 'MOVE_QUICK_ATTACK', 'MOVE_CHARM', 'MOVE_NONE'] -> ['MOVE_CHARM', 'MOVE_THUNDER_PUNCH', 'MOVE_ENDURE', 'MOVE_HEADBUTT']
- party[0].iv_scale: 0 -> 145

## res/trainers/data/hiker_kevin.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_PHANPY'
- party[0].level: 17 -> 24
- party[0].moves: None -> ['MOVE_TAKE_DOWN', 'MOVE_ROLLOUT', 'MOVE_NATURAL_GIFT', 'MOVE_SLAM']
- party[0].iv_scale: 0 -> 45
- party[1].species: 'SPECIES_GEODUDE' -> 'SPECIES_CUBONE'
- party[1].level: 17 -> 24
- party[1].moves: None -> ['MOVE_LEER', 'MOVE_FOCUS_ENERGY', 'MOVE_BONEMERANG', 'MOVE_RAGE']
- party[1].iv_scale: 0 -> 154
- party[2].level: 19 -> 24
- party[2].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_RAGE', 'MOVE_ROCK_TOMB', 'MOVE_SANDSTORM']
- party[2].iv_scale: 0 -> 163
- party[3].level: 19 -> 24
- party[3].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_MAGNITUDE', 'MOVE_SELFDESTRUCT', 'MOVE_ROLLOUT']
- party[3].iv_scale: 0 -> 184

## res/trainers/data/hiker_justin.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_DIGLETT'
- party[0].level: 20 -> 25
- party[0].moves: None -> ['MOVE_MAGNITUDE', 'MOVE_MUD_SLAP', 'MOVE_DIG', 'MOVE_SUCKER_PUNCH']
- party[0].iv_scale: 0 -> 167
- party[1].level: 20 -> 25
- party[1].moves: None -> ['MOVE_HARDEN', 'MOVE_ROCK_THROW', 'MOVE_BLOCK', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 0 -> 161

## res/trainers/data/battle_girl_helen.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOP' -> 'SPECIES_MAKUHITA'
- party[0].level: 21 -> 26
- party[0].moves: None -> ['MOVE_WHIRLWIND', 'MOVE_KNOCK_OFF', 'MOVE_SMELLING_SALT', 'MOVE_BELLY_DRUM']
- party[0].iv_scale: 20 -> 144
- party[1].species: 'SPECIES_MEDITITE' -> 'SPECIES_RIOLU'
- party[1].level: 21 -> 26
- party[1].moves: None -> ['MOVE_FORCE_PALM', 'MOVE_FEINT', 'MOVE_REVERSAL', 'MOVE_SCREECH']
- party[1].iv_scale: 20 -> 168

## res/trainers/data/hiker_robert.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_NOSEPASS' -> 'SPECIES_GRAVELER'
- party[0].level: 22 -> 28
- party[0].moves: None -> ['MOVE_MAGNITUDE', 'MOVE_SELFDESTRUCT', 'MOVE_ROLLOUT', 'MOVE_ROCK_BLAST']
- party[0].iv_scale: 0 -> 178

## res/trainers/data/hiker_alexander.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_GRAVELER' -> 'SPECIES_GOLEM'
- party[0].level: 38 -> 45
- party[0].moves: None -> ['MOVE_ROCK_BLAST', 'MOVE_EARTHQUAKE', 'MOVE_EXPLOSION', 'MOVE_DOUBLE_EDGE']
- party[0].iv_scale: 0 -> 157
- party[1].level: 40 -> 45
- party[1].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_ROCK_SLIDE', 'MOVE_SANDSTORM', 'MOVE_REST']
- party[1].iv_scale: 0 -> 209

## res/trainers/data/hiker_jonathan.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_ONIX' -> 'SPECIES_NIDORINO'
- party[0].level: 22 -> 27
- party[0].moves: None -> ['MOVE_DOUBLE_KICK', 'MOVE_POISON_STING', 'MOVE_DIG', 'MOVE_HEADBUTT']
- party[0].iv_scale: 0 -> 169

## res/trainers/data/black_belt_kyle.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOP' -> 'SPECIES_MACHOKE'
- party[0].level: 23 -> 29
- party[0].moves: None -> ['MOVE_FORESIGHT', 'MOVE_SEISMIC_TOSS', 'MOVE_REVENGE', 'MOVE_VITAL_THROW']
- party[0].iv_scale: 30 -> 193

## res/trainers/data/fisherman_cody.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_BARBOACH' -> 'SPECIES_WHISCASH'
- party[0].level: 33 -> 44
- party[0].moves: None -> ['MOVE_MAGNITUDE', 'MOVE_REST', 'MOVE_SNORE', 'MOVE_AQUA_TAIL']
- party[0].iv_scale: 0 -> 202
- party[1].level: 33 -> 44
- party[1].moves: None -> ['MOVE_AQUA_TAIL', 'MOVE_RAIN_DANCE', 'MOVE_CRUNCH', 'MOVE_DRAGON_DANCE']
- party[1].iv_scale: 0 -> 182

## res/trainers/data/aroma_lady_hannah.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 18 -> 27
- party[0].moves: None -> ['MOVE_LEECH_SEED', 'MOVE_MAGICAL_LEAF', 'MOVE_GRASS_WHISTLE', 'MOVE_GIGA_DRAIN']
- party[0].iv_scale: 0 -> 150
- party[1].species: 'SPECIES_COMBEE' -> 'SPECIES_JUMPLUFF'
- party[1].level: 22 -> 27
- party[1].moves: None -> ['MOVE_STUN_SPORE', 'MOVE_SLEEP_POWDER', 'MOVE_BULLET_SEED', 'MOVE_LEECH_SEED']
- party[1].iv_scale: 0 -> 174

## res/trainers/data/artist_william.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 20 -> 26
- party[0].moves: None -> ['MOVE_MIMIC', 'MOVE_LIGHT_SCREEN', 'MOVE_REFLECT', 'MOVE_PSYBEAM']
- party[0].iv_scale: 0 -> 132
- party[1].species: 'SPECIES_BONSLY' -> 'SPECIES_SMEARGLE'
- party[1].level: 20 -> 26
- party[1].moves: None -> ['MOVE_FLAME_WHEEL', 'MOVE_AQUA_JET', 'MOVE_BULLET_SEED', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 152

## res/trainers/data/breeder_albert.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 20 -> 26
- party[0].moves: None -> ['MOVE_WATER_SPORT', 'MOVE_STUN_SPORE', 'MOVE_GIGA_DRAIN', 'MOVE_SWIFT']
- party[0].iv_scale: 0 -> 204
- party[1].level: 20 -> 26
- party[1].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_MIMIC', 'MOVE_BLOCK', 'MOVE_FAINT_ATTACK']
- party[1].iv_scale: 0 -> 192
- party[2].level: 20 -> 26
- party[2].moves: None -> ['MOVE_TAIL_WHIP', 'MOVE_THUNDER_WAVE', 'MOVE_SWEET_KISS', 'MOVE_VOLT_TACKLE']
- party[2].iv_scale: 0 -> 203
- party[3].level: 20 -> 26
- party[3].moves: None -> ['MOVE_HEADBUTT', 'MOVE_DIG', 'MOVE_YAWN', 'MOVE_QUICK_ATTACK']
- party[3].iv_scale: 0 -> 207

## res/trainers/data/breeder_jennifer.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BUDEW' -> 'SPECIES_RIOLU'
- party[0].level: 20 -> 26
- party[0].moves: None -> ['MOVE_FORCE_PALM', 'MOVE_FEINT', 'MOVE_REVERSAL', 'MOVE_SCREECH']
- party[0].iv_scale: 0 -> 209
- party[1].species: 'SPECIES_MIME_JR' -> 'SPECIES_SMOOCHUM'
- party[1].level: 20 -> 26
- party[1].moves: None -> ['MOVE_CONFUSION', 'MOVE_SING', 'MOVE_MEAN_LOOK', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 0 -> 198
- party[2].level: 20 -> 26
- party[2].moves: None -> ['MOVE_SING', 'MOVE_SWEET_KISS', 'MOVE_COPYCAT', 'MOVE_MAGICAL_LEAF']
- party[2].iv_scale: 0 -> 210
- party[3].level: 20 -> 26
- party[3].moves: None -> ['MOVE_HEADBUTT', 'MOVE_DIG', 'MOVE_YAWN', 'MOVE_QUICK_ATTACK']
- party[3].iv_scale: 0 -> 202

## res/trainers/data/cowgirl_shelley.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_MILTANK'
- party[0].level: 23 -> 30
- party[0].moves: None -> ['MOVE_BIDE', 'MOVE_MILK_DRINK', 'MOVE_BODY_SLAM', 'MOVE_ZEN_HEADBUTT']
- party[0].iv_scale: 0 -> 232

## res/trainers/data/jogger_richard.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_LUXIO' -> 'SPECIES_ELECTABUZZ'
- party[0].level: 23 -> 30
- party[0].moves: None -> ['MOVE_ICE_PUNCH', 'MOVE_LOW_KICK', 'MOVE_LIGHT_SCREEN', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 0 -> 177

## res/trainers/data/poke_kid_danielle.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PICHU' -> 'SPECIES_CLEFABLE'
- party[0].level: 22 -> 30
- party[0].moves: None -> ['MOVE_SING', 'MOVE_DOUBLE_SLAP', 'MOVE_MINIMIZE', 'MOVE_METRONOME']
- party[0].iv_scale: 0 -> 203

## res/trainers/data/young_couple_ty_and_sue.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BUNEARY' -> 'SPECIES_LOPUNNY'
- party[0].level: 23 -> 31
- party[0].moves: ['MOVE_FORESIGHT', 'MOVE_JUMP_KICK', 'MOVE_QUICK_ATTACK', 'MOVE_DEFENSE_CURL'] -> ['MOVE_RETURN', 'MOVE_JUMP_KICK', 'MOVE_QUICK_ATTACK', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 0 -> 200
- party[1].species: 'SPECIES_BUIZEL' -> 'SPECIES_FLOATZEL'
- party[1].level: 23 -> 31
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_SWIFT', 'MOVE_PURSUIT', 'MOVE_SONIC_BOOM'] -> ['MOVE_AQUA_JET', 'MOVE_ICE_PUNCH', 'MOVE_PURSUIT', 'MOVE_WATERFALL']
- party[1].iv_scale: 0 -> 200

## res/trainers/data/breeder_kahlil.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 23 -> 31
- party[0].moves: None -> ['MOVE_CROSS_CHOP', 'MOVE_ICE_PUNCH', 'MOVE_LIGHT_SCREEN', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 0 -> 235
- party[1].species: 'SPECIES_HAPPINY' -> 'SPECIES_MAGBY'
- party[1].level: 23 -> 31
- party[1].moves: None -> ['MOVE_FLARE_BLITZ', 'MOVE_CROSS_CHOP', 'MOVE_MACH_PUNCH', 'MOVE_FIRE_PUNCH']
- party[1].iv_scale: 0 -> 234

## res/trainers/data/breeder_amber.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGBY' -> 'SPECIES_HAPPINY'
- party[0].level: 23 -> 31
- party[0].moves: None -> ['MOVE_COUNTER', 'MOVE_COPYCAT', 'MOVE_METRONOME', 'MOVE_SWEET_KISS']
- party[0].iv_scale: 0 -> 208
- party[1].level: 23 -> 31
- party[1].moves: None -> ['MOVE_YAWN', 'MOVE_EXTRASENSORY', 'MOVE_MIRROR_MOVE', 'MOVE_METRONOME']
- party[1].iv_scale: 0 -> 255

## res/trainers/data/dummy_058.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_058.json
- class: 'TRAINER_CLASS_COWGIRL' -> 'TRAINER_CLASS_DP_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_059.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_059.json
- class: 'TRAINER_CLASS_JOGGER' -> 'TRAINER_CLASS_DP_PLAYER_MALE_2'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_060.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_060.json
- class: 'TRAINER_CLASS_POKEFAN_MALE' -> 'TRAINER_CLASS_DP_PLAYER_FEMALE_2'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_061.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_061.json
- class: 'TRAINER_CLASS_POKEFAN_FEMALE' -> 'TRAINER_CLASS_DP_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/twins_teri_and_tia.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PIKACHU' -> 'SPECIES_GLOOM'
- party[0].level: 23 -> 32
- party[0].moves: None -> ['MOVE_STUN_SPORE', 'MOVE_SLEEP_POWDER', 'MOVE_GIGA_DRAIN', 'MOVE_SYNTHESIS']
- party[0].iv_scale: 0 -> 191
- party[1].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_WEEPINBELL'
- party[1].level: 23 -> 32
- party[1].moves: None -> ['MOVE_STUN_SPORE', 'MOVE_KNOCK_OFF', 'MOVE_SUCKER_PUNCH', 'MOVE_SEED_BOMB']
- party[1].iv_scale: 0 -> 209

## res/trainers/data/ace_trainer_ernest.json
- party[0].species: 'SPECIES_SCYTHER' -> 'SPECIES_SCIZOR'
- party[0].level: 32 -> 41
- party[0].moves: ['MOVE_SLASH', 'MOVE_WING_ATTACK', 'MOVE_PURSUIT', 'MOVE_QUICK_ATTACK'] -> ['MOVE_BULLET_PUNCH', 'MOVE_NIGHT_SLASH', 'MOVE_IRON_HEAD', 'MOVE_X_SCISSOR']
- party[0].iv_scale: 50 -> 238
- party[1].level: 31 -> 41
- party[1].moves: ['MOVE_THUNDER_WAVE', 'MOVE_ROCK_SLIDE', 'MOVE_MAGNET_BOMB', 'MOVE_IRON_DEFENSE'] -> ['MOVE_EARTH_POWER', 'MOVE_THUNDER_WAVE', 'MOVE_FLASH_CANNON', 'MOVE_THUNDERBOLT']
- party[1].iv_scale: 50 -> 239
- party[2].species: 'SPECIES_LUXIO' -> 'SPECIES_AMPHAROS'
- party[2].level: 34 -> 41
- party[2].moves: ['MOVE_THUNDERBOLT', 'MOVE_CRUNCH', 'MOVE_SWAGGER', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_OUTRAGE', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 50 -> 244

## res/trainers/data/ace_trainer_alyssa.json
- party[0].species: 'SPECIES_AIPOM' -> 'SPECIES_AMBIPOM'
- party[0].level: 32 -> 42
- party[0].moves: ['MOVE_SWIFT', 'MOVE_WATER_PULSE', 'MOVE_SHOCK_WAVE', 'MOVE_AERIAL_ACE'] -> ['MOVE_FAKE_OUT', 'MOVE_FIRE_PUNCH', 'MOVE_LOW_KICK', 'MOVE_AERIAL_ACE']
- party[0].iv_scale: 50 -> 237
- party[1].level: 32 -> 42
- party[1].moves: ['MOVE_DOUBLE_HIT', 'MOVE_PSYBEAM', 'MOVE_ASSURANCE', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_HEADBUTT', 'MOVE_ZEN_HEADBUTT', 'MOVE_SUCKER_PUNCH', 'MOVE_LIGHT_SCREEN']
- party[1].iv_scale: 50 -> 248
- party[2].species: 'SPECIES_GROTLE' -> 'SPECIES_TORTERRA'
- party[2].level: 33 -> 42
- party[2].moves: ['MOVE_MEGA_DRAIN', 'MOVE_BITE', 'MOVE_CURSE', 'MOVE_NONE'] -> ['MOVE_ENERGY_BALL', 'MOVE_EARTH_POWER', 'MOVE_GIGA_DRAIN', 'MOVE_LEECH_SEED']
- party[2].iv_scale: 50 -> 254

## res/trainers/data/veteran_brian.json
- party[0].species: 'SPECIES_TANGELA' -> 'SPECIES_TANGROWTH'
- party[0].level: 32 -> 43
- party[0].moves: ['MOVE_INGRAIN', 'MOVE_GIGA_DRAIN', 'MOVE_ANCIENT_POWER', 'MOVE_TOXIC'] -> ['MOVE_ANCIENT_POWER', 'MOVE_ENERGY_BALL', 'MOVE_FOCUS_BLAST', 'MOVE_SLEEP_POWDER']
- party[0].iv_scale: 100 -> 218
- party[1].species: 'SPECIES_PONYTA' -> 'SPECIES_MAGCARGO'
- party[1].level: 32 -> 43
- party[1].moves: ['MOVE_FIRE_SPIN', 'MOVE_STOMP', 'MOVE_TAKE_DOWN', 'MOVE_NONE'] -> ['MOVE_LAVA_PLUME', 'MOVE_ANCIENT_POWER', 'MOVE_EARTH_POWER', 'MOVE_WILL_O_WISP']
- party[1].iv_scale: 100 -> 210
- party[2].species: 'SPECIES_BUIZEL' -> 'SPECIES_MILOTIC'
- party[2].level: 32 -> 43
- party[2].moves: ['MOVE_AQUA_JET', 'MOVE_WHIRLPOOL', 'MOVE_PURSUIT', 'MOVE_QUICK_ATTACK'] -> ['MOVE_DRAGON_PULSE', 'MOVE_REST', 'MOVE_HYDRO_PUMP', 'MOVE_CONFUSE_RAY']
- party[2].iv_scale: 100 -> 249

## res/trainers/data/black_belt_adam.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOKE' -> 'SPECIES_PRIMEAPE'
- party[0].level: 34 -> 42
- party[0].moves: None -> ['MOVE_OUTRAGE', 'MOVE_POISON_JAB', 'MOVE_ICE_PUNCH', 'MOVE_CLOSE_COMBAT']
- party[0].iv_scale: 30 -> 249

## res/trainers/data/ninja_boy_joel.json
- party size changed (4 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ninja_boy_joel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/ninja_boy_nathan.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ninja_boy_nathan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/ninja_boy_davido.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 33 -> 41
- party[0].moves: None -> ['MOVE_SIGNAL_BEAM', 'MOVE_PSYCHIC', 'MOVE_ENERGY_BALL', 'MOVE_AIR_SLASH']
- party[0].iv_scale: 0 -> 252

## res/trainers/data/dragon_tamer_patrick.json
- party[0].species: 'SPECIES_GIBLE' -> 'SPECIES_ALTARIA'
- party[0].level: 34 -> 43
- party[0].moves: None -> ['MOVE_OUTRAGE', 'MOVE_SKY_ATTACK', 'MOVE_EARTHQUAKE', 'MOVE_DRAGON_DANCE']
- party[0].iv_scale: 50 -> 253

## res/trainers/data/bird_keeper_brianna.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_PIDGEOT'
- party[0].level: 31 -> 42
- party[0].moves: None -> ['MOVE_BRAVE_BIRD', 'MOVE_STEEL_WING', 'MOVE_ROOST', 'MOVE_TAILWIND']
- party[0].iv_scale: 50 -> 245
- party[1].species: 'SPECIES_NOCTOWL' -> 'SPECIES_SKARMORY'
- party[1].level: 33 -> 42
- party[1].moves: None -> ['MOVE_DRILL_PECK', 'MOVE_STEEL_WING', 'MOVE_ROCK_TOMB', 'MOVE_WHIRLWIND']
- party[1].iv_scale: 50 -> 255

## res/trainers/data/double_team_zac_and_jen.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 36 -> 42
- party[0].moves: None -> ['MOVE_ICE_FANG', 'MOVE_WATERFALL', 'MOVE_STONE_EDGE', 'MOVE_OUTRAGE']
- party[0].iv_scale: 50 -> 214
- party[1].level: 36 -> 42
- party[1].moves: None -> ['MOVE_VOLT_TACKLE', 'MOVE_RAIN_DANCE', 'MOVE_FAKE_OUT', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 50 -> 254

## res/trainers/data/bird_keeper_alexandra.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARLY' -> 'SPECIES_SWABLU'
- party[0].level: 17 -> 19
- party[0].moves: None -> ['MOVE_ASTONISH', 'MOVE_SING', 'MOVE_FURY_ATTACK', 'MOVE_SAFEGUARD']
- party[0].iv_scale: 20 -> 111
- party[1].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_STARAVIA'
- party[1].level: 17 -> 20
- party[1].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_WING_ATTACK', 'MOVE_DOUBLE_TEAM', 'MOVE_ENDEAVOR']
- party[1].iv_scale: 20 -> 159

## res/trainers/data/ninja_boy_zach.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_SHROOMISH'
- party[0].level: 14 -> 19
- party[0].moves: None -> ['MOVE_TACKLE', 'MOVE_STUN_SPORE', 'MOVE_LEECH_SEED', 'MOVE_MEGA_DRAIN']
- party[0].iv_scale: 0 -> 138
- party[1].species: 'SPECIES_ZUBAT' -> 'SPECIES_PARAS'
- party[1].level: 14 -> 19
- party[1].moves: None -> ['MOVE_STUN_SPORE', 'MOVE_POISON_POWDER', 'MOVE_BUG_BITE', 'MOVE_SPORE']
- party[1].iv_scale: 0 -> 153
- party[2].species: 'SPECIES_ZUBAT' -> 'SPECIES_SEEDOT'
- party[2].level: 14 -> 19
- party[2].moves: None -> ['MOVE_LEECH_SEED', 'MOVE_HARDEN', 'MOVE_BULLET_SEED', 'MOVE_NATURE_POWER']
- party[2].iv_scale: 0 -> 142

## res/trainers/data/rich_boy_jason.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PRINPLUP' -> 'SPECIES_FERALIGATR'
- party[0].level: 27 -> 37
- party[0].moves: None -> ['MOVE_WATERFALL', 'MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_PUNCH']
- party[0].iv_scale: 0 -> 226

## res/trainers/data/lady_melissa.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CHERUBI' -> 'SPECIES_SCEPTILE'
- party[0].level: 27 -> 37
- party[0].moves: None -> ['MOVE_NIGHT_SLASH', 'MOVE_EARTHQUAKE', 'MOVE_LEAF_BLADE', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 0 -> 230

## res/trainers/data/gentleman_jeremy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 27 -> 37
- party[0].moves: None -> ['MOVE_TAUNT', 'MOVE_MIMIC', 'MOVE_ROOST', 'MOVE_UPROAR']
- party[0].iv_scale: 0 -> 243

## res/trainers/data/socialite_reina.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ROSELIA' -> 'SPECIES_JUMPLUFF'
- party[0].level: 27 -> 37
- party[0].moves: None -> ['MOVE_SEED_BOMB', 'MOVE_AERIAL_ACE', 'MOVE_SLEEP_POWDER', 'MOVE_U_TURN']
- party[0].iv_scale: 0 -> 235

## res/trainers/data/policeman_bobby.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_SWELLOW'
- party[0].level: 24 -> 34
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_AERIAL_ACE', 'MOVE_DOUBLE_TEAM', 'MOVE_ENDEAVOR']
- party[0].iv_scale: 0 -> 249
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_ARCANINE'
- party[1].level: 26 -> 34
- party[1].moves: None -> ['MOVE_CRUNCH', 'MOVE_ROAR', 'MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG']
- party[1].iv_scale: 0 -> 238

## res/trainers/data/policeman_alex.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_PIDGEOTTO'
- party[0].level: 25 -> 35
- party[0].moves: None -> ['MOVE_WHIRLWIND', 'MOVE_AERIAL_ACE', 'MOVE_FEATHER_DANCE', 'MOVE_AGILITY']
- party[0].iv_scale: 0 -> 249
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_NINETALES'
- party[1].level: 25 -> 35
- party[1].moves: None -> ['MOVE_FLAMETHROWER', 'MOVE_HIDDEN_POWER', 'MOVE_CONFUSE_RAY', 'MOVE_WILL_O_WISP']
- party[1].iv_scale: 0 -> 244

## res/trainers/data/policeman_dylan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_DODRIO'
- party[0].level: 26 -> 36
- party[0].item: None -> 'ITEM_NONE'
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_BRAVE_BIRD', 'MOVE_ACUPRESSURE', 'MOVE_KNOCK_OFF']
- party[0].iv_scale: 0 -> 229
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_MAROWAK'
- party[1].level: 24 -> 36
- party[1].item: None -> 'ITEM_THICK_CLUB'
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_IRON_HEAD', 'MOVE_THUNDER_PUNCH', 'MOVE_LOW_KICK']
- party[1].iv_scale: 0 -> 236

## res/trainers/data/fisherman_juan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GYARADOS' -> 'SPECIES_GOREBYSS'
- party[0].level: 29 -> 36
- party[0].moves: None -> ['MOVE_AMNESIA', 'MOVE_AQUA_RING', 'MOVE_PSYCHIC', 'MOVE_SURF']
- party[0].iv_scale: 0 -> 246

## res/trainers/data/fisherman_josh.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLDEEN' -> 'SPECIES_CLAMPERL'
- party[0].level: 27 -> 35
- party[0].item: None -> 'ITEM_DEEPSEATOOTH'
- party[0].moves: None -> ['MOVE_BLIZZARD', 'MOVE_SURF', 'MOVE_CONFUSE_RAY', 'MOVE_HIDDEN_POWER']
- party[0].iv_scale: 0 -> 248
- party[1].species: 'SPECIES_GOLDEEN' -> 'SPECIES_HUNTAIL'
- party[1].level: 27 -> 36
- party[1].item: None -> 'ITEM_NONE'
- party[1].moves: None -> ['MOVE_SCARY_FACE', 'MOVE_ICE_FANG', 'MOVE_AQUA_TAIL', 'MOVE_SUCKER_PUNCH']
- party[1].iv_scale: 0 -> 244

## res/trainers/data/fisherman_travis.json
- party size changed (4 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/fisherman_travis.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/ranger_jeffrey.json
- party[0].species: 'SPECIES_MONFERNO' -> 'SPECIES_TAUROS'
- party[0].level: 31 -> 39
- party[0].moves: None -> ['MOVE_REST', 'MOVE_HEADBUTT', 'MOVE_ZEN_HEADBUTT', 'MOVE_EARTHQUAKE']
- party[0].iv_scale: 50 -> 231

## res/trainers/data/ranger_allison.json
- party[0].species: 'SPECIES_MARILL' -> 'SPECIES_KANGASKHAN'
- party[0].level: 29 -> 39
- party[0].moves: None -> ['MOVE_DIZZY_PUNCH', 'MOVE_CRUNCH', 'MOVE_ENDURE', 'MOVE_OUTRAGE']
- party[0].iv_scale: 50 -> 206
- party[1].level: 29 -> 39
- party[1].moves: None -> ['MOVE_RAZOR_LEAF', 'MOVE_QUICK_ATTACK', 'MOVE_SYNTHESIS', 'MOVE_MAGICAL_LEAF']
- party[1].iv_scale: 50 -> 249

## res/trainers/data/scientist_stefano.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_KADABRA' -> 'SPECIES_MUK'
- party[0].level: 30 -> 38
- party[0].moves: ['MOVE_PSYBEAM', 'MOVE_DISABLE', 'MOVE_KINESIS', 'MOVE_ICE_PUNCH'] -> ['MOVE_GUNK_SHOT', 'MOVE_SHADOW_PUNCH', 'MOVE_SHADOW_SNEAK', 'MOVE_ICE_PUNCH']
- party[0].iv_scale: 0 -> 250

## res/trainers/data/policeman_caleb.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_HONCHKROW'
- party[0].level: 23 -> 35
- party[0].moves: None -> ['MOVE_HAZE', 'MOVE_AERIAL_ACE', 'MOVE_SWAGGER', 'MOVE_SUCKER_PUNCH']
- party[0].iv_scale: 0 -> 231
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_SANDSLASH'
- party[1].level: 27 -> 35
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_CRUSH_CLAW', 'MOVE_POISON_JAB', 'MOVE_BRICK_BREAK']
- party[1].iv_scale: 0 -> 254

## res/trainers/data/swimmer_sheltin.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 32 -> 43
- party[0].moves: None -> ['MOVE_ICE_FANG', 'MOVE_AQUA_TAIL', 'MOVE_BOUNCE', 'MOVE_HEADBUTT']
- party[0].iv_scale: 0 -> 250
- party[1].species: 'SPECIES_GYARADOS' -> 'SPECIES_LANTURN'
- party[1].level: 32 -> 43
- party[1].moves: None -> ['MOVE_DISCHARGE', 'MOVE_SURF', 'MOVE_SIGNAL_BEAM', 'MOVE_CONFUSE_RAY']
- party[1].iv_scale: 0 -> 254
- party[2].species: 'SPECIES_GYARADOS' -> 'SPECIES_SHARPEDO'
- party[2].level: 32 -> 43
- party[2].moves: None -> ['MOVE_CRUNCH', 'MOVE_SLASH', 'MOVE_AQUA_JET', 'MOVE_TAUNT']
- party[2].iv_scale: 0 -> 255

## res/trainers/data/swimmer_evan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLDUCK' -> 'SPECIES_POLITOED'
- party[0].level: 32 -> 44
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_PERISH_SONG', 'MOVE_FOCUS_BLAST', 'MOVE_RAIN_DANCE']
- party[0].iv_scale: 0 -> 245
- party[1].species: 'SPECIES_GOLDUCK' -> 'SPECIES_MANTINE'
- party[1].level: 34 -> 44
- party[1].moves: None -> ['MOVE_WATER_PULSE', 'MOVE_SIGNAL_BEAM', 'MOVE_CONFUSE_RAY', 'MOVE_AIR_CUTTER']
- party[1].iv_scale: 0 -> 237

## res/trainers/data/swimmer_haley.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PSYDUCK' -> 'SPECIES_GOLDUCK'
- party[0].level: 31 -> 43
- party[0].moves: None -> ['MOVE_AQUA_JET', 'MOVE_ZEN_HEADBUTT', 'MOVE_WATERFALL', 'MOVE_ICE_PUNCH']
- party[0].iv_scale: 0 -> 251
- party[1].species: 'SPECIES_AZUMARILL' -> 'SPECIES_SLOWBRO'
- party[1].level: 35 -> 43
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_SHADOW_BALL', 'MOVE_SLACK_OFF']
- party[1].iv_scale: 0 -> 253

## res/trainers/data/swimmer_mary.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_FINNEON' -> 'SPECIES_LUMINEON'
- party[0].level: 33 -> 44
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_BLIZZARD', 'MOVE_AQUA_RING', 'MOVE_TAILWIND']
- party[0].iv_scale: 0 -> 221
- party[1].species: 'SPECIES_PELIPPER' -> 'SPECIES_LAPRAS'
- party[1].level: 33 -> 44
- party[1].moves: None -> ['MOVE_PERISH_SONG', 'MOVE_ICE_BEAM', 'MOVE_BRINE', 'MOVE_SAFEGUARD']
- party[1].iv_scale: 0 -> 227

## res/trainers/data/tuber_jared.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SHELLOS' -> 'SPECIES_GASTRODON'
- party[0].form: 1 -> 0
- party[0].level: 25 -> 36
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_HIDDEN_POWER', 'MOVE_RAIN_DANCE', 'MOVE_EARTH_POWER']
- party[0].iv_scale: 0 -> 248
- party[1].species: 'SPECIES_SHELLOS' -> 'SPECIES_LUVDISC'
- party[1].form: 1 -> 0
- party[1].level: 25 -> 36
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_SWEET_KISS', 'MOVE_HIDDEN_POWER']
- party[1].iv_scale: 0 -> 158
- party[2].species: 'SPECIES_SHELLOS' -> 'SPECIES_GASTRODON'
- party[2].form: 0 -> 1
- party[2].level: 26 -> 36
- party[2].moves: None -> ['MOVE_WATERFALL', 'MOVE_STONE_EDGE', 'MOVE_RAIN_DANCE', 'MOVE_EARTHQUAKE']
- party[2].iv_scale: 0 -> 209

## res/trainers/data/tuber_chelsea.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MARILL' -> 'SPECIES_AZUMARILL'
- party[0].level: 28 -> 37
- party[0].moves: None -> ['MOVE_WATERFALL', 'MOVE_ICE_PUNCH', 'MOVE_SUPERPOWER', 'MOVE_AQUA_JET']
- party[0].iv_scale: 0 -> 253

## res/trainers/data/sailor_paul.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_TENTACOOL' -> 'SPECIES_TENTACRUEL'
- party[0].level: 31 -> 44
- party[0].moves: None -> ['MOVE_WATERFALL', 'MOVE_ACUPRESSURE', 'MOVE_POISON_JAB', 'MOVE_SCREECH']
- party[0].iv_scale: 0 -> 249
- party[1].level: 31 -> 44
- party[1].moves: None -> ['MOVE_STOCKPILE', 'MOVE_SWALLOW', 'MOVE_SPIT_UP', 'MOVE_FLY']
- party[1].iv_scale: 0 -> 250
- party[2].species: 'SPECIES_MACHOKE' -> 'SPECIES_KINGLER'
- party[2].level: 34 -> 44
- party[2].moves: None -> ['MOVE_GUILLOTINE', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']
- party[2].iv_scale: 0 -> 254

## res/trainers/data/fisherman_kenneth.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 25 -> 36
- party[0].moves: None -> ['MOVE_AURORA_BEAM', 'MOVE_FLAMETHROWER', 'MOVE_WATER_PULSE', 'MOVE_SIGNAL_BEAM']
- party[0].iv_scale: 0 -> 230
- party[1].species: 'SPECIES_REMORAID' -> 'SPECIES_WAILMER'
- party[1].level: 25 -> 36
- party[1].moves: None -> ['MOVE_RAIN_DANCE', 'MOVE_ICE_BEAM', 'MOVE_SURF', 'MOVE_WATER_SPOUT']
- party[1].iv_scale: 0 -> 235
- party[2].level: 28 -> 36
- party[2].moves: None -> ['MOVE_HEADBUTT', 'MOVE_DRAGON_DANCE', 'MOVE_ICE_FANG', 'MOVE_AQUA_TAIL']
- party[2].iv_scale: 0 -> 234

## res/trainers/data/ruin_maniac_bryan.json
- party[0].species: 'SPECIES_BRONZOR' -> 'SPECIES_AERODACTYL'
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_AERIAL_ACE', 'MOVE_STONE_EDGE', 'MOVE_THUNDER_FANG', 'MOVE_TAILWIND']
- party[0].iv_scale: 0 -> 251
- party[1].species: 'SPECIES_CRANIDOS' -> 'SPECIES_RAMPARDOS'
- party[1].level: 26 -> 33
- party[1].moves: None -> ['MOVE_HEADBUTT', 'MOVE_STONE_EDGE', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[1].iv_scale: 0 -> 245

## res/trainers/data/ruin_maniac_ronald.json
- party[0].species: 'SPECIES_SHIELDON' -> 'SPECIES_DUGTRIO'
- party[0].level: 27 -> 35
- party[0].moves: None -> ['MOVE_NIGHT_SLASH', 'MOVE_DIG', 'MOVE_AERIAL_ACE', 'MOVE_STONE_EDGE']
- party[0].iv_scale: 0 -> 246

## res/trainers/data/psychic_mitchell.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_DUSKULL' -> 'SPECIES_HYPNO'
- party[0].level: 26 -> 34
- party[0].moves: None -> ['MOVE_PSYCHO_CUT', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_DRAIN_PUNCH']
- party[0].iv_scale: 0 -> 249
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_CHIMECHO'
- party[1].level: 26 -> 34
- party[1].moves: None -> ['MOVE_PSYCHIC', 'MOVE_SHADOW_BALL', 'MOVE_ENERGY_BALL', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 0 -> 245

## res/trainers/data/psychic_abigail.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CHINGLING' -> 'SPECIES_WOBBUFFET'
- party[0].level: 23 -> 34
- party[0].moves: None -> ['MOVE_COUNTER', 'MOVE_MIRROR_COAT', 'MOVE_SAFEGUARD', 'MOVE_DESTINY_BOND']
- party[0].iv_scale: 0 -> 249
- party[1].species: 'SPECIES_DRIFLOON' -> 'SPECIES_BELDUM'
- party[1].level: 25 -> 34
- party[1].moves: None -> ['MOVE_IRON_HEAD', 'MOVE_ZEN_HEADBUTT', 'MOVE_NONE', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 251
- party[2].species: 'SPECIES_KIRLIA' -> 'SPECIES_EXEGGUTOR'
- party[2].level: 27 -> 34
- party[2].moves: None -> ['MOVE_ENERGY_BALL', 'MOVE_PSYCHIC', 'MOVE_ANCIENT_POWER', 'MOVE_SYNTHESIS']
- party[2].iv_scale: 0 -> 254

## res/trainers/data/pi_carlos.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_RISKY'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLDEEN' -> 'SPECIES_SEAKING'
- party[0].level: 30 -> 36
- party[0].moves: ['MOVE_HORN_DRILL', 'MOVE_FLAIL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HORN_DRILL', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 50 -> 241

## res/trainers/data/black_belt_gregory.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 23 -> 34
- party[0].moves: None -> ['MOVE_BULLET_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_LOW_KICK', 'MOVE_WAKE_UP_SLAP']
- party[0].iv_scale: 30 -> 240
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_BRELOOM'
- party[1].level: 23 -> 34
- party[1].moves: None -> ['MOVE_MACH_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_THUNDER_PUNCH', 'MOVE_SKY_UPPERCUT']
- party[1].iv_scale: 30 -> 191
- party[2].species: 'SPECIES_MACHOP' -> 'SPECIES_HITMONCHAN'
- party[2].level: 23 -> 34
- party[2].moves: None -> ['MOVE_MACH_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_FIRE_PUNCH']
- party[2].iv_scale: 30 -> 199

## res/trainers/data/black_belt_derek.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_CROAGUNK' -> 'SPECIES_TYROGUE'
- party[0].level: 26 -> 34
- party[0].moves: None -> ['MOVE_BRICK_BREAK', 'MOVE_BULLET_PUNCH', 'MOVE_FAKE_OUT', 'MOVE_MACH_PUNCH']
- party[0].iv_scale: 30 -> 205

## res/trainers/data/black_belt_nathaniel.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 21 -> 34
- party[0].moves: None -> ['MOVE_POISON_JAB', 'MOVE_BULLET_PUNCH', 'MOVE_LOW_KICK', 'MOVE_SUCKER_PUNCH']
- party[1].level: 24 -> 34
- party[1].moves: None -> ['MOVE_THUNDER_PUNCH', 'MOVE_PSYCHO_CUT', 'MOVE_FIRE_PUNCH', 'MOVE_HI_JUMP_KICK']
- party[1].iv_scale: 30 -> 253
- party[2].species: 'SPECIES_MACHOP' -> 'SPECIES_HITMONLEE'
- party[2].level: 24 -> 34
- party[2].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_BULLET_PUNCH', 'MOVE_HI_JUMP_KICK', 'MOVE_FAKE_OUT']
- party[2].iv_scale: 30 -> 198

## res/trainers/data/jogger_scott.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARAVIA' -> 'SPECIES_FARFETCHD'
- party[0].level: 25 -> 34
- party[0].moves: None -> ['MOVE_LEAF_BLADE', 'MOVE_AERIAL_ACE', 'MOVE_POISON_JAB', 'MOVE_NIGHT_SLASH']
- party[0].iv_scale: 0 -> 134

## res/trainers/data/ace_trainer_blake.json
- party[0].level: 39 -> 48
- party[0].iv_scale: 50 -> 251
- party[1].level: 40 -> 48
- party[1].iv_scale: 50 -> 235

## res/trainers/data/ace_trainer_garrett.json
- party[0].level: 37 -> 47
- party[0].moves: ['MOVE_PSYBEAM', 'MOVE_MIMIC', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN']
- party[0].iv_scale: 50 -> 236
- party[1].species: 'SPECIES_DUSCLOPS' -> 'SPECIES_DUSKNOIR'
- party[1].level: 39 -> 47
- party[1].iv_scale: 50 -> 234
- party[2].species: 'SPECIES_SCYTHER' -> 'SPECIES_SCIZOR'
- party[2].level: 39 -> 47
- party[2].moves: ['MOVE_SLASH', 'MOVE_X_SCISSOR', 'MOVE_QUICK_ATTACK', 'MOVE_FURY_CUTTER'] -> ['MOVE_SLASH', 'MOVE_X_SCISSOR', 'MOVE_BULLET_PUNCH', 'MOVE_NIGHT_SLASH']
- party[2].iv_scale: 50 -> 255

## res/trainers/data/ace_trainer_laura.json
- party[0].level: 42 -> 50
- party[0].moves: ['MOVE_AIR_SLASH', 'MOVE_BODY_SLAM', 'MOVE_MAGICAL_LEAF', 'MOVE_SWEET_SCENT'] -> ['MOVE_AIR_SLASH', 'MOVE_LEAF_STORM', 'MOVE_OMINOUS_WIND', 'MOVE_TAILWIND']
- party[0].iv_scale: 50 -> 236

## res/trainers/data/ace_trainer_maria.json
- party[0].level: 38 -> 47
- party[0].moves: ['MOVE_WATER_PULSE', 'MOVE_CONFUSION', 'MOVE_DISABLE', 'MOVE_SCREECH'] -> ['MOVE_CROSS_CHOP', 'MOVE_ICE_PUNCH', 'MOVE_AQUA_JET', 'MOVE_CONFUSE_RAY']
- party[0].iv_scale: 50 -> 214
- party[1].level: 39 -> 47
- party[1].moves: ['MOVE_FIRE_BLAST', 'MOVE_TAKE_DOWN', 'MOVE_FURY_ATTACK', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_BOUNCE', 'MOVE_POISON_JAB', 'MOVE_WILL_O_WISP']
- party[1].iv_scale: 50 -> 237
- party[2].level: 38 -> 47
- party[2].moves: ['MOVE_ROCK_SLIDE', 'MOVE_LOW_KICK', 'MOVE_FLAIL', 'MOVE_ENDURE'] -> ['MOVE_STONE_EDGE', 'MOVE_LOW_KICK', 'MOVE_WOOD_HAMMER', 'MOVE_THUNDER_PUNCH']
- party[2].iv_scale: 50 -> 217

## res/trainers/data/skier_bradley.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SNORUNT' -> 'SPECIES_FURRET'
- party[0].level: 36 -> 54
- party[0].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_AMNESIA', 'MOVE_BATON_PASS', 'MOVE_ME_FIRST']
- party[0].iv_scale: 0 -> 233
- party[1].species: 'SPECIES_SWINUB' -> 'SPECIES_STANTLER'
- party[1].level: 36 -> 54
- party[1].moves: None -> ['MOVE_ZEN_HEADBUTT', 'MOVE_IMPRISON', 'MOVE_CAPTIVATE', 'MOVE_ME_FIRST']
- party[1].iv_scale: 0 -> 245
- party[2].species: 'SPECIES_SNOVER' -> 'SPECIES_LINOONE'
- party[2].level: 36 -> 54
- party[2].moves: None -> ['MOVE_COVET', 'MOVE_SLASH', 'MOVE_REST', 'MOVE_BELLY_DRUM']
- party[2].iv_scale: 0 -> 245

## res/trainers/data/skier_edward.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SNEASEL' -> 'SPECIES_ABOMASNOW'
- party[0].level: 39 -> 50
- party[0].moves: None -> ['MOVE_BLIZZARD', 'MOVE_ENERGY_BALL', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_BALL']
- party[0].iv_scale: 0 -> 239

## res/trainers/data/skier_kaitlyn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SWINUB' -> 'SPECIES_MAMOSWINE'
- party[0].level: 36 -> 54
- party[0].moves: None -> ['MOVE_ICE_FANG', 'MOVE_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_SUPERPOWER']
- party[0].iv_scale: 0 -> 246
- party[1].species: 'SPECIES_SNOVER' -> 'SPECIES_DELIBIRD'
- party[1].level: 38 -> 54
- party[1].moves: None -> ['MOVE_PRESENT', 'MOVE_BLIZZARD', 'MOVE_SIGNAL_BEAM', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 226

## res/trainers/data/skier_andrea.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SNOVER' -> 'SPECIES_FROSLASS'
- party[0].level: 39 -> 55
- party[0].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_THUNDERBOLT', 'MOVE_THUNDER_WAVE', 'MOVE_BLIZZARD']
- party[0].iv_scale: 0 -> 246

## res/trainers/data/ace_trainer_dalton.json
- party[0].species: 'SPECIES_ELECTABUZZ' -> 'SPECIES_ELECTIVIRE'
- party[0].level: 40 -> 52
- party[0].moves: ['MOVE_THUNDERBOLT', 'MOVE_SWIFT', 'MOVE_QUICK_ATTACK', 'MOVE_THUNDER_WAVE'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ICE_PUNCH', 'MOVE_THUNDER_WAVE']
- party[0].iv_scale: 50 -> 242
- party[1].species: 'SPECIES_MAGMAR' -> 'SPECIES_MAGMORTAR'
- party[1].level: 40 -> 52
- party[1].moves: ['MOVE_FLAMETHROWER', 'MOVE_FAINT_ATTACK', 'MOVE_SMOG', 'MOVE_WILL_O_WISP'] -> ['MOVE_FLAMETHROWER', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_WILL_O_WISP']
- party[1].iv_scale: 50 -> 252

## res/trainers/data/ace_trainer_olivia.json
- party[0].species: 'SPECIES_KIRLIA' -> 'SPECIES_ALTARIA'
- party[0].level: 38 -> 52
- party[0].moves: ['MOVE_FUTURE_SIGHT', 'MOVE_PSYCHIC', 'MOVE_MAGICAL_LEAF', 'MOVE_LUCKY_CHANT'] -> ['MOVE_DRAGON_DANCE', 'MOVE_OUTRAGE', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[0].iv_scale: 50 -> 238
- party[1].species: 'SPECIES_SEAKING' -> 'SPECIES_LAPRAS'
- party[1].level: 39 -> 52
- party[1].moves: ['MOVE_WATERFALL', 'MOVE_POISON_JAB', 'MOVE_SUPERSONIC', 'MOVE_AQUA_RING'] -> ['MOVE_DRAGON_DANCE', 'MOVE_WATERFALL', 'MOVE_OUTRAGE', 'MOVE_REST']
- party[1].iv_scale: 50 -> 242
- party[2].species: 'SPECIES_BUNEARY' -> 'SPECIES_URSARING'
- party[2].level: 38 -> 52
- party[2].moves: ['MOVE_DIZZY_PUNCH', 'MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_SHADOW_BALL'] -> ['MOVE_SLASH', 'MOVE_SWORDS_DANCE', 'MOVE_STONE_EDGE', 'MOVE_CLOSE_COMBAT']
- party[2].iv_scale: 50 -> 220

## res/trainers/data/skier_shawn.json
- party size changed (3 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/skier_shawn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/skier_bjorn.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/skier_bjorn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/skier_lexie.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PILOSWINE' -> 'SPECIES_DEWGONG'
- party[0].level: 37 -> 51
- party[0].moves: None -> ['MOVE_DIVE', 'MOVE_WATERFALL', 'MOVE_SHEER_COLD', 'MOVE_AQUA_JET']
- party[0].iv_scale: 0 -> 232
- party[1].level: 37 -> 51
- party[1].moves: None -> ['MOVE_ICE_BEAM', 'MOVE_SHADOW_BALL', 'MOVE_ROAR', 'MOVE_TOXIC']
- party[1].iv_scale: 0 -> 252

## res/trainers/data/skier_madison.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SNORUNT' -> 'SPECIES_JYNX'
- party[0].level: 39 -> 51
- party[0].moves: None -> ['MOVE_PSYCHIC', 'MOVE_BLIZZARD', 'MOVE_ENERGY_BALL', 'MOVE_PERISH_SONG']
- party[0].iv_scale: 0 -> 232

## res/trainers/data/ninja_boy_matthew.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_SHEDINJA'
- party[0].level: 39 -> 51
- party[0].moves: None -> ['MOVE_X_SCISSOR', 'MOVE_CONFUSE_RAY', 'MOVE_SHADOW_SNEAK', 'MOVE_NIGHT_SLASH']
- party[0].iv_scale: 0 -> 250

## res/trainers/data/ninja_boy_ethan.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ninja_boy_ethan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/black_belt_luke.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_CROAGUNK' -> 'SPECIES_TOXICROAK'
- party[0].level: 37 -> 51
- party[0].moves: None -> ['MOVE_DARK_PULSE', 'MOVE_NASTY_PLOT', 'MOVE_VACUUM_WAVE', 'MOVE_SLUDGE_BOMB']
- party[0].iv_scale: 30 -> 251
- party[1].species: 'SPECIES_RIOLU' -> 'SPECIES_LUCARIO'
- party[1].level: 37 -> 51
- party[1].moves: None -> ['MOVE_AURA_SPHERE', 'MOVE_CLOSE_COMBAT', 'MOVE_DRAGON_PULSE', 'MOVE_EXTREME_SPEED']
- party[1].iv_scale: 30 -> 245
- party[2].species: 'SPECIES_MACHOKE' -> 'SPECIES_BRELOOM'
- party[2].level: 37 -> 51
- party[2].moves: None -> ['MOVE_SKY_UPPERCUT', 'MOVE_SPORE', 'MOVE_SEED_BOMB', 'MOVE_MACH_PUNCH']
- party[2].iv_scale: 30 -> 239

## res/trainers/data/fisherman_miguel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GYARADOS' -> 'SPECIES_STARMIE'
- party[0].level: 33 -> 44
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_RECOVER', 'MOVE_PSYCHIC', 'MOVE_CONFUSE_RAY']
- party[0].iv_scale: 0 -> 235
- party[1].species: 'SPECIES_GYARADOS' -> 'SPECIES_LANTURN'
- party[1].level: 33 -> 44
- party[1].moves: None -> ['MOVE_THUNDERBOLT', 'MOVE_SURF', 'MOVE_SIGNAL_BEAM', 'MOVE_DISCHARGE']
- party[1].iv_scale: 0 -> 233

## res/trainers/data/fisherman_luc.json
- party size changed (5 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/fisherman_luc.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_adrian.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_adrian.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_erik.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_TENTACRUEL' -> 'SPECIES_SLOWKING'
- party[0].level: 35 -> 45
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_NASTY_PLOT', 'MOVE_POWER_GEM']
- party[0].iv_scale: 0 -> 255

## res/trainers/data/swimmer_vincent.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']
- party[0].level: 33 -> 44
- party[0].moves: None -> ['MOVE_RAIN_DANCE', 'MOVE_TAILWIND', 'MOVE_SKY_ATTACK', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 240
- party[1].species: 'SPECIES_GASTRODON' -> 'SPECIES_KABUTOPS'
- party[1].level: 33 -> 44
- party[1].moves: None -> ['MOVE_STONE_EDGE', 'MOVE_WATERFALL', 'MOVE_KNOCK_OFF', 'MOVE_SUPERPOWER']
- party[1].iv_scale: 0 -> 247

## res/trainers/data/swimmer_jessica.json
- party size changed (4 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_jessica.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_erica.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_FINNEON' -> 'SPECIES_BIBAREL'
- party[0].level: 35 -> 45
- party[0].moves: None -> ['MOVE_DEFENSE_CURL', 'MOVE_ROLLOUT', 'MOVE_QUICK_ATTACK', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 252

## res/trainers/data/swimmer_katelyn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']
- party[0].species: 'SPECIES_BUIZEL' -> 'SPECIES_POLITOED'
- party[0].level: 32 -> 43
- party[0].moves: ['MOVE_AQUA_JET', 'MOVE_SONIC_BOOM', 'MOVE_QUICK_ATTACK', 'MOVE_ATTRACT'] -> ['MOVE_RAIN_DANCE', 'MOVE_PERISH_SONG', 'MOVE_SURF', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 244
- party[1].level: 32 -> 43
- party[1].moves: ['MOVE_CONFUSION', 'MOVE_BRICK_BREAK', 'MOVE_MEDITATE', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_HI_JUMP_KICK', 'MOVE_BULLET_PUNCH', 'MOVE_PSYCHO_CUT']
- party[1].iv_scale: 0 -> 223
- party[2].species: 'SPECIES_SEAKING' -> 'SPECIES_LUDICOLO'
- party[2].level: 32 -> 43
- party[2].moves: ['MOVE_WATER_PULSE', 'MOVE_HORN_ATTACK', 'MOVE_AQUA_RING', 'MOVE_CAPTIVATE'] -> ['MOVE_SEED_BOMB', 'MOVE_WATERFALL', 'MOVE_THUNDER_PUNCH', 'MOVE_ZEN_HEADBUTT']
- party[2].iv_scale: 0 -> 253

## res/trainers/data/swimmer_dillon.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_dillon.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_vanessa.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLDUCK' -> 'SPECIES_CORSOLA'
- party[0].level: 35 -> 46
- party[0].moves: None -> ['MOVE_ICE_BEAM', 'MOVE_EARTH_POWER', 'MOVE_SURF', 'MOVE_POWER_GEM']
- party[0].iv_scale: 0 -> 243

## res/trainers/data/fisherman_cory.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_FINNEON' -> 'SPECIES_SEADRA'
- party[0].level: 30 -> 44
- party[0].moves: None -> ['MOVE_DRAGON_PULSE', 'MOVE_TWISTER', 'MOVE_BRINE', 'MOVE_HYDRO_PUMP']
- party[0].iv_scale: 0 -> 239
- party[1].species: 'SPECIES_FINNEON' -> 'SPECIES_SHARPEDO'
- party[1].level: 32 -> 44
- party[1].moves: None -> ['MOVE_CRUNCH', 'MOVE_SLASH', 'MOVE_AQUA_JET', 'MOVE_TAUNT']
- party[1].iv_scale: 0 -> 254
- party[2].species: 'SPECIES_FINNEON' -> 'SPECIES_DRAGONAIR'
- party[2].level: 34 -> 44
- party[2].moves: None -> ['MOVE_DRAGON_RUSH', 'MOVE_HEADBUTT', 'MOVE_AQUA_TAIL', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 0 -> 253

## res/trainers/data/ace_trainer_jake.json
- party[0].species: 'SPECIES_STARAPTOR' -> 'SPECIES_BANETTE'
- party[0].level: 35 -> 46
- party[0].moves: ['MOVE_TAKE_DOWN', 'MOVE_AERIAL_ACE', 'MOVE_ENDEAVOR', 'MOVE_QUICK_ATTACK'] -> ['MOVE_NIGHT_SLASH', 'MOVE_SHADOW_SNEAK', 'MOVE_SUCKER_PUNCH', 'MOVE_EMBARGO']
- party[0].iv_scale: 50 -> 255
- party[1].species: 'SPECIES_GIRAFARIG' -> 'SPECIES_GALLADE'
- party[1].level: 36 -> 46
- party[1].moves: ['MOVE_DOUBLE_HIT', 'MOVE_PSYCHIC', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_PSYCHO_CUT', 'MOVE_LEAF_BLADE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE']
- party[1].iv_scale: 50 -> 249

## res/trainers/data/ace_trainer_shannon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']
- party[0].level: 34 -> 45
- party[0].moves: ['MOVE_PETAL_DANCE', 'MOVE_MAGICAL_LEAF', 'MOVE_LEECH_SEED', 'MOVE_NONE'] -> ['MOVE_ENERGY_BALL', 'MOVE_WEATHER_BALL', 'MOVE_LEECH_SEED', 'MOVE_SUNNY_DAY']
- party[0].iv_scale: 50 -> 237
- party[1].species: 'SPECIES_AZUMARILL' -> 'SPECIES_MILTANK'
- party[1].level: 34 -> 45
- party[1].moves: ['MOVE_DOUBLE_EDGE', 'MOVE_BUBBLE_BEAM', 'MOVE_AQUA_RING', 'MOVE_NONE'] -> ['MOVE_HAMMER_ARM', 'MOVE_FIRE_PUNCH', 'MOVE_HEADBUTT', 'MOVE_MILK_DRINK']
- party[1].iv_scale: 50 -> 239
- party[2].level: 35 -> 45
- party[2].moves: ['MOVE_JUMP_KICK', 'MOVE_QUICK_ATTACK', 'MOVE_CHARM', 'MOVE_NONE'] -> ['MOVE_JUMP_KICK', 'MOVE_QUICK_ATTACK', 'MOVE_FIRE_PUNCH', 'MOVE_DIZZY_PUNCH']
- party[2].iv_scale: 50 -> 240

## res/trainers/data/fisherman_brett.json
- party size changed (3 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/fisherman_brett.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/fisherman_alec.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGIKARP' -> 'SPECIES_GYARADOS'
- party[0].level: 42 -> 57
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_WATERFALL', 'MOVE_DRAGON_DANCE', 'MOVE_ICE_FANG']
- party[0].iv_scale: 0 -> 253
- party[1].level: 45 -> 57
- party[1].moves: None -> ['MOVE_BOUNCE', 'MOVE_IRON_HEAD', 'MOVE_AQUA_TAIL', 'MOVE_STONE_EDGE']
- party[1].iv_scale: 0 -> 253

## res/trainers/data/fisherman_george.json
- party size changed (4 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/fisherman_george.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/fisherman_cole.json
- party size changed (3 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/fisherman_cole.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/sailor_luther.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WINGULL' -> 'SPECIES_PELIPPER'
- party[0].level: 41 -> 56
- party[0].moves: None -> ['MOVE_SWALLOW', 'MOVE_SPIT_UP', 'MOVE_STOCKPILE', 'MOVE_TAILWIND']
- party[0].iv_scale: 0 -> 246
- party[1].species: 'SPECIES_MACHOKE' -> 'SPECIES_HARIYAMA'
- party[1].level: 42 -> 56
- party[1].moves: None -> ['MOVE_BULLET_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_BULK_UP', 'MOVE_CLOSE_COMBAT']
- party[1].iv_scale: 0 -> 252
- party[2].species: 'SPECIES_GASTRODON' -> 'SPECIES_HUNTAIL'
- party[2].level: 43 -> 56
- party[2].moves: None -> ['MOVE_DIVE', 'MOVE_CRUNCH', 'MOVE_AQUA_TAIL', 'MOVE_HYDRO_PUMP']
- party[2].iv_scale: 0 -> 229

## res/trainers/data/swimmer_wesley.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 43 -> 60
- party[0].moves: None -> ['MOVE_CRUNCH', 'MOVE_AGILITY', 'MOVE_WATERFALL', 'MOVE_RAZOR_WIND']
- party[0].iv_scale: 0 -> 217
- party[1].species: 'SPECIES_TENTACRUEL' -> 'SPECIES_CLOYSTER'
- party[1].level: 43 -> 60
- party[1].moves: None -> ['MOVE_ICE_BEAM', 'MOVE_PROTECT', 'MOVE_SURF', 'MOVE_SPIKE_CANNON']
- party[1].iv_scale: 0 -> 231

## res/trainers/data/swimmer_ricardo.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 61
- party[0].moves: None -> ['MOVE_POISON_JAB', 'MOVE_SCREECH', 'MOVE_HYDRO_PUMP', 'MOVE_WRING_OUT']
- party[0].iv_scale: 0 -> 248

## res/trainers/data/swimmer_francisco.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_TENTACOOL' -> 'SPECIES_KINGLER'
- party[0].level: 41 -> 60
- party[0].moves: None -> ['MOVE_GUILLOTINE', 'MOVE_SLAM', 'MOVE_BRINE', 'MOVE_CRABHAMMER']
- party[0].iv_scale: 0 -> 254
- party[1].species: 'SPECIES_GOLDUCK' -> 'SPECIES_QUAGSIRE'
- party[1].level: 45 -> 60
- party[1].moves: None -> ['MOVE_TOXIC', 'MOVE_EARTHQUAKE', 'MOVE_WATERFALL', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 0 -> 225

## res/trainers/data/swimmer_colton.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WINGULL' -> 'SPECIES_SLOWBRO'
- party[0].level: 40 -> 59
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_SLACK_OFF', 'MOVE_AMNESIA', 'MOVE_PSYCHIC']
- party[0].iv_scale: 0 -> 238
- party[1].level: 44 -> 59
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_SIGNAL_BEAM', 'MOVE_ICE_BEAM', 'MOVE_HYPER_BEAM']
- party[1].iv_scale: 0 -> 229
- party[2].level: 44 -> 59
- party[2].moves: None -> ['MOVE_FLY', 'MOVE_ICE_BEAM', 'MOVE_TAILWIND', 'MOVE_HYDRO_PUMP']
- party[2].iv_scale: 0 -> 229

## res/trainers/data/swimmer_troy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 61
- party[0].moves: None -> ['MOVE_DRAGON_DANCE', 'MOVE_WATERFALL', 'MOVE_ICE_FANG', 'MOVE_EARTHQUAKE']
- party[0].iv_scale: 0 -> 243

## res/trainers/data/swimmer_oscar.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_oscar.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_miranda.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 61
- party[0].moves: None -> ['MOVE_SWEET_KISS', 'MOVE_AIR_CUTTER', 'MOVE_SURF', 'MOVE_SILVER_WIND']
- party[0].iv_scale: 0 -> 249

## res/trainers/data/swimmer_aubree.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 43 -> 60
- party[0].moves: None -> ['MOVE_DEFENSE_CURL', 'MOVE_ROLLOUT', 'MOVE_WATERFALL', 'MOVE_QUICK_ATTACK']
- party[0].iv_scale: 0 -> 223
- party[1].level: 43 -> 60
- party[1].moves: None -> ['MOVE_FOCUS_BLAST', 'MOVE_GRASS_KNOT', 'MOVE_BLIZZARD', 'MOVE_HYDRO_PUMP']
- party[1].iv_scale: 0 -> 244

## res/trainers/data/swimmer_paige.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MARILL' -> 'SPECIES_LAPRAS'
- party[0].level: 41 -> 59
- party[0].moves: None -> ['MOVE_BRINE', 'MOVE_SAFEGUARD', 'MOVE_HYDRO_PUMP', 'MOVE_SHEER_COLD']
- party[0].iv_scale: 0 -> 212
- party[1].species: 'SPECIES_WINGULL' -> 'SPECIES_DEWGONG'
- party[1].level: 42 -> 59
- party[1].moves: None -> ['MOVE_DIVE', 'MOVE_AQUA_TAIL', 'MOVE_ICE_BEAM', 'MOVE_SAFEGUARD']
- party[1].iv_scale: 0 -> 236
- party[2].species: 'SPECIES_GOLDUCK' -> 'SPECIES_SLOWKING'
- party[2].level: 43 -> 59
- party[2].moves: None -> ['MOVE_HYDRO_PUMP', 'MOVE_PSYCHIC', 'MOVE_POWER_GEM', 'MOVE_FLAMETHROWER']
- party[2].iv_scale: 0 -> 229

## res/trainers/data/swimmer_crystal.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WINGULL' -> 'SPECIES_SEAKING'
- party[0].level: 42 -> 60
- party[0].moves: None -> ['MOVE_FURY_ATTACK', 'MOVE_WATERFALL', 'MOVE_HORN_DRILL', 'MOVE_AGILITY']
- party[0].iv_scale: 0 -> 254
- party[1].species: 'SPECIES_SEAKING' -> 'SPECIES_CORSOLA'
- party[1].level: 44 -> 60
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_POWER_GEM', 'MOVE_MIRROR_COAT', 'MOVE_EARTH_POWER']
- party[1].iv_scale: 0 -> 248

## res/trainers/data/swimmer_cassandra.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_cassandra.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_gabrielle.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 61
- party[0].moves: None -> ['MOVE_ICE_PUNCH', 'MOVE_ZEN_HEADBUTT', 'MOVE_AQUA_JET', 'MOVE_WATERFALL']
- party[0].iv_scale: 0 -> 251

## res/trainers/data/worker_colin.json
- party[0].level: 6 -> 12
- party[0].moves: None -> ['MOVE_TACKLE', 'MOVE_DEFENSE_CURL', 'MOVE_MUD_SPORT', 'MOVE_ROCK_THROW']
- party[0].iv_scale: 0 -> 145
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_WHISMUR'
- party[1].level: 8 -> 12
- party[1].moves: None -> ['MOVE_UPROAR', 'MOVE_ASTONISH', 'MOVE_POUND', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 157

## res/trainers/data/worker_mason.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 9 -> 12
- party[0].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_DEFENSE_CURL', 'MOVE_MUD_SPORT', 'MOVE_ROCK_POLISH']
- party[0].iv_scale: 0 -> 144

## res/trainers/data/bug_catcher_jack.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WURMPLE' -> 'SPECIES_KAKUNA'
- party[0].level: 11 -> 16
- party[0].moves: ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_NONE'] -> ['MOVE_BUG_BITE', 'MOVE_IRON_DEFENSE', 'MOVE_POISON_STING', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 220
- party[1].species: 'SPECIES_SILCOON' -> 'SPECIES_CASCOON'
- party[1].level: 13 -> 16
- party[1].moves: ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_HARDEN'] -> ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_BUG_BITE']
- party[1].iv_scale: 0 -> 130
- party[2].species: 'SPECIES_BEAUTIFLY' -> 'SPECIES_METAPOD'
- party[2].level: 15 -> 16
- party[2].moves: ['MOVE_TACKLE', 'MOVE_POISON_STING', 'MOVE_ABSORB', 'MOVE_GUST'] -> ['MOVE_BUG_BITE', 'MOVE_POISON_STING', 'MOVE_IRON_DEFENSE', 'MOVE_NONE']
- party[2].iv_scale: 20 -> 164

## res/trainers/data/bug_catcher_phillip.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_WURMPLE' -> 'SPECIES_NINCADA'
- party[0].level: 11 -> 17
- party[0].moves: ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_NONE'] -> ['MOVE_HARDEN', 'MOVE_LEECH_LIFE', 'MOVE_SAND_ATTACK', 'MOVE_FURY_SWIPES']
- party[0].iv_scale: 0 -> 106
- party[1].species: 'SPECIES_CASCOON' -> 'SPECIES_BUTTERFREE'
- party[1].level: 13 -> 17
- party[1].moves: ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_POISON_STING', 'MOVE_HARDEN'] -> ['MOVE_POISON_POWDER', 'MOVE_CONFUSION', 'MOVE_SLEEP_POWDER', 'MOVE_GUST']
- party[1].iv_scale: 0 -> 136
- party[2].level: 15 -> 19
- party[2].moves: ['MOVE_TACKLE', 'MOVE_POISON_STING', 'MOVE_CONFUSION', 'MOVE_GUST'] -> ['MOVE_BUG_BITE', 'MOVE_CONFUSION', 'MOVE_GUST', 'MOVE_PROTECT']
- party[2].iv_scale: 20 -> 136

## res/trainers/data/bug_catcher_donald.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BURMY' -> 'SPECIES_PINECO'
- party[0].form: 1 -> 0
- party[0].level: 14 -> 17
- party[0].moves: None -> ['MOVE_SELFDESTRUCT', 'MOVE_BUG_BITE', 'MOVE_TAKE_DOWN', 'MOVE_RAPID_SPIN']
- party[0].iv_scale: 10 -> 179
- party[1].species: 'SPECIES_BURMY' -> 'SPECIES_COMBEE'
- party[1].form: 2 -> 0
- party[1].level: 14 -> 19
- party[1].moves: None -> ['MOVE_SWEET_SCENT', 'MOVE_GUST', 'MOVE_BUG_BITE', 'MOVE_NONE']
- party[1].iv_scale: 10 -> 135

## res/trainers/data/lass_briana.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PACHIRISU' -> 'SPECIES_SLAKOTH'
- party[0].level: 16 -> 17
- party[0].moves: None -> ['MOVE_SCRATCH', 'MOVE_YAWN', 'MOVE_ENCORE', 'MOVE_SLACK_OFF']
- party[0].iv_scale: 0 -> 157

## res/trainers/data/psychic_elijah.json
- party[0].species: 'SPECIES_ABRA' -> 'SPECIES_WYNAUT'
- party[0].moves: ['MOVE_HIDDEN_POWER', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_COUNTER', 'MOVE_MIRROR_COAT', 'MOVE_SAFEGUARD', 'MOVE_DESTINY_BOND']
- party[0].iv_scale: 20 -> 184

## res/trainers/data/psychic_lindsey.json
- party[0].species: 'SPECIES_ABRA' -> 'SPECIES_EXEGGCUTE'
- party[0].moves: ['MOVE_HIDDEN_POWER', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HYPNOSIS', 'MOVE_REFLECT', 'MOVE_LEECH_SEED', 'MOVE_BULLET_SEED']
- party[0].iv_scale: 20 -> 113

## res/trainers/data/dummy_208.json
- class: 'TRAINER_CLASS_WORKER' -> 'TRAINER_CLASS_MAID'
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_HAPPINY'
- party[0].level: 5 -> 12
- party[0].item: None -> 'ITEM_TOXIC_ORB'
- party[0].moves: None -> ['MOVE_HELPING_HAND', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']

## res/trainers/data/dummy_209.json
- class: 'TRAINER_CLASS_WORKER' -> 'TRAINER_CLASS_MAID'
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_CHANSEY'
- party[0].level: 5 -> 26
- party[0].item: None -> 'ITEM_TOXIC_ORB'
- party[0].moves: None -> ['MOVE_HELPING_HAND', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']

## res/trainers/data/dummy_210.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_210.json
- class: 'TRAINER_CLASS_WORKER' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_211.json
- class: 'TRAINER_CLASS_ACE_TRAINER_SNOW_MALE' -> 'TRAINER_CLASS_MAID'
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_BLISSEY'
- party[0].level: 5 -> 49
- party[0].item: None -> 'ITEM_TOXIC_ORB'
- party[0].moves: None -> ['MOVE_HELPING_HAND', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']

## res/trainers/data/dummy_212.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_212.json
- class: 'TRAINER_CLASS_ACE_TRAINER_SNOW_MALE' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_213.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_213.json
- class: 'TRAINER_CLASS_ACE_TRAINER_SNOW_FEMALE' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_214.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_214.json
- class: 'TRAINER_CLASS_ACE_TRAINER_SNOW_FEMALE' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_215.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_215.json
- class: 'TRAINER_CLASS_VETERAN' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_216.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_216.json
- class: 'TRAINER_CLASS_VETERAN' -> 'TRAINER_CLASS_MAID'

## res/trainers/data/dummy_217.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_217.json
- class: 'TRAINER_CLASS_PSYCHIC_MALE' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/dummy_218.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_218.json
- class: 'TRAINER_CLASS_PSYCHIC_FEMALE' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/dummy_219.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_219.json
- class: 'TRAINER_CLASS_DRAGON_TAMER' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/dummy_220.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_220.json
- class: 'TRAINER_CLASS_SAILOR' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/dummy_221.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_221.json
- class: 'TRAINER_CLASS_SCHOOL_KID_MALE' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/dummy_222.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_222.json
- class: 'TRAINER_CLASS_SCHOOL_KID_FEMALE' -> 'TRAINER_CLASS_MAID'
- double_battle: False -> True

## res/trainers/data/ace_trainer_omar.json
- party[0].level: 45 -> 63
- party[0].moves: ['MOVE_BLIZZARD', 'MOVE_ICE_FANG', 'MOVE_ROCK_SLIDE', 'MOVE_GIGA_IMPACT'] -> ['MOVE_EARTHQUAKE', 'MOVE_ICE_FANG', 'MOVE_ROCK_SLIDE', 'MOVE_GIGA_IMPACT']
- party[0].iv_scale: 50 -> 246
- party[1].level: 46 -> 63
- party[1].moves: ['MOVE_SILVER_WIND', 'MOVE_AIR_SLASH', 'MOVE_PSYCHIC', 'MOVE_TOXIC'] -> ['MOVE_BUG_BUZZ', 'MOVE_AIR_SLASH', 'MOVE_PSYCHIC', 'MOVE_TOXIC']
- party[1].iv_scale: 50 -> 209
- party[2].level: 48 -> 63
- party[2].moves: ['MOVE_HEAD_SMASH', 'MOVE_ZEN_HEADBUTT', 'MOVE_ANCIENT_POWER', 'MOVE_SCREECH'] -> ['MOVE_HEAD_SMASH', 'MOVE_ZEN_HEADBUTT', 'MOVE_IRON_HEAD', 'MOVE_THUNDER_PUNCH']
- party[2].iv_scale: 50 -> 219

## res/trainers/data/ace_trainer_henry.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_mariah.json
- party[0].level: 45 -> 63
- party[0].moves: ['MOVE_DOUBLE_EDGE', 'MOVE_SING', 'MOVE_SOFTBOILED', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_HYPER_BEAM', 'MOVE_SING', 'MOVE_SOFTBOILED', 'MOVE_LIGHT_SCREEN']
- party[0].iv_scale: 50 -> 255
- party[1].level: 46 -> 63
- party[1].iv_scale: 50 -> 214
- party[2].species: 'SPECIES_MAGNEZONE' -> 'SPECIES_TYRANITAR'
- party[2].level: 48 -> 63
- party[2].moves: ['MOVE_DISCHARGE', 'MOVE_FLASH_CANNON', 'MOVE_THUNDER_WAVE', 'MOVE_BARRIER'] -> ['MOVE_STONE_EDGE', 'MOVE_CRUNCH', 'MOVE_THUNDER_FANG', 'MOVE_EARTHQUAKE']
- party[2].iv_scale: 50 -> 253

## res/trainers/data/ace_trainer_sydney.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/veteran_edgar.json
- party[0].level: 46 -> 63
- party[0].iv_scale: 100 -> 172
- party[1].level: 46 -> 63
- party[1].iv_scale: 100 -> 223
- party[2].level: 46 -> 63
- party[2].moves: ['MOVE_BRINE', 'MOVE_DRILL_PECK', 'MOVE_METAL_CLAW', 'MOVE_GROWL'] -> ['MOVE_BRINE', 'MOVE_DRILL_PECK', 'MOVE_FLASH_CANNON', 'MOVE_GROWL']
- party[2].iv_scale: 100 -> 250

## res/trainers/data/veteran_clayton.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dragon_tamer_ondrej.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dragon_tamer_clinton.json
- party[0].species: 'SPECIES_GIBLE' -> 'SPECIES_GARCHOMP'
- party[0].level: 43 -> 63
- party[0].moves: None -> ['MOVE_FLAMETHROWER', 'MOVE_DRAGON_PULSE', 'MOVE_SURF', 'MOVE_EARTH_POWER']
- party[0].iv_scale: 50 -> 243
- party[1].species: 'SPECIES_SWABLU' -> 'SPECIES_FLYGON'
- party[1].level: 45 -> 63
- party[1].moves: None -> ['MOVE_EARTH_POWER', 'MOVE_DRACO_METEOR', 'MOVE_SILVER_WIND', 'MOVE_FLAMETHROWER']
- party[1].iv_scale: 50 -> 238
- party[2].species: 'SPECIES_GABITE' -> 'SPECIES_AERODACTYL'
- party[2].level: 47 -> 63
- party[2].moves: None -> ['MOVE_CRUNCH', 'MOVE_STONE_EDGE', 'MOVE_IRON_HEAD', 'MOVE_DRAGON_CLAW']
- party[2].iv_scale: 50 -> 208

## res/trainers/data/black_belt_david.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/black_belt_david.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/bird_keeper_hana.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/bird_keeper_hana.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/psychic_bryce.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HAUNTER' -> 'SPECIES_GRUMPIG'
- party[0].level: 43 -> 63
- party[0].moves: None -> ['MOVE_PSYCHIC', 'MOVE_PSYCHIC', 'MOVE_POWER_GEM', 'MOVE_HIDDEN_POWER']
- party[0].iv_scale: 0 -> 248
- party[1].level: 46 -> 63
- party[1].moves: None -> ['MOVE_PSYCHIC', 'MOVE_CALM_MIND', 'MOVE_HIDDEN_POWER', 'MOVE_HYPNOSIS']
- party[1].iv_scale: 0 -> 232
- party[2].level: 46 -> 63
- party[2].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_DARK_PULSE', 'MOVE_DESTINY_BOND', 'MOVE_SLUDGE_BOMB']
- party[2].iv_scale: 0 -> 255

## res/trainers/data/psychic_valencia.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 44 -> 63
- party[0].moves: None -> ['MOVE_HEAL_BELL', 'MOVE_SAFEGUARD', 'MOVE_EXTRASENSORY', 'MOVE_SHADOW_BALL']
- party[0].iv_scale: 0 -> 205
- party[1].level: 45 -> 63
- party[1].moves: None -> ['MOVE_X_SCISSOR', 'MOVE_NIGHT_SLASH', 'MOVE_ZEN_HEADBUTT', 'MOVE_PSYCHO_CUT']
- party[1].iv_scale: 0 -> 247
- party[2].level: 46 -> 63
- party[2].moves: None -> ['MOVE_SHADOW_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_FIRE_PUNCH']
- party[2].iv_scale: 0 -> 255

## res/trainers/data/double_team_jo_and_pat.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/double_team_jo_and_pat.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/double_team_al_and_kay.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/double_team_al_and_kay.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/veteran_grant.json
- party[0].species: 'SPECIES_RIOLU' -> 'SPECIES_LUCARIO'
- party[0].level: 34 -> 45
- party[0].iv_scale: 100 -> 194
- party[1].species: 'SPECIES_STARAPTOR' -> 'SPECIES_EXPLOUD'
- party[1].level: 34 -> 45
- party[1].moves: ['MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK', 'MOVE_GROWL'] -> ['MOVE_BITE', 'MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG', 'MOVE_ICE_FANG']
- party[1].iv_scale: 100 -> 206
- party[2].species: 'SPECIES_GRAVELER' -> 'SPECIES_GOLEM'
- party[2].level: 34 -> 45
- party[2].iv_scale: 100 -> 162

## res/trainers/data/youngster_jonathon.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_RHYHORN'
- party[0].level: 11 -> 13
- party[0].moves: ['MOVE_TACKLE', 'MOVE_DEFENSE_CURL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_FURY_ATTACK', 'MOVE_ROCK_TOMB', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 122

## res/trainers/data/youngster_darius.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_ARON'
- party[0].level: 9 -> 13
- party[0].moves: ['MOVE_TACKLE', 'MOVE_DEFENSE_CURL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HEADBUTT', 'MOVE_ROCK_TOMB', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 112
- party[1].level: 9 -> 13
- party[1].iv_scale: 10 -> 119

## res/trainers/data/leader_roark.json
- party size changed (3 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_roark.json
- items: ['ITEM_POTION', 'ITEM_POTION'] -> []

## res/trainers/data/rival_route_203_piplup.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 7 -> 10
- party[0].moves: ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_WING_ATTACK', 'MOVE_NONE']
- party[0].iv_scale: 30 -> 134
- party[1].level: 9 -> 11
- party[1].moves: ['MOVE_TACKLE', 'MOVE_WITHDRAW', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_TACKLE', 'MOVE_WITHDRAW', 'MOVE_ABSORB', 'MOVE_NONE']
- party[1].iv_scale: 30 -> 136

## res/trainers/data/rival_route_203_turtwig.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 7 -> 10
- party[0].moves: ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_WING_ATTACK', 'MOVE_NONE']
- party[0].iv_scale: 30 -> 134
- party[1].level: 9 -> 11
- party[1].moves: ['MOVE_SCRATCH', 'MOVE_LEER', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_SCRATCH', 'MOVE_LEER', 'MOVE_EMBER', 'MOVE_NONE']
- party[1].iv_scale: 30 -> 136

## res/trainers/data/rival_route_203_chimchar.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 7 -> 10
- party[0].moves: ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_QUICK_ATTACK', 'MOVE_GROWL', 'MOVE_WING_ATTACK', 'MOVE_NONE']
- party[0].iv_scale: 30 -> 134
- party[1].level: 9 -> 11
- party[1].moves: ['MOVE_POUND', 'MOVE_GROWL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_POUND', 'MOVE_GROWL', 'MOVE_BUBBLE', 'MOVE_NONE']
- party[1].iv_scale: 30 -> 139

## res/trainers/data/leader_byron.json
- party size changed (3 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_byron.json
- items: ['ITEM_HYPER_POTION', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/worker_jackson.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/worker_jackson.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/worker_gary.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_MAGNETON'
- party[0].level: 37 -> 51
- party[0].moves: ['MOVE_SPARK', 'MOVE_MAGNET_BOMB', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_THUNDERBOLT', 'MOVE_TRI_ATTACK', 'MOVE_FLASH_CANNON', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 244

## res/trainers/data/black_belt_philip.json
- items: [] -> ['ITEM_GREAT_BALL']
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MACHOKE' -> 'SPECIES_MACHAMP'
- party[0].level: 40 -> 56
- party[0].moves: None -> ['MOVE_THUNDER_PUNCH', 'MOVE_CROSS_CHOP', 'MOVE_POISON_JAB', 'MOVE_LOW_KICK']
- party[0].iv_scale: 30 -> 240

## res/trainers/data/aroma_lady_jenna.json
- party[0].species: 'SPECIES_BUDEW' -> 'SPECIES_CACNEA'
- party[0].level: 15 -> 23
- party[0].moves: ['MOVE_ABSORB', 'MOVE_STUN_SPORE', 'MOVE_WATER_SPORT', 'MOVE_NONE'] -> ['MOVE_GROWTH', 'MOVE_LEECH_SEED', 'MOVE_GRASS_KNOT', 'MOVE_PIN_MISSILE']
- party[0].iv_scale: 20 -> 180
- party[1].species: 'SPECIES_BUDEW' -> 'SPECIES_ODDISH'
- party[1].level: 16 -> 23
- party[1].moves: ['MOVE_ABSORB', 'MOVE_STUN_SPORE', 'MOVE_WATER_SPORT', 'MOVE_NONE'] -> ['MOVE_POISON_POWDER', 'MOVE_STUN_SPORE', 'MOVE_SLEEP_POWDER', 'MOVE_MEGA_DRAIN']
- party[1].iv_scale: 20 -> 165
- party[2].species: 'SPECIES_BUDEW' -> 'SPECIES_LOTAD'
- party[2].level: 17 -> 23
- party[2].moves: ['MOVE_ABSORB', 'MOVE_STUN_SPORE', 'MOVE_WATER_SPORT', 'MOVE_NONE'] -> ['MOVE_NATURE_POWER', 'MOVE_WATER_GUN', 'MOVE_NATURAL_GIFT', 'MOVE_MEGA_DRAIN']
- party[2].iv_scale: 20 -> 183

## res/trainers/data/aroma_lady_angela.json
- party[0].species: 'SPECIES_ROSELIA' -> 'SPECIES_SUNFLORA'
- party[0].level: 19 -> 23
- party[0].moves: ['MOVE_MEGA_DRAIN', 'MOVE_POISON_STING', 'MOVE_STUN_SPORE', 'MOVE_NONE'] -> ['MOVE_MEGA_DRAIN', 'MOVE_LEECH_SEED', 'MOVE_INGRAIN', 'MOVE_SYNTHESIS']
- party[0].iv_scale: 20 -> 155

## res/trainers/data/elite_four_aaron.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_aaron.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_BATON_PASS']

## res/trainers/data/elite_four_bertha.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_bertha.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/elite_four_flint.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_flint.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/elite_four_lucian.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_lucian.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/camper_curtis.json
- party[0].species: 'SPECIES_STARLY' -> 'SPECIES_DODUO'
- party[0].level: 7 -> 10
- party[0].moves: None -> ['MOVE_PECK', 'MOVE_GROWL', 'MOVE_QUICK_ATTACK', 'MOVE_RAGE']
- party[0].iv_scale: 0 -> 139
- party[1].species: 'SPECIES_SHINX' -> 'SPECIES_NIDORAN_M'
- party[1].level: 7 -> 10
- party[1].moves: None -> ['MOVE_LEER', 'MOVE_PECK', 'MOVE_FOCUS_ENERGY', 'MOVE_DOUBLE_KICK']
- party[1].iv_scale: 0 -> 128

## res/trainers/data/champion_cynthia.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- party[0].level: 58 -> 77
- party[0].item: 'ITEM_NONE' -> 'ITEM_LEFTOVERS'
- party[0].iv_scale: 250 -> 254
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_PORYGON_Z'
- party[1].level: 58 -> 77
- party[1].item: 'ITEM_NONE' -> 'ITEM_CHOICE_SPECS'
- party[1].moves: ['MOVE_ENERGY_BALL', 'MOVE_SLUDGE_BOMB', 'MOVE_TOXIC', 'MOVE_EXTRASENSORY'] -> ['MOVE_HYPER_BEAM', 'MOVE_THUNDERBOLT', 'MOVE_ICE_BEAM', 'MOVE_PSYCHIC']
- party[1].ability/gender: 0/None -> 2/None
- party[2].level: 60 -> 77
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_AIR_SLASH', 'MOVE_AURA_SPHERE', 'MOVE_WATER_PULSE', 'MOVE_SHOCK_WAVE'] -> ['MOVE_AIR_SLASH', 'MOVE_AURA_SPHERE', 'MOVE_FLAMETHROWER', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 250 -> 229
- party[2].ability/gender: 0/None -> 2/None
- party[3].level: 60 -> 77
- party[3].item: 'ITEM_NONE' -> 'ITEM_CHOICE_SCARF'
- party[3].moves: ['MOVE_AURA_SPHERE', 'MOVE_EXTREME_SPEED', 'MOVE_SHADOW_BALL', 'MOVE_STONE_EDGE'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_EXTREME_SPEED', 'MOVE_BULLET_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[3].iv_scale: 250 -> 245
- party[4].level: 58 -> 77
- party[4].item: 'ITEM_NONE' -> 'ITEM_FLAME_ORB'
- party[4].moves: ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_MIRROR_COAT', 'MOVE_DRAGON_PULSE'] -> ['MOVE_HYDRO_PUMP', 'MOVE_ICE_BEAM', 'MOVE_MIRROR_COAT', 'MOVE_RECOVER']
- party[4].iv_scale: 250 -> 246
- party[5].level: 62 -> 78
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_YACHE_BERRY'
- party[5].moves: ['MOVE_DRAGON_RUSH', 'MOVE_EARTHQUAKE', 'MOVE_FLAMETHROWER', 'MOVE_GIGA_IMPACT'] -> ['MOVE_OUTRAGE', 'MOVE_EARTHQUAKE', 'MOVE_FIRE_FANG', 'MOVE_GIGA_IMPACT']
- party[5].iv_scale: 250 -> 247

## res/trainers/data/ace_trainer_sergio.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_isaiah.json
- party[0].level: 44 -> 55
- party[0].moves: ['MOVE_EARTHQUAKE', 'MOVE_FURY_ATTACK', 'MOVE_ICE_FANG', 'MOVE_ANCIENT_POWER'] -> ['MOVE_EARTHQUAKE', 'MOVE_BITE', 'MOVE_ICE_FANG', 'MOVE_STONE_EDGE']
- party[0].iv_scale: 60 -> 239

## res/trainers/data/ace_trainer_savannah.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_savannah.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/ace_trainer_alicia.json
- party[0].species: 'SPECIES_SNEASEL' -> 'SPECIES_CLOYSTER'
- party[0].level: 40 -> 54
- party[0].moves: ['MOVE_ICY_WIND', 'MOVE_SLASH', 'MOVE_SCREECH', 'MOVE_FAINT_ATTACK'] -> ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_SIGNAL_BEAM', 'MOVE_TOXIC_SPIKES']
- party[0].iv_scale: 60 -> 228
- party[1].species: 'SPECIES_SNEASEL' -> 'SPECIES_SEALEO'
- party[1].level: 43 -> 55
- party[1].moves: ['MOVE_ICY_WIND', 'MOVE_SLASH', 'MOVE_SCREECH', 'MOVE_FAINT_ATTACK'] -> ['MOVE_SHEER_COLD', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']
- party[1].iv_scale: 60 -> 199

## res/trainers/data/collector_douglas.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_THUNDER_SHOCK', 'MOVE_QUICK_ATTACK', 'MOVE_DOUBLE_KICK']
- party[0].iv_scale: 0 -> 200
- party[1].level: 24 -> 33
- party[1].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_WATER_GUN', 'MOVE_QUICK_ATTACK', 'MOVE_BITE']
- party[1].iv_scale: 0 -> 237
- party[2].level: 24 -> 33
- party[2].moves: None -> ['MOVE_SAND_ATTACK', 'MOVE_EMBER', 'MOVE_QUICK_ATTACK', 'MOVE_BITE']
- party[2].iv_scale: 0 -> 236

## res/trainers/data/collector_brady.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SKORUPI' -> 'SPECIES_KANGASKHAN'
- party[0].level: 21 -> 28
- party[0].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_MEGA_PUNCH', 'MOVE_HAMMER_ARM', 'MOVE_DIZZY_PUNCH']
- party[0].iv_scale: 0 -> 213
- party[1].level: 21 -> 28
- party[1].moves: None -> ['MOVE_POISON_POWDER', 'MOVE_LEAF_STORM', 'MOVE_LEECH_SEED', 'MOVE_ANCIENT_POWER']
- party[1].iv_scale: 0 -> 246
- party[2].level: 21 -> 28
- party[2].moves: None -> ['MOVE_SONIC_BOOM', 'MOVE_DETECT', 'MOVE_AIR_CUTTER', 'MOVE_SIGNAL_BEAM']
- party[2].iv_scale: 0 -> 255
- party[3].level: 21 -> 28
- party[3].moves: None -> ['MOVE_SEED_BOMB', 'MOVE_SYNTHESIS', 'MOVE_INGRAIN', 'MOVE_KNOCK_OFF']
- party[3].iv_scale: 0 -> 246
- party[4].species: 'SPECIES_CROAGUNK' -> 'SPECIES_PARASECT'
- party[4].level: 21 -> 28
- party[4].moves: None -> ['MOVE_X_SCISSOR', 'MOVE_SEED_BOMB', 'MOVE_SPORE', 'MOVE_CROSS_POISON']
- party[4].iv_scale: 0 -> 244
- party[5].level: 21 -> 28
- party[5].moves: None -> ['MOVE_LEAF_STORM', 'MOVE_AIR_CUTTER', 'MOVE_OMINOUS_WIND', 'MOVE_WHIRLWIND']
- party[5].iv_scale: 0 -> 204

## res/trainers/data/collector_ivan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_TOGETIC' -> 'SPECIES_TOGEKISS'
- party[0].level: 35 -> 47
- party[0].moves: None -> ['MOVE_HIDDEN_POWER', 'MOVE_SHADOW_BALL', 'MOVE_AURA_SPHERE', 'MOVE_AIR_SLASH']
- party[0].iv_scale: 0 -> 240

## res/trainers/data/collector_fernando.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 25 -> 32
- party[0].moves: None -> ['MOVE_NIGHT_SLASH', 'MOVE_BRICK_BREAK', 'MOVE_COUNTER', 'MOVE_AERIAL_ACE']
- party[0].iv_scale: 0 -> 198

## res/trainers/data/collector_edwin.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 25 -> 32
- party[0].item: None -> 'ITEM_CHESTO_BERRY'
- party[0].moves: None -> ['MOVE_HEADBUTT', 'MOVE_ICE_PUNCH', 'MOVE_REST', 'MOVE_ZEN_HEADBUTT']
- party[0].iv_scale: 0 -> 227

## res/trainers/data/dragon_tamer_hayden.json
- party[0].level: 56 -> 85
- party[0].moves: None -> ['MOVE_DRAGON_DANCE', 'MOVE_DRAGON_PULSE', 'MOVE_PERISH_SONG', 'MOVE_FLAMETHROWER']
- party[0].iv_scale: 50 -> 227
- party[1].species: 'SPECIES_SEADRA' -> 'SPECIES_KINGDRA'
- party[1].level: 56 -> 85
- party[1].moves: None -> ['MOVE_ICE_BEAM', 'MOVE_HYDRO_PUMP', 'MOVE_DRAGON_DANCE', 'MOVE_DRAGON_PULSE']
- party[1].iv_scale: 50 -> 211

## res/trainers/data/ace_trainer_dennis.json
- party[0].level: 24 -> 35
- party[0].moves: ['MOVE_SCREECH', 'MOVE_FAINT_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_POISON_STING'] -> ['MOVE_KNOCK_OFF', 'MOVE_U_TURN', 'MOVE_SLASH', 'MOVE_TAILWIND']
- party[0].iv_scale: 50 -> 216
- party[1].species: 'SPECIES_BUIZEL' -> 'SPECIES_FLOATZEL'
- party[1].level: 24 -> 35
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_SWIFT', 'MOVE_PURSUIT', 'MOVE_QUICK_ATTACK'] -> ['MOVE_ICE_PUNCH', 'MOVE_CRUNCH', 'MOVE_AQUA_JET', 'MOVE_BRICK_BREAK']
- party[1].iv_scale: 50 -> 208
- party[2].level: 25 -> 35
- party[2].moves: ['MOVE_SWALLOW', 'MOVE_GUST', 'MOVE_STOCKPILE', 'MOVE_OMINOUS_WIND'] -> ['MOVE_THUNDERBOLT', 'MOVE_WEATHER_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_OMINOUS_WIND']
- party[2].iv_scale: 50 -> 197

## res/trainers/data/ace_trainer_cesar.json
- party[0].level: 40 -> 51
- party[0].iv_scale: 60 -> 235

## res/trainers/data/ace_trainer_allen.json
- party[0].species: 'SPECIES_GASTLY' -> 'SPECIES_ROTOM'
- party[0].level: 21 -> 29
- party[0].moves: ['MOVE_NIGHT_SHADE', 'MOVE_SUCKER_PUNCH', 'MOVE_CURSE', 'MOVE_CONFUSE_RAY'] -> ['MOVE_SHADOW_BALL', 'MOVE_SHOCK_WAVE', 'MOVE_THUNDER_WAVE', 'MOVE_CONFUSE_RAY']
- party[0].iv_scale: 60 -> 204
- party[1].species: 'SPECIES_GASTLY' -> 'SPECIES_SABLEYE'
- party[1].level: 22 -> 29
- party[1].iv_scale: 60 -> 213
- party[2].level: 24 -> 29
- party[2].iv_scale: 60 -> 173

## res/trainers/data/ace_trainer_zachery.json
- party[0].species: 'SPECIES_ELECTABUZZ' -> 'SPECIES_MAGNEZONE'
- party[0].level: 47 -> 60
- party[0].moves: ['MOVE_THUNDERBOLT', 'MOVE_SHOCK_WAVE', 'MOVE_QUICK_ATTACK', 'MOVE_IRON_TAIL'] -> ['MOVE_THUNDERBOLT', 'MOVE_FLASH_CANNON', 'MOVE_TRI_ATTACK', 'MOVE_RAIN_DANCE']
- party[0].iv_scale: 60 -> 254
- party[1].species: 'SPECIES_MAGNETON' -> 'SPECIES_ROTOM'
- party[1].level: 48 -> 60
- party[1].moves: ['MOVE_THUNDERBOLT', 'MOVE_TRI_ATTACK', 'MOVE_MIRROR_SHOT', 'MOVE_NONE'] -> ['MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_LIGHT_SCREEN', 'MOVE_WILL_O_WISP']
- party[1].iv_scale: 60 -> 253

## res/trainers/data/ace_trainer_ruben.json
- party[0].species: 'SPECIES_NUZLEAF' -> 'SPECIES_SHIFTRY'
- party[0].level: 56 -> 80
- party[0].moves: ['MOVE_EXTRASENSORY', 'MOVE_FAKE_OUT', 'MOVE_FAINT_ATTACK', 'MOVE_RAZOR_LEAF'] -> ['MOVE_EXTRASENSORY', 'MOVE_FAKE_OUT', 'MOVE_SUCKER_PUNCH', 'MOVE_SEED_BOMB']
- party[0].iv_scale: 50 -> 248
- party[1].level: 57 -> 80
- party[1].iv_scale: 50 -> 249

## res/trainers/data/ace_trainer_breanna.json
- party[0].species: 'SPECIES_BRONZOR' -> 'SPECIES_SKARMORY'
- party[0].level: 35 -> 50
- party[0].moves: ['MOVE_GYRO_BALL', 'MOVE_EXTRASENSORY', 'MOVE_CONFUSE_RAY', 'MOVE_NONE'] -> ['MOVE_STEEL_WING', 'MOVE_DRILL_PECK', 'MOVE_STEALTH_ROCK', 'MOVE_ROOST']
- party[0].iv_scale: 60 -> 231
- party[1].species: 'SPECIES_BRONZOR' -> 'SPECIES_PROBOPASS'
- party[1].level: 36 -> 50
- party[1].moves: ['MOVE_GYRO_BALL', 'MOVE_EXTRASENSORY', 'MOVE_CONFUSE_RAY', 'MOVE_NONE'] -> ['MOVE_THUNDERBOLT', 'MOVE_HIDDEN_POWER', 'MOVE_POWER_GEM', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 60 -> 234
- party[2].species: 'SPECIES_BRONZOR' -> 'SPECIES_BRONZONG'
- party[2].level: 38 -> 50
- party[2].moves: ['MOVE_GYRO_BALL', 'MOVE_EXTRASENSORY', 'MOVE_CONFUSE_RAY', 'MOVE_NONE'] -> ['MOVE_GYRO_BALL', 'MOVE_ZEN_HEADBUTT', 'MOVE_CONFUSE_RAY', 'MOVE_IRON_DEFENSE']
- party[2].iv_scale: 60 -> 209

## res/trainers/data/ace_trainer_catherine.json
- party[0].species: 'SPECIES_HAUNTER' -> 'SPECIES_SPIRITOMB'
- party[0].level: 23 -> 29
- party[0].moves: ['MOVE_NIGHT_SHADE', 'MOVE_CONFUSE_RAY', 'MOVE_SUCKER_PUNCH', 'MOVE_CURSE'] -> ['MOVE_FAINT_ATTACK', 'MOVE_HYPNOSIS', 'MOVE_DREAM_EATER', 'MOVE_OMINOUS_WIND']
- party[0].iv_scale: 60 -> 196
- party[1].level: 24 -> 29
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PAIN_SPLIT', 'MOVE_CONFUSE_RAY', 'MOVE_SPITE'] -> ['MOVE_CONFUSE_RAY', 'MOVE_MEAN_LOOK', 'MOVE_PSYBEAM', 'MOVE_PAIN_SPLIT']
- party[1].iv_scale: 60 -> 178

## res/trainers/data/ace_trainer_destiny.json
- party[0].species: 'SPECIES_ELECTABUZZ' -> 'SPECIES_ELECTIVIRE'
- party[0].level: 47 -> 60
- party[0].moves: ['MOVE_THUNDERBOLT', 'MOVE_SHOCK_WAVE', 'MOVE_QUICK_ATTACK', 'MOVE_IRON_TAIL'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_LOW_KICK', 'MOVE_LIGHT_SCREEN', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 60 -> 229
- party[1].species: 'SPECIES_RAICHU' -> 'SPECIES_JOLTEON'
- party[1].level: 48 -> 60
- party[1].moves: ['MOVE_THUNDERBOLT', 'MOVE_DIG', 'MOVE_THUNDER_WAVE', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_SIGNAL_BEAM']
- party[1].iv_scale: 60 -> 211

## res/trainers/data/ace_trainer_jamie.json
- party[0].level: 60 -> 84
- party[0].moves: ['MOVE_METEOR_MASH', 'MOVE_HAMMER_ARM', 'MOVE_PSYCHIC', 'MOVE_MAGNET_RISE'] -> ['MOVE_METEOR_MASH', 'MOVE_HAMMER_ARM', 'MOVE_ZEN_HEADBUTT', 'MOVE_BULLET_PUNCH']
- party[0].iv_scale: 50 -> 247

## res/trainers/data/ace_trainer_maya.json
- party[0].species: 'SPECIES_ROSELIA' -> 'SPECIES_ROSERADE'
- party[0].level: 24 -> 35
- party[0].iv_scale: 50 -> 212
- party[1].species: 'SPECIES_RALTS' -> 'SPECIES_GARDEVOIR'
- party[1].level: 24 -> 35
- party[1].moves: ['MOVE_PSYCHIC', 'MOVE_MAGICAL_LEAF', 'MOVE_CALM_MIND', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_PSYCHIC', 'MOVE_ENERGY_BALL', 'MOVE_CALM_MIND', 'MOVE_THUNDERBOLT']
- party[1].iv_scale: 50 -> 196
- party[2].level: 25 -> 35
- party[2].moves: ['MOVE_SUPERSONIC', 'MOVE_STOMP', 'MOVE_ROLLOUT', 'MOVE_DEFENSE_CURL'] -> ['MOVE_FIRE_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_ZEN_HEADBUTT', 'MOVE_THUNDER_PUNCH']
- party[2].iv_scale: 50 -> 238

## res/trainers/data/psychic_maxwell.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MISDREAVUS' -> 'SPECIES_MISMAGIUS'
- party[0].level: 58 -> 80
- party[0].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_PSYCHIC', 'MOVE_WILL_O_WISP', 'MOVE_THUNDER_WAVE']
- party[0].iv_scale: 0 -> 247
- party[1].species: 'SPECIES_HAUNTER' -> 'SPECIES_SLOWKING'
- party[1].level: 54 -> 80
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_PSYCH_UP']
- party[1].iv_scale: 0 -> 229

## res/trainers/data/psychic_brittney.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_DROWZEE' -> 'SPECIES_HYPNO'
- party[0].level: 55 -> 80
- party[0].moves: None -> ['MOVE_PSYCHO_CUT', 'MOVE_DRAIN_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 0 -> 244
- party[1].level: 57 -> 80
- party[1].moves: None -> ['MOVE_CALM_MIND', 'MOVE_PSYCHIC', 'MOVE_ENERGY_BALL', 'MOVE_FOCUS_BLAST']
- party[1].iv_scale: 0 -> 254

## res/trainers/data/belle_and_pa_ava_and_matt.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_VULPIX'
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_IMPRISON', 'MOVE_FLAMETHROWER', 'MOVE_SAFEGUARD', 'MOVE_PAYBACK']
- party[0].iv_scale: 0 -> 162
- party[1].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[1].level: 24 -> 33
- party[1].moves: None -> ['MOVE_FLAMETHROWER', 'MOVE_QUICK_ATTACK', 'MOVE_CONFUSE_RAY', 'MOVE_SAFEGUARD']
- party[1].iv_scale: 0 -> 219

## res/trainers/data/rancher_marco.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_TAUROS'
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_PURSUIT', 'MOVE_REST', 'MOVE_HEADBUTT', 'MOVE_ZEN_HEADBUTT']
- party[0].iv_scale: 0 -> 197

## res/trainers/data/fisherman_erick.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLDEEN' -> 'SPECIES_LANTURN'
- party[0].level: 28 -> 39
- party[0].moves: ['MOVE_WATER_PULSE', 'MOVE_PECK', 'MOVE_FLAIL', 'MOVE_SUPERSONIC'] -> ['MOVE_THUNDERBOLT', 'MOVE_ICE_BEAM', 'MOVE_SURF', 'MOVE_SIGNAL_BEAM']
- party[0].iv_scale: 10 -> 238
- party[1].species: 'SPECIES_SEAKING' -> 'SPECIES_CRAWDAUNT'
- party[1].level: 31 -> 39
- party[1].moves: ['MOVE_WATER_PULSE', 'MOVE_FURY_ATTACK', 'MOVE_FLAIL', 'MOVE_SUPERSONIC'] -> ['MOVE_KNOCK_OFF', 'MOVE_WATERFALL', 'MOVE_SUPERPOWER', 'MOVE_NIGHT_SLASH']
- party[1].iv_scale: 10 -> 236
- party[2].level: 31 -> 39
- party[2].moves: ['MOVE_THRASH', 'MOVE_BITE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_DRAGON_DANCE', 'MOVE_ICE_FANG', 'MOVE_AQUA_TAIL', 'MOVE_EARTHQUAKE']
- party[2].iv_scale: 10 -> 237

## res/trainers/data/twins_emma_and_lil.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BONSLY' -> 'SPECIES_SUDOWOODO'
- party[0].level: 22 -> 30
- party[0].moves: None -> ['MOVE_MIMIC', 'MOVE_BLOCK', 'MOVE_FAINT_ATTACK', 'MOVE_ROCK_TOMB']
- party[0].iv_scale: 0 -> 213
- party[1].species: 'SPECIES_MIME_JR' -> 'SPECIES_MR_MIME'
- party[1].level: 22 -> 30
- party[1].moves: None -> ['MOVE_LIGHT_SCREEN', 'MOVE_REFLECT', 'MOVE_PSYBEAM', 'MOVE_SUBSTITUTE']
- party[1].iv_scale: 0 -> 200

## res/trainers/data/commander_mars_valley_windworks.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_floaroma_meadow_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_EKANS'
- party[0].level: 13 -> 15
- party[0].moves: None -> ['MOVE_GLARE', 'MOVE_BIDE', 'MOVE_SCREECH', 'MOVE_POISON_FANG']
- party[0].iv_scale: 0 -> 102

## res/trainers/data/galactic_grunt_floaroma_meadow_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 11 -> 15
- party[0].moves: None -> ['MOVE_BITE', 'MOVE_SUPERSONIC', 'MOVE_ASTONISH', 'MOVE_PLUCK']
- party[0].iv_scale: 0 -> 96
- party[1].species: 'SPECIES_ZUBAT' -> 'SPECIES_POOCHYENA'
- party[1].level: 11 -> 15
- party[1].moves: None -> ['MOVE_BITE', 'MOVE_HOWL', 'MOVE_SAND_ATTACK', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 132

## res/trainers/data/galactic_grunt_valley_windworks_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_GRIMER'
- party[0].level: 13 -> 15
- party[0].moves: None -> ['MOVE_POISON_GAS', 'MOVE_POUND', 'MOVE_HARDEN', 'MOVE_MUD_SLAP']
- party[0].iv_scale: 0 -> 117

## res/trainers/data/galactic_grunt_valley_windworks_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_WEEDLE'
- party[0].level: 11 -> 15
- party[0].moves: None -> ['MOVE_POISON_STING', 'MOVE_STRING_SHOT', 'MOVE_BUG_BITE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 122
- party[1].species: 'SPECIES_STUNKY' -> 'SPECIES_CATERPIE'
- party[1].level: 11 -> 15
- party[1].moves: None -> ['MOVE_TACKLE', 'MOVE_STRING_SHOT', 'MOVE_BUG_BITE', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 105

## res/trainers/data/guitarist_tony.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 33 -> 44
- party[0].moves: None -> ['MOVE_X_SCISSOR', 'MOVE_SCREECH', 'MOVE_TAUNT', 'MOVE_NIGHT_SLASH']
- party[0].iv_scale: 0 -> 237
- party[1].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_EXPLOUD'
- party[1].level: 33 -> 44
- party[1].moves: None -> ['MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG', 'MOVE_ICE_FANG', 'MOVE_CRUNCH']
- party[1].iv_scale: 0 -> 232

## res/trainers/data/guitarist_jerry.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/guitarist_jerry.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/guitarist_preston.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/guitarist_preston.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/guitarist_lonnie.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 47 -> 60
- party[0].moves: ['MOVE_THUNDERBOLT', 'MOVE_SLAM', 'MOVE_THUNDER_WAVE', 'MOVE_QUICK_ATTACK'] -> ['MOVE_THUNDERBOLT', 'MOVE_GRASS_KNOT', 'MOVE_THUNDER_WAVE', 'MOVE_NASTY_PLOT']
- party[0].iv_scale: 10 -> 245

## res/trainers/data/ruin_maniac_calvin.json
- party[0].species: 'SPECIES_BRONZOR' -> 'SPECIES_BRONZONG'
- party[0].level: 23 -> 33
- party[0].moves: None -> ['MOVE_EXTRASENSORY', 'MOVE_IRON_DEFENSE', 'MOVE_SAFEGUARD', 'MOVE_ANCIENT_POWER']
- party[0].iv_scale: 0 -> 197
- party[1].species: 'SPECIES_SHIELDON' -> 'SPECIES_BASTIODON'
- party[1].level: 23 -> 33
- party[1].moves: None -> ['MOVE_OUTRAGE', 'MOVE_SWAGGER', 'MOVE_IRON_HEAD', 'MOVE_HEADBUTT']
- party[1].iv_scale: 0 -> 216

## res/trainers/data/ruin_maniac_larry.json
- party[0].level: 57 -> 84
- party[0].moves: None -> ['MOVE_IRON_HEAD', 'MOVE_STONE_EDGE', 'MOVE_THUNDER_FANG', 'MOVE_GIGA_IMPACT']
- party[0].iv_scale: 0 -> 231

## res/trainers/data/jogger_wyatt.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PIKACHU' -> 'SPECIES_MANECTRIC'
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_THUNDER_FANG', 'MOVE_FIRE_FANG', 'MOVE_CRUNCH']
- party[0].iv_scale: 0 -> 195

## res/trainers/data/jogger_craig.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_LUXIO' -> 'SPECIES_LUXRAY'
- party[0].level: 22 -> 34
- party[0].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_ICE_FANG', 'MOVE_ROAR', 'MOVE_SUPERPOWER']
- party[0].iv_scale: 0 -> 237
- party[1].species: 'SPECIES_LUXIO' -> 'SPECIES_PACHIRISU'
- party[1].level: 24 -> 34
- party[1].moves: None -> ['MOVE_THUNDER_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_GUNK_SHOT', 'MOVE_SUPER_FANG']
- party[1].iv_scale: 0 -> 225

## res/trainers/data/jogger_raul.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARAVIA' -> 'SPECIES_SWELLOW'
- party[0].level: 23 -> 31
- party[0].moves: None -> ['MOVE_QUICK_ATTACK', 'MOVE_BRAVE_BIRD', 'MOVE_ROOST', 'MOVE_ENDEAVOR']
- party[0].iv_scale: 0 -> 168

## res/trainers/data/black_belt_colby.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOKE' -> 'SPECIES_TYROGUE'
- party[0].level: 23 -> 33
- party[0].moves: ['MOVE_KARATE_CHOP', 'MOVE_LEER', 'MOVE_FORESIGHT', 'MOVE_NONE'] -> ['MOVE_HI_JUMP_KICK', 'MOVE_MACH_PUNCH', 'MOVE_BULLET_PUNCH', 'MOVE_FAKE_OUT']
- party[0].iv_scale: 40 -> 183
- party[1].level: 25 -> 33
- party[1].moves: ['MOVE_LOW_KICK', 'MOVE_FORESIGHT', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_SUPERPOWER', 'MOVE_FIRE_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_NONE']
- party[1].iv_scale: 40 -> 229
- party[2].species: 'SPECIES_MACHOKE' -> 'SPECIES_HITMONCHAN'
- party[2].level: 27 -> 33
- party[2].moves: ['MOVE_SUBMISSION', 'MOVE_LEER', 'MOVE_FORESIGHT', 'MOVE_NONE'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_MACH_PUNCH', 'MOVE_BULLET_PUNCH']
- party[2].iv_scale: 40 -> 189

## res/trainers/data/black_belt_darren.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MACHOP' -> 'SPECIES_PRIMEAPE'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_KARATE_CHOP', 'MOVE_FORESIGHT', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_CLOSE_COMBAT', 'MOVE_SEED_BOMB', 'MOVE_U_TURN']
- party[0].iv_scale: 40 -> 186
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_CONFUSION', 'MOVE_FORCE_PALM', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HI_JUMP_KICK', 'MOVE_PSYCHO_CUT', 'MOVE_ICE_PUNCH', 'MOVE_NONE']
- party[1].iv_scale: 40 -> 192
- party[2].species: 'SPECIES_MACHOKE' -> 'SPECIES_HITMONLEE'
- party[2].level: 25 -> 35
- party[2].moves: ['MOVE_KARATE_CHOP', 'MOVE_FORESIGHT', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HI_JUMP_KICK', 'MOVE_ROCK_SLIDE', 'MOVE_MACH_PUNCH', 'MOVE_POISON_JAB']
- party[2].iv_scale: 40 -> 241

## res/trainers/data/black_belt_jeffery.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 28 -> 36
- party[0].moves: ['MOVE_BRICK_BREAK', 'MOVE_AERIAL_ACE', 'MOVE_LEER', 'MOVE_NONE'] -> ['MOVE_BRICK_BREAK', 'MOVE_AERIAL_ACE', 'MOVE_BUG_BITE', 'MOVE_NIGHT_SLASH']
- party[0].iv_scale: 40 -> 199

## res/trainers/data/black_belt_carl.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_TYROGUE' -> 'SPECIES_HITMONCHAN'
- party[0].level: 55 -> 82
- party[0].moves: None -> ['MOVE_MEGA_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_CLOSE_COMBAT']
- party[0].iv_scale: 30 -> 222
- party[1].level: 59 -> 82
- party[1].moves: None -> ['MOVE_ENDURE', 'MOVE_MEGA_KICK', 'MOVE_CLOSE_COMBAT', 'MOVE_BLAZE_KICK']
- party[1].iv_scale: 30 -> 223

## res/trainers/data/black_belt_ricky.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 38 -> 51
- party[0].moves: ['MOVE_IRON_TAIL', 'MOVE_TAUNT', 'MOVE_TORMENT', 'MOVE_SCREECH'] -> ['MOVE_IRON_HEAD', 'MOVE_STONE_EDGE', 'MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG']
- party[0].iv_scale: 40 -> 253

## res/trainers/data/leader_gardenia.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_gardenia.json
- items: ['ITEM_SUPER_POTION', 'ITEM_SUPER_POTION'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/leader_wake.json
- party size changed (3 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_wake.json
- items: ['ITEM_HYPER_POTION', 'ITEM_HYPER_POTION'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/leader_maylene.json
- party size changed (3 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_fantina.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_fantina.json
- items: ['ITEM_SUPER_POTION', 'ITEM_SUPER_POTION'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']

## res/trainers/data/leader_candice.json
- party size changed (4 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_candice.json
- items: ['ITEM_HYPER_POTION', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/leader_volkner.json
- party size changed (4 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_volkner.json
- items: ['ITEM_HYPER_POTION', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/lass_madeline.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 8 -> 10
- party[0].moves: None -> ['MOVE_WATER_SPORT', 'MOVE_SCRATCH', 'MOVE_TAIL_WHIP', 'MOVE_WATER_GUN']
- party[0].iv_scale: 0 -> 119

## res/trainers/data/lass_kaitlin.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BIDOOF' -> 'SPECIES_GROWLITHE'
- party[0].level: 4 -> 7
- party[0].moves: None -> ['MOVE_BITE', 'MOVE_ROAR', 'MOVE_EMBER', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 123
- party[1].species: 'SPECIES_BUDEW' -> 'SPECIES_SUNKERN'
- party[1].level: 4 -> 7
- party[1].moves: None -> ['MOVE_MEGA_DRAIN', 'MOVE_GROWTH', 'MOVE_NONE', 'MOVE_NONE']
- party[1].iv_scale: 0 -> 137
- party[2].species: 'SPECIES_STARLY' -> 'SPECIES_TAILLOW'
- party[2].level: 4 -> 7
- party[2].moves: None -> ['MOVE_PECK', 'MOVE_GROWL', 'MOVE_FOCUS_ENERGY', 'MOVE_NONE']
- party[2].iv_scale: 0 -> 138
- party[3].species: 'SPECIES_ABRA' -> 'SPECIES_SPOINK'
- party[3].level: 4 -> 7
- party[3].moves: None -> ['MOVE_HIDDEN_POWER', 'MOVE_PSYWAVE', 'MOVE_NONE', 'MOVE_NONE']
- party[3].iv_scale: 0 -> 119

## res/trainers/data/lass_caroline.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_CHERUBI' -> 'SPECIES_HOPPIP'
- party[0].level: 17 -> 22
- party[0].moves: ['MOVE_TACKLE', 'MOVE_LEECH_SEED', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_STUN_SPORE', 'MOVE_SLEEP_POWDER', 'MOVE_BULLET_SEED', 'MOVE_LEECH_SEED']
- party[0].iv_scale: 20 -> 159
- party[1].species: 'SPECIES_ROSELIA' -> 'SPECIES_SKIPLOOM'
- party[1].level: 17 -> 23
- party[1].moves: ['MOVE_MEGA_DRAIN', 'MOVE_POISON_STING', 'MOVE_STUN_SPORE', 'MOVE_NONE'] -> ['MOVE_POISON_POWDER', 'MOVE_STUN_SPORE', 'MOVE_LEECH_SEED', 'MOVE_BULLET_SEED']
- party[1].iv_scale: 20 -> 182

## res/trainers/data/lass_molly.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 23 -> 29
- party[0].moves: ['MOVE_PAIN_SPLIT', 'MOVE_PSYBEAM', 'MOVE_CONFUSE_RAY', 'MOVE_NONE'] -> ['MOVE_CONFUSE_RAY', 'MOVE_MEAN_LOOK', 'MOVE_PSYBEAM', 'MOVE_PAIN_SPLIT']
- party[0].iv_scale: 10 -> 206

## res/trainers/data/hiker_louis.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_SABLEYE'
- party[0].level: 14 -> 19
- party[0].moves: None -> ['MOVE_NIGHT_SHADE', 'MOVE_ASTONISH', 'MOVE_FURY_SWIPES', 'MOVE_FAKE_OUT']
- party[0].iv_scale: 0 -> 159
- party[1].species: 'SPECIES_ONIX' -> 'SPECIES_MAWILE'
- party[1].level: 18 -> 19
- party[1].moves: None -> ['MOVE_ASTONISH', 'MOVE_FAKE_TEARS', 'MOVE_BITE', 'MOVE_SWEET_SCENT']
- party[1].iv_scale: 0 -> 160

## res/trainers/data/parasol_lady_alexa.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/parasol_lady_alexa.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/parasol_lady_sabrina.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/parasol_lady_sabrina.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/picnicker_diana.json
- party[0].species: 'SPECIES_BIDOOF' -> 'SPECIES_NIDORAN_F'
- party[0].level: 9 -> 10
- party[0].moves: None -> ['MOVE_GROWL', 'MOVE_SCRATCH', 'MOVE_TAIL_WHIP', 'MOVE_DOUBLE_KICK']
- party[0].iv_scale: 0 -> 129

## res/trainers/data/poke_kid_meghan.json
- party size changed (4 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/poke_kid_meghan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/policeman_danny.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_NOCTOWL'
- party[0].level: 26 -> 37
- party[0].moves: None -> ['MOVE_HEAT_WAVE', 'MOVE_TAILWIND', 'MOVE_AIR_SLASH', 'MOVE_PSYCHIC']
- party[0].iv_scale: 0 -> 228
- party[1].species: 'SPECIES_MACHOP' -> 'SPECIES_MACHAMP'
- party[1].level: 28 -> 37
- party[1].moves: None -> ['MOVE_CROSS_CHOP', 'MOVE_POISON_JAB', 'MOVE_BULLET_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[1].iv_scale: 0 -> 232

## res/trainers/data/policeman_thomas.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 43 -> 58
- party[0].moves: None -> ['MOVE_EXTRASENSORY', 'MOVE_HYPNOSIS', 'MOVE_ROOST', 'MOVE_DREAM_EATER']
- party[0].iv_scale: 0 -> 237
- party[1].species: 'SPECIES_MACHOKE' -> 'SPECIES_GALLADE'
- party[1].level: 43 -> 58
- party[1].moves: None -> ['MOVE_NIGHT_SLASH', 'MOVE_DRAIN_PUNCH', 'MOVE_PROTECT', 'MOVE_CLOSE_COMBAT']
- party[1].iv_scale: 0 -> 237

## res/trainers/data/rich_boy_trey.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 57
- party[0].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_CRUNCH', 'MOVE_FIRE_FANG', 'MOVE_SUPERPOWER']
- party[0].iv_scale: 0 -> 247

## res/trainers/data/sailor_marc.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MANTYKE' -> 'SPECIES_MANTINE'
- party[0].level: 45 -> 58
- party[0].moves: None -> ['MOVE_CONFUSE_RAY', 'MOVE_ICE_BEAM', 'MOVE_AQUA_RING', 'MOVE_HYDRO_PUMP']
- party[0].iv_scale: 0 -> 230

## res/trainers/data/sailor_skyler.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MANTYKE' -> 'SPECIES_MANTINE'
- party[0].level: 32 -> 44
- party[0].item: None -> 'ITEM_NONE'
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_PSYBEAM', 'MOVE_CONFUSE_RAY', 'MOVE_SIGNAL_BEAM']
- party[0].iv_scale: 0 -> 240
- party[1].species: 'SPECIES_MACHOKE' -> 'SPECIES_HARIYAMA'
- party[1].level: 34 -> 44
- party[1].item: None -> 'ITEM_SITRUS_BERRY'
- party[1].moves: None -> ['MOVE_BELLY_DRUM', 'MOVE_SUPERPOWER', 'MOVE_FIRE_PUNCH', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 0 -> 245

## res/trainers/data/sailor_damian.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WINGULL' -> 'SPECIES_PELIPPER'
- party[0].level: 31 -> 39
- party[0].moves: ['MOVE_WATER_PULSE', 'MOVE_WING_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_NONE'] -> ['MOVE_SURF', 'MOVE_SKY_ATTACK', 'MOVE_ROOST', 'MOVE_RAIN_DANCE']
- party[0].iv_scale: 10 -> 238
- party[1].species: 'SPECIES_PELIPPER' -> 'SPECIES_CLOYSTER'
- party[1].level: 31 -> 39
- party[1].moves: ['MOVE_WATER_PULSE', 'MOVE_WING_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_NONE'] -> ['MOVE_ICICLE_SPEAR', 'MOVE_ROCK_BLAST', 'MOVE_POISON_JAB', 'MOVE_BRINE']
- party[1].iv_scale: 10 -> 251

## res/trainers/data/school_kid_chance.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GASTLY' -> 'SPECIES_SHEDINJA'
- party[0].level: 23 -> 29
- party[0].moves: ['MOVE_NIGHT_SHADE', 'MOVE_SUCKER_PUNCH', 'MOVE_CONFUSE_RAY', 'MOVE_HYPNOSIS'] -> ['MOVE_FAINT_ATTACK', 'MOVE_NIGHT_SLASH', 'MOVE_BUG_BITE', 'MOVE_SPITE']
- party[0].iv_scale: 10 -> 116

## res/trainers/data/school_kid_forrest.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 47 -> 59
- party[0].moves: ['MOVE_THUNDERBOLT', 'MOVE_TRI_ATTACK', 'MOVE_MIRROR_SHOT', 'MOVE_NONE'] -> ['MOVE_THUNDERBOLT', 'MOVE_TRI_ATTACK', 'MOVE_FLASH_CANNON', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 252

## res/trainers/data/school_kid_harrison.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARLY' -> 'SPECIES_ABRA'
- party[0].level: 6 -> 8
- party[0].moves: ['MOVE_QUICK_ATTACK', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_HIDDEN_POWER', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 128

## res/trainers/data/school_kid_mackenzie.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_DRIFLOON' -> 'SPECIES_SHUPPET'
- party[0].level: 21 -> 26
- party[0].moves: ['MOVE_PAYBACK', 'MOVE_GUST', 'MOVE_ASTONISH', 'MOVE_MINIMIZE'] -> ['MOVE_CURSE', 'MOVE_SPITE', 'MOVE_SHADOW_SNEAK', 'MOVE_WILL_O_WISP']
- party[0].iv_scale: 10 -> 185
- party[1].species: 'SPECIES_DRIFLOON' -> 'SPECIES_DUSKULL'
- party[1].level: 21 -> 26
- party[1].moves: ['MOVE_SPIT_UP', 'MOVE_SWALLOW', 'MOVE_STOCKPILE', 'MOVE_NONE'] -> ['MOVE_ASTONISH', 'MOVE_CONFUSE_RAY', 'MOVE_SHADOW_SNEAK', 'MOVE_PURSUIT']
- party[1].iv_scale: 10 -> 186

## res/trainers/data/school_kid_tiera.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 47 -> 59
- party[0].moves: ['MOVE_LAST_RESORT', 'MOVE_SUPER_FANG', 'MOVE_DISCHARGE', 'MOVE_SWEET_KISS'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_SUPER_FANG', 'MOVE_SEED_BOMB', 'MOVE_SWEET_KISS']
- party[0].iv_scale: 10 -> 248

## res/trainers/data/school_kid_christine.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BIDOOF' -> 'SPECIES_RALTS'
- party[0].level: 6 -> 8
- party[0].moves: None -> ['MOVE_CONFUSION', 'MOVE_GROWL', 'MOVE_HIDDEN_POWER', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 98

## res/trainers/data/beauty_cyndy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_PERSIAN'
- party[0].level: 29 -> 37
- party[0].moves: None -> ['MOVE_GUNK_SHOT', 'MOVE_SHADOW_CLAW', 'MOVE_SEED_BOMB', 'MOVE_SLASH']
- party[0].iv_scale: 0 -> 218

## res/trainers/data/youngster_dallas.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 8 -> 10
- party[0].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_THUNDER_WAVE', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 114

## res/trainers/data/youngster_sebastian.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 8 -> 10
- party[0].moves: ['MOVE_LOW_KICK', 'MOVE_LEER', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_LOW_KICK', 'MOVE_LEER', 'MOVE_KARATE_CHOP', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 154

## res/trainers/data/youngster_donny.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 20 -> 27
- party[0].moves: ['MOVE_SUCKER_PUNCH', 'MOVE_NIGHT_SHADE', 'MOVE_CONFUSE_RAY', 'MOVE_CURSE'] -> ['MOVE_NIGHT_SHADE', 'MOVE_CONFUSE_RAY', 'MOVE_SUCKER_PUNCH', 'MOVE_HYPNOSIS']
- party[0].iv_scale: 10 -> 195
- party[1].level: 22 -> 27
- party[1].moves: ['MOVE_SPIT_UP', 'MOVE_SWALLOW', 'MOVE_STOCKPILE', 'MOVE_NONE'] -> ['MOVE_PAYBACK', 'MOVE_STOCKPILE', 'MOVE_SWALLOW', 'MOVE_SPIT_UP']
- party[1].iv_scale: 10 -> 152

## res/trainers/data/tuber_trenton.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SHELLOS' -> 'SPECIES_GASTRODON'
- party[0].level: 31 -> 43
- party[0].moves: None -> ['MOVE_HIDDEN_POWER', 'MOVE_RAIN_DANCE', 'MOVE_SLUDGE_BOMB', 'MOVE_MUDDY_WATER']
- party[0].iv_scale: 0 -> 230
- party[1].species: 'SPECIES_SHELLOS' -> 'SPECIES_DEWGONG'
- party[1].level: 33 -> 43
- party[1].moves: None -> ['MOVE_SHEER_COLD', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_AQUA_TAIL']
- party[1].iv_scale: 0 -> 245

## res/trainers/data/tuber_conner.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_REMORAID' -> 'SPECIES_OCTILLERY'
- party[0].level: 44 -> 58
- party[0].moves: None -> ['MOVE_WRING_OUT', 'MOVE_SIGNAL_BEAM', 'MOVE_ICE_BEAM', 'MOVE_HYPER_BEAM']
- party[0].iv_scale: 0 -> 255

## res/trainers/data/tuber_mariel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MARILL' -> 'SPECIES_AZUMARILL'
- party[0].level: 31 -> 43
- party[0].moves: None -> ['MOVE_LIGHT_SCREEN', 'MOVE_SURF', 'MOVE_FOCUS_BLAST', 'MOVE_ICE_BEAM']
- party[0].iv_scale: 0 -> 250
- party[1].species: 'SPECIES_MARILL' -> 'SPECIES_GASTRODON'
- party[1].form: 0 -> 1
- party[1].level: 33 -> 43
- party[1].moves: None -> ['MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_STONE_EDGE', 'MOVE_SANDSTORM']
- party[1].iv_scale: 0 -> 239

## res/trainers/data/tuber_holly.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_REMORAID' -> 'SPECIES_KINGDRA'
- party[0].level: 44 -> 59
- party[0].moves: None -> ['MOVE_OUTRAGE', 'MOVE_IRON_HEAD', 'MOVE_DRAGON_DANCE', 'MOVE_WATERFALL']
- party[0].iv_scale: 0 -> 210

## res/trainers/data/veteran_armando.json
- party[0].level: 53 -> 80
- party[0].moves: ['MOVE_ACID_ARMOR', 'MOVE_TOXIC', 'MOVE_SLUDGE_BOMB', 'MOVE_DARK_PULSE'] -> ['MOVE_DIG', 'MOVE_TOXIC', 'MOVE_GUNK_SHOT', 'MOVE_MINIMIZE']
- party[0].iv_scale: 100 -> 255
- party[1].level: 53 -> 80
- party[1].moves: ['MOVE_SUCKER_PUNCH', 'MOVE_TAUNT', 'MOVE_ASSURANCE', 'MOVE_TAKE_DOWN'] -> ['MOVE_SUCKER_PUNCH', 'MOVE_POISON_FANG', 'MOVE_ICE_FANG', 'MOVE_THUNDER_FANG']
- party[1].iv_scale: 100 -> 248
- party[2].species: 'SPECIES_LICKITUNG' -> 'SPECIES_LICKILICKY'
- party[2].level: 56 -> 80
- party[2].iv_scale: 100 -> 194

## res/trainers/data/waitress_kati.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_ABSOL'
- party[0].level: 25 -> 33
- party[0].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_SWORDS_DANCE', 'MOVE_ZEN_HEADBUTT', 'MOVE_SUPERPOWER']
- party[0].iv_scale: 0 -> 203

## res/trainers/data/worker_gerardo.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_FORRETRESS'
- party[0].level: 35 -> 49
- party[0].moves: ['MOVE_SUPERSONIC', 'MOVE_MAGNET_BOMB', 'MOVE_SPARK', 'MOVE_NONE'] -> ['MOVE_SELFDESTRUCT', 'MOVE_STEALTH_ROCK', 'MOVE_GYRO_BALL', 'MOVE_TOXIC_SPIKES']
- party[0].iv_scale: 10 -> 223
- party[1].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_MAWILE'
- party[1].level: 35 -> 49
- party[1].moves: ['MOVE_THUNDER_WAVE', 'MOVE_MAGNET_BOMB', 'MOVE_SPARK', 'MOVE_NONE'] -> ['MOVE_THUNDER_FANG', 'MOVE_BRICK_BREAK', 'MOVE_FIRE_FANG', 'MOVE_IRON_HEAD']
- party[1].iv_scale: 10 -> 219

## res/trainers/data/battle_girl_tyler.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MEDICHAM' -> 'SPECIES_BRELOOM'
- party[0].level: 38 -> 48
- party[0].moves: None -> ['MOVE_SKY_UPPERCUT', 'MOVE_THUNDER_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_SPORE']
- party[0].iv_scale: 30 -> 251

## res/trainers/data/bird_keeper_autumn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MURKROW' -> 'SPECIES_HONCHKROW'
- party[0].level: 54 -> 78
- party[0].moves: None -> ['MOVE_SWAGGER', 'MOVE_SUPERPOWER', 'MOVE_NIGHT_SLASH', 'MOVE_BRAVE_BIRD']
- party[0].iv_scale: 0 -> 251
- party[1].level: 54 -> 78
- party[1].moves: None -> ['MOVE_OMINOUS_WIND', 'MOVE_HEAT_WAVE', 'MOVE_HIDDEN_POWER', 'MOVE_PSYCHIC']
- party[1].iv_scale: 0 -> 239

## res/trainers/data/camper_zackary.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']
- party[0].species: 'SPECIES_AIPOM' -> 'SPECIES_CASTFORM'
- party[0].level: 14 -> 15
- party[0].moves: None -> ['MOVE_RAIN_DANCE', 'MOVE_WATER_PULSE', 'MOVE_NONE', 'MOVE_POWDER_SNOW']
- party[0].iv_scale: 0 -> 165

## res/trainers/data/camper_lawrence.json
- party[0].species: 'SPECIES_AIPOM' -> 'SPECIES_AMBIPOM'
- party[0].level: 34 -> 46
- party[0].moves: None -> ['MOVE_FAKE_OUT', 'MOVE_HEADBUTT', 'MOVE_LOW_KICK', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 0 -> 232
- party[1].level: 36 -> 46
- party[1].moves: None -> ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_PUNCH', 'MOVE_LOW_KICK']
- party[1].iv_scale: 0 -> 223

## res/trainers/data/camper_diego.json
- party[0].level: 22 -> 25
- party[0].moves: None -> ['MOVE_TICKLE', 'MOVE_FURY_SWIPES', 'MOVE_SWIFT', 'MOVE_SCREECH']
- party[0].iv_scale: 0 -> 152

## res/trainers/data/camper_parker.json
- party[0].level: 20 -> 24
- party[0].iv_scale: 0 -> 182
- party[1].species: 'SPECIES_SHINX' -> 'SPECIES_LUXIO'
- party[1].level: 20 -> 24
- party[1].iv_scale: 0 -> 157

## res/trainers/data/collector_dean.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].level: 27 -> 37
- party[0].moves: None -> ['MOVE_TOXIC', 'MOVE_QUICK_ATTACK', 'MOVE_CONFUSE_RAY', 'MOVE_SUCKER_PUNCH']
- party[0].iv_scale: 0 -> 253
- party[1].level: 27 -> 37
- party[1].moves: None -> ['MOVE_SIGNAL_BEAM', 'MOVE_SHADOW_BALL', 'MOVE_SWIFT', 'MOVE_PSYCHIC']
- party[1].iv_scale: 0 -> 248

## res/trainers/data/collector_jamal.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PORYGON' -> 'SPECIES_PORYGON2'
- party[0].level: 27 -> 35
- party[0].moves: None -> ['MOVE_RECOVER', 'MOVE_THUNDERBOLT', 'MOVE_PSYCHIC', 'MOVE_RECYCLE']
- party[0].iv_scale: 0 -> 248

## res/trainers/data/collector_terry.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GIBLE' -> 'SPECIES_BAGON'
- party[0].level: 22 -> 25
- party[0].moves: None -> ['MOVE_LEER', 'MOVE_HEADBUTT', 'MOVE_FOCUS_ENERGY', 'MOVE_EMBER']
- party[0].iv_scale: 0 -> 161

## res/trainers/data/dragon_tamer_joe.json
- party[0].species: 'SPECIES_DRATINI' -> 'SPECIES_DRAGONITE'
- party[0].level: 52 -> 78
- party[0].moves: None -> ['MOVE_DRAGON_DANCE', 'MOVE_WING_ATTACK', 'MOVE_OUTRAGE', 'MOVE_WATERFALL']
- party[0].iv_scale: 50 -> 210
- party[1].species: 'SPECIES_GABITE' -> 'SPECIES_GARCHOMP'
- party[1].level: 56 -> 78
- party[1].moves: None -> ['MOVE_DRAGON_CLAW', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_FIRE_FANG']
- party[1].iv_scale: 50 -> 215

## res/trainers/data/ace_trainer_jonah.json
- party[0].species: 'SPECIES_QUAGSIRE' -> 'SPECIES_HIPPOWDON'
- party[0].level: 35 -> 47
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_THUNDER_FANG', 'MOVE_CRUNCH', 'MOVE_FIRE_FANG']
- party[0].iv_scale: 50 -> 251
- party[1].species: 'SPECIES_STARAPTOR' -> 'SPECIES_QUAGSIRE'
- party[1].level: 36 -> 47
- party[1].moves: None -> ['MOVE_WATERFALL', 'MOVE_YAWN', 'MOVE_EARTHQUAKE', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 50 -> 245
- party[2].species: 'SPECIES_HIPPOPOTAS' -> 'SPECIES_TORTERRA'
- party[2].level: 38 -> 47
- party[2].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED', 'MOVE_SEED_BOMB', 'MOVE_CRUNCH']
- party[2].iv_scale: 50 -> 255

## res/trainers/data/ace_trainer_micah.json
- party[0].species: 'SPECIES_METANG' -> 'SPECIES_METAGROSS'
- party[0].level: 55 -> 78
- party[0].iv_scale: 50 -> 236
- party[1].level: 56 -> 78
- party[1].moves: ['MOVE_WATER_PULSE', 'MOVE_ZEN_HEADBUTT', 'MOVE_ENERGY_BALL', 'MOVE_FAKE_OUT'] -> ['MOVE_WATERFALL', 'MOVE_ZEN_HEADBUTT', 'MOVE_SEED_BOMB', 'MOVE_FAKE_OUT']
- party[1].iv_scale: 50 -> 243

## res/trainers/data/ace_trainer_arthur.json
- party[0].level: 54 -> 78
- party[0].moves: ['MOVE_MUDDY_WATER', 'MOVE_RECOVER', 'MOVE_TOXIC', 'MOVE_WATER_PULSE'] -> ['MOVE_MUDDY_WATER', 'MOVE_RECOVER', 'MOVE_TOXIC', 'MOVE_EARTH_POWER']
- party[0].iv_scale: 50 -> 248
- party[1].level: 54 -> 78
- party[1].iv_scale: 50 -> 245
- party[2].level: 55 -> 78
- party[2].moves: ['MOVE_THUNDERBOLT', 'MOVE_HYPER_BEAM', 'MOVE_ENDURE', 'MOVE_EXPLOSION'] -> ['MOVE_THUNDERBOLT', 'MOVE_HYPER_BEAM', 'MOVE_HIDDEN_POWER', 'MOVE_EXPLOSION']
- party[2].iv_scale: 50 -> 236

## res/trainers/data/ace_trainer_brenda.json
- party[0].level: 38 -> 47
- party[0].moves: None -> ['MOVE_LOW_KICK', 'MOVE_DIZZY_PUNCH', 'MOVE_FAKE_OUT', 'MOVE_BOUNCE']
- party[0].iv_scale: 50 -> 247
- party[1].species: 'SPECIES_KIRLIA' -> 'SPECIES_GARDEVOIR'
- party[1].level: 36 -> 47
- party[1].moves: None -> ['MOVE_CALM_MIND', 'MOVE_PSYCHIC', 'MOVE_FOCUS_BLAST', 'MOVE_SIGNAL_BEAM']
- party[1].iv_scale: 50 -> 234
- party[2].level: 35 -> 47
- party[2].moves: None -> ['MOVE_ZEN_HEADBUTT', 'MOVE_HI_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_BULLET_PUNCH']
- party[2].iv_scale: 50 -> 246

## res/trainers/data/ace_trainer_brandi.json
- party[0].level: 54 -> 78
- party[0].moves: ['MOVE_BONE_RUSH', 'MOVE_STONE_EDGE', 'MOVE_SWORDS_DANCE', 'MOVE_ENDEAVOR'] -> ['MOVE_EARTHQUAKE', 'MOVE_STONE_EDGE', 'MOVE_SWORDS_DANCE', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 50 -> 248
- party[1].level: 57 -> 78
- party[1].iv_scale: 50 -> 251

## res/trainers/data/ace_trainer_clarice.json
- party[0].level: 53 -> 78
- party[0].iv_scale: 50 -> 237
- party[1].level: 54 -> 78
- party[1].iv_scale: 50 -> 243
- party[2].level: 56 -> 78
- party[2].moves: ['MOVE_FLASH_CANNON', 'MOVE_MIRROR_COAT', 'MOVE_DISCHARGE', 'MOVE_HYPER_BEAM'] -> ['MOVE_FLASH_CANNON', 'MOVE_MIRROR_COAT', 'MOVE_THUNDERBOLT', 'MOVE_HYPER_BEAM']
- party[2].iv_scale: 50 -> 252

## res/trainers/data/psychic_kody.json
- party[0].species: 'SPECIES_MEDITITE' -> 'SPECIES_SLOWPOKE'
- party[0].level: 17 -> 18
- party[0].moves: ['MOVE_CONFUSION', 'MOVE_BIDE', 'MOVE_MEDITATE', 'MOVE_NONE'] -> ['MOVE_YAWN', 'MOVE_GROWL', 'MOVE_WATER_GUN', 'MOVE_CONFUSION']
- party[0].iv_scale: 20 -> 159

## res/trainers/data/psychic_landon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SHUPPET' -> 'SPECIES_BANETTE'
- party[0].level: 53 -> 78
- party[0].iv_scale: 0 -> 251
- party[1].level: 55 -> 78
- party[1].moves: ['MOVE_PSYCHIC', 'MOVE_FUTURE_SIGHT', 'MOVE_RECOVER', 'MOVE_FOCUS_BLAST'] -> ['MOVE_PSYCHIC', 'MOVE_ENERGY_BALL', 'MOVE_RECOVER', 'MOVE_FOCUS_BLAST']
- party[1].iv_scale: 0 -> 242

## res/trainers/data/psychic_deandre.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 56 -> 78
- party[0].iv_scale: 0 -> 253

## res/trainers/data/psychic_rachael.json
- party[0].species: 'SPECIES_PSYDUCK' -> 'SPECIES_CHINGLING'
- party[0].level: 17 -> 18
- party[0].moves: ['MOVE_CONFUSION', 'MOVE_WATER_GUN', 'MOVE_SCRATCH', 'MOVE_NONE'] -> ['MOVE_GROWL', 'MOVE_RECOVER', 'MOVE_CONFUSION', 'MOVE_UPROAR']
- party[0].iv_scale: 20 -> 149

## res/trainers/data/psychic_desiree.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 54 -> 78
- party[0].moves: ['MOVE_PSYCHIC', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN', 'MOVE_DRAIN_PUNCH'] -> ['MOVE_PSYCHIC', 'MOVE_MAGICAL_LEAF', 'MOVE_LIGHT_SCREEN', 'MOVE_REFLECT']
- party[0].iv_scale: 0 -> 242
- party[1].level: 54 -> 78
- party[1].moves: ['MOVE_SHADOW_BALL', 'MOVE_MAGICAL_LEAF', 'MOVE_AERIAL_ACE', 'MOVE_SHOCK_WAVE'] -> ['MOVE_SHADOW_BALL', 'MOVE_ENERGY_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_THUNDERBOLT']
- party[1].iv_scale: 0 -> 241

## res/trainers/data/psychic_kendra.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/psychic_kendra.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/fisherman_walter.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 33 -> 39
- party[0].moves: ['MOVE_WATER_PULSE', 'MOVE_MAGNITUDE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_AQUA_TAIL', 'MOVE_MAGNITUDE', 'MOVE_ZEN_HEADBUTT', 'MOVE_NONE']
- party[0].iv_scale: 10 -> 239

## res/trainers/data/galactic_boss_cyrus_galactic_hq.json
- party size changed (3 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_boss_cyrus_galactic_hq.json
- items: ['ITEM_HYPER_POTION', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/galactic_boss_cyrus_distortion_world.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_boss_cyrus_distortion_world.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/commander_mars_lake_verity.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/commander_jupiter_team_galactic_eterna_building.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/commander_jupiter_team_galactic_eterna_building.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']

## res/trainers/data/commander_jupiter_spear_pillar.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/commander_saturn_valor_cavern.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/commander_saturn_valor_cavern.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_HARRASSMENT']

## res/trainers/data/commander_saturn_galactic_hq.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_team_galactic_eterna_building_1f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_GLAMEOW'
- party[0].level: 17 -> 24
- party[0].moves: None -> ['MOVE_GROWL', 'MOVE_HYPNOSIS', 'MOVE_FAINT_ATTACK', 'MOVE_FURY_SWIPES']
- party[0].iv_scale: 0 -> 199
- party[1].species: 'SPECIES_STUNKY' -> 'SPECIES_SKITTY'
- party[1].level: 17 -> 24
- party[1].moves: None -> ['MOVE_SING', 'MOVE_DOUBLE_SLAP', 'MOVE_COPYCAT', 'MOVE_ASSIST']
- party[1].iv_scale: 0 -> 194

## res/trainers/data/galactic_grunt_team_galactic_eterna_building_2f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 19 -> 24
- party[0].moves: None -> ['MOVE_PURSUIT', 'MOVE_FAINT_ATTACK', 'MOVE_WAKE_UP_SLAP', 'MOVE_SWAGGER']
- party[0].iv_scale: 0 -> 161

## res/trainers/data/galactic_grunt_jubilife_city_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 11 -> 13
- party[0].moves: None -> ['MOVE_SCRATCH', 'MOVE_POISON_GAS', 'MOVE_SCREECH', 'MOVE_FURY_SWIPES']
- party[0].iv_scale: 0 -> 118

## res/trainers/data/galactic_grunt_jubilife_city_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 11 -> 13
- party[0].moves: None -> ['MOVE_FAKE_OUT', 'MOVE_SCRATCH', 'MOVE_GROWL', 'MOVE_HYPNOSIS']
- party[0].iv_scale: 0 -> 120

## res/trainers/data/galactic_grunt_celestic_town.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOUNDOUR' -> 'SPECIES_HOUNDOOM'
- party[0].level: 32 -> 43
- party[0].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_SUCKER_PUNCH', 'MOVE_FIRE_FANG', 'MOVE_ROAR']
- party[0].iv_scale: 30 -> 240
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_ARMALDO'
- party[1].level: 30 -> 43
- party[1].moves: None -> ['MOVE_ROCK_POLISH', 'MOVE_X_SCISSOR', 'MOVE_CROSS_POISON', 'MOVE_STONE_EDGE']
- party[1].iv_scale: 30 -> 243

## res/trainers/data/galactic_grunt_lake_valor_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_MUK'
- party[0].level: 37 -> 50
- party[0].moves: None -> ['MOVE_GUNK_SHOT', 'MOVE_ICE_PUNCH', 'MOVE_SHADOW_PUNCH', 'MOVE_SHADOW_SNEAK']
- party[0].iv_scale: 30 -> 222

## res/trainers/data/galactic_grunt_lake_valor_2.json
- party size changed (4 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_lake_valor_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_lake_verity_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CROAGUNK' -> 'SPECIES_NIDOKING'
- party[0].level: 37 -> 50
- party[0].moves: None -> ['MOVE_SURF', 'MOVE_SLUDGE_BOMB', 'MOVE_THUNDERBOLT', 'MOVE_EARTH_POWER']
- party[0].iv_scale: 30 -> 220

## res/trainers/data/galactic_grunt_lake_verity_3.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_lake_verity_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_team_galactic_eterna_building_1f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_STUNKY'
- party[0].level: 16 -> 24
- party[0].moves: None -> ['MOVE_POISON_GAS', 'MOVE_SMOKE_SCREEN', 'MOVE_FEINT', 'MOVE_SLASH']
- party[0].iv_scale: 0 -> 185
- party[1].species: 'SPECIES_GLAMEOW' -> 'SPECIES_KOFFING'
- party[1].level: 18 -> 24
- party[1].moves: None -> ['MOVE_SMOKE_SCREEN', 'MOVE_ASSURANCE', 'MOVE_SELFDESTRUCT', 'MOVE_SLUDGE']
- party[1].iv_scale: 0 -> 148

## res/trainers/data/galactic_grunt_team_galactic_eterna_building_2f_2.json
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_NIDORINA'
- party[0].level: 19 -> 24
- party[0].moves: None -> ['MOVE_DOUBLE_KICK', 'MOVE_POISON_STING', 'MOVE_SUPER_FANG', 'MOVE_BITE']
- party[0].iv_scale: 0 -> 204

## res/trainers/data/galactic_grunt_team_galactic_eterna_building_3f.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_SKORUPI'
- party[0].level: 16 -> 24
- party[0].moves: None -> ['MOVE_KNOCK_OFF', 'MOVE_PIN_MISSILE', 'MOVE_ACUPRESSURE', 'MOVE_SCARY_FACE']
- party[0].iv_scale: 0 -> 197
- party[1].species: 'SPECIES_CROAGUNK' -> 'SPECIES_SEVIPER'
- party[1].level: 16 -> 24
- party[1].moves: None -> ['MOVE_LICK', 'MOVE_BITE', 'MOVE_POISON_TAIL', 'MOVE_SCREECH']
- party[1].iv_scale: 0 -> 205
- party[2].species: 'SPECIES_GLAMEOW' -> 'SPECIES_BEEDRILL'
- party[2].level: 16 -> 24
- party[2].moves: None -> ['MOVE_FOCUS_ENERGY', 'MOVE_TWINEEDLE', 'MOVE_RAGE', 'MOVE_PURSUIT']
- party[2].iv_scale: 0 -> 169

## res/trainers/data/galactic_grunt_lake_valor_3.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_lake_valor_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_lake_verity_2.json
- party size changed (3 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_lake_verity_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_lake_verity_4.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_lake_verity_4.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_galactic_hq_1f.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_galactic_hq_1f.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_galactic_hq_2f_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_HOUNDOOM'
- party[0].level: 39 -> 54
- party[0].moves: None -> ['MOVE_FLAMETHROWER', 'MOVE_SOLAR_BEAM', 'MOVE_DARK_PULSE', 'MOVE_SUNNY_DAY']
- party[0].iv_scale: 30 -> 233
- party[1].species: 'SPECIES_HOUNDOUR' -> 'SPECIES_VICTREEBEL'
- party[1].level: 39 -> 54
- party[1].moves: None -> ['MOVE_SOLAR_BEAM', 'MOVE_WEATHER_BALL', 'MOVE_SYNTHESIS', 'MOVE_SLUDGE_BOMB']
- party[1].iv_scale: 30 -> 237

## res/trainers/data/ruin_maniac_harry.json
- party[1].species: 'SPECIES_BRONZOR' -> 'SPECIES_SHIELDON'
- party[2].species: 'SPECIES_BRONZOR' -> 'SPECIES_CRANIDOS'

## res/trainers/data/ruin_maniac_gerald.json
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_BRONZOR'
- party[0].level: 19 -> 25
- party[0].moves: None -> ['MOVE_HYPNOSIS', 'MOVE_IMPRISON', 'MOVE_CONFUSE_RAY', 'MOVE_EXTRASENSORY']
- party[0].iv_scale: 0 -> 147
- party[1].species: 'SPECIES_BRONZOR' -> 'SPECIES_GRAVELER'
- party[1].level: 21 -> 25
- party[1].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_MAGNITUDE', 'MOVE_SELFDESTRUCT', 'MOVE_ROLLOUT']
- party[1].iv_scale: 0 -> 139

## res/trainers/data/black_belt_miles.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/black_belt_miles.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/black_belt_kendal.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 38 -> 48
- party[0].moves: None -> ['MOVE_SLUDGE_BOMB', 'MOVE_DARK_PULSE', 'MOVE_MUD_BOMB', 'MOVE_VACUUM_WAVE']
- party[0].iv_scale: 30 -> 251

## res/trainers/data/black_belt_eddie.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_MANKEY' -> 'SPECIES_PRIMEAPE'
- party[0].level: 51 -> 78
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_THRASH', 'MOVE_POISON_JAB', 'MOVE_CLOSE_COMBAT']
- party[0].iv_scale: 30 -> 247
- party[1].species: 'SPECIES_MACHOKE' -> 'SPECIES_BRELOOM'
- party[1].level: 53 -> 78
- party[1].moves: None -> ['MOVE_SPORE', 'MOVE_THUNDER_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_DYNAMIC_PUNCH']
- party[1].iv_scale: 30 -> 255
- party[2].level: 55 -> 78
- party[2].moves: None -> ['MOVE_CLOSE_COMBAT', 'MOVE_FAKE_OUT', 'MOVE_THUNDER_PUNCH', 'MOVE_FLARE_BLITZ']
- party[2].iv_scale: 30 -> 237

## res/trainers/data/black_belt_willie.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 54 -> 78
- party[0].moves: None -> ['MOVE_CLOSE_COMBAT', 'MOVE_REVERSAL', 'MOVE_STONE_EDGE', 'MOVE_MEGAHORN']
- party[0].iv_scale: 30 -> 241
- party[1].species: 'SPECIES_MACHAMP' -> 'SPECIES_HITMONTOP'
- party[1].level: 54 -> 78
- party[1].moves: None -> ['MOVE_BULLET_PUNCH', 'MOVE_DETECT', 'MOVE_CLOSE_COMBAT', 'MOVE_ENDEAVOR']
- party[1].iv_scale: 30 -> 255

## res/trainers/data/lass_cassidy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 22 -> 24
- party[0].moves: None -> ['MOVE_ENDURE', 'MOVE_RETURN', 'MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK']
- party[0].iv_scale: 0 -> 138

## res/trainers/data/hiker_theodore.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_ONIX' -> 'SPECIES_LARVITAR'
- party[0].level: 18 -> 20
- party[0].moves: None -> ['MOVE_BITE', 'MOVE_SANDSTORM', 'MOVE_SCREECH', 'MOVE_ROCK_SLIDE']
- party[0].iv_scale: 0 -> 251
- party[1].level: 20 -> 21
- party[1].moves: None -> ['MOVE_SCREECH', 'MOVE_ROCK_THROW', 'MOVE_RAGE', 'MOVE_ROCK_TOMB']
- party[1].iv_scale: 0 -> 156

## res/trainers/data/hiker_damon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_NOSEPASS' -> 'SPECIES_PROBOPASS'
- party[0].level: 35 -> 46
- party[0].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_FLASH_CANNON', 'MOVE_SANDSTORM', 'MOVE_ANCIENT_POWER']
- party[0].iv_scale: 0 -> 195
- party[1].species: 'SPECIES_ONIX' -> 'SPECIES_AGGRON'
- party[1].level: 33 -> 46
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_IRON_HEAD', 'MOVE_FIRE_PUNCH', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 0 -> 245
- party[2].species: 'SPECIES_STEELIX' -> 'SPECIES_SUDOWOODO'
- party[2].level: 34 -> 46
- party[2].moves: None -> ['MOVE_WOOD_HAMMER', 'MOVE_LOW_KICK', 'MOVE_ROCK_SLIDE', 'MOVE_THUNDER_PUNCH']
- party[2].iv_scale: 0 -> 197

## res/trainers/data/hiker_reginald.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_BONSLY'
- party[0].level: 20 -> 25
- party[0].moves: None -> ['MOVE_ROCK_THROW', 'MOVE_MIMIC', 'MOVE_BLOCK', 'MOVE_FAINT_ATTACK']
- party[0].iv_scale: 0 -> 158
- party[1].species: 'SPECIES_GEODUDE' -> 'SPECIES_PHANPY'
- party[1].level: 20 -> 25
- party[1].moves: None -> ['MOVE_TAKE_DOWN', 'MOVE_ROLLOUT', 'MOVE_NATURAL_GIFT', 'MOVE_SLAM']
- party[1].iv_scale: 0 -> 137

## res/trainers/data/hiker_lorenzo.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 22 -> 26
- party[0].moves: None -> ['MOVE_RAGE', 'MOVE_ROCK_TOMB', 'MOVE_SANDSTORM', 'MOVE_SLAM']
- party[0].iv_scale: 0 -> 116

## res/trainers/data/picnicker_karina.json
- party[0].level: 14 -> 16
- party[0].moves: ['MOVE_BUBBLE', 'MOVE_PECK', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_BUBBLE', 'MOVE_PECK', 'MOVE_YAWN', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 118

## res/trainers/data/picnicker_summer.json
- party[0].level: 37 -> 46
- party[0].moves: None -> ['MOVE_THUNDER_WAVE', 'MOVE_GRASS_KNOT', 'MOVE_SIGNAL_BEAM', 'MOVE_THUNDERBOLT']
- party[0].iv_scale: 0 -> 247

## res/trainers/data/picnicker_tori.json
- party[0].species: 'SPECIES_PSYDUCK' -> 'SPECIES_SLOWPOKE'
- party[0].level: 22 -> 24
- party[0].moves: None -> ['MOVE_GROWL', 'MOVE_WATER_GUN', 'MOVE_CONFUSION', 'MOVE_DISABLE']
- party[0].iv_scale: 0 -> 149

## res/trainers/data/picnicker_ana.json
- party[0].species: 'SPECIES_HOOTHOOT' -> 'SPECIES_NOCTOWL'
- party[0].level: 22 -> 24
- party[0].moves: None -> ['MOVE_PECK', 'MOVE_UPROAR', 'MOVE_REFLECT', 'MOVE_CONFUSION']
- party[0].iv_scale: 0 -> 172

## res/trainers/data/rival_route_209_piplup.json
- party[0].level: 25 -> 32
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_WING_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM']
- party[0].iv_scale: 50 -> 200
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_BUIZEL' -> 'SPECIES_STARYU'
- party[1].level: 23 -> 32
- party[1].item: None -> 'ITEM_NONE'
- party[1].moves: ['MOVE_WATER_GUN', 'MOVE_QUICK_ATTACK', 'MOVE_PURSUIT', 'MOVE_GROWL'] -> ['MOVE_BUBBLE_BEAM', 'MOVE_SIGNAL_BEAM', 'MOVE_CAMOUFLAGE', 'MOVE_RECOVER']
- party[1].iv_scale: 50 -> 196
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_PONYTA' -> 'SPECIES_VULPIX'
- party[2].level: 23 -> 32
- party[2].item: None -> 'ITEM_NONE'
- party[2].moves: ['MOVE_EMBER', 'MOVE_TACKLE', 'MOVE_TAIL_WHIP', 'MOVE_GROWL'] -> ['MOVE_FLAMETHROWER', 'MOVE_WILL_O_WISP', 'MOVE_ENERGY_BALL', 'MOVE_CONFUSE_RAY']
- party[2].iv_scale: 50 -> 177
- party[2].ability/gender: 0/None -> 1/None
- party[3].level: 27 -> 33
- party[3].item: None -> 'ITEM_SITRUS_BERRY'
- party[3].moves: ['MOVE_RAZOR_LEAF', 'MOVE_TACKLE', 'MOVE_ABSORB', 'MOVE_WITHDRAW'] -> ['MOVE_SEED_BOMB', 'MOVE_CURSE', 'MOVE_BITE', 'MOVE_LEECH_SEED']
- party[3].iv_scale: 50 -> 198
- party[3].ability/gender: 0/None -> 1/None

## res/trainers/data/rival_route_209_turtwig.json
- party[0].level: 25 -> 32
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_WING_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM']
- party[0].iv_scale: 50 -> 200
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_BUIZEL' -> 'SPECIES_STARYU'
- party[1].level: 23 -> 32
- party[1].item: None -> 'ITEM_NONE'
- party[1].moves: ['MOVE_WATER_GUN', 'MOVE_QUICK_ATTACK', 'MOVE_PURSUIT', 'MOVE_GROWL'] -> ['MOVE_BUBBLE_BEAM', 'MOVE_SIGNAL_BEAM', 'MOVE_CAMOUFLAGE', 'MOVE_RECOVER']
- party[1].iv_scale: 50 -> 120
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_ROSELIA' -> 'SPECIES_SHIFTRY'
- party[2].level: 23 -> 32
- party[2].item: None -> 'ITEM_NONE'
- party[2].moves: ['MOVE_MEGA_DRAIN', 'MOVE_POISON_STING', 'MOVE_LEECH_SEED', 'MOVE_STUN_SPORE'] -> ['MOVE_SEED_BOMB', 'MOVE_LEECH_SEED', 'MOVE_FAKE_OUT', 'MOVE_FAINT_ATTACK']
- party[2].iv_scale: 50 -> 87
- party[2].ability/gender: 0/None -> 1/None
- party[3].level: 27 -> 33
- party[3].item: None -> 'ITEM_SITRUS_BERRY'
- party[3].moves: ['MOVE_FLAME_WHEEL', 'MOVE_MACH_PUNCH', 'MOVE_FURY_SWIPES', 'MOVE_LEER'] -> ['MOVE_FIRE_PUNCH', 'MOVE_MACH_PUNCH', 'MOVE_FAKE_OUT', 'MOVE_THUNDER_PUNCH']
- party[3].iv_scale: 50 -> 205
- party[3].ability/gender: 0/None -> 1/None

## res/trainers/data/rival_route_209_chimchar.json
- party[0].level: 25 -> 32
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_WING_ATTACK', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_ENDEAVOR', 'MOVE_DOUBLE_TEAM']
- party[0].iv_scale: 50 -> 245
- party[0].ability/gender: 0/None -> 1/'female'
- party[1].species: 'SPECIES_ROSELIA' -> 'SPECIES_SHIFTRY'
- party[1].level: 23 -> 32
- party[1].item: None -> 'ITEM_NONE'
- party[1].moves: ['MOVE_MEGA_DRAIN', 'MOVE_POISON_STING', 'MOVE_LEECH_SEED', 'MOVE_STUN_SPORE'] -> ['MOVE_SEED_BOMB', 'MOVE_LEECH_SEED', 'MOVE_FAINT_ATTACK', 'MOVE_FAKE_OUT']
- party[1].iv_scale: 50 -> 155
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_PONYTA' -> 'SPECIES_VULPIX'
- party[2].level: 23 -> 32
- party[2].item: None -> 'ITEM_NONE'
- party[2].moves: ['MOVE_EMBER', 'MOVE_TACKLE', 'MOVE_TAIL_WHIP', 'MOVE_GROWL'] -> ['MOVE_FLAMETHROWER', 'MOVE_WILL_O_WISP', 'MOVE_ENERGY_BALL', 'MOVE_CONFUSE_RAY']
- party[2].iv_scale: 50 -> 245
- party[2].ability/gender: 0/None -> 1/None
- party[3].level: 27 -> 33
- party[3].item: None -> 'ITEM_SITRUS_BERRY'
- party[3].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_PECK', 'MOVE_METAL_CLAW', 'MOVE_GROWL'] -> ['MOVE_WATER_PULSE', 'MOVE_BRINE', 'MOVE_GRASS_KNOT', 'MOVE_AQUA_RING']
- party[3].iv_scale: 50 -> 148
- party[3].ability/gender: 0/None -> 2/None

## res/trainers/data/rival_pastoria_city_piplup.json
- party size changed (4 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/rival_pastoria_city_turtwig.json
- party size changed (4 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/rival_pastoria_city_chimchar.json
- party size changed (4 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/rival_canalave_city_piplup.json
- party[0].level: 36 -> 48
- party[0].item: None -> 'ITEM_WHITE_HERB'
- party[0].moves: ['MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_DOUBLE_EDGE', 'MOVE_CLOSE_COMBAT', 'MOVE_ROOST']
- party[0].iv_scale: 100 -> 238
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 35 -> 48
- party[1].item: None -> 'ITEM_SEA_INCENSE'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_PURSUIT', 'MOVE_QUICK_ATTACK', 'MOVE_SWIFT'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_BRINE', 'MOVE_RECOVER']
- party[1].iv_scale: 100 -> 98
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_SNORLAX'
- party[2].level: 37 -> 48
- party[2].item: None -> 'ITEM_LEFTOVERS'
- party[2].moves: ['MOVE_BRICK_BREAK', 'MOVE_AERIAL_ACE', 'MOVE_NIGHT_SLASH', 'MOVE_HORN_ATTACK'] -> ['MOVE_BODY_SLAM', 'MOVE_BRICK_BREAK', 'MOVE_REST', 'MOVE_SLEEP_TALK']
- party[2].iv_scale: 100 -> 249
- party[2].ability/gender: 0/None -> 2/None
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 35 -> 48
- party[3].item: None -> 'ITEM_CHOICE_SPECS'
- party[3].moves: ['MOVE_FIRE_SPIN', 'MOVE_TAKE_DOWN', 'MOVE_STOMP', 'MOVE_TAIL_WHIP'] -> ['MOVE_HEAT_WAVE', 'MOVE_ENERGY_BALL', 'MOVE_EXTRASENSORY', 'MOVE_DARK_PULSE']
- party[3].iv_scale: 100 -> 154
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 38 -> 49
- party[4].item: None -> 'ITEM_SITRUS_BERRY'
- party[4].moves: ['MOVE_RAZOR_LEAF', 'MOVE_BITE', 'MOVE_MEGA_DRAIN', 'MOVE_LEECH_SEED'] -> ['MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_WOOD_HAMMER', 'MOVE_LEECH_SEED']
- party[4].iv_scale: 100 -> 63
- party[4].ability/gender: 0/None -> 2/None

## res/trainers/data/rival_canalave_city_turtwig.json
- party[0].level: 36 -> 48
- party[0].item: None -> 'ITEM_WHITE_HERB'
- party[0].moves: ['MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_DOUBLE_EDGE', 'MOVE_CLOSE_COMBAT', 'MOVE_ROOST']
- party[0].iv_scale: 100 -> 237
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 35 -> 48
- party[1].item: None -> 'ITEM_SEA_INCENSE'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_PURSUIT', 'MOVE_QUICK_ATTACK', 'MOVE_SWIFT'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_BRINE', 'MOVE_RECOVER']
- party[1].iv_scale: 100 -> 97
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_SNORLAX'
- party[2].level: 37 -> 48
- party[2].item: None -> 'ITEM_LEFTOVERS'
- party[2].moves: ['MOVE_BRICK_BREAK', 'MOVE_AERIAL_ACE', 'MOVE_NIGHT_SLASH', 'MOVE_HORN_ATTACK'] -> ['MOVE_BODY_SLAM', 'MOVE_BRICK_BREAK', 'MOVE_REST', 'MOVE_SLEEP_TALK']
- party[2].iv_scale: 100 -> 248
- party[2].ability/gender: 0/None -> 2/None
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].level: 35 -> 48
- party[3].item: None -> 'ITEM_FOCUS_SASH'
- party[3].moves: ['MOVE_GIGA_DRAIN', 'MOVE_TOXIC_SPIKES', 'MOVE_LEECH_SEED', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_LEAF_STORM', 'MOVE_SUCKER_PUNCH', 'MOVE_FOCUS_BLAST', 'MOVE_FAKE_OUT']
- party[3].iv_scale: 100 -> 64
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 38 -> 49
- party[4].item: None -> 'ITEM_LIFE_ORB'
- party[4].moves: ['MOVE_BRICK_BREAK', 'MOVE_FLAME_WHEEL', 'MOVE_MACH_PUNCH', 'MOVE_AERIAL_ACE'] -> ['MOVE_ICE_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_MACH_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[4].iv_scale: 100 -> 242
- party[4].ability/gender: 0/None -> 1/None

## res/trainers/data/rival_canalave_city_chimchar.json
- party[0].level: 36 -> 48
- party[0].item: None -> 'ITEM_WHITE_HERB'
- party[0].moves: ['MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK', 'MOVE_DOUBLE_TEAM'] -> ['MOVE_AERIAL_ACE', 'MOVE_DOUBLE_EDGE', 'MOVE_CLOSE_COMBAT', 'MOVE_ROOST']
- party[0].iv_scale: 100 -> 236
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].level: 35 -> 48
- party[1].item: None -> 'ITEM_FOCUS_SASH'
- party[1].moves: ['MOVE_GIGA_DRAIN', 'MOVE_TOXIC_SPIKES', 'MOVE_LEECH_SEED', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_LEAF_STORM', 'MOVE_SUCKER_PUNCH', 'MOVE_FOCUS_BLAST', 'MOVE_FAKE_OUT']
- party[1].iv_scale: 100 -> 219
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_SNORLAX'
- party[2].level: 37 -> 48
- party[2].item: None -> 'ITEM_LEFTOVERS'
- party[2].moves: ['MOVE_BRICK_BREAK', 'MOVE_AERIAL_ACE', 'MOVE_NIGHT_SLASH', 'MOVE_HORN_ATTACK'] -> ['MOVE_BODY_SLAM', 'MOVE_BRICK_BREAK', 'MOVE_REST', 'MOVE_SLEEP_TALK']
- party[2].iv_scale: 100 -> 247
- party[2].ability/gender: 0/None -> 2/None
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 35 -> 48
- party[3].item: None -> 'ITEM_CHOICE_SPECS'
- party[3].moves: ['MOVE_FIRE_SPIN', 'MOVE_TAKE_DOWN', 'MOVE_STOMP', 'MOVE_TAIL_WHIP'] -> ['MOVE_HEAT_WAVE', 'MOVE_ENERGY_BALL', 'MOVE_EXTRASENSORY', 'MOVE_DARK_PULSE']
- party[3].iv_scale: 100 -> 152
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 38 -> 49
- party[4].item: None -> 'ITEM_SITRUS_BERRY'
- party[4].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_AERIAL_ACE', 'MOVE_METAL_CLAW', 'MOVE_FURY_ATTACK'] -> ['MOVE_WATERFALL', 'MOVE_IRON_DEFENSE', 'MOVE_EARTHQUAKE', 'MOVE_STEEL_WING']
- party[4].iv_scale: 100 -> 255
- party[4].ability/gender: 0/None -> 2/None

## res/trainers/data/rival_pokemon_league_piplup.json
- party[0].level: 48 -> 70
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 213
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 47 -> 70
- party[1].item: None -> 'ITEM_SITRUS_BERRY'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_HYDRO_PUMP', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_RECOVER']
- party[1].iv_scale: 200 -> 250
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 48 -> 70
- party[2].item: None -> 'ITEM_YACHE_BERRY'
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_OUTRAGE', 'MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 200 -> 251
- party[2].ability/gender: 0/None -> 1/None
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 47 -> 70
- party[3].item: None -> 'ITEM_WIDE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_NASTY_PLOT']
- party[3].iv_scale: 200 -> 244
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 49 -> 70
- party[4].item: None -> 'ITEM_CHESTO_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_ZEN_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 244
- party[4].ability/gender: 0/None -> 2/None
- party[5].level: 51 -> 71
- party[5].item: None -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_LEAF_STORM', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_SYNTHESIS'] -> ['MOVE_WOOD_HAMMER', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_LEECH_SEED']
- party[5].iv_scale: 200 -> 249
- party[5].ability/gender: 0/None -> 2/None

## res/trainers/data/rival_pokemon_league_turtwig.json
- party[0].level: 48 -> 70
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 213
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 47 -> 70
- party[1].item: None -> 'ITEM_SITRUS_BERRY'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_HYDRO_PUMP', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_RECOVER']
- party[1].iv_scale: 200 -> 250
- party[1].ability/gender: 0/None -> 2/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 48 -> 70
- party[2].item: None -> 'ITEM_YACHE_BERRY'
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_OUTRAGE', 'MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 200 -> 251
- party[2].ability/gender: 0/None -> 1/None
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].level: 47 -> 70
- party[3].item: None -> 'ITEM_TANGA_BERRY'
- party[3].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK', 'MOVE_TAILWIND']
- party[3].iv_scale: 200 -> 250
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 49 -> 70
- party[4].item: None -> 'ITEM_CHESTO_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_ZEN_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 244
- party[4].ability/gender: 0/None -> 2/None
- party[5].level: 51 -> 71
- party[5].item: None -> 'ITEM_LIFE_ORB'
- party[5].moves: ['MOVE_FLAMETHROWER', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_CLAW', 'MOVE_AERIAL_ACE'] -> ['MOVE_FIRE_PUNCH', 'MOVE_CLOSE_COMBAT', 'MOVE_THUNDER_PUNCH', 'MOVE_SWORDS_DANCE']
- party[5].iv_scale: 200 -> 217
- party[5].ability/gender: 0/None -> 1/None

## res/trainers/data/rival_pokemon_league_chimchar.json
- party[0].level: 48 -> 70
- party[0].item: None -> 'ITEM_FOCUS_SASH'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 213
- party[0].ability/gender: 0/None -> 1/None
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].level: 47 -> 70
- party[1].item: None -> 'ITEM_TANGA_BERRY'
- party[1].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK', 'MOVE_TAILWIND']
- party[1].iv_scale: 200 -> 250
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 48 -> 70
- party[2].item: None -> 'ITEM_YACHE_BERRY'
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_OUTRAGE', 'MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_THUNDER_WAVE']
- party[2].iv_scale: 200 -> 251
- party[2].ability/gender: 0/None -> 1/None
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 47 -> 70
- party[3].item: None -> 'ITEM_WIDE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[3].iv_scale: 200 -> 244
- party[3].ability/gender: 0/None -> 1/None
- party[4].level: 49 -> 70
- party[4].item: None -> 'ITEM_CHESTO_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_ZEN_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 244
- party[4].ability/gender: 0/None -> 2/None
- party[5].level: 51 -> 71
- party[5].item: None -> 'ITEM_SALAC_BERRY'
- party[5].moves: ['MOVE_BRINE', 'MOVE_AERIAL_ACE', 'MOVE_METAL_CLAW', 'MOVE_SHADOW_CLAW'] -> ['MOVE_FLAIL', 'MOVE_WATERFALL', 'MOVE_SWORDS_DANCE', 'MOVE_ENDURE']
- party[5].iv_scale: 200 -> 255
- party[5].ability/gender: 0/None -> 2/None

## res/trainers/data/sailor_zachariah.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PELIPPER' -> 'SPECIES_POLIWRATH'
- party[0].level: 40 -> 59
- party[0].moves: None -> ['MOVE_BELLY_DRUM', 'MOVE_POISON_JAB', 'MOVE_DYNAMIC_PUNCH', 'MOVE_ICE_PUNCH']
- party[0].iv_scale: 0 -> 219
- party[1].species: 'SPECIES_MACHOKE' -> 'SPECIES_MACHAMP'
- party[1].level: 42 -> 59
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_THUNDER_PUNCH', 'MOVE_POISON_JAB', 'MOVE_DYNAMIC_PUNCH']
- party[1].iv_scale: 0 -> 244
- party[2].level: 44 -> 59
- party[2].moves: None -> ['MOVE_TOXIC', 'MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_RECOVER']
- party[2].iv_scale: 0 -> 222

## res/trainers/data/sailor_samson.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_WINGULL' -> 'SPECIES_TENTACRUEL'
- party[0].level: 29 -> 39
- party[0].moves: ['MOVE_WATER_PULSE', 'MOVE_WING_ATTACK', 'MOVE_SUPERSONIC', 'MOVE_NONE'] -> ['MOVE_ICE_BEAM', 'MOVE_SURF', 'MOVE_SLUDGE_BOMB', 'MOVE_TOXIC_SPIKES']
- party[0].iv_scale: 10 -> 253
- party[1].species: 'SPECIES_SHELLOS' -> 'SPECIES_KINGLER'
- party[1].level: 30 -> 39
- party[1].moves: ['MOVE_WATER_PULSE', 'MOVE_MUD_BOMB', 'MOVE_RAIN_DANCE', 'MOVE_NONE'] -> ['MOVE_METAL_CLAW', 'MOVE_STOMP', 'MOVE_KNOCK_OFF', 'MOVE_GUILLOTINE']
- party[1].iv_scale: 10 -> 238
- party[2].level: 31 -> 39
- party[2].moves: ['MOVE_FURY_SWIPES', 'MOVE_CONFUSION', 'MOVE_WATER_PULSE', 'MOVE_NONE'] -> ['MOVE_AQUA_JET', 'MOVE_ZEN_HEADBUTT', 'MOVE_CROSS_CHOP', 'MOVE_ICE_PUNCH']
- party[2].iv_scale: 10 -> 217

## res/trainers/data/scientist_shaun.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_MAGNETON'
- party[0].level: 30 -> 37
- party[0].moves: ['MOVE_SPARK', 'MOVE_MAGNET_BOMB', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_FLASH_CANNON', 'MOVE_THUNDERBOLT', 'MOVE_TRI_ATTACK', 'MOVE_THUNDER_WAVE']
- party[0].iv_scale: 0 -> 232
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_ELECTABUZZ'
- party[1].level: 26 -> 37
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_DISABLE', 'MOVE_KINESIS', 'MOVE_THUNDER_PUNCH'] -> ['MOVE_LOW_KICK', 'MOVE_LIGHT_SCREEN', 'MOVE_THUNDER_PUNCH', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 0 -> 248

## res/trainers/data/ninja_boy_fabian.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ninja_boy_fabian.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/ninja_boy_brennan.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ninja_boy_brennan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/ninja_boy_bruce.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_BEEDRILL'
- party[0].level: 33 -> 41
- party[0].moves: None -> ['MOVE_BRICK_BREAK', 'MOVE_KNOCK_OFF', 'MOVE_POISON_JAB', 'MOVE_X_SCISSOR']
- party[0].iv_scale: 0 -> 254

## res/trainers/data/beauty_devon.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 24 -> 33
- party[0].moves: None -> ['MOVE_HIDDEN_POWER', 'MOVE_ENERGY_BALL', 'MOVE_SYNTHESIS', 'MOVE_SIGNAL_BEAM']
- party[0].iv_scale: 0 -> 253
- party[1].level: 24 -> 33
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_RAZOR_LEAF', 'MOVE_SUCKER_PUNCH', 'MOVE_BUG_BITE']
- party[1].iv_scale: 0 -> 189
- party[2].level: 24 -> 33
- party[2].moves: None -> ['MOVE_IRON_HEAD', 'MOVE_SUCKER_PUNCH', 'MOVE_BUG_BITE', 'MOVE_GUNK_SHOT']
- party[2].iv_scale: 0 -> 189

## res/trainers/data/beauty_nicola.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 45 -> 57
- party[0].moves: None -> ['MOVE_DIZZY_PUNCH', 'MOVE_QUICK_ATTACK', 'MOVE_BOUNCE', 'MOVE_CHARM']
- party[0].iv_scale: 0 -> 241

## res/trainers/data/swimmer_claire.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_FLOATZEL' -> 'SPECIES_OMASTAR'
- party[0].level: 35 -> 45
- party[0].moves: None -> ['MOVE_BRINE', 'MOVE_RAIN_DANCE', 'MOVE_ANCIENT_POWER', 'MOVE_ICE_BEAM']
- party[0].iv_scale: 0 -> 243

## res/trainers/data/youngster_wayne.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 17 -> 24
- party[0].moves: None -> ['MOVE_WING_ATTACK', 'MOVE_DOUBLE_TEAM', 'MOVE_ENDEAVOR', 'MOVE_WHIRLWIND']
- party[0].iv_scale: 0 -> 160
- party[1].species: 'SPECIES_SHELLOS' -> 'SPECIES_GROWLITHE'
- party[1].level: 20 -> 24
- party[1].moves: None -> ['MOVE_LEER', 'MOVE_ODOR_SLEUTH', 'MOVE_HELPING_HAND', 'MOVE_FLAME_WHEEL']
- party[1].iv_scale: 0 -> 162
- party[2].level: 20 -> 24
- party[2].moves: None -> ['MOVE_EMBER', 'MOVE_FLAME_WHEEL', 'MOVE_STOMP', 'MOVE_FIRE_SPIN']
- party[2].iv_scale: 0 -> 161

## res/trainers/data/tuber_jacky.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 32 -> 39
- party[0].moves: ['MOVE_WATER_GUN', 'MOVE_ROLLOUT', 'MOVE_HYPER_FANG', 'MOVE_YAWN'] -> ['MOVE_HYPER_FANG', 'MOVE_YAWN', 'MOVE_AMNESIA', 'MOVE_AQUA_TAIL']
- party[0].iv_scale: 10 -> 243

## res/trainers/data/tuber_caitlyn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_AZURILL' -> 'SPECIES_LUMINEON'
- party[0].level: 27 -> 39
- party[0].moves: ['MOVE_WATER_GUN', 'MOVE_SLAM', 'MOVE_CHARM', 'MOVE_NONE'] -> ['MOVE_SURF', 'MOVE_RAIN_DANCE', 'MOVE_SAFEGUARD', 'MOVE_AQUA_RING']
- party[0].iv_scale: 10 -> 238
- party[1].species: 'SPECIES_MARILL' -> 'SPECIES_SEAKING'
- party[1].level: 29 -> 39
- party[1].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_ROLLOUT', 'MOVE_DEFENSE_CURL', 'MOVE_AQUA_RING'] -> ['MOVE_POISON_JAB', 'MOVE_WATERFALL', 'MOVE_KNOCK_OFF', 'MOVE_AQUA_RING']
- party[1].iv_scale: 10 -> 204
- party[2].level: 31 -> 39
- party[2].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_DOUBLE_EDGE', 'MOVE_ROLLOUT', 'MOVE_AQUA_RING'] -> ['MOVE_BELLY_DRUM', 'MOVE_WATERFALL', 'MOVE_AQUA_JET', 'MOVE_ICE_PUNCH']
- party[2].iv_scale: 10 -> 236

## res/trainers/data/veteran_terrell.json
- party[0].level: 53 -> 78
- party[0].moves: ['MOVE_X_SCISSOR', 'MOVE_GIGA_DRAIN', 'MOVE_SPORE', 'MOVE_SLASH'] -> ['MOVE_X_SCISSOR', 'MOVE_CROSS_POISON', 'MOVE_SPORE', 'MOVE_SEED_BOMB']
- party[0].iv_scale: 100 -> 255
- party[1].species: 'SPECIES_RHYDON' -> 'SPECIES_RHYPERIOR'
- party[1].level: 54 -> 78
- party[1].iv_scale: 100 -> 249
- party[2].species: 'SPECIES_MAGMAR' -> 'SPECIES_MAGMORTAR'
- party[2].level: 55 -> 78
- party[2].moves: ['MOVE_FIRE_BLAST', 'MOVE_CONFUSE_RAY', 'MOVE_IRON_TAIL', 'MOVE_FOCUS_BLAST'] -> ['MOVE_FIRE_BLAST', 'MOVE_CONFUSE_RAY', 'MOVE_THUNDERBOLT', 'MOVE_FOCUS_BLAST']
- party[2].iv_scale: 100 -> 249

## res/trainers/data/veteran_brenden.json
- party[0].level: 54 -> 78
- party[0].moves: ['MOVE_FLASH_CANNON', 'MOVE_ROCK_SLIDE', 'MOVE_STEALTH_ROCK', 'MOVE_TOXIC_SPIKES'] -> ['MOVE_GYRO_BALL', 'MOVE_ROCK_SLIDE', 'MOVE_STEALTH_ROCK', 'MOVE_TOXIC_SPIKES']
- party[0].iv_scale: 100 -> 223
- party[1].level: 54 -> 78
- party[1].moves: ['MOVE_EARTHQUAKE', 'MOVE_AQUA_TAIL', 'MOVE_ICE_FANG', 'MOVE_DRAGON_PULSE'] -> ['MOVE_EARTHQUAKE', 'MOVE_AQUA_TAIL', 'MOVE_ICE_FANG', 'MOVE_NONE']
- party[1].iv_scale: 100 -> 244
- party[2].level: 54 -> 78
- party[2].moves: ['MOVE_DIG', 'MOVE_CRUNCH', 'MOVE_PROTECT', 'MOVE_REST'] -> ['MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_YAWN', 'MOVE_REST']
- party[2].iv_scale: 100 -> 255

## res/trainers/data/worker_noel.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_MAGNETON'
- party[0].level: 34 -> 46
- party[0].moves: None -> ['MOVE_MAGNET_BOMB', 'MOVE_SCREECH', 'MOVE_DISCHARGE', 'MOVE_MIRROR_SHOT']
- party[0].iv_scale: 0 -> 253
- party[1].species: 'SPECIES_MAGNEMITE' -> 'SPECIES_MAWILE'
- party[1].level: 36 -> 46
- party[1].moves: None -> ['MOVE_IRON_HEAD', 'MOVE_CRUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_SUCKER_PUNCH']
- party[1].iv_scale: 0 -> 251

## res/trainers/data/worker_braden.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 37 -> 48
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_CURSE', 'MOVE_IRON_TAIL', 'MOVE_CRUNCH']
- party[0].iv_scale: 0 -> 245

## res/trainers/data/worker_brendon.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/worker_brendon.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/worker_quentin.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/worker_quentin.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_galactic_hq_b2f_1.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_galactic_hq_b2f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']

## res/trainers/data/galactic_grunt_galactic_hq_b2f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOUNDOUR' -> 'SPECIES_CACTURNE'
- party[0].level: 38 -> 54
- party[0].moves: None -> ['MOVE_SPIKES', 'MOVE_SUCKER_PUNCH', 'MOVE_PAYBACK', 'MOVE_NEEDLE_ARM']
- party[0].iv_scale: 30 -> 227
- party[1].species: 'SPECIES_MURKROW' -> 'SPECIES_SEVIPER'
- party[1].level: 40 -> 54
- party[1].moves: None -> ['MOVE_SWAGGER', 'MOVE_HAZE', 'MOVE_NIGHT_SLASH', 'MOVE_POISON_JAB']
- party[1].iv_scale: 30 -> 223

## res/trainers/data/galactic_grunt_galactic_hq_3f_1.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_galactic_hq_3f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_galactic_hq_2f_1.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_galactic_hq_2f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/galactic_grunt_galactic_hq_3f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MURKROW' -> 'SPECIES_KRICKETUNE'
- party[0].level: 39 -> 53
- party[0].moves: None -> ['MOVE_TAUNT', 'MOVE_NIGHT_SLASH', 'MOVE_BUG_BUZZ', 'MOVE_PERISH_SONG']
- party[0].iv_scale: 30 -> 253
- party[1].species: 'SPECIES_STUNKY' -> 'SPECIES_GASTRODON'
- party[1].level: 39 -> 53
- party[1].moves: None -> ['MOVE_HIDDEN_POWER', 'MOVE_RAIN_DANCE', 'MOVE_BODY_SLAM', 'MOVE_MUDDY_WATER']
- party[1].iv_scale: 30 -> 216

## res/trainers/data/galactic_grunt_galactic_hq_2f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_FEAROW'
- party[0].level: 40 -> 54
- party[0].moves: None -> ['MOVE_U_TURN', 'MOVE_STEEL_WING', 'MOVE_ROOST', 'MOVE_DRILL_PECK']
- party[0].iv_scale: 30 -> 202
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_SHARPEDO'
- party[1].level: 38 -> 54
- party[1].moves: None -> ['MOVE_AQUA_JET', 'MOVE_ICE_FANG', 'MOVE_CRUNCH', 'MOVE_SKULL_BASH']
- party[1].iv_scale: 30 -> 248

## res/trainers/data/galactic_grunt_galactic_hq_3f_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_URSARING'
- party[0].level: 38 -> 54
- party[0].moves: None -> ['MOVE_SLASH', 'MOVE_FOCUS_PUNCH', 'MOVE_REST', 'MOVE_BRICK_BREAK']
- party[0].iv_scale: 30 -> 213
- party[1].species: 'SPECIES_CROAGUNK' -> 'SPECIES_GRANBULL'
- party[1].level: 40 -> 54
- party[1].moves: None -> ['MOVE_ROAR', 'MOVE_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH']
- party[1].iv_scale: 30 -> 220

## res/trainers/data/galactic_grunt_mt_coronet_3f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MURKROW' -> 'SPECIES_MISMAGIUS'
- party[0].level: 43 -> 55
- party[0].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_THUNDERBOLT', 'MOVE_ENERGY_BALL', 'MOVE_WILL_O_WISP']
- party[0].iv_scale: 30 -> 203

## res/trainers/data/galactic_grunt_mt_coronet_4f_1.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_mt_coronet_4f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_mt_coronet_4f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_DRAPION'
- party[0].level: 42 -> 54
- party[0].moves: None -> ['MOVE_TOXIC_SPIKES', 'MOVE_X_SCISSOR', 'MOVE_POISON_FANG', 'MOVE_CRUNCH']
- party[0].iv_scale: 30 -> 247
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_CAMERUPT'
- party[1].level: 40 -> 54
- party[1].moves: None -> ['MOVE_LAVA_PLUME', 'MOVE_ROCK_SLIDE', 'MOVE_EARTH_POWER', 'MOVE_EARTHQUAKE']
- party[1].iv_scale: 30 -> 245

## res/trainers/data/galactic_grunt_mt_coronet_tunnel_room_1.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_mt_coronet_tunnel_room_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_mt_coronet_tunnel_room_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_WOBBUFFET'
- party[0].level: 43 -> 55
- party[0].moves: None -> ['MOVE_COUNTER', 'MOVE_MIRROR_COAT', 'MOVE_SAFEGUARD', 'MOVE_DESTINY_BOND']
- party[0].iv_scale: 30 -> 226

## res/trainers/data/galactic_grunt_mt_coronet_5f_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_MIGHTYENA'
- party[0].level: 41 -> 54
- party[0].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_THUNDER_FANG', 'MOVE_FIRE_FANG', 'MOVE_SUPER_FANG']
- party[0].iv_scale: 30 -> 228
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_ELECTRODE'
- party[1].level: 41 -> 54
- party[1].moves: None -> ['MOVE_THUNDERBOLT', 'MOVE_MAGNET_RISE', 'MOVE_THUNDER_WAVE', 'MOVE_EXPLOSION']
- party[1].iv_scale: 30 -> 229

## res/trainers/data/galactic_grunt_spear_pillar_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CROAGUNK' -> 'SPECIES_GOLEM'
- party[0].level: 39 -> 54
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_EXPLOSION', 'MOVE_DOUBLE_EDGE', 'MOVE_STONE_EDGE']
- party[0].iv_scale: 30 -> 205
- party[1].species: 'SPECIES_CROAGUNK' -> 'SPECIES_NIDOKING'
- party[1].level: 43 -> 54
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_POISON_JAB', 'MOVE_STONE_EDGE', 'MOVE_THUNDER_PUNCH']
- party[1].iv_scale: 30 -> 247

## res/trainers/data/galactic_grunt_galactic_hq_3f_4.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_galactic_hq_3f_4.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_mt_coronet_3f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_SWALOT'
- party[0].level: 43 -> 55
- party[0].moves: None -> ['MOVE_GUNK_SHOT', 'MOVE_SEED_BOMB', 'MOVE_FIRE_PUNCH', 'MOVE_TOXIC']
- party[0].iv_scale: 30 -> 222

## res/trainers/data/galactic_grunt_mt_coronet_tunnel_room_3.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_mt_coronet_tunnel_room_3.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_mt_coronet_5f_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_HOUNDOUR' -> 'SPECIES_KECLEON'
- party[0].level: 40 -> 54
- party[0].moves: None -> ['MOVE_SCREECH', 'MOVE_SUBSTITUTE', 'MOVE_SUCKER_PUNCH', 'MOVE_SHADOW_CLAW']
- party[0].iv_scale: 30 -> 237
- party[1].species: 'SPECIES_GLAMEOW' -> 'SPECIES_EXPLOUD'
- party[1].level: 42 -> 54
- party[1].moves: None -> ['MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG', 'MOVE_CRUNCH', 'MOVE_ROAR']
- party[1].iv_scale: 30 -> 247

## res/trainers/data/galactic_grunt_mt_coronet_6f.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_grunt_mt_coronet_6f.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/galactic_grunt_spear_pillar_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STUNKY' -> 'SPECIES_FORRETRESS'
- party[0].level: 41 -> 54
- party[0].moves: None -> ['MOVE_TOXIC_SPIKES', 'MOVE_EXPLOSION', 'MOVE_IRON_DEFENSE', 'MOVE_GYRO_BALL']
- party[0].iv_scale: 30 -> 250
- party[1].species: 'SPECIES_GLAMEOW' -> 'SPECIES_NIDOQUEEN'
- party[1].level: 41 -> 54
- party[1].moves: None -> ['MOVE_SLUDGE_BOMB', 'MOVE_FLAMETHROWER', 'MOVE_SURF', 'MOVE_EARTH_POWER']
- party[1].iv_scale: 30 -> 235

## res/trainers/data/commander_mars_spear_pillar.json
- party size changed (3 -> 5 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/roughneck_kirby.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CLEFFA' -> 'SPECIES_WIGGLYTUFF'
- party[0].level: 23 -> 33
- party[0].item: None -> 'ITEM_NONE'
- party[0].moves: None -> ['MOVE_SING', 'MOVE_PSYCHIC', 'MOVE_REST', 'MOVE_SNORE']
- party[0].iv_scale: 0 -> 209

## res/trainers/data/pokefan_leonard.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PICHU' -> 'SPECIES_PLUSLE'
- party[0].level: 19 -> 31
- party[0].moves: None -> ['MOVE_FAKE_TEARS', 'MOVE_COPYCAT', 'MOVE_THUNDERBOLT', 'MOVE_FAKE_TEARS']
- party[0].iv_scale: 0 -> 199
- party[1].species: 'SPECIES_PICHU' -> 'SPECIES_MINUN'
- party[1].level: 19 -> 31
- party[1].moves: None -> ['MOVE_CHARM', 'MOVE_COPYCAT', 'MOVE_THUNDERBOLT', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 0 -> 198
- party[2].level: 22 -> 31
- party[2].moves: None -> ['MOVE_DOUBLE_TEAM', 'MOVE_SLAM', 'MOVE_THUNDERBOLT', 'MOVE_FEINT']
- party[2].iv_scale: 0 -> 208

## res/trainers/data/pokefan_rebekah.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_BONSLY' -> 'SPECIES_SUDOWOODO'
- party[0].level: 23 -> 33
- party[0].moves: None -> ['MOVE_WOOD_HAMMER', 'MOVE_LOW_KICK', 'MOVE_THUNDER_PUNCH', 'MOVE_ROCK_TOMB']
- party[0].iv_scale: 0 -> 200

## res/trainers/data/youngster_oliver.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 20 -> 31
- party[0].moves: None -> ['MOVE_OMINOUS_WIND', 'MOVE_PSYCHIC', 'MOVE_SIGNAL_BEAM', 'MOVE_POISON_POWDER']
- party[0].iv_scale: 0 -> 168
- party[1].species: 'SPECIES_BARBOACH' -> 'SPECIES_CRAWDAUNT'
- party[1].level: 19 -> 30
- party[1].moves: None -> ['MOVE_WATERFALL', 'MOVE_DRAGON_DANCE', 'MOVE_KNOCK_OFF', 'MOVE_BRICK_BREAK']
- party[1].iv_scale: 0 -> 197
- party[2].level: 21 -> 31
- party[2].moves: None -> ['MOVE_AIR_CUTTER', 'MOVE_CHATTER', 'MOVE_ROOST', 'MOVE_MIMIC']
- party[2].iv_scale: 0 -> 207

## res/trainers/data/belle_and_pa_beth_and_bob.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PONYTA' -> 'SPECIES_GROWLITHE'
- party[0].level: 23 -> 33
- party[0].moves: None -> ['MOVE_ROAR', 'MOVE_CRUNCH', 'MOVE_FIRE_FANG', 'MOVE_MORNING_SUN']
- party[0].iv_scale: 0 -> 208
- party[1].level: 23 -> 33
- party[1].moves: None -> ['MOVE_HEADBUTT', 'MOVE_FLAME_WHEEL', 'MOVE_BOUNCE', 'MOVE_HYPNOSIS']
- party[1].iv_scale: 0 -> 189

## res/trainers/data/young_couple_mike_and_nat.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 23 -> 33
- party[0].moves: None -> ['MOVE_DRILL_PECK', 'MOVE_SUCKER_PUNCH', 'MOVE_WHIRLWIND', 'MOVE_TAUNT']
- party[0].iv_scale: 0 -> 199
- party[1].level: 23 -> 33
- party[1].moves: None -> ['MOVE_MEAN_LOOK', 'MOVE_PSYCHIC', 'MOVE_PAIN_SPLIT', 'MOVE_SHADOW_BALL']
- party[1].iv_scale: 0 -> 201

## res/trainers/data/aroma_lady_alison.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/artist_ismael.json
- party[0].species: 'SPECIES_KRICKETUNE' -> 'SPECIES_SMEARGLE'

## res/trainers/data/pi_kendrick.json
- party[0].species: 'SPECIES_RHYHORN' -> 'SPECIES_KANGASKHAN'
- party[0].moves: ['MOVE_HORN_DRILL', 'MOVE_REVERSAL', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_DIZZY_PUNCH', 'MOVE_BRICK_BREAK', 'MOVE_NONE', 'MOVE_NONE']

## res/trainers/data/ruin_maniac_karl.json
- party[0].species: 'SPECIES_GEODUDE' -> 'SPECIES_NIDOKING'
- party[0].level: 19 -> 31
- party[0].moves: None -> ['MOVE_DIG', 'MOVE_BRICK_BREAK', 'MOVE_POISON_JAB', 'MOVE_THRASH']
- party[0].iv_scale: 0 -> 228
- party[1].species: 'SPECIES_GEODUDE' -> 'SPECIES_DONPHAN'
- party[1].level: 21 -> 31
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_FIRE_FANG', 'MOVE_THUNDER_FANG', 'MOVE_SEED_BOMB']
- party[1].iv_scale: 0 -> 207
- party[2].level: 23 -> 31
- party[2].moves: None -> ['MOVE_CONFUSE_RAY', 'MOVE_EXTRASENSORY', 'MOVE_IRON_DEFENSE', 'MOVE_SAFEGUARD']
- party[2].iv_scale: 0 -> 195

## res/trainers/data/bird_keeper_audrey.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_TAILLOW' -> 'SPECIES_SWELLOW'
- party[0].level: 51 -> 73
- party[0].moves: None -> ['MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN', 'MOVE_WHIRLWIND']
- party[0].iv_scale: 0 -> 245
- party[1].level: 53 -> 73
- party[1].moves: None -> ['MOVE_NIGHT_SLASH', 'MOVE_LEAF_BLADE', 'MOVE_QUICK_ATTACK', 'MOVE_AERIAL_ACE']
- party[1].iv_scale: 0 -> 214
- party[2].level: 55 -> 73
- party[2].moves: None -> ['MOVE_ROOST', 'MOVE_TAILWIND', 'MOVE_HEAT_WAVE', 'MOVE_AIR_SLASH']
- party[2].iv_scale: 0 -> 223

## res/trainers/data/bird_keeper_geneva.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 55 -> 74
- party[0].moves: None -> ['MOVE_AGILITY', 'MOVE_ASSURANCE', 'MOVE_ROOST', 'MOVE_DRILL_PECK']
- party[0].iv_scale: 0 -> 208
- party[1].level: 57 -> 74
- party[1].moves: None -> ['MOVE_OMINOUS_WIND', 'MOVE_SIGNAL_BEAM', 'MOVE_HEAT_WAVE', 'MOVE_PSYCHIC']
- party[1].iv_scale: 0 -> 251

## res/trainers/data/bird_keeper_krystal.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_STARAVIA' -> 'SPECIES_STARAPTOR'
- party[0].level: 55 -> 78
- party[0].moves: None -> ['MOVE_U_TURN', 'MOVE_CLOSE_COMBAT', 'MOVE_QUICK_ATTACK', 'MOVE_BRAVE_BIRD']
- party[0].iv_scale: 0 -> 253
- party[1].level: 57 -> 78
- party[1].moves: None -> ['MOVE_AGILITY', 'MOVE_U_TURN', 'MOVE_ROOST', 'MOVE_DRILL_PECK']
- party[1].iv_scale: 0 -> 203
- party[2].level: 59 -> 78
- party[2].moves: None -> ['MOVE_EXTRASENSORY', 'MOVE_HYPNOSIS', 'MOVE_ROOST', 'MOVE_DREAM_EATER']
- party[2].iv_scale: 0 -> 254

## res/trainers/data/dragon_tamer_geoffrey.json
- party[0].species: 'SPECIES_GABITE' -> 'SPECIES_GARCHOMP'
- party[0].level: 53 -> 74
- party[0].moves: None -> ['MOVE_DRAGON_CLAW', 'MOVE_DIG', 'MOVE_CRUNCH', 'MOVE_DRAGON_RUSH']
- party[0].iv_scale: 50 -> 229
- party[1].level: 55 -> 74
- party[1].moves: None -> ['MOVE_FIRE_BLAST', 'MOVE_DRAGON_PULSE', 'MOVE_HIDDEN_POWER', 'MOVE_MIRROR_MOVE']
- party[1].iv_scale: 50 -> 255

## res/trainers/data/dragon_tamer_darien.json
- party[0].level: 60 -> 78
- party[0].moves: None -> ['MOVE_DRAGON_RUSH', 'MOVE_FIRE_PUNCH', 'MOVE_DRAGON_DANCE', 'MOVE_WING_ATTACK']
- party[0].iv_scale: 50 -> 219

## res/trainers/data/dragon_tamer_stanley.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dragon_tamer_drake.json
- party[0].species: 'SPECIES_GIBLE' -> 'SPECIES_DRAGONITE'
- party[0].level: 57 -> 78
- party[0].moves: None -> ['MOVE_DRAGON_DANCE', 'MOVE_ROOST', 'MOVE_OUTRAGE', 'MOVE_EXTREME_SPEED']
- party[0].iv_scale: 50 -> 216
- party[1].species: 'SPECIES_GABITE' -> 'SPECIES_KINGDRA'
- party[1].level: 57 -> 78
- party[1].moves: None -> ['MOVE_ICE_BEAM', 'MOVE_HYDRO_PUMP', 'MOVE_DRAGON_DANCE', 'MOVE_DRAGON_PULSE']
- party[1].iv_scale: 50 -> 233
- party[2].species: 'SPECIES_DRAGONAIR' -> 'SPECIES_ALTARIA'
- party[2].level: 57 -> 78
- party[2].moves: None -> ['MOVE_FLAMETHROWER', 'MOVE_DRAGON_PULSE', 'MOVE_ROOST', 'MOVE_HIDDEN_POWER']
- party[2].iv_scale: 50 -> 247

## res/trainers/data/dragon_tamer_kenny.json
- party[0].species: 'SPECIES_BAGON' -> 'SPECIES_SALAMENCE'
- party[0].level: 57 -> 78
- party[0].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_OUTRAGE', 'MOVE_FLAMETHROWER']
- party[0].iv_scale: 50 -> 248
- party[1].species: 'SPECIES_SHELGON' -> 'SPECIES_FLYGON'
- party[1].level: 57 -> 78
- party[1].moves: None -> ['MOVE_THUNDER_PUNCH', 'MOVE_OUTRAGE', 'MOVE_U_TURN', 'MOVE_EARTHQUAKE']
- party[1].iv_scale: 50 -> 213
- party[2].species: 'SPECIES_VIBRAVA' -> 'SPECIES_CHARIZARD'
- party[2].level: 57 -> 78
- party[2].moves: None -> ['MOVE_FLARE_BLITZ', 'MOVE_OUTRAGE', 'MOVE_THUNDER_PUNCH', 'MOVE_ROOST']
- party[2].iv_scale: 50 -> 238

## res/trainers/data/ace_trainer_rodolfo.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_saul.json
- party[0].level: 61 -> 78
- party[0].iv_scale: 50 -> 236

## res/trainers/data/ace_trainer_jose.json
- party[0].level: 56 -> 76
- party[0].iv_scale: 50 -> 246
- party[1].level: 56 -> 76
- party[1].iv_scale: 50 -> 247
- party[2].level: 57 -> 76
- party[2].iv_scale: 50 -> 242

## res/trainers/data/ace_trainer_felix.json
- party[0].species: 'SPECIES_DUSCLOPS' -> 'SPECIES_DUSKNOIR'
- party[0].level: 55 -> 76
- party[0].iv_scale: 50 -> 236
- party[1].level: 56 -> 76
- party[1].iv_scale: 50 -> 226

## res/trainers/data/ace_trainer_quinn.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_graham.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_keenan.json
- party[0].level: 58 -> 78
- party[0].moves: None -> ['MOVE_CROSS_CHOP', 'MOVE_ICE_PUNCH', 'MOVE_U_TURN', 'MOVE_CLOSE_COMBAT']
- party[0].iv_scale: 50 -> 236
- party[1].species: 'SPECIES_ELECTABUZZ' -> 'SPECIES_ELECTIVIRE'
- party[1].level: 58 -> 78
- party[1].moves: None -> ['MOVE_THUNDERBOLT', 'MOVE_FLAMETHROWER', 'MOVE_PSYCHIC', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 50 -> 247
- party[2].level: 59 -> 78
- party[2].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_WILL_O_WISP']
- party[2].iv_scale: 50 -> 203

## res/trainers/data/ace_trainer_stefan.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_skylar.json
- party[0].species: 'SPECIES_LOUDRED' -> 'SPECIES_EXPLOUD'
- party[0].level: 58 -> 78
- party[0].moves: ['MOVE_HYPER_VOICE', 'MOVE_BITE', 'MOVE_SUPERSONIC', 'MOVE_SCREECH'] -> ['MOVE_HYPER_VOICE', 'MOVE_FLAMETHROWER', 'MOVE_FOCUS_BLAST', 'MOVE_ICE_BEAM']
- party[0].iv_scale: 50 -> 244
- party[1].level: 59 -> 78
- party[1].moves: ['MOVE_HEAD_SMASH', 'MOVE_ZEN_HEADBUTT', 'MOVE_ANCIENT_POWER', 'MOVE_SCREECH'] -> ['MOVE_HEAD_SMASH', 'MOVE_ZEN_HEADBUTT', 'MOVE_EARTHQUAKE', 'MOVE_THUNDER_PUNCH']
- party[1].iv_scale: 50 -> 250
- party[2].level: 58 -> 78
- party[2].moves: ['MOVE_AIR_SLASH', 'MOVE_WATER_PULSE', 'MOVE_ROOST', 'MOVE_QUICK_ATTACK'] -> ['MOVE_AIR_SLASH', 'MOVE_HYDRO_PUMP', 'MOVE_ROOST', 'MOVE_ICE_BEAM']
- party[2].iv_scale: 50 -> 253

## res/trainers/data/ace_trainer_abel.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_deanna.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_moira.json
- party[0].species: 'SPECIES_SANDSLASH' -> 'SPECIES_DUGTRIO'
- party[0].level: 56 -> 76
- party[0].moves: ['MOVE_SLASH', 'MOVE_GYRO_BALL', 'MOVE_DIG', 'MOVE_X_SCISSOR'] -> ['MOVE_EARTHQUAKE', 'MOVE_FISSURE', 'MOVE_NIGHT_SLASH', 'MOVE_STONE_EDGE']
- party[0].iv_scale: 50 -> 245
- party[1].level: 56 -> 76
- party[1].moves: ['MOVE_MUDDY_WATER', 'MOVE_RECOVER', 'MOVE_BODY_SLAM', 'MOVE_PROTECT'] -> ['MOVE_MUDDY_WATER', 'MOVE_RECOVER', 'MOVE_TOXIC', 'MOVE_PROTECT']
- party[1].iv_scale: 50 -> 255
- party[2].level: 57 -> 76
- party[2].iv_scale: 50 -> 254

## res/trainers/data/ace_trainer_dana.json
- party[0].level: 55 -> 75
- party[0].moves: ['MOVE_CRUNCH', 'MOVE_SUCKER_PUNCH', 'MOVE_IRON_TAIL', 'MOVE_SCARY_FACE'] -> ['MOVE_CRUNCH', 'MOVE_SUCKER_PUNCH', 'MOVE_IRON_TAIL', 'MOVE_THUNDER_FANG']
- party[0].iv_scale: 50 -> 217
- party[1].species: 'SPECIES_KIRLIA' -> 'SPECIES_GARDEVOIR'
- party[1].level: 56 -> 75
- party[1].iv_scale: 50 -> 254

## res/trainers/data/ace_trainer_mikayla.json
- party[0].level: 56 -> 76
- party[0].iv_scale: 50 -> 242
- party[1].level: 56 -> 76
- party[1].moves: ['MOVE_NIGHT_SLASH', 'MOVE_POWER_GEM', 'MOVE_FAINT_ATTACK', 'MOVE_FAKE_OUT'] -> ['MOVE_NIGHT_SLASH', 'MOVE_SLASH', 'MOVE_FAINT_ATTACK', 'MOVE_FAKE_OUT']
- party[1].iv_scale: 50 -> 241
- party[2].level: 56 -> 76
- party[2].iv_scale: 50 -> 239

## res/trainers/data/ace_trainer_meagan.json
- party[0].level: 57 -> 77
- party[0].iv_scale: 50 -> 222
- party[1].level: 58 -> 77
- party[1].iv_scale: 50 -> 244

## res/trainers/data/ace_trainer_sandra.json
- party[0].species: 'SPECIES_DUGTRIO' -> 'SPECIES_CACTURNE'
- party[0].level: 55 -> 74
- party[0].moves: None -> ['MOVE_SEED_BOMB', 'MOVE_THUNDER_PUNCH', 'MOVE_SUCKER_PUNCH', 'MOVE_DESTINY_BOND']
- party[0].iv_scale: 50 -> 246
- party[1].level: 54 -> 74
- party[1].moves: None -> ['MOVE_GRASS_KNOT', 'MOVE_HIDDEN_POWER', 'MOVE_THUNDER_WAVE', 'MOVE_THUNDER']
- party[1].iv_scale: 50 -> 243
- party[2].level: 54 -> 74
- party[2].moves: None -> ['MOVE_FIRE_BLAST', 'MOVE_WILL_O_WISP', 'MOVE_ENERGY_BALL', 'MOVE_CALM_MIND']
- party[2].iv_scale: 50 -> 251

## res/trainers/data/ace_trainer_kassandra.json
- party[0].level: 58 -> 78
- party[0].iv_scale: 50 -> 251
- party[1].species: 'SPECIES_ONIX' -> 'SPECIES_STEELIX'
- party[1].level: 58 -> 78
- party[1].moves: ['MOVE_STONE_EDGE', 'MOVE_EARTHQUAKE', 'MOVE_IRON_TAIL', 'MOVE_DRAGON_BREATH'] -> ['MOVE_STONE_EDGE', 'MOVE_EARTHQUAKE', 'MOVE_IRON_HEAD', 'MOVE_THUNDER_FANG']
- party[1].iv_scale: 50 -> 236
- party[2].level: 59 -> 78
- party[2].iv_scale: 50 -> 215

## res/trainers/data/ace_trainer_jasmin.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ace_trainer_natasha.json
- party[0].level: 58 -> 78
- party[0].iv_scale: 50 -> 236
- party[1].species: 'SPECIES_GARDEVOIR' -> 'SPECIES_LOPUNNY'
- party[1].level: 59 -> 78
- party[1].moves: ['MOVE_PSYCHIC', 'MOVE_MAGICAL_LEAF', 'MOVE_CALM_MIND', 'MOVE_FOCUS_BLAST'] -> ['MOVE_BOUNCE', 'MOVE_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 50 -> 230
- party[2].level: 58 -> 78
- party[2].moves: ['MOVE_RECOVER', 'MOVE_FORCE_PALM', 'MOVE_PSYCHIC', 'MOVE_ROCK_SLIDE'] -> ['MOVE_RECOVER', 'MOVE_PSYCHO_CUT', 'MOVE_HI_JUMP_KICK', 'MOVE_ICE_PUNCH']
- party[2].iv_scale: 50 -> 209

## res/trainers/data/ace_trainer_monique.json
- party[0].level: 58 -> 78
- party[0].iv_scale: 50 -> 252
- party[1].level: 59 -> 78
- party[1].iv_scale: 50 -> 252
- party[2].level: 58 -> 78
- party[2].iv_scale: 50 -> 247

## res/trainers/data/psychic_corbin.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_XATU' -> 'SPECIES_MEDICHAM'
- party[0].level: 56 -> 76
- party[0].moves: None -> ['MOVE_PSYCHO_CUT', 'MOVE_ICE_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_RECOVER']
- party[0].iv_scale: 0 -> 243
- party[1].level: 56 -> 76
- party[1].moves: None -> ['MOVE_LEAF_BLADE', 'MOVE_X_SCISSOR', 'MOVE_NIGHT_SLASH', 'MOVE_CLOSE_COMBAT']
- party[1].iv_scale: 0 -> 241

## res/trainers/data/psychic_sterling.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/psychic_sterling.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/psychic_daisy.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SLOWPOKE' -> 'SPECIES_SLOWKING'
- party[0].level: 52 -> 74
- party[0].moves: None -> ['MOVE_POWER_GEM', 'MOVE_PSYCHIC', 'MOVE_SURF', 'MOVE_SHADOW_BALL']
- party[0].iv_scale: 0 -> 242
- party[1].level: 56 -> 74
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_FLAMETHROWER']
- party[1].iv_scale: 0 -> 242

## res/trainers/data/psychic_chelsey.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/psychic_chelsey.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/black_belt_davon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].species: 'SPECIES_TYROGUE' -> 'SPECIES_PRIMEAPE'
- party[0].level: 54 -> 75
- party[0].moves: None -> ['MOVE_THUNDER_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_U_TURN', 'MOVE_CLOSE_COMBAT']
- party[0].iv_scale: 30 -> 245
- party[1].species: 'SPECIES_MAKUHITA' -> 'SPECIES_HARIYAMA'
- party[1].level: 54 -> 75
- party[1].moves: None -> ['MOVE_STONE_EDGE', 'MOVE_WHIRLWIND', 'MOVE_CLOSE_COMBAT', 'MOVE_REVERSAL']
- party[1].iv_scale: 30 -> 243
- party[2].level: 57 -> 75
- party[2].moves: None -> ['MOVE_BULLET_PUNCH', 'MOVE_CROSS_CHOP', 'MOVE_POISON_JAB', 'MOVE_STONE_EDGE']
- party[2].iv_scale: 30 -> 250

## res/trainers/data/black_belt_griffin.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 58 -> 76
- party[0].moves: ['MOVE_SPORE', 'MOVE_MACH_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_SKY_UPPERCUT'] -> ['MOVE_SPORE', 'MOVE_MACH_PUNCH', 'MOVE_SEED_BOMB', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 30 -> 254
- party[1].level: 58 -> 76
- party[1].moves: ['MOVE_DETECT', 'MOVE_PSYCHIC', 'MOVE_HI_JUMP_KICK', 'MOVE_ICE_PUNCH'] -> ['MOVE_DETECT', 'MOVE_PSYCHO_CUT', 'MOVE_HI_JUMP_KICK', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 30 -> 248

## res/trainers/data/black_belt_ray.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/black_belt_ray.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/black_belt_jarrett.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/black_belt_jarrett.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_PRIORITIZE_EXTREMES'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/ranger_kyler.json
- party[0].species: 'SPECIES_EXEGGCUTE' -> 'SPECIES_EXEGGUTOR'
- party[0].level: 55 -> 75
- party[0].moves: None -> ['MOVE_LIGHT_SCREEN', 'MOVE_SYNTHESIS', 'MOVE_PSYCHIC', 'MOVE_LEAF_STORM']
- party[0].iv_scale: 50 -> 251
- party[1].level: 55 -> 75
- party[1].moves: None -> ['MOVE_DETECT', 'MOVE_SLASH', 'MOVE_X_SCISSOR', 'MOVE_CLOSE_COMBAT']
- party[1].iv_scale: 50 -> 246
- party[2].species: 'SPECIES_EMPOLEON' -> 'SPECIES_FERALIGATR'
- party[2].level: 58 -> 75
- party[2].moves: None -> ['MOVE_CRUNCH', 'MOVE_AQUA_TAIL', 'MOVE_SUPERPOWER', 'MOVE_ICE_FANG']
- party[2].iv_scale: 50 -> 254

## res/trainers/data/ranger_deshawn.json
- party[0].level: 54 -> 74
- party[0].moves: None -> ['MOVE_SUCKER_PUNCH', 'MOVE_DOUBLE_EDGE', 'MOVE_FIRE_PUNCH', 'MOVE_THRASH']
- party[0].iv_scale: 50 -> 254
- party[1].level: 54 -> 74
- party[1].moves: None -> ['MOVE_SUBSTITUTE', 'MOVE_SUCKER_PUNCH', 'MOVE_SHADOW_CLAW', 'MOVE_ICE_PUNCH']
- party[1].iv_scale: 50 -> 247
- party[2].level: 54 -> 74
- party[2].moves: None -> ['MOVE_HEADBUTT', 'MOVE_FIRE_PUNCH', 'MOVE_SUPERPOWER', 'MOVE_CRUNCH']
- party[2].iv_scale: 50 -> 215

## res/trainers/data/ranger_dwayne.json
- party[0].level: 54 -> 73
- party[0].moves: None -> ['MOVE_STEEL_WING', 'MOVE_BRAVE_BIRD', 'MOVE_STEALTH_ROCK', 'MOVE_NIGHT_SLASH']
- party[0].iv_scale: 50 -> 232
- party[1].level: 54 -> 73
- party[1].moves: None -> ['MOVE_AQUA_JET', 'MOVE_ZEN_HEADBUTT', 'MOVE_AMNESIA', 'MOVE_WATERFALL']
- party[1].iv_scale: 50 -> 248
- party[2].level: 54 -> 73
- party[2].moves: None -> ['MOVE_THUNDER_FANG', 'MOVE_ICE_SHARD', 'MOVE_EARTHQUAKE', 'MOVE_GIGA_IMPACT']
- party[2].iv_scale: 50 -> 254

## res/trainers/data/ranger_ashlee.json
- party size changed (2 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/ranger_felicia.json
- party[0].species: 'SPECIES_SKIPLOOM' -> 'SPECIES_JUMPLUFF'
- party[0].level: 59 -> 76
- party[0].moves: None -> ['MOVE_SLEEP_POWDER', 'MOVE_U_TURN', 'MOVE_BOUNCE', 'MOVE_SEED_BOMB']
- party[0].iv_scale: 50 -> 244
- party[1].level: 59 -> 76
- party[1].moves: None -> ['MOVE_DIZZY_PUNCH', 'MOVE_JUMP_KICK', 'MOVE_BOUNCE', 'MOVE_QUICK_ATTACK']
- party[1].iv_scale: 50 -> 204

## res/trainers/data/ranger_krista.json
- party[0].species: 'SPECIES_LAIRON' -> 'SPECIES_AGGRON'
- party[0].level: 57 -> 76
- party[0].moves: None -> ['MOVE_STONE_EDGE', 'MOVE_IRON_HEAD', 'MOVE_DOUBLE_EDGE', 'MOVE_METAL_BURST']
- party[0].iv_scale: 50 -> 255
- party[1].level: 57 -> 76
- party[1].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_BELLY_DRUM', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[1].iv_scale: 50 -> 199

## res/trainers/data/swimmer_glenn.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 53 -> 73
- party[0].moves: None -> ['MOVE_HYDRO_PUMP', 'MOVE_SIGNAL_BEAM', 'MOVE_ICE_BEAM', 'MOVE_HYPER_BEAM']
- party[0].iv_scale: 0 -> 240
- party[1].species: 'SPECIES_POLIWHIRL' -> 'SPECIES_POLITOED'
- party[1].level: 53 -> 73
- party[1].moves: None -> ['MOVE_PERISH_SONG', 'MOVE_ICE_BEAM', 'MOVE_SURF', 'MOVE_HYPER_VOICE']
- party[1].iv_scale: 0 -> 242

## res/trainers/data/swimmer_kurt.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_kurt.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_sam.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SEALEO' -> 'SPECIES_WALREIN'
- party[0].level: 53 -> 73
- party[0].moves: None -> ['MOVE_REST', 'MOVE_SURF', 'MOVE_BLIZZARD', 'MOVE_SHEER_COLD']
- party[0].iv_scale: 0 -> 240
- party[1].level: 53 -> 73
- party[1].moves: None -> ['MOVE_SURF', 'MOVE_EARTH_POWER', 'MOVE_HIDDEN_POWER', 'MOVE_RECOVER']
- party[1].iv_scale: 0 -> 241

## res/trainers/data/swimmer_wade.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/swimmer_wade.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/swimmer_joanna.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 52 -> 73
- party[0].moves: None -> ['MOVE_AQUA_RING', 'MOVE_SURF', 'MOVE_RAIN_DANCE', 'MOVE_BLIZZARD']
- party[0].iv_scale: 0 -> 247
- party[1].level: 54 -> 73
- party[1].moves: None -> ['MOVE_PSYCHIC', 'MOVE_THUNDER', 'MOVE_HYDRO_PUMP', 'MOVE_SHEER_COLD']
- party[1].iv_scale: 0 -> 243

## res/trainers/data/swimmer_sophia.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 53 -> 73
- party[0].moves: None -> ['MOVE_PRESENT', 'MOVE_ICE_BEAM', 'MOVE_NONE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 242
- party[1].level: 53 -> 73
- party[1].moves: None -> ['MOVE_CONFUSE_RAY', 'MOVE_SIGNAL_BEAM', 'MOVE_AQUA_RING', 'MOVE_HYDRO_PUMP']
- party[1].iv_scale: 0 -> 232

## res/trainers/data/swimmer_mallory.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_SURSKIT' -> 'SPECIES_MASQUERAIN'
- party[0].level: 52 -> 73
- party[0].moves: None -> ['MOVE_HYDRO_PUMP', 'MOVE_AIR_SLASH', 'MOVE_WHIRLWIND', 'MOVE_BUG_BUZZ']
- party[0].iv_scale: 0 -> 244
- party[1].species: 'SPECIES_LOMBRE' -> 'SPECIES_LUDICOLO'
- party[1].level: 54 -> 73
- party[1].moves: None -> ['MOVE_ENERGY_BALL', 'MOVE_LEECH_SEED', 'MOVE_RAIN_DANCE', 'MOVE_SURF']
- party[1].iv_scale: 0 -> 243

## res/trainers/data/swimmer_lydia.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MARILL' -> 'SPECIES_BLASTOISE'
- party[0].level: 54 -> 73
- party[0].moves: None -> ['MOVE_FLASH_CANNON', 'MOVE_ICE_BEAM', 'MOVE_RAIN_DANCE', 'MOVE_HYDRO_PUMP']
- party[0].iv_scale: 0 -> 248
- party[1].species: 'SPECIES_SPHEAL' -> 'SPECIES_WALREIN'
- party[1].level: 54 -> 73
- party[1].moves: None -> ['MOVE_REST', 'MOVE_SURF', 'MOVE_BLIZZARD', 'MOVE_SHEER_COLD']
- party[1].iv_scale: 0 -> 249
- party[2].species: 'SPECIES_WAILMER' -> 'SPECIES_WAILORD'
- party[2].level: 54 -> 73
- party[2].moves: None -> ['MOVE_AMNESIA', 'MOVE_ICE_BEAM', 'MOVE_REST', 'MOVE_HYDRO_PUMP']
- party[2].iv_scale: 0 -> 242

## res/trainers/data/veteran_harlan.json
- party[0].level: 57 -> 78
- party[0].iv_scale: 100 -> 248
- party[1].level: 58 -> 78
- party[1].moves: ['MOVE_EXPLOSION', 'MOVE_SHADOW_BALL', 'MOVE_TOXIC', 'MOVE_FLY'] -> ['MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_TOXIC', 'MOVE_AIR_CUTTER']
- party[1].iv_scale: 100 -> 249
- party[2].level: 59 -> 78
- party[2].moves: ['MOVE_LEAF_STORM', 'MOVE_FAINT_ATTACK', 'MOVE_EXTRASENSORY', 'MOVE_QUICK_ATTACK'] -> ['MOVE_LEAF_STORM', 'MOVE_DARK_PULSE', 'MOVE_EXTRASENSORY', 'MOVE_SHADOW_BALL']
- party[2].iv_scale: 100 -> 232

## res/trainers/data/rival_spear_pillar_piplup.json
- party[0].species: 'SPECIES_MUNCHLAX' -> 'SPECIES_SNORLAX'
- party[0].level: 40 -> 58
- party[0].moves: ['MOVE_BODY_SLAM', 'MOVE_STOCKPILE', 'MOVE_SWALLOW', 'MOVE_SCREECH'] -> ['MOVE_BODY_SLAM', 'MOVE_EARTHQUAKE', 'MOVE_FIRE_PUNCH', 'MOVE_REST']
- party[0].iv_scale: 200 -> 169
- party[0].ability/gender: 0/None -> 2/None
- party[1].level: 42 -> 58
- party[1].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK'] -> ['MOVE_DOUBLE_EDGE', 'MOVE_BRAVE_BIRD', 'MOVE_CLOSE_COMBAT', 'MOVE_QUICK_ATTACK']
- party[1].iv_scale: 200 -> 97
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[2].level: 40 -> 58
- party[2].moves: ['MOVE_AQUA_JET', 'MOVE_PURSUIT', 'MOVE_BRICK_BREAK', 'MOVE_IRON_TAIL'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_RECOVER']
- party[2].iv_scale: 200 -> 234
- party[2].ability/gender: 0/None -> 2/None
- party[3].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[3].level: 42 -> 58
- party[3].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRICK_BREAK', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_DRAGON_RUSH', 'MOVE_WATERFALL', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_WAVE']
- party[3].iv_scale: 200 -> 252
- party[3].ability/gender: 0/None -> 1/None
- party[4].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[4].level: 40 -> 58
- party[4].moves: ['MOVE_FIRE_BLAST', 'MOVE_WILL_O_WISP', 'MOVE_STOMP', 'MOVE_TAKE_DOWN'] -> ['MOVE_FLAMETHROWER', 'MOVE_ENERGY_BALL', 'MOVE_CONFUSE_RAY', 'MOVE_WILL_O_WISP']
- party[4].iv_scale: 200 -> 253
- party[4].ability/gender: 0/None -> 1/None
- party[5].level: 44 -> 59
- party[5].moves: ['MOVE_GIGA_DRAIN', 'MOVE_BITE', 'MOVE_LEECH_SEED', 'MOVE_SYNTHESIS'] -> ['MOVE_WOOD_HAMMER', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED']
- party[5].iv_scale: 200 -> 198
- party[5].ability/gender: 0/None -> 2/None

## res/trainers/data/cheryl_eterna_forest.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/riley_iron_island.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/marley_victory_road.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/buck_stark_mountain.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/mira_wayward_cave.json
- party size changed (1 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/lucas_jubilife_city_chimchar.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/lucas_jubilife_city_piplup.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/lucas_jubilife_city_turtwig.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/dawn_jubilife_city_chimchar.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/dawn_jubilife_city_piplup.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/dawn_jubilife_city_turtwig.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- items: ['ITEM_POTION'] -> []

## res/trainers/data/rival_spear_pillar_turtwig.json
- party[0].species: 'SPECIES_MUNCHLAX' -> 'SPECIES_SNORLAX'
- party[0].level: 40 -> 58
- party[0].moves: ['MOVE_BODY_SLAM', 'MOVE_STOCKPILE', 'MOVE_SWALLOW', 'MOVE_SCREECH'] -> ['MOVE_BODY_SLAM', 'MOVE_EARTHQUAKE', 'MOVE_FIRE_PUNCH', 'MOVE_REST']
- party[0].iv_scale: 200 -> 157
- party[0].ability/gender: 0/None -> 2/None
- party[1].level: 42 -> 58
- party[1].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_QUICK_ATTACK']
- party[1].iv_scale: 200 -> 85
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[2].level: 40 -> 58
- party[2].moves: ['MOVE_AQUA_JET', 'MOVE_PURSUIT', 'MOVE_BRICK_BREAK', 'MOVE_IRON_TAIL'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_ICE_BEAM', 'MOVE_RECOVER']
- party[2].iv_scale: 200 -> 222
- party[2].ability/gender: 0/None -> 2/None
- party[3].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[3].level: 42 -> 58
- party[3].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRICK_BREAK', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_DRAGON_RUSH', 'MOVE_WATERFALL', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_WAVE']
- party[3].iv_scale: 200 -> 252
- party[3].ability/gender: 0/None -> 1/None
- party[4].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[4].level: 40 -> 58
- party[4].moves: ['MOVE_GIGA_DRAIN', 'MOVE_TOXIC', 'MOVE_INGRAIN', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LEECH_SEED', 'MOVE_LOW_KICK']
- party[4].iv_scale: 200 -> 188
- party[4].ability/gender: 0/None -> 1/None
- party[5].level: 44 -> 59
- party[5].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_PUNISHMENT', 'MOVE_FLAME_WHEEL', 'MOVE_WILL_O_WISP'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH', 'MOVE_SLACK_OFF']
- party[5].iv_scale: 200 -> 90
- party[5].ability/gender: 0/None -> 1/None

## res/trainers/data/rival_spear_pillar_chimchar.json
- party[0].species: 'SPECIES_MUNCHLAX' -> 'SPECIES_SNORLAX'
- party[0].level: 40 -> 58
- party[0].moves: ['MOVE_BODY_SLAM', 'MOVE_STOCKPILE', 'MOVE_SWALLOW', 'MOVE_SCREECH'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[0].iv_scale: 200 -> 156
- party[0].ability/gender: 0/None -> 2/None
- party[1].level: 42 -> 58
- party[1].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_TAKE_DOWN', 'MOVE_QUICK_ATTACK'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_QUICK_ATTACK']
- party[1].iv_scale: 200 -> 84
- party[1].ability/gender: 0/None -> 1/None
- party[2].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[2].level: 40 -> 58
- party[2].moves: ['MOVE_GIGA_DRAIN', 'MOVE_TOXIC', 'MOVE_INGRAIN', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LEECH_SEED', 'MOVE_LOW_KICK']
- party[2].iv_scale: 200 -> 187
- party[2].ability/gender: 0/None -> 1/None
- party[3].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[3].level: 42 -> 58
- party[3].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRICK_BREAK', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_DRAGON_RUSH', 'MOVE_WATERFALL', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_WAVE']
- party[3].iv_scale: 200 -> 251
- party[3].ability/gender: 0/None -> 1/None
- party[4].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[4].level: 40 -> 58
- party[4].moves: ['MOVE_FIRE_BLAST', 'MOVE_WILL_O_WISP', 'MOVE_STOMP', 'MOVE_TAKE_DOWN'] -> ['MOVE_FLAMETHROWER', 'MOVE_ENERGY_BALL', 'MOVE_CONFUSE_RAY', 'MOVE_WILL_O_WISP']
- party[4].iv_scale: 200 -> 252
- party[4].ability/gender: 0/None -> 1/None
- party[5].level: 44 -> 59
- party[5].moves: ['MOVE_AQUA_JET', 'MOVE_AERIAL_ACE', 'MOVE_METAL_CLAW', 'MOVE_SWAGGER'] -> ['MOVE_WATERFALL', 'MOVE_EARTHQUAKE', 'MOVE_STEEL_WING', 'MOVE_SWORDS_DANCE']
- party[5].iv_scale: 200 -> 164
- party[5].ability/gender: 0/None -> 2/None

## res/trainers/data/lucas_veilstone_city_turtwig.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_FLAREON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_FLAMETHROWER', 'MOVE_SHADOW_BALL', 'MOVE_WILL_O_WISP', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_PRINPLUP' -> 'SPECIES_EMPOLEON'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_METAL_CLAW', 'MOVE_PECK', 'MOVE_GROWL'] -> ['MOVE_YAWN', 'MOVE_SIGNAL_BEAM', 'MOVE_BRINE', 'MOVE_FLASH_CANNON']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/lucas_veilstone_city_chimchar.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_VAPOREON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_WATER_PULSE', 'MOVE_SHADOW_BALL', 'MOVE_YAWN', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_GROTLE' -> 'SPECIES_TORTERRA'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_RAZOR_LEAF', 'MOVE_MEGA_DRAIN', 'MOVE_BITE', 'MOVE_CURSE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUPERPOWER', 'MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/lucas_veilstone_city_piplup.json
- class: 'TRAINER_CLASS_DP_PLAYER_MALE' -> 'TRAINER_CLASS_PLAYER_MALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_JOLTEON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_MONFERNO' -> 'SPECIES_INFERNAPE'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_FLAME_WHEEL', 'MOVE_MACH_PUNCH', 'MOVE_FURY_SWIPES', 'MOVE_TORMENT'] -> ['MOVE_MACH_PUNCH', 'MOVE_BLAZE_KICK', 'MOVE_THUNDER_PUNCH', 'MOVE_SLACK_OFF']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/dawn_veilstone_city_turtwig.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_FLAREON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_FLAMETHROWER', 'MOVE_SHADOW_BALL', 'MOVE_WILL_O_WISP', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_PRINPLUP' -> 'SPECIES_EMPOLEON'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_BUBBLE_BEAM', 'MOVE_METAL_CLAW', 'MOVE_PECK', 'MOVE_GROWL'] -> ['MOVE_YAWN', 'MOVE_SIGNAL_BEAM', 'MOVE_BRINE', 'MOVE_FLASH_CANNON']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/dawn_veilstone_city_chimchar.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_VAPOREON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_WATER_PULSE', 'MOVE_SHADOW_BALL', 'MOVE_YAWN', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_GROTLE' -> 'SPECIES_TORTERRA'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_RAZOR_LEAF', 'MOVE_MEGA_DRAIN', 'MOVE_BITE', 'MOVE_CURSE'] -> ['MOVE_SEED_BOMB', 'MOVE_SUPERPOWER', 'MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/dawn_veilstone_city_piplup.json
- class: 'TRAINER_CLASS_DP_PLAYER_FEMALE' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- party[0].species: 'SPECIES_CLEFAIRY' -> 'SPECIES_LOPUNNY'
- party[0].level: 25 -> 35
- party[0].moves: ['MOVE_METRONOME', 'MOVE_GRAVITY', 'MOVE_WAKE_UP_SLAP', 'MOVE_SING'] -> ['MOVE_QUICK_ATTACK', 'MOVE_JUMP_KICK', 'MOVE_FIRE_PUNCH', 'MOVE_THUNDER_PUNCH']
- party[0].iv_scale: 60 -> 200
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_JOLTEON'
- party[1].level: 25 -> 35
- party[1].moves: ['MOVE_PSYBEAM', 'MOVE_PSYCHO_CUT', 'MOVE_REFLECT', 'MOVE_LIGHT_SCREEN'] -> ['MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_FAKE_TEARS']
- party[1].iv_scale: 60 -> 200
- party[2].species: 'SPECIES_MONFERNO' -> 'SPECIES_INFERNAPE'
- party[2].level: 27 -> 36
- party[2].moves: ['MOVE_FLAME_WHEEL', 'MOVE_MACH_PUNCH', 'MOVE_FURY_SWIPES', 'MOVE_TORMENT'] -> ['MOVE_MACH_PUNCH', 'MOVE_BLAZE_KICK', 'MOVE_THUNDER_PUNCH', 'MOVE_SLACK_OFF']
- party[2].iv_scale: 60 -> 200

## res/trainers/data/dragon_tamer_patrick_rematch_1.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dragon_tamer_patrick_rematch_2.json
- party[0].species: 'SPECIES_SHELGON' -> 'SPECIES_SALAMENCE'
- party[1].species: 'SPECIES_GABITE' -> 'SPECIES_GARCHOMP'
- party[2].species: 'SPECIES_DRAGONAIR' -> 'SPECIES_DRAGONITE'

## res/trainers/data/psychic_maxwell_rematch.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN']
- party[0].species: 'SPECIES_MISDREAVUS' -> 'SPECIES_MISMAGIUS'
- party[0].level: 58 -> 80
- party[0].moves: None -> ['MOVE_SHADOW_BALL', 'MOVE_ENERGY_BALL', 'MOVE_CALM_MIND', 'MOVE_THUNDERBOLT']
- party[0].iv_scale: 0 -> 240
- party[1].level: 62 -> 80
- party[1].moves: None -> ['MOVE_DREAM_EATER', 'MOVE_HYPNOSIS', 'MOVE_DESTINY_BOND', 'MOVE_NIGHTMARE']
- party[1].iv_scale: 0 -> 250

## res/trainers/data/twins_teri_and_tia_rematch_1.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/twins_teri_and_tia_rematch_2.json
- party size changed (2 -> 4 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/guitarist_tony_rematch.json
- party[1].species: 'SPECIES_MAGNETON' -> 'SPECIES_LUDICOLO'

## res/trainers/data/ranger_taylor_rematch_1.json
- party[0].level: 34 -> 39
- party[0].moves: None -> ['MOVE_STOCKPILE', 'MOVE_SPIT_UP', 'MOVE_SWALLOW', 'MOVE_CRUNCH']
- party[0].iv_scale: 50 -> 251
- party[1].level: 36 -> 39
- party[1].moves: None -> ['MOVE_FIRE_FANG', 'MOVE_ROAR', 'MOVE_SWAGGER', 'MOVE_THUNDER_FANG']
- party[1].iv_scale: 50 -> 222

## res/trainers/data/ranger_allison_rematch_1.json
- party[0].species: 'SPECIES_AZUMARILL' -> 'SPECIES_KANGASKHAN'
- party[0].level: 35 -> 39
- party[0].moves: None -> ['MOVE_OUTRAGE', 'MOVE_CRUNCH', 'MOVE_DIZZY_PUNCH', 'MOVE_FIRE_PUNCH']
- party[0].iv_scale: 50 -> 214
- party[1].level: 35 -> 39
- party[1].moves: None -> ['MOVE_SEED_BOMB', 'MOVE_QUICK_ATTACK', 'MOVE_SYNTHESIS', 'MOVE_KNOCK_OFF']
- party[1].iv_scale: 50 -> 252

## res/trainers/data/ninja_boy_zach_rematch_1.json
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_PARAS'
- party[2].species: 'SPECIES_GOLBAT' -> 'SPECIES_GULPIN'

## res/trainers/data/ninja_boy_zach_rematch_2.json
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_PARASECT'
- party[2].species: 'SPECIES_GOLBAT' -> 'SPECIES_SWALOT'

## res/trainers/data/ninja_boy_zach_rematch_3.json
- party[0].species: 'SPECIES_GOLBAT' -> 'SPECIES_PARASECT'
- party[1].species: 'SPECIES_CROBAT' -> 'SPECIES_SWALOT'

## res/trainers/data/beauty_cyndy_rematch_1.json
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_LOUDRED'

## res/trainers/data/beauty_cyndy_rematch_2.json
- party[0].species: 'SPECIES_MEOWTH' -> 'SPECIES_PERSIAN'
- party[1].species: 'SPECIES_SKITTY' -> 'SPECIES_DELCATTY'
- party[2].species: 'SPECIES_GLAMEOW' -> 'SPECIES_EXPLOUD'

## res/trainers/data/tuber_jared_rematch_1.json
- party[1].species: 'SPECIES_SHELLOS' -> 'SPECIES_CHINCHOU'
- party[1].form: 1 -> 0

## res/trainers/data/tuber_jared_rematch_2.json
- party[1].species: 'SPECIES_GASTRODON' -> 'SPECIES_LANTURN'
- party[1].form: 1 -> 0

## res/trainers/data/dummy_779.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_779.json
- class: 'TRAINER_CLASS_CAMERAMAN' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_780.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_780.json
- class: 'TRAINER_CLASS_CAMERAMAN' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_781.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_781.json
- class: 'TRAINER_CLASS_CAMERAMAN' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_782.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_782.json
- class: 'TRAINER_CLASS_CAMERAMAN' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_783.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_783.json
- class: 'TRAINER_CLASS_CAMERAMAN' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_784.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_784.json
- class: 'TRAINER_CLASS_GUITARIST' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/dummy_787.json
- class: 'TRAINER_CLASS_GUITARIST' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_PIPLUP'
- party[0].level: 5 -> 9
- party[0].moves: None -> ['MOVE_POUND', 'MOVE_GROWL', 'MOVE_BUBBLE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 119

## res/trainers/data/dummy_788.json
- class: 'TRAINER_CLASS_GUITARIST' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_TURTWIG'
- party[0].level: 5 -> 9
- party[0].moves: None -> ['MOVE_TACKLE', 'MOVE_WITHDRAW', 'MOVE_ABSORB', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 114

## res/trainers/data/dummy_789.json
- class: 'TRAINER_CLASS_GUITARIST' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_CHIMCHAR'
- party[0].level: 5 -> 9
- party[0].moves: None -> ['MOVE_SCRATCH', 'MOVE_LEER', 'MOVE_EMBER', 'MOVE_TAUNT']
- party[0].iv_scale: 0 -> 110

## res/trainers/data/dummy_790.json
- class: 'TRAINER_CLASS_IDOL' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_PIPLUP'
- party[0].level: 5 -> 9
- party[0].moves: None -> ['MOVE_POUND', 'MOVE_GROWL', 'MOVE_BUBBLE', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 119

## res/trainers/data/dummy_791.json
- class: 'TRAINER_CLASS_IDOL' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_TURTWIG'
- party[0].level: 5 -> 9
- party[0].moves: None -> ['MOVE_TACKLE', 'MOVE_WITHDRAW', 'MOVE_ABSORB', 'MOVE_NONE']
- party[0].iv_scale: 0 -> 114

## res/trainers/data/dummy_792.json
- class: 'TRAINER_CLASS_IDOL' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_RATTATA' -> 'SPECIES_CHIMCHAR'
- party[0].level: 5 -> 9
- party[0].iv_scale: 0 -> 110

## res/trainers/data/dummy_793.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_793.json
- class: 'TRAINER_CLASS_IDOL' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_794.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_794.json
- class: 'TRAINER_CLASS_IDOL' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_799.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_799.json
- class: 'TRAINER_CLASS_CLOWN' -> 'TRAINER_CLASS_PLAYER_FEMALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_800.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_800.json
- class: 'TRAINER_CLASS_CLOWN' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_801.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_801.json
- class: 'TRAINER_CLASS_CLOWN' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/dummy_802.json
- party size changed (1 -> 3 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/dummy_802.json
- class: 'TRAINER_CLASS_CLOWN' -> 'TRAINER_CLASS_PLAYER_MALE'
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/tower_tycoon_palmer_dummy.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/tower_tycoon_palmer_dummy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_RISKY', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/ace_trainer_anton.json
- party[0].level: 44 -> 54
- party[0].moves: ['MOVE_ICE_BEAM', 'MOVE_CRUNCH', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_ICE_SHARD', 'MOVE_CRUNCH', 'MOVE_IRON_HEAD', 'MOVE_NONE']
- party[0].iv_scale: 50 -> 252

## res/trainers/data/ace_trainer_brenna.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/scientist_darrius.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_PORYGON2' -> 'SPECIES_PORYGON_Z'
- party[0].level: 42 -> 55
- party[0].iv_scale: 0 -> 251

## res/trainers/data/scientist_fredrick.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_KIRLIA' -> 'SPECIES_GARDEVOIR'
- party[0].level: 40 -> 53
- party[0].moves: ['MOVE_PSYCHIC', 'MOVE_MAGICAL_LEAF', 'MOVE_HYPNOSIS', 'MOVE_FUTURE_SIGHT'] -> ['MOVE_PSYCHIC', 'MOVE_CALM_MIND', 'MOVE_HYPNOSIS', 'MOVE_FOCUS_BLAST']
- party[0].iv_scale: 0 -> 244
- party[1].species: 'SPECIES_KADABRA' -> 'SPECIES_ALAKAZAM'
- party[1].level: 40 -> 53
- party[1].moves: ['MOVE_PSYCHIC', 'MOVE_PSYCHO_CUT', 'MOVE_THUNDER_WAVE', 'MOVE_RECOVER'] -> ['MOVE_PSYCHIC', 'MOVE_ENERGY_BALL', 'MOVE_THUNDER_WAVE', 'MOVE_RECOVER']
- party[1].iv_scale: 0 -> 253

## res/trainers/data/scientist_travon.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 20 -> 24
- party[0].moves: ['MOVE_CONFUSION', 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'] -> ['MOVE_PSYBEAM', 'MOVE_DISABLE', 'MOVE_SIGNAL_BEAM', 'MOVE_NONE']
- party[0].iv_scale: 20 -> 218

## res/trainers/data/poke_kid_janet.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].level: 42 -> 57
- party[0].moves: None -> ['MOVE_RAIN_DANCE', 'MOVE_HIDDEN_POWER', 'MOVE_LIGHT_SCREEN', 'MOVE_THUNDER']
- party[0].iv_scale: 0 -> 251
- party[1].level: 42 -> 57
- party[1].moves: None -> ['MOVE_SUBSTITUTE', 'MOVE_FOCUS_PUNCH', 'MOVE_FAKE_OUT', 'MOVE_VOLT_TACKLE']
- party[1].iv_scale: 0 -> 250

## res/trainers/data/galactic_grunt_iron_island_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_YANMEGA'
- party[0].level: 34 -> 46
- party[0].moves: None -> ['MOVE_ANCIENT_POWER', 'MOVE_SILVER_WIND', 'MOVE_GIGA_DRAIN', 'MOVE_TAILWIND']
- party[0].iv_scale: 30 -> 239
- party[1].species: 'SPECIES_HOUNDOUR' -> 'SPECIES_KECLEON'
- party[1].level: 34 -> 46
- party[1].moves: None -> ['MOVE_SLASH', 'MOVE_ICE_PUNCH', 'MOVE_SUBSTITUTE', 'MOVE_SUCKER_PUNCH']
- party[1].iv_scale: 30 -> 231
- party[2].species: 'SPECIES_GOLBAT' -> 'SPECIES_SOLROCK'
- party[2].level: 34 -> 46
- party[2].moves: None -> ['MOVE_EARTHQUAKE', 'MOVE_STONE_EDGE', 'MOVE_IRON_HEAD', 'MOVE_ZEN_HEADBUTT']
- party[2].iv_scale: 30 -> 245

## res/trainers/data/galactic_grunt_iron_island_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_PURUGLY'
- party[0].level: 34 -> 46
- party[0].moves: None -> ['MOVE_FAKE_OUT', 'MOVE_SLASH', 'MOVE_SUCKER_PUNCH', 'MOVE_SHADOW_CLAW']
- party[0].iv_scale: 30 -> 230
- party[1].species: 'SPECIES_STUNKY' -> 'SPECIES_SKUNTANK'
- party[1].level: 34 -> 46
- party[1].moves: None -> ['MOVE_TOXIC', 'MOVE_DARK_PULSE', 'MOVE_FLAMETHROWER', 'MOVE_SLUDGE_BOMB']
- party[1].iv_scale: 30 -> 228
- party[2].species: 'SPECIES_CROAGUNK' -> 'SPECIES_TOXICROAK'
- party[2].level: 34 -> 46
- party[2].moves: None -> ['MOVE_POISON_JAB', 'MOVE_SUCKER_PUNCH', 'MOVE_FOCUS_PUNCH', 'MOVE_X_SCISSOR']
- party[2].iv_scale: 30 -> 212

## res/trainers/data/rival_survival_area_1_piplup.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_DRAGON_CLAW', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_LEAF_STORM', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_LEECH_SEED'] -> ['MOVE_WOOD_HAMMER', 'MOVE_EARTHQUAKE', 'MOVE_STONE_EDGE', 'MOVE_LEECH_SEED']

## res/trainers/data/rival_survival_area_1_turtwig.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_DRAGON_CLAW', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[3].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_FLAMETHROWER', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_CLAW', 'MOVE_AERIAL_ACE'] -> ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_U_TURN', 'MOVE_SLACK_OFF']

## res/trainers/data/rival_survival_area_1_chimchar.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[1].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_DRAGON_CLAW', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_HYDRO_PUMP', 'MOVE_METAL_CLAW', 'MOVE_DRILL_PECK', 'MOVE_SHADOW_CLAW'] -> ['MOVE_HYDRO_PUMP', 'MOVE_ICE_BEAM', 'MOVE_FLASH_CANNON', 'MOVE_AGILITY']

## res/trainers/data/rival_survival_area_unused_piplup.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_MEGAHORN', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_LEAF_STORM', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_STONE_EDGE'] -> ['MOVE_WOOD_HAMMER', 'MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED', 'MOVE_STONE_EDGE']

## res/trainers/data/rival_survival_area_unused_turtwig.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[3].moves: ['MOVE_SLUDGE_BOMB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_FLARE_BLITZ', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_CLAW', 'MOVE_AERIAL_ACE'] -> ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_U_TURN', 'MOVE_SLACK_OFF']

## res/trainers/data/rival_survival_area_unused_chimchar.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[1].moves: ['MOVE_SLUDGE_BOMB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_ROCK_SLIDE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_MEGAHORN', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_HYDRO_PUMP', 'MOVE_METAL_CLAW', 'MOVE_DRILL_PECK', 'MOVE_ICE_BEAM'] -> ['MOVE_HYDRO_PUMP', 'MOVE_AGILITY', 'MOVE_FLASH_CANNON', 'MOVE_ICE_BEAM']

## res/trainers/data/galactic_grunt_valley_windworks_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_GLAMEOW' -> 'SPECIES_GULPIN'
- party[0].level: 13 -> 14
- party[0].moves: None -> ['MOVE_POISON_GAS', 'MOVE_SLUDGE', 'MOVE_YAWN', 'MOVE_POUND']
- party[0].iv_scale: 30 -> 153

## res/trainers/data/worker_dillan.json
- party size changed (2 -> 1 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/worker_dillan.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/worker_holden.json
- party size changed (3 -> 2 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/worker_holden.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']

## res/trainers/data/worker_conrad.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_MAGMAR' -> 'SPECIES_MAGMORTAR'
- party[0].level: 35 -> 46
- party[0].moves: None -> ['MOVE_CONFUSE_RAY', 'MOVE_FLARE_BLITZ', 'MOVE_THUNDER_PUNCH', 'MOVE_MACH_PUNCH']
- party[0].iv_scale: 0 -> 255

## res/trainers/data/galactic_grunt_valor_lakefront.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_CROAGUNK' -> 'SPECIES_TOXICROAK'
- party[0].level: 31 -> 41
- party[0].moves: None -> ['MOVE_CROSS_CHOP', 'MOVE_SUCKER_PUNCH', 'MOVE_ICE_PUNCH', 'MOVE_POISON_JAB']
- party[0].iv_scale: 30 -> 251

## res/trainers/data/galactic_grunt_veilstone_city_1.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_SWALOT'
- party[0].level: 24 -> 35
- party[0].moves: None -> ['MOVE_SLUDGE_BOMB', 'MOVE_SHADOW_BALL', 'MOVE_DESTINY_BOND', 'MOVE_TOXIC']
- party[0].iv_scale: 30 -> 222
- party[1].species: 'SPECIES_STUNKY' -> 'SPECIES_SKUNTANK'
- party[1].level: 26 -> 35
- party[1].moves: None -> ['MOVE_SLUDGE_BOMB', 'MOVE_TOXIC', 'MOVE_DARK_PULSE', 'MOVE_FLAMETHROWER']
- party[1].iv_scale: 30 -> 227

## res/trainers/data/galactic_grunt_veilstone_city_2.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT']
- party[0].species: 'SPECIES_ZUBAT' -> 'SPECIES_VENOMOTH'
- party[0].level: 24 -> 35
- party[0].moves: None -> ['MOVE_SLUDGE_BOMB', 'MOVE_PSYCHIC', 'MOVE_SLEEP_POWDER', 'MOVE_SILVER_WIND']
- party[0].iv_scale: 30 -> 204
- party[1].species: 'SPECIES_CROAGUNK' -> 'SPECIES_VICTREEBEL'
- party[1].level: 26 -> 35
- party[1].moves: None -> ['MOVE_SEED_BOMB', 'MOVE_SLEEP_POWDER', 'MOVE_SUCKER_PUNCH', 'MOVE_SWEET_SCENT']
- party[1].iv_scale: 30 -> 232

## res/trainers/data/rival_route_201_piplup.json
- party[0].iv_scale: 0 -> 144

## res/trainers/data/rival_route_201_turtwig.json
- party[0].iv_scale: 0 -> 179

## res/trainers/data/rival_route_201_chimchar.json
- party[0].iv_scale: 0 -> 136

## res/trainers/data/leader_candice_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_candice_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/leader_maylene_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_volkner_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_volkner_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/leader_byron_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_byron_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/leader_gardenia_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_gardenia_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/leader_roark_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_roark_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/leader_wake_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_wake_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/leader_fantina_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/leader_fantina_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/riley_battleground.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/riley_battleground.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/buck_battleground.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/buck_battleground.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/marley_battleground.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/marley_battleground.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/mira_battleground.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/mira_battleground.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/cheryl_battleground.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/cheryl_battleground.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/elite_four_aaron_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_aaron_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_BATON_PASS']

## res/trainers/data/elite_four_bertha_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_bertha_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/elite_four_flint_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_flint_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_WEATHER']

## res/trainers/data/elite_four_lucian_rematch.json
- party size changed (5 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/elite_four_lucian_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []

## res/trainers/data/champion_cynthia_rematch.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- party[0].level: 74 -> 89
- party[0].item: 'ITEM_NONE' -> 'ITEM_SITRUS_BERRY'
- party[0].moves: ['MOVE_DARK_PULSE', 'MOVE_PSYCHIC', 'MOVE_SILVER_WIND', 'MOVE_OMINOUS_WIND'] -> ['MOVE_SHADOW_BALL', 'MOVE_DARK_PULSE', 'MOVE_PSYCHIC', 'MOVE_WILL_O_WISP']
- party[0].iv_scale: 250 -> 254
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_PORYGON_Z'
- party[1].level: 74 -> 89
- party[1].item: 'ITEM_NONE' -> 'ITEM_CHOICE_SPECS'
- party[1].moves: ['MOVE_ENERGY_BALL', 'MOVE_SLUDGE_BOMB', 'MOVE_SHADOW_BALL', 'MOVE_EXTRASENSORY'] -> ['MOVE_HYPER_BEAM', 'MOVE_ICE_BEAM', 'MOVE_THUNDERBOLT', 'MOVE_PSYCHIC']
- party[1].iv_scale: 250 -> 228
- party[2].level: 76 -> 89
- party[2].item: 'ITEM_NONE' -> 'ITEM_LEFTOVERS'
- party[2].moves: ['MOVE_AIR_SLASH', 'MOVE_AURA_SPHERE', 'MOVE_WATER_PULSE', 'MOVE_PSYCHIC'] -> ['MOVE_AIR_SLASH', 'MOVE_AURA_SPHERE', 'MOVE_THUNDER_WAVE', 'MOVE_FLAMETHROWER']
- party[2].iv_scale: 250 -> 234
- party[3].level: 76 -> 89
- party[3].item: 'ITEM_NONE' -> 'ITEM_CHOICE_BAND'
- party[3].moves: ['MOVE_AURA_SPHERE', 'MOVE_DRAGON_PULSE', 'MOVE_PSYCHIC', 'MOVE_EARTHQUAKE'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BULLET_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ICE_PUNCH']
- party[3].iv_scale: 250 -> 211
- party[4].level: 74 -> 89
- party[4].item: 'ITEM_NONE' -> 'ITEM_FLAME_ORB'
- party[4].moves: ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_MIRROR_COAT', 'MOVE_AQUA_RING'] -> ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_MIRROR_COAT', 'MOVE_RECOVER']
- party[5].level: 78 -> 90
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_YACHE_BERRY'
- party[5].moves: ['MOVE_DRAGON_RUSH', 'MOVE_EARTHQUAKE', 'MOVE_BRICK_BREAK', 'MOVE_GIGA_IMPACT'] -> ['MOVE_OUTRAGE', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_FIRE_FANG']
- party[5].iv_scale: 250 -> 213

## res/trainers/data/rival_survival_area_2_piplup.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_STONE_EDGE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_MEGAHORN', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_GIGA_IMPACT', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_LEAF_STORM', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_STONE_EDGE'] -> ['MOVE_WOOD_HAMMER', 'MOVE_EARTHQUAKE', 'MOVE_LEECH_SEED', 'MOVE_STONE_EDGE']

## res/trainers/data/rival_survival_area_2_turtwig.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].item: 'ITEM_NONE' -> 'ITEM_WISE_GLASSES'
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_SURF', 'MOVE_ICE_BEAM', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_STONE_EDGE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[3].moves: ['MOVE_SLUDGE_BOMB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_GIGA_IMPACT', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_FLARE_BLITZ', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_CLAW', 'MOVE_AERIAL_ACE'] -> ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_U_TURN', 'MOVE_SLACK_OFF']

## res/trainers/data/rival_survival_area_2_chimchar.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']
- party[0].item: 'ITEM_NONE' -> 'ITEM_MUSCLE_BAND'
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_QUICK_ATTACK', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].item: 'ITEM_NONE' -> 'ITEM_FOCUS_SASH'
- party[1].moves: ['MOVE_SLUDGE_BOMB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].item: 'ITEM_NONE' -> 'ITEM_LIFE_ORB'
- party[2].moves: ['MOVE_MEGAHORN', 'MOVE_CLOSE_COMBAT', 'MOVE_NIGHT_SLASH', 'MOVE_STONE_EDGE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].item: 'ITEM_NONE' -> 'ITEM_SCOPE_LENS'
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_MEGAHORN', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[4].item: 'ITEM_NONE' -> 'ITEM_LUM_BERRY'
- party[4].moves: ['MOVE_GIGA_IMPACT', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ZEN_HEADBUTT'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_CURSE']
- party[5].item: 'ITEM_SITRUS_BERRY' -> 'ITEM_LEFTOVERS'
- party[5].moves: ['MOVE_HYDRO_PUMP', 'MOVE_METAL_CLAW', 'MOVE_DRILL_PECK', 'MOVE_ICE_BEAM'] -> ['MOVE_HYDRO_PUMP', 'MOVE_FLASH_CANNON', 'MOVE_AGILITY', 'MOVE_ICE_BEAM']

## res/trainers/data/hall_matron_argenta_dummy.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/hall_matron_argenta_dummy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_RISKY', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/factory_head_thorton_dummy.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/factory_head_thorton_dummy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_RISKY', 'AI_FLAG_PRIORITIZE_EXTREMES']

## res/trainers/data/arcade_star_dahlia_dummy.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/arcade_star_dahlia_dummy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_RISKY', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/castle_valet_darach_dummy.json
- party size changed (1 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/castle_valet_darach_dummy.json
- ai_flags: ['AI_FLAG_BASIC'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_SETUP_FIRST_TURN', 'AI_FLAG_RISKY', 'AI_FLAG_PRIORITIZE_EXTREMES', 'AI_FLAG_CHECK_HP']

## res/trainers/data/galactic_boss_cyrus_celestic_town_ruins.json
- party size changed (3 -> 6 mons); needs a human to add/remove party-member objects, not applied

## res/trainers/data/galactic_boss_cyrus_celestic_town_ruins.json
- items: ['ITEM_HYPER_POTION'] -> []

## res/trainers/data/leader_volkner_fight_area.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- party[0].level: 56 -> 74
- party[0].iv_scale: 200 -> 236
- party[1].level: 56 -> 74
- party[1].moves: ['MOVE_PIN_MISSILE', 'MOVE_CHARGE_BEAM', 'MOVE_DOUBLE_KICK', 'MOVE_QUICK_ATTACK'] -> ['MOVE_THUNDER', 'MOVE_SHADOW_BALL', 'MOVE_SIGNAL_BEAM', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 200 -> 237
- party[2].level: 58 -> 75
- party[2].moves: ['MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_BRICK_BREAK', 'MOVE_GIGA_IMPACT'] -> ['MOVE_THUNDER_PUNCH', 'MOVE_FIRE_PUNCH', 'MOVE_CROSS_CHOP', 'MOVE_GIGA_IMPACT']
- party[2].iv_scale: 200 -> 251

## res/trainers/data/elite_four_flint_fight_area.json
- items: ['ITEM_FULL_RESTORE', 'ITEM_FULL_RESTORE'] -> []
- party[0].level: 56 -> 74
- party[0].iv_scale: 250 -> 242
- party[1].species: 'SPECIES_FLAREON' -> 'SPECIES_ARCANINE'
- party[1].level: 56 -> 74
- party[1].moves: ['MOVE_OVERHEAT', 'MOVE_GIGA_IMPACT', 'MOVE_QUICK_ATTACK', 'MOVE_WILL_O_WISP'] -> ['MOVE_FLARE_BLITZ', 'MOVE_THUNDER_FANG', 'MOVE_IRON_HEAD', 'MOVE_CRUNCH']
- party[1].iv_scale: 250 -> 240
- party[2].level: 58 -> 75
- party[2].moves: ['MOVE_FLAMETHROWER', 'MOVE_THUNDERBOLT', 'MOVE_SOLAR_BEAM', 'MOVE_HYPER_BEAM'] -> ['MOVE_FIRE_BLAST', 'MOVE_THUNDERBOLT', 'MOVE_SOLAR_BEAM', 'MOVE_HYPER_BEAM']
- party[2].iv_scale: 250 -> 248

## res/trainers/data/rival_fight_area_piplup.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 53 -> 74
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 245
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 52 -> 74
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_HYDRO_PUMP', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[1].iv_scale: 200 -> 254
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 53 -> 74
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[2].iv_scale: 200 -> 255
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 52 -> 74
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[3].iv_scale: 200 -> 234
- party[4].level: 54 -> 74
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 246
- party[5].level: 56 -> 75
- party[5].moves: ['MOVE_LEAF_STORM', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_SYNTHESIS'] -> ['MOVE_WOOD_HAMMER', 'MOVE_EARTHQUAKE', 'MOVE_CRUNCH', 'MOVE_LEECH_SEED']
- party[5].iv_scale: 200 -> 252

## res/trainers/data/rival_fight_area_turtwig.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 53 -> 74
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 245
- party[1].species: 'SPECIES_FLOATZEL' -> 'SPECIES_STARMIE'
- party[1].level: 52 -> 74
- party[1].moves: ['MOVE_AQUA_JET', 'MOVE_CRUNCH', 'MOVE_ICE_FANG', 'MOVE_BRICK_BREAK'] -> ['MOVE_HYDRO_PUMP', 'MOVE_PSYCHIC', 'MOVE_THUNDERBOLT', 'MOVE_RECOVER']
- party[1].iv_scale: 200 -> 254
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 53 -> 74
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_OUTRAGE', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[2].iv_scale: 200 -> 255
- party[3].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[3].level: 52 -> 74
- party[3].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[3].iv_scale: 200 -> 253
- party[4].level: 54 -> 74
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 246
- party[5].level: 56 -> 75
- party[5].moves: ['MOVE_FLAMETHROWER', 'MOVE_FOCUS_BLAST', 'MOVE_SHADOW_CLAW', 'MOVE_AERIAL_ACE'] -> ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_THUNDER_PUNCH', 'MOVE_SLACK_OFF']
- party[5].iv_scale: 200 -> 249

## res/trainers/data/rival_fight_area_chimchar.json
- ai_flags: ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT'] -> ['AI_FLAG_BASIC', 'AI_FLAG_EVAL_ATTACK', 'AI_FLAG_EXPERT', 'AI_FLAG_PRIORITIZE_EXTREMES']
- party[0].level: 53 -> 74
- party[0].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_AERIAL_ACE', 'MOVE_STEEL_WING', 'MOVE_U_TURN'] -> ['MOVE_CLOSE_COMBAT', 'MOVE_BRAVE_BIRD', 'MOVE_DOUBLE_EDGE', 'MOVE_U_TURN']
- party[0].iv_scale: 200 -> 245
- party[1].species: 'SPECIES_ROSERADE' -> 'SPECIES_SHIFTRY'
- party[1].level: 52 -> 74
- party[1].moves: ['MOVE_POISON_JAB', 'MOVE_GIGA_DRAIN', 'MOVE_SHADOW_BALL', 'MOVE_GRASS_WHISTLE'] -> ['MOVE_SWORDS_DANCE', 'MOVE_SEED_BOMB', 'MOVE_SUCKER_PUNCH', 'MOVE_LOW_KICK']
- party[1].iv_scale: 200 -> 253
- party[2].species: 'SPECIES_HERACROSS' -> 'SPECIES_DRAGONITE'
- party[2].level: 53 -> 74
- party[2].moves: ['MOVE_CLOSE_COMBAT', 'MOVE_ROCK_SLIDE', 'MOVE_NIGHT_SLASH', 'MOVE_AERIAL_ACE'] -> ['MOVE_DRAGON_CLAW', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_ROOST']
- party[2].iv_scale: 200 -> 255
- party[3].species: 'SPECIES_RAPIDASH' -> 'SPECIES_NINETALES'
- party[3].level: 52 -> 74
- party[3].moves: ['MOVE_FIRE_BLAST', 'MOVE_SUNNY_DAY', 'MOVE_BOUNCE', 'MOVE_WILL_O_WISP'] -> ['MOVE_FIRE_BLAST', 'MOVE_ENERGY_BALL', 'MOVE_HYPNOSIS', 'MOVE_WILL_O_WISP']
- party[3].iv_scale: 200 -> 234
- party[4].level: 54 -> 74
- party[4].moves: ['MOVE_BODY_SLAM', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST'] -> ['MOVE_BODY_SLAM', 'MOVE_FIRE_PUNCH', 'MOVE_EARTHQUAKE', 'MOVE_REST']
- party[4].iv_scale: 200 -> 246
- party[5].level: 56 -> 75
- party[5].moves: ['MOVE_BRINE', 'MOVE_AERIAL_ACE', 'MOVE_METAL_CLAW', 'MOVE_SHADOW_CLAW'] -> ['MOVE_HYDRO_PUMP', 'MOVE_ICE_BEAM', 'MOVE_FLASH_CANNON', 'MOVE_YAWN']
- party[5].iv_scale: 200 -> 253

## res/trainers/data/commander_mars_stark_mountain.json
- party[0].species: 'SPECIES_BRONZONG' -> 'SPECIES_SOLROCK'
- party[0].level: 58 -> 77
- party[0].moves: ['MOVE_GYRO_BALL', 'MOVE_EXTRASENSORY', 'MOVE_LIGHT_SCREEN', 'MOVE_CONFUSE_RAY'] -> ['MOVE_ZEN_HEADBUTT', 'MOVE_STONE_EDGE', 'MOVE_LIGHT_SCREEN', 'MOVE_WILL_O_WISP']
- party[0].iv_scale: 200 -> 248
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_PERSIAN'
- party[1].level: 58 -> 77
- party[1].moves: ['MOVE_AIR_CUTTER', 'MOVE_BITE', 'MOVE_POISON_FANG', 'MOVE_CONFUSE_RAY'] -> ['MOVE_FAKE_OUT', 'MOVE_HEADBUTT', 'MOVE_AERIAL_ACE', 'MOVE_U_TURN']
- party[1].iv_scale: 200 -> 226
- party[2].level: 60 -> 78
- party[2].iv_scale: 200 -> 233

## res/trainers/data/commander_jupiter_stark_mountain.json
- party[0].species: 'SPECIES_BRONZONG' -> 'SPECIES_LUNATONE'
- party[0].level: 58 -> 77
- party[0].moves: ['MOVE_GYRO_BALL', 'MOVE_EXTRASENSORY', 'MOVE_ROCK_SLIDE', 'MOVE_REFLECT'] -> ['MOVE_PSYCHIC', 'MOVE_ANCIENT_POWER', 'MOVE_EARTH_POWER', 'MOVE_STEALTH_ROCK']
- party[0].iv_scale: 200 -> 249
- party[1].species: 'SPECIES_GOLBAT' -> 'SPECIES_DELCATTY'
- party[1].level: 58 -> 77
- party[1].moves: ['MOVE_SLUDGE_BOMB', 'MOVE_AIR_CUTTER', 'MOVE_GIGA_DRAIN', 'MOVE_MEAN_LOOK'] -> ['MOVE_ICE_BEAM', 'MOVE_THUNDERBOLT', 'MOVE_SHADOW_BALL', 'MOVE_THUNDER_WAVE']
- party[1].iv_scale: 200 -> 225
- party[2].level: 60 -> 78
- party[2].iv_scale: 200 -> 238

