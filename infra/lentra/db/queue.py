# ============================================================
# LENTRA POSTGRES QUEUE (FIXED V10.24 - ALIGN WITH DB SCHEMA)
# ============================================================

from typing import Dict, Any, Optional


class PostgresQueue:
    """
    Единая очередь задач (aligned with processing_queue table)
    """

    def __init__(self, pool):
        self.pool = pool

    async def create_task(self, task: Dict[str, Any]) -> None:
        query = """
        INSERT INTO processing_queue (task_type, payload, status)
        VALUES ($1, $2, 'new');
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                task["type"],
                task["payload"]
            )

    async def claim_task(self) -> Optional[Dict[str, Any]]:
        query = """
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status = 'new'
        ORDER BY id ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED;
        """

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query)

            if not row:
                return None

            await conn.execute(
                "UPDATE processing_queue SET status='processing' WHERE id=$1",
                row["id"]
            )

            return dict(row)

    async def mark_done(self, task_id: int) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE processing_queue SET status='done' WHERE id=$1",
                task_id
            )

    async def mark_failed(self, task_id: int, error: str = "") -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE processing_queue SET status='failed' WHERE id=$1",
                task_id
            )
