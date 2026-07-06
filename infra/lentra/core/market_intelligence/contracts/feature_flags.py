def is_enabled(flag: str, context: dict = None) -> bool:
    context = context or {}

    flags = context.get("flags", {})

    return bool(flags.get(flag, False))
