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

def burst(thread_id):
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    # 🔥 BURST PHASE (high pressure)
    for i in range(500):
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
            300000 + thread_id * 10000 + i,
            random.choice(task_types),
            json.dumps({"thread": thread_id, "seq": i})
        ))

        if i % 50 == 0:
            conn.commit()
            print(f"[LOAD V3] thread={thread_id} inserted={i}")

        time.sleep(0.01)  # почти без паузы = stress

    conn.commit()
    conn.close()


print("[LOAD V3] STARTED (STRESS MODE)")

threads = []

# 8 параллельных потоков
for t in range(8):
    th = threading.Thread(target=burst, args=(t,))
    th.start()
    threads.append(th)

for th in threads:
    th.join()

print("[LOAD V3] DONE")
