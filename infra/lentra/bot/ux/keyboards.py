from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UXKeyboards:

    def results(self, query: str, offset: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Следующие",
                    callback_data=f"next:{query}:{offset}"
                ),
                InlineKeyboardButton(
                    text="🔁 Новый поиск",
                    callback_data="new_search"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎯 Фильтры",
                    callback_data=f"filters:{query}"
                )
            ]
        ])
