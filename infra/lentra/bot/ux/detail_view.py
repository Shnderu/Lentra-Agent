from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class DetailView:

    def render(self, item: dict):

        text = (
            f"🏠 {item['title']}\n"
            f"📍 {item['city']} · {item['district']}\n"
            f"💰 {item['price_vnd_mln']}M VND\n"
            f"⭐ {item['score']}\n"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data=f"back:list:{item['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❤️ Сохранить",
                    callback_data=f"save:{item['id']}"
                ),
                InlineKeyboardButton(
                    text="📊 Похожие",
                    callback_data=f"similar:{item['id']}"
                )
            ]
        ])

        return text, keyboard
