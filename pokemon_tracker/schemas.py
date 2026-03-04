"""Pydantic schemas for request/response validation."""

from typing import Optional
from pydantic import BaseModel


class CardBase(BaseModel):
    name: str
    set_name: Optional[str] = None
    set_id: Optional[str] = None
    number: Optional[str] = None
    rarity: Optional[str] = None
    supertype: Optional[str] = None
    subtypes: Optional[str] = None
    hp: Optional[int] = None
    types: Optional[str] = None
    image_url: Optional[str] = None
    image_url_hires: Optional[str] = None
    condition: str = "NM"
    quantity: int = 1
    purchase_price: Optional[float] = None
    is_foil: bool = False
    is_graded: bool = False
    grade_score: Optional[float] = None
    grading_company: Optional[str] = None
    notes: Optional[str] = None


class CardCreate(CardBase):
    api_id: Optional[str] = None
    attacks: Optional[str] = None
    weaknesses: Optional[str] = None
    resistances: Optional[str] = None
    retreat_cost: Optional[int] = None
    market_price_low: Optional[float] = None
    market_price_mid: Optional[float] = None
    market_price_high: Optional[float] = None
    market_price_market: Optional[float] = None


class CardUpdate(BaseModel):
    condition: Optional[str] = None
    quantity: Optional[int] = None
    purchase_price: Optional[float] = None
    is_foil: Optional[bool] = None
    is_graded: Optional[bool] = None
    grade_score: Optional[float] = None
    grading_company: Optional[str] = None
    notes: Optional[str] = None


class CardResponse(CardCreate):
    id: int

    model_config = {"from_attributes": True}
