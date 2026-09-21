#!/usr/bin/env python3
"""Carry Hardlove's tables into res/ and generated/.

The counterpart to import_base_rom.py, which carries Ian's DSPRE edits over.
This one brings in content from the donor ROM for Phase 4. Each subcommand does
one table and each is idempotent: run it twice and the second run reports
nothing to do.

Reading is all in donor.py; this file only decides what the repo should say.

    python3 tools/oxide/import_donor.py abilities [--dry-run]
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import donor  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MSGENC = os.path.join(ROOT, "build", "tools", "msgenc", "msgenc")
CHARMAP = os.path.join(ROOT, "tools", "msgenc", "charmap.txt")


# ------------------------------------------------------------------ helpers
def constant_name(prefix, name):
    """A C constant from a display name. Apostrophes vanish rather than becoming
    underscores, so Dragon's Maw is DRAGONS_MAW and not DRAGON_S_MAW."""
    s = name.upper().replace("'", "").replace("’", "")
    s = re.sub(r"[^A-Z0-9]+", "_", s)
    return prefix + s.strip("_")


def deduplicate(names):
    """Hardlove reuses a display name for several ids: As One twice, Embody
    Aspect four times, Placeholder twice. Each repeat after the first gets a
    numeric suffix in id order. Guessing which mask or which horse each one is
    would be a guess, and none of them is reachable in Oxide."""
    seen = {}
    out = []
    for n in names:
        seen[n] = seen.get(n, 0) + 1
        out.append(n if seen[n] == 1 else "%s_%d" % (n, seen[n]))
    return out


def append_messages(path, bank_index, first_id, messages, dry_run, log):
    """Append to one res/text bank, leaving every existing byte alone. The repo's
    JSON formatting is not uniform and whole-file rewrites make merges painful,
    so this is string surgery on the tail rather than a json.dump."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    tail = "    }\n  ]\n}\n"
    if not text.endswith(tail):
        raise SystemExit("%s does not end the way this tool expects" % path)
    chunks = []
    for i, body in enumerate(messages):
        msg_id = "pl_msg_%08d_%05d" % (bank_index, first_id + i)
        if isinstance(body, list):
            lines = ",\n".join('        %s' % json.dumps(l, ensure_ascii=False) for l in body)
            value = "[\n%s\n      ]" % lines
        else:
            value = json.dumps(body, ensure_ascii=False)
        chunks.append('    {\n      "id": "%s",\n      "en_US": %s\n    }' % (msg_id, value))
    new = text[:-len(tail)] + "    },\n" + ",\n".join(chunks) + "\n  ]\n}\n"
    log.append("%s: +%d messages" % (os.path.relpath(path, ROOT), len(messages)))
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)


# ---------------------------------------------------------------- abilities
def import_abilities(d, dry_run, log):
    """Take the donor's whole ability table, not just the ids the pick-list
    species need. Ids 0..123 already agree with Platinum's, so importing the
    rest contiguously keeps donor ids and Oxide ids equal for good, and every
    later import can use a donor number as-is instead of going through a map.
    The names and descriptions come across here; the effects are element 5."""
    names = d.text_bank(donor.TEXT_ABILITY_NAMES, MSGENC, CHARMAP)
    upper = d.text_bank(donor.TEXT_ABILITY_NAMES_UPPER, MSGENC, CHARMAP)
    descs = d.text_bank(donor.TEXT_ABILITY_DESCRIPTIONS, MSGENC, CHARMAP)
    if not (len(names) == len(upper) == len(descs)):
        raise SystemExit("donor ability banks disagree on length")

    enum_path = os.path.join(ROOT, "generated", "abilities.txt")
    existing = [l.strip() for l in open(enum_path) if l.strip()]
    first = len(existing)
    if first >= len(names):
        log.append("abilities: nothing to do, already %d" % first)
        return

    # Check the donor agrees with what is already here before extending it.
    derived = deduplicate(names)
    for i in range(1, first):
        want = constant_name("ABILITY_", derived[i])
        if existing[i] != want and existing[i] != want.replace("_EYES", "EYES"):
            log.append("  note: id %d is %s here and %r in the donor"
                       % (i, existing[i], names[i]))

    new_consts = [constant_name("ABILITY_", derived[i]) for i in range(first, len(names))]
    clash = [c for c in new_consts if c in existing]
    if clash:
        raise SystemExit("new ability constants clash with existing ones: %s" % clash)

    log.append("generated/abilities.txt: +%d constants (%d..%d)"
               % (len(new_consts), first, len(names) - 1))
    if not dry_run:
        with open(enum_path, "a") as f:
            f.write("\n".join(new_consts) + "\n")

    append_messages(os.path.join(ROOT, "res", "text", "ability_names.json"),
                    610, first, names[first:], dry_run, log)
    append_messages(os.path.join(ROOT, "res", "text", "ability_names_uppercase.json"),
                    611, first, upper[first:], dry_run, log)
    append_messages(os.path.join(ROOT, "res", "text", "ability_descriptions.json"),
                    612, first, descs[first:], dry_run, log)


# ------------------------------------------------------------------ species
# The natives that a new species hangs off, so the family root can be carried
# down. Those natives' own evolution records are a separate pass; this only
# says where each new species' egg comes from. Source: the evolution table in
# docs/oxide/species-pick-list.md.
NEW_SPECIES_PARENTS = {
    "SPECIES_ANNIHILAPE": "SPECIES_PRIMEAPE",
    "SPECIES_KLEAVOR": "SPECIES_SCYTHER",
    "SPECIES_SYLVEON": "SPECIES_EEVEE",
    "SPECIES_GYARADOS_M": "SPECIES_GYARADOS",
    "SPECIES_LOPUNNY_M": "SPECIES_LOPUNNY",
    "SPECIES_CLODSIRE": "SPECIES_WOOPER",
    "SPECIES_ALOMOMOLA": "SPECIES_LUVDISC",
}


def import_species(d, dry_run, log):
    import species_import
    conv = species_import.Converter(d)
    writer = species_import.Writer(conv, dry_run, log)
    written = {}
    for row in conv.map:
        written[row["constant"]] = writer.write(row)
    log.extend("  note: " + n for n in conv.notes)
    if dry_run:
        log.append("species: would write %d directories" % len(written))
        return

    natives = {}
    for constant, parent in NEW_SPECIES_PARENTS.items():
        path = os.path.join(ROOT, "res", "pokemon",
                            species_import.dirname_of(parent), "data.json")
        with open(path, encoding="utf-8") as f:
            natives[constant] = json.load(f)["offspring"]
    species_import.fix_offspring(written, natives)
    for constant, data in written.items():
        path = os.path.join(ROOT, "res", "pokemon",
                            species_import.dirname_of(constant), "data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write("\n")

    species_import.insert_species_constants(
        [r["constant"] for r in conv.map], dry_run, log)
    species_import.register_cries(conv.map, dry_run, log)
    log.append("species: %d directories written" % len(written))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["abilities", "species"])
    ap.add_argument("--rom", default=donor.DEFAULT_ROM)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    d = donor.Donor(args.rom)
    log = []
    if args.what == "abilities":
        import_abilities(d, args.dry_run, log)
    elif args.what == "species":
        import_species(d, args.dry_run, log)
    print("\n".join(log) if log else "nothing to do")


if __name__ == "__main__":
    main()
