# LENTRA LOAD v2 - METRICS ENGINE

import asyncio
import time
import subprocess
from pyrogram import Client

API_ID = 34837463
API_HASH = "660e4e614f3ebc98d02284ef4cffec19"
SESSION = "lentra_pyro"

TOTAL = 100
DELAY = 0.05


async def send_load():
    app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
    await app.start()

    print("[LOAD v2] START")

    start_time = time.time()

    for i in range(TOTAL):
        msg = f"LOAD_V2_{i}"
        await app.send_message("me", msg)
        print(f"[SEND] {i}")
        await asyncio.sleep(DELAY)

    await app.stop()

    return start_time


def db_query(sql):
    cmd = f"""psql -U postgres -d lentra -c "{sql}" """
    return subprocess.getoutput(cmd)


def get_queue_metrics():
    return db_query("""
    SELECT
        status,
        COUNT(*)
    FROM processing_queue
    GROUP BY status;
    """)


def get_latency():
    # если нет timestamps — fallback на approximation
    return db_query("""
    SELECT
        COUNT(*) as total,
        MAX(id) - MIN(id) as spread
    FROM processing_queue;
    """)


def system_snapshot():
    return subprocess.getoutput("free -h")


def report():
    print("\n====================")
    print("[LOAD v2 REPORT]")
    print("====================")

    print("\n[QUEUE METRICS]")
    print(get_queue_metrics())

    print("\n[LATENCY (proxy)]")
    print(get_latency())

    print("\n[SYSTEM]")
    print(system_snapshot())


async def main():
    await send_load()

    # wait worker flush
    await asyncio.sleep(5)

    report()


if __name__ == "__main__":
    asyncio.run(main())
