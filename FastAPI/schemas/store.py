from pydantic import BaseModel
from typing import List
from .stock import StockResponse

# --- CREATE MODELS ---
class StoreCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True  # Allows the model to work with SQLAlchemy ORM instances

# --- RESPONSE MODELS ---
class StoreResponse(BaseModel):
    id: int
    name: str
    stock: List[StockResponse]

    class Config:
        orm_mode = True

# --- UPDATE MODELS ---
class StoreUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True