import json


class IntentRouter:
    """
    Maps raw intent into executable workflow definition.
    """

    def route(self, task: dict):
        task_type = task.get("type")
        payload = task.get("payload")

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        if task_type == "rent.search":
            return {
                "workflow": "rent_search_v1",
                "steps": [
                    {"type": "validate_input"},
                    {"type": "rent.search", "payload": payload},
                    {"type": "rank_results"},
                    {"type": "finalize"}
                ]
            }

        return {
            "workflow": "default",
            "steps": [
                {"type": "noop"}
            ]
        }
