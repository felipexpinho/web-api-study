from pydantic import BaseModel
from typing import List
from schemas.stock import StockResponse

# --- CREATE MODELS ---
class ProductCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True  # Allows the model to work with SQLAlchemy ORM instances

# --- RESPONSE MODELS ---
class ProductResponse(BaseModel):
    id: int
    name: str
    stock: List[StockResponse]

    class Config:
        orm_mode = True

# --- UPDATE MODELS ---
class ProductUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True