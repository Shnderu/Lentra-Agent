import time
import threading
import psycopg2
import json
import random

DB = {
    "dbname": "lentra",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432
}

task_types = ["telegram_message", "parse_property", "ranking_event"]

def worker_thread(thread_id):
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    i = 0
    while i < 200:
        i += 1

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
            200000 + thread_id * 1000 + i,
            random.choice(task_types),
            json.dumps({"thread": thread_id, "seq": i})
        ))

        conn.commit()

        if i % 20 == 0:
            print(f"[LOAD V2] thread={thread_id} inserted={i}")

        time.sleep(random.uniform(0.05, 0.2))

    conn.close()


print("[LOAD V2] STARTED")

threads = []

# 5 параллельных потоков
for t in range(5):
    th = threading.Thread(target=worker_thread, args=(t,))
    th.start()
    threads.append(th)

for th in threads:
    th.join()

print("[LOAD V2] DONE")
