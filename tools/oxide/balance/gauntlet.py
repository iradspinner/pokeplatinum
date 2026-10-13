"""Gauntlets: trainers fought in a row with no healing between them (Ian,
2026-09-27; balance plan, "Attrition lives in gauntlets").

A gauntlet is 2 to 5 mandatory trainers on the easier side of average,
bosses outside it, and the bag may heal between its fights: the danger is
deaths snowballing. This module holds the built sections and the trainers
each holds in walking order, which the reward table (rewards.py) and
docs/oxide/trainer-roles.tsv rest on. A section's split is its first
trainer's placement (required.placements).

Its two readings of a section ran on the first scoring system and were
retired with it on 2026-10-13; Ian decided the same day that the
perfect-line scorer will read a section, one team through its fights in
order (plstudy.section is a start).
"""
import json
import os

from . import data, required, splits

# Each section: its label, its maps in walking order, which part of a map
# (None for all of it, or the trainer constants a half holds), and the
# trainers left out of it. Mt. Coronet's officers are left out: Hesperid is
# a fight Ian rated as a boss, and Moira and Argo read well above the
# split's average; Somnu, at it, joins the floors below. The ten sections
# are the built ones (src/gauntlet.c, main-gauntlets): Victory Road's 2F and
# B1F are detours inside 1F's locks, not sections, so their eight trainers
# are optional (Ian, 2026-09-29, restated 2026-10-07), and 1F's halves hold
# the trainers the code lists.
SECTIONS = {
    "galactic_eterna": [
        ("1F and 2F", ["TEAM_GALACTIC_ETERNA_BUILDING_1F", "TEAM_GALACTIC_ETERNA_BUILDING_2F"],
         None, ()),
        ("3F", ["TEAM_GALACTIC_ETERNA_BUILDING_3F"], None, ())],
    "galactic_hq": [
        ("1F", ["GALACTIC_HQ_1F"], None, ()), ("2F", ["GALACTIC_HQ_2F"], None, ()),
        ("3F", ["GALACTIC_HQ_3F"], None, ()), ("B2F", ["GALACTIC_HQ_B2F"], None, ())],
    "mt_coronet": [
        ("1F's tunnel", ["MT_CORONET_1F_TUNNEL_ROOM"], None, ()),
        ("3F, 4F and Somnu on 5F", ["MT_CORONET_3F", "MT_CORONET_4F_ROOMS_1_AND_2",
                                     "MT_CORONET_5F"], None, (520, 526, 834))],
    "victory_road": [
        ("1F, the half nearer the entrance", ["VICTORY_ROAD_1F"],
         ("TRAINER_PSYCHIC_BRYCE", "TRAINER_BIRD_KEEPER_HANA", "TRAINER_ACE_TRAINER_MARIAH"), ()),
        ("1F, the far half", ["VICTORY_ROAD_1F"],
         ("TRAINER_BLACK_BELT_MILES", "TRAINER_DRAGON_TAMER_CLINTON", "TRAINER_VETERAN_EDGAR"), ())],
}


def _positions(header):
    """{trainer id: its z on the map}, from the map's events."""
    events = splits.headers()[header].get("eventsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json")
    ids = {t["constant"]: tr for tr, t in data.oxide_trainers().items()}
    out = {}
    if events and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for o in json.load(f).get("object_events", []):
                tr = ids.get(str(o.get("script", "")))
                if tr is not None:
                    out[tr] = o.get("z", 0)
    return out


def section_trainers(area, section):
    """A section's trainers in walking order, from the map's entrance, taken
    as the larger z. A half of a map holds the trainers it names."""
    _label, maps, half, leave_out = section
    placed = required.placements()
    ox = data.oxide_trainers()
    out = []
    for h in maps:
        on_map = [tr for tr, ms in splits.trainer_maps().items()
                  if h in ms and tr in placed and tr not in leave_out]
        pos = _positions(h)
        on_map.sort(key=lambda tr: (-pos.get(tr, 0), tr))
        if half is not None:
            on_map = [tr for tr in on_map if ox[tr]["constant"] in half]
        out += on_map
    return out
