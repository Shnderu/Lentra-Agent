from typing import Any, Dict


class FusionEngineV1:
    def evaluate(self, engine_result: Dict[str, Any]) -> Dict[str, Any]:
        pricing = engine_result.get("pricing") or {}
        risk = engine_result.get("risk") or {}
        signals = engine_result.get("signals") or {}
        area = engine_result.get("area") or {}
        dedup = engine_result.get("dedup") or {}

        score = self._score(pricing, risk, signals, area, dedup)
        decision = self._decision(score)
        explanation = self._explain(pricing, risk, signals, area, dedup)

        return {
            "score": score,
            "decision": decision,
            "explanation": explanation
        }

    def _score(self, pricing, risk, signals, area, dedup) -> float:
        score = 0.5

        delta = pricing.get("delta", 0)
        if delta <= 0:
            score += 0.2
        else:
            score -= 0.1

        level = risk.get("level", "unknown")
        if level == "low":
            score += 0.2
        elif level == "high":
            score -= 0.3

        if signals.get("length", 0) > 10:
            score += 0.1

        if area.get("detected") and area.get("detected") != "unknown":
            score += 0.05

        if dedup.get("duplicates", 0) == 0:
            score += 0.1

        return max(0.0, min(1.0, score))

    def _decision(self, score: float) -> str:
        if score >= 0.75:
            return "MATCH"
        if score >= 0.4:
            return "REVIEW"
        return "REJECT"

    def _explain(self, pricing, risk, signals, area, dedup) -> str:
        parts = []

        parts.append(f"Price delta = {pricing.get('delta', 0)}")
        parts.append(f"Risk level = {risk.get('level', 'unknown')}")
        parts.append(f"Signal type = {signals.get('type', 'unknown')}")
        parts.append(f"Area = {area.get('detected', 'unknown')}")
        parts.append(f"Duplicates = {dedup.get('duplicates', 0)}")

        return " | ".join(parts)


def build_fusion_engine():
    return FusionEngineV1()
