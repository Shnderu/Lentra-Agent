from aiogram import Router, types
from lentra.bot.core.container import Container


def build_main_router(container: Container) -> Router:

    router = Router()

    @router.message()
    async def handle_search(message: types.Message):

        query = message.text

        results = await container.search_service.search(query=query)

        text = "\n".join(
            f"🏠 {r.title} — {r.price_vnd_mln} млн VND"
            for r in results
        )

        await message.answer(text or "Ничего не найдено")

    return router
