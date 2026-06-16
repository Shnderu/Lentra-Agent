from lentra.bot.ux.cards import CardRenderer
from lentra.bot.ux.detail_view import DetailView


class UXRenderer:

    def __init__(self, cache):
        self.cards = CardRenderer()
        self.detail = DetailView()
        self.cache = cache

    async def render(self, state, message):

        # LIST MODE
        if state.mode == "LIST":

            # fetch cached objects
            items = self.cache.get_results(state.search_id)

            page = state.page

            keyboard = self.cards.render_list(items, state.search_id, page)

            await message.answer(
                "📍 Результаты поиска",
                reply_markup=keyboard
            )

        # DETAIL MODE
        if state.mode == "DETAIL":

            items = self.cache.get_results(state.search_id)

            item = next((x for x in items if x["id"] == state.selected_id), None)

            if not item:
                await message.answer("Not found")
                return

            text, keyboard = self.detail.render(item)

            await message.answer(text, reply_markup=keyboard)
