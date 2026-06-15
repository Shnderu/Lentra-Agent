from typing import List


class Pagination:

    def slice(self, items: List, page: int = 0, size: int = 5):
        start = page * size
        end = start + size
        return items[start:end]

    def next_page(self, page: int) -> int:
        return page + 1
