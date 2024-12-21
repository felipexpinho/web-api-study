from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from schemas.store import StoreCreate, StoreResponse, StoreUpdate
from schemas.stock import StockResponse

from models.store import Store
from models.stock import Stock

# ------------ API POST ------------

def create_store_service(store: StoreCreate, db: Session) -> dict:
    # Create the store in the database
    new_store = Store(name=store.name)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    return new_store._asdict()


# ------------ API GET ------------

def get_stores_service(id: Optional[int], name: Optional[str], db: Session):
    query = db.query(Store).options(joinedload(Store.stock).joinedload(Stock.product))  # Join stock and product

    # Filter by store ID or name if provided
    if id:
        query = query.filter(Store.id == id)
    if name:
        query = query.filter(Store.name.ilike(f"%{name}%"))

    stores = query.all()

    if not stores:
        raise ValueError("Store not found")  # Raise a generic exception to signal the controller

    store_responses = [
        StoreResponse(
            id=store.id,
            name=store.name,
            stock=[
                StockResponse(
                    id=stock.id,
                    store_id=stock.store_id,
                    product_id=stock.product_id,
                    price=stock.price,
                    is_available=stock.is_available,
                    category=stock.category,
                    product_name=stock.product.name,
                    store_name=stock.store.name
                )
                for stock in store.stock
            ]
        ).model_dump()  # Ensure the model is serializable
        for store in stores
    ]

    return store_responses


# ------------ API DELETE ------------

def delete_store(store_id: int, db: Session) -> dict:
    # Query the store by ID
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise ValueError("Store not found")
    
    # Delete associated stocks
    for stock in store.stock:
        db.delete(stock)
    
    # Delete the store itself
    db.delete(store)
    db.commit()
    
    # Return the deleted store ID as confirmation
    return {"store_id": store_id}


# ------------ API UPDATE ------------

def update_store(store_id: int, store_update: StoreUpdate, db: Session) -> dict:
    # Query the store by ID
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise ValueError("Store not found")
    
    # Update the store data
    store.name = store_update.name
    db.commit()
    db.refresh(store)
    
    # Return the updated store data
    return store._asdict()