

CITY_HEATMAP = {}


def update_heatmap(city: str, location: str, price: float):

    key = f"{city}:{location}"

    if key not in CITY_HEATMAP:
        CITY_HEATMAP[key] = []

    CITY_HEATMAP[key].append(price)

    avg = sum(CITY_HEATMAP[key]) / len(CITY_HEATMAP[key])

    return {
        "location": location,
        "avg_price": round(avg, 2),
        "data_points": len(CITY_HEATMAP[key])
    }


def get_city_map(city: str):

    result = {}

    for key, values in CITY_HEATMAP.items():
        if key.startswith(city + ":"):
            location = key.split(":")[1]
            result[location] = sum(values) / len(values)

    return result
