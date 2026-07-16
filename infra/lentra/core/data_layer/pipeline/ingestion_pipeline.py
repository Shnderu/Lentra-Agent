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

from lentra.core.market_intelligence.adapters.pipeline_snapshot_adapter import (
    PipelineSnapshotAdapter
)

from lentra.core.market_intelligence.engines.risk_engine import (
    RiskEngine
)

from lentra.core.market_intelligence.adapters.risk_engine_adapter import (
    RiskEngineAdapter
)


class IngestionPipeline:


    def __init__(self):

        self.normalizer = NormalizationEngine()

        self.store = PersistenceLayer()

        self.deduper = PipelineDedupAdapter()

        self.pricing = PipelinePricingAdapter()

        self.area = PipelineAreaAdapter()

        self.snapshot = PipelineSnapshotAdapter()

        self.risk = RiskEngineAdapter(
            RiskEngine()
        )



    def ingest_batch(
        self,
        raw_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:


        normalized_items = []


        for item in raw_items:

            normalized_items.append(
                self.normalizer.normalize(
                    item
                )
            )



        dedup_result = self.deduper.deduplicate(
            normalized_items
        )


        clusters = dedup_result.get(
            "clusters",
            []
        )


        cluster_metadata = dedup_result.get(
            "cluster_metadata",
            []
        )


        market_stats = self.pricing.build_market(
            clusters
        )


        enriched = []


        for cluster_index, cluster in enumerate(clusters):

            duplicate_count = len(
                cluster
            )


            metadata = {}

            if cluster_index < len(cluster_metadata):

                metadata = cluster_metadata[
                    cluster_index
                ]


            object_memory = metadata.get(
                "object_memory",
                {}
            )


            entity = metadata.get(
                "entity",
                {}
            )


            cluster_data = metadata.get(
                "cluster",
                {}
            )


            entity_context = {

                "entity_id": entity.get(
                    "entity_id",
                    object_memory.get(
                        "object_id"
                    )
                ),

                "canonical_object_id": object_memory.get(
                    "object_id"
                ),

                "duplicate_count": duplicate_count,

                "duplicate_sources": cluster_data.get(
                    "sources",
                    []
                ),

            }


            snapshot_memory = {
                **object_memory,

                "price_history": list(
                    object_memory.get(
                        "price_history",
                        []
                    )
                )
            }


            cluster_items = []


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


                snapshot_memory = self.snapshot.update(
                    snapshot_memory,
                    item_with_area
                )


                cluster_items.append(
                    item_with_area
                )



            for item_with_area in cluster_items:


                item_with_snapshot = {

                    **item_with_area,

                    **entity_context,

                    **snapshot_memory

                }


                risk_eval = self.risk.evaluate(
                    item_with_snapshot,
                    market_stats,
                    duplicate_count
                )


                enriched.append(
                    {
                        **item_with_snapshot,

                        "risk_score": risk_eval.get(
                            "risk_score",
                            0.0
                        ),

                        "risk_level": risk_eval.get(
                            "risk_level",
                            "unknown"
                        ),

                        "risk_signals": risk_eval.get(
                            "risk_signals",
                            []
                        ),
                    }
                )



        for item in enriched:

            self.store.upsert(
                item
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

            "items": enriched,

            "market_segments": market_stats,

            "status": "ok"

        }



    def dump_all(self):

        return self.store.all()
