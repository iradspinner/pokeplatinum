"""The Sync bridge: the OxiDex watches Ian's save file and hands its party and
boxes to the Calc tab (Ian's save plan, step 3, 2026-09-27).

The vendored calculator's Sync talks to a patched DeSmuME that serves game
memory over HTTP. Oxide is played on melonDS, which has no such thing, but it
writes the .sav whenever the player saves in game, so the OxiDex reads that
file and answers the same request (/api/save/packed, savefile.packed). What
Sync shows is the game as of the last in-game save.

The path is one setting, kept outside the repository, which is public, in
~/.config/oxidex/settings.json (OXIDEX_SETTINGS names another file, which the
tests use). It is set from the Calc tab's save bar or by editing that file. A
Windows path is taken as WSL sees it: G:\\PokeROMs\\x.sav is /mnt/g/PokeROMs/x.sav
and \\\\wsl.localhost\\Ubuntu\\home\\ian\\x.sav is /home/ian/x.sav.

The file is only ever read, whole, in one call; it is never written, locked
or held open. A save on the Linux filesystem is watched with inotify, which
sees a write through WSL's file server as it closes. A save under /mnt, a
Windows drive, is polled for its modification time every few seconds instead,
since inotify sees nothing written from the Windows side. Either way the file
is read once it has stopped changing for half a second, and a read that finds
no valid block keeps the last good save and reports why.
"""
import ctypes
import ctypes.util
import json
import os
import re
import select
import struct
import threading
import time

from . import savefile

POLL_SECONDS = 3            # a Windows drive, or the fallback when inotify is missing
SAFETY_SECONDS = 15         # a stat even under inotify, in case an event is missed
SETTLE_SECONDS = 0.5        # how long the file must stay unchanged before it is read
IN_MODIFY, IN_CLOSE_WRITE, IN_MOVED_TO, IN_CREATE = 0x2, 0x8, 0x80, 0x100
IN_NONBLOCK, IN_CLOEXEC = 0o4000, 0o2000000


def settings_path():
    return os.environ.get("OXIDEX_SETTINGS") or os.path.expanduser("~/.config/oxidex/settings.json")


def load_settings():
    try:
        with open(settings_path(), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_settings(settings):
    path = settings_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=1)
        f.write("\n")


def normalize(path):
    """A path as WSL sees it, from a Windows or a Linux spelling of it."""
    p = (path or "").strip().strip('"').strip("'")
    m = re.match(r"^\\\\wsl(?:\.localhost|\$)\\[^\\]+\\(.*)$", p, re.I)
    if m:
        return "/" + m.group(1).replace("\\", "/")
    m = re.match(r"^([A-Za-z]):[\\/](.*)$", p)
    if m:
        return f"/mnt/{m.group(1).lower()}/" + m.group(2).replace("\\", "/")
    return os.path.expanduser(p) if p else ""


def _inotify():
    """libc's inotify calls, or None where there are none."""
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
        libc.inotify_init1.argtypes = [ctypes.c_int]
        libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
        return libc
    except (OSError, AttributeError):
        return None


class Watcher:
    """One save file, watched on a thread of its own. `snapshot()` and
    `packed()` are what the server's routes read."""

    def __init__(self):
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._thread = None
        self._data = self._save = self._log = None
        self._seen = None                  # (mtime, size) of the last read
        self.state = {"path": None, "mode": None, "seq": 0, "mtime": None,
                      "read_at": None, "error": None}

    # -- what the routes use ----------------------------------------------------

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._run, daemon=True, name="savewatch")
            self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        self._wake.set()

    def set_path(self, path):
        """Remembers the save's path in the settings file and watches it."""
        path = normalize(path)
        settings = load_settings()
        settings["save_path"] = path
        save_settings(settings)
        with self._lock:
            self._data = self._save = self._seen = self._log = None
            self.state.update(path=path or None, mtime=None, read_at=None, error=None)
        self._wake.set()
        return path

    def current(self):
        """The last save read, parsed (savefile.parse), or None."""
        with self._lock:
            return self._save

    def snapshot(self):
        """{path, mode, seq, mtime, read_at, error, save summary or None}."""
        with self._lock:
            out = dict(self.state)
            out["save"] = savefile.summary(self._save) if self._save else None
            data = self._data
        if out["save"]:
            # How many battles the log holds, from its header alone, so the
            # calculator knows whether to ask for the log itself.
            from . import battlelog
            copy = battlelog.current(data)
            out["save"]["battle_log"] = {"count": copy["count"], "counter": copy["counter"]} if copy else None
        return out

    def raw(self):
        """(bytes, parsed save, seq, path) of the last save read, or Nones:
        the alpha checklist reads its ticks and its notes' stamps from it."""
        with self._lock:
            return self._data, self._save, self.state["seq"], self.state["path"]

    def packed(self):
        with self._lock:
            data = self._data
        return savefile.packed(data) if data else None

    def battle_log(self):
        """{seq, log, calc} for the last save read, or None: the battle log
        named (battlelog.read) and as the calculator's Battle Log payload.
        Worked out once per save read, since the calculator asks after every
        new save and names cost a file read per trainer."""
        from . import battlelog
        with self._lock:
            data, save, seq = self._data, self._save, self.state["seq"]
            cached = self._log if self._log and self._log["seq"] == seq else None
        if cached or not data:
            return cached
        log = battlelog.read(data, save)
        out = {"seq": seq, "log": log, "calc": battlelog.calc_payload(log, save)}
        with self._lock:
            if self.state["seq"] == seq:
                self._log = out
        return out

    def check(self):
        """Reads the file now if it changed since the last read. The thread
        calls it on every event and poll; a test can call it directly."""
        path = self.state["path"]
        if not path:
            return False
        try:
            st = os.stat(path)
        except OSError as exc:
            with self._lock:
                self.state["error"] = f"cannot see the save: {exc.strerror or exc}"
            return False
        if (st.st_mtime_ns, st.st_size) == self._seen:
            return False
        # Wait for the writer to finish: the same size and time twice running.
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            time.sleep(SETTLE_SECONDS)
            try:
                again = os.stat(path)
            except OSError:
                return False
            if (again.st_mtime_ns, again.st_size) == (st.st_mtime_ns, st.st_size):
                break
            st = again
        try:
            with open(path, "rb") as f:
                data = f.read()
            save = savefile.parse(data, path)
        except (OSError, savefile.SaveError) as exc:
            with self._lock:
                self._seen = (st.st_mtime_ns, st.st_size)
                self.state["error"] = str(exc)
            return False
        with self._lock:
            self._data, self._save = data, save
            self._seen = (st.st_mtime_ns, st.st_size)
            self.state.update(seq=self.state["seq"] + 1, mtime=st.st_mtime, read_at=time.time(),
                              error=None)
        return True

    # -- the thread -------------------------------------------------------------

    def _run(self):
        libc = _inotify()
        while not self._stop.is_set():
            self._wake.clear()
            path = normalize(load_settings().get("save_path") or "")
            with self._lock:
                if path != self.state["path"]:
                    self._data = self._save = self._seen = None
                self.state["path"] = path or None
            if not path:
                self.state["mode"] = None
                self._wake.wait(POLL_SECONDS)
                continue
            use_inotify = libc is not None and not path.startswith("/mnt/")
            self.state["mode"] = "inotify" if use_inotify else "polling"
            self.check()
            if use_inotify and self._watch_inotify(libc, path):
                continue
            self.state["mode"] = "polling"
            while not self._stop.is_set() and not self._wake.wait(POLL_SECONDS):
                self.check()

    def _watch_inotify(self, libc, path):
        """Watches the save's folder until the path changes or the watcher
        stops. False when inotify cannot watch it, so the caller polls."""
        fd = libc.inotify_init1(IN_NONBLOCK | IN_CLOEXEC)
        if fd < 0:
            return False
        try:
            folder = os.path.dirname(path) or "."
            mask = IN_MODIFY | IN_CLOSE_WRITE | IN_MOVED_TO | IN_CREATE
            if libc.inotify_add_watch(fd, folder.encode(), mask) < 0:
                return False
            name = os.path.basename(path).encode()
            last_safety = time.monotonic()
            while not self._stop.is_set() and not self._wake.is_set():
                ready, _, _ = select.select([fd], [], [], 1.0)
                hit = False
                if ready:
                    try:
                        buf = os.read(fd, 65536)
                    except BlockingIOError:
                        buf = b""
                    i = 0
                    while i + 16 <= len(buf):
                        _wd, _mask, _cookie, length = struct.unpack_from("iIII", buf, i)
                        if buf[i + 16:i + 16 + length].rstrip(b"\0") == name:
                            hit = True
                        i += 16 + length
                if hit or time.monotonic() - last_safety > SAFETY_SECONDS:
                    last_safety = time.monotonic()
                    self.check()
            return True
        finally:
            os.close(fd)


WATCHER = Watcher()
