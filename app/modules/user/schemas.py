from pydantic import BaseModel, EmailStr
from typing import Optional


class AddressSchema(BaseModel):
    line1: str
    city: str
    state: str
    pincode: str


class UserCreateSchema(BaseModel):
    phone: str
    email: Optional[EmailStr]
    name: str
    address: AddressSchema


class UserResponseSchema(UserCreateSchema):
    id: str


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
