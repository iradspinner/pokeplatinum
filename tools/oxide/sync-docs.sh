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

# The mirror is what the chat surface reads as current, so it only ever comes
# from `oxide`. Run from a track branch or worktree, it would copy that
# branch's older tracker over the current one (it happened on 2026-09-22).
branch="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [ "$branch" != "oxide" ]; then
    echo "sync-docs: refusing to mirror from branch '$branch'; run it from the main checkout on oxide" >&2
    exit 1
fi
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
copy "tracker-archive.md" "notes/tracker-archive.md"
copy "phase1-hg-engine-survey.md" "notes/phase1-hg-engine-survey.md"
copy "phase2-approach-breakdown.md" "notes/phase2-approach-breakdown.md"
copy "phase3-base-rom-inventory.md" "notes/phase3-base-rom-inventory.md"
copy "phase3-answers-and-trainer-format.md" "notes/phase3-answers-and-trainer-format.md"
copy "setup-fork-and-wsl2.md" "notes/setup-fork-and-wsl2.md"
copy "reviews/buff-review/rules.md" "notes/reviews/buff-review/rules.md"
copy "reviews/buff-review/suggestions.md" "notes/reviews/buff-review/suggestions.md"
copy "reviews/buff-review/principles.md" "notes/reviews/buff-review/principles.md"
copy "reviews/buff-review/scores.md" "notes/reviews/buff-review/scores.md"
copy "reviews/encounter-review/zones.md" "notes/reviews/encounter-review/zones.md"
copy "reviews/encounter-review/water.md" "notes/reviews/encounter-review/water.md"
copy "reviews/encounter-review/principles.md" "notes/reviews/encounter-review/principles.md"
copy "save-layout.md" "notes/save-layout.md"
copy "battle-log.md" "notes/battle-log.md"
copy "trainer-scoring-handoff.md" "notes/trainer-scoring-handoff.md"
copy "scorer-speed-plan.md" "notes/scorer-speed-plan.md"
copy "how-a-fight-is-read.md" "notes/how-a-fight-is-read.md"
copy "restart-checks.md" "notes/restart-checks.md"
copy "prompt-audit-2026-10-02.md" "notes/prompt-audit-2026-10-02.md"
copy "plugin-review-2026-10-06.md" "notes/plugin-review-2026-10-06.md"
copy "learnset-checks.md" "notes/learnset-checks.md"
copy "learnset-baseline.md" "notes/learnset-baseline.md"
copy "learnset-insights.md" "notes/learnset-insights.md"
copy "learnset-exam.md" "notes/learnset-exam.md"
copy "learnset-exam-changes.md" "notes/learnset-exam-changes.md"
copy "learnset-capture-spikes.md" "notes/learnset-capture-spikes.md"
copy "tm-list-by-number.md" "notes/tm-list-by-number.md"
copy "alpha-readiness.md" "notes/alpha-readiness.md"
copy "learnset-rewrite.md" "notes/learnset-rewrite.md"
for split in roark gardenia fantina maylene wake byron candice hq galactic volkner barry league; do
    copy "learnset-sheets/$split.md" "notes/learnset-sheets/$split.md"
done
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
copy "qa-review-2026-09-22-element6.md" "notes/qa-review-2026-09-22-element6.md"
copy "qa-review-2026-09-23-element6.md" "notes/qa-review-2026-09-23-element6.md"
copy "qa-review-2026-09-22-encounter-d4d5.md" "notes/qa-review-2026-09-22-encounter-d4d5.md"
copy "test-kit.md" "notes/test-kit.md"
copy "ingame-checklist.md" "notes/ingame-checklist.md"
copy "balance-plan.md" "notes/balance-plan.md"
copy "battle-zone-plan.md" "notes/battle-zone-plan.md"
copy "pocket-pc.md" "notes/pocket-pc.md"
copy "frontier-brains.md" "notes/frontier-brains.md"
copy "kaizo-move-changes.md" "notes/kaizo-move-changes.md"
copy "kaizo-learnsets.tsv" "notes/kaizo-learnsets.tsv"
copy "kaizo-comparison.md" "notes/kaizo-comparison.md"
copy "wild-movesets.md" "notes/wild-movesets.md"
copy "pairwise-candidates.md" "notes/pairwise-candidates.md"
copy "status-move-tiers.md" "notes/status-move-tiers.md"
copy "trainer-survey.md" "notes/trainer-survey.md"
copy "status-move-tiers.md" "notes/status-move-tiers.md"
copy "script-index.md" "notes/script-index.md"
copy "script-index.json" "notes/script-index.json"
copy "staples-survey.md" "notes/staples-survey.md"
copy "move-pool-survey.md" "notes/move-pool-survey.md"
copy "move-pool-survey.csv" "notes/move-pool-survey.csv"
copy "pokemon-gifts.md" "notes/pokemon-gifts.md"
copy "pokemon-gifts.csv" "notes/pokemon-gifts.csv"
copy "pokemon-sources.md" "notes/pokemon-sources.md"
copy "pokemon-sources.csv" "notes/pokemon-sources.csv"
copy "battle-ai/README.md" "notes/battle-ai/README.md"
copy "battle-ai/basic.md" "notes/battle-ai/basic.md"
copy "battle-ai/expert-1.md" "notes/battle-ai/expert-1.md"
copy "battle-ai/expert-2.md" "notes/battle-ai/expert-2.md"
copy "battle-ai/other-flags.md" "notes/battle-ai/other-flags.md"
copy "battle-ai/expert-gaps.md" "notes/battle-ai/expert-gaps.md"
copy "battle-ai/expert-new-moves.md" "notes/battle-ai/expert-new-moves.md"
copy "battle-ai/switching-and-items.md" "notes/battle-ai/switching-and-items.md"
copy "encounter-design-survey.md" "Claude outputs/encounter-design-survey.md"
copy "encounter-tool-design.md" "Claude outputs/encounter-tool-design.md"
copy "encounter-tool-build-plan.md" "Claude outputs/encounter-tool-build-plan.md"
copy "encounter-tool-build-plan-archive.md" "Claude outputs/encounter-tool-build-plan-archive.md"
copy "encounter-tool-visual-design.md" "Claude outputs/encounter-tool-visual-design.md"
copy "encounter-authoring-plan.md" "Claude outputs/encounter-authoring-plan.md"
copy "encounters/design.json" "Claude outputs/encounters/design.json"
copy "encounters/availability-plan.json" "Claude outputs/encounters/availability-plan.json"
copy "encounters/availability.md" "Claude outputs/encounters/availability.md"
copy "encounters/scripted-sources.md" "Claude outputs/encounters/scripted-sources.md"
copy "encounters/scripted.json" "Claude outputs/encounters/scripted.json"
copy "encounters/water-biomes.json" "Claude outputs/encounters/water-biomes.json"
copy "encounters/water-lint-draft.md" "Claude outputs/encounters/water-lint-draft.md"
copy "encounters/values.json" "Claude outputs/encounters/values.json"
copy "encounters/friendship-evolutions.md" "Claude outputs/encounters/friendship-evolutions.md"
copy "encounters/frontier-brains-rewards.md" "Claude outputs/encounters/frontier-brains-rewards.md"
copy "encounters/regional-dex-proposal.md" "Claude outputs/encounters/regional-dex-proposal.md"
copy "encounters/clown-replacements.md" "Claude outputs/encounters/clown-replacements.md"
copy "encounters/classic-starters.md" "Claude outputs/encounters/classic-starters.md"
copy "encounters/ability-audit.md" "Claude outputs/encounters/ability-audit.md"

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
