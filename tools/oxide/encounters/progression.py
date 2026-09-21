"""The progression order: every encounter area in the order a player meets
it. Authoring plan decision 6.

This is the agent's default, from Sinnoh's actual route sequence as the plan
outlines it, written into the sidecar once by `cli order-init`. After that
the sidecar is the source and Ian corrects it there; this list is only what
the sidecar started from and is not consulted again.

Areas with several files (Mt Coronet, Victory Road, Turnback Cave) take
consecutive integers in floor order. Places the outline names that have no
encounter file (Sandgem, Jubilife, Oreburgh, Floaroma, Hearthome, Solaceon,
Veilstone, Snowpoint, Spear Pillar, Survival Area) are simply absent. Three
groups the outline does not name are placed by their levels and access: the
Old Chateau after Eterna Forest, Snowpoint Temple after the League, and the
twenty-five `unknown_533` to `unknown_557` files (level 45-48, five species
each, following Turnback Cave in the NARC) last, as the plan's "post-game
lake rooms". Route 207 has one file and sits at its first mention, Route 224
after Victory Road's post-game rooms, and the Ruin Maniac's cave with Maniac
Tunnel.
"""

DEFAULT_ORDER = [
    # Twinleaf to Oreburgh
    "twinleaf_town",
    "route_201",
    "lake_verity",
    "lake_verity_low_water",
    "route_202",
    "route_203",
    "oreburgh_gate_1f",
    "oreburgh_gate_b1f",
    "route_207",
    "oreburgh_mine_b1f",
    "oreburgh_mine_b2f",
    # to Floaroma and Eterna
    "route_204_south",
    "ravaged_path",
    "route_204_north",
    "route_205_south",
    "valley_windworks_outside",
    "route_205_north",
    "eterna_forest",
    "old_chateau",
    "old_chateau_dining_area",
    "old_chateau_side_rooms",
    "old_chateau_corridor",
    "old_chateau_back_west_room",
    "old_chateau_back_middle_west_room",
    "old_chateau_back_middle_room",
    "old_chateau_back_middle_east_room",
    "old_chateau_back_east_room",
    "eterna_city",
    "route_211_west",
    "mt_coronet_1f_north_room_1",
    # the bike road to Hearthome
    "route_206",
    "wayward_cave_1f",
    "wayward_cave_b1f",
    "route_208",
    "mt_coronet_1f_south",
    "route_209",
    "route_209_lost_tower_1f",
    "route_209_lost_tower_2f",
    "route_209_lost_tower_3f",
    "route_209_lost_tower_4f",
    "route_209_lost_tower_5f",
    # Solaceon and the ruins
    "solaceon_ruins_room_1_northwest_dead_end",
    "solaceon_ruins_room_1_southeast_dead_end",
    "solaceon_ruins_room_2",
    "solaceon_ruins_room_2_northeast_dead_end",
    "solaceon_ruins_room_2_southeast_dead_end",
    "solaceon_ruins_room_3",
    "solaceon_ruins_room_3_northwest_dead_end",
    "solaceon_ruins_room_3_southwest_dead_end",
    "solaceon_ruins_room_4",
    "solaceon_ruins_room_4_southeast_dead_end",
    "solaceon_ruins_room_5",
    "solaceon_ruins_room_5_southeast_deadend",
    "solaceon_ruins_room_5_southwest_dead_end",
    "solaceon_ruins_room_6",
    "solaceon_ruins_room_6_northwest_dead_end",
    "solaceon_ruins_room_6_southeast_dead_end",
    "solaceon_ruins_room_7",
    "solaceon_ruins_maniac_tunnel_room",
    # Veilstone and the south-east
    "route_210_south",
    "route_215",
    "route_214",
    "maniac_tunnel",
    "ruin_maniac_cave_short",
    "ruin_maniac_cave_long",
    "valor_lakefront",
    "route_213",
    "pastoria_city",
    "great_marsh_1",
    "great_marsh_2",
    "great_marsh_3",
    "great_marsh_4",
    "great_marsh_5",
    "great_marsh_6",
    "route_212_north",
    "route_212_south",
    "trophy_garden",
    # Celestic and the west
    "route_210_north",
    "route_211_east",
    "celestic_town",
    "fuego_ironworks_outside",
    "route_218",
    "canalave_city",
    "iron_island",
    "iron_island_1f",
    "iron_island_b1f_left_room",
    "iron_island_b1f_right_room",
    "iron_island_b2f_right_room",
    "iron_island_b2f_left_room",
    "iron_island_b3f",
    "route_219",
    "route_220",
    "route_221",
    "lake_valor",
    # the north
    "route_216",
    "route_217",
    "acuity_lakefront",
    "lake_acuity",
    # Mt Coronet, the climb
    "mt_coronet_1f_tunnel_room",
    "mt_coronet_1f_north_room_2",
    "mt_coronet_b1f",
    "mt_coronet_2f",
    "mt_coronet_3f",
    "mt_coronet_outside_south",
    "mt_coronet_4f_rooms_1_and_2",
    "mt_coronet_4f_room_3",
    "mt_coronet_outside_north",
    "mt_coronet_5f",
    "mt_coronet_6f",
    # Sendoff Spring and Turnback Cave
    "sendoff_spring",
    "turnback_cave_entrance",
    "turnback_cave_pillar_1_room_1",
    "turnback_cave_pillar_1_room_2",
    "turnback_cave_pillar_1_room_3",
    "turnback_cave_pillar_1_room_4",
    "turnback_cave_pillar_1_room_5",
    "turnback_cave_pillar_1_room_6",
    "turnback_cave_pillar_2_room_1",
    "turnback_cave_pillar_2_room_2",
    "turnback_cave_pillar_2_room_3",
    "turnback_cave_pillar_2_room_4",
    "turnback_cave_pillar_2_room_5",
    "turnback_cave_pillar_2_room_6",
    "turnback_cave_pillar_3_room_1",
    "turnback_cave_pillar_3_room_2",
    "turnback_cave_pillar_3_room_3",
    "turnback_cave_pillar_3_room_4",
    "turnback_cave_pillar_3_room_5",
    "turnback_cave_pillar_3_room_6",
    "turnback_cave_pillar_room",
    "turnback_cave_giratina_room",
    # Sunyshore and the League
    "route_222",
    "sunyshore_city",
    "route_223",
    "victory_road_1f",
    "victory_road_2f",
    "victory_road_b1f",
    "victory_road_1f_room_1",
    "victory_road_1f_room_2",
    "victory_road_1f_room_3",
    "route_224",
    "pokemon_league",
    # post-game
    "snowpoint_temple_1f",
    "snowpoint_temple_b1f",
    "snowpoint_temple_b2f",
    "snowpoint_temple_b3f",
    "snowpoint_temple_b4f",
    "snowpoint_temple_b5f",
    "route_225",
    "route_226",
    "route_227",
    "stark_mountain_outside",
    "stark_mountain_room_1",
    "stark_mountain_room_2",
    "route_228",
    "route_229",
    "resort_area",
    "route_230",
    # the two species-only sources, kept in the same sequence
    "honey_tree",
    "great_marsh_lookout",
] + [f"unknown_{n}" for n in range(533, 558)]


def default_order():
    """{area file name: 1-based position}."""
    return {f"encounters_{stem}": i + 1 for i, stem in enumerate(DEFAULT_ORDER)}


def write_order(sidecar, names, order=None):
    """Put `order` on every area entry, adding minimal entries for areas the
    sidecar has none for (the twelve land_rate 0 files and the two species-
    only files), so that every one of the 185 carries a position. Returns
    the names in `names` that the order does not cover."""
    order = order or default_order()
    areas = sidecar.setdefault("areas", {})
    missing = []
    for name in names:
        if name not in order:
            missing.append(name)
            continue
        entry = areas.setdefault(name, {
            "archetype": None, "band": None, "intent": "", "locked": [],
            "base_level": None})
        entry["order"] = order[name]
    return missing


def sorted_by_order(sidecar, names):
    """`names` in sidecar order, with any area lacking one at the end."""
    areas = (sidecar or {}).get("areas") or {}
    return sorted(names, key=lambda n: (areas.get(n, {}).get("order") is None,
                                        areas.get(n, {}).get("order") or 0, n))
