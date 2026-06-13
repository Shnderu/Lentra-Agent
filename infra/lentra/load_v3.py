import asyncio
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

    print("[LOAD v3] START")

    for i in range(TOTAL):
        await app.send_message("me", f"LOAD_V3_{i}")
        await asyncio.sleep(DELAY)

    await app.stop()


def db(sql):
    return subprocess.getoutput(f"""psql -U postgres -d lentra -c "{sql}" """)


def latency_stats():
    return db("""
    SELECT
        COUNT(*) as total,
        MIN(EXTRACT(EPOCH FROM (processed_at - ingested_at))) as min_latency,
        AVG(EXTRACT(EPOCH FROM (processed_at - ingested_at))) as avg_latency,
        MAX(EXTRACT(EPOCH FROM (processed_at - ingested_at))) as max_latency
    FROM processing_queue
    WHERE processed_at IS NOT NULL;
    """)


def percentiles():
    return db("""
    SELECT
        percentile_cont(0.5) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (processed_at - ingested_at))
        ) AS p50,
        percentile_cont(0.95) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (processed_at - ingested_at))
        ) AS p95,
        percentile_cont(0.99) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (processed_at - ingested_at))
        ) AS p99
    FROM processing_queue
    WHERE processed_at IS NOT NULL;
    """)


def queue():
    return db("""
    SELECT status, COUNT(*) FROM processing_queue GROUP BY status;
    """)


async def main():
    await send_load()

    await asyncio.sleep(5)

    print("\n====================")
    print("[LOAD v3 REPORT]")
    print("====================")

    print("\n[QUEUE]")
    print(queue())

    print("\n[LATENCY]")
    print(latency_stats())

    print("\n[PERCENTILES]")
    print(percentiles())


if __name__ == "__main__":
    asyncio.run(main())
