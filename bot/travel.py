def score_flight(price: int, duration: int, stops: int) -> float:
    score = 100
    score -= price * 0.02
    score -= duration * 0.1
    score -= stops * 15
    return round(max(score, 0), 2)
