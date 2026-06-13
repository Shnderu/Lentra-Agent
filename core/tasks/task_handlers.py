"""
ЧИСТЫЕ БИЗНЕС-ХЕНДЛЕРЫ
(без БД, без Telegram, только логика)
"""


def route_search_handler(payload: dict):
    return {
        "routes": [],
        "price": 0
    }


def notify_user_handler(payload: dict):
    return {
        "sent": True
    }


def alert_engine_handler(payload: dict):
    return {
        "triggered": True
    }


HANDLERS = {
    "route_search": route_search_handler,
    "notify_user": notify_user_handler,
    "alert_engine": alert_engine_handler
}
