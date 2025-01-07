from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class menu_table_response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    #description: str
    price: int
    id: Optional[int] = None


class customer_order_details(BaseModel):
    order_id: str
    order_details: str
    cart_price: int
    payment_mode: str
    user_name: str
    user_phone: str
    order_date: int
    id: Optional[int] = None


class customer_order_details_response(BaseModel):
    order_details: str
    cart_price: int
    payment_mode: str
    user_phone: str
    order_date: int

