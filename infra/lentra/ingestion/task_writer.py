import json
import uuid
import psycopg2
import os


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "lentra"),
    "password": os.getenv("DB_PASSWORD", "lentra"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
}


class TaskWriter:

    def __init__(self):
        pass


    def push(self, payload: dict) -> str:

        task_id = str(uuid.uuid4())

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO tasks (
                id,
                payload,
                status
            )
            VALUES (
                %s,
                %s,
                'pending'
            )
            """,
            (
                task_id,
                json.dumps(payload)
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return task_id
