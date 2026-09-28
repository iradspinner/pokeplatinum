#!/bin/bash
# Restarts Ian's OxiDex server, so any session can bring it up to date after
# a landing (Ian, 2026-09-27). Ian allows exactly this command in his own
# settings, run from a repo root with no arguments:
#
#     bash tools/oxide/encounters/restart_server.sh
#
# It stops the OxiDex server listening on port 8765 and nothing else (a
# process whose command runs `-m tools.oxide.encounters.server`, and only the
# one on that port, so a second copy on another port is left alone), waits
# for the port to free, starts the server again from Ian's worktree
# (.claude/worktrees/ian-tool) wherever this is run from, detached so it
# outlives the session that started it, and waits until /api/save answers.
# It prints the new pid and the save it is watching, or fails with the tail
# of the log. The watched save's path lives in ~/.config/oxidex/settings.json,
# which this leaves as it is.
#
# For a dry run only, OXIDEX_PORT puts the whole thing on another port, so a
# test never touches the live server; the allow rule never sets it.
set -u

PORT="${OXIDEX_PORT:-8765}"
WORKTREE=/home/ian/pokeplatinum/.claude/worktrees/ian-tool
PY="$HOME/.venvs/oxide/bin/python3"
LOG_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/oxidex"
LOG="$LOG_DIR/server-$PORT.log"
MODULE="tools.oxide.encounters.server"

fail() { echo "restart_server: $*" >&2; exit 1; }
[ -d "$WORKTREE" ] || fail "no worktree at $WORKTREE"
[ -x "$PY" ] || fail "no Python at $PY"

# The pids listening on the port whose command line runs the OxiDex module.
oxidex_pids() {
    ss -ltnpH "sport = :$PORT" 2>/dev/null | grep -o 'pid=[0-9]*' | cut -d= -f2 | sort -u |
    while read -r pid; do
        if tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | grep -q -- "-m $MODULE"; then
            echo "$pid"
        fi
    done
}
port_busy() { [ -n "$(ss -ltnH "sport = :$PORT" 2>/dev/null)" ]; }

old=$(oxidex_pids)
if [ -z "$old" ]; then
    echo "no OxiDex server on port $PORT; starting one"
else
    echo "stopping the OxiDex server on port $PORT (pid $(echo $old))"
    kill $old 2>/dev/null
    for _ in $(seq 1 20); do
        [ -z "$(oxidex_pids)" ] && break
        sleep 0.5
    done
    left=$(oxidex_pids)
    [ -n "$left" ] && { echo "still running after 10 s; killing pid $left"; kill -9 $left 2>/dev/null; }
fi
for _ in $(seq 1 20); do
    port_busy || break
    sleep 0.5
done
port_busy && fail "port $PORT is still taken by something that is not the OxiDex server: $(ss -ltnpH "sport = :$PORT")"

mkdir -p "$LOG_DIR"
args=()
[ "$PORT" != 8765 ] && args=(--port "$PORT")
(
    cd "$WORKTREE" || exit 1
    PYTHONPATH=. setsid nohup "$PY" -m "$MODULE" "${args[@]}" > "$LOG" 2>&1 < /dev/null &
)

for _ in $(seq 1 60); do
    body=$(curl -s -m 2 "http://127.0.0.1:$PORT/api/save") && [ -n "$body" ] && break
    body=""
    sleep 0.5
done
if [ -z "$body" ]; then
    echo "restart_server: the server did not answer on port $PORT within 30 s; the log says:" >&2
    tail -n 20 "$LOG" >&2
    exit 1
fi
new=$(oxidex_pids)
watching=$(printf '%s' "$body" | "$PY" -c 'import json, sys; s = json.load(sys.stdin); print(s.get("path") or "no save set")')
echo "OxiDex server running: pid $new, port $PORT, from $WORKTREE"
echo "watching: $watching"
echo "log: $LOG"
