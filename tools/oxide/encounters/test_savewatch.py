"""The Sync bridge (savewatch.py): the OxiDex watches a save file and serves
its party and boxes to the calculator's Sync.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_savewatch

Every save here is built byte by byte in a temporary folder (test_savefile's
builder), and the path setting goes to a temporary file through
OXIDEX_SETTINGS, so the test touches neither Ian's save nor his settings.
"""
import hashlib
import http.client
import json
import os
import shutil
import struct
import sys
import tempfile
import threading
import time

from . import savefile as S
from . import savewatch as W
from . import server
from . import test_savefile as T


def wait_for(cond, seconds=8.0):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if cond():
            return True
        time.sleep(0.1)
    return cond()


def party_save(level):
    """A save whose one party Pokemon is a Chimchar at `level`."""
    mon = T.record(0x12345678, T.species_id("SPECIES_CHIMCHAR"), [T.move_id("MOVE_SCRATCH")],
                   T.ability_id("ABILITY_BLAZE"), exp=S._tables()["exp"]["medium_slow"][level],
                   party_level=level)
    return T.make_save([mon], {(1, 1): T.record(0x0BADF00D, T.species_id("SPECIES_GLIMMET"),
                                                [T.move_id("MOVE_SCRATCH")], 1, exp=500)})


def write(path, data):
    """Replaces the file the way an emulator does: written in place."""
    with open(path, "wb") as f:
        f.write(data)


def main():
    results = []
    tmp = tempfile.mkdtemp(prefix="oxidex-savewatch-")
    os.environ["OXIDEX_SETTINGS"] = os.path.join(tmp, "settings.json")

    results.append(("a Windows path is read as WSL sees it: a drive letter under /mnt, a "
                    "\\\\wsl.localhost path on the Linux side",
                    W.normalize(r"G:\PokeROMs\Rokemon RomHack Creation Hub\x.sav")
                    == "/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/x.sav"
                    and W.normalize(r"\\wsl.localhost\Ubuntu\home\ian\oxide-playtest\a.sav")
                    == "/home/ian/oxide-playtest/a.sav"
                    and W.normalize(r"\\wsl$\Ubuntu\home\ian\a.sav") == "/home/ian/a.sav"
                    and W.normalize(' "/home/ian/a.sav" ') == "/home/ian/a.sav", ""))

    data = party_save(6)
    pk = S.packed(data)
    tid, sid, count, boxes, psize, bsize, slots, current = struct.unpack_from("<HHBBHHHB", pk, 4)
    n0 = S.blocks(data)[S.BLOCK_NORMAL]["start"]
    raw_party = data[n0 + S.PARTY_AT + 8:n0 + S.PARTY_AT + 8 + S.PARTY_RECORD]
    results.append(("the packed save is the calculator's DPB1: its header, then the party and "
                    "every box slot exactly as the save stores them",
                    pk[:4] == b"DPB1" and (tid, sid, count, boxes, psize, bsize, slots)
                    == (25097, 32454, 1, 18, 236, 136, 540)
                    and pk[18:18 + 236] == raw_party and len(pk) == 18 + 236 + 540 * 136,
                    f"{len(pk)} bytes"))

    # The watcher, on its own thread, with inotify and then without it.
    for mode in ("inotify", "polling"):
        path = os.path.join(tmp, f"{mode}.sav")
        write(path, party_save(6))
        before = hashlib.sha1(open(path, "rb").read()).hexdigest()
        if mode == "polling":
            real, W._inotify = W._inotify, lambda: None
            real_poll, W.POLL_SECONDS = W.POLL_SECONDS, 1
        w = W.Watcher()
        try:
            w.set_path(path)
            w.start()
            first = wait_for(lambda: w.state["seq"] >= 1)
            seen_mode = w.state["mode"]
            level = lambda: (w.snapshot()["save"] or {}).get("party", [""])[0]
            untouched = hashlib.sha1(open(path, "rb").read()).hexdigest() == before
            time.sleep(1.1)                     # a new mtime even on a coarse clock
            write(path, party_save(9))
            second = wait_for(lambda: w.state["seq"] >= 2 and "Lv 9" in level())
        finally:
            w.stop()
            if mode == "polling":
                W._inotify, W.POLL_SECONDS = real, real_poll
        results.append((f"the watcher by {mode}: reads the save, sees it saved again, and never "
                        f"changes the file", first and second and seen_mode == mode and untouched,
                        f"mode {seen_mode}, seq {w.state['seq']}, {level()}"))

    # A save that goes bad keeps the last good one and says why.
    path = os.path.join(tmp, "bad.sav")
    write(path, party_save(6))
    w = W.Watcher()
    w.set_path(path)
    w.check()
    time.sleep(1.1)
    write(path, bytes(0x80000))
    w.check()
    snap = w.snapshot()
    results.append(("a file that stops being a readable save keeps the last good one and "
                    "reports why", snap["save"] is not None and snap["seq"] == 1
                    and "normal block" in (snap["error"] or ""), snap["error"] or ""))

    # The routes, on a live server, with the path in the temporary settings.
    path = os.path.join(tmp, "route.sav")
    write(path, party_save(6))
    httpd = server.Server(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
        W.WATCHER.set_path("")
        conn.request("GET", "/api/save/packed")
        r0 = conn.getresponse()
        r0.read()
        conn.request("POST", "/api/save/path", json.dumps({"path": path}),
                     {"Content-Type": "application/json"})
        r1 = conn.getresponse()
        state = json.loads(r1.read())
        conn.request("GET", "/api/save/packed")
        r2 = conn.getresponse()
        body = r2.read()
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    stored = json.load(open(os.environ["OXIDEX_SETTINGS"]))
    results.append(("/api/save/packed is 404 with no save; POST /api/save/path watches one "
                    "and remembers it in the settings; then the packed save is served",
                    r0.status == 404 and r1.status == 200 and (state.get("save") or {}).get("party_count") == 1
                    and stored.get("save_path") == path and r2.status == 200
                    and body == S.packed(open(path, "rb").read()),
                    f"{r0.status}, {r1.status}, {r2.status}"))
    results.append(("the settings live outside the repository unless a test says otherwise",
                    W.settings_path() == os.environ["OXIDEX_SETTINGS"]
                    and not _default_in_repo(), ""))

    # The calculator's side: Sync reads the bridge under the Oxide title.
    calc = os.path.join(S.model.repo_root(), "tools", "oxide", "encounters", "calc")
    read = lambda *p: open(os.path.join(calc, *p), encoding="utf-8").read()
    results.append(("the calculator's Sync reads the bridge under the Oxide title, and polls it "
                    "(VENDORED.md patch 16)",
                    '"/api/save/packed"' in read("js", "moveset_import.js")
                    and 'TITLE == "Platinum Oxide"' in read("js", "calc_ui", "menu_settings.js")
                    and "/api/save" in read("js", "oxide", "save_sync.js")
                    and 'src="./js/oxide/save_sync.js"' in read("index.html"), ""))

    shutil.rmtree(tmp, ignore_errors=True)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


def _default_in_repo():
    saved = os.environ.pop("OXIDEX_SETTINGS")
    try:
        return os.path.abspath(W.settings_path()).startswith(os.path.abspath(S.model.repo_root()))
    finally:
        os.environ["OXIDEX_SETTINGS"] = saved


if __name__ == "__main__":
    sys.exit(main())
