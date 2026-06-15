import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Distance in km
    """
    R = 6371

    phi1 = math.radians(lat1 or 0)
    phi2 = math.radians(lat2 or 0)

    dphi = math.radians((lat2 or 0) - (lat1 or 0))
    dlambda = math.radians((lon2 or 0) - (lon1 or 0))

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def geo_score(prop, user_location=None):
    """
    Returns boost based on distance (km)
    """
    if not user_location:
        return 0.0

    lat1, lon1 = user_location.get("lat"), user_location.get("lng")
    lat2, lon2 = prop.get("lat"), prop.get("lng")

    if not lat1 or not lon1 or not lat2 or not lon2:
        return 0.0

    dist = haversine(lat1, lon1, lat2, lon2)

    if dist < 2:
        return 0.5
    if dist < 5:
        return 0.3
    if dist < 15:
        return 0.1

    return 0.0
