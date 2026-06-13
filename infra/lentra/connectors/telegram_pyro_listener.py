import time
from lentra.storage.db import get_conn

print("[LENTRA] Listener starting...")

def handle_message(message):
    trace_id = message.id
    now = time.time()

    conn = get_conn()

    conn.execute("""
        INSERT INTO processing_queue (raw_message_id, task_type, payload, status, ingested_at)
        VALUES (%s, %s, %s, %s, to_timestamp(%s))
    """, (trace_id, "telegram_message", {}, "new", now))

    print(f"[INGEST] OK trace={trace_id}")

def main():
    print("[LENTRA] ACTIVE PIPELINE V1")
    while True:
        pass

if __name__ == "__main__":
    main()
