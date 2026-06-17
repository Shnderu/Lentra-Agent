class ErrorClassifier:

    def classify(self, error: Exception) -> dict:
        name = type(error).__name__

        if "AttributeError" in name:
            return {"type": "contract_violation", "severity": "high"}

        if "Timeout" in name:
            return {"type": "timeout", "severity": "medium"}

        if "Connection" in name:
            return {"type": "network", "severity": "medium"}

        return {"type": "unknown", "severity": "low"}
