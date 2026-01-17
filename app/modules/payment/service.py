from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from app.core.database import db


async def update_payment_status(
    pot_id: str,
    user_id: str,
    status: str,
):
    if status == "confirmed":
        result = await db.pot_entries.update_many(
            {
                "pot_id": ObjectId(pot_id),
                "user_id": ObjectId(user_id),
                "status": "pending",
            },
            {
                "$set": {
                    "status": "confirmed",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        await db.pots.update_one(
            {"_id": ObjectId(pot_id)},
            {"$inc": {"current_entries": result.modified_count}},
        )

        return {"confirmed_entries": result.modified_count}

    elif status == "defaulter":
        result = await db.pot_entries.delete_many(
            {
                "pot_id": ObjectId(pot_id),
                "user_id": ObjectId(user_id),
                "status": "pending",
            }
        )

        return {"deleted_entries": result.deleted_count}

    else:
        raise HTTPException(status_code=400, detail="Invalid payment status")
