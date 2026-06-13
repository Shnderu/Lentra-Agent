# ============================================================
# PRICE TRACKER V17.1
# ============================================================


class PriceTracker:
    def detect_change(self, old, new):
        if not old:
            return None

        old_price = old.get("price", 0)
        new_price = new.get("price", 0)

        if new_price < old_price:
            return {
                "type": "price_drop",
                "drop": old_price - new_price
            }

        if new_price > old_price:
            return {
                "type": "price_increase",
                "increase": new_price - old_price
            }

        return None
