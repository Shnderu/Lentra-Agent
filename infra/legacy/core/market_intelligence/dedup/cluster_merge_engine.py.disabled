

def is_same_object(a, b):

    # price band
    if abs(a["price"] - b["price"]) > 150:
        return False

    # title similarity (very simple v1 heuristic)
    a_title = set(a["title"].lower().split())
    b_title = set(b["title"].lower().split())

    overlap = len(a_title.intersection(b_title))

    if overlap < 2:
        return False

    # location proximity (string-based v1)
    if a.get("location") and b.get("location"):
        if a["location"] != b["location"]:
            return False

    return True


def merge_clusters(base_cluster, new_listing):

    base_cluster["listings_count"] += 1

    # update price range
    price = new_listing["price"]

    base_cluster["min_price"] = min(base_cluster["min_price"], price)
    base_cluster["max_price"] = max(base_cluster["max_price"], price)

    # recompute avg
    base_cluster["avg_price"] = (
        (base_cluster["avg_price"] * (base_cluster["listings_count"] - 1) + price)
        / base_cluster["listings_count"]
    )

    return base_cluster
