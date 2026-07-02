def assert_valid_engine(engine, name: str):
    if engine is None:
        raise RuntimeError(f"ENGINE {name} IS NONE")

    if isinstance(engine, dict):
        raise RuntimeError(
            f"ENGINE {name} IS DICT (invalid state pollution). Expected instance with .evaluate()"
        )

    if not hasattr(engine, "evaluate"):
        raise RuntimeError(
            f"ENGINE {name} HAS NO evaluate() METHOD"
        )
