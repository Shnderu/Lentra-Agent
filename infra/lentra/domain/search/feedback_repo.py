import psycopg2


class FeedbackRepo:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="lentra",
            user="lentra",
            password="lentra",
            host="localhost",
            port=5432
        )

    def load(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT property_id, views, clicks, likes
            FROM property_feedback_agg
        """)

        data = {}
        for pid, v, c, l in cur.fetchall():
            data[pid] = {
                "view": v,
                "click": c,
                "like": l
            }

        cur.close()
        return data
