#!/usr/bin/env python3
"""Move a tool onto the pinned interpreter if it was started on another one.

`tools/oxide/oxide-python` is the policy and `CLAUDE.md` says to go through it,
but the documented command for most of these tools is still `python3
tools/oxide/<thing>.py`, and this machine's system Python returns wrong answers
from ordinary string work often enough to matter. A wrong answer here is not a
crash, it is a `res/` file rewritten with the wrong bytes, so the tools do not
rely on being invoked correctly.

`ensure()` re-executes the process on the pinned interpreter and says so. It is
deliberately fail-open: if the pin cannot be resolved, or resolves to the
interpreter already running, it prints nothing and carries on, because a tool
that refuses to run is worse than one running on a slightly suspect Python.

Call it from `if __name__ == "__main__":` and nowhere else. Calling it at import
time would re-execute whichever tool happened to import this one partway
through its own run.

    if __name__ == "__main__":
        pinned_python.ensure()
        main()
"""

import os
import subprocess
import sys

GUARD = "OXIDE_PYTHON_REEXEC"
WRAPPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oxide-python")


def pinned():
    """The interpreter the project wants, or None if it cannot be resolved."""
    try:
        out = subprocess.run([WRAPPER, "--path"], capture_output=True, text=True,
                             timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    path = out.stdout.strip()
    return path if path and os.path.exists(path) else None


def ensure():
    """Re-exec on the pinned interpreter unless we are already on it."""
    if os.environ.get(GUARD):          # already been through here; never loop
        return
    want = pinned()
    if not want:
        return
    try:
        same = os.path.samefile(want, sys.executable)
    except OSError:
        same = os.path.realpath(want) == os.path.realpath(sys.executable)
    if same:
        return
    print("[oxide] re-running on the pinned interpreter %s (was %s); "
          "see tools/oxide/oxide-python" % (want, sys.executable),
          file=sys.stderr)
    os.environ[GUARD] = "1"
    try:
        os.execv(want, [want] + sys.argv)
    except OSError as e:
        print("[oxide] could not re-exec (%s); continuing on %s"
              % (e, sys.executable), file=sys.stderr)
