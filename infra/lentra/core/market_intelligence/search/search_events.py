from lentra.core.market_intelligence.events.event_bus import EventBus

bus = EventBus()


def emit_search_event(listing: dict):
    try:
        bus.publish("search_event", {
            "price": listing.get("price"),
            "title": listing.get("title"),
            "event_emitted": True
        })
    except:
        pass
