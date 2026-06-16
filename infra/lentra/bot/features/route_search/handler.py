from lentra.bot.features.base.context import FeatureContext


async def route_search_feature(ctx: FeatureContext) -> str:
    """
    Production domain feature: route search (MVP stub).
    """

    query = (ctx.text or "").strip().lower()

    if not query:
        return "Введите маршрут или запрос"

    # MVP логика (заглушка под будущий поиск маршрутов)
    return (
        "✈️ Route search engine\n\n"
        f"Query: {query}\n\n"
        "Status: MVP stub (no backend integration yet)"
    )
