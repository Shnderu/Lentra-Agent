from lentra.core.seal.system_seal import SystemSeal


def assert_domain_safe():
    if SystemSeal.is_sealed():
        raise RuntimeError("[DOMAIN SEALED] modification not allowed at runtime")
