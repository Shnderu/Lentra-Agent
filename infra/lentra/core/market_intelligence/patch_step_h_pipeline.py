from lentra.core.market_intelligence.contracts.listing_contract_guard import ListingContractGuard

class StepHPatch:

    @staticmethod
    def apply(listings: list) -> list:
        normalized = []

        for l in listings:
            safe = ListingContractGuard.normalize(l)

            # гарантируем deep safety before engines
            if not safe:
                continue

            normalized.append(safe)

        return normalized
