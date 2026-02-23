from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.modules.pots.schemas import (
    PotCreateSchema,
    PotUpdateSchema,
    PotEntrySchema,
    PotFullResponse,
    PotPublicResponse,
)
from fastapi import Query
from app.modules.pots.schemas import CreatePotEntrySchema


from app.modules.pots.service import (
    create_pot,
    update_pot,
    change_pot_status,
    get_pot,
    enter_pot,
    get_user_entries,
    declare_winner,
    create_pending_entry,
    get_all_pots,
    get_pots,
)

from app.api.deps import require_admin
from app.utils.mongo import serialize_mongo_list, serialize_mongo

from typing import Optional
from app.modules.pots.enums import PotStatus, PotType


router = APIRouter(prefix="/pots", tags=["pots"])


# ---------- User APIs ----------


@router.get("/", response_model=list[PotPublicResponse])
async def list_pots(
    status: Optional[PotStatus] = Query(None),
    type: Optional[PotType] = Query(None),
):
    return await get_pots(
        type=type,
        status=status,
    )


@router.get("/all", response_model=list[PotFullResponse])
async def list_all_pots():
    return await get_all_pots()


@router.get("/{pot_id}")
async def view_pot(pot_id: str):
    pot = await get_pot(pot_id)
    return serialize_mongo(pot)


@router.post("/{pot_id}/enter")
async def buy_entries(
    pot_id: str, payload: PotEntrySchema, user=Depends(get_current_user)
):
    await enter_pot(pot_id, str(user["_id"]), payload.quantity)
    return {"message": "Entries created"}


@router.get("/me/entries")
async def my_entries(user=Depends(get_current_user)):
    entries = await get_user_entries(str(user["_id"]))
    return serialize_mongo_list(entries)


# ---------- Admin APIs ----------


@router.post("/admin")
async def admin_create_pot(payload: PotCreateSchema, admin=Depends(require_admin)):
    pot_id = await create_pot(payload.model_dump())
    return {"pot_id": str(pot_id)}


@router.put("/admin/{pot_id}")
async def admin_update_pot(
    pot_id: str, payload: PotUpdateSchema, admin=Depends(require_admin)
):
    await update_pot(pot_id, payload.model_dump(exclude_unset=True))
    return {"message": "Pot updated"}


@router.patch("/admin/{pot_id}/status")
async def admin_change_status(pot_id: str, status: str, admin=Depends(require_admin)):
    await change_pot_status(pot_id, status)
    return {"message": "Status updated"}


@router.post("/admin/{pot_id}/declare-winner")
async def admin_declare_winner(pot_id: str, admin=Depends(require_admin)):
    return await declare_winner(pot_id)


@router.post("/{pot_id}/entry")
async def create_entry(
    pot_id: str,
    payload: CreatePotEntrySchema,
    current=Depends(get_current_user),
):
    user, _ = current
    return await create_pending_entry(
        pot_id, str(user["_id"]), payload.quantity, payload.reference_id
    )
