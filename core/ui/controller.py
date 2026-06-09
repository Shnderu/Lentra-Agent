from core.ui.screens.home import show_home
from core.ui.screens.route_search import route_screen
from core.ui.screens.deals import deals_screen
from core.ui.screens.watch import watch_screen
from core.ui.screens.planner import planner_screen

from core.fsm.flows.route_flow import start_route_flow


async def route_ui(action: str, message, state=None):

    if action == "home":
        return await show_home(message)

    if action == "onboarding":
        return await show_onboarding(message)

    if action == "route_search":
        # 🔥 CRITICAL FIX: start FSM here
        start_route_flow(message.from_user.id)
        return await route_screen(message, state)

    if action == "deals":
        return await deals_screen(message)

    if action == "watch":
        return await watch_screen(message)

    if action == "planner":
        return await planner_screen(message)

    return await show_home(message)
