"""One thread per process for numpy's matrix library, set before numpy first
loads. The scorer runs one process per core; a library thread per core in
each of them thrashed the machine twice on 2026-10-02 (a network fight took
77 seconds in a pool and 5 alone; self-play reached a load of 328 and wrote
nothing in two hours). Every scorer module that loads numpy imports this
first, so no import order can reach numpy before it."""
import os

for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")
