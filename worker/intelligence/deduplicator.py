from hashlib import md5

def generate_fingerprint(item: dict) -> str:
    base = f"{item.get('title')}|{item.get('location')}|{item.get('price')}"
    return md5(base.encode()).hexdigest()


def deduplicate(items: list) -> list:
    seen = set()
    result = []

    for item in items:
        fp = generate_fingerprint(item)

        if fp in seen:
            continue

        seen.add(fp)
        result.append(item)

    return result
