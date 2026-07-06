import time
import signal

from lentra.runtime.bootstrap_guard import enforce_bootstrap


running = True


def shutdown(*args):
    global running
    running = False


def main():
    enforce_bootstrap()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    print("[WORKER] locked runtime started")

    while running:
        time.sleep(1)

    print("[WORKER] shutdown")


if __name__ == "__main__":
    main()
