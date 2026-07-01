from typing import Dict, Any


class MarketIntelligenceContractEnforcer:

    """
    Гарантирует отсутствие "потерянного интеллекта"
    """

    def validate(self, engine_result: Dict[str, Any], mapped: Dict[str, Any]) -> Dict[str, Any]:

        engine_keys = set(engine_result.keys())

        mapped_values = set()
        for k, v in mapped.items():
            if v is not None:
                mapped_values.add(k.split(".")[0])

        missing = engine_keys - mapped_values

        return {
            "violations": sorted(list(missing)),
            "is_valid": len(missing) == 0
        }
