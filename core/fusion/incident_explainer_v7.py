"""
Lentra Fusion Core v7
Unified Explanation Layer
"""


class IncidentExplainer:

    def explain(self, fusion_report):
        severity = fusion_report["severity"]
        size = fusion_report["graph_size"]
        edges = fusion_report["edges"]

        explanation = []

        explanation.append("INCIDENT FUSION REPORT v7")
        explanation.append("--------------------------")

        explanation.append(f"Severity: {severity}")
        explanation.append(f"Graph nodes: {size}")
        explanation.append(f"Graph edges: {edges}")

        if severity == "NONE":
            explanation.append("System is stable, no anomalies detected.")

        elif severity == "LOW":
            explanation.append("Minor incident activity detected with low correlation density.")

        elif severity == "MEDIUM":
            explanation.append("Multiple correlated events suggest emerging incident pattern.")

        else:
            explanation.append("High-density failure cluster detected. System degradation likely.")

        return {
            "report": "\n".join(explanation)
        }


if __name__ == "__main__":
    print("Explainer ready")
