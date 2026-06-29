from dataclasses import dataclass


@dataclass
class NegotiationResult:
    can_negotiate: bool
    suggested_offer: float
    expected_discount_pct: float
    reasoning: str


class NegotiationEngine:
    """
    Determines negotiation potential for rental listings.
    """

    def evaluate(self, listing: dict) -> NegotiationResult:

        price = listing.get("price") or 0
        risk = listing.get("risk") or 0.5
        deviation = listing.get("deviation") or 0

        # HIGH RISK → stronger negotiation leverage
        base_discount = 0.05 + (risk * 0.25)

        # overpriced → more aggressive negotiation
        if deviation > 20:
            base_discount += 0.10

        # low demand segments (coastal premium volatility)
        segment = listing.get("location", {}).get("segment", "")
        if "coastal" in segment:
            base_discount += 0.05

        base_discount = min(base_discount, 0.35)

        suggested_offer = price * (1 - base_discount)

        return NegotiationResult(
            can_negotiate=base_discount > 0.08,
            suggested_offer=round(suggested_offer, 2),
            expected_discount_pct=round(base_discount * 100, 2),
            reasoning="Negotiation based on risk + market deviation + segment volatility"
        )
