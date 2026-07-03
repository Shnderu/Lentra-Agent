import time
import os
from lentra.runtime.bootstrap.wiring_safe import build_gateway


def main():
    print("[WORKER] START")

    gateway = build_gateway()

    print("[WORKER] gateway initialized")

    # HARD BLOCKING LOOP (keep process alive)
    while True:
        try:
            # minimal heartbeat / future queue hook
            time.sleep(5)

        except KeyboardInterrupt:
            print("[WORKER] shutdown signal received")
            break


if __name__ == "__main__":
    main()
