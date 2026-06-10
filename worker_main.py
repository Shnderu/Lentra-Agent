import asyncio
import time
import os
import psycopg2

from aiogram import Bot

from core.worker.router import process_once
from core.queue.queue import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


async def wait_db():
    while True:
        try:
            conn = get_conn()
            conn.close()
            print("[DB] READY")
            return
        except Exception as e:
            print("[DB WAIT]", e)
            time.sleep(2)


async def loop():
    print(">>> WORKER STARTED")
    await wait_db()

    while True:
        try:
            await process_once(bot)
        except Exception as e:
            print("[WORKER ERROR]", e)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(loop())
