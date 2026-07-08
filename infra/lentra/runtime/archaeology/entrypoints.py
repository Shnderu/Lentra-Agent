from pathlib import Path


ENTRYPOINT_MARKERS = {
    "lentra/api",
    "lentra/runtime",
    "lentra/bot",
    "lentra/services",
}


class EntrypointDetector:


    def detect(
        self,
        nodes
    ):

        result = []

        for path in nodes:

            normalized = str(
                Path(path)
            )

            for marker in ENTRYPOINT_MARKERS:

                if marker in normalized:

                    result.append(
                        path
                    )

                    break

        return result
