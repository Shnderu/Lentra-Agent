from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


def get_gateway():
    return build_gateway_v3()


class Dispatcher:
    def __init__(self):
        self.gateway = get_gateway()
