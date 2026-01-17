from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.config import settings
from uuid import uuid4


ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_exp_minutes


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")


def create_access_token(
    subject: str,
    role: str = "user",
    expires_minutes: int | None = None,
):
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.jwt_exp_minutes
    )

    payload = {
        "sub": subject,
        "role": role,
        "jti": str(uuid4()),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
