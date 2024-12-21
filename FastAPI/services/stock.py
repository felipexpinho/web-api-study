from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from schemas.store import StoreCreate, StoreResponse, StoreUpdate
from schemas.stock import StockCreate, StockResponse, StockUpdate

from models.product import Product
from models.store import Store
from models.stock import Stock

# ------------ API POST ------------

def create_stock_service(stock: StockCreate, db: Session) -> dict:
    # Check if the store exists
    store = db.query(Store).filter(Store.id == stock.store_id).first()
    if not store:
        raise ValueError("Store not found")

    # Check if the product exists
    product = db.query(Product).filter(Product.id == stock.product_id).first()
    if not product:
        raise ValueError("Product not found")

    # Create the new stock
    new_stock = Stock(
        store_id=stock.store_id,
        product_id=stock.product_id,
        price=stock.price,
        is_available=stock.is_available,
        category=stock.category
    )

    # Add the new stock to both the product and store stock lists
    store.stock.append(new_stock)
    product.stock.append(new_stock)

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)  # Refresh to get the ID

    return new_stock._asdict()


# ------------ API GET ------------

def get_stocks_service(
    db: Session, 
    product_name: str = None, 
    store_name: str = None, 
    max_price: float = None, 
    is_available: bool = None, 
    category: str = None
) -> list:
    # Initialize the query with necessary joins
    query = db.query(Stock).options(joinedload(Stock.product), joinedload(Stock.store))

    # Apply filters based on provided parameters
    if product_name:
        query = query.filter(Stock.product.has(Product.name.ilike(f"%{product_name}%")))
    if store_name:
        query = query.filter(Stock.store.has(Store.name.ilike(f"%{store_name}%")))
    if max_price is not None:
        query = query.filter(Stock.price <= max_price)
    if is_available is not None:
        query = query.filter(Stock.is_available == is_available)
    if category:
        query = query.filter(Stock.category.ilike(f"%{category}%"))

    # Execute the query and get all results
    stocks = query.all()

    # If no stocks found, raise an exception
    if not stocks:
        raise ValueError("No matching stocks found")
    
    stock_responses = [
        StockResponse(
            id=stock.id,
            store_id=stock.store_id,
            product_id=stock.product_id,
            price=stock.price,
            is_available=stock.is_available,
            category=stock.category,
            product_name=stock.product.name,
            store_name=stock.store.name
        ).model_dump()  # Serialize using model_dump() here
        for stock in stocks
    ]

    return stock_responses


# ------------ API DELETE ------------

def delete_stock_service(stock_id: int, db: Session) -> dict:
    # Query the stock by ID
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    
    if not stock:
        raise ValueError("Stock not found")
    
    # Delete the stock
    db.delete(stock)
    db.commit()

    # Return the deleted product ID as confirmation
    return {"stock_id": stock_id}


# ------------ API UPDATE ------------

def update_store_service(store_id: int, store_update: StoreUpdate, db: Session) -> dict:
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

def update_stock_service(
    db: Session, 
    stock_id: int, 
    stock_update: StockUpdate
) -> Stock:
    # Fetch the stock to update
    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        raise ValueError("Stock not found")

    # Check if any field is provided for update
    updated = False

    if stock_update.price is not None:
        stock.price = stock_update.price
        updated = True
    if stock_update.is_available is not None:
        stock.is_available = stock_update.is_available
        updated = True
    if stock_update.category is not None:
        stock.category = stock_update.category
        updated = True

    # If no fields are provided, raise an error
    if not updated:
        raise ValueError("Nothing to update")

    db.commit()
    db.refresh(stock)  # Refresh the stock to get the updated data
    
    return stock._asdict()