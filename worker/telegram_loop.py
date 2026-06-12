import asyncio
import os
from aiogram import Bot
from core.queue.queue import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def wait_db():
    import time
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
    print(">>> TELEGRAM LOOP STARTED")
    await wait_db()

    while True:
        try:
            # сюда позже вернём bot polling / handlers
            print(">>> TELEGRAM HEARTBEAT")
            await asyncio.sleep(5)

        except Exception as e:
            print("[TELEGRAM ERROR]", e)

if __name__ == "__main__":
    asyncio.run(loop())
