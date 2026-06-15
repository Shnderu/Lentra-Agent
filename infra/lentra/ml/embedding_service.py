import hashlib
import json
from typing import Dict, Any, List


class EmbeddingService:
    """
    v3 base implementation (no external model yet).
    Deterministic pseudo-embedding for safe rollout.
    """

    DIM = 64

    def _hash_token(self, token: str) -> int:
        h = hashlib.sha256(token.encode()).hexdigest()
        return int(h[:8], 16)

    def encode_text(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self.DIM

        tokens = text.lower().split()

        vec = [0.0] * self.DIM

        for t in tokens:
            idx = self._hash_token(t) % self.DIM
            vec[idx] += 1.0

        # normalize
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        vec = [v / norm for v in vec]

        return vec

    def encode_property(self, prop: Dict[str, Any]) -> List[float]:
        text = " ".join([
            prop.get("title", ""),
            json.dumps(prop.get("features", {})),
            str(prop.get("area_m2", "")),
        ])
        return self.encode_text(text)
