import psycopg2
import os
import time
import json

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "lentra"),
    "password": os.getenv("DB_PASSWORD", "lentra"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": 5432,
}


def conn():
    c = psycopg2.connect(**DB_CONFIG)
    c.autocommit = True
    return c


def fetch(cur):
    cur.execute("""
        SELECT id, task_type, payload
        FROM public.processing_queue
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 20
    """)
    return cur.fetchall()


def mark_done(cur, task_id):
    cur.execute("""
        UPDATE public.processing_queue
        SET status = 'done',
            processed_at = NOW()
        WHERE id = %s
    """, (task_id,))


def main():
    print("[WORKER FINAL CLEAN STARTED]")

    connection = conn()
    cur = connection.cursor()

    while True:
        try:
            tasks = fetch(cur)

            for task_id, task_type, payload in tasks:

                # payload ALWAYS jsonb
                if isinstance(payload, str):
                    payload = json.loads(payload)

                chat_id = payload.get("chat_id")
                text = payload.get("text", "")

                print("[EXEC]", task_id, task_type, chat_id, text)

                # UI routing
                if text == "/start":
                    response_text = "Главное меню"
                elif "аренда" in text.lower():
                    response_text = "🏠 Аренда\nВведите город:"
                else:
                    response_text = "Команда не распознана"

                # push response task for consumer
                cur.execute("""
                    INSERT INTO processing_queue (
                        task_type,
                        payload,
                        status
                    )
                    VALUES (
                        'SEND_MESSAGE',
                        %s,
                        'pending'
                    )
                """, (json.dumps({
                    "chat_id": chat_id,
                    "text": response_text
                }),))

                mark_done(cur, task_id)

            time.sleep(1)

        except Exception as e:
            print("[WORKER ERROR]", e)
            time.sleep(2)


if __name__ == "__main__":
    main()
