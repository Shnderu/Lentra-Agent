

class ContractIntelligenceEngine:

    def analyze(self, contract_text: str):

        text = contract_text.lower()

        risk_score = 0.0
        flags = []
        leverage = []

        # deposit risk
        if "non-refundable" in text:
            risk_score += 0.4
            flags.append("non_refundable_deposit")

        # eviction flexibility
        if "terminate anytime" in text or "without notice" in text:
            risk_score += 0.3
            flags.append("unstable_contract_terms")
            leverage.append("push_for_notice_period")

        # price increase clause
        if "price may change" in text or "owner discretion" in text:
            risk_score += 0.2
            flags.append("uncontrolled_price_change")

        # utility ambiguity
        if "utilities not included" in text:
            flags.append("hidden_costs_risk")

        # cap
        risk_score = min(risk_score, 1.0)

        interpretation = self._interpret(risk_score)

        return {
            "risk_score": round(risk_score, 3),
            "flags": flags,
            "leverage_points": leverage,
            "interpretation": interpretation
        }


    def _interpret(self, score):

        if score > 0.7:
            return "high_risk_contract"
        elif score > 0.4:
            return "medium_risk_contract"
        else:
            return "standard_contract"
