# DISABLED: auto execution bridge removed
# System now uses manual/selfheal.sh execution only

class AutoHealBridge:

    def __init__(self):
        pass

    def run(self):
        return {
            "status": "disabled",
            "reason": "auto-execution bridge removed for safety"
        }
