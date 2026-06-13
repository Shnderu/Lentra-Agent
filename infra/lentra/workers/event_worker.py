from lentra.events.stream import consume
from lentra.parsers.property_parser import get_property_by_raw_message
from lentra.ml.vector_search import search
from lentra.services.ranking_ensemble import rank
from lentra.services.revenue import score_revenue_value
from lentra.services.telegram_notifier import TelegramNotifier
from lentra.observability.tracker import track
import json

notifier = TelegramNotifier()
notifier.start()


def handle(event):
    data = json.loads(event["data"])

    property_obj = get_property_by_raw_message(data["message_id"])
    if not property_obj:
        return

    candidates = search(property_obj.title or "", limit=20)

    ranked = rank([property_obj])

    revenue_score = score_revenue_value(property_obj)

    for r in ranked:
        track("send", {"property_id": r["id"], "score": r["score"]})

        notifier.send(
            data["chat_id"],
            f"🏠 {r['title']} | score={r['score']:.2f} | rev={revenue_score:.1f}"
        )


if __name__ == "__main__":
    print("[H-LAYER] system active")

    for msg_id, data in consume():
        handle({"data": data})
