#!/usr/bin/env python3
"""Check one carried-over map against the base ROM.

Platinum Oxide project. Once a map's events, script and text are written into
res/, this says whether the rebuilt ROM agrees with the base ROM.

Events are compared byte for byte. The script is compared command by command
rather than byte for byte, because removing a map's orphaned pick-event names
renumbers the message ids after them: that is a deliberate cleanup, so a message
id is allowed to differ as long as every occurrence remaps the same way and the
message it now points at reads the same as the base ROM's.

Usage:
    python3 tools/oxide/checkmap.py MAP
"""
import os, sys, importlib.util
MAP = sys.argv[1]
MAP = sys.argv[1]
sys.path.insert(0, "tools/oxide")
import scriptdis as sd
spec = importlib.util.spec_from_file_location("imp", "tools/oxide/import_base_rom.py")
m = importlib.util.module_from_spec(spec); sys.argv=["x"]; spec.loader.exec_module(m)
scripts = [l.strip() for l in open("res/field/scripts/scripts.order") if l.strip()]
events = [l.strip() for l in open("res/field/events/zone_event.order") if l.strip()]
banks = [l.strip() for l in open("generated/text_banks.txt") if l.strip()]
si, ei = scripts.index("scripts_"+MAP), events.index("events_"+MAP)
bi = banks.index("TEXT_BANK_"+MAP.upper())
built = m.Rom("build/pokeplatinum.us.nds"); base = m.Rom(os.path.expanduser("~/roms/base.nds"))
ok = True
ev_same = bytes(built.narc(m.EVENTS_NARC)[ei]) == bytes(base.narc(m.EVENTS_NARC)[ei])
print(f"events byte-identical: {ev_same}"); ok &= ev_same
def cmds(rom, br):
    sd.use_base_rom_table(br)
    d, l, h, mv = sd.walk(rom.narc(sd.SCRIPTS_NARC)[si])
    return [(d[o].cmd.macro, [(n, v) for _, n, v in d[o].values]) for o in sorted(d)]
cb, cr = cmds(built, False), cmds(base, True)
if len(cb) != len(cr):
    print(f"command count {len(cb)} vs {len(cr)}"); ok = False
else:
    mapping, bad = {}, 0
    for (mb, vb), (mr, vr) in zip(cb, cr):
        if mb != mr: bad += 1; print("  macro:", mb, "vs", mr); continue
        for (nb, xb), (nr, xr) in zip(vb, vr):
            if xb == xr: continue
            if nb in ("messageID", "entryStringID"):
                if mapping.setdefault(xr, xb) != xb: bad += 1; print(f"  inconsistent remap {xr}")
            else: bad += 1; print(f"  {mb}.{nb}: {xb} vs {xr}")
    print(f"script: {len(cb)} commands, {bad} mismatches, message remap {dict(sorted(mapping.items()))}")
    ok &= bad == 0
    T = os.environ["CLAUDE_JOB_DIR"]+"/tmp"
    tb = m.decode_text_bank("build/tools/msgenc/msgenc","tools/msgenc/charmap.txt",built.narc("msgdata/pl_msg.narc")[bi],T,"cb")
    rb = m.decode_text_bank("build/tools/msgenc/msgenc","tools/msgenc/charmap.txt",base.narc("msgdata/pl_msg.narc")[bi],T,"cr")
    print(f"text: built {len(tb)} vs base {len(rb)} messages")
    for o, n in mapping.items():
        if m.message_body(tb[n]) != m.message_body(rb[o]):
            print(f"  remapped message {o}->{n} differs!"); ok = False
    # every message id the script actually uses must read the same on both
    # sides, whether or not it was renumbered
    used = set()
    for mac, vals in cr:
        for n, v in vals:
            if n in ("messageID", "entryStringID"): used.add(v)
    checked = 0
    for o in sorted(used):
        n = mapping.get(o, o)
        if n >= len(tb) or o >= len(rb):
            print(f"  message {o} -> {n} is out of range!"); ok = False; continue
        if m.message_body(tb[n]) != m.message_body(rb[o]):
            print(f"  message {o} -> {n} differs: {m.message_body(tb[n])!r}"); ok = False
        checked += 1
    print(f"  {checked} referenced messages read the same as the base ROM's")
print("RESULT:", "ok" if ok else "PROBLEM")
