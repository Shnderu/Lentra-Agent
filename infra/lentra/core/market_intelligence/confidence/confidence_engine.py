class ConfidenceEngine:

    def run(self, obj: dict):

        confidence = obj.get("confidence")

        if confidence is None:
            confidence = 0.0

        obj["confidence"] = float(confidence)

        return obj
