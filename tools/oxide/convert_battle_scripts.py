#!/usr/bin/env python3
"""Convert hg-engine's battle scripts into Platinum's dialect.

Phase 4 element 4. The 452 imported moves reference 116 battle effects Platinum
does not have, currently stubs. hg-engine has all 116, and the two projects'
battle scripts turn out to be the same language: the opcodes are the same, the
structure is the same, and what differs is a header and about sixty constant
names. `effect_script_0006` is identical in both once those are applied.

**The rename map is derived, not written down.** Both projects ship effect
scripts 0 to 276, so this tool lines those 277 pairs up and reads the renames
straight off them: where hg-engine has one identifier in a position and
Platinum has another, that is a rename, witnessed by however many files agree.
198 of the 277 pairs line up token for token. The map cannot drift from the
tree, because it is rebuilt from the tree on every run.

Three rules keep the derivation honest, and each was learned by getting it
wrong. A `|`-joined flag list carries no order, so the two sides are compared
as sets and only the leftovers pair up. A name Platinum already defines is
shared, never renamed: when the two sides use different shared names in the
same place, the games are choosing different behaviour, and until 2026-09-23
the tool recorded three such choices as renames (`MOVE_SIDE_EFFECT_TO_ATTACKER`
to `ON_HIT`, `SPEED_UP_1_STAGE` to `RAPID_SPIN`, `SPEED_DOWN_2_STAGES` to
`SPEED_DOWN_1_STAGE`) and would have rewritten every converted script that
used them. And names no shared script happens to use are not guessed: they
are in `SUPPLEMENT`, each matched by value.

**What the self-test says.** Of the 198 aligned pairs, 196 convert to
Platinum's own script exactly. The two that do not are String Shot and Rapid
Spin, which Hardlove really changed (String Shot drops Speed two stages,
Rapid Spin raises the user's Speed); they are behaviour, and the converter
leaves them alone. The other 79 pairs do not line up because the games
implement them differently.

`--audit` triages hg-engine's effects for Oxide and `--write` converts the
ones it calls ready into `res/battle/scripts/effects`, refusing the rest.

    python3 tools/oxide/convert_battle_scripts.py --selftest
    python3 tools/oxide/convert_battle_scripts.py --map
"""

import argparse
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HG = os.environ.get("HG_ENGINE", os.path.expanduser("~/hg-engine"))
HG_EFFECTS = os.path.join(HG, "data", "battle_scripts", "effects")
HG_SUBSCRIPTS = os.path.join(HG, "data", "battle_scripts", "subscripts")
PLAT_EFFECTS = os.path.join(ROOT, "res", "battle", "scripts", "effects")

PLATINUM_EFFECTS = 277      # the ids both projects have
HEADER = '#include "macros/btlcmd.inc"\n\n\n'

TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def hg_index(folder, prefix):
    out = {}
    for p in glob.glob(os.path.join(folder, prefix + "_*.s")):
        m = re.match(prefix + r"_(\d{4})_(.+)\.s$", os.path.basename(p))
        if m:
            out[int(m.group(1))] = (m.group(2), p)
    return out


def body_lines(path):
    """A script's meaningful lines, with each project's own preamble dropped."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


def split_args(line):
    head, _, rest = line.partition(" ")
    return head, ([a.strip() for a in rest.split(",")] if rest.strip() else [])


def derive_renames(effects=None, have=None):
    """The hg-engine to Platinum identifier map, read off the shared scripts.

    Returns (map, aligned, skipped). A pair that does not line up argument for
    argument is skipped rather than guessed at: those are the effects the two
    games implement differently, and forcing an alignment there would invent
    renames that are really behaviour differences.
    """
    effects = effects if effects is not None else hg_index(HG_EFFECTS, "effect_script")
    pairs = collections.Counter()
    aligned, skipped = 0, []
    for n in range(PLATINUM_EFFECTS):
        plat = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % n)
        if n not in effects or not os.path.exists(plat):
            continue
        a, b = body_lines(effects[n][1]), body_lines(plat)
        if len(a) != len(b):
            skipped.append(n)
            continue
        local, ok = [], True
        for la, lb in zip(a, b):
            ha, aa = split_args(la)
            hb, ab = split_args(lb)
            if ha != hb:
                local.append((ha, hb))
            if len(aa) != len(ab):
                ok = False
                break
            for x, y in zip(aa, ab):
                xs, ys = x.split("|"), y.split("|")
                if len(xs) != len(ys):
                    ok = False
                    break
                if len(xs) > 1:
                    # A flag list has no order. Pair only what the two sides do
                    # not already share, so flags both projects spell the same
                    # way are never mistaken for renames of each other.
                    rx, ry = sorted(set(xs) - set(ys)), sorted(set(ys) - set(xs))
                    if len(rx) == len(ry):
                        local += list(zip(rx, ry))
                    continue
                tx, ty = TOKEN.findall(x), TOKEN.findall(y)
                if len(tx) != len(ty):
                    ok = False
                    break
                local += [(p, q) for p, q in zip(tx, ty) if p != q]
            if not ok:
                break
        if not ok:
            skipped.append(n)
            continue
        aligned += 1
        for pr in local:
            pairs[pr] += 1

    votes = collections.defaultdict(collections.Counter)
    for (x, y), c in pairs.items():
        votes[x][y] += c
    # A name Platinum already defines is shared, not renamed. When the two
    # sides of an aligned pair use different shared names in the same place,
    # that is the two games choosing different behaviour, and recording it as
    # a rename would silently rewrite hg-engine's choice into Platinum's
    # everywhere else. This was a real defect until 2026-09-23: it turned
    # MOVE_SIDE_EFFECT_TO_ATTACKER into ON_HIT and SPEED_UP_1_STAGE into
    # RAPID_SPIN in every converted script. Each false rename was witnessed by
    # a few pairs where Hardlove changed a move, then applied to every pair,
    # so it also caused most of the self-test's mismatches (161 exact of 198
    # with it, 196 without).
    have = have if have is not None else platinum_identifiers()
    shared = {x for x in votes if x in have}
    for x in shared:
        del votes[x]
    conflicts = {x: dict(ys) for x, ys in votes.items() if len(ys) > 1}
    return ({x: ys.most_common(1)[0][0] for x, ys in votes.items()},
            aligned, skipped, conflicts)


# Renames the shared scripts never witness, because no effect 0 to 276 happens
# to use them. Each one was matched by value and, for the flag words, by which
# status field Platinum's own scripts pair it with, so none is a guess from the
# name alone (2026-09-23). `supplemented()` refuses to run if a target stops
# existing in Platinum.
SUPPLEMENT = {
    "STATUS_NONE": "MON_CONDITION_NONE",                                   # 0
    "STATUS_POISON": "MON_CONDITION_POISON",                               # 1 << 3
    "STATUS_BAD_POISON": "MON_CONDITION_TOXIC",                            # 1 << 7
    "BMON_DATA_ABILITY": "BATTLEMON_ABILITY",                              # 0x1A
    "BMON_DATA_HELD_ITEM": "BATTLEMON_HELD_ITEM",                          # 0x37
    "BMON_DATA_STAT_CHANGE_SPEED": "BATTLEMON_SPEED_STAGE",                # 21
    "BMON_DATA_STAT_CHANGE_SPATK": "BATTLEMON_SP_ATTACK_STAGE",            # 22
    "BMON_DATA_STAT_CHANGE_SPDEF": "BATTLEMON_SP_DEFENSE_STAGE",           # 23
    "BSCRIPT_VAR_MOVE_TYPE": "BTLVAR_MOVE_TYPE",                           # 0x39
    "BSCRIPT_VAR_BATTLER_STAT_CHANGE": "BTLVAR_SIDE_EFFECT_MON",           # 0x11
    "BSCRIPT_VAR_BATTLE_STATUS_2": "BTLVAR_BATTLE_CTX_STATUS_2",           # 0x3C
    "BSCRIPT_VAR_SIDE_EFFECT_PARAM": "BTLVAR_SIDE_EFFECT_PARAM",           # 0x22
    "BATTLE_STATUS_MOVE_ANIMATIONS_OFF": "SYSCTL_PLAYED_MOVE_ANIMATION",   # status, 1 << 14
    "BATTLE_STATUS2_UPDATE_STAT_STAGES": "SYSCTL_UPDATE_STAT_STAGES",      # status 2, 1 << 1
    "BATTLE_STATUS2_STAT_STAGE_CHANGE_SHOWN": "SYSCTL_STAT_STAGE_CHANGE_SHOWN",  # status 2, 1 << 7
    "MULTIHIT_TRIPLE_KICK": "SYSCTL_TRIPLE_KICK",                          # 0xDD both sides
}


def platinum_identifiers():
    """Every name a Platinum battle script can use: generated enums, the
    script macros, and whatever the headers define or enumerate."""
    have = set()
    for f in glob.glob(os.path.join(ROOT, "generated", "*.txt")):
        have |= {l.strip() for l in open(f, encoding="utf-8") if l.strip()}
    for root in ("include", os.path.join("build", "res", "text", "bank"), "asm"):
        for dp, _, names in os.walk(os.path.join(ROOT, root)):
            for n in names:
                if not n.endswith((".h", ".inc")):
                    continue
                t = open(os.path.join(dp, n), encoding="utf-8", errors="ignore").read()
                have |= set(re.findall(r"#define\s+(\w+)", t))
                have |= set(re.findall(r"^\s*\.macro\s+(\w+)", t, re.M))
                for blk in re.findall(r"enum\s*\w*\s*\{(.*?)\}", t, re.S):
                    have |= set(re.findall(r"^\s*([A-Za-z_]\w*)\s*(?:=|,|$)", blk, re.M))
    return have


def supplemented(renames, have=None):
    have = have if have is not None else platinum_identifiers()
    gone = sorted(v for v in SUPPLEMENT.values() if v not in have)
    if gone:
        sys.exit("SUPPLEMENT names identifiers Platinum no longer has: %s" % gone)
    merged = dict(SUPPLEMENT)
    merged.update(renames)
    return merged


def convert(path, renames):
    """One hg-engine script in Platinum's dialect."""
    out = [HEADER.rstrip("\n"), "", ""]
    for line in open(path, encoding="utf-8"):
        raw = line.rstrip("\n")
        stripped = raw.split("//")[0].rstrip()
        if stripped.startswith(("#include", ".include")) or stripped.strip() == ".data":
            continue
        if not stripped.strip():
            continue
        out.append(TOKEN.sub(lambda m: renames.get(m.group(0), m.group(0)), raw.rstrip()))
    return "\n".join(out) + "\n"


def same_line(a, b):
    """Two script lines that mean the same thing. A `|`-joined flag list is a
    set, so `A|B` and `B|A` are the same line and a text comparison would call
    them different."""
    ha, aa = split_args(a)
    hb, ab = split_args(b)
    if ha != hb or len(aa) != len(ab):
        return False
    return all(set(x.split("|")) == set(y.split("|")) for x, y in zip(aa, ab))


def selftest(renames, skipped):
    """Convert the 277 effects both projects have and compare to Platinum's.

    Scored on the pairs that line up structurally, because those are the ones
    that say anything about the rename map. The rest are effects the two games
    implement differently, hg-engine having moved work out of the script that
    Platinum still does in it (effect 7, Selfdestruct, is the clearest: hg's is
    a bare hit, Platinum's carries the whole Damp check). A difference there is
    not a gap in the map and cannot be fixed by renaming anything.

    A map that rebuilds Platinum's own scripts from hg-engine's is good enough
    to bring the new ones across; that is the whole claim this test supports.
    """
    effects = hg_index(HG_EFFECTS, "effect_script")
    exact, differ, structural = 0, [], 0
    for n in range(PLATINUM_EFFECTS):
        plat = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % n)
        if n not in effects or not os.path.exists(plat):
            continue
        if n in skipped:
            structural += 1
            continue
        got = body_lines_from_text(convert(effects[n][1], renames))
        want = body_lines(plat)
        if len(got) == len(want) and all(same_line(x, y) for x, y in zip(got, want)):
            exact += 1
        else:
            differ.append(n)
    return exact, differ, structural


def body_lines_from_text(text):
    out = []
    for line in text.splitlines():
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


PLAT_EFFECTS_OWNED = range(PLATINUM_EFFECTS, 407)   # the stubs element 4 created


def hg_move_names():
    """hg-engine's own MOVE_ constant for each move id, for finding where its C
    code names a move. Oxide's enum names differ in a few places (hg-engine's
    MOVE_GUARDIAN_OF_ALOLA is Oxide's MOVE_ALOLAN_GUARDIAN), so these have to
    come from hg-engine, not from generated/moves.txt."""
    out = {}
    for line in open(os.path.join(HG, "include", "constants", "moves.h"), encoding="utf-8"):
        m = re.match(r"#define\s+(MOVE_\w+)\s+(\d+)", line)
        if m:
            out.setdefault(int(m.group(2)), m.group(1))
    return out


def c_references(names):
    """Where hg-engine's C names each constant, split into behaviour and list
    membership. A line that is only `MOVE_X,` is an entry in an array (a
    Metronome ban list, the moves Iron Fist boosts), which belongs to whatever
    ability or item reads the list and says nothing about the move's own
    effect. Anything else (a `case`, a comparison) is behaviour."""
    import subprocess
    out = {}
    if not names:
        return out
    pattern = r"\b(" + "|".join(sorted(names)) + r")\b"
    found = subprocess.run(["grep", "-rnE", pattern, "src"], cwd=HG,
                           capture_output=True, text=True).stdout
    for line in found.splitlines():
        path, _, rest = line.split(":", 2)
        for name in re.findall(pattern, rest):
            kind = "list" if re.fullmatch(r"\s*\w+,?\s*(//.*)?", rest) else "code"
            out.setdefault(name, []).append((kind, os.path.basename(path)))
    return out


def audit(ids, renames, have):
    """What stands between each hg-engine effect and a working Platinum one.

    `ready` means the converted script uses only names Platinum has, prints no
    message by raw number, and hg-engine's C never implements part of the
    effect itself, keyed on either the effect's id or one of its moves. It
    does not mean the move has been tried in a battle.
    """
    import donor_moves
    effects = hg_index(HG_EFFECTS, "effect_script")
    dm = donor_moves.DonorMoves()
    recs = dm.moves()
    mnames = hg_move_names()
    users = collections.defaultdict(list)
    for i, r in enumerate(recs):
        if 0 < i <= 922:
            users[r["effect"]].append(i)
    effect_const = {e: "MOVE_EFFECT_" + effects[e][0] for e in ids}
    move_consts = {mnames[i] for e in ids for i in users[e] if i in mnames}
    refs = c_references(set(effect_const.values()) | move_consts)

    rows = []
    for e in ids:
        text = convert(effects[e][1], renames)
        lines = body_lines_from_text(text)
        labels = {l[:-1] for l in lines if l.endswith(":")}
        unresolved, messages, items = set(), [], set()
        for l in lines:
            if l.endswith(":"):
                continue
            head, args = split_args(l)
            if head not in have:
                unresolved.add(head)
            for a in args:
                for t in re.findall(r"[A-Za-z_]\w*", a):
                    if t in labels or t in have:
                        continue
                    (items if t.startswith("HOLD_EFFECT_") else unresolved).add(t)
            if head == "PrintMessage" and args and re.fullmatch(r"\d+", args[0]):
                messages.append(int(args[0]))
        code = sorted({f for n in [effect_const[e]] + [mnames.get(i) for i in users[e]]
                       for kind, f in refs.get(n, []) if kind == "code"})
        if items:
            verdict = "items"
        elif unresolved:
            verdict = "names"
        elif messages:
            verdict = "text"
        elif code:
            verdict = "c"
        else:
            verdict = "ready"
        rows.append(dict(id=e, name=effects[e][0], verdict=verdict,
                         unresolved=sorted(unresolved), messages=messages,
                         items=sorted(items), code=code,
                         moves=[dm.names()[i] for i in users[e]][:3]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--audit", nargs="*", type=int, metavar="N",
                    help="triage hg-engine effects (default: every one Oxide's moves use)")
    ap.add_argument("--write", nargs="+", type=int, metavar="N",
                    help="convert these effects into res/battle/scripts/effects; "
                         "refuses any the audit does not call ready")
    ap.add_argument("--map", action="store_true", help="print the derived renames")
    ap.add_argument("--selftest", action="store_true",
                    help="convert the shared 277 effects and compare to Platinum's")
    ap.add_argument("--show", type=int, metavar="N",
                    help="print the conversion of hg-engine effect N")
    a = ap.parse_args()

    if not os.path.isdir(HG_EFFECTS):
        sys.exit("no hg-engine checkout at %s; set HG_ENGINE or clone it "
                 "(see the tracker's element 4 entry)" % HG)

    renames, aligned, skipped, conflicts = derive_renames()
    # The summary goes to stderr: `--show N > effect_script_NNNN.s` must leave
    # nothing but the script on stdout (2026-09-22 review finding).
    print("rename map: %d entries, derived from %d aligned script pairs of %d; "
          "%d pairs differ in shape and were not used"
          % (len(renames), aligned, PLATINUM_EFFECTS, len(skipped)), file=sys.stderr)
    if conflicts:
        print("AMBIGUOUS, the map is not trustworthy until these are resolved:", file=sys.stderr)
        for x, ys in conflicts.items():
            print("    %-44s %s" % (x, ys), file=sys.stderr)

    have = platinum_identifiers()
    renames = supplemented(renames, have)

    if a.audit is not None or a.write:
        import donor_moves
        recs = donor_moves.DonorMoves().moves()
        wanted = sorted({r["effect"] for r in recs[1:923] if r["effect"] >= PLATINUM_EFFECTS})
        rows = audit(a.audit or wanted, renames, have)
        if a.audit is not None:
            order = ["ready", "c", "text", "names", "items"]
            for v in order:
                group = [r for r in rows if r["verdict"] == v]
                if not group:
                    continue
                print("%s: %d" % (v, len(group)))
                for r in group:
                    why = {"ready": "", "c": "C: " + ", ".join(r["code"]),
                           "text": "messages %s" % r["messages"],
                           "names": "unresolved: " + ", ".join(r["unresolved"]),
                           "items": "items: " + ", ".join(r["items"][:3])}[v]
                    print("    %d %-38s %-34s %s" % (r["id"], r["name"],
                                                    ", ".join(r["moves"])[:34], why))
        if a.write:
            verdicts = {r["id"]: r["verdict"] for r in audit(a.write, renames, have)}
            refused = [e for e in a.write if verdicts[e] != "ready"]
            if refused:
                sys.exit("refusing %s: the audit does not call them ready" % refused)
            effects = hg_index(HG_EFFECTS, "effect_script")
            for e in a.write:
                if e not in PLAT_EFFECTS_OWNED:
                    sys.exit("%d is not one of the stubs element 4 created" % e)
                out = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % e)
                with open(out, "w", encoding="utf-8", newline="\n") as f:
                    f.write(convert(effects[e][1], renames))
            print("wrote %d effect scripts" % len(a.write), file=sys.stderr)

    if a.map:
        for x, y in sorted(renames.items()):
            print("    %-46s -> %s" % (x, y))
    if a.show is not None:
        effects = hg_index(HG_EFFECTS, "effect_script")
        sys.stdout.write(convert(effects[a.show][1], renames))
    if a.selftest:
        exact, differ, structural = selftest(renames, set(skipped))
        total = exact + len(differ)
        print("selftest: of the %d shared effects that line up structurally, "
              "%d convert to Platinum's own script exactly and %d differ"
              % (total, exact, len(differ)))
        print("  %d more were not scored: the two games implement those "
              "differently, which no rename can fix" % structural)
        if differ:
            print("  differing ids: %s%s" % (differ[:25], " ..." if len(differ) > 25 else ""))
        return 0 if not differ else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
