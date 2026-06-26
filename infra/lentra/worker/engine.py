from lentra.core.di.container import build_container


def build_gateway():
    """
    Worker gateway is now fully DI-driven.
    No partial arguments allowed.
    """
    container = build_container()

    return container
