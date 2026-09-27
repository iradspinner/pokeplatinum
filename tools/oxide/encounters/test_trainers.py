"""The trainer team builder (build plan item 28): the Trainers tab's model
(trainers.py) and its routes.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_trainers

Read-only: it reads res/trainers/data/ and asks a throwaway server on a free
port for the tab's data, and checks that nothing in the checkout changed.
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
