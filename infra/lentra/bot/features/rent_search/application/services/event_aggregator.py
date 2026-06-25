import asyncpg


class EventAggregator:

    def __init__(self, dsn: str):
        self.dsn = dsn

    async def compute_click_rates(self):

        conn = await asyncpg.connect(self.dsn)

        rows = await conn.fetch("""
            SELECT
                item_title,
                item_city,
                COUNT(*) FILTER (WHERE event_type='impression') AS impressions,
                COUNT(*) FILTER (WHERE event_type='click') AS clicks
            FROM rent_events
            GROUP BY item_title, item_city
        """)

        stats = {}

        for r in rows:

            key = f"{r['item_city']}:{r['item_title']}"

            impressions = r["impressions"] or 0
            clicks = r["clicks"] or 0

            ctr = clicks / impressions if impressions > 0 else 0.0

            stats[key] = ctr

        await conn.close()

        return stats
