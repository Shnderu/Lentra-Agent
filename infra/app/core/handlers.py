from app.core.events import Event
from app.services.rent_search import rent_search


def intent_router(event: Event):
    """
    Точка маршрутизации.
    Здесь чаще всего ломается логика.
    """

    text = event.payload.get("text", "")

    print(f"[ROUTER] trace={event.trace_id} text={text}")

    if "rent" in text.lower():
        return Event(
            type="RENT_SEARCH",
            payload={"query": text},
            trace_id=event.trace_id
        )

    return Event(
        type="UNKNOWN",
        payload={"raw": text},
        trace_id=event.trace_id
    )


def rent_search_handler(event: Event):
    """
    Интеграция внешнего сервиса — основная зона риска
    """

    query = event.payload.get("query")

    print(f"[RENT_SEARCH] trace={event.trace_id} query={query}")

    result = rent_search(query)

    print(f"[RENT_SEARCH_RESULT] trace={event.trace_id} result={result}")

    return Event(
        type="RESPONSE",
        payload=result,
        trace_id=event.trace_id
    )


def response_handler(event: Event):
    print(f"[RESPONSE] trace={event.trace_id} payload={event.payload}")


def unknown_handler(event: Event):
    print(f"[UNKNOWN] trace={event.trace_id} payload={event.payload}")
