
from core.search.engine import SearchEngine
from core.deals.engine import DealEngine
from core.ai.planner.engine import AIPlanner
from core.fsm.manager import handle_message
from core.fsm.flows.route_flow import start_route_flow
from core.fsm.flows.watch_flow import start_watch_flow
from core.fsm.flows.planner_flow import start_planner_flow


search = SearchEngine()
deals = DealEngine()
planner = AIPlanner()


async def execute(intent, user_id: int):

    if intent.name == "route_search":
        return await handle_message(user_id, intent.payload["text"])

    if intent.name == "watch_route":
        return start_watch_flow(user_id)

    if intent.name == "deal_search":
        return deals.get_deals()

    if intent.name == "ai_planner":
        return planner.plan(intent.payload["text"], user_id)

    return "🤖 I didn't understand your request"
