import json
from core.observability.rca_engine_v2 import RCAEngine
from core.observability.incidence_cluster_v2 import IncidentCluster
from core.observability.failure_timeline_v2 import timeline

"""
Lentra Observable Core v2
Unified RCA Report
"""


def build_report():
    engine = RCAEngine()
    clusters = IncidentCluster()

    report = {
        "rca": engine.analyze(),
        "clusters": clusters.cluster_by_task(),
        "timeline": timeline()
    }

    return report


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
