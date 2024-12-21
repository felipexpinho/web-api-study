from pydantic import BaseModel, ConfigDict
from typing import List
from .stock import StockResponse

# --- CREATE MODELS ---
class StoreCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

# --- RESPONSE MODELS ---
class StoreResponse(BaseModel):
    id: int
    name: str
    stock: List[StockResponse]

    model_config = ConfigDict(from_attributes=True)

# --- UPDATE MODELS ---
class StoreUpdate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)