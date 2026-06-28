

import hashlib
from collections import defaultdict


class MarketGraphEngine:

    def build_graph(self, listings):

        graph = defaultdict(list)

        for l in listings:

            # stable identity key (primitive v1)
            key_raw = (
                l.get("title", "") +
                str(l.get("price", "")) +
                l.get("location", "")
            )

            property_id = hashlib.md5(key_raw.encode()).hexdigest()

            graph[property_id].append(l)

        return graph


    def normalize_properties(self, graph):

        properties = []

        for property_id, listings in graph.items():

            prices = [l.get("price", 0) for l in listings if l.get("price")]

            if prices:
                market_price = sum(prices) / len(prices)
            else:
                market_price = 0

            properties.append({
                "property_id": property_id,
                "market_price": market_price,
                "price_range": {
                    "min": min(prices) if prices else 0,
                    "max": max(prices) if prices else 0
                },
                "listings": listings,
                "sources": list(set([l.get("source", "unknown") for l in listings]))
            })

        return properties
