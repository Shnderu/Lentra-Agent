from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class ResponseBuilder:

    def build(self, context: SearchContext, items) -> str:

        header = (
            f"🏠 Lentra Rent Search\n"
            f"Запрос: {context.raw_query}\n"
            f"Страна: {context.country or 'any'}\n"
            f"Город: {context.city or 'any'}\n\n"
        )

        if not items:
            return header + "Объекты не найдены"

        lines = []

        for item in items[:20]:

            lines.append(
                f"• {item.title}\n"
                f"  💰 {item.price}\n"
                f"  📍 {item.city}\n"
            )

        return header + "\n".join(lines)
