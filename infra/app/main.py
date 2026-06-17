from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_intelligence_handler,
    rent_search_handler,
    response_handler,
    unknown_handler
)
from app.core.trace import Span
from app.core.metrics import LatencyHistogram, EventGraph
from app.core.executor import TaskExecutor
from app.core.dlq import DeadLetterQueue
from app.core.retry_policy import RetryPolicy
from app.core.replay import ReplayEngine


def main():
    executor = TaskExecutor(max_workers=4, max_queue=5)
    dlq = DeadLetterQueue()
    retry_policy = RetryPolicy(max_retries=2)

    bus = EventBus(executor, dlq, retry_policy)

    hist = LatencyHistogram()
    graph = EventGraph()

    # 🔥 новый слой
    bus.subscribe("USER_MESSAGE", lambda e, s, g: bus.publish(intent_router(e, s, g), s, g, e))
    bus.subscribe("INTENT", lambda e, s, g: bus.publish(rent_intelligence_handler(e, s, g), s, g, e))
    bus.subscribe("RENT_SEARCH", lambda e, s, g: bus.publish(rent_search_handler(e, s, g), s, g, e))

    bus.subscribe("RESPONSE", lambda e, s, g: response_handler(e, s, g))
    bus.subscribe("UNKNOWN", lambda e, s, g: unknown_handler(e, s, g))

    print("[BOOT] v6 + RENT INTELLIGENCE REINTEGRATED")

    inputs = [
        "rent apartment in Bangkok 800",
        "rent studio Saigon",
        "hello world",
        "rent villa Bali 2000"
    ]

    span = Span(trace_id="GLOBAL")
    span.hist = hist

    for t in inputs:
        event = Event(type="USER_MESSAGE", payload={"text": t})
        bus.publish(event, span, graph)

    print("\n--- DLQ ---")
    dlq.dump()

    print("\n--- GRAPH ---")
    graph.dump()


if __name__ == "__main__":
    main()
