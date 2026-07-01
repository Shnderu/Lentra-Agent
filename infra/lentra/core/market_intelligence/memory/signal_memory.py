from typing import Dict, Any, List
from collections import deque

from lentra.core.market_intelligence.memory.signal_memory_store import SignalMemoryStore


class SignalMemory:

    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.store = SignalMemoryStore()
        self.history = deque(self.store.load(), maxlen=window_size)

    def add(self, signals: List[Dict[str, Any]]):
        self.history.append(signals)
        self.store.save(list(self.history))

    def get_history(self) -> List[List[Dict[str, Any]]]:
        return list(self.history)

    def detect_drift(self, current_signals: List[Dict[str, Any]]) -> Dict[str, Any]:

        if not self.history:
            return {
                "drift_score": 0.0,
                "confidence_adjustment": 0.0,
                "patterns": []
            }

        last = self.history[-1]

        drift_score = 0.0
        patterns = []

        def get(sig_list, name):
            for s in sig_list:
                if s.get("name") == name:
                    return s.get("value")
            return None

        curr_price = get(current_signals, "price")
        prev_price = get(last, "price")

        if curr_price and prev_price:
            diff = abs(curr_price - prev_price) / max(prev_price, 1)
            drift_score += diff

            if diff > 0.1:
                patterns.append("price_jump")

        curr_risk = get(current_signals, "risk_level")
        prev_risk = get(last, "risk_level")

        if curr_risk != prev_risk:
            drift_score += 0.2
            patterns.append("risk_change")

        curr_area = get(current_signals, "area_score")
        prev_area = get(last, "area_score")

        if curr_area and prev_area:
            if abs(curr_area - prev_area) > 2:
                drift_score += 0.15
                patterns.append("area_volatility")

        confidence_adjustment = -min(drift_score, 0.5)

        return {
            "drift_score": round(drift_score, 4),
            "confidence_adjustment": confidence_adjustment,
            "patterns": patterns
        }
