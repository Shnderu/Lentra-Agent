# ============================================================
# LENTRA QUALITY MODEL V16.3
# ============================================================

from dataclasses import dataclass


@dataclass
class QualityScore:
    listing_id: str
    trust_score: float          # 0-100
    source_score: float         # 0-100
    noise_score: float          # 0-100 (higher = worse)
    duplicate_score: float      # 0-100 (higher = duplicate risk)
