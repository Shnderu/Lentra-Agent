from lentra.bot.services.registry import SearchResult
from lentra.bot.domain.dto import PropertyDTO


class PropertyMapper:

    def to_dto(self, r: SearchResult, idx: int) -> PropertyDTO:
        return PropertyDTO(
            id=idx,
            title=r.title,
            city=r.city,
            district=r.district,
            price_vnd_mln=r.price_vnd_mln,
            score=r.score,
            pool=r.pool,
            sea_view=r.sea_view
        )
