class RuleViolation(Exception):
    pass


FORBIDDEN_IMPORTS = [
    "lentra.domain -> lentra.services",
    "lentra.domain -> lentra.api",
    "lentra.core -> lentra.api",
]


class RuleChecker:

    @staticmethod
    def validate(graph: dict):

        for file, deps in graph.items():
            for dep in deps:
                for rule in FORBIDDEN_IMPORTS:
                    src, dst = rule.split(" -> ")
                    if src in file and dst in dep:
                        raise RuleViolation(
                            f"[ARCH RULE VIOLATION] {file} -> {dep}"
                        )

        return True
