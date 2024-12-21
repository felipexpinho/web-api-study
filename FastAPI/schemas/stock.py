from pydantic import BaseModel, Field

# --- CREATE MODELS ---
class StockCreate(BaseModel):
    store_id: int  # ID of the store (Foreign Key)
    product_id: int  # ID of the product (Foreign Key)
    price: float
    is_available: bool
    category: str

    class Config:
        orm_mode = True  # Allows the model to work with SQLAlchemy ORM instances

# --- RESPONSE MODELS ---
class StockResponse(BaseModel):
    id: int
    store_id: int
    product_id: int
    price: float
    is_available: bool
    category: str
    product_name: str
    store_name: str

    class Config:
        orm_mode = True

# --- UPDATE MODELS ---
class StockUpdate(BaseModel):
    # Field(None) makes the field optional
    price: float = Field(None)
    is_available: bool = Field(None)
    category: str = Field(None)

    class Config:
        orm_mode = True