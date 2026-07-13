import time


def main():
    print("[WORKER] START (disabled legacy runtime)")

    # Legacy worker retired.
    # Production execution path:
    # PostgreSQL task queue -> recovery/runtime pipeline.
    #
    # This module intentionally does not initialize GatewayV3.
    # See ARCHITECTURE_CLEANUP_PLAN and AUDIT_CURRENT_STATE_2026-07-13.

    while True:
        try:
            time.sleep(5)

        except KeyboardInterrupt:
            print("[WORKER] shutdown signal received")
            break


if __name__ == "__main__":
    main()
