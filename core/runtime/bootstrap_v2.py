import os

from core.runtime.preflight_checks_v2 import run as preflight
from core.runtime.dependency_lock_v2 import validate

"""
Lentra Bootstrap v2

Добавлено:
- preflight checks
- dependency validation
"""

MODE = os.getenv("LENTRA_MODE", "worker")


def start_worker():
    from worker.worker import run
    run()


def main():
    print(">>> BOOTSTRAP V2 START")

    validate()
    preflight()

    print(f">>> MODE = {MODE}")

    if MODE == "worker":
        start_worker()
    else:
        raise ValueError("Only worker mode supported in v2 hardening layer")


if __name__ == "__main__":
    main()
