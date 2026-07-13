from lentra.bot.core.intent_router import IntentRouter
from lentra.bot.core.intent_resolver import IntentResolver
from lentra.bot.core.feature_registry import FeatureRegistry

from lentra.application.rent_search.service import (
    RentSearchApplicationService
)


class Container:
    """
    Runtime dependency container.

    Single composition root for bot delivery layer.
    """

    def __init__(self, connector):

        self.connector = connector

        self.feature_registry = FeatureRegistry()

        self.rent_search_service = RentSearchApplicationService(
            connector
        )

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


def build_container(connector):

    return Container(
        connector
    )
