import json
from core.observability.rca_engine_v2 import RCAEngine
from core.observability.incidence_cluster_v2 import IncidentCluster
from core.observability.explainer_v4 import Explainer
from core.observability.incident_narrative_v4 import NarrativeBuilder

"""
Lentra Observable Core v4
Unified Human-Readable RCA Report
"""


def build_report():
    rca = RCAEngine()
    cluster = IncidentCluster()
    explainer = Explainer()
    narrative = NarrativeBuilder()

    report = {
        "executive_summary": narrative.build(),
        "causal_analysis": rca.analyze(),
        "clusters": cluster.cluster_by_task(),
        "event_explanation": explainer.explain()
    }

    return report


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
