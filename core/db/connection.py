import os
import time
import psycopg2


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "readme_to_recover"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


def get_conn(retries: int = 5, delay: float = 1.5):
    """
    Единая точка подключения к БД.
    Добавлен retry слой (защита от docker startup race condition).
    """

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(**DB_CONFIG)

            # ВАЖНО: autocommit включаем глобально
            # чтобы не ловить зависшие транзакции в worker/queue
            conn.autocommit = True

            return conn

        except Exception as e:
            last_error = e
            print(f"[DB CONNECT RETRY] attempt {attempt}/{retries} error={e}")
            time.sleep(delay)

    raise RuntimeError(f"[DB FATAL] cannot connect: {last_error}")
