# ============================================================
# LENTRA RENT SUBSCRIPTIONS V15.8
# ============================================================

from typing import Dict, Any, List
import time


class SubscriptionStore:
    """
    Простое in-memory хранилище.
    В проде заменяется на PostgreSQL таблицу subscriptions.
    """

    def __init__(self):
        self.subscriptions: List[Dict[str, Any]] = []

    def add(self, query: Dict[str, Any], user_id: str):
        self.subscriptions.append({
            "id": f"sub_{int(time.time()*1000)}",
            "user_id": user_id,
            "query": query,
            "last_seen_ids": set(),
        })

    def all(self):
        return self.subscriptions
