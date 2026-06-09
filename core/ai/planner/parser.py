
import re
from core.ai.planner.intents import TravelIntent


def parse_query(text: str) -> TravelIntent:

    text_lower = text.lower()

    # naive extraction (v1 stub, later → LLM)

    origin = None
    destination = None

    if "из" in text_lower and "в" in text_lower:
        try:
            origin = text_lower.split("из")[1].split("в")[0].strip()
            destination = text_lower.split("в")[1].split()[0].strip()
        except:
            pass

    budget = None
    match = re.search(r"(\d+)\s?(€|eur|руб|rub)", text_lower)
    if match:
        budget = int(match.group(1))

    return TravelIntent(
        origin=origin,
        destination=destination,
        date=None,
        budget=budget,
        mode="ai_planner",
        tags=[]
    )
