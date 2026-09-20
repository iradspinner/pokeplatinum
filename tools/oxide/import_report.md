# Base ROM import report

base: `base.nds`  vanilla: `vanilla.nds`  dry run: False

Files changed: {'species': 0, 'moves': 0, 'trainers': 0, 'trainers_party_resized': 153, 'encounters': 0, 'npc_trades': 0, 'text': 0, 'map_headers': 0, 'events': 70, 'heights': 0, 'items': 0}

## pl_enc_data.narc (partially imported)
- 241 differing values in unown_table, rate_form0, rate_form1, rate_form2, rate_form3, rate_form4 were not carried over; see ENCOUNTER_SKIP_KEYS in this importer for why

## TEXT_BANK_WAYWARD_CAVE_1F[6]
- unused slot gained or lost text; skipped: ('garbage', 29) -> 'Please leave me alone!!\r'

## TEXT_BANK_WAYWARD_CAVE_1F[7]
- unused slot gained or lost text; skipped: ('garbage', 29) -> 'Sorry I got terrified...\r'

## TEXT_BANK_MENU_ENTRIES[24]
- unused slot gained or lost text; skipped: ('garbage', 8) -> ('garbage', 0)

## TEXT_BANK_MENU_ENTRIES[30]
- unused slot gained or lost text; skipped: ('garbage', 8) -> 'Repel'

## TEXT_BANK_MENU_ENTRIES[31]
- unused slot gained or lost text; skipped: ('garbage', 8) -> 'Super Repel'

## TEXT_BANK_MENU_ENTRIES[32]
- unused slot gained or lost text; skipped: ('garbage', 8) -> 'Max Repel'

## TEXT_BANK_MENU_ENTRIES[57]
- unused slot gained or lost text; skipped: ('garbage', 1) -> 'Teleport System'

## TEXT_BANK_MENU_ENTRIES[84]
- unused slot gained or lost text; skipped: ('garbage', 8) -> 'Potential Rater'

## TEXT_BANK_MENU_ENTRIES[85]
- unused slot gained or lost text; skipped: ('garbage', 8) -> 'Name Rater APP'

## TEXT_BANK_MENU_ENTRIES[86]
- unused slot gained or lost text; skipped: ('garbage', 10) -> 'Hidden Power APP'

## TEXT_BANK_MENU_ENTRIES[87]
- unused slot gained or lost text; skipped: ('garbage', 4) -> 'Happiness Up'

## TEXT_BANK_MENU_ENTRIES[88]
- unused slot gained or lost text; skipped: ('garbage', 4) -> 'Legendary Reset'

## TEXT_BANK_MENU_ENTRIES[89]
- unused slot gained or lost text; skipped: ('garbage', 4) -> 'Superbosses/Gyms Reset'

## TEXT_BANK_MENU_ENTRIES[90]
- unused slot gained or lost text; skipped: ('garbage', 4) -> 'Trades/Gifts Reset'

## TEXT_BANK_MENU_ENTRIES[93]
- unused slot gained or lost text; skipped: ('garbage', 7) -> 'Online Shop'

## TEXT_BANK_FIELD_MOVES[7]
- unused slot gained or lost text; skipped: ('garbage', 54) -> 'The water is a deep blue color...\n'

## pl_msg.narc (partially imported)
- 60 banks changed message count and are left for the script carry-over: TEXT_BANK_JUBILIFE_CITY (101->117), TEXT_BANK_JUBILIFE_CITY_SOUTH_HOUSE_1F (3->9), TEXT_BANK_CANALAVE_CITY (44->51), TEXT_BANK_CANALAVE_CITY_GYM (10->20), TEXT_BANK_CANALAVE_LIBRARY_2F (14->24), TEXT_BANK_OREBURGH_CITY (31->41), TEXT_BANK_OREBURGH_CITY_GYM (10->16), TEXT_BANK_OREBURGH_CITY_MIDDLE_HOUSE (2->8), TEXT_BANK_ETERNA_CITY (43->55), TEXT_BANK_ETERNA_CITY_GYM (17->23), TEXT_BANK_ETERNA_CITY_CONDOMINIUMS_1F (16->22), TEXT_BANK_HEARTHOME_CITY (61->73), TEXT_BANK_HEARTHOME_CITY_GYM_LEADER_ROOM (9->15), TEXT_BANK_HEARTHOME_CITY_POKEMON_FAN_CLUB (14->26), TEXT_BANK_PASTORIA_CITY (45->55), TEXT_BANK_PASTORIA_CITY_GYM (10->20), TEXT_BANK_PASTORIA_CITY_NORTH_HOUSE (3->12), TEXT_BANK_VEILSTONE_CITY (69->80), TEXT_BANK_VEILSTONE_CITY_GYM (13->23), TEXT_BANK_VEILSTONE_CITY_NORTHEAST_HOUSE (9->15), TEXT_BANK_SUNYSHORE_CITY (28->39), TEXT_BANK_SUNYSHORE_CITY_GYM_ROOM_1 (5->7), TEXT_BANK_SUNYSHORE_CITY_GYM_ROOM_3 (6->14), TEXT_BANK_SNOWPOINT_CITY (20->39), TEXT_BANK_SNOWPOINT_CITY_GYM (10->20), TEXT_BANK_POKEMON_LEAGUE (3->15), TEXT_BANK_POKEMON_LEAGUE_CHAMPION_ROOM (4->5), TEXT_BANK_FIGHT_AREA (52->58), TEXT_BANK_COMMON_STRINGS (132->256), TEXT_BANK_ETERNA_FOREST (16->17), TEXT_BANK_VICTORY_ROAD_1F_ROOM_2 (12->13), TEXT_BANK_FLOAROMA_MEADOW_HOUSE (2->8), TEXT_BANK_STARK_MOUNTAIN_OUTSIDE (10->17), TEXT_BANK_STARK_MOUNTAIN_ROOM_1 (10->14), TEXT_BANK_STARK_MOUNTAIN_ROOM_2 (12->9), TEXT_BANK_TURNBACK_CAVE_ENTRANCE (2->4), TEXT_BANK_TURNBACK_CAVE_GIRATINA_ROOM (5->12), TEXT_BANK_IRON_ISLAND (6->8), TEXT_BANK_ROUTE_201 (63->71), TEXT_BANK_ROUTE_202 (20->22), TEXT_BANK_ROUTE_207 (14->24), TEXT_BANK_ROUTE_210_SOUTH (12->14), TEXT_BANK_POKEMON_MANSION_OFFICE (23->27), TEXT_BANK_ROUTE_221 (3->5), TEXT_BANK_ROUTE_224 (13->15), TEXT_BANK_ROUTE_227 (13->14), TEXT_BANK_TWINLEAF_TOWN (15->40), TEXT_BANK_SANDGEM_TOWN (30->35), TEXT_BANK_SANDGEM_TOWN_HOUSE (2->8), TEXT_BANK_FLOAROMA_TOWN (15->19), TEXT_BANK_FLOAROMA_TOWN_MIDDLE_HOUSE (6->13), TEXT_BANK_SOLACEON_TOWN (15->20), TEXT_BANK_POKEMON_DAY_CARE (3->20), TEXT_BANK_SOLACEON_TOWN_NORTHEAST_HOUSE (2->8), TEXT_BANK_SOLACEON_TOWN_NORTH_HOUSE (2->129), TEXT_BANK_CELESTIC_TOWN (18->26), TEXT_BANK_SURVIVAL_AREA (14->19), TEXT_BANK_BATTLEGROUND (144->66), TEXT_BANK_SURVIVAL_AREA_SOUTH_HOUSE (2->129), TEXT_BANK_RESORT_AREA (28->37)
- TEXT_BANK_SPECIES_NAME: skipped, species names decode identically; the bank differs only in bytes the decoder does not read
- TEXT_BANK_SPECIES_POKEDEX_ENTRY_EN: skipped, Pokedex entries decode identically, same as species names
- TEXT_BANK_NPC_TRAINER_MESSAGES: skipped, trainer battle messages are keyed by TRMSG_* type per trainer, not by a flat bank index; mapping the 2,497 entries back needs trainerproc's packing order, which is its own job

## res/field/events/events_trainers_school.json
- object_events[8].script: 7258 -> 7057

## res/field/events/events_team_galactic_eterna_building_2f.json
- object_events[4].script: 7262 -> 7059

## res/field/events/events_team_galactic_eterna_building_3f.json
- object_events[3].script: 7263 -> 7061

## res/field/events/events_team_galactic_eterna_building_4f.json
- object_events[4].script: 7277 -> 7028
- object_events[5].script: 7264 -> 7073
- object_events[6].script: 7265 -> 7252

## res/field/events/events_veilstone_city_galactic_warehouse.json
- object_events[0].script: 7111 -> 7108
- object_events[1].script: 7236 -> 7421

## res/field/events/events_oreburgh_mine_b1f.json
- object_events[1].script: 7235 -> 7004

## res/field/events/events_eterna_forest_outside.json
- object_events[8].script: 7028 -> 7409
- object_events[9].script: 7029 -> 7222

## res/field/events/events_fuego_ironworks_building.json
- object_events[0].script: 7120 -> 7362
- object_events[1].script: 7122 -> 7049
- object_events[2].script: 7121 -> 7315
- object_events[3].script: 7123 -> 7082
- object_events[8].script: 7280 -> 7073
- object_events[9].script: 7281 -> 7072
- object_events[10].script: 7282 -> 7075
- object_events[11].script: 7283 -> 7074

## res/field/events/events_mt_coronet_1f_south.json
- object_events[5].script: 7047 -> 7109

## res/field/events/events_mt_coronet_2f.json
- object_events[0].script: 7170 -> 7029
- object_events[1].script: 7172 -> 7077
- object_events[2].script: 7171 -> 7407
- object_events[3].script: 7173 -> 7078

## res/field/events/events_mt_coronet_1f_north_room_1.json
- object_events[11].script: 7150 -> 7050
- object_events[12].script: 7148 -> 7396
- object_events[13].script: 7149 -> 7078
- object_events[14].script: 7174 -> 7329
- object_events[18].script: 7261 -> 7020

## res/field/events/events_solaceon_ruins_room_7.json
- object_events[0].script: 7095 -> 7307
- object_events[1].script: 7096 -> 7314
- object_events[2].script: 7097 -> 7092
- object_events[3].script: 7098 -> 7424

## res/field/events/events_victory_road_1f.json
- object_events[0].script: 7183 -> 7050
- object_events[1].script: 7182 -> 7077
- object_events[2].script: 7181 -> 7368
- object_events[3].script: 7185 -> 7326
- object_events[4].script: 7184 -> 7052

## res/field/events/events_amity_square.json
- object_events[2].script: 7051 -> 7372
- object_events[3].script: 7052 -> 7370
- object_events[4].script: 7053 -> 7310
- object_events[14].script: 7250 -> 7223

## res/field/events/events_ravaged_path.json
- object_events[27].script: 7011 -> 7366
- object_events[28].script: 7012 -> 7319
- object_events[29].script: 7013 -> 7330
- object_events[30].script: 7251 -> 7017

## res/field/events/events_floaroma_meadow.json
- object_events[4].script: 7146 -> 7239
- object_events[5].script: 7234 -> 7085
- object_events[6].script: 7284 -> 7002
- object_events[7].script: 7285 -> 7050

## res/field/events/events_oreburgh_gate_b1f.json
- object_events[11].script: 7003 -> 7328
- object_events[12].script: 7006 -> 7305
- object_events[13].script: 7004 -> 7358
- object_events[14].script: 7005 -> 7397
- object_events[16].script: 7169 -> 7089

## res/field/events/events_fullmoon_island_forest.json
- object_events[1].script: 7092 -> 7453

## res/field/events/events_ruin_maniac_cave_short.json
- object_events[0].script: 7116 -> 7355

## res/field/events/events_iron_island_b1f_right_room.json
- object_events[0].script: 7137 -> 7077
- object_events[1].script: 7136 -> 7078
- object_events[3].script: 7289 -> 7028

## res/field/events/events_iron_island_b2f_left_room.json
- object_events[0].script: 7142 -> 7002
- object_events[1].script: 7140 -> 7013
- object_events[2].script: 7141 -> 7024
- object_events[3].script: 7143 -> 7045
- object_events[15].script: 7286 -> 7072
- object_events[16].script: 7288 -> 7242

## res/field/events/events_old_chateau_dining_area.json
- object_events[1].script: 7266 -> 7050
- object_events[2].script: 7267 -> 7089

## res/field/events/events_old_chateau_side_rooms.json
- object_events[0].script: 7022 -> 7054

## res/field/events/events_old_chateau_back_middle_east_room.json
- object_events[0].script: 7248 -> 7417

## res/field/events/events_galactic_hq_1f.json
- object_events[2].script: 7165 -> 7376
- object_events[10].script: 7297 -> 7324

## res/field/events/events_galactic_hq_2f.json
- object_events[0].script: 7167 -> 7029
- object_events[5].script: 7298 -> 7075

## res/field/events/events_galactic_hq_3f.json
- object_events[1].script: 7166 -> 7348
- object_events[8].script: 7168 -> 7041
- object_events[9].script: 7295 -> 7046

## res/field/events/events_lake_verity_low_water.json
- object_events[6].script: 7239 -> 7365

## res/field/events/events_lake_verity.json
- object_events[4].script: 7239 -> 7365

## res/field/events/events_lake_valor_drained.json
- object_events[29].script: 7240 -> 7352

## res/field/events/events_lake_valor.json
- object_events[0].script: 7240 -> 7352

## res/field/events/events_lake_acuity_low_water.json
- object_events[1].script: 7241 -> 7341

## res/field/events/events_lake_acuity.json
- object_events[0].script: 7241 -> 7341

## res/field/events/events_unused_battle_park.json
- object_events[10].script: 7245 -> 7327

## res/field/events/events_valor_lakefront.json
- object_events[3].script: 7083 -> 7412
- object_events[4].script: 7084 -> 7002
- object_events[11].script: 7315 -> 7047

## res/field/events/events_acuity_lakefront.json
- object_events[0].script: 7163 -> 7002
- object_events[3].script: 7309 -> 7325

## res/field/events/events_route_203.json
- object_events[10].script: 7001 -> 7079
- object_events[11].script: 7002 -> 7004
- object_events[14].script: 7255 -> 7058

## res/field/events/events_route_204_south.json
- object_events[7].script: 7009 -> 7254
- object_events[8].script: 7010 -> 7045
- object_events[9].script: 7082 -> 7022

## res/field/events/events_route_204_north.json
- object_events[9].script: 7014 -> 7336
- object_events[11].script: 7254 -> 7021

## res/field/events/events_route_205_south.json
- object_events[10].script: 7016 -> 7014
- object_events[11].script: 7017 -> 7062
- object_events[29].script: 7253 -> 7026
- object_events[30].script: 7126 -> 7079

## res/field/events/events_route_205_north.json
- object_events[6].script: 7023 -> 7055

## res/field/events/events_route_206.json
- object_events[13].script: 7030 -> 7245
- object_events[14].script: 7031 -> 7051
- object_events[20].script: 7033 -> 7019
- object_events[21].script: 7032 -> 7076

## res/field/events/events_route_208.json
- object_events[17].script: 7050 -> 7038
- object_events[19].script: 7049 -> 7003

## res/field/events/events_route_210_north.json
- object_events[15].script: 7117 -> 7228
- object_events[16].script: 7118 -> 7317
- object_events[17].script: 7119 -> 7357
- object_events[24].script: 7279 -> 7052
- object_events[25].script: 7278 -> 7072

## res/field/events/events_route_211_west.json
- object_events[5].script: 7027 -> 7339

## res/field/events/events_route_211_east.json
- object_events[12].script: 7147 -> 7356
- object_events[21].script: 7316 -> 7048

## res/field/events/events_route_212_north.json
- object_events[12].script: 7055 -> 7318
- object_events[13].script: 7054 -> 7338
- object_events[18].script: 7056 -> 7040
- object_events[28].script: 7273 -> 7075
- object_events[29].script: 7272 -> 7047

## res/field/events/events_pokemon_mansion_maids_room.json
- object_events[0].script: 7058 -> 7011

## res/field/events/events_route_212_south.json
- object_events[20].script: 7059 -> 7027
- object_events[21].script: 7060 -> 7411
- object_events[22].script: 7061 -> 7389
- object_events[23].script: 7062 -> 7052
- object_events[24].script: 7063 -> 7025
- object_events[25].script: 7064 -> 7333
- object_events[26].script: 7065 -> 7028
- object_events[42].script: 7275 -> 7040
- object_events[43].script: 7274 -> 7073

## res/field/events/events_route_213.json
- object_events[22].script: 7076 -> 7367
- object_events[23].script: 7077 -> 7074
- object_events[24].script: 7078 -> 7029
- object_events[25].script: 7079 -> 7084
- object_events[26].script: 7075 -> 7332
- object_events[27].script: 7080 -> 7051
- object_events[28].script: 7081 -> 7046

## res/field/events/events_route_214.json
- object_events[17].script: 7115 -> 7050
- object_events[18].script: 7114 -> 7077
- object_events[19].script: 7113 -> 7072
- object_events[20].script: 7112 -> 7296
- object_events[27].script: 7317 -> 7323

## res/field/events/events_route_215.json
- object_events[19].script: 7105 -> 7025
- object_events[20].script: 7107 -> 7027
- object_events[21].script: 7106 -> 7039
- object_events[22].script: 7108 -> 7361
- object_events[24].script: 7104 -> 7303
- object_events[28].script: 7270 -> 7045

## res/field/events/events_route_216.json
- object_events[11].script: 7157 -> 7340
- object_events[12].script: 7159 -> 7027
- object_events[13].script: 7158 -> 7219
- object_events[14].script: 7246 -> 7045
- object_events[15].script: 7290 -> 7024
- object_events[16].script: 7291 -> 7028

## res/field/events/events_route_217.json
- object_events[10].script: 7161 -> 7427
- object_events[11].script: 7162 -> 7047
- object_events[12].script: 7160 -> 7334
- object_events[16].script: 7292 -> 7073
- object_events[17].script: 7293 -> 7002
- object_events[18].script: 7294 -> 7050

## res/field/events/events_route_218.json
- object_events[6].script: 7132 -> 7050
- object_events[7].script: 7133 -> 7025
- object_events[20].script: 7256 -> 7060

## res/field/events/events_route_219.json
- object_events[3].script: 7124 -> 7018

## res/field/events/events_route_222.json
- object_events[19].script: 7176 -> 7023
- object_events[20].script: 7175 -> 7048
- object_events[30].script: 7299 -> 7015
- object_events[31].script: 7300 -> 7051

## res/field/events/events_route_225.json
- object_events[2].script: 7198 -> 7327
- object_events[3].script: 7199 -> 7050
- object_events[4].script: 7200 -> 7045
- object_events[5].script: 7201 -> 7255
- object_events[6].script: 7202 -> 7324
- object_events[7].script: 7203 -> 7109
- object_events[12].script: 7204 -> 7028
- object_events[30].script: 7306 -> 7075

## res/field/events/events_route_229.json
- object_events[7].script: 7229 -> 7325
- object_events[8].script: 7231 -> 7023
- object_events[9].script: 7230 -> 7046

## res/field/events/events_route_226.json
- object_events[1].script: 7205 -> 7380
- object_events[2].script: 7207 -> 7048
- object_events[3].script: 7206 -> 7279

## res/field/events/events_route_230.json
- object_events[4].script: 7233 -> 7050
- object_events[18].script: 7308 -> 7073

## res/field/events/events_galactic_hq_laboratory.json
- object_events[2].script: 7296 -> 7023

## res/field/events/events_great_marsh_1.json
- object_events[0].script: 7066 -> 7074
- object_events[1].script: 7067 -> 7004

## res/field/events/events_great_marsh_2.json
- object_events[0].script: 7068 -> 7073

## res/field/events/events_great_marsh_3.json
- object_events[0].script: 7070 -> 7003

## res/field/events/events_great_marsh_4.json
- object_events[0].script: 7071 -> 7075
- object_events[1].script: 7069 -> 7004

## res/field/events/events_great_marsh_5.json
- object_events[0].script: 7072 -> 7003

## res/field/events/events_great_marsh_6.json
- object_events[0].script: 7073 -> 7072

## res/field/events/events_ruin_maniac_cave_long.json
- object_events[1].script: 7116 -> 7355

## res/field/events/events_maniac_tunnel.json
- object_events[1].script: 7116 -> 7355

## fielddata/eventdata/zone_event.narc (partially imported)
- 88 maps left for the per-map carry-over:
- events_jubilife_city.json: its script file changed too
- events_jubilife_city_south_house_1f.json: its script file changed too
- events_unused_jubilife_city_south_house_3f.json: its script file changed too
- events_canalave_city.json: its script file changed too
- events_canalave_city_gym.json: its script file changed too
- events_canalave_library_2f.json: its script file changed too
- events_oreburgh_city.json: its script file changed too
- events_oreburgh_city_gym.json: its script file changed too
- events_oreburgh_city_middle_house.json: its script file changed too
- events_eterna_city.json: its script file changed too
- events_eterna_city_gym.json: its script file changed too
- events_eterna_city_condominiums_1f.json: its script file changed too
- events_hearthome_city.json: its script file changed too
- events_hearthome_city_gym_leader_room.json: its script file changed too
- events_hearthome_city_pokemon_fan_club.json: its script file changed too
- events_pastoria_city.json: its script file changed too
- events_pastoria_city_gym.json: its script file changed too
- events_pastoria_city_north_house.json: its script file changed too
- events_veilstone_city.json: its script file changed too
- events_veilstone_city_gym.json: its script file changed too
- events_veilstone_city_northeast_house.json: its script file changed too
- events_sunyshore_city.json: its script file changed too
- events_sunyshore_city_gym_room_1.json: its script file changed too
- events_sunyshore_city_gym_room_3.json: its script file changed too
- events_snowpoint_city.json: its script file changed too
- events_snowpoint_city_gym.json: its script file changed too
- events_pokemon_league.json: its script file changed too
- events_fight_area.json: its script file changed too
- events_oreburgh_mine_b2f.json: gained or lost events, so new LOCALID names are needed
- events_valley_windworks_outside.json: its script file changed too
- events_eterna_forest.json: its script file changed too
- events_mt_coronet_outside_north.json: its script file changed too
- events_mt_coronet_outside_south.json: its script file changed too
- events_mt_coronet_4f_rooms_1_and_2.json: its script file changed too
- events_mt_coronet_6f.json: its script file changed too
- events_mt_coronet_b1f.json: its script file changed too
- events_victory_road_2f.json: its script file changed too
- events_victory_road_b1f.json: its script file changed too
- events_victory_road_1f_room_2.json: its script file changed too
- events_floaroma_meadow_house.json: its script file changed too
- events_stark_mountain_outside.json: its script file changed too
- events_stark_mountain_room_1.json: its script file changed too
- events_stark_mountain_room_2.json: its script file changed too
- events_turnback_cave_entrance.json: its script file changed too
- events_turnback_cave_giratina_room.json: its script file changed too
- events_snowpoint_temple_b1f.json: its script file changed too
- events_snowpoint_temple_b4f.json: its script file changed too
- events_wayward_cave_1f.json: its script file changed too
- events_wayward_cave_b1f.json: its script file changed too
- events_iron_island_b1f_left_room.json: its script file changed too
- events_iron_island_b2f_right_room.json: its script file changed too
- events_iron_island_b3f.json: its script file changed too
- events_old_chateau_back_west_room.json: its script file changed too
- events_old_chateau_back_middle_west_room.json: its script file changed too
- events_old_chateau_back_east_room.json: its script file changed too
- events_galactic_hq_b2f.json: gained or lost events, so new LOCALID names are needed
- events_route_201.json: its script file changed too
- events_route_202.json: its script file changed too
- events_route_207.json: its script file changed too
- events_route_209.json: its script file changed too
- events_route_209_lost_tower_2f.json: its script file changed too
- events_route_209_lost_tower_3f.json: its script file changed too
- events_route_209_lost_tower_4f.json: its script file changed too
- events_route_210_south.json: its script file changed too
- events_pokemon_mansion_office.json: its script file changed too
- events_route_221.json: its script file changed too
- events_route_224.json: its script file changed too
- events_route_227.json: its script file changed too
- events_route_228.json: its script file changed too
- events_twinleaf_town.json: its script file changed too
- events_sandgem_town.json: its script file changed too
- events_sandgem_town_house.json: its script file changed too
- events_floaroma_town.json: its script file changed too
- events_floaroma_town_middle_house.json: its script file changed too
- events_solaceon_town.json: its script file changed too
- events_pokemon_day_care.json: its script file changed too
- events_solaceon_town_northeast_house.json: its script file changed too
- events_solaceon_town_north_house.json: its script file changed too
- events_celestic_town.json: its script file changed too
- events_survival_area.json: its script file changed too
- events_battleground.json: its script file changed too
- events_survival_area_south_house.json: its script file changed too
- events_resort_area.json: its script file changed too
- events_route_220.json: its script file changed too
- events_route_223.json: its script file changed too
- events_iron_island_iron_ruins.json: its script file changed too
- events_mt_coronet_iceberg_ruins.json: its script file changed too
- events_route_228_rock_peak_ruins.json: its script file changed too

## height.narc (not imported)
- 298 of 1976 members differ
- 164 of them write a byte where vanilla has an empty member (a gender the species does not have; the decomp derives this from the gender ratio and cannot express it as an edit)
- 116 species had male == female in vanilla and have only the male offset changed in the base ROM, which a hand edit would not do
- reading this as a DSPRE re-save, not an edit; skipped pending Ian

## pl_item_data.narc (not imported)
- 6 of 446 records differ: ITEM_HP_UP, ITEM_PROTEIN, ITEM_IRON, ITEM_CARBOS, ITEM_CALCIUM, ITEM_ZINC
- ITEM_HP_UP: 34 bytes -> 36 bytes
- ITEM_PROTEIN: 34 bytes -> 36 bytes
- ITEM_IRON: 34 bytes -> 36 bytes
- ITEM_CARBOS: 34 bytes -> 36 bytes
- ITEM_CALCIUM: 34 bytes -> 36 bytes
- ITEM_ZINC: 34 bytes -> 36 bytes
- every differing record grew from ItemData's 34 bytes to 36, with the vitamin's EV amount zeroed and everything after it shifted one byte right, so the friendship values no longer line up with the struct
- reading this as DSPRE writing a malformed record, not an edit; skipped pending Ian. The vitamin change he described is the EV cap (100 -> 252), which is a code edit and is already its own tracker item

