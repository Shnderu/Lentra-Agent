"""
Runtime bootstrap layer (ARCH LOCK SAFE)
DO NOT import core.bootstrap
"""

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


def main():
    # runtime entry must NOT depend on core.bootstrap
    gateway = build_gateway_v3()

    return {
        "gateway": gateway
    }


if __name__ == "__main__":
    main()
