from lentra.domain.vietnam.adapter import get_vietnam_properties
from lentra.ux.composer.engine import compose_properties


def run_scenario(intent, payload, state):

    if intent == "property_search":
        props = get_vietnam_properties(payload, state)

        # ❗ ВАЖНО: передаём в composer, а не строим UI тут
        return compose_properties(props)

    if intent == "chat":
        return {
            "screen": "chat",
            "type": "text",
            "text": "Готов помочь с арендой во Вьетнаме."
        }

    return {
        "screen": "default",
        "type": "text",
        "text": "Запрос обработан"
    }
