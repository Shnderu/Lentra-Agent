class VietnamGeoEngine:
    """
    Normalizes Vietnam market geography into unified segments.
    """

    def normalize(self, listing: dict):

        text = (listing.get("location") or "").lower()

        if "da nang" in text:
            city = "da_nang"
        elif "hanoi" in text:
            city = "hanoi"
        elif "ho chi minh" in text or "saigon" in text:
            city = "ho_chi_minh"
        elif "nha trang" in text:
            city = "nha_trang"
        elif "hoi an" in text:
            city = "hoi_an"
        elif "phu quoc" in text:
            city = "phu_quoc"
        else:
            city = "unknown"

        listing["country"] = "vietnam"
        listing["city"] = city

        return listing
