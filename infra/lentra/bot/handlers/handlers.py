from aiogram import Router

router = Router()

# IMPORTANT:
# no pipeline init here
# no service init here
# handlers must be pure registration layer

from aiogram.types import Message
from aiogram import F

from lentra.bot.services.search_pipeline import SearchPipeline

pipeline = None


def get_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = SearchPipeline()
    return pipeline


@router.message(F.text)
async def handle_search(message: Message):
    p = get_pipeline()

    state = await p.execute(
        user_id=message.from_user.id,
        query=message.text
    )

    await message.answer(f"Found: {len(state.results)} results")
