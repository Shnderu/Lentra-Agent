from lentra.telegram.connectors.telegram_event_listener import TelegramEventListener
from lentra.core.router.intent_router import IntentRouter
from lentra.core.trace.trace import Trace

def build_graph_v2():
    trace = Trace()

    router = IntentRouter(
        handlers={
            "default": lambda e: {"ok": True}
        }
    )

    listener = TelegramEventListener(
        router=router,
        trace=trace
    )

    return {
        "listener": listener,
        "router": router,
        "trace": trace
    }
