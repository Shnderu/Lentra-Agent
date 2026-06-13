import asyncio
import os
import json
import psycopg2

from aiogram import Bot


class Sender:

    def __init__(self):
        self.bot = Bot(os.getenv("BOT_TOKEN"))
        self.dsn = os.getenv("DATABASE_URL")

    def get_conn(self):
        return psycopg2.connect(self.dsn)

    def fetch_done(self):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload, result
            FROM tasks
            WHERE status = 'done'
            ORDER BY id
            LIMIT 20
        """)

        rows = cur.fetchall()
        conn.close()
        return rows

    def mark_sent(self, task_id: int):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'sent',
                updated_at = NOW()
            WHERE id = %s
        """, (task_id,))

        conn.commit()
        conn.close()

    async def loop(self):

        print(">>> SENDER V2 STARTED")

        while True:

            tasks = self.fetch_done()

            for task_id, payload, result in tasks:

                try:
                    if isinstance(payload, str):
                        payload = json.loads(payload)

                    user_id = payload["user_id"]

                    await self.bot.send_message(
                        chat_id=user_id,
                        text=str(result)
                    )

                    self.mark_sent(task_id)

                except Exception as e:
                    print("[SENDER ERROR]", e)

            await asyncio.sleep(2)


async def main():
    sender = Sender()
    try:
        await sender.loop()
    finally:
        await sender.bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
