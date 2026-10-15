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
# With --since REF, step 4 runs only the checks the changes since REF can
# reach (Ian, 2026-10-13: most of the gate's time went to tool suites that
# most landings never touch). tools/oxide/gate_scope.py works out which, from
# the code: a check runs when the landing changes its module, a tool module
# its imports reach, or a file one of those modules names. A change to the
# game's data or engine, to the build or to the gate itself runs everything.
# The build, the docs mirror, the tracker's size, the scheduled items and the
# doc viewer's test run on every landing. merge-branch.sh passes --since
# origin/oxide; without --since, or with --full, every check runs, which is
# the gate for step 15's reading, the alpha ROM and a cloud session.
#
# Usage:
#   tools/oxide/integrate.sh              # the lot
#   tools/oxide/integrate.sh --dry-run    # preconditions and what would merge, nothing changes
#   tools/oxide/integrate.sh --no-build   # skip `make rom` and the checks that need the built ROM
#   tools/oxide/integrate.sh --no-push    # do not push oxide at the end
#   tools/oxide/integrate.sh --verify-only  # steps 4 and 5 on the tree as it is:
#                                           # no fetch, no merge, no push (the QA pass)
#   tools/oxide/integrate.sh --since REF  # step 4 runs only what the changes since REF reach
#   tools/oxide/integrate.sh --full       # every check, whatever --since says
#   tools/oxide/integrate.sh --rom PATH   # check PATH, a ROM built elsewhere, instead of
#                                         # building one; only the build's small helper
#                                         # files are made, on two jobs
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

PY=python3

DRY_RUN=0; BUILD=1; PUSH=1; VERIFY_ONLY=0; ROM_GIVEN=""; SINCE=""; FULL=0
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY_RUN=1 ;;
        --no-build) BUILD=0 ;;
        --no-push) PUSH=0 ;;
        --verify-only) VERIFY_ONLY=1; PUSH=0 ;;
        --since) SINCE="${2:-}"; shift ;;
        --since=*) SINCE="${1#--since=}" ;;
        --full) FULL=1 ;;
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
if [ -n "$SINCE" ] && ! git rev-parse --verify -q "$SINCE^{commit}" >/dev/null; then
    echo "integrate: --since $SINCE: no such commit" >&2; exit 2
fi

BASE="$HOME/roms/base.nds"
VANILLA="$HOME/roms/vanilla.nds"
ROM="${ROM_GIVEN:-build/pokeplatinum.us.nds}"
# Test suites that check a built ROM read its path from OXIDE_ROM, so with
# --rom they check the ROM given, not a stale one left in build/.
export OXIDE_ROM="$ROM"
PASS=(); FAIL=(); MERGED=(); WARN=(); NOT_NEEDED=()

say()  { printf '\n== %s ==\n' "$*"; }
ok()   { PASS+=("$1"); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL+=("$1"); printf 'FAIL  %s\n' "$1"; }
warn() { WARN+=("$1"); printf 'WARN  %s\n' "$1"; }
die()  { printf 'integrate: %s\n' "$*" >&2; exit 1; }

# The scope of a --since run: the tool modules the changes reach, one path a
# line, from gate_scope.py. Empty means every check runs.
SCOPE_FILE=""
# True when a check whose tool module is $1 must run: always on a full run,
# and on a scoped one when the module is on gate_scope.py's list.
needed() { [ -z "$SCOPE_FILE" ] || grep -qxF -- "$1" "$SCOPE_FILE"; }
# True when any of the modules named must run.
needed_any() { local m; for m in "$@"; do needed "$m" && return 0; done; return 1; }
# The tool module a check runs, read from its command: the module after -m,
# or the first tools/oxide/*.py argument. None (the build, a shell script)
# means the check runs on every landing.
entry_of() {
    local prev="" a
    for a in "$@"; do
        if [ "$prev" = "-m" ]; then printf '%s.py\n' "${a//.//}"; return; fi
        case "$a" in tools/oxide/*.py) printf '%s\n' "$a"; return ;; esac
        prev="$a"
    done
}

# Run a check. $1 is the label, the rest is the command. Passes when the exit
# code is 0 and, if CHECK_EXPECT is set, when the output contains that text.
# The last lines of output are printed either way so a failure is readable,
# and any output line starting "gate warning: " becomes one of the gate's
# warnings. On a scoped run a check whose module the landing does not reach
# is counted as not needed and not run.
check() {
    local label="$1"; shift
    local entry out rc line
    entry="$(entry_of "$@")"
    if [ -n "$entry" ] && ! needed "$entry"; then
        NOT_NEEDED+=("$label"); return 0
    fi
    out="$("$@" 2>&1)"; rc=$?
    printf '%s\n' "$out" | tail -n 3 | sed 's/^/      /'
    while IFS= read -r line; do
        warn "${line#gate warning: }"
    done < <(printf '%s\n' "$out" | grep '^gate warning: ')
    # The expected text is looked for in a here-string, not through a pipe:
    # under pipefail, grep -q exiting at its first match kills a printf still
    # writing an output larger than the pipe's 64 KB, and the check failed on
    # a test that passed (test_fightsim's 65,892 bytes, 2026-10-15).
    if [ $rc -eq 0 ] && { [ -z "${CHECK_EXPECT:-}" ] || grep -q -- "$CHECK_EXPECT" <<< "$out"; }; then
        ok "$label"
    else
        bad "$label (exit $rc${CHECK_EXPECT:+, expected \"$CHECK_EXPECT\"})"
    fi
}

# ---------------------------------------------------------------- 1. preconditions
say "preconditions"
branch="$(git rev-parse --abbrev-ref HEAD)"
# Merging happens only on oxide. A verify-only run checks whatever branch it
# is on, which is how a cloud session gates its own cloud/<track> branch.
[ "$branch" = "oxide" ] || [ $VERIFY_ONLY -eq 1 ] || die "on branch $branch, not oxide"
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

# The pinned base and vanilla ROMs live outside the repo (Nintendo's, never
# committed). A cloud session does not have them, and Ian ruled on 2026-09-25
# that cloud sessions skip the checks that need them: each such check is then
# listed under one warning rather than failing, and the gate still covers the
# build, the encounter tables against their JSON, and every test suite.
REFS=1
if [ ! -f "$BASE" ] || [ ! -f "$VANILLA" ]; then
    REFS=0
    [ -n "${OXIDE_CLOUD:-}" ] || echo "integrate: $BASE or $VANILLA missing; the checks that need them are skipped" >&2
fi
SKIPPED_REF=()
refcheck() {
    if [ $REFS -eq 1 ]; then check "$@"; else SKIPPED_REF+=("$1"); fi
}

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
# The scope. A local ROM is trusted without GitHub's build to compare it with
# (Ian, 2026-10-06), so that comparison, which only ever warned on a landing
# (the push comes after the gate), is gone (Ian, 2026-10-13).
if [ -n "$SINCE" ] && [ $FULL -eq 0 ]; then
    scope_out="$("$PY" tools/oxide/gate_scope.py "$SINCE" 2>&1)" || die "gate_scope.py failed: $scope_out"
    case "$scope_out" in
        full\ *) echo "scope: everything, because ${scope_out#full }" ;;
        scoped\ *)
            SCOPE_FILE="$(mktemp "${TMPDIR:-/tmp}/gate-scope.XXXX")"
            trap 'rm -f "$SCOPE_FILE"' EXIT
            printf '%s\n' "$scope_out" | tail -n +2 > "$SCOPE_FILE"
            echo "scope: $(printf '%s\n' "$scope_out" | head -n 1 | cut -d' ' -f2-), so only the checks they reach run"
            ;;
        *) die "gate_scope.py said something unexpected: $scope_out" ;;
    esac
elif [ $FULL -eq 1 ]; then
    echo "scope: everything (--full)"
else
    echo "scope: everything (no --since given)"
fi
# With --rom, the ROM was built elsewhere and only the helpers the checks read
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
        check "make rom" make rom
    fi
    if [ -f "$ROM" ]; then
        refcheck "verify_narcs (species/moves/evo/learnsets)" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE"
        # The encounter tables are checked against their source JSON (M7), not
        # the base ROM: once the authoring pass rewrites a table the base ROM
        # stops being its truth. --encounters --ref still exists for the
        # tables that have not been authored yet.
        check "verify_narcs --encounters --source" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --encounters --source
        # Every species' TM and HM bits read back from the built pl_personal
        # against its JSON and tm-list.tsv (the TM pass); no base ROM needed.
        check "tmcompat check (TM bits read back)" "$PY" -m tools.oxide.balance.tmcompat check --rom "$ROM"
        refcheck "verify_narcs --text" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --text
        refcheck "verify_narcs --map-headers" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --map-headers
        refcheck "verify_narcs --land-data" "$PY" tools/oxide/verify_narcs.py --built "$ROM" --ref "$BASE" --land-data
        CHECK_EXPECT="would write 0 script files" refcheck "bulk_scripts --dry-run" "$PY" tools/oxide/bulk_scripts.py --dry-run --built "$ROM"
        CHECK_EXPECT="would write 0 event files" refcheck "bulk_events --dry-run" "$PY" tools/oxide/bulk_events.py --dry-run --built "$ROM"
        CHECK_EXPECT="would write 0" refcheck "bulk_text --dry-run" "$PY" tools/oxide/bulk_text.py --dry-run --built "$ROM"
    else
        bad "built ROM missing at $ROM"
    fi
else
    warn "build skipped (--no-build); ROM-dependent checks not run"
fi

# The importer must find nothing left to import: every count 0.
if ! needed tools/oxide/import_base_rom.py; then
    NOT_NEEDED+=("import_base_rom --dry-run")
elif [ $REFS -eq 1 ]; then
out="$("$PY" tools/oxide/import_base_rom.py --base "$BASE" --vanilla "$VANILLA" --dry-run 2>&1 | tail -n 1)"
printf '      %s\n' "$out"
if grep -q "would change" <<< "$out" && ! grep -Eq "': [1-9]" <<< "$out"; then
    ok "import_base_rom --dry-run, every count 0"
else
    bad "import_base_rom --dry-run reports something left to import"
fi
git checkout -q tools/oxide/import_report.md 2>/dev/null || true   # the dry run rewrites the report
else
    SKIPPED_REF+=("import_base_rom --dry-run")
fi

CHECK_EXPECT="0 failed" refcheck "scriptdis --verify (vanilla)" "$PY" tools/oxide/scriptdis.py --rom "$VANILLA" --verify
CHECK_EXPECT="0 failed" refcheck "scriptdis --verify --base-rom" "$PY" tools/oxide/scriptdis.py --rom "$BASE" --verify --base-rom
# The land data check's own test: an unregistered map edit must fail it.
CHECK_EXPECT="0 failed" refcheck "verify_narcs --land-data, its own test" "$PY" tools/oxide/test_land_data.py --base "$BASE"

export PYTHONPATH=.
# The encounter tools read vanilla data from the `main` branch (git ls-tree and
# git show main:...). A cloud session's checkout carries only the branch it was
# given, so fetch main's tip if it is missing (six checks failed without it on
# the first cloud run, 2026-09-25).
git rev-parse --verify -q main >/dev/null || git fetch -q --depth=1 origin main:main || warn "could not fetch main; the encounter checks that read vanilla will fail"
# The engine's level caps (element 8) against the balance track's fights.json,
# so a cap moved in one and not the other fails here.
CHECK_EXPECT="passed" check "level caps: engine table, fights.json and closing scripts agree" "$PY" tools/oxide/test_level_caps.py
# The reward placer's own test (alpha readiness, step 9), so a change to the
# placement tool or the scripts it hooks into fails here.
CHECK_EXPECT="passed" check "reward placements: place_rewards.py's own test" "$PY" tools/oxide/test_place_rewards.py
for t in tools/oxide/encounters/test_*.py; do
    name="$(basename "$t" .py)"
    CHECK_EXPECT="passed" check "encounter tool $name" "$PY" -m "tools.oxide.encounters.$name"
done
# The balance track's reference suite reads data kept outside the repo (the
# reference hacks' calculator files) and two outputs of the build, so on a
# machine or a --no-build run without any of them it is skipped with a
# warning rather than failed. Under a minute.
b1_missing=""
for p in "$HOME/roms/balance-refs" build/tools/msgenc/msgenc build/generated/vars_flags.h; do
    [ -e "$p" ] || b1_missing="$b1_missing $p"
done
# Every balance suite runs whenever a landing reaches it, and a change to the
# game's data reaches them all, because a change elsewhere can break what they
# guard: on 2026-09-26 the encounter track's table fold changed Roark's and
# Gardenia's player pools, and test_b3 failed on oxide while the gate, which
# then ran test_b1 alone, passed. test_b3 runs the calculator in one Node
# process for about 30 seconds; test_learnstudy checks the learnset study's
# reading of Kaizo, test_learncheck the learnset rules on Oxide's lists, and
# test_learnrewrite the generator's own rules, reporting without failing
# which species files differ from its output (under a minute together).
BALANCE_SUITES=(test_b1 test_b1e test_b3 test_learnstudy test_learncheck test_learnrewrite)
if [ -z "$b1_missing" ]; then
    for t in "${BALANCE_SUITES[@]}"; do
        CHECK_EXPECT="passed" check "balance $t" "$PY" -m "tools.oxide.balance.$t"
    done
elif needed_any $(printf 'tools/oxide/balance/%s.py ' "${BALANCE_SUITES[@]}"); then
    warn "balance suites skipped, missing:$b1_missing"
fi
# The fight scorer's fast tests read only the tree and need no build, each in
# about 2 to 10 seconds: the difficulty store and Ian's formula, the weather
# ruling (no player species learns a weather move), the simulator's
# mechanics, the AI mirror against trainer_ai.c, and the planner's network
# features. All but the first need numpy, which the setup guide installs and
# a cloud VM may lack, so without it they are skipped with a warning. The
# first scoring system and its suites (B2's metrics, B4's level curve, B6's
# audit, the stored-score fingerprints) were retired on 2026-10-13.
# test_plplan, the planner's exact odds and turns (about 30 seconds), came
# back on 2026-10-13 once it found Roark's Lileep by species. test_plfixes,
# the mechanics the Roark fight showed missing (about 45 seconds), reads its
# Roark from a saved copy of the team before his redesign and one box from
# ~/oxide-trials/three-gym-run, so it runs only where that folder is;
# test_plgoal3 reads ~/oxide-trials too and stays out.
if "$PY" -c "import numpy" 2>/dev/null; then
    for t in test_difficulty test_weather_moves test_fightsim test_fightai test_plfeat test_plplan; do
        CHECK_EXPECT="passed" check "scorer $t" "$PY" -m "tools.oxide.balance.$t"
    done
    if [ -d "$HOME/oxide-trials/three-gym-run" ]; then
        CHECK_EXPECT="passed" check "scorer test_plfixes" "$PY" -m tools.oxide.balance.test_plfixes
    elif needed tools/oxide/balance/test_plfixes.py; then
        warn "scorer test_plfixes skipped: ~/oxide-trials/three-gym-run is missing"
    fi
else
    CHECK_EXPECT="passed" check "scorer test_difficulty" "$PY" -m tools.oxide.balance.test_difficulty
    numpy_suites=(test_weather_moves test_fightsim test_fightai test_plfeat test_plplan test_plfixes)
    if needed_any $(printf 'tools/oxide/balance/%s.py ' "${numpy_suites[@]}"); then
        warn "scorer tests skipped, numpy missing: ${numpy_suites[*]}"
    fi
fi
# The working tree passes every rule, R12 included since 2026-09-27: the
# legendaries Ian keeps out of reach are warnings with his reason. The same
# lint on vanilla (`--ref main`) was cut on 2026-10-13 (Ian): the encounter
# tool's own tests already check that vanilla passes its rules, and it never
# caught anything.
check "encounter lint on the working tree (--fail-on error, R12 included)" "$PY" -m tools.oxide.encounters.cli lint --fail-on error

# The script index (docs/oxide/script-index.md and .json) is generated from the
# scripts and events. Its own test checks the tool against facts known from the
# scripts; the committed copy going stale only warns, since a script edit need
# not wait on it (Ian, 2026-09-27). Both need the branch's full history, which
# a shallow clone lacks, so there the comparison is skipped with a warning.
CHECK_EXPECT="passed" check "script index: known facts (test_scriptindex)" "$PY" tools/oxide/test_scriptindex.py
if needed tools/oxide/scriptindex.py; then
    si_out="$("$PY" tools/oxide/scriptindex.py --check 2>&1)"; si_rc=$?
    case $si_rc in
        0) echo "$si_out" ;;
        1) warn "script index out of date: rerun tools/oxide/scriptindex.py and commit docs/oxide/script-index.md and .json" ;;
        *) warn "script index not compared: $si_out" ;;
    esac
fi

# The tracker holds open work only and every main-track session reads it in
# full, so it is kept short: finished blocks move to tracker-archive.md. This
# warns rather than fails when it passes 9,000 words (6,000 until Ian raised
# it on 2026-10-03, after it was outgrown twice), so it cannot quietly
# grow back to the 20,000 it reached before the 2026-09-23 cut.
tracker_words="$(wc -w < docs/oxide/tracker.md)"
if [ "$tracker_words" -gt 9000 ]; then
    warn "tracker.md is $tracker_words words, over 9,000: move finished blocks to docs/oxide/tracker-archive.md"
else
    echo "tracker.md is $tracker_words words (warns over 9,000)"
fi

# Deferred instructions (Ian, 2026-10-01): each lives in the tracker's
# Scheduled list with why it exists and what would make it unneeded, and is
# checked against today's state before it is done. An entry without its
# reason, one past due, or a dated deferral anywhere else fails here.
check "deferred instructions (deferred_check.py)" "$PY" tools/oxide/deferred_check.py

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

[ ${#SKIPPED_REF[@]} -eq 0 ] || warn "no pinned base or vanilla ROM here, so skipped: ${SKIPPED_REF[*]}"
say "summary"
echo "merged:   ${MERGED[*]:-(nothing new)}"
echo "passed:   ${#PASS[@]}"
echo "failed:   ${#FAIL[@]}${FAIL[*]:+  -> ${FAIL[*]}}"
echo "warnings: ${#WARN[@]}${WARN[*]:+  -> ${WARN[*]}}"
[ -z "$SCOPE_FILE" ] || echo "not needed: ${#NOT_NEEDED[@]} checks this landing does not touch"
echo "head:     $(git log --oneline -1)"
[ ${#FAIL[@]} -eq 0 ]
