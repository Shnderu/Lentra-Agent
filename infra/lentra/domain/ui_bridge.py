def handle_screen(screen: str, event: dict) -> dict:

    if screen == "main":
        return {"text": "Главное меню готово"}

    if screen == "rent":
        return {"text": "🏠 Аренда\nВведите город или район для поиска."}

    if screen == "search":
        return {"text": "🔎 Поиск\nВведите запрос:"}

    if screen == "alerts":
        return {"text": "📊 Уведомления\nНастройка алертов."}

    if screen == "profile":
        return {"text": "👤 Профиль"}

    return {"text": "Неизвестный сценарий"}
