from typing import Dict, Any, List
import time
import uuid


class TraceStore:
    """
    Lightweight in-memory trace registry (STEP 1.9)

    SAFE:
    - no external deps
    - no blocking IO
    - per-request isolation via request_id
    """

    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def new_request_id(self) -> str:
        return str(uuid.uuid4())

    def start(self, request_id: str):
        self._store[request_id] = []

    def add(self, request_id: str, engine: str, payload: Dict[str, Any], duration_ms: float):
        if request_id not in self._store:
            self._store[request_id] = []

        self._store[request_id].append({
            "engine": engine,
            "duration_ms": round(duration_ms, 4),
            "ts": time.time(),
            "payload_keys": list(payload.keys()) if isinstance(payload, dict) else []
        })

    def get(self, request_id: str) -> List[Dict[str, Any]]:
        return self._store.get(request_id, [])

    def clear(self, request_id: str):
        if request_id in self._store:
            del self._store[request_id]


trace_store = TraceStore()
