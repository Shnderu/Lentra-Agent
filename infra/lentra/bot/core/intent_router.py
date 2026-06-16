from typing import Callable, Dict, Any


class IntentRouter:
    """
    Простейший intent-router (без AI).
    Позже можно расширить до LLM routing.
    """

    def __init__(self):
        self._routes: Dict[str, Callable] = {}

    def register(self, intent: str, handler: Callable):
        self._routes[intent] = handler

    async def route(self, intent: str, ctx: Dict[str, Any]):
        handler = self._routes.get(intent)
        if not handler:
            return None
        return await handler(ctx)
