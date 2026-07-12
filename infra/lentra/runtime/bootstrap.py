from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


def init_runtime():
    return {
        "gateway": build_gateway_v3()
    }
