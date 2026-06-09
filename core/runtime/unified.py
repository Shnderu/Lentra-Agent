from core.fsm.context import get_state
from core.fsm.manager import handle_message
from core.intent.router import route


async def unified_entry(message):

    user_id = message.from_user.id
    text = message.text

    state = get_state(user_id)

    print("🧠 UNIFIED INPUT:", text)
    print("🧠 CURRENT STATE:", state)

    # ----------------------------------
    # FSM FIRST
    # ----------------------------------

    if state != "idle":
        result = await handle_message(user_id, text)

        print("🧠 FSM RESULT:", result)

        return result

    # ----------------------------------
    # INTENT FLOW
    # ----------------------------------

    result = await route(user_id, text)

    print("🧠 ROUTE RESULT:", result)

    return result
