SCREEN_MAIN = "main"
SCREEN_RENT = "rent"


def resolve_screen(text: str) -> str:
    text = (text or "").lower()

    if text in ["/start", "start"]:
        return SCREEN_MAIN

    if "аренда" in text:
        return SCREEN_RENT

    return SCREEN_MAIN


def render(screen: str) -> dict:

    if screen == SCREEN_MAIN:
        return {
            "text": "Главное меню",
            "reply_markup": {
                "keyboard": [
                    ["🏠 Аренда"],
                    ["🔎 Поиск"],
                    ["📊 Уведомления"],
                    ["👤 Профиль"]
                ],
                "resize_keyboard": True
            }
        }

    if screen == SCREEN_RENT:
        return {
            "text": "🏠 Аренда\nВведите город:",
            "reply_markup": {
                "keyboard": [["🏠 Главное меню"]],
                "resize_keyboard": True
            }
        }

    return {
        "text": "Ошибка UI"
    }
