from lentra.bot.ux.cards import CardFactory
from lentra.bot.ux.renderer import UIRenderer
from lentra.bot.ux.actions import UXActions


class UXStateAdapter:

    def __init__(self):
        self.renderer = UIRenderer()

    def build_list_view(self, state):

        cards = CardFactory.from_state_results(state.results)

        text = self.renderer.render_list(cards, state.page)

        keyboard = UXActions.list_keyboard(cards)

        return text, keyboard

    def build_detail_view(self, state):

        cards = CardFactory.from_state_results(state.results)

        card = next((c for c in cards if c.id == state.selected_id), None)

        if not card:
            return "Not found", None

        text = self.renderer.render_detail(card)

        return text, None
