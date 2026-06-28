

from lentra.core.pipeline.models import Listing

from lentra.core.pipeline.hooks.index_hook import index_listing

from lentra.core.market_intelligence.idempotency.idempotency_engine import build_idempotency_key
from lentra.core.market_intelligence.dedup.dedup_engine import assign_cluster
from lentra.core.market_intelligence.pricing.price_engine import compute_price_signal
from lentra.core.market_intelligence.risk.risk_engine import update_risk_score


class LentraPipeline:

    def run(self, raw_listing: dict):

        print(f"[PIPELINE] RECEIVED: {raw_listing['id']}")

        listing = Listing(raw_listing)

        listing.idempotency_key = build_idempotency_key(raw_listing)

        cluster_id = assign_cluster(listing.id, listing.idempotency_key)

        listing.cluster_id = cluster_id

        # pricing + risk
        signal = compute_price_signal(listing.price, cluster_id)
        listing.normalized_price = signal["normalized_price"]

        listing.risk = update_risk_score(listing)

        # FINAL STEP: INDEX INTO VECTOR STORE (NEW CRITICAL STEP)
        index_listing(listing.to_dict())

        print(f"[PIPELINE] DONE: {raw_listing['id']}")

        return listing.to_dict()
