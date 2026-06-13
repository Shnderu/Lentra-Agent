"""
Lentra Event Validator v11
Hard gatekeeper for all system inputs
"""

from core.schema.event_schema_v11 import EventSchemaV11


class EventValidator:

    def __init__(self):
        self.schema = EventSchemaV11()

    def validate(self, event: dict):
        normalized = self.schema.normalize(event)

        errors = []

        if not normalized["type"]:
            errors.append("MISSING_TYPE")

        if normalized["severity"] not in ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            errors.append("INVALID_SEVERITY")

        if normalized["graph_size"] < 0:
            errors.append("NEGATIVE_GRAPH_SIZE")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "event": normalized
        }


if __name__ == "__main__":
    validator = EventValidator()

    print(validator.validate({
        "type": "rent.search",
        "severity": "CRITICAL",
        "graph_size": "10",
        "edges": "5",
        "payload": {"city": "Phu Quoc"}
    }))
