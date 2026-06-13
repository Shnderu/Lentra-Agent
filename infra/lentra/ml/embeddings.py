import hashlib
import numpy as np


# MOCK embedding (позже заменишь на OpenAI / local model)
def embed(text: str):
    h = hashlib.sha256(text.encode()).hexdigest()

    vec = np.array([int(h[i:i+2], 16) for i in range(0, 32, 2)], dtype=float)

    vec = vec / np.linalg.norm(vec)

    return vec.tolist()
