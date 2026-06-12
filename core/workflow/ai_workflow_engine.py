import json


class AIWorkflowEngine:
    """
    Converts task -> execution DAG (multi-step workflow)
    """

    def build(self, task: dict) -> dict:
        task_type = task.get("type")
        payload = task.get("payload", {})

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        if task_type == "rent.search":

            city = payload.get("city", "unknown")

            return {
                "workflow_id": f"wf_{task.get('task_id')}",
                "steps": [
                    {
                        "id": "validate_input",
                        "type": "validate",
                        "input": payload
                    },
                    {
                        "id": "fetch_sources",
                        "type": "fetch",
                        "providers": ["faswaz"]
                    },
                    {
                        "id": "rank_results",
                        "type": "rank",
                        "strategy": "simple_rank"
                    },
                    {
                        "id": "build_response",
                        "type": "aggregate",
                        "city": city
                    }
                ]
            }

        return {
            "workflow_id": f"wf_{task.get('task_id')}",
            "steps": [
                {
                    "id": "noop",
                    "type": "noop"
                }
            ]
        }
