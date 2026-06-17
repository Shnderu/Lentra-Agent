# ============================================================
# LENTRA POSTGRES QUEUE (FIXED V10.25 - ATOMIC CLAIM FIX)
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
        """
        Атомарное захватывание задачи.
        ВАЖНО: одна транзакция + RETURNING
        """

        query = """
        UPDATE processing_queue
        SET status = 'processing',
            started_at = NOW()
        WHERE id = (
            SELECT id
            FROM processing_queue
            WHERE status = 'new'
            ORDER BY id ASC
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING id, task_type, payload;
        """

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(query)

                if not row:
                    return None

                return dict(row)

    async def mark_done(self, task_id: int) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE processing_queue
                SET status = 'done',
                    processed_at = NOW()
                WHERE id = $1
                """,
                task_id
            )

    async def mark_failed(self, task_id: int, error: str = "") -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE processing_queue
                SET status = 'failed',
                    error_text = $2,
                    failed_at = NOW()
                WHERE id = $1
                """,
                task_id,
                error
            )
