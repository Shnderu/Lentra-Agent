
def deduplicate(listings):
    seen = {}
    result = []

    for l in listings:
        key = l["title"].lower()

        if key in seen:
            seen[key].append(l["id"])
        else:
            seen[key] = [l["id"]]
            result.append(l)

    for r in result:
        r["duplicates"] = seen[r["title"].lower()]

    return result
