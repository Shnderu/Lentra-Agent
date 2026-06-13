# ============================================================
# ALERT ENGINE V17.1
# ============================================================


class AlertEngine:
    def generate(self, event):
        if event["type"] == "price_drop":
            return {
                "severity": "high",
                "message": f"Price dropped by {event['drop']}"
            }

        return {
            "severity": "low",
            "message": "Market update"
        }
