import json
from core.fusion.incident_rca_fusion_v7 import IncidentRCAFusion
from core.fusion.incident_explainer_v7 import IncidentExplainer

"""
Lentra Fusion Core v7
Final Unified Incident Intelligence Layer
"""


class IncidentIntelligence:

    def run(self):
        fusion = IncidentRCAFusion().run()
        explainer = IncidentExplainer().explain(fusion)

        return {
            "fusion": fusion,
            "explanation": explainer
        }


if __name__ == "__main__":
    engine = IncidentIntelligence()
    print(json.dumps(engine.run(), indent=2))
