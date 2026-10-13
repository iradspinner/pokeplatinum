"""B6, the first scoring system's audit, retired on 2026-10-13.

Only its name stays, for goal 3's fight list: plgoal3.py loads
goal3_fights.py from ~/oxide-trials/scorer-stage2, outside the repo, and
that script reads the census's placements as b6.placements. The placements
live in required.py now; new code imports them from there. The rest of B6
(its scores, levers, pairs and report) is in the commit the balance plan's
banner names.
"""
from .required import placements  # noqa: F401
