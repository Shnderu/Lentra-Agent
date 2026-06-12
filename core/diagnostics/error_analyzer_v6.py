from collections import Counter

"""
Lentra Diagnostics v6-lite
Error Pattern Analyzer
"""


class ErrorAnalyzer:

    def analyze(self, error_logs: list):
        if not error_logs:
            return {"status": "NO_ERRORS"}

        types = [e.get("error_type") for e in error_logs]
        messages = [e.get("message") for e in error_logs]

        return {
            "total_errors": len(error_logs),
            "top_error_type": Counter(types).most_common(1),
            "top_message": Counter(messages).most_common(1),
            "pattern": "RECURRING_FAILURE" if len(set(types)) < len(types) else "SCATTERED_FAILURE"
        }
