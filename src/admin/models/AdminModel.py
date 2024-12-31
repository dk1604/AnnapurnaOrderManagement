from dataclasses import dataclass
from typing import Optional

from attr import field
from pydantic import BaseModel, ConfigDict


class CanteenMenu(BaseModel):
    name: str
    description: str
    price: int
    food_category: str
    id: Optional[int] = field(default=None)
