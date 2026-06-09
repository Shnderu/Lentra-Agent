
def score_deal(price: int) -> int:
    """
    Simple heuristic scoring:
    lower price = higher score
    """

    if price < 100:
        return 100

    if price < 200:
        return 70

    if price < 350:
        return 40

    return 10
