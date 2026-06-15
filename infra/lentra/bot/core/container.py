from dataclasses import dataclass

from lentra.bot.client import APIClient
from lentra.bot.services.registry import SearchService


@dataclass
class Container:
    api_client: APIClient
    search_service: SearchService


def build_container() -> Container:
    api_client = APIClient(base_url="http://localhost:8000")

    search_service = SearchService(client=api_client)

    return Container(
        api_client=api_client,
        search_service=search_service,
    )
