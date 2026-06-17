from collections import defaultdict


class SessionStore:
    """
    Простая in-memory сессия.
    Хранит контекст пользователя между запросами.
    """

    def __init__(self):
        self.sessions = defaultdict(lambda: {
            "city": None,
            "budget": None,
            "history": []
        })

    def get(self, user_id: str):
        return self.sessions[user_id]

    def update(self, user_id: str, intent: dict):
        s = self.sessions[user_id]

        if intent.get("city"):
            s["city"] = intent["city"]

        if intent.get("budget"):
            s["budget"] = intent["budget"]

        s["history"].append(intent.get("raw", ""))

        return s
