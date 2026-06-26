# CRITICAL: DO NOT IMPORT policy.py here

class ScenarioPolicyEngine:
    def __init__(self, rules):
        self.rules = rules or []

    def evaluate(self, context):
        return {"ok": True}
