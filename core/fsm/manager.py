
from core.fsm.context import set_state, get_state, set_data, get_data, clear
from core.search.engine import SearchEngine
from core.deals.engine import DealEngine
from core.ai.planner.engine import AIPlanner


search_engine = SearchEngine()
deal_engine = DealEngine()
planner = AIPlanner()


async def handle_message(user_id: int, text: str):

    state = get_state(user_id)
    data = get_data(user_id)

    # ROUTE FLOW
    if state == "route_from":
        set_data(user_id, "from", text)
        set_state(user_id, "route_to")
        return "✈️ Куда летим?"

    if state == "route_to":
        set_data(user_id, "to", text)
        set_state(user_id, "route_date")
        return "📅 Когда вылет?"

    if state == "route_date":

        data = get_data(user_id)
        clear(user_id)

        result = search_engine.search_route(
            origin=data["from"],
            destination=data["to"],
            date=text
        )

        return f"✈️ Найдено {result['count']} вариантов"

    # WATCH FLOW
    if state == "watch_from":
        set_data(user_id, "from", text)
        set_state(user_id, "watch_to")
        return "👉 Куда следить?"

    if state == "watch_to":
        set_data(user_id, "to", text)
        set_state(user_id, "watch_price")
        return "💰 Целевая цена?"

    if state == "watch_price":
        data = get_data(user_id)
        clear(user_id)

        return "👀 Мониторинг запущен"

    # PLANNER FLOW
    if state == "planner_input":
        clear(user_id)

        result = planner.plan(text, user_id)

        return f"🧠 AI обработал запрос (task {result['task_id']})"

    return None
