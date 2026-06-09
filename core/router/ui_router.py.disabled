
from core.ui.controller import route_ui


async def handle_ui(callback_data, message):

    mapping = {
        "ui:home": "home",
        "ui:route_search": "route_search",
        "ui:deals": "deals",
        "ui:watch": "watch",
        "ui:planner": "planner",
        "ui:onboarding": "onboarding"
    }

    action = mapping.get(callback_data, "home")

    return await route_ui(action, message)
