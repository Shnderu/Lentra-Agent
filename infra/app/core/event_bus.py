from app.core.handlers import (
    intent_router,
    rent_intelligence_handler,
    rent_fetch_handler,
    rent_aggregate_handler,
    response_handler,
    unknown_handler
)

from app.core.observability.tracer import Tracer


class EventBus:

    def __init__(self, graph, dlq, retry_policy):
        self.graph = graph
        self.dlq = dlq
        self.retry_policy = retry_policy
        self.tracer = Tracer()

        self.handlers = {
            "USER_MESSAGE": rent_intelligence_handler,
            "RENT_FETCH": rent_fetch_handler,
            "RENT_AGGREGATE": rent_aggregate_handler,
            "RESPONSE": response_handler
        }

    def publish(self, event, span, graph=None):

        current = event

        while current:

            handler = self.handlers.get(current.type, unknown_handler)

            trace_id = current.trace_id

            self.tracer.start(trace_id, current.type)

            try:
                current = handler(current, span, graph)

            finally:
                self.tracer.end(trace_id, current.type if current else "UNKNOWN")

        return current
