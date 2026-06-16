from lentra.bot.features.base.context import FeatureContext


async def fallback_feature(ctx: FeatureContext) -> str:
    return "❓ I did not understand the request"
