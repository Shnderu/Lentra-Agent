from lentra.bot.services.registry import SearchResult
from lentra.bot.ux.cards import CardBuilder


class TelegramFormatter:
    def __init__(self):
        self.card = CardBuilder()

    def format_page(self, results: list[SearchResult], offset: int = 0) -> str:
        if not results:
            return "❌ Ничего не найдено"

        header = "🏡 <b>Lentra Rentals</b>\n🔎 результаты поиска\n\n"

        body = "\n\n".join(
            self.card.build(r, offset + i + 1)
            for i, r in enumerate(results)
        )

        return header + body
