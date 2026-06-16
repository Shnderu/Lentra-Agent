from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardFactory:

    @staticmethod
    def list(results, search_id, page: int):

        buttons = []

        for r in results:
            buttons.append([
                InlineKeyboardButton(
                    text=r["title"],
                    callback_data=f"item:{r['id']}"
                )
            ])

        nav = []

        nav.append(
            InlineKeyboardButton(
                text="◀",
                callback_data=f"search:{search_id}:page:{page-1}"
            )
        )

        nav.append(
            InlineKeyboardButton(
                text="▶",
                callback_data=f"search:{search_id}:page:{page+1}"
            )
        )

        buttons.append(nav)

        return InlineKeyboardMarkup(inline_keyboard=buttons)
