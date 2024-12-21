from pydantic import BaseModel, ConfigDict
from typing import List
from schemas.stock import StockResponse

# --- CREATE MODELS ---
class ProductCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

# --- RESPONSE MODELS ---
class ProductResponse(BaseModel):
    id: int
    name: str
    stock: List[StockResponse]

    model_config = ConfigDict(from_attributes=True)

# --- UPDATE MODELS ---
class ProductUpdate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)