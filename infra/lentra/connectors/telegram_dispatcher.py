import time
import os
import requests
import psycopg2

DB = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432"))
}

BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_ME")


def get_conn():
    return psycopg2.connect(**DB)


def fetch_done(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, raw_message_id, result
        FROM processing_queue
        WHERE status='done'
          AND result IS NOT NULL
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })


def mark_sent(conn, task_id):
    cur = conn.cursor()
    cur.execute("""
        UPDATE processing_queue
        SET status='sent'
        WHERE id=%s
    """, (task_id,))
    cur.close()


def main():
    print("[DISPATCHER] started")

    conn = get_conn()
    conn.autocommit = False

    while True:
        try:
            rows = fetch_done(conn)

            if not rows:
                conn.commit()
                time.sleep(0.5)
                continue

            for task_id, chat_id, result in rows:
                try:
                    text = result["message"] if isinstance(result, dict) else str(result)

                    send_message(chat_id, text)
                    mark_sent(conn, task_id)

                    print(f"[SENT] task={task_id}")

                except Exception as e:
                    print(f"[DISPATCH ERROR] {task_id}: {e}")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"[FATAL]: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
