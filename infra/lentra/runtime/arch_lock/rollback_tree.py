import json


class RollbackTree:
    """
    Tracks architecture history for rollback capability.
    """

    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception:
            return {"nodes": []}

    def find_last_good(self):
        data = self.load()
        if not data["nodes"]:
            return None
        return data["nodes"][-1]
