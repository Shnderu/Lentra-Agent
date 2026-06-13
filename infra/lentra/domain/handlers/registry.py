from lentra.domain.vietnam.adapter import get_vietnam_properties


def handle_parse_property(payload):
    return {
        "ux": {
            "screen": "property_list",
            "title": "Подобрано для тебя",
            "cards": get_vietnam_properties(payload)
        },
        "telegram_text": "🏠 Список объектов сформирован"
    }


def handle_ranking_event(payload):
    # временный fallback (чтобы не падало)
    return {
        "ux": {
            "screen": "ranking",
            "title": "Ranking обработан",
            "data": payload
        },
        "telegram_text": "📊 Ranking event processed"
    }


def handle_telegram_message(payload):
    return {
        "ux": {
            "screen": "telegram_ack",
            "title": "Сообщение получено",
            "data": payload
        },
        "telegram_text": "💬 Message received"
    }


HANDLERS = {
    "parse_property": handle_parse_property,
    "ranking_event": handle_ranking_event,
    "telegram_message": handle_telegram_message,
}
