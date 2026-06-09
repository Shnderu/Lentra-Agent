
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def show_onboarding(message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Далее →", callback_data="ui:onb_2")]
    ])

    await message.answer(
        "👋 Добро пожаловать в FlyRum AI\n\n"
        "1) Ищем дешёвые билеты\n"
        "2) Следим за ценами 24/7\n"
        "3) AI подбирает маршруты",
        reply_markup=keyboard
    )
