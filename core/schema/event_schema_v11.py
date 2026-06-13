"""
Lentra Event Schema v11
Single Source of Truth for all system events
"""

from typing import Dict, Any


class EventSchemaV11:

    def normalize(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes ALL incoming events into strict canonical format
        """

        return {
            "event_id": str(event.get("event_id", "")),
            "type": str(event.get("type", "unknown")),
            "severity": self._normalize_severity(event.get("severity", "NONE")),
            "graph_size": self._int(event.get("graph_size", 0)),
            "edges": self._int(event.get("edges", 0)),
            "timestamp": self._float(event.get("timestamp", 0)),
            "payload": self._normalize_payload(event.get("payload", {}))
        }

    def _normalize_severity(self, severity):
        severity = str(severity).upper()

        allowed = ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

        if severity not in allowed:
            return "NONE"

        return severity

    def _int(self, v):
        try:
            return int(v)
        except:
            return 0

    def _float(self, v):
        try:
            return float(v)
        except:
            return 0.0

    def _normalize_payload(self, payload):
        if isinstance(payload, dict):
            return payload
        return {"raw": str(payload)}


if __name__ == "__main__":
    schema = EventSchemaV11()

    print(schema.normalize({
        "event_id": 123,
        "type": "rent.search",
        "severity": "high",
        "graph_size": "5",
        "edges": "3",
        "timestamp": "1781290000.12",
        "payload": "{\"city\":\"Phu Quoc\"}"
    }))
