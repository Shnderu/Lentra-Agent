import json
import asyncio

from core.ingestion.lock import acquire_lock, release_lock
from core.ingestion.router import load_sources, select_sources


class IngestionProcessorV5:

    def __init__(self, r):
        self.r = r
        self.sources = load_sources()

    def _load(self, task_id):
        raw = self.r.get(f"task:{task_id}")
        return json.loads(raw) if raw else None

    def _save(self, task):
        self.r.set(f"task:{task['id']}", json.dumps(task))

    async def _execute(self, task):

        from core.ingestion.parallel import AsyncExecutor

        executor = AsyncExecutor(self.sources)

        source_names = select_sources(task["payload"])

        results = await executor.run(source_names, task["payload"])

        task["status"] = "done"
        task["result"] = {
            "listings": results,
            "sources_used": source_names,
            "meta": {
                "version": "ingestion_v5"
            }
        }

        self._save(task)

    def run(self, task_id: str):
        task = self._load(task_id)
        if not task:
            return

        if not acquire_lock(self.r, task_id):
            return

        try:
            task["status"] = "running"
            self._save(task)

            asyncio.run(self._execute(task))

        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            self._save(task)

        finally:
            release_lock(self.r, task_id)
