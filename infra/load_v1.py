import time
import psycopg2
import random
import json

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

cur = conn.cursor()

task_types = ["telegram_message", "parse_property", "ranking_event"]

print("[LOAD V1] STARTED")

i = 0

while True:
    i += 1

    task_type = random.choice(task_types)

    cur.execute("""
        INSERT INTO processing_queue (
            raw_message_id,
            task_type,
            payload,
            status,
            created_at,
            ingested_at
        )
        VALUES (%s, %s, %s, 'new', NOW(), NOW())
    """, (
        100000 + i,
        task_type,
        json.dumps({"seq": i, "source": "load_v1"})
    ))

    conn.commit()

    if i % 10 == 0:
        print(f"[LOAD V1] inserted={i}")

    time.sleep(0.3)
