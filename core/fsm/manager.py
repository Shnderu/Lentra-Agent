from core.fsm.context import get_state, set_state, set_data, get_data, clear
from core.queue.queue import enqueue


async def handle_message(user_id: int, text: str):

    state = get_state(user_id)
    data = get_data(user_id)

    print("[FSM]", user_id, state, text)

    # -------------------------
    # HARD GUARANTEE: ALWAYS RETURN STRING
    # -------------------------

    if state == "route_from":
        set_data(user_id, "origin", text)
        set_state(user_id, "route_to")
        return "✈️ Куда летим?"

    if state == "route_to":
        set_data(user_id, "destination", text)
        set_state(user_id, "route_date")
        return "📅 Когда вылет?"

    if state == "route_date":
        set_data(user_id, "date", text)

        payload = {
            "origin": data.get("origin"),
            "destination": data.get("destination"),
            "date": text,
            "user_id": user_id
        }

        task_id = enqueue("route_search", payload)

        clear(user_id)

        return (
            "🔍 Ищу рейсы...\n"
            f"{payload['origin']} → {payload['destination']}\n"
            f"Дата: {payload['date']}\n"
            f"Task ID: {task_id}"
        )

    # 🔥 CRITICAL: NEVER RETURN NONE
    clear(user_id)
    return f"⚠️ FSM LOST STATE: {state}"
