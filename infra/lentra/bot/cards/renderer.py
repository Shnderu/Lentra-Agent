from lentra.bot.cards.builder import Card
from lentra.bot.ux.keyboard import UXKeyboard


class CardRenderer:

    def __init__(self):
        self.kb = UXKeyboard()

    def render_list_card(self, card: Card):
        text = (
            f"🏠 {card.title}\n\n"
            f"📍 {card.location}\n\n"
            f"💰 {card.price}\n"
            f"⭐ {card.score}\n\n"
            f"{' '.join(card.features)}"
        )

        return text, self.kb.list_card(card.id)

    def render_detail(self, card: Card):
        text = (
            f"🏠 {card.title}\n\n"
            f"📍 {card.location}\n"
            f"💰 {card.price}\n"
            f"⭐ {card.score}\n\n"
            f"Фичи:\n" +
            "\n".join(card.features)
        )

        return text, self.kb.detail_card(card.id)
