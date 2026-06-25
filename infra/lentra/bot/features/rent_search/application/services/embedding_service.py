from typing import List
import math


class EmbeddingService:
    """
    v1 stub embeddings service.
    Пока без OpenAI — локальный fallback hash-embedding.
    Позже заменим на real embeddings API.
    """

    def embed(self, text: str) -> List[float]:

        if not text:
            return [0.0] * 32

        text = text.lower()

        vec = [0.0] * 32

        for i, ch in enumerate(text):

            idx = (ord(ch) * (i + 1)) % 32
            vec[idx] += 1.0

        # normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0

        return [x / norm for x in vec]


    def similarity(self, a: List[float], b: List[float]) -> float:

        return sum(x * y for x, y in zip(a, b))
