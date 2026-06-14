from lentra.telegram.ux.router.init_router import router


def build_telegram_message(result: dict, context: dict = None):
    """
    UX result → Telegram payload with callback awareness
    """

    context = context or {}

    ux = result.get("ux", {})

    # allow callback-driven override
    callback = ux.get("callback_data")

    if callback:
        return router.handle(callback, context)

    return {
        "screen": ux.get("screen", "error"),
        "text": ux.get("text", ""),
        "cards": ux.get("cards", []),
        "buttons": ux.get("buttons", [])
    }
