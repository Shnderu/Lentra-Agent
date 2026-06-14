from lentra.domain.handlers.registry import HANDLERS


def route(event: dict) -> dict:
    text = (event.get("text") or "").strip()

    # --- INTENTS ---
    if text == "/start":
        return {
            "text": "Привет 👋 Я Lentra Agent. Система активна."
        }

    if text == "/help":
        return {
            "text": "Доступные команды: /start /help"
        }

    # --- DOMAIN HANDLER ---
    handler = HANDLERS.get("telegram_message")

    if handler:
        return handler(event)

    return {
        "text": "Команда не распознана"
    }
