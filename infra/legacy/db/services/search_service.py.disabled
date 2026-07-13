from dataclasses import dataclass
from typing import List, Optional

from lentra.db.repositories.apartment_repo import ApartmentRepository
from lentra.db.models.apartment import Apartment


# ----------------------------
# DTO входа сервиса
# ----------------------------
@dataclass
class SearchRequestDTO:
    query: str
    budget_max: Optional[float] = None


# ----------------------------
# DTO результата
# ----------------------------
@dataclass
class SearchResultDTO:
    id: int
    title: str
    price_vnd_mln: float
    area_m2: float
    city: str
    district: str
    pool: bool
    sea_view: bool
    score: float


# ----------------------------
# SERVICE LAYER (CORE)
# ----------------------------
class SearchService:

    def __init__(self, repo: ApartmentRepository):
        self.repo = repo

    def search(self, req: SearchRequestDTO) -> dict:
        """
        1. Получить кандидатов из DB
        2. Применить фильтры
        3. Посчитать score
        4. Отсортировать
        5. Вернуть DTO
        """

        candidates: List[Apartment] = self.repo.list_all()

        filtered = self._apply_filters(candidates, req)
        scored = self._score(filtered, req)
        ranked = sorted(scored, key=lambda x: x.score, reverse=True)

        return {
            "query": req.query,
            "results": [self._to_dict(x) for x in ranked]
        }

    # ----------------------------
    # FILTER LAYER
    # ----------------------------
    def _apply_filters(
        self,
        items: List[Apartment],
        req: SearchRequestDTO
    ) -> List[Apartment]:

        result = []

        for a in items:

            if req.budget_max is not None and a.price_vnd_mln > req.budget_max:
                continue

            result.append(a)

        return result

    # ----------------------------
    # SCORING ENGINE
    # ----------------------------
    def _score(
        self,
        items: List[Apartment],
        req: SearchRequestDTO
    ) -> List[SearchResultDTO]:

        scored = []

        for a in items:
            score = 0.0

            # базовая релевантность
            score += 0.2

            # pool bonus
            if a.pool:
                score += 0.3

            # sea view bonus
            if a.sea_view:
                score += 0.3

            # price attractiveness (дешевле = лучше)
            if req.budget_max:
                score += max(0, 0.2 * (1 - a.price_vnd_mln / req.budget_max))

            scored.append(
                SearchResultDTO(
                    id=a.id,
                    title=a.title,
                    price_vnd_mln=a.price_vnd_mln,
                    area_m2=a.area_m2,
                    city=a.city,
                    district=a.district,
                    pool=a.pool,
                    sea_view=a.sea_view,
                    score=round(score, 3),
                )
            )

        return scored

    # ----------------------------
    # RESPONSE SERIALIZATION
    # ----------------------------
    def _to_dict(self, x: SearchResultDTO) -> dict:
        return {
            "id": x.id,
            "title": x.title,
            "price_vnd_mln": x.price_vnd_mln,
            "area_m2": x.area_m2,
            "city": x.city,
            "district": x.district,
            "pool": x.pool,
            "sea_view": x.sea_view,
            "score": x.score,
        }
