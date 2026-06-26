from lentra.core.models.listing import Listing


def deduplicate(listings: list) -> list:
    seen = {}

    for l in listings:
        key = (l.title.lower(), l.location.lower(), l.price)

        if key in seen:
            seen[key].duplicates.append(l.id)
        else:
            seen[key] = l

    return list(seen.values())
