from lentra.bot.core.intent_router import IntentRouter
from lentra.bot.core.intent_resolver import IntentResolver
from lentra.bot.core.feature_registry import FeatureRegistry

from lentra.bot.ports.rent_search import RentSearchPort


class Container:
    """
    Runtime dependency container.

    Delivery layer composition root.

    Bot depends only on ports.
    """

    def __init__(
        self,
        rent_search_service: RentSearchPort
    ):

        self.rent_search_service = rent_search_service

        self.feature_registry = FeatureRegistry()

        self._register_features()

        self.intent_resolver = IntentResolver(
            feature_registry=self.feature_registry
        )

        self.router = IntentRouter(
            registry=self.feature_registry
        )


    def _register_features(self):

        async def rent_search_entry(ctx):

            return await self.rent_search_service.search(
                {
                    "text": ctx.text,
                    "intent": ctx.intent,
                    "meta": ctx.meta
                }
            )


        self.feature_registry.register(
            "rent_search",
            rent_search_entry
        )


        self.feature_registry.register(
            "fallback",
            lambda ctx: {
                "status": "fallback"
            }
        )


def build_container(
    rent_search_service: RentSearchPort
):

    return Container(
        rent_search_service
    )
