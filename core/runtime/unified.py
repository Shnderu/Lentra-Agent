
from core.intent.router import route as intent_route
from core.fsm.context import get_state
from core.fsm.manager import handle_message as fsm_handle
from core.router.ui_router import handle_ui


async def unified_entry(update):

    user_id = update.from_user.id

    text = getattr(update, "text", None)
    data = getattr(update, "data", None)

    # -------------------------
    # UI CALLBACK FLOW (FIXED)
    # -------------------------
    if data:
        result = await handle_ui(data, update.message)
        return result

    # -------------------------
    # FSM OVERRIDE
    # -------------------------
    state = get_state(user_id)

    if state and state != "idle":
        return await fsm_handle(user_id, text)

    # -------------------------
    # INTENT ROUTING
    # -------------------------
    result = await intent_route(user_id, text, source="message")

    if not result:
        return "🤖 I didn't understand your request"

    return result
