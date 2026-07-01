from typing import Any, Dict

from .engine_output_contract import EngineOutput


class EngineAdapter:
    """
    Normalizes heterogeneous engine outputs into a single contract.
    """

    def normalize(self, raw: Any) -> EngineOutput:

        if raw is None:
            return EngineOutput(value=None, score=0.0)

        if isinstance(raw, dict):
            return EngineOutput(
                value=raw.get("value"),
                score=raw.get("score"),
                signals=raw.get("signals", {}),
                meta=raw.get("meta", {}),
            )

        # fallback scalar
        return EngineOutput(value=raw, score=None)
