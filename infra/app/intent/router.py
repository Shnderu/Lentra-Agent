from typing import Any, Dict

# FIX: unified import layer over scattered implementations
# выбираем реальный существующий router

try:
    from lentra.core.router.intent_router import IntentRouter as _IntentRouter
except Exception:
    try:
        from lentra.telegram.intent.router import IntentRouter as _IntentRouter
    except Exception:
        from lentra.bot.core.intent_router import IntentRouter as _IntentRouter


class IntentRouter(_IntentRouter):
    """
    Compatibility layer:
    гарантирует что worker всегда может делать:
        route(user_input, ctx)
    """

    def classify(self, user_input: Dict[str, Any]):
        # backward compatibility
        if hasattr(super(), "classify"):
            return super().classify(user_input)
        return {"type": "fallback"}

    def route(self, user_input: Dict[str, Any], ctx: Dict[str, Any] = None):
        # FIX: нормализуем ctx
        ctx = ctx or {}
        if hasattr(super(), "route"):
            try:
                return super().route(user_input, ctx)
            except TypeError:
                return super().route(user_input)
        return {"type": "fallback"}
