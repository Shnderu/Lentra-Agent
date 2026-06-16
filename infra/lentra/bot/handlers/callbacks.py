from aiogram import Router, F
from aiogram.types import CallbackQuery

from lentra.bot.ux.callback_parser import CallbackParser


def build_callback_router(container) -> Router:

    router = Router()

    fsm = container.fsm
    store = container.state_store
    renderer = container.renderer

    @router.callback_query(F.data)
    async def handle(call: CallbackQuery):

        event = CallbackParser.parse(call.data)

        state = store.load(call.from_user.id)

        state = fsm.handle(state, event)

        store.save(state)

        await renderer.render(state, call.message)

        await call.answer()

    return router
