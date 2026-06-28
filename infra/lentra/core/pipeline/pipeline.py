

from lentra.core.market_intelligence.normalization.listing_normalizer import normalize_listing
from lentra.core.market_intelligence.dedup.dedup_engine import assign_cluster
from lentra.core.market_intelligence.risk.risk_engine import update_risk_score
from lentra.core.market_intelligence.pricing.price_engine import compute_price_signal
from lentra.core.market_intelligence.area.area_intelligence import compute_area_intelligence

from lentra.core.ai.concierge.ranker.meta_ranking_engine import compute_meta_score


class LentraPipeline:

    def run(self, raw_listing):

        print(f"[PIPELINE] RECEIVED: {raw_listing.get('id')}")

        # 1. NORMALIZE
        listing = normalize_listing(raw_listing)

        # 2. CLUSTER
        cluster_id = assign_cluster(listing["id"], listing.get("location"))

        # 3. RISK
        risk = update_risk_score(listing)

        # 4. PRICE SIGNAL (FIXED CONTRACT)
        price_signal = compute_price_signal(
            listing["price"],
            {"cluster_hint": cluster_id}
        )

        # 5. AREA INTELLIGENCE
        area = compute_area_intelligence(listing, {"listings_count": 1})

        # 6. META RANKING
        meta = compute_meta_score(
            price_signal,
            risk,
            {"scam_score": 0.5},
            area
        )

        result = {
            "id": listing["id"],
            "cluster_id": cluster_id,
            "price": listing["price"],
            "normalized_price": listing["price"],
            "signal": price_signal.get("signal"),
            "risk": risk.get("risk_score"),
            "area_score": area.get("area_score"),
            "meta_score": meta.get("final_score"),
            "status": "indexed"
        }

        print(f"[PIPELINE] DONE: {listing['id']}")
        return result
