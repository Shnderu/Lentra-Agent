from lentra.domain.handlers.telegram_message import handle as telegram_message_handler

def handle_parse_property(event):
    return {"status": "ok"}

def handle_ranking_event(event):
    return {"status": "ok"}


HANDLERS = {
    "parse_property": handle_parse_property,
    "ranking_event": handle_ranking_event,
    "telegram_message": telegram_message_handler
}
