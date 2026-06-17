from app.core.event_bus import EventBus
from app.core.events import Event
from app.core.handlers import (
    intent_router,
    rent_search_handler,
    response_handler,
    unknown_handler
)


def main():
    bus = EventBus()

    # регистрация pipeline
    bus.subscribe("USER_MESSAGE", lambda e: bus.publish(intent_router(e)))
    bus.subscribe("RENT_SEARCH", lambda e: bus.publish(rent_search_handler(e)))
    bus.subscribe("RESPONSE", response_handler)
    bus.subscribe("UNKNOWN", unknown_handler)

    print("[BOOT] minimal event pipeline started")

    # test input
    bus.publish(Event(
        type="USER_MESSAGE",
        payload={"text": "I want rent apartment in Ho Chi Minh"}
    ))

    bus.publish(Event(
        type="USER_MESSAGE",
        payload={"text": "hello"}
    ))


if __name__ == "__main__":
    main()
