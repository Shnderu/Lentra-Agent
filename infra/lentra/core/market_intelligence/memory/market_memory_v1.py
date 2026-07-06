from dataclasses import dataclass, field
from typing import Dict, List, Any
import time


@dataclass
class MarketSignal:
    entity_id: str
    signal_type: str
    value: Any
    timestamp: float


class MarketMemoryV1:
    """
    Deterministic market memory layer.

    Rules:
    - no learning models
    - only append + deterministic aggregation
    - time-aware signal storage
    """

    def __init__(self):
        self.store: Dict[str, List[MarketSignal]] = {}

    def add_signal(self, entity_id: str, signal_type: str, value: Any):
        signal = MarketSignal(
            entity_id=entity_id,
            signal_type=signal_type,
            value=value,
            timestamp=time.time()
        )

        if entity_id not in self.store:
            self.store[entity_id] = []

        self.store[entity_id].append(signal)

    def get_latest(self, entity_id: str, signal_type: str):
        signals = self.store.get(entity_id, [])

        filtered = [s for s in signals if s.signal_type == signal_type]

        if not filtered:
            return None

        return sorted(filtered, key=lambda x: x.timestamp)[-1].value

    def aggregate(self, entity_id: str, signal_type: str):
        signals = self.store.get(entity_id, [])

        values = [s.value for s in signals if s.signal_type == signal_type]

        if not values:
            return None

        # deterministic aggregation (NO ML)
        if all(isinstance(v, (int, float)) for v in values):
            return sum(values) / len(values)

        return values[-1]
