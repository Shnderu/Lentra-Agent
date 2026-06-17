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
from app.core.dlq import DeadLetterQueue
from app.core.retry_policy import RetryPolicy


def main():
    bus = EventBus(None, DeadLetterQueue(), RetryPolicy())

    print("[BOOT] v7 real source integration")

    inputs = [
        "rent apartment Bangkok",
        "rent studio Bangkok 500",
        "hello world"
    ]

    span = Span(trace_id="GLOBAL")

    for t in inputs:
        event = Event(type="USER_MESSAGE", payload={"text": t})
        bus.publish(event, span, None)


if __name__ == "__main__":
    main()
