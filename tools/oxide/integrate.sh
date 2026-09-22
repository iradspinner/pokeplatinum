#!/usr/bin/env bash
# Collect every parallel track into `oxide`, verify the result, mirror the docs.
#
# Platinum Oxide project. Run this when all other agents are stopped and the
# question is "is everything on one branch, and does it all still check out".
# The mechanical part lives here so it needs one command and one approval; the
# judgment part (reading the status docs against what actually landed) is the
# /integrate slash command in .claude/commands/integrate.md, which calls this.
#
# What it does, in order, stopping at the first thing it cannot do safely:
#   1. Preconditions: on `oxide`, main checkout clean, every worktree clean.
#      A Claude process still attached to a worktree is reported as a warning,
#      because a stopped-but-idle session looks the same as a running one.
#   2. `git fetch`, then fast-forward `oxide` onto `origin/oxide` if it is behind.
#   3. Merge every local `worktree-*` branch (and every branch a worktree has
#      checked out) that is not already an ancestor of `oxide`. A conflict that
#      touches only docs/oxide/tracker.md is resolved by taking the `oxide` side,
#      which is the project's rule (each track has one status home; the tracker
#      belongs to the main track). Any other conflict aborts the merge and stops.
#   4. Verification: the restart check-list from the tracker plus the encounter
#      tool's tests. Each check reports pass or fail; the script keeps going so
#      the summary is complete, and exits non-zero if any failed.
#   5. tools/oxide/sync-docs.sh.
#
# Usage:
#   tools/oxide/integrate.sh              # the lot
#   tools/oxide/integrate.sh --dry-run    # preconditions and what would merge, nothing changes
#   tools/oxide/integrate.sh --no-build   # skip `make rom` and the checks that need the built ROM
#   tools/oxide/integrate.sh --no-push    # do not push oxide at the end
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

PY=python3

DRY_RUN=0; BUILD=1; PUSH=1
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --no-build) BUILD=0 ;;
        --no-push) PUSH=0 ;;
        -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
        *) echo "integrate: unknown option $arg" >&2; exit 2 ;;
    esac
done

BASE="$HOME/roms/base.nds"
VANILLA="$HOME/roms/vanilla.nds"
ROM="build/pokeplatinum.us.nds"
PASS=(); FAIL=(); MERGED=(); WARN=()

say()  { printf '\n== %s ==\n' "$*"; }
ok()   { PASS+=("$1"); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL+=("$1"); printf 'FAIL  %s\n' "$1"; }
warn() { WARN+=("$1"); printf 'WARN  %s\n' "$1"; }
die()  { printf 'integrate: %s\n' "$*" >&2; exit 1; }

# Run a check. $1 is the label, the rest is the command. Passes when the exit
# code is 0 and, if CHECK_EXPECT is set, when the output contains that text.
# The last lines of output are printed either way so a failure is readable.
check() {
    local label="$1"; shift
    local out rc
    out="$("$@" 2>&1)"; rc=$?
    printf '%s\n' "$out" | tail -n 3 | sed 's/^/      /'
    if [ $rc -eq 0 ] && { [ -z "${CHECK_EXPECT:-}" ] || printf '%s' "$out" | grep -q -- "$CHECK_EXPECT"; }; then
        ok "$label"
    else
        bad "$label (exit $rc${CHECK_EXPECT:+, expected \"$CHECK_EXPECT\"})"
    fi
}

# ---------------------------------------------------------------- 1. preconditions
say "preconditions"
branch="$(git rev-parse --abbrev-ref HEAD)"
[ "$branch" = "oxide" ] || die "on branch $branch, not oxide"
if [ -n "$(git status --porcelain)" ]; then
    git status --short >&2
    die "main checkout has uncommitted changes; commit or discard them first"
fi

# Every worktree must be clean. Worktree branches are collected here too.
declare -a TRACK_BRANCHES=()
while IFS= read -r line; do
    case "$line" in
        worktree\ *) wt="${line#worktree }" ;;
        branch\ *)
            b="${line#branch refs/heads/}"
            [ "$wt" = "$REPO" ] && continue
            if [ -n "$(git -C "$wt" status --porcelain 2>/dev/null)" ]; then
                git -C "$wt" status --short >&2
                die "worktree $wt ($b) has uncommitted changes; that agent is not finished"
            fi
            TRACK_BRANCHES+=("$b")
            ;;
    esac
done < <(git worktree list --porcelain)
# Plus any local worktree-* branch whose worktree was removed but never merged.
while IFS= read -r b; do
    case " ${TRACK_BRANCHES[*]:-} " in *" $b "*) ;; *) TRACK_BRANCHES+=("$b") ;; esac
done < <(git for-each-ref --format='%(refname:short)' 'refs/heads/worktree-*')
echo "track branches: ${TRACK_BRANCHES[*]:-(none)}"

# A Claude process whose working directory is inside a worktree is probably a
# session that has not been stopped. Reported, not fatal: an idle one is harmless.
for pid in $(pgrep -x claude 2>/dev/null || true); do
    cwd="$(readlink "/proc/$pid/cwd" 2>/dev/null || true)"
    case "$cwd" in
        "$REPO"/.claude/worktrees/*) warn "claude pid $pid still has its cwd in $cwd" ;;
    esac
done

[ -f "$BASE" ] || die "$BASE missing (pinned base ROM)"
[ -f "$VANILLA" ] || die "$VANILLA missing (pinned vanilla ROM)"

# ---------------------------------------------------------------- 2. fetch and ff
say "fetch"
git fetch -q origin || die "git fetch failed"
if [ "$(git rev-list --count oxide..origin/oxide)" != "0" ]; then
    if [ $DRY_RUN -eq 1 ]; then
        echo "would fast-forward oxide onto origin/oxide ($(git rev-list --count oxide..origin/oxide) commits)"
    else
        git merge --ff-only origin/oxide || die "origin/oxide has diverged from local oxide; reconcile by hand"
        echo "fast-forwarded to origin/oxide"
    fi
fi

# ---------------------------------------------------------------- 3. merge tracks
say "merge"
for b in "${TRACK_BRANCHES[@]:-}"; do
    [ -n "$b" ] || continue
    if git merge-base --is-ancestor "$b" oxide; then
        echo "already merged: $b"; continue
    fi
    n="$(git rev-list --count oxide.."$b")"
    if [ $DRY_RUN -eq 1 ]; then
        echo "would merge: $b ($n commits)"
        git diff --stat oxide..."$b" | tail -n 1 | sed 's/^/      /'
        continue
    fi
    echo "merging $b ($n commits)"
    merge_out="$(git merge --no-edit "$b" 2>&1)" && { MERGED+=("$b"); continue; }
    conflicts="$(git diff --name-only --diff-filter=U)"
    if [ -z "$conflicts" ]; then
        git merge --abort 2>/dev/null
        die "merging $b failed without a content conflict:"$'\n'"$merge_out"
    fi
    # Two files conflict routinely and each has one right resolution. The
    # tracker belongs to the main track, so its side wins (one status home per
    # track). Track agents only append to the design doc's findings log, so a
    # conflict there is both tracks appending entries and the answer is to keep
    # both, in order. Deletions from the log happen only in a docs pass with
    # every track paused, precisely so this never resurrects a deleted entry.
    resolved=()
    for f in $conflicts; do
        case "$f" in
            docs/oxide/tracker.md)
                git checkout --ours "$f" && git add "$f" && resolved+=("$f: kept the oxide side") ;;
            docs/oxide/design-doc.md)
                sed -i '/^<<<<<<< /d;/^=======$/d;/^>>>>>>> /d' "$f"
                grep -q '^<<<<<<<\|^>>>>>>>' "$f" && { git merge --abort; die "design-doc.md conflict in $b is not a plain log append; resolve by hand"; }
                git add "$f" && resolved+=("$f: kept both sides of the findings log") ;;
            *)
                git merge --abort
                die "merging $b conflicts in a file this script does not resolve, aborted:"$'\n'"$conflicts" ;;
        esac
    done
    git commit -q --no-edit || die "could not commit the resolved merge of $b"
    printf '      %s\n' "${resolved[@]}"
    MERGED+=("$b (${#resolved[@]} conflict(s) resolved)")
done
[ $DRY_RUN -eq 1 ] && { say "dry run, stopping before verification"; exit 0; }

# ---------------------------------------------------------------- 4. verify
say "verify"
if [ $BUILD -eq 1 ]; then
    check "make rom" make rom
    if [ -f "$ROM" ]; then
        check "verify_narcs (species/moves/evo/learnsets)" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE"
        # The encounter tables are checked against their source JSON (M7), not
        # the base ROM: once the authoring pass rewrites a table the base ROM
        # stops being its truth. --encounters --ref still exists for the
        # tables that have not been authored yet.
        check "verify_narcs --encounters --source" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --encounters --source
        check "verify_narcs --text" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --text
        check "verify_narcs --map-headers" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --map-headers
        CHECK_EXPECT="would write 0 script files" check "bulk_scripts --dry-run" "$PY" tools/oxide/bulk_scripts.py --dry-run
        CHECK_EXPECT="would write 0 event files" check "bulk_events --dry-run" "$PY" tools/oxide/bulk_events.py --dry-run
        CHECK_EXPECT="would write 0" check "bulk_text --dry-run" "$PY" tools/oxide/bulk_text.py --dry-run
    else
        bad "built ROM missing at $ROM"
    fi
else
    warn "build skipped (--no-build); ROM-dependent checks not run"
fi

# The importer must find nothing left to import: every count 0.
out="$("$PY" tools/oxide/import_base_rom.py --base "$BASE" --vanilla "$VANILLA" --dry-run 2>&1 | tail -n 1)"
printf '      %s\n' "$out"
if printf '%s' "$out" | grep -q "would change" && ! printf '%s' "$out" | grep -Eq "': [1-9]"; then
    ok "import_base_rom --dry-run, every count 0"
else
    bad "import_base_rom --dry-run reports something left to import"
fi
git checkout -q tools/oxide/import_report.md 2>/dev/null || true   # the dry run rewrites the report

CHECK_EXPECT="0 failed" check "scriptdis --verify (vanilla)" "$PY" tools/oxide/scriptdis.py --rom "$VANILLA" --verify
CHECK_EXPECT="0 failed" check "scriptdis --verify --base-rom" "$PY" tools/oxide/scriptdis.py --rom "$BASE" --verify --base-rom

export PYTHONPATH=.
for t in tools/oxide/encounters/test_*.py; do
    name="$(basename "$t" .py)"
    CHECK_EXPECT="passed" check "encounter tool $name" "$PY" -m "tools.oxide.encounters.$name"
done
# R12 (availability against Ian's pick-list) is ignored here: vanilla was never
# built for that list and fails it on purpose. It runs on the working tree.
check "encounter lint on vanilla (--ref main --fail-on error, R12 ignored)" "$PY" -m tools.oxide.encounters.cli --ref main lint --fail-on error --ignore R12

# ---------------------------------------------------------------- 5. docs mirror
say "docs"
check "sync-docs" bash tools/oxide/sync-docs.sh

# ---------------------------------------------------------------- 6. push, summary
if [ $PUSH -eq 1 ] && [ ${#FAIL[@]} -eq 0 ]; then
    say "push"
    if git push -q origin oxide; then ok "push origin oxide"; else bad "push origin oxide"; fi
elif [ $PUSH -eq 1 ]; then
    warn "not pushed: a check failed"
fi

say "summary"
echo "merged:   ${MERGED[*]:-(nothing new)}"
echo "passed:   ${#PASS[@]}"
echo "failed:   ${#FAIL[@]}${FAIL[*]:+  -> ${FAIL[*]}}"
echo "warnings: ${#WARN[@]}${WARN[*]:+  -> ${WARN[*]}}"
echo "head:     $(git log --oneline -1)"
[ ${#FAIL[@]} -eq 0 ]
