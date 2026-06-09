
from core.ui.controller import route_ui


async def handle_ui(callback_data, message):

    # нормализация callback
    if not callback_data:
        return None

    return await route_ui(callback_data, message)
