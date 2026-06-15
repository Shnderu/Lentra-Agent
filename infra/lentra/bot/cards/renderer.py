from lentra.bot.cards.builder import Card


class CardRenderer:

    def render_list_card(self, card: Card) -> str:
        features = "\n".join(card.features)

        return (
            f"🏠 {card.title}\n\n"
            f"📍 {card.location}\n\n"
            f"💰 {card.price}\n"
            f"⭐ {card.score}\n\n"
            f"{features}\n\n"
            f"[Подробнее] [❤️ Сохранить] [Похожие]"
        )

    def render_detail(self, card: Card) -> str:
        return (
            f"🏠 {card.title}\n\n"
            f"📍 {card.location}\n"
            f"💰 {card.price}\n"
            f"⭐ {card.score}\n\n"
            f"Фичи:\n" +
            "\n".join(card.features) +
            "\n\n[⬅ Назад]"
        )
