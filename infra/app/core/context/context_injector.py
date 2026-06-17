from app.core.session.session_store import SessionStore


class ContextInjector:

    def __init__(self):
        self.store = SessionStore()

    def enrich(self, user_id: str, intent: dict):
        session = self.store.get(user_id)

        enriched = dict(intent)

        # если нет city — берём из памяти
        if not enriched.get("city"):
            enriched["city"] = session.get("city")

        # если нет budget — берём из памяти
        if not enriched.get("budget"):
            enriched["budget"] = session.get("budget")

        enriched["session"] = session

        return enriched

    def update(self, user_id: str, intent: dict):
        self.store.update(user_id, intent)
