from dataclasses import dataclass


# =========================
# SCREENS
# =========================

SCREEN_MAIN = "main"
SCREEN_START = "start"
SCREEN_UNKNOWN = "unknown"


# =========================
# UI LAYOUTS (Telegram text + buttons)
# =========================

UI = {
    SCREEN_START: {
        "text": "Привет 👋 Я Lentra Agent\nВыбери действие:",
        "keyboard": [
            ["🏠 Главное меню"]
        ]
    },

    SCREEN_MAIN: {
        "text": "Главное меню:",
        "keyboard": [
            ["🏠 Аренда"],
            ["🔎 Поиск"],
            ["📊 Уведомления"],
            ["👤 Профиль"]
        ]
    },

    SCREEN_UNKNOWN: {
        "text": "Команда не распознана. Вернись в меню:",
        "keyboard": [
            ["🏠 Главное меню"]
        ]
    }
}


# =========================
# STATE RESOLVER
# =========================

def resolve_screen(text: str, state: dict = None) -> str:
    text = (text or "").strip().lower()

    if text in ["/start", "start"]:
        return SCREEN_START

    if text in ["🏠 главное меню", "menu", "/menu"]:
        return SCREEN_MAIN

    if state and state.get("screen"):
        return state["screen"]

    return SCREEN_UNKNOWN


# =========================
# RENDER ENGINE
# =========================

def render(screen_id: str) -> dict:
    screen = UI.get(screen_id, UI[SCREEN_UNKNOWN])

    return {
        "text": screen["text"],
        "reply_markup": {
            "keyboard": screen["keyboard"],
            "resize_keyboard": True,
            "one_time_keyboard": False
        },
        "screen": screen_id
    }
