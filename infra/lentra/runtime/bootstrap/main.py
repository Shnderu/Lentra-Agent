"""
Runtime bootstrap layer.

Legacy bootstrap entrypoint retired.

Canonical execution path:

    SearchPipeline
        ->
    GatewayV3
        ->
    Market Intelligence engines
        ->
    DecisionLayer

This module is kept only for compatibility with
bootstrap_lock metadata.
"""


def main():
    return {
        "gateway": None,
        "status": "retired"
    }


if __name__ == "__main__":
    main()
