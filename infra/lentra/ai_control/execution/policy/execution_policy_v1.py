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

    Controlled runtime whitelist.

    Allowed:
    - python
    - echo
    - aider

    Forbidden:
    - shell escalation
    - system prompt injection
    - destructive commands
    """

    def __init__(self):
        self.allowed_binaries = {
            "python",
            "echo",
            "aider",
        }

        self.allowed_patterns = {
            "risk_engine",
            "dedup",
            "area",
            "market",
        }

        self.blocked_tokens = {
            "--system_prompt",
            "system_prompt",
            "rm",
            "sudo",
            "chmod",
            "chown",
        }


    def validate(
        self,
        command: List[str]
    ) -> PolicyDecision:

        if not command:
            return PolicyDecision(
                False,
                "Empty command"
            )


        for token in command:
            if any(
                b in token
                for b in self.blocked_tokens
            ):
                return PolicyDecision(
                    False,
                    f"Blocked token detected: {token}"
                )


        binary = command[0]


        if binary not in self.allowed_binaries:
            return PolicyDecision(
                False,
                f"Binary not allowed: {binary}"
            )


        joined = " ".join(command)


        if binary == "aider":

            if not any(
                pattern in joined
                for pattern in self.allowed_patterns
            ):
                return PolicyDecision(
                    False,
                    "Aider target outside allowed scope"
                )


            return PolicyDecision(
                True,
                "Aider execution approved",
                command
            )


        if binary in {
            "python",
            "echo",
        }:
            return PolicyDecision(
                True,
                "Safe execution approved",
                command
            )


        return PolicyDecision(
            False,
            "Policy rejected"
        )
