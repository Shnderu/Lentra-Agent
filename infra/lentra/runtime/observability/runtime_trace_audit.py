"""
RUNTIME OBSERVABILITY LAYER

ONLY runtime may import this
"""

class RuntimeTraceAudit:

    def trace(self, event: str, payload: dict):
        return {
            "event": event,
            "payload": payload
        }
