USER_STATE = {}


def start_rent(chat_id: int) -> dict:
    USER_STATE[chat_id] = {
        "step": "city"
    }

    return {
        "text": "🏠 Аренда\nВведите город или район:",
        "next_step": "city"
    }


def handle_rent(chat_id: int, text: str) -> dict:
    state = USER_STATE.get(chat_id, {"step": "city"})
    step = state["step"]

    # =========================
    # STEP 1: CITY
    # =========================
    if step == "city":
        state["city"] = text
        state["step"] = "budget"

        return {
            "text": f"📍 Город: {text}\nТеперь укажи бюджет (например 500-1000$):"
        }

    # =========================
    # STEP 2: BUDGET
    # =========================
    if step == "budget":
        state["budget"] = text
        state["step"] = "search"

        city = state.get("city")

        return {
            "text": (
                f"🔎 Поиск жилья\n"
                f"Город: {city}\n"
                f"Бюджет: {text}\n\n"
                f"Ищу варианты..."
            ),
            "action": "search_rentals",
            "payload": state
        }

    return {
        "text": "Ошибка rental flow"
    }
