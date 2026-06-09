
def check_triggers(watch, price):

    triggers = []

    if price <= watch.get("target_price", 999999):
        triggers.append("target_price_reached")

    if price < watch.get("baseline_price", 999999) * 0.8:
        triggers.append("price_drop_20%")

    if price < 100:
        triggers.append("deal_zone")

    return triggers
