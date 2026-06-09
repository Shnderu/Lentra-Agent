
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def show_home(message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✈️ Поиск рейса", callback_data="ui:route_search")],
        [InlineKeyboardButton(text="🔥 Горящие предложения", callback_data="ui:deals")],
        [InlineKeyboardButton(text="👀 Мониторинг цен", callback_data="ui:watch")],
        [InlineKeyboardButton(text="🧠 AI Планировщик", callback_data="ui:planner")]
    ])

    await message.answer(
        "✈️ FlyRum AI\nВыберите сценарий:",
        reply_markup=keyboard
    )
