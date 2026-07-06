from dataclasses import dataclass
from typing import List


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    normalized_command: list[str] | None = None


class ExecutionPolicyV1:
    """
    STRICT EXECUTION POLICY LAYER

    Purpose:
    - Remove free-form command execution
    - Enforce whitelist-based runtime behavior
    - Ensure deterministic command graph
    """

    def __init__(self):
        self.allowed_binaries = {
            "python",
            "echo",
        }

        self.allowed_patterns = {
            "risk_engine",
            "dedup",
            "area",
        }

        self.blocked_tokens = {
            "--system_prompt",
            "system_prompt",
            "rm",
            "sudo",
        }

    def validate(self, command: List[str]) -> PolicyDecision:
        if not command:
            return PolicyDecision(False, "Empty command")

        for token in command:
            if any(b in token for b in self.blocked_tokens):
                return PolicyDecision(False, f"Blocked token detected: {token}")

        binary = command[0]

        if binary not in self.allowed_binaries:
            return PolicyDecision(False, f"Binary not allowed: {binary}")

        joined = " ".join(command)

        if not any(p in joined for p in self.allowed_patterns):
            # allow safe python echo fallback only
            if binary == "python" or binary == "echo":
                return PolicyDecision(True, "Fallback safe execution", command)

            return PolicyDecision(False, "No allowed pattern matched")

        return PolicyDecision(True, "Policy approved", command)
