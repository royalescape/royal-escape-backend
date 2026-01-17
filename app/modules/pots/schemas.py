from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class FAQSchema(BaseModel):
    q: str
    a: str


class PotCreateSchema(BaseModel):
    name: str
    description: str
    entry_price: int
    max_entries: int
    start_date: datetime
    closing_date: datetime
    faq: List[FAQSchema]
    terms_and_conditions: str


class PotUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    closing_date: Optional[datetime]
    faq: Optional[List[FAQSchema]]
    terms_and_conditions: Optional[str]


class PotEntrySchema(BaseModel):
    quantity: int = 1
