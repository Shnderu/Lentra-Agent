import json


class WorkflowComposer:
    """
    Converts intent into multi-step task graph (future AI layer).
    """

    def build(self, intent: str, payload: dict):
        if intent == "rent.search":
            return [
                {"step": "validate", "type": "validation"},
                {"step": "search", "type": "rent.search", "payload": payload},
                {"step": "rank", "type": "ranking"},
            ]

        return [
            {"step": "unknown", "type": intent, "payload": payload}
        ]
