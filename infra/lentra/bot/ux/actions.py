from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UXActions:

    @staticmethod
    def list_keyboard(cards):

        buttons = []

        for c in cards:
            buttons.append([
                InlineKeyboardButton(
                    text=f"Open {c.title[:20]}",
                    callback_data=f"open:{c.id}"
                )
            ])

        buttons.append([
            InlineKeyboardButton(text="⬅️ Prev", callback_data="prev"),
            InlineKeyboardButton(text="➡️ Next", callback_data="next"),
        ])

        return InlineKeyboardMarkup(inline_keyboard=buttons)
