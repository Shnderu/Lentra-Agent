from typing import List, Dict, Any

from lentra.core.data_layer.normalization.engine import NormalizationEngine
from lentra.core.data_layer.store.persistence import PersistenceLayer

from lentra.core.market_intelligence.adapters.pipeline_dedup_adapter import (
    PipelineDedupAdapter
)

from lentra.core.market_intelligence.adapters.pipeline_pricing_adapter import (
    PipelinePricingAdapter
)

from lentra.core.market_intelligence.adapters.pipeline_area_adapter import (
    PipelineAreaAdapter
)

from lentra.core.market_intelligence.engines.risk_engine import (
    RiskEngine
)

from lentra.core.market_intelligence.adapters.risk_engine_adapter import (
    RiskEngineAdapter
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
    MARKET INTELLIGENCE DEDUP
        |
        v
    MARKET INTELLIGENCE PRICING
        |
        v
    MARKET INTELLIGENCE AREA
        |
        v
    MARKET INTELLIGENCE RISK
    """


    def __init__(self):

        self.normalizer = NormalizationEngine()

        self.store = PersistenceLayer()

        self.deduper = PipelineDedupAdapter()

        self.pricing = PipelinePricingAdapter()

        self.area = PipelineAreaAdapter()

        self.risk = RiskEngineAdapter(
            RiskEngine()
        )


    def ingest_batch(
        self,
        raw_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        normalized_items = []


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


        dedup_result = self.deduper.deduplicate(
            normalized_items
        )

        clusters = dedup_result.get(
            "clusters",
            []
        )


        market_stats = self.pricing.build_market(
            clusters
        )


        enriched = []


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


                area_eval = self.area.evaluate(
                    item_with_price
                )


                item_with_area = {
                    **item_with_price,
                    **area_eval
                }


                risk_eval = self.risk.evaluate(
                    item_with_area,
                    market_stats,
                    duplicate_count
                )


                enriched.append(
                    {
                        **item_with_area,

                        "risk_score": risk_eval.get(
                            "risk_score",
                            0.0
                        ),

                        "risk_level": risk_eval.get(
                            "risk_level",
                            "unknown"
                        ),

                        "risk_signals": risk_eval.get(
                            "signals",
                            []
                        ),
                    }
                )


        return {
            "ingested": len(
                normalized_items
            ),

            "clusters": len(
                clusters
            ),

            "enriched": len(
                enriched
            ),

            "status": "ok"
        }


    def dump_all(self):

        return self.store.all()
