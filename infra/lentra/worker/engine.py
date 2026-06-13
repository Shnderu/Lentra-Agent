# ============================================================
# LENTRA WORKER ENGINE V15.4 (PIPELINE INTEGRATION LAYER)
# ============================================================

import asyncio
import logging
from typing import Dict, Any, Optional

from lentra.rent.domain_v1 import create_rent_router

logger = logging.getLogger("lentra.worker")


# ============================================================
# 1. ROUTER INIT
# ============================================================

router = create_rent_router()


# ============================================================
# 2. CONTRACT VALIDATION (V15.2 INTEGRATION HOOK)
# ============================================================

def validate_task_contract(task: Dict[str, Any]) -> bool:
    if "id" not in task:
        raise ValueError("[CONTRACT] missing task.id")

    if "type" not in task:
        raise ValueError("[CONTRACT] missing task.type")

    if "payload" not in task:
        raise ValueError("[CONTRACT] missing task.payload")

    return True


# ============================================================
# 3. TASK STORE ABSTRACTION (POSTGRES HOOK PLACEHOLDER)
# ============================================================

class TaskStore:
    """
    Абстракция над PostgreSQL queue.
    В реальной системе здесь будут SQL SELECT ... FOR UPDATE SKIP LOCKED
    """

    async def fetch_task(self) -> Optional[Dict[str, Any]]:
        # TODO: заменить на реальный SQL fetch
        return None

    async def mark_done(self, task_id: int):
        logger.info(f"[DB] task {task_id} -> done")

    async def mark_failed(self, task_id: int, reason: str):
        logger.error(f"[DB] task {task_id} -> failed: {reason}")


# ============================================================
# 4. WORKER CORE LOOP
# ============================================================

class WorkerEngine:
    def __init__(self, store: TaskStore):
        self.store = store
        self.running = True

    async def process(self, task: Dict[str, Any]):
        validate_task_contract(task)

        result = await router.route(task)

        await self.store.mark_done(task["id"])

        return result

    async def run(self):
        logger.info("[WORKER] started")

        while self.running:
            try:
                task = await self.store.fetch_task()

                if not task:
                    await asyncio.sleep(1)
                    continue

                try:
                    await self.process(task)

                except Exception as e:
                    await self.store.mark_failed(task["id"], str(e))

            except Exception as loop_error:
                logger.error(f"[WORKER LOOP ERROR] {loop_error}")
                await asyncio.sleep(2)


# ============================================================
# 5. ENTRYPOINT
# ============================================================

def create_worker(store: TaskStore) -> WorkerEngine:
    return WorkerEngine(store)
