"""The buff review's changes to test, each scored on the story fights before
Ian decides (2026-09-29; ~/oxide-trials/buff-review/out/suggestions.md,
sections C and D, with Glaceon's Ice Scales, Gale Wings on Talonflame at its
own level and after Maylene's split, and Houndoom's sheet line with
Houndour's evolution after Gardenia's split).

    PYTHONPATH=. python3 -m tools.oxide.balance.buffvariants run NAME OUT.json   # one variant

`run` changes the named species' records in the working tree, scores the 33
story fights and Hesperid's two as B6's levers do (every matchup, the
player's side at the split's cap, no fingerprints and nothing stored), puts
the records back, and writes the fight readings and each changed species'
own row (the boss Pokemon it faces, surely answers, and alone answers). Run
it in a scratch worktree, one variant a process, so every cache starts from
the changed data. `base` is the tree as it stands.

What the scorer can read: stats, types, and the abilities the damage engine
models (Pixilate, Ice Scales, Sheer Force, Technician, Adaptability). The
player's side takes each species' first ability, so a variant that adds an
ability puts it first. Gale Wings' priority is not in the Generation 4
engine; a Gale Wings variant gives its Pokemon's Flying moves priority in
every matchup, the best case, since the full-HP condition cannot be followed
turn by turn. Magic Guard, Magic Bounce, Contrary and Regenerator are
outside the scorer, so those suggestions are named, not scored (UNSCORED).
"""
import concurrent.futures
import json
import os
import sys
import tempfile

from ..encounters import calc_export
from .. import jsonstyle
from . import b6, data, pool, pressure

# (HP, Atk, Def, SpA, SpD, Spe), as the review writes them.
_ORDER = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")


def _stats(*values):
    return {"base_stats": dict(zip(_ORDER, values))}


def _set(**kw):
    return {"base_stats": kw}


def _first(*abilities):
    return {"abilities": ["ABILITY_" + a for a in abilities]}


# name: (what it is, {species dir: changes})
VARIANTS = {
    "haunter": ("Haunter, Kaizo's 60/50/60/115/75/110", {"haunter": _stats(60, 50, 60, 115, 75, 110)}),
    "machoke": ("Machoke 90/100/80/50/70/45", {"machoke": _stats(90, 100, 80, 50, 70, 45)}),
    "gabite": ("Gabite 68/90/75/50/65/82", {"gabite": _stats(68, 90, 75, 50, 65, 82)}),
    "rhyhorn": ("Rhyhorn 90/95/95/30/30/25", {"rhyhorn": _stats(90, 95, 95, 30, 30, 25)}),
    "litwick": ("Litwick 60/30/65/75/65/20", {"litwick": _stats(60, 30, 65, 75, 65, 20)}),
    "sandygast": ("Sandygast 65/55/90/80/55/15", {"sandygast": _stats(65, 55, 90, 80, 55, 15)}),
    "lunatone": ("Lunatone SpA 110, SpD 95", {"lunatone": _set(special_attack=110, special_defense=95)}),
    "solrock": ("Solrock Atk 110, Def 95", {"solrock": _set(attack=110, defense=95)}),
    "seaking": ("Seaking, Odyssey's 85/105/70/65/80/70", {"seaking": _stats(85, 105, 70, 65, 80, 70)}),
    "lanturn": ("Lanturn Def 68, SpA 86, SpD 86",
                {"lanturn": _set(defense=68, special_attack=86, special_defense=86)}),
    "kingler": ("Kingler HP 65, SpD 65", {"kingler": _set(hp=65, special_defense=65)}),
    "kingler_sheer": ("Kingler HP 65, SpD 65, with Sheer Force",
                      {"kingler": dict(_set(hp=65, special_defense=65),
                                       **_first("SHEER_FORCE", "HYPER_CUTTER", "SHEER_FORCE"))}),
    "sudowoodo": ("Sudowoodo 85/110/115/30/80/30", {"sudowoodo": _stats(85, 110, 115, 30, 80, 30)}),
    "bibarel": ("Bibarel Def 70, SpD 70", {"bibarel": _set(defense=70, special_defense=70)}),
    "emolga": ("Emolga 70/75/70/95/60/103", {"emolga": _stats(70, 75, 70, 95, 60, 103)}),
    "mothim": ("Mothim 80/94/60/94/60/76", {"mothim": _stats(80, 94, 60, 94, 60, 76)}),
    "togedemaru": ("Togedemaru 75/108/73/40/73/96", {"togedemaru": _stats(75, 108, 73, 40, 73, 96)}),
    "dewgong": ("Dewgong, Odyssey's 100/70/90/70/100/70", {"dewgong": _stats(100, 70, 90, 70, 100, 70)}),
    "ludicolo": ("Ludicolo SpA 100, Def 80", {"ludicolo": _set(special_attack=100, defense=80)}),
    "toucannon": ("Toucannon with Sheer Force (Sheer Force | Skill Link)",
                  {"toucannon": _first("SHEER_FORCE", "SKILL_LINK", "SHEER_FORCE")}),
    "talonflame": ("Talonflame with Gale Wings",
                   {"talonflame": _first("GALE_WINGS", "FLAME_BODY", "GALE_WINGS")}),
    "talonflame_late": ("Talonflame with Gale Wings, evolving at 40, after Maylene's split",
                        {"talonflame": _first("GALE_WINGS", "FLAME_BODY", "GALE_WINGS"),
                         "fletchinder": {"evolution_level": 40}}),
    "frosmoth": ("Frosmoth with Ice Scales", {"frosmoth": _first("ICE_SCALES", "SHIELD_DUST", "ICE_SCALES")}),
    "glaceon": ("Glaceon with Ice Scales", {"glaceon": _first("ICE_SCALES", "SNOW_CLOAK", "ICE_BODY")}),
    "sylveon": ("Sylveon with Pixilate", {"sylveon": _first("PIXILATE", "CUTE_CHARM", "PIXILATE")}),
    "pupitar": ("Pupitar +10 HP and +10 Atk (80/94/70/65/70/51)", {"pupitar": _set(hp=80, attack=94)}),
    "ampharos": ("Ampharos Electric/Dragon", {"ampharos": {"types": ["TYPE_ELECTRIC", "TYPE_DRAGON"]}}),
    "houndoom": ("Houndoom SpA 120 and Spe 105, Houndour evolving at 27, after Gardenia's split",
                 {"houndoom": _set(special_attack=120, speed=105), "houndour": {"evolution_level": 27}}),
}
# Suggestions whose effect the scorer cannot read.
UNSCORED = {
    "Florges: Flower Veil to Magic Guard": "Magic Guard stops passive damage, which the scorer does not model",
    "Espeon: Synchronize to Magic Bounce": "Magic Bounce reflects status moves, which the scorer does not model",
    "Lurantis: Leaf Guard to Contrary": "Contrary turns Leaf Storm's drop into a boost, and the scorer "
                                        "plays no stat stages",
    "Volbeat and Illumise": "not obtainable, so trainer palette only; no story fight fields them",
    "Sturdy restored": "Ian ruled that Sturdy stays as it is",
}


def _apply(changes):
    """Writes the changes into the species records; returns the original
    texts to put back."""
    saved = {}
    for sp, ch in changes.items():
        path = os.path.join(data.ROOT, "res", "pokemon", sp, "data.json")
        text = open(path, encoding="utf-8").read()
        saved[path] = text
        for stat, v in (ch.get("base_stats") or {}).items():
            text = jsonstyle.replace_value(text, ["base_stats", stat], v)
        if "types" in ch:
            text = jsonstyle.replace_value(text, ["types"], ch["types"])
        if "abilities" in ch:
            text = jsonstyle.replace_value(text, ["abilities"], ch["abilities"])
        if "evolution_level" in ch:
            text = jsonstyle.replace_value(text, ["evolutions", 0, 1], ch["evolution_level"])
        open(path, "w", encoding="utf-8").write(text)
    return saved


def _gale_wings(st, blob):
    """Flying moves of a Gale Wings Pokemon go first, the best case."""
    for (a, _d), row in st["rows"].items():
        if (st["pokemon"].get(a) or {}).get("ability") != "Gale Wings":
            continue
        for name, mv in row["moves"].items():
            if "rolls" in mv and (blob["moves"].get(name) or {}).get("type") == "Flying":
                mv["priority"] = max(mv.get("priority", 0), 1)


def score(watch, workers=16):
    """{fight key: readings and each watched species' row} for the story
    fights and Hesperid's two, on the tree as it stands."""
    blob = calc_export.build()
    fights = b6.boss_fights()
    sides = {}
    for fight, _parties in fights:
        if fight["split"] not in sides:
            sides[fight["split"]] = pool.pool(fight["split"], blob)
    with tempfile.TemporaryDirectory(prefix="oxide-buffs-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)

        def one(item):
            fight, parties = item
            side = sides[fight["split"]]
            jobs, ctx = pressure.fight_jobs(fight, blob, side=side, parties=parties)
            st = b6.run_state(jobs, ctx, side, blob_path)
            _gale_wings(st, blob)
            per_mon = b6.score_all(st)
            r = b6.roll(per_mon)
            rows = {c: v for c, v in b6.species_rows(st, per_mon).items() if c in watch}
            return fight["key"], {**{k: r[k] for k in ("safe", "threat_chance", "answers_bait", "cover")},
                                  "split": fight["split"], "label": fight["label"], "species": rows}
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            return dict(ex.map(one, fights))


def _watch():
    return {"SPECIES_" + sp.upper() for _l, ch in VARIANTS.values() for sp in ch}


def run(name, out):
    saved = _apply(VARIANTS[name][1] if name != "base" else {})
    try:
        res = score(_watch())
    finally:
        for path, text in saved.items():
            open(path, "w", encoding="utf-8").write(text)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"variant": name, "fights": res}, f, indent=1, sort_keys=True)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) == 3 and argv[0] == "run" and (argv[1] == "base" or argv[1] in VARIANTS):
        run(argv[1], argv[2])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
