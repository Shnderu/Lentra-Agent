
from core.fsm.context import set_state


def start_route_flow(user_id: int):

    set_state(user_id, "route_from")

    return "✈️ Откуда вылет?"
