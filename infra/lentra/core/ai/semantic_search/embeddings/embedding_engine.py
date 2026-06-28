

import hashlib


def embed(text: str):

    """
    MVP embedding (deterministic hash-based).
    Replace later with real model (OpenAI / sentence-transformers).
    """

    h = hashlib.sha256(text.encode()).hexdigest()

    # convert hash → pseudo vector (10-dim)
    vector = [int(h[i:i+2], 16) / 255 for i in range(0, 20, 2)]

    return vector
