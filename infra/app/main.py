# v8: main теперь только для тестов pipeline, не API

from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_intelligence_handler,
    rent_fetch_handler,
    rent_aggregate_handler,
    response_handler,
    unknown_handler
)
from app.core.trace import Span


def main():
    print("[BOOT] v8 core test mode (not API)")

    span = Span(trace_id="LOCAL_TEST")

    bus = EventBus(None, None, None)

    inputs = [
        "rent apartment Bangkok",
        "rent studio Bangkok",
        "hello world"
    ]

    for t in inputs:
        event = Event(type="USER_MESSAGE", payload={"text": t})
        bus.publish(event, span, None)


if __name__ == "__main__":
    main()
