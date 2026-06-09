from core.search.engine import SearchEngine
from core.alerts.triggers import check_triggers
from core.alerts.dispatcher import send_notification


engine = SearchEngine()


class AlertEngine:

    def process_watch(self, watch):

        result = engine.search_route(
            origin=watch["from"],
            destination=watch["to"],
            date=watch.get("date")
        )

        best_price = result["best_price"]

        triggers = check_triggers(watch, best_price)

        if not triggers:
            return {"status": "no_event"}

        event = {
            "watch_id": watch["id"],
            "price": best_price,
            "triggers": triggers
        }

        send_notification(watch["user_id"], event)

        return event
