from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class RegisterUserRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    pincode: str = Field(..., min_length=4, max_length=10)


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
