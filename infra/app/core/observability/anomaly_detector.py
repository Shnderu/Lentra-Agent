from app.core.observability.alerts.alert_manager import AlertManager


class AnomalyDetector:

    def __init__(self, metrics_store):
        self.metrics = metrics_store
        self.alerts = AlertManager()

        # thresholds (v1 static)
        self.latency_threshold = 1.5  # sec
        self.error_threshold = 3

    def analyze(self):

        snapshot = self.metrics.snapshot()

        # -------------------------
        # LATENCY ANOMALY
        # -------------------------
        for stage, avg in snapshot["latency_avg"].items():
            if avg > self.latency_threshold:
                self.alerts.emit(
                    "warning",
                    f"High latency detected in {stage}",
                    {"avg_latency": avg}
                )

        # -------------------------
        # ERROR SPIKE
        # -------------------------
        for source, errors in snapshot["errors"].items():
            if errors >= self.error_threshold:
                self.alerts.emit(
                    "critical",
                    f"Error spike detected in {source}",
                    {"errors": errors}
                )

        return self.alerts.get_alerts()
