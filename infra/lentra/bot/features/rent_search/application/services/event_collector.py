from lentra.bot.features.rent_search.application.services.events import RentEvent


class EventCollector:
    """
    Simple event sink (stub → future DB/stream)
    """

    def track(self, event: RentEvent):

        print(
            f"[EVENT] {event.event_type} "
            f"user={event.user_id} "
            f"city={event.city} "
            f"item={event.item_title} "
            f"pos={event.position}"
        )
