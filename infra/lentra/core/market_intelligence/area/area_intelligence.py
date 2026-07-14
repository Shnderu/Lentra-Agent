def compute_area_intelligence(
    listing,
    cluster_stats
):

    breakdown = {}

    score = 5.0


    raw_location = listing.get(
        "location"
    ) or ""


    if isinstance(raw_location, dict):

        location = " ".join(
            str(v)
            for v in raw_location.values()
        ).lower()

    else:

        location = str(
            raw_location
        ).lower()


    title = (
        listing.get(
            "title",
            ""
        )
        or ""
    ).lower()


    description = (
        listing.get(
            "description",
            ""
        )
        or ""
    ).lower()


    text = (
        location
        + " "
        + title
        + " "
        + description
    )


    features = listing.get(
        "features"
    ) or []


    profile = {

        "internet": 5.0,

        "safety": 5.0,

        "noise": 5.0,

        "infrastructure": 5.0,

        "expat_density": 5.0

    }


    # Internet

    if any(
        word in text
        for word in [
            "wifi",
            "wi-fi",
            "internet",
            "fiber"
        ]
    ):

        score += 1.5

        profile["internet"] = 9.0

        breakdown["internet"] = 1.5

    else:

        score -= 1.0

        profile["internet"] = 6.0

        breakdown["internet"] = -1.0



    # Beach / location

    if any(
        word in text
        for word in [
            "beach",
            "sea",
            "ocean",
            "my khe"
        ]
    ):

        score += 2.0

        profile["infrastructure"] = 9.0

        breakdown["beach_access"] = 2.0

    else:

        score -= 0.5

        breakdown["beach_access"] = -0.5



    # Expat density

    if (
        cluster_stats
        and cluster_stats.get(
            "listings_count",
            0
        ) > 3
    ):

        score += 0.7

        profile["expat_density"] = 8.5

        breakdown["expat_density"] = 0.7



    # Studio / city living

    if "studio" in title:

        score += 0.3

        profile["infrastructure"] = max(
            profile["infrastructure"],
            7.0
        )

        breakdown["urban_density"] = 0.3



    # Central area

    if "central" in text:

        profile["infrastructure"] = max(
            profile["infrastructure"],
            7.5
        )

        profile["safety"] = 7.0



    # Noise

    if any(
        word in text
        for word in [
            "old building",
            "busy road",
            "market"
        ]
    ):

        profile["noise"] = 5.5

    else:

        profile["noise"] = 7.0



    score = max(
        0,
        min(
            10,
            score
        )
    )


    if score >= 8:

        level = "premium"

    elif score >= 6:

        level = "good"

    elif score >= 4:

        level = "average"

    else:

        level = "poor"



    return {

        "area_score": round(
            score,
            2
        ),

        "area_level": level,

        "profile": profile,

        "breakdown": breakdown

    }
