from pydantic import BaseModel
from typing import Optional

# book item model
class BookItem(BaseModel):
    title: str
    description: str = None
    price: float


class CreateUser(BaseModel):
    username: str
    password: str
    email: Optional[str]
    first_name: str
    last_name: str
