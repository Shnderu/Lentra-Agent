from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class ResponseBuilder:
    """
    Формирует финальный текст ответа пользователю
    """

    def build(self, context: SearchContext, items) -> str:

        header = (
            f"🏠 Rent search result\n"
            f"Query: {context.raw_query}\n"
            f"City: {context.city or 'any'}\n\n"
        )

        if not items:
            return header + "No results found"

        body = "\n".join(
            f"• {i.title} | {i.price} | {i.city}"
            for i in items
        )

        return header + body
