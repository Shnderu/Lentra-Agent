def deduplicate(items: list):
    seen = set()
    result = []

    for item in items:
        key = (item.get("title"), item.get("price"), item.get("district"))

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result
