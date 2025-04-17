from pydantic import BaseModel


class PricingBase(BaseModel):
    delivery_type: str
    distance: float
    weight: float = 0
