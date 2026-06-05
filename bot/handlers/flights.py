from aiogram import Router
from aiogram.types import Message

from bot.services.routes import (
    add_route,
    get_routes,
    delete_routes,
)

router = Router()


@router.message(lambda m: m.text.startswith("/add"))
async def add_flight(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Использование:\n/add MOW BKK"
        )
        return

    route = parts[1]

    add_route(
        message.from_user.id,
        route
    )

    await message.answer(
        f"Маршрут добавлен:\n{route}"
    )


@router.message(lambda m: m.text == "/list")
async def list_flights(message: Message):

    routes = get_routes(
        message.from_user.id
    )

    if not routes:
        await message.answer(
            "Маршрутов нет"
        )
        return

    text = "\n".join(routes)

    await message.answer(
        f"Ваши маршруты:\n\n{text}"
    )


@router.message(lambda m: m.text == "/delete")
async def delete_flights(message: Message):

    delete_routes(
        message.from_user.id
    )

    await message.answer(
        "Все маршруты удалены"
    )
