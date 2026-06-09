
from core.intent.router import route


async def handle_update(message):

    user_id = message.from_user.id
    text = message.text or ""

    result = await route(user_id, text, source="message")

    await message.answer(str(result))
