"""Load and save encounter tables, one slot at a time.

The decomp's res/field/encounters/*.json files are the tool's state. There is
no database and no export step. An edit lands as a git diff on exactly the key
that changed, because writes go through jsonstyle.replace_value on the file's
own text rather than re-serialising the parsed object. Whole-file rewriting was
abandoned during the species import: the repo's JSON style is not reproducible
from Python across every file, so untouched text must never be re-rendered.

The calibration corpus lives on `main`, not in the working tree. This branch's
res/field/encounters/ holds the base ROM's rewritten tables, so anything that
asks "does this reproduce vanilla" has to load through `ref="main"`, which
reads via `git show` and is therefore read-only by construction.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jsonstyle  # noqa: E402

ENC_DIR = os.path.join("res", "field", "encounters")
SIDECAR = os.path.join("docs", "oxide", "encounters", "design.json")

# Hardcoded in the game, see src/overlay006/wild_encounters.c. Twelve slots.
LAND_RATES = (20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1)

# Time-of-day layers replace exactly these slots, so a day/night swap can move
# at most 20% of a table. Design doc 1.3.
DAY_NIGHT_SLOTS = (2, 3)

# Band cutoffs on a table's median level. Design doc 2.5.
BAND_EARLY_MAX = 12
BAND_MID_MAX = 29


def repo_root():
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _read(path, ref=None):
    """Read a repo-relative path from the working tree, or from a git ref."""
    if ref is None:
        with open(os.path.join(repo_root(), path), encoding="utf-8") as f:
            return f.read()
    out = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=repo_root(), capture_output=True, text=True, check=True)
    return out.stdout


def area_names(ref=None):
    """Every encounter file's area name, sorted. Includes the two that are not
    land tables at all; callers filter with Area.has_land."""
    if ref is None:
        names = os.listdir(os.path.join(repo_root(), ENC_DIR))
    else:
        out = subprocess.run(
            ["git", "ls-tree", "--name-only", ref, ENC_DIR + "/"],
            cwd=repo_root(), capture_output=True, text=True, check=True)
        names = [os.path.basename(p) for p in out.stdout.split()]
    return sorted(n[:-len(".json")] for n in names if n.endswith(".json"))


class Area:
    """One encounter file: its raw text, its parsed view, and slot-level edits.

    `text` is authoritative. `data` is a convenience read-model kept in step
    with it; nothing is ever written back from `data` wholesale.
    """

    def __init__(self, name, text, ref=None):
        self.name = name
        self.text = text
        self.ref = ref
        self.data = json.loads(text)

    @property
    def path(self):
        return os.path.join(ENC_DIR, self.name + ".json")

    # -- shape ------------------------------------------------------------

    @property
    def has_land(self):
        """False for the two files that are not land tables: the Great Marsh
        lookout (binocular data) and the honey tree pools."""
        le = self.data.get("land_encounters")
        return isinstance(le, list) and len(le) == len(LAND_RATES)

    @property
    def land_active(self):
        """A table with land_rate 0 is never rolled against. Twelve files are
        like this: they carry a full 12 slots that the game never reaches."""
        return self.has_land and self.data.get("land_rate", 0) > 0

    @property
    def slots(self):
        """[(species, level)] for the twelve land slots, base (morning) layer."""
        return [(e["species"], e["level"]) for e in self.data["land_encounters"]]

    @property
    def levels(self):
        return [e["level"] for e in self.data["land_encounters"]]

    @property
    def band(self):
        """early / mid / late from the table's median level. Design doc 2.5."""
        if not self.land_active:
            return None
        lv = sorted(self.levels)
        median = lv[len(lv) // 2]
        if median <= BAND_EARLY_MAX:
            return "early"
        if median <= BAND_MID_MAX:
            return "mid"
        return "late"

    # -- edits ------------------------------------------------------------

    def set_slot(self, index, species=None, level=None):
        """Rewrite one land slot. Touches only the keys actually given."""
        if not 0 <= index < len(LAND_RATES):
            raise IndexError(f"land slot {index} out of range")
        if species is not None:
            self._replace(["land_encounters", index, "species"], species)
        if level is not None:
            self._replace(["land_encounters", index, "level"], int(level))

    def set_land_rate(self, rate):
        self._replace(["land_rate"], int(rate))

    def set_time_slot(self, layer, index, species):
        """day/night carry two species each, standing in for slots 2 and 3.
        Writing anywhere else would be illegal per R7, so it is refused here
        rather than left for the linter to catch after the fact."""
        if layer not in ("day", "night"):
            raise ValueError(f"not a time-of-day layer: {layer}")
        if index not in (0, 1):
            raise IndexError(f"{layer} has two entries, not {index + 1}")
        self._replace([layer, index], species)

    def _replace(self, path, value):
        if self.ref is not None:
            raise RuntimeError(
                f"{self.name} was loaded from ref {self.ref!r}; it is read-only")
        self.text = jsonstyle.replace_value(self.text, path, value)
        self.data = json.loads(self.text)

    def save(self):
        if self.ref is not None:
            raise RuntimeError(
                f"{self.name} was loaded from ref {self.ref!r}; it is read-only")
        full = os.path.join(repo_root(), self.path)
        with open(full, "w", encoding="utf-8", newline="\n") as f:
            f.write(self.text)

    # -- the round-trip check --------------------------------------------

    def rewrite_identity(self):
        """Replace every land value with the value it already holds.

        This is the real M1 gate. Writing raw text back is trivially clean;
        what has to be proved is that the *edit path* — locating a key and
        re-rendering its value in repo style — is byte-identical for every
        slot of every file. Returns a list of (path, before, after) for the
        keys that did not survive, empty when the file round-trips.
        """
        bad = []
        paths = [["land_rate"]] if "land_rate" in self.data else []
        if self.has_land:
            for i in range(len(LAND_RATES)):
                paths.append(["land_encounters", i, "species"])
                paths.append(["land_encounters", i, "level"])
        for layer in ("day", "night", "swarms", "radar"):
            if isinstance(self.data.get(layer), list):
                for i in range(len(self.data[layer])):
                    paths.append([layer, i])
        for path in paths:
            current = jsonstyle.get_value(self.text, path)
            after = jsonstyle.replace_value(self.text, path, current)
            if after != self.text:
                bad.append((path, self.text, after))
        return bad


def load_area(name, ref=None):
    area = Area(name, _read(os.path.join(ENC_DIR, name + ".json"), ref), ref)
    return area


def load_all(ref=None, land_only=False, active_only=False):
    areas = [load_area(n, ref) for n in area_names(ref)]
    if active_only:
        return [a for a in areas if a.land_active]
    if land_only:
        return [a for a in areas if a.has_land]
    return areas


# -- the sidecar ----------------------------------------------------------
#
# Design intent that the decomp format has nowhere to put. Hand-editable on
# purpose: it is what Ian diffs when he wants to know why a route looks the
# way it does. Archetype assignment waits for M2, which is what can measure
# fit; M1 writes only what can be derived without the analysis engine.


def sidecar_path():
    return os.path.join(repo_root(), SIDECAR)


def load_sidecar():
    path = sidecar_path()
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_sidecar(obj):
    path = sidecar_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_sidecar(ref=None):
    """Initial sidecar: band and an empty intent per area, plus the archetype
    budget from design doc 2.3. Thresholds land with the linter in M3."""
    areas = load_all(ref)
    entries = {}
    inactive, special = [], []
    for a in areas:
        if not a.has_land:
            special.append(a.name)
            continue
        if not a.land_active:
            inactive.append(a.name)
            continue
        entries[a.name] = {
            "archetype": None,
            "band": a.band,
            "intent": "",
            "locked": [],
            "base_level": min(a.levels),
        }
    from . import lint  # deferred: lint reads analysis, model reads neither
    return {
        "_comment": (
            "Design intent for the encounter tables. Hand-editable. "
            "See docs/oxide/encounter-tool-design.md section 3.2. "
            "Thresholds are Ian's house rules; edit them here, never in "
            "lint.py. Rules tagged aspirational in lint.py sit beyond what "
            "vanilla Platinum does, on purpose."),
        "thresholds": lint.DEFAULT_THRESHOLDS,
        "budget": {
            "concentrated": 0.18,
            "dominant": 0.14,
            "mid": 0.50,
            "broad": 0.18,
        },
        "areas": entries,
        "inactive_areas": inactive,
        "non_land_files": special,
    }
