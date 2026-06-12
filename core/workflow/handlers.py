from worker.handlers.rent_search import handle_rent_search


def validate(step, ctx):
    return {"ok": True}


def fetch(step, ctx):
    providers = step.get("providers", [])
    return {
        "providers": providers,
        "data": "mocked_sources"
    }


def rank(step, ctx):
    return {
        "ranked": True,
        "strategy": step.get("strategy")
    }


def aggregate(step, ctx):
    return {
        "response": "generated_response",
        "city": step.get("city")
    }


HANDLERS = {
    "validate": validate,
    "fetch": fetch,
    "rank": rank,
    "aggregate": aggregate
}
