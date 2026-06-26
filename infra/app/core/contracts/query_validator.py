from lentra.core.contracts.query_options import QueryOptions


class QueryValidator:

    def validate(self, options: QueryOptions):

        if options.limit < 1:
            options.limit = 1

        if options.limit > 50:
            options.limit = 50

        if options.offset < 0:
            options.offset = 0

        if options.sort_by not in ["score", "price"]:
            options.sort_by = "score"

        return options
