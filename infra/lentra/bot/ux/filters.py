from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FiltersUI:

    def build(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🏊 бассейн", callback_data="filter:pool:toggle"),
                InlineKeyboardButton(text="🌊 море", callback_data="filter:sea:toggle"),
            ],
            [
                InlineKeyboardButton(text="💰 до 5 млн", callback_data="filter:price:5"),
                InlineKeyboardButton(text="💰 до 10 млн", callback_data="filter:price:10"),
            ],
            [
                InlineKeyboardButton(text="🔁 применить", callback_data="filter:apply"),
            ]
        ])
