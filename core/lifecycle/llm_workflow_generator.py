import json


class LLMWorkflowGenerator:
    """
    Stub LLM-based DAG generator (future real LLM integration point).
    """

    def generate(self, task: dict):
        task_type = task.get("type")
        payload = task.get("payload")

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        if task_type == "rent.search":
            return {
                "dag": [
                    {"id": "ingest", "type": "normalize_input"},
                    {"id": "expand", "type": "geo_expand"},
                    {"id": "fetch", "type": "provider_faswaz"},
                    {"id": "rank", "type": "rank_results"},
                    {"id": "render", "type": "format_response"}
                ],
                "meta": {
                    "strategy": "rent_search_v2_llm_stub"
                }
            }

        return {
            "dag": [
                {"id": "noop", "type": "noop"}
            ],
            "meta": {"strategy": "default"}
        }
