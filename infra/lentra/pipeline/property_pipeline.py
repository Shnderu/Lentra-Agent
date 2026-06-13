import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


# ============================================================
# PROPERTY DOMAIN MODEL
# ============================================================

@dataclass
class Property:
    title: str
    price_vnd: Optional[float] = None
    deposit_vnd: Optional[float] = None
    area_m2: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    pet_friendly: Optional[bool] = None
    pool: Optional[bool] = None
    sea_view: Optional[bool] = None
    raw_text: str = ""


# ============================================================
# TELEGRAM MESSAGE INPUT ADAPTER
# ============================================================

class TelegramMessageAdapter:
    @staticmethod
    def to_text(message: Dict[str, Any]) -> str:
        return message.get("text", "") or ""


# ============================================================
# PROPERTY PARSER (Domiko / rental-style text)
# ============================================================

class PropertyParser:

    PRICE_RE = re.compile(r"(\d+(\.\d+)?)\s*млн")
    AREA_RE = re.compile(r"(\d+(\.\d+)?)\s*кв")
    BED_RE = re.compile(r"(\d+)\s*\+")
    DEPOSIT_RE = re.compile(r"Депозит:\s*(\d+(\.\d+)?)\s*млн", re.IGNORECASE)

    @staticmethod
    def parse(text: str) -> Property:

        price = PropertyParser._extract_float(PropertyParser.PRICE_RE, text)
        area = PropertyParser._extract_float(PropertyParser.AREA_RE, text)
        deposit = PropertyParser._extract_float(PropertyParser.DEPOSIT_RE, text)
        bedrooms = PropertyParser._extract_int(PropertyParser.BED_RE, text)

        return Property(
            title=PropertyParser._extract_title(text),
            price_vnd=price,
            deposit_vnd=deposit,
            area_m2=area,
            bedrooms=bedrooms,
            bathrooms=PropertyParser._infer_bathrooms(text),
            pet_friendly=PropertyParser._contains(text, "питомц"),
            pool=PropertyParser._contains(text, "бассейн"),
            sea_view=PropertyParser._contains(text, "море"),
            raw_text=text
        )

    @staticmethod
    def _extract_float(pattern, text: str) -> Optional[float]:
        match = pattern.search(text)
        if not match:
            return None
        return float(match.group(1))

    @staticmethod
    def _extract_int(pattern, text: str) -> Optional[int]:
        match = pattern.search(text)
        if not match:
            return None
        return int(match.group(1))

    @staticmethod
    def _contains(text: str, keyword: str) -> bool:
        return keyword.lower() in text.lower()

    @staticmethod
    def _extract_title(text: str) -> str:
        lines = text.split("\n")
        return lines[0].strip() if lines else "Unknown"

    @staticmethod
    def _infer_bathrooms(text: str) -> Optional[int]:
        if "2 сануз" in text or "2 ванных" in text:
            return 2
        if "сануз" in text or "ванн" in text:
            return 1
        return None


# ============================================================
# NORMALIZER (canonical schema v1)
# ============================================================

class PropertyNormalizer:

    @staticmethod
    def normalize(p: Property) -> Dict[str, Any]:

        return {
            "title": p.title,
            "price_vnd_mln": p.price_vnd,
            "deposit_vnd_mln": p.deposit_vnd,
            "area_m2": p.area_m2,
            "bedrooms": p.bedrooms,
            "bathrooms": p.bathrooms,
            "features": {
                "pet_friendly": p.pet_friendly,
                "pool": p.pool,
                "sea_view": p.sea_view,
            },
            "quality_flags": PropertyNormalizer._quality_flags(p)
        }

    @staticmethod
    def _quality_flags(p: Property) -> List[str]:

        flags = []

        if p.pool:
            flags.append("HAS_POOL")
        if p.sea_view:
            flags.append("SEA_VIEW")
        if p.pet_friendly:
            flags.append("PET_FRIENDLY")

        if p.area_m2 and p.area_m2 > 100:
            flags.append("LARGE_AREA")

        return flags


# ============================================================
# SCORING ENGINE v1 (simple heuristic MVP)
# ============================================================

class PropertyScorer:

    @staticmethod
    def score(p: Property) -> float:

        score = 0.0

        # price attractiveness (lower is better)
        if p.price_vnd:
            if p.price_vnd < 15:
                score += 50
            elif p.price_vnd < 25:
                score += 30
            else:
                score += 10

        # features
        if p.pool:
            score += 20
        if p.sea_view:
            score += 25
        if p.pet_friendly:
            score += 10

        # size bonus
        if p.area_m2:
            score += min(p.area_m2 / 10, 20)

        return round(score, 2)


# ============================================================
# PIPELINE ORCHESTRATOR
# ============================================================

class PropertyPipeline:

    def process_telegram_message(self, message: Dict[str, Any]) -> Dict[str, Any]:

        text = TelegramMessageAdapter.to_text(message)

        parsed = PropertyParser.parse(text)
        normalized = PropertyNormalizer.normalize(parsed)
        score = PropertyScorer.score(parsed)

        return {
            "property": normalized,
            "score": score,
            "source": "telegram",
            "raw": text
        }
