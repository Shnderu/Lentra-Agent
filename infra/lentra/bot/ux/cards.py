from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class CardRenderer:

    def render_list(self, results: list, search_id: str, page: int):

        buttons = []

        for r in results:

            text = f"{r['title']} · {r['price_vnd_mln']}M · ⭐{r['score']}"

            buttons.append([
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"item:{r['id']}"
                )
            ])

        nav = [
            InlineKeyboardButton(
                text="◀",
                callback_data=f"search:{search_id}:page:{page-1}"
            ),
            InlineKeyboardButton(
                text="▶",
                callback_data=f"search:{search_id}:page:{page+1}"
            )
        ]

        buttons.append(nav)

        return InlineKeyboardMarkup(inline_keyboard=buttons)
