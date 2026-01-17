from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from app.core.database import db
import random


# ---------- Admin ----------


async def create_pot(data: dict):
    now = datetime.utcnow()
    pot = {
        **data,
        "type": "lucky_draw",
        "status": "draft",
        "current_entries": 0,
        "winner_entry_id": None,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.pots.insert_one(pot)
    return result.inserted_id


async def update_pot(pot_id: str, data: dict):
    await db.pots.update_one(
        {"_id": ObjectId(pot_id)}, {"$set": {**data, "updated_at": datetime.utcnow()}}
    )


async def change_pot_status(pot_id: str, status: str):
    await db.pots.update_one(
        {"_id": ObjectId(pot_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}},
    )


# ---------- User ----------


async def list_active_pots():
    return await db.pots.find({"status": "active"}).to_list(100)


async def get_pot(pot_id: str):
    pot = await db.pots.find_one({"_id": ObjectId(pot_id)})
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    return pot


async def enter_pot(pot_id: str, user_id: str, quantity: int):
    pot = await get_pot(pot_id)

    if pot["status"] != "active":
        raise HTTPException(status_code=400, detail="Pot not active")

    remaining = pot["max_entries"] - pot["current_entries"]
    if quantity > remaining:
        raise HTTPException(status_code=400, detail="Not enough entries")

    start_entry = pot["current_entries"] + 1
    now = datetime.utcnow()

    entries = []
    for i in range(quantity):
        entries.append(
            {
                "pot_id": ObjectId(pot_id),
                "user_id": ObjectId(user_id),
                "entry_number": start_entry + i,
                "created_at": now,
            }
        )

    await db.pot_entries.insert_many(entries)
    await db.pots.update_one(
        {"_id": ObjectId(pot_id)}, {"$inc": {"current_entries": quantity}}
    )


async def get_user_entries(user_id: str):
    return await db.pot_entries.find({"user_id": ObjectId(user_id)}).to_list(100)


##### ADmin API ##########


async def declare_winner(pot_id: str):
    pot = await db.pots.find_one({"_id": ObjectId(pot_id)})

    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")

    if pot["status"] != "closed":
        raise HTTPException(status_code=400, detail="Pot must be closed first")

    total_entries = await db.pot_entries.count_documents({"pot_id": ObjectId(pot_id)})

    if total_entries == 0:
        raise HTTPException(status_code=400, detail="No entries in pot")

    # Secure randomness
    random_index = random.SystemRandom().randint(0, total_entries - 1)

    winner_entry = (
        await db.pot_entries.find({"pot_id": ObjectId(pot_id)})
        .skip(random_index)
        .limit(1)
        .to_list(1)
    )[0]

    await db.pot_winners.insert_one(
        {
            "pot_id": ObjectId(pot_id),
            "user_id": winner_entry["user_id"],
            "entry_id": winner_entry["_id"],
            "declared_at": datetime.utcnow(),
        }
    )

    await db.pots.update_one(
        {"_id": ObjectId(pot_id)},
        {
            "$set": {
                "status": "winner_declared",
                "winner_entry_id": winner_entry["_id"],
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return {
        "winner_user_id": str(winner_entry["user_id"]),
        "entry_number": winner_entry["entry_number"],
    }
