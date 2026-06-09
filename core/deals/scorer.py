
def score_deal(price: int, baseline: int = 300):

    score = 0

    # чем ниже цена — тем выше score
    score += max(0, 100 - price // 5)

    # бонус за сильное отклонение от рынка
    if price < baseline * 0.5:
        score += 50

    if price < 100:
        score += 30

    return min(score, 100)
