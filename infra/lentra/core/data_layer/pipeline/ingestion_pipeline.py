from typing import List, Dict, Any

from lentra.core.data_layer.normalization.engine import NormalizationEngine
from lentra.core.data_layer.store.persistence import PersistenceLayer
from lentra.core.data_layer.dedup.deduplicator import Deduplicator

from lentra.core.market.pricing_engine import PricingEngine

from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.adapters.risk_engine_adapter import (
    RiskEngineAdapter,
)


class IngestionPipeline:
    """
    VIETNAM PIPELINE:

    INGESTION
        |
        v
    NORMALIZATION
        |
        v
    DEDUP
        |
        v
    PRICING
        |
        v
    MARKET INTELLIGENCE RISK
    """

    def __init__(self):
        self.normalizer = NormalizationEngine()
        self.store = PersistenceLayer()
        self.deduper = Deduplicator()

        self.pricing = PricingEngine()

        self.risk = RiskEngineAdapter(
            RiskEngine()
        )


    def ingest_batch(
        self,
        raw_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        normalized_items = []


        # 1. normalize + persist
        for item in raw_items:

            normalized = self.normalizer.normalize(
                item
            )

            self.store.upsert(
                normalized
            )

            normalized_items.append(
                normalized
            )


        # 2. dedup
        dedup_result = self.deduper.deduplicate(
            normalized_items
        )

        clusters = dedup_result["clusters"]


        # 3. pricing
        market_stats = self.pricing.build_market(
            clusters
        )


        enriched = []


        # 4. risk scoring
        for cluster in clusters:

            duplicate_count = len(
                cluster
            )


            for item in cluster:

                price_eval = self.pricing.evaluate(
                    item,
                    market_stats
                )


                item_with_price = {
                    **item,
                    **price_eval
                }


                risk_eval = self.risk.evaluate(
                    item_with_price,
                    market_stats,
                    duplicate_count
                )


                enriched.append(
                    {
                        **item_with_price,

                        "risk_score": risk_eval[
                            "risk_score"
                        ],

                        "risk_level": risk_eval[
                            "risk_level"
                        ],

                        "risk_signals": risk_eval[
                            "signals"
                        ],
                    }
                )


        return {
            "ingested": len(
                normalized_items
            ),

            "clusters": len(
                clusters
            ),

            "status": "ok"
        }


    def dump_all(self):

        return self.store.all()
