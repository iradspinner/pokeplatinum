#!/bin/bash
# Starts Ian's OxiDex server when a session opens and nothing serves its port
# (Ian, 2026-10-06: "have it autostart when I open Overseer"). It runs the
# restart script a landing uses, so the server comes from Ian's worktree
# (.claude/worktrees/ian-tool) whichever checkout the session is in, and runs
# it detached, so opening a session never waits on it. A server already
# listening is left alone. Cloud sessions have no OxiDex worktree and skip it.
#
# OXIDEX_PORT moves the whole thing to another port, for a test that must not
# touch the live server; the hook never sets it.
REPO=/home/ian/pokeplatinum
PORT="${OXIDEX_PORT:-8765}"

[ -n "${OXIDE_CLOUD:-}" ] && exit 0
[ -d "$REPO/.claude/worktrees/ian-tool" ] || exit 0
ss -ltnH "sport = :$PORT" 2>/dev/null | grep -q . && exit 0

cd "$REPO" || exit 0
OXIDEX_PORT="$PORT" setsid nohup bash tools/oxide/encounters/restart_server.sh \
    >/dev/null 2>&1 </dev/null &
exit 0
