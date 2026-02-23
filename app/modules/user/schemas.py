from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


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
