import psycopg2


class FeedbackStore:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="lentra",
            user="lentra",
            password="lentra",
            host="localhost",
            port=5432
        )

    def save(self, event: dict):
        cur = self.conn.cursor()

        cur.execute("""
            INSERT INTO user_feedback (user_id, property_id, event_type, meta, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (
            event["user_id"],
            event["property_id"],
            event["event_type"],
            event["meta"]
        ))

        self.conn.commit()
        cur.close()
