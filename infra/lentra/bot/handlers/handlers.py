from aiogram import Router, F
from aiogram.types import Message


def build_message_router(container) -> Router:

    router = Router()

    pipeline = container.search_pipeline

    @router.message(F.text)
    async def handle_search(message: Message):

        await pipeline.execute(
            user_id=message.from_user.id,
            query=message.text,
            message=message
        )

    return router
