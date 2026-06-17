class ContainerValidator:

    REQUIRED = [
        "connector",
        "graph_factory"
    ]

    def validate(self, container):
        missing = []

        for r in self.REQUIRED:
            if not hasattr(container, r):
                missing.append(r)

        if missing:
            raise RuntimeError(f"[CONTAINER INVALID] missing: {missing}")

        return True
