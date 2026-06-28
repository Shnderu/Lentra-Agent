from lentra.core.contracts.v1.guard import enforce_listing_contract

from lentra.core.market_intelligence.idempotency.idempotency_engine import (
    build_idempotency_key,
    is_processed,
    mark_processed
)

from lentra.core.market_intelligence.dedup.dedup_engine import assign_cluster
from lentra.core.market_intelligence.features.feature_mapper import to_feature_vector

from lentra.core.market_intelligence.pricing.price_engine import update_cluster_stats
from lentra.core.market_intelligence.risk.risk_engine import update_risk_score


class LentraPipeline:

    def run(self, raw_listing):
        dto = enforce_listing_contract(raw_listing)

        print("[PIPELINE] RECEIVED:", dto.id)

        key = build_idempotency_key(raw_listing)

        if is_processed(key):
            print("[PIPELINE] SKIP IDEMPOTENT:", dto.id)
            return {"status": "skipped"}

        # 1. FEATURE LAYER (НОВЫЙ СТАНДАРТ)
        feature = to_feature_vector(dto)

        # 2. DEDUP
        cluster_id = assign_cluster(raw_listing, key)

        # 3. MARK IDEMPOTENT
        mark_processed(dto.id, key)

        # 4. MARKET INTELLIGENCE
        update_cluster_stats(cluster_id)
        update_risk_score(cluster_id)

        print("[PIPELINE] DONE:", dto.id)

        return {
            "id": dto.id,
            "cluster_id": cluster_id,
            "price": feature.price,
            "normalized_price": feature.normalized_price,
            "status": "indexed"
        }
