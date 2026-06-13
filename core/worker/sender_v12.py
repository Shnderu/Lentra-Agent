import asyncio
import os
import json
import psycopg2

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
            WITH cte AS (
                SELECT id, payload, result
                FROM tasks
                WHERE status = 'pending'
                ORDER BY id
                FOR UPDATE SKIP LOCKED
                LIMIT 10
            )
            UPDATE tasks t
            SET status = 'processing',
                updated_at = NOW()
            FROM cte
            WHERE t.id = cte.id
            RETURNING t.id, t.payload, t.result;
        """)

        rows = cur.fetchall()
        conn.commit()
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
