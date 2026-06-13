# ============================================================
# LENTRA ALERT ENGINE V15.8
# ============================================================

from typing import Dict, Any, List
import asyncio

from lentra.rent.search_pipeline import run_search_pipeline


class AlertEngine:
    def __init__(self, adapter, subscription_store, task_queue):
        self.adapter = adapter
        self.store = subscription_store
        self.queue = task_queue

    async def scan(self):
        """
        Перезапуск всех подписок → поиск новых объявлений
        """

        for sub in self.store.all():
            raw = await self.adapter.search_listings(sub["query"])

            results = run_search_pipeline(raw, sub["query"])

            new_items = []

            for r in results:
                if r["id"] not in sub["last_seen_ids"]:
                    new_items.append(r)
                    sub["last_seen_ids"].add(r["id"])

            if new_items:
                await self._emit_alert(sub, new_items)

    async def _emit_alert(self, sub, items):
        await self.queue.create_task({
            "type": "notify_new_listing",
            "payload": {
                "user_id": sub["user_id"],
                "items": items
            }
        })
