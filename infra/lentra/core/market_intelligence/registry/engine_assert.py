def assert_valid_engine(engine, name: str):
    if engine is None:
        raise RuntimeError(f"ENGINE {name} IS NONE")

    if isinstance(engine, dict):
        raise RuntimeError(
            f"ENGINE {name} IS DICT (invalid state pollution). Expected instance with .run()"
        )

    if not hasattr(engine, "run"):
        raise RuntimeError(
            f"ENGINE {name} HAS NO run() METHOD"
        )
