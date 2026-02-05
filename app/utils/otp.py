import random
from twilio.rest import Client
from app.core.config import settings

twilio_client = Client(settings.twilio_sid, settings.twilio_token)


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


async def send_otp_sms(phone: str, otp: str):
    twilio_client.messages.create(
        body=f"Your Royal Escape code is {otp}. Unlock your dreams now!",
        from_=settings.twilio_from,
        to=phone,
    )
