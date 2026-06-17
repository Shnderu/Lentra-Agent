# ============================================================
# EXECUTOR COMPAT LAYER
# restores ActionExecutor for container DI
# ============================================================

import subprocess


class ActionExecutor:
    """
    Compatibility wrapper for legacy container expectations.
    """
    def execute(self, action, data):
        if action is None:
            return data

        # безопасное выполнение логики действия
        # (временно упрощённый слой)
        if isinstance(action, dict):
            cmd = action.get("cmd")
            if cmd:
                try:
                    return subprocess.getoutput(cmd)
                except Exception as e:
                    return {"error": str(e), "action": action}

        if callable(action):
            try:
                return action(data)
            except Exception as e:
                return {"error": str(e)}

        return data
