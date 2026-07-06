"""
Backward compatibility shim
ONLY for migration period B4
"""

from lentra.runtime.contracts.envelope import ExecutionEnvelope

# legacy alias
TaskEnvelope = ExecutionEnvelope
