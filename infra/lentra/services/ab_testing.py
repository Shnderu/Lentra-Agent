import random


def choose_variant(user_id: int):
    return "A" if hash(user_id) % 2 == 0 else "B"


def apply_ranking(variant, ml_ranked, vector_ranked):
    if variant == "A":
        return ml_ranked
    return vector_ranked
