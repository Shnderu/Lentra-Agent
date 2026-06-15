from aiogram import Router, types
from lentra.bot.services.search_pipeline import SearchPipeline
from lentra.bot.state.state_store import StateStore

router = Router()

pipeline = SearchPipeline()
state_store = StateStore()


@router.message()
async def handle_search(message: types.Message):
    user_id = message.from_user.id
    query = message.text

    state = await pipeline.execute(user_id, query)

    # LIST RENDER
    if state.mode == "LIST":
        for item in state.results:
            await message.answer(item["text"])
        return

    await message.answer("No results")
