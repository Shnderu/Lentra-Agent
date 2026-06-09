from core.fsm.flows.route_flow import start_route_flow


async def handle_ui(action: str, message):

    user_id = message.chat.id

    print("[UI ROUTER]", action)

    if action == "route_search":
        return start_route_flow(user_id)

    return "UI: unknown action"
