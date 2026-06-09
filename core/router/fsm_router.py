
from core.fsm.manager import handle_message


async def process_fsm(user_id: int, text: str):

    result = await handle_message(user_id, text)

    return result
