class SavedSearches:

    def add(self, state, query: str):

        if query not in state.saved_searches:
            state.saved_searches.append(query)

        return state
