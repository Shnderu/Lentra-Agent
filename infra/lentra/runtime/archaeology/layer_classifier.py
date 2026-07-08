from typing import Dict, List


class LayerClassifier:
    """
    Architecture layer classifier.

    Purpose:
    - classify repository modules
    - separate active architecture
    - detect legacy zones
    """


    RULES = {

        "api": [
            "lentra.api"
        ],

        "market_intelligence": [
            "lentra.core.market_intelligence"
        ],

        "runtime": [
            "lentra.runtime"
        ],

        "bot": [
            "lentra.bot"
        ],

        "domain": [
            "lentra.domain"
        ],

        "services": [
            "lentra.services"
        ],

        "legacy": [
            "lentra.old",
            "lentra.archive",
            "lentra.v1",
            "backup"
        ]

    }


    def classify(
        self,
        modules: List[str]
    ) -> Dict[str, List[str]]:

        result = {}

        for layer in self.RULES:
            result[layer] = []


        result["unknown"] = []


        for module in modules:

            matched = False


            for layer, prefixes in self.RULES.items():

                for prefix in prefixes:

                    if module.startswith(prefix):

                        result[layer].append(
                            module
                        )

                        matched = True
                        break


                if matched:
                    break


            if not matched:

                result["unknown"].append(
                    module
                )


        return result
