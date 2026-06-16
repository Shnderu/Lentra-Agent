from typing import List
from lentra.bot.features.rent_search.models import RentalCard


class RentResponseBuilder:
    """
    Converts ranked rental cards into assistant-friendly message.
    """

    def build(self, cards: List[RentalCard]) -> str:
        if not cards:
            return "Я не нашёл подходящих вариантов."

        top = cards[:3]

        header = "🏠 Вот что удалось найти:\n"

        blocks = []
        for i, c in enumerate(top, 1):
            blocks.append(
                f"{i}. {c.title}\n"
                f"📍 {c.city}\n"
                f"💰 {c.price}\n"
                f"⭐ релевантность: {round(c.score, 2)}"
            )

        footer = "\n\nЕсли нужно — уточни бюджет или район, сузим поиск."

        return header + "\n\n".join(blocks) + footer
