import asyncio
import os
import psycopg2
import json
from aiogram import Bot


BOT = Bot(os.getenv("BOT_TOKEN"))


async def run():

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (type, payload, result, status)
        VALUES ('test', '{"user_id": 928857415}', '"STABILITY OK"'::jsonb, 'done')
        RETURNING id;
    """)

    task_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    print("TASK CREATED:", task_id)

    await BOT.send_message(928857415, "STABILITY TEST MESSAGE")

    await BOT.session.close()


if __name__ == "__main__":
    print(">>> STABILITY TEST 03 - SENDER")
    asyncio.run(run())
