from pathlib import Path


class DomainClassifier:


    RULES = {

        "market_intelligence": [
            "market_intelligence",
            "pricing",
            "risk",
            "dedup",
            "signals",
            "intelligence",
        ],


        "decision": [
            "decision",
            "verdict",
            "fusion",
            "policy",
        ],


        "ranking": [
            "ranking",
            "ranker",
            "scoring",
        ],


        "runtime": [
            "runtime",
            "bootstrap",
            "worker",
            "pipeline",
        ],


        "services": [
            "services",
            "service",
        ],


        "domain": [
            "domain",
        ],


        "modules": [
            "modules",
        ],


        "config": [
            "config",
        ],


        "tests": [
            "test",
            "tests",
        ],


        "tools": [
            "tools",
            "scripts",
        ]

    }



    def classify(
        self,
        files
    ):

        result = {}

        for key in self.RULES:
            result[key] = []


        result["unknown"] = []


        for file in files:

            path = str(
                Path(file)
            ).lower()


            matched = False


            for group, patterns in self.RULES.items():

                if any(
                    pattern in path
                    for pattern in patterns
                ):

                    result[group].append(
                        file
                    )

                    matched = True

                    break


            if not matched:

                result["unknown"].append(
                    file
                )


        return result
