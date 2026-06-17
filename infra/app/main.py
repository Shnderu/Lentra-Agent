from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_search_handler,
    response_handler,
    unknown_handler
)
from app.core.trace import Span
from app.core.metrics import LatencyHistogram, EventGraph
from app.core.executor import TaskExecutor
from app.core.dlq import DeadLetterQueue


def main():
    executor = TaskExecutor(max_workers=4, max_queue=5)
    dlq = DeadLetterQueue()

    bus = EventBus(executor, dlq)

    hist = LatencyHistogram()
    graph = EventGraph()

    bus.subscribe("USER_MESSAGE", lambda e, s, g: bus.publish(intent_router(e, s, g), s, g, e))
    bus.subscribe("RENT_SEARCH", lambda e, s, g: bus.publish(rent_search_handler(e, s, g), s, g, e))
    bus.subscribe("RESPONSE", lambda e, s, g: response_handler(e, s, g))
    bus.subscribe("UNKNOWN", lambda e, s, g: unknown_handler(e, s, g))

    print("[BOOT] v5 production-grade diagnostic pipeline")

    inputs = [
        "rent apartment Ho Chi Minh",
        "hello world",
        "rent studio Bangkok",
        "rent villa Bali",
        "rent cheap flat Saigon"
    ]

    for t in inputs:
        span = Span(trace_id="trace-" + t[:6])
        span.hist = hist

        event = Event(type="USER_MESSAGE", payload={"text": t})

        bus.publish(event, span, graph)

        span.report()

    print("\n--- METRICS ---")
    hist.dump_all()

    print("\n--- DLQ ---")
    dlq.dump()

    print("\n--- GRAPH ---")
    graph.dump()


if __name__ == "__main__":
    main()
