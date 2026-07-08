from pathlib import Path


class ArchitectureClassifier:

    CORE_PATHS = [
        "lentra/core/market_intelligence",
        "lentra/core/ai",
        "lentra/runtime",
    ]

    API_PATHS = [
        "lentra/api",
    ]

    BOT_PATHS = [
        "lentra/bot",
    ]

    DATA_PATHS = [
        "lentra/data",
    ]


    def classify(
        self,
        files
    ):

        result = {
            "core": [],
            "api": [],
            "bot": [],
            "data": [],
            "legacy": [],
            "unknown": [],
        }


        for file in files:

            path = str(
                Path(file)
            )


            if any(
                x in path
                for x in self.CORE_PATHS
            ):
                result["core"].append(
                    path
                )


            elif any(
                x in path
                for x in self.API_PATHS
            ):
                result["api"].append(
                    path
                )


            elif any(
                x in path
                for x in self.BOT_PATHS
            ):
                result["bot"].append(
                    path
                )


            elif any(
                x in path
                for x in self.DATA_PATHS
            ):
                result["data"].append(
                    path
                )


            else:
                result["unknown"].append(
                    path
                )


        return result
