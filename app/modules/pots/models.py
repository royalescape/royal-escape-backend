from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Pot(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    name: str
    value: float
    type: str
    closing_date: datetime
    winner: str | None = None


    class Config:
        arbitrary_types_allowed = True