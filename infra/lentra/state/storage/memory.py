# ============================================================
# STATE STORAGE V16.5 (MVP IN-MEMORY)
# ============================================================

from typing import Dict
from lentra.state.models import UserSession, SavedSearch


class MemoryStateStore:
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.saved_searches: Dict[str, SavedSearch] = {}

    # -------------------------
    # SESSIONS
    # -------------------------

    def get_session(self, user_id: str):
        return self.sessions.get(user_id)

    def create_session(self, user_id: str):
        session = UserSession(user_id=user_id)
        self.sessions[user_id] = session
        return session

    def update_session(self, user_id: str, preferences: dict):
        session = self.sessions.get(user_id)
        if not session:
            session = self.create_session(user_id)

        session.preferences.update(preferences)
        session.last_active = __import__("time").time()

        return session

    # -------------------------
    # SAVED SEARCHES
    # -------------------------

    def save_search(self, user_id: str, query: dict):
        search_id = f"ss_{len(self.saved_searches)+1}"

        search = SavedSearch(
            id=search_id,
            user_id=user_id,
            query=query,
        )

        self.saved_searches[search_id] = search
        return search

    def get_user_searches(self, user_id: str):
        return [
            s for s in self.saved_searches.values()
            if s.user_id == user_id and s.active
        ]
