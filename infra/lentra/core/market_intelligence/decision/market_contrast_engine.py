import math


class MarketContrastEngine:
    """
    Restores distribution contrast in market decisions.

    Fixes:
    - over-smoothing
    - excessive FAIR dominance
    - loss of signal separation
    """

    def amplify(self, market_pressure: float, volatility: float) -> float:

        # -------------------------
        # TAIL AMPLIFICATION
        # -------------------------
        # non-linear stretch of extremes
        amplified = math.tanh(market_pressure * 2.2) * 1.4

        # -------------------------
        # VOLATILITY BOOST
        # -------------------------
        # unstable markets exaggerate signals
        amplified *= (1.0 + volatility * 0.35)

        return amplified

    def entropy_penalty(self, value: float) -> float:
        """
        Penalize neutral clustering around zero.
        """

        # strongest compression zone around 0
        return math.exp(-abs(value) * 2.5)

    def apply(self, market_pressure: float, volatility: float) -> float:

        amplified = self.amplify(market_pressure, volatility)

        # entropy correction
        penalty = self.entropy_penalty(amplified)

        return amplified * (1.0 + (1.0 - penalty))
