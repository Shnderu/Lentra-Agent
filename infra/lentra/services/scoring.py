def calculate_score(apartment, budget_max: float | None = None, query: str = ""):
    """
    Простая, но расширяемая scoring модель
    """

    score = 0.0

    # pool bonus
    if apartment["pool"]:
        score += 0.4

    # sea view bonus
    if apartment["sea_view"]:
        score += 0.4

    # budget fit
    if budget_max is not None:
        if apartment["price_vnd_mln"] <= budget_max:
            score += 0.6
        else:
            score -= 0.5

    # area bonus
    if apartment["area_m2"] > 80:
        score += 0.2

    # default stability bias
    score += 0.1

    return round(score, 4)
