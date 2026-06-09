
from core.fsm.context import set_state


def start_watch_flow(user_id: int):

    set_state(user_id, "watch_from")

    return "👀 Откуда следить?"
