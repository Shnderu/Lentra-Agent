def parse_property(payload, state):
    return {
        "ux": {
            "screen": "property_list",
            "cards": payload.get("properties", [])
        }
    }

def ranking_event(payload, state):
    return {
        "ux": {
            "screen": "ranking",
            "data": payload
        }
    }

def telegram_message(payload, state):
    return {
        "ux": {
            "screen": "telegram_ack"
        }
    }

HANDLERS = {
    "parse_property": parse_property,
    "ranking_event": ranking_event,
    "telegram_message": telegram_message
}
