from lentra.core.memory.db import MemoryDB


class ContextInjector:

    def __init__(self):
        self.db = MemoryDB()

    def enrich(self, user_id: str, intent: dict):

        profile = self.db.get_profile(user_id)
        history = self.db.get_history(user_id)

        enriched = dict(intent)

        # 🔥 persistent memory override
        enriched["city"] = enriched.get("city") or profile.get("city")
        enriched["budget"] = enriched.get("budget") or profile.get("budget")

        enriched["session"] = {
            "profile": profile,
            "history": history
        }

        return enriched

    def update(self, user_id: str, intent: dict):

        city = intent.get("city")
        budget = intent.get("budget")

        if city or budget:
            self.db.update_profile(user_id, city=city, budget=budget)

        self.db.add_query(user_id, intent.get("raw", ""))
