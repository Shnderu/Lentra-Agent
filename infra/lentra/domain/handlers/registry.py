def safe_handler(name):
    def fallback(payload, state):
        return {"ux": {"screen": "error"}}
    return fallback


HANDLERS = {}


try:
    from lentra.domain.handlers.parse_property import handle as parse_property
    HANDLERS["parse_property"] = parse_property
except:
    HANDLERS["parse_property"] = safe_handler("parse_property")


try:
    from lentra.domain.handlers.ranking_event import handle as ranking_event
    HANDLERS["ranking_event"] = ranking_event
except:
    HANDLERS["ranking_event"] = safe_handler("ranking_event")


try:
    from lentra.domain.handlers.telegram_message import handle as telegram_message
    HANDLERS["telegram_message"] = telegram_message
except:
    HANDLERS["telegram_message"] = safe_handler("telegram_message")
