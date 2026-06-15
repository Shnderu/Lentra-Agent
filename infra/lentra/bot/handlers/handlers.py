from aiogram import Router, types, F
from lentra.bot.services.search_pipeline import SearchPipeline
from lentra.bot.state.state_store import StateStore
from lentra.bot.cards.builder import CardBuilder
from lentra.bot.cards.renderer import CardRenderer

router = Router()

pipeline = SearchPipeline()
state_store = StateStore()

builder = CardBuilder()
renderer = CardRenderer()


@router.message()
async def handle_search(message: types.Message):
    user_id = message.from_user.id
    query = message.text

    state = await pipeline.execute(user_id, query)

    for item in state.results:
        card = builder.build(item)

        text, kb = renderer.render_list_card(card)

        await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("detail:"))
async def open_detail(callback: types.CallbackQuery):
    item_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    state = state_store.load(user_id)

    item = next((x for x in state.results if x["id"] == item_id), None)
    if not item:
        await callback.answer("Not found")
        return

    card = builder.build(item)

    text, kb = renderer.render_detail(card)

    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "back:list")
async def back_to_list(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    state = state_store.load(user_id)

    for item in state.results:
        card = builder.build(item)
        text, kb = renderer.render_list_card(card)
        await callback.message.answer(text, reply_markup=kb)

    await callback.answer()
