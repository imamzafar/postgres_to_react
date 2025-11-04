from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, constr


class ItemBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    description: Optional[str] = None
    quantity: int = 0
    price: condecimal(max_digits=10, decimal_places=2) = 0


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
