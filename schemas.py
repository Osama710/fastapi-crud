# schemas.py
from pydantic import BaseModel
from typing import Optional, List


# TO support creation and update APIs
class CreateAndUpdateItem(BaseModel):
    name: str = None
    description: str = None


# TO support list and get APIs
class Item(CreateAndUpdateItem):
    id: int

    class Config:
        orm_mode = True


# To support list Items API
class PaginatedItem(BaseModel):
    limit: int
    offset: int
    data: List[Item]
    message: str

# To support list Items API with message
class ItemWithMessage(BaseModel):
    data: Item
    message: str

# To support message
class MessageOnly(BaseModel):
    message: str