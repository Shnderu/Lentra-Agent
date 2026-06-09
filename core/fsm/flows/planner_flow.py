
from core.fsm.context import set_state


def start_planner_flow(user_id: int):

    set_state(user_id, "planner_input")

    return "🧠 Опиши маршрут своими словами"
