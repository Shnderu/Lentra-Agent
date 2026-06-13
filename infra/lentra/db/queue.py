# ============================================================
# PATCH: CREATE TASK (V15.8 EXTENSION)
# ============================================================

    async def create_task(self, task: Dict[str, Any]):
        query = """
        INSERT INTO tasks (type, payload, status, attempts)
        VALUES ($1, $2, 'pending', 0);
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, task["type"], task["payload"])

        logger.info(f"[QUEUE] task created: {task['type']}")
