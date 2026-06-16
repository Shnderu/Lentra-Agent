class FilterEngine:

    def apply(self, state, filters: dict):

        for k, v in filters.items():
            if v is not None:
                state.filters[k] = v

        return state
