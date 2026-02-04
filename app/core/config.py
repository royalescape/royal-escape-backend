from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Royal Escape API"
    redis_url: str

    mongo_uri: str
    mongo_db: str = "royal--escape"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60 * 24

    twilio_sid: str
    twilio_token: str
    twilio_from: str

    # OTP
    otp_expiry_seconds: int = 3000  # 5 minutes
    otp_resend_limit_seconds: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
