from lentra.core.runtime.trace_graph_v2 import RuntimeTraceV2
from lentra.telegram.router.intent_router import IntentRouter
from lentra.telegram.connectors.telegram_event_listener import TelegramEventListener


class Orchestrator:

    def __init__(self):

        # TRACE LAYER (side effect only)
        self.trace = RuntimeTraceV2(trace_id="telegram-runtime")

        # PURE LOGIC LAYER
        self.router = IntentRouter()

        # ADAPTER LAYER
        self.listener = TelegramEventListener(
            router=self.router,
            trace=self.trace
        )

    def listener_instance(self):
        return self.listener

    def router_instance(self):
        return self.router

    def trace_instance(self):
        return self.trace
