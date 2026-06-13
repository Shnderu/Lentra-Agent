import hashlib


def flag(user_id: int, feature: str) -> bool:
    h = hashlib.md5(f"{user_id}:{feature}".encode()).hexdigest()
    return int(h, 16) % 2 == 0
