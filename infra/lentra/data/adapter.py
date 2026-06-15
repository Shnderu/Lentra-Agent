from lentra.data.providers.properties_provider import fetch_properties


def get_properties(query=None, conn=None):
    """
    DATA LAYER ENTRYPOINT (v6.6)
    """

    if conn is None:
        raise ValueError("DB connection required in v6.6")

    return fetch_properties(conn, query or {})
