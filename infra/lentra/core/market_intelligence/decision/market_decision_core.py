from lentra.core.market_intelligence.negotiation.negotiation_engine import NegotiationEngine
from lentra.core.market_intelligence.affordability.affordability_engine import AffordabilityEngine
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine


class MarketDecisionCore:

    def __init__(self):
        self.negotiation = NegotiationEngine()
        self.affordability = AffordabilityEngine()
        self.expat = ExpatScoreEngine()

    def decide(self, listing: dict):

        negotiation = self.negotiation.evaluate(listing)
        affordability = self.affordability.evaluate(listing)
        expat = self.expat.score(listing)

        listing["negotiation"] = negotiation.__dict__
        listing.update(affordability)
        listing.update(expat)

        # FINAL HUMAN DECISION LAYER
        if expat["expat_score"] > 0.75 and affordability["affordability_level"] == "safe":
            listing["final_verdict"] = "STRONG_BUY"

        elif expat["expat_score"] > 0.5:
            listing["final_verdict"] = "CONSIDER"

        else:
            listing["final_verdict"] = "AVOID"

        return listing
