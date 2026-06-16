from typing import Protocol
from lentra.bot.features.base.context import FeatureContext


class Feature(Protocol):
    """
    Production feature contract.
    """

    async def handle(self, ctx: FeatureContext) -> str:
        ...
