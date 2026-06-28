
from lentra.core.ai.concierge.negotiation.negotiation_engine import NegotiationEngine


class NegotiationModule:

    def __init__(self):
        self.engine = NegotiationEngine()

    def run(self, ctx):

        ctx.negotiation = self.engine.negotiate(
            listing_price=600,
            market_price=600,
            risk=0.5,
            area_score=5
        )

        return ctx
