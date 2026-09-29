#!/usr/bin/env bash
# Land one finished branch on `oxide`: merge it, build the merged tree here,
# run the full gate on that ROM, and push only if the gate passes. Platinum Oxide project. The Overseer runs it for each
# track or cloud branch it merges, after reading the branch's report (the
# `cloud-job` skill has the review that comes first).
#
# Steps, stopping at the first failure with nothing pushed to `oxide`:
#   1. On `oxide` with no uncommitted changes to tracked files; fetch, and
#      fast-forward onto origin/oxide if it moved.
#   2. Merge the branch. A conflict stops here: resolve it, commit the merge,
#      and rerun with --merged. The tracker and the design doc conflict most;
#      keep both sides' current entries (the `cloud-job` skill says how).
#   3. integrate.sh --verify-only: `make rom`, then the base-ROM checks, the
#      encounter and balance suites, the word limits. Any failure stops here.
#      The ROM is copied to ~/oxide-playtest/pokeplatinum-oxide-<commit>.nds,
#      the name fetch-rom gives, for Ian.
#   4. Push `oxide` and run sync-docs.sh. GitHub's free build of the public
#      repo then prints the ROM's SHA-1, which should match the copy.
# Until 2026-09-29 the build ran on GitHub (fetch-rom), because the old CPU
# could not build; Ian ruled out Actions in the private repos until
# 2026-10-01, and the new CPU builds the same ROM byte for byte.
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
LOG="$(mktemp "${TMPDIR:-/tmp}/merge-branch-$HEAD_SHORT.XXXX.log")"
say "building $HEAD_SHORT here and running the gate (log: $LOG)"
bash tools/oxide/integrate.sh --verify-only >"$LOG" 2>&1; GATE_RC=$?
grep -E '^(FAIL|WARN)|every count|^passed:|^failed:' "$LOG"
[ $GATE_RC -eq 0 ] || die "the gate failed (log above); oxide is merged locally but not pushed"
ROM="$HOME/oxide-playtest/pokeplatinum-oxide-$HEAD_SHORT.nds"
mkdir -p "$(dirname "$ROM")" && cp build/pokeplatinum.us.nds "$ROM" \
    && sha1sum "$ROM" | cut -d' ' -f1 > "${ROM%.nds}.sha1" \
    && say "ROM for Ian: $ROM (SHA-1 $(cat "${ROM%.nds}.sha1"))"

if [ $PUSH -eq 0 ]; then
    say "gate passed; --no-push given, so oxide is not pushed"
    exit 0
fi
git push -q origin oxide || die "could not push oxide"
bash tools/oxide/sync-docs.sh >/dev/null || say "sync-docs reported a problem; run it by hand to see"
say "pushed oxide at $(git rev-parse --short=9 HEAD) and mirrored the docs"
