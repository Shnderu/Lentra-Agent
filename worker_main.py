import asyncio
from core.worker.router import process_once

async def loop():
    print(">>> WORKER STARTED")

    while True:
        try:
            await process_once()
        except Exception as e:
            print("[WORKER ERROR]", e)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(loop())
