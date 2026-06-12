import json
import time
import random


class AINativeOrchestrator:
    """
    Top-level AI orchestration layer.
    Produces execution strategy for lifecycle engine.
    """

    def build_strategy(self, task: dict, metrics: dict = None):
        task_type = task.get("type")
        payload = task.get("payload")

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        base_strategy = {
            "mode": "deterministic",
            "risk": "low",
            "parallel": False
        }

        # --- AI heuristic decision layer (stub of LLM reasoning) ---

        if task_type == "rent.search":
            city = payload.get("city", "")

            # adaptive complexity scoring
            complexity = len(city) % 3

            if complexity == 0:
                return {
                    "mode": "fast_path",
                    "parallel": False,
                    "providers": ["faswaz"],
                    "ranking": "simple",
                    "cache": True
                }

            elif complexity == 1:
                return {
                    "mode": "balanced",
                    "parallel": True,
                    "providers": ["faswaz"],
                    "ranking": "ai_rank_v1",
                    "cache": True
                }

            else:
                return {
                    "mode": "deep_ai",
                    "parallel": True,
                    "providers": ["faswaz"],
                    "ranking": "ai_rank_v2",
                    "cache": False,
                    "retry_policy": "aggressive"
                }

        # fallback
        return base_strategy


    def reward_signal(self, latency: float, success: bool):
        """
        Simple reinforcement feedback signal generator.
        """
        score = 0

        if success:
            score += 1.0
        else:
            score -= 1.0

        # latency penalty
        score -= min(latency, 5) * 0.1

        return score
