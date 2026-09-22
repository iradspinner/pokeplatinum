#!/usr/bin/env bash
# Mirror docs/oxide/ into the project folder on the G: drive, so the separate
# chat surface that works from there (see docs/oxide/START-HERE-current-state.md)
# always sees the current docs. Run whenever a docs/oxide file changes this session.
#
# The mapping is explicit because the destination names differ from the repo
# names. Any docs/oxide file that is not mapped is reported at the end, so a new
# doc cannot be silently left out of the mirror.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$REPO_ROOT/docs/oxide"
DEST="/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/Hardlove Gold-Platinum Oxide Integration Project"

if [ ! -d "$DEST" ]; then
    echo "sync-docs: project folder not reachable at $DEST, skipping" >&2
    exit 0
fi

declare -A MAPPED=()

copy() {
    local src="$SRC/$1" dest="$DEST/$2"
    MAPPED["$1"]=1
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
copy "save-layout.md" "notes/save-layout.md"
copy "species-pick-list.md" "notes/species-pick-list.md"
copy "species-pick-list.csv" "notes/species-pick-list.csv"
copy "species-id-scheme.md" "notes/species-id-scheme.md"
copy "species-id-map.csv" "notes/species-id-map.csv"
copy "donor-tables.md" "notes/donor-tables.md"
copy "donor-move-tables.md" "notes/donor-move-tables.md"
copy "move-animation-map.json" "notes/move-animation-map.json"
copy "move-descriptions.json" "notes/move-descriptions.json"
copy "battle-effect-names.json" "notes/battle-effect-names.json"
copy "phase3-scripts-and-events-plan.md" "notes/phase3-scripts-and-events-plan.md"
copy "phase4-engine-change-answers.md" "notes/phase4-engine-change-answers.md"
copy "qa-review-2026-09-22.md" "notes/qa-review-2026-09-22.md"
copy "qa-review-2026-09-22-encounter-m8.md" "notes/qa-review-2026-09-22-encounter-m8.md"
copy "agent-brief-workflow-improvements.md" "notes/agent-brief-workflow-improvements.md"
copy "agent-brief-encounter-docs-split.md" "notes/agent-brief-encounter-docs-split.md"
copy "agent-brief-element4-effects.md" "notes/agent-brief-element4-effects.md"
copy "test-kit.md" "notes/test-kit.md"
copy "pokemon-gifts.md" "notes/pokemon-gifts.md"
copy "pokemon-gifts.csv" "notes/pokemon-gifts.csv"
copy "pokemon-sources.md" "notes/pokemon-sources.md"
copy "pokemon-sources.csv" "notes/pokemon-sources.csv"
copy "encounter-design-survey.md" "Claude outputs/encounter-design-survey.md"
copy "encounter-tool-design.md" "Claude outputs/encounter-tool-design.md"
copy "encounter-tool-build-plan.md" "Claude outputs/encounter-tool-build-plan.md"
copy "encounter-tool-visual-design.md" "Claude outputs/encounter-tool-visual-design.md"
copy "encounter-authoring-plan.md" "Claude outputs/encounter-authoring-plan.md"
copy "encounters/design.json" "Claude outputs/encounters/design.json"
copy "encounters/availability-plan.json" "Claude outputs/encounters/availability-plan.json"
copy "encounters/availability.md" "Claude outputs/encounters/availability.md"
copy "encounters/scripted-sources.md" "Claude outputs/encounters/scripted-sources.md"

# Anything under docs/oxide that the list above does not name. caught.json is
# per-playthrough state and gitignored, so it is not a doc and is not mirrored.
unmapped=0
while IFS= read -r -d '' f; do
    rel="${f#$SRC/}"
    case "$rel" in encounters/caught.json) continue ;; esac
    if [ -z "${MAPPED[$rel]:-}" ]; then
        echo "sync-docs: NOT MIRRORED (add it to the list): $rel" >&2
        unmapped=1
    fi
done < <(find "$SRC" -type f -print0)
exit $unmapped
