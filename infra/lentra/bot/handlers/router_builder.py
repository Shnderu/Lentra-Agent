from aiogram import Router
from lentra.telegram.ui.renderer import renderer


def build_main_router():
    router = Router()

    # пример базового handler'а (если уже есть — адаптируй сюда)
    # важно: UI не через container, а напрямую

    @router.message()
    async def default_handler(message):
        text = renderer.render_message(
            {
                "screen": "property_list",
                "cards": []
            }
        )
        await message.answer(text)

    return router
