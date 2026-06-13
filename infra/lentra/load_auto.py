# LENTRA AUTO LOAD ENGINE v1

import asyncio
import time
import subprocess
from pyrogram import Client

API_ID = 34837463
API_HASH = "660e4e614f3ebc98d02284ef4cffec19"
SESSION = "lentra_pyro"

async def send_load(total: int, delay: float):
    app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

    await app.start()

    print(f"[LOAD] START total={total}")

    start = time.time()

    for i in range(total):
        msg = f"LOAD_TEST_{i}"
        await app.send_message("me", msg)
        print(f"[LOAD] SENT {i}")
        await asyncio.sleep(delay)

    await app.stop()

    duration = time.time() - start

    return total, duration


def get_queue_stats():
    cmd = """psql -U postgres -d lentra -c "SELECT status, COUNT(*) FROM processing_queue GROUP BY status;" """
    return subprocess.getoutput(cmd)


def get_system():
    return subprocess.getoutput("free -h")


def report(total, duration):
    print("\n====================")
    print("[AUTO LOAD REPORT]")
    print("====================")
    print(f"Sent: {total}")
    print(f"Duration: {round(duration,2)} sec")
    print(f"Avg rate: {round(total/duration,2)} msg/sec")

    print("\n[QUEUE]")
    print(get_queue_stats())

    print("\n[SYSTEM]")
    print(get_system())


async def main():
    total = 100
    delay = 0.1

    total, duration = await send_load(total, delay)

    await asyncio.sleep(3)

    report(total, duration)


if __name__ == "__main__":
    asyncio.run(main())
