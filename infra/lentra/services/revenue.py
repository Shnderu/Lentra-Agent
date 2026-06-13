

def score_revenue_value(property_obj):
    score = 0

    if property_obj.price_vnd_mln:
        score += property_obj.price_vnd_mln * 0.1

    if property_obj.sea_view:
        score += 5

    if property_obj.pool:
        score += 3

    return score
