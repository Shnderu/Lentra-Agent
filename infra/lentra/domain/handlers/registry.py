from lentra.domain.handlers.parse_property import handle as parse_property
from lentra.domain.handlers.ranking_event import handle as ranking_event
from lentra.domain.handlers.telegram_message import handle as telegram_message

HANDLERS = {
    "parse_property": parse_property,
    "ranking_event": ranking_event,
    "telegram_message": telegram_message
}
