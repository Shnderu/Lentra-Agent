class ProviderRouter:
    """
    Routes tasks to best provider (future multi-source system).
    """

    def choose(self, task: dict):
        task_type = task.get("type")

        if task_type == "rent.search":
            return ["faswaz"]  # future: multiple providers

        return ["default"]
