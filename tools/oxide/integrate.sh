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
#      checked out) that is not already an ancestor of `oxide`. A conflict in
#      docs/oxide/tracker.md is resolved block by block: the encounter track's
#      paragraph takes that track's side, and any other block stops the merge.
#      Findings-log appends in the design doc keep both sides. Any other
#      conflict aborts the merge and stops.
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
#   tools/oxide/integrate.sh --verify-only  # steps 4 and 5 on the tree as it is:
#                                           # no fetch, no merge, no push (the QA pass)
#   tools/oxide/integrate.sh --rom PATH   # check PATH, a ROM from tools/oxide/fetch-rom,
#                                         # instead of building one; only the build's small
#                                         # helper files are made, on two jobs (for while
#                                         # this CPU cannot take a full build)
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

PY=python3

DRY_RUN=0; BUILD=1; PUSH=1; VERIFY_ONLY=0; ROM_GIVEN=""
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY_RUN=1 ;;
        --no-build) BUILD=0 ;;
        --no-push) PUSH=0 ;;
        --verify-only) VERIFY_ONLY=1; PUSH=0 ;;
        --rom) ROM_GIVEN="${2:-}"; shift ;;
        --rom=*) ROM_GIVEN="${1#--rom=}" ;;
        -h|--help) sed -n '/^set -uo/q;2,$p' "$0"; exit 0 ;;
        *) echo "integrate: unknown option $1" >&2; exit 2 ;;
    esac
    shift
done
if [ -n "$ROM_GIVEN" ] && [ ! -f "$ROM_GIVEN" ]; then
    echo "integrate: --rom $ROM_GIVEN: no such file" >&2; exit 2
fi

BASE="$HOME/roms/base.nds"
VANILLA="$HOME/roms/vanilla.nds"
ROM="${ROM_GIVEN:-build/pokeplatinum.us.nds}"
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
# A verify-only run looks at this checkout alone, so it skips all of this.
declare -a TRACK_BRANCHES=()
if [ $VERIFY_ONLY -eq 0 ]; then
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
# Found by reading each process's comm file rather than with pgrep: while the
# degraded CPU leaves a process wedged on its memory lock, pgrep and ps block
# for good reading that process, and comm and cwd are the two reads that do not
# need the lock (2026-09-22: this check hung the whole gate).
for d in /proc/[0-9]*; do
    [ "$(cat "$d/comm" 2>/dev/null)" = claude ] || continue
    pid="${d#/proc/}"
    cwd="$(readlink "$d/cwd" 2>/dev/null || true)"
    case "$cwd" in
        "$REPO"/.claude/worktrees/*) warn "claude pid $pid still has its cwd in $cwd" ;;
    esac
done
fi

[ -f "$BASE" ] || die "$BASE missing (pinned base ROM)"
[ -f "$VANILLA" ] || die "$VANILLA missing (pinned vanilla ROM)"

# ---------------------------------------------------------------- 2. fetch and ff
if [ $VERIFY_ONLY -eq 0 ]; then
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
# The tracker belongs to the main track, apart from the encounter track's one
# paragraph near its top, so its conflicts are resolved one block at a time.
# A block whose two sides are both that paragraph takes the encounter branch's
# side. Any other block, or that paragraph conflicting on some other branch,
# fails with the block printed: keeping one side of the whole file came close
# to silently dropping the encounter track's update on 2026-09-22, and a stop
# costs less than a loss. $1 is the conflicted file, $2 the branch merging in.
ENCOUNTER_PARAGRAPH='**Second track: the encounter tool.**'
resolve_tracker() {
    local take=0
    case "$2" in *encounter*) take=1 ;; esac
    awk -v mark="$ENCOUNTER_PARAGRAPH" -v take="$take" -v branch="$2" '
        # True when every non-blank line of a conflict side is the paragraph.
        function paragraph_only(side,   n, i, line, seen) {
            n = split(side, line, "\n")
            for (i = 1; i <= n; i++) {
                if (line[i] == "") continue
                if (index(line[i], mark) != 1) return 0
                seen = 1
            }
            return seen
        }
        !inblock && /^<<<<<<< / { inblock = 1; side = "ours"; ours = theirs = ""; block = $0 "\n"; next }
        inblock {
            block = block $0 "\n"
            if (substr($0, 1, 8) == "||||||| ") { side = "base"; next }
            if ($0 == "=======") { side = "theirs"; next }
            if (/^>>>>>>> /) {
                inblock = 0
                if (take && paragraph_only(ours) && paragraph_only(theirs)) { printf "%s", theirs; next }
                printf "tracker.md: a conflict block this script will not resolve, merging %s:\n%s", branch, block > "/dev/stderr"
                failed = 1
                next
            }
            if (side == "ours") ours = ours $0 "\n"
            else if (side == "theirs") theirs = theirs $0 "\n"
            next
        }
        { print }
        END { exit failed }
    ' "$1" > "$1.resolved" || { rm -f "$1.resolved"; return 1; }
    mv "$1.resolved" "$1"
}

# The design doc conflicts in two routine ways. Both tracks append to the
# findings log (section 8), and the right answer is to keep both entries in
# order. Both tracks also bump the version line at the top, and there keeping
# both would leave two version lines, so the higher version wins. Any other
# block fails with the block printed. $1 is the conflicted file, $2 the branch.
resolve_design_doc() {
    awk -v branch="$2" '
        # The version on a "Design document, vMAJOR.MINOR (date)" line as one
        # comparable number, so v0.33 beats v0.4; -1 if the side is anything else.
        function version(side,   n, i, line, v, num, part) {
            n = split(side, line, "\n"); v = -1
            for (i = 1; i <= n; i++) {
                if (line[i] == "") continue
                if (line[i] !~ /^Design document, v[0-9]+\.[0-9]+ /) return -1
                if (v != -1) return -1
                num = substr(line[i], 19)
                sub(/ .*/, "", num)
                split(num, part, ".")
                v = part[1] * 100000 + part[2]
            }
            return v
        }
        /^## 8\. / { inlog = 1 }
        !inblock && /^<<<<<<< / { inblock = 1; side = "ours"; ours = theirs = ""; block = $0 "\n"; next }
        inblock {
            block = block $0 "\n"
            if (substr($0, 1, 8) == "||||||| ") { side = "base"; next }
            if ($0 == "=======") { side = "theirs"; next }
            if (/^>>>>>>> /) {
                inblock = 0
                vo = version(ours); vt = version(theirs)
                if (vo >= 0 && vt >= 0) { printf "%s", (vo >= vt ? ours : theirs); next }
                if (inlog) { printf "%s%s", ours, theirs; next }
                printf "design-doc.md: a conflict block this script will not resolve, merging %s:\n%s", branch, block > "/dev/stderr"
                failed = 1
                next
            }
            if (side == "ours") ours = ours $0 "\n"
            else if (side == "theirs") theirs = theirs $0 "\n"
            next
        }
        { print }
        END { exit failed }
    ' "$1" > "$1.resolved" || { rm -f "$1.resolved"; return 1; }
    mv "$1.resolved" "$1"
}

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
    # Two files conflict routinely. The tracker is resolved one conflict block
    # at a time by resolve_tracker, above. Track agents only append to the
    # design doc's findings log, so a conflict there is both tracks appending
    # entries and the answer is to keep both, in order. Deletions from the log
    # happen only in a docs pass with every track paused, precisely so this
    # never resurrects a deleted entry.
    resolved=()
    for f in $conflicts; do
        case "$f" in
            docs/oxide/tracker.md)
                resolve_tracker "$f" "$b" || { git merge --abort; die "tracker.md conflict in $b needs a hand merge; the block is printed above"; }
                git add "$f" && resolved+=("$f: took $b's side of the encounter paragraph") ;;
            docs/oxide/design-doc.md)
                resolve_design_doc "$f" "$b" || { git merge --abort; die "design-doc.md conflict in $b needs a hand merge; the block is printed above"; }
                git add "$f" && resolved+=("$f: kept both sides of the findings log, and the higher version") ;;
            *)
                git merge --abort
                die "merging $b conflicts in a file this script does not resolve, aborted:"$'\n'"$conflicts" ;;
        esac
    done
    git commit -q --no-edit || die "could not commit the resolved merge of $b"
    printf '      %s\n' "${resolved[@]}"
    MERGED+=("$b (${#resolved[@]} conflict(s) resolved)")
done
fi
[ $DRY_RUN -eq 1 ] && { say "dry run, stopping before verification"; exit 0; }

# ---------------------------------------------------------------- 4. verify
say "verify"
# Until the replacement CPU is in, a build can crash and pass on a rerun, so
# `make rom` gets a few tries (delete the retry with the Makefile's venv block).
make_rom() {
    local i
    for i in 1 2 3 4; do
        make rom && return 0
        echo "make rom failed, try $i of 4 (degraded CPU, see CLAUDE.md)"
    done
    return 1
}
# The ROM of record is GitHub's build (oxide-rom.yml): the local ROM passes
# when its SHA-1 matches the one a successful run printed. That workflow skips
# a push that changes only Markdown, so the run to compare against is the
# newest ancestor of HEAD that has one and differs from HEAD in Markdown alone;
# its ROM is HEAD's ROM. The exclusion stays exactly `*.md`, the workflow's own
# filter, because the build reads the rest of tools/. Prints "<sha1> <commit>".
# No such run (not pushed, or still building) is a warning, not a failure.
# The hash is read from the job's own log: `gh run view --log` comes back empty
# for some finished runs whose logs GitHub still holds (2026-09-22).
ci_hash() {
    local c sha id job
    declare -A run=()
    while read -r sha id; do
        [ -n "$sha" ] && run[$sha]="$id"
    done < <(gh run list --workflow oxide-rom.yml --status success --limit 100 \
             --json headSha,databaseId --jq '.[] | "\(.headSha) \(.databaseId)"' 2>/dev/null)
    for c in $(git rev-list --max-count=200 HEAD); do
        [ -n "${run[$c]:-}" ] || continue
        git diff --quiet "$c" HEAD -- . ':(exclude)*.md' || continue
        job="$(gh run view "${run[$c]}" --json jobs --jq '.jobs[0].databaseId' 2>/dev/null)"
        printf '%s %s\n' "$(gh api "repos/{owner}/{repo}/actions/jobs/$job/logs" 2>/dev/null |
            grep -o 'ROM SHA-1: [0-9a-f]\{40\}' | head -n 1 | cut -d' ' -f3)" "$c"
        return 0
    done
    return 1
}
# With --rom, the ROM comes from GitHub and only the helpers the checks read
# from build/ are made: the generated headers, msgenc and enumproc, and the
# sound archive's index. Two jobs, so this CPU is never loaded on every core.
make_helpers() {
    [ -f build/build.ninja ] || make configure || return 1
    ninja -C build -j2 tools/msgenc/msgenc tools/enumproc/enumproc res/sound/pl_sound_data.naix \
        $(ninja -C build -t targets all | cut -d: -f1 | grep -E '^generated/[^/]+\.h$')
}
if [ $BUILD -eq 1 ]; then
    if [ -n "$ROM_GIVEN" ]; then
        check "build helpers on two jobs (the ROM is $ROM_GIVEN, not built here)" make_helpers
    else
        check "make rom" make_rom
    fi
    if [ -f "$ROM" ]; then
        local_sha="$(sha1sum "$ROM" | cut -d' ' -f1)"
        if ci="$(ci_hash)" && remote_sha="${ci%% *}" && [ -n "$remote_sha" ]; then
            ci_commit="${ci#* }"
            of="GitHub's build"
            [ "$ci_commit" = "$(git rev-parse HEAD)" ] ||
                of="GitHub's build of $(git rev-parse --short "$ci_commit") (HEAD differs from it only in Markdown)"
            if [ "$local_sha" = "$remote_sha" ]; then ok "ROM matches $of ($local_sha)"
            else bad "ROM $local_sha differs from $of, $remote_sha: rebuild before trusting it"; fi
        else
            warn "no finished GitHub build for HEAD to compare the ROM against ($local_sha)"
        fi
    fi
    if [ -f "$ROM" ]; then
        check "verify_narcs (species/moves/evo/learnsets)" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE"
        # The encounter tables are checked against their source JSON (M7), not
        # the base ROM: once the authoring pass rewrites a table the base ROM
        # stops being its truth. --encounters --ref still exists for the
        # tables that have not been authored yet.
        check "verify_narcs --encounters --source" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --encounters --source
        check "verify_narcs --text" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --text
        check "verify_narcs --map-headers" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --map-headers
        CHECK_EXPECT="would write 0 script files" check "bulk_scripts --dry-run" "$PY" tools/oxide/bulk_scripts.py --dry-run --built "$ROM"
        CHECK_EXPECT="would write 0 event files" check "bulk_events --dry-run" "$PY" tools/oxide/bulk_events.py --dry-run --built "$ROM"
        CHECK_EXPECT="would write 0" check "bulk_text --dry-run" "$PY" tools/oxide/bulk_text.py --dry-run --built "$ROM"
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
# The balance track's reference suite reads data kept outside the repo (the
# reference hacks and the donor ROM) and two outputs of the build, so on a
# machine or a --no-build run without any of them it is skipped with a
# warning rather than failed. About a minute, mostly decoding Hardlove's text.
b1_missing=""
for p in "$HOME/roms/balance-refs" "$HOME/roms/hardlove.nds" build/tools/msgenc/msgenc build/generated/vars_flags.h; do
    [ -e "$p" ] || b1_missing="$b1_missing $p"
done
if [ -z "$b1_missing" ]; then
    CHECK_EXPECT="passed" check "balance test_b1" "$PY" -m tools.oxide.balance.test_b1
else
    warn "balance test_b1 skipped, missing:$b1_missing"
fi
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
