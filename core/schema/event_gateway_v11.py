"""
Lentra Event Gateway v11
All system inputs MUST pass here
"""

from core.schema.event_validator_v11 import EventValidator


class EventGateway:

    def __init__(self):
        self.validator = EventValidator()

    def ingest(self, event: dict):
        result = self.validator.validate(event)

        if not result["valid"]:
            return {
                "status": "REJECTED",
                "errors": result["errors"]
            }

        return {
            "status": "ACCEPTED",
            "event": result["event"]
        }


if __name__ == "__main__":
    gateway = EventGateway()

    print(gateway.ingest({
        "type": "rent.search",
        "severity": "HIGH",
        "graph_size": "12",
        "edges": "6",
        "payload": {"city": "Phu Quoc"}
    }))
