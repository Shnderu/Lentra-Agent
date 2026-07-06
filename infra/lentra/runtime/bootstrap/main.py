"""
Runtime bootstrap layer (ARCH LOCK SAFE)
DO NOT import core.bootstrap
"""

from lentra.core.market_intelligence.build import build_intelligence_gateway


def main():
    # runtime entry must NOT depend on core.bootstrap
    gateway = build_intelligence_gateway()

    return {
        "gateway": gateway
    }


if __name__ == "__main__":
    main()
