"""Where each encounter file is met: the map headers that use it and the
location name the player sees on the map popup.

Ian's capture rule (2026-09-21): a nuzlocke capture is per location *name*,
so two tables that share a name are one capture opportunity. Lake Verity
and its drained version, the two floors of Oreburgh Gate, both halves of
Route 204 and of Route 205, every room of Mt. Coronet. Nothing in the
encounter format says this; it is in `include/data/map_headers.h`, where
every map header names its wild encounter file and its label text, and in
`res/text/location_names.json`, where the label ids become English.

Read-only. The headers are the engine's, not this track's, so this module
never writes them; Verity Lakefront's header pointing at no table is a
backlog item, not something to fix from here.
"""
import collections
import functools
import json
import os
import re

from . import model

HEADERS = os.path.join("include", "data", "map_headers.h")
NAMES = os.path.join("res", "text", "location_names.json")

_ENTRY = re.compile(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \},", re.S)
_ENC = re.compile(r"\.wildEncountersArchiveID = (\w+)")
_LABEL = re.compile(r"\.mapLabelTextID = (\w+)")


@functools.lru_cache(maxsize=None)
def header_uses(root=None):
    """{encounter file stem: [(map header, label id)]} for every header that
    names a table. ENCOUNTERS_NONE is left out."""
    root = root or model.repo_root()
    with open(os.path.join(root, HEADERS), encoding="utf-8") as f:
        text = f.read()
    out = collections.defaultdict(list)
    for header, body in _ENTRY.findall(text):
        enc = _ENC.search(body)
        label = _LABEL.search(body)
        if not enc or enc.group(1) == "ENCOUNTERS_NONE":
            continue
        out[enc.group(1)].append((header, label.group(1) if label else None))
    return dict(out)


@functools.lru_cache(maxsize=None)
def label_names(root=None):
    """{label id: English name} from the location-names text bank."""
    root = root or model.repo_root()
    with open(os.path.join(root, NAMES), encoding="utf-8") as f:
        data = json.load(f)
    # the bank is {"key": ..., "messages": [{"id": ..., "en_US": ...}, ...]}
    entries = data.get("messages") if isinstance(data, dict) else data
    out = {}
    for e in entries or []:
        if isinstance(e, dict) and e.get("id"):
            out[e["id"]] = e.get("en_US") or e["id"]
    return out


def location_of(root=None):
    """{encounter file stem: location name}. A file used under several
    names (none today) gets them joined with ' / '; a file no header uses
    gets its sidecar `planned_location` if it has one (a table built ahead of
    its map), else None (the Turnback Cave rooms and the twenty-five unknown
    files). A sidecar `capture_area` overrides both."""
    root = root or model.repo_root()
    names = label_names(root)
    out = {}
    for stem, uses in header_uses(root).items():
        labels = sorted({names.get(l, l) for _, l in uses if l})
        out[stem] = " / ".join(labels) if labels else None
    # A table built ahead of its map (Verity Lakefront, Amity Square, Snowpoint
    # City's water) has no header pointing at it yet. Its sidecar entry names
    # the location it is planned for, so it counts as that capture area now
    # rather than under its file name. A header, once it exists, wins.
    areas = (model.load_sidecar() or {}).get("areas") or {}
    for stem, entry in areas.items():
        planned = entry.get("planned_location")
        if planned and not out.get(stem):
            out[stem] = planned
    # Ian's capture areas can be finer than the game's names: Mt. Coronet is
    # five captures, not one (2026-09-26). A sidecar `capture_area` names the
    # capture a table counts as, over whatever its header says.
    for stem, entry in areas.items():
        if entry.get("capture_area"):
            out[stem] = entry["capture_area"]
    return out


def by_location(root=None):
    """{location name: [encounter file stems]}, the capture areas."""
    out = collections.defaultdict(list)
    for stem, name in location_of(root).items():
        if name:
            out[name].append(stem)
    return {k: sorted(v) for k, v in out.items()}


def location(stem, root=None):
    """The location name of one encounter file, or None."""
    return location_of(root).get(stem)
