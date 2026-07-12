import time
import os
from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


def main():
    print("[WORKER] START")

    gateway = build_gateway_v3()

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
