"""The alpha checklist's feedback (alpha readiness step 17, checks 3 and 6):
what Ian writes beside each trainer, gauntlet section and zone in the alpha
run, kept for one playthrough and exported for the other sessions.

Each note is one entry under a key the page gives it: a trainer's row key
("barry_1", "TRAINER_YOUNGSTER_TRISTAN"), "gauntlet:<split>:<section>" for a
gauntlet section, or "zone:<split>:<zone>" for a zone. An entry holds:

  fought   whether Ian fought it (the page also ticks it from the save)
  rating   1 to 10, for bosses and gauntlet sections (the run plan's item 7)
  note     free text
  death    {"mon", "killer", "saw"}: which Pokemon died, what killed it,
           and whether Ian saw it coming ("yes" or "no"); the fight is the
           row the note sits on
  stamp    when it was written, the ROM's commit (from the watched save's
           file name, which melonDS takes from the ROM's), the badges, the
           split and the party (from the save), the zone (from the row), and
           the battle on screen when the live bridge answers

The local file (docs/oxide/encounters/alpha-feedback.json) is gitignored, as
caught.json is: it belongs to one playthrough. Export writes it to
alpha-notes.json beside it, which "Commit my edits" may commit, and a
readable alpha-notes.md; when the local file is missing (a new checkout, a
cleared run) the export is read back in its place. A new run moves the local
file aside under its start date and starts empty.

OXIDE_ALPHA_DIR points all three files at a scratch folder, so the tests
never touch Ian's notes.
"""
import datetime
import json
import os
import re
import urllib.request

from . import model

FOLDER = os.path.join("docs", "oxide", "encounters")
LOCAL = "alpha-feedback.json"
EXPORT = "alpha-notes.json"
EXPORT_MD = "alpha-notes.md"
BRIDGE = "http://127.0.0.1:31124"
ROM_NAME = re.compile(r"pokeplatinum-oxide(?:-testkit)?-([0-9a-f]{7,40})", re.I)


def folder(root=None):
    return os.environ.get("OXIDE_ALPHA_DIR") or os.path.join(root or model.repo_root(), FOLDER)


def _empty():
    return {"run": None, "started": None, "notes": {}}


def _read(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("notes"), dict):
        raise ValueError(f"{path} is not an alpha notes file")
    return data


def load(root=None):
    """The current run's notes: the local file, else the export read back,
    else an empty run. {"run", "started", "notes", "from"}."""
    base = folder(root)
    for name, where in ((LOCAL, "local"), (EXPORT, "export")):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return dict(_read(path), **{"from": where})
    return dict(_empty(), **{"from": None})


def _write(root, store):
    path = os.path.join(folder(root), LOCAL)
    body = {k: store.get(k) for k in ("run", "started", "notes")}
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def _bridge_battle(timeout=0.4):
    """The battle on screen, from melonDS-oxide's /battle_state, or None when
    the bridge is not running or no battle is on. Species are the game's
    numbers; the reader names them."""
    try:
        with urllib.request.urlopen(BRIDGE + "/battle_state", timeout=timeout) as r:
            state = json.loads(r.read())
    except Exception:
        return None
    if not state.get("inBattle"):
        return None
    side = lambda xs: [{k: x.get(k) for k in ("species", "level", "currentHp", "maxHp")}
                       for x in (xs or [])]
    return {"turn": state.get("turn"), "player": side(state.get("playerActive")),
            "enemy": side(state.get("enemyActive"))}


def stamp(zone, split, raw=None, bridge=True):
    """What a note is stamped with. `raw` is the save watcher's (bytes, save,
    seq, path); every field the save or the bridge cannot answer is None."""
    from . import savefile
    _data, save, _seq, path = raw or (None, None, None, None)
    rom = ROM_NAME.search(os.path.basename(path or ""))
    out = {"at": datetime.datetime.now().isoformat(timespec="seconds"),
           "rom": rom.group(1) if rom else None, "save": os.path.basename(path) if path else None,
           "zone": zone, "split": split, "badges": None, "save_split": None, "party": None,
           "battle": _bridge_battle() if bridge else None}
    if save:
        progress = save.get("progress") or {}
        out["badges"] = progress.get("badges")
        out["save_split"] = (progress.get("split") or {}).get("name")
        out["party"] = [savefile.describe(m) for m in save.get("party") or []]
    return out


def _clean(fields):
    """The editable fields, checked: a rating 1 to 10 or none, a death note's
    three parts as text, "yes", "no" or none for whether it was seen."""
    out = {}
    if "fought" in fields:
        out["fought"] = bool(fields["fought"])
    if "rating" in fields:
        r = fields["rating"]
        if r in (None, ""):
            out["rating"] = None
        elif isinstance(r, (int, str)) and str(r).isdigit() and 1 <= int(r) <= 10:
            out["rating"] = int(r)
        else:
            raise ValueError(f"a rating is 1 to 10, not {r!r}")
    if "note" in fields:
        out["note"] = str(fields["note"] or "")[:4000]
    if "death" in fields:
        d = fields["death"]
        if not d:
            out["death"] = None
        elif isinstance(d, dict):
            saw = d.get("saw")
            if saw not in (None, "", "yes", "no"):
                raise ValueError(f"saw it coming is yes or no, not {saw!r}")
            out["death"] = {"mon": str(d.get("mon") or "")[:200], "killer": str(d.get("killer") or "")[:400],
                            "saw": saw or None}
        else:
            raise ValueError("a death note is {mon, killer, saw}")
    return out


def record(root, key, fields, label="", zone=None, split=None, raw=None, bridge=True):
    """Saves one note's fields, stamped now, and returns the entry."""
    if not key or len(key) > 200:
        raise ValueError("which row?")
    store = load(root)
    if not store.get("started"):
        store["started"] = datetime.date.today().isoformat()
    entry = dict(store["notes"].get(key) or {})
    entry.update(_clean(fields))
    entry.update(label=label or entry.get("label") or key, zone=zone or entry.get("zone"),
                 split=split or entry.get("split"))
    entry["stamp"] = stamp(entry["zone"], entry["split"], raw, bridge)
    entry.setdefault("first", entry["stamp"]["at"])
    store["notes"][key] = entry
    _write(root, store)
    return entry


def new_run(root, name=None):
    """Moves the current run's local file aside under its start date and
    starts an empty one."""
    base = folder(root)
    store = load(root)
    path = os.path.join(base, LOCAL)
    if os.path.exists(path):
        when = store.get("started") or datetime.date.today().isoformat()
        aside = os.path.join(base, f"alpha-feedback-{when}.json")
        n = 2
        while os.path.exists(aside):
            aside = os.path.join(base, f"alpha-feedback-{when}-{n}.json")
            n += 1
        os.replace(path, aside)
    _write(root, dict(_empty(), run=name or None, started=datetime.date.today().isoformat()))
    return load(root)


def export(root=None, order=None):
    """Writes the run's notes to alpha-notes.json (the store as it is, which
    load() reads back) and alpha-notes.md (the same, readable, in walking
    order where `order` gives it: [(split, zone)]). Returns their paths."""
    base = folder(root)
    store = load(root)
    body = {k: store.get(k) for k in ("run", "started", "notes")}
    jpath, mpath = os.path.join(base, EXPORT), os.path.join(base, EXPORT_MD)
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(markdown(body, order))
    return [jpath, mpath]


def markdown(store, order=None):
    """The notes as Markdown for the other sessions: by split and zone, each
    note with its rating, its death note and its stamp."""
    rank = {k: i for i, k in enumerate(order or [])}
    notes = sorted(store["notes"].items(), key=lambda kv: (
        rank.get((kv[1].get("split"), kv[1].get("zone")), 1e9), kv[1].get("split") or "",
        kv[1].get("zone") or "", kv[0]))
    lines = ["# Alpha run notes", "",
             "Exported from the OxiDex's Alpha tab (tools/oxide/encounters/alphanotes.py). "
             "The JSON beside this file is the same notes, which the tool reads back.", ""]
    if store.get("run") or store.get("started"):
        lines += [f"Run: {store.get('run') or 'unnamed'}, started {store.get('started') or 'unknown'}.", ""]
    if not notes:
        lines.append("No notes yet.")
    where = None
    for key, e in notes:
        here = (e.get("split"), e.get("zone"))
        if here != where:
            lines += ["", f"## {e.get('zone') or 'Anywhere'} ({e.get('split') or 'no split'})", ""]
            where = here
        bits = [f"**{e.get('label') or key}**"]
        if e.get("fought"):
            bits.append("fought")
        if e.get("rating"):
            bits.append(f"rated {e['rating']} of 10")
        lines.append("- " + ", ".join(bits) + (f": {e['note']}" if e.get("note") else ""))
        d = e.get("death")
        if d:
            seen = {"yes": "saw it coming", "no": "did not see it coming"}.get(d.get("saw"), "")
            lines.append(f"  - Death: {d.get('mon') or 'a Pokemon'}, killed by {d.get('killer') or 'unknown'}"
                         + (f"; {seen}" if seen else "") + ".")
        s = e.get("stamp") or {}
        party = ", ".join(s.get("party") or []) or "unknown"
        lines.append(f"  - Stamped {s.get('at')}: ROM {s.get('rom') or 'unknown'}, "
                     f"{s.get('badges') if s.get('badges') is not None else 'unknown'} badges, "
                     f"party {party}.")
    return "\n".join(lines) + "\n"
