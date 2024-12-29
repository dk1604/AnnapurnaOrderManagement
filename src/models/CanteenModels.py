from typing import Optional

from pydantic import BaseModel, ConfigDict


class menu_table_response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    #description: str
    price: int
    id: Optional[int] = None
