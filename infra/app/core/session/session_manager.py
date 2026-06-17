from app.core.session.memory_store import MemoryStore


class SessionManager:

    def __init__(self):
        self.memory = MemoryStore()

    def extract_context(self, user_id: str):
        return self.memory.get(user_id)

    def update_context(self, user_id: str, intent: dict):
        update = {}

        if intent.get("city"):
            update["city"] = intent["city"]

        if intent.get("budget"):
            update["budget"] = intent["budget"]

        if update:
            self.memory.update(user_id, update)
