from lentra.core.seal.system_seal import SystemSeal


class SideEffectGuard:

    @staticmethod
    def assert_safe_layer(layer: str):
        if layer not in ["adapter", "infrastructure"]:
            raise RuntimeError(
                f"[SIDE EFFECT VIOLATION] {layer} cannot perform IO"
            )

        SystemSeal.assert_not_sealed()
