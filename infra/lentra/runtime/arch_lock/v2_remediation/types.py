def load_default_rules():
    """
    ARCH LOCK v2 compatible rule format (tuple-based)
    """

    return [
        ("lentra.runtime", "lentra.core"),
        ("lentra.runtime.bootstrap", "lentra.core"),
        ("lentra.runtime.arch_lock", "lentra.core"),
    ]
