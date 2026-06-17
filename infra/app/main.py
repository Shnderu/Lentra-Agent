from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_search_handler,
    response_handler,
    unknown_handler
)
from app.core.trace import Span


def main():
    bus = EventBus()

    bus.subscribe("USER_MESSAGE", lambda e, s: bus.publish(intent_router(e, s), s))
    bus.subscribe("RENT_SEARCH", lambda e, s: bus.publish(rent_search_handler(e, s), s))
    bus.subscribe("RESPONSE", lambda e, s: response_handler(e, s))
    bus.subscribe("UNKNOWN", lambda e, s: unknown_handler(e, s))

    print("[BOOT] pipeline v2 latency tracing enabled")

    test_events = [
        "I want rent apartment in Ho Chi Minh",
        "hello world"
    ]

    for text in test_events:
        span = Span(trace_id="trace-" + text[:5])

        event = Event(
            type="USER_MESSAGE",
            payload={"text": text}
        )

        bus.publish(event, span)
        span.report()


if __name__ == "__main__":
    main()
