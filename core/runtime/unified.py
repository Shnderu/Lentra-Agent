
from core.fsm.manager import handle_message as fsm_handle
from core.fsm.context import get_state
from core.intent.router import route as intent_route
from core.router.ui_router import handle_ui


async def unified_entry(update):

    user_id = update.from_user.id

    text = getattr(update, "text", None)
    data = getattr(update, "data", None)

    # -------------------------
    # 1. CALLBACK UI ROUTING
    # -------------------------
    if data:
        return await handle_ui(data, update.message)

    # -------------------------
    # 2. FSM OVERRIDE (HIGHEST PRIORITY)
    # -------------------------
    state = get_state(user_id)

    if state and state != "idle":
        result = await fsm_handle(user_id, text)
        return result

    # -------------------------
    # 3. INTENT ROUTER v2
    # -------------------------
    result = await intent_route(user_id, text, source="message")

    return result
