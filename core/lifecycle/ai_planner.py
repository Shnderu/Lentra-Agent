import json


class AIPlanner:
    """
    Placeholder LLM-style planner (rule-based fallback for now).
    Will later be replaced by real LLM orchestration layer.
    """

    def plan(self, task: dict):
        task_type = task.get("type")
        payload = task.get("payload")

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        if task_type == "rent.search":
            return {
                "plan": "ai_rent_pipeline_v1",
                "graph": [
                    {"node": "normalize_input"},
                    {"node": "geo_expand"},
                    {"node": "source_faswaz"},
                    {"node": "rank_results"},
                    {"node": "format_response"}
                ]
            }

        return {
            "plan": "default",
            "graph": [{"node": "noop"}]
        }
