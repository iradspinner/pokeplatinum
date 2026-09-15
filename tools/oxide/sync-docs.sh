#!/usr/bin/env bash
# Mirror docs/oxide/*.md into the project folder on the G: drive, so the
# separate chat surface that works from there (see
# docs/oxide/START-HERE-current-state.md) always sees the current docs.
# Run whenever a docs/oxide/*.md file changes this session.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$REPO_ROOT/docs/oxide"
DEST="/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/Hardlove Gold-Platinum Oxide Integration Project"

if [ ! -d "$DEST" ]; then
    echo "sync-docs: project folder not reachable at $DEST, skipping" >&2
    exit 0
fi

copy() {
    local src="$SRC/$1" dest="$DEST/$2"
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "synced: $1 -> $2"
}

copy "design-doc.md" "Platinum Oxide - Design Doc.md"
copy "tracker.md" "Platinum Oxide - Tracker.md"
copy "START-HERE-current-state.md" "notes/START-HERE-current-state.md"
copy "phase1-hg-engine-survey.md" "notes/phase1-hg-engine-survey.md"
copy "phase2-approach-breakdown.md" "notes/phase2-approach-breakdown.md"
copy "phase3-base-rom-inventory.md" "notes/phase3-base-rom-inventory.md"
copy "phase3-answers-and-trainer-format.md" "notes/phase3-answers-and-trainer-format.md"
copy "setup-fork-and-wsl2.md" "notes/setup-fork-and-wsl2.md"
copy "import-report-species-moves.md" "notes/import-report-species-moves.md"
