def diversify(results):
    """
    Prevents same-city clustering in top results
    """

    seen_cities = set()
    output = []

    for r in results:
        city = r.get("city")

        if city in seen_cities and len(output) < 5:
            continue

        if city:
            seen_cities.add(city)

        output.append(r)

    return output
