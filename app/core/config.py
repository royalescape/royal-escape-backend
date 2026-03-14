from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Royal Escape API"
    upstash_redis_rest_url: str
    upstash_redis_rest_token: str

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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Prevents crashing if Vercel has extra variables
    )


settings = Settings()
