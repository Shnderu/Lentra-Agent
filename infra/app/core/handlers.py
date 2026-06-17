from app.core.events import Event
from app.services.rent_search import rent_search
from app.core.trace import Span
import time


def intent_router(event: Event, span: Span):
    span.start("router")

    text = event.payload.get("text", "")
    time.sleep(0.02)  # имитация parsing

    if "rent" in text.lower():
        out = Event(
            type="RENT_SEARCH",
            payload={"query": text},
            trace_id=event.trace_id
        )
    else:
        out = Event(
            type="UNKNOWN",
            payload={"raw": text},
            trace_id=event.trace_id
        )

    span.end("router")
    return out


def rent_search_handler(event: Event, span: Span):
    span.start("rent_handler")

    query = event.payload.get("query")

    result = rent_search(query)

    span.start("rent_service_call")
    time.sleep(0.01)
    span.end("rent_service_call")

    span.end("rent_handler")

    return Event(
        type="RESPONSE",
        payload=result,
        trace_id=event.trace_id
    )


def response_handler(event: Event, span: Span):
    span.start("response")
    print(f"[RESPONSE] {event.payload}")
    span.end("response")


def unknown_handler(event: Event, span: Span):
    span.start("unknown")
    print(f"[UNKNOWN] {event.payload}")
    span.end("unknown")
