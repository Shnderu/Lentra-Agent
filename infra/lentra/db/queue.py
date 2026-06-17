# ============================================================
# LENTRA POSTGRES QUEUE (FIXED STABLE LAYER V10.21)
# SINGLE SOURCE OF TRUTH FOR TASK EXECUTION
# ============================================================

from typing import Dict, Any, Optional


class PostgresQueue:
    """
    Единая очередь задач.
    Используется worker_engine + api + rent pipeline.
    """

    def __init__(self, pool):
        self.pool = pool

    async def create_task(self, task: Dict[str, Any]) -> None:
        query = """
        INSERT INTO tasks (type, payload, status, attempts)
        VALUES ($1, $2, 'pending', 0);
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                task["type"],
                task["payload"]
            )

    async def claim_task(self) -> Optional[Dict[str, Any]]:
        query = """
        SELECT id, type, payload, attempts
        FROM tasks
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED;
        """

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query)

            if not row:
                return None

            await conn.execute(
                "UPDATE tasks SET status='processing' WHERE id=$1",
                row["id"]
            )

            return dict(row)

    async def mark_done(self, task_id: int) -> None:
        query = """
        UPDATE tasks
        SET status='done'
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
        UPDATE tasks
        SET status='failed',
            attempts=$2
        WHERE id=$1;
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, task_id, attempts)

