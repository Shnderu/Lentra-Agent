import psycopg2


class FeedbackRepo:

    def __init__(self, conn):
        self.conn = conn

    def load(self):
        cur = self.conn.cursor()

        cur.execute("""
            SELECT
                property_id,
                views,
                clicks,
                likes
            FROM property_feedback_agg
        """)

        rows = cur.fetchall()
        cur.close()

        return {
            r[0]: {
                "views": r[1] or 0,
                "clicks": r[2] or 0,
                "likes": r[3] or 0
            }
            for r in rows
        }
