import asyncio
import os
import psycopg2
import json
from aiogram import Bot

bot = Bot(os.getenv("BOT_TOKEN"))


def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


async def loop():
    print(">>> FIXED SENDER V11.5")

    while True:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload, result
            FROM tasks
            WHERE status = 'done'
            LIMIT 10
            FOR UPDATE SKIP LOCKED
        """)

        rows = cur.fetchall()

        for task_id, payload, result in rows:

            try:
                if isinstance(payload, str):
                    payload = json.loads(payload)

                user_id = payload["user_id"]

                await bot.send_message(user_id, str(result))

                cur.execute("""
                    UPDATE tasks
                    SET status='sent',
                        updated_at=NOW()
                    WHERE id=%s
                """, (task_id,))

                conn.commit()

            except Exception as e:
                print("[ERROR]", e)

        conn.close()
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(loop())
