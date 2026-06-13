def boost_score(score, is_premium=False):
    if is_premium:
        return score * 1.3
    return score
