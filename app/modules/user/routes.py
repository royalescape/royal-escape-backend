from fastapi import APIRouter, Depends
from app.modules.user.schemas import (
    CheckUserRequest,
    SetPinRequest,
    LoginPinRequest,
)
from app.modules.user.service import (
    check_user,
    verify_otp_registration,
    set_pin,
    login_with_pin,
    logout,
)
from app.api.deps import get_current_user
from app.modules.user.schemas import VerifyOtpRequest

from app.modules.user.schemas import SendOtpRequest
from app.modules.user.service import send_otp_registration


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/send")
async def send_otp_api(payload: SendOtpRequest):
    await send_otp_registration(payload.phone)
    return {"otp_sent": True}


@router.post("/check-user")
async def check_user_api(payload: CheckUserRequest):
    return await check_user(payload.phone)


@router.post("/otp/verify")
async def verify_otp_api(payload: VerifyOtpRequest):
    token = await verify_otp_registration(payload.phone, payload.otp)
    return {"registration_token": token}


@router.post("/set-pin")
async def set_pin_api(
    payload: SetPinRequest,
    current=Depends(get_current_user),
):
    user, _ = current
    token = await set_pin(str(user["_id"]), payload.pin)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login-pin")
async def login_pin_api(payload: LoginPinRequest):
    token = await login_with_pin(payload.phone, payload.pin)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout_api(current=Depends(get_current_user)):
    _, payload = current
    await logout(payload)
    return {"logged_out": True}
