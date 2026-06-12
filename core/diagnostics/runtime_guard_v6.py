from core.diagnostics.error_schema_v6 import normalize_error
from core.diagnostics.error_analyzer_v6 import ErrorAnalyzer

"""
Lentra Diagnostics v6-lite
Runtime Guard
"""


class RuntimeGuard:

    def __init__(self):
        self.errors = []
        self.analyzer = ErrorAnalyzer()

    def safe(self, fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                err = normalize_error(e, context=fn.__name__)
                self.errors.append(err)

                print(">>> DIAGNOSTIC ERROR CAPTURED:", err["error_type"])

                return {
                    "status": "SAFE_FAIL",
                    "error": err
                }

        return wrapper

    def report(self):
        return self.analyzer.analyze(self.errors)
