import json
import os
from typing import List, Dict, Any


class SignalMemoryStore:

    def __init__(self, path="/opt/lentra/infra/lentra/core/market_intelligence/state/signal_memory.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load(self) -> List[List[Dict[str, Any]]]:
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, history: List[List[Dict[str, Any]]]):
        with open(self.path, "w") as f:
            json.dump(history, f)
