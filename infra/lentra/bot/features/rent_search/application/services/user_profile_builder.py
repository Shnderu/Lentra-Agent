import asyncpg


class UserProfileBuilder:

    def __init__(self, dsn: str):
        self.dsn = dsn

    async def rebuild(self):

        conn = await asyncpg.connect(self.dsn)

        rows = await conn.fetch("""
            SELECT
                user_id,
                city,
                AVG(price_value) as avg_price
            FROM user_rent_events
            WHERE event_type = 'click'
            GROUP BY user_id, city
        """)

        for r in rows:

            await conn.execute("""
                INSERT INTO user_rent_profile (user_id, preferred_city, avg_price, updated_at)
                VALUES ($1, $2, $3, now())
                ON CONFLICT (user_id)
                DO UPDATE SET
                    preferred_city = EXCLUDED.preferred_city,
                    avg_price = EXCLUDED.avg_price,
                    updated_at = now()
            """,
            r["user_id"],
            r["city"],
            r["avg_price"])

        await conn.close()
