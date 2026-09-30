"""Checks on the perfect-line store (plrescore.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_pline

Every fight of the game has a stored reading whose fingerprint matches its
inputs today, every stored reading was verified by a second run, and each
holds the three numbers the trainer pass judges by.
"""
import sys

from . import plrescore as R


def check_fingerprints(results):
    store = R.load()["fights"]
    stale = [R.key_of(f) for f, boss in R.fights()
             if store.get(R.key_of(f), {}).get("fingerprint") != R.fingerprint(f, boss)]
    results.append(("every fight's stored reading matches its inputs", not stale,
                    f"{len(stale)} stale or missing, e.g. {stale[:5]}" if stale else f"{len(store)} readings"))


def check_verified(results):
    store = R.load()["fights"]
    bad = [k for k, r in store.items() if not r.get("verified")]
    results.append(("every stored reading was verified by a second run", not bad,
                    f"{len(bad)} unverified, e.g. {bad[:5]}" if bad else "all verified"))


def check_numbers(results):
    store = R.load()["fights"]
    need = ("blind_rate", "blind_deaths", "blind_wipe")
    boss_need = ("planned_rate", "planned_deaths", "planned_wipe")
    bad = [k for k, r in store.items()
           if any(r.get(x) is None for x in need + (boss_need if r.get("boss") else ()))]
    results.append(("each reading holds its clean-win rate, deaths and wipe chance", not bad, str(bad[:5])))


def main():
    results = []
    for check in (check_fingerprints, check_verified, check_numbers):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
