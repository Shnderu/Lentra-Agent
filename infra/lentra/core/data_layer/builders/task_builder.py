class TaskBuilder:
    def build(self, payload):
        if isinstance(payload, str):
            payload = {"title": payload}

        if not isinstance(payload, dict):
            payload = {"title": str(payload)}

        return {
            "query": payload.get("title", ""),
            "raw": payload
        }


# BACKWARD COMPATIBILITY LAYER (CRITICAL)
def build_task(payload):
    return TaskBuilder().build(payload)
