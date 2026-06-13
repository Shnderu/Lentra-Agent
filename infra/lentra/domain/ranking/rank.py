def rank_properties(properties, state=None):
    """
    Simple ranking v1
    """

    return sorted(
        properties,
        key=lambda x: (
            x.get("score", 0),
            -x.get("price", 0)
        ),
        reverse=True
    )
