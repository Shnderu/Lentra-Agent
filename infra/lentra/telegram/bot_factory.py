from lentra.telegram.runtime import TelegramRuntime
from lentra.telegram.connectors.telegram_event_listener import TelegramEventListener
from lentra.core.router.intent_router import IntentRouter
from lentra.core.trace.trace_validator import TraceValidator


def create_bot():
    router = IntentRouter()
    trace = None

    listener = TelegramEventListener(
        router=router,
        trace=trace
    )

    runtime = TelegramRuntime(
        listener=listener,
        router=router,
        trace=trace
    )

    # 🔒 IMMUTABLE GATE
    validator = TraceValidator()
    validator.validate(router, listener, trace)

    return runtime
