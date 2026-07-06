"""
DTO ONLY LAYER

RULE:
- no imports from core
- no logic
- no enforcement
"""

class IntelligenceEnvelope:

    def wrap(self, data: dict) -> dict:
        return {
            "payload": data,
            "meta": {
                "version": "v1"
            }
        }
