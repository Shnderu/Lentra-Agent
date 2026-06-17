from typing import Dict, Any


class MemoryStore:
    """
    Простая in-memory память пользователя
    (v10 минимальная реализация)
    """

    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def get(self, user_id: str) -> Dict[str, Any]:
        return self.store.get(user_id, {})

    def update(self, user_id: str, data: Dict[str, Any]):
        current = self.store.get(user_id, {})
        current.update(data)
        self.store[user_id] = current

    def clear(self, user_id: str):
        if user_id in self.store:
            del self.store[user_id]
