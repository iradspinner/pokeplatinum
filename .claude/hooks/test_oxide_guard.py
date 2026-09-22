#!/usr/bin/env python3
"""Checks oxide_guard.py's wedge rule and wedge_status.sh against fake /proc trees.

Run from anywhere: python3 .claude/hooks/test_oxide_guard.py
Builds one tree with a process stuck on __vma_start_write and one without,
then asks the guard and the status line about each. Prints "N passed" or the
first failure, and exits non-zero on a failure.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oxide_guard  # noqa: E402


def fake_proc(root, procs):
    """Write a /proc lookalike: one directory per pid holding comm and wchan."""
    for pid, comm, wchan in procs:
        d = os.path.join(root, str(pid))
        os.makedirs(d)
        with open(os.path.join(d, "comm"), "w") as f:
            f.write(comm + "\n")
        with open(os.path.join(d, "wchan"), "w") as f:
            f.write(wchan)  # the kernel writes wchan with no newline
    os.makedirs(os.path.join(root, "sys"))  # a non-pid entry the scan must skip


def main():
    passed = 0

    def expect(name, cond):
        nonlocal passed
        if not cond:
            print("FAIL", name)
            sys.exit(1)
        passed += 1

    with tempfile.TemporaryDirectory() as tmp:
        stuck = os.path.join(tmp, "stuck")
        clean = os.path.join(tmp, "clean")
        fake_proc(stuck, [(1, "init", "do_epoll_wait"), (4242, "cc1", "__vma_start_write")])
        fake_proc(clean, [(1, "init", "do_epoll_wait"), (4242, "cc1", "do_wait")])

        expect("scan finds the wedged pid", oxide_guard.wedged(stuck) == [("4242", "cc1")])
        expect("scan finds nothing on a clean tree", oxide_guard.wedged(clean) == [])

        refusal = oxide_guard.check("ps aux", "/", proc_root=stuck)
        expect("ps aux refused while wedged", refusal is not None)
        expect("refusal names the pid and command", "pid 4242 (cc1)" in (refusal or ""))
        expect("ps aux allowed on a clean tree", oxide_guard.check("ps aux", "/", proc_root=clean) is None)
        for cmd in ("ls", "ls -la /proc"):
            expect("%s allowed while wedged" % cmd, oxide_guard.check(cmd, "/", proc_root=stuck) is None)
            expect("%s allowed on a clean tree" % cmd, oxide_guard.check(cmd, "/", proc_root=clean) is None)
        for cmd in ("pgrep -f make", "sudo pkill cc1", "timeout 5 top -b -n1", "/usr/bin/pidof make",
                    "htop", "echo hi && ps -ef | grep x"):
            expect("%s refused while wedged" % cmd, oxide_guard.check(cmd, "/", proc_root=stuck) is not None)

        status = os.path.join(HERE, "wedge_status.sh")
        out = subprocess.run(["sh", status, stuck], input="{}", capture_output=True, text=True).stdout
        expect("status line names the wedged pid", "4242" in out and "cc1" in out)
        out = subprocess.run(["sh", status, clean], input="{}", capture_output=True, text=True).stdout
        expect("status line is empty on a clean tree", out == "")

    print("%d passed" % passed)


if __name__ == "__main__":
    main()
