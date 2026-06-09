from core.fsm.flows.route_flow import start_route_flow


async def route_screen(message, state=None):

    # 🔥 CRITICAL FIX: START FSM HERE
    start_route_flow(message.from_user.id)

    await message.answer(
        "✈️ Поиск рейса\n\n"
        "Введите маршрут:\n"
        "Пример: Самара → Париж"
    )
