

from lentra.core.market_intelligence.core_v2.anomaly.anomaly_engine import detect_anomaly
from lentra.core.market_intelligence.core_v2.history.history_engine import record_price, get_trend
from lentra.core.market_intelligence.core_v2.heatmap.heatmap_engine import update_heatmap


def apply_market_intelligence_v2(listing, cluster_stats, city_stats):

    anomaly = detect_anomaly(listing, cluster_stats, city_stats)

    history = record_price(listing.city, listing.cluster_id, listing.price)

    trend = get_trend(listing.city, listing.cluster_id)

    heat = update_heatmap(listing.city, listing.location, listing.price)

    return {
        "anomaly": anomaly,
        "trend": trend,
        "heatmap": heat
    }
