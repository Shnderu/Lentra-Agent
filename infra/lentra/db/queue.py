# ============================================================
# LENTRA POSTGRES QUEUE (FIXED STABLE V10.22)
# SINGLE SOURCE OF TRUTH: processing_queue
# ============================================================

from typing import Dict, Any, Optional


class PostgresQueue:
    """
    Очередь задач на базе таблицы processing_queue.
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
        SELECT id, task_type, payload, status
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
                """
                UPDATE processing_queue
                SET status='processing',
                    ingested_at=now()
                WHERE id=$1
                """,
                row["id"]
            )

            return dict(row)

    async def mark_done(self, task_id: int) -> None:
        query = """
        UPDATE processing_queue
        SET status='done',
            processed_at=now()
        WHERE id=$1;
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, task_id)

    async def mark_failed(
        self,
        task_id: int,
        error: str,
        attempts: int = 0
    ) -> None:
        query = """
        UPDATE processing_queue
        SET status='failed'
        WHERE id=$1;
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, task_id)

