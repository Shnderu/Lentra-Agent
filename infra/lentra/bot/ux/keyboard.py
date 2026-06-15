from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UXKeyboard:

    def list_card(self, item_id: str):
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Подробнее", callback_data=f"detail:{item_id}"),
                InlineKeyboardButton(text="♡ Сохранить", callback_data=f"save:{item_id}")
            ]
        ])

    def detail_card(self, item_id: str):
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅ Назад", callback_data="back:list"),
                InlineKeyboardButton(text="♡ Сохранить", callback_data=f"save:{item_id}")
            ]
        ])
