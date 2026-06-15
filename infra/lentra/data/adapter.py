from lentra.data.providers.vietnam_provider import fetch_vietnam_listings


def get_properties(query=None):
    """
    DATA LAYER ENTRYPOINT (STABLE MODE)

    NOTE:
    SQL filtering disabled intentionally.
    Provider returns normalized dataset.
    """

    raw = fetch_vietnam_listings(query)

    return raw
