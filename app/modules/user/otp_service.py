from app.core.redis import redis_client
from app.utils.otp import generate_otp, send_otp_sms
from app.core.config import settings
from fastapi import HTTPException, status

OTP_KEY = "otp:{phone}"
RATE_KEY = "otp_rate:{phone}"


async def send_otp(phone: str):
    rate_key = RATE_KEY.format(phone=phone)

    if await redis_client.exists(rate_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OTP already sent. Please wait.",
        )

    otp = generate_otp()
    otp_key = OTP_KEY.format(phone=phone)

    await redis_client.setex(otp_key, settings.otp_expiry_seconds, otp)

    print("OTP stored in Redis:", otp_key)

    await redis_client.setex(rate_key, settings.otp_resend_limit_seconds, 1)

    await send_otp_sms(phone, otp)


async def verify_otp(phone: str, otp: str):
    otp_key = OTP_KEY.format(phone=phone)
    stored_otp = await redis_client.get(otp_key)

    if not stored_otp or stored_otp != otp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP"
        )

    await redis_client.delete(otp_key)
