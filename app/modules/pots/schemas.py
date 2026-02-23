from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.modules.pots.enums import PotType


class FAQSchema(BaseModel):
    q: str
    a: str


class CreatePotEntrySchema(BaseModel):
    quantity: int = 1
    reference_id: str


class PotCreateSchema(BaseModel):
    name: str
    description: str
    entry_price: int
    max_entries: int
    prize_amount: float
    icon: str
    start_date: datetime
    closing_date: datetime
    faq: List[FAQSchema]
    terms_and_conditions: list[str]
    type: PotType


class PotUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    closing_date: Optional[datetime]
    faq: Optional[List[FAQSchema]]
    terms_and_conditions: list[str]


class PotEntrySchema(BaseModel):
    quantity: int = 1


class PotPublicResponse(BaseModel):
    id: str
    icon: Optional[str]
    name: str
    description: str
    prize_amount: float
    type: PotType


class FAQItem(BaseModel):
    q: str
    a: str


class PotFullResponse(BaseModel):
    id: str
    category: str
    type: str
    name: str
    icon: Optional[str]
    description: str
    prizeValue: str
    totalSlots: int
    filled: int
    remaining: int
    daysLeft: int
    endDate: str
    status: str
    entryFee: Optional[int]
    maxEntries: Optional[int]
    revenue: Optional[int]
    createdDate: Optional[str]
    drawDate: Optional[str]
    winner: Optional[str]
    totalEntries: Optional[int]
    prizeDetails: Optional[List[str]]
    gallery: Optional[List[str]]
    faqs: Optional[List[FAQItem]]
    termsAndConditions: Optional[List[str]]
    color: Optional[str]
