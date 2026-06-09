
from core.ui.controller import route_ui


async def handle_ui(callback_data: str, message):

    if not callback_data:
        return None

    if callback_data.startswith("ui:"):
        action = callback_data.replace("ui:", "")
    else:
        action = callback_data

    return await route_ui(action, message)
