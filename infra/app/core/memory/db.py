import sqlite3
import os

DB_PATH = "data/memory.db"


class MemoryDB:

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id TEXT PRIMARY KEY,
            city TEXT,
            budget INTEGER
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS interaction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query TEXT
        )
        """)

        self.conn.commit()

    # -------------------------
    # PROFILE
    # -------------------------

    def get_profile(self, user_id: str):
        cur = self.conn.cursor()
        cur.execute("SELECT city, budget FROM user_profile WHERE user_id=?", (user_id,))
        row = cur.fetchone()

        if not row:
            return {"city": None, "budget": None}

        return {"city": row[0], "budget": row[1]}

    def update_profile(self, user_id: str, city=None, budget=None):
        cur = self.conn.cursor()

        profile = self.get_profile(user_id)

        city = city or profile["city"]
        budget = budget or profile["budget"]

        cur.execute("""
        INSERT INTO user_profile (user_id, city, budget)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            city=excluded.city,
            budget=excluded.budget
        """, (user_id, city, budget))

        self.conn.commit()

    # -------------------------
    # HISTORY
    # -------------------------

    def add_query(self, user_id: str, query: str):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO interaction_history (user_id, query) VALUES (?, ?)",
            (user_id, query)
        )
        self.conn.commit()

    def get_history(self, user_id: str, limit=10):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT query FROM interaction_history
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT ?
        """, (user_id, limit))

        return [r[0] for r in cur.fetchall()]
