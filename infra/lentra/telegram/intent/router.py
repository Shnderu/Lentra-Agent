from lentra.telegram.ui.router import resolve_screen
from lentra.telegram.ui.router import render


def route(event: dict) -> dict:
    text = (event.get("text") or "").strip()

    # нормализация
    lower = text.lower()

    # базовый UX routing
    if lower in ["/start", "start", "меню", "menu"]:
        screen = "main"
        return render(screen)

    if "аренда" in lower or "rent" in lower:
        screen = "rent"
        return render(screen)

    if "поиск" in lower or "search" in lower:
        return {
            "text": "🔎 Поиск\nВведите запрос:",
            "reply_markup": {
                "keyboard": [["🏠 Главное меню"]],
                "resize_keyboard": True
            }
        }

    if "профиль" in lower or "profile" in lower:
        return {
            "text": "👤 Профиль\n(пока пусто)",
            "reply_markup": {
                "keyboard": [["🏠 Главное меню"]],
                "resize_keyboard": True
            }
        }

    # fallback — ВСЕГДА возвращаем UI, никогда пустоту
    return {
        "text": f"📩 Получено: {text}",
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
