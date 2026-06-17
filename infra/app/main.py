from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_intelligence_handler,
    rent_fetch_handler,
    rent_aggregate_handler,
    response_handler,
    unknown_handler,
    health
)
from app.core.trace import Span


def main():
    bus = EventBus(None, None, None)

    print("[BOOT] v7.1 source health + SLA layer")

    inputs = [
        "rent apartment Bangkok",
        "rent studio Bangkok",
        "rent villa Bangkok",
        "hello world"
    ]

    span = Span(trace_id="GLOBAL")

    for t in inputs:
        event = Event(type="USER_MESSAGE", payload={"text": t})
        bus.publish(event, span, None)

    health.dump()


if __name__ == "__main__":
    main()
