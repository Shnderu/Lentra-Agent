from typing import Dict, Any


class SignalContract:

    def __init__(self, area_score: float = 0.0, internet_score: float = 0.0, noise_score: float = 0.0):
        self.area_score = area_score
        self.internet_score = internet_score
        self.noise_score = noise_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "area_score": float(self.area_score),
            "internet_score": float(self.internet_score),
            "noise_score": float(self.noise_score),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SignalContract":
        return SignalContract(
            area_score=data.get("area_score", 0.0),
            internet_score=data.get("internet_score", 0.0),
            noise_score=data.get("noise_score", 0.0),
        )
