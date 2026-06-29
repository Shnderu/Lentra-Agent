# lazy import only to avoid circular dependency

def parse_query(*args, **kwargs):
    from .query_parser import parse_query as _impl
    return _impl(*args, **kwargs)


def QueryParser(*args, **kwargs):
    from .query_parser import QueryParser as _impl
    return _impl(*args, **kwargs)
