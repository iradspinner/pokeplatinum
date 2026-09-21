#!/usr/bin/env python3
"""Hold one GDB-stub session open against a running melonDS and log breakpoint hits.

Platinum Oxide. Written for the Windows melonDS 1.1 build, whose stub differs
from the Linux one in two ways that decide how it can be used (measured
2026-09-21): it takes exactly one client per emulator session and does not
recover from a dropped one, and it only services the socket while the CPU is
stopped, so a running target cannot be interrupted on demand. What does work is
connecting while the emulator is held at its startup break ("Break on startup"
in the Devtools tab), planting breakpoints, continuing, and being told when
one fires. This script does that and keeps the connection for its whole life.

    PYTHONPATH=. python3 tools/oxide/live_watch.py [--nef build/main.nef] [--log FILE]
                                                   [--every N] SYMBOL_OR_ADDR ...

Start melonDS with the stub on 3333 and break-on-startup, load the ROM, then run
this. It connects, plants a hardware breakpoint on every symbol given (default:
the whiteout task, the two script commands the Route 202 hang points at), sends
`c`, and then blocks. Every stop is logged with its time, pc, the symbol at pc,
r0-r3 and lr, and the target is continued again. A breakpoint that fires every
frame (ScrCmd_WaitMovement while a script waits) is logged on its first hits and
then every N-th, so the log stays readable and the game stays playable. Create
the file named by --stop-file to make it detach cleanly; killing it also works,
the emulator just loses its stub for that session.

Reads only. It never writes memory and never sets a breakpoint it was not given.
"""
import argparse
import os
import socket
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import live  # noqa: E402  (tools/oxide/live.py: GdbStub, Symbols)

DEFAULT_SYMBOLS = ["FieldTask_BlackOutFromBattle", "ScrCmd_BlackOutFromBattle",
                   "ScrCmd_ApplyMovement", "ScrCmd_WaitMovement"]


def connect_at_break(host, port, timeout):
    """A GdbStub without its constructor's halt(): the target is already stopped
    at the startup break and the Windows stub does not answer an interrupt."""
    stub = live.GdbStub.__new__(live.GdbStub)
    stub.sock = socket.create_connection((host, port), timeout=timeout)
    stub.sock.settimeout(timeout)
    stub.running = False
    stub.no_ack = False
    stub._buf = b""
    stub.sock.sendall(b"+")
    stub._expect_ack()
    reason = stub.cmd("?").decode()
    return stub, reason


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("symbols", nargs="*", default=DEFAULT_SYMBOLS,
                    help="function names (resolved in --nef) or hex addresses")
    ap.add_argument("--nef", default="build/main.nef")
    ap.add_argument("--log", default=os.path.expanduser("~/roms/live-watch.log"))
    ap.add_argument("--stop-file", default=os.path.expanduser("~/roms/live-watch.stop"))
    ap.add_argument("--every", type=int, default=120,
                    help="after the first 5 hits of one breakpoint, log every N-th")
    ap.add_argument("--hold-at", default=None, metavar="SYMBOL:N",
                    help="after the N-th hit of SYMBOL stay halted and serve commands "
                         "from --cmd-file (bp NAME|ADDR, rm NAME|ADDR, regs, read ADDR LEN, "
                         "sym ADDR, step, c, detach); each result is appended to the log")
    ap.add_argument("--hold-burst", default=None, metavar="SYMBOL:K",
                    help="hold when SYMBOL fires K times within two seconds: the shape of a "
                         "state machine spinning every frame, as opposed to a normal map load")
    ap.add_argument("--auto", action="append", default=[], metavar="CMD",
                    help="a command to run at every hold before continuing automatically; "
                         "may repeat. Addresses may be REG+HEX, e.g. 'read r0+0x18 4'. "
                         "'steps N' single-steps N times naming each pc")
    ap.add_argument("--arm-on", default=None, metavar="SYMBOL",
                    help="holds (--hold-at, --hold-burst) stay disarmed until SYMBOL fires; "
                         "--hold-at's count restarts at that moment")
    ap.add_argument("--plant-on-arm", default="", metavar="SYM,SYM,...",
                    help="breakpoints planted only once --arm-on fires, so they cost nothing "
                         "during play; logged on every hit (a per-frame stage trail)")
    ap.add_argument("--sections", default="main,overlay5,overlay6,overlay7",
                    help="comma list of ELF sections whose symbols may name a pc; several "
                         "overlays share addresses, so the ones not loaded must be excluded")
    ap.add_argument("--cmd-file", default=os.path.expanduser("~/roms/live-watch.cmd"))
    ap.add_argument("--host", default=live.STUB_HOST)
    ap.add_argument("--port", type=int, default=live.STUB_PORT)
    a = ap.parse_args()

    syms = live.Symbols(a.nef)
    wanted = set(a.sections.split(","))

    def name_pc(pc):
        """The function holding pc, restricted to the sections that are loaded."""
        hits = [(n, off, sec) for n, off, sec in syms.containing(pc, code_only=True) if sec in wanted]
        return " | ".join("%s+0x%x (%s)" % h for h in hits) or "0x%08x" % pc
    targets = {}
    for s in a.symbols:
        addr = int(s, 16) if s.lower().startswith("0x") else syms.addr(s)
        targets[addr] = s
    log = open(a.log, "a", buffering=1)

    def say(msg):
        line = "%s %s" % (time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        log.write(line + "\n")

    try:
        stub, reason = connect_at_break(a.host, a.port, timeout=10.0)
    except (OSError, RuntimeError) as e:
        say("connect failed: %s (is melonDS at its startup break with the stub on?)" % e)
        return 1
    say("connected, stop reason %s" % reason)
    for addr, name in targets.items():
        say("breakpoint %s at 0x%08x -> %s" % (name, addr, stub.breakpoint(addr)))
    hits = {addr: 0 for addr in targets}
    hold_addr, hold_n = None, 0
    if a.hold_at:
        s, n = a.hold_at.rsplit(":", 1)
        hold_addr = int(s, 16) if s.lower().startswith("0x") else syms.addr(s)
        hold_n = int(n)
        targets.setdefault(hold_addr, s)
        if hold_addr not in hits:
            say("breakpoint %s at 0x%08x -> %s" % (s, hold_addr, stub.breakpoint(hold_addr)))
            hits[hold_addr] = 0

    burst_addr, burst_k, burst_times = None, 0, []
    if a.hold_burst:
        s, k = a.hold_burst.rsplit(":", 1)
        burst_addr = int(s, 16) if s.lower().startswith("0x") else syms.addr(s)
        burst_k = int(k)
        if burst_addr not in hits:
            targets[burst_addr] = s
            say("breakpoint %s at 0x%08x -> %s" % (s, burst_addr, stub.breakpoint(burst_addr)))
            hits[burst_addr] = 0

    def resolve(s, regs=None):
        base, _, off = s.partition("+")
        if regs and base in regs:
            v = regs[base]
        elif base.lower().startswith("0x"):
            v = int(base, 16)
        else:
            v = syms.addr(base)
        return v + (int(off, 0) if off else 0)

    def run_one(cmd, regs):
        parts = cmd.split()
        if parts[0] == "bp":
            addr = resolve(parts[1], regs); targets[addr] = parts[1]; hits.setdefault(addr, 0)
            say("> %s -> %s" % (cmd, stub.breakpoint(addr)))
        elif parts[0] == "rm":
            addr = resolve(parts[1], regs); say("> %s -> %s" % (cmd, stub.remove_breakpoint(addr)))
        elif parts[0] == "regs":
            say("> regs " + " ".join("%s=%08x" % kv for kv in regs.items()))
        elif parts[0] == "read":
            addr = resolve(parts[1], regs); ln = int(parts[2], 0)
            say("> read 0x%08x %d: %s" % (addr, ln, stub.read(addr, ln).hex()))
        elif parts[0] == "peek":
            # peek EXPR LEN: EXPR may nest dereferences, e.g. [[sApplication+4]+0x18]+0x10
            def ev(e):
                e = e.strip()
                while "[" in e:
                    i = e.rfind("["); j = e.find("]", i)
                    inner = ev(e[i + 1:j]); e = e[:i] + ("0x%x" % stub.read_u32(inner)) + e[j + 1:]
                total = 0
                for term in e.replace("-", "+-").split("+"):
                    if not term:
                        continue
                    neg = term.startswith("-"); term = term.lstrip("-")
                    v = regs[term] if term in regs else (int(term, 0) if term[:2].lower() == "0x" or term.isdigit() else syms.addr(term))
                    total += -v if neg else v
                return total & 0xFFFFFFFF
            addr = ev(parts[1]); ln = int(parts[2], 0)
            data = stub.read(addr, ln) if 0x02000000 <= addr < 0x02400000 else b""
            words = " ".join("%08x" % int.from_bytes(data[i:i + 4], "little") for i in range(0, len(data) - 3, 4))
            names = [syms.describe(int.from_bytes(data[i:i + 4], "little"), code_only=True) for i in range(0, len(data) - 3, 4)]
            names = [n.split(" | ")[0] for n in names if n]
            say("> peek %s = 0x%08x: %s%s" % (parts[1], addr, words or "(not RAM)", ("   fns: " + "; ".join(names)) if names else ""))
        elif parts[0] == "readptr":
            # readptr BASE OFF LEN: follow the pointer stored at BASE+OFF, dump LEN bytes there
            base = resolve(parts[1], regs) + int(parts[2], 0)
            ptr = stub.read_u32(base); ln = int(parts[3], 0)
            say("> readptr [0x%08x] = 0x%08x -> %s" % (base, ptr, stub.read(ptr, ln).hex() if 0x02000000 <= ptr < 0x02400000 else "(not a RAM pointer)"))
        elif parts[0] == "sym":
            say("> sym %s -> %s" % (parts[1], syms.describe(resolve(parts[1], regs))))
        elif parts[0] == "step":
            say("> step -> %s" % stub.step())
        elif parts[0] == "trace":
            # single-step N times but log only when the enclosing function changes,
            # so a long stretch reads as a call trace rather than an instruction dump
            last = None
            for i in range(int(parts[1])):
                stub.step()
                pc = stub.reg("pc")
                fn = name_pc(pc).split("+")[0]
                if fn != last:
                    say("> trace %d: pc=%08x %s" % (i + 1, pc, fn))
                    last = fn
            say("> trace ended at pc=%08x %s" % (pc, name_pc(pc)))
        elif parts[0] == "steps":
            for i in range(int(parts[1])):
                stub.step()
                pc = stub.reg("pc")
                say("> step %d: pc=%08x %s" % (i + 1, pc, name_pc(pc)))
        else:
            say("> unknown command: %s" % cmd)

    def serve_commands():
        """Target is halted. Read command lines from the cmd file until 'c' or 'detach'.
        Returns 'c' to continue holding on the next stop, 'go' to stop holding, 'detach'."""
        regs = stub.regs()
        for cmd in a.auto:
            try:
                run_one(cmd, regs)
            except Exception as e:
                say("> %s -> error %s" % (cmd, e))
        if a.auto:
            return "c"
        say("HELD: target stopped, waiting for commands in %s" % a.cmd_file)
        done = 0
        while True:
            lines = []
            if os.path.exists(a.cmd_file):
                with open(a.cmd_file) as fh:
                    lines = [l.strip() for l in fh if l.strip()]
            if len(lines) <= done:
                time.sleep(0.5)
                continue
            for cmd in lines[done:]:
                done += 1
                parts = cmd.split()
                try:
                    if parts[0] == "c":
                        say("> c"); return "c"
                    elif parts[0] == "go":
                        say("> go (no more holds)"); return "go"
                    elif parts[0] == "detach":
                        return "detach"
                    else:
                        run_one(cmd, stub.regs())
                except Exception as e:  # keep serving; a typo must not lose the session
                    say("> %s -> error %s" % (cmd, e))

    verbose = set()  # breakpoints logged on every hit, whatever --every says
    arm_addr = None
    if a.arm_on:
        arm_addr = resolve(a.arm_on)
        if arm_addr not in hits:
            targets[arm_addr] = a.arm_on
            say("breakpoint %s at 0x%08x -> %s (arms the holds)" % (a.arm_on, arm_addr, stub.breakpoint(arm_addr)))
            hits[arm_addr] = 0
    armed = arm_addr is None
    since_arm = {}
    stub.cont()
    say("continued; play. stop file: %s" % a.stop_file)

    while True:
        if os.path.exists(a.stop_file):
            os.remove(a.stop_file)
            say("stop file seen, detaching (the emulator keeps running)")
            break
        try:
            reason = stub.wait_stop(timeout=1.0)
        except socket.timeout:
            continue
        except (ConnectionError, RuntimeError) as e:
            say("connection lost: %s" % e)
            break
        regs = stub.regs()
        pc = regs.get("pc", regs.get("r15", 0))
        # a Z1 stop reports pc at the breakpoint; name it from the symbol table
        name = targets.get(pc) or name_pc(pc)
        hits[pc] = hits.get(pc, 0) + 1
        n = hits[pc]
        if n <= 5 or n % a.every == 0 or pc in verbose:
            say("stop %s hit#%d at %s r0=%08x r1=%08x r2=%08x r3=%08x lr=%08x"
                % (reason, n, name, regs.get("r0", 0), regs.get("r1", 0),
                   regs.get("r2", 0), regs.get("r3", 0), regs.get("lr", regs.get("r14", 0))))
        if not armed and pc == arm_addr:
            armed = True
            say("ARMED by %s; holds are live from here" % targets[pc])
            for s in [x for x in a.plant_on_arm.split(",") if x]:
                addr = resolve(s); targets[addr] = s; hits[addr] = 0; verbose.add(addr)
                say("breakpoint %s at 0x%08x -> %s (planted on arm)" % (s, addr, stub.breakpoint(addr)))
        if armed:
            since_arm[pc] = since_arm.get(pc, 0) + 1
        if not armed:
            stub.cont()
            continue
        n = since_arm[pc] if arm_addr is not None else n
        if burst_addr is not None and pc == burst_addr:
            now = time.time()
            burst_times = [x for x in burst_times if now - x < 2.0] + [now]
            if len(burst_times) >= burst_k:
                say("BURST: %s fired %d times in two seconds" % (targets[pc], len(burst_times)))
                burst_addr = None
                verdict = serve_commands()
                if verdict == "detach":
                    say("detaching (the emulator keeps running)"); stub.cont(); break
                if verdict == "c":
                    hold_addr, hold_n = pc, 0  # keep holding on every later hit
        if hold_addr is not None and pc == hold_addr and n >= hold_n:
            verdict = serve_commands()
            if verdict == "detach":
                say("detaching (the emulator keeps running)"); stub.cont(); break
            if verdict == "go":
                hold_addr = None
        stub.cont()
    return 0


if __name__ == "__main__":
    sys.exit(main())
