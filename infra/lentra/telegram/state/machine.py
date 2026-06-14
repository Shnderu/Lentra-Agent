from lentra.telegram.state.store import get_state, set_state


def next_state(user_id: int, action: str, payload: dict):
    """
    Простая state machine логика
    """

    state = get_state(user_id)

    current_screen = state.get("screen", "start")

    if action == "filter":
        new_state = {
            "screen": "filter",
            "prev": current_screen
        }

    elif action == "refine":
        new_state = {
            "screen": "refine",
            "prev": current_screen
        }

    else:
        new_state = {
            "screen": "start"
        }

    set_state(user_id, new_state)

    return new_state
