from lentra.telegram.ux.renderers.telegram_keyboard import build_keyboard


def render_telegram_message(screen: dict):
    """
    Final conversion: UXScreen → Telegram payload
    """

    text = screen.get("text", "")
    buttons = screen.get("buttons", [])

    keyboard = build_keyboard(buttons)

    return {
        "text": text,
        "keyboard": keyboard
    }
