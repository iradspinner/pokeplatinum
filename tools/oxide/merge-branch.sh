#!/usr/bin/env bash
# Land one finished branch on `oxide` while this CPU cannot build: merge it,
# have GitHub build the merged tree, run the full gate on that ROM, and push
# only if the gate passes. Platinum Oxide project. The Overseer runs it for each
# track or cloud branch it merges, after reading the branch's report (the
# `cloud-job` skill has the review that comes first).
#
# Steps, stopping at the first failure with nothing pushed to `oxide`:
#   1. On `oxide` with no uncommitted changes to tracked files; fetch, and
#      fast-forward onto origin/oxide if it moved.
#   2. Merge the branch. A conflict stops here: resolve it, commit the merge,
#      and rerun with --merged. The tracker and the design doc conflict most;
#      keep both sides' current entries (the `cloud-job` skill says how).
#   3. Push the merged tree to `integration-check` and build it with
#      tools/oxide/fetch-rom, which reuses a build when only docs changed.
#   4. integrate.sh --verify-only --rom <that ROM>: the base-ROM checks, the
#      encounter and balance suites, the word limits. Any failure stops here.
#   5. Push `oxide`, delete `integration-check`, run sync-docs.sh.
#
# Usage:
#   tools/oxide/merge-branch.sh <branch>             # origin/<branch>, or any commit
#   tools/oxide/merge-branch.sh --merged             # the merge is already committed
#   tools/oxide/merge-branch.sh --no-push <branch>   # stop after the gate
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

MERGED=0; PUSH=1; BRANCH=""
while [ $# -gt 0 ]; do
    case "$1" in
        --merged) MERGED=1 ;;
        --no-push) PUSH=0 ;;
        -h|--help) sed -n '/^set -uo/q;2,$p' "$0"; exit 0 ;;
        -*) echo "merge-branch: unknown option $1" >&2; exit 2 ;;
        *) BRANCH="$1" ;;
    esac
    shift
done

die() { echo "merge-branch: $*" >&2; exit 1; }
say() { echo "merge-branch: $*"; }

[ "$(git rev-parse --abbrev-ref HEAD)" = "oxide" ] || die "not on oxide"
[ -z "$(git status --porcelain --untracked-files=no)" ] || die "uncommitted changes to tracked files; commit or stash them first"

git fetch -q origin || die "git fetch failed"

if [ $MERGED -eq 0 ]; then
    [ -n "$BRANCH" ] || die "name a branch, or pass --merged"
    # Take the remote branch when there is one, since tracks and cloud sessions
    # push there; otherwise accept a local branch or a commit.
    if git rev-parse --verify -q "origin/$BRANCH^{commit}" >/dev/null; then
        REF="origin/$BRANCH"
    elif git rev-parse --verify -q "$BRANCH^{commit}" >/dev/null; then
        REF="$BRANCH"
    else
        die "no branch or commit called $BRANCH"
    fi
    if ! git merge-base --is-ancestor origin/oxide HEAD; then
        git merge -q --ff-only origin/oxide || die "oxide has diverged from origin/oxide; sort that out first"
    fi
    if git merge-base --is-ancestor "$REF" HEAD; then
        say "$REF is already in oxide; nothing to merge"
        exit 0
    fi
    say "merging $REF ($(git rev-parse --short=9 "$REF"))"
    if ! git merge --no-edit "$REF" >/dev/null 2>&1; then
        echo "merge-branch: conflicts, resolve them, commit, then rerun with --merged:" >&2
        git diff --name-only --diff-filter=U | sed 's/^/  /' >&2
        exit 1
    fi
fi

HEAD_SHORT="$(git rev-parse --short=9 HEAD)"
say "building $HEAD_SHORT on GitHub"
git push -q -f origin HEAD:refs/heads/integration-check || die "could not push integration-check"
FETCH_OUT="$(sh tools/oxide/fetch-rom HEAD 2>&1)"; FETCH_RC=$?
echo "$FETCH_OUT" | tail -3
[ $FETCH_RC -eq 0 ] || die "fetch-rom failed; oxide is merged locally but not pushed"
ROM="$(echo "$FETCH_OUT" | sed -n 's/^ROM: *//p' | tail -1)"
[ -f "$ROM" ] || die "fetch-rom printed no ROM path"

LOG="$(mktemp "${TMPDIR:-/tmp}/merge-branch-$HEAD_SHORT.XXXX.log")"
say "gate on $ROM (log: $LOG)"
bash tools/oxide/integrate.sh --verify-only --rom "$ROM" >"$LOG" 2>&1; GATE_RC=$?
grep -E '^(FAIL|WARN)|every count|^passed:|^failed:' "$LOG"
[ $GATE_RC -eq 0 ] || die "the gate failed (log above); oxide is merged locally but not pushed"

if [ $PUSH -eq 0 ]; then
    say "gate passed; --no-push given, so oxide is not pushed"
    exit 0
fi
git push -q origin oxide || die "could not push oxide"
git push -q origin --delete integration-check 2>/dev/null
bash tools/oxide/sync-docs.sh >/dev/null || say "sync-docs reported a problem; run it by hand to see"
say "pushed oxide at $(git rev-parse --short=9 HEAD) and mirrored the docs"
