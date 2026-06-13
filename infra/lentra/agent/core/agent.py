# ============================================================
# PATCH V17.1 - AUTONOMOUS CAPABILITY
# ============================================================

from lentra.agent.planner.planner import Planner
from lentra.agent.decider.decider import Decider
from lentra.agent.actions.executor import ActionExecutor
from lentra.agent.loop.engine import AutonomousLoop
from lentra.agent.monitor.market_state import MarketState
from lentra.agent.monitor.price_tracker import PriceTracker
from lentra.agent.alerts.alert_engine import AlertEngine


class RentAgent:
    def __init__(self):
        self.planner = Planner()
        self.decider = Decider()
        self.executor = ActionExecutor()

        self.loop = AutonomousLoop(
            handler=None,
            market_state=MarketState(),
            price_tracker=PriceTracker(),
            alert_engine=AlertEngine()
        )

    async def run(self, intent, base_data):
        plan = self.planner.build_plan(intent)

        data = base_data

        for step in plan:
            action = self.decider.choose_action(step, data)
            data = self.executor.execute(action, data)

        return {
            "result": data,
            "steps": plan,
            "mode": "v17_agentic"
        }

    async def start_autonomous_mode(self, query):
        return await self.loop.run_cycle(query)
EOFcat << 'EOF' > lentra/agent/core/agent.py
# ============================================================
# PATCH V17.1 - AUTONOMOUS CAPABILITY
# ============================================================

from lentra.agent.planner.planner import Planner
from lentra.agent.decider.decider import Decider
from lentra.agent.actions.executor import ActionExecutor
from lentra.agent.loop.engine import AutonomousLoop
from lentra.agent.monitor.market_state import MarketState
from lentra.agent.monitor.price_tracker import PriceTracker
from lentra.agent.alerts.alert_engine import AlertEngine


class RentAgent:
    def __init__(self):
        self.planner = Planner()
        self.decider = Decider()
        self.executor = ActionExecutor()

        self.loop = AutonomousLoop(
            handler=None,
            market_state=MarketState(),
            price_tracker=PriceTracker(),
            alert_engine=AlertEngine()
        )

    async def run(self, intent, base_data):
        plan = self.planner.build_plan(intent)

        data = base_data

        for step in plan:
            action = self.decider.choose_action(step, data)
            data = self.executor.execute(action, data)

        return {
            "result": data,
            "steps": plan,
            "mode": "v17_agentic"
        }

    async def start_autonomous_mode(self, query):
        return await self.loop.run_cycle(query)
