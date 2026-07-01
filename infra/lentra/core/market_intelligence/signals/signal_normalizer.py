from typing import Dict, Any

from lentra.core.market_intelligence.signals.signal_contract import SignalContract


class SignalNormalizer:

    @staticmethod
    def normalize(expat_result: Dict[str, Any]) -> Dict[str, Any]:

        contract = SignalContract(
            area_score=expat_result.get("score", 0.0),
            internet_score=expat_result.get("internet", 0.0),
            noise_score=expat_result.get("noise", 0.0),
        )

        return contract.to_dict()
