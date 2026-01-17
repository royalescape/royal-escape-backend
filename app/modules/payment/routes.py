from fastapi import APIRouter
from app.modules.payment.schemas import PaymentUpdateSchema
from app.modules.payment.service import update_payment_status
from app.api.deps import get_current_user
from fastapi import Depends


router = APIRouter(prefix="/payment", tags=["payment"])


@router.get("/scanner-image")
async def get_scanner_image():
    return {"scanner_image_url": "https://your-cdn.com/upi_scanner.png"}


@router.post("/update-status")
async def update_status(
    payload: PaymentUpdateSchema,
    current=Depends(get_current_user),
):
    user, _ = current
    return await update_payment_status(
        payload.pot_id,
        str(user["_id"]),
        payload.status,
    )
