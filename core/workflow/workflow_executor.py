import time


class WorkflowExecutor:
    """
    Executes DAG step-by-step (deterministic engine)
    """

    def __init__(self):
        pass

    def execute(self, workflow: dict, handlers: dict) -> dict:
        results = {}

        for step in workflow.get("steps", []):
            step_type = step.get("type")

            handler = handlers.get(step_type)

            if handler:
                results[step["id"]] = handler(step, results)
            else:
                results[step["id"]] = {"skipped": True}

        return results
