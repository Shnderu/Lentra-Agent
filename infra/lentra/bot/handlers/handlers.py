from aiogram import Router
from aiogram.types import Message

from lentra.bot.services.registry import search_service

router = Router()


@router.message()
async def handle_search(message: Message):
    query = message.text

    results = await search_service.search(query=query)

    if not results:
        await message.answer("Ничего не найдено")
        return

    top = results[:5]

    text = "\n".join(
        f"{r.title} — {r.price_vnd_mln} млн VND"
        for r in top
    )

    await message.answer(text)
