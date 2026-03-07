from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from attr import field
from pydantic import BaseModel, ConfigDict


class CanteenMenu(BaseModel):
    name: str
    description: str
    price: int
    food_category: str
    id: Optional[int] = field(default=None)


class VendorExpenseModel(BaseModel):
    vendor: str
    material: str
    amount: float
    payment_mode: str
    date: Optional[datetime] = None
    id: Optional[int] = None

class MenuResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str
    price: int
    id: Optional[int] = None
