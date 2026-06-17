class AlertManager:

    def __init__(self):
        self.alerts = []

    def emit(self, level: str, message: str, meta=None):
        alert = {
            "level": level,
            "message": message,
            "meta": meta or {}
        }

        self.alerts.append(alert)

        print(f"[ALERT-{level.upper()}] {message}")

    def get_alerts(self):
        return self.alerts
