"""Step 8 of docs/oxide/alpha-readiness.md, the balance track's part: every
species' TM compatibility on the new TM list (docs/oxide/tm-list.tsv).

    PYTHONPATH=. python3 -m tools.oxide.balance.tmcompat plan    # what would change, no write
    PYTHONPATH=. python3 -m tools.oxide.balance.tmcompat write   # the by_tm lists in res/pokemon/

A species may learn a TM when its move is one Oxide's lists already teach it
by machine or tutor, or one a later game teaches it by TM, tutor or level-up
(rewards.compat, the reading the TM set was chosen on). A TM that left the
list leaves every species' list, and its number, where a new move took it,
is set by the new move. The item records that say what each TM teaches are
the main track's (main-tm-items); a TM past the tree's count (NUM_EXTRA_TMS
in include/constants/items.h) waits for them, since the build refuses a
label it cannot hold, and a rerun adds it.
"""
import argparse
import csv
import os
import re
import sys

from .. import jsonstyle
from ..encounters import pokedex
from . import data, rewards

TM_LIST = os.path.join(data.ROOT, "docs", "oxide", "tm-list.tsv")


def tm_list():
    """[(label, MOVE_X)] in the new list's order."""
    with open(TM_LIST, encoding="utf-8") as f:
        return [(r["tm"], r["move"]) for r in csv.DictReader(f, delimiter="\t")]


def tm_count():
    """How many TMs the tree can hold: 92 and its NUM_EXTRA_TMS."""
    with open(os.path.join(data.ROOT, "include", "constants", "items.h"), encoding="utf-8") as f:
        m = re.search(r"#define NUM_EXTRA_TMS\s+(\d+)", f.read())
    return 92 + int(m.group(1) if m else 0)


def holds(label):
    return not label.startswith("TM") or int(label[2:]) <= tm_count()


def label_key(label):
    return (label.startswith("HM"), int(label[2:]))


def new_by_tm(species):
    """The species' TM labels on the new list."""
    learns = rewards.compat(species)
    return sorted((lb for lb, mv in tm_list() if mv in learns and holds(lb)), key=label_key)


def path_of(species):
    return os.path.join(data.ROOT, "res", "pokemon", pokedex.folder_of(species), "data.json")


def current(text):
    try:
        return jsonstyle.get_value(text, ["learnset", "by_tm"])
    except KeyError:
        return None


def render(text, labels):
    """The file's text with its TM list replaced, one label a line, an empty
    list written as the file writes one (vanilla's "[  ]", or "[]")."""
    vs, ve, indent = jsonstyle._find_key(text, ["learnset", "by_tm"])
    empty = text[vs:ve] if not text[vs:ve].strip("[] ") else "[]"
    return text[:vs] + jsonstyle.dumps(list(labels), indent, max_inline=0, empty_array=empty) + text[ve:]


def plan():
    """{species: (old labels, new labels)} for every species whose list changes."""
    out = {}
    for sp in sorted(pokedex.species_list(data.ROOT)):
        with open(path_of(sp), encoding="utf-8") as f:
            text = f.read()
        old = current(text)
        if old is None:
            continue
        new = new_by_tm(sp)
        if new != old:
            out[sp] = (old, new)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["plan", "write"])
    args = ap.parse_args(argv)
    changes = plan()
    waiting = [lb for lb, _m in tm_list() if not holds(lb)]
    print(f"{len(changes)} species' TM lists change; the tree holds {tm_count()} TMs"
          + (f", so {', '.join(waiting)} wait for the main track's item records" if waiting else ""))
    if args.what == "write":
        for sp, (_old, new) in changes.items():
            with open(path_of(sp), encoding="utf-8") as f:
                text = f.read()
            with open(path_of(sp), "w", encoding="utf-8", newline="\n") as f:
                f.write(render(text, new))
        print(f"wrote {len(changes)} species files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
