import asyncio
import os

from core.worker.sender import send_loop


def main():
    print(">>> LENTRA WORKER V11.2 STARTED")

    try:
        asyncio.run(send_loop())
    except KeyboardInterrupt:
        print(">>> WORKER STOPPED (keyboard interrupt)")
    except Exception as e:
        print("[FATAL WORKER ERROR]", e)
        raise


if __name__ == "__main__":
    main()
