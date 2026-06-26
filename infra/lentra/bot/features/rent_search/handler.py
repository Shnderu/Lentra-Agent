from lentra.bot.features.base.context import FeatureContext


async def rent_search_feature(ctx: FeatureContext) -> str:
    text = getattr(ctx, "text", "")

    return f"[RENT SEARCH OK] query={text}"
