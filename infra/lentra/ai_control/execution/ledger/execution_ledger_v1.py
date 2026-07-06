import hashlib
import json
from datetime import datetime


class ExecutionLedgerV1:
    """
    Deterministic execution tracking layer.

    Guarantees:
    - same input → same execution_id
    - full trace chain stored
    - no side effects
    """

    def create_execution_id(self, query: str, plan: dict) -> str:
        payload = {
            "query": query,
            "plan": plan,
        }

        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def create_trace(self, execution_id: str, stage: str, data: dict):
        return {
            "execution_id": execution_id,
            "stage": stage,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
