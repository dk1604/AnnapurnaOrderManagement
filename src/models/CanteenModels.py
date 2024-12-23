from pydantic import BaseModel, ConfigDict


class menu_table_response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    name: str
    description: str
    price: int
