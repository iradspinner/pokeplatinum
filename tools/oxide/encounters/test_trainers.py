"""The trainer team builder (build plan item 28): the Trainers tab's model
(trainers.py) and its routes.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_trainers

It never writes the tree's trainers: every save goes to a scratch copy of
res/trainers/data/ in a temporary folder, through save()'s folder and
registry arguments or a throwaway server pointed there by
OXIDE_TRAINERS_DIR. It checks that nothing in the checkout changed.
"""
import http.client
import json
import os
import subprocess
import sys
import threading

from . import calc_trainers
from . import model
from . import server
from . import trainers


def get(port, path):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = json.loads(resp.read().decode("utf-8") or "{}")
    conn.close()
    return resp.status, body


def check_read(results, root):
    rows = trainers.summary(root)
    files = [f for f in os.listdir(os.path.join(root, *trainers.DATA)) if f.endswith(".json")]
    results.append(("every trainer file is a row, with its party, split and cap",
                    len(rows) == len(files) and all("party" in r for r in rows)
                    and next(r for r in rows if r["stem"] == "leader_roark")["cap"] == 16,
                    f"{len(rows)} rows"))
    # The list places trainers without building parties; teamscore.resolve,
    # which the score uses, builds them. The two must agree, except that the
    # score refuses a split with no cap (Post), which the list still names.
    from ..balance import teamscore
    sample = [r["stem"] for r in rows if r["split"]][::40]
    differ = []
    for stem in sample:
        try:
            got = teamscore.resolve(stem)["split"]
        except ValueError:
            got = None
        listed = trainers.split_map(root)[stem]
        if got != (listed if listed in trainers.caps() else None):
            differ.append(f"{stem}: list {listed}, score {got}")
    results.append(("the list's split is the one the score uses (teamscore.resolve), "
                    "which refuses a split with no cap",
                    sample and not differ, f"{len(sample)} sampled; " + "; ".join(differ[:3])))
    # The list sorts by the balance track's stored scores (Ian, 2026-09-27):
    # a story fight's from pressure.json, shared by its variants, and an
    # ordinary trainer's from b6.json, each on Ian's scale by the plan's line.
    from ..balance import b6, pressure
    line = b6.scale_line()
    on = lambda safe: round(b6.on_scale(safe, line), 1)
    by = {r["stem"]: r["score"] for r in rows}
    tristan = b6.load()["trainers"]["1"]
    barry = [by.get(s) for s in ("rival_route_201_piplup", "rival_route_201_turtwig",
                                 "rival_route_201_chimchar")]
    results.append(("each row carries its stored score: Roark's story fight, Tristan's own, and "
                    "one score for every variant of a story fight",
                    by["leader_roark"] == {"scale": on(pressure.load()["fights"]["roark"]["safe"]),
                                           "fight": "roark", "band": by["leader_roark"]["band"]}
                    and by["youngster_tristan"]["scale"] == on(tristan["safe"])
                    and by["youngster_tristan"]["fight"] is None
                    and all(barry) and barry[0]["fight"] == "barry_1"
                    and len({json.dumps(b, sort_keys=True) for b in barry}) == 1
                    and all("score" in r for r in rows),
                    f"Roark {by['leader_roark']}, Tristan {by['youngster_tristan']}"))
    d = trainers.detail(root, "leader_roark")
    built = calc_trainers.build_trainer(root, "leader_roark")
    results.append(("a team shows what the game builds: Roark's natures, abilities and moves",
                    [m["built"]["nature"] for m in d["members"]] == [s["nature"] for _, s in built]
                    and [m["built"]["ability"] for m in d["members"]] == [s["ability"] for _, s in built]
                    and d["members"][0]["built"]["moves"][0] == "Block"
                    and d["cap"] == 16 and d["split"] == "Roark", ""))
    results.append(("the AI flags listed are the named ones, in bit order",
                    d["all_ai_flags"][0] == "AI_FLAG_BASIC"
                    and not any(f.startswith("AI_FLAG_UNUSED") for f in d["all_ai_flags"]),
                    f"{len(d['all_ai_flags'])} flags"))
    try:
        trainers.load(root, "../x")
        refused = False
    except KeyError:
        refused = True
    results.append(("a stem is a file name, never a path", refused, ""))


def check_move_lists(results, root):
    from . import learnsets
    bidoof = learnsets.lists(root, "SPECIES_BIDOOF", 0, 10)
    results.append(("a Sinnoh line cut from Scarlet and Violet takes Generation 8 from BDSP "
                    "(Bidoof)", bidoof["latest"]["gen"] == 8
                    and "Brilliant Diamond" in bidoof["latest"]["games"]
                    and len(bidoof["latest"]["moves"]) > 20,
                    f"gen {bidoof['latest']['gen']}, {len(bidoof['latest']['moves'])} moves"))
    sinistcha = learnsets.lists(root, "SPECIES_SINISTCHA", 0, 30)
    results.append(("a species added after Generation IV has an empty Generation IV list, and "
                    "Oxide's own list follows Oxide's chain (Sinistcha from Sinistea)",
                    sinistcha["gen4"]["moves"] == [] and sinistcha["latest"]["gen"] == 9
                    and any(e["from"] == "Sinistea" for e in sinistcha["oxide"]), ""))
    politoed = learnsets.lists(root, "SPECIES_POLITOED", 0, 40)
    by_name = lambda lst, n: next((e for e in lst if e["name"] == n), None)
    bubble = by_name(politoed["oxide"], "Bubble")
    results.append(("an earlier stage's move is listed and credited to it (Bubble, as Poliwhirl)",
                    bubble is not None and bubble["from"] == "Poliwhirl"
                    and by_name(politoed["gen4"]["moves"], "Bubble") is not None, ""))
    level_up = [e for e in politoed["oxide"] if e["how"].startswith("Level") and not e["from"]]
    own = [lv for lv, _ in (calc_trainers._raw_species(root, "SPECIES_POLITOED")
                            .get("learnset") or {}).get("by_level") or []]
    results.append(("Oxide's own list stops at the member's level",
                    level_up and max(int(e["how"].split()[1].split(",")[0]) for e in level_up) <= 40
                    and max(own) > 40, f"learns up to {max(own)}"))
    ids = learnsets.move_ids(root)
    results.append(("canon moves map to Oxide's, the Generation IV spellings included "
                    "(Faint Attack, Hi Jump Kick)",
                    ids.get("feintattack") == ids.get("faintattack") is not None
                    and ids.get("highjumpkick") is not None, ""))


def check_lint(results, root):
    roark = trainers.load(root, "leader_roark")
    clean = trainers.lint(root, roark)

    def with_member(**change):
        d = json.loads(json.dumps(roark))
        d["party"][0].update(change)
        return [f["message"] for f in trainers.lint(root, d) if f["severity"] == "error"]
    choice = json.loads(json.dumps(roark))
    choice["party"][1]["item"] = "ITEM_CHOICE_SCARF"
    lone = dict(json.loads(json.dumps(roark)), double_battle=True)
    lone["party"] = lone["party"][:1]
    mixed = json.loads(json.dumps(roark))
    mixed["party"][2]["moves"] = None
    results.append(("the trainer lint passes Roark and refuses what the packer or the game would "
                    "get wrong", not [f for f in clean if f["severity"] == "error"]
                    and with_member(level=101) and with_member(moves=["MOVE_NOPE"])
                    and with_member(nature="NATURE_COUNT") and with_member(ability=4)
                    and with_member(species="SPECIES_NIDORAN_M", gender="female")
                    and with_member(form=3) and trainers.lint(root, lone)
                    and any("moves or none does" in f["message"] for f in trainers.lint(root, mixed)),
                    ""))
    results.append(("a Choice item is a warning, not an error (Ian, 2026-09-26)",
                    [f["severity"] for f in trainers.lint(root, choice)] == ["warn"], ""))


def check_style(results, root):
    """A save touches only the fields that changed, in the files' own style."""
    party_miss, field_miss = [], []
    folder = trainers.data_dir(root)
    for f in sorted(os.listdir(folder)):
        with open(os.path.join(folder, f), encoding="utf-8") as fh:
            text = fh.read()
        data = json.loads(text)
        vs, ve, indent = trainers.jsonstyle._find_key(text, ["party"])
        if data["party"] and trainers.dump_party(data["party"], indent) != text[vs:ve]:
            party_miss.append(f)
        t = text
        for key in trainers.HEADER_EDITS:
            t = trainers._replace(t, [key], data[key])
        for i, m in enumerate(data["party"]):
            for key, val in m.items():
                t = trainers._replace(t, ["party", i, key], val)
        if t != text:
            field_miss.append(f)
    results.append(("rewriting a whole party reproduces every file's party byte for byte",
                    not party_miss, ", ".join(party_miss[:4])))
    # Two files write their AI flags on one line, against every other file;
    # a save changes them only when their flags are edited.
    results.append(("rewriting any field with its own value leaves every file as it was, bar "
                    "the two that write their AI flags on one line",
                    set(field_miss) == {"bug_catcher_jack.json", "ninja_boy_zach.json"},
                    ", ".join(field_miss[:4])))


def check_save(results, root):
    """Saving, on a scratch copy of the trainers: never the tree's own files."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "data")
        shutil.copytree(trainers.data_dir(root), folder)
        registry = os.path.join(tmp, "trainers_diverged.json")
        path = os.path.join(folder, "leader_roark.json")
        with open(path, encoding="utf-8") as f:
            before = f.read()
        d = json.loads(before)
        d["party"][0]["level"] = 16
        d["party"][1]["nature"] = "NATURE_ADAMANT"
        d["ai_flags"] = d["ai_flags"] + ["AI_FLAG_RISKY"]
        out = trainers.save(root, "leader_roark", d, folder=folder, registry=registry)
        with open(path, encoding="utf-8") as f:
            after = f.read()
        import difflib
        diff = [l for l in difflib.unified_diff(before.splitlines(), after.splitlines(),
                                                lineterm="", n=0)
                if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        lost = [l[1:] for l in diff if l.startswith("-")]
        gained = [l[1:] for l in diff if l.startswith("+")]
        with open(registry, encoding="utf-8") as f:
            reg = json.load(f)
        results.append(("a save writes only what changed: a level, a named nature after the IV "
                        "scale, an AI flag; it packs, and registers the trainer",
                        len(lost) == 2 and len(gained) == 4
                        and '            "nature": "NATURE_ADAMANT",' in gained
                        and out["packer"] in ("packed", None)
                        and set(reg["leader_roark"]) == {"party", "ai_flags"},
                        f"-{len(lost)} +{len(gained)}, {out['packer']}"))
        bad = json.loads(after)
        bad["party"][0]["level"] = 101
        try:
            trainers.save(root, "leader_roark", bad, folder=folder, registry=registry)
            refused = False
        except trainers.SaveRefused:
            refused = True
        # A packer refusal puts the file back as it was.
        real_check = trainers.pack_check
        trainers.pack_check = lambda _root, _folder: (False, "refused on purpose")
        try:
            again = json.loads(after)
            again["party"][0]["level"] = 17
            trainers.save(root, "leader_roark", again, folder=folder, registry=registry)
            restored = False
        except trainers.SaveRefused:
            with open(path, encoding="utf-8") as f:
                restored = f.read() == after
        finally:
            trainers.pack_check = real_check
        results.append(("a save the lint refuses writes nothing, and one the packer refuses is "
                        "put back", refused and restored, ""))


def check_importer(results, root):
    """The base ROM importer leaves a registered trainer's fields alone, the
    header fields included, which it did not before 2026-09-27."""
    import tempfile
    sys.path.insert(0, os.path.join(root, "tools", "oxide"))
    import import_base_rom as ib
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "builder_probe.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"name": "X", "class": "TRAINER_CLASS_YOUNGSTER", "items": [],
                                "ai_flags": ["AI_FLAG_BASIC"], "double_battle": False,
                                "party": []}, indent=4))
        vanilla = {"class": "TRAINER_CLASS_YOUNGSTER", "items": [],
                   "ai_flags": ["AI_FLAG_BASIC", "AI_FLAG_EXPERT"], "double_battle": False}
        base = dict(vanilla, ai_flags=["AI_FLAG_EXPERT"])
        free = ib.apply_trainer_diff(path, base, [], vanilla, [], True, [])
        ib.TRAINERS_DIVERGED["builder_probe"] = {"ai_flags": "a test"}
        try:
            kept = not ib.apply_trainer_diff(path, base, [], vanilla, [], True, [])
        finally:
            del ib.TRAINERS_DIVERGED["builder_probe"]
    results.append(("the importer would carry the base ROM's AI flags back, and leaves them "
                    "alone once the trainer is registered", free and kept, ""))
    results.append(("the importer reads the builder's registry beside it",
                    ib.TRAINERS_DIVERGED_FILE.endswith(os.path.join("tools", "oxide",
                                                                    "trainers_diverged.json"))
                    and trainers.registry_path(root) == ib.TRAINERS_DIVERGED_FILE
                    or bool(os.environ.get("OXIDE_TRAINERS_REGISTRY")), ""))


def post(port, path, data):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=120)
    conn.request("POST", path, json.dumps({"data": data}), {"Content-Type": "application/json"})
    resp = conn.getresponse()
    body = json.loads(resp.read().decode("utf-8") or "{}")
    conn.close()
    return resp.status, body


def check_edit_routes(results, root):
    """/preview and a save through the server, pointed at a scratch copy by
    OXIDE_TRAINERS_DIR, as a test server is."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "data")
        shutil.copytree(trainers.data_dir(root), folder)
        keep = {k: os.environ.get(k) for k in ("OXIDE_TRAINERS_DIR", "OXIDE_TRAINERS_REGISTRY")}
        os.environ["OXIDE_TRAINERS_DIR"] = folder
        os.environ["OXIDE_TRAINERS_REGISTRY"] = os.path.join(tmp, "trainers_diverged.json")
        httpd = server.Server(("127.0.0.1", 0), server.Handler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            d = trainers.load(root, "leader_roark")
            d["party"][1]["nature"] = "NATURE_ADAMANT"
            preview = post(port, "/api/trainer/leader_roark/preview", d)
            strong = json.loads(json.dumps(d))
            strong["party"][3]["level"] = 30
            harder = post(port, "/api/trainer/leader_roark/preview", strong)
            scored = post(port, "/api/trainer/leader_roark/score", strong)
            post_trainer = get(port, "/api/trainer/cameraman_tevin_rematch_1")
            bad = json.loads(json.dumps(d))
            bad["party"][0]["level"] = 0
            refused = post(port, "/api/trainer/leader_roark", bad)
            saved = post(port, "/api/trainer/leader_roark", d)
        finally:
            httpd.shutdown()
            httpd.server_close()
            for k, v in keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        with open(os.path.join(folder, "leader_roark.json"), encoding="utf-8") as f:
            written = json.load(f)
    results.append(("/preview rebuilds an unsaved team (Geodude Adamant) and writes nothing",
                    preview[0] == 200 and preview[1]["detail"]["members"][1]["built"]["nature"]
                    == "Adamant", str(preview[0])))
    results.append(("a save through the server refuses a lint error with its findings (409) and "
                    "writes a good team", refused[0] == 409 and refused[1]["findings"]
                    and saved[0] == 200 and written["party"][1].get("nature") == "NATURE_ADAMANT",
                    f"{refused[0]} {saved[0]}"))
    est, hard = preview[1].get("estimate") or {}, harder[1].get("estimate") or {}
    results.append(("every preview carries teamscore's estimate with its margin, and a stronger "
                    "unsaved team reads harder (Cranidos at 30)",
                    est.get("kind") == "estimate" and est.get("split") == "Roark"
                    and est.get("cap") == 16 and (est.get("fit") or {}).get("story_max_error")
                    and hard.get("safe", 1) < est.get("safe", 0),
                    f"{est.get('scale')} then {hard.get('scale')}"))
    results.append(("Score it runs the full scorer on the unsaved team and gives the reference "
                    "hacks' same seat; a Post trainer is not scored",
                    scored[0] == 200 and scored[1].get("kind") == "score"
                    and "vanilla" in (scored[1].get("references") or {})
                    and "error" in (post_trainer[1].get("estimate") or {}),
                    f"{scored[1].get('scale')} in {scored[1].get('seconds')} s"))


SOMNU, MOIRA = "galactic_grunt_lake_verity_3", "galactic_grunt_lake_verity_4"
LAKE_PAIR = f"{SOMNU}+{MOIRA}"


def check_pairs(results, root):
    """Two trainers fought as one double (Ian, 2026-09-28), from the balance
    track's finder: a row per pair, both teams in one view, and a save that
    writes both or neither, on a scratch copy of the trainers."""
    import shutil
    import tempfile
    entries = trainers.pair_entries()
    rows = trainers.pair_rows(root)
    by_label = {r["label"]: r for r in rows}
    files = set(trainers.stems(root))
    unmatched = sorted({st for p in entries for st in p["stems"] if st not in files})
    results.append(("every pair the finder names has a row, so the tab and the scores agree "
                    "on which trainers fight together",
                    len(rows) == len(entries) and not unmatched,
                    f"{len(rows)} rows for {len(entries)} pairs"
                    + (f"; no file for {', '.join(unmatched[:4])}" if unmatched else "")))
    find = lambda *names: next((r for r in rows if all(n in r["label"] for n in names)), None)
    tyche, somnu, maya = find("Tyche", "Hermes"), find("Somnu", "Moira"), find("Maya", "Dennis")
    results.append(("Ian's three pairs are one row each: Tyche and Hermes (scripted), Somnu and "
                    "Moira (eye contact, Candice's split), Maya and Dennis (Maylene's split)",
                    tyche and tyche["how"] == "scripted" and somnu and somnu["how"] == "eye contact"
                    and somnu["split"] == "Candice" and maya and maya["split"] == "Maylene"
                    and all(len(r["parties"]) == 2 and all(r["parties"]) for r in (tyche, somnu, maya)),
                    ", ".join(r["label"] for r in (tyche, somnu, maya) if r)))
    ashlee = [r for r in rows if "ranger_ashlee" in r["stems"]]
    tag = next((r for r in rows if r["how"] == "tag" and "jubilife" in r["key"]), None)
    results.append(("a trainer in two pairs is in both rows (Ranger Ashlee), and a tag battle "
                    "names the partner beside the player (Dawn or Lucas at Jubilife)",
                    len(ashlee) == 2 and tag and any("Dawn" in n for n in tag["partners"])
                    and any("Lucas" in n for n in tag["partners"]),
                    f"{len(ashlee)} rows for Ashlee"))
    d = trainers.pair_detail(root, LAKE_PAIR)
    results.append(("a pair's view holds both teams, each with its members and its own estimate",
                    [s["stem"] for s in d["sides"]] == [SOMNU, MOIRA]
                    and all(s["members"] and "estimate" in s for s in d["sides"])
                    and d["split"] == "Candice", str([len(s["members"]) for s in d["sides"]])))
    # The pair as one fight (teamscore takes the pair's key and {stem: JSON}).
    joint = d.get("estimate") or {}
    stronger = trainers.load(root, MOIRA)
    for m in stronger["party"]:
        m["level"] = m["level"] + 8
    harder = trainers.pair_preview(root, LAKE_PAIR, {MOIRA: stronger}).get("estimate") or {}
    results.append(("the pair has its own estimate as one fight in Candice's split, and an unsaved "
                    "stronger team on one side reads harder",
                    joint.get("kind") == "estimate" and joint.get("split") == "Candice"
                    and not joint.get("error") and harder.get("safe", 1) < joint.get("safe", 0),
                    f"{joint.get('scale')} then {harder.get('scale')}"))

    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "data")
        shutil.copytree(trainers.data_dir(root), folder)
        registry = os.path.join(tmp, "trainers_diverged.json")
        read = lambda st: open(os.path.join(folder, st + ".json"), encoding="utf-8").read()
        somnu_before, moira_before = read(SOMNU), read(MOIRA)
        moira = json.loads(moira_before)
        moira["party"][0]["level"] = moira["party"][0]["level"] + 1
        out = trainers.pair_save(root, LAKE_PAIR, {MOIRA: moira}, folder=folder, registry=registry)
        with open(registry, encoding="utf-8") as f:
            reg = json.load(f)
        results.append(("saving one side of a pair writes that trainer's file only",
                        read(SOMNU) == somnu_before and read(MOIRA) != moira_before
                        and set(out) == {MOIRA} and set(reg) == {MOIRA}, str(list(reg))))
        moira_saved = read(MOIRA)
        bad = json.loads(somnu_before)
        bad["party"][0]["level"] = 0
        again = json.loads(moira_saved)
        again["party"][0]["level"] = again["party"][0]["level"] + 1
        try:
            trainers.pair_save(root, LAKE_PAIR, {SOMNU: bad, MOIRA: again}, folder=folder, registry=registry)
            lint_refused = None
        except trainers.SaveRefused as exc:
            lint_refused = exc
        results.append(("a lint error on one side writes neither team, and its findings name "
                        "their side", lint_refused is not None and read(SOMNU) == somnu_before
                        and read(MOIRA) == moira_saved
                        and any(f.get("stem") == SOMNU for f in lint_refused.findings), ""))
        # The packer refuses the second side after the first was written: the
        # first is put back, file and registry, so nothing is half-saved.
        real_check, calls = trainers.pack_check, []

        def second_refused(_root, _folder):
            calls.append(1)
            return (False, "refused on purpose") if len(calls) == 2 else (True, "")
        trainers.pack_check = second_refused
        reg_before = open(registry, encoding="utf-8").read()
        good_somnu = json.loads(somnu_before)
        good_somnu["party"][0]["level"] = good_somnu["party"][0]["level"] + 1
        try:
            trainers.pair_save(root, LAKE_PAIR, {SOMNU: good_somnu, MOIRA: again},
                               folder=folder, registry=registry)
            packer_refused = False
        except trainers.SaveRefused:
            packer_refused = True
        finally:
            trainers.pack_check = real_check
        results.append(("when the packer refuses the second side, the first is put back, file "
                        "and registry", packer_refused and len(calls) == 2
                        and read(SOMNU) == somnu_before and read(MOIRA) == moira_saved
                        and open(registry, encoding="utf-8").read() == reg_before, ""))
        try:
            trainers.pair_save(root, LAKE_PAIR, {"leader_roark": moira}, folder=folder, registry=registry)
            stray = False
        except trainers.SaveRefused:
            stray = True
        results.append(("a pair refuses an edit to a trainer outside it", stray, ""))

    # The routes, against a scratch copy as a test server is.
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "data")
        shutil.copytree(trainers.data_dir(root), folder)
        keep = {k: os.environ.get(k) for k in ("OXIDE_TRAINERS_DIR", "OXIDE_TRAINERS_REGISTRY")}
        os.environ["OXIDE_TRAINERS_DIR"] = folder
        os.environ["OXIDE_TRAINERS_REGISTRY"] = os.path.join(tmp, "trainers_diverged.json")
        httpd = server.Server(("127.0.0.1", 0), server.Handler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            listing = get(port, "/api/trainers")
            one = get(port, "/api/pair/" + LAKE_PAIR)
            missing = get(port, "/api/pair/no_such+pair")
            moira = trainers.load(root, MOIRA)
            moira["party"][0]["level"] += 1
            preview = post(port, f"/api/pair/{LAKE_PAIR}/preview", {MOIRA: moira})
            bad = json.loads(json.dumps(moira))
            bad["party"][0]["level"] = 0
            refused = post(port, f"/api/pair/{LAKE_PAIR}", {SOMNU: trainers.load(root, SOMNU), MOIRA: bad})
            scored = post(port, f"/api/pair/{LAKE_PAIR}/score", {MOIRA: moira})
            saved = post(port, f"/api/pair/{LAKE_PAIR}", {MOIRA: moira})
        finally:
            httpd.shutdown()
            httpd.server_close()
            for k, v in keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    results.append(("the routes: /api/trainers lists the pairs, /api/pair/<key> is both teams (an "
                    "unknown pair a 404), /preview rebuilds one side, and a save refuses a lint "
                    "error (409) and writes a good one",
                    listing[0] == 200 and len(listing[1].get("pairs") or []) == len(rows)
                    and one[0] == 200 and len(one[1]["sides"]) == 2 and missing[0] == 404
                    and preview[0] == 200 and list(preview[1]["sides"]) == [MOIRA]
                    and refused[0] == 409 and saved[0] == 200
                    and list(saved[1]["changed"]) == [MOIRA],
                    f"{one[0]} {missing[0]} {preview[0]} {refused[0]} {saved[0]}"))
    results.append(("/api/pair/<key>/score runs the full scorer on the pair as one fight, with "
                    "the unsaved edit in place", scored[0] == 200 and scored[1].get("kind") == "score"
                    and scored[1].get("split") == "Candice",
                    f"{scored[1].get('scale')} in {scored[1].get('seconds')} s"))


def check_routes(results):
    httpd = server.Server(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        listing = get(port, "/api/trainers")
        one = get(port, "/api/trainer/leader_roark")
        missing = get(port, "/api/trainer/no_such_trainer")
        lists = get(port, "/api/trainer-moves?species=SPECIES_NOSEPASS&level=15")
        bad = get(port, "/api/trainer-moves?species=SPECIES_NOPE")
    finally:
        httpd.shutdown()
        httpd.server_close()
    results.append(("/api/trainers lists them in split order's terms, and /api/trainer/<stem> "
                    "is one team; an unknown stem is a 404",
                    listing[0] == 200 and listing[1]["splits"][0] == "Roark"
                    and listing[1]["caps"]["Roark"] == 16
                    and one[0] == 200 and len(one[1]["members"]) == 4
                    and missing[0] == 404, f"{listing[0]} {one[0]} {missing[0]}"))
    results.append(("/api/trainer-moves gives the three lists apart; an unknown species is a 404",
                    lists[0] == 200 and {"oxide", "gen4", "latest"} <= set(lists[1])
                    and lists[1]["level"] == 15 and bad[0] == 404, f"{lists[0]} {bad[0]}"))


def main():
    results = []
    root = model.repo_root()
    before = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                            capture_output=True, text=True).stdout
    check_read(results, root)
    check_move_lists(results, root)
    check_lint(results, root)
    check_style(results, root)
    check_save(results, root)
    check_importer(results, root)
    check_edit_routes(results, root)
    check_pairs(results, root)
    check_routes(results)
    after = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                           capture_output=True, text=True).stdout
    results.append(("nothing in the checkout changed", before == after, ""))

    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
