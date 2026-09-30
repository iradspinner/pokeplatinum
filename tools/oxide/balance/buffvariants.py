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


def _load(folder, name):
    path = os.path.join(folder, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)["fights"]


def _share(fights, constant):
    """(boss Pokemon faced, surely answered, alone answered, fights met) for
    one species over the story fights."""
    faced = answered = alone = met = 0
    for r in fights.values():
        row = r["species"].get(constant)
        if row and row["faced"]:
            faced += row["faced"]
            answered += row["answered"]
            alone += row["alone"]
            met += 1
    return faced, answered, alone, met


def report(folder, out=sys.stdout):
    """The doc: for each variant, the story fights it moves on Ian's scale
    and each changed species' own share of the boss Pokemon it surely
    answers, against B6's line for a species that carries the game."""
    say = lambda *a: print(*a, file=out)
    base = _load(folder, "base")
    line = b6.scale_line()
    scale = lambda safe: b6.on_scale(safe, line)
    say("# Buff review: the changes Ian decides from the scores\n")
    say("Written by `tools/oxide/balance/buffvariants.py` for the buff review's sections C and D "
        "and the variants Ian asked for (2026-09-29). Each variant is scored on the 33 story fights "
        "and Hesperid's two, as B6's levers score them, against the tree with his approved changes "
        "(the sheet's slips, section A's five lines and section B). A negative change on his scale "
        "is an easier fight. A species' share is the boss Pokemon it surely answers out of those it "
        f"faces, over the story fights it is on the player's side for; B6 flags a species that "
        f"carries the game at {b6.CARRIES} or more over {b6.MIN_FIGHTS} or more fights.\n")
    say("Gale Wings is read at its best case: the Flying moves of a Gale Wings Pokemon go first in "
        "every matchup, since the scorer cannot follow its full-HP condition turn by turn. A "
        "variant that adds an ability puts it in the first slot, which the player's side reads.\n")
    say("| Variant | Fights moved 0.1 or more on Ian's scale | Mean change | Species' share, now to "
        "variant (fights) |")
    say("|---|---|---|---|")
    for name, (label, changes) in VARIANTS.items():
        var = _load(folder, name)
        if var is None:
            say(f"| {label} | not run | | |")
            continue
        moved = []
        deltas = []
        for key, r in var.items():
            d = scale(r["safe"]) - scale(base[key]["safe"])
            deltas.append(d)
            if abs(d) >= 0.1:
                moved.append((d, r["label"]))
        moved.sort()
        cells = ", ".join(f"{lab} {d:+.1f}" for d, lab in moved) or "none"
        shares = []
        for sp in changes:
            c = "SPECIES_" + sp.upper()
            f0, a0, _l0, m0 = _share(base, c)
            f1, a1, _l1, m1 = _share(var, c)
            if f0 or f1:
                flag = " (carries)" if f1 and a1 / f1 >= b6.CARRIES and m1 >= b6.MIN_FIGHTS else ""
                shares.append(f"{sp.title()} {a0 / f0 if f0 else 0:.2f} to {a1 / f1 if f1 else 0:.2f} "
                              f"({m1}){flag}")
        say(f"| {label} | {cells} | {sum(deltas) / len(deltas):+.2f} | "
            f"{'; '.join(shares) or 'not on the side in a story fight'} |")
    say("\nNot scored, since the scorer cannot read them:\n")
    for what, why in UNSCORED.items():
        say(f"- {what}: {why}.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) == 3 and argv[0] == "run" and (argv[1] == "base" or argv[1] in VARIANTS):
        run(argv[1], argv[2])
        return 0
    if len(argv) >= 2 and argv[0] == "report":
        if len(argv) == 3:
            with open(argv[2], "w", encoding="utf-8") as f:
                report(argv[1], f)
        else:
            report(argv[1])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
