from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class User(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    phone: str

    pin_hash: str | None = None
    pin_set: bool = False

    is_verified: bool = False

    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
