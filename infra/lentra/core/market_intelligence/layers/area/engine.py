from typing import Dict, Any

class AreaLayer:
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(payload)

        payload["area"] = {
            "internet_score": 8.0,
            "noise_level": 5.0,
            "expat_score": 7.5
        }

        return payload
