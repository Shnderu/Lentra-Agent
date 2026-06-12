from core.diagnostics.runtime_guard_v6 import RuntimeGuard

guard = RuntimeGuard()

@guard.safe
def broken_function():
    return 1 / 0

broken_function()

print(guard.report())
