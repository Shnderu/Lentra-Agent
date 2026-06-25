from typing import List
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.application.services.event_collector import EventCollector
from lentra.bot.features.rent_search.contracts.events import RentEvent


class ResponseBuilder:

    def __init__(self):
        self.events = EventCollector()

    def build(self, context: SearchContext, items: List[RentSearchItem]) -> str:

        header = (
            f"🏠 Rent search result\n"
            f"Query: {context.raw_query}\n"
            f"City: {context.city or 'any'}\n\n"
        )

        if not items:
            return header + "No results found"

        lines = []

        for idx, item in enumerate(items):

            # impression event
            self.events.track(
                RentEvent(
                    event_type="impression",
                    query=context.query,
                    city=context.city,
                    item_title=item.title,
                    item_city=item.city,
                    position=idx
                )
            )

            lines.append(
                f"• {item.title} | {item.price} | {item.city}"
            )

        return header + "\n".join(lines)
