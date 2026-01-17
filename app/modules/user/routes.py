from fastapi import APIRouter
from app.modules.user.schemas import UserCreateSchema
from app.modules.user.service import create_user, get_dashboard
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from pydantic import BaseModel
from app.modules.user.otp_service import send_otp
from app.modules.user.service import verify_otp_and_login
from app.utils.mongo import serialize_mongo


router = APIRouter(prefix="/users", tags=["users"])


class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


@router.post("/")
async def register_user(payload: UserCreateSchema):
    user_id = await create_user(payload.model_dump())
    return {"user_id": str(user_id)}


@router.get("/me")
async def my_profile(current_user=Depends(get_current_user)):
    return serialize_mongo(current_user)


@router.get("/me/dashboard")
async def my_dashboard(current_user=Depends(get_current_user)):
    return await get_dashboard(str(current_user["_id"]))


@router.post("/auth/otp/send")
async def send_otp_api(payload: SendOTPRequest):
    await send_otp(payload.phone)
    return {"message": "OTP sent successfully"}


@router.post("/auth/otp/verify")
async def verify_otp_api(payload: VerifyOTPRequest):
    token = await verify_otp_and_login(payload.phone, payload.otp)
    return {"access_token": token, "token_type": "bearer"}
