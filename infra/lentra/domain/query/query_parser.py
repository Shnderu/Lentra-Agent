from dataclasses import dataclass


@dataclass
class QueryObject:
    city: str | None = None
    budget_max: float | None = None
    pool: bool | None = None
    sea_view: bool | None = None


def parse_query(text: str) -> QueryObject:
    text = text.lower()

    return QueryObject(
        city="Da Nang" if "da nang" in text else None,
        budget_max=None,
        pool="pool" in text,
        sea_view="sea view" in text or "sea" in text,
    )
