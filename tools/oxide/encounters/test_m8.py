"""M8 D1 to D5: the dex data layer reads species, moves, sprites and the type
chart out of res/, says what changed from vanilla, indexes who learns what, and
feeds the vendored damage calculator Oxide's own numbers.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m8

Read-only. The point of the milestone is that the dex cannot drift from the
game, so these checks pin real values out of the tree rather than fixtures.
"""
import os
import re
import sys

from . import model
from . import pokedex
from . import server


def check_species(results):
    root = model.repo_root()
    names = pokedex.species_list(root)
    # 493 natives plus the 159 Phase 4 added; SPECIES_NONE, EGG and BAD_EGG are
    # not species and are left out.
    results.append(("every species in the tree has a folder and a record",
                    len(names) == 652 and "SPECIES_NONE" not in names
                    and all(pokedex.load(root, n) for n in names[:40]),
                    f"{len(names)} species"))

    clefairy = pokedex.load(root, "SPECIES_CLEFAIRY")
    results.append(("a species reads its stats, its total and its name",
                    clefairy["bst"] == 323 and clefairy["stats"]["hp"] == 70
                    and clefairy["name"] == "Clefairy", f"bst {clefairy['bst']}"))

    gyarados = pokedex.load(root, "SPECIES_GYARADOS")
    results.append(("a dual type keeps its order, a single type is one type",
                    gyarados["types"] == ["WATER", "FLYING"]
                    and clefairy["types"] == ["FAIRY"],
                    f"{gyarados['types']}, {clefairy['types']}"))

    floette = pokedex.load(root, "SPECIES_FLOETTE")
    results.append(("the third ability slot is the hidden one, and NONE is not "
                    "an ability",
                    floette["hidden_ability"] == "SYMBIOSIS"
                    and floette["abilities"] == ["FLOWER_VEIL"]
                    and gyarados["abilities"] == ["INTIMIDATE"], ""))

    results.append(("evolutions carry their method and level",
                    pokedex.load(root, "SPECIES_LITTEN")["evolutions"]
                    == [{"method": "LEVEL", "level": 16, "item": None,
                         "into": "SPECIES_TORRACAT", "form": False}], ""))
    results.append(("the level-up learnset comes through",
                    pokedex.load(root, "SPECIES_LITTEN")["learnset"][0]
                    == [1, "MOVE_SCRATCH"], ""))


def check_delta(results):
    root = model.repo_root()
    # Clefairy is one of the twenty species Phase 4 element 1 retyped to Fairy,
    # and it lost Cute Charm in the same pass.
    d = pokedex.delta(root, "SPECIES_CLEFAIRY")
    results.append(("a retyped species reports the type it was and the type it is",
                    d and d["types"] == {"was": ["NORMAL"], "now": ["FAIRY"]},
                    str(d and d.get("types"))))
    results.append(("a species this project added reads as new, not as changed",
                    pokedex.delta(root, "SPECIES_SCORBUNNY") == {"new": True}, ""))
    # One of the seven natives that gained an evolution into a new species.
    d = pokedex.delta(root, "SPECIES_PRIMEAPE")
    results.append(("a native that gained an evolution reports it",
                    bool(d and d.get("evolutions")),
                    str((d or {}).get("evolutions"))))
    unchanged = pokedex.delta(root, "SPECIES_BULBASAUR")
    results.append(("a species vanilla still agrees with reports nothing",
                    unchanged is None, str(unchanged)))


def check_chart(results):
    root = model.repo_root()
    chart = pokedex.type_chart(root)
    types = {a for a, _ in chart} | {d for _, d in chart}
    results.append(("the chart is read out of the battle code, all eighteen types",
                    len(types) == 18 and "FAIRY" in types, f"{len(types)} types"))
    # This fork's chart is neither generation's, which is why the calculator
    # cannot use a stock setting: Fairy is in, and Steel still resists Dark and
    # Ghost the way it did before Generation 6 took that away. Ian ruled to
    # keep it that way (2026-09-22), so this guards a decision.
    results.append(("Steel still resists Dark and Ghost, as Generation 4 had it",
                    chart.get(("DARK", "STEEL")) == 0.5
                    and chart.get(("GHOST", "STEEL")) == 0.5,
                    f"dark {chart.get(('DARK', 'STEEL'))}, "
                    f"ghost {chart.get(('GHOST', 'STEEL'))}"))
    results.append(("Fairy is complete: strong on three, weak to two, immune to "
                    "Dragon",
                    chart.get(("FAIRY", "DRAGON")) == 2.0
                    and chart.get(("FAIRY", "DARK")) == 2.0
                    and chart.get(("FAIRY", "FIGHTING")) == 2.0
                    and chart.get(("POISON", "FAIRY")) == 2.0
                    and chart.get(("STEEL", "FAIRY")) == 2.0
                    and chart.get(("DRAGON", "FAIRY")) == 0.0, ""))
    results.append(("effectiveness multiplies across both of a species' types",
                    pokedex.effectiveness(chart, "FIGHTING", ["STEEL", "FAIRY"]) == 1.0
                    and pokedex.effectiveness(chart, "GROUND", ["FIRE"]) == 2.0
                    and pokedex.effectiveness(chart, "ELECTRIC", ["GROUND"]) == 0.0,
                    ""))


def check_moves_and_sprites(results):
    root = model.repo_root()
    moves = pokedex.moves(root)
    # Counted from the tree rather than written down: the branch that wrote
    # this check predates element 4's move import, which took 468 to 923.
    # A move is a folder with a data.json; `.shared` holds scripts, not a move.
    folders = [f for f in os.listdir(os.path.join(root, "res", "moves"))
               if os.path.isfile(os.path.join(root, "res", "moves", f, "data.json"))]
    results.append(("every move folder reads, and meson.build is not a move",
                    len(moves) == len(folders) and "MOVE_MESON.BUILD" not in moves,
                    f"{len(moves)} moves of {len(folders)} folders"))
    flamethrower = moves["MOVE_FLAMETHROWER"]
    results.append(("a move carries what a damage formula needs",
                    flamethrower["type"] == "FIRE" and flamethrower["power"] == 90
                    and flamethrower["class"] == "SPECIAL"
                    and flamethrower["accuracy"] == 100
                    and flamethrower["priority"] == 0, ""))
    sprites = pokedex.sprites(root, "SPECIES_CLEFAIRY")
    results.append(("a species finds its sprites and its icon",
                    "icon" in sprites and "male_front" in sprites
                    and sprites["icon"].startswith("res/pokemon/clefairy/"), ""))


def check_captures(results):
    caught = pokedex.captures()
    results.append(("the cross-link finds every species the tables actually hold",
                    len(caught) > 200 and "SPECIES_LITTEN" in caught,
                    f"{len(caught)} species"))
    litten = caught["SPECIES_LITTEN"][0]
    results.append(("an appearance names the area, its location, its split, its "
                    "share and its levels",
                    litten["area"] == "encounters_route_204_north"
                    and litten["location"] == "Route 204"
                    and litten["split"] == "Gardenia"
                    and abs(litten["share"] - 0.20) < 1e-9
                    and litten["level_min"] == 9, str(litten)))
    rods = [r for rows in caught.values() for r in rows if r["kind"] != "land"]
    results.append(("water tables are cross-linked too, with their level ranges",
                    rods and all(r["level_min"] is not None for r in rods),
                    f"{len(rods)} water appearances"))

    # D3 draws a party icon beside every slot, and the page finds it by
    # lowercasing the species constant rather than asking. That holds for all
    # 652 species today; this is what notices if a table ever names one it does
    # not hold for, which would be a broken image in the middle of a table.
    root = model.repo_root()
    iconless = [s for s in caught
                if "icon" not in pokedex.sprites(root, s)]
    results.append(("every species a table holds has an icon to draw beside it",
                    not iconless, f"no icon: {iconless[:4]}"))


def check_endpoints(results):
    out = server.dex_list()
    results.append(("the list endpoint returns one row per species, with the "
                    "vanilla comparison folded in",
                    out["count"] == 652
                    and any(r["new"] for r in out["rows"])
                    and any(r["changed"] for r in out["rows"]), f"{out['count']} rows"))
    detail = server.dex_detail("SPECIES_LITTEN")
    results.append(("the detail endpoint carries the record, the delta, the "
                    "sprites, the captures and the matchups",
                    detail["name"] == "Litten" and detail["delta"] == {"new": True}
                    and detail["sprites"] and detail["captures"]
                    and detail["matchups"]["WATER"] == 2.0, ""))
    results.append(("an unknown species is an error rather than a crash",
                    "error" in server.dex_detail("SPECIES_NOT_A_POKEMON"), ""))


def check_canon(results):
    """The second baseline: what a species really is, in its own generation.

    `main` answers that for the 493 natives and nothing for the 159 ported
    ones, which is why the dex read "new" and stopped. The canonical table
    covers all of them, and it has to be the upstream one: the vendored
    calculator ships whatever data it was last built with, which is a romhack's.
    """
    from . import canon
    root = model.repo_root()
    names = pokedex.species_list(root)
    results.append(("every species in the tree lands on a canonical name, which "
                    "is also the map the calculator will need",
                    not canon.unmatched(names),
                    f"unmatched {canon.unmatched(names)[:4]}"))
    results.append(("the awkward spellings are the ones the calculator uses",
                    canon.showdown_name("SPECIES_ALOLAN_NINETALES") == "Ninetales-Alola"
                    and canon.showdown_name("SPECIES_GYARADOS_M") == "Gyarados-Mega"
                    and canon.showdown_name("SPECIES_FARFETCHD") == "Farfetch’d"
                    and canon.showdown_name("SPECIES_JANGMO_O") == "Jangmo-o"
                    and canon.showdown_name("SPECIES_MR_MIME") == "Mr. Mime"
                    and canon.showdown_name("SPECIES_PORYGON_Z") == "Porygon-Z", ""))

    # The table that proved untrustworthy had Lopunny as Normal/Fighting, Arbok
    # as Dark/Poison and Lapras as Dragon/Water. If canon.json is ever
    # regenerated from the wrong species.js, this is what says so.
    table = canon.table()
    results.append(("the canonical table is canonical, not some romhack's",
                    table["Lopunny"]["types"] == ["Normal"]
                    and table["Arbok"]["types"] == ["Poison"]
                    and table["Lapras"]["types"] == ["Water", "Ice"]
                    and sum(table["Annihilape"]["stats"].values()) == 535,
                    f"lopunny {table['Lopunny']['types']}"))

    scorbunny = pokedex.load(root, "SPECIES_SCORBUNNY")
    results.append(("a ported species compares against its real self rather "
                    "than reading as new and stopping",
                    pokedex.delta(root, "SPECIES_SCORBUNNY") == {"new": True}
                    and canon.delta("SPECIES_SCORBUNNY", scorbunny) is not None
                    and not canon.delta("SPECIES_SCORBUNNY", scorbunny).get("stats"),
                    ""))
    # Ian's own buffs should read as buffs: the base ROM lifts a lot of weak
    # natives, and Alolan Ninetales came in 50 points above the real one.
    ninetales = pokedex.load(root, "SPECIES_ALOLAN_NINETALES")
    results.append(("a species this project moved reports how far it moved",
                    canon.delta("SPECIES_ALOLAN_NINETALES", ninetales)["bst"] == 50
                    and canon.delta("SPECIES_SLUGMA",
                                    pokedex.load(root, "SPECIES_SLUGMA"))["bst"] == 140,
                    ""))
    results.append(("the alternate-form records get a name rather than dashes",
                    ninetales["name"] == "Alolan Ninetales"
                    and pokedex.load(root, "SPECIES_LOPUNNY_M")["name"] == "Lopunny M",
                    ""))
    # A mega shares its base's line but is not a stage of it, and it is entered
    # twice, once for the day method and once for the night one.
    lopunny = server.dex_detail("SPECIES_LOPUNNY")
    results.append(("a mega is a forme, listed once, not two extra stages",
                    [m["label"] for m in lopunny["line"]] == ["Buneary", "Lopunny"]
                    and len(lopunny["formes"]) == 1
                    and not lopunny["evolutions"], ""))
    results.append(("a stage that merely looks like a form suffix is still a stage",
                    [m["label"] for m in server.dex_detail("SPECIES_PORYGON")["line"]]
                    == ["Porygon", "Porygon2", "Porygon-Z"], ""))


def check_weather_flag(results):
    """Build plan item 20: a weather ability in a regular slot is flagged in
    the dex and wherever a table or scripted source offers the species. The
    hidden slot is the Ability Patch's, so it is not flagged."""
    root = model.repo_root()
    rows = {r["species"]: r for r in server.dex_list()["rows"]}
    flagged = sorted(s for s, r in rows.items() if r["weather"])
    page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "index.html"),
                encoding="utf-8").read()
    results.append(("a weather ability in a regular slot is flagged, a hidden one is not",
                    rows["SPECIES_HIPPOPOTAS"]["weather"] == ["SAND_STREAM"]
                    and rows["SPECIES_ALOLAN_NINETALES"]["weather"] == []
                    and pokedex.load(root, "SPECIES_ALOLAN_NINETALES")["hidden_ability"]
                    == "SNOW_WARNING"
                    and server.dex_detail("SPECIES_SNOVER")["weather"] == ["SNOW_WARNING"]
                    and not rows["SPECIES_BULBASAUR"]["weather"],
                    f"{len(flagged)} species"))
    results.append(("the page shows the flag in the dex and on every source's species",
                    page.count("${weatherTag(") == 4 and 'data-f="weather"' in page,
                    ""))


def check_page(results):
    """D2's gate: every line the pick-list carries opens, and carries what the
    page draws. A species that half renders is worse than one that fails."""
    from . import dex
    root = model.repo_root()
    needed = ("name", "types", "stats", "bst", "abilities", "evolutions",
              "learnset", "sprites", "captures", "matchups", "line", "delta")
    # The two `cut` rows, Toxel and Toxtricity, are on the sheet and deliberately
    # not in the tree: their evolution depends on nature, which Generation 4 has
    # no method for. Everything else must be there.
    rows = [r for r in dex.pick_list(root) if r.get("status") != "cut"]
    constants = []
    for row in rows:
        try:
            constants.append(dex.constant_of(root, row["name"]))
        except Exception:
            constants.append(None)
    known = [c for c in constants if c]
    results.append(("every pick-list row but the two cut ones resolves to a "
                    "species in the tree",
                    len(known) == len(rows), f"{len(known)} of {len(rows)}"))

    broken, iconless = [], []
    for species in known:
        detail = server.dex_detail(species)
        if "error" in detail or any(k not in detail for k in needed):
            broken.append(species)
            continue
        if "icon" not in detail["sprites"]:
            iconless.append(species)
    results.append(("every one of them opens with everything the page draws",
                    not broken, f"broken {broken[:4]}"))
    results.append(("every one of them has a party icon to draw in the list",
                    not iconless, f"no icon: {iconless[:4]}"))

    # The list view draws an icon per row, so a row without a folder is a hole.
    rows = server.dex_list()["rows"]
    results.append(("every list row carries the folder its icon comes from",
                    all(r.get("folder") and r.get("name") and r.get("types")
                        for r in rows), ""))

    litten = server.dex_detail("SPECIES_LITTEN")
    members = {m["species"]: m for m in litten["line"]}
    # Fletchling's line, since Litten keeps only its Route 204 home now and
    # Torracat is met nowhere (the scarcity pass, 2026-09-26).
    fletch = {m["species"]: m for m in server.dex_detail("SPECIES_FLETCHLING")["line"]}
    results.append(("the line view answers where the other stages are met, which "
                    "is what the per-species index cannot",
                    "SPECIES_FLETCHINDER" in fletch
                    and fletch["SPECIES_FLETCHINDER"]["appearances"] > 0
                    and fletch["SPECIES_FLETCHINDER"]["folder"] == "fletchinder"
                    and "SPECIES_TORRACAT" in members, ""))
    results.append(("a learnset row carries the move's own numbers, not just its "
                    "name",
                    litten["learnset"][1]["type"] == "FIRE"
                    and litten["learnset"][1]["power"] == 40, ""))

    # Two views in one page means two of everything, and the first thing that
    # went wrong was an id used twice: both lists had `id="sortbar"`, the
    # tables view wires its buttons with the unscoped `#sortbar button`, and it
    # ran last, so the dex's four filters silently sorted the hidden tables
    # list instead. An id is unique or it is a class.
    page_path = os.path.join(root, "tools", "oxide", "encounters", "ui", "index.html")
    page = open(page_path, encoding="utf-8").read()
    ids = re.findall(r'id="([\w-]+)"', page)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    results.append(("no id is used twice, now that one page holds two views",
                    not dupes, f"duplicated: {dupes}"))
    script = page[page.index("<script>"):]
    used = set(re.findall(r'\$\("#([\w-]+)"\)', script))
    results.append(("every id the script reaches for exists in the markup",
                    not (used - set(ids)), f"missing: {sorted(used - set(ids))}"))
    # Each view's controls are selected through its own section, so neither can
    # reach into the other even if a class is shared.
    results.append(("each list's buttons are wired through its own section",
                    '"#list .sortbar button"' in script
                    and '"#dexlist .sortbar button"' in script, ""))

    # The page has two views and shows one by toggling `hidden` on a <main>.
    # That attribute carries its own display:none, but any author display rule
    # outranks it, and main is display:grid here: the first cut drew both views
    # stacked. The rule that settles it is easy to lose in a refactor and no
    # endpoint test can see it, so it is pinned here.
    page = open(os.path.join(root, "tools", "oxide", "encounters", "ui",
                             "index.html"), encoding="utf-8").read()
    style = page[page.index("<style>"):page.index("</style>")]
    hides = [line for line in style.splitlines()
             if "[hidden]" in line and "display" in line and "none" in line]
    # One toggle per view, so every view the header offers can be hidden.
    views = len(re.findall(r'<button data-view="', page))
    toggled = page.count(".hidden = view !==")
    results.append(("a hidden view is actually hidden, which `hidden` alone does "
                    "not manage against a styled display",
                    # Five since the box simulator's tab (2026-09-26).
                    bool(hides) and views == 5 and toggled == views,
                    f"{hides}, {toggled} toggles for {views} views"))

    # Ian's notes after D4: a species in a table opens its dex page, and Back
    # retraces the path. Both live only in the page, so the wiring is pinned:
    # the slot, water and "meets" icons link, the tables view catches their
    # click on the way down (before a water panel's own click can switch the
    # table), and every place is a history entry the popstate handler restores.
    results.append(("a species in the tables view opens the dex, and Back "
                    "retraces the path",
                    "icon(held, true)" in script and "icon(sl.species, true)" in script
                    and "icon(m.species, true)" in script
                    and '$("#mid").addEventListener("click"' in script
                    and "}, true);" in script
                    and 'id="back"' in page and "history.pushState" in script
                    and 'addEventListener("popstate"' in script, ""))

    # The sprites carry no alpha, so the server marks palette entry 0 clear.
    raw = open(os.path.join(root, "res", "pokemon", "clefairy",
                            "male_front.png"), "rb").read()
    once = server._transparent_background(raw)
    results.append(("a served sprite gets its transparent entry, and only once",
                    b"tRNS" not in raw and b"tRNS" in once
                    and server._transparent_background(once) == once, ""))


def check_qa_findings(results):
    """The QA pass of 2026-09-22 (docs/oxide/qa-review-2026-09-22-encounter-m8.md)."""
    root = model.repo_root()
    names = lambda d: [m["label"] for m in d["line"]]
    # Finding 1: Nidoran's male constant ends in _M, which is not a mega.
    nido = server.dex_detail("SPECIES_NIDORAN_M")
    results.append(("Nidoran\u2642 is a species in its own line, not a mega",
                    nido["mega_of"] is None
                    and names(nido) == ["Nidoran\u2642", "Nidorino", "Nidoking"]
                    and server.dex_detail("SPECIES_GYARADOS_M")["mega_of"]
                    == "SPECIES_GYARADOS", ""))
    # Finding 2: a line reads from its first stage, not alphabetically.
    eevee = server.dex_detail("SPECIES_EEVEE")
    results.append(("a line is in stage order, and a branch is siblings at one stage",
                    names(server.dex_detail("SPECIES_LITTEN"))
                    == ["Litten", "Torracat", "Incineroar"]
                    and names(server.dex_detail("SPECIES_GYARADOS"))
                    == ["Magikarp", "Gyarados"]
                    and eevee["line"][0]["label"] == "Eevee"
                    and eevee["line"][0]["stage"] == 0
                    and len(eevee["line"]) > 2
                    and all(m["stage"] == 1 for m in eevee["line"][1:]),
                    f"Eevee's branch: {len(eevee['line']) - 1}"))
    # Finding 4: a species file touched while the server runs is read again.
    path = os.path.join(root, "res", "pokemon", "litten", "data.json")
    st = os.stat(path)
    pokedex.load(root, "SPECIES_LITTEN")
    before = pokedex._load.cache_info().misses
    try:
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))
        pokedex.load(root, "SPECIES_LITTEN")
        reread = pokedex._load.cache_info().misses == before + 1
    finally:
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))
    results.append(("a species file changed while the server runs is read again",
                    reread, ""))


def check_moves_view(results):
    """D4: the move list, the move page and the reverse index."""
    root = model.repo_root()
    moves = pokedex.moves(root)
    results.append(("a move's id is its place in the enum, which is positional",
                    moves["MOVE_POUND"]["id"] == 1
                    and moves["MOVE_HONE_CLAWS"]["id"] == 471
                    and all(m["id"] is not None for m in moves.values()), ""))

    # Which effects are placeholders changes as element 4 writes scripts, so
    # nothing here pins a count: only what a placeholder can and cannot be.
    stubs = pokedex.stub_effects(root)
    ids = pokedex._effect_ids(root)
    results.append(("only an effect from the donor's range can be a placeholder, "
                    "and Platinum's own plain hit and Splash never are",
                    all(ids[e] >= pokedex.FIRST_DONOR_EFFECT for e in stubs)
                    and "HIT" not in stubs and "DO_NOTHING" not in stubs,
                    f"{len(stubs)} placeholder effects"))
    results.append(("a move is flagged exactly when its effect is a placeholder",
                    all(m["stub"] == (m["effect"] in stubs) for m in moves.values())
                    and not moves["MOVE_FLAMETHROWER"]["stub"]
                    and not moves["MOVE_FROST_BREATH"]["stub"],
                    f"{sum(m['stub'] for m in moves.values())} moves"))

    vanilla = pokedex.vanilla_moves(root)
    d = lambda mv: pokedex.move_delta(moves[mv], vanilla.get(mv))
    results.append(("the vanilla baseline is every move main has, read in one go",
                    len(vanilla) == 468 and "MOVE_MOONBLAST" not in vanilla,
                    f"{len(vanilla)} moves"))
    # Charm is element 1's Fairy retype, Tackle and Attack Order are the base
    # ROM's own edits, and Flamethrower is one of the 95 natives given the
    # King's Rock flag.
    results.append(("a move reports what changed from vanilla, field by field",
                    d("MOVE_CHARM") == {"type": {"was": "NORMAL", "now": "FAIRY"}}
                    and d("MOVE_TACKLE") == {"power": {"was": 35, "now": 40},
                                             "accuracy": {"was": 95, "now": 100}}
                    and d("MOVE_ATTACK_ORDER")["effect"]["now"] == "POISON_HIT"
                    and d("MOVE_FLAMETHROWER")
                    == {"power": {"was": 95, "now": 90},
                        "flags": {"gained": ["TRIGGERS_KINGS_ROCK"], "lost": []}}
                    and d("MOVE_POUND") is None
                    and d("MOVE_MOONBLAST") == {"new": True}, ""))

    machines = pokedex.machines(root)
    results.append(("every TM and HM names the move it teaches",
                    len(machines) == 100 and machines["TM02"] == "MOVE_DRAGON_CLAW"
                    and machines["HM03"] == "MOVE_SURF", f"{len(machines)} machines"))
    learnt = pokedex.learners(root)
    surf = {(r["species"], r["how"], r["machine"]) for r in learnt["MOVE_SURF"]}
    results.append(("the reverse index covers level-up, machines, tutors and eggs",
                    ("SPECIES_SQUIRTLE", "machine", "HM03") in surf
                    and {"species": "SPECIES_LITTEN", "how": "level", "level": 1,
                         "machine": None} in learnt["MOVE_SCRATCH"]
                    and any(r["how"] == "tutor" for r in learnt["MOVE_MUD_SLAP"])
                    and any(r["species"] == "SPECIES_GIBLE" and r["how"] == "egg"
                            for r in learnt["MOVE_OUTRAGE"]), ""))

    rows = server.move_list()["rows"]
    results.append(("the list is every move but NONE, with the comparison and the "
                    "learner count folded in",
                    len(rows) == len(moves) - 1
                    and [r["id"] for r in rows] == sorted(r["id"] for r in rows)
                    and any(r["new"] for r in rows) and any(r["changed"] for r in rows)
                    and next(r for r in rows if r["move"] == "MOVE_SURF")["learners"]
                    == len({s for s, _, _ in surf}), f"{len(rows)} rows"))

    detail = server.move_detail("surf")
    order = [pokedex.LEARN_KINDS.index(l["how"]) for l in detail["learners"]]
    wild = [l for l in detail["learners"] if l["first_split"]]
    results.append(("the move page names its machine and sorts who learns it by "
                    "how, then level",
                    detail["machine"] == "HM03" and order == sorted(order)
                    and wild and all(l["label"] and l["folder"] for l in wild), ""))
    scratch = [l["level"] for l in server.move_detail("MOVE_SCRATCH")["learners"]]
    results.append(("level-up learners come in level order",
                    scratch == sorted(scratch), ""))
    results.append(("an unknown move is an error rather than a crash",
                    "error" in server.move_detail("MOVE_NOT_A_MOVE"), ""))

    # Every move opens with what its page draws. Sampled, because each page
    # walks every species' learnset; one in twenty-five covers every range.
    needed = ("name", "type", "class", "id", "effect", "effect_id", "stub",
              "delta", "learners", "flags", "description")
    sample = [r["move"] for r in rows[::25]] + ["MOVE_HONE_CLAWS", "MOVE_CHARM"]
    broken = [mv for mv in sample
              if any(k not in server.move_detail(mv) for k in needed)]
    results.append(("a sample of moves across the whole range opens with "
                    "everything the page draws", not broken,
                    f"{len(sample)} opened, broken {broken[:4]}"))

    gible = server.dex_detail("SPECIES_GIBLE")
    garchomp = server.dex_detail("SPECIES_GARCHOMP")
    results.append(("the species page lists its machine, tutor and egg moves, "
                    "each naming the move it opens",
                    garchomp["machine_moves"][0] == {
                        "machine": "TM02", "move": "MOVE_DRAGON_CLAW",
                        "type": "DRAGON", "label": "Dragon Claw"}
                    and garchomp["tutor_moves"]
                    and any(m["move"] == "MOVE_OUTRAGE" for m in gible["egg_moves"]),
                    ""))


def check_calculator(results):
    """D5: the calculator's data comes from res/, carries this fork's chart,
    names everything the calculator can model, and loads nothing remote."""
    from . import calc_export
    root = model.repo_root()
    blob = calc_export.build()
    poks = blob["poks"]
    garchomp = poks.get("Garchomp", {})
    results.append(("every species is exported under the calculator's name, with "
                    "Oxide's numbers",
                    len(poks) == len(pokedex.species_list(root)) + len(calc_export.form_folders())
                    and garchomp.get("bs") == {"hp": 108, "at": 130, "df": 95,
                                               "sa": 85, "sd": 85, "sp": 102}
                    and poks["Clefairy"]["types"] == ["Fairy"]
                    and poks["Ninetales-Alola"]["types"] == ["Ice", "Fairy"]
                    and poks["Gible"]["abilities"] == {"0": "Sand Veil", "1": "Rough Skin"},
                    f"{len(poks)} species"))
    moves = blob["moves"]
    results.append(("moves carry Oxide's type, category and power, and a coded "
                    "power is left to the calculator",
                    moves["Charm"]["type"] == "Fairy"
                    and moves["Attack Order"]["basePower"] == 120
                    and moves["Dragon Breath"]["type"] == "Dragon"
                    and "basePower" not in moves["Grass Knot"], f"{len(moves)} moves"))

    # The chart is the reason the data travels at all: Generation 4 with
    # Fairy, Steel keeping its resistances to Ghost and Dark (Ian, 2026-09-22).
    chart = blob["type_chart"]
    results.append(("the exported chart is this fork's, not a stock one",
                    chart["Dark"]["Steel"] == 0.5 and chart["Ghost"]["Steel"] == 0.5
                    and chart["Dragon"]["Fairy"] == 0.0
                    and chart["Fairy"]["Dragon"] == 2.0
                    and chart["Fighting"]["Fairy"] == 0.5, ""))

    report = calc_export.report()
    known = calc_export.calc_names()["moves"]
    results.append(("every ability and move lands on a name the calculator has "
                    "logic for, and every hand-listed alias exists there",
                    not report["unknown_abilities"] and not report["unknown_moves"]
                    and all(calc_export.clean(t) in known
                            for t in calc_export.ALIASES.values()),
                    f"unknown: {report['unknown_abilities'][:3]} {report['unknown_moves'][:3]}"))
    # The named example has to be a move element 4 has not done. Grassy Terrain
    # stays a stub until terrain is ported, which waits on Ian; Acrobatics was
    # the example until element 4 finished it.
    stubbed = {m["name"] for m in pokedex.moves(root).values() if m["stub"]}
    results.append(("the report names the moves modelled with an effect Oxide's "
                    "script does not have yet",
                    set(report["placeholder_effects"]) <= stubbed
                    and "Grassy Terrain" in report["placeholder_effects"],
                    f"{len(report['placeholder_effects'])} moves"))

    # A species edited while the server runs is in the next export. The file
    # is put back exactly as it was whatever happens.
    path = os.path.join(root, "res", "pokemon", "gible", "data.json")
    with open(path, encoding="utf-8") as f:
        original = f.read()
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(original.replace('"attack": 70,', '"attack": 71,', 1))
        edited = calc_export.build()["poks"]["Gible"]["bs"]["at"]
    finally:
        with open(path, "w", encoding="utf-8") as f:
            f.write(original)
    results.append(("an edited species regenerates in the export without a restart",
                    edited == 71
                    and calc_export.build()["poks"]["Gible"]["bs"]["at"] == 70,
                    f"edited attack read {edited}"))

    # Offline: nothing the calculator's page loads may leave the machine. A
    # link a person could click is allowed; a script, stylesheet or image
    # source is not.
    calc_dir = os.path.join(root, "tools", "oxide", "encounters", "calc")
    page = open(os.path.join(calc_dir, "index.html"), encoding="utf-8").read()
    loads = re.findall(r'<(?:script|link|img|iframe)\b[^>]*?(?:src|href)=["\']\s*([^"\']+)', page)
    remote = [u for u in loads if re.match(r"\s*(https?:)?//", u)]
    init = open(os.path.join(calc_dir, "js", "initialize.js"), encoding="utf-8").read()
    results.append(("the calculator's page loads nothing from the network, and its "
                    "data comes from this server",
                    loads and not remote and "api.npoint.io" not in init
                    and "const npoint = `/api/calc-data`" in init
                    and "googletagmanager" not in page,
                    f"{len(loads)} loads, remote {remote[:3]}"))

    svg = server.calc_sprite("front", "garchomp.gif") or b""
    results.append(("the calculator's sprites are Oxide's own, first frame only",
                    svg.startswith(b"<svg") and b'viewBox="0 0 80 80"' in svg
                    and server.calc_sprite("pokesprite", "ninetales-alola.png")
                    and server.calc_sprite("front", "notapokemon.gif") is None, ""))

    # The picker: Oxide's species and the forms picked by hand, not every
    # species Showdown knows. Forms with a record carry Oxide's numbers
    # (Rotom's appliances are Electric/Fire here, Deoxys-Attack has Magic
    # Guard); there is no Pixie Plate, so no Arceus-Fairy.
    from . import canon
    picker = set(blob["picker"])
    forms = calc_export.form_folders()
    results.append(("the species picker offers Oxide's species and its hand-picked "
                    "forms, and nothing else",
                    picker == set(poks) and len(picker) == len(pokedex.species_list(root)) + len(forms)
                    and {"Rotom-Heat", "Giratina-Origin", "Shaymin-Sky", "Castform-Sunny",
                         "Cherrim-Sunshine", "Arceus-Fire"} <= picker
                    and not {"Arceus-Fairy", "Pikachu-Alola", "Burmy-Sandy"} & picker
                    and all(n in canon.table() for n in forms),
                    f"{len(picker)} names, {len(forms)} forms"))
    results.append(("a form with its own record carries Oxide's numbers for it",
                    poks["Rotom-Heat"]["types"] == ["Electric", "Fire"]
                    and poks["Rotom-Heat"]["bs"]["sp"] == 91
                    and poks["Deoxys-Attack"]["abilities"] == {"0": "Magic Guard"}
                    and poks["Castform-Rainy"]["types"] == ["Water"], ""))
    results.append(("every picked form has a sprite to draw",
                    all(server.calc_sprite("front", n.lower() + ".gif")
                        and server.calc_sprite("pokesprite", n.lower() + ".png")
                        for n in forms), ""))
    shared = open(os.path.join(calc_dir, "js", "shared_controls.js"), encoding="utf-8").read()

    # The skin is generated from upstream's stylesheets. If either changes
    # without a rerun, the calculator is drawn in stale colours.
    from . import make_calc_skin
    skin = open(make_calc_skin.OUT, encoding="utf-8").read()
    results.append(("the calculator's skin is current, loaded after upstream's "
                    "stylesheets, and follows the tool's toggle",
                    skin == make_calc_skin.build()
                    and not re.search(r"#[0-9a-fA-F]{6}\b", skin.split("*/", 1)[1])
                    and page.index("oxide-skin.css") > page.rindex("stylesheet\" href=\"./css/")
                    and '<script src="/theme.js">' in page, ""))

    # The Platinum Oxide profile's move lists and chart order are read from
    # the engine. If the engine's lists change without a rerun, the
    # calculator applies Sharpness or Sheer Force to the wrong moves.
    from . import make_calc_mechanics
    mech = open(os.path.join(root, make_calc_mechanics.OUT), encoding="utf-8").read()
    fresh = make_calc_mechanics.build(root)
    results.append(("the calculator's Oxide mechanics data is current and loaded "
                    "before the romhack profiles",
                    mech == make_calc_mechanics.render(fresh)
                    and "Night Slash" in fresh["slicing"] and "Frost Breath" in fresh["alwaysCrit"]
                    and page.index("profiles/platinum-oxide-data.js")
                    < page.index("profiles/platinum-oxide.js")
                    < page.index("romhacks/index.js"),
                    f"{len(fresh['slicing'])} slicing, {len(fresh['sheerForce'])} Sheer Force"))

    # Every patch is written down, so an upstream update knows what to redo.
    vendored = open(os.path.join(calc_dir, "VENDORED.md"), encoding="utf-8").read()
    results.append(("every patch to the vendored calculator is in its patch list",
                    all(f in vendored for f in ("js/initialize.js", "index.html",
                                                "js/oxide/title_to_backup_mappings.js",
                                                "js/vendor/oxide/", "oxide-skin.css",
                                                "js/shared_controls.js",
                                                "js/oxide/prefill_picker.js",
                                                "calc/mechanics/gen4.js",
                                                "calc/mechanics/util.js",
                                                "romhacks/helpers.js",
                                                "profiles/platinum-oxide.js",
                                                "js/oxide/menu.svg"))
                    and 'src="./js/oxide/menu.svg"' in page and "./img/menu.svg" not in page
                    and "npoint_data.picker" in shared
                    and 'src="./js/oxide/prefill_picker.js"' in page, ""))


def check_calc_mechanics(results):
    """The Platinum Oxide profile's rules, run through the calculator's own
    engine headless (the balance track's runner). Each case is compared with
    the same matchup without the ability, or pinned to a property the game's
    arithmetic has, so a stat change elsewhere does not break it."""
    import json
    import subprocess
    import tempfile
    from . import calc_export
    root = model.repo_root()
    runner = os.path.join(root, "tools", "oxide", "balance", "calc_headless.js")
    cases = {
        "sharp": ("Scyther", "Sharpness", "Bronzong", "", "Night Slash"),
        "blunt": ("Scyther", "Technician", "Bronzong", "", "Night Slash"),
        "pixie": ("Sylveon", "Pixilate", "Garchomp", "", "Hyper Voice"),
        "plain": ("Sylveon", "Cute Charm", "Garchomp", "", "Hyper Voice"),
        "sap": ("Venusaur", "Overgrow", "Goodra", "Sap Sipper", "Energy Ball"),
        "psywave": ("Alakazam", "Synchronize", "Garchomp", "", "Psywave"),
        "fang": ("Raticate", "Guts", "Garchomp", "", "Super Fang"),
        "crit": ("Frosmoth", "Shield Dust", "Crawdaunt", "Hyper Cutter", "Frost Breath"),
        "armor": ("Frosmoth", "Shield Dust", "Crawdaunt", "Shell Armor", "Frost Breath"),
        "ball": ("Pikachu", "Static", "Gyarados", "", "Electro Ball"),
        "order": ("Tyranitar", "Sand Stream", "Bronzor", "", "Crunch"),
        "order2": ("Machamp", "Guts", "Bronzor", "", "Cross Chop"),
    }
    jobs = {"pokemon": {}, "pairs": []}
    for key, (att, ability, dfn, dability, move) in cases.items():
        jobs["pokemon"]["a" + key] = {"species": att, "ability": ability, "level": 50}
        jobs["pokemon"]["d" + key] = {"species": dfn, "ability": dability or None, "level": 50}
        jobs["pairs"].append(["a" + key, "d" + key, [move], None])
    with tempfile.TemporaryDirectory() as tmp:
        paths = [os.path.join(tmp, n) for n in ("blob.json", "jobs.json", "out.json")]
        for path, data in zip(paths, (calc_export.build(), jobs)):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        run = subprocess.run(["node", runner] + paths, capture_output=True, text=True)
        out = json.load(open(paths[2])) if run.returncode == 0 else {"results": []}
    rolls = {}
    for key, row in zip(cases, out["results"]):
        rolls[key] = next(iter(row["moves"].values())).get("rolls") or [None]
    if len(rolls) < len(cases) or any(None in r for r in rolls.values()):
        results.append(("the calculator's Oxide profile runs", False, run.stderr[-200:]))
        return
    hp = out["pokemon"]["dfang"]["hp"]
    results.append(("the calculator applies Sharpness, Pixilate and Sap Sipper as "
                    "Oxide does",
                    rolls["sharp"][-1] >= rolls["blunt"][-1] * 14 // 10
                    and rolls["pixie"][0] > rolls["plain"][-1] and set(rolls["sap"]) == {0},
                    f"Night Slash {rolls['blunt'][-1]} to {rolls['sharp'][-1]}, "
                    f"Hyper Voice {rolls['plain'][-1]} to {rolls['pixie'][-1]}"))
    results.append(("Psywave, Super Fang and Electro Ball do what Oxide's engine does",
                    rolls["psywave"][0] == 25 and rolls["psywave"][-1] == 75
                    and set(rolls["fang"]) == {hp // 2} and rolls["ball"][-1] <= 12,
                    f"Psywave {rolls['psywave'][0]} to {rolls['psywave'][-1]}, "
                    f"Electro Ball at most {rolls['ball'][-1]}"))
    # Frost Breath always lands a critical hit unless the target has Shell
    # Armor. Crunch into Bronzor applies Psychic's double before Steel's half,
    # as the chart's rows come; the other way round every roll would be even.
    # Fighting's rows put Psychic's half first, so Cross Chop's rolls all are.
    results.append(("the always-critical moves crit, and a dual type's factors "
                    "come in chart order",
                    rolls["crit"][0] > rolls["armor"][-1] * 3 // 2
                    and any(r % 2 for r in rolls["order"])
                    and not any(r % 2 for r in rolls["order2"]),
                    f"Frost Breath {rolls['armor'][-1]} to {rolls['crit'][-1]}, "
                    f"Crunch {rolls['order'][0]} to {rolls['order'][-1]}, "
                    f"Cross Chop {rolls['order2'][0]} to {rolls['order2'][-1]}"))


def check_trainer_sets(results):
    """Every trainer's party in the calculator, rebuilt as the game builds it
    in battle. The natures are the part nothing stores, so the roll is pinned
    against an independent source: upstream's data for vanilla Platinum,
    generated by hzla's own tools, agreed with this code on 1,872 of 1,873
    vanilla sets when checked on 2026-09-22. Three of them are pinned here."""
    from . import calc_export, calc_trainers as ct
    root = model.repo_root()
    # Vanilla Roark: trainer 246, class 62 (male), IV scale 50. Upstream has
    # Geodude Lax, Onix Bold and Cranidos Jolly.
    natures = [ct.NATURES[ct.personality(246, 62, False, sp, lv, 50, ratio) % 25]
               for sp, lv, ratio in ((74, 12, 127), (95, 12, 127), (408, 14, 31))]
    results.append(("the nature roll reproduces the game's, pinned against "
                    "upstream's vanilla data", natures == ["Lax", "Bold", "Jolly"],
                    str(natures)))
    # Vanilla Lopunny's learnset, walked the way BoxPokemon_SetDefaultMoves
    # walks it: at level 38 the last four it learned, in the order learned.
    lopunny = [(1, "MIRROR_COAT"), (1, "MAGIC_COAT"), (1, "SPLASH"), (1, "POUND"),
               (1, "DEFENSE_CURL"), (1, "FORESIGHT"), (6, "ENDURE"), (13, "RETURN"),
               (16, "QUICK_ATTACK"), (23, "JUMP_KICK"), (26, "BATON_PASS"),
               (33, "AGILITY"), (36, "DIZZY_PUNCH"), (43, "CHARM")]
    results.append(("a trainer Pokemon with no moves listed gets the game's "
                    "default moveset", ct.default_moves(lopunny, 38)
                    == ["JUMP_KICK", "BATON_PASS", "AGILITY", "DIZZY_PUNCH"]
                    and ct.default_moves([(1, "A"), (1, "A"), (5, "B")], 5) == ["A", "B"],
                    ""))
    # This fork's gender and ability requests share the personality's low
    # byte; slot 2 with no gender sets bit 0 and nothing else.
    results.append(("an ability-slot request sets personality bit 0, and a gender "
                    "request lands on that gender",
                    ct.low_byte(127, None, 2, 136) == 137
                    and ct.low_byte(127, None, 1, 136) == 136
                    and ct.gender_of(127, ct.low_byte(127, "male", 0, 120)) == "M"
                    and ct.gender_of(127, ct.low_byte(127, "female", 2, 136)) == "F", ""))

    # A named nature (Oxide) steps the rolled high part until it lands, and
    # leaves the low byte, which holds gender and ability, alone. The C that
    # does this (TrainerMon_Personality) was compiled on the host and agreed
    # with this on 20,000 random inputs on 2026-09-22.
    rolled = ct.personality(246, 62, False, 74, 12, 50, 127)
    named = [ct.personality(246, 62, False, 74, 12, 255, 127, nature=n) for n in range(25)]
    results.append(("a named nature always lands, keeping the gender and ability "
                    "byte", all(p % 25 == n and p & 0xFF == rolled & 0xFF
                                for n, p in enumerate(named))
                    and ct.personality(246, 62, False, 74, 12, 50, 127,
                                       nature=rolled % 25) == rolled, ""))
    # The importer leaves a re-tuned member's nature and IV scale alone, and
    # still sees any real difference from the base ROM.
    sys.path.insert(0, os.path.join(root, "tools", "oxide"))
    import import_base_rom as ib
    base = [{"species": "SPECIES_NOSEPASS", "level": 15, "iv_scale": 250}]
    tuned = [dict(base[0], iv_scale=255, nature="NATURE_ADAMANT")]
    results.append(("the base ROM importer treats a named nature and its IV scale "
                    "as Oxide's own",
                    not ib._party_differs(tuned, base)
                    and ib._party_differs([dict(tuned[0], level=16)], base)
                    and ib._party_differs([dict(base[0], iv_scale=255)], base)
                    and ib._keep_oxide_tuning(tuned, base)[0]["nature"] == "NATURE_ADAMANT",
                    ""))

    blob = calc_export.build()
    sets = blob["formatted_sets"]
    members = 0
    for f in os.listdir(os.path.join(root, "res", "trainers", "data")):
        if not f.startswith("dummy"):
            with open(os.path.join(root, "res", "trainers", "data", f), encoding="utf-8") as fh:
                members += len(__import__("json").load(fh).get("party") or [])
    names = {n for by in sets.values() for n in by}
    parse = re.compile(r"\(Lvl\s+-?\d+\s+([^)]+)\)")
    results.append(("every party member of every trainer is a set, under a name "
                    "the calculator can parse",
                    sum(len(v) for v in sets.values()) == members
                    and set(sets) <= set(blob["poks"])
                    and all(parse.search(f"X ({n})") for n in names)
                    and "Lvl 15 Leader Roark" in names
                    and "Lvl 15 Leader Roark Rematch" not in names,
                    f"{sum(len(v) for v in sets.values())} sets for {members} members"))
    roark = sets["Cranidos"]["Lvl 15 Leader Roark"]
    rematch = next(s for sp, by in sets.items() for n, s in by.items()
                   if n.endswith("Leader Roark Rematch"))
    results.append(("a set carries the level, IVs, item, moves and AI flags the "
                    "game gives it",
                    roark["level"] == 16 and roark["item"] == "Sitrus Berry"
                    and roark["ivs"]["sp"] == 223 * 31 // 255 == 27
                    and roark["moves"][0] == "Headbutt" and roark["ai"] == 0b111
                    and rematch["ai"] & (1 << 3) and rematch["ai"] & (1 << 5),
                    f"Cranidos {roark['nature']} {roark['ability']}"))
    # A held item the calculator has no name for is dropped from the set.
    # Today that is only Rare Candy, which does nothing in battle.
    import json as _json
    unnamed = set()
    for f in os.listdir(os.path.join(root, "res", "trainers", "data")):
        with open(os.path.join(root, "res", "trainers", "data", f), encoding="utf-8") as fh:
            for m in _json.load(fh).get("party") or []:
                if m.get("item") and m["item"] != "ITEM_NONE" and not ct._item_name(m["item"]):
                    unnamed.add(m["item"])
    results.append(("every item a trainer holds reaches the calculator, bar one "
                    "with no battle effect, and has an icon",
                    unnamed <= {"ITEM_RARE_CANDY"}
                    and server.calc_item_icon("sitrus_berry.png")
                    and server.calc_item_icon("choice_specs.png"),
                    f"unnamed {sorted(unnamed)}"))
    results.append(("a trainer's form keeps its form in the calculator",
                    "Rotom-Mow" in sets and any(
                        n.endswith("Leader Volkner") for n in sets["Rotom-Mow"]), ""))


def main():
    results = []
    for check in (check_species, check_delta, check_chart, check_moves_and_sprites,
                  check_captures, check_endpoints, check_canon, check_page,
                  check_weather_flag, check_qa_findings, check_moves_view, check_calculator,
                  check_calc_mechanics, check_trainer_sets):
        check(results)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
