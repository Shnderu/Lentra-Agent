from lentra.bot.cards.intelligence import IntelligenceCardBuilder


class IntelligenceCardRenderer:


    def __init__(self):
        self.builder = IntelligenceCardBuilder()


    def render(self, data: dict) -> str:

        if data.get("status") != "ok":
            return "❌ Ошибка анализа рынка"


        result = data.get(
            "result",
            {}
        )


        results = result.get(
            "results",
            []
        )


        if not results:
            return "Ничего не найдено"


        snapshot = result.get(
            "market_snapshot",
            {}
        )


        median_price = snapshot.get(
            "median_price",
            0
        )


        lines = [
            f"🏠 Найдено объектов: {len(results)}",
            f"📊 Рынок Da Nang: ${median_price}/месяц",
            ""
        ]


        for item in results[:5]:

            card = self.builder.build(item)


            lines.append(
                f"""
━━━━━━━━━━━━

🏠 {card.title}

{card.text}
"""
            )


        return "\n".join(lines)
