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


def main():
    bus = EventBus()

    hist = LatencyHistogram()
    graph = EventGraph()

    bus.subscribe("USER_MESSAGE", lambda e, s, g: bus.publish(intent_router(e, s, g), s, g, e))
    bus.subscribe("RENT_SEARCH", lambda e, s, g: bus.publish(rent_search_handler(e, s, g), s, g, e))
    bus.subscribe("RESPONSE", lambda e, s, g: response_handler(e, s, g))
    bus.subscribe("UNKNOWN", lambda e, s, g: unknown_handler(e, s, g))

    print("[BOOT] v3 diagnostics pipeline")

    test_inputs = [
        "I want rent apartment in Ho Chi Minh",
        "hello world",
        "rent studio in Bangkok"
    ]

    for text in test_inputs:
        span = Span(trace_id="trace-" + text[:6])
        span.hist = hist

        event = Event(type="USER_MESSAGE", payload={"text": text})

        bus.publish(event, span, graph)

        span.report()

    print("\n--- METRICS ---")
    print(hist.summary("rent_search"))

    graph.dump()


if __name__ == "__main__":
    main()
