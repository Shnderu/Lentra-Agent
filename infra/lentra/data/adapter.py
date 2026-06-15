from lentra.data.providers.properties_provider import fetch_properties
from lentra.data.providers.feature_loader import load_features_from_properties


def get_properties(query: dict, conn=None):
    """
    Вход: уже нормализованный query (parse_query result)
    """

    props = fetch_properties(conn, query)

    # обновляем feature store
    load_features_from_properties(props)

    return props
