from lentra.core.ai.semantic_search.vector_store.vector_store import search
from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed

from lentra.core.market_intelligence.dedup.dedup_engine import DedupEngine
from lentra.core.market_intelligence.object_model.property_object import PropertyObject
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.market_intelligence.area.area_engine import AreaEngine
from lentra.core.ai.decision.ai_decision_engine import AIDecisionEngine


class LentraPipeline:

    def run(self, raw_listing: dict):

        print(f"[PIPELINE] RECEIVED: {raw_listing.get('id')}")

        results = search(embed(raw_listing.get("title", "")))

        clusters = DedupEngine(threshold=0.85).cluster(results)

        mi_engine = MarketIntelligenceEngine()
        area_engine = AreaEngine()
        ai_engine = AIDecisionEngine()

        property_objects = [
            PropertyObject(cluster_id, listings)
            for cluster_id, listings in clusters.items()
        ]

        enriched = []

        for obj in property_objects:

            market = mi_engine.analyze(obj)

            location = obj.listings[0].get("location", "")

            area = area_engine.score(location)

            decision = ai_engine.decide(market, area)

            enriched.append({
                "cluster_id": obj.cluster_id,

                "market_price": market["market_price"],
                "price_deviation": market["price_deviation"],
                "risk": market["risk"],

                "area_score": area,

                "verdict": decision["verdict"],
                "negotiation": {
                    "strategy": decision["negotiation_strategy"],
                    "target_discount": decision["target_discount"]
                },

                "ai": {
                    "explanation": decision["explanation"],
                    "warnings": decision["warnings"]
                },

                "listings": obj.listings
            })

        print(f"[PIPELINE] DONE: {raw_listing.get('id')}")

        return {
            "id": raw_listing.get("id"),
            "objects": enriched
        }
