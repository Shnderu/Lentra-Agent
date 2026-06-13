# ============================================================
# GRACEFUL FALLBACK V17.2
# ============================================================


class FallbackStrategy:
    def execute(self, primary_result, cache_result=None):
        if primary_result:
            return primary_result

        if cache_result:
            return {
                "fallback": True,
                "data": cache_result
            }

        return {
            "fallback": True,
            "data": [],
            "status": "degraded"
        }
