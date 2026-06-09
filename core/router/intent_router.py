import re
from dataclasses import dataclass
from typing import Dict, Any


# -----------------------------
# INTENT TYPES (CANONICAL)
# -----------------------------
ROUTE_SEARCH = "route_search"
WATCH_ROUTE = "watch_route"
BUDGET_SEARCH = "budget_search"
DEAL_SEARCH = "deal_search"
AI_PLANNER = "ai_planner"
ERROR_FARE = "error_fare"
UNKNOWN = "unknown"


@dataclass
class IntentResult:
    intent: str
    confidence: float
    payload: Dict[str, Any]


# -----------------------------
# SIMPLE RULE-BASED ROUTER v1
# -----------------------------
class IntentRouter:

    def route(self, text: str) -> IntentResult:
        text_l = text.lower().strip()

        # 1. ERROR FARE
        if any(w in text_l for w in ["error fare", "ошибоч", "аномал", "сбой тариф"]):
            return IntentResult(ERROR_FARE, 0.95, {"text": text})

        # 2. WATCH ROUTE
        if any(w in text_l for w in ["следи", "монитор", "цена упад", "уведом"]):
            return IntentResult(WATCH_ROUTE, 0.90, {"text": text})

        # 3. BUDGET SEARCH
        if re.search(r"\d+\s*(₽|руб|rub|eur|€|$)", text_l):
            return IntentResult(BUDGET_SEARCH, 0.85, {"text": text})

        # 4. DEAL SEARCH
        if any(w in text_l for w in ["горящ", "дешев", "скидк", "deal", "offer"]):
            return IntentResult(DEAL_SEARCH, 0.80, {"text": text})

        # 5. AI PLANNER
        if any(w in text_l for w in ["куда", "спланируй", "план", "хочу", "подбери"]):
            return IntentResult(AI_PLANNER, 0.75, {"text": text})

        # 6. ROUTE SEARCH (default travel intent)
        if any(w in text_l for w in ["из ", "в ", "перелет", "рейс", "билет"]):
            return IntentResult(ROUTE_SEARCH, 0.70, {"text": text})

        return IntentResult(UNKNOWN, 0.5, {"text": text})
