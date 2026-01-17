from pydantic import BaseModel


class PaymentUpdateSchema(BaseModel):
    pot_id: str
    status: str  # confirmed | defaulter
