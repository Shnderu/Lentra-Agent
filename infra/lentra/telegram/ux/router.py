from lentra.telegram.ux.screens.registry import SCREEN_MAP


def build_telegram_message(result: dict):
    """
    Converts worker result → UX screen → Telegram payload
    """

    ux = result.get("ux", {})

    screen_type = ux.get("screen", "error")
    cards = ux.get("cards", [])

    builder = SCREEN_MAP.get(screen_type)

    if not builder:
        builder = SCREEN_MAP["error"]

    screen = builder(cards) if screen_type == "property_list" else builder()

    return screen.to_dict()
