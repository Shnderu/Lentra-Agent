# ============================================================
# STATE SERVICE V16.5
# ============================================================

from lentra.state.storage.memory import MemoryStateStore


class StateService:
    def __init__(self):
        self.store = MemoryStateStore()

    def init_user(self, user_id: str):
        return self.store.create_session(user_id)

    def update_preferences(self, user_id: str, prefs: dict):
        return self.store.update_session(user_id, prefs)

    def save_search(self, user_id: str, query: dict):
        return self.store.save_search(user_id, query)

    def get_context(self, user_id: str):
        session = self.store.get_session(user_id)
        searches = self.store.get_user_searches(user_id)

        return {
            "session": session,
            "saved_searches": searches,
        }
