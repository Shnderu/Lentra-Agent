from aiogram import Router, F
from aiogram.types import Message

from lentra.bot.services.registry import Registry
from lentra.bot.core.fsm import FSMEngine
from lentra.bot.services.search_pipeline import SearchPipeline

router = Router()

registry = Registry()
fsm = FSMEngine()

pipeline = SearchPipeline(
    search_service=registry.search_service,
    state_store=registry.state_store,
    fsm=fsm
)


def build_message_router(container):
    return router


@router.message(F.text)
async def handle_search(message: Message):

    await pipeline.execute(
        user_id=message.from_user.id,
        query=message.text,
        message=message
    )
