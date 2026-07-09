from typing import Dict, Any, List

from pydantic import BaseModel


class MiniAppObjectSchema(BaseModel):

    id: str

    title: str

    price: float

    currency: str

    city: str


class MiniAppIntelligenceSchema(BaseModel):

    price_signal: str

    market_difference: float

    risk_level: str

    duplicates: int

    trend: str


class MiniAppVerdictSchema(BaseModel):

    label: str

    confidence: float


class MiniAppExplanationSchema(BaseModel):

    summary: str

    movement: str


class MiniAppCardSchema(BaseModel):

    schema_version: str

    object: MiniAppObjectSchema

    intelligence: MiniAppIntelligenceSchema

    verdict: MiniAppVerdictSchema

    explanation: MiniAppExplanationSchema


class MiniAppSearchResponseSchema(BaseModel):

    api_version: str

    schema_version: str

    platform: str

    query: str

    count: int

    results: List[MiniAppCardSchema]
