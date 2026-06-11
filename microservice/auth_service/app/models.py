# common/models.py

from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Item(BaseModel):
    item_name: str
    price: float
