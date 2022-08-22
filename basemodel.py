from pydantic import BaseModel


# book item model
class BookItem(BaseModel):
    title: str
    description: str = None
    price: float
