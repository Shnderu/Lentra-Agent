from lentra.core.intent_router import classify
from lentra.storage.db import get_conn

def push_to_queue(conn, task):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO processing_queue (task_type, payload, status)
        VALUES (%s, %s, 'new')
    """, (task["task_type"], json.dumps(task["payload"])))
    cur.close()


def main():
    conn = get_conn()
    print("[INTENT ROUTER] ACTIVE")

    while True:
        # имитация входящего сообщения
        msg = input("> ")

        task = classify(msg)

        push_to_queue(conn, task)

        conn.commit()
        print("[ROUTED]", task)
