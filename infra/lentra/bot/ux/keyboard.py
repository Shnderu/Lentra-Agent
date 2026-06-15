from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardBuilder:

    def list_view(self, results: list):

        buttons = []

        for r in results[:5]:
            buttons.append([
                InlineKeyboardButton(
                    text=f"🏡 {r['title'][:22]}",
                    callback_data=f"detail:{r['id']}"
                )
            ])

        buttons.append([
            InlineKeyboardButton(text="🏊 Pool", callback_data="filter:pool:1"),
            InlineKeyboardButton(text="🌊 Sea", callback_data="filter:sea:1")
        ])

        buttons.append([
            InlineKeyboardButton(text="💰 <5M", callback_data="filter:max_price:5")
        ])

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    def detail_view(self, item_id: str):

        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Back", callback_data="back_list")
            ]
        ])
