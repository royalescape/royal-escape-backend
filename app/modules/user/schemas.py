from pydantic import BaseModel, Field
from typing import Optional


class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)
    pin: str = Field(..., min_length=4, max_length=6)
    email: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, min_length=6, max_length=6)


class DashboardSchema(BaseModel):
    balance: float
    total_entries: int
    total_winnings: float


class CheckUserRequest(BaseModel):
    phone: str


class SetPinRequest(BaseModel):
    pin: str


class LoginPinRequest(BaseModel):
    phone: str
    pin: str


class VerifyOtpRequest(BaseModel):
    phone: str
    otp: str


class SendOtpRequest(BaseModel):
    phone: str
