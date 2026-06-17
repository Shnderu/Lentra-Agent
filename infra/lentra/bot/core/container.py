from lentra.bot.core.intent_router import IntentRouter
from lentra.bot.core.intent_resolver import IntentResolver
from lentra.bot.core.feature_registry import FeatureRegistry


class Container:
    def __init__(self, connector):
        self.connector = connector

        self.feature_registry = FeatureRegistry()

        self.intent_resolver = IntentResolver(
            feature_registry=self.feature_registry
        )

        self.router = IntentRouter(
            intent_resolver=self.intent_resolver,
            connector=connector
        )


def build_container(connector):
    return Container(connector)
