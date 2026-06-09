
async def route_screen(message, state=None):

    await message.answer(
        "✈️ Поиск рейса\n\n"
        "Введите маршрут:\n"
        "Пример: Самара → Париж"
    )
