from typing import Dict, Any
import psycopg2


class FeatureStore:
    """
    In-memory feature cache (v1)
    - feedback signals
    - future: embeddings, user signals, aggregations
    """

    def __init__(self, conn):
        self.conn = conn
        self._cache = None

    def load_feedback_agg(self) -> Dict[int, Dict[str, Any]]:
        """
        Returns:
            {
                property_id: {
                    "views": int,
                    "clicks": int,
                    "likes": int
                }
            }
        """

        if self._cache is not None:
            return self._cache

        cur = self.conn.cursor()

        try:
            cur.execute("""
                SELECT property_id, views, clicks, likes
                FROM property_feedback_agg
            """)

            rows = cur.fetchall()

            self._cache = {
                r[0]: {
                    "views": r[1],
                    "clicks": r[2],
                    "likes": r[3]
                }
                for r in rows
            }

            return self._cache

        finally:
            cur.close()
