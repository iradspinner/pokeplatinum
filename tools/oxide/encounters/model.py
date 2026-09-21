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

# The other species lists a land table carries, with their fixed lengths.
# swarms and the five dual-slot lists stand in for slots 0-1 (swarm) and 8-9
# (dual-slot) the way day/night stand in for 2-3; radar replaces slots 4-5
# with one of four species. All of them are leaks if they hold an off-list
# species, which is why the writers exist before their design does.
SWARM_KEY = "swarms"
RADAR_KEY = "radar"
DUAL_SLOT_KEYS = ("ruby", "sapphire", "emerald", "firered", "leafgreen")
LIST_KEY_SIZES = {SWARM_KEY: 2, "day": 2, "night": 2, RADAR_KEY: 4,
                  **{k: 2 for k in DUAL_SLOT_KEYS}}

# Species-only sources outside the land format, read for the audit and left
# alone by the writers: their design is a later pass.
HONEY_TREE = "encounters_honey_tree"          # common / uncommon / rare
GREAT_MARSH_LOOKOUT = "encounters_great_marsh_lookout"  # binocular pools
TROPHY_GARDEN = "encounters_trophy_garden"    # daily_encounters, 16 species
HONEY_TREE_KEYS = ("common", "uncommon", "rare")
GREAT_MARSH_KEYS = ("before_national_dex", "after_national_dex")
DAILY_KEY = "daily_encounters"

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

    # -- water -----------------------------------------------------------

    def kind_slots(self, kind):
        """[(species, lo, hi)] for any table kind, or [] when absent.

        Water slots carry a level range where land carries one level, so they
        are returned in the three-element form the analysis layer normalises
        to. Land is returned the same way for uniformity.
        """
        from . import analysis
        key, _, _ = analysis.TABLE_KINDS[kind]
        rows = self.data.get(key)
        if not isinstance(rows, list) or not rows:
            return []
        out = []
        for e in rows:
            if "level" in e:
                out.append((e["species"], e["level"], e["level"]))
            else:
                lo, hi = e["level_min"], e["level_max"]
                out.append((e["species"], min(lo, hi), max(lo, hi)))
        return out

    def kind_rate(self, kind):
        from . import analysis
        _, rate_key, _ = analysis.TABLE_KINDS[kind]
        return self.data.get(rate_key, 0)

    def kinds_present(self):
        """The table kinds this area actually has, in menu order."""
        from . import analysis
        return [k for k in analysis.TABLE_KINDS
                if self.kind_slots(k) and self.kind_rate(k)]

    def set_water_slot(self, kind, index, species=None,
                       level_min=None, level_max=None):
        """Rewrite one water slot. Land goes through set_slot instead."""
        from . import analysis
        if kind == "land":
            raise ValueError("use set_slot for land tables")
        key, _, rates = analysis.TABLE_KINDS[kind]
        if not 0 <= index < len(rates):
            raise IndexError(f"{kind} slot {index} out of range")
        if species is not None:
            self._replace([key, index, "species"], species)
        if level_min is not None:
            self._replace([key, index, "level_min"], int(level_min))
        if level_max is not None:
            self._replace([key, index, "level_max"], int(level_max))

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

    def set_kind_rate(self, kind, rate):
        """The encounter rate of any table kind (land_rate, surf_rate, the
        three rod rates)."""
        from . import analysis
        _, rate_key, _ = analysis.TABLE_KINDS[kind]
        self._replace([rate_key], int(rate))

    def set_time_slot(self, layer, index, species):
        """day/night carry two species each, standing in for slots 2 and 3.
        Writing anywhere else would be illegal per R7, so it is refused here
        rather than left for the linter to catch after the fact."""
        if layer not in ("day", "night"):
            raise ValueError(f"not a time-of-day layer: {layer}")
        if index not in (0, 1):
            raise IndexError(f"{layer} has two entries, not {index + 1}")
        self._replace([layer, index], species)

    def _set_list_species(self, key, index, species):
        size = LIST_KEY_SIZES.get(key)
        if size is None:
            raise ValueError(f"not a species list: {key}")
        if not 0 <= index < size:
            raise IndexError(f"{key} has {size} entries, not {index + 1}")
        if not isinstance(self.data.get(key), list):
            raise KeyError(f"{self.name} has no {key} list")
        self._replace([key, index], species)

    def set_swarm(self, index, species):
        """The two swarm species, which replace slots 0-1 while a swarm is on."""
        self._set_list_species(SWARM_KEY, index, species)

    def set_radar(self, index, species):
        """The four Poke Radar species, which replace slots 4-5."""
        self._set_list_species(RADAR_KEY, index, species)

    def set_dual_slot(self, game, index, species):
        """One of the five dual-slot lists (ruby, sapphire, emerald, firered,
        leafgreen), each two species standing in for slots 8-9."""
        if game not in DUAL_SLOT_KEYS:
            raise ValueError(f"not a dual-slot game: {game}")
        self._set_list_species(game, index, species)

    def reference_species(self):
        """Every species reference in the file, {key: [species]} in the
        file's own order. The audit reads this. Water slots holding
        SPECIES_NONE are the empty marker, not a reference, and are dropped."""
        from . import analysis
        out = {}
        for kind, (key, _, _) in analysis.TABLE_KINDS.items():
            rows = self.data.get(key)
            if isinstance(rows, list) and rows:
                vals = [e["species"] for e in rows if e["species"] != "SPECIES_NONE"]
                if vals:
                    out[key] = vals
        for key in (SWARM_KEY, "day", "night", RADAR_KEY, *DUAL_SLOT_KEYS,
                    *HONEY_TREE_KEYS, *GREAT_MARSH_KEYS, DAILY_KEY):
            vals = self.data.get(key)
            if isinstance(vals, list) and vals:
                out[key] = list(vals)
        return out

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
        for layer in ("day", "night", "swarms", "radar", *DUAL_SLOT_KEYS):
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


# -- the species-only sources ---------------------------------------------
#
# Three encounter sources the land format does not cover. Read for the audit
# (species only); nothing writes them yet, their design is a later pass.


def honey_tree_species(ref=None):
    """{common|uncommon|rare: [six species]}."""
    d = load_area(HONEY_TREE, ref).data
    return {k: list(d[k]) for k in HONEY_TREE_KEYS}


def great_marsh_lookout_species(ref=None):
    """{before_national_dex|after_national_dex: [32 species]}, the pools the
    lookout binoculars draw from."""
    d = load_area(GREAT_MARSH_LOOKOUT, ref).data
    return {k: list(d[k]) for k in GREAT_MARSH_KEYS}


def trophy_garden_daily_species(ref=None):
    """The 16 species Mr. Backlot's garden rotates through, from the same
    file as the garden's own land table."""
    return list(load_area(TROPHY_GARDEN, ref).data[DAILY_KEY])


# -- the sidecar ----------------------------------------------------------
#
# Design intent that the decomp format has nowhere to put. Hand-editable on
# purpose: it is what Ian diffs when he wants to know why a route looks the
# way it does. Archetype assignment waits for M2, which is what can measure
# fit; M1 writes only what can be derived without the analysis engine.


# -- the caught record ------------------------------------------------------
#
# Per-playthrough state, not design intent, so it is gitignored rather than
# living in the sidecar. {area: species}: one encounter per area, the
# nuzlocke model the dupes clause comes from.

CAUGHT_FILE = os.path.join("docs", "oxide", "encounters", "caught.json")


def load_encounters():
    path = os.path.join(repo_root(), CAUGHT_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            return dict(json.load(f).get("encounters") or {})
    except (FileNotFoundError, ValueError):
        return {}


def save_encounters(encounters):
    path = os.path.join(repo_root(), CAUGHT_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"encounters": dict(sorted(encounters.items()))}, f,
                  indent=2)
        f.write("\n")


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
