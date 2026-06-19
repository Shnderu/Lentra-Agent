"""
COMPAT LAYER v1
Graph execution bridge → Scenario Engine v1
"""

from lentra.core.executor import execute_scenario  # предполагаемый единый executor

class ExecutionEngine:
    def run(self, payload: dict):
        """
        Unified execution entry point
        """
        return execute_scenario(payload)

execution_engine = ExecutionEngine()
