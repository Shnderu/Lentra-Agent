class PreflightValidator:

    def validate_container(self, container):
        required = ["connector"]

        for r in required:
            if not hasattr(container, r) or getattr(container, r) is None:
                raise RuntimeError(f"[PRE-FLIGHT FAIL] missing: {r}")

        return True
