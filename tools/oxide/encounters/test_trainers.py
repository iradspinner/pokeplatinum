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
