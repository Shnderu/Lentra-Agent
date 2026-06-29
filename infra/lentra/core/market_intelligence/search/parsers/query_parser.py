class QueryParser:

    def __init__(self, query: str):
        self.query = query

    def parse(self):
        return {
            "raw": self.query,
            "tokens": self.query.lower().split()
        }


def parse_query(query: str):
    return QueryParser(query).parse()
