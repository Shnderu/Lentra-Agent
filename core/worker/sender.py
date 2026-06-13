import asyncio
import os
import json
from aiogram import Bot

from core.db.task_claim_v11_3 import claim_tasks
from core.db.task_state_v11_3 import mark_sent, mark_failed
from core.db.task_retry_v11_4 import increase_retry, should_dead_letter
from core.db.dlq_v11_4 import move_to_dlq


BOT_TOKEN = os.getenv("BOT_TOKEN")


async def send_loop():

    if not BOT_TOKEN:
        print("[FATAL] BOT_TOKEN missing")
        return

    bot = Bot(BOT_TOKEN)

    print(">>> SENDER V11.4 STARTED")

    try:
        while True:

            rows = claim_tasks(10)

            for task_id, payload, result in rows:

                try:
                    if isinstance(payload, str):
                        payload = json.loads(payload)

                    user_id = payload.get("user_id")
                    if not user_id:
                        mark_failed(task_id)
                        continue

                    text = result.get("text") if isinstance(result, dict) else str(result)

                    await bot.send_message(user_id, text)

                    mark_sent(task_id)

                except Exception as e:
                    err = str(e)

                    print("[SENDER ERROR]", task_id, err)

                    increase_retry(task_id)

                    # fetch retry count
                    conn = __import__("psycopg2").connect(os.getenv("DATABASE_URL"))
                    cur = conn.cursor()
                    cur.execute("SELECT retry_count FROM tasks WHERE id=%s", (task_id,))
                    retry_count = cur.fetchone()[0]
                    conn.close()

                    if should_dead_letter(retry_count):
                        move_to_dlq(task_id, err)
                    else:
                        mark_failed(task_id)

            await asyncio.sleep(2)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(send_loop())
