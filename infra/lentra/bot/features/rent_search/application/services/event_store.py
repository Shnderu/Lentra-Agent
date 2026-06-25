import asyncpg


class EventStore:

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def init(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def write_event(self, event: dict):

        async with self.pool.acquire() as conn:

            await conn.execute(
                """
                INSERT INTO rent_events
                (event_type, query, city, item_title, item_city, position)
                VALUES ($1,$2,$3,$4,$5,$6)
                """,
                event["event_type"],
                event.get("query"),
                event.get("city"),
                event.get("item_title"),
                event.get("item_city"),
                event.get("position"),
            )
