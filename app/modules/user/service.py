from datetime import datetime
from bson import ObjectId
from app.core.database import db


from app.core.security import create_access_token
from app.modules.user.otp_service import verify_otp
from app.modules.user.otp_service import send_otp


from fastapi import HTTPException

from app.core.hashing import hash_pin, verify_pin
from app.core.redis import blacklist_token


async def create_user(data: dict):
    now = datetime.utcnow()
    user = {
        **data,
        "is_verified": True,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.users.insert_one(user)
    await db.user_wallets.insert_one(
        {
            "user_id": result.inserted_id,
            "balance": 0,
            "currency": "INR",
            "updated_at": now,
        }
    )
    return result.inserted_id


async def get_user(user_id: str):
    return await db.users.find_one({"_id": ObjectId(user_id)})


async def send_otp_registration(phone: str):
    # Safety check: do NOT send OTP if user already exists
    user = await db.users.find_one({"phone": phone})
    if user:
        raise HTTPException(
            status_code=400,
            detail="User already exists, use PIN login",
        )

    await send_otp(phone)


async def get_dashboard(user_id: str):
    entries = await db.user_entries.count_documents({"user_id": ObjectId(user_id)})
    winnings = await db.user_winnings.aggregate(
        [
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
        ]
    ).to_list(1)

    return {
        "total_entries": entries,
        "total_winnings": winnings[0]["total"] if winnings else 0,
    }


# -------- CHECK USER --------
async def check_user(phone: str):
    user = await db.users.find_one({"phone": phone})
    if user:
        return {"exists": True, "pin_required": user.get("pin_set", False)}
    return {"exists": False, "otp_required": True}


# -------- OTP VERIFY (REGISTRATION STEP) --------
async def verify_otp_registration(phone: str, otp: str):
    await verify_otp(phone, otp)

    user = await db.users.find_one({"phone": phone})
    if not user:
        now = datetime.utcnow()
        result = await db.users.insert_one(
            {
                "phone": phone,
                "pin_set": False,
                "is_verified": True,
                "created_at": now,
                "updated_at": now,
            }
        )
        user_id = str(result.inserted_id)
    else:
        user_id = str(user["_id"])

    # short-lived registration token
    return create_access_token(
        subject=user_id,
        expires_minutes=10,
    )


# -------- SET PIN --------
async def set_pin(user_id: str, pin: str):
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "pin_hash": hash_pin(pin),
                "pin_set": True,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return create_access_token(subject=user_id)


# -------- LOGIN WITH PIN --------
async def login_with_pin(phone: str, pin: str):
    user = await db.users.find_one({"phone": phone})
    if not user or not user.get("pin_set"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_pin(pin, user["pin_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token(subject=str(user["_id"]))


# -------- LOGOUT --------
async def logout(token_payload: dict):
    exp = token_payload["exp"]
    jti = token_payload["jti"]

    ttl = int(exp - datetime.utcnow().timestamp())
    await blacklist_token(jti, ttl)


# ------------------  Register User ----------------


async def register_user_profile(user_id: str, payload):
    update_data = {
        "name": payload.name,
        "pincode": payload.pincode,
        "updated_at": datetime.utcnow(),
    }

    if payload.email:
        update_data["email"] = payload.email

    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
    )

    return {"message": "User profile registered successfully"}
