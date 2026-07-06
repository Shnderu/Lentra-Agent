"""
RUNTIME INTELLIGENCE ENFORCER

Sits above core.
Never imported by core.
"""

class IntelligenceEnforcer:

    def validate(self, result: dict):
        if result is None:
            raise RuntimeError("[ENFORCER] invalid output")
        return result

    def wrap(self, fn):
        def inner(*args, **kwargs):
            result = fn(*args, **kwargs)
            return self.validate(result)
        return inner
