from lentra.connectors.registry.registry import ConnectorRegistry
from lentra.normalizers.property_normalizer import PropertyNormalizer


class SearchService:

    async def search(self, query: str):

        properties = []

        for connector in ConnectorRegistry.get_connectors():

            raw_results = await connector.search(query)

            properties.extend(
                [
                    PropertyNormalizer.normalize(
                        item,
                        connector.__class__.__name__
                    )
                    for item in raw_results
                ]
            )

        return properties
