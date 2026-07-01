from typing import Dict, Any

from lentra.core.market_intelligence.decision.signal_authority_resolver import SignalAuthorityResolver


class IntegratedSignalDecision:
    """
    Bridges raw Market Intelligence signals -> authoritative decision layer.

    Responsibilities:
    - collect signals from engine context
    - resolve conflicts via SignalAuthorityResolver
    - produce decision-ready structure for output contract
    """

    def __init__(self):
        self.resolver = SignalAuthorityResolver()

    def build(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            context: raw enriched intelligence payload from engine

        Returns:
            decision-ready normalized structure
        """

        signals = self._extract_signals(context)

        resolution = self.resolver.resolve(signals)

        return {
            "signals": resolution["resolved_signals"],
            "dominant_signal": resolution["dominant_signal"],
            "authority_score": resolution["authority_score"],
            "decision_flags": self._build_flags(
                resolution["resolved_signals"],
                resolution["dominant_signal"]
            )
        }

    def _extract_signals(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes raw engine context into signal map.
        """

        return {
            # pricing
            "price_market_deviation": context.get("deviation_pct"),
            "price_trend": context.get("price_trend"),

            # risk
            "fraud_probability": context.get("risk_score"),
            "listing_staleness": context.get("staleness"),

            # dedup
            "duplicate_cluster_size": context.get("duplicates"),

            # area
            "area_internet_quality": context.get("area", {}).get("internet"),
            "area_noise_level": context.get("area", {}).get("noise"),
            "area_expat_density": context.get("area", {}).get("expat_density"),
        }

    def _build_flags(self, signals: Dict[str, Any], dominant: str | None) -> Dict[str, Any]:
        """
        Converts signal state into decision flags used by UI + API.
        """

        flags = {
            "is_overpriced": False,
            "is_risky": False,
            "is_duplicate_heavy": False,
        }

        # pricing logic
        if signals.get("price_market_deviation", 0) and signals["price_market_deviation"] > 0.1:
            flags["is_overpriced"] = True

        # risk logic
        if signals.get("fraud_probability", 0) and signals["fraud_probability"] > 0.6:
            flags["is_risky"] = True

        # dedup logic
        if signals.get("duplicate_cluster_size", 0) and signals["duplicate_cluster_size"] > 2:
            flags["is_duplicate_heavy"] = True

        # dominant signal influence override
        if dominant == "fraud_probability":
            flags["is_risky"] = True

        return flags
