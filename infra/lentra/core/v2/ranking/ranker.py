from lentra.core.dto.listing_dto import ListingDTO


class Ranker:

    def rank(self, listings):

        def score(l: ListingDTO):
            return l.price

        return sorted(listings, key=score)
