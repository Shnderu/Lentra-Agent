from aiogram import Router, types, F

from lentra.bot.services.search_pipeline import SearchPipeline
from lentra.bot.state.state_store import StateStore
from lentra.bot.core.state_machine import StateMachine

from lentra.bot.cards.builder import CardBuilder
from lentra.bot.cards.renderer import CardRenderer
from lentra.bot.ux.keyboard import UXKeyboard

router = Router()

pipeline = SearchPipeline()
state_store = StateStore()
sm = StateMachine()

builder = CardBuilder()
renderer = CardRenderer()
kb = UXKeyboard()


def paginate(items, page, size):
    start = page * size
    return items[start:start + size]


@router.message()
async def handle_search(message: types.Message):
    user_id = message.from_user.id
    query = message.text

    state = await pipeline.execute(user_id, query)

    page_items = paginate(state.results, state.page, state.page_size)

    for item in page_items:
        card = builder.build(item)
        text, keyboard = renderer.render_list_card(card)
        await message.answer(text, reply_markup=keyboard)

    await message.answer("Навигация:", reply_markup=kb.pagination())


@router.callback_query(F.data.startswith("detail:"))
async def detail(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.split(":")[1]

    state = state_store.load(user_id)
    state = sm.set_detail(state, item_id)
    state_store.save(state)

    item = next((x for x in state.results if x["id"] == item_id), None)
    if not item:
        await callback.answer("Not found")
        return

    card = builder.build(item)
    text, keyboard = renderer.render_detail(card)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "page:next")
async def next_page(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state = state_store.load(user_id)

    state = sm.next_page(state)
    state_store.save(state)

    await callback.message.answer("➡ следующая страница")
    await callback.answer()


@router.callback_query(F.data == "page:prev")
async def prev_page(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state = state_store.load(user_id)

    state = sm.prev_page(state)
    state_store.save(state)

    await callback.message.answer("⬅ предыдущая страница")
    await callback.answer()


@router.callback_query(F.data == "back:list")
async def back(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state = state_store.load(user_id)

    page_items = paginate(state.results, state.page, state.page_size)

    for item in page_items:
        card = builder.build(item)
        text, keyboard = renderer.render_list_card(card)
        await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()
