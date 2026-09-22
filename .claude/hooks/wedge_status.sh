#!/bin/sh
# Claude Code status line (the statusLine entry in ~/.claude/settings.json):
# names any process wedged in the kernel on __vma_start_write, and prints
# nothing otherwise.
#
# Until the replacement CPU is in, a process can stick there, and anything
# that reads its details (ps, pgrep, top) then blocks for good. Only
# `wsl --shutdown` clears it, so this tells Ian when to run it. It reads only
# wchan and comm, the per-process files that stay safe, with one grep, because
# the status line refreshes often. The argument is the /proc root, for tests.
# Delete this, its statusLine entry and the guard's wedge rule when the new
# chip is in.
root=${1:-/proc}
while read -r _; do :; done   # drain the session JSON Claude Code sends
for f in $(grep -l __vma_start_write "$root"/[0-9]*/wchan 2>/dev/null); do
    d=${f%/wchan}
    printf 'WEDGED: pid %s (%s), run wsl --shutdown  ' "${d#"$root"/}" "$(cat "$d/comm" 2>/dev/null)"
done
