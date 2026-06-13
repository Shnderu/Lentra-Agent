import asyncio
import os
import psycopg2
import json
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

async def send_loop():
    print(">>> SENDER V12 STARTED")

    while True:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload, result
            FROM tasks
            WHERE status = 'done'
            ORDER BY id ASC
            LIMIT 10
        """)

        rows = cur.fetchall()
        conn.close()

        for task_id, payload, result in rows:
            try:
                if isinstance(payload, str):
                    payload = json.loads(payload)

                user_id = payload["user_id"]

                await bot.send_message(user_id, str(result))

                conn = get_conn()
                cur = conn.cursor()

                cur.execute("""
                    UPDATE tasks
                    SET status = 'sent',
                        updated_at = NOW()
                    WHERE id = %s
                """, (task_id,))

                conn.commit()
                conn.close()

            except Exception as e:
                print("[SENDER ERROR]", e)

                conn = get_conn()
                cur = conn.cursor()

                cur.execute("""
                    UPDATE tasks
                    SET status = 'failed',
                        result = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (str(e), task_id))

                conn.commit()
                conn.close()

        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(send_loop())
