"""The pick-list's `tier` column: proposed defaults. Authoring plan decision 7.

R12 needs every line on the pick-list to carry a tier, which sets how cheap
the line has to be to catch. The plan fixes the defaults and says Ian edits
them in the CSV afterwards; this module derives them once, for
`cli tier-init`, and is not consulted again.

    gate              legendaries and mythicals, the starter lines, the fossil
                      lines, and anything a script battles the player with.
                      These are scripted, not wild; R12 asks for a scripted
                      source rather than a cost.
    starter-adjacent  lines whose first stage can sit on Routes 201-205. The
                      default reads that off vanilla: any line whose first
                      stage vanilla places in an early-band land table.
    preferred         the rest of the Sinnoh dex (Platinum's 210).
    filler            the remainder.

A line has one tier, so for the natives the tier propagates over the
evolution line, highest first (gate > starter-adjacent > preferred >
filler). The 159 new species are tiered by their national dex number alone,
since the tree has no line data for them yet. The Sinnoh dex membership is
read from the pinned vanilla ROM's pl_pokezukan.narc; the repo's prebuilt
pokezukan.narc is Diamond and Pearl's 151 and is not it.
"""
import csv
import os
import struct

from . import analysis as A
from . import dex
from . import model

TIERS = ("gate", "starter-adjacent", "preferred", "filler")

# National dex numbers. Legendaries and mythicals through Gen 9, the starter
# lines, and the fossil lines. Only the pick-list's rows matter, so a stray
# number here costs nothing; a missing one shows up as a wrong default Ian
# corrects in the CSV.
LEGENDARY = set(
    [144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251]
    + list(range(377, 387)) + list(range(480, 494)) + [494]
    + list(range(638, 650)) + list(range(716, 722)) + [772, 773]
    + list(range(785, 810)) + list(range(888, 899)) + [905]
    + [1001, 1002, 1003, 1004, 1007, 1008, 1014, 1015, 1016, 1017, 1024, 1025])
STARTER = set(n for start in (1, 152, 252, 387, 495, 650, 722, 810, 906)
              for n in range(start, start + 9))

# Lines whose first stage sits on the first routes of its own game, so it
# can sit on Routes 201-205 here. Vanilla's early band supplies only seven
# pick-list lines (the list dropped Starly, Bidoof, Kricketot and the rest),
# which cannot fill seventeen corridor tables at three to five species each;
# these are the other regions' Route 1 and Route 2 regulars, natives and new
# alike. Step 2's availability plan is built on this set. Ian's to edit.
EARLY_LINES = {
    "SPECIES_SENTRET", "SPECIES_NIDORAN_F", "SPECIES_NIDORAN_M", "SPECIES_VULPIX",
    "SPECIES_SHROOMISH", "SPECIES_LOTAD",
    "SPECIES_PURRLOIN", "SPECIES_SEWADDLE", "SPECIES_MINCCINO", "SPECIES_FLETCHLING",
    "SPECIES_PIKIPEK", "SPECIES_GRUBBIN", "SPECIES_BOUNSWEET", "SPECIES_ROOKIDEE",
    "SPECIES_BLIPBUG", "SPECIES_WOOLOO", "SPECIES_PAWMI", "SPECIES_SMOLIV",
    "SPECIES_NACLI",
}
FOSSIL = set(n for lo, hi in ((138, 142), (345, 348), (408, 411), (564, 567),
                              (696, 699), (880, 883))
             for n in range(lo, hi + 1))

# Ian, 2026-09-21: the eight new starter lines are wild, not gifted, so they
# leave the gate tier. Preferred, so R12 holds them to a cost ceiling:
# Fennekin, Scorbunny and Popplio at a real share on their home tables, the
# rest as tails or honey-tree rarities (see the availability plan).
WILD_STARTERS = {
    "SPECIES_SNIVY", "SPECIES_FENNEKIN", "SPECIES_FROAKIE", "SPECIES_ROWLET",
    "SPECIES_LITTEN", "SPECIES_POPPLIO", "SPECIES_SCORBUNNY", "SPECIES_SPRIGATITO",
}


def sinnoh_dex(rom_path):
    """The species with a Sinnoh dex number in a Platinum ROM."""
    import ndspy.narc
    import ndspy.rom
    rom = ndspy.rom.NintendoDSRom.fromFile(os.path.expanduser(rom_path))

    def walk(folder, prefix=""):
        out = {}
        for i, name in enumerate(folder.files):
            out[prefix + name] = folder.firstID + i
        for sub, f in folder.folders:
            out.update(walk(f, prefix + sub + "/"))
        return out
    names = walk(rom.filenames)
    member = ndspy.narc.NARC(rom.files[names["poketool/pl_pokezukan.narc"]]).files[0]
    nums = struct.unpack("<%dH" % (len(member) // 2), member)
    species = [l.strip() for l in open(os.path.join(model.repo_root(), "generated",
                                                    "species.txt")) if l.strip()]
    return {species[i] for i, v in enumerate(nums) if v and i < len(species)}


def early_bases(ref="main"):
    """First-stage species vanilla places in an early-band land table."""
    root = model.repo_root()
    line_of = dex.lines(root)
    out = set()
    for a in model.load_all(ref, active_only=True):
        if a.band != "early":
            continue
        for sp, _ in a.slots:
            if sp in dex.line_base(root, line_of.get(sp, sp)):
                out.add(sp)
    return out


def national_numbers():
    """{species: national dex number} from the tree's species order, which
    is the national order through Arceus. Twenty-one native rows on the
    pick-list carry no `natdex` (their stats were UNMATCHED against the
    spreadsheet), and this is where their number comes from instead."""
    path = os.path.join(model.repo_root(), "generated", "species.txt")
    names = [l.strip() for l in open(path, encoding="utf-8") if l.strip()]
    return {sp: i for i, sp in enumerate(names) if 0 < i <= 493}


def species_tier(row, statics, sinnoh, natdex_of=None):
    natdex = int(row["natdex"]) if row.get("natdex", "").isdigit() else 0
    c = row.get("constant")
    if not natdex and c and natdex_of:
        natdex = natdex_of.get(c, 0)
    if natdex in LEGENDARY or natdex in STARTER or natdex in FOSSIL or (c and c in statics):
        return "gate"
    if natdex and (c in sinnoh if c else False):
        return "preferred"
    return "filler"


def defaults(rom_path="~/roms/vanilla.nds", ref="main"):
    """{pick-list name: tier} for every row."""
    from . import audit
    root = model.repo_root()
    rows = dex.pick_list(root)
    sinnoh = sinnoh_dex(rom_path)
    statics = {r["species"] for r in audit.script_references(root)
               if r["command"] in audit.BATTLE_COMMANDS}
    early = early_bases(ref) | EARLY_LINES
    line_of = dex.lines(root)
    natdex_of = national_numbers()
    tier = {r["name"]: species_tier(r, statics, sinnoh, natdex_of) for r in rows}
    # natives: the first stage decides starter-adjacent, and the whole line
    # takes its strongest member's tier
    by_line = {}
    for r in rows:
        if r["constant"]:
            by_line.setdefault(line_of.get(r["constant"], r["constant"]), []).append(r)
    rank = {t: i for i, t in enumerate(TIERS)}
    for line_id, members in by_line.items():
        best = min((tier[m["name"]] for m in members), key=rank.get)
        bases = dex.line_base(root, line_id)
        if any(b in WILD_STARTERS for b in bases):
            best = "preferred"
        if best != "gate" and any(m["constant"] in early for m in members
                                  if m["constant"] in bases):
            best = "starter-adjacent"
        for m in members:
            tier[m["name"]] = best
    return tier


def write_column(tier_by_name, path=None):
    """Add or replace the `tier` column, touching nothing else: the file is
    re-emitted through the csv module with the same dialect it was read
    with, and a round-trip of the untouched columns is checked first."""
    path = path or os.path.join(model.repo_root(), *dex.PICK_LIST)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    rows = list(csv.DictReader(text.splitlines()))
    fields = list(rows[0].keys())
    if "tier" not in fields:
        fields.append("tier")

    def emit(rows, fields):
        import io
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
        return out.getvalue()
    original_fields = [k for k in fields if k != "tier" or "tier" in rows[0]]
    if emit(rows, original_fields) != text:
        raise RuntimeError(f"{path} does not round-trip through the csv module; "
                           f"refusing to rewrite it")
    for r in rows:
        r["tier"] = tier_by_name[r["name"]]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(emit(rows, fields))
    return len(rows)
