"""The trainer team builder's model (build plan item 28, Ian, 2026-09-27).

Every trainer is one file under res/trainers/data/, which the packer
(tools/dataproc/src/trainerproc.c) turns into the game's trainer archives.
This module reads those files for the Trainers tab: a list of every trainer
with its split and level cap, and one trainer's team as the game builds it
in battle (nature, ability, gender and default moves come from
calc_trainers, which follows TrainerData_BuildParty).

The split is the balance track's placement, read without building any party
so the whole list costs about three seconds once: a story fight's split from
fights.json, else the split B6 places the trainer in, else the maps that
field it. It is the order teamscore.resolve uses, and test_trainers holds
the two to the same answer. A trainer with no split (the dummies, and the
slots no map fields) has no cap and no score.

Saving (piece 3) edits the file's text field by field with jsonstyle, never
a reformat, so a change is an ordinary git diff. A save runs the trainer lint
first and refuses on an error, then runs the real packer over the folder it
wrote to and puts the file back if the packer refuses, and then registers
the trainer in trainers_diverged.json beside the base ROM importer, which
otherwise carries the base ROM's team back.
"""
import datetime
import functools
import json
import os
import re
import subprocess
import tempfile
import threading

from . import calc_trainers
from . import dex
from . import model
from . import pokedex
from .. import jsonstyle

DATA = ("res", "trainers", "data")
REGISTRY = ("tools", "oxide", "trainers_diverged.json")
PACKER = ("build", "tools", "dataproc", "trainerproc")
# A member's keys in the order the files keep them; a key a member lacks goes
# in after the nearest one before it that it has.
MEMBER_ORDER = ["species", "form", "level", "item", "moves", "iv_scale", "nature",
                "ball_seal", "ability", "gender"]
# The trainer's own fields the builder edits; the rest of the header is left
# as it is.
HEADER_EDITS = ("ai_flags", "double_battle")
CHOICE_ITEMS = {"ITEM_CHOICE_BAND", "ITEM_CHOICE_SPECS", "ITEM_CHOICE_SCARF"}
# enum TrainerMonAbility: 0 either ordinary slot by personality, 1 and 2 that
# slot, 3 the hidden ability (1832a346c).
ABILITY_CHOICES = {0: "either, by personality", 1: "slot 1", 2: "slot 2", 3: "hidden"}


def data_dir(root):
    """The trainer folder. OXIDE_TRAINERS_DIR points a test server at a
    scratch copy, so a save can be tried end to end without touching res/."""
    return os.environ.get("OXIDE_TRAINERS_DIR") or os.path.join(root, *DATA)


def registry_path(root):
    """The divergence registry, which OXIDE_TRAINERS_REGISTRY can point at a
    scratch copy alongside OXIDE_TRAINERS_DIR."""
    return os.environ.get("OXIDE_TRAINERS_REGISTRY") or os.path.join(root, *REGISTRY)


def path_of(root, stem):
    return os.path.join(data_dir(root), stem + ".json")


def stems(root):
    return sorted(f[:-5] for f in os.listdir(data_dir(root)) if f.endswith(".json"))


def load(root, stem):
    """The trainer's file as JSON. A stem is a file name, never a path."""
    if not stem or "/" in stem or "\\" in stem or stem.startswith("."):
        raise KeyError(stem)
    with open(path_of(root, stem), encoding="utf-8") as f:
        return json.load(f)


def _stamp(root):
    """Changes whenever a trainer file does, so the list is rebuilt after a save."""
    base = data_dir(root)
    return max(os.stat(os.path.join(base, f)).st_mtime_ns for f in os.listdir(base))


@functools.lru_cache(maxsize=1)
def split_map(root):
    """{stem: split or None}, placed as teamscore.resolve places a fight."""
    from ..balance import b6, data as bdata, splits as bsplits
    ids = calc_trainers._tables(root)["ids"]
    story = {}
    for fight in bdata.fights()["fights"]:
        for tr in fight["tr_ids"]:
            story.setdefault(tr, fight["split"])
    placed = b6.placements()
    out = {}
    for stem in stems(root):
        tr = ids.get("TRAINER_" + stem.upper())
        if tr is None:
            out[stem] = None
            continue
        out[stem] = story.get(tr) or (placed.get(tr) or {}).get("split") \
            or bsplits.trainer_split(tr)
    return out


@functools.lru_cache(maxsize=1)
def caps():
    """{split: level cap}, the balance track's, which its tests hold to the engine's."""
    from ..balance import pool
    return dict(pool.caps())


def split_order():
    from ..balance import pool
    return list(pool.SPLITS)


def summary(root=None):
    """One row per trainer for the list, rebuilt when a trainer file changes,
    each with its stored score (or None) for the list to sort by."""
    root = root or model.repo_root()
    scores = stored_scores(root)
    return [dict(r, score=scores.get(r["stem"])) for r in _summary(root, _stamp(root))]


# -- the stored scores (Ian, 2026-09-27) ------------------------------------------
# The list sorts by the numbers the balance plan reports, read from the
# balance track's stored results without scoring anything: a story fight's
# from pressure.json (Hesperid's two from calibrate.json), shared by every
# variant of it (Barry's three starters), and an ordinary trainer's from
# b6.json. Each goes onto Ian's fight scale by the plan's own line. A team
# saved since its last rescore shows the score from before the save. When the
# Balance Agent's rebuilt score lands, this function is the one to repoint.

def _score_files():
    from ..balance import b6, calibrate, pressure
    return tuple(p for p in (pressure.OUT, calibrate.OUT, b6.OUT) if os.path.exists(p))


def stored_scores(root=None):
    """{stem: {"scale", "band", "fight"}} for every trainer with a stored score;
    "fight" is the story fight's key, or None for an ordinary trainer."""
    root = root or model.repo_root()
    files = _score_files()
    return _stored_scores(root, tuple(os.stat(p).st_mtime_ns for p in files))


@functools.lru_cache(maxsize=2)
def _stored_scores(root, stamp):
    from ..balance import b6, calibrate, data as bdata
    try:
        line = b6.scale_line()
    except (KeyError, ZeroDivisionError):  # no stored story fights to draw the line from
        return {}
    stem_of = {tr: name[len("TRAINER_"):].lower()
               for name, tr in calc_trainers._tables(root)["ids"].items()}
    rate = lambda safe: round(b6.on_scale(safe, line), 1)
    out = {}
    for tr, r in b6.load().get("trainers", {}).items():
        stem = stem_of.get(int(tr))
        if stem and r.get("safe") is not None:
            out[stem] = {"scale": rate(r["safe"]), "fight": None}
    stories = b6.story_scores()
    fights = [(f["key"], f["tr_ids"]) for f in bdata.fights()["fights"]]
    by_constant = {name: tr for name, tr in calc_trainers._tables(root)["ids"].items()}
    fights += [(key, [by_constant[c]]) for c, _split, key, _label in calibrate.EXTRA if c in by_constant]
    for key, ids in fights:
        r = stories.get(key)
        if not r or r.get("safe") is None:
            continue
        for tr in ids:
            stem = stem_of.get(tr)
            if stem:
                out[stem] = {"scale": rate(r["safe"]), "fight": key}
    for v in out.values():
        v["band"] = b6.band(v["scale"])
    return out


@functools.lru_cache(maxsize=2)
def _summary(root, stamp):
    places, cap = split_map(root), caps()
    rows = []
    for stem in stems(root):
        data = load(root, stem)
        party = data.get("party") or []
        split = places.get(stem)
        rows.append({
            "stem": stem, "name": data.get("name", ""), "label": calc_trainers.trainer_name(root, data, stem),
            "class": data.get("class"), "split": split, "cap": cap.get(split),
            "double": bool(data.get("double_battle")),
            "party": [{"species": m["species"], "level": m["level"]} for m in party],
            "top": max((m["level"] for m in party), default=0),
        })
    return rows


def _ability_options(root, species, form):
    """The names a party member's ability value can give, from the record the
    game reads: the form's own where it has one (f801cc160)."""
    folder = calc_trainers.FORM_FOLDERS.get((species, form or 0))
    record = calc_trainers._raw_species(root, species, folder)
    a1, a2, hidden = (record["abilities"] + ["ABILITY_NONE"] * 3)[:3]
    tidy = lambda a: None if a == "ABILITY_NONE" else a.replace("ABILITY_", "")
    return {"1": tidy(a1), "2": tidy(a2), "hidden": tidy(hidden)}


def _default_move_ids(root, member):
    folder = calc_trainers.FORM_FOLDERS.get((member["species"], member.get("form") or 0))
    record = calc_trainers._raw_species(root, member["species"], folder)
    learnset = [tuple(e) for e in (record.get("learnset") or {}).get("by_level") or []]
    return calc_trainers.default_moves(learnset, member["level"])


def detail(root, stem, data=None):
    """One trainer's team, as the file has it and as the game builds it.
    `data` is an unsaved edit of the file, shown the same way."""
    data = data if data is not None else load(root, stem)
    moves = pokedex.moves(root)
    built = calc_trainers.build_trainer(root, stem, data)
    party = data.get("party") or []
    split = split_map(root).get(stem)
    members = []
    for m, (showdown, s) in zip(party, built):
        rec = pokedex.load(root, m["species"]) or {}
        file_moves = m.get("moves")
        members.append({
            "file": m,
            "name": dex.display_name(m["species"]),
            "folder": rec.get("folder"),
            "types": rec.get("types") or [],
            "stats": rec.get("stats") or {},
            "abilities": _ability_options(root, m["species"], m.get("form")),
            "iv": m["iv_scale"] * calc_trainers.MAX_IV // calc_trainers.MAX_IV_SCALE,
            "built": {"nature": s["nature"], "ability": s["ability"], "gender": s["gender"],
                      "moves": s["moves"], "item": s.get("item"),
                      "default_moves": not isinstance(file_moves, list)},
            "move_names": [(moves.get(mv) or {}).get("name", mv)
                           for mv in (file_moves or []) if mv and mv != "MOVE_NONE"],
            # The level-up default as move constants, the starting point when
            # a trainer that lists no moves is given some.
            "default_move_ids": _default_move_ids(root, m),
            "calc_name": showdown,
        })
    return {
        "data": data,
        "stem": stem, "label": calc_trainers.trainer_name(root, data, stem),
        "name": data.get("name", ""), "class": data.get("class"),
        "ai_flags": data.get("ai_flags") or [], "double_battle": bool(data.get("double_battle")),
        "items": data.get("items") or [], "split": split, "cap": caps().get(split),
        "members": members,
        "all_ai_flags": ai_flags(root, data.get("ai_flags") or []),
        "ability_choices": ABILITY_CHOICES,
    }


def preview(root, stem, data):
    """An unsaved edit rebuilt as the game would build it, with its lint and
    the instant score. Nothing is written. A team the lint rejects may not
    build at all, and then only the findings come back."""
    findings = lint(root, data)
    try:
        shown = detail(root, stem, data)
    except (KeyError, ValueError, TypeError, IndexError, FileNotFoundError):
        shown = None
    errors = any(f["severity"] == "error" for f in findings)
    return {"detail": shown, "findings": findings,
            "estimate": None if errors or shown is None else estimate(stem, data)}


# -- the score (piece 4), agreed with the Balance Agent -----------------------------
# The tool never scores by itself: both numbers are the balance track's
# teamscore.py, which places the fight (a story fight's variants and tag
# partner, weather, Trick Room) and returns the split and its cap.

def estimate(stem, data=None):
    """teamscore.estimate: the instant number for every edit, 0.01 to 0.06 s
    once warm. {"error": why} for a trainer it does not score."""
    from ..balance import teamscore
    try:
        return teamscore.estimate(stem, data)
    except Exception as exc:              # a trainer with no capped split, or a team it cannot build
        return {"error": str(exc)}


def warm():
    """The estimate's first call builds the calculator data and every split's
    side, about 4 to 9 seconds; the server does it at start, off to one side."""
    from ..balance import pool, teamscore
    for split in pool.SPLITS:
        try:
            teamscore.side(split)
        except Exception:
            pass


_SCORING = threading.Lock()


def full_score(stem, data=None):
    """teamscore.score, the balance plan's own number: one Node process, 1 s
    early in the game to 20 s late. One at a time, pinned to one core; the
    affinity is this thread's, which the Node process inherits."""
    from ..balance import teamscore
    if not _SCORING.acquire(blocking=False):
        return {"error": "a score is already running; one at a time"}
    cores = sorted(os.sched_getaffinity(0))
    try:
        os.sched_setaffinity(0, {cores[-1]})
        return teamscore.score(stem, data)
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        os.sched_setaffinity(0, set(cores))
        _SCORING.release()


def choices(root):
    """What the editor offers: every species, move, item and nature by name.
    A move also carries its type, which colours its box in the editor."""
    moves = pokedex.moves(root)
    tidy = lambda c, p: c[len(p):].replace("_", " ").title()
    e = enums(root)
    return {
        "moves": sorted(([c, r.get("name") or c, r.get("type") or ""] for c, r in moves.items()
                         if c != "MOVE_NONE" and "(Special)" not in (r.get("name") or "")),
                        key=lambda x: x[1]),
        "items": sorted(([c, tidy(c, "ITEM_")] for c in e["items"] if c != "ITEM_NONE"),
                        key=lambda x: x[1]),
        "natures": [[c, tidy(c, "NATURE_")] for c in e["natures"]],
        "species": sorted(([c, dex.display_name(c)] for c in e["species"]), key=lambda x: x[1]),
        "forms": e["forms"],
    }


def ai_flags(root, chosen=()):
    """The AI flags in bit order: every named one, and an unused bit only
    when this trainer sets it, since nothing reads those."""
    bits = calc_trainers._tables(root)["ai_bits"]
    return [f for f in sorted(bits, key=bits.get)
            if not f.startswith("AI_FLAG_UNUSED") or f in chosen]


# -- the trainer lint -----------------------------------------------------------

@functools.lru_cache(maxsize=2)
def enums(root):
    """The names the packer accepts, from the generated lists it is built with,
    and each species' form count from include/constants/forms.h."""
    def lines(name):
        with open(os.path.join(root, "generated", name + ".txt"), encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    with open(os.path.join(root, "include", "constants", "forms.h"), encoding="utf-8") as f:
        forms = {"SPECIES_" + name: int(n) for name, n in
                 re.findall(r"#define (\w+)_FORM_COUNT\s+(\d+)", f.read())}
    return {"species": set(lines("species")) - {"SPECIES_NONE", "SPECIES_EGG"},
            "items": set(lines("items")), "natures": lines("natures")[:25],
            "forms": forms}


def lint(root, data):
    """[{severity, member, message}] for one trainer, member None for the
    trainer itself. An error is anything the packer would refuse or the game
    would get wrong; a warning is legal but worth a look."""
    e, out = enums(root), []
    moves = pokedex.moves(root)
    flags = set(calc_trainers._tables(root)["ai_bits"])

    def add(severity, member, message):
        out.append({"severity": severity, "member": member, "message": message})
    party = data.get("party") or []
    if not 1 <= len(party) <= 6:
        add("error", None, f"a party holds 1 to 6 Pokemon, not {len(party)}")
    if data.get("double_battle") and len(party) < 2:
        add("error", None, "a double battle needs at least two Pokemon")
    for f in data.get("ai_flags") or []:
        if f not in flags:
            add("error", None, f"{f} is not an AI flag")
    # The packer reads the first member to decide whether the party carries
    # moves and items at all (a list of moves, an item name; null or no key
    # is none), so every member must match it.
    carries = {"moves": lambda m: isinstance(m.get("moves"), list),
               "item": lambda m: isinstance(m.get("item"), str)}
    for key, has in carries.items():
        if party and len({has(m) for m in party}) > 1:
            add("error", None, f"every Pokemon lists {key} or none does")
    for i, m in enumerate(party):
        sp = m.get("species")
        if sp not in e["species"]:
            add("error", i, f"{sp} is not a species")
            continue
        form = m.get("form", 0)
        if not isinstance(form, int) or not 0 <= form < e["forms"].get(sp, 1):
            add("error", i, f"form {form} does not exist for {dex.display_name(sp)}")
        level = m.get("level")
        if not isinstance(level, int) or not 1 <= level <= 100:
            add("error", i, f"level {level} is outside 1 to 100")
        iv = m.get("iv_scale")
        if not isinstance(iv, int) or not 0 <= iv <= 255:
            add("error", i, f"IV scale {iv} is outside 0 to 255")
        if isinstance(m.get("item"), str):
            if m["item"] not in e["items"]:
                add("error", i, f"{m['item']} is not an item")
            elif m["item"] in CHOICE_ITEMS:
                add("warn", i, f"{m['item'].replace('ITEM_', '').replace('_', ' ').title()}: "
                    "Ian wants Choice items nearly gone (2026-09-26)")
        if isinstance(m.get("moves"), list):
            real = [mv for mv in m["moves"] if mv and mv != "MOVE_NONE"]
            if not real or len(m["moves"]) > 4:
                add("error", i, "a Pokemon lists one to four moves")
            for mv in real:
                if mv not in moves:
                    add("error", i, f"{mv} is not a move")
            if len(set(real)) != len(real):
                add("error", i, "the same move is listed twice")
        nature = m.get("nature")
        if nature is not None and nature not in e["natures"]:
            add("error", i, f"{nature} is not one of the 25 natures")
        ability = m.get("ability", 0)
        if ability not in ABILITY_CHOICES:
            add("error", i, f"ability {ability} is not 0, 1, 2 or 3")
        else:
            names = _ability_options(root, sp, form if isinstance(form, int) else 0)
            if ability == 2 and not names["2"]:
                add("warn", i, "slot 2 is empty for this species, so it takes slot 1")
            if ability == 3 and not names["hidden"]:
                add("warn", i, "no hidden ability here, so it keeps its ordinary one")
        gender = m.get("gender")
        ratio = (pokedex.load(root, sp) or {}).get("gender_ratio", "")
        if gender not in (None, "male", "female"):
            add("error", i, f"gender {gender!r} is not male, female or null")
        elif gender and ratio.endswith("NO_GENDER"):
            add("error", i, "this species has no gender")
        elif gender == "female" and ratio.endswith("MALE_ONLY"):
            add("error", i, "this species is male only")
        elif gender == "male" and ratio.endswith("FEMALE_ONLY"):
            add("error", i, "this species is female only")
    return out


# -- saving ----------------------------------------------------------------------

class SaveRefused(Exception):
    def __init__(self, message, findings=()):
        super().__init__(message)
        self.findings = list(findings)


def _after(member_keys, key):
    """The key a new `key` is inserted after in a member."""
    idx = MEMBER_ORDER.index(key) if key in MEMBER_ORDER else len(MEMBER_ORDER)
    for k in reversed(MEMBER_ORDER[:idx]):
        if k in member_keys:
            return k
    return list(member_keys)[-1]


def _dump(value, indent):
    """A value as the trainer files write it: every list one element a line,
    however short, and an empty one as []. jsonstyle's default puts a list of
    one or two on one line, which in these files would change 361 AI flag
    lists and 11 move lists that are not being edited."""
    return jsonstyle.dumps(value, indent, max_inline=0, empty_array="[]")


def dump_party(party, indent):
    """The party array as the files write it (all 928 match but the empty one)."""
    return _dump(party, indent)


def _replace(text, path, value):
    """jsonstyle.replace_value, in the trainer files' own list style."""
    vs, ve, indent = jsonstyle._find_key(text, path)
    return text[:vs] + _dump(value, indent) + text[ve:]


def edit_text(text, new):
    """The file's text with `new`'s editable fields written into it, and the
    list of what changed. Only the fields that differ are touched."""
    old = json.loads(text)
    changed = []
    # A field left null that the file never had (no named nature, say) stays
    # out of the file rather than appearing as null.
    new = dict(new, party=[
        {k: v for k, v in m.items()
         if v is not None or (i < len(old.get("party") or []) and k in old["party"][i])}
        for i, m in enumerate(new.get("party") or [])])
    for key in set(old) | set(new):
        if key in HEADER_EDITS or key == "party":
            continue
        if old.get(key) != new.get(key):
            raise SaveRefused(f"{key} is not edited here; only the team, the AI flags "
                              "and the battle type are")
    for key in HEADER_EDITS:
        if old.get(key) != new.get(key):
            text = _replace(text, [key], new.get(key))
            changed.append(key)
    old_party, new_party = old.get("party") or [], new.get("party") or []
    if len(old_party) != len(new_party):
        vs, ve, indent = jsonstyle._find_key(text, ["party"])
        text = text[:vs] + dump_party(new_party, indent) + text[ve:]
        changed.append(f"party: {len(old_party)} to {len(new_party)} Pokemon")
    else:
        for i, (om, nm) in enumerate(zip(old_party, new_party)):
            for key in [k for k in MEMBER_ORDER if k in nm] + [k for k in nm if k not in MEMBER_ORDER]:
                if key not in om:
                    text = jsonstyle.insert_key(text, ["party", i], _after(om, key), key, nm[key])
                    if isinstance(nm[key], list):      # insert_key writes a short list inline
                        text = _replace(text, ["party", i, key], nm[key])
                    om = dict(om, **{key: nm[key]})
                    changed.append(f"party[{i}].{key}")
                elif om[key] != nm[key]:
                    text = _replace(text, ["party", i, key], nm[key])
                    changed.append(f"party[{i}].{key}")
            for key in om:
                if key not in nm:
                    raise SaveRefused(f"party[{i}] drops {key}; a field is set to null, not removed")
    if json.loads(text) != new:
        raise SaveRefused("the edited text does not read back as the team sent; nothing was written")
    return text, changed


def pack_check(root, data_dir):
    """(ok, message): the real packer over the folder, into a scratch folder."""
    exe = os.path.join(root, *PACKER)
    header = os.path.join(root, "build", "generated", "trainers.h")
    if not (os.path.exists(exe) and os.path.exists(header)):
        return None, "the packer is not built in this checkout, so the save was not packed"
    with tempfile.TemporaryDirectory() as out:
        r = subprocess.run([exe, "-M", os.path.join(out, "trainers.d"), "-o", out, header, data_dir],
                           capture_output=True, text=True, timeout=180)
    message = (r.stderr or r.stdout).strip()[-2000:]
    # A packer built before its source last changed judges by the old rules
    # (it refused ability 3 on 2026-09-27 until rebuilt), so say so.
    source = os.path.join(root, "tools", "dataproc", "src", "trainerproc.c")
    if os.path.getmtime(source) > os.path.getmtime(exe):
        message = ("the packer is older than its source; rebuild it with "
                   "`ninja -C build -j2 tools/dataproc/trainerproc`. " + message).strip()
    return r.returncode == 0, message


def register(root, stem, fields, registry=None):
    """Record the trainer's edited fields as intended divergences from the
    base ROM, so import_base_rom.py leaves them alone."""
    path = registry or registry_path(root)
    try:
        with open(path, encoding="utf-8") as f:
            reg = json.load(f)
    except FileNotFoundError:
        reg = {}
    why = f"edited in the OxiDex team builder, {datetime.date.today().isoformat()}"
    entry = reg.setdefault(stem, {})
    for field in fields:
        entry.setdefault(field, why)
    ordered = {k: reg[k] for k in sorted(reg)}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ordered, indent=2) + "\n")


def save(root, stem, new, folder=None, registry=None):
    """Write an edited trainer. `folder` and `registry` point a test at a
    scratch copy; by default they are the tree's own. Returns what changed."""
    findings = lint(root, new)
    if any(f["severity"] == "error" for f in findings):
        raise SaveRefused("the trainer lint found errors; nothing was written", findings)
    folder = folder or data_dir(root)
    if not stem or "/" in stem or "\\" in stem or stem.startswith("."):
        raise SaveRefused(f"not a trainer: {stem}")
    path = os.path.join(folder, stem + ".json")
    with open(path, encoding="utf-8") as f:
        before = f.read()
    text, changed = edit_text(before, new)
    if not changed:
        return {"changed": [], "findings": findings, "packer": None}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    ok, message = pack_check(root, folder)
    if ok is False:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(before)
        raise SaveRefused("the packer refused the edited file, so it was put back: " + message,
                          findings)
    fields = sorted({"party" if c.startswith("party") else c for c in changed})
    register(root, stem, fields, registry)
    return {"changed": changed, "findings": findings, "packer": message if ok is None else "packed"}
