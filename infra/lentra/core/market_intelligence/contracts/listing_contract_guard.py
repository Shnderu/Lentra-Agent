class ListingContractGuard:

    """
    Runtime contract safety layer.

    Rules:
    - price_vnd is canonical internal price
    - price is compatibility alias only
    - market_price belongs to MarketService
    - guard must not create market truth
    """

    @staticmethod
    def normalize(
        listing: dict
    ) -> dict:


        # -------------------------
        # PRICE CONTRACT
        # -------------------------

        price_vnd = listing.get(
            "price_vnd"
        )


        if price_vnd is not None:

            listing["price_vnd"] = float(
                price_vnd
            )

            # legacy compatibility
            listing["price"] = float(
                price_vnd
            )


        else:

            # fallback for legacy inputs
            listing["price"] = float(
                listing.get(
                    "price",
                    0
                )
                or 0
            )


            listing["price_vnd"] = listing[
                "price"
            ]



        # -------------------------
        # MARKET PRICE
        # -------------------------
        #
        # Market truth belongs to MarketService.
        # Do not calculate here.
        #

        if listing.get(
            "market_price"
        ) is not None:

            listing["market_price"] = float(
                listing["market_price"]
            )



        # -------------------------
        # LOCATION CONTRACT
        # -------------------------

        loc = listing.get(
            "location"
        )


        if isinstance(
            loc,
            str
        ):

            listing["location"] = {
                "segment": loc,
                "micro_market": "unknown"
            }


        elif isinstance(
            loc,
            dict
        ):

            listing["location"] = {
                "segment": loc.get(
                    "segment",
                    "unknown"
                ),

                "micro_market": loc.get(
                    "micro_market",
                    "unknown"
                )
            }


        else:

            listing["location"] = {
                "segment": "unknown",
                "micro_market": "unknown"
            }



        # -------------------------
        # RISK CONTRACT
        # -------------------------

        listing["risk"] = float(
            listing.get(
                "risk",
                0.5
            )
            or 0.5
        )


        return listing
