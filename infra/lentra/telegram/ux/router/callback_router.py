from typing import Dict, Callable, Any


class CallbackRouter:
    """
    Maps Telegram callback_data → handler
    """

    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def register(self, key: str, handler: Callable):
        self.routes[key] = handler

    def handle(self, callback_data: str, context: Dict[str, Any]):
        """
        callback_data format:
        action:payload
        """
        if not callback_data:
            return {"screen": "error"}

        parts = callback_data.split(":", 1)
        action = parts[0]
        payload = parts[1] if len(parts) > 1 else None

        handler = self.routes.get(action)

        if not handler:
            return {"screen": "error"}

        return handler(payload, context)
