from dataclasses import dataclass
from typing import Any, Callable


# =========================
# TRACE LAYER (immutable)
# =========================

@dataclass(frozen=True)
class Trace:
    enabled: bool = True

    async def emit(self, event: str, payload: dict):
        if self.enabled:
            # здесь можно подключить логгер/экспорт
            print(f"[TRACE] {event}: {payload}")


# =========================
# INTENT ROUTER V2 (SYNC SAFE CONTRACT)
# =========================

class IntentRouter:
    """
    ВАЖНО:
    - НИКАКОГО async внутри route
    - только sync decision → async dispatch вызывается runtime
    """

    def __init__(self, trace: Trace):
        self.trace = trace

    def resolve(self, event: dict) -> Callable:
        """
        PURE routing decision (sync only)
        """
        async def default_handler(e: dict):
            await self.trace.emit("unhandled_event", e)
            return {"status": "ignored"}

        # пример логики
        if event.get("type") == "message":
            return self.handle_message

        return default_handler

    async def handle_message(self, event: dict):
        await self.trace.emit("message", event)
        return {"status": "ok", "type": "message"}


# =========================
# EVENT LISTENER V2
# =========================

class TelegramEventListener:
    def __init__(self, router: IntentRouter, trace: Trace):
        self.router = router
        self.trace = trace

    async def dispatch(self, event: dict):
        await self.trace.emit("event_in", event)

        handler = self.router.resolve(event)

        # async boundary enforcement
        if not callable(handler):
            raise TypeError("Router returned non-callable handler")

        result = await handler(event)

        await self.trace.emit("event_out", result)
        return result


# =========================
# GRAPH IMMUTABLE CONTAINER
# =========================

@dataclass(frozen=True)
class GraphV2:
    listener: TelegramEventListener
    router: IntentRouter
    trace: Trace


def build_graph() -> GraphV2:
    trace = Trace(enabled=True)
    router = IntentRouter(trace=trace)
    listener = TelegramEventListener(router=router, trace=trace)

    return GraphV2(
        listener=listener,
        router=router,
        trace=trace
    )
