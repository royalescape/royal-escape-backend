from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException
from app.core.database import db
import random
from app.modules.pots.enums import PotStatus, PotType


# ---------- Admin ----------


async def create_pot(data: dict):
    now = datetime.utcnow()
    pot = {
        **data,
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


async def change_pot_status(pot_id: str, status: PotStatus):
    await db.pots.update_one(
        {"_id": ObjectId(pot_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}},
    )


# ---------- User ----------


async def list_active_pots():
    return await db.pots.find({"status": "active"}).to_list(100)


async def list_pots(status: str | None = None):
    query = {}
    if status:
        query["status"] = status

    return await db.pots.find(query).to_list(100)


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


async def create_pending_entry(
    pot_id: str, user_id: str, quantity: int, reference_id: str
):
    pot = await get_pot(pot_id)

    if pot["status"] != "active":
        raise HTTPException(status_code=400, detail="Pot not active")

    now = datetime.utcnow()

    start_entry = pot["current_entries"] + 1
    entries = []

    for i in range(quantity):
        entries.append(
            {
                "pot_id": ObjectId(pot_id),
                "user_id": ObjectId(user_id),
                "entry_number": start_entry + i,
                "status": "pending",
                "reference_id": reference_id,
                "created_at": now,
                "updated_at": now,
            }
        )

    await db.pot_entries.insert_many(entries)

    return {"entries_created": quantity}


async def get_pots(
    type: PotType,
    status: PotStatus = PotStatus.ACTIVE,
):
    query = {}

    if status:
        query["status"] = status.value

    if type:
        query["type"] = type.value

    # Default behavior: if nothing passed, return only active
    if not status and not type:
        query = {}

    pots_cursor = db.pots.find(query)

    results = []
    async for pot in pots_cursor:
        results.append(
            {
                "id": str(pot["_id"]),
                "icon": pot.get("icon"),
                "name": pot.get("name"),
                "description": pot.get("description"),
                "prize_amount": pot.get("prize_amount"),
                "type": pot.get("type"),
            }
        )

    return results


async def get_all_pots():
    pots_cursor = db.pots.find({})

    results = []

    async for pot in pots_cursor:
        now = datetime.now(timezone.utc)

        closing_date = pot.get("closing_date")

        if closing_date:
            if closing_date.tzinfo is None:
                closing_date = closing_date.replace(tzinfo=timezone.utc)
            delta = closing_date - now
            days_left = max(delta.days, 0)

        total_slots = pot.get("max_entries", 0)
        filled = pot.get("current_entries", 0)
        remaining = max(total_slots - filled, 0)

        results.append(
            {
                "id": str(pot["_id"]),
                "category": pot.get("type"),  # you may separate later
                "type": pot.get("type"),
                "name": pot.get("name"),
                "icon": pot.get("icon"),
                "description": pot.get("description"),
                "prizeValue": f"₹ {pot.get('prize_amount', 0)}",
                "totalSlots": total_slots,
                "filled": filled,
                "remaining": remaining,
                "daysLeft": days_left,
                "endDate": closing_date.isoformat() if closing_date else None,
                "status": pot.get("status"),
                "entryFee": pot.get("entry_price"),
                "maxEntries": pot.get("max_entries"),
                "revenue": filled * pot.get("entry_price", 0),
                "createdDate": pot.get("created_at").isoformat()
                if pot.get("created_at")
                else None,
                "drawDate": closing_date.isoformat() if closing_date else None,
                "winner": str(pot.get("winner_entry_id"))
                if pot.get("winner_entry_id")
                else None,
                "totalEntries": filled,
                "prizeDetails": pot.get("prize_details"),
                "gallery": pot.get("gallery"),
                "faqs": pot.get("faq"),
                "termsAndConditions": pot.get("terms_and_conditions"),
                "color": None,
            }
        )

    return results
