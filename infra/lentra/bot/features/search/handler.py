from lentra.bot.features.base.context import FeatureContext


async def search_feature(ctx: FeatureContext) -> str:
    """
    Minimal production-grade search feature.
    """

    query = ctx.text.strip()

    if not query:
        return "Empty search query"

    # stub logic (future: route-search / embeddings / DB)
    return f"🔎 Search result for: {query}"
