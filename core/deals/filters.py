
def is_valid_deal(route):

    price = route.get("price")

    if not price:
        return False

    if price > 800:
        return False

    return True
