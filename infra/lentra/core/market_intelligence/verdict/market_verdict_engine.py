from lentra.core.market_intelligence.area.market_segmentation_engine import MarketSegmentationEngine
from lentra.core.market_intelligence.area.micro_market_engine import MicroMarketEngine


class MarketVerdictEngine:

    def __init__(self):
        self.segmenter = MarketSegmentationEngine()
        self.micro = MicroMarketEngine()

    def evaluate(self, listing: dict):

        segment = self.segmenter.update(listing)
        cluster = self.micro.update(listing)

        deviation = self.micro.deviation(listing)

        area = listing.get("area_quality") or 5
        area_factor = (float(area) - 5) / 10

        adjusted = deviation - area_factor * 0.15

        # -------------------------
        # DECISION LOGIC
        # -------------------------
        if adjusted > 0.25:
            verdict = "overpriced"
        elif adjusted < -0.25:
            verdict = "cheap"
        else:
            verdict = "fair"

        confidence = 1.0 - min(1.0, abs(adjusted))

        return {
            "segment": segment,
            "micro_market": cluster,
            "market_verdict": verdict,
            "market_deviation": deviation,
            "market_adjusted": adjusted,
            "market_confidence": confidence
        }
