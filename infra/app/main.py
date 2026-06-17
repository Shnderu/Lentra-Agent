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
from app.core.retry_policy import RetryPolicy
from app.core.replay import ReplayEngine


def main():
    executor = TaskExecutor(max_workers=4, max_queue=5)
    dlq = DeadLetterQueue()
    retry_policy = RetryPolicy(max_retries=2)

    bus = EventBus(executor, dlq, retry_policy)

    hist = LatencyHistogram()
    graph = EventGraph()

    bus.subscribe("USER_MESSAGE", lambda e, s, g: bus.publish(intent_router(e, s, g), s, g, e))
    bus.subscribe("RENT_SEARCH", lambda e, s, g: bus.publish(rent_search_handler(e, s, g), s, g, e))
    bus.subscribe("RESPONSE", lambda e, s, g: response_handler(e, s, g))
    bus.subscribe("UNKNOWN", lambda e, s, g: unknown_handler(e, s, g))

    print("[BOOT] v6 production control pipeline")

    inputs = [
        "rent apartment Ho Chi Minh",
        "hello world",
        "rent studio Bangkok",
        "rent villa Bali"
    ]

    span = Span(trace_id="GLOBAL_TRACE")
    span.hist = hist

    for t in inputs:
        event = Event(type="USER_MESSAGE", payload={"text": t})
        bus.publish(event, span, graph)

    print("\n--- DLQ BEFORE REPLAY ---")
    dlq.dump()

    replay = ReplayEngine(bus, dlq)
    replay.replay_all(span, graph)

    print("\n--- FINAL GRAPH ---")
    graph.dump()


if __name__ == "__main__":
    main()
