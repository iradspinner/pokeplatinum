#!/usr/bin/env python3
"""Drive a live melonDS from Python: launch it, look at its window, press
buttons, and talk to its GDB stub without needing GDB itself.

Written for the Platinum Oxide whiteout-hang reproduction, but nothing here is
Platinum-specific: it works for any NDS ROM and any ELF with symbols, so it can
be lifted into another project as-is.

Pieces (each usable on its own):

  MelonDS   launch or attach to a melonDS window under WSLg (X11 via python-xlib),
            capture the window to a PNG, press DS buttons with XTest key events,
            close it cleanly so it writes its config and save.
  GdbStub   a minimal GDB remote-serial-protocol client for melonDS's stub
            (port 3333 = ARM9, 3334 = ARM7): halt, continue, step, registers,
            read/write memory, hardware breakpoints and watchpoints.
  Symbols   read the symbol table out of an ELF (the build's main.nef) so an
            address can be named and a name can be located, with no external tool.

Command line (see --help): launch, attach, shot, press, halt, cont, regs, read,
bt-ish "where", sym, close, kill.

Environment, all optional:
  OXIDE_MELONDS_DIR   directory holding squashfs-root/ (the extracted AppImage)
                      and extlib/ (locally unpacked .debs); default ~/tools/melonds
  OXIDE_MELONDS_HOST  host of the GDB stub, default 127.0.0.1
  OXIDE_MELONDS_PORT  port of the ARM9 stub, default 3333
  DISPLAY             the X display (WSLg gives :0)

The recipe that makes all of this work in WSL2 without sudo is in
docs/oxide/setup-fork-and-wsl2.md, part 5.
"""

import argparse
import os
import socket
import struct
import subprocess
import sys
import time

# ---------------------------------------------------------------------------
# melonDS process and window
# ---------------------------------------------------------------------------

MELONDS_DIR = os.path.expanduser(os.environ.get("OXIDE_MELONDS_DIR", "~/tools/melonds"))
STUB_HOST = os.environ.get("OXIDE_MELONDS_HOST", "127.0.0.1")
STUB_PORT = int(os.environ.get("OXIDE_MELONDS_PORT", "3333"))

# DS button -> X keysym. These must match [Instance0.Keyboard] in
# ~/.config/melonDS/melonDS.toml (Qt key codes: X=0x58 Z=0x5a S=0x53 A=0x41
# Q=0x51 W=0x57 Return=0x01000004 Backspace=0x01000003 Up=0x01000013
# Down=0x01000015 Left=0x01000012 Right=0x01000014).
BUTTON_KEYSYM = {
    "A": "x", "B": "z", "X": "s", "Y": "a", "L": "q", "R": "w",
    "START": "Return", "SELECT": "BackSpace",
    "UP": "Up", "DOWN": "Down", "LEFT": "Left", "RIGHT": "Right",
}


class MelonDS:
    """One melonDS window. Either launch() a new one or attach() to a running one."""

    def __init__(self):
        from Xlib import display  # imported lazily so GdbStub works without X
        self.display = display.Display()
        self.window = None
        self.proc = None

    # -- process ------------------------------------------------------------

    @staticmethod
    def env():
        e = dict(os.environ)
        extlib = os.path.join(MELONDS_DIR, "extlib", "usr", "lib", "x86_64-linux-gnu")
        e["LD_LIBRARY_PATH"] = extlib + (":" + e["LD_LIBRARY_PATH"] if e.get("LD_LIBRARY_PATH") else "")
        e["QT_QPA_PLATFORM"] = "xcb"  # the AppImage has no wayland plugin; WSLg's X11 works
        return e

    def launch(self, rom, log=None, wait=8.0):
        """Start melonDS on `rom` (its .sav sits beside it) and attach to the window.

        `log` captures melonDS's stdout. Leave it off unless you are diagnosing a
        launch: the stub logs one line per CPU poll once a client has gone away
        without detaching, and that filled 12 GB in a few minutes here."""
        exe = os.path.join(MELONDS_DIR, "squashfs-root", "AppRun")
        out = open(log, "w") if log else subprocess.DEVNULL
        self.proc = subprocess.Popen([exe, os.path.abspath(rom)], cwd=MELONDS_DIR, env=self.env(),
                                     stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                     start_new_session=True)
        deadline = time.time() + wait
        while time.time() < deadline:
            if self.attach(quiet=True):
                return self
            time.sleep(0.5)
        raise RuntimeError("melonDS window did not appear; see %s" % (log or "its stdout"))

    def attach(self, quiet=False):
        """Find the running melonDS main window (title 'melonDS ...', class AppRun/melonDS)."""
        for w in self._windows(self.display.screen().root):
            try:
                name = w.get_wm_name() or ""
                cls = w.get_wm_class() or ("", "")
            except Exception:
                continue
            if "melonDS" in name and cls[0] in ("AppRun", "melonDS"):
                self.window = w
                return self
        if not quiet:
            raise RuntimeError("no melonDS window on %s" % os.environ.get("DISPLAY"))
        return None

    def _windows(self, w):
        try:
            for c in w.query_tree().children:
                yield c
                yield from self._windows(c)
        except Exception:
            return

    def title(self):
        return self.window.get_wm_name()

    def close(self):
        """Ask the window to close (WM_DELETE_WINDOW). melonDS then writes its .sav and config."""
        from Xlib import X, protocol
        wm_protocols = self.display.intern_atom("WM_PROTOCOLS")
        wm_delete = self.display.intern_atom("WM_DELETE_WINDOW")
        ev = protocol.event.ClientMessage(window=self.window, client_type=wm_protocols,
                                          data=(32, [wm_delete, X.CurrentTime, 0, 0, 0]))
        self.window.send_event(ev, event_mask=0)
        self.display.flush()

    @staticmethod
    def kill_all():
        # By process name, not -f: the AppImage runs as "AppRun", and a -f pattern
        # would also match the shell that is running this command.
        subprocess.run(["pkill", "-9", "-x", "AppRun"], check=False)

    # -- screen ---------------------------------------------------------------

    def screenshot(self, path=None):
        """Grab the window's pixels (works under rootless Xwayland where the root is black)."""
        from Xlib import X
        from PIL import Image
        g = self.window.get_geometry()
        raw = self.window.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xFFFFFFFF)
        im = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
        if path:
            im.save(path)
        return im

    def screens(self, path_top=None, path_bottom=None, menu_height=19):
        """Split the capture into the two DS screens (default layout, 256 wide)."""
        im = self.screenshot()
        top = im.crop((0, menu_height, 256, menu_height + 192))
        bottom = im.crop((0, menu_height + 192, 256, menu_height + 384))
        if path_top:
            top.save(path_top)
        if path_bottom:
            bottom.save(path_bottom)
        return top, bottom

    # -- input ----------------------------------------------------------------

    def focus(self):
        from Xlib import X
        self.window.set_input_focus(X.RevertToParent, X.CurrentTime)
        self.display.sync()

    def _keycode(self, button):
        from Xlib import XK
        sym = XK.string_to_keysym(BUTTON_KEYSYM[button.upper()])
        return self.display.keysym_to_keycode(sym)

    def hold(self, *buttons):
        from Xlib import X
        from Xlib.ext import xtest
        self.focus()
        for b in buttons:
            xtest.fake_input(self.display, X.KeyPress, self._keycode(b))
        self.display.sync()

    def release(self, *buttons):
        from Xlib import X
        from Xlib.ext import xtest
        for b in buttons:
            xtest.fake_input(self.display, X.KeyRelease, self._keycode(b))
        self.display.sync()

    def press(self, *buttons, hold=0.08, gap=0.12):
        """Tap each button in turn. `hold` is how long it stays down (seconds; a DS
        frame is 1/60 s, and the game polls once a frame), `gap` the pause after."""
        for b in buttons:
            self.hold(b)
            time.sleep(hold)
            self.release(b)
            time.sleep(gap)

    def walk(self, direction, steps, step_time=0.27):
        """Hold a direction long enough to walk `steps` tiles (walking is 16 frames a tile)."""
        self.hold(direction)
        time.sleep(step_time * steps)
        self.release(direction)


# ---------------------------------------------------------------------------
# GDB remote serial protocol client for the melonDS stub
# ---------------------------------------------------------------------------

REG_NAMES = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12",
             "sp", "lr", "pc", "cpsr"]


class GdbStub:
    """Talks to melonDS's GDB stub directly. One client at a time; close GDB first.

    While the target runs, the stub only listens for a 0x03 interrupt, so every
    method that needs the target stopped calls halt() first. cont() returns
    immediately; wait_stop() blocks for the next stop packet (breakpoint hit,
    watchpoint, or an interrupt)."""

    def __init__(self, host=STUB_HOST, port=STUB_PORT, timeout=5.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.running = True  # melonDS starts the ROM running; the stub reports 'running' until halted
        self.no_ack = False
        self._buf = b""
        # melonDS's handshake: the client must send a bare '+' within a second of
        # connecting, and the stub answers with its own '+'. Without it the stub
        # drops the connection.
        self.sock.sendall(b"+")
        self._expect_ack()
        # Halt right away so every method that follows has a stopped target.
        self.halt()

    # -- packet layer -----------------------------------------------------------

    @staticmethod
    def _csum(data):
        return sum(data) & 0xFF

    def _send(self, payload):
        pkt = b"$" + payload + b"#" + b"%02x" % self._csum(payload)
        self.sock.sendall(pkt)
        if not self.no_ack:
            self._expect_ack()

    def _expect_ack(self):
        while True:
            c = self._recv_byte()
            if c == b"+":
                return
            if c == b"-":
                raise RuntimeError("stub NAKed a packet")

    def _recv_byte(self):
        if not self._buf:
            self._buf = self.sock.recv(4096)
            if not self._buf:
                raise ConnectionError("stub closed the connection")
        c, self._buf = self._buf[:1], self._buf[1:]
        return c

    def _recv_packet(self, timeout=None):
        old = self.sock.gettimeout()
        if timeout is not None:
            self.sock.settimeout(timeout)
        try:
            while self._recv_byte() != b"$":
                pass
            data = b""
            while True:
                c = self._recv_byte()
                if c == b"#":
                    break
                data += c
            csum = self._recv_byte() + self._recv_byte()
            if int(csum, 16) != self._csum(data):
                self.sock.sendall(b"-")
                raise RuntimeError("bad checksum from stub")
            if not self.no_ack:
                self.sock.sendall(b"+")
            return data
        finally:
            self.sock.settimeout(old)

    def cmd(self, payload, timeout=None):
        """Send one packet and return the reply payload (bytes)."""
        if isinstance(payload, str):
            payload = payload.encode()
        self._send(payload)
        return self._recv_packet(timeout)

    # -- execution control ----------------------------------------------------

    def halt(self):
        """Stop the target if it is running; return the stop reason (e.g. 'T05...')."""
        if self.running:
            self.sock.sendall(b"\x03")
            reply = self._recv_packet()
            self.running = False
            return reply.decode()
        return self.cmd("?").decode()

    def cont(self):
        """Resume. Returns at once; call wait_stop() to block until the next stop."""
        self._send(b"c")
        self.running = True

    def wait_stop(self, timeout=None):
        """Block until the target stops (breakpoint, watchpoint, or halt())."""
        reply = self._recv_packet(timeout)
        self.running = False
        return reply.decode()

    def run_until_stop(self, timeout=None):
        self.cont()
        return self.wait_stop(timeout)

    def step(self):
        reply = self.cmd("s")
        return reply.decode()

    # -- registers --------------------------------------------------------------

    def regs(self):
        """All registers as a dict {name: int}; index 16 is cpsr, banked ones follow."""
        data = self.cmd("g").decode()
        words = [struct.unpack("<I", bytes.fromhex(data[i:i + 8]))[0] for i in range(0, len(data), 8)]
        out = {}
        for i, v in enumerate(words):
            out[REG_NAMES[i] if i < len(REG_NAMES) else "reg%d" % i] = v
        return out

    def reg(self, name):
        return self.regs()[name]

    def set_reg(self, index, value):
        return self.cmd("P%x=%s" % (index, struct.pack("<I", value).hex())).decode()

    # -- memory -----------------------------------------------------------------

    def read(self, addr, length):
        out = b""
        while length:
            n = min(length, 0x200)
            reply = self.cmd("m%x,%x" % (addr, n))
            if reply.startswith(b"E"):
                raise RuntimeError("read %08x,%x failed: %s" % (addr, n, reply.decode()))
            chunk = bytes.fromhex(reply.decode())
            out += chunk
            addr += len(chunk)
            length -= len(chunk)
        return out

    def read_u32(self, addr):
        return struct.unpack("<I", self.read(addr, 4))[0]

    def read_u16(self, addr):
        return struct.unpack("<H", self.read(addr, 2))[0]

    def read_u8(self, addr):
        return self.read(addr, 1)[0]

    def write(self, addr, data):
        reply = self.cmd("M%x,%x:%s" % (addr, len(data), data.hex()))
        if reply != b"OK":
            raise RuntimeError("write %08x failed: %s" % (addr, reply.decode()))

    def write_u32(self, addr, value):
        self.write(addr, struct.pack("<I", value))

    def write_u16(self, addr, value):
        self.write(addr, struct.pack("<H", value))

    def write_u8(self, addr, value):
        self.write(addr, bytes([value & 0xFF]))

    # -- breakpoints ------------------------------------------------------------
    # melonDS turns every Z0/Z1 into an address compare in the CPU loop, so
    # `kind` (2 thumb, 4 arm) only needs to be non-zero.

    def breakpoint(self, addr, kind=4):
        return self.cmd("Z1,%x,%d" % (addr, kind)).decode()

    def remove_breakpoint(self, addr, kind=4):
        return self.cmd("z1,%x,%d" % (addr, kind)).decode()

    def watchpoint(self, addr, length=4, mode="write"):
        typ = {"write": 2, "read": 3, "access": 4}[mode]
        return self.cmd("Z%d,%x,%d" % (typ, addr, length)).decode()

    def remove_watchpoint(self, addr, length=4, mode="write"):
        typ = {"write": 2, "read": 3, "access": 4}[mode]
        return self.cmd("z%d,%x,%d" % (typ, addr, length)).decode()

    def detach(self):
        """Always detach before closing the socket. The stub does not notice a
        closed client (recv() returning 0 is treated as 'no packet yet') and spins
        logging a line per poll; 'D' makes it drop the connection and resume."""
        try:
            self.sock.sendall(b"$D#44")
            try:
                self._recv_packet(timeout=1.0)
            except (TimeoutError, OSError, RuntimeError):
                pass
        finally:
            self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.detach()

    # -- convenience --------------------------------------------------------------

    def where(self, symbols=None, depth=12):
        """Registers plus a crude stack scan: every word on the stack that looks like a
        return address into the ARM9 binary or an overlay, named if `symbols` is given.
        Not a real unwinder (Metrowerks output has no frame pointers), but it is
        enough to see who called whom."""
        r = self.regs()
        lines = ["pc=%08x lr=%08x sp=%08x cpsr=%08x%s" % (
            r["pc"], r["lr"], r["sp"], r["cpsr"], " (thumb)" if r["cpsr"] & 0x20 else "")]
        for name in ("pc", "lr"):
            if symbols:
                lines.append("  %s %s" % (name, symbols.describe(r[name])))
        words = self.read(r["sp"], 4 * 64)
        found = 0
        for i in range(0, len(words), 4):
            v = struct.unpack("<I", words[i:i + 4])[0]
            if 0x02000000 <= v < 0x02400000 and symbols and symbols.describe(v, code_only=True):
                lines.append("  [sp+%03x] %08x %s" % (i, v, symbols.describe(v, code_only=True)))
                found += 1
                if found >= depth:
                    break
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# ELF symbols (no external tools)
# ---------------------------------------------------------------------------

class Symbols:
    """Function and object symbols from an ELF32 file (the decomp's build/main.nef).

    Overlays share address ranges, so an address can match a symbol in several
    sections; describe() lists them all with their section, and the caller uses
    the game's overlay table (or context) to pick. Section names in main.nef are
    like '.text' for the static ARM9 binary and 'overlay16' for overlay 16."""

    def __init__(self, path):
        self.path = path
        self.funcs = []   # (addr, size, name, section)
        self.objects = []
        self._load()

    def _load(self):
        with open(self.path, "rb") as f:
            data = f.read()
        if data[:4] != b"\x7fELF" or data[4] != 1:
            raise ValueError("not an ELF32 file: %s" % self.path)
        e_shoff = struct.unpack_from("<I", data, 0x20)[0]
        e_shentsize, e_shnum, e_shstrndx = struct.unpack_from("<HHH", data, 0x2E)
        sections = []
        for i in range(e_shnum):
            off = e_shoff + i * e_shentsize
            sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = \
                struct.unpack_from("<IIIIIIIIII", data, off)
            sections.append((sh_name, sh_type, sh_addr, sh_offset, sh_size, sh_link, sh_entsize))
        shstr = sections[e_shstrndx]
        names = [self._cstr(data, shstr[3] + s[0]) for s in sections]
        self.sections = names
        for idx, s in enumerate(sections):
            if s[1] != 2:  # SHT_SYMTAB
                continue
            strtab = sections[s[5]]
            for off in range(s[3], s[3] + s[4], 16):
                st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack_from("<IIIBBH", data, off)
                typ = st_info & 0xF
                if st_shndx == 0 or st_shndx >= len(names):
                    continue
                name = self._cstr(data, strtab[3] + st_name)
                if not name:
                    continue
                entry = (st_value & ~1, st_size, name, names[st_shndx])
                if typ == 2:
                    self.funcs.append(entry)
                elif typ == 1:
                    self.objects.append(entry)
        self.funcs.sort()
        self.objects.sort()

    @staticmethod
    def _cstr(data, off):
        end = data.index(b"\0", off)
        return data[off:end].decode("latin-1")

    def lookup(self, name):
        """All (addr, size, section) for a symbol name (a function or a global)."""
        out = [(a, s, sec) for a, sz, n, sec in self.funcs if n == name for s in [sz]]
        out += [(a, s, sec) for a, sz, n, sec in self.objects if n == name for s in [sz]]
        return out

    def addr(self, name):
        hits = self.lookup(name)
        if not hits:
            raise KeyError(name)
        return hits[0][0]

    def containing(self, addr, code_only=False):
        """Every symbol whose [addr, addr+size) holds `addr` (size 0 counts as 4)."""
        hits = []
        for table in ((self.funcs,) if code_only else (self.funcs, self.objects)):
            for a, sz, n, sec in table:
                if a <= addr < a + max(sz, 4):
                    hits.append((n, addr - a, sec))
        return hits

    def describe(self, addr, code_only=False):
        hits = self.containing(addr, code_only)
        return " | ".join("%s+0x%x (%s)" % h for h in hits)


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("launch", help="start melonDS on a ROM (its .sav must sit beside it)")
    p.add_argument("rom")
    p.add_argument("--log", default=None)
    sub.add_parser("attach", help="check a melonDS window is up and print its title")
    p = sub.add_parser("shot", help="save the window (or the two DS screens) to PNG")
    p.add_argument("out")
    p.add_argument("--screens", action="store_true", help="write OUT-top.png and OUT-bottom.png instead")
    p = sub.add_parser("press", help="tap DS buttons in order, e.g. press A A START")
    p.add_argument("buttons", nargs="+")
    p.add_argument("--hold", type=float, default=0.08)
    p.add_argument("--gap", type=float, default=0.12)
    p = sub.add_parser("walk", help="hold a direction for N tiles")
    p.add_argument("direction")
    p.add_argument("steps", type=int)
    p = sub.add_parser("halt", help="stop the ARM9 and print where it is")
    p.add_argument("--nef", default=None, help="ELF with symbols (build/main.nef) to name addresses")
    sub.add_parser("cont", help="resume the ARM9 (after halt)")
    p = sub.add_parser("regs", help="print ARM9 registers (halts)")
    p = sub.add_parser("read", help="hex dump ARM9 memory (halts, then resumes)")
    p.add_argument("addr", type=lambda s: int(s, 0))
    p.add_argument("length", type=lambda s: int(s, 0), nargs="?", default=64)
    p = sub.add_parser("sym", help="look a symbol up in an ELF, or name an address")
    p.add_argument("nef")
    p.add_argument("what")
    sub.add_parser("close", help="close melonDS cleanly (writes save and config)")
    sub.add_parser("kill", help="kill every melonDS process")
    a = ap.parse_args(argv)

    if a.cmd == "launch":
        m = MelonDS().launch(a.rom, log=a.log)
        print("melonDS up:", m.title())
    elif a.cmd == "attach":
        print(MelonDS().attach().title())
    elif a.cmd == "shot":
        m = MelonDS().attach()
        if a.screens:
            base = a.out[:-4] if a.out.endswith(".png") else a.out
            m.screens(base + "-top.png", base + "-bottom.png")
            print(base + "-top.png", base + "-bottom.png")
        else:
            m.screenshot(a.out)
            print(a.out)
    elif a.cmd == "press":
        MelonDS().attach().press(*a.buttons, hold=a.hold, gap=a.gap)
    elif a.cmd == "walk":
        MelonDS().attach().walk(a.direction.upper(), a.steps)
    elif a.cmd == "halt":
        # Detaching resumes the target, so this is a snapshot of where it is, not a pause.
        with GdbStub() as g:
            syms = Symbols(a.nef) if a.nef else None
            print(g.where(syms))
    elif a.cmd == "cont":
        with GdbStub():
            pass
    elif a.cmd == "regs":
        with GdbStub() as g:
            for k, v in g.regs().items():
                print("%-6s %08x" % (k, v))
    elif a.cmd == "read":
        with GdbStub() as g:
            data = g.read(a.addr, a.length)
        for i in range(0, len(data), 16):
            print("%08x  %s" % (a.addr + i, data[i:i + 16].hex(" ")))
    elif a.cmd == "sym":
        s = Symbols(a.nef)
        try:
            addr = int(a.what, 0)
            print(s.describe(addr) or "no symbol")
        except ValueError:
            for addr_, size, sec in s.lookup(a.what):
                print("%08x size=%#x %s" % (addr_, size, sec))
    elif a.cmd == "close":
        MelonDS().attach().close()
    elif a.cmd == "kill":
        MelonDS.kill_all()


if __name__ == "__main__":
    main()
